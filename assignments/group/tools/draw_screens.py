#!/usr/bin/env python3
"""Low-fidelity wireframes of the SEATS screens of Appendix D (Tables D.1 and D.2 of the project document).

Grayscale, English placeholder text; the Customer Web App (C1-C9) and the staff-phone screens of the back-office
(B5, B6) at the 360 x 640 phone viewport, the other back-office screens (B1-B4, B7) in a 1100 x 680 desktop browser
window.  Table status is shown by pattern and label, never by colour alone.  Each figure is one HTML page whose
div.figure holds the screens with their captions (screen id, name, use case steps of Appendix D); the PNG is a 2x
screenshot of that element, taken with headless Chromium (Playwright).

Style copied (not imported) from assignments/group/tools/build_wireframes.py of the 2110628 repository, without the
numbered markers and the note columns: the tables of Appendix D carry the step numbers, the figures show the screens.

Output: workspace/report/project-document/assets/screens-<figure>.html and .png
Usage:  python3 tools/draw_screens.py            (any working directory; needs playwright + chromium)
"""
import re
import struct
from pathlib import Path

GROUP = Path(__file__).resolve().parent.parent
OUT = GROUP / "workspace" / "report" / "project-document" / "assets"

CSS = """
  body { margin: 0; background: #fff; font-family: "Noto Sans", "Liberation Sans", Arial, sans-serif; color: #222; }
  .figure { display: flex; gap: 26px; padding: 16px; background: #fff; align-items: flex-start; width: max-content; }
  .figure.desk { padding: 8px; }
  .cell { width: 380px; }
  .cell.desk { width: 1100px; }
  .cell .cap { font-size: 15px; font-weight: 600; margin: 0 0 8px 2px; line-height: 1.3; }
  .cell.ph .cap { min-height: 39px; }
  .cell .cap span { font-weight: 400; color: #555; font-size: 13.5px; }
  .cell .cap .nb { white-space: nowrap; }
  .phone { width: 360px; border: 2px solid #555; border-radius: 22px; overflow: hidden; background: #fff; position: relative; flex: none; }
  .statusbar { height: 20px; background: #ddd; font-size: 10.5px; display: flex; justify-content: space-between; padding: 0 14px; align-items: center; color: #444; }
  .browserbar { height: 36px; background: #e8e8e8; border-bottom: 1px solid #bbb; display: flex; align-items: center; gap: 10px; padding: 0 12px; font-size: 12px; color: #444; }
  .browserbar .x { font-size: 15px; }
  .browserbar .url { flex: 1; background: #fff; border: 1px solid #bbb; border-radius: 10px; padding: 2px 10px; color: #666; font-size: 11.5px; }
  .viewport { width: 360px; height: 640px; position: relative; overflow: hidden; background: #fff; }
  .appbar { height: 48px; display: flex; align-items: center; gap: 10px; padding: 0 14px; border-bottom: 1px solid #bbb; font-weight: 600; font-size: 16px; background: #f5f5f5; box-sizing: border-box; }
  .appbar .back { font-size: 20px; color: #444; font-weight: 400; }
  .appbar .right { margin-left: auto; font-weight: 700; font-size: 15px; }
  .appbar .more { margin-left: auto; font-size: 20px; color: #444; font-weight: 400; }
  .appbar .right + .more { margin-left: 10px; }
  .topbar.phone-top { height: 36px; font-size: 14px; padding: 0 12px; gap: 10px; flex: none; }
  .topbar.phone-top .burger { font-size: 17px; font-weight: 400; }
  .content { padding: 12px 14px; font-size: 14px; line-height: 1.35; }
  .card { border: 1px solid #999; border-radius: 6px; padding: 10px 12px; margin: 10px 0; background: #fff; }
  .card.soft { background: #f4f4f4; border-style: dashed; }
  .btn { display: block; width: 100%; box-sizing: border-box; text-align: center; padding: 11px 0; border-radius: 6px; font-weight: 600; font-size: 15px; margin-top: 10px; border: 1.5px solid #444; }
  .btn.primary { background: #444; color: #fff; }
  .btn.secondary { background: #fff; color: #333; }
  .btn.small { padding: 7px 0; font-size: 13px; margin-top: 8px; }
  .btn.disabled { border-color: #bbb; color: #999; background: #f3f3f3; }
  .btn.half { display: inline-block; width: 48.5%; }
  .input { border: 1.5px solid #999; border-radius: 5px; padding: 9px 10px; color: #777; margin: 4px 0 8px; background: #fff; }
  .input.err { border-color: #222; border-width: 2px; }
  .errtext { font-size: 12px; color: #222; font-weight: 600; margin: -4px 0 8px; }
  .label { font-size: 11.5px; color: #555; text-transform: uppercase; letter-spacing: .3px; margin-top: 8px; }
  .row { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
  .muted { color: #666; font-size: 13px; }
  .tiny { color: #666; font-size: 11.5px; }
  .b { font-weight: 700; }
  .badge { display: inline-block; border: 1px solid #666; border-radius: 10px; padding: 1px 9px; font-size: 11px; font-weight: 600; background: #fff; white-space: nowrap; }
  .badge.fill { background: #666; color: #fff; border-color: #666; }
  .badge.hatch { background: repeating-linear-gradient(45deg, #bbb 0 3px, #fff 3px 6px); }
  .badge.dim { color: #777; border-color: #aaa; }
  .hr { border-top: 1px solid #ccc; margin: 10px 0; }
  .check { display: inline-block; width: 16px; height: 16px; border: 1.5px solid #555; border-radius: 3px; vertical-align: -3px; margin-right: 8px; text-align: center; font-size: 12px; line-height: 15px; background: #fff; }
  .check.on { background: #444; color: #fff; }
  .stepper { display: inline-flex; border: 1.5px solid #555; border-radius: 6px; overflow: hidden; }
  .stepper span { width: 36px; text-align: center; padding: 5px 0; font-size: 16px; }
  .stepper .v { width: 44px; border-left: 1.5px solid #555; border-right: 1.5px solid #555; font-weight: 700; background: #f4f4f4; }
  .toast { position: absolute; left: 14px; right: 14px; bottom: 16px; background: #333; color: #fff; padding: 10px 12px; border-radius: 6px; font-size: 13px; line-height: 1.3; }
  .modal-bg { position: absolute; inset: 0; background: rgba(0, 0, 0, .38); }
  .modal { position: absolute; left: 22px; right: 22px; background: #fff; border: 1.5px solid #444; border-radius: 8px; padding: 14px; font-size: 14px; }
  .qr { width: 140px; height: 140px; margin: 6px auto; background: conic-gradient(#222 25%, #fff 0 50%, #222 0 75%, #fff 0); background-size: 20px 20px; border: 6px solid #fff; outline: 1.5px solid #555; }
  .qr.small { width: 110px; height: 110px; background-size: 16px 16px; }
  .placeholder { background: repeating-linear-gradient(-45deg, #eee 0 6px, #f8f8f8 6px 12px); border: 1px dashed #999; color: #666; display: flex; align-items: center; justify-content: center; font-size: 12.5px; text-align: center; box-sizing: border-box; }
  .mono { font-family: "DejaVu Sans Mono", "Liberation Mono", monospace; letter-spacing: .5px; }
  .chat { padding: 10px 12px; }
  .bubble { max-width: 250px; background: #f0f0f0; border: 1px solid #ccc; border-radius: 12px; padding: 8px 11px; font-size: 13px; margin: 8px 0; line-height: 1.3; }
  .bubble.me { margin-left: auto; background: #dcdcdc; }
  .richmenu { position: absolute; left: 0; right: 0; bottom: 0; height: 180px; background: #e6e6e6; border-top: 1px solid #aaa; display: grid; grid-template-columns: 1fr 1fr; gap: 1px; }
  .richmenu div { background: #f4f4f4; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 600; color: #333; text-align: center; padding: 4px; }
  .richmenu div.hi { background: #cfcfcf; outline: 2px solid #333; outline-offset: -3px; }
  .legend { display: flex; gap: 12px; font-size: 11.5px; margin: 6px 0 2px; flex-wrap: wrap; }
  .legend span { display: inline-flex; align-items: center; gap: 5px; }
  .sw { display: inline-block; width: 14px; height: 14px; border: 1.2px solid #444; border-radius: 3px; background: #fff; }
  .sw.hatch { background: repeating-linear-gradient(45deg, #888 0 2px, #fff 2px 5px); }
  .sw.fill { background: #777; }
  .sw.dark { background: #333; }
  .result { border: 2.5px solid #222; border-radius: 8px; padding: 10px 12px; text-align: center; margin: 8px 0; }
  .result .big { font-size: 24px; font-weight: 800; letter-spacing: 1px; }
  .kv { display: grid; grid-template-columns: 112px 1fr; gap: 3px 8px; font-size: 13.5px; margin: 6px 0; }
  .kv .k { color: #666; }
  .banner { padding: 9px 11px; border: 1.5px solid #444; border-radius: 6px; background: repeating-linear-gradient(-45deg, #f3f3f3 0 8px, #fff 8px 16px); font-size: 13px; margin: 8px 0; }
  .viewfinder { width: 300px; height: 230px; margin: 14px auto 10px; position: relative; background: repeating-linear-gradient(-45deg, #e9e9e9 0 6px, #f6f6f6 6px 12px); border: 1px solid #999; }
  .viewfinder .frame { position: absolute; left: 60px; top: 30px; width: 170px; height: 170px; border: 2.5px dashed #333; }
  .viewfinder .hint { position: absolute; left: 0; right: 0; bottom: 6px; text-align: center; font-size: 12px; color: #444; }

  /* desktop browser window of the back-office */
  .win { width: 1100px; height: 680px; border: 2px solid #555; border-radius: 8px; overflow: hidden; background: #fff; display: flex; flex-direction: column; box-sizing: border-box; }
  .win .browserbar { flex: none; }
  .topbar { flex: none; height: 44px; background: #3a3a3a; color: #fff; display: flex; align-items: center; padding: 0 16px; font-weight: 700; font-size: 16px; gap: 12px; }
  .topbar .who { margin-left: auto; font-weight: 400; font-size: 12.5px; color: #ddd; }
  .wbody { display: flex; flex: 1; min-height: 0; }
  .nav { width: 180px; flex: none; background: #f0f0f0; border-right: 1px solid #bbb; padding: 8px 0; font-size: 14px; box-sizing: border-box; }
  .nav div { padding: 9px 16px; color: #333; }
  .nav div.cur { background: #d4d4d4; font-weight: 700; border-left: 4px solid #333; padding-left: 12px; }
  .nav .sep { border-top: 1px solid #bbb; margin: 8px 12px; padding: 0; }
  .main { flex: 1; min-width: 0; padding: 14px 16px; font-size: 13.5px; line-height: 1.35; overflow: hidden; box-sizing: border-box; }
  .main h1 { font-size: 17px; margin: 0 0 10px; }
  .cols { display: flex; gap: 12px; align-items: flex-start; }
  .panel { border: 1px solid #999; border-radius: 6px; padding: 8px 12px; background: #fff; box-sizing: border-box; }
  .panel + .panel { margin-top: 8px; }
  .main .tiny { font-size: 12px; }
  .tbl.small { font-size: 12px; }
  .pt { font-weight: 700; font-size: 13.5px; margin: 0 0 6px; }
  .frow { display: flex; align-items: center; gap: 8px; margin: 4px 0; }
  .frow .fl { width: 92px; flex: none; color: #555; font-size: 12px; }
  .frow .fin { flex: 1; }
  .frow .unit { color: #666; font-size: 12px; flex: none; }
  .fin { min-width: 0; border: 1.5px solid #999; border-radius: 5px; padding: 4px 8px; font-size: 13px; background: #fff; white-space: nowrap; overflow: hidden; box-sizing: border-box; }
  .fin.sel { display: flex; justify-content: space-between; gap: 6px; }
  .fin.err { border-color: #222; border-width: 2px; }
  .tbl { border-collapse: collapse; width: 100%; font-size: 12.5px; }
  .tbl th, .tbl td { border: 1px solid #bbb; padding: 4px 7px; text-align: left; vertical-align: top; }
  .tbl th { background: #eee; font-weight: 700; font-size: 11.5px; }
  .tbl tr.sel td { background: #e2e2e2; font-weight: 600; }
  .tbl td.num, .tbl th.num { text-align: right; }
  .tbl td.err { border: 2px solid #222; }
  .chip { display: inline-block; border: 1px solid #666; border-radius: 12px; padding: 1px 9px; font-size: 12px; margin: 2px 4px 2px 0; background: #fff; }
  .chip.add { border-style: dashed; color: #555; }
  .btnrow { display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; align-items: center; }
  .btn.inline { display: inline-block; width: auto; padding: 7px 14px; margin: 0; font-size: 13px; }
  .list .it { border: 1px solid #aaa; border-radius: 6px; padding: 7px 10px; margin: 6px 0; font-size: 13px; line-height: 1.3; }
  .list .it .badge { margin-top: 4px; }
  .list .hd { font-weight: 700; font-size: 13.5px; margin-bottom: 2px; }
  .list .it.cur { background: #e2e2e2; border-color: #333; border-width: 2px; }
  .vbox { border: 2px solid #222; border-radius: 6px; padding: 8px 12px; font-size: 12.5px; background: #fff; }
  .vbox.ok { border-style: dashed; }
  .vbox .t { font-weight: 700; margin-bottom: 3px; }
  .vbox ul { margin: 0; padding-left: 18px; }
  .counts { display: flex; gap: 10px; margin: 8px 0 0; font-size: 13px; }
  .counts span { border: 1px solid #999; border-radius: 6px; padding: 4px 10px; background: #f7f7f7; white-space: nowrap; }
  .signin { width: 360px; margin: 110px auto 0; border: 1px solid #999; border-radius: 8px; padding: 22px 26px; box-sizing: border-box; }
  .signin .title { font-size: 20px; font-weight: 700; margin-bottom: 2px; }
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


# ----------------------------------------------------------------------------------------------------------- table map
# Zone A near the stage (round 2-person, square 4-person, sofa 6-person), Zone B behind it (adds the 1-person triangle).
# Status: available (white), held (hatch), booked (solid grey), occupied (dark) - pattern + label, not colour.
ZONE_A = [  # (id, kind), row by row
    [("A1", "c"), ("A2", "c"), ("A3", "c"), ("A4", "s"), ("A5", "s")],
    [("A6", "f"), ("A7", "f"), ("A8", "c"), ("A9", "c"), ("A10", "c")],
    [("A11", "s"), ("A12", "s"), ("A13", "s"), ("A14", "c"), ("A15", "c")],
]
ZONE_B = [
    [("B1", "c"), ("B2", "c"), ("B3", "s"), ("B4", "s"), ("B5", "f")],
    [("B6", "c"), ("B7", "c"), ("B8", "c"), ("B9", "s"), ("B10", "s")],
    [("B11", "t"), ("B12", "t"), ("B13", "t"), ("B14", "t"), ("B15", "t"), ("B16", "t")],
]
BOOKED = {"A1", "A3", "A5", "A8", "A11", "A13", "A15", "B2", "B5", "B7", "B10", "B12", "B14"}
HELD = {"A7", "A14", "B3"}


def table_map(width=332, highlight="A12", tapped=True, compact=False, occupied=None, scale=1.0,
              status=True, editor=False):
    """SVG zone map.  highlight = the table the customer taps (C3) or is guided to (B6).
    scale draws the same map larger (viewBox scaling: shapes and text grow together).
    status=False draws every table as available (the zone map editor has no bookings).
    editor=True adds the venue image placeholder, the zones as labelled dashed rectangles and, at the right, a zone
    still without a name holding table 17 without a table type (the two validation problems of B2)."""
    occupied = occupied or set()
    h = 178 if compact else (314 if editor else 300)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width * scale:.0f}" height="{h * scale:.0f}" '
           f'viewBox="0 0 {width} {h}" style="display:block">',
           '<defs><pattern id="hatch" patternUnits="userSpaceOnUse" width="6" height="6">'
           '<path d="M0 6 L6 0 M-1 1 L1 -1 M5 7 L7 5" stroke="#777" stroke-width="1.4"/></pattern>'
           '<pattern id="img" patternUnits="userSpaceOnUse" width="12" height="12" patternTransform="rotate(-45)">'
           '<rect width="12" height="12" fill="#f5f5f5"/><rect width="6" height="12" fill="#ebebeb"/></pattern></defs>',
           f'<rect x="0" y="0" width="{width}" height="{h}" fill="{"url(#img)" if editor else "#fff"}"/>']
    tw = width - 76 if editor else width   # table area (the unnamed zone takes the right strip of the editor)
    # stage
    out.append(f'<rect x="{tw/2-70:.0f}" y="4" width="140" height="20" fill="#ddd" stroke="#666"/>')
    out.append(f'<text x="{tw/2:.0f}" y="18" text-anchor="middle" font-size="11" font-weight="700" fill="#333">STAGE</text>')

    def draw(zone, y0, label):
        if editor:
            out.append(f'<rect x="3" y="{y0 - 16}" width="{tw - 6}" height="132" rx="4" fill="none" stroke="#333" '
                       f'stroke-width="1.3" stroke-dasharray="5 3"/>')
        out.append(f'<text x="8" y="{y0 - 5}" font-size="10.5" font-weight="700" fill="#333">{label}</text>')
        for r, row in enumerate(zone):
            n = len(row)
            slot = (tw - 12) / n
            for i, (tid, kind) in enumerate(row):
                cx = 6 + slot * (i + 0.5)
                cy = y0 + 18 + r * 40
                fill, stroke, txt = "#fff", "#444", "#222"
                if status and tid in BOOKED:
                    fill, txt = "#777", "#fff"
                elif status and tid in HELD:
                    fill = "url(#hatch)"
                if tid in occupied:
                    fill, txt = "#333", "#fff"
                sw = 2.6 if tid == highlight else 1.2
                if kind == "c":
                    out.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
                elif kind == "s":
                    out.append(f'<rect x="{cx-12:.1f}" y="{cy-12}" width="24" height="24" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
                elif kind == "f":
                    out.append(f'<rect x="{cx-24:.1f}" y="{cy-11}" width="48" height="22" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
                else:
                    out.append(f'<polygon points="{cx:.1f},{cy-13} {cx+13:.1f},{cy+10} {cx-13:.1f},{cy+10}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
                ty = cy + 4 if kind != "t" else cy + 7
                fs = 8.5 if kind != "f" else 9
                out.append(f'<text x="{cx:.1f}" y="{ty}" text-anchor="middle" font-size="{fs}" font-weight="600" fill="{txt}">{tid}</text>')
                if tid == highlight and tapped:
                    out.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="19" fill="none" stroke="#111" stroke-width="1.5" stroke-dasharray="3 3"/>')

    draw(ZONE_A, 46, "Zone A &middot; front stage" if editor else "ZONE A")
    if not compact:
        draw(ZONE_B, 180, "Zone B" if editor else "ZONE B")
    if editor:
        x0 = tw + 2
        out.append(f'<rect x="{x0}" y="30" width="{width - x0 - 3}" height="266" rx="4" fill="none" stroke="#333" '
                   f'stroke-width="1.3" stroke-dasharray="5 3"/>')
        out.append(f'<text x="{x0 + 5}" y="41" font-size="9.5" font-style="italic" fill="#555">(no name)</text>')
        cx = x0 + (width - x0) / 2
        out.append(f'<circle cx="{cx:.1f}" cy="150" r="12" fill="#fff" stroke="#444" stroke-width="1.2" stroke-dasharray="2 2"/>')
        out.append(f'<text x="{cx:.1f}" y="154" text-anchor="middle" font-size="8.5" font-weight="600" fill="#222">17</text>')
        out.append(f'<text x="{cx:.1f}" y="172" text-anchor="middle" font-size="8" fill="#555">no type</text>')
        out.append(f'<text x="{width - 4}" y="{h - 5}" text-anchor="end" font-size="9" font-style="italic" fill="#777">venue image: main-hall.jpg</text>')
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------------------------------------------------- phone frame
def phone(chrome, appbar, body, status_right="LTE 78%"):
    """chrome: 'line' (LINE chat, no browser bar), 'liff' (LINE in-app browser: the app bar ends with the &#8942; menu of
    the web app, which opens the two screens LINE's rich menu would open and Log out), 'staff' (the back-office on a
    staff phone: the web app's top bar above the app bar, its sidebar behind the &#9776;)."""
    bar = ""
    top = ""
    if chrome == "liff":
        bar = '<div class="browserbar"><span class="x">&#10005;</span><span class="url">liff.line.me/seats &middot; La Loy Bar</span><span>&#8942;</span></div>'
        appbar = f'{appbar}<span class="more">&#8942;</span>'
    elif chrome == "staff":
        bar = '<div class="browserbar"><span class="x">&#8592;</span><span class="url">seats-backoffice.example &middot; signed in as door1</span><span>&#8942;</span></div>'
        top = '<div class="topbar phone-top"><span class="burger">&#9776;</span>SEATS back-office<span class="who">signed in as door1</span></div>'
    app = f'<div class="appbar">{appbar}</div>' if appbar else ""
    return (f'<div class="phone"><div class="statusbar"><span>19:02</span><span>{status_right}</span></div>{bar}'
            f'<div class="viewport">{top}{app}{body}</div></div>')


# ------------------------------------------------------------------------------------------------- desktop browser frame
NAV = ["Concert rounds", "Zone maps", "Live view", "Check-in", "Business parameters", "Staff accounts"]


def desktop(user, current, main, nav=True):
    """The back-office in a desktop browser: browser bar, top app bar, left navigation (current items highlighted), main area."""
    bar = ('<div class="browserbar"><span class="x">&#8249;</span><span class="x">&#8250;</span><span class="x">&#8635;</span>'
           f'<span class="url">seats-backoffice.example &middot; {user}</span></div>')
    top = f'<div class="topbar">SEATS back-office<span class="who">{user}</span></div>'
    items = "".join(f'<div class="{"cur" if n in current else ""}">{n}</div>' for n in NAV)
    navhtml = f'<div class="nav">{items}<div class="sep"></div><div>Sign out</div></div>' if nav else ""
    return f'<div class="win">{bar}{top}<div class="wbody">{navhtml}<div class="main">{main}</div></div></div>'


def frow(label, value, kind="", unit=""):
    caret = '<span>&#9662;</span>' if kind == "sel" else ""
    u = f'<span class="unit">{unit}</span>' if unit else ""
    return f'<div class="frow"><span class="fl">{label}</span><span class="fin {kind}">{value}{caret}</span>{u}</div>'


def listing(title, new, items):
    """Left column of an editor: the objects with their status; (name, sub line, badge html, current?)."""
    its = "".join(f'<div class="it{" cur" if cur else ""}"><div{" class=b" if cur else ""}>{n}</div><div class="tiny">{sub}</div>{badge}</div>'
                  for n, sub, badge, cur in items)
    return f'<div class="list"><div class="hd">{title}</div><div class="btn secondary small" style="margin:0 0 6px">{new}</div>{its}</div>'


def tbl(head, rows, widths=None, small=False):
    cols = ""
    if widths:
        cols = "<colgroup>" + "".join(f'<col style="width:{w}">' for w in widths) + "</colgroup>"
    th = "".join(f'<th class="{c}">{t}</th>' for t, c in head)
    body = ""
    for cls, cells in rows:
        body += f'<tr class="{cls}">' + "".join(f'<td class="{c}">{t}</td>' for t, c in cells) + "</tr>"
    return f'<table class="tbl{" small" if small else ""}">{cols}<tr>{th}</tr>{body}</table>'


def vbox(title, problems, note, ok=False):
    li = "".join(f"<li>{p}</li>" for p in problems)
    return (f'<div class="vbox{" ok" if ok else ""}"><div class="t">{title}</div>'
            + (f"<ul>{li}</ul>" if problems else "") + f'<div class="tiny" style="margin-top:4px">{note}</div></div>')


def page(title, inner, desk=False):
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>{esc(title)}</title><style>{CSS}</style></head>'
            f'<body><div class="figure{" desk" if desk else ""}">{inner}</div></body></html>')


