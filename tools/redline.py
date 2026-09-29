#!/usr/bin/env python3
"""Redline of the project document between two versions: what was deleted, inserted and changed, paragraph by paragraph.

Compares the markdown sources of assignments/group/workspace/report/project-document/ at a git revision (a tag such as
doc-v1.1-submitted) with another revision or with the working tree, and writes one HTML page: a summary per file, then
every changed paragraph under its section heading, with deleted words struck through in red and inserted words
underlined in green. Unchanged paragraphs are folded. The markdown source is shown as text (tables and lists stay
readable and a change inside a table cell is not lost to rendering).

Usage (from the repository root):
    python3 tools/redline.py                                       # doc-v1.1-submitted -> working tree
    python3 tools/redline.py --base doc-v1.1-submitted --head doc-v2.0-draft1
    python3 tools/redline.py --pdf                                 # also write a PDF (WeasyPrint)
Output: assignments/group/workspace/report/build/redline_<base>_to_<head>.html (.pdf)
"""
import argparse
import difflib
import html
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOC = "assignments/group/workspace/report/project-document"
OUT = REPO / "assignments/group/workspace/report/build"
TOKEN = re.compile(r"\s+|\w+|[^\w\s]", re.U)


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True, check=True).stdout


def files_at(rev: str | None) -> dict[str, str]:
    """{file name: text} of the document's markdown files at a revision, or in the working tree when rev is None."""
    if rev is None:
        return {p.name: p.read_text(encoding="utf-8") for p in sorted((REPO / DOC).glob("*.md"))}
    names = [n for n in git("ls-tree", "--name-only", f"{rev}:{DOC}").split() if n.endswith(".md")]
    return {n: git("show", f"{rev}:{DOC}/{n}") for n in names}


