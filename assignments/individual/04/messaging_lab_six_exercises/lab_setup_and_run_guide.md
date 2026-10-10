# Message Queue Lab — Setup & Run Guide

> Read this completely before starting. All commands are run from inside the `messaging_lab_six_exercises/` folder unless stated otherwise.

---

## 1. Prerequisites

You need the following installed on your machine before anything else.

| Requirement | Version | How to check |
|---|---|---|
| Python | 3.10 or newer | `python3 --version` |
| pip | any recent | `pip --version` |
| Docker Desktop | any recent | `docker --version` |
| Docker Compose | v2 (built into Docker Desktop) | `docker compose version` |

**Docker Desktop must be running** before you start the brokers. On Windows and macOS, open Docker Desktop from your applications and wait until the whale icon in the taskbar is steady (not animated).

---

## 2. Folder Structure

After unzipping the lab package you should see:

```
messaging_lab_six_exercises/
├── compose.yaml              ← starts RabbitMQ and Kafka
├── requirements.txt          ← Python dependencies
├── check_local.py            ← pre-flight check (no broker needed)
├── evidence_to_csv.py        ← converts Kafka log files to CSV
├── rabbitmq/
│   ├── common.py
│   ├── demo1_crash_ack.py    ← Exercise 1
│   ├── demo2_late_subscriber.py  ← Exercise 2
│   └── demo3_completion_order.py ← Exercise 3
└── kafka/
    ├── common.py
    ├── effects.py
    ├── ex4_groups.py         ← Exercise 4
    ├── ex5_ordering.py       ← Exercise 5
    └── ex6_crash_commit.py   ← Exercise 6
```

**All commands must be run from the `messaging_lab_six_exercises/` root folder.**

---

## 3. One-Time Environment Setup

Do this once. You only need to repeat it if you delete the `.venv` folder.

### Step 1 — Create a virtual environment

**macOS / Linux:**
```bash
python3 -m venv .venv
```

**Windows (Command Prompt):**
```cmd
py -m venv .venv
```

### Step 2 — Activate the virtual environment

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate
```

You will see `(.venv)` at the start of your prompt when the environment is active. **You must activate the virtual environment in every new terminal window you open.**

### Step 3 — Install Python dependencies

```bash
pip install -r requirements.txt
```

This installs `pika==1.3.2` and `confluent-kafka==2.11.1`.

### Step 4 — Run the pre-flight check

This verifies your Python setup without needing any broker running:

```bash
python check_local.py
```

Expected output:
```
PASS Python syntax
PASS effect/deduplication/rollback: demo1_crash_ack.py
PASS effect/deduplication/rollback: effects.py
PASS seven command-line entry points
PASS commit helper error handling
PASS keyed and deliberately broken event plans
Offline checks passed. Live broker integration is NOT tested here.
```

If any line shows `FAIL`, re-check that your virtual environment is active and dependencies are installed.

---

## 4. Starting the Brokers

The lab uses two brokers — RabbitMQ and Kafka — both running locally in Docker containers.

### Start both brokers

```bash
docker compose up -d
```

### Check they are running

```bash
docker compose ps
```

Wait until both services show `healthy` or `running`. This can take **30–60 seconds** on first start because Docker needs to download the images.

### Port assignments (intentionally non-default to avoid conflicts)

| Service | Port | Purpose |
|---|---|---|
| RabbitMQ | `5673` | AMQP (Python connects here) |
| RabbitMQ Management UI | `15673` | Browser UI — `http://localhost:15673` |
| Kafka | `19092` | Kafka bootstrap (Python connects here) |

RabbitMQ Management UI login: **username** `guest` / **password** `guest`

### If the default ports are already in use

Set environment variables to point scripts at a different broker:

