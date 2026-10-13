#!/usr/bin/env python3
"""Run the six messaging-lab exercises end to end and collect evidence for the report.

For every command it writes terminal/<step>.txt (the command line, its output and exit code),
and at key moments it screenshots the RabbitMQ management UI into screenshots/ with Playwright.
Kafka exercises additionally write the JSONL evidence files that the lab guide names
into messaging_lab_six_exercises/evidence/.
"""
import json
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
LAB = HERE.parent / "messaging_lab_six_exercises"
PY = LAB / ".venv" / "bin" / "python"
TERM = HERE / "terminal"
SHOTS = HERE / "screenshots"
UI = "http://127.0.0.1:15673"
PROMPT = "(.venv) $ "
SUFFIX = "1"  # run-label suffix, e.g. unsafe1 / fanout1 / order1
ENV = dict(os.environ, PYTHONUNBUFFERED="1")

TERM.mkdir(exist_ok=True)
SHOTS.mkdir(exist_ok=True)


def say(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


# ----------------------------------------------------------------------------- processes

def run(step, args, timeout=180):
    """Run one command to completion; record command, output and exit code."""
    cmd = ["python", *args]
    say(f"run  {step}: {' '.join(cmd)}")
    proc = subprocess.run([str(PY), *args], cwd=LAB, env=ENV, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    text = f"{PROMPT}{' '.join(cmd)}\n{proc.stdout}"
    if proc.returncode:
        text += f"[process exited with code {proc.returncode}]\n"
    (TERM / f"{step}.txt").write_text(text)
    return proc.stdout, proc.returncode


class Bg:
    """A long-running role (worker / consumer) in its own 'terminal'."""

    def __init__(self, step, args):
        self.step = step
        self.path = TERM / f"{step}.txt"
        cmd = ["python", *args]
        say(f"start {step}: {' '.join(cmd)}")
        self.path.write_text(f"{PROMPT}{' '.join(cmd)}\n")
        self.file = open(self.path, "a")
        self.proc = subprocess.Popen([str(PY), *args], cwd=LAB, env=ENV,
                                     stdout=self.file, stderr=subprocess.STDOUT)

    def text(self):
        return self.path.read_text()

    def count(self, pattern):
        return len(re.findall(pattern, self.text()))

    def wait_for(self, pattern, n=1, timeout=120):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.count(pattern) >= n:
                return
            if self.proc.poll() is not None:
                break
            time.sleep(0.2)
        raise RuntimeError(f"{self.step}: did not see {n}x /{pattern}/ in time\n{self.text()}")

    def stop(self):
        """Ctrl+C the process, like stopping a terminal by hand."""
        if self.proc.poll() is None:
            self.proc.send_signal(signal.SIGINT)
            try:
                self.proc.wait(20)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()
        self.file.write("^C\n")
        if self.proc.returncode:
            self.file.write(f"[process exited with code {self.proc.returncode}]\n")
        self.file.close()
        say(f"stop  {self.step} (exit {self.proc.returncode})")


def stop_all(procs):
    """Ctrl+C every consumer of a group at the same moment, so no SIGINT lands inside a rebalance callback."""
    for p in procs:
        if p.proc.poll() is None:
            p.proc.send_signal(signal.SIGINT)
    for p in procs:
        p.stop()


def wait_quiet(procs, settle=8, timeout=90):
    """Wait until none of the logs has changed for `settle` seconds (rebalance settled)."""
    deadline = time.time() + timeout
    last = {p.step: p.text() for p in procs}
    stamp = time.time()
    while time.time() < deadline:
        time.sleep(1)
        now = {p.step: p.text() for p in procs}
        if now != last:
            last, stamp = now, time.time()
        elif time.time() - stamp >= settle:
            return
    say("warning: logs never went quiet; continuing")


def total(procs, pattern):
    return sum(p.count(pattern) for p in procs)


def wait_total(procs, pattern, n, timeout=120):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if total(procs, pattern) >= n:
            return
        time.sleep(0.3)
    raise RuntimeError(f"expected {n}x /{pattern}/ across {[p.step for p in procs]}, "
                       f"got {total(procs, pattern)}")


# ----------------------------------------------------------------------------- RabbitMQ UI

class Ui:
    def __init__(self):
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch()
        self.page = self.browser.new_page(viewport={"width": 1400, "height": 900})
        self.page.goto(UI + "/", wait_until="networkidle")
        self.page.fill('input[name="username"]', "guest")
        self.page.fill('input[name="password"]', "guest")
        self.page.click('input[type="submit"]')
        self.page.wait_for_timeout(1500)
        assert self.page.locator("text=Overview").count(), "RabbitMQ UI login failed"

    def shot(self, name, route, settle=2500, expand=("Bindings", "Consumers"), focus=(), crop=True):
        """Screenshot #/route. `focus` = selectors (or (selector, nth) pairs) to outline in red; with `crop`
        the image is cut from the page title down to the lowest outlined element."""
        self.page.goto(f"{UI}/#/{route}", wait_until="networkidle")
        self.page.wait_for_timeout(settle)
        for _ in range(10):  # queue/exchange pages: wait for the first stats sample
            if not self.page.locator("text=Waiting for data").count():
                break
            self.page.wait_for_timeout(1000)
        for heading in expand:
            h2 = self.page.locator(f"h2:has-text('{heading}')")
            for _ in range(4):  # the page auto-refreshes; retry until the section is really open
                if not h2.count() or "section-visible" in h2.first.evaluate("e => e.parentElement.className"):
                    break
                h2.first.click()
                self.page.wait_for_timeout(600)
        boxes = []
        for item in focus:
            selector, nth = (item, 0) if isinstance(item, str) else item
            loc = self.page.locator(selector).nth(nth)
            if not loc.count():
                say(f"      focus not found: {item}")
                continue
            loc.evaluate("e => { e.style.outline = '4px solid #e00000'; e.style.outlineOffset = '5px'; "
                         "e.style.boxShadow = '0 0 0 9px rgba(224,0,0,0.12)'; }")
            boxes.append(loc.bounding_box())
        clip = None
        if crop and boxes:
            title = self.page.locator("h1").first.bounding_box()
            top = max(0, (title["y"] if title else boxes[0]["y"]) - 8)
            bottom = max(b["y"] + b["height"] for b in boxes) + 22
            clip = {"x": 20, "y": top, "width": 1360, "height": bottom - top}
        self.page.screenshot(path=str(SHOTS / f"{name}.png"), full_page=True, clip=clip)
        say(f"shot  {name}  (#/{route})")

    def close(self):
        self.browser.close()
        self.pw.stop()


def q(name):
    return f"queues/%2F/{name}"


def x(name):
    return f"exchanges/%2F/{name}"


# ----------------------------------------------------------------------------- exercises

def exercise1(ui):
    say("=== Exercise 1: crash before ACK ===")
    for mode in ("unsafe", "safe"):
        run_label = f"{mode}{SUFFIX}"
        queue = f"lab.failure.crash.{mode}.{run_label}"
        run(f"ex1-{mode}-1-publish", ["rabbitmq/demo1_crash_ack.py", "publish", "--mode", mode, "--run", run_label])
        ui.shot(f"ex1-{mode}-queue-after-publish", q(queue), focus=[("table.legend", 1), ("table.facts", 1), ("table.facts", 2)])
        _, code = run(f"ex1-{mode}-2-worker-crash",
                      ["rabbitmq/demo1_crash_ack.py", "worker", "--mode", mode, "--run", run_label, "--crash-before-ack"])
        assert code == 99, f"expected intentional exit 99, got {code}"
        ui.shot(f"ex1-{mode}-queue-after-crash", q(queue), focus=[("table.legend", 1), ("table.facts", 1), ("table.facts", 2)])
        run(f"ex1-{mode}-3-worker-restart", ["rabbitmq/demo1_crash_ack.py", "worker", "--mode", mode, "--run", run_label])
        ui.shot(f"ex1-{mode}-queue-after-restart", q(queue), focus=[("table.legend", 1), ("table.facts", 1), ("table.facts", 2)])


def exercise2(ui):
    say("=== Exercise 2: late subscribers ===")
    label = f"fanout{SUFFIX}"
    exchange = f"lab.failure.fanout.{label}"
    run("ex2-1-setup", ["rabbitmq/demo2_late_subscriber.py", "setup", "--run", label])
    run("ex2-2-publish-before", ["rabbitmq/demo2_late_subscriber.py", "publish", "--run", label, "--message", "BEFORE"])
    ui.shot("ex2-exchange-after-before", x(exchange), focus=["div.bindings-wrapper"])
    ui.shot("ex2-queues-after-before", "queues", focus=[f'table.list tr:has-text("{exchange}.saved")'])
    durable = Bg("ex2-3-durable-consumer", ["rabbitmq/demo2_late_subscriber.py", "durable", "--run", label])
    durable.wait_for(r"READY")
    temporary = Bg("ex2-4-temporary-consumer", ["rabbitmq/demo2_late_subscriber.py", "temporary", "--run", label])
    temporary.wait_for(r"READY")
    time.sleep(1)
    ui.shot("ex2-exchange-bindings-both-consumers", x(exchange), focus=["div.bindings-wrapper"])
    ui.shot("ex2-queues-both-consumers", "queues",
            focus=['table.list tr:has-text("amq.gen")', f'table.list tr:has-text("{exchange}.saved")'])
    run("ex2-5-publish-after", ["rabbitmq/demo2_late_subscriber.py", "publish", "--run", label, "--message", "AFTER"])
    durable.wait_for(r"RECEIVED .*AFTER")
    temporary.wait_for(r"RECEIVED .*AFTER")
    time.sleep(1)
    durable.stop()
    temporary.stop()
    time.sleep(1)
    ui.shot("ex2-queues-after-consumers-stopped", "queues", focus=["table.list"])


def exercise3(ui):
    say("=== Exercise 3: delivery vs completion order ===")
    order, serial = f"order{SUFFIX}", f"serial{SUFFIX}"
    queue = f"lab.failure.order.{order}"
    workers = [Bg(f"ex3-parallel-W{i}", ["rabbitmq/demo3_completion_order.py", "worker", "--run", order, "--name", f"W{i}"])
               for i in (1, 2, 3)]
    for w in workers:
        w.wait_for(r"READY")
    time.sleep(6)  # let the management plugin publish a stats sample that includes the 3 consumers
    ui.shot("ex3-queue-three-workers-ready", q(queue),
            focus=[("table.facts", 1), 'div.section-visible:has(h2:has-text("Consumers")) table.list'])
    run("ex3-parallel-publish", ["rabbitmq/demo3_completion_order.py", "publish", "--run", order])
    time.sleep(2.5)
    ui.shot("ex3-queue-three-workers-busy", q(queue), settle=300,
            focus=[("table.legend", 1), ("table.facts", 1), 'div.section-visible:has(h2:has-text("Consumers")) table.list'])
    wait_total(workers, r" DONE ", 3, timeout=30)
    time.sleep(0.5)
    for w in workers:
        w.stop()
    only = Bg("ex3-serial-ONLY", ["rabbitmq/demo3_completion_order.py", "worker", "--run", serial, "--name", "ONLY"])
    only.wait_for(r"READY")
    run("ex3-serial-publish", ["rabbitmq/demo3_completion_order.py", "publish", "--run", serial])
    time.sleep(2.5)
    ui.shot("ex3-queue-one-worker-backlog", q(f"lab.failure.order.{serial}"), settle=300,
            focus=[("table.legend", 1), ("table.facts", 1), 'div.section-visible:has(h2:has-text("Consumers")) table.list'])
    only.wait_for(r" DONE ", n=3, timeout=30)
    time.sleep(0.5)
    only.stop()


def consumers(script, topic, group, names, prefix, extra=()):
    procs = []
    for name in names:
        procs.append(Bg(f"{prefix}-{name}", [script, "consume", "--topic", topic, "--group", group, "--name", name,
                                               "--seconds", "300", "--log", f"evidence/{prefix}-{name}.jsonl", *extra]))
        time.sleep(1.5)
    for p in procs:
        p.wait_for(r'"kind": "assigned"', timeout=90)
    wait_quiet(procs, settle=8)
    return procs


def exercise4():
    say("=== Exercise 4: consumer groups and partitions ===")
    for word, n in (("two", 2), ("four", 4), ("five", 5)):
        topic = f"lab.ex4.{word}{SUFFIX}"
        run(f"ex4-{word}-0-setup", ["kafka/ex4_groups.py", "setup", "--topic", topic])
        procs = consumers("kafka/ex4_groups.py", topic, topic, [f"C{i}" for i in range(1, n + 1)], f"ex4-{word}")
        run(f"ex4-{word}-publish", ["kafka/ex4_groups.py", "publish", "--topic", topic, "--count", "40",
                                    "--log", f"evidence/ex4-{word}-publisher.jsonl"])
        wait_total(procs, r'"kind": "completed"', 40, timeout=90)
        time.sleep(1)
        stop_all(procs)
    run("ex4-replay-analytics", ["kafka/ex4_groups.py", "consume", "--topic", f"lab.ex4.two{SUFFIX}", "--group", f"lab.ex4.analytics{SUFFIX}",
                                 "--name", "Analytics", "--seconds", "30", "--log", "evidence/ex4-replay.jsonl"], timeout=120)


def exercise5():
    say("=== Exercise 5: keyed ordering ===")
    for mode, expected in (("keyed", 9), ("broken", 3)):
        topic = f"lab.ex5.{mode}{SUFFIX}"
        run(f"ex5-{mode}-0-setup", ["kafka/ex5_ordering.py", "setup", "--topic", topic])
        extra = ("--mode", "broken") if mode == "broken" else ()
        procs = consumers("kafka/ex5_ordering.py", topic, topic, ["C1", "C2", "C3"], f"ex5-{mode}", extra)
        run(f"ex5-{mode}-publish", ["kafka/ex5_ordering.py", "publish", "--topic", topic, "--mode", mode,
                                    "--log", f"evidence/ex5-{mode}-publisher.jsonl"])
        wait_total(procs, r'"kind": "completed"', expected, timeout=90)
        time.sleep(1)
        stop_all(procs)
        run(f"ex5-{mode}-csv", ["evidence_to_csv.py", *[f"evidence/ex5-{mode}-C{i}.jsonl" for i in (1, 2, 3)],
                                "--out", f"evidence/ex5-{mode}.csv"])


def exercise6():
    say("=== Exercise 6: crash before offset commit ===")
    for mode in ("unsafe", "safe"):
        topic = f"lab.ex6.{mode}{SUFFIX}"
        log = f"evidence/ex6-{mode}.jsonl"
        run(f"ex6-{mode}-0-setup", ["kafka/ex6_crash_commit.py", "setup", "--topic", topic])
        run(f"ex6-{mode}-1-publish", ["kafka/ex6_crash_commit.py", "publish", "--topic", topic])
        _, code = run(f"ex6-{mode}-2-consume-crash", ["kafka/ex6_crash_commit.py", "consume", "--topic", topic, "--group", topic,
                                                      "--mode", mode, "--crash-before-commit", "--log", log])
        assert code == 99, f"expected intentional exit 99, got {code}"
        say("waiting 12 s for the Kafka session timeout of the crashed member")
        time.sleep(12)
        run(f"ex6-{mode}-3-consume-restart", ["kafka/ex6_crash_commit.py", "consume", "--topic", topic, "--group", topic,
                                              "--mode", mode, "--log", log], timeout=150)


def main():
    global SUFFIX
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", choices=["all", "rabbit", "kafka"], default="all")
    ap.add_argument("--suffix", default=SUFFIX, help="run-label suffix (use a fresh one for every repeat)")
    a = ap.parse_args()
    SUFFIX = a.suffix
    (LAB / "evidence").mkdir(exist_ok=True)
    ui = Ui()
    try:
        if a.only in ("all", "rabbit"):
            ui.shot("00-overview-start", "")
            exercise1(ui)
            exercise2(ui)
            exercise3(ui)
        if a.only in ("all", "kafka"):
            exercise4()
            exercise5()
            exercise6()
        ui.shot("99-overview-end", "", crop=False)
        ui.shot("99-queues-end", "queues", crop=False)
        ui.shot("99-exchanges-end", "exchanges", crop=False)
    finally:
        ui.close()
    say("ALL DONE")


if __name__ == "__main__":
    main()
