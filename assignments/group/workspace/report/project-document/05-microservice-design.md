# 5 Microservice Design

## 5.1 Scope of the Microservice Design

This section presents the second version of the microservice architecture for the Seating & Event Availability Tracking System (SEATS). It defines the parts of the system and how they communicate (Section 5.2), lists the services with their operations and collaborators (Section 5.3), traces every step of the four use cases to the operations that carry it out (Section 5.4), and draws the architecture (Section 5.5). The section describes the MVP of Section 1.3 only: the operations, collaborations and components that Increment 2 and later increments add are not shown, and they are added to this section when those increments are designed.

The architecture covers the four use cases end to end, including the alternative and exception flows that the MVP builds:

- **UC-01 Reserve a Specific Table** — the **Customer** browses **concert rounds**, holds a table for 15 minutes, completes the profile, accepts the terms, pays the **full table fee** through the simulated **Payment Gateway** (ADR-11) and receives a QR **e-ticket** by LINE.
- **UC-02 Check In Using Digital QR Ticket** — **Front Staff** scans the **e-ticket** at the door, the **booking reference** is verified against the **check-in window** and the **grace period**, the entry is confirmed and the table becomes occupied on the **live view**.
- **UC-03 Create Concert Event** — the **Manager** creates a **concert round** on the venue **zone map**, prices the **table types**, validates and publishes it, which makes the round bookable in UC-01 and defines the **check-in window** used in UC-02.
- **UC-04 Create Venue Zone Map** — the **Manager** uploads the image of the venue, defines and names venue **zones** on it, places tables with unique table numbers, assigns **table types** and seating capacities, validates and activates the map, which makes it selectable in UC-03 and provides the floor plan used in UC-01 and UC-02 for rounds that use it.

The Deliverable #2 brief asks for at least three business use cases; the design covers all four. The venue **zone map** is owned by the same service that owns the rounds, because a round cannot be created without it. Which tables of a round are booked is read from the Table Availability Service, which owns the status of every table, so the Concert Round Service does not depend on the Booking Service. The **back-office** accounts of ADR-07 are owned by the Staff Account Service.

The services follow the bounded contexts of the domain, and each is named by the glossary term for what it owns:

- **Concert Round Service** — the venue and events context: **zone maps**, **table types**, **concert rounds**, prices and **business parameters**. A supporting subdomain.
- **Table Availability Service** — the table availability context: the status of every table of every round and the rule that one **hold** or booking exists per table per round (**first lock wins**). A core subdomain, since double bookings are the problem the system solves.
- **Booking Service** — the booking context: the booking from Held to Checked-in, with the **customer profile** and the **e-ticket** as parts of the same aggregate. A core subdomain.
- **Payment Service**, **Notification Service** and **Staff Account Service** — the generic subdomains of payment, messaging and staff identity, each behind an external provider or a standard mechanism, and each changing for its own reasons.

Table Availability and Booking stay two services although every booking state change has a matching table status change: the table status is also written by the Concert Round Service when a round is published, it is read by every open map, and its consistency with the booking is handled by ADR-08.

The architecture diagram of Section 5.5 (Figure 5.1) is drawn in the ports-and-adapters style: every service is a hexagon whose business logic is reached only through the ports on its edges, a REST tab for the calls routed by the API Gateway and a gRPC tab for the calls of other services, and that reaches the external systems only through adapters. The API Gateway carries the REST tab that the Frontend calls: it is the only API that the web apps use. An arrow A → B means A invokes B; response paths are not drawn. The three dashed boundaries are the parts of Section 5.2. The **hosted checkout** page of the **Payment Gateway** is opened by the customer's browser inside the web app and is therefore not shown as a service call. The web apps read the table status by polling through the API Gateway (ADR-09), and the **Payment Gateway** is the simulated gateway of ADR-11.

## 5.2 Parts of the System and Communication

SEATS is divided into three parts: the Frontend, the Backend and the External systems (Table 5.1). Figure 5.1 draws their boundaries, and each ADR names the part it concerns (Table 4.1). How the parts communicate with each other, and how the services communicate inside the Backend, is decided in ADR-12 and summarised in Table 5.2.

