"""Assemble captures into an HTML report and print it to PDF with Playwright (Chromium)."""
import os, html, datetime
from playwright.sync_api import sync_playwright
W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT_HTML = os.path.join(W, "report", "KONG_Assignment05_6970267821.html")
OUT_PDF = os.path.join(W, "report", "KONG_Assignment05_6970267821.pdf")
IP = "10.0.10.51"

from PIL import Image
def fig(kind, name, caption, w=100):
    p = os.path.join(W, "captures", kind, name + ".png"); assert os.path.exists(p), p
    im = Image.open(p); iw, ih = im.size
    if ih > 1.35 * iw:  # tall modal form: split into two overlapping halves so each fits a page and stays readable
        sd = os.path.join(W, "captures", kind, "_split"); os.makedirs(sd, exist_ok=True)
        cut = int(ih * 0.55); out = []
        # moderately tall forms (service/upstream): only the top part carries the filled fields
        parts = [(0, 0, iw, int(ih * 0.6))] if ih < 1.8 * iw else [(0, 0, iw, cut), (0, ih - cut, iw, ih)]
        for i, box in enumerate(parts):
            fp = os.path.join(sd, f"{name}-{i+1}.png"); im.crop(box).save(fp)
            out.append(f'<figure style="width:{w}%"><img src="../captures/{kind}/_split/{name}-{i+1}.png"><figcaption>{html.escape(caption)}{"" if len(parts) == 1 else (" (ส่วนบน)" if i == 0 else " (ส่วนล่าง)")}</figcaption></figure>')
        return "".join(out)
    return f'<figure style="width:{w}%"><img src="../captures/{kind}/{name}.png"><figcaption>{html.escape(caption)}</figcaption></figure>'
def term(name, caption): return fig("terminal", name, caption)
def konga(name, caption): return fig("konga", name, caption)
def inso(name, caption): return fig("insomnia", name, caption)
def h2(t): return f"<h2>{html.escape(t)}</h2>"
def h3(t): return f"<h3>{html.escape(t)}</h3>"
def p(t): return f"<p>{t}</p>"
def code(t): return f"<pre class=cmd>{html.escape(t)}</pre>"

parts = []
# ---------- cover
parts.append(f"""
<section class="cover">
<div class="course">2110521 Software Architecture &mdash; Section WED (วันพุธ)</div>
<h1>Assignment 05<br>Microservice API Gateway using KONG</h1>
<div class="sub">ติดตั้งและใช้งาน KONG เป็น API Gateway หน้า HTTP / REST / gRPC services<br>พร้อม Konga (UI), Upstream load balancer, Basic Auth และ Key Auth</div>
<table class="meta">
<tr><th>ชื่อ</th><td>Watayut Aiamanan</td></tr>
<tr><th>รหัสนิสิต</th><td>6970267821</td></tr>
<tr><th>วันที่ส่ง</th><td>20 ตุลาคม 2026</td></tr>
<tr><th>IP address ของเครื่อง</th><td>{IP} (แทน localhost ตามที่โจทย์กำหนด)</td></tr>
</table>
<div class="note">โจทย์: ติดตั้งและใช้งาน KONG เป็น API Gateway เพื่อไปใช้กับ REST/gRPC Services และ capture หน้าจอแสดง services และ routes ที่ใช้
(กรณีที่ Services อยู่ที่ localhost ให้ใช้ ip address ของตนแทน)</div>
</section>""")

