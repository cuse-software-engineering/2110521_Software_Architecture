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

Operations are the business operations exposed by each service; each operation is one function, so creating and updating a record are two operations. Collaborators are the services or adapters that the service invokes to complete its own operations; an em dash means the service completes its work without calling anyone else. A call to another service is a gRPC call, and a call to an adapter stays inside the service (Section 5.2).

Note: the table lists only what the MVP builds. The operations and collaborators that Increment 2 and later increments add (Section 1.3) are not written here.

*Table 5.3 Service–Operations–Collaborators of the MVP*

| Service | Operations | Collaborators |
|---|---|---|
| **Concert Round Service** | createZoneMap()<br>updateZoneMap()<br>uploadZoneMapImage()<br>defineTableType()<br>listZoneMaps()<br>getZoneMap()<br>validateZoneMap()<br>activateZoneMap()<br>getBusinessParameters()<br>updateBusinessParameters()<br>createRound()<br>updateRound()<br>editPublishedRound()<br>validateRound()<br>previewRound()<br>publishRound()<br>getUpcomingRounds()<br>getRound()<br>getRoundTables()<br>getRoundPricing()<br>getCheckInWindow() | **Table Availability Service**<br>initializeRoundTableStatus()<br>getRoundTableStatus()<br>countAvailableTables()<br>**Media Storage Adapter**<br>storeZoneMapImage() |
| **Table Availability Service** | initializeRoundTableStatus()<br>getRoundTableStatus()<br>countAvailableTables()<br>holdTable()<br>releaseHold()<br>markTableBooked()<br>markTableOccupied() | — |
| **Booking Service** | createHeldBooking()<br>getBooking()<br>setPartySize()<br>calculateTableFee()<br>getCustomerProfile()<br>createCustomerProfile()<br>updateCustomerProfile()<br>getBookingTerms()<br>acceptBookingTerms()<br>startPayment()<br>confirmBookingPayment()<br>issueETicket()<br>getETicket()<br>getCustomerBookings()<br>cancelBooking()<br>expireUnpaidBookings()<br>verifyBookingReference()<br>checkInBooking()<br>getRoundBookings() | **Concert Round Service**<br>getRound()<br>getRoundPricing()<br>getCheckInWindow()<br>**Table Availability Service**<br>holdTable()<br>releaseHold()<br>markTableBooked()<br>markTableOccupied()<br>**Payment Service**<br>createPaymentRequest()<br>**Notification Service**<br>sendBookingConfirmation()<br>sendHoldExpiredNotice() |
| **Payment Service** | createPaymentRequest()<br>receivePaymentResult()<br>getPaymentStatus() | **Payment Gateway Adapter**<br>createCheckoutSession()<br>verifyWebhookSignature()<br>**Booking Service**<br>confirmBookingPayment()<br>**Notification Service**<br>sendPaymentFailedNotice() |
| **Notification Service** | sendBookingConfirmation()<br>sendHoldExpiredNotice()<br>sendPaymentFailedNotice()<br>retryFailedMessages() | **LINE Messaging Adapter**<br>pushLineMessage() |
| **Staff Account Service** | signIn()<br>signOut()<br>createStaffAccount()<br>listStaffAccounts()<br>updateStaffAccount()<br>disableStaffAccount() | — |

## 5.4 Use Case Traceability

Tables 5.4 to 5.8 check the design backwards from the use cases. Each row follows one step, or the consecutive steps served by one operation, of a use case: who invokes the operation (an actor, through the API Gateway, or a service), the service and operation that carry the step out, the collaborations the operation needs, the data it stores, and the requirements it realises. Steps in which the actor acts without the system, such as UC-02 step 5, are left out unless a rule applies to them. Only the flows that the MVP builds are listed (Section 1.3), and Table 5.8 covers the requirements that are not tied to one step. Every operation of Table 5.3 appears in at least one row, and every MVP requirement of Section 3.1 is realised by at least one row.