# ------------------------------------------------------------------------------------------ Customer Web App (Table D.1)
def c1():
    body = ('<div class="chat">'
            '<div class="bubble">Booking for <b>Sat 26 Sep 2026 &middot; 20:00</b> (Artist name) is open now. Tap <b>Reserve a table</b> below.</div>'
            '<div class="bubble me">Hi, is a 4-person table still free?</div>'
            '<div class="bubble">Please use the menu below: the map shows what is free right now and your table is held while you pay.</div>'
            '</div>'
            '<div class="richmenu"><div class="hi">Reserve a table</div><div>My bookings</div><div>Contact us</div><div>Booking terms</div></div>'
            '<div class="modal-bg"></div>'
            '<div class="modal" style="top:150px"><div class="b" style="font-size:15px">LINE Login</div>'
            '<div class="muted" style="margin:4px 0 8px">SEATS Booking (La Loy Bar) wants to use:</div>'
            '<div>&#8226; your LINE profile name<br>&#8226; your LINE user ID</div>'
            '<div class="tiny" style="margin-top:6px">No separate registration: one LINE account is one customer.</div>'
            '<div class="btn primary small">Allow</div><div class="btn secondary small">Cancel</div></div>')
    ph = phone("line", '<span class="back">&#8249;</span>La Loy Bar <span class="tiny" style="margin-left:6px">Official Account</span>', body)
    return "C1", "Rich Menu and LINE Login", "UC-01 steps 1&ndash;2, EF-2", ph