*Table 5.1 Parts of the system*

| Part | Components | Where it runs, and who can reach it |
|---|---|---|
| Frontend | Customer Web App (a **LIFF** app inside LINE); Back-office Web App | In the phones and browsers of the **Customers**, the **Front Staff**, the **Manager** and the **Owner**. The Frontend is not trusted: every request it sends is authenticated and checked in the Backend. |
| Backend | API Gateway; the Concert Round, Table Availability, Booking, Payment, Notification and Staff Account Services, each with its private database; the adapters to the external systems | On the servers that run SEATS. The API Gateway is the only component reachable from the internet; the services and their databases sit on a private network behind it. Each adapter is a module of the component that uses it. |
| External systems | **LINE Platform** (LINE Login and the Messaging API); **Payment Gateway**; Cloud Object Storage for the image of the venue | Run by third parties, outside the control of SEATS. The simulated gateway of the MVP (ADR-11) is built by the group but deployed and treated as an external system, so that the real gateway can replace it. |

*Table 5.2 Communication between and inside the parts (ADR-12)*

| From | To | How | Used for |
|---|---|---|---|
| Frontend | API Gateway | REST: JSON over HTTPS | Every operation that an actor invokes (Section 5.4) |
| **Payment Gateway** | API Gateway | REST: signed webhook over HTTPS | Payment results |
| API Gateway | Services | REST: JSON over HTTP on the private network | Each request goes to the service that owns the operation |
| Service | Service | gRPC: Protocol Buffers over HTTP/2 | Every collaboration between services in Table 5.3 |
| Service or API Gateway | Its adapters | Call inside the same process | Reaching an external system |
| Adapter | External system | The provider's HTTPS API | LINE ID token check, LINE push messages, checkout and payment results, storing the image of the venue |
| Frontend | External systems | The provider's own SDK or page | LINE Login in the **LIFF** app; the **hosted checkout** of the **Payment Gateway** |
| Service | Its database | Database driver (MongoDB, ADR-06) | A service reads and writes only its own database |

Every service that the web apps use offers a REST API to the API Gateway, and every service that another service calls offers a gRPC API: the Notification Service has only a gRPC API and the Staff Account Service only a REST API. The API Gateway authenticates every request before routing it: a **Customer** by the LINE ID token, checked through the LINE Login Adapter, and a member of staff by the session token issued by the Staff Account Service (ADR-07), whose role decides which operations the request may reach (FR-66). The payment webhook is the exception: the gateway passes it on, and the Payment Service verifies its signature (NFR-38).

## 5.3 Service–Operations–Collaborators

Operations are the business operations that a service exposes to the web apps (REST) or to other services (gRPC); each operation is one function, so creating and updating a record are two operations. What a service does on its own timer, or as a step inside another operation, is not an operation and is described below the table. Collaborators are the services or adapters that the service invokes to complete its own operations; an em dash means the service completes its work without calling anyone else. A call to another service is a gRPC call, and a call to an adapter stays inside the service (Section 5.2).

Note: the table lists only what the MVP builds. The operations and collaborators that Increment 2 and later increments add (Section 1.3) are not written here.

*Table 5.3 Service–Operations–Collaborators of the MVP*

