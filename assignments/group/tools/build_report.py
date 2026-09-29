#!/usr/bin/env python3
"""Build the PDF of the project document: workspace/report/project-document/NN-*.md, in file order.

Reuses the report builder of the 2110628 repository (assignments/group/tools/build_pdf.py: markdown -> HTML -> PDF in
headless Chromium, TH Sarabun, table and figure captions, contents with page numbers, landscape pages for wide
figures). That repository is found as $REQ_REPO, else the tree this repository is nested in
(<2110628>/workspace/2110521_Software_Architecture), else a sibling folder 2110628_Requirement. Only the cover and the
running header are replaced here: they carry this course, group SE 101 and the version.

Usage (from the repository root):
    python3 assignments/group/tools/build_report.py                          # 2.0 draft 5
    python3 assignments/group/tools/build_report.py --version "2.0" --status final
Output: assignments/group/workspace/report/build/seats_project_document_v<version>.pdf (git-ignored)
"""
import argparse
import base64
import html
import os
import re
import sys
from pathlib import Path

GROUP = Path(__file__).resolve().parent.parent
REPO = GROUP.parent.parent
DOC = GROUP / "workspace" / "report" / "project-document"
OUT = GROUP / "workspace" / "report" / "build"

TITLE = "Seating & Event Availability Tracking System (SEATS)"
FORMER_NAME = "named Concert Table Reservation System (CTRS) in Deliverables #1 and #2"
SUBTITLE = "Project Description, ADRs and Microservice Design"
COURSE = "2110521 Software Architecture"
COURSE_TH = "2110521 วิศวกรรมสถาปัตยกรรมซอฟต์แวร์"
GROUP_NAME = "SE 101"
MEMBERS = [("6772012221", "Chetsada Winaikoson"), ("6872081621", "Waris Natirutthakorn"),
           ("6870083521", "Natcha Thawinpipat"), ("6970267821", "Watayut Aiamanan")]
# KI-13 / CH-21: the course belongs to the Department of Computer Engineering (syllabus item 4)
AFFILIATION = ("This document is an integral component of the subject 2110521 Software Architecture, Department of "
               "Computer Engineering, Faculty of Engineering, Chulalongkorn University, Semester 1 of the academic year 2026.")


def find_req_repo() -> Path:
    for c in (os.environ.get("REQ_REPO"), REPO.parent.parent, REPO.parent / "2110628_Requirement"):
        if c and (Path(c) / "assignments" / "group" / "tools" / "build_pdf.py").is_file():
            return Path(c).resolve()
    raise SystemExit("2110628 repository not found: set REQ_REPO=<path to 2110628_Requirement>")


sys.path.insert(0, str(find_req_repo() / "assignments" / "group" / "tools"))
import build_pdf  # noqa: E402  (report builder of the 2110628 repository)


def make_cover(label: str, date: str, status: str):
    def cover(_version, _parts):
        members = "".join(f'<tr><td>{html.escape(n)}</td><td class="id">Student ID {i}</td></tr>' for i, n in MEMBERS)
        return f"""<section class="cover">
<img class="emblem" src="{build_pdf.LOGO_EMBLEM.as_uri()}" alt="Chulalongkorn University">
<div class="title">{html.escape(TITLE)}</div>
<div class="subtitle">{html.escape(SUBTITLE)}<br>{html.escape(COURSE_TH)} ({html.escape(COURSE)})<br><small>{html.escape(FORMER_NAME)}</small></div>
<div class="members-title">Group Members</div>
<div class="group">{html.escape(GROUP_NAME)}</div>
<table>{members}</table>
<div class="version">Version {html.escape(label)} · {html.escape(date)} · {html.escape(status)}<br>{html.escape(AFFILIATION)}</div>
</section>"""
    return cover


def running_header() -> str:
    def uri(p: Path) -> str:
        return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
    return (f"<div style='width:100%;box-sizing:border-box;padding:6mm 18mm 0;font-family:Arial,sans-serif;-webkit-print-color-adjust:exact;'>"
            f"<div style='display:flex;align-items:center;justify-content:space-between;'>"
            f"<div style='display:flex;align-items:center;gap:5px;'><img src='{uri(build_pdf.LOGO_GEAR)}' style='height:22px'>"
            f"<img src='{uri(build_pdf.LOGO_STRIP)}' style='height:19px'></div>"
            f"<div style='text-align:right;font-size:8.5px;color:#374151;line-height:1.5;'>{html.escape(COURSE)}<br>"
            f"Group {html.escape(GROUP_NAME)} · SEATS project document<br><span style='color:#6b7280'><span class='pageNumber'></span> / <span class='totalPages'></span></span></div>"
            f"</div><div style='height:2px;background:#8b1a1a;margin-top:3px;-webkit-print-color-adjust:exact;'></div></div>")