```bash
export RABBITMQ_URL=amqp://guest:guest@localhost:5672/%2F
export KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

### Stopping the brokers (keeps data)

```bash
docker compose stop
```

### Stopping and deleting all data (full reset)

```bash
docker compose down -v
```

> ⚠️ Use `down -v` only when you want to completely start over. It deletes all queues, topics, and offsets.

---

## 5. Creating an Evidence Folder

Kafka exercises write log files. Create a folder for them before starting:

```bash
mkdir evidence
```

---

## 6. Running Each Exercise

> **Before every exercise:** make sure your virtual environment is active (`(.venv)` in the prompt) and the brokers are running (`docker compose ps`).

> **Terminal tip:** exercises that require multiple roles (publisher + workers, or multiple consumers) need **multiple terminal windows open at the same time**, all with the virtual environment activated.

---

### Exercise 1 — RabbitMQ: Crash Before ACK

Uses **2 terminals** (or run sequentially — the worker exits on its own).

**Unsafe mode:**

Terminal 1 — publish one message:
```bash
python rabbitmq/demo1_crash_ack.py publish --mode unsafe --run unsafe1
```

Terminal 1 — start worker that crashes before ACK (exit code 99 is intentional):
```bash
python rabbitmq/demo1_crash_ack.py worker --mode unsafe --run unsafe1 --crash-before-ack
```

Terminal 1 — restart the worker (no new publish):
```bash
python rabbitmq/demo1_crash_ack.py worker --mode unsafe --run unsafe1
```

**Safe mode** (use a fresh `--run` label):
```bash
python rabbitmq/demo1_crash_ack.py publish --mode safe --run safe1
python rabbitmq/demo1_crash_ack.py worker --mode safe --run safe1 --crash-before-ack
python rabbitmq/demo1_crash_ack.py worker --mode safe --run safe1
```

> Use a new `--run` label (e.g. `unsafe2`, `safe2`) each time you repeat the experiment.

---

### Exercise 2 — RabbitMQ: Late Subscribers

Uses **4 terminals**.

**Terminal 1 — setup and publish BEFORE:**
```bash
python rabbitmq/demo2_late_subscriber.py setup --run fanout1
python rabbitmq/demo2_late_subscriber.py publish --run fanout1 --message BEFORE
```

**Terminal 2 — durable consumer (start after BEFORE is published):**
```bash
python rabbitmq/demo2_late_subscriber.py durable --run fanout1
```

**Terminal 3 — temporary consumer (start after BEFORE is published):**
```bash
python rabbitmq/demo2_late_subscriber.py temporary --run fanout1
```

Wait until both consumers print `READY`.

**Terminal 1 — publish AFTER:**
```bash
python rabbitmq/demo2_late_subscriber.py publish --run fanout1 --message AFTER
```

Stop both consumers with `Ctrl+C` when done.

> Use a fresh `--run` label (e.g. `fanout2`) each time you repeat.

---

### Exercise 3 — RabbitMQ: Delivery vs. Completion Order

#### Three-worker run — uses 4 terminals

**Terminals 1, 2, 3 — one worker each:**
```bash
python rabbitmq/demo3_completion_order.py worker --run order1 --name W1
python rabbitmq/demo3_completion_order.py worker --run order1 --name W2
python rabbitmq/demo3_completion_order.py worker --run order1 --name W3
```

Wait until all three print `READY`.

**Terminal 4 — publish:**
```bash
python rabbitmq/demo3_completion_order.py publish --run order1
```

Stop workers with `Ctrl+C` after all tasks complete.

#### One-worker run — uses 2 terminals (fresh run label)

**Terminal 1:**
```bash
python rabbitmq/demo3_completion_order.py worker --run serial1 --name ONLY
```

**Terminal 2:**
```bash
python rabbitmq/demo3_completion_order.py publish --run serial1
```

---

### Exercise 4 — Kafka: Consumer Groups and Partitions

This exercise has three sub-experiments (groups of 2, 4, and 5) plus a replay. Each uses a different topic name.

#### Group of 2 consumers — 3 terminals

**Terminal 1 — setup topic:**
```bash
python kafka/ex4_groups.py setup --topic lab.ex4.two1
```

**Terminals 2 and 3 — one consumer each:**
```bash
python kafka/ex4_groups.py consume --topic lab.ex4.two1 --group lab.ex4.two1 --name C1 --seconds 300 --log evidence/ex4-two-C1.jsonl
python kafka/ex4_groups.py consume --topic lab.ex4.two1 --group lab.ex4.two1 --name C2 --seconds 300 --log evidence/ex4-two-C2.jsonl
```

Wait until partition assignment logs have settled (no new `revoked` lines — allow ~10 s).

**Terminal 1 — publish:**
```bash
python kafka/ex4_groups.py publish --topic lab.ex4.two1 --count 40 --log evidence/ex4-two-publisher.jsonl
```

Stop consumers with `Ctrl+C` after all events complete.

#### Group of 4 consumers — repeat with a new topic

```bash
python kafka/ex4_groups.py setup --topic lab.ex4.four1
# Start C1, C2, C3, C4 in four separate terminals (same pattern as above)
python kafka/ex4_groups.py publish --topic lab.ex4.four1 --count 40 --log evidence/ex4-four-publisher.jsonl
```

#### Group of 5 consumers — repeat with a new topic

```bash
python kafka/ex4_groups.py setup --topic lab.ex4.five1
# Start C1, C2, C3, C4, C5 in five separate terminals
python kafka/ex4_groups.py publish --topic lab.ex4.five1 --count 40 --log evidence/ex4-five-publisher.jsonl
```

#### Analytics group replay (same topic as the group-of-2 experiment)

```bash
python kafka/ex4_groups.py consume --topic lab.ex4.two1 --group lab.ex4.analytics1 --name Analytics --seconds 30 --log evidence/ex4-replay.jsonl
```

No new publish needed — the analytics group reads from the beginning of the retained log.

---

### Exercise 5 — Kafka: Keyed Ordering

#### Keyed mode — 4 terminals

**Terminal 1:**
```bash
python kafka/ex5_ordering.py setup --topic lab.ex5.keyed1
```

**Terminals 2, 3, 4 — one consumer each:**
```bash
python kafka/ex5_ordering.py consume --topic lab.ex5.keyed1 --group lab.ex5.keyed1 --name C1 --seconds 300 --log evidence/ex5-keyed-C1.jsonl
python kafka/ex5_ordering.py consume --topic lab.ex5.keyed1 --group lab.ex5.keyed1 --name C2 --seconds 300 --log evidence/ex5-keyed-C2.jsonl
python kafka/ex5_ordering.py consume --topic lab.ex5.keyed1 --group lab.ex5.keyed1 --name C3 --seconds 300 --log evidence/ex5-keyed-C3.jsonl
```

Wait for assignment to settle.

**Terminal 1 — publish:**
```bash
python kafka/ex5_ordering.py publish --topic lab.ex5.keyed1 --mode keyed --log evidence/ex5-keyed-publisher.jsonl
```

Stop consumers after all 9 events complete.

#### Broken mode — 4 terminals (new topic)

**Terminal 1:**
```bash
python kafka/ex5_ordering.py setup --topic lab.ex5.broken1
```

**Terminals 2, 3, 4:**
```bash
python kafka/ex5_ordering.py consume --topic lab.ex5.broken1 --group lab.ex5.broken1 --mode broken --name C1 --seconds 300 --log evidence/ex5-broken-C1.jsonl
python kafka/ex5_ordering.py consume --topic lab.ex5.broken1 --group lab.ex5.broken1 --mode broken --name C2 --seconds 300 --log evidence/ex5-broken-C2.jsonl
python kafka/ex5_ordering.py consume --topic lab.ex5.broken1 --group lab.ex5.broken1 --mode broken --name C3 --seconds 300 --log evidence/ex5-broken-C3.jsonl
```

**Terminal 1 — publish:**
```bash
python kafka/ex5_ordering.py publish --topic lab.ex5.broken1 --mode broken --log evidence/ex5-broken-publisher.jsonl
```

#### Converting evidence logs to CSV (optional but recommended for submission)

```bash
python evidence_to_csv.py evidence/ex5-keyed-C1.jsonl evidence/ex5-keyed-C2.jsonl evidence/ex5-keyed-C3.jsonl --out evidence/ex5-keyed.csv
python evidence_to_csv.py evidence/ex5-broken-C1.jsonl evidence/ex5-broken-C2.jsonl evidence/ex5-broken-C3.jsonl --out evidence/ex5-broken.csv
```

---

### Exercise 6 — Kafka: Crash Before Offset Commit

#### Unsafe mode

```bash
python kafka/ex6_crash_commit.py setup --topic lab.ex6.unsafe1
python kafka/ex6_crash_commit.py publish --topic lab.ex6.unsafe1
python kafka/ex6_crash_commit.py consume --topic lab.ex6.unsafe1 --group lab.ex6.unsafe1 --mode unsafe --crash-before-commit --log evidence/ex6-unsafe.jsonl
```

Exit code 99 is intentional — the consumer crashed before committing its offset. Wait ~10 s for the session timeout. Then restart **without** the crash flag and **without** publishing again:

```bash
python kafka/ex6_crash_commit.py consume --topic lab.ex6.unsafe1 --group lab.ex6.unsafe1 --mode unsafe --log evidence/ex6-unsafe.jsonl
```

#### Safe mode (new topic)

```bash
python kafka/ex6_crash_commit.py setup --topic lab.ex6.safe1
python kafka/ex6_crash_commit.py publish --topic lab.ex6.safe1
python kafka/ex6_crash_commit.py consume --topic lab.ex6.safe1 --group lab.ex6.safe1 --mode safe --crash-before-commit --log evidence/ex6-safe.jsonl
python kafka/ex6_crash_commit.py consume --topic lab.ex6.safe1 --group lab.ex6.safe1 --mode safe --log evidence/ex6-safe.jsonl
```

---

## 7. Common Problems and Fixes

| Problem | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: pika` or `confluent_kafka` | Virtual environment not active | Run `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate` (Windows) |
| `Connection refused` on RabbitMQ | Broker not running or not ready | Run `docker compose ps` and wait for `healthy` status |
| `Connection refused` on Kafka | Broker not ready yet | Wait 30 s, check `docker compose logs kafka` |
| `PASS` lines missing from `check_local.py` | Dependencies missing | Run `pip install -r requirements.txt` again |
| Topic setup fails with partition-count mismatch | Reusing a topic name with different settings | Use a new topic name (e.g. `lab.ex4.two2`) |
| Consumer receives nothing on replay | Same group name was used — offset is already committed | Use a different `--group` name for replay |
| Exit code 99 looks like an error | Intentional simulated crash | This is expected — proceed to the restart command |
| Kafka consumer takes a long time to start receiving | Waiting for group rebalance | Allow 10–30 s after starting consumers before publishing |
| `docker compose` command not found | Old Docker installation with separate `docker-compose` tool | Try `docker-compose` (with a hyphen) instead |
| Kafka logs show `AccessDeniedException: /tmp/kraft-combined-logs` | Volume mounted at a root-owned path (`/tmp`) — deleting the volume does not help | See **Kafka Permission Error** section below — replace `compose.yaml` with the fixed version |