def blocks(text: str) -> list[str]:
    """Paragraph-level blocks: split on blank lines, keeping fenced code blocks whole."""
    out, cur, fenced = [], [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            fenced = not fenced
        if not line.strip() and not fenced:
            if cur:
                out.append("\n".join(cur)); cur = []
            continue
        cur.append(line)
    if cur:
        out.append("\n".join(cur))
    return out


def word_diff(a: str, b: str) -> tuple[str, int, int]:
    """HTML of b against a with <del>/<ins> runs; returns (html, words deleted, words inserted)."""
    ta, tb = TOKEN.findall(a), TOKEN.findall(b)
    sm = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
    parts, dn, inn = [], 0, 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            parts.append(html.escape("".join(ta[i1:i2])))
            continue
        if i2 > i1:
            parts.append(f"<del>{html.escape(''.join(ta[i1:i2]))}</del>")
            dn += sum(1 for t in ta[i1:i2] if t.strip())
        if j2 > j1:
            parts.append(f"<ins>{html.escape(''.join(tb[j1:j2]))}</ins>")
            inn += sum(1 for t in tb[j1:j2] if t.strip())
    return "".join(parts), dn, inn


def heading_of(block: str) -> str | None:
    m = re.match(r"(#{1,4}) (.+)", block)
    return m.group(2) if m else None


def diff_file(a: str, b: str):
    """Change groups of one file: [(section heading, html)], plus counters."""
    ba, bb = blocks(a), blocks(b)
    sm = difflib.SequenceMatcher(None, ba, bb, autojunk=False)
    groups, stats = [], {"changed": 0, "inserted": 0, "deleted": 0, "unchanged": 0, "words_del": 0, "words_ins": 0}
    section = None
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        for blk in (bb[j1:j2] if op != "delete" else ba[i1:i2]):
            section = heading_of(blk) or section
        if op == "equal":
            stats["unchanged"] += i2 - i1
            continue
        old, new = "\n\n".join(ba[i1:i2]), "\n\n".join(bb[j1:j2])
        body, dn, inn = word_diff(old, new)
        stats["words_del"] += dn; stats["words_ins"] += inn
        kind = {"replace": "changed", "insert": "inserted", "delete": "deleted"}[op]
        stats[kind] += max(i2 - i1, j2 - j1)
        groups.append((section, kind, body))
    return groups, stats


CSS = """
body { font-family: "Sarabun", "TH Sarabun New", "Noto Sans Thai", system-ui, sans-serif; margin: 24px auto; max-width: 1000px;
       padding: 0 16px; color: #1f2933; background: #fff; }
h1 { font-size: 22px; margin: 0 0 4px; } h2 { font-size: 18px; margin: 28px 0 8px; border-bottom: 2px solid #c9a227; padding-bottom: 4px; }
p.meta { color: #52606d; margin: 0 0 16px; }
table.sum { border-collapse: collapse; font-size: 13px; margin: 8px 0 16px; }
table.sum th, table.sum td { border: 1px solid #cbd2d9; padding: 4px 8px; text-align: right; }
table.sum th:first-child, table.sum td:first-child { text-align: left; }
div.chg { border-left: 4px solid #9aa5b1; margin: 10px 0; padding: 6px 10px; background: #f8f9fa;
          white-space: pre-wrap; font-size: 13px; line-height: 1.45; font-family: "Sarabun", system-ui, sans-serif; }
div.chg.inserted { border-left-color: #2f855a; } div.chg.deleted { border-left-color: #c53030; } div.chg.changed { border-left-color: #b7791f; }
div.where { font-size: 12px; color: #52606d; margin-top: 14px; }
del { color: #c53030; background: #fde8e8; text-decoration: line-through; }
ins { color: #22543d; background: #e3f6ea; text-decoration: underline; }
span.kind { font-size: 11px; text-transform: uppercase; letter-spacing: .04em; color: #52606d; }
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="doc-v1.1-submitted", help="git revision of the old version (default: %(default)s)")
    ap.add_argument("--head", default=None, help="git revision of the new version (default: the working tree)")
    ap.add_argument("--pdf", action="store_true", help="also write a PDF next to the HTML")
    a = ap.parse_args()
    old, new = files_at(a.base), files_at(a.head)
    head_name = a.head or "working-tree"
    rows, sections = [], []
    for name in sorted(set(old) | set(new)):
        groups, st = diff_file(old.get(name, ""), new.get(name, ""))
        status = "new file" if name not in old else "removed" if name not in new else ("unchanged" if not groups else "")
        rows.append(f"<tr><td>{html.escape(name)} {status}</td><td>{st['changed']}</td><td>{st['inserted']}</td>"
                    f"<td>{st['deleted']}</td><td>{st['unchanged']}</td><td>{st['words_del']}</td><td>{st['words_ins']}</td></tr>")
        if groups:
            items = "".join(f"<div class='where'>§ {html.escape(sec or '(start of file)')} <span class='kind'>{kind}</span></div>"
                            f"<div class='chg {kind}'>{body}</div>" for sec, kind, body in groups)
            sections.append(f"<h2>{html.escape(name)}</h2>{items}")
    page = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>Redline {html.escape(a.base)} to {html.escape(head_name)}</title><style>{CSS}</style></head><body>"
            f"<h1>Project document redline</h1><p class='meta'>From <b>{html.escape(a.base)}</b> to <b>{html.escape(head_name)}</b>. "
            f"Deleted text is <del>struck through</del>, inserted text is <ins>underlined</ins>; unchanged paragraphs are folded. "
            f"Each change sits under the nearest section heading of the new version. Why each change was made is in the Change Log "
            f"of the document (00-document-control.md).</p>"
            f"<table class='sum'><tr><th>File</th><th>Changed</th><th>Inserted</th><th>Deleted</th><th>Unchanged</th>"
            f"<th>Words deleted</th><th>Words inserted</th></tr>{''.join(rows)}</table>"
            f"<p class='meta'>Counts are paragraph blocks (a table or a list counts as one block when it has no blank line).</p>"
            f"{''.join(sections)}</body></html>")
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"redline_{a.base}_to_{head_name}.html"
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out.relative_to(REPO)}")
    if a.pdf:
        from weasyprint import HTML
        HTML(string=page).write_pdf(out.with_suffix(".pdf"))
        print(f"wrote {out.with_suffix('.pdf').relative_to(REPO)}")


if __name__ == "__main__":
    main()
