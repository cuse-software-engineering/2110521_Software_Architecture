#!/usr/bin/env python3
"""Draw the SEATS use case diagram of the project document (Figure 2.1) in the style of the 2110628 report and render it.

Adapted from the 2110628 repository's assignments/group/tools/build_usecase_diagrams.py (same SVG drawing and geometry
checks: no edge may pass through a node it does not end at, edges should not cross, nodes must not overlap). Writes
workspace/report/project-document/assets/use-case-diagram.html (the editable source) and renders
use-case-diagram.png next to it with headless Chromium at 2x.

Usage (from the repository root):  python3 assignments/group/tools/draw_use_case_diagram.py
"""
import math, sys
from pathlib import Path

import os, json
DIAGRAMS = Path(__file__).resolve().parent.parent / "workspace" / "report" / "project-document" / "assets"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else DIAGRAMS / "use-case-diagram.html"
OVR = json.loads(os.environ.get("UCD_OVR", "{}"))

W, H = 1200, 745
RX, RY = 118, 38
BOX_W, BOX_H = 176, 66
FS_NAME, FS_ID, FS_ACT, FS_REL = 19, 15, 18, 15
LINE_H = 21

# Use cases in one column in the order of use (UC-04 -> UC-03 -> UC-01 -> UC-02); people on the left, the external
# systems and Time on the right. The Manager's associations with UC-01 (transfer-slip review) and UC-02 (escalation)
# are secondary and belong to Increment 2 flows; the one crossing they cause (Manager-UC-02 over Customer-UC-01) is
# accepted rather than leaving them out, so that the diagram shows every actor of Table 2.1.
BOUND = dict(x=250, y=15, w=700, h=710)
UC = {
    "UC-04": dict(x=600, y=115, name=["Create Venue", "Zone Map"]),
    "UC-03": dict(x=600, y=250, name=["Create", "Concert Event"]),
    "UC-01": dict(x=600, y=430, name=["Reserve a", "Specific Table"]),
    "UC-02": dict(x=600, y=620, name=["Check In Using", "Digital QR Ticket"]),
}
ACT = {
    "Manager":    dict(x=100, y=182, name=["Manager"]),
    "Customer":   dict(x=100, y=480, name=["Customer"]),
    "FrontStaff": dict(x=100, y=660, name=["Front Staff"]),
    "PG":         dict(x=1080, y=320, box=True, name=["Payment Gateway"]),
    "LINE":       dict(x=1080, y=450, box=True, name=["LINE Platform"]),
    "Time":       dict(x=1080, y=600, name=["Time"], stereo="«timer»"),
}
ASSOC = [
    ("Manager", "UC-04"), ("Manager", "UC-03"), ("Manager", "UC-01"), ("Manager", "UC-02"),
    ("Customer", "UC-01"), ("Customer", "UC-02"),
    ("FrontStaff", "UC-02"),
    ("PG", "UC-01"), ("LINE", "UC-01"), ("Time", "UC-01"), ("Time", "UC-02"),
]
EXTEND = []
INCLUDE = []
GEN = []
TITLE = "Seating & Event Availability Tracking System (SEATS)"
for k, v in OVR.get("UC", {}).items(): UC[k].update(v)
for k, v in OVR.get("ACT", {}).items(): ACT[k].update(v)
for k, v in OVR.get("EXTEND", {}).items():
    EXTEND[:] = [tuple([e[0], e[1], e[2], v[0], v[1], e[5]]) if f"{e[0]}->{e[1]}" == k else e for e in EXTEND]
for k, v in OVR.get("INCLUDE", {}).items():
    INCLUDE[:] = [tuple([e[0], e[1], e[2], v[0], v[1], e[5]]) if f"{e[0]}->{e[1]}" == k else e for e in INCLUDE]

# ---------------- geometry ----------------
for u in UC.values():
    u["rx"], u["ry"] = RX, RY
for a in ACT.values():
    if a.get("box"):
        a["hw"], a["hh"] = BOX_W / 2, BOX_H / 2
    else:
        a["hw"], a["hh"] = 20, 32


