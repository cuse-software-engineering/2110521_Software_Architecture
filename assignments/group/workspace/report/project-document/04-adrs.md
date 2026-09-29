# 4 Architecture Decision Records (ADRs)

The ADRs follow the course template (Michael Nygard's format: Title, Context, Decision, Status, Consequences). An accepted ADR is not rewritten when its decision changes: a new ADR supersedes it, and the old record keeps its text with a status that names its successor. Corrections to how a record is written, such as the teacher's comment on ADR-06 (FB-D1-01), are made in place and listed in the Change Log.

*Table 4.1 Architecture decision records*

| ADR | Title | Status |
|---|---|---|
| ADR-01 | Frontend Architecture & Client Channel | Accepted |
| ADR-02 | Real-Time Floor Plan Communication | Superseded by ADR-08 and ADR-09 |
| ADR-03 | Backend Language & Framework | Accepted; Socket.io deferred by ADR-09 |
| ADR-04 | Notification Engine | Superseded by ADR-10 |
| ADR-05 | Interactive Floor Plan Rendering | Accepted |
| ADR-06 | Primary Database Engine | Accepted (revised after FB-D1-01) |
| ADR-07 | Internal Role Authentication (Front Staff, Manager) | Accepted |
| ADR-08 | Table Hold and Concurrency Control | Accepted |
| ADR-09 | Table Status Updates in the MVP: Polling | Accepted |
| ADR-10 | Customer Notifications through the LINE Messaging API Only | Accepted |
| ADR-11 | Simulated Payment Gateway for the MVP | Accepted |

## 4.1 ADR-01: Frontend Architecture & Client Channel

**Context**
Target users primarily interact via mobile phones while coordinating nightlife plans on LINE. Requiring an App Store/Play Store download would cause high user drop-off. The client must support mobile responsiveness and rich interactive graphics for table selection.

**Decision**
Use Next.js (React) bundled as a LINE Front-end Framework (LIFF) Web App, with fallback access via standard mobile browsers.

**Status**
Accepted

**Consequences**
- Eliminates app install friction; customers book directly inside the LINE app.
- Allows seamless integration with LINE Login and LINE Messaging API.
- Requires compliance with LIFF webview constraints and in-app browser caching behaviors.

## 4.2 ADR-02: Real-Time Floor Plan Communication

**Context**
When multiple customers look at the floor plan simultaneously on busy nights, table statuses must update instantaneously to prevent double-booking conflicts and outdated views.

**Decision**
Implement WebSocket (or Server-Sent Events - SSE) for real-time table status broadcasting, combined with short-term Redis distributed locks for table selection checkout.

**Status**
Superseded by ADR-08 (table hold) and ADR-09 (table status updates) on 2026-09-29.

**Consequences**
- Delivers sub-second UI updates when tables are locked, booked, or released.
- Avoids wasteful client polling against the backend server.
- Requires maintaining persistent connection pools and managing socket disconnect/reconnect states on mobile networks.

## 4.3 ADR-03: Backend Language & Framework

**Context**
The system requires rapid development cycles while supporting RESTful APIs, real-time bi-directional communication for floor plan updates, seamless integration with the LINE Messaging API/LIFF SDK, and scheduled background tasks to automatically release expired table reservations past the cutoff window. Options considered include Go, Java, and Node.js (JavaScript). Given that the frontend is built using Next.js/React, adopting a unified language stack across client and server significantly streamlines development.

**Decision**
Use Node.js (JavaScript) with the Express.js framework for the core API services, combined with Socket.io for real-time WebSocket communication and node-cron for background cutoff scheduling.

**Status**
Accepted. Amended on 2026-09-29: the Socket.io part is deferred to Increment 2 by ADR-09, and node-cron runs the scheduled jobs of ADR-08 (hold expiry) instead of cutoff scheduling.

**Consequences**
- Enables a unified full-stack JavaScript environment, allowing the team to share utility logic, minimize context switching, and accelerate feature delivery.
- Leverages Node.js's event-driven, non-blocking I/O model to handle concurrent client connections efficiently during peak reservation hours.
- Because JavaScript is dynamically typed, the backend requires robust runtime request validation and clear documentation to prevent data type mismatches.

## 4.4 ADR-04: Notification Engine

**Context**
Reminders before cutoff times are critical to reducing lost tables. Traditional SMS is costly per transaction, whereas email is rarely checked by nightlife patrons in real time.

**Decision**
Use LINE Messaging API (Push Messages / Flex Messages) as the primary notification channel, supplemented by Web Push notifications.

**Status**
Superseded by ADR-10 on 2026-09-29.

**Consequences**
1. Near 100% open rate with interactive rich cards ("On My Way" / "Postpone 30 mins").
2. Low messaging cost within standard official account quotas.
3. Requires users to add or link the venue's LINE Official Account (OA).

## 4.5 ADR-05: Interactive Floor Plan Rendering

**Context**
The floor plan needs to support responsive rendering, pinch-to-zoom, zone highlighting, and seat view popups without lagging on mid-range smartphones.

**Decision**
Use HTML5 Canvas / SVG (via Fabric.js or Konva.js) embedded within the Next.js client.

**Status**
Accepted

**Consequences**
- Smooth vector scaling and interactive zone/table hit-testing.
- Managers can visually manipulate coordinates for tables and stages.
- Requires custom responsive coordinate mapping to ensure layouts adapt across various mobile screen sizes.

## 4.6 ADR-06: Primary Database Engine

**Context**
The system needs to store diverse data structures, including flexible venue floor plan layouts (coordinates, shapes, multi-table zone configs, the image of the venue), booking transaction records, customer profiles, and time-stamped status transitions. Traditional relational databases (RDBMS) enforce rigid table schemas that make storing deeply nested floor layout geometries and dynamic table attributes cumbersome. A zone map is naturally one nested document (zones that contain tables with their coordinates, types and capacities) whose shape differs from venue to venue, so the layouts need a flexible schema that stores such a document whole, without complex multi-table joins. Additionally, the backend runtime is Node.js/JavaScript, making native JSON/BSON document handling particularly advantageous for rapid development.

**Decision**
Use MongoDB as the primary NoSQL document database, accessed via the Mongoose Object Data Modeling (ODM) library in the Node.js backend.

**Status**
Accepted. Revised on 2026-09-29 after the teacher's feedback (FB-D1-01): the need for a flexible schema moved from Consequences to Context.

**Consequences**
- **Seamless Node.js Integration:** Documents map directly to JavaScript objects (JSON) reducing serialization overhead and development friction.
- **Atomic Single-Document Updates:** A table's status can be changed with one conditional update, which gives the first-lock-wins hold of ADR-08 without a separate lock server.
- **Horizontal Scalability:** Supports horizontal partitioning (sharding) should the platform expand to serve multiple nightlife venues concurrently.
- **Validation Moves into the Application:** The flexible schema does not check the documents, so every service validates what it stores with Mongoose schemas.
- **Multi-Document Changes Need Care:** A change that spans several documents, such as a booking and its payment, needs a multi-document transaction, which MongoDB supports only on a replica set, or separate steps that can be retried safely.

## 4.7 ADR-07: Internal Role Authentication (Front Staff, Manager)

**Context**
Customers reach the web app through LINE and are authenticated with LINE Login, as decided in ADR-01. Front Staff and Managers use internal accounts created by the venue, and front-of-house staff work from shared devices. Binding those accounts to personal LINE profiles would tie venue access to individual social accounts and make shift handover and staff turnover difficult. Options considered: LINE Login for every role, venue-issued username and password accounts, and an external identity provider.

**Decision**
Use venue-issued username and password accounts with JWT sessions for all internal roles (Front Staff, Manager, and the Owner with read-only access, FR-65), kept separate from the customer LINE Login flow. Each account carries a role that determines which back-office functions it may use (e.g. check-in for Front Staff; zone map and round creation for the Manager). The Manager creates, updates, and deactivates internal accounts from the venue configuration.

**Status**
Accepted

**Consequences**
- Venue access stays under the owner's control and survives staff turnover, because accounts are not tied to personal LINE profiles.
- Requires the system to implement password storage, session expiry, and account lockout instead of delegating all authentication to LINE.
- Two authentication paths must be maintained and tested, one for customers and one for internal roles.

## 4.8 ADR-08: Table Hold and Concurrency Control

**Context**
Selecting a table gives the Customer a hold of 15 minutes (BRULE-02, FR-07). When several customers select the same table, exactly one hold may succeed (first lock wins, BRULE-03, FR-08); NFR-20 tests this with at least 50 simultaneous attempts. An unpaid hold must be released within 10 seconds of its end, with a timer accuracy of ±5 seconds, and the Customer informed (FR-23, NFR-21). Version 1.1 named three different mechanisms for this: short-term Redis distributed locks (ADR-02), MongoDB TTL indexes (ADR-06) and a node-cron job (ADR-03). Options considered: a Redis lock with an expiry time, a MongoDB TTL index on hold documents, and a conditional update of the table's status with a scheduled release job.

**Decision**
The Table Availability Service owns the status of every table of every round in its own database. holdTable() is one conditional update that changes a table from available to held only if it is still available, and stores the booking and the end of the hold; exactly one of several concurrent requests succeeds. The Booking Service owns the hold timer of the booking: a scheduled job (node-cron, ADR-03) runs every 5 seconds, calls expireUnpaidBookings(), sets every overdue Held booking to Expired, calls releaseHold() of the Table Availability Service and asks the Notification Service to send the hold-expired notice. No Redis server and no TTL index are used.

**Status**
Accepted on 2026-09-29. Supersedes the locking part of ADR-02 and the TTL consequence of ADR-06.

**Consequences**
- One atomic operation in one database gives first lock wins, and it can be load-tested directly (NFR-20).
- A 5-second job meets the 10-second release requirement. A MongoDB TTL index would not: its background task runs only every 60 seconds, and it deletes the document instead of releasing the table and informing the Customer.
- No extra infrastructure is needed, which helps keep the operating cost within the limit of NFR-32.
- The two services must agree after a crash between the booking update and the table release: the job retries releaseHold() for Expired bookings whose table is still held, so releaseHold() must be idempotent.

## 4.9 ADR-09: Table Status Updates in the MVP: Polling

**Context**
A table status change must appear on every open map within 2 seconds (FR-06, NFR-25), with up to 200 customers browsing at once and rounds of up to 60 tables (NFR-27). ADR-02 chose WebSocket or Server-Sent Events, and the 2110628 design constraint CON-04 also prefers pushed updates. The teacher's feedback on Deliverable #2 (FB-D2-01) recommends leaving real-time WebSocket out of the MVP and adding it later.

**Decision**
In the MVP the Customer Web App and the Back-office Web App poll getRoundTableStatus() of the Table Availability Service through the API Gateway every 2 seconds while a zone map is open; the response carries a version number of the round's table status, so an unchanged map costs one small response. In Increment 2 the Table Availability Service pushes status changes to the open maps by WebSocket (Socket.io, ADR-03), and polling stays as the fallback after a lost connection.

**Status**
Accepted on 2026-09-29. Supersedes the real-time part of ADR-02.

**Consequences**
- A change reaches every open map within 2 seconds plus one response time, as FR-06 requires, and the MVP has no persistent connections to manage.
- 200 customers polling every 2 seconds make about 100 small requests per second at booking open; the answer is one status document per round, which the Table Availability Service can cache.
- Between two polls a customer can still select a table that has just been taken; the conditional update of ADR-08 refuses the hold and UC-01 AF-3 refreshes the map.
- Requests are wasted when nothing changes, which is the cost ADR-02 wanted to avoid; Increment 2 removes most of it.

## 4.10 ADR-10: Customer Notifications through the LINE Messaging API Only

**Context**
ADR-04 chose LINE Messaging API push messages supplemented by Web Push, mainly for reminders before cutoff times with "On My Way" and "Postpone 30 mins" buttons. The requirements now use the check-in window and the grace period as the arrival rule; reminders and the grace extension are planned for Release 2.0 of the 2110628 requirements (FR-45, FR-46, FR-55) and are out of scope (Section 3.1.7). The customer web app runs inside LINE's in-app browser (LIFF), which does not support the Push API that Web Push needs, and the system is LINE-only (CON-02). The messages in scope are the booking confirmation with the e-ticket, the hold-expired notice and, from Increment 2, the refund and slip-decision notices (FR-20, FR-21), each retried 3 times within 5 minutes (FR-22) and sent within the Official Account's monthly push quota.

**Decision**
Send every customer notification as a LINE Messaging API push message (a Flex Message for the e-ticket) from the Notification Service through the LINE Messaging Adapter. No Web Push, SMS or e-mail.

**Status**
Accepted on 2026-09-29. Supersedes ADR-04.

**Consequences**
- One channel that every customer already has, since the LINE account is the customer's identity (BRULE-12).
- The Customer must be a friend of the venue's LINE Official Account, as the precondition of UC-01 already requires.
- Push messages count against the monthly quota; the MVP sends only transactional messages.
- When LINE is unavailable the confirmation is delayed, but the e-ticket stays available under My Bookings (FR-22).

## 4.11 ADR-11: Simulated Payment Gateway for the MVP

**Context**
UC-01 pays the full table fee through a payment gateway (BRULE-01, FR-13, FR-16). The 2110628 Payment Gateway Feasibility Study chose Beam Checkout, with Opn Payments as the fallback, and requires one payment-service interface so that the gateway can be replaced (NFR-37) and a sandbox for testing (NFR-31). Onboarding with a real gateway needs a registered merchant. The teacher's feedback on Deliverable #2 (FB-D2-01) recommends a simulated payment in the MVP, and automatic refunds, transfer-slip review and the degraded payment mode later.

**Decision**
The Payment Service reaches a gateway only through the Payment Gateway Adapter, the port of Section 5 (createCheckoutSession(), verifyWebhookSignature(), queryPaymentStatus(), refundPayment()). In the MVP the adapter is backed by a simulated gateway: a small checkout page, opened inside the web app like a hosted checkout, where the tester chooses to pay or to decline, after which it sends a signed webhook to the API Gateway as a real gateway would. In Increment 2 a Beam Checkout adapter replaces it, first against Beam's sandbox, together with status polling, automatic refund of a late payment and the degraded mode.

**Status**
Accepted on 2026-09-29.

**Consequences**
- The MVP demonstrates the whole booking flow, including a declined payment and the signed webhook, without a merchant account or real money.
- The Payment Service and the Booking Service do not change when the real gateway arrives; only the adapter does (NFR-37).
- The simulated gateway must never run in production; only the test configuration enables it (NFR-31).
- What only a real gateway shows (late or missing results, refunds, outages) is not exercised until Increment 2.