# ---------- 1 overview
parts.append(h2("1. ภาพรวมและสภาพแวดล้อมที่ใช้"))
parts.append(p("งานนี้ทำบน GitHub Codespaces (Ubuntu 24.04, Docker-in-Docker) แทน Windows 10 ตาม tutorial จึงใช้คำสั่ง <code>hostname -I</code> แทน <code>ipconfig</code> ในการหา IP address ของเครื่อง ซึ่งได้ <b>" + IP + "</b> และใช้ IP นี้เป็น host ของทุก service ที่ลงทะเบียนใน Kong"))
parts.append("""<table class="env">
<tr><th>ส่วนประกอบ</th><th>เวอร์ชัน / ค่าที่ใช้</th><th>หน้าที่</th></tr>
<tr><td>Docker</td><td>29.8.0</td><td>รัน Postgres, Kong, Konga เป็น container ใน network <code>kong-net</code></td></tr>
<tr><td>PostgreSQL</td><td><b>postgres:9.6</b> (ตาม PDF)</td><td>ฐานข้อมูลของ Kong และ Konga</td></tr>
<tr><td>Kong</td><td><b>kong:2.8</b> (2.8.5)</td><td>API Gateway: proxy :8000, admin :8001, gRPC proxy :9080</td></tr>
<tr><td>Konga</td><td>pantsel/konga 0.14.9</td><td>Web UI สำหรับจัดการ Kong ที่ :1337</td></tr>
<tr><td>Node.js</td><td>v24.21.0</td><td>รัน SimpleHTTP (8081, 8082), SimpleREST (3000), SimplegRPC (50051)</td></tr>
<tr><td>Insomnia</td><td>13.3.1 (Linux AppImage บน Xvfb)</td><td>ยิงทดสอบ HTTP / REST / gRPC ผ่าน Kong</td></tr>
<tr><td>curl / grpcurl</td><td>grpcurl 1.9.4</td><td>ทดสอบจาก terminal</td></tr>
</table>""")
parts.append(p("<b>หมายเหตุเรื่องเวอร์ชัน:</b> PDF ระบุ <code>docker pull kong</code> (latest) ซึ่งในปี 2022 คือ Kong 2.x แต่ปัจจุบัน latest คือ Kong 3.x ที่ Konga รองรับไม่สมบูรณ์ จึงเลือก <code>kong:2.8</code> คู่กับ <code>postgres:9.6</code> ตาม PDF เพื่อให้ Konga ทำงานได้ครบ"))
parts.append("""<div class="arch">
<div class="box client">Clients<br><small>curl / grpcurl / Insomnia / browser</small></div>
<div class="arrow">&#8594;</div>
<div class="box kong">Kong 2.8 (API Gateway)<br><small>:8000 http &nbsp;|&nbsp; :9080 grpc &nbsp;|&nbsp; :8001 admin</small><br><small>plugins: key-auth, basic-auth</small></div>
<div class="arrow">&#8594;</div>
<div class="box svc">httpservice1 &rarr; http://10.0.10.51:8081<br>lbservice &rarr; upstream http-upstream {8081, 8082}<br>restservice &rarr; http://10.0.10.51:3000<br>grpcservice &rarr; grpc://10.0.10.51:50051</div>
</div>
<div class="arch2">Konga 0.14.9 (:1337) &#8594; Kong Admin API (http://kong:8001) &nbsp;&nbsp;&nbsp; Kong / Konga &#8594; PostgreSQL 9.6 (kong-database)</div>""")

# ---------- 2 install
parts.append(h2("2. Step 0-1: ติดตั้ง Docker, Node.js และสร้าง container ของ Postgres 9.6 และ Kong"))
parts.append(term("01-docker-version", "ตรวจสอบเวอร์ชัน Docker, Node.js และ npm"))
parts.append(term("02-docker-images", "image ที่ pull มา: postgres:9.6, kong:2.8, pantsel/konga"))
parts.append(term("03-network-create", "1.3 a) สร้าง docker network ชื่อ kong-net"))
parts.append(term("04-run-postgres", "1.3 b) รัน Postgres 9.6 ชื่อ kong-database ใน kong-net"))
parts.append(term("05-kong-migrations", "1.3 c) รัน kong migrations bootstrap เพื่อเตรียมฐานข้อมูลให้ Kong"))
parts.append(term("06-run-kong", "1.3 d) รัน Kong พร้อมเปิด admin :8001 และ proxy :8000 / :9080 (http2 สำหรับ gRPC) ตามคำสั่งใน PDF"))
parts.append(term("07-curl-kong-admin", "1.3 e) ตรวจสอบว่า Kong ทำงาน: curl http://localhost:8001/ ได้ 200 OK, Server: kong/2.8.5"))

