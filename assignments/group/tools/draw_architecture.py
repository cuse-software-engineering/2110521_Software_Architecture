#!/usr/bin/env python3
"""Draw the SEATS microservice architecture diagram (project document Figure 5.1) and render it.

Writes workspace/report/project-document/assets/architecture-diagram.html (one inline SVG, the editable source of the
figure) and renders assets/architecture-diagram.png with headless Chromium at 2x (Playwright). Every element and arrow is
placed by coordinates below: move a service by changing its hexagon() call and adjust the arrows that touch it.
Only the MVP is drawn (Section 5 of the document). Arrows marked grpc=True are purple (gRPC: the API Gateway to the
services and between services, ADR-12); the others are REST or HTTPS. Every service has one API, gRPC, drawn as a tab on
each side it is called from; the API Gateway has the only REST tab. The three dashed boundaries are the parts of the system of Section 5.2.

Usage (from the repository root):  python3 assignments/group/tools/draw_architecture.py
"""
import sys
from html import escape
from pathlib import Path

GROUP = Path(__file__).resolve().parent.parent
OUT = str(GROUP / "workspace/report/project-document/assets/architecture-diagram.html")
W, H = 1925, 1010
S = []                                   # svg elements
DARK, PURPLE = "#3E4C59", "#6B46C1"

def text(x, y, lines, size=15, weight="normal", anchor="middle", color="#1F2933", style="normal", lh=None):
    lh = lh or size * 1.25
    lines = [lines] if isinstance(lines, str) else lines
    y0 = y - (len(lines) - 1) * lh / 2
    t = "".join(f'<tspan x="{x}" y="{y0 + i*lh:.1f}">{escape(l)}</tspan>' for i, l in enumerate(lines))
    S.append(f'<text font-size="{size}" font-weight="{weight}" font-style="{style}" text-anchor="{anchor}" fill="{color}" dominant-baseline="middle">{t}</text>')

def box(x, y, w, h, title, sub=None, fill="#fff", stroke=DARK, dash=None, r=10, tsize=16, ssize=13):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    S.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"{d}/>')
    if sub:
        subl = [sub] if isinstance(sub, str) else sub
        th, sh = tsize * 1.3, ssize * 1.3
        top = y + h/2 - (th + sh * len(subl)) / 2
        text(x + w/2, top + th/2, title, tsize, "bold")
        text(x + w/2, top + th + sh * len(subl) / 2, subl, ssize, color="#52606D", lh=sh)
    else:
        text(x + w/2, y + h/2, title, tsize, "bold")

def boundary(x, y, w, h, label, lx, ly):
    """A part of the system (Section 5.2): dashed outline, label in its corner."""
    S.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="none" stroke="#7B8794" stroke-width="2" stroke-dasharray="10 6"/>')
    text(lx, ly, label, 16, "bold", anchor="start", color="#52606D", style="italic")

def person(cx, cy, color="#B7950B"):
    S.append(f'<circle cx="{cx}" cy="{cy-22}" r="11" fill="{color}"/>'
             f'<path d="M{cx-15},{cy+26} L{cx-15},{cy-4} Q{cx-15},{cy-10} {cx-9},{cy-10} L{cx+9},{cy-10} Q{cx+15},{cy-10} {cx+15},{cy-4} L{cx+15},{cy+26} Z" fill="{color}"/>')

def actor(x, y, name, sub=None, icon=True):
    if icon:
        person(x - 30, y + 25)
    box(x, y, 140, 50, name, sub, fill="#FFF6D5", stroke="#C9A227", r=25, tsize=16, ssize=11)

def tab(x, y, kind):
    """Driving port: the REST tab of the API Gateway, or the gRPC tab of a service (drawn on each side it is called from)."""
    if kind == "REST":
        S.append(f'<rect x="{x-19}" y="{y-12}" width="38" height="24" rx="4" fill="#fff" stroke="{DARK}" stroke-width="1.6"/>')
        text(x, y, "REST", 11, "bold", color=DARK)
    else:
        S.append(f'<rect x="{x-20}" y="{y-12}" width="40" height="24" rx="4" fill="#fff" stroke="{PURPLE}" stroke-width="1.8"/>')
        text(x, y, "gRPC", 11, "bold", color=PURPLE)

