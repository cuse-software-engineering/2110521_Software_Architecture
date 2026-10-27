# [Review Question] ADR & Domain-Driven Design

| | |
|---|---|
| **วิชา** | 2110521 Software Architecture (2026/1) |
| **ประเภท** | Review Question – 20 ข้อ (18 ปรนัย ข้อละ 1 คะแนน + 2 อัตนัย 0 คะแนน) |
| **ที่มา** | ถอดจาก [adr.txt](adr.txt) (ไม่มีเฉลยทางการ, ข้อ 4 และ 8 มีคำตอบที่เขียนส่งไว้) |
| **Slide ที่เกี่ยวข้อง** | **Architectural Decision Record (ADR)** (Duangdao Wichadakul, 81 slides) → [ADRs_2026](../materials/lecture_notes/adrs/md/ADRs_2026-13578-17883142164608.md) — ข้อ 1–4 |
| | **Domain Driven Design (DDD)** (Duangdao Wichadakul, 91 slides) → [DDD_2026](../materials/lecture_notes/ddd/md/DDD_2026-13578-17883142498154.md) — ข้อ 5–20 |

> ✅ = เฉลยที่วิเคราะห์จาก slide (ไม่ใช่เฉลยทางการ) พร้อมระบุ slide ที่ใช้ตอบ
> ⚠️ = ข้อที่ slide ไม่ได้ตอบตรง ๆ ใช้การตีความ มีหมายเหตุไว้ใต้ข้อ

---

# Part A – ADR (ข้อ 1–4)

## ข้อ 1 – ADR คืออะไร

What is an ADR?

- ✅ **A documentation of architecture decision (AD)**
- A knowledge-based management of architecture decision (AD)
- A log of ADs
- A problem-solving record

**เหตุผล:** ADR = เอกสารที่บันทึก architecture decision (AD) สำคัญ พร้อม context และ consequence ส่วน "log of ADs" คือ **ADL** (Architectural Decision Log) และ "knowledge management" คือ **AKM**
**Slide:** ADR 9–13 (ADR and related terms)

---

## ข้อ 2 – ช่อง Positions ใน template ของ Tyree & Akerman

What is the "positions" in the ADR's template of Tyree and Akerman used for?

- Explain why the decision is made
- Describe locations or positions of servers / deployment environments
- Highlight the posture of software aspects
- ✅ **Record alternatives, other possible approaches/solutions**

**เหตุผล:** Positions = "Other options / alternatives; to avoid question *Did you think about..?*" ส่วน "ทำไมถึงเลือก" คือช่อง **Argument**
**Slide:** ADR 29 (Decision record template by Tyree and Akerman), 35 (ตัวอย่าง Positions/Argument)

---

## ข้อ 3 – ใครเขียน ADR ⚠️

Who writes the ADR?

- System analysts
- Developers / Programmers
- ✅ **Teammates of the project**
- Project manager

**เหตุผล:** best practice คือ "Promote ownership: each project are empowered to create and own ADRs" และขั้นตอนเริ่มใช้ ADR คือ "Talk to team members" ADR จึงเป็นของทีมโปรเจกต์ ไม่ผูกกับตำแหน่งใดตำแหน่งหนึ่ง
**หมายเหตุ:** slide ไม่มีประโยคที่ตอบตรง ๆ ตีความจาก best practice ด้านบน
**Slide:** ADR 14 (ADR best practices), 15 (How to start using ADRs)

---

## ข้อ 4 – ทำไม ADR จึงสำคัญ (อัตนัย)

Why is ADR important?

**คำตอบที่ส่งไว้:**
> สำคัญเพราะช่วยบันทึก "เหตุผล" เบื้องหลังการตัดสินใจด้านสถาปัตยกรรม รวมถึงบริบทและทางเลือกที่เคยพิจารณา ทำให้ทีมเข้าใจว่าทำไมระบบถึงออกแบบมาแบบนี้ สมาชิกใหม่เรียนรู้ได้เร็ว ไม่ต้องถกเถียงเรื่องเดิมซ้ำ