---

## 8. Kafka Permission Error (AccessDeniedException)

If you open Docker Desktop logs for the Kafka container and see:

```
Error while writing meta.properties file /tmp/kraft-combined-logs:
java.nio.file.AccessDeniedException: /tmp/kraft-combined-logs/bootstrap.checkpoint.tmp
```

### Root cause

The original `compose.yaml` mounts the Docker volume at `/tmp/kraft-combined-logs`. When Docker mounts a named volume there, it creates the directory owned by **root** — but Kafka runs as `appuser` (uid=1000) and cannot write to it. Deleting the volume does not help because Docker recreates it with the same root ownership every time.

The fix is to move the volume mount to `/var/lib/kafka/data`, a directory that already belongs to `appuser` inside the `apache/kafka` image.

### Fix — replace compose.yaml

A corrected `compose.yaml` is provided alongside this guide. It makes three changes from the original:

| Setting | Original | Fixed |
|---|---|---|
| `KAFKA_LOG_DIRS` | `/tmp/kraft-combined-logs` | `/var/lib/kafka/data` |
| Volume mount point | `kafka-data:/tmp/kraft-combined-logs` | `kafka-data:/var/lib/kafka/data` |
| Kafka healthcheck | *(missing)* | Added — waits until broker is ready |

**Step 1 — Replace `compose.yaml` with the fixed version:**

