# [Review Question] Interprocess Communication & RabbitMQ

| | |
|---|---|
| **วิชา** | 2110521 Software Architecture (2026/1) |
| **ประเภท** | Review Question – 14 ข้อ (13 ปรนัย + 1 อัตนัย) ข้อละ 1 คะแนน |
| **ที่มา** | ถอดจาก [intercomm.txt](intercomm.txt) (ไม่มีเฉลยทางการ) |
| **Slide ที่เกี่ยวข้อง** | **Interprocess Communication: RPI, service discovery and messaging** (Richardson ch. 3, 77 slides) → [Interprocess_Communication_ธีมเดิม_ล่าสุด](../materials/lecture_notes/interprocess-communication/md/Interprocess_Communication_ธีมเดิม_ล่าสุด-13578-17913032229622.md) |
| | **Messaging with RabbitMQ (hands-on)** (Duangdao Wichadakul, 28 slides) → [RabbitMQ_Practice_2026_1](../materials/lecture_notes/rabbitmq-practice/md/RabbitMQ_Practice_2026_1-13578-17913034815264.md) |

> ✅ = เฉลยที่วิเคราะห์จาก slide (ไม่ใช่เฉลยทางการ) พร้อมระบุ slide ที่ใช้ตอบ
> ⚠️ = ข้อที่ตัวเลือกกำกวม มีหมายเหตุไว้ใต้ข้อ

---

## ข้อ 1 – สิ่งที่ไม่เกี่ยวกับ REST

Which one does not relate to REST?

- The most popular REST IDL is the Open API Specification.
- Often in the form of an XML document or JSON object
- Uses the HTTP verbs (method) for manipulating resources.
- ✅ **Binary messages in the Protocol Buffers format using HTTP/2**

**เหตุผล:** binary message แบบ Protocol Buffers บน HTTP/2 คือ **gRPC** ส่วน REST ใช้ HTTP verb กับ resource, representation เป็น JSON/XML และ IDL ยอดนิยมคือ OpenAPI (เดิมคือ Swagger)
**Slide:** IPC 18 (Using REST), 19 (Specifying REST APIs), 21 (gRPC)

---

## ข้อ 2 – สิ่งที่ไม่ใช่ลักษณะของ invocation-based IPC

Which one is not a characteristic of the invocation-based IPC mechanism?

- Clients may block waiting for a response.
- ✅ **A client may send requests to many services in a command.**
- The client assumes that the response will arrive in a timely fashion.
- A client sends a request and service sends back a response.

**เหตุผล:** Remote Procedure Invocation (RPI) เป็น **one-to-one request/response** client ส่ง request ไปหา service เดียวแล้วรอ reply (block หรือ reactive ก็ได้) และคาดว่า reply จะมาเร็ว การส่งไปหลาย service ในคำสั่งเดียวเป็นลักษณะของ one-to-many (publish/subscribe)
**Slide:** IPC 7 (Interaction styles), 13 (Remote procedure invocation)

---

## ข้อ 3 – สิ่งที่ผิดเกี่ยวกับ Circuit breaker

Which one is incorrect about the Circuit breaker pattern?

- Relating to design your services to prevent partial failures.
- ✅ **Included in the five groups of communication patterns under Discovery topic.**
- We need to decide how your services should recover from an unresponsive remote service.
- Developing Robust RPI Proxies are needed.

**เหตุผล:** ใน pattern map ของ Richardson Circuit breaker อยู่กลุ่ม **Reliability** ไม่ใช่ Discovery (Discovery มี client-side/server-side discovery, self/3rd-party registration, service registry) ส่วนการป้องกัน partial failure แบ่งเป็น 2 ส่วน คือ (1) robust RPI proxies: timeout, limit requests, circuit breaker และ (2) ตัดสินใจว่าจะ recover จาก service ที่ไม่ตอบอย่างไร
**Slide:** IPC 14 (Patterns map), 28 (Patterns map: reliability), 29 (Preventing partial failure), 30 (Robust RPI proxies)