**ประเด็นเพิ่มเติมจาก slide:**
- AD มีผลต่อ structure, non-functional requirements, dependencies, interfaces, construction techniques จึงต้องมีบันทึก (ADR 3–8)
- ADR ที่ดีต้องมี Point in time, Rationality, Immutable record, Specificity → ย้อนดูได้ว่าตัดสินใจเมื่อไหร่ ทำไม และไม่แก้ของเดิม (ADR 26)
- ถ้ากลับคำตัดสินใจให้ mark เป็น superseded ไม่ลบ → เก็บประวัติความคิดไว้ (ADR 64)
- ควรเขียน ADR "almost always" (ADR 67)

---

# Part B – DDD (ข้อ 5–20)

## ข้อ 5 – ให้ XML schema แก่ context อื่น

If a bounded context provided an XML schema of its provided data for other bounded contexts to use, which context map relationship is used?

- Conformist
- Anticorruption Layer
- Open Host Service
- ✅ **Published Language**

**เหตุผล:** Published Language = shared language ที่นิยามได้ด้วย **XML Schema**, JSON Schema, Protobuf, Avro (คำถาม "outsiders ได้รับ shape/vocabulary อะไร") ส่วน Open Host Service คือ "ประตู" (protocol/interface ที่ให้เข้าถึง เช่น REST, gRPC)
**Slide:** DDD 74 (Open Host Service), 75 (Published Language), 76 (OHS vs PL)

---

## ข้อ 6 – ทำงานกับ big ball of mud

When we need to work with a big ball of mud system, which context map's technique that we should use?

- ✅ **Anticorruption Layer**
- Separate Ways
- Conformist
- Customer/Supplier

**เหตุผล:** "Avoid to create big ball of mud, and if need to use it, try ACL" ACL เป็น relationship ที่ defensive ที่สุด แยก downstream model ออกจาก upstream ที่ยุ่งเหยิงและแปลระหว่างกัน
**Slide:** DDD 72–73 (Anticorruption Layer), 79 (Big Ball of Mud)

---

## ข้อ 7 – Event Storming ใช้ทำอะไร ⚠️

What is the Event-Storming used for?

- Map out events within a domain
- Captures concepts and processes for a specific domain
- Model the domain
- ✅ **All are correct**

**เหตุผล:** EventStorming (Alberto Brandolini) เป็น workshop แบบ collective learning ที่ให้ domain expert กับ developer ช่วยกันวาง domain event บน timeline แล้วต่อยอดเป็น command, aggregate, bounded context จึงครอบคลุมทั้ง map events, capture concepts/processes และ model the domain
**หมายเหตุ:** slide กล่าวถึงแค่ชื่อหนังสือ/วิดีโอ (take-home) ไม่ได้อธิบายรายละเอียด
**Slide:** DDD 87–88 (Take Home: Event Storming, Introducing EventStorming)

---

## ข้อ 8 – keyword ของ DDD (อัตนัย)

List at least 5 keywords related to DDD...

**คำตอบที่ส่งไว้:** Ubiquitous Language, Bounded Context, Aggregate, Entity, Value Object, Domain Event, Repository

**keyword อื่นจาก slide:** Model-Driven Design, Layered Architecture, Service (Domain/Application), Factory, Aggregate Root, Invariant, Context Map, Shared Kernel, Customer/Supplier, Conformist, Anticorruption Layer, Open Host Service, Published Language, Separate Ways, Partnership, Big Ball of Mud, Core Domain, Domain Expert, Strategic Design / Tactical Design, Continuous Integration, EventStorming
**Slide:** DDD 19 (Building blocks), 56 (Strategic design map)

---

## ข้อ 9 – Address เป็น value object หรือไม่

The address is considered as value object.

- True
- False
- ✅ **It depends on the context and business model**
- No correct answer

**เหตุผล:** Mail-order company → Address เป็น Value Object (สนใจแค่ค่า street/city/zip), Postal service → Entity (ต้อง track ตัวตนเมื่อ zone เปลี่ยน), Electric utility → Entity หรือย้าย identity ไปที่ Dwelling แล้ว Address กลับเป็น VO คำถามที่ถูกคือ "X ต้องการ tracked identity ใน model นี้หรือไม่"
**Slide:** DDD 24–29 (Is "Address" a Value Object?)

---