HEX = {}
def hexagon(name, cx, cy, w, h, d, desc, db, tabs, tsize=17, desc_dx=-8, db_at=None):
    """tabs: [(kind, where, offset)] with where in left/right/top/bottom; offset moves a top/bottom tab along the edge.
    db_at: (dx, dy) of the data store from the centre; by default bottom right."""
    pts = [(cx-w, cy), (cx-w+d, cy-h), (cx+w-d, cy-h), (cx+w, cy), (cx+w-d, cy+h), (cx-w+d, cy+h)]
    S.append('<polygon points="' + " ".join(f"{a:.0f},{b:.0f}" for a, b in pts) + '" fill="#EFE9F8" stroke="#6B46C1" stroke-width="2.2"/>')
    text(cx, cy - h + 26, name, tsize, "bold")
    text(cx + desc_dx, cy + 8, desc, 12.5, color="#3E4C59", lh=15)
    dx, dy = (cx + db_at[0], cy + db_at[1]) if db_at else (cx + w - d - 40, cy + h - 32)
    S.append(f'<path d="M{dx-17},{dy-8} v18 a17,6 0 0 0 34,0 v-18" fill="#fff" stroke="#6B46C1" stroke-width="1.6"/>'
             f'<ellipse cx="{dx}" cy="{dy-8}" rx="17" ry="6" fill="#fff" stroke="#6B46C1" stroke-width="1.6"/>')
    text(dx, dy + 24, db, 11, color="#52606D", style="italic")
    for kind, where, off in tabs:
        x, y = {"left": (cx - w, cy), "right": (cx + w, cy), "top": (cx + off, cy - h), "bottom": (cx + off, cy + h)}[where]
        tab(x, y, kind)
    HEX[name] = (cx, cy, w, h, d)

