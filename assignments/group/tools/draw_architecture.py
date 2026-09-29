#!/usr/bin/env python3
"""Draw the SEATS microservice architecture diagram (project document Figure 5.1) and render it.

Writes workspace/report/project-document/assets/architecture-diagram.html (one inline SVG, the editable source of the
figure) and renders assets/architecture-diagram.png with headless Chromium at 2x (Playwright). Every element and arrow is
placed by coordinates below: move a service by changing its hexagon() call and adjust the arrows that touch it.
Arrows marked inc2=True are drawn grey and dashed (added in Increment 2); dotted=True is a server-initiated push.

Usage (from the repository root):  python3 assignments/group/tools/draw_architecture.py
"""
import sys
from html import escape
from pathlib import Path

GROUP = Path(__file__).resolve().parent.parent
OUT = str(GROUP / "workspace/report/project-document/assets/architecture-diagram.html")
W, H = 1745, 1010
S = []                                   # svg elements
DARK, GREY = "#3E4C59", "#9AA5B1"

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

def group(x, y, w, h, label, bottom=False):
    S.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="none" stroke="#9AA5B1" stroke-width="1.5" stroke-dasharray="6 5"/>')
    text(x + 12, y + h - 16 if bottom else y + 16, label, 14, anchor="start", color="#52606D", style="italic")

def person(cx, cy, color="#B7950B"):
    S.append(f'<circle cx="{cx}" cy="{cy-22}" r="11" fill="{color}"/>'
             f'<path d="M{cx-15},{cy+26} L{cx-15},{cy-4} Q{cx-15},{cy-10} {cx-9},{cy-10} L{cx+9},{cy-10} Q{cx+15},{cy-10} {cx+15},{cy-4} L{cx+15},{cy+26} Z" fill="{color}"/>')

def actor(x, y, name, sub=None, icon=True):
    if icon:
        person(x - 30, y + 25)
    box(x, y, 140, 50, name, sub, fill="#FFF6D5", stroke="#C9A227", r=25, tsize=16, ssize=11)

HEX = {}
def hexagon(name, cx, cy, w, h, d, desc, db):
    pts = [(cx-w, cy), (cx-w+d, cy-h), (cx+w-d, cy-h), (cx+w, cy), (cx+w-d, cy+h), (cx-w+d, cy+h)]
    S.append('<polygon points="' + " ".join(f"{a:.0f},{b:.0f}" for a, b in pts) + '" fill="#EFE9F8" stroke="#6B46C1" stroke-width="2.2"/>')
    text(cx, cy - h*0.45, name, 17, "bold")
    text(cx - 8, cy + h*0.12, desc, 12.5, color="#3E4C59", lh=15)
    # REST tab on the left vertex = driving port
    S.append(f'<rect x="{cx-w-19}" y="{cy-12}" width="38" height="24" rx="4" fill="#fff" stroke="#6B46C1" stroke-width="1.6"/>')
    text(cx - w, cy, "REST", 11, color="#3E4C59")
    # private data store, bottom right inside the hexagon
    dx, dy = cx + w - d - 38, cy + h - 34
    S.append(f'<path d="M{dx-17},{dy-8} v18 a17,6 0 0 0 34,0 v-18" fill="#fff" stroke="#6B46C1" stroke-width="1.6"/>'
             f'<ellipse cx="{dx}" cy="{dy-8}" rx="17" ry="6" fill="#fff" stroke="#6B46C1" stroke-width="1.6"/>')
    text(dx, dy + 26, db, 11, color="#52606D", style="italic")
    HEX[name] = (cx, cy, w, h, d)

def arrow(path, inc2=False, dotted=False, label=None, lx=None, ly=None, lanchor="middle", lsize=12):
    color = GREY if (inc2 or dotted) else DARK
    dash = ' stroke-dasharray="3 5"' if dotted else (' stroke-dasharray="9 6"' if inc2 else "")
    marker = "url(#ag)" if (inc2 or dotted) else "url(#ad)"
    S.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2"{dash} marker-end="{marker}"/>')
    if label:
        text(lx, ly, label, lsize, anchor=lanchor, color="#52606D" if not (inc2 or dotted) else "#7B8794", style="italic")

# ---------------- groups
group(262, 140, 232, 420, "Client applications", bottom=True)
group(716, 118, 620, 800, "Internal services (one box = one business capability)")