---

## ข้อ 4 – สิ่งที่ไม่ใช่ประโยชน์ของ gRPC

Which one is not a benefit of using gRPC?

- Appropriate for an API with a rich set of update operations.
- ✅ **Takes less work for JavaScript clients comparison to REST/JSON-based APIs**
- Bidirectional streaming enables both RPI and messaging styles of communication.
- Enables interoperability between clients and services written in a wide range of languages.

**เหตุผล:** "More work for JavaScript clients" เป็น **drawback** ของ gRPC (browser ต้องใช้ gRPC-Web/Connect) ส่วน benefit คือ rich update operations, compact message, bidirectional streaming และรองรับหลายภาษา
**Slide:** IPC 23 (gRPC: trade-offs)

---

## ข้อ 5 – Queue สำหรับ kitchen ที่ทำอาหารเฉพาะประเภท

If we would like our kitchen microservices to cook for specific food types, which kind of queue that we can use in RabbitMQ?

- Queue with exchange type is direct with the use of wildcard keys
- Queue with exchange type is headers with the use of wildcard keys
- ✅ **Queue with exchange type is direct with the use of routing keys**
- Queue with exchange type is fanout

**เหตุผล:** pattern **Routing** ใช้ exchange type `direct` แล้ว bind queue ด้วย binding key ให้ตรงกับ routing key (เช่น `thai`, `japanese`) message จะถูกส่งเฉพาะ queue ที่ key ตรง wildcard (`*`, `#`) ใช้ได้กับ `topic` เท่านั้น ส่วน fanout จะ broadcast ไปทุก queue
**Slide:** RabbitMQ 4 (Overview of the tutorial patterns), 22–24 ((4) Routing)

---

## ข้อ 6 – สิ่งที่ไม่ใช่ asynchronous interaction style

Which one in these following options is not asynchronous interaction style?

- ✅ **Request/response**
- Publish/subscribe
- One-way notifications
- Publish/async responses

**เหตุผล:** ตาราง interaction style: **Synchronous** = Request/response ส่วน **Asynchronous** = Asynchronous request/response, One-way notifications (one-to-one) และ Publish/subscribe, Publish/async responses (one-to-many)
**Slide:** IPC 7 (Interaction styles), 8–9 (Asynchronous interactions)

---

## ข้อ 7 – worker ทุกตัวสนใจสิ่งเดียวกัน ⚠️

If all workers are interested in the same thing, which kind of queue that we SHOULD use?

- Queue with exchange type is topic
- Worker queue
- ✅ **Queue with exchange type is fanout**
- Queue with exchange type is direct

**เหตุผล:** ถ้าทุก consumer ต้องการ **รับ message เดียวกันทั้งหมด** ต้องใช้ Publish/Subscribe ด้วย exchange type `fanout` ซึ่ง broadcast ไปทุก queue ที่ bind ไว้ ส่วน Worker queue (competing consumer) จะกระจาย message ให้ worker ตัวใดตัวหนึ่งเท่านั้น
**หมายเหตุ:** ถ้าตีความว่า "สนใจงานประเภทเดียวกัน แต่แบ่งกันทำ" คำตอบจะเป็น Worker queue แต่คำว่า "interested in the same thing" ตรงกับคำอธิบาย fanout ใน tutorial มากกว่า
**Slide:** RabbitMQ 4, 12–16 ((2) Work queue), 19–21 ((3) Publish/Subscribe fanout)

---

## ข้อ 8 – สิ่งที่ไม่ใช่ synchronous communication

Which one in these following options is not synchronous communication mechanisms?

- ✅ **AMQP**
- HTTP
- gRPC
- REST

**เหตุผล:** Synchronous = request/response ผ่าน REST หรือ gRPC บน HTTP ส่วน Asynchronous = messaging ผ่าน **AMQP** หรือ STOMP
**Slide:** IPC 5 (Many IPC technologies)

