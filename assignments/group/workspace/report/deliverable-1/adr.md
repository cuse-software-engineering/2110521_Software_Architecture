# Architecture Decision Records (ADRs)

> Part of [Deliverable-1.md](Deliverable-1.md) — Concert Table Reservation System (2110521 Software Architecture).

## Contents

| ID | Title | Status |
|---|---|---|
| [ADR-01](#adr-01-frontend-architecture--client-channel) | Frontend Architecture & Client Channel | Accepted |
| [ADR-02](#adr-02-real-time-floor-plan-communication) | Real-Time Floor Plan Communication | Accepted |
| [ADR-03](#adr-03-backend-language--framework) | Backend Language & Framework | Accepted |
| [ADR-04](#adr-04-notification-engine) | Notification Engine | Accepted |
| [ADR-05](#adr-05-interactive-floor-plan-rendering) | Interactive Floor Plan Rendering | Accepted |
| [ADR-06](#adr-06-primary-database-engine) | Primary Database Engine | Accepted |
| [ADR-07](#adr-07-internal-role-authentication-front-staff-manager) | Internal Role Authentication (Front Staff, Manager) | Accepted |

---


## ADR-01: Frontend Architecture & Client Channel

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

## ADR-02: Real-Time Floor Plan Communication

**Context**
When multiple customers look at the floor plan simultaneously on busy nights, table statuses must update instantaneously to prevent double-booking conflicts and outdated views.

**Decision**
Implement WebSocket (or Server-Sent Events - SSE) for real-time table status broadcasting, combined with short-term Redis distributed locks for table selection checkout.

**Status**
Accepted

**Consequences**
- Delivers sub-second UI updates when tables are locked, booked, or released.
- Avoids wasteful client polling against the backend server.
- Requires maintaining persistent connection pools and managing socket disconnect/reconnect states on mobile networks.

## ADR-03: Backend Language & Framework

**Context**
The system requires rapid development cycles while supporting RESTful APIs, real-time bi-directional communication for floor plan updates, seamless integration with the LINE Messaging API/LIFF SDK, and scheduled background tasks to automatically release expired table reservations past the cutoff window. Options considered include Go, Java, and Node.js (JavaScript). Given that the frontend is built using Next.js/React, adopting a unified language stack across client and server significantly streamlines development.

**Decision**
Use Node.js (JavaScript) with the Express.js framework for the core API services, combined with Socket.io for real-time WebSocket communication and node-cron for background cutoff scheduling.

**Status**
Accepted

**Consequences**
- Enables a unified full-stack JavaScript environment, allowing the team to share utility logic, minimize context switching, and accelerate feature delivery.
- Leverages Node.js's event-driven, non-blocking I/O model to handle concurrent client connections efficiently during peak reservation hours.
- Because JavaScript is dynamically typed, the backend requires robust runtime request validation and clear documentation to prevent data type mismatches.

## ADR-04: Notification Engine

**Context**
Reminders before cutoff times are critical to reducing lost tables. Traditional SMS is costly per transaction, whereas email is rarely checked by nightlife patrons in real time.

**Decision**
Use LINE Messaging API (Push Messages / Flex Messages) as the primary notification channel, supplemented by Web Push notifications.

**Status**
Accepted

**Consequences**
1. Near 100% open rate with interactive rich cards ("On My Way" / "Postpone 30 mins").
2. Low messaging cost within standard official account quotas.
3. Requires users to add or link the venue's LINE Official Account (OA).

## ADR-05: Interactive Floor Plan Rendering

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

## ADR-06: Primary Database Engine

**Context**
The system needs to store diverse data structures, including flexible venue floor plan layouts (coordinates, shapes, multi-table zone configs, table perspective photos), booking transaction records, customer profiles, and time-stamped status transitions. Traditional relational databases (RDBMS) enforce rigid table schemas that make storing deeply nested floor layout geometries and dynamic table attributes cumbersome. Additionally, the backend runtime is Node.js/JavaScript, making native JSON/BSON document handling particularly advantageous for rapid development.

**Decision**
Use MongoDB as the primary NoSQL document database, accessed via the Mongoose Object Data Modeling (ODM) library in the Node.js backend.

**Status**
Accepted

**Consequences**
- **Flexible Schema for Layouts:** Enables storing complex, nested JSON objects (such as floor plan coordinate maps, zone definitions, and table media links) directly without complex multi-table joins.
- **Seamless Node.js Integration:** Documents map directly to JavaScript objects (JSON) reducing serialization overhead and development friction.
- **Native TTL (Time-To-Live) Indexes:** Provides built-in TTL indexing capabilities, which can automatically handle temporary reservation locks or draft bookings that expire if not checked out within a few minutes.
- **Horizontal Scalability:** Supports horizontal partitioning (sharding) should the platform expand to serve multiple nightlife venues concurrently.

## ADR-07: Internal Role Authentication (Front Staff, Manager)

**Context**
Customers reach the web app through LINE and are authenticated with LINE Login, as decided in ADR-01. Front Staff and Managers use internal accounts created by the venue, and front-of-house staff work from shared devices. Binding those accounts to personal LINE profiles would tie venue access to individual social accounts and make shift handover and staff turnover difficult. Options considered: LINE Login for every role, venue-issued username and password accounts, and an external identity provider.

**Decision**
Use venue-issued username and password accounts with JWT sessions for all internal roles (Front Staff and Manager), kept separate from the customer LINE Login flow. Each account carries a role that determines which back-office functions it may use (e.g. check-in for Front Staff; zone map and round creation for the Manager). The Manager creates, updates, and deactivates internal accounts from the venue configuration.

**Status**
Accepted

**Consequences**
- Venue access stays under the owner's control and survives staff turnover, because accounts are not tied to personal LINE profiles.
- Requires the system to implement password storage, session expiry, and account lockout instead of delegating all authentication to LINE.
- Two authentication paths must be maintained and tested, one for customers and one for internal roles.