def c2():
    def card(date, artist, badge, opens, action):
        return (f'<div class="card"><div class="row"><span class="b">{date}</span>{badge}</div>'
                f'<div>{artist}</div><div class="muted">{opens}</div>{action}</div>')
    body = ('<div class="content">'
            + card("Sat 26 Sep 2026 &middot; 20:00", "Artist name", '<span class="badge">Open</span>',
                   "Booking opened Fri 18 Sep 18:00", '<div class="btn primary small">Select this round</div>')
            + card("Sat 3 Oct 2026 &middot; 20:00", "Artist name", '<span class="badge hatch">Not yet open</span>',
                   "Booking opens Fri 25 Sep 18:00", '<div class="btn small disabled">Opens in 9 days</div>')
            + card("Fri 25 Sep 2026 &middot; 20:00", "Artist name", '<span class="badge fill">Sold out</span>',
                   "All tables booked", '<div class="btn small disabled">Sold out</div>')
            + '<div class="tiny" style="margin-top:8px">Rounds are listed by date. Prices and the zone map are shown after you select a round.</div></div>')
    ph = phone("liff", "Concert rounds", body)
    return "C2", "Concert rounds", "UC-01 steps 3&ndash;4, AF-1, AF-2", ph


def c3():
    body = ('<div class="content" style="padding-top:8px">'
            '<div class="row"><span class="muted">Zone map &middot; refreshed live</span><span class="tiny">Tap an available table</span></div>'
            + table_map() +
            '<div class="legend"><span><i class="sw"></i>Available</span><span><i class="sw hatch"></i>Held (15 min)</span><span><i class="sw fill"></i>Booked</span></div>'
            '<div class="tiny">Zone A: &#9675; 2 p 2,400 &middot; &#9633; 4 p 4,800 &middot; sofa 6 p 7,200 THB<br>'
            'Zone B: &#9675; 2,000 &middot; &#9633; 4,000 &middot; sofa 6,000 &middot; &#9651; 1 p 700 THB<br>Extra person +600 THB each (added with the party size)</div>'
            '</div>'
            '<div class="toast">Table A7 was just taken by another customer. The map has been refreshed.</div>')
    ph = phone("liff", '<span class="back">&#8249;</span>Sat 26 Sep &middot; 20:00 &middot; Artist name', body)
    return "C3", "Table map", "UC-01 steps 5&ndash;8, AF-3", ph