---

## ข้อ 9 – ทำไมต้องมี fair dispatch

Why fair-dispatching is introduced in RabbitMQ?

- ✅ **Different consumers may work on different speed.**
- Producer may produce too much messages
- We need work queue that works as round-robin
- Several producers may compete to produce the messages

**เหตุผล:** การ dispatch แบบ round-robin (default) จะส่ง message ลำดับที่ n ให้ consumer ตัวที่ n เสมอโดยไม่สนว่าตัวนั้นยังทำงานค้างอยู่หรือไม่ ถ้า consumer เร็ว/ช้าไม่เท่ากัน ตัวช้าจะกองงาน fair dispatch (`basic_qos(prefetch_count=1)`) จำกัดให้ consumer มี message ที่ยังไม่ ack ได้ทีละ 1 ตัว broker จึงส่งงานใหม่ให้เฉพาะตัวที่ว่าง
**Slide:** RabbitMQ 16 (Work queue: Fair dispatch)

---

## ข้อ 10 – issue ที่ไม่จำเป็นสำหรับ Asynchronous messaging

Which issue in the following options is not necessary for an Asynchronous messaging pattern?

- Which type will be used between a point-to-point channel or a publish-subscribe channel?
- ✅ **How to design the Circuit breaker pattern when a service is not respond?**
- Which is better between Brokerless vs broker-based architectures?
- What kinds of messages will be used?

**เหตุผล:** Circuit breaker เป็น reliability pattern ของ **synchronous call** (RPI) ส่วน asynchronous messaging ต้องตัดสินใจเรื่องชนิด message (document/command/event), ชนิด channel (point-to-point/publish-subscribe) และสถาปัตยกรรม (brokerless/broker-based)
**Slide:** IPC 28 (Circuit breaker = reliability for synchronous calls), 44, 46 (Messages and channels), 48 (Two kinds of channels), 51 (Brokerless vs broker-based)

---

## ข้อ 11 – สิ่งที่ไม่ใช่ลักษณะของ Brokerless ⚠️

What is not a characteristic of Brokerless architecture in an Asynchronous messaging pattern?

- ✅ **Higher network traffic and latency comparison to Broker-based architecture.**
- Services must use one of the discovery mechanisms.
- Availability is reduced comparison to Broker-based architecture.
- Higher operational complexity comparison to Broker-based architecture.

**เหตุผล:** Brokerless มี benefit คือ **traffic น้อยกว่าและ latency ต่ำกว่า** (ส่งตรงไม่ผ่านคนกลาง) และไม่มี broker เป็น bottleneck/SPOF ส่วน drawback คือต้องมี service discovery และทั้งสองฝั่งต้องออนไลน์พร้อมกัน (availability ลดลง)
**หมายเหตุ:** ตัวเลือก "Higher operational complexity" ก็ขัดกับหนังสือ Richardson (brokerless มี operational complexity **ต่ำกว่า** เพราะไม่ต้องดูแล broker) แต่ slide ไม่ได้พูดถึงประเด็นนี้ตรง ๆ จึงเลือกข้อ traffic/latency ที่ขัดกับ slide ชัดเจนที่สุด
**Slide:** IPC 52 (Brokerless messaging: trade-offs), 54 (Broker-based: trade-offs)

---

## ข้อ 12 – เลือก RabbitMQ แทน Kafka (อัตนัย)

Which kind of applications that you may decide to use RabbitMQ over Kafka and WHY? Please give an application as the example.

**แนวคำตอบ:**

เลือก RabbitMQ เมื่อ application เป็น **task queue / งานที่ต้องการ routing ซับซ้อน** ปริมาณ message ไม่สูงมาก ต้องการ latency ต่ำ ack เป็นราย message และลบ message ทิ้งหลังประมวลผลเสร็จ ไม่ต้องการ replay