def arrow(path, grpc=False, label=None, lx=None, ly=None, lanchor="middle", lsize=12):
    color = PURPLE if grpc else DARK
    S.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2" marker-end="url(#{"ap" if grpc else "ad"})"/>')
    if label:
        text(lx, ly, label, lsize, anchor=lanchor, color="#553C9A" if grpc else "#52606D", style="italic", lh=lsize * 1.2)

# ---------------- parts of the system (Section 5.2)
boundary(252, 132, 252, 460, "Frontend", 266, 572)
boundary(522, 34, 1136, 946, "Backend", 536, 962)
boundary(1674, 34, 220, 894, "External systems", 1688, 910)

# ---------------- actors
actor(90, 175, "Customer")
actor(90, 375, "Front Staff", "scans at the door")
actor(90, 475, "Manager", "runs the back-office")
actor(90, 615, "Time", "scheduled triggers", icon=False)

# ---------------- frontend, gateway
box(280, 170, 196, 74, "Customer Web App", ["(LIFF, inside", "LINE Messenger)"], fill="#E3F0FC", stroke="#2B6CB0")
box(280, 420, 196, 82, "Back-office Web App", ["rounds, live view,", "QR scan on phone"], fill="#E3F0FC", stroke="#2B6CB0")
box(566, 330, 160, 124, "API Gateway", ["REST in, gRPC out;", "verifies caller", "identity and role"], fill="#E6F4EA", stroke="#2F855A")
tab(566, 392, "REST")                    # the REST API that the Frontend calls (FTGO draws the gateway the same way)

# ---------------- services (hexagon = one business capability; tabs = its APIs)
hexagon("Table Availability Service", 930, 232, 132, 72, 36, ["read model of the table map:", "per-round table status", "(ADR-13)"], "Table Status DB",
        [("gRPC", "left", 0), ("gRPC", "right", 0)])
hexagon("Concert Round Service", 1334, 262, 128, 88, 38, ["venue zone map, tables,", "table types; rounds,", "prices, check-in window,", "business parameters"], "Round DB",
        [("gRPC", "top", -30), ("gRPC", "left", 0)], tsize=16)
hexagon("Booking Service", 972, 490, 142, 100, 46, ["booking lifecycle: hold", "(first lock wins), fee,", "profile, terms,", "confirmation, e-ticket,", "check-in, hold expiry"], "Booking DB",
        [("gRPC", "left", 0), ("gRPC", "bottom", 68)], desc_dx=-34, db_at=(80, 4))
hexagon("Payment Service", 990, 772, 128, 80, 38, ["payment requests,", "signed payment result", "(simulated gateway)"], "Payment DB",
        [("gRPC", "left", 0), ("gRPC", "top", -10)])
hexagon("Notification Service", 1382, 606, 110, 62, 28, ["LINE messages,", "retries"], "Notification DB",
        [("gRPC", "left", 0)], tsize=16, desc_dx=-30, db_at=(46, 18))
hexagon("Staff Account Service", 660, 712, 124, 80, 32, ["back-office accounts,", "roles, sign-in"], "Staff Account DB",
        [("gRPC", "top", 0)], tsize=15, desc_dx=0, db_at=(40, 44))

# ---------------- adapters (modules of the component that uses them) and external systems
AD = "#FEF1E1"; ADS = "#DD6B20"; EX = "#FDECEC"; EXS = "#C53030"
box(1496, 42, 150, 50, "LINE Login", "Adapter", fill=AD, stroke=ADS, tsize=15, ssize=12)
box(1698, 42, 182, 50, "LINE Login Platform", "external", fill=EX, stroke=EXS, dash="7 5", tsize=14, ssize=12)
box(1506, 290, 140, 58, "Media Storage", "Adapter", fill=AD, stroke=ADS, tsize=15, ssize=12)
box(1698, 290, 182, 58, "Cloud Object Storage", "external", fill=EX, stroke=EXS, dash="7 5", tsize=14, ssize=12)
box(1520, 577, 126, 58, "LINE Messaging", "Adapter", fill=AD, stroke=ADS, tsize=14, ssize=12)
box(1698, 577, 182, 58, "LINE Messaging API", "external", fill=EX, stroke=EXS, dash="7 5", tsize=14, ssize=12)
box(1496, 808, 150, 58, "Payment Gateway", "Adapter", fill=AD, stroke=ADS, tsize=15, ssize=12)
box(1698, 782, 182, 110, "Payment Gateway", ["external", "simulated in the MVP", "(ADR-11)"], fill=EX, stroke=EXS, dash="7 5", tsize=14, ssize=11)

# ---------------- actors to the frontend
arrow("M230,200 L274,204")
arrow("M230,400 C252,402 256,448 274,452")
arrow("M230,500 C252,500 256,478 274,476")
# frontend to the gateway (REST over HTTPS) and to LINE Login
arrow("M378,170 L378,20 L1789,20 L1789,36", label="LINE Login in the LIFF app", lx=1120, ly=9, lsize=11.5)
arrow("M476,214 C512,226 520,330 545,388")
arrow("M476,462 C506,460 520,436 545,396")
# gateway: customer identity through its LINE Login Adapter
arrow("M612,330 L612,67 L1490,67", label="verify ID token", lx=626, ly=56, lanchor="start", lsize=11.5)
arrow("M1646,67 L1692,67")
# payment result: the external gateway calls the API Gateway (signed webhook)
arrow("M1880,837 L1914,837 L1914,104 L660,104 L660,324", label="payment result (signed webhook)", lx=1180, ly=94, lsize=11.5)
# gateway to the services (gRPC: one call per REST route, ADR-12)
arrow("M700,330 L700,128 L1304,128 L1304,162", grpc=True)
arrow("M726,344 C760,320 760,240 777,236", grpc=True)
arrow("M726,404 C760,420 790,480 809,488", grpc=True)
arrow("M726,446 C812,480 812,720 841,768", grpc=True)
arrow("M660,454 L660,618", grpc=True)
# service to service (gRPC)
arrow("M1222,214 L1086,230", grpc=True, label=["createRoundTableStatus()", "getRoundTableStatus()", "countAvailableTables()"], lx=1150, ly=176, lsize=11)
arrow("M1062,392 L1062,258", grpc=True, label=["holdTable(), releaseHold(),", "markTableBooked(),", "markTableOccupied()"], lx=1052, ly=346, lanchor="end", lsize=11)
arrow("M1098,428 C1150,390 1168,300 1184,272", grpc=True, label=["getRound()", "getRoundPricing()", "getCheckInWindow()"], lx=1132, ly=432, lanchor="start", lsize=11)
arrow("M980,592 L980,678", grpc=True, label="createPaymentRequest()", lx=970, ly=636, lanchor="end", lsize=11)
arrow("M1040,692 L1040,616", grpc=True, label="confirmBookingPayment()", lx=1050, ly=652, lanchor="start", lsize=11)
arrow("M1088,552 C1160,580 1220,600 1250,604", grpc=True, label=["sendBookingConfirmation()", "sendHoldExpiredNotice()"], lx=1150, ly=520, lanchor="start", lsize=11)
arrow("M1118,772 C1200,772 1236,650 1252,616", grpc=True, label="sendPaymentFailedNotice()", lx=1236, ly=748, lanchor="start", lsize=11)
# services to their adapters (in-process), adapters to external systems (HTTPS)
arrow("M1462,262 C1480,262 1486,300 1500,310")
arrow("M1492,606 L1514,606")
arrow("M1100,812 C1250,850 1400,846 1490,840")
arrow("M1646,319 L1692,319")
arrow("M1646,606 L1692,606")
arrow("M1646,837 L1692,837")
# Time: the Booking Service's own job releases unpaid holds every 5 seconds (ADR-08)
arrow("M230,640 C440,618 640,590 848,552", label="expire unpaid holds", lx=250, ly=668, lanchor="start", lsize=11.5)

# ---------------- legend
lx, ly = 30, 838
S.append(f'<rect x="{lx}" y="{ly}" width="470" height="160" rx="8" fill="#F8F9FA" stroke="#CBD2D9"/>')
text(lx + 14, ly + 18, "Legend (the MVP only)", 14, "bold", anchor="start")
rows = [("part", "grey dashed outline: part of the system (Section 5.2)"),
        ("rest", "A → B: A invokes B by REST or HTTPS (JSON)"),
        ("grpc", "A → B: A invokes B by gRPC (ADR-12)"),
        ("tabs", "REST / gRPC tab: the API a component offers"),
        ("hex", "hexagon: service; cylinder: its private database"),
        ("ad", "orange box: adapter, part of the component that uses it"),
        ("box", "red dashed box: external system")]
for i, (k, desc) in enumerate(rows):
    y = ly + 40 + i * 17
    if k in ("rest", "grpc"):
        col, mk = (DARK, "ad") if k == "rest" else (PURPLE, "ap")
        S.append(f'<path d="M{lx+16},{y} L{lx+70},{y}" stroke="{col}" stroke-width="2" marker-end="url(#{mk})"/>')
    text(lx + 86, y, desc, 12, anchor="start", color="#3E4C59")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">'
       f'<defs><marker id="ad" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
       f'<path d="M0,0 L10,5 L0,10 z" fill="{DARK}"/></marker>'
       f'<marker id="ap" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
       f'<path d="M0,0 L10,5 L0,10 z" fill="{PURPLE}"/></marker></defs>'
       f'<rect width="{W}" height="{H}" fill="#fff"/>' + "".join(S) + "</svg>")
