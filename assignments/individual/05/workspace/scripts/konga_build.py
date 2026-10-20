"""Build the Kong configuration through the Konga UI (Steps 3-6 of the tutorial) and capture screenshots."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from konga_lib import *
IP = os.environ.get("HOST_IP", "10.0.10.51")

def tag_input(pg, label):
    """The tag-style inputs (Hosts/Paths/Methods/Protocols) have no ng-model: find the first input after the label."""
    return pg.locator(f"xpath=//label[contains(normalize-space(.),'{label}')]/following::input[1]")

def add_tags(pg, label, values):
    inp = tag_input(pg, label)
    for v in values:
        inp.click(); inp.fill(v); inp.press("Enter"); pg.wait_for_timeout(200)

def open_service(pg, name):
    pg.goto(KONGA + "/#!/services", wait_until="networkidle"); pg.wait_for_timeout(1500)
    pg.get_by_text(name, exact=True).first.click(); pg.wait_for_timeout(2000)

def create_service(pg, n, name, url, desc):
    pg.goto(KONGA + "/#!/services", wait_until="networkidle"); pg.wait_for_timeout(1500)
    pg.get_by_text("ADD NEW SERVICE").first.click(); pg.wait_for_timeout(1200)
    pg.fill("input[ng-model='service.name']", name); pg.fill("input[ng-model='service.extras.description']", desc)
    pg.fill("input[ng-model='service.url']", url)
    shot(pg, f"{n}a-add-service-{name}"); pg.get_by_text("SUBMIT SERVICE").click(); pg.wait_for_timeout(2500)
    shot(pg, f"{n}b-services-list")

def create_route(pg, n, service, rname, paths, protocols=None, strip=None):
    open_service(pg, service)
    pg.get_by_text("Routes", exact=True).first.click(); pg.wait_for_timeout(1200)
    pg.locator("button").filter(has_text="ADD ROUTE").first.click(); pg.wait_for_timeout(1200)
    pg.fill("input[ng-model='route.name']", rname)
    add_tags(pg, "Paths", paths)
    if protocols:
        # Konga pre-fills http,https: remove the existing chips before adding the gRPC protocols
        chips = pg.locator("chips[ng-model='route.protocols'] [remove-chip]")
        cnt = chips.count(); print("  existing protocol chips:", cnt)
        for _ in range(cnt): chips.first.click(); pg.wait_for_timeout(200)
        add_tags(pg, "Protocols", protocols)
    if strip is not None:
        cb = pg.locator("input[ng-model='route.strip_path']")
        if cb.is_checked() != strip: cb.locator("xpath=ancestor::div[contains(@class,'bootstrap-switch')][1]").click(); pg.wait_for_timeout(300)
    shot(pg, f"{n}a-add-route-{rname}"); pg.get_by_text("SUBMIT ROUTE").click(); pg.wait_for_timeout(2500)
    shot(pg, f"{n}b-service-{service}-routes")

if __name__ == "__main__":
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    with sync_playwright() as p:
        b, pg = browser(p); login(pg)
        # Step 3: HTTP service + route (service httpservice1 already created in exploration; create route)
        if start <= 3:
            create_route(pg, "14", "httpservice1", "http1-route", ["/http1"])
        # Step 4: upstream with two targets + service + route (load balancer)
        if start <= 4:
            pg.goto(KONGA + "/#!/upstreams", wait_until="networkidle"); pg.wait_for_timeout(1500)
            if not pg.get_by_text("http-upstream", exact=True).count():
                pg.get_by_text("CREATE UPSTREAM").first.click(); pg.wait_for_timeout(1200)
                pg.fill("input[ng-model='upstream.name']", "http-upstream"); shot(pg, "15a-add-upstream-form")
                pg.get_by_text("SUBMIT UPSTREAM").click(); pg.wait_for_timeout(2500); shot(pg, "15b-upstreams-list")
            pg.locator("a", has_text="DETAILS").first.click(); pg.wait_for_timeout(2000); print("upstream URL", pg.url)
            print("=== upstream detail ==="); dump(pg, "a[ng-click], button, a:not([href])")
            pg.get_by_text("Targets", exact=True).first.click(); pg.wait_for_timeout(1200); shot(pg, "15c-upstream-targets-empty")
            print("=== targets tab ==="); dump(pg, "button, input, label")
            for i, port in enumerate(["8081", "8082"]):
                pg.locator("button").filter(has_text="ADD TARGET").first.click(); pg.wait_for_timeout(1000)
                if i == 0: print("=== add target form ==="); dump(pg, "input, label, button")
                pg.locator("input[ng-model='item.target']").fill(f"{IP}:{port}")
                w = pg.locator("input[ng-model='item.weight']")
                if w.count(): w.fill("100")
                if i == 0: shot(pg, "15d-add-target-form")
                pg.get_by_text("SUBMIT TARGET").click(); pg.wait_for_timeout(2000)
            shot(pg, "15e-upstream-targets")
            create_service(pg, "16", "lbservice", "http://http-upstream", "load balanced to SimpleHTTP 8081/8082 via upstream")
            create_route(pg, "17", "lbservice", "lb-route", ["/lb"])
        # Step 5: REST service + route
        if start <= 5:
            create_service(pg, "18", "restservice", f"http://{IP}:3000", "SimpleREST express app on port 3000")
            create_route(pg, "19", "restservice", "rest-route", ["/rest"], strip=True)
        # Step 6: gRPC service + route
        if start <= 6:
            create_service(pg, "20", "grpcservice", f"grpc://{IP}:50051", "SimplegRPC greeter_server on port 50051")
            create_route(pg, "21", "grpcservice", "grpc-route", ["/helloworld.Greeter"], protocols=["grpc", "grpcs"], strip=False)
        # overview pages
        pg.goto(KONGA + "/#!/services", wait_until="networkidle"); pg.wait_for_timeout(2000); shot(pg, "22-all-services")
        pg.goto(KONGA + "/#!/routes", wait_until="networkidle"); pg.wait_for_timeout(2000); shot(pg, "23-all-routes")
        pg.goto(KONGA + "/#!/upstreams", wait_until="networkidle"); pg.wait_for_timeout(2000); shot(pg, "24-all-upstreams")
        b.close()