def c4():
    body = ('<div class="content">'
            '<div class="card"><div class="b">Sat 26 Sep 2026 &middot; 20:00 &middot; Artist name</div>'
            '<div>Table <b>A12</b> &middot; Zone A &middot; 4-person square</div>'
            '<div class="muted">Package: 2 towers + 2 ice &middot; 4,800 THB</div></div>'
            '<div class="label">Party size</div>'
            '<div class="row" style="margin-top:4px"><span class="stepper"><span>-</span><span class="v">5</span><span>+</span></span>'
            '<span class="tiny" style="text-align:right">Capacity 4<br>1 extra person &times; 600 THB</span></div>'
            '<div class="hr"></div>'
            '<div class="row"><span>Package price</span><span>4,800 THB</span></div>'
            '<div class="row"><span>Extra-person fee</span><span>600 THB</span></div>'
            '<div class="row b" style="font-size:16px;margin-top:4px"><span>Full table fee</span><span>5,400 THB</span></div>'
            '<div class="tiny">Paid in full now; nothing to pay at the venue.</div>'
            '<div class="btn primary">Continue</div>'
            '<div class="btn secondary">Cancel hold</div>'
            '<div class="tiny" style="margin-top:8px">The table is held for you for 15 minutes. If the hold expires before payment, it returns to the map.</div>'
            '</div>')
    ph = phone("liff", '<span class="back">&#8249;</span>Your table is held <span class="right">14:32</span>', body)
    return "C4", "Hold and booking summary", "UC-01 steps 8&ndash;11, AF-4, EF-1", ph