| Service | Operations | Collaborators |
|---|---|---|
| **Concert Round Service** | createZoneMap()<br>updateZoneMap()<br>uploadZoneMapImage()<br>defineTableType()<br>listTableTypes()<br>listZoneMaps()<br>getZoneMap()<br>validateZoneMap()<br>activateZoneMap()<br>getBusinessParameters()<br>updateBusinessParameters()<br>createRound()<br>updateRound()<br>validateRound()<br>publishRound()<br>getUpcomingRounds()<br>getRound()<br>getRoundTables()<br>getRoundPricing()<br>getCheckInWindow() | **Table Availability Service**<br>initializeRoundTableStatus()<br>getRoundTableStatus()<br>countAvailableTables()<br>**Media Storage Adapter**<br>storeZoneMapImage() |
| **Table Availability Service** | initializeRoundTableStatus()<br>getRoundTableStatus()<br>countAvailableTables()<br>holdTable()<br>releaseHold()<br>markTableBooked()<br>markTableOccupied() | — |
| **Booking Service** | createHeldBooking()<br>getBooking()<br>setPartySize()<br>getCustomerProfile()<br>createCustomerProfile()<br>updateCustomerProfile()<br>getBookingTerms()<br>acceptBookingTerms()<br>startPayment()<br>confirmBookingPayment()<br>getETicket()<br>getCustomerBookings()<br>cancelBooking()<br>verifyBookingReference()<br>checkInBooking()<br>getRoundBookings() | **Concert Round Service**<br>getRound()<br>getRoundPricing()<br>getCheckInWindow()<br>**Table Availability Service**<br>holdTable()<br>releaseHold()<br>markTableBooked()<br>markTableOccupied()<br>**Payment Service**<br>createPaymentRequest()<br>**Notification Service**<br>sendBookingConfirmation()<br>sendHoldExpiredNotice() |
| **Payment Service** | createPaymentRequest()<br>receivePaymentResult()<br>getPaymentStatus() | **Payment Gateway Adapter**<br>createCheckoutSession()<br>verifyWebhookSignature()<br>**Booking Service**<br>confirmBookingPayment()<br>**Notification Service**<br>sendPaymentFailedNotice() |
| **Notification Service** | sendBookingConfirmation()<br>sendHoldExpiredNotice()<br>sendPaymentFailedNotice() | **LINE Messaging Adapter**<br>pushLineMessage() |
| **Staff Account Service** | signIn()<br>signOut()<br>createStaffAccount()<br>listStaffAccounts()<br>updateStaffAccount()<br>disableStaffAccount() | — |

Two services also run a job on their own timer, which is not an operation: the hold-expiry job of the Booking Service sets every overdue Held booking to Expired every 5 seconds and calls releaseHold() and sendHoldExpiredNotice() (ADR-08, UC-01 EF-1), and the retry job of the Notification Service resends a failed message 3 times within 5 minutes (FR-22, UC-01 EF-6). Two steps are part of a larger operation: setPartySize() computes the **full table fee** (UC-01 steps 10–11), and confirmBookingPayment() issues the **e-ticket** (UC-01 steps 19–20). A Published round is changed with updateRound(), which then allows only the changes of UC-03 AF-3 (BRULE-07), and the preview of a round (UC-03 step 13) is the customer's own view, getRound() and getRoundTables().

## 5.4 Use Case Traceability

Table 5.4 traces the four use cases and the system-wide functions to the operations of Table 5.3: a cell names the steps and flows of the use case that the operation serves, whether the actor invokes it through the API Gateway or another service invokes it as a collaborator. Every operation has at least one cell, and the two jobs on a timer are listed below the operations. Appendix D gives the same trace step by step, with who invokes each operation, the collaborations it needs, the data it stores and the requirements it realises; only the flows that the MVP builds are traced (Section 1.3).

<div class="matrix" markdown="1">

*Table 5.4 Operations by use case*