ตัวอย่าง: **ระบบสั่งอาหาร (FTGO) ส่ง order ไปให้ kitchen service** ที่แต่ละครัวรับเฉพาะอาหารประเภทของตัวเอง ใช้ direct/topic exchange route ตาม routing key ให้ worker หลายตัวแบ่งงานกัน (competing consumers) แต่ละ order ต้องถูกทำครั้งเดียวแล้ว ack ทิ้ง ไม่ต้องเก็บ log ไว้อ่านซ้ำ ตัวอย่างอื่น เช่น email/notification queue, image-resize job queue

ตรงข้ามกับ Kafka ที่เหมาะกับ event streaming ปริมาณสูงมาก, event sourcing, หลาย consumer อ่านข้อมูลชุดเดียวกัน และต้องการ replay

**Slide:** IPC 67 (RabbitMQ vs Kafka key differences), 68 (When to use RabbitMQ vs Kafka)

---

## ข้อ 13 – คำสั่ง docker run

From this command,

```sh
docker run -d --name some-rabbit -p 5672:5672 -p 8080:15672 rabbitmq:3
```

Which choice is INCORRECT?

- ✅ **The container name is rabbitmq:3**
- 8080 is public port to access the rabbitmq management
- We start RabbitMQ with its default ports
- We are starting RabbitMQ as a detached mode

**เหตุผล:** `--name some-rabbit` คือชื่อ container ส่วน `rabbitmq:3` คือ **image**:tag ที่เหลือถูก: `-d` = detached, `5672` = AMQP port default, `15672` = management UI (map ออกเป็น 8080)
**Slide:** RabbitMQ 5 (Pre-requisite: docker run), 6 (management UI ที่ localhost:8080)

---

## ข้อ 14 – สิ่งที่ผิดเกี่ยวกับ RabbitMQ

What is INCORRECT about RabbitMQ?

- RabbitMQ queue types enable the flexibility of message handling
- RabbitMQ is a message broker
- RabbitMQ's based protocol is AMQP
- ✅ **RabbitMQ supports the replay messages**

**เหตุผล:** RabbitMQ ลบ message หลัง consume และ **replay ไม่ได้โดย default** (ต้องใช้ Streams ที่เพิ่มมาใน 3.9) replay เป็นจุดเด่นของ Kafka ส่วน RabbitMQ เป็น message broker บน AMQP (รองรับ STOMP, MQTT ด้วย) และมี queue type หลายแบบ (classic, quorum, stream)
**Slide:** IPC 63 (RabbitMQ), 66 (queue types), 67 (RabbitMQ vs Kafka); RabbitMQ 2 (AMQP, MQTT)

---

## สรุปคำตอบ

| ข้อ | หัวข้อ | เฉลย (วิเคราะห์) | Slide |
|---|---|---|---|
| 1 | ไม่เกี่ยวกับ REST | Binary messages in Protocol Buffers over HTTP/2 | IPC 18–21 |
| 2 | ไม่ใช่ลักษณะ RPI | client ส่งไปหลาย service ในคำสั่งเดียว | IPC 7, 13 |
| 3 | ผิดเรื่อง Circuit breaker | อยู่กลุ่ม Discovery (จริงคือ Reliability) | IPC 14, 28–30 |
| 4 | ไม่ใช่ benefit ของ gRPC | JS client ทำงานน้อยกว่า REST | IPC 23 |
| 5 | kitchen เฉพาะประเภทอาหาร | direct exchange + routing keys | RabbitMQ 4, 22–24 |
| 6 | ไม่ใช่ async style | Request/response | IPC 7–9 |
| 7 | ทุก worker สนใจสิ่งเดียวกัน | fanout ⚠️ | RabbitMQ 19–21 |
| 8 | ไม่ใช่ sync mechanism | AMQP | IPC 5 |
| 9 | ทำไมต้องมี fair dispatch | consumer เร็วช้าไม่เท่ากัน | RabbitMQ 16 |
| 10 | issue ที่ไม่จำเป็นสำหรับ async | ออกแบบ Circuit breaker | IPC 28, 46–51 |
| 11 | ไม่ใช่ลักษณะ Brokerless | traffic/latency สูงกว่า ⚠️ | IPC 52, 54 |
| 12 | RabbitMQ แทน Kafka | task queue / complex routing เช่น kitchen order | IPC 67–68 |
| 13 | docker run ผิด | ชื่อ container คือ rabbitmq:3 | RabbitMQ 5–6 |
| 14 | ผิดเรื่อง RabbitMQ | รองรับ replay | IPC 63–67 |

