# [Review Question] API Gateway

| | |
|---|---|
| **วิชา** | 2110521 Software Architecture (2026/1) |
| **ประเภท** | Review Question – 9 ข้อ |
| **ที่มา** | ถอดจาก [api_gateway_quiz_qa.txt](api_gateway_quiz_qa.txt) |
| **Slide ที่เกี่ยวข้อง** | **External API Pattern: API gateway, BFF, gateway implementation** (Richardson ch. 8, Pittipol Kantavat, 67 slides) → [9_External_API_Pattern_3_11_2020](../materials/lecture_notes/external-api-pattern/md/9_External_API_Pattern_3_11_2020-5208-17917891450627.md) |

> ✅ = เฉลย พร้อมเหตุผลสั้น ๆ ใต้แต่ละข้อ

---

## ข้อ 1 – ที่ที่ไม่ควร implement authentication

Which one is NOT the place we implement the authentication function?

- Explicitly implement the edge function services
- API gateway
- At the backend Microservices
- ✅ **Client-side app**

**เหตุผล:** authentication ทำที่ edge / API gateway หรือ backend service เท่านั้น ห้ามไว้ใจฝั่ง client เพราะแก้ไขหรือ bypass ได้

---

## ข้อ 2 – ข้อที่ไม่ใช่ drawback ของ API gateway

Which one is NOT a drawback of using API gateway for external API pattern?

- ✅ **Encapsulation of an internal structure of the application might be violated**
- The client development teams will have additional modules under their control.
- A risk that the API gateway becomes a development bottleneck.
- A highly available component that must be developed, deployed, and managed.

**เหตุผล:** การ "ซ่อน" โครงสร้างภายในของระบบคือ **ประโยชน์หลัก** ของ API gateway ไม่ใช่ข้อเสีย ส่วนอีกสามข้อเป็น drawback จริง (ต้องดูแล HA component, เสี่ยงเป็น bottleneck, ทีม client ต้องดูแล module เพิ่ม)

---

## ข้อ 3 – สิ่งที่ KONG ไม่รองรับ

Which one is NOT supported by KONG API gateway?

- ✅ **API composition**
- Authentication
- Request Logging
- Routing mapping

**เหตุผล:** Kong ทำ routing, authentication และ request logging ผ่าน plugin ได้ แต่ไม่ได้รวม (aggregate) response จากหลาย service ให้เป็นก้อนเดียว ต้องเขียน service แยกเอง

---

## ข้อ 4 – สิ่งที่ไม่ใช่ปัญหาของ client นอก firewall

What one is NOT the problem for the client app outside firewall to connect to microservices?

- Higher Latency
- Lower bandwidth internet
- ✅ **Single API request**
- Unstable API risk

**เหตุผล:** "ยิง request ครั้งเดียว" คือ **เป้าหมาย** ของการใช้ gateway ปัญหาจริงคือ client ต้องยิงหลายรอบผ่าน internet ที่ latency สูง bandwidth ต่ำ และ API ของแต่ละ service เปลี่ยนได้ตลอด

---

## ข้อ 5 – สิ่งที่ไม่ใช่หน้าที่ของ API gateway

Which one is NOT an API gateway responsibility?

- Protocol translation
- Request routing mapping
- ✅ **Message broking**
- API composition

**เหตุผล:** การเป็นตัวกลางส่ง message ระหว่าง service เป็นหน้าที่ของ **message broker** (เช่น Kafka, RabbitMQ) ไม่ใช่ gateway

---

## ข้อ 6 – ownership model ที่ทีม client ดูแล API module ของตัวเอง

Which one relates to the external API ownership model that the client teams own their API module layers and common layers?

- ✅ **Backends for frontends pattern**
- API composition pattern
- Web API pattern
- API gateway pattern

**เหตุผล:** BFF (Backends for Frontends) ให้แต่ละทีม client (mobile, web, 3rd-party) มี gateway / API module ของตัวเอง และแชร์ common layer สำหรับ cross-cutting concern ร่วมกัน