def c5():
    body = ('<div class="content">'
            '<div class="card soft"><div class="b">Why we ask</div><div class="muted">Your name and phone are used for this booking, its payment, check-in and contact about it only. They are collected once and pre-filled on your next booking.</div></div>'
            '<div><span class="check on">&#10003;</span>I consent to the collection of my name and phone for these purposes</div>'
            '<div class="label">Name</div><div class="input" style="color:#222">Somchai P.</div>'
            '<div class="label">Mobile phone</div><div class="input err">08 1234 56</div>'
            '<div class="errtext">Enter a 10-digit Thai mobile number.</div>'
            '<div class="btn primary">Continue</div>'
            '<div class="btn secondary">Decline and cancel the booking</div>'
            '<div class="tiny" style="margin-top:8px">Returning customer? Your saved details are shown here to confirm or correct.</div>'
            '</div>')
    ph = phone("liff", '<span class="back">&#8249;</span>Your details <span class="right">13:50</span>', body)
    return "C5", "Customer profile and consent", "UC-01 step 12, AF-5; UC-09 steps 1&ndash;8, AF-1, AF-2", ph


def c6():
    body = ('<div class="content">'
            '<div class="card"><ol style="margin:0;padding-left:20px">'
            '<li><b>Full payment confirms the booking.</b> No deposit, nothing to pay at the venue.</li>'
            '<li style="margin-top:6px"><b>Check-in window opens 2 hours before the show</b> (from 18:00). Show the e-ticket QR at the door.</li>'
            '<li style="margin-top:6px"><b>Late arrival:</b> your table is kept until 30 minutes after the start (20:30).</li>'
            '<li style="margin-top:6px"><b>No-show:</b> after 20:30 the table is released and the fee is not refunded.</li>'
            '</ol></div>'
            '<div><span class="check on">&#10003;</span>I have read and accept the booking terms</div>'
            '<div class="btn primary">Pay 5,400 THB</div>'
            '<div class="btn secondary" style="font-size:13.5px">Decline the terms and cancel the booking</div>'
            '<div class="tiny" style="margin-top:8px">The terms are sent again with your e-ticket.</div>'
            '</div>')
    ph = phone("liff", '<span class="back">&#8249;</span>Booking terms <span class="right">13:05</span>', body)
    return "C6", "Booking terms", "UC-01 steps 13&ndash;14", ph


def c7():
    body = ('<div class="content">'
            '<div class="row"><span class="muted">Amount to pay</span><span class="b" style="font-size:18px">5,400 THB</span></div>'
            '<div class="card" style="border-width:1.5px"><div class="row"><span class="b">Hosted checkout</span><span class="tiny">Payment Gateway</span></div>'
            '<div class="hr"></div>'
            '<div class="row"><span><span class="check on">&#10003;</span>PromptPay QR</span><span class="tiny">selected</span></div>'
            '<div class="qr small"></div><div class="tiny" style="text-align:center">Scan with your banking app</div>'
            '<div class="hr"></div>'
            '<div><span class="check"></span>Credit / debit card</div>'
            '<div style="margin-top:6px"><span class="check"></span>Mobile banking</div>'
            '<div style="margin-top:6px"><span class="check"></span>E-wallet</div>'
            '</div>'
            '<div class="row" style="margin-top:8px"><span class="muted">Waiting for the payment result&hellip;</span><span class="tiny">checked every 2 s</span></div>'
            '<div class="btn secondary">Cancel the booking</div>'
            '<div class="tiny" style="margin-top:8px">Pay before the hold expires. The confirmation appears here automatically once the payment is received.</div>'
            '</div>')
    ph = phone("liff", '<span class="back">&#8249;</span>Payment <span class="right">12:40</span>', body)
    return "C7", "Payment", "UC-01 step 15; UC-10 steps 1&ndash;7, AF-1, EF-4", ph


def c8():
    body = ('<div class="content" style="padding-top:8px">'
            '<div class="result" style="border-style:solid"><div class="big">&#10003; Booking confirmed</div><div class="muted">Paid in full &middot; 5,400 THB</div></div>'
            '<div class="card" style="text-align:center;padding-top:6px"><div class="tiny">E-TICKET</div><div class="qr"></div>'
            '<div class="mono" style="font-size:13px">SEATS-260926-A12-7K3Q</div>'
            '<div class="hr"></div>'
            '<div style="text-align:left" class="kv"><span class="k">Round</span><span>Sat 26 Sep 2026 &middot; 20:00</span>'
            '<span class="k">Table</span><span>A12 &middot; Zone A &middot; 4-person square</span>'
            '<span class="k">Party size</span><span>5 (1 extra person paid)</span>'
            '<span class="k">Check-in</span><span>from 18:00 &middot; table kept until 20:30</span></div></div>'
            '<div class="tiny">A copy with the booking terms was sent to your LINE chat.</div>'
            '<div class="btn secondary small">My bookings</div>'
            '</div>')
    ph = phone("liff", "Confirmation", body)
    return "C8", "Confirmation and e-ticket", "UC-01 steps 16&ndash;20, EF-3", ph


