#!/usr/bin/env python3
"""Build the PDF of the project document: workspace/report/project-document/NN-*.md, in file order.

Reuses the report builder of the 2110628 repository (assignments/group/tools/build_pdf.py: markdown -> HTML -> PDF in
headless Chromium, TH Sarabun, table and figure captions, contents with page numbers, landscape pages for wide
figures). That repository is found as $REQ_REPO, else the tree this repository is nested in
(<2110628>/workspace/2110521_Software_Architecture), else a sibling folder 2110628_Requirement. Only the cover and the
running header are replaced here: they carry this course, group SE 101 and the version.

Usage (from the repository root):
    python3 assignments/group/tools/build_report.py                          # 2.0 draft 27
    python3 assignments/group/tools/build_report.py --changelog              # the separate change-log document
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
SUBTITLE = "Project Description, ADRs, Microservice Design and API Specification"
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
PORTRAIT_FIGURES = ["use-case-diagram.png"]    # readable at portrait width; landscape would strand the headings before it


def normalize(text: str) -> str:
    """Markdown as GitHub reads it -> markdown as python-markdown needs it, without changing the words:
    a blank line before every list and after a bold label line (**Context**, **Precondition:**), a bold
    label that follows a text line starts its own paragraph, nested list items indented by 4 spaces per
    level, and em-only lines that are not table or figure captions ({step names}, "Alternative Flows:")
    made bold so that the builder does not style them as figure captions."""
    for name in PORTRAIT_FIGURES:
        text = re.sub(r"(!\[[^\]]*\]\([^)]*" + re.escape(name) + r"\))(?!\{)", r'\1{: data-portrait="1" }', text)
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
    """The 2110628 renderer on a normalized copy next to the source (so relative image paths still resolve); a heading
    right before a wide figure goes onto the figure's landscape page instead of staying alone on the portrait page."""
    tmp = md_path.with_name(f".render-{md_path.name}")
    tmp.write_text(normalize(md_path.read_text(encoding="utf-8")), encoding="utf-8")
    try:
        body, toc = _render_part(tmp)
    finally:
        tmp.unlink()
    # only the one heading right before the figure: its content may not cross into another heading
    body = re.sub(r'(<h([2-4])\b[^>]*>(?:(?!</?h\d).)*</h\2>)\s*<div class="landscape">', r'<div class="landscape with-heading">\1',
                  body, flags=re.S)
    return body, toc