def anchor(n, p):
    dx, dy = p["x"] - n["x"], p["y"] - n["y"]
    if "rx" in n:
        t = math.atan2(dy / n["ry"], dx / n["rx"])
        return (n["x"] + n["rx"] * math.cos(t), n["y"] + n["ry"] * math.sin(t))
    sx = n["hw"] / abs(dx or 1e-9)
    sy = n["hh"] / abs(dy or 1e-9)
    s = min(sx, sy)
    return (n["x"] + dx * s, n["y"] + dy * s)


def node(name):
    return UC[name] if name in UC else ACT[name]


def inside(n, x, y, margin=8):
    if "rx" in n:
        return ((x - n["x"]) / (n["rx"] + margin)) ** 2 + ((y - n["y"]) / (n["ry"] + margin)) ** 2 < 1
    return abs(x - n["x"]) < n["hw"] + margin and abs(y - n["y"]) < n["hh"] + margin


def seg_hits(seg, exclude):
    (x1, y1), (x2, y2) = seg
    hits = []
    for name, n in list(UC.items()) + list(ACT.items()):
        if name in exclude:
            continue
        for k in range(1, 60):
            t = k / 60
            if inside(n, x1 + (x2 - x1) * t, y1 + (y2 - y1) * t):
                hits.append(name)
                break
    return hits


def cross(s1, s2):
    (ax, ay), (bx, by) = s1
    (cx, cy), (dx, dy) = s2
    def orient(px, py, qx, qy, rx, ry):
        return (qx - px) * (ry - py) - (qy - py) * (rx - px)
    o1, o2 = orient(ax, ay, bx, by, cx, cy), orient(ax, ay, bx, by, dx, dy)
    o3, o4 = orient(cx, cy, dx, dy, ax, ay), orient(cx, cy, dx, dy, bx, by)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    return False


segments = []   # (label, seg, endpoints)
for a, u in ASSOC:
    na, nu = node(a), node(u)
    segments.append((f"{a}-{u}", (anchor(na, nu), anchor(nu, na)), {a, u}))
for f, t, *_ in EXTEND + INCLUDE:
    segments.append((f"{f}->{t}", (anchor(UC[f], UC[t]), anchor(UC[t], UC[f])), {f, t}))
# generalisation: children -> bus -> parent (the bus always reaches the parent's y, so an off-centre parent stays connected)
def gen_lines(g):
    bx, P = g["bus_x"], UC[g["parent"]]
    ys = [UC[c]["y"] for c in g["children"]]
    stubs = [((UC[c]["x"] - RX, UC[c]["y"]), (bx, UC[c]["y"])) for c in g["children"]]
    bus = ((bx, min(ys + [P["y"]])), (bx, max(ys + [P["y"]])))
    arrow = ((bx, P["y"]), (P["x"] + RX, P["y"]))
    return stubs, bus, arrow
for gi, g in enumerate(GEN):
    stubs, bus, arrow = gen_lines(g)
    for c, st in zip(g["children"], stubs):
        segments.append((f"gen{gi}-{c}", st, {c}))
    segments.append((f"gen{gi}-bus", bus, set()))
    segments.append((f"gen{gi}-arrow", arrow, {g["parent"]}))

problems = []
for label, seg, ends in segments:
    h = seg_hits(seg, ends)
    if h:
        problems.append(f"edge {label} passes through {h}")
for i in range(len(segments)):
    for j in range(i + 1, len(segments)):
        l1, s1, e1 = segments[i]
        l2, s2, e2 = segments[j]
        if e1 & e2:
            continue          # share a node: they meet at it, not a crossing
        if l1.startswith("gen") and l2.startswith("gen") and l1.split("-")[0] == l2.split("-")[0]:
            continue          # one generalization tree: its stubs, bus and arrow meet by design
        if cross(s1, s2):
            problems.append(f"edges cross: {l1} x {l2}")