def c9():
    def card(date, badge, lines, action=""):
        return (f'<div class="card"><div class="row"><span class="b">{date}</span>{badge}</div>{lines}{action}</div>')
    body = ('<div class="content">'
            + card("Sat 26 Sep 2026 &middot; 20:00", '<span class="badge fill">Confirmed</span>',
                   '<div>Artist name &middot; Table <b>A12</b> &middot; Zone A</div>'
                   '<div class="muted">4-person square &middot; party size 5 &middot; paid in full</div>'
                   '<div class="tiny">Check-in from 18:00 &middot; <span class="mono">SEATS-260926-A12-7K3Q</span></div>',
                   '<div class="btn primary small">Show e-ticket</div>')
            + card("Sat 3 Oct 2026 &middot; 20:00", '<span class="badge hatch">Held</span>',
                   '<div>Artist name &middot; Table <b>B4</b> &middot; Zone B</div>'
                   '<div class="muted">Hold ends in 11:20 &middot; pay to confirm</div>',
                   '<div class="btn secondary small">Continue to payment</div>')
            + card("Sat 12 Sep 2026 &middot; 20:00", '<span class="badge dim">Cancelled</span>',
                   '<div>Artist name &middot; Table <b>A9</b> &middot; Zone A</div>'
                   '<div class="muted">Cancelled by you on 10 Sep &middot; nothing charged</div>')
            + card("Fri 4 Sep 2026 &middot; 20:00", '<span class="badge dim">Expired</span>',
                   '<div>Artist name &middot; Table <b>B9</b> &middot; Zone B</div>'
                   '<div class="muted">Hold expired before payment &middot; nothing charged</div>')
            + '<div class="tiny" style="margin-top:6px">Bookings are listed newest first.</div></div>')
    ph = phone("liff", '<span class="back">&#8249;</span>My bookings', body)
    return "C9", "My Bookings", "UC-06", ph


# --------------------------------------------------------------------------------------- Back-office Web App (Table D.2)
def b1():
    main = ('<div class="signin"><div class="title">SEATS back-office</div><div class="muted" style="margin-bottom:12px">Sign in with your staff account</div>'
            '<div class="label">Username</div><div class="input" style="color:#222">manager</div>'
            '<div class="label">Password</div><div class="input" style="color:#222;letter-spacing:2px">&#8226;&#8226;&#8226;&#8226;&#8226;&#8226;&#8226;&#8226;</div>'
            '<div class="btn primary">Sign in</div>'
            '<div class="tiny" style="margin-top:12px">Staff accounts are issued by the Manager. Your role decides which screens open.</div></div>')
    win = desktop("not signed in", (), main, nav=False)
    return "B1", "Sign-in", "UC-08 (sign in and log out)", win


def b2():
    left = listing("Zone maps", "+ New map",
                   [("Main hall v2", "edited today", '<span class="badge">Draft</span>', True),
                    ("Main hall", "used by 2 rounds", '<span class="badge fill">Active</span>', False),
                    ("Garden stage", "edited 2 Sep", '<span class="badge">Draft</span>', False)])
    centre = ('<div class="row" style="margin-bottom:6px"><span class="b">Main hall v2 <span class="badge">Draft</span></span><span class="tiny">Draw a zone, then place tables in it</span></div>'
              + table_map(width=344, scale=1.15, highlight="A12", tapped=True, status=False, editor=True) +
              '<div class="btnrow"><span class="btn secondary inline">Upload image</span><span class="btn secondary inline">Validate</span>'
              '<span class="btn inline disabled">Activate</span></div>'
              '<div style="margin-top:10px">' + vbox("Validation result &middot; 2 problems",
                                                     ["Table 17 has no table type and no seating capacity.",
                                                      "The zone containing table 17 has no name."],
                                                     "Activate opens once the map passes validation; the preview then shows it as the Customer sees it.") + '</div>')
    right = ('<div class="panel"><div class="pt">Table properties &middot; selected A12</div>'
             + frow("Number", "A12") + frow("Zone", "Zone A", "sel") + frow("Table type", "4-person square", "sel")
             + frow("Capacity", "4", unit="seats") + '</div>'
             '<div class="panel"><div class="pt">Tables and capacity per zone</div>'
             + tbl([("Zone", ""), ("Tables", "num"), ("Seats", "num")],
                   [("", [("Zone A &middot; front stage", ""), ("15", "num"), ("48", "num")]),
                    ("", [("Zone B", ""), ("16", "num"), ("38", "num")]),
                    ("", [("(no name)", ""), ("1", "num"), ("&ndash;", "num")])], ["", "56px", "52px"]) + '</div>'
             '<div class="panel"><div class="pt">Table types</div>'
             + tbl([("Name", ""), ("Cap.", "num"), ("Package content", "")],
                   [("", [("2-person round", ""), ("2", "num"), ("1 tower + 1 ice", "")]),
                    ("", [("4-person square", ""), ("4", "num"), ("2 towers + 2 ice", "")]),
                    ("", [("6-person sofa", ""), ("6", "num"), ("3 towers + 3 ice", "")]),
                    ("", [("1-person seat", ""), ("1", "num"), ("1 bucket", "")])], ["110px", "40px", ""], small=True) +
             '<div class="btnrow" style="margin-top:6px"><span class="btn secondary inline" style="padding:5px 12px;font-size:12px">+ Add table type</span></div></div>')
    main = (f'<div class="cols"><div style="width:170px;flex:none">{left}</div>'
            f'<div style="width:396px;flex:none">{centre}</div><div style="width:296px;flex:none">{right}</div></div>')
    win = desktop("signed in as manager", {"Zone maps"}, main)
    return "B2", "Zone map editor", "UC-04 steps 1&ndash;13, S-1, AF-1, AF-3, EF-1 to EF-3; table types (FR-37)", win