Copy the provided `compose.yaml` file into your `messaging_lab_six_exercises/` folder, overwriting the original.

**Step 2 — Stop and remove the old broken volume:**
```bash
docker compose down -v
```

> `down -v` is required here — it removes the old volume so Docker recreates it at the new path with correct ownership. This also removes RabbitMQ data, so do this before starting any exercises.

**Step 3 — Start again with the fixed file:**
```bash
docker compose up -d
```

**Step 4 — Confirm both brokers are healthy:**
```bash
docker compose ps
```

Wait until both `rabbitmq` and `kafka` show `healthy`. Kafka may take up to **60 seconds** on first start.

**Step 5 — Confirm in the logs (no errors):**
```bash
docker compose logs kafka | tail -5
```

You should see `Kafka Server started` with no `AccessDeniedException`.

---

## 9. Quick Reference — All Run Commands

```bash
# ── Environment ──────────────────────────────────────────────────────
source .venv/bin/activate          # macOS/Linux (every terminal)
.venv\Scripts\activate             # Windows (every terminal)
docker compose up -d               # start brokers
docker compose ps                  # check broker status
mkdir evidence                     # create evidence folder (once)
python check_local.py              # verify Python setup

# ── Exercise 1 ───────────────────────────────────────────────────────
python rabbitmq/demo1_crash_ack.py publish --mode unsafe --run unsafe1
python rabbitmq/demo1_crash_ack.py worker  --mode unsafe --run unsafe1 --crash-before-ack
python rabbitmq/demo1_crash_ack.py worker  --mode unsafe --run unsafe1
python rabbitmq/demo1_crash_ack.py publish --mode safe   --run safe1
python rabbitmq/demo1_crash_ack.py worker  --mode safe   --run safe1 --crash-before-ack
python rabbitmq/demo1_crash_ack.py worker  --mode safe   --run safe1

# ── Exercise 2 ───────────────────────────────────────────────────────
python rabbitmq/demo2_late_subscriber.py setup     --run fanout1
python rabbitmq/demo2_late_subscriber.py publish   --run fanout1 --message BEFORE
python rabbitmq/demo2_late_subscriber.py durable   --run fanout1          # Terminal A
python rabbitmq/demo2_late_subscriber.py temporary --run fanout1          # Terminal B
python rabbitmq/demo2_late_subscriber.py publish   --run fanout1 --message AFTER

# ── Exercise 3 ───────────────────────────────────────────────────────
python rabbitmq/demo3_completion_order.py worker  --run order1  --name W1    # Terminal 1
python rabbitmq/demo3_completion_order.py worker  --run order1  --name W2    # Terminal 2
python rabbitmq/demo3_completion_order.py worker  --run order1  --name W3    # Terminal 3
python rabbitmq/demo3_completion_order.py publish --run order1               # Terminal 4
python rabbitmq/demo3_completion_order.py worker  --run serial1 --name ONLY  # Terminal 1
python rabbitmq/demo3_completion_order.py publish --run serial1              # Terminal 2

# ── Exercise 4 ───────────────────────────────────────────────────────
python kafka/ex4_groups.py setup   --topic lab.ex4.two1
python kafka/ex4_groups.py consume --topic lab.ex4.two1  --group lab.ex4.two1  --name C1 --seconds 300 --log evidence/ex4-two-C1.jsonl
python kafka/ex4_groups.py consume --topic lab.ex4.two1  --group lab.ex4.two1  --name C2 --seconds 300 --log evidence/ex4-two-C2.jsonl
python kafka/ex4_groups.py publish --topic lab.ex4.two1  --count 40 --log evidence/ex4-two-publisher.jsonl
python kafka/ex4_groups.py consume --topic lab.ex4.two1  --group lab.ex4.analytics1 --name Analytics --seconds 30 --log evidence/ex4-replay.jsonl

# ── Exercise 5 ───────────────────────────────────────────────────────
python kafka/ex5_ordering.py setup   --topic lab.ex5.keyed1
python kafka/ex5_ordering.py consume --topic lab.ex5.keyed1  --group lab.ex5.keyed1  --name C1 --seconds 300 --log evidence/ex5-keyed-C1.jsonl
python kafka/ex5_ordering.py consume --topic lab.ex5.keyed1  --group lab.ex5.keyed1  --name C2 --seconds 300 --log evidence/ex5-keyed-C2.jsonl
python kafka/ex5_ordering.py consume --topic lab.ex5.keyed1  --group lab.ex5.keyed1  --name C3 --seconds 300 --log evidence/ex5-keyed-C3.jsonl
python kafka/ex5_ordering.py publish --topic lab.ex5.keyed1  --mode keyed  --log evidence/ex5-keyed-publisher.jsonl
python kafka/ex5_ordering.py setup   --topic lab.ex5.broken1
python kafka/ex5_ordering.py consume --topic lab.ex5.broken1 --group lab.ex5.broken1 --mode broken --name C1 --seconds 300 --log evidence/ex5-broken-C1.jsonl
python kafka/ex5_ordering.py consume --topic lab.ex5.broken1 --group lab.ex5.broken1 --mode broken --name C2 --seconds 300 --log evidence/ex5-broken-C2.jsonl
python kafka/ex5_ordering.py consume --topic lab.ex5.broken1 --group lab.ex5.broken1 --mode broken --name C3 --seconds 300 --log evidence/ex5-broken-C3.jsonl
python kafka/ex5_ordering.py publish --topic lab.ex5.broken1 --mode broken --log evidence/ex5-broken-publisher.jsonl
python evidence_to_csv.py evidence/ex5-keyed-C1.jsonl  evidence/ex5-keyed-C2.jsonl  evidence/ex5-keyed-C3.jsonl  --out evidence/ex5-keyed.csv
python evidence_to_csv.py evidence/ex5-broken-C1.jsonl evidence/ex5-broken-C2.jsonl evidence/ex5-broken-C3.jsonl --out evidence/ex5-broken.csv

# ── Exercise 6 ───────────────────────────────────────────────────────
python kafka/ex6_crash_commit.py setup   --topic lab.ex6.unsafe1
python kafka/ex6_crash_commit.py publish --topic lab.ex6.unsafe1
python kafka/ex6_crash_commit.py consume --topic lab.ex6.unsafe1 --group lab.ex6.unsafe1 --mode unsafe --crash-before-commit --log evidence/ex6-unsafe.jsonl
python kafka/ex6_crash_commit.py consume --topic lab.ex6.unsafe1 --group lab.ex6.unsafe1 --mode unsafe --log evidence/ex6-unsafe.jsonl
python kafka/ex6_crash_commit.py setup   --topic lab.ex6.safe1
python kafka/ex6_crash_commit.py publish --topic lab.ex6.safe1
python kafka/ex6_crash_commit.py consume --topic lab.ex6.safe1   --group lab.ex6.safe1   --mode safe   --crash-before-commit --log evidence/ex6-safe.jsonl
python kafka/ex6_crash_commit.py consume --topic lab.ex6.safe1   --group lab.ex6.safe1   --mode safe   --log evidence/ex6-safe.jsonl
```