# ---------------- actors
actor(90, 175, "Customer")
actor(90, 375, "Front Staff", "scans at the door")
actor(90, 475, "Manager", "runs the back-office")
actor(90, 760, "Time", "scheduled triggers", icon=False)

# ---------------- clients, gateway
box(282, 170, 192, 72, "Customer Web App", ["(LIFF, inside", "LINE Messenger)"], fill="#E3F0FC", stroke="#2B6CB0")
box(282, 420, 192, 80, "Back-office Web App", ["rounds, live view,", "QR scan on phone"], fill="#E3F0FC", stroke="#2B6CB0")
box(528, 330, 156, 120, "API Gateway", ["routes requests,", "verifies caller", "identity and role"], fill="#E6F4EA", stroke="#2F855A")

# ---------------- services
hexagon("Table Availability Service", 862, 222, 128, 72, 36, ["per-round table status,", "15-minute holds,", "first lock wins"], "Table Status DB")
hexagon("Concert Round Service", 1152, 262, 132, 90, 40, ["venue zone map, tables,", "table types; rounds,", "schedule, prices,", "check-in window,", "publish / draft"], "Round DB")
hexagon("Booking Service", 912, 474, 142, 106, 46, ["booking lifecycle: hold, fee,", "customer profile, terms,", "confirmation, e-ticket,", "check-in, expiry;", "no-show, escalation (Inc. 2)"], "Booking DB")
hexagon("Payment Service", 902, 752, 128, 84, 38, ["payment requests,", "signed webhook; polling,", "refunds, transfer-slip", "review (Inc. 2)"], "Payment DB")
hexagon("Notification Service", 1204, 556, 128, 66, 34, ["LINE messages,", "retries,", "delivery status"], "Notification DB")

# ---------------- adapters and external systems
AD = "#FEF1E1"; ADS = "#DD6B20"; EX = "#FDECEC"; EXS = "#C53030"
box(1362, 42, 162, 54, "LINE Login", "Adapter", fill=AD, stroke=ADS, tsize=15, ssize=12)
box(1560, 42, 168, 54, "LINE Login Platform", "external", fill=EX, stroke=EXS, dash="7 5", tsize=14, ssize=12)
box(1362, 290, 162, 58, "Media Storage", "Adapter", fill=AD, stroke=ADS, tsize=15, ssize=12)
box(1560, 290, 168, 58, "Cloud Object Storage", "external", fill=EX, stroke=EXS, dash="7 5", tsize=14, ssize=12)
box(1362, 527, 162, 58, "LINE Messaging", "Adapter", fill=AD, stroke=ADS, tsize=15, ssize=12)
box(1560, 527, 168, 58, "LINE Messaging API", "external", fill=EX, stroke=EXS, dash="7 5", tsize=14, ssize=12)
box(1362, 800, 162, 58, "Payment Gateway", "Adapter", fill=AD, stroke=ADS, tsize=15, ssize=12)
box(1560, 776, 168, 106, "Payment Gateway", ["external", "MVP: simulated (ADR-11)", "Inc. 2: Beam sandbox"], fill=EX, stroke=EXS, dash="7 5", tsize=14, ssize=11)