---

## ข้อ 7 – ข้อที่ผิดเรื่อง synchronous vs asynchronous I/O

In designing an API gateway, which option is INCORRECT about using synchronous vs. asynchronous I/O?

- A synchronous I/O API gateway is heavyweight because a number of concurrent threads will be created.
- ✅ **In asynchronous I/O API gateway, the single loop event thread is still blocked until the event handler finishes its job.**
- The drawback of asynchronous I/O is that the callback-based programming model is much more complex.
- Designing and implementing a synchronous I/O is more straightforward than an asynchronous I/O.

**เหตุผล:** event loop เป็น **non-blocking** มันลงทะเบียน callback แล้วไปประมวลผล event อื่นต่อทันที ไม่ได้รอ handler ทำงานเสร็จ

---

## ข้อ 8 – วิธีทำให้ API gateway reliable

Which one effectively helps the API gateway be more reliable?

- Avoid implement edge functions in the gateway
- Most of them do not implement HTTP method-based routing.
- ✅ **Run multiple instance of gateway behind a load balancer**
- Use backends for frontend pattern to separate the gateways

**เหตุผล:** redundancy ให้ high availability ถ้า instance หนึ่งล่ม load balancer จะส่ง traffic ไปตัวอื่นแทน

---

## ข้อ 9 – สิ่งที่ไม่ใช่หน้าที่ของ Edge function

What is NOT a duty of the Edge function?

- Metrics collection
- Rate limiting
- ✅ **Data aggregation**
- Caching

**เหตุผล:** การรวมข้อมูลจากหลาย service คือ **API composition** ส่วน edge function ครอบคลุม authentication, authorization, rate limiting, caching, metrics collection และ request logging

---

## สรุปคำตอบ

| ข้อ | หัวข้อ | เฉลย |
|---|---|---|
| 1 | ที่ที่ไม่ implement authentication | Client-side app |
| 2 | ไม่ใช่ drawback ของ gateway | Encapsulation … might be violated |
| 3 | KONG ไม่รองรับ | API composition |
| 4 | ไม่ใช่ปัญหาของ client นอก firewall | Single API request |
| 5 | ไม่ใช่หน้าที่ gateway | Message broking |
| 6 | ทีม client ดูแล API module เอง | Backends for frontends pattern |
| 7 | ข้อผิดเรื่อง sync/async I/O | event loop ถูก block จน handler เสร็จ |
| 8 | ทำให้ gateway reliable | หลาย instance หลัง load balancer |
| 9 | ไม่ใช่หน้าที่ edge function | Data aggregation |

---

## Cheat sheet สั้น ๆ

**หน้าที่ของ API gateway**
- Request routing mapping, API composition, Protocol translation
- Edge functions: authentication, authorization, rate limiting, caching, metrics collection, request logging
- **ไม่ใช่** หน้าที่: message brokering (ของ message broker), data aggregation = API composition (ไม่ใช่ edge function)

**ประโยชน์ / ข้อเสีย**
- ประโยชน์: ซ่อน internal structure, client ยิง request เดียว, ลดรอบ round trip บน internet ที่ latency สูง/bandwidth ต่ำ
- ข้อเสีย: เป็น HA component ที่ต้อง dev/deploy/manage, เสี่ยงเป็น development bottleneck, ทีม client ต้องดูแล module เพิ่ม

**Design**
- Sync I/O: thread ต่อ request → heavyweight แต่เขียนง่าย
- Async I/O: single event loop non-blocking → เบากว่า แต่ callback model ซับซ้อน
- Reliability: run หลาย instance หลัง load balancer
- Ownership: **BFF** = แต่ละทีม client มี gateway ของตัวเอง + common layer ร่วม

**KONG**
- รองรับ routing, authentication, request logging (plugin) แต่ **ไม่ทำ API composition**