| Service | Operation | UC-01 | UC-02 | UC-03 | UC-04 | System-wide |
|---|---|---|---|---|---|---|
| **Concert Round Service** | createZoneMap() |  |  |  | 1–2 |  |
|  | updateZoneMap() |  |  |  | 4; 5–6; AF-1; AF-3 |  |
|  | uploadZoneMapImage() |  |  |  | 3, EF-3 |  |
|  | defineTableType() |  |  |  | 5–6 |  |
|  | listTableTypes() |  |  |  | 5–6 |  |
|  | listZoneMaps() |  |  | 6 | AF-1 |  |
|  | getZoneMap() |  |  | 7 | 7; 10; AF-1 |  |
|  | validateZoneMap() |  |  |  | 8–9, S-1, EF-1 |  |
|  | activateZoneMap() |  |  |  | 11–12, EF-2 |  |
|  | getBusinessParameters() |  |  | 3–5 |  | Business parameters |
|  | updateBusinessParameters() |  |  |  |  | Business parameters |
|  | createRound() |  |  | 1–2 |  |  |
|  | updateRound() |  |  | 3–5; 8; 9–10; AF-1; AF-3 |  |  |
|  | validateRound() |  |  | 11–12, S-1, EF-1 |  |  |
|  | publishRound() |  |  | 14–15, EF-2 |  |  |
|  | getUpcomingRounds() | 3, AF-2 |  |  |  |  |
|  | getRound() | 4, AF-1; 6–8, AF-3 |  | 13; AF-3 |  |  |
|  | getRoundTables() | 5, AF-2 |  | 13 |  |  |
|  | getRoundPricing() | 10–11 |  |  |  |  |
|  | getCheckInWindow() | 13 | 2–4, S-1, AF-2, AF-3, AF-5, EF-1, EF-2 |  |  |  |
| **Table Availability Service** | initializeRoundTableStatus() |  |  | 14–15, EF-2 |  |  |
|  | getRoundTableStatus() | 5, AF-2 | 7 | AF-3 | AF-1 | Live view |
|  | countAvailableTables() | 3, AF-2 |  |  |  |  |
|  | holdTable() | 6–8, AF-3 |  |  |  |  |
|  | releaseHold() | AF-4, AF-6; EF-1 |  |  |  |  |
|  | markTableBooked() | 19–20 |  |  |  |  |
|  | markTableOccupied() |  | 6, EF-5 |  |  |  |
| **Booking Service** | createHeldBooking() | 6–8, AF-3 |  |  |  |  |
|  | getBooking() | 9; 21, AF-5 |  |  |  |  |
|  | setPartySize() | 10–11 |  |  |  |  |
|  | getCustomerProfile() | 12 |  |  |  |  |
|  | createCustomerProfile() | 12a, AF-7 |  |  |  |  |
|  | updateCustomerProfile() | 12b |  |  |  |  |
|  | getBookingTerms() | 13 |  |  |  |  |
|  | acceptBookingTerms() | 14 |  |  |  |  |
|  | startPayment() | 15 |  |  |  |  |
|  | confirmBookingPayment() | 18, AF-5; 19–20 |  |  |  |  |
|  | getETicket() | 21, AF-5 |  |  |  | My Bookings |
|  | getCustomerBookings() |  |  |  |  | My Bookings |
|  | cancelBooking() | AF-4, AF-6 |  |  |  |  |
|  | verifyBookingReference() |  | 2–4, S-1, AF-2, AF-3, AF-5, EF-1, EF-2 |  |  |  |
|  | checkInBooking() |  | 6, EF-5 |  |  |  |
|  | getRoundBookings() |  | 7 |  |  | Live view |
| **Payment Service** | createPaymentRequest() | 15 |  |  |  |  |
|  | receivePaymentResult() | 18, AF-5 |  |  |  |  |
|  | getPaymentStatus() | 21, AF-5 |  |  |  |  |
| **Notification Service** | sendBookingConfirmation() | 22, S-1 |  |  |  |  |
|  | sendHoldExpiredNotice() | EF-1; EF-1, S-1 |  |  |  |  |
|  | sendPaymentFailedNotice() | 18, AF-5; AF-5 |  |  |  |  |
| **Staff Account Service** | signIn() |  |  |  |  | Sign-in and roles |
|  | signOut() |  |  |  |  | Log out |
|  | createStaffAccount() |  |  |  |  | Staff accounts |
|  | listStaffAccounts() |  |  |  |  | Staff accounts |
|  | updateStaffAccount() |  |  |  |  | Staff accounts |
|  | disableStaffAccount() |  |  |  |  | Staff accounts |
| *Jobs on a timer (not operations)* | hold-expiry job of the Booking Service | EF-1 | | | | |
| | retry job of the Notification Service | EF-6 | | | | |

</div>

## 5.5 Architecture Diagram

![SEATS microservice architecture, version 2](assets/architecture-diagram.png)

*Figure 5.1 SEATS microservice architecture, version 2*
