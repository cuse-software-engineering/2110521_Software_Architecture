"""Shared Playwright helpers for driving Konga (http://localhost:1337)."""
import os, sys
from playwright.sync_api import sync_playwright
KONGA = "http://localhost:1337"
CAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "captures", "konga")
ADMIN = dict(username="admin", email="watayut@example.com", password="adminadminadmin")

def shot(pg, name):
    pg.wait_for_timeout(800)
    path = os.path.join(CAP, name + ".png"); pg.screenshot(path=path, full_page=False); print("  saved", name)

def dump(pg, sel="input, button, a, select, textarea, [ng-click]"):
    for el in pg.query_selector_all(sel):
        try:
            print("   ", el.evaluate("e=>[e.tagName,e.type||'',e.name||'',e.placeholder||'',(e.innerText||'').trim().slice(0,50),e.getAttribute('href')||'',e.getAttribute('ng-click')||'',e.getAttribute('ng-model')||'']"))
        except Exception: pass

def login(pg):
    pg.goto(KONGA + "/", wait_until="networkidle"); pg.wait_for_timeout(1500)
    if "/register" in pg.url:
        pg.fill("input[name=username]", ADMIN["username"]); pg.fill("input[name=email]", ADMIN["email"])
        pg.fill("input[name=password]", ADMIN["password"]); pg.fill("input[name=password_confirmation]", ADMIN["password"])
        shot(pg, "01-register-admin"); pg.get_by_role("button").first.click(); pg.wait_for_timeout(3000)
    if "/login" in pg.url:
        pg.fill("input[name=username]", ADMIN["username"]); pg.fill("input[name=password]", ADMIN["password"])
        shot(pg, "02-login"); pg.get_by_role("button").first.click(); pg.wait_for_timeout(3000)
    print("  after login:", pg.url)

def browser(p):
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1440, "height": 900}); pg = ctx.new_page(); return b, pg
