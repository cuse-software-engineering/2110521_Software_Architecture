"""Draw red highlight boxes + Thai labels on the Insomnia screenshots (1500x900) using Chromium so Thai text is shaped correctly."""
import os
from playwright.sync_api import sync_playwright
import shutil, json, base64
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "captures", "insomnia")
URL = (380, 146, 850, 180); STATUS = (950, 148, 1090, 180); RESP = (940, 250, 1500, 395); RESP_TALL = (940, 250, 1500, 700)
GURL = (385, 146, 745, 180); GSTATUS = (950, 148, 1010, 180); GRESP = (940, 225, 1500, 330)
BOXES = {
 "01-http1-via-kong": [(URL, "GET /http1 ผ่าน Kong :8000"), (STATUS, "200 OK"), (RESP, "Hello World from Service1")],
 "02-lb-via-kong-1": [(URL, "GET /lb ผ่าน upstream"), (STATUS, "200 OK"), (RESP, "ครั้งที่ 1")],
 "03-lb-via-kong-2": [(URL, "GET /lb ผ่าน upstream"), (STATUS, "200 OK"), (RESP, "ครั้งที่ 2 ได้อีก service")],
 "04-rest-get-via-kong": [(URL, "GET /rest/account ผ่าน Kong"), ((390, 365, 925, 397), "query username=nraboy"), (STATUS, "200 OK"), (RESP, "JSON จาก SimpleREST")],
 "05-rest-post-via-kong": [(URL, "POST /rest/account ผ่าน Kong"), (STATUS, "200 OK"), (RESP, "JSON body ถูก echo กลับ")],
 "06-grpc-request-view": [(GURL, "gRPC server + method /Greeter/SayHello")],
 "07-grpc-via-kong": [(GURL, "gRPC ผ่าน Kong localhost:9080"), (GSTATUS, "0 OK"), (GRESP, "Hello Watayut")],
 "08-rest-get-401-after-basic-auth": [(URL, "ไม่ใส่ credentials"), (STATUS, "401 Unauthorized"), (RESP, "basic-auth ปฏิเสธ")],
 "09-http1-401-after-key-auth": [(URL, "ไม่ใส่ apikey"), (STATUS, "401 Unauthorized"), (RESP, "key-auth ปฏิเสธ")],
 "10-rest-basic-auth-bob-200": [((390, 275, 925, 420), "Auth = Basic bob / bob1234"), (STATUS, "200 OK"), (RESP, "ผ่านแล้ว")],
 "11-http1-key-auth-200": [((390, 378, 925, 412), "header apikey = bob-secret-key-123"), (STATUS, "200 OK"), (RESP, "ผ่านแล้ว")],
 "12-admin-services": [(URL, "Kong Admin API /services"), (STATUS, "200 OK"), (RESP_TALL, "services ทั้ง 4")],
 "13-admin-routes": [(URL, "Kong Admin API /routes"), (STATUS, "200 OK"), (RESP_TALL, "routes ทั้ง 4")],
}

TPL = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1500px;height:900px;position:relative;font-family:'Noto Sans Thai','Laksaman',sans-serif}
img{position:absolute;left:0;top:0;width:1500px;height:900px}
.b{position:absolute;border:4px solid #e53935;border-radius:5px;box-shadow:0 0 0 2px #fff,0 0 10px rgba(229,57,53,.7)}
.l{position:absolute;left:-4px;top:-30px;background:#e53935;color:#fff;font-weight:700;font-size:15px;line-height:26px;padding:0 9px;border-radius:4px;white-space:nowrap}
</style></head><body><img src="%s">%s</body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1500, "height": 900})
    def rect(bx):
        (x0, y0, x1, y1), label = bx; ly0 = y0 - 34 if y0 > 34 else y0; lx1 = x0 + 9 * len(label) + 20
        return (x0 - 4, ly0, max(x1, lx1) + 4, y1 + 4)
    for name, boxes in BOXES.items():
        rs = [rect(b) for b in boxes]
        for i in range(len(rs)):
            for j in range(i + 1, len(rs)):
                a, c = rs[i], rs[j]
                if a[0] < c[2] and c[0] < a[2] and a[1] < c[3] and c[1] < a[3]: print("  !! overlap in", name, ":", boxes[i][1], "<->", boxes[j][1])
        src = os.path.join(D, name + ".png"); orig = os.path.join(D, "_orig", name + ".png")
        os.makedirs(os.path.join(D, "_orig"), exist_ok=True)
        if not os.path.exists(orig): shutil.copy(src, orig)
        divs = ""
        for (x0, y0, x1, y1), label in boxes:
            top = f"top:-30px" if y0 > 34 else f"top:{y1-y0+8}px"
            divs += f'<div class="b" style="left:{x0-4}px;top:{y0-4}px;width:{x1-x0}px;height:{y1-y0}px"><div class="l" style="{top}">{label}</div></div>'
        pg.set_content(TPL % ("data:image/png;base64," + base64.b64encode(open(orig, "rb").read()).decode(), divs)); pg.wait_for_timeout(300)
        pg.screenshot(path=src, clip={"x": 0, "y": 0, "width": 1500, "height": 900}); print("annotated", name)
    b.close()