class _Markdown(build_pdf.markdown.Markdown):
    """Keep the number of the first item of an ordered list: flow steps resume at 3 after a step-name line."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("lazy_ol", False)
        super().__init__(*args, **kwargs)


def check_use_cases(path: Path) -> None:
    """Every described use case keeps its Basic Flow with the steps numbered 1..n without a gap. Draft 21 lost the
    Preconditions, the Postconditions and steps 1 to 11 of UC-01 unnoticed for five drafts (CH-57): refuse to build."""
    text = path.read_text(encoding="utf-8")
    for m in re.finditer(r"^### 2\.2\.\d+ (UC-\d+ [^\n]+)", text, re.M):
        nxt = text.find("\n### ", m.end())
        sec = text[m.end(): nxt if nxt > 0 else len(text)]
        bf = sec.find("#### Basic Flow")
        if bf < 0:
            raise SystemExit(f"{m.group(1)}: no Basic Flow")
        end = min(x for x in (sec.find("#### Subflows", bf), sec.find("#### Alternative Flows", bf), len(sec)) if x > 0)
        nums = [int(n) for n in re.findall(r"^(\d+)\. ", sec[bf:end], re.M)]
        if not nums or nums != list(range(1, len(nums) + 1)):
            raise SystemExit(f"{m.group(1)}: the basic flow steps are {nums}, not 1..n")
        for k in ("#### Preconditions", "#### Postconditions", "#### Relationships"):
            if k not in sec:
                raise SystemExit(f"{m.group(1)}: no {k[5:]}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", default="2.0 draft 27", help="version label on the cover (default: %(default)s)")
    ap.add_argument("--date", default="29 September 2026")
    ap.add_argument("--status", default="draft for review by the group")
    ap.add_argument("--changelog", action="store_true", help="build the separate change-log document (project-document/change-log/) instead")
    a = ap.parse_args()
    if a.changelog:
        SUBTITLE = "Change Log of the Project Document"
        parts = sorted(p for p in (DOC / "change-log").glob("[0-9][0-9]-*.md"))
    else:
        parts = sorted(p for p in DOC.glob("[0-9][0-9]-*.md"))
        check_use_cases(DOC / "02-use-cases.md")
    build_pdf.COURSE, build_pdf.DRAFT = COURSE, False
    build_pdf.cover = make_cover(a.version, a.date, a.status)
    build_pdf.running_header = running_header
    build_pdf.render_part = render_part
    # the 2110628 CSS centres any paragraph whose only element is an <em> as a figure caption, which also catches a
    # sentence with one italic phrase ("marked *(Increment 2)*"): keep that style for real figure captions only
    # ADRs (section 4): one key-value table per ADR, each ADR on a new page
    # a heading never ends a page; a heading moved onto a landscape page leaves room for itself above the figure
    build_pdf.CSS += ("\nh1, h2, h3, h4, h5 { break-after: avoid; page-break-after: avoid; }"
                      "\n.landscape.with-heading > h2, .landscape.with-heading > h3 { margin-top: 0; }"
                      "\n.landscape.with-heading img { max-height: 136mm; }"
                      "\n.toc li { margin: 1pt 0; } .toc ul { margin-top: 0; margin-bottom: 0; } .toc > .toc { margin-bottom: 7pt; }")   # the contents fit two pages
    # use case traceability (Appendix A.2): narrow columns for steps, callers and requirement IDs; Collaborations takes the rest
    build_pdf.CSS += ("\ndiv.trace table th:nth-child(1) { width: 10%; } div.trace table th:nth-child(2) { width: 10%; }"
                      "\ndiv.trace table th:nth-child(3) { width: 24%; } div.trace table th:nth-child(5) { width: 18%; }"
                      "\ndiv.trace table th:nth-child(6) { width: 11%; }")
    # operations-by-use-case matrix (Appendix A.1): narrow use case columns, operation names never wrap
    build_pdf.CSS += ("\ndiv.matrix table { font-size: 8.5pt; line-height: 1.2; } div.matrix table th, div.matrix table td { padding: 1.5pt 3pt; }"
                      "\ndiv.matrix table th:nth-child(1) { width: 10%; } div.matrix table th:nth-child(2) { width: 22%; }"
                      "\ndiv.matrix table td:nth-child(2) { white-space: nowrap; } div.matrix table th:nth-child(n+3):nth-child(-n+11) { width: 7%; }")
    # use cases (2.2.1 .. 2.2.4) each start on a new page, as the ADRs do
    build_pdf.CSS += "\nh3[id*='-uc-0'] { break-before: page; page-break-before: always; }"
    build_pdf.CSS += "\nh3[id*='-uc-01'] { break-before: auto; page-break-before: auto; }"   # UC-01 follows the 2.2 introduction; the others start a page
    build_pdf.CSS += ("\nh2[id*='adr-'] { break-before: page; page-break-before: always; }"
                      "\ntable.adr { border: 1pt solid #4b5563; font-size: 12pt; line-height: 1.35; margin: 4pt 0 12pt; }"
                      "\ntable.adr td { border: 0.6pt solid #6b7280; padding: 5pt 8pt 6pt; vertical-align: top; }"
                      "\ntable.adr td.k { width: 17%; font-weight: bold; color: #0b2a4a; background: #eef2f7; }"
                      "\ntable.adr tr { page-break-inside: auto; break-inside: auto; }"
                      "\ntable.adr p { margin: 0 0 4pt; text-align: left; }"
                      "\ntable.adr ul, table.adr ol { margin: 0 0 4pt; padding-left: 18pt; }"
                      "\n.keep:has(> table.adr) { break-inside: auto; page-break-inside: auto; }")
    # the use case diagram is taller than wide: cap its height so that it stays on the page of the Section 2 headings
    build_pdf.CSS += "\nimg[src*='use-case-diagram'] { max-height: 190mm; width: auto; }"
    build_pdf.CSS += ("\np > em:only-child { display: inline; text-align: inherit; font-size: inherit; margin-top: 0; }"
                      "\np[id^='fig-'] > em:only-child { display: block; text-align: center; font-size: 13pt; margin-top: -2pt; }")
    # 2026-09-30: the base rule sets code at a fixed 11pt, which towers over the 12pt TH Sarabun of a table cell;
    # size it relative to the text around it instead (about 9pt in a table, 11pt in body text)
    build_pdf.CSS += "\ncode { font-size: 0.75em; }"
    # draft 25: the tables of 6.4: div.api = operation | gRPC method | request | response; div.api5 = the same with a service column;
    # div.msg = service | message | fields; div.routes = service | route | gRPC method | web app | roles | request body | response
    build_pdf.CSS += ("\ndiv.api table, div.api5 table, div.msg table, div.routes table { font-size: 11pt; line-height: 1.3; }"
                      "\ndiv.api th, div.api td, div.api5 th, div.api5 td, div.msg th, div.msg td, div.routes th, div.routes td { padding: 3pt 4pt; }"
                      "\ndiv.api table th:nth-child(1) { width: 19%; } div.api table th:nth-child(2) { width: 18%; } div.api table th:nth-child(3) { width: 34%; }"
                      "\ndiv.api5 table th:nth-child(1) { width: 12%; } div.api5 table th:nth-child(2) { width: 19%; } div.api5 table th:nth-child(3) { width: 19%; } div.api5 table th:nth-child(4) { width: 26%; }"
                      "\ndiv.msg table th:nth-child(1) { width: 13%; } div.msg table th:nth-child(2) { width: 20%; }"
                      "\ndiv.routes table { font-size: 10.5pt; } div.routes table th:nth-child(1) { width: 10%; } div.routes table th:nth-child(2) { width: 22%; } div.routes table th:nth-child(3) { width: 16%; }"
                      "\ndiv.routes table th:nth-child(4) { width: 10%; } div.routes table th:nth-child(5) { width: 10%; } div.routes table th:nth-child(6) { width: 18%; }")
    # draft 27: Appendix D screen tables: screen | name | use case steps | main elements | routes called
    build_pdf.CSS += ("\ndiv.screens table { font-size: 10.5pt; line-height: 1.3; } div.screens th, div.screens td { padding: 3pt 4pt; }"
                      "\ndiv.screens table th:nth-child(1) { width: 8%; } div.screens table th:nth-child(2) { width: 15%; } div.screens table th:nth-child(3) { width: 16%; } div.screens table th:nth-child(4) { width: 30%; }")
    build_pdf.markdown.Markdown = _Markdown
    stem = "seats_project_document_change_log" if a.changelog else "seats_project_document"
    out = OUT / f"{stem}_v{re.sub(r'[^0-9A-Za-z.]+', '-', a.version).strip('-')}.pdf"
    build_pdf.build(parts, "v" + a.version, out)
