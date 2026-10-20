"""Re-take the Konga screenshots used in the report with red highlight boxes around the elements of interest.
Entities already exist in Kong; forms are re-opened and re-filled but never submitted."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from konga_build import *

JS = """(boxes) => {
  document.querySelectorAll('.hl-box').forEach(e => e.remove());
  boxes.forEach(([x, y, w, h, label]) => {
    w = Math.min(w, window.innerWidth - x - 14);
    const d = document.createElement('div'); d.className = 'hl-box';
    d.style.cssText = `position:fixed;left:${x-6}px;top:${y-6}px;width:${w+12}px;height:${h+12}px;border:4px solid #e53935;border-radius:6px;box-shadow:0 0 0 2px #fff,0 0 12px rgba(229,57,53,.6);z-index:99999;pointer-events:none;`;
    if (label) { const t = document.createElement('div'); t.textContent = label;
      t.style.cssText = 'position:absolute;left:-4px;top:-26px;background:#e53935;color:#fff;font:bold 13px sans-serif;padding:2px 8px;border-radius:4px;white-space:nowrap;'; d.appendChild(t); }
    document.body.appendChild(d);
  });
}"""
def hl(pg, items, name):
    """items: list of (locator, label). Draw boxes then screenshot."""
    boxes = []
    for loc, label in items:
        try:
            if isinstance(loc, str): loc = pg.locator(loc)
            loc = loc.first; loc.scroll_into_view_if_needed(); pg.wait_for_timeout(150)
            bb = loc.bounding_box()
            if bb and bb["width"] > 0: boxes.append([bb["x"], bb["y"], bb["width"], bb["height"], label])
            else: print("  !! no box for", label)
        except Exception as e: print("  !! missing", label, str(e)[:80])
    # overlap check including the label strip above each box
    def rect(b): return (b[0] - 6, b[1] - 32 if b[4] else b[1] - 6, max(b[0] + b[2], b[0] + 8 * len(b[4] or "")) + 6, b[1] + b[3] + 6)
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, c = rect(boxes[i]), rect(boxes[j])
            if a[0] < c[2] and c[0] < a[2] and a[1] < c[3] and c[1] < a[3]: print("  !! overlap in", name, ":", boxes[i][4], "<->", boxes[j][4])
    pg.evaluate(JS, boxes); pg.wait_for_timeout(500)
    dlg = pg.locator(".modal-dialog:visible")
    if dlg.count():
        m = dlg.first.bounding_box(); x0 = max(0, m["x"] - 20); y0 = max(0, m["y"] - 20)
        clip = {"x": x0, "y": y0, "width": min(1440 - x0, m["width"] + 40), "height": min(2800 - y0, m["height"] + 40)}
    else:
        clip = {"x": 0, "y": 0, "width": 1440, "height": 900}
    path = os.path.join(CAP, name + ".png"); pg.screenshot(path=path, clip=clip); print("  saved", name, "clip h=%d" % clip["height"])

def field(model): return f"input[ng-model='{model}']"
def row(text): return f"tr:has-text('{text}')"
def formrow(label): return f"xpath=//label[contains(normalize-space(.),'{label}')]/ancestor::div[contains(@class,'form-group')][1]"

def service_form(pg, name, url, desc):
    pg.goto(KONGA + "/#!/services", wait_until="networkidle"); pg.wait_for_timeout(1200)
    pg.get_by_text("ADD NEW SERVICE").first.click(); pg.wait_for_timeout(1000)
    pg.fill(field("service.name"), name); pg.fill(field("service.extras.description"), desc); pg.fill(field("service.url"), url)

def route_form(pg, service, rname, paths, protocols=None, strip=None):
    open_service(pg, service); pg.get_by_text("Routes", exact=True).first.click(); pg.wait_for_timeout(1000)
    pg.locator("button").filter(has_text="ADD ROUTE").first.click(); pg.wait_for_timeout(1000)
    pg.fill(field("route.name"), rname); add_tags(pg, "Paths", paths)
    if protocols:
        chips = pg.locator("chips[ng-model='route.protocols'] [remove-chip]")
        for _ in range(chips.count()): chips.first.click(); pg.wait_for_timeout(150)
        add_tags(pg, "Protocols", protocols)
    if strip is not None:
        cb = pg.locator(field("route.strip_path"))
        if cb.is_checked() != strip: cb.locator("xpath=ancestor::div[contains(@class,'bootstrap-switch')][1]").click(); pg.wait_for_timeout(300)

def consumer_creds(pg, tab):
    pg.goto(KONGA + "/#!/consumers", wait_until="networkidle"); pg.wait_for_timeout(1200)
    pg.get_by_text("Bob", exact=True).first.click(); pg.wait_for_timeout(1500)
    pg.get_by_text("Credentials", exact=True).first.click(); pg.wait_for_timeout(900)
    if tab: pg.get_by_text(tab, exact=True).first.click(); pg.wait_for_timeout(900)

def plugins_tab(pg, service):
    open_service(pg, service); pg.get_by_text("Plugins", exact=True).first.click(); pg.wait_for_timeout(1000)

IP = os.environ.get("HOST_IP", "10.0.10.51")
STEPS = {
 "01-register-admin": lambda pg: (pg.goto(KONGA + "/register", wait_until="networkidle"), pg.wait_for_timeout(800),
     [ (f) for f in [] ] and None,
     (pg.fill("input[name=username]", "admin"), pg.fill("input[name=email]", "watayut@example.com"), pg.fill("input[name=password]", "x"*14), pg.fill("input[name=password_confirmation]", "x"*14)) if "/register" in pg.url else None,
     hl(pg, [("form", "สร้าง admin user ของ Konga")], "01-register-admin")),
}
def run_all():
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1440, "height": 2800}); pg = ctx.new_page(); login(pg)
        def fresh():
            pg.goto(KONGA + "/#!/dashboard", wait_until="networkidle"); pg.reload(wait_until="networkidle"); pg.wait_for_timeout(800)
        # 04 new connection form (dashboard shows it only when no connection; use CONNECTIONS -> NEW CONNECTION instead)
        pg.goto(KONGA + "/#!/connections", wait_until="networkidle"); pg.wait_for_timeout(1200)
        pg.get_by_text("NEW CONNECTION").first.click(); pg.wait_for_timeout(1000)
        pg.fill(field("node.name"), "Connect1"); pg.fill(field("node.kong_admin_url"), "http://kong:8001")
        hl(pg, [(field("node.name"), "Name"), (field("node.kong_admin_url"), "Kong Admin URL = http://kong:8001"), ("button:has-text('CREATE CONNECTION')", None)], "04-new-connection-form")
        fresh(); pg.goto(KONGA + "/#!/connections", wait_until="networkidle"); pg.wait_for_timeout(1500)
        hl(pg, [(row("Connect1"), "connection Connect1 → Kong 2.8.5 (active)")], "06-connections-list")
        # services forms
        for n, name, url, desc in [("09-add-service-httpservice1-form", "httpservice1", f"http://{IP}:8081", "SimpleHTTP main1.js on port 8081"),
                                   ("16a-add-service-lbservice", "lbservice", "http://http-upstream", "load balanced to SimpleHTTP 8081/8082 via upstream"),
                                   ("18a-add-service-restservice", "restservice", f"http://{IP}:3000", "SimpleREST express app on port 3000"),
                                   ("20a-add-service-grpcservice", "grpcservice", f"grpc://{IP}:50051", "SimplegRPC greeter_server on port 50051")]:
            fresh(); service_form(pg, name, url, desc)
            hl(pg, [(field("service.name"), "Name"), (field("service.url"), "Url = " + url), ("button:has-text('SUBMIT SERVICE')", None)], n)
        # route forms
        fresh(); route_form(pg, "httpservice1", "http1-route", ["/http1"])
        hl(pg, [(field("route.name"), "Name"), (formrow("Paths"), "Paths = /http1"), ("button:has-text('SUBMIT ROUTE')", None)], "14a-add-route-http1-route")
        fresh(); route_form(pg, "lbservice", "lb-route", ["/lb"])
        hl(pg, [(field("route.name"), "Name"), (formrow("Paths"), "Paths = /lb"), ("button:has-text('SUBMIT ROUTE')", None)], "17a-add-route-lb-route")
        fresh(); route_form(pg, "restservice", "rest-route", ["/rest"], strip=True)
        hl(pg, [(field("route.name"), "Name"), (formrow("Paths"), "Paths = /rest"), (formrow("Strip Path"), "Strip Path = YES"), ("button:has-text('SUBMIT ROUTE')", None)], "19a-add-route-rest-route")
        fresh(); route_form(pg, "grpcservice", "grpc-route", ["/helloworld.Greeter"], protocols=["grpc", "grpcs"], strip=False)
        hl(pg, [(field("route.name"), "Name"), (formrow("Paths"), "Paths = /helloworld.Greeter"), (formrow("Strip Path"), "Strip Path = NO"), (formrow("Protocols"), "Protocols = grpc, grpcs"), ("button:has-text('SUBMIT ROUTE')", None)], "21a-add-route-grpc-route")
        # route lists per service
        for svc, n, label, rname in [("httpservice1", "14b-service-httpservice1-routes", "route http1-route → /http1", "http1-route"), ("lbservice", "17b-service-lbservice-routes", "route lb-route → /lb", "lb-route"),
                              ("restservice", "19b-service-restservice-routes", "route rest-route → /rest", "rest-route"), ("grpcservice", "21b-service-grpcservice-routes", "route grpc-route → /helloworld.Greeter (grpc, grpcs)", "grpc-route")]:
            fresh(); open_service(pg, svc); pg.get_by_text("Routes", exact=True).first.click(); pg.wait_for_timeout(1200)
            hl(pg, [(row(rname), label)], n)
        # upstream
        fresh(); pg.goto(KONGA + "/#!/upstreams", wait_until="networkidle"); pg.wait_for_timeout(1200)
        pg.get_by_text("CREATE UPSTREAM").first.click(); pg.wait_for_timeout(1000); pg.fill(field("upstream.name"), "http-upstream")
        hl(pg, [(field("upstream.name"), "Name = http-upstream"), ("button:has-text('SUBMIT UPSTREAM')", None)], "15a-add-upstream-form")
        fresh(); pg.goto(KONGA + "/#!/upstreams", wait_until="networkidle"); pg.wait_for_timeout(1200)
        pg.locator("a", has_text="DETAILS").first.click(); pg.wait_for_timeout(1500); pg.get_by_text("Targets", exact=True).first.click(); pg.wait_for_timeout(1000)
        pg.locator("button").filter(has_text="ADD TARGET").first.click(); pg.wait_for_timeout(800)
        pg.fill(field("item.target"), f"{IP}:8081"); pg.fill(field("item.weight"), "100")
        hl(pg, [(field("item.target"), f"Target = {IP}:8081 (และ :8082)"), (field("item.weight"), "Weight = 100"), ("button:has-text('SUBMIT TARGET')", None)], "15d-add-target-form")
        fresh(); pg.goto(KONGA + "/#!/upstreams", wait_until="networkidle"); pg.wait_for_timeout(1200)
        pg.locator("a", has_text="DETAILS").first.click(); pg.wait_for_timeout(1500); pg.get_by_text("Targets", exact=True).first.click(); pg.wait_for_timeout(1200)
        hl(pg, [("table tbody", f"targets {IP}:8081 และ {IP}:8082 weight 100 (healthy)")], "15e-upstream-targets")
        # overview pages
        fresh(); pg.goto(KONGA + "/#!/services", wait_until="networkidle"); pg.wait_for_timeout(1500)
        hl(pg, [("table tbody", f"4 services: host = {IP} / http-upstream")], "22-all-services")
        pg.goto(KONGA + "/#!/routes", wait_until="networkidle"); pg.wait_for_timeout(1500)
        hl(pg, [("table tbody", "4 routes: /http1, /lb, /rest, /helloworld.Greeter")], "23-all-routes")
        pg.goto(KONGA + "/#!/upstreams", wait_until="networkidle"); pg.wait_for_timeout(1500)
        hl(pg, [(row("http-upstream"), "upstream http-upstream")], "24-all-upstreams")
        # consumer
        fresh(); pg.goto(KONGA + "/#!/consumers", wait_until="networkidle"); pg.wait_for_timeout(1200)
        pg.get_by_text("CREATE CONSUMER").first.click(); pg.wait_for_timeout(900); pg.fill(field("consumer.username"), "Bob"); pg.fill(field("consumer.custom_id"), "bob-001")
        hl(pg, [(field("consumer.username"), "username = Bob"), (field("consumer.custom_id"), "custom_id"), ("button:has-text('SUBMIT CONSUMER')", None)], "26a-add-consumer-form")
        fresh(); consumer_creds(pg, None); pg.get_by_text("CREATE CREDENTIALS").first.click(); pg.wait_for_timeout(900)
        pg.fill(field("credentials.username"), "bob"); pg.fill(field("credentials.password"), "bob1234")
        hl(pg, [(field("credentials.username"), "username = bob"), (field("credentials.password"), "password = bob1234"), ("button[ng-click='manage()']", None)], "31a-consumer-basic-auth-form")
        fresh(); consumer_creds(pg, None); hl(pg, [(row("bob"), "basic-auth credential ของ Bob")], "31b-consumer-basic-auth-list")
        fresh(); consumer_creds(pg, "API KEYS"); pg.locator("button").filter(has_text="CREATE API KEY").first.click(); pg.wait_for_timeout(900); pg.fill(field("key.value"), "bob-secret-key-123")
        hl(pg, [(field("key.value"), "key = bob-secret-key-123"), (".modal button[ng-click='createApiKey()']", None)], "32a-consumer-api-key-form")
        fresh(); consumer_creds(pg, "API KEYS"); hl(pg, [(row("bob-secret-key-123"), "api key ของ Bob = bob-secret-key-123")], "32b-consumer-api-key-list")
        # plugins
        fresh(); plugins_tab(pg, "restservice"); pg.locator("button").filter(has_text="ADD PLUGIN").first.click(); pg.wait_for_timeout(1200)
        hl(pg, [(".modal .panel:has-text('Basic Auth'), .modal div:has(> strong:has-text('Basic Auth'))", "Basic Auth → ADD PLUGIN")], "33a-restservice-add-plugin-catalog")
        pg.locator(".modal button").filter(has_text="ADD PLUGIN").nth(0).click(); pg.wait_for_timeout(1200)
        hl(pg, [("button[ng-click='addPlugin()']", "ADD PLUGIN (basic-auth ให้ restservice)")], "33b-restservice-basic-auth-plugin-form")
        fresh(); plugins_tab(pg, "restservice"); hl(pg, [(row("basic-auth"), "plugin basic-auth เปิดอยู่บน restservice")], "33c-restservice-plugins")
        fresh(); plugins_tab(pg, "httpservice1"); pg.locator("button").filter(has_text="ADD PLUGIN").first.click(); pg.wait_for_timeout(1200)
        pg.locator(".modal button").filter(has_text="ADD PLUGIN").nth(1).click(); pg.wait_for_timeout(1200)
        kin = pg.locator("xpath=//label[contains(normalize-space(.),'key names')]/following::input[1]"); kin.click(); kin.fill("apikey"); kin.press("Enter"); pg.wait_for_timeout(300)
        hl(pg, [(formrow("key names"), "key names = apikey"), ("button[ng-click='addPlugin()']", "ADD PLUGIN (key-auth ให้ httpservice1)")], "34a-httpservice1-key-auth-plugin-form")
        fresh(); plugins_tab(pg, "httpservice1"); hl(pg, [(row("key-auth"), "plugin key-auth เปิดอยู่บน httpservice1")], "34b-httpservice1-plugins")
        fresh(); pg.goto(KONGA + "/#!/plugins", wait_until="networkidle"); pg.wait_for_timeout(1500)
        hl(pg, [("table tbody", "key-auth → httpservice1, basic-auth → restservice")], "35-all-plugins")
        pg.goto(KONGA + "/#!/consumers", wait_until="networkidle"); pg.wait_for_timeout(1500)
        hl(pg, [(row("Bob"), "consumer Bob")], "36-all-consumers")
        b.close()
        # register page: Konga redirects when an admin exists, so keep the original 01-register-admin.png
if __name__ == "__main__": run_all()
