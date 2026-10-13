#!/usr/bin/env python3
"""Rewrite the run-specific values in report.md (ids, timestamps, which worker took which task)
from the current terminal captures, so the prose always matches the evidence shown."""
import re
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
TERM = HERE / "terminal"
md = (HERE / "report.md").read_text()


def cap(name):
    return (TERM / f"{name}.txt").read_text()


def ts(line):  # "2026-10-13T14:13:57.012+00:00 ..." -> "14:13:57.012"
    return line[11:23]


def when(line):
    return datetime.fromisoformat(line.split(" ")[0])


def sub(pattern, repl, count=1):
    global md
    new, n = re.subn(pattern, repl, md, count=count, flags=re.S)
    if n == 0:
        print("  not found:", pattern[:70])
    md = new


# --- Exercise 1: event id quoted in the explanation
event = re.search(r"RECEIVED id=([0-9a-f]{8})", cap("ex1-unsafe-3-worker-restart")).group(1)
sub(r"already handled event `[0-9a-f]{8}…`", f"already handled event `{event}…`")

# --- Exercise 2: receive times
dur = cap("ex2-3-durable-consumer")
tmp = cap("ex2-4-temporary-consumer")
before = ts(next(l for l in dur.splitlines() if "BEFORE" in l and "RECEIVED" in l))
after_d = ts(next(l for l in dur.splitlines() if '"AFTER"' in l and "RECEIVED" in l))
after_t = ts(next(l for l in tmp.splitlines() if '"AFTER"' in l and "RECEIVED" in l))
sub(r"\| Durable \(`setup` ran first\) \| ✅ received at [0-9:.]+ \(on start-up\) \| ✅ received at [0-9:.]+ \|",
    f"| Durable (`setup` ran first) | ✅ received at {before} (on start-up) | ✅ received at {after_d} |")
sub(r"\| Temporary \(bound after `BEFORE`\) \| ❌ never received \| ✅ received at [0-9:.]+ \|",
    f"| Temporary (bound after `BEFORE`) | ❌ never received | ✅ received at {after_t} |")

# --- Exercise 3: parallel run
done = {}
for w in ("W1", "W2", "W3"):
    text = cap(f"ex3-parallel-{w}")
    start = next(l for l in text.splitlines() if " START " in l)
    fin = next(l for l in text.splitlines() if " DONE " in l)
    task = re.search(r" DONE (\w) elapsed=([0-9.]+)s", fin)
    done[w] = dict(task=task.group(1), elapsed=task.group(2), done=ts(fin), start=when(start), end=when(fin))
order = sorted(done.items(), key=lambda kv: kv[1]["end"])
rank = {w: i for i, (w, _) in enumerate(order)}
words = ["first", "second", "last"]
for w, d in done.items():
    sub(rf"!\[{w} took \w and finished \w+ at [0-9:.]+ \([0-9.]+ s\)\]",
        f"![{w} took {d['task']} and finished {words[rank[w]]} at {d['done']} ({d['elapsed']} s)]")
seq = " → ".join(f"{d['task']} ({d['done']})" for _, d in order)
elapsed = (max(d["end"] for d in done.values()) - min(d["start"] for d in done.values())).total_seconds()
sub(r"\| 3 \(parallel\) \| A → B → C \| \*\*.*?\*\* \| ≈ [0-9.]+ s \|",
    f"| 3 (parallel) | A → B → C | **{seq}** | ≈ {elapsed:.1f} s |")
# the explanation sentence names which worker ran which task
by_task = {d["task"]: w for w, d in done.items()}
sub(r"which is what spread A, B and C across W\d, W\d and W\d",
    f"which is what spread A, B and C across {by_task['A']}, {by_task['B']} and {by_task['C']}")

# --- Exercise 3: serial run
only = cap("ex3-serial-ONLY").splitlines()
dones = [l for l in only if " DONE " in l]
starts = [l for l in only if " START " in l]
seq_s = " → ".join(f"{re.search(r' DONE (\w)', l).group(1)} ({ts(l)})" for l in dones)
elapsed_s = (when(dones[-1]) - when(starts[0])).total_seconds()
sub(r"\| 1 \(sequential\) \| A → B → C \| \*\*.*?\*\* \| ≈ [0-9.]+ s \|",
    f"| 1 (sequential) | A → B → C | **{seq_s}** | ≈ {elapsed_s:.1f} s |")

(HERE / "report.md").write_text(md)
print("report.md refreshed:", event, before, after_d, after_t, seq, f"{elapsed:.1f}s", "|", seq_s, f"{elapsed_s:.1f}s")
