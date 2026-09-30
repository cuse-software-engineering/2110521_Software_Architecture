# 4 Architecture Decision Records (ADRs)

The ADRs follow the course template (Michael Nygard's format: Title, Context, Decision, Status, Consequences); each ADR is a table of these five fields and starts on a new page. An accepted ADR is not rewritten when its decision changes: a new ADR supersedes it, and the old record keeps its text with a status that names its successor. Corrections to how a record is written, such as the teacher's comment on ADR-06 (FB-D1-01), are made in place and listed in the change-log document. The Part column names the part of the system that each decision concerns: the Frontend, the Backend or the External systems (Section 5.2).

*Table 4.1 Architecture decision records*

| ADR | Title | Part of the system | Status |
|---|---|---|---|
| ADR-01 | Frontend Architecture & Client Channel | Frontend | Accepted |
| ADR-02 | Real-Time Floor Plan Communication | Frontend, Backend | Superseded by ADR-08 and ADR-09 |
| ADR-03 | Backend Language & Framework | Backend | Accepted; Socket.io deferred by ADR-09 |
| ADR-04 | Notification Engine | Backend, External systems | Superseded by ADR-10 |
| ADR-05 | Interactive Floor Plan Rendering | Frontend | Accepted |
| ADR-06 | Primary Database Engine | Backend | Accepted (revised after FB-D1-01) |
| ADR-07 | Internal Role Authentication (**Front Staff**, **Manager**) | Frontend, Backend | Accepted |
| ADR-08 | Table Hold and Concurrency Control | Backend | Accepted; the lock moved to the Booking Service by ADR-13 |
| ADR-09 | Table Status Updates in the MVP: Polling | Frontend, Backend | Accepted |
| ADR-10 | **Customer** Notifications through the LINE Messaging API Only | Backend, External systems | Accepted |
| ADR-11 | Simulated **Payment Gateway** for the MVP | Backend, External systems | Accepted |
| ADR-12 | Communication: REST at the API Gateway, gRPC inside the Backend | All three parts | Accepted |
| ADR-13 | The Booking Owns the Hold; the Table Map Is a Read Model | Backend | Accepted |

## 4.1 ADR-01: Frontend Architecture & Client Channel

*Table 4.2 ADR-01 Frontend Architecture & Client Channel*

<table class="adr" markdown="1">
<tr markdown="1">
<td class="k">Title</td>
<td markdown="block">

Frontend Architecture & Client Channel

</td>
</tr>
<tr markdown="1">
<td class="k">Context</td>
<td markdown="block">

Target users primarily interact via mobile phones while coordinating nightlife plans on LINE. Requiring an App Store/Play Store download would cause high user drop-off. The client must support mobile responsiveness and rich interactive graphics for table selection.

</td>
</tr>
<tr markdown="1">
<td class="k">Decision</td>
<td markdown="block">

Use Next.js (React) bundled as a LINE Front-end Framework (LIFF) Web App, with fallback access via standard mobile browsers.

</td>
</tr>
<tr markdown="1">
<td class="k">Status</td>
<td markdown="block">

Accepted

</td>
</tr>
<tr markdown="1">
<td class="k">Consequences</td>
<td markdown="block">

- Eliminates app install friction; customers book directly inside the LINE app.
- Allows seamless integration with LINE Login and LINE Messaging API.
- Requires compliance with LIFF webview constraints and in-app browser caching behaviors.

</td>
</tr>
</table>

## 4.2 ADR-02: Real-Time Floor Plan Communication

*Table 4.3 ADR-02 Real-Time Floor Plan Communication*

<table class="adr" markdown="1">
<tr markdown="1">
<td class="k">Title</td>
<td markdown="block">

Real-Time Floor Plan Communication

</td>
</tr>
<tr markdown="1">
<td class="k">Context</td>
<td markdown="block">

When multiple customers look at the **zone map** simultaneously on busy nights, table statuses must update instantaneously to prevent double-booking conflicts and outdated views.

</td>
</tr>
<tr markdown="1">
<td class="k">Decision</td>
<td markdown="block">

Implement WebSocket (or Server-Sent Events - SSE) for real-time table status broadcasting, combined with short-term Redis distributed locks for table selection checkout.

</td>
</tr>
<tr markdown="1">
<td class="k">Status</td>
<td markdown="block">

Superseded by ADR-08 (table hold) and ADR-09 (table status updates) on 2026-09-29.

</td>
</tr>
<tr markdown="1">
<td class="k">Consequences</td>
<td markdown="block">

- Delivers sub-second UI updates when tables are locked, booked, or released.
- Avoids wasteful client polling against the backend server.
- Requires maintaining persistent connection pools and managing socket disconnect/reconnect states on mobile networks.

</td>
</tr>
</table>

## 4.3 ADR-03: Backend Language & Framework

*Table 4.4 ADR-03 Backend Language & Framework*

<table class="adr" markdown="1">
<tr markdown="1">
<td class="k">Title</td>
<td markdown="block">

Backend Language & Framework

</td>
</tr>
<tr markdown="1">
<td class="k">Context</td>
<td markdown="block">

The system requires rapid development cycles while supporting RESTful APIs, real-time bi-directional communication for **zone map** updates, seamless integration with the LINE Messaging API/LIFF SDK, and scheduled background tasks to automatically release expired table reservations past the cutoff window. Options considered include Go, Java, and Node.js (JavaScript). Given that the frontend is built using Next.js/React, adopting a unified language stack across client and server significantly streamlines development.

</td>
</tr>
<tr markdown="1">
<td class="k">Decision</td>
<td markdown="block">

Use Node.js (JavaScript) with the Express.js framework for the core API services, combined with Socket.io for real-time WebSocket communication and node-cron for background cutoff scheduling.

</td>
</tr>
<tr markdown="1">
<td class="k">Status</td>
<td markdown="block">

Accepted. Amended on 2026-09-29: the Socket.io part is deferred to Increment 2 by ADR-09, and node-cron runs the scheduled jobs of ADR-08 (hold expiry) instead of cutoff scheduling.

</td>
</tr>
<tr markdown="1">
<td class="k">Consequences</td>
<td markdown="block">

- Enables a unified full-stack JavaScript environment, allowing the team to share utility logic, minimize context switching, and accelerate feature delivery.
- Leverages Node.js's event-driven, non-blocking I/O model to handle concurrent client connections efficiently during peak reservation hours.
- Because JavaScript is dynamically typed, the backend requires robust runtime request validation and clear documentation to prevent data type mismatches.

</td>
</tr>
</table>

## 4.4 ADR-04: Notification Engine

*Table 4.5 ADR-04 Notification Engine*

<table class="adr" markdown="1">
<tr markdown="1">
<td class="k">Title</td>
<td markdown="block">

Notification Engine

</td>
</tr>
<tr markdown="1">
<td class="k">Context</td>
<td markdown="block">

Reminders before cutoff times are critical to reducing lost tables. Traditional SMS is costly per transaction, whereas email is rarely checked by nightlife patrons in real time.

</td>
</tr>
<tr markdown="1">
<td class="k">Decision</td>
<td markdown="block">

Use LINE Messaging API (Push Messages / Flex Messages) as the primary notification channel, supplemented by Web Push notifications.

</td>
</tr>
<tr markdown="1">
<td class="k">Status</td>
<td markdown="block">

Superseded by ADR-10 on 2026-09-29.

</td>
</tr>
<tr markdown="1">
<td class="k">Consequences</td>
<td markdown="block">

1. Near 100% open rate with interactive rich cards ("On My Way" / "Postpone 30 mins").
2. Low messaging cost within standard official account quotas.
3. Requires users to add or link the venue's **LINE Official Account** (OA).

</td>
</tr>
</table>

## 4.5 ADR-05: Interactive Floor Plan Rendering

*Table 4.6 ADR-05 Interactive Floor Plan Rendering*

<table class="adr" markdown="1">
<tr markdown="1">
<td class="k">Title</td>
<td markdown="block">

Interactive Floor Plan Rendering

</td>
</tr>
<tr markdown="1">
<td class="k">Context</td>
<td markdown="block">

The **zone map** needs to support responsive rendering, pinch-to-zoom, **zone** highlighting, and seat view popups without lagging on mid-range smartphones.

</td>
</tr>
<tr markdown="1">
<td class="k">Decision</td>
<td markdown="block">

Use HTML5 Canvas / SVG (via Fabric.js or Konva.js) embedded within the Next.js client.

</td>
</tr>
<tr markdown="1">
<td class="k">Status</td>
<td markdown="block">

Accepted

</td>
</tr>
<tr markdown="1">
<td class="k">Consequences</td>
<td markdown="block">

- Smooth vector scaling and interactive **zone**/table hit-testing.
- **Managers** can visually manipulate coordinates for tables and stages.
- Requires custom responsive coordinate mapping to ensure the **zone map** adapts across various mobile screen sizes.

</td>
</tr>
</table>

## 4.6 ADR-06: Primary Database Engine

*Table 4.7 ADR-06 Primary Database Engine*

<table class="adr" markdown="1">
<tr markdown="1">
<td class="k">Title</td>
<td markdown="block">

Primary Database Engine

</td>
</tr>
<tr markdown="1">
<td class="k">Context</td>
<td markdown="block">

The system needs to store diverse data structures, including flexible venue **zone maps** (coordinates, shapes, multi-table **zone** configs, the image of the venue), booking transaction records, **customer profiles**, and time-stamped status transitions. Traditional relational databases (RDBMS) enforce rigid table schemas that make storing deeply nested **zone map** geometries and dynamic table attributes cumbersome. A **zone map** is naturally one nested document (**zones** that contain tables with their coordinates, types and capacities) whose shape differs from venue to venue, so the **zone maps** need a flexible schema that stores such a document whole, without complex multi-table joins. Additionally, the backend runtime is Node.js/JavaScript, making native JSON/BSON document handling particularly advantageous for rapid development.

</td>
</tr>
<tr markdown="1">
<td class="k">Decision</td>
<td markdown="block">

Use MongoDB as the primary NoSQL document database, accessed via the Mongoose Object Data Modeling (ODM) library in the Node.js backend.

</td>
</tr>
<tr markdown="1">
<td class="k">Status</td>
<td markdown="block">

Accepted. Revised on 2026-09-29 after the teacher's feedback (FB-D1-01): the need for a flexible schema moved from Consequences to Context.

</td>
</tr>
<tr markdown="1">
<td class="k">Consequences</td>
<td markdown="block">

- **Seamless Node.js Integration:** Documents map directly to JavaScript objects (JSON) reducing serialization overhead and development friction.
- **Atomic Single-Document Updates:** A table's status can be changed with one conditional update, which gives the first-lock-wins hold of ADR-08 without a separate lock server.
- **Horizontal Scalability:** Supports horizontal partitioning (sharding) should the platform expand to serve multiple nightlife venues concurrently.
- **Validation Moves into the Application:** The flexible schema does not check the documents, so every service validates what it stores with Mongoose schemas.
- **Multi-Document Changes Need Care:** A change that spans several documents, such as a booking and its payment, needs a multi-document transaction, which MongoDB supports only on a replica set, or separate steps that can be retried safely.

</td>
</tr>
</table>

## 4.7 ADR-07: Internal Role Authentication (Front Staff, Manager)

*Table 4.8 ADR-07 Internal Role Authentication (Front Staff, Manager)*

<table class="adr" markdown="1">
<tr markdown="1">
<td class="k">Title</td>
<td markdown="block">

Internal Role Authentication (**Front Staff**, **Manager**)

</td>
</tr>
<tr markdown="1">
<td class="k">Context</td>
<td markdown="block">

**Customers** reach the web app through LINE and are authenticated with LINE Login, as decided in ADR-01. **Front Staff** and **Managers** use internal accounts created by the venue, and front-of-house staff work from shared devices. Binding those accounts to personal LINE profiles would tie venue access to individual social accounts and make shift handover and staff turnover difficult. Options considered: LINE Login for every role, venue-issued username and password accounts, and an external identity provider.

</td>
</tr>
<tr markdown="1">
<td class="k">Decision</td>
<td markdown="block">

Use venue-issued username and password accounts with JWT sessions for all internal roles (**Front Staff**, **Manager**, and the **Owner** with read-only access, FR-65), kept separate from the customer LINE Login flow. Each account carries a role that determines which **back-office** functions it may use (e.g. check-in for **Front Staff**; **zone map** and round creation for the **Manager**). The **Manager** creates, updates, and deactivates internal accounts from the venue configuration.

</td>
</tr>
<tr markdown="1">
<td class="k">Status</td>
<td markdown="block">

Accepted

</td>
</tr>
<tr markdown="1">
<td class="k">Consequences</td>
<td markdown="block">

- Venue access stays under the owner's control and survives staff turnover, because accounts are not tied to personal LINE profiles.
- Requires the system to implement password storage, session expiry, and account lockout instead of delegating all authentication to LINE.
- Two authentication paths must be maintained and tested, one for customers and one for internal roles.

</td>
</tr>
</table>

## 4.8 ADR-08: Table Hold and Concurrency Control

*Table 4.9 ADR-08 Table Hold and Concurrency Control*

<table class="adr" markdown="1">
<tr markdown="1">
<td class="k">Title</td>
<td markdown="block">

Table Hold and Concurrency Control

</td>
</tr>
<tr markdown="1">
<td class="k">Context</td>
<td markdown="block">

Selecting a table gives the **Customer** a **hold** of 15 minutes (BRULE-02, FR-07). When several customers select the same table, exactly one hold may succeed (**first lock wins**, BRULE-03, FR-08); NFR-20 tests this with at least 50 simultaneous attempts. An unpaid hold must be released within 10 seconds of its end, with a timer accuracy of ±5 seconds, and the **Customer** informed (FR-23, NFR-21). Version 1.1 named three different mechanisms for this: short-term Redis distributed locks (ADR-02), MongoDB TTL indexes (ADR-06) and a node-cron job (ADR-03). Options considered: a Redis lock with an expiry time, a MongoDB TTL index on hold documents, and a conditional update of the table's status with a scheduled release job.

</td>
</tr>
<tr markdown="1">
<td class="k">Decision</td>
<td markdown="block">

The Table Availability Service owns the status of every table of every round in its own database. holdTable() is one conditional update that changes a table from available to held only if it is still available, and stores the booking and the end of the **hold**; exactly one of several concurrent requests succeeds. The Booking Service owns the **hold** timer of the booking: a scheduled job (node-cron, ADR-03) runs every 5 seconds, calls expireUnpaidBookings(), sets every overdue Held booking to Expired, calls releaseHold() of the Table Availability Service and asks the Notification Service to send the hold-expired notice. No Redis server and no TTL index are used.

</td>
</tr>
<tr markdown="1">
<td class="k">Status</td>
<td markdown="block">

Accepted on 2026-09-29. Supersedes the locking part of ADR-02 and the TTL consequence of ADR-06. Superseded in part on 2026-09-30 by ADR-13: the Booking Service owns the hold and the Table Availability Service keeps the read model; the timer job of this record stays.

</td>
</tr>
<tr markdown="1">
<td class="k">Consequences</td>
<td markdown="block">

- One atomic operation in one database gives **first lock wins**, and it can be load-tested directly (NFR-20).
- A 5-second job meets the 10-second release requirement. A MongoDB TTL index would not: its background task runs only every 60 seconds, and it deletes the document instead of releasing the table and informing the **Customer**.
- No extra infrastructure is needed, which helps keep the operating cost within the limit of NFR-32.
- The two services must agree after a crash between the booking update and the table release: the job retries releaseHold() for Expired bookings whose table is still held, so releaseHold() must be idempotent.

</td>
</tr>
</table>

## 4.9 ADR-09: Table Status Updates in the MVP: Polling

*Table 4.10 ADR-09 Table Status Updates in the MVP: Polling*

<table class="adr" markdown="1">
<tr markdown="1">
<td class="k">Title</td>
<td markdown="block">

Table Status Updates in the MVP: Polling

</td>
</tr>
<tr markdown="1">
<td class="k">Context</td>
<td markdown="block">

A table status change must appear on every open map within 2 seconds (FR-06, NFR-25), with up to 200 customers browsing at once and rounds of up to 60 tables (NFR-27). ADR-02 chose WebSocket or Server-Sent Events, and the design constraints of the system also prefer pushed map updates to polling. The teacher's feedback on Deliverable #2 (FB-D2-01) recommends leaving real-time WebSocket out of the MVP and adding it later.

</td>
</tr>
<tr markdown="1">
<td class="k">Decision</td>
<td markdown="block">

In the MVP the Customer Web App and the Back-office Web App poll getRoundTableStatus() of the Table Availability Service through the API Gateway every 2 seconds while a **zone map** is open; the response carries a version number of the round's table status, so an unchanged map costs one small response. In Increment 2 the Table Availability Service pushes status changes to the open maps by WebSocket (Socket.io, ADR-03), and polling stays as the fallback after a lost connection.

</td>
</tr>
<tr markdown="1">
<td class="k">Status</td>
<td markdown="block">

Accepted on 2026-09-29. Supersedes the real-time part of ADR-02.

</td>
</tr>
<tr markdown="1">
<td class="k">Consequences</td>
<td markdown="block">

- A change reaches every open map within 2 seconds plus one response time, as FR-06 requires, and the MVP has no persistent connections to manage.
- 200 customers polling every 2 seconds make about 100 small requests per second at booking open; the answer is one status document per round, which the Table Availability Service can cache.
- Between two polls a customer can still select a table that has just been taken; the conditional update of ADR-08 refuses the **hold** and UC-01 AF-3 refreshes the map.
- Requests are wasted when nothing changes, which is the cost ADR-02 wanted to avoid; Increment 2 removes most of it.

</td>
</tr>
</table>

## 4.10 ADR-10: Customer Notifications through the LINE Messaging API Only

*Table 4.11 ADR-10 Customer Notifications through the LINE Messaging API Only*

<table class="adr" markdown="1">
<tr markdown="1">
<td class="k">Title</td>
<td markdown="block">

**Customer** Notifications through the LINE Messaging API Only

</td>
</tr>
<tr markdown="1">
<td class="k">Context</td>
<td markdown="block">

ADR-04 chose LINE Messaging API push messages supplemented by Web Push, mainly for reminders before cutoff times with "On My Way" and "Postpone 30 mins" buttons. The requirements now use the **check-in window** and the **grace period** as the arrival rule; reminders and the grace extension are planned for a later release and are out of scope (Section 3.1.7). The customer web app runs inside LINE's in-app browser (LIFF), which does not support the Push API that Web Push needs, and the system is LINE-only. The messages in scope are the booking confirmation with the **e-ticket**, the hold-expired and payment-failed notices and, from Increment 2, the refund and slip-decision notices (FR-20, FR-21), each retried 3 times within 5 minutes (FR-22) and sent within the Official Account's monthly push quota.

</td>
</tr>
<tr markdown="1">
<td class="k">Decision</td>
<td markdown="block">

Send every customer notification as a LINE Messaging API push message (a Flex Message for the **e-ticket**) from the Notification Service through the LINE Messaging Adapter. No Web Push, SMS or e-mail.

</td>
</tr>
<tr markdown="1">
<td class="k">Status</td>
<td markdown="block">

Accepted on 2026-09-29. Supersedes ADR-04.

</td>
</tr>
<tr markdown="1">
<td class="k">Consequences</td>
<td markdown="block">

- One channel that every customer already has, since the LINE account is the customer's identity (BRULE-12).
- The **Customer** must be a friend of the venue's **LINE Official Account**, as the precondition of UC-01 already requires.
- Push messages count against the monthly quota; the MVP sends only transactional messages.
- When LINE is unavailable the confirmation is delayed, but the **e-ticket** stays available under My Bookings (FR-22).

</td>
</tr>
</table>

## 4.11 ADR-11: Simulated Payment Gateway for the MVP

*Table 4.12 ADR-11 Simulated Payment Gateway for the MVP*

<table class="adr" markdown="1">
<tr markdown="1">
<td class="k">Title</td>
<td markdown="block">

Simulated **Payment Gateway** for the MVP

</td>
</tr>
<tr markdown="1">
<td class="k">Context</td>
<td markdown="block">

UC-01 pays the **full table fee** through a payment gateway (BRULE-01, FR-13, FR-16). A payment gateway feasibility study selected Beam Checkout, with Opn Payments as the fallback; the requirements ask for one payment-service interface so that the gateway can be replaced (NFR-37) and a sandbox for testing (NFR-31). Onboarding with a real gateway needs a registered merchant. The teacher's feedback on Deliverable #2 (FB-D2-01) recommends a simulated payment in the MVP, and automatic refunds, transfer-slip review and the degraded payment mode later.

</td>
</tr>
<tr markdown="1">
<td class="k">Decision</td>
<td markdown="block">

The Payment Service reaches a gateway only through the Payment Gateway Adapter, the port of Section 5 (createCheckoutSession(), verifyWebhookSignature(), queryPaymentStatus(), refundPayment()). In the MVP the adapter is backed by a simulated gateway: a small checkout page, opened inside the web app like a hosted checkout, where the tester chooses to pay or to decline, after which it sends a signed webhook to the API Gateway as a real gateway would. In Increment 2 a Beam Checkout adapter replaces it, first against Beam's sandbox, together with status polling, automatic refund of a late payment and the **degraded mode**.

</td>
</tr>
<tr markdown="1">
<td class="k">Status</td>
<td markdown="block">

Accepted on 2026-09-29.

</td>
</tr>
<tr markdown="1">
<td class="k">Consequences</td>
<td markdown="block">

- The MVP demonstrates the whole booking flow, including a declined payment and the signed webhook, without a merchant account or real money.
- The Payment Service and the Booking Service do not change when the real gateway arrives; only the adapter does (NFR-37).
- The simulated gateway must never run in production; only the test configuration enables it (NFR-31).
- What only a real gateway shows (late or missing results, refunds, outages) is not exercised until Increment 2.

</td>
</tr>
</table>

## 4.12 ADR-12: Communication: REST at the API Gateway, gRPC inside the Backend

*Table 4.13 ADR-12 Communication: REST at the API Gateway, gRPC inside the Backend*

<table class="adr" markdown="1">
<tr markdown="1">
<td class="k">Title</td>
<td markdown="block">

Communication: REST at the API Gateway, gRPC inside the Backend

</td>
</tr>
<tr markdown="1">
<td class="k">Context</td>
<td markdown="block">

SEATS has three parts (Section 5.2): the Frontend in the users' browsers, the Backend on the servers of SEATS, and the External systems. Version 1 of the architecture (Deliverable #2) used REST for every call, as the Deliverable #2 brief allowed for a first version; the brief asks the later versions to choose REST, gRPC or asynchronous messaging for each part according to its work, and the minimum requirements of the course project include at least one REST service and one gRPC service. Three kinds of call cross or stay inside the parts:

- The web apps run in LINE's in-app browser (LIFF, ADR-01) and in ordinary browsers, which speak HTTP and JSON; the **Payment Gateway** reports payment results by an HTTPS webhook.
- Inside the Backend the services call each other on the busiest paths: holding a table calls the Concert Round Service and the Table Availability Service within one customer request, which must answer within 2 seconds at the 95th percentile (NFR-04) at 5 hold requests per second (NFR-01).
- The backend is written in JavaScript (ADR-03), which is dynamically typed, so nothing checks that a caller and a service agree on the shape of their messages.

Options considered: REST everywhere; gRPC everywhere, with gRPC-Web for the browsers; REST into the API Gateway and through it to the services, with gRPC only between the services; REST at the API Gateway only, which translates each call into gRPC; asynchronous messages through a message broker.

</td>
</tr>
<tr markdown="1">
<td class="k">Decision</td>
<td markdown="block">

- **Frontend to Backend:** REST, JSON over HTTPS, only through the API Gateway, which authenticates each request and routes it to the service that owns the operation.
- **External systems to Backend:** the payment webhook is a REST call over HTTPS to the API Gateway, which passes it to the Payment Service.
- **API Gateway to services:** gRPC. The API Gateway is the only component that speaks REST: it maps each of its routes to one gRPC method of the service that owns the operation, turns the path, the query and the JSON body into the request message, the response message into JSON and the gRPC status into the HTTP status (Section 6.7). It holds no business logic.
- **Service to service:** gRPC, Protocol Buffers over HTTP/2, with @grpc/grpc-js. Every service has exactly one API, described by one .proto file, from which the API Gateway and the other services generate their clients; every collaboration between services in Table 5.3 is a gRPC call. Every call carries a deadline, and only calls that are safe to repeat, such as releaseHold() (ADR-08), are retried.
- **Backend to External systems:** through the adapters, over the provider's HTTPS API.
- **No message broker in the MVP:** every call is synchronous.

</td>
</tr>
<tr markdown="1">
<td class="k">Status</td>
<td markdown="block">

Accepted on 2026-09-30.

</td>
</tr>
<tr markdown="1">
<td class="k">Consequences</td>
<td markdown="block">

- The browsers, the LIFF app and the payment webhook use plain HTTPS and JSON, so no gRPC-Web proxy is needed.
- Each service has one API and one contract, its .proto file, which generates the client and server code and catches the type mismatches that ADR-03 warns about when a service changes its messages, in the API Gateway as in every other caller.
- The calls between services use a compact binary encoding over long-lived HTTP/2 connections, which keeps the internal calls of a **hold** small within the 2-second budget of NFR-04.
- The API Gateway is the REST service of the system: it offers the create, read, update and delete of **zone maps** and **concert rounds** over REST, served by the Concert Round Service over gRPC, and every service is a gRPC service, so the design contains the REST service and the gRPC service that the course project requires.
- The API Gateway grows by one route per operation: the route table and the mapping of gRPC statuses to HTTP statuses live in one place, and the polled read of the table map (ADR-09) answers 304 at the gateway, which compares the version of the read model with the If-None-Match header of the request. The team has to learn gRPC and Protocol Buffers.
- gRPC messages are binary and harder to inspect than JSON; debugging needs tools such as grpcurl and server reflection.
- Every call is synchronous: when a service is down, the calls to it fail and so does the request that made them. Calls that can be delayed without harm, such as the LINE messages, are the first candidates for asynchronous messaging when a later ADR revisits it.
- The services find each other by service names that the deployment resolves; how services are discovered is left to a later ADR.

</td>
</tr>
</table>

## 4.13 ADR-13: The Booking Owns the Hold; the Table Map Is a Read Model

*Table 4.14 ADR-13 The Booking Owns the Hold; the Table Map Is a Read Model*

<table class="adr" markdown="1">
<tr markdown="1">
<td class="k">Title</td>
<td markdown="block">

The Booking Owns the **Hold**; the Table Map Is a Read Model

</td>
</tr>
<tr markdown="1">
<td class="k">Context</td>
<td markdown="block">

ADR-08 put the lock in the Table Availability Service: holdTable() is a conditional update of the table's status, and the Booking Service writes its own Held record afterwards. One business fact, a table taken by a customer, is therefore written twice, in two databases, and kept consistent by retries and an idempotent releaseHold(). The domain model (Section 6.1) shows that the booking history already contains every fact the table map shows: a table is unavailable exactly when an active booking, Held, Confirmed or Checked-in, exists for it in that round. An audit trail of booking state changes is wanted for disputes at the door, and the minimum requirements of the course project include a service fed through a message broker. Options considered: keep the lock in the Table Availability Service (ADR-08); make the booking the single truth with a uniqueness rule and derive the table map as a read model, fed synchronously now and by events later; full event sourcing with an event store and state rebuilt by replay.

</td>
</tr>
<tr markdown="1">
<td class="k">Decision</td>
<td markdown="block">

The Booking Service owns the **hold**. A booking is created as Held by one insert that a unique partial index on (round, table, active status) in the Booking DB accepts for exactly one caller, which is **first lock wins** (BRULE-03, FR-08); every later transition is appended to the booking's history. The Table Availability Service keeps the read model of the table map, one document per round: createRoundTableStatus() creates it from the round when the round is published, and the Booking Service updates it after each transition with holdTable(), releaseHold(), markTableBooked() and markTableOccupied(). The read model never decides who gets a table. In the MVP the updates are synchronous gRPC calls; from Increment 2 they are events on a message broker that the Table Availability Service consumes. There is no event store: a booking stores its current state and its history.

</td>
</tr>
<tr markdown="1">
<td class="k">Status</td>
<td markdown="block">

Accepted on 2026-09-30. Supersedes the locking part of ADR-08; the 5-second hold-expiry job of ADR-08 stays.

</td>
</tr>
<tr markdown="1">
<td class="k">Consequences</td>
<td markdown="block">

- One source of truth: the invariant of BRULE-03 is a database constraint, tested directly under the concurrent holds of NFR-20, and no lock crosses a service boundary.
- Every booking carries its own audit trail, and the table map can be rebuilt at any time from the bookings and the round.
- The message broker of Increment 2 gets a real consumer, the read model, instead of being added for its own sake.
- The map lags a booking change by one call in the MVP, or one event later; the customer who holds sees the result in the same request, other customers within the 2-second poll of ADR-09.
- A failed update leaves the map stale until the Booking Service retries it; the updates are idempotent, and a stale map only costs a customer a refused hold (UC-01 AF-3), never a double booking.
- The polled read stays with the Table Availability Service, so the Booking DB is not hit by the map polling.

</td>
</tr>
</table>
