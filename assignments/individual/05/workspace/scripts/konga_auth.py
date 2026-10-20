"""Steps 7-8: consumer credentials (basic + key) and auth plugins on services, through the Konga UI."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from konga_build import *

def modal_dump(pg, title):
    print(f"=== {title} ==="); dump(pg, ".modal input, .modal select, .modal label, .modal button")

if __name__ == "__main__":
    with sync_playwright() as p:
        b, pg = browser(p); login(pg)
        # --- consumer Bob: basic-auth credentials
        pg.goto(KONGA + "/#!/consumers", wait_until="networkidle"); pg.wait_for_timeout(1500)
        pg.get_by_text("Bob", exact=True).first.click(); pg.wait_for_timeout(2000)
        pg.get_by_text("Credentials", exact=True).first.click(); pg.wait_for_timeout(1200)
        pg.get_by_text("CREATE CREDENTIALS").first.click(); pg.wait_for_timeout(1500); modal_dump(pg, "basic-auth credential form")
        pg.fill("input[ng-model='credentials.username']", "bob"); pg.fill("input[ng-model='credentials.password']", "bob1234")
        shot(pg, "31a-consumer-basic-auth-form"); pg.locator("button[ng-click='manage()']").click(); pg.wait_for_timeout(2500); shot(pg, "31b-consumer-basic-auth-list")
        # --- consumer Bob: key-auth credentials
        pg.get_by_text("API KEYS", exact=True).first.click(); pg.wait_for_timeout(1200)
        print("=== api keys tab ==="); dump(pg, "button")
        pg.locator("button").filter(has_text="CREATE API KEY").first.click(); pg.wait_for_timeout(1500); modal_dump(pg, "api key form")
        keyin = pg.locator("input[ng-model='credentials.key'], .modal input[type=text]:visible")
        if keyin.count(): keyin.first.fill("bob-secret-key-123")
        shot(pg, "32a-consumer-api-key-form"); pg.locator("button[ng-click='manage()'], .modal button:visible").filter(has_text="SUBMIT").first.click(); pg.wait_for_timeout(2500); shot(pg, "32b-consumer-api-key-list")
        # --- basic-auth plugin on restservice
        open_service(pg, "restservice"); pg.get_by_text("Plugins", exact=True).first.click(); pg.wait_for_timeout(1200)
        pg.locator("button").filter(has_text="ADD PLUGIN").first.click(); pg.wait_for_timeout(1500); shot(pg, "33a-restservice-add-plugin-catalog")
        pg.locator(".modal button").filter(has_text="ADD PLUGIN").nth(0).click(); pg.wait_for_timeout(1500); shot(pg, "33b-restservice-basic-auth-plugin-form")
        pg.locator("button[ng-click='addPlugin()']").click(); pg.wait_for_timeout(3000); shot(pg, "33c-restservice-plugins")
        # --- key-auth plugin on httpservice1
        open_service(pg, "httpservice1"); pg.get_by_text("Plugins", exact=True).first.click(); pg.wait_for_timeout(1200)
        pg.locator("button").filter(has_text="ADD PLUGIN").first.click(); pg.wait_for_timeout(1500)
        pg.locator(".modal button").filter(has_text="ADD PLUGIN").nth(1).click(); pg.wait_for_timeout(1500); modal_dump(pg, "key-auth plugin form"); shot(pg, "34a-httpservice1-key-auth-plugin-form")
        pg.locator("button[ng-click='addPlugin()']").click(); pg.wait_for_timeout(3000); shot(pg, "34b-httpservice1-plugins")
        pg.goto(KONGA + "/#!/plugins", wait_until="networkidle"); pg.wait_for_timeout(2000); shot(pg, "35-all-plugins")
        pg.goto(KONGA + "/#!/consumers", wait_until="networkidle"); pg.wait_for_timeout(2000); shot(pg, "36-all-consumers")
        b.close()