def b3():
    left = listing("Concert rounds", "+ New round",
                   [("Friday Live", "Fri 9 Oct 2026 &middot; 20:00", '<span class="badge">Draft</span>', True),
                    ("Saturday Session", "Sat 3 Oct 2026 &middot; 20:00", '<span class="badge fill">Published</span>', False),
                    ("Saturday Session", "Sat 26 Sep 2026 &middot; 20:00", '<span class="badge fill">Published</span>', False)])
    col1 = ('<div class="panel"><div class="pt">Concert details</div>'
            + frow("Name", "Friday Live") + frow("Artist", "Artist name") + frow("Date", "Fri 9 Oct 2026")
            + frow("Doors open", "18:00") + frow("Start", "20:00") + frow("Booking opens", "Fri 2 Oct 2026 &middot; 18:00") +
            '<div class="tiny" style="margin-top:6px">Check-in window <b>18:00&ndash;20:30</b>: from 2 h before the start until 30 min after it (business parameters).</div></div>'
            '<div class="panel"><div class="pt">Zone map</div>' + frow("Zone map", "Main hall (Active)", "sel") +
            '<div class="tiny" style="margin:6px 0 3px">Tables not for sale in this round</div>'
            '<span class="chip">A6 &times;</span><span class="chip">B15 &times;</span><span class="chip">B16 &times;</span><span class="chip add">+ mark a table</span></div>'
            '<div class="panel"><div class="pt">Tables for sale and capacity per zone</div>'
            + tbl([("Zone", ""), ("For sale", "num"), ("Seats", "num")],
                  [("", [("Zone A &middot; front stage", ""), ("14 of 15", "num"), ("42", "num")]),
                   ("", [("Zone B", ""), ("14 of 16", "num"), ("36", "num")]),
                   ("", [("<b>Total</b>", ""), ("<b>28</b>", "num"), ("<b>78</b>", "num")])]) + '</div>')

    def cell(price, content):
        return f'<b>{price} THB</b><br><span class="tiny">{content}</span>'
    col2 = ('<div class="panel"><div class="pt">Package price and content per zone and table type</div>'
            + tbl([("Table type", ""), ("Zone A &middot; front stage", ""), ("Zone B", "")],
                  [("", [("2-person round", ""), (cell("2,400", "1 tower + 1 ice"), ""), (cell("2,000", "1 tower + 1 ice"), "")]),
                   ("", [("4-person square", ""), (cell("4,800", "2 towers + 2 ice"), ""), (cell("4,000", "2 towers + 2 ice"), "")]),
                   ("", [("6-person sofa", ""), (cell("7,200", "3 towers + 3 ice"), ""), (cell("6,000", "3 towers + 3 ice"), "")]),
                   ("", [("1-person seat", ""), ('<span class="tiny">none in this zone</span>', ""), ('<span class="tiny">price missing</span>', "err")])],
                  ["120px", "", ""]) + '</div>'
            '<div class="cols" style="margin-top:10px"><div style="flex:1">'
            + vbox("Validation result &middot; 1 problem",
                   ["No package price for the 1-person seat in Zone B."],
                   "Times are in order and no Published round overlaps Fri 9 Oct 2026. Publish opens once the round passes validation.") + '</div>'
            '<div style="width:118px;flex:none"><div class="placeholder" style="width:118px;height:196px;border-radius:12px;padding:8px">Preview:<br>as the Customer<br>sees it (C3)</div></div></div>'
            '<div class="btnrow"><span class="btn secondary inline">Save draft</span><span class="btn secondary inline">Validate</span>'
            '<span class="btn secondary inline">Preview</span><span class="btn inline disabled">Publish</span></div>')
    main = (f'<div class="cols"><div style="width:170px;flex:none">{left}</div>'
            f'<div style="width:312px;flex:none">{col1}</div><div style="width:380px;flex:none">{col2}</div></div>')
    win = desktop("signed in as manager", {"Concert rounds"}, main)
    return "B3", "Round editor", "UC-03 steps 1&ndash;16, S-1, AF-1, AF-3, EF-1, EF-2", win


def b4():
    occupied = {"A2", "A4", "A9", "A12", "B1", "B8"}
    head = ('<div class="row" style="margin-bottom:8px"><span style="display:flex;align-items:center;gap:8px"><span class="tiny" style="font-size:12.5px;color:#555">Round</span>'
            '<span class="fin sel" style="width:330px">Sat 26 Sep 2026 &middot; 20:00 &middot; Artist name<span>&#9662;</span></span></span>'
            '<span class="tiny">Refreshed every 2 s &middot; last 19:05:12</span></div>')
    left = (table_map(width=372, scale=1.4, highlight=None, tapped=False, occupied=occupied) +
            '<div class="legend" style="font-size:12.5px;margin-top:8px"><span><i class="sw"></i>Available</span><span><i class="sw hatch"></i>Held</span>'
            '<span><i class="sw fill"></i>Booked</span><span><i class="sw dark"></i>Occupied (checked in)</span></div>'
            '<div class="counts"><span>Available <b>9</b></span><span>Held <b>3</b></span><span>Booked <b>13</b></span><span>Occupied <b>6</b></span><span class="tiny" style="border:0;background:none;padding:4px 0">of 31 tables</span></div>')
    right = ('<div class="pt">Bookings of the round</div>'
             + tbl([("Table", ""), ("Name", ""), ("Party", "num"), ("Status", ""), ("Checked in", "")],
                   [("", [("A12", ""), ("Somchai P.", ""), ("5", "num"), ("Checked-in", ""), ("19:05 door1", "")]),
                    ("", [("A2", ""), ("Nattaya K.", ""), ("2", "num"), ("Checked-in", ""), ("18:41 door1", "")]),
                    ("", [("B1", ""), ("Preecha S.", ""), ("2", "num"), ("Checked-in", ""), ("18:52 door2", "")]),
                    ("", [("A1", ""), ("Kamon W.", ""), ("2", "num"), ("Confirmed", ""), ("&ndash;", "")]),
                    ("", [("B5", ""), ("Anong T.", ""), ("6", "num"), ("Confirmed", ""), ("&ndash;", "")]),
                    ("", [("A7", ""), ('<span class="tiny">(paying)</span>', ""), ("&ndash;", "num"), ("Held", ""), ("&ndash;", "")])],
                   ["52px", "", "48px", "82px", "88px"]) +
             '<div class="tiny" style="margin-top:6px">Showing 6 of 22 bookings &middot; scroll for more. Checked in 6 of 19 confirmed.</div>')
    main = head + f'<div class="cols"><div style="width:522px;flex:none">{left}</div><div style="flex:1;min-width:0">{right}</div></div>'
    win = desktop("signed in as manager", {"Live view"}, main)
    return "B4", "Live view", "UC-05; UC-02 step 7", win


def b5():
    body = ('<div class="content" style="padding-top:8px">'
            '<div class="row"><span class="b">Checked in 37 / 112</span><span class="tiny">Window open since 18:00</span></div>'
            '<div class="viewfinder"><div class="frame"></div><div class="hint">Point the camera at the e-ticket QR code</div></div>'
            '<div class="muted" style="text-align:center">The customer shows the e-ticket on the phone</div>'
            '<div class="hr"></div>'
            '<div class="label">Cannot scan?</div>'
            '<div class="btn secondary small">Type the booking reference</div>'
            '</div>')
    ph = phone("staff", 'Check-in &middot; Sat 26 Sep &middot; 20:00', body)
    return "B5", "Check-in scanner", "UC-02 steps 1&ndash;2, AF-2", ph