LIST = re.compile(r"^(\s*)([-*]|\d+\.)\s")


def normalize(text: str) -> str:
    """Markdown as GitHub reads it -> markdown as python-markdown needs it, without changing the words:
    a blank line before every list and after a bold label line (**Context**, **Precondition:**), a bold
    label that follows a text line starts its own paragraph, nested list items indented by 4 spaces per
    level, and em-only lines that are not table or figure captions ({step names}, "Alternative Flows:")
    made bold so that the builder does not style them as figure captions."""
    out, stack, in_list, fenced = [], [], False, False
    for line in text.split("\n"):
        if line.startswith("```"):
            fenced = not fenced
        if fenced or line.startswith("```"):
            out.append(line); continue
        s = line.strip()
        m = re.fullmatch(r"\*(?!\*)(?!Table |Figure )(.+?)\*", s)
        if m and not line.startswith(" "):
            line = s = f"**{m.group(1)}**"
        prev = out[-1] if out else ""
        lm = LIST.match(line)
        if lm:
            i = len(lm.group(1))
            if not in_list:
                stack = []
            while stack and stack[-1] > i:
                stack.pop()
            if not stack or stack[-1] < i:
                stack.append(i)
            line = " " * (4 * (len(stack) - 1)) + line.lstrip()
            if prev.strip() and not LIST.match(prev):   # after a text line, even inside a list item
                out.append("")
            in_list = True
        elif not s:
            pass
        elif line.startswith(" ") and in_list:
            i = len(line) - len(line.lstrip())
            line = " " * (4 * sum(1 for x in stack if x < i)) + line.lstrip()
        else:
            if (in_list or s.startswith("**")) and prev.strip() and not prev.lstrip().startswith("|"):
                out.append("")
            in_list, stack = False, []
        out.append(line)
        if not lm and re.fullmatch(r"\*\*[^*]+\*\*", s):
            out.append("")
    return "\n".join(out)


_render_part = build_pdf.render_part


def render_part(md_path: Path):
    """The 2110628 renderer on a normalized copy next to the source (so relative image paths still resolve)."""
    tmp = md_path.with_name(f".render-{md_path.name}")
    tmp.write_text(normalize(md_path.read_text(encoding="utf-8")), encoding="utf-8")
    try:
        return _render_part(tmp)
    finally:
        tmp.unlink()


class _Markdown(build_pdf.markdown.Markdown):
    """Keep the number of the first item of an ordered list: flow steps resume at 3 after a step-name line."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("lazy_ol", False)
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", default="2.0 draft 5", help="version label on the cover (default: %(default)s)")
    ap.add_argument("--date", default="29 September 2026")
    ap.add_argument("--status", default="draft for review by the group")
    a = ap.parse_args()
    parts = sorted(p for p in DOC.glob("[0-9][0-9]-*.md"))
    build_pdf.COURSE, build_pdf.DRAFT = COURSE, False
    build_pdf.cover = make_cover(a.version, a.date, a.status)
    build_pdf.running_header = running_header
    build_pdf.render_part = render_part
    # the 2110628 CSS centres any paragraph whose only element is an <em> as a figure caption, which also catches a
    # sentence with one italic phrase ("marked *(Increment 2)*"): keep that style for real figure captions only
    # ADRs (section 4): one key-value table per ADR, each ADR on a new page
    build_pdf.CSS += ("\nh2[id*='adr-'] { break-before: page; page-break-before: always; }"
                      "\ntable.adr { border: 1pt solid #4b5563; font-size: 12pt; line-height: 1.35; margin: 4pt 0 12pt; }"
                      "\ntable.adr td { border: 0.6pt solid #6b7280; padding: 5pt 8pt 6pt; vertical-align: top; }"
                      "\ntable.adr td.k { width: 17%; font-weight: bold; color: #0b2a4a; background: #eef2f7; }"
                      "\ntable.adr tr { page-break-inside: auto; break-inside: auto; }"
                      "\ntable.adr p { margin: 0 0 4pt; text-align: left; }"
                      "\ntable.adr ul, table.adr ol { margin: 0 0 4pt; padding-left: 18pt; }"
                      "\n.keep:has(> table.adr) { break-inside: auto; page-break-inside: auto; }")
    build_pdf.CSS += ("\np > em:only-child { display: inline; text-align: inherit; font-size: inherit; margin-top: 0; }"
                      "\np[id^='fig-'] > em:only-child { display: block; text-align: center; font-size: 13pt; margin-top: -2pt; }")
    build_pdf.markdown.Markdown = _Markdown
    out = OUT / f"seats_project_document_v{re.sub(r'[^0-9A-Za-z.]+', '-', a.version).strip('-')}.pdf"
    build_pdf.build(parts, "v" + a.version, out)