# labels of extend / include edges vs nodes / other edges (approximate box)
for f, t, lines, lx, ly, anc in EXTEND + INCLUDE:
    w = max(len(s) for s in lines) * FS_REL * 0.55
    h = len(lines) * 18
    x0 = lx - w / 2 if anc == "middle" else (lx - w if anc == "end" else lx)
    box = (x0, ly - 14, x0 + w, ly - 14 + h)
    for name, n in list(UC.items()) + list(ACT.items()):
        cx, cy = min(max(n["x"], box[0]), box[2]), min(max(n["y"], box[1]), box[3])
        if inside(n, cx, cy, margin=2) or inside(n, box[0], box[1], 2) or inside(n, box[2], box[3], 2) or inside(n, box[0], box[3], 2) or inside(n, box[2], box[1], 2):
            problems.append(f"label of {f}->{t} overlaps {name}")
    for label, seg, ends in segments:
        if label == f"{f}->{t}":
            continue
        (x1, y1), (x2, y2) = seg
        for k in range(0, 41):
            tt = k / 40
            px, py = x1 + (x2 - x1) * tt, y1 + (y2 - y1) * tt
            if box[0] <= px <= box[2] and box[1] <= py <= box[3]:
                problems.append(f"label of {f}->{t} sits on edge {label}")
                break
# nodes inside the boundary; actors outside
for name, u in UC.items():
    if not (BOUND["x"] + 10 < u["x"] - RX and u["x"] + RX < BOUND["x"] + BOUND["w"] - 10 and BOUND["y"] + 40 < u["y"] - RY and u["y"] + RY < BOUND["y"] + BOUND["h"] - 10):
        problems.append(f"{name} not inside the boundary")
names = list(UC.items())
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        a, b = names[i][1], names[j][1]
        if abs(a["x"] - b["x"]) < 2 * RX + 20 and abs(b["y"] - a["y"]) < 2 * RY + 12:
            problems.append(f"{names[i][0]} and {names[j][0]} too close")

# ---------------- SVG ----------------
o = []
def add(s): o.append(s)
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")
def text(x, y, lines, cls, anchor_="middle", line_h=LINE_H):
    t = [f'<text x="{x}" y="{y}" text-anchor="{anchor_}" class="{cls}">']
    for i, ln in enumerate(lines):
        c, s = (ln["cls"], ln["t"]) if isinstance(ln, dict) else ("", ln)
        t.append(f'<tspan x="{x}" dy="{0 if i == 0 else line_h}"{f" class=\"{c}\"" if c else ""}>{esc(s)}</tspan>')
    t.append("</text>")
    add("".join(t))

add(f'<!doctype html><html><head><meta charset="utf-8"><title>SEATS use-case diagram</title>')
add("""<style>
  body { margin: 0; background: #fff; font-family: "Noto Sans", "Liberation Sans", Arial, sans-serif; }
  .figure { width: %dpx; height: %dpx; background: #fff; }
  svg text { font-family: "Noto Sans", "Liberation Sans", Arial, sans-serif; fill: #111; }
  .uc-id { font-size: %dpx; fill: #555; }
  .uc-name { font-size: %dpx; }
  .actor-name { font-size: %dpx; }
  .stereo { font-size: 14px; font-style: italic; fill: #333; }
  .rel { font-size: %dpx; font-style: italic; fill: #1f3a5f; }
  .guard { font-size: %dpx; font-style: normal; fill: #1f3a5f; }
  .title { font-size: 21px; font-weight: 600; }
</style></head><body>""" % (W, H, FS_ID, FS_NAME, FS_ACT, FS_REL, FS_REL))
add(f'<div class="figure"><svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add('<defs>'
    '<marker id="open" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" orient="auto" markerUnits="userSpaceOnUse">'
    '<path d="M2 2 L15 8 L2 14" fill="none" stroke="#1f3a5f" stroke-width="1.4" stroke-linejoin="miter"/></marker>'
    '<marker id="tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" orient="auto" markerUnits="userSpaceOnUse">'
    '<path d="M1 1.5 L15 8 L1 14.5 Z" fill="#fff" stroke="#1f3a5f" stroke-width="1.4" stroke-linejoin="miter"/></marker>'
    '</defs>')
