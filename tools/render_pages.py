#!/usr/bin/env python3
"""Render the pages of a PDF to PNG, the way the transcriptions of this repository embed them.

One image per page at 110 DPI, named page-NN.png (page-NNN.png when the document has 100 or more pages), written to
png/ next to the PDF unless an output folder is given. The png/ folders are git-ignored; run `--all` after a fresh
clone so the page images embedded in the transcriptions (md/<name>.md, links ../png/page-NN.png) render.

Usage (from the repository root):
    python3 tools/render_pages.py <file.pdf> [<file.pdf> ...]     # each into <pdf folder>/png/
    python3 tools/render_pages.py <file.pdf> --out <folder>        # one PDF into a chosen folder
    python3 tools/render_pages.py --all                            # every transcribed PDF (see ALL_*)
"""
import argparse
from pathlib import Path

import pymupdf

REPO = Path(__file__).resolve().parent.parent
DPI = 110
ALL_DIRS = ["materials", "assignments/group/workspace/received"]            # every PDF here -> png/ next to it
ALL_PAIRS = [  # handed-in PDFs whose transcription lives elsewhere: (PDF, png folder next to the transcription)
    ("assignments/group/deliverables/report/Deliverable-1.pdf", "assignments/group/workspace/report/deliverable-1/png"),
]


def render(pdf: Path, out: Path | None = None) -> None:
    out = out or pdf.parent / "png"
    out.mkdir(parents=True, exist_ok=True)
    with pymupdf.open(pdf) as doc:
        width = 3 if doc.page_count >= 100 else 2
        for i, page in enumerate(doc, 1):
            page.get_pixmap(dpi=DPI).save(out / f"page-{i:0{width}d}.png")
        print(f"{doc.page_count:4d} pages  {out.relative_to(REPO) if out.is_relative_to(REPO) else out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdfs", nargs="*", type=Path)
    ap.add_argument("--out", type=Path, help="output folder (only with one PDF)")
    ap.add_argument("--all", action="store_true", help="render every transcribed PDF of the repository")
    a = ap.parse_args()
    if a.out and len(a.pdfs) != 1:
        ap.error("--out takes exactly one PDF")
    if a.all:
        for d in ALL_DIRS:
            for pdf in sorted((REPO / d).rglob("*.pdf")):
                render(pdf)
        for pdf, out in ALL_PAIRS:
            render(REPO / pdf, REPO / out)
    for pdf in a.pdfs:
        render(pdf.resolve(), a.out.resolve() if a.out else None)
    if not a.all and not a.pdfs:
        ap.print_help()
