#!/usr/bin/env python3
"""Turn the Kafka JSONL evidence of exercises 4-6 into Markdown tables for the report."""
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
EV = HERE.parent / "messaging_lab_six_exercises" / "evidence"


def rows(name):
    path = EV / name
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def table(header, body):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in body]
    return "\n".join(out)


def ex4():
    print("\n## Exercise 4\n")
    for word, n in (("two", 2), ("four", 4), ("five", 5)):
        body = []
        total = 0
        logs = {i: rows(f"ex4-{word}-C{i}.jsonl") for i in range(1, n + 1)}
        # Assignments after the first Ctrl+C belong to the shutdown rebalance, not to the experiment.
        stop = min((x["timestamp"] for r in logs.values() for x in r if x["kind"] == "interrupted"), default="9")
        for i in range(1, n + 1):
            r = logs[i]
            assigned = [x["partitions"] for x in r if x["kind"] == "assigned" and x["timestamp"] < stop]
            final = assigned[-1] if assigned else None
            done = [x for x in r if x["kind"] == "completed"]
            per_part = Counter(x["partition"] for x in done)
            summary = next((x["unique_completed"] for x in r if x["kind"] == "summary"), "?")
            total += len(done)
            body.append((f"C{i}", " → ".join(str(a) for a in assigned), str(final) if final is not None else "[] (idle)", len(done),
                         ", ".join(f"P{p}:{c}" for p, c in sorted(per_part.items())) or "–", summary))
        pub = rows(f"ex4-{word}-publisher.jsonl")
        pubparts = Counter(x["partition"] for x in pub if x["kind"] == "published")
        print(f"### Group of {n} consumers — topic `lab.ex4.{word}1` (published {len(pub)} records: "
              + ", ".join(f"P{p}:{c}" for p, c in sorted(pubparts.items())) + f"; consumed {total})\n")
        print(table(["Consumer", "Assignment history", "Final partitions", "Records completed", "Per partition", "unique_completed"], body))
        print()
    r = rows("ex4-replay.jsonl")
    assigned = [x["partitions"] for x in r if x["kind"] == "assigned"]
    done = [x for x in r if x["kind"] == "completed"]
    per_part = Counter(x["partition"] for x in done)
    offsets = defaultdict(list)
    for x in done:
        offsets[x["partition"]].append(x["offset"])
    print(f"### Analytics group replay — group `lab.ex4.analytics1` on `lab.ex4.two1`\n")
    print(table(["Consumer", "Assigned partitions", "Records completed", "Per partition", "Offset range per partition"],
                [("Analytics", str(assigned), len(done), ", ".join(f"P{p}:{c}" for p, c in sorted(per_part.items())),
                  "; ".join(f"P{p}: {min(o)}–{max(o)}" for p, o in sorted(offsets.items())))]))


def ex5():
    print("\n## Exercise 5\n")
    for mode in ("keyed", "broken"):
        pub = [x for x in rows(f"ex5-{mode}-publisher.jsonl") if x["kind"] == "published"]
        pub_by_id = {x["event_id"]: x for x in pub}
        events = []
        for i in (1, 2, 3):
            for x in rows(f"ex5-{mode}-C{i}.jsonl"):
                if x["kind"] in ("started", "completed"):
                    events.append(x)
        events.sort(key=lambda x: x["timestamp"])
        completed = [x for x in events if x["kind"] == "completed"]
        print(f"### {mode.capitalize()} mode — topic `lab.ex5.{mode}1` ({len(pub)} published, {len(completed)} completed)\n")
        body = []
        for pos, x in enumerate(completed, 1):
            body.append((pos, x["order_id"], x["sequence"], x["payload"]["action"], f"P{x['partition']}", x["offset"],
                         x["consumer"], x["timestamp"][11:23]))
        print(table(["Finish #", "Order", "Seq", "Event", "Partition", "Offset", "Consumer", "Completed at (UTC)"], body))
        print()
        per_order = defaultdict(list)
        for x in completed:
            per_order[x["order_id"]].append(x["sequence"])
        print(table(["Order", "Partitions used", "Completion sequence", "In order?"],
                    [(o, ", ".join(sorted({f"P{x['partition']}" for x in completed if x["order_id"] == o})),
                      " → ".join(map(str, s)), "✅" if s == sorted(s) else "❌") for o, s in per_order.items()]))
        print()


def ex6():
    print("\n## Exercise 6\n")
    body = []
    for mode in ("unsafe", "safe"):
        r = rows(f"ex6-{mode}.jsonl")
        runs = []
        current = []
        for x in r:
            current.append(x)
            if x["kind"] in ("intentional_crash", "summary"):
                runs.append(current)
                current = []
        for label, run in zip(("first run (crash)", "restart"), runs):
            db = next((x for x in run if x["kind"] == "db_committed"), None)
            committed = any(x["kind"] == "committed" for x in run)
            rec = next((x for x in run if x["kind"] == "received"), {})
            body.append((mode, label, rec.get("offset", "?"), db and db["applied"], db and db["business_effect_count"],
                         "✅ yes" if committed else "❌ no (crashed first)"))
    print(table(["Mode", "Run", "Offset received", "applied", "business_effect_count", "Offset committed?"], body))


if __name__ == "__main__":
    ex4()
    ex5()
    ex6()