add(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>')
add(f'<rect x="{BOUND["x"]}" y="{BOUND["y"]}" width="{BOUND["w"]}" height="{BOUND["h"]}" fill="#f8fafc" stroke="#1f3a5f" stroke-width="1.6"/>')
text(BOUND["x"] + 18, BOUND["y"] + 30, [TITLE], "title", "start")

def line(p1, p2, dashed=False, marker=None):
    a = f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="#1f3a5f" stroke-width="1.5"'
    if dashed: a += ' stroke-dasharray="7 5"'
    if marker: a += f' marker-end="url(#{marker})"'
    add(a + "/>")

for a, u in ASSOC:
    na, nu = node(a), node(u)
    line(anchor(na, nu), anchor(nu, na))
for f, t, lines, lx, ly, anc in EXTEND + INCLUDE:
    line(anchor(UC[f], UC[t]), anchor(UC[t], UC[f]), dashed=True, marker="open")
    text(lx, ly, [{"t": lines[0], "cls": "rel"}] + [{"t": s, "cls": "guard"} for s in lines[1:]], "", anc, 18)
for g in GEN:
    stubs, bus, arrow = gen_lines(g)
    for st in stubs:
        line(*st)
    line(*bus)
    line(*arrow, marker="tri")

for name, u in UC.items():
    add(f'<ellipse cx="{u["x"]}" cy="{u["y"]}" rx="{RX}" ry="{RY}" fill="#fff" stroke="#1f3a5f" stroke-width="1.6"/>')
    lines = [{"t": name, "cls": "uc-id"}] + [{"t": s, "cls": "uc-name"} for s in u["name"]]
    total = 15 + LINE_H * len(u["name"])
    text(u["x"], u["y"] - total / 2 + 12, lines, "", "middle", LINE_H)
for name, a in ACT.items():
    if a.get("box"):
        add(f'<rect x="{a["x"] - BOX_W / 2}" y="{a["y"] - BOX_H / 2}" width="{BOX_W}" height="{BOX_H}" fill="#fff" stroke="#1f3a5f" stroke-width="1.6"/>')
        text(a["x"], a["y"] - BOX_H / 2 + 19, [{"t": "«actor»", "cls": "stereo"}] + [{"t": s, "cls": "actor-name"} for s in a["name"]], "", "middle", 18)
    else:
        x, y = a["x"], a["y"]
        add(f'<g stroke="#1f3a5f" stroke-width="1.8" fill="#fff" stroke-linecap="round">'
            f'<circle cx="{x}" cy="{y - 21}" r="10"/><line x1="{x}" y1="{y - 11}" x2="{x}" y2="{y + 12}"/>'
            f'<line x1="{x - 18}" y1="{y - 3}" x2="{x + 18}" y2="{y - 3}"/>'
            f'<line x1="{x}" y1="{y + 12}" x2="{x - 15}" y2="{y + 31}"/><line x1="{x}" y1="{y + 12}" x2="{x + 15}" y2="{y + 31}"/></g>')
        lines = ([{"t": a["stereo"], "cls": "stereo"}] if a.get("stereo") else []) + [{"t": s, "cls": "actor-name"} for s in a["name"]]
        text(x, y + 50, lines, "", "middle", 18)
add("</svg></div></body></html>")
OUT.write_text("\n".join(o) + "\n", encoding="utf-8")
if os.environ.get("UCD_QUIET"):
    print(len(problems)); [print(p) for p in problems] if os.environ.get("UCD_VERBOSE") else None
else:
    print(f"wrote {OUT}")
    print("\n".join(problems) if problems else "geometry: no problems")

def render() -> None:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=2)
        page.goto(OUT.resolve().as_uri())
        page.locator(".figure").screenshot(path=str(OUT.with_suffix(".png")))
        browser.close()
    print(f"wrote {OUT.with_suffix('.png')}")


render()