<div class="trace" markdown="1">

*Table 5.4 Traceability of Reserve a Specific Table*

| Steps | Invoked by | Operation | Collaborations | Data stored | Requirements |
|---|---|---|---|---|---|
| 1–2, EF-5 | **Customer** | API Gateway: check the LINE ID token that LINE Login gave the **LIFF** app | LINE Login Adapter, which asks the **LINE Platform** | — | FR-01, FR-02 |
| 3, AF-2 | **Customer** | Concert Round Service: getUpcomingRounds(), with the status of each round | Table Availability Service: countAvailableTables(), for the sold-out status | — | FR-03 |
| 4, AF-1 | **Customer** | Concert Round Service: getRound() | — | — | FR-03, FR-04 |
| 5, AF-2 | **Customer** | Concert Round Service: getRoundTables()<br>Table Availability Service: getRoundTableStatus(), polled every 2 seconds | — | — | FR-05, FR-06 |
| 6–8, AF-3 | **Customer** | Booking Service: createHeldBooking() | Concert Round Service: getRound(), to check that booking is open<br>Table Availability Service: holdTable() | Booking DB: booking Held until the end of the **hold**<br>Table Status DB: table held | FR-04, FR-07, FR-08 |
| 9 | **Customer** | Booking Service: getBooking(), the booking summary and the remaining **hold** time | — | — | FR-07 |
| 10 | **Customer** | Booking Service: setPartySize() | — | Booking DB: **party size** | FR-09 |
| 11 | **Customer** | Booking Service: calculateTableFee() | Concert Round Service: getRoundPricing() | Booking DB: **full table fee** | FR-09 |
| 12 | **Customer** | Booking Service: getCustomerProfile(), which tells whether a profile exists | — | — | FR-10 |
| 12a, AF-7 | **Customer** | Booking Service: createCustomerProfile(), with the consent, the name and the phone; AF-7 is its validation | — | Booking DB: **customer profile** and consent | FR-10 |
| 12b | **Customer** | Booking Service: updateCustomerProfile(), when the **Customer** corrects the pre-filled profile | — | Booking DB: **customer profile** | FR-10 |
| 13 | **Customer** | Booking Service: getBookingTerms() | Concert Round Service: getCheckInWindow() | — | FR-12 |
| 14 | **Customer** | Booking Service: acceptBookingTerms() | — | Booking DB: **booking terms** accepted | FR-12 |
| 15 | **Customer** | Booking Service: startPayment() | Payment Service: createPaymentRequest() | Booking DB: payment started | FR-13 |
| 15 | Booking Service | Payment Service: createPaymentRequest() | Payment Gateway Adapter: createCheckoutSession() | Payment DB: payment request | FR-13 |
| 16–17 | **Customer** | No operation of SEATS: the **Customer** pays in the **hosted checkout** of the **Payment Gateway**, simulated in the MVP (ADR-11) | — | — | FR-13 |
| 18, AF-5 | **Payment Gateway** | Payment Service: receivePaymentResult(), the signed webhook routed by the API Gateway; a duplicate result is ignored | Payment Gateway Adapter: verifyWebhookSignature()<br>Booking Service: confirmBookingPayment(), when paid<br>Notification Service: sendPaymentFailedNotice(), when declined | Payment DB: payment result, processed once | FR-14, FR-16, FR-21 |
| 19 | Payment Service | Booking Service: confirmBookingPayment() | Table Availability Service: markTableBooked() | Booking DB: payment recorded, booking Confirmed<br>Table Status DB: table booked | FR-16 |
| 20 | Booking Service | Booking Service: issueETicket(), at the end of confirmBookingPayment() | — | Booking DB: **e-ticket** with the signed **booking reference** | FR-19 |
| 21, AF-5 | **Customer** | Payment Service: getPaymentStatus()<br>Booking Service: getBooking(), getETicket() | — | — | FR-14, FR-19 |
| 22, S-1 | Booking Service | Notification Service: sendBookingConfirmation() | LINE Messaging Adapter: pushLineMessage() | Notification DB: message and delivery result | FR-20 |
| AF-4, AF-6 | **Customer** | Booking Service: cancelBooking() | Table Availability Service: releaseHold() | Booking DB: booking Cancelled<br>Table Status DB: table available | FR-10, FR-11 |
| AF-5 | Payment Service | Notification Service: sendPaymentFailedNotice() | LINE Messaging Adapter: pushLineMessage() | Notification DB: message and delivery result | FR-21 |
| EF-1 | Time | Booking Service: expireUnpaidBookings(), every 5 seconds (ADR-08) | Table Availability Service: releaseHold()<br>Notification Service: sendHoldExpiredNotice() | Booking DB: booking Expired<br>Table Status DB: table available | FR-21, FR-23 |
| EF-1, S-1 | Booking Service | Notification Service: sendHoldExpiredNotice() | LINE Messaging Adapter: pushLineMessage() | Notification DB: message and delivery result | FR-21 |
| EF-6 | Notification Service, on its own timer | Notification Service: retryFailedMessages(), 3 times within 5 minutes | LINE Messaging Adapter: pushLineMessage() | Notification DB: delivery result | FR-22 |