## ข้อ 10 – Ubiquitous Language

What is the primary purpose of a "Ubiquitous Language" in Domain-Driven Design?

- To enforce the use of a specific programming language like Java or C#.
- ✅ **To create a shared, unambiguous language used by developers, domain experts, and stakeholders.**
- A formal language used exclusively for database schema definitions.
- A set of terms used only in technical documentation.

**เหตุผล:** หลักการแกนของ DDD คือใช้ภาษาที่อิงจาก model ร่วมกันทั้ง developer และ domain expert หา key concept ของ domain แล้วใช้คำเดียวกันอย่างสม่ำเสมอ
**Slide:** DDD 12–14 (Ubiquitous Language), 15–17 (ตัวอย่าง Flight control, Netflix)

---

## ข้อ 11 – หน้าที่ของ Aggregate Root

In DDD, what is the main responsibility of an "Aggregate Root"?

- To directly save all child objects to the database.
- To create instances of any object in the system.
- To represent the primary business entity in the application without any specific rules.
- ✅ **To enforce invariants (business rules) for all objects within the Aggregate boundary.**

**เหตุผล:** Aggregate มี root เป็น Entity เดียวที่เข้าถึงได้จากภายนอก "the root is responsible for enforcing the aggregate's invariants" ทุกการเปลี่ยนแปลงใน boundary ต้องผ่าน root (เช่น `Car.rotate()` ตรวจ invariant ของ Wheel/Tire)
**Slide:** DDD 32 (Aggregates), 33–38 (ตัวอย่าง Booking, Car, Purchase Order)

---

## ข้อ 12 – Entity vs Value Object

What is the key difference between an Entity and a Value Object?

- Entities are always complex, while Value Objects are always simple.
- Entities are always mapped to database tables, whereas Value Objects are not.
- ✅ **An Entity has a unique identity that persists over time, while a Value Object is defined by its attributes.**
- Entities are mutable, while Value Objects must always be immutable.

**เหตุผล:** Entity มี identity ที่ต้อง track ข้าม state change ส่วน Value Object ไม่มี identity ของตัวเอง สอง VO ที่ attribute เท่ากันถือว่าเท่ากัน (immutability เป็นคุณสมบัติที่ "ควร" มีของ VO แต่ไม่ใช่ความต่างหลัก)
**Slide:** DDD 21 (Entities), 22–23 (Value Objects), 29 (Ask the right question)

---

## ข้อ 13 – Bounded Context

A "Bounded Context" in DDD defines a:

- Security boundary to prevent unauthorized access.
- ✅ **Boundary within which a particular domain model is consistent and well-defined.**
- The user interface layer of an application.
- A boundary defined strictly by a microservice or a database schema.

**เหตุผล:** "Explicitly define the context within which a model applies … keep the model strictly consistent within these bounds" boundary อาจสะท้อนเป็นทีม, code base, database schema ได้ แต่ไม่ได้ถูกนิยามโดยสิ่งเหล่านั้น
**Slide:** DDD 56 (Bounded Context: defines the range of applicability of each model), 62 (To manage a large project), 63 (ตัวอย่าง Booking vs Operations context)

---

## ข้อ 14 – บทบาทของ Repository

What is the designated role of a Repository in DDD?

- To map any domain object to a database table row, similar to a generic DAO.
- To create new instances of Aggregates.
- ✅ **To provide a collection-like interface for accessing and persisting Aggregate Roots.**
- To execute business logic that involves multiple Aggregates.

**เหตุผล:** Repository ให้ client ขอ object "ในภาษาของ model" (`findByConfirmationCode`, `findCustomers(criteria)`) และซ่อน database access technology ไว้ภายใน decouple domain จาก persistence และ swap เป็น in-memory ตอน test ได้ การสร้าง Aggregate เป็นหน้าที่ Factory
**Slide:** DDD 39–44 (Repositories)

---

## ข้อ 15 – Strategic Design

Which of the following is considered part of DDD's "Strategic Design"?

- Designing a Value Object.
- Implementing a Repository for an Aggregate.
- ✅ **Defining Bounded Contexts and their relationships (Context Mapping).**
- Creating an Aggregate with Entities and a Root.