---

## Cheat sheet สั้น ๆ

**Interaction styles (IPC 5–9)**
- Sync = Request/response (REST, gRPC บน HTTP) / Async = messaging (AMQP, STOMP)
- One-to-one: Request/response, Async request/response, One-way notification
- One-to-many: Publish/subscribe, Publish/async responses
- Text format: JSON, XML / Binary: Protocol Buffers, Avro / IDL: OpenAPI (REST), Protobuf (gRPC), AsyncAPI (messaging)

**RPI, REST, gRPC (IPC 13–23)**
- RPI = request/response, client อาจ block หรือ reactive, คาดว่า reply มาเร็ว
- REST benefit: simple, ทดสอบง่าย, firewall friendly, ไม่ต้องมี broker / drawback: request/response เท่านั้น, ทั้งสองฝั่งต้อง running, client ต้องหา instance, หลาย resource = หลาย call
- gRPC benefit: rich update ops, compact, bidirectional streaming, หลายภาษา / drawback: JS client ยุ่งยาก, firewall เก่า block HTTP/2

**Pattern map ของ Richardson (IPC 14)**
- Communication style: Messaging, RPI, Domain-specific
- Reliability: **Circuit breaker**
- Discovery: Client-side discovery, Self registration, Service registry, Server-side discovery, 3rd-party registration
- Transactional messaging: Polling publisher, Transaction log tailing, Transactional outbox
- External API: API gateway, BFF

**Partial failure (IPC 27–30)**
- Part 1 robust RPI proxy: timeout, limit outstanding requests, circuit breaker (trip เมื่อ error rate เกิน threshold → fail fast)
- Part 2 ตัดสินใจวิธี recover จาก service ที่ไม่ตอบ

**Messaging (IPC 44–58)**
- Message: document / command / event; Channel: point-to-point / publish-subscribe
- Brokerless: traffic น้อย latency ต่ำ ไม่มี SPOF / ต้องมี discovery ทั้งสองฝั่งต้องพร้อม
- Broker-based: loose coupling ไม่ต้อง discovery, buffering, หลาย interaction style / อาจเป็น bottleneck, SPOF, operations เพิ่ม
- Sharded channel รักษาลำดับ; dedupe ด้วยตาราง processed message id

**RabbitMQ vs Kafka (IPC 63–68)**
- RabbitMQ: broker push, AMQP, Producer → Exchange → Queue → Consumer, ลบหลัง consume, replay ไม่ได้ default, routing ยืดหยุ่น, เหมาะ task queue
- Kafka: distributed log pull, retain ตามเวลา, replay ได้, partition รักษาลำดับ, at-least-once, throughput สูงมาก, เหมาะ event streaming

**RabbitMQ hands-on (RabbitMQ 4–27)**
- (1) Hello world (2) Work queue = competing consumers, `durable=True`, `basic_ack`, fair dispatch `prefetch_count=1` (3) Pub/Sub = `fanout` (4) Routing = `direct` binding key == routing key (5) Topics = `topic`, `*` หนึ่งคำ `#` ศูนย์คำขึ้นไป (6) RPC = `reply_to` + `correlation_id` (7) Publisher confirms
- docker: `-d` detached, `--name` ชื่อ container, 5672 AMQP, 15672 management (guest/guest)