*Table 5.5 Traceability of Check In Using Digital QR Ticket*

| Steps | Invoked by | Operation | Collaborations | Data stored | Requirements |
|---|---|---|---|---|---|
| 2–4, S-1, AF-2, AF-3, AF-5, EF-1, EF-2 | **Front Staff** | Booking Service: verifyBookingReference(), with the **booking reference** scanned (step 2) or typed (AF-2); its answer is the result of step 4 or the reason of AF-3, AF-5, EF-1 and EF-2 | Concert Round Service: getCheckInWindow() | — (verification changes nothing) | FR-24, FR-25, FR-26, FR-27 |
| 6, EF-5 | **Front Staff** | Booking Service: checkInBooking(); a retry finds the existing check-in and does not repeat it (EF-5) | Table Availability Service: markTableOccupied() | Booking DB: booking Checked-in with the time and the staff account<br>Table Status DB: table occupied | FR-28 |
| 7 | **Manager** | Booking Service: getRoundBookings()<br>Table Availability Service: getRoundTableStatus(), polled every 2 seconds | — | — | FR-06, FR-42 |
| AF-4 | **Front Staff** | No operation of SEATS: extra guests are handled by hand (BRULE-09) | — | — | — |

*Table 5.6 Traceability of Create Concert Event*

| Steps | Invoked by | Operation | Collaborations | Data stored | Requirements |
|---|---|---|---|---|---|
| 1–2 | **Manager** | Concert Round Service: createRound() | — | Round DB: a new round, Draft | FR-34 |
| 3–5 | **Manager** | Concert Round Service: updateRound(), with the concert details, the times and the **booking-open time**; it derives the **check-in window** from getBusinessParameters() | — | Round DB: schedule, **booking-open time**, **check-in window** | FR-34, FR-38 |
| 6 | **Manager** | Concert Round Service: listZoneMaps(), the Active maps | — | — | FR-35 |
| 7 | **Manager** | Concert Round Service: getZoneMap() | — | — | FR-35 |
| 8 | **Manager** | Concert Round Service: updateRound(), with the **zone map** and the tables not for sale | — | Round DB: the round's **zone map** and tables for sale | FR-35 |
| 9–10 | **Manager** | Concert Round Service: updateRound(), with the **package price** and content of each **table type** in each **zone**; it answers with the tables for sale and the capacity of each **zone** | — | Round DB: **package prices** | FR-37 |
| 11–12, S-1, EF-1 | **Manager** | Concert Round Service: validateRound() | — | — | FR-75 |
| 13 | **Manager** | Concert Round Service: previewRound() | — | — | — |
| 14–15, EF-2 | **Manager** | Concert Round Service: publishRound(); a retry finds the published round and does not create a second one (EF-2) | Table Availability Service: initializeRoundTableStatus() | Round DB: round Published<br>Table Status DB: every table for sale available | FR-34, FR-75 |
| AF-1 | **Manager** | Concert Round Service: updateRound(); the round stays Draft | — | Round DB: the round as entered | FR-34 |
| AF-3 | **Manager** | Concert Round Service: getRound(), then editPublishedRound(), which allows only the changes of AF-3 (BRULE-07) | Table Availability Service: getRoundTableStatus(), whose booked tables are the Confirmed bookings | Round DB: the changed fields | FR-34, FR-35 |

