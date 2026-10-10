# Message Queue Lab — Objectives & Expected Outcomes

---

## Overview

This lab covers six exercises across two message brokers — **RabbitMQ** (via Pika) and **Kafka** (via confluent-kafka). Each exercise is self-contained and builds on a core concept in reliable message processing.

| File | Exercise |
|---|---|
| `rabbitmq/demo1_crash_ack.py` | Exercise 1 – Crash before ACK |
| `rabbitmq/demo2_late_subscriber.py` | Exercise 2 – Late subscribers |
| `rabbitmq/demo3_completion_order.py` | Exercise 3 – Delivery vs completion order |
| `kafka/ex4_groups.py` | Exercise 4 – Consumer groups and partitions |
| `kafka/ex5_ordering.py` | Exercise 5 – Keyed ordering |
| `kafka/ex6_crash_commit.py` | Exercise 6 – Crash before offset commit |

---

## Exercise 1 — RabbitMQ: Crash Before ACK

### What you will observe

This exercise demonstrates what happens when a consumer commits a database change and then crashes **before** sending an acknowledgement (ACK) back to RabbitMQ.

You will run the same scenario twice — once in **unsafe** mode (no deduplication) and once in **safe** mode (idempotent processing).

### Learning Objectives

1. Understand that RabbitMQ's at-least-once delivery guarantee requires explicit acknowledgement (ACK).
2. Observe that a crash between a committed business effect and the ACK causes the broker to redeliver the message.
3. Understand that idempotency is the consumer's responsibility, not the broker's.
4. Implement an atomic deduplication strategy using a unique event ID and a database marker.

### What you should be able to explain afterwards

- What happens to an unacknowledged message when its consumer process dies.
- Why the unsafe mode produces two database entries for one published message.
- How the `INSERT OR IGNORE` pattern combined with a shared transaction prevents the duplicate.
- Why the dedupe marker and the business effect must be in the **same** database transaction — not two separate commits.
- The difference between `os._exit()` and `sys.exit()`, and why only `os._exit()` faithfully simulates a crash.

### Expected results

| Run | `applied` | `business_effect_count` |
|---|---|---|
| Unsafe — first run (crash) | `True` | `1` |
| Unsafe — restart | `True` | `2` ← duplicate |
| Safe — first run (crash) | `True` | `1` |
| Safe — restart | `False` | `1` ← deduplicated |

### What to submit

- [ ] Terminal output from the **unsafe** mode — both the crash run and the restart, showing `applied` and `business_effect_count`
- [ ] Terminal output from the **safe** mode — both the crash run and the restart, showing `applied` and `business_effect_count`
- [ ] Written explanation (3–5 sentences): Why does the unsafe mode produce a duplicate? How does the safe mode prevent it, and what role does the single transaction play?

---

## Exercise 2 — RabbitMQ: Late Subscribers

### What you will observe

This exercise shows that a fanout exchange **routes to queues that are bound at the moment of publication**. A queue that is created or bound after a message is published will never receive that message.

You will compare a durable queue (created and bound before any messages are published) with a temporary exclusive queue (created after the first message is published).

### Learning Objectives

1. Understand that a fanout exchange is a routing mechanism, not a message store.
2. Distinguish between queue durability (survives broker restart) and message buffering (queue holds messages while its consumer is offline).
3. Recognise that a queue must exist and be bound **before** a message is published for that message to be received.
4. Understand the lifecycle of an exclusive auto-delete queue — it is deleted when its owning connection closes.

### What you should be able to explain afterwards

- Why the temporary queue misses the `BEFORE` message.
- Why the durable queue receives both `BEFORE` and `AFTER` even though its consumer was offline during the first publication.
- The difference between queue durability and message persistence — these are two separate settings.
- What happens if you call `publish` without ever running `setup` first.

### Expected results

| Consumer | `BEFORE` message | `AFTER` message |
|---|---|---|
| Durable (`setup` ran first) | ✅ Received | ✅ Received |
| Temporary (bound after `BEFORE`) | ❌ Missed | ✅ Received |

### What to submit

- [ ] Terminal output from the **durable** consumer showing both `BEFORE` and `AFTER` received
- [ ] Terminal output from the **temporary** consumer showing `AFTER` received and `BEFORE` missing
- [ ] Written explanation (3–5 sentences): Why did the temporary queue miss `BEFORE`? What would need to change for it to receive `BEFORE`?

---

## Exercise 3 — RabbitMQ: Delivery vs. Completion Order

### What you will observe

Three tasks — A (5 s), B (1 s), C (2 s) — are delivered to three workers in order A→B→C. Because the workers process them concurrently and each task takes a different amount of time, the **completion** order differs from the delivery order.

You will then repeat the experiment with a single worker and observe that completion order matches delivery order, at the cost of longer total time.