def b6_result():
    body = ('<div class="content" style="padding-top:8px">'
            '<div class="result"><div class="big">VALID</div><div class="muted">Confirmed booking &middot; tonight&rsquo;s round &middot; not yet checked in</div></div>'
            '<div class="kv"><span class="k">Table</span><span class="b">A12 &middot; Zone A</span>'
            '<span class="k">Type / package</span><span>4-person square &middot; 2 towers + 2 ice</span>'
            '<span class="k">Party size paid</span><span>5</span>'
            '<span class="k">Name</span><span>Somchai P.</span>'
            '<span class="k">Payment</span><span>Paid in full &middot; 5,400 THB</span></div>'
            '<div class="hr"></div>'
            '<div class="btn primary">Confirm entry</div>'
            '<div class="tiny" style="margin-top:8px">A refused ticket shows the reason here instead: already checked in (with time and staff), unknown, another round, window not open yet, after the grace period.</div>'
            '</div>')
    ph = phone("staff", '<span class="back">&#8249;</span>Verification result', body)
    return "B6", "Verification result", "UC-02 steps 3&ndash;6, S-1, AF-3 to AF-5, EF-1, EF-2", ph


def b6_confirmed():
    body = ('<div class="content" style="padding-top:8px">'
            '<div class="result" style="border-style:solid"><div class="big">&#10003; Checked in</div><div class="muted">19:05 &middot; by door1 &middot; party size 5</div></div>'
            '<div class="b" style="margin-top:6px">Guide the party to table A12</div>'
            '<div class="muted">Zone A, third row, second from the left</div>'
            + table_map(compact=True, tapped=False, occupied={"A12"}) +
            '<div class="tiny">Live view updated: the Manager sees A12 as occupied.</div>'
            '<div class="btn primary">Next scan</div>'
            '</div>')
    ph = phone("staff", 'Entry confirmed', body)
    return "B6", "Entry confirmed", "UC-02 steps 6&ndash;8, EF-5", ph


def b7():
    left = ('<div class="panel"><div class="pt">Business parameters</div>'
            + frow("Hold period", "15", unit="min") + frow("Check-in window", "2", unit="h before the start")
            + frow("Grace period", "30", unit="min after the start") + frow("Extra-person fee", "600", unit="THB per person") +
            '<div class="btnrow"><span class="btn primary inline">Save</span><span class="tiny">Last saved 12 Sep 2026 by manager</span></div>'
            '<div class="tiny" style="margin-top:8px">The hold period bounds every new hold; the check-in window and the grace period are derived for each round from these values; the extra-person fee is charged per person above the capacity of the table type.</div></div>')
    right = ('<div class="panel"><div class="row" style="margin-bottom:6px"><span class="pt" style="margin:0">Staff accounts</span><span class="btn secondary inline" style="padding:5px 12px;font-size:12px">+ Create account</span></div>'
             + tbl([("Username", ""), ("Role", ""), ("Status", ""), ("Last sign-in", "")],
                   [("", [("manager", ""), ("Manager", ""), ("Active", ""), ("today 17:40", "")]),
                    ("", [("owner", ""), ("Owner (read-only live view)", ""), ("Active", ""), ("26 Sep", "")]),
                    ("sel", [("door1", ""), ("Front Staff", ""), ("Active", ""), ("today 18:02", "")]),
                    ("", [("door2", ""), ("Front Staff", ""), ("Active", ""), ("today 18:05", "")]),
                    ("", [("door3", ""), ("Front Staff", ""), ("Disabled", ""), ("12 Sep", "")])],
                   ["90px", "", "72px", "96px"]) +
             '<div class="btnrow"><span class="tiny">Selected: door1</span><span class="btn secondary inline">Change role</span><span class="btn secondary inline">Disable</span></div>'
             '<div class="tiny" style="margin-top:8px">A disabled account can no longer sign in; its past check-ins keep its name.</div></div>')
    main = f'<div class="cols"><div style="width:380px;flex:none">{left}</div><div style="flex:1;min-width:0">{right}</div></div>'
    win = desktop("signed in as manager", {"Business parameters", "Staff accounts"}, main)
    return "B7", "Business parameters and staff accounts", "UC-07; UC-08", win


# --------------------------------------------------------------------------------------------------------------- figures
def cell(sid, title, steps, inner, desk=False):
    """One captioned screen; the caption may wrap between step ids, never inside one ("EF-3", "1&ndash;2")."""
    parts = re.split(r"(, |; )", steps)
    st = "".join(t if t in (", ", "; ") else f'<span class="nb">{t}</span>' for t in parts)
    return f'<div class="cell {"desk" if desk else "ph"}"><div class="cap">{sid} &middot; {title} <span>&middot; {st}</span></div>{inner}</div>'


# One image per screen, no caption: the document puts the description beside or under it (Appendix D). B6 shows its
# two states side by side, each with a state label.
SINGLES = [("screen-c1", [c1], False), ("screen-c2", [c2], False), ("screen-c3", [c3], False), ("screen-c4", [c4], False),
           ("screen-c5", [c5], False), ("screen-c6", [c6], False), ("screen-c7", [c7], False), ("screen-c8", [c8], False),
           ("screen-c9", [c9], False), ("screen-b1", [b1], True), ("screen-b2", [b2], True), ("screen-b3", [b3], True),
           ("screen-b4", [b4], True), ("screen-b5", [b5], False), ("screen-b6", [b6_result, b6_confirmed], False), ("screen-b7", [b7], True)]


def png_size(path):
    with open(path, "rb") as f:
        f.seek(16)
        return struct.unpack(">II", f.read(8))




def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pages = []
    for stem, fns, desk in SINGLES:
        cells = []
        for fn in fns:
            sid, title, _steps, inner = fn()
            label = f'<div class="cap">{title}</div>' if len(fns) > 1 else ""   # the state of a two-state screen
            cells.append(f'<div class="cell {"desk" if desk else "ph"}">{label}{inner}</div>')
        f = OUT / f"{stem}.html"
        f.write_text(page(stem, "".join(cells), desk=desk), encoding="utf-8")
        pages.append(f)
        print("wrote", f.relative_to(GROUP))
    from playwright.sync_api import sync_playwright  # imported lazily: slow
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(device_scale_factor=2, viewport={"width": 1600, "height": 1200})
        page_ = ctx.new_page()
        for f in pages:
            page_.goto(f.as_uri(), wait_until="networkidle")
            page_.wait_for_timeout(200)  # let the fonts settle
            out = f.with_suffix(".png")
            page_.locator("div.figure").first.screenshot(path=str(out), scale="device")
            w, h = png_size(out)
            print(f"wrote {out.relative_to(GROUP)}  {w}x{h}")
        ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