# ---------- 3 konga
parts.append(h2("3. Step 2: ติดตั้ง Konga และเชื่อมต่อกับ Kong"))
parts.append(term("08-konga-prepare", "2.2 a) เตรียมฐานข้อมูล konga ใน Postgres เดียวกัน (prepare)"))
parts.append(term("09-run-konga", "2.2 b) รัน Konga ที่ port 1337"))
parts.append(term("10-docker-ps", "container ทั้ง 3 ตัวทำงานอยู่: konga, kong, kong-database"))
parts.append(konga("01-register-admin", "2.2 d) สร้าง admin user ของ Konga (http://localhost:1337)"))
parts.append(konga("04-new-connection-form", "2.2 e) สร้าง connection ชื่อ Connect1 ไปที่ Kong Admin URL = http://kong:8001"))
parts.append(konga("06-connections-list", "Konga เชื่อมต่อ Kong สำเร็จ แสดง Kong version 2.8.5 และสถานะ Connected to Connect1"))

# ---------- 4 services
parts.append(h2("4. Start HTTP / REST / gRPC services ด้วย Node.js (2.2 f)"))
parts.append(p("start service ทั้ง 4 ตัวจาก source code ของอาจารย์ (SimpleServices) ค้างไว้ใน background แล้วตรวจสอบว่าเรียกตรง ๆ ผ่าน IP ของเครื่องได้"))
parts.append(code("cd SimpleHTTP   && node main1.js            # Hello World from Service1  :8081\ncd SimpleHTTP   && node main2.js            # Hello World from Service2  :8082\ncd SimpleREST   && node app.js              # express REST /account      :3000\ncd SimplegRPC/node && node greeter_server.js # helloworld.Greeter/SayHello :50051"))
parts.append(term("11-ip-address", "หา IP address ของเครื่อง (ใช้แทน localhost)"))
parts.append(term("12-services-direct", "เรียก service ตรง ๆ ที่ IP ของเครื่อง ก่อนผ่าน Kong"))

# ---------- 5 step3 http
parts.append(h2("5. Step 3: สร้าง Service และ Route สำหรับ HTTP (httpservice1 → :8081) ด้วย Konga"))
parts.append(konga("09-add-service-httpservice1-form", "Add service: name = httpservice1, url = http://" + IP + ":8081"))
parts.append(konga("14a-add-route-http1-route", "Add route ให้ httpservice1: name = http1-route, paths = /http1"))
parts.append(konga("14b-service-httpservice1-routes", "Route ของ httpservice1 ถูกสร้างแล้ว"))
parts.append(term("16-test-http1-via-kong", "ทดสอบผ่าน Kong: GET http://" + IP + ":8000/http1 → 200 OK ผ่าน Via: kong/2.8.5"))
parts.append(inso("01-http1-via-kong", "Insomnia: GET http://" + IP + ":8000/http1 → 200 OK \"Hello World from Service1\""))

# ---------- 6 step4 lb
parts.append(h2("6. Step 4: Upstream (load balancer) ไปที่ :8081 และ :8082"))
parts.append(konga("15a-add-upstream-form", "สร้าง upstream ชื่อ http-upstream"))
parts.append(konga("15d-add-target-form", "เพิ่ม target " + IP + ":8081 (weight 100) และ " + IP + ":8082 (weight 100)"))
parts.append(konga("15e-upstream-targets", "targets ทั้งสองของ http-upstream"))
parts.append(konga("16a-add-service-lbservice", "สร้าง service lbservice ชี้ไปที่ http://http-upstream (ชื่อ upstream แทน host)"))
parts.append(konga("17a-add-route-lb-route", "Route lb-route: paths = /lb"))
parts.append(term("17-test-lb-via-kong", "เรียก /lb 6 ครั้ง Kong สลับ (round-robin) ระหว่าง Service1 และ Service2"))
parts.append(inso("02-lb-via-kong-1", "Insomnia: GET /lb ครั้งที่ 1"))
parts.append(inso("03-lb-via-kong-2", "Insomnia: GET /lb ครั้งที่ 2 ได้อีก service หนึ่ง"))