### Learning Objectives

1. Understand that message delivery order does not determine completion order.
2. Understand how `prefetch_count=1` enables fair dispatch across multiple workers.
3. Observe that concurrent processing of variable-duration tasks produces out-of-order completion.
4. Understand the trade-off between concurrency (throughput) and sequential processing (ordering).
5. Recognise when sequential processing is necessary and what it costs.

### What you should be able to explain afterwards

- Why B finishes before A even though A was delivered first.
- What `prefetch_count=1` does and why removing it would change the behaviour.
- Why `connection.sleep()` is used instead of `time.sleep()` inside the callback.
- How you would design a system that needs to process each **order's** events in sequence while still processing different orders concurrently.

### Expected results

| Workers | Completion order | Total time |
|---|---|---|
| 3 (parallel) | B, C, A (typical) | ≈5 s |
| 1 (sequential) | A, B, C (guaranteed) | ≈8 s |

### What to submit

- [ ] Terminal output from the **3-worker** run showing completion order
- [ ] Terminal output from the **1-worker** run showing completion order
- [ ] Written explanation (3–5 sentences): Why do the two runs produce different completion orders? When would you choose one worker over three?

---

## Exercise 4 — Kafka: Consumer Groups and Partitions

### What you will observe

A four-partition topic is consumed by groups of different sizes. You will observe how Kafka assigns partitions to consumers, what happens when there are more consumers than partitions, and how a completely separate consumer group can independently replay the same topic.

### Learning Objectives

1. Understand that a Kafka partition is the unit of parallelism — one partition is assigned to at most one consumer per group at a time.
2. Observe how partition assignment changes as the group size changes.
3. Understand that a consumer beyond the partition count receives no assignment and stays idle.
4. Understand that different consumer groups are fully independent — they each maintain their own offset and do not interfere with each other.
5. Understand that `auto.offset.reset=earliest` applies only when a group has no previously committed offset.

### What you should be able to explain afterwards

- How many partitions each consumer receives for groups of 2, 4, and 5 on a 4-partition topic.
- Why the 5th consumer in a 4-partition group is idle.
- Why a new consumer group (analytics) can read all 40 records even though the first group already processed them.
- The key difference between Kafka's partition-assignment model and RabbitMQ's competing-consumer model.
- What happens during a rebalance when a consumer joins or leaves the group.

### Expected results

| Group size | Partitions per consumer | Records per consumer |
|---|---|---|
| 2 consumers | 2 each | 20 each |
| 4 consumers | 1 each | 10 each |
| 5 consumers | 1 each (4 consumers), 0 (1 consumer) | 10/10/10/10/0 |
| Analytics group (replay) | 2 each | 40 total across group |

### What to submit

- [ ] Evidence logs (or terminal screenshots) showing partition assignment for group sizes **2, 4, and 5**
- [ ] Evidence log from the **analytics group** replay showing all 40 records received
- [ ] Written explanation (3–5 sentences): Why is the 5th consumer idle? Why can the analytics group replay all records that the first group already consumed?

---

## Exercise 5 — Kafka: Keyed Ordering

### What you will observe

You will run two scenarios. In the **keyed** scenario, each order's events are published with the order ID as the message key. Kafka's default partitioner ensures all events for the same order go to the same partition, preserving their sequence.

In the **broken** scenario, the same order's events are deliberately sent to different partitions. Because three consumers process them in parallel with different simulated delays, the events complete out of order.

### Learning Objectives

1. Understand that Kafka's default partitioner routes records with the same key to the same partition, preserving per-key sequence.
2. Observe that per-partition ordering is guaranteed, but there is no ordering guarantee across partitions.
3. Understand that the **producer** is responsible for establishing business sequence — Kafka preserves the order it receives, but does not interpret business meaning.
4. Observe what goes wrong when a producer breaks key affinity.
5. Understand that adding partitions to a topic can remap keys and break existing ordering.

### What you should be able to explain afterwards

- Why all events for `order-123` appear in sequence 1→2→3 in the keyed scenario.
- Why the broken scenario produces `Updated/Cancelled/Created` completion order.
- What `partition=None` means in the publisher and what `partition=index` means.
- How you would design a partitioning strategy for an order processing system that requires per-order sequence.

### Expected results — Keyed mode

| Order | Events | Partition | Completion sequence |
|---|---|---|---|
| order-123 | Created → Updated → Cancelled | Single partition | 1, 2, 3 ✅ |
| order-456 | Created → Updated → Cancelled | Single partition | 1, 2, 3 ✅ |
| order-789 | Created → Updated → Cancelled | Single partition | 1, 2, 3 ✅ |

### Expected results — Broken mode

