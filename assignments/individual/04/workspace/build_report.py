#!/usr/bin/env python3
"""Build report.pdf from report.md.

1. terminal/<step>.txt  ->  terminal/png/<step>.png   (terminal-styled screenshot, via Chromium)
2. report.md            ->  report.html               (python-markdown)
3. report.html          ->  report.pdf                (Chromium print to PDF)
"""
import html
import re
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
TERM = HERE / "terminal"
PDF_NAME = "6970267821_Watayut_Aiamanan_Message_Queue_Lab_Report.pdf"
TERM_PNG = TERM / "png"
PROMPT_RE = re.compile(r"^\(\.venv\) \$ (.*)$")

TERMINAL_CSS = """
body { margin: 0; background: #ffffff; }
.term { display: inline-block; min-width: 900px; max-width: 1200px; background: #1e1e1e; border-radius: 8px;
        box-shadow: 0 2px 12px rgba(0,0,0,.35); font-family: 'DejaVu Sans Mono', 'Liberation Mono', monospace;
        font-size: 13px; color: #d4d4d4; }
.bar { background: #2d2d2d; border-radius: 8px 8px 0 0; padding: 6px 12px; color: #bbb; font-size: 12px;
       display: flex; align-items: center; gap: 8px; }
.dot { width: 11px; height: 11px; border-radius: 50%; display: inline-block; }
pre { margin: 0; padding: 12px 14px; white-space: pre-wrap; word-break: break-all; line-height: 1.42; }
.prompt { color: #4ec9b0; } .path { color: #569cd6; } .cmd { color: #ffffff; font-weight: 600; }
.ok { color: #6a9955; } .warn { color: #dcdcaa; } .err { color: #f14c4c; } .ctrl { color: #c586c0; }
"""


def colour(line):
    m = PROMPT_RE.match(line)
    if m:
        return (f'<span class="prompt">(.venv) @Watayut</span> <span class="path">~/messaging_lab_six_exercises</span> '
                f'<span class="prompt">$</span> <span class="cmd">{html.escape(m.group(1))}</span>')
    text = html.escape(line)
    if line.startswith("^C"):
        return f'<span class="ctrl">{text}</span>'
    if "exited with code" in line or "INTENTIONAL CRASH" in line or "intentional_crash" in line or "Traceback" in line:
        return f'<span class="err">{text}</span>'
    if "CONFIRMED" in line or "ACK SENT" in line or "DONE" in line or '"completed"' in line or '"committed"' in line:
        return f'<span class="ok">{text}</span>'
    if "READY" in line or "RECEIVED" in line or '"assigned"' in line or '"received"' in line or "START" in line:
        return f'<span class="warn">{text}</span>'
    return text


MAX_LINES = 26  # long Kafka logs: keep the head and the tail, elide the middle


def shorten(lines):
    if len(lines) <= MAX_LINES:
        return lines
    head, tail = lines[:MAX_LINES - 10], lines[-8:]
    return head + [f"··· {len(lines) - len(head) - len(tail)} more lines (full text in terminal/{{name}}.txt) ···"] + tail


def terminal_html(path: Path):
    lines = [l.replace("{name}", path.stem) for l in shorten(path.read_text().rstrip("\n").split("\n"))]
    body = "\n".join(colour(line) for line in lines)
    return (f"<html><head><meta charset='utf-8'><style>{TERMINAL_CSS}</style></head><body>"
            f"<div class='term'><div class='bar'><span class='dot' style='background:#ff5f56'></span>"
            f"<span class='dot' style='background:#ffbd2e'></span><span class='dot' style='background:#27c93f'></span>"
            f"&nbsp;{html.escape(path.stem)} — bash</div><pre>{body}</pre></div></body></html>")


def render_terminals(page):
    TERM_PNG.mkdir(exist_ok=True)
    for txt in sorted(TERM.glob("*.txt")):
        page.set_content(terminal_html(txt))
        page.locator(".term").screenshot(path=str(TERM_PNG / f"{txt.stem}.png"))
    print(f"rendered {len(list(TERM.glob('*.txt')))} terminal captures -> {TERM_PNG.relative_to(HERE)}/")


REPORT_CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
body { font-family: 'DejaVu Sans', 'Liberation Sans', Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #1a1a1a; }
h1 { font-size: 22pt; margin: 0 0 4pt; } h1 + p { margin-top: 0; }
h2 { font-size: 16pt; margin-top: 22pt; border-bottom: 2px solid #c0392b; padding-bottom: 3pt; page-break-before: always; }
h2.first { page-break-before: avoid; }
h3 { font-size: 12.5pt; margin-top: 16pt; color: #2c3e50; page-break-after: avoid; }
h4 { font-size: 11pt; margin: 12pt 0 4pt; page-break-after: avoid; }
table { border-collapse: collapse; margin: 8pt 0; font-size: 9.5pt; }
th, td { border: 1px solid #bbb; padding: 3pt 6pt; vertical-align: top; }
th { background: #f0f0f0; text-align: left; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 9pt; background: #f4f4f4; padding: 0 2px; }
pre { background: #f6f8fa; border: 1px solid #ddd; padding: 6pt 8pt; font-size: 8.5pt; white-space: pre-wrap;
      word-break: break-all; page-break-inside: avoid; }
pre code { background: none; padding: 0; font-size: 8.5pt; }
img { max-width: 100%; max-height: 105mm; width: auto; height: auto; display: block; margin: 6pt auto; border: 1px solid #ccc; page-break-inside: avoid; }
figure { margin: 8pt 0; page-break-inside: avoid; }
figcaption, .caption { font-size: 9pt; color: #555; text-align: center; margin-top: -2pt; }
blockquote { border-left: 3px solid #c0392b; margin: 8pt 0; padding: 2pt 10pt; color: #333; background: #fdf3f2; }
.meta { color: #555; font-size: 10pt; }
.answer { background: #eef6ee; border: 1px solid #b7d7b7; padding: 6pt 10pt; margin: 8pt 0; }
"""


def build_html():
    md = (HERE / "report.md").read_text()
    body = markdown.markdown(md, extensions=["tables", "fenced_code", "attr_list", "md_in_html", "toc"])
    # Every image caption: "![caption](path)" renders as <img alt=caption>; add a visible caption under it.
    body = re.sub(r'<p><img alt="([^"]*)" src="([^"]*)"\s*/?></p>',
                  r'<figure><img alt="\1" src="\2"><figcaption>\1</figcaption></figure>', body)
    body = body.replace('<h2 id="', '<h2 class="first" id="', 1)
    page = f"<!doctype html><html><head><meta charset='utf-8'><title>Message Queue Lab Report</title><style>{REPORT_CSS}</style></head><body>{body}</body></html>"
    (HERE / "report.html").write_text(page)
    return HERE / "report.html"


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1250, "height": 800}, device_scale_factor=2)
        render_terminals(page)
        out = build_html()
        page = browser.new_page()
        page.goto(out.as_uri(), wait_until="networkidle")
        page.pdf(path=str(HERE / PDF_NAME), format="A4", print_background=True,
                 display_header_footer=True,
                 header_template="<div></div>",
                 footer_template="<div style='font-size:8px;color:#777;width:100%;text-align:center;'>"
                                 "2110521 Software Architecture — Message Queue Lab — Watayut Aiamanan (6970267821) — page "
                                 "<span class='pageNumber'></span> / <span class='totalPages'></span></div>",
                 margin={"top": "18mm", "bottom": "18mm", "left": "16mm", "right": "16mm"})
        browser.close()
    print(f"wrote {HERE / PDF_NAME}")


if __name__ == "__main__":
    main()