*Table 5.7 Traceability of Create Venue Zone Map*

| Steps | Invoked by | Operation | Collaborations | Data stored | Requirements |
|---|---|---|---|---|---|
| 1–2 | **Manager** | Concert Round Service: createZoneMap() | — | Round DB: a new **zone map**, Draft | FR-37 |
| 3, EF-3 | **Manager** | Concert Round Service: uploadZoneMapImage() | Media Storage Adapter: storeZoneMapImage() | Cloud Object Storage: image of the venue<br>Round DB: its address | FR-39 |
| 4 | **Manager** | Concert Round Service: updateZoneMap(), with the **zones** drawn and named | — | Round DB: **zones** | FR-37 |
| 5–6 | **Manager** | Concert Round Service: updateZoneMap(), with each table's position, number, **table type** and capacity; defineTableType() for a **table type** the venue does not have yet | — | Round DB: tables and **table types** | FR-37, FR-39 |
| 7 | **Manager** | Concert Round Service: getZoneMap(), with the number of tables and the capacity of each **zone** | — | — | FR-37 |
| 8–9, S-1, EF-1 | **Manager** | Concert Round Service: validateZoneMap() | — | — | FR-74 |
| 10 | **Manager** | Concert Round Service: getZoneMap(), the preview | — | — | — |
| 11–12, EF-2 | **Manager** | Concert Round Service: activateZoneMap(); a retry finds the Active map and does not create a second one (EF-2) | — | Round DB: **zone map** Active | FR-74 |
| AF-1 | **Manager** | Concert Round Service: listZoneMaps(), getZoneMap(), then updateZoneMap(), which allows only the changes of AF-1 | Table Availability Service: getRoundTableStatus(), for the Published rounds that use the map | Round DB: the changed **zones** and tables | FR-37 |
| AF-3 | **Manager** | Concert Round Service: updateZoneMap(); the map stays Draft | — | Round DB: the map as entered | FR-37 |

*Table 5.8 Traceability of the requirements not tied to one step*

| Function | Invoked by | Operation | Collaborations | Data stored | Requirements |
|---|---|---|---|---|---|
| **Business parameters** | **Manager** | Concert Round Service: getBusinessParameters(), updateBusinessParameters() | — | Round DB: the **business parameters**; a round uses the values in force at its **booking-open time** | FR-38 |
| My Bookings | **Customer** | Booking Service: getCustomerBookings(), getETicket() | — | — | FR-40 |
| **Live view** | **Manager**, **Owner** | Booking Service: getRoundBookings()<br>Table Availability Service: getRoundTableStatus() | — | — | FR-42 |
| Staff accounts | **Manager** | Staff Account Service: createStaffAccount(), listStaffAccounts(), updateStaffAccount() for the role, disableStaffAccount() | — | Staff Account DB: accounts, roles and password hashes | FR-65 |
| Sign-in and roles | **Front Staff**, **Manager**, **Owner** | Staff Account Service: signIn(); the API Gateway checks the role of every request | — | — | FR-65, FR-66 |
| Log out | All users | Staff Account Service: signOut(); a **Customer** logs out of LINE Login in the web app | — | — | FR-73 |

</div>

## 5.5 Architecture Diagram

![SEATS microservice architecture, version 2](assets/architecture-diagram.png)

*Figure 5.1 SEATS microservice architecture, version 2*