# ---------- 7 step5 rest
parts.append(h2("7. Step 5: Service และ Route สำหรับ REST (restservice → :3000)"))
parts.append(konga("18a-add-service-restservice", "สร้าง service restservice url = http://" + IP + ":3000"))
parts.append(konga("19a-add-route-rest-route", "Route rest-route: paths = /rest, strip path = YES (Kong ตัด /rest ออกก่อนส่งต่อ จึงเรียก /rest/account → /account)"))
parts.append(konga("19b-service-restservice-routes", "Route ของ restservice"))
parts.append(term("18-test-rest-via-kong", "GET /rest/account?username=nraboy และ POST /rest/account ผ่าน Kong"))
parts.append(inso("04-rest-get-via-kong", "Insomnia: GET http://" + IP + ":8000/rest/account?username=nraboy → 200 OK JSON"))
parts.append(inso("05-rest-post-via-kong", "Insomnia: POST http://" + IP + ":8000/rest/account (JSON body) → echo กลับมา"))

# ---------- 8 step6 grpc
parts.append(h2("8. Step 6: Service และ Route สำหรับ gRPC (grpcservice → :50051)"))
parts.append(p("Kong รับ gRPC ที่ port 9080 (http2) ซึ่งคำสั่งใน PDF publish ไว้ที่ <code>127.0.0.1:9080</code> เท่านั้น การทดสอบ gRPC จึงเรียกที่ <code>localhost:9080</code> ส่วน service ปลายทางยังชี้ไปที่ IP ของเครื่อง สำหรับ route ต้องตั้ง protocols = grpc, grpcs และ strip path = NO เพราะ path <code>/helloworld.Greeter</code> คือชื่อ service ของ gRPC ที่ต้องส่งต่อไปทั้งก้อน"))
parts.append(konga("20a-add-service-grpcservice", "สร้าง service grpcservice url = grpc://" + IP + ":50051"))
parts.append(konga("21a-add-route-grpc-route", "Route grpc-route: paths = /helloworld.Greeter, protocols = grpc, grpcs, strip path = NO"))
parts.append(konga("21b-service-grpcservice-routes", "Route ของ grpcservice"))
parts.append(term("19-test-grpc-via-kong", "grpcurl เรียก helloworld.Greeter/SayHello ผ่าน Kong :9080 → \"Hello Watayut\""))
parts.append(inso("06-grpc-request-view", "Insomnia gRPC request: proto helloworld.proto, method /Greeter/SayHello, server localhost:9080"))
parts.append(inso("07-grpc-via-kong", "Insomnia: ส่ง {\"name\":\"Watayut\"} ผ่าน Kong ได้ response {\"message\":\"Hello Watayut\"} (0 OK)"))

# ---------- 9 summary capture (assignment deliverable)
parts.append(h2("9. สรุป Services และ Routes ทั้งหมดใน Kong (หน้าจอที่โจทย์ต้องการ)"))
parts.append(konga("22-all-services", "Konga → SERVICES: httpservice1, lbservice, restservice, grpcservice (host = " + IP + " / http-upstream)"))
parts.append(konga("23-all-routes", "Konga → ROUTES: http1-route (/http1), lb-route (/lb), rest-route (/rest), grpc-route (/helloworld.Greeter)"))
parts.append(konga("24-all-upstreams", "Konga → UPSTREAMS: http-upstream"))
parts.append(term("13-kong-services", "Kong Admin API: GET /services"))
parts.append(term("14-kong-routes", "Kong Admin API: GET /routes"))
parts.append(term("15-kong-upstream-targets", "Kong Admin API: targets ของ http-upstream"))
parts.append(inso("12-admin-services", "Insomnia: GET http://localhost:8001/services"))
parts.append(inso("13-admin-routes", "Insomnia: GET http://localhost:8001/routes"))