**เหตุผล:** Strategic design = การรักษา model integrity ระดับใหญ่ ได้แก่ Bounded Context, Continuous Integration, Context Map และ relationship ต่าง ๆ ส่วน Entity/VO/Aggregate/Repository/Factory เป็น building blocks ของ Model-Driven Design (tactical)
**Slide:** DDD 19 (Building blocks = tactical), 56 (A set of techniques used to maintain model integrity = strategic), 64–68 (Context Map)

---

## ข้อ 16 – Domain Event

A Domain Event represents:

- A command to be executed in the future.
- A system-level exception or error that has occurred.
- A user interaction, such as a button click in the UI.
- ✅ **Something significant that has already happened in the domain.**

**เหตุผล:** "A domain event is representation of something that happened in the domain … that domain experts care about" ตั้งชื่อเป็นอดีตกาล เช่น OrderPlaced, PaymentReceived
**Slide:** DDD 53 (Domain Events)

---

## ข้อ 17 – เมื่อไหร่ใช้ Anti-Corruption Layer

When is an "Anti-Corruption Layer" (ACL) pattern most useful?

- When two teams are collaborating closely on a new Bounded Context.
- ✅ **When integrating with a legacy or external system whose model is messy or undesirable.**
- When one Bounded Context must conform completely to the model of an upstream context.
- When you need to share a database schema between two services.

**เหตุผล:** ACL แปลและกันไม่ให้ model ที่ไม่ต้องการของ upstream (legacy / big ball of mud) รั่วเข้ามาใน model ของเรา ตัวเลือกอื่นคือ Partnership, Conformist และ Shared Kernel ตามลำดับ
**Slide:** DDD 72–73 (ACL), 79 (Big Ball of Mud)

---

## ข้อ 18 – Application Service

What best describes the role of an Application Service?

- To contain core, reusable business logic that doesn't fit within an Entity or Value Object.
- ✅ **To orchestrate calls to the domain model (Aggregates and Domain Services) to fulfill a use case.**
- To handle infrastructure concerns like sending emails or SMS messages.
- To directly manage database connections and transactions.

**เหตุผล:** ใน Layered Architecture ชั้น **Application** "coordinates tasks and delegates work to collaboration of domain objects in the domain layer" ไม่มี business rule เอง ส่วน business logic ที่ไม่เข้ากับ Entity/VO คือ **Domain Service** และ email/persistence คือชั้น Infrastructure
**Slide:** DDD 20 (Layered Architecture), 45–46 (Services)

---

## ข้อ 19 – Factory

In DDD, what is the primary purpose of a Factory?

- To retrieve existing Aggregates from a database or other persistence mechanism.
- To manage dependency injection for services.
- ✅ **To encapsulate the logic of creating complex objects and Aggregates, ensuring they are in a valid state.**
- To orchestrate business processes that span multiple Bounded Contexts.

**เหตุผล:** "Factories are used to encapsulate the knowledge necessary for object creation … guarantee that an Aggregate is created in a valid, consistent state from the very start" แยก "how to build" ออกจาก "how to use" การดึง Aggregate ที่มีอยู่คือ Repository
**Slide:** DDD 47–51 (Factories)

---

## ข้อ 20 – ลักษณะของ Value Object

A value object in DDD is best characterized by:

- An identifier that distinguishes it from other objects
- Being stored in a separate database table
- Acting as a system-wide configuration entity
- ✅ **Its immutability and equality by values rather than identity**

**เหตุผล:** VO ไม่มี identity สอง VO ที่ค่าเท่ากันถือว่าเหมือนกันและสลับกันได้ และควร immutable (เปลี่ยนค่า = สร้าง instance ใหม่)
**Slide:** DDD 22 (Value Objects), 30 (More examples of Value Objects)

---

## สรุปคำตอบ