html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>SEATS microservice architecture, version 2</title>
<!-- Source of assets/architecture-diagram.png (project document v2.0, CH-37, CH-40). Rendered with headless Chromium
     at 2x: the screenshot covers div.canvas. The MVP only; purple arrows are gRPC calls (ADR-12). -->
<style>body {{ margin: 0; background: #fff; }} .canvas {{ width: {W}px; height: {H}px; }}</style>
</head><body><div class="canvas">{svg}</div></body></html>
"""
open(OUT, "w", encoding="utf-8").write(html)
print("wrote", OUT)


def render() -> None:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=2)
        page.goto(Path(OUT).resolve().as_uri())
        page.locator(".canvas").screenshot(path=OUT[:-5] + ".png")
        browser.close()
    print("wrote", OUT[:-5] + ".png")



JS = r"""
() => {
  const svg = document.querySelector('svg');
  const W = +svg.getAttribute('width');
  const all = [...svg.querySelectorAll('polygon, rect, ellipse, circle, path')];
  const arrows = all.filter(e => e.tagName === 'path' && e.getAttribute('marker-end'));
  const shapes = all.filter(e => !arrows.includes(e)
      && !(e.getAttribute('fill') === 'none')               // group outlines
      && !(e.tagName === 'rect' && +e.getAttribute('width') >= W - 1));   // background
  const legend = [...svg.querySelectorAll('rect')].find(r => r.getAttribute('fill') === '#F8F9FA');
  const lb = legend.getBBox();
  const inLegend = b => b.x >= lb.x && b.y >= lb.y && b.x + b.width <= lb.x + lb.width && b.y + b.height <= lb.y + lb.height;
  const texts = [...svg.querySelectorAll('text')].filter(t => !inLegend(t.getBBox()));
  const desc = e => { const b = e.getBBox(); return `${e.tagName}@(${Math.round(b.x)},${Math.round(b.y)} ${Math.round(b.width)}x${Math.round(b.height)})`; };
  const near = e => { // name a shape by the text whose centre is inside its box
    const b = e.getBBox(); const t = texts.find(t => { const c = t.getBBox(); const cx = c.x + c.width/2, cy = c.y + c.height/2;
      return cx > b.x && cx < b.x + b.width && cy > b.y && cy < b.y + b.height && c.width > 20; });
    return t ? t.textContent.slice(0, 28) : desc(e); };
  const out = [];
  for (const a of arrows) {
    if (inLegend(a.getBBox())) continue;
    const L = a.getTotalLength(), d0 = a.getAttribute('d').split(' ')[0];
    const hits = new Map();
    for (let s = 6; s <= L - 6; s += 2) {
      const p = a.getPointAtLength(s), pt = new DOMPoint(p.x, p.y);
      for (const sh of shapes) if (sh.isPointInFill(pt)) { const k = 'shape: ' + near(sh); if (!hits.has(k)) hits.set(k, [Math.round(p.x), Math.round(p.y)]); }
      for (const t of texts) { const b = t.getBBox();
        if (p.x > b.x + 1 && p.x < b.x + b.width - 1 && p.y > b.y + 1 && p.y < b.y + b.height - 1) {
          const k = 'text: ' + t.textContent.slice(0, 30); if (!hits.has(k)) hits.set(k, [Math.round(p.x), Math.round(p.y)]); } }
    }
    for (const [k, v] of hits) out.push(`arrow ${d0} ... crosses ${k} at ${v}`);
  }
  // arrow labels (italic text) must not overlap a shape; a data-store label must lie inside its own service
  for (const t of texts.filter(t => t.getAttribute('font-style') === 'italic' && !t.textContent.endsWith(' DB') && !['Frontend', 'Backend', 'External systems'].includes(t.textContent))) {
    const b = t.getBBox();
    for (const sh of shapes) {
      const pts = [[b.x+2,b.y+2],[b.x+b.width-2,b.y+2],[b.x+2,b.y+b.height-2],[b.x+b.width-2,b.y+b.height-2],[b.x+b.width/2,b.y+b.height/2]];
      if (pts.some(([x,y]) => sh.isPointInFill(new DOMPoint(x,y)))) { const n = near(sh);
        if (!n.startsWith(t.textContent.slice(0, 10))) out.push(`label "${t.textContent.slice(0, 34)}" overlaps shape ${n}`); break; }
    }
  }
  for (const t of texts.filter(t => t.textContent.endsWith(' DB'))) {
    const b = t.getBBox(), c = new DOMPoint(b.x + b.width / 2, b.y + b.height / 2);
    const own = shapes.find(s => s.tagName === 'polygon' && s.isPointInFill(c));
    const corners = [[b.x, b.y], [b.x + b.width, b.y], [b.x, b.y + b.height], [b.x + b.width, b.y + b.height]];
    if (!own || !corners.every(([x, y]) => own.isPointInFill(new DOMPoint(x, y)))) out.push(`data-store label "${t.textContent}" leaves its service`);
  }
  // labels must not overlap each other
  const labs = texts.filter(t => t.getAttribute('font-style') === 'italic');
  for (let i = 0; i < labs.length; i++) for (let j = i + 1; j < labs.length; j++) {
    const a = labs[i].getBBox(), b = labs[j].getBBox();
    if (a.x < b.x + b.width && b.x < a.x + a.width && a.y < b.y + b.height && b.y < a.y + a.height)
      out.push(`labels overlap: "${labs[i].textContent.slice(0, 24)}" / "${labs[j].textContent.slice(0, 24)}"`);
  }
  return out;
}
"""


def check() -> None:
    """Every arrow sampled every 2 px against every shape and every text box (the first and last 6 px, where it
    leaves its source and meets its target, are allowed); labels against shapes and each other."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(Path(OUT).resolve().as_uri())
        problems = page.evaluate(JS)
        browser.close()
    print("\n".join(problems) if problems else "geometry: no overlaps")


render()
check()