# ---------- 10 auth
parts.append(h2("10. Step 7-8: Basic Authentication และ Key Authentication ของ consumer"))
parts.append(p("สร้าง consumer ชื่อ <b>Bob</b> ให้ credentials สองแบบ (basic-auth: bob / bob1234 และ api key: bob-secret-key-123) แล้วเปิด plugin <b>basic-auth</b> ที่ restservice และ <b>key-auth</b> ที่ httpservice1 จากนั้นทดสอบว่าถ้าไม่ส่ง credentials จะได้ 401 และเมื่อส่งถูกต้องจะได้ 200"))
parts.append(konga("26a-add-consumer-form", "3.1 สร้าง consumer Bob (custom_id bob-001)"))
parts.append(konga("31a-consumer-basic-auth-form", "Credentials → BASIC: username bob, password bob1234"))
parts.append(konga("31b-consumer-basic-auth-list", "basic-auth credential ของ Bob"))
parts.append(konga("32a-consumer-api-key-form", "Credentials → API KEYS: key = bob-secret-key-123"))
parts.append(konga("32b-consumer-api-key-list", "api key ของ Bob"))
parts.append(konga("33a-restservice-add-plugin-catalog", "3.2 restservice → Plugins → ADD PLUGIN → Authentication"))
parts.append(konga("33b-restservice-basic-auth-plugin-form", "เพิ่ม plugin Basic Auth ให้ restservice"))
parts.append(konga("33c-restservice-plugins", "restservice มี plugin basic-auth แล้ว"))
parts.append(konga("34a-httpservice1-key-auth-plugin-form", "Step 8: เพิ่ม plugin Key Auth ให้ httpservice1 (key name = apikey)"))
parts.append(konga("34b-httpservice1-plugins", "httpservice1 มี plugin key-auth แล้ว"))
parts.append(konga("35-all-plugins", "Konga → PLUGINS: key-auth (httpservice1) และ basic-auth (restservice)"))
parts.append(konga("36-all-consumers", "Konga → CONSUMERS: Bob"))
parts.append(h3("ผลการทดสอบ authentication"))
parts.append(term("20-kong-consumer-credentials", "credentials ของ Bob จาก Kong Admin API"))
parts.append(term("21-kong-plugins", "plugins ที่เปิดอยู่และ service ที่ผูก"))
parts.append(term("22-test-basic-auth-rest", "restservice: ไม่ส่ง credentials → 401 Unauthorized, ส่ง -u bob:bob1234 → 200 OK"))
parts.append(term("23-test-key-auth-http1", "httpservice1: ไม่มี apikey → 401 \"No API key found in request\", ส่ง apikey ทาง header หรือ query → 200 OK"))
parts.append(term("24-test-wrong-credentials", "รหัสผ่านผิด / key ผิด → 401 \"Invalid authentication credentials\""))
parts.append(inso("08-rest-get-401-after-basic-auth", "Insomnia: /rest/account โดยไม่ใส่ auth หลังเปิด basic-auth → 401 Unauthorized"))
parts.append(inso("09-http1-401-after-key-auth", "Insomnia: /http1 โดยไม่ใส่ apikey หลังเปิด key-auth → 401"))
parts.append(inso("10-rest-basic-auth-bob-200", "Insomnia: Auth = Basic (bob / bob1234) → 200 OK"))
parts.append(inso("11-http1-key-auth-200", "Insomnia: header apikey: bob-secret-key-123 → 200 OK"))

