"""Render each captures/terminal/*.txt as a terminal-style PNG with Playwright (Chromium)."""
import os, glob, html
from playwright.sync_api import sync_playwright
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "captures", "terminal")
TPL = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;background:#1e1e1e}
.win{width:1100px;background:#1e1e1e;border-radius:8px;overflow:hidden;font-family:'DejaVu Sans Mono','Noto Sans Mono',monospace}
.bar{background:#323233;height:34px;display:flex;align-items:center;padding:0 12px;color:#ccc;font:13px sans-serif}
.dot{width:12px;height:12px;border-radius:50%%;margin-right:8px;display:inline-block}
pre{margin:0;padding:14px 18px;color:#d4d4d4;font-size:14px;line-height:1.45;white-space:pre-wrap;word-break:break-all}
.p{color:#4ec9b0;font-weight:bold}.c{color:#dcdcaa}.ok{color:#6a9955}.err{color:#f14c4c}
.hl{background:#5a3a00;outline:2px solid #ffb300;outline-offset:1px;color:#fff;font-weight:bold;display:inline-block;width:100%%;box-sizing:border-box}
</style></head><body><div class="win"><div class="bar"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span>codespace@codespace_launcher: bash — %s</div><pre>%s</pre></div></body></html>"""
import re
# lines to highlight (regex) per capture; lines matching get a yellow outline
HL = {
 "01": r"Docker version|^v\d|^\d+\.\d+\.\d+$", "02": r"kong:2\.8|konga|postgres:9\.6", "03": r"^[0-9a-f]{64}$", "04": r"^[0-9a-f]{64}$",
 "05": r"migrations processed|executed|up-to-date", "06": r"^[0-9a-f]{64}$", "07": r"HTTP/1\.1 200|Server: kong|Welcome to kong",
 "08": r"migrations completed", "09": r"^[0-9a-f]{64}$", "10": r"^(konga|kong|kong-database)\b", "11": r"^10\.", "12": r"Hello World|username",
 "13": r"service$|^\w+service\s", "14": r"-route", "15": r"10\.0\.10\.51:808", "16": r"HTTP/1\.1 200|Via: kong|X-Kong", "17": r"Hello World",
 "18": r"username", "19": r"message|Hello Watayut", "20": r"username =|key =", "21": r"-auth",
 "22": r"HTTP/1\.1|Unauthorized|username", "23": r"HTTP/1\.1|No API key|Hello World", "24": r"HTTP/1\.1|Invalid authentication",
}
def colorize(text, pat=None):
    out = []
    for line in text.splitlines():
        e = html.escape(line)
        if line.startswith("$ "): out.append('<span class="p">$</span> <span class="c">' + e[2:] + "</span>")
        elif line.startswith("[exit 0]"): out.append('<span class="ok">' + e + "</span>")
        elif line.startswith("[exit"): out.append('<span class="err">' + e + "</span>")
        elif pat and re.search(pat, line): out.append('<span class="hl">' + e + "</span>")
        else: out.append(e)
    return "\n".join(out)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1100, "height": 400})
    for f in sorted(glob.glob(os.path.join(D, "*.txt"))):
        name = os.path.basename(f)[:-4]
        pg.set_content(TPL % (name, colorize(open(f).read())))
        pg.locator(".win").screenshot(path=os.path.join(D, name + ".png")); print("rendered", name)
    b.close()
