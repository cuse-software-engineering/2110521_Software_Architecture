# Quiz – 2110521 Software Architecture (2026/1)

Review question ของแต่ละหัวข้อ ถอดเป็น markdown พร้อมเฉลยที่วิเคราะห์จาก slide และระบุเลข slide ที่ใช้ตอบ
ใช้เป็นสารตั้งต้นสำหรับ generate mock exam

## Index: quiz ↔ slide

| Quiz | จำนวนข้อ | Slide (ชื่อ deck ใน `materials/lecture_notes/`) | ผู้สอน | เฉลยทางการ |
|---|---|---|---|---|
| [rest_grpc_quiz.md](rest_grpc_quiz.md) | 11 | **REST API** → `rest/` REST_2023 (54 slides) / **gRPC** → `grpc/` gRPC_2026 (73 slides) | Nuengwong Tuaycharoen | ไม่มี (เห็นตัวเลือกที่กดส่ง) |
| [api_gateway_quiz.md](api_gateway_quiz.md) | 9 | **External API Pattern: API gateway, BFF** → `external-api-pattern/` 9_External_API_Pattern_3_11_2020 (67 slides) | Pittipol Kantavat | มีในไฟล์ txt |
| [intercomm_quiz.md](intercomm_quiz.md) | 14 | **Interprocess Communication: RPI, service discovery, messaging** → `interprocess-communication/` Interprocess_Communication_ธีมเดิม_ล่าสุด (77 slides) / **Messaging with RabbitMQ (hands-on)** → `rabbitmq-practice/` RabbitMQ_Practice_2026_1 (28 slides) | Wiwat Vatanawood, Duangdao Wichadakul, Nuengwong Tuaycharoen, Pittipol Kantavat | ไม่มี |
| [adr_ddd_quiz.md](adr_ddd_quiz.md) | 20 | **Architectural Decision Record (ADR)** → `adrs/` ADRs_2026 (81 slides) / **Domain Driven Design (DDD)** → `ddd/` DDD_2026 (91 slides) | Duangdao Wichadakul | ไม่มี |

Deck ที่ยังไม่มี quiz: `intro-swarch/` (Introduction to Software Architecture), `microservice-patterns/` (Intro to Microservice Patterns)

## ไฟล์ดิบ

| ไฟล์ | เนื้อหา |
|---|---|
| [rest_grpc/](rest_grpc/) | ภาพถ่าย 6 รูป (IMG_3950–3955) + รูปตัด `q1_postman_xss.png`, `q8_rest_grpc_diagram.png` |
| [api_gateway_quiz_qa.txt](api_gateway_quiz_qa.txt) | Q&A API gateway พร้อมเฉลย |
| [intercomm.txt](intercomm.txt) | คำถาม IPC/RabbitMQ (copy จากหน้าเว็บ ไม่มีเฉลย) |
| [adr.txt](adr.txt) | คำถาม ADR/DDD (copy จากหน้าเว็บ ไม่มีเฉลย ยกเว้นข้ออัตนัยที่เขียนส่ง) |

## รูปแบบของแต่ละไฟล์

1. ตารางหัว: วิชา, ประเภท, ที่มา, slide ที่เกี่ยวข้อง (ลิงก์ไป md transcription)
2. รายข้อ: โจทย์ ตัวเลือก (✅ เฉลย) เหตุผล และ `Slide:` เลขหน้าที่ใช้ตอบ
3. ตารางสรุปคำตอบ
4. Cheat sheet ของหัวข้อนั้น

สัญลักษณ์: ✅ เฉลยที่วิเคราะห์ / 🔘 ตัวเลือกที่กดส่งจริง (เฉพาะ rest_grpc) / ⚠️ ข้อที่กำกวมหรือ slide ไม่ได้ตอบตรง ๆ

## แนวทางใช้ gen mock exam

- สุ่มข้อจาก quiz เดิมแล้วแปลงเป็นข้อใหม่ที่ถามแนวคิดเดียวกัน (เช่น เปลี่ยน "ข้อใด**ไม่ใช่**" เป็น "ข้อใด**ใช่**")
- ใช้ cheat sheet ท้ายไฟล์เป็น concept list แล้วออกข้อที่ยังไม่เคยถาม
- ข้อที่ติด ⚠️ ควรถามให้ชัดกว่าต้นฉบับ
- ใช้ `Slide:` เพื่อดึงเนื้อหาจาก transcription มาออกข้อเพิ่ม โดยเฉพาะ deck ที่ยังไม่มี quiz