# ---------------- arrows: actors to clients
arrow("M230,200 L276,204")
arrow("M230,400 C252,402 256,448 276,452")
arrow("M230,500 C252,500 256,472 276,470")
# clients to gateway and to LINE Login
arrow("M378,170 L378,22 L1644,22 L1644,36", label="LINE Login (LIFF)", lx=980, ly=12)
arrow("M474,212 C505,222 505,330 524,352")
arrow("M474,458 C500,456 505,430 524,424")
arrow("M606,330 L606,69 L1356,69", label="verify ID token", lx=660, ly=58, lanchor="start")
arrow("M1524,69 L1554,69")
# gateway to services
arrow("M684,342 C704,318 704,240 713,226")
arrow("M684,356 C790,340 930,322 1000,272", label="", )
arrow("M684,398 C704,420 732,466 749,474")
arrow("M664,450 C636,580 690,720 753,752")
# table status push to the client (Increment 2)
arrow("M734,206 C640,150 560,150 478,196", dotted=True, label="table status push (WebSocket, Inc. 2)", lx=388, ly=128, lanchor="start", lsize=11.5)
# service to service
arrow("M1100,176 C1060,138 1010,150 988,210", label="initializeRoundTableStatus()", lx=1118, ly=154, lanchor="start", lsize=11.5)
arrow("M1025,410 C1045,390 1065,370 1082,356", label="getRound()", lx=1044, ly=350, lanchor="end", lsize=11.5)
arrow("M1120,354 C1110,420 1090,455 1060,470", label="getConfirmedBookingCount()", lx=1102, ly=440, lanchor="start", lsize=11.5)
arrow("M860,368 L860,300")
arrow("M852,580 L852,662", label="createPaymentRequest()", lx=842, ly=622, lanchor="end", lsize=10.5)
arrow("M920,668 L920,584", label="confirmBookingPayment()", lx=930, ly=612, lanchor="start", lsize=10.5)
arrow("M1036,515 C1042,538 1046,552 1053,556")
arrow("M1030,752 C1052,690 1066,618 1074,572", inc2=True, label="sendSlipDecisionNotice() (Inc. 2)", lx=1086, ly=690, lanchor="start", lsize=11)
arrow("M1284,262 C1316,262 1336,300 1356,312")
arrow("M1005,800 C1120,820 1330,816 1348,750 L1348,382 C1348,364 1366,354 1392,352", inc2=True, label="storeTransferSlip() (Inc. 2)", lx=1326, ly=722, lanchor="end", lsize=11)
arrow("M1332,556 L1356,556")
arrow("M998,822 C1120,846 1260,836 1356,830")
# adapters to external systems
arrow("M1524,319 L1554,319")
arrow("M1524,556 L1554,556")
arrow("M1524,829 L1554,829")
# payment result webhook back to the gateway
arrow("M1644,882 L1644,968 L606,968 L606,456", label="payment result (signed webhook)", lx=1110, ly=956)
# Time
arrow("M230,775 C420,760 600,640 780,560", label="expire holds; mark no-shows (Inc. 2)", lx=250, ly=711, lanchor="start", lsize=11.5)
arrow("M230,800 C420,810 600,770 751,758", inc2=True, label="poll payment results (Inc. 2)", lx=420, ly=822, lanchor="start")

# ---------------- legend
lx, ly = 30, 858
S.append(f'<rect x="{lx}" y="{ly}" width="520" height="140" rx="8" fill="#F8F9FA" stroke="#CBD2D9"/>')
text(lx + 14, ly + 18, "Legend", 14, "bold", anchor="start")
rows = [("solid", "A → B means A invokes B (synchronous REST); built in the MVP"),
        ("dash", "invocation added in Increment 2"),
        ("dot", "server-initiated push to the client (Increment 2)"),
        ("box", "dashed box: external system"),
        ("hex", "hexagon: service core; REST tab on the left vertex = driving port"),
        ("cyl", "cylinder: data store owned privately by that service")]
for i, (k, desc) in enumerate(rows):
    y = ly + 40 + i * 17
    if k in ("solid", "dash", "dot"):
        dash = {"solid": "", "dash": ' stroke-dasharray="9 6"', "dot": ' stroke-dasharray="3 5"'}[k]
        col = DARK if k == "solid" else GREY
        S.append(f'<path d="M{lx+16},{y} L{lx+70},{y}" stroke="{col}" stroke-width="2"{dash} marker-end="url(#{"ad" if k=="solid" else "ag"})"/>')
    text(lx + 86, y, desc, 12, anchor="start", color="#3E4C59")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">'
       f'<defs><marker id="ad" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
       f'<path d="M0,0 L10,5 L0,10 z" fill="{DARK}"/></marker>'
       f'<marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
       f'<path d="M0,0 L10,5 L0,10 z" fill="{GREY}"/></marker></defs>'
       f'<rect width="{W}" height="{H}" fill="#fff"/>' + "".join(S) + "</svg>")
html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>SEATS microservice architecture, version 2</title>
<!-- Source of assets/architecture-diagram.png (project document v2.0, CH-20). Rendered with headless Chromium
     at 2x: the screenshot covers div.canvas. Grey dashed and dotted arrows are added in Increment 2. -->
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
  for (const t of texts.filter(t => t.getAttribute('font-style') === 'italic' && !t.textContent.endsWith(' DB') && !t.textContent.startsWith('Internal services') && !t.textContent.startsWith('Client applications'))) {
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