| ข้อ | หัวข้อ | เฉลย (วิเคราะห์) | Slide |
|---|---|---|---|
| 1 | ADR คือ | เอกสารบันทึก AD | ADR 9–13 |
| 2 | Positions (Tyree & Akerman) | บันทึกทางเลือกอื่น | ADR 29 |
| 3 | ใครเขียน ADR | Teammates of the project ⚠️ | ADR 14–15 |
| 4 | ทำไม ADR สำคัญ | อัตนัย (เหตุผล/บริบท/ทางเลือก, onboarding, ไม่ถกซ้ำ) | ADR 3–8, 26, 64 |
| 5 | ให้ XML schema | Published Language | DDD 75–76 |
| 6 | big ball of mud | Anticorruption Layer | DDD 72, 79 |
| 7 | Event Storming | All are correct ⚠️ | DDD 87–88 |
| 8 | keyword DDD | อัตนัย | DDD 19, 56 |
| 9 | Address เป็น VO? | ขึ้นกับ context | DDD 24–29 |
| 10 | Ubiquitous Language | ภาษากลางที่ไม่กำกวมของ dev + domain expert | DDD 12–14 |
| 11 | Aggregate Root | บังคับ invariant ใน boundary | DDD 32–38 |
| 12 | Entity vs VO | identity vs attributes | DDD 21–23, 29 |
| 13 | Bounded Context | boundary ที่ model consistent | DDD 56, 62–63 |
| 14 | Repository | collection-like interface ของ Aggregate Root | DDD 39–44 |
| 15 | Strategic Design | Bounded Context + Context Mapping | DDD 56, 64–68 |
| 16 | Domain Event | สิ่งสำคัญที่เกิดขึ้นแล้วใน domain | DDD 53 |
| 17 | เมื่อไหร่ใช้ ACL | integrate กับ legacy/external ที่ model ยุ่ง | DDD 72–73, 79 |
| 18 | Application Service | orchestrate domain model ตาม use case | DDD 20, 45 |
| 19 | Factory | ห่อ logic การสร้าง Aggregate ให้ valid | DDD 47–51 |
| 20 | Value Object | immutable + equality by value | DDD 22, 30 |

---

## Cheat sheet สั้น ๆ

**ADR (ADR 9–13, 26, 29–31, 61–64)**
- ADR = เอกสารบันทึก AD + context + consequence / ADL = log รวม ADR ของโปรเจกต์ / ASR = requirement ที่มีผลวัดได้ต่อ architecture / AKM = ทั้งหมดรวมกัน
- ADR ที่ดี: Point in time, Rationality, Immutable record, Specificity
- Tyree & Akerman 14 หัวข้อ: Summary (Issue, Decision, Status, Group) / Details (Assumptions, Constraints, **Positions** = ทางเลือก, **Argument** = ทำไมเลือก, Implications) / Related (decisions, requirements, artifacts, principles) / Notes
- Nygard: Title, Context, Decision, Status, Consequences เก็บใน `doc/arch/adr-NNN.md` เลขไม่ใช้ซ้ำ ถ้ากลับคำให้ mark superseded
- Alexandrian: "In the context of … facing … we decided for … to achieve … accepting …"

**DDD tactical – building blocks (DDD 19–53)**
- Layered: UI / Application (coordinate) / Domain (heart) / Infrastructure
- Entity = identity ที่ track ได้ / Value Object = เท่ากันด้วยค่า immutable (default เป็น VO ก่อน) / Address ขึ้นกับ context
- Aggregate = cluster ที่เปลี่ยนเป็นหน่วยเดียว root เป็น Entity เดียวที่เข้าถึงได้ บังคับ invariant
- Repository = ขอ/เก็บ Aggregate ในภาษา model ซ่อน DB / Factory = สร้าง Aggregate ให้ valid / Service = behavior ที่ไม่ใช่ของ Entity ใด stateless
- Domain Event = สิ่งที่เกิดขึ้นแล้วที่ domain expert สนใจ (OrderPlaced)

**DDD strategic – model integrity (DDD 56–80)**
- Bounded Context → Ubiquitous Language, Continuous Integration, Context Map
- Context Map: Shared Kernel, Customer/Supplier, Conformist, **ACL** (defensive ที่สุด ใช้กับ legacy/big ball of mud), **Open Host Service** (ประตู: REST/gRPC) → **Published Language** (คำศัพท์: XML/JSON Schema, Protobuf), Separate Ways, Partnership
- integrate ระหว่าง context: RPC (SOAP/WSDL), RESTful, Messaging (Domain Event)