| Sequence | Event | Partition | Processing delay | Typical finish position |
|---|---|---|---|---|
| 1 | Created | P0 | 5 s | Last ❌ |
| 2 | Updated | P1 | 1 s | First ❌ |
| 3 | Cancelled | P2 | 2 s | Second ❌ |

### What to submit

- [ ] Evidence logs from the **keyed** mode confirming sequence 1→2→3 is preserved for each order
- [ ] Evidence logs from the **broken** mode showing out-of-order completion
- [ ] Written explanation (3–5 sentences): What causes the difference between the two modes? Who is responsible for ensuring business-level ordering — the producer, the broker, or the consumer?

---

## Exercise 6 — Kafka: Crash Before Offset Commit

### What you will observe

This exercise is the Kafka equivalent of Exercise 1. A consumer processes a message and commits the database effect, then crashes **before** committing its Kafka offset. Because the offset was not advanced, the same message is replayed on restart.

You will compare **unsafe** processing (the effect is applied twice) with **safe** processing (idempotent deduplication keeps the effect count at 1).

### Learning Objectives

1. Understand that Kafka's at-least-once guarantee requires a manual offset commit **after** the business effect succeeds.
2. Observe that a crash between a committed business effect and the offset commit causes the consumer to replay the event.
3. Understand the symmetric risk: committing the offset **before** processing could silently skip an event if the consumer then crashes.
4. Apply the same atomic idempotency pattern from Exercise 1 to the Kafka context.
5. Understand what `commit(message=message, asynchronous=False)` does: it commits `offset + 1`, marking the **next** record to fetch.

### What you should be able to explain afterwards

- Why the unsafe consumer's effect count rises from 1 to 2 after a crash and restart.
- Why `enable.auto.commit=False` **and** `enable.auto.offset.store=False` are both needed — setting only one is not enough.
- The difference between synchronous (`asynchronous=False`) and asynchronous offset commits, and when each matters.
- Why the safe consumer's effect count stays at 1 across the crash and restart.
- How this exercise compares to Exercise 1 — same failure mode, different broker mechanism (Kafka offsets vs RabbitMQ ACKs).

### Expected results

| Mode | Run | `applied` | `business_effect_count` | Kafka offset committed? |
|---|---|---|---|---|
| Unsafe | First run (crash) | `True` | `1` | ❌ No |
| Unsafe | Restart | `True` | `2` ← duplicate | ✅ Yes |
| Safe | First run (crash) | `True` | `1` | ❌ No |
| Safe | Restart | `False` | `1` ← deduplicated | ✅ Yes |

### What to submit

- [ ] Terminal output from the **unsafe** mode — crash run and restart, showing `applied` and `business_effect_count`
- [ ] Terminal output from the **safe** mode — crash run and restart, showing `applied` and `business_effect_count`
- [ ] Written explanation (3–5 sentences): Compare the Kafka offset commit mechanism in this exercise with the RabbitMQ ACK mechanism in Exercise 1. What is the same? What is different?

---

## Overall Submission Checklist

Combine all of the above into **one PDF or Markdown file** and submit before the deadline.

- [ ] Exercise 1 — unsafe and safe terminal output + written explanation
- [ ] Exercise 2 — durable and temporary terminal output + written explanation
- [ ] Exercise 3 — 3-worker and 1-worker terminal output + written explanation
- [ ] Exercise 4 — partition assignment logs (groups of 2, 4, 5) + analytics replay log + written explanation
- [ ] Exercise 5 — keyed and broken evidence logs + written explanation
- [ ] Exercise 6 — unsafe and safe terminal output + written explanation
- [ ] Overall Reflection (5–8 sentences): Which failure mode surprised you most, and why? What design principle would you apply in your own system to handle message redelivery safely?

---

## Concepts Summary

The table below shows which core concepts each exercise covers.

| Concept | Ex 1 | Ex 2 | Ex 3 | Ex 4 | Ex 5 | Ex 6 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| At-least-once delivery | ✅ | | | | | ✅ |
| Idempotency / deduplication | ✅ | | | | | ✅ |
| Acknowledgement / offset commit | ✅ | | | | | ✅ |
| Queue durability & binding time | | ✅ | | | | |
| Fanout / pub-sub routing | | ✅ | | | | |
| Work queue / competing consumers | | | ✅ | | | |
| Concurrency & completion order | | | ✅ | | | |
| Consumer groups & partition assignment | | | | ✅ | | |
| Independent group replay | | | | ✅ | | |
| Key-based partitioning & ordering | | | | | ✅ | |
| Cross-partition ordering failure | | | | | ✅ | |
| Producer idempotence | | | | | ✅ | |
| Crash recovery & progress tracking | ✅ | | | | | ✅ |
| RabbitMQ vs Kafka comparison | | | | | | ✅ |