# ---------- 11 problems
CSS = """
@page { size: A4; margin: 16mm 14mm 16mm 14mm; }
body { font-family: "Noto Sans Thai", "Laksaman", "Noto Sans", "DejaVu Sans", sans-serif; font-size: 11.5pt; line-height: 1.55; color: #1b1f24; }
code, pre { font-family: "DejaVu Sans Mono", "Noto Sans Mono", monospace; }
code { background: #f1f3f5; padding: 0 4px; border-radius: 3px; font-size: 10pt; }
pre.cmd { background: #1e1e1e; color: #d4d4d4; padding: 10px 14px; border-radius: 6px; font-size: 9pt; line-height: 1.4; white-space: pre-wrap; word-break: break-all; }
h1 { font-size: 26pt; line-height: 1.25; margin: 10mm 0 4mm; color: #0b3d2e; }
h2 { font-size: 16pt; color: #0b3d2e; border-bottom: 2px solid #1abc9c; padding-bottom: 3px; margin: 10mm 0 3mm; page-break-before: always; page-break-after: avoid; }
h3 { font-size: 13pt; color: #0b3d2e; margin: 6mm 0 2mm; page-break-after: avoid; }
p { margin: 2mm 0; text-align: justify; }
figure { margin: 3mm auto 5mm; page-break-inside: avoid; }
figure img { max-width: 100%; max-height: 225mm; border: 1px solid #cfd4da; border-radius: 4px; display: block; margin: 0 auto; }
figcaption { font-size: 10pt; color: #444; margin-top: 1.5mm; }
table.env, table.meta { border-collapse: collapse; width: 100%; margin: 3mm 0; font-size: 10.5pt; }
table.env th, table.env td { border: 1px solid #cfd4da; padding: 4px 8px; vertical-align: top; text-align: left; }
table.env th { background: #e8f8f4; }
.cover { text-align: center; padding-top: 30mm; }
.cover .course { font-size: 14pt; color: #555; }
.cover .sub { font-size: 13pt; color: #333; margin-bottom: 10mm; }
.cover table.meta { width: 70%; margin: 0 auto 8mm; }
.cover table.meta th { text-align: right; padding: 4px 10px; color: #555; width: 45%; }
.cover table.meta td { text-align: left; padding: 4px 10px; font-weight: 600; }
.cover .note { background: #f6f8fa; border-left: 4px solid #1abc9c; padding: 6px 12px; text-align: left; font-size: 10.5pt; }
.arch { display: flex; align-items: center; justify-content: center; gap: 6px; margin: 5mm 0 2mm; }
.arch .box { border: 2px solid #1abc9c; border-radius: 8px; padding: 8px 12px; font-size: 10pt; text-align: center; background: #f7fffc; }
.arch .box.kong { background: #e8f8f4; font-weight: 600; }
.arch .box.svc { text-align: left; font-family: "DejaVu Sans Mono", monospace; font-size: 9pt; }
.arch .arrow { font-size: 20pt; color: #1abc9c; }
.arch2 { text-align: center; font-size: 10pt; color: #555; margin-bottom: 4mm; }
"""
doc = f"<!doctype html><html lang='th'><head><meta charset='utf-8'><title>KONG Assignment 05 - 6970267821</title><style>{CSS}</style></head><body>{''.join(parts)}</body></html>"
os.makedirs(os.path.dirname(OUT_HTML), exist_ok=True); open(OUT_HTML, "w").write(doc); print("html:", OUT_HTML)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto("file://" + OUT_HTML, wait_until="networkidle"); pg.wait_for_timeout(1500)
    pg.pdf(path=OUT_PDF, format="A4", print_background=True, display_header_footer=True,
           header_template="<div></div>",
           footer_template="<div style='font-size:8pt;color:#777;width:100%;text-align:center;font-family:sans-serif'>2110521 Software Architecture - Assignment 05 KONG API Gateway - Watayut Aiamanan 6970267821 - page <span class='pageNumber'></span>/<span class='totalPages'></span></div>",
           margin={"top": "16mm", "bottom": "18mm", "left": "14mm", "right": "14mm"})
    b.close()
print("pdf:", OUT_PDF)
