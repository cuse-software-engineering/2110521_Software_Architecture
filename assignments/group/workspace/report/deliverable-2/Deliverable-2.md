# Concert Table Reservation System for Restaurant

**2110521 วิศวกรรมสถาปัตยกรรมซอฟต์แวร์ (Software Architecture)** · Deliverable #2

> Transcribed from [Deliverable-2.pdf](../../../deliverables/report/Deliverable-2.pdf) (8 pages), the version handed in. Page images are in [png/](png/) (render with `python3 tools/render_pages.py --all`); the architecture diagram of page 7 is extracted at full resolution to [assets/architecture-diagram.png](assets/architecture-diagram.png). Section numbers are kept as submitted (two sections are numbered 1). Page 8 is blank apart from the running header.

## Group Members — SE 101

| Name | Student ID |
|---|---|
| Chetsada Winaikoson | 6772012221 |
| Waris Natirutthakorn | 6872081621 |
| Natcha Thawinpipat | 6870083521 |
| Watayut Aiamanan | 6970267821 |

This document is an integral component of the subject 2110521 Software Architecture, Department of Software Engineering, Faculty of Engineering, Chulalongkorn University

---

## 1. Scope of this deliverable

This document presents the first version of the microservice architecture for the Concert Table Reservation System (CTRS). It contains the Service–Operations–Collaborators table and the architecture diagram of the system, together with the reasoning that ties them to the three business use cases of Deliverable #1.

The architecture covers the three business use cases end to end, including their alternative and exceptional flows:

- **UC-01 Reserve a Specific Table** — the customer browses concert rounds, holds a table for 15 minutes, completes the profile, accepts the terms, pays the full table fee through the Payment Gateway and receives a QR e-ticket by LINE.
- **UC-02 Check In Using Digital QR Ticket** — Front Staff scans the e-ticket at the door, the booking reference is verified against the check-in window, the entry is confirmed and the table becomes occupied; bookings not checked in by the end of the grace period become no-shows.
- **UC-03 Create Concert Event** — the Manager creates a concert round on the venue zone map, prices the table types, validates and publishes it, which makes the round bookable in UC-01 and defines the check-in window used in UC-02.
- **UC-04 Create Venue Zone Map** — the Manager defines and names venue zones, places tables with unique table numbers, assigns table types and seating capacities, uploads seat-view photographs, validates and activates the map, which makes it selectable in UC-03 and provides the floor plan used in UC-01 and UC-02 for rounds that use it.

Maintaining the venue zone map is not itself one of the three business use cases. It appears in the architecture because a round cannot be created without it, and it is owned by the same service that owns the rounds.

---

## 1. Service–Operations–Collaborators

Operations are the business operations exposed by each service. Collaborators are the services or adapters that the service invokes to complete its own operations; an em dash means the service completes its work without calling anyone else.

| Service | Operations | Collaborators |
|---|---|---|
| **Concert Round Service** | createOrUpdateZoneMap()<br>setTableType()<br>uploadSeatViewPhoto()<br>createRound()<br>copyRound()<br>saveRoundAsDraft()<br>validateRound()<br>previewRound()<br>publishRound()<br>unpublishRound()<br>editPublishedRound()<br>getUpcomingRounds()<br>getRound()<br>getRoundTables()<br>getRoundPricing()<br>getCheckInWindow() | **Table Availability Service**<br>initializeRoundTableStatus()<br>**Booking Service**<br>getConfirmedBookingCount()<br>**Media Storage Adapter**<br>storeSeatViewPhoto() |
| **Table Availability Service** | initializeRoundTableStatus()<br>getRoundTableStatus()<br>holdTable()<br>extendHold()<br>releaseHold()<br>markTableBooked()<br>markTableOccupied()<br>releaseTable()<br>publishTableStatusUpdate() | — |
| **Booking Service** | createHeldBooking()<br>setPartySize()<br>calculateTableFee()<br>saveCustomerProfile()<br>acceptBookingTerms()<br>startPayment()<br>confirmBookingPayment()<br>issueETicket()<br>getETicket()<br>cancelBooking()<br>getCustomerBookings()<br>findBookings()<br>checkInBooking()<br>recordAdditionalGuests()<br>escalateCheckIn()<br>resolveEscalation()<br>expireUnpaidBookings()<br>markNoShows()<br>getConfirmedBookingCount() | **Concert Round Service**<br>getRound()<br>getRoundPricing()<br>getCheckInWindow()<br>**Table Availability Service**<br>holdTable()<br>extendHold()<br>releaseHold()<br>markTableBooked()<br>markTableOccupied()<br>releaseTable()<br>**Payment Service**<br>createPaymentRequest()<br>requestRefund()<br>**Notification Service**<br>sendBookingConfirmation()<br>sendHoldExpiredNotice()<br>sendRefundNotice() |
| **Payment Service** | createPaymentRequest()<br>receivePaymentResult()<br>getPaymentStatus()<br>pollPendingPaymentResults()<br>requestRefund()<br>submitTransferSlip()<br>reviewTransferSlip() | **Payment Gateway Adapter**<br>createCheckoutSession()<br>verifyWebhookSignature()<br>queryPaymentStatus()<br>refundPayment()<br>**Media Storage Adapter**<br>storeTransferSlip()<br>**Booking Service**<br>confirmBookingPayment() |
| **Notification Service** | sendBookingConfirmation()<br>sendHoldExpiredNotice()<br>sendRefundNotice()<br>sendSlipDecisionNotice()<br>retryFailedMessages()<br>getDeliveryStatus() | **LINE Messaging Adapter**<br>pushLineMessage() |

---

## Architecture diagram

![CTRS microservice architecture, version 1](assets/architecture-diagram.png)

*Figure 1  CTRS microservice architecture, version 1, drawn in the ports-and-adapters style: every service is a hexagon whose business logic is reached only through adapters on its edges. An arrow A → B means A invokes B; response paths are not drawn. The hosted checkout page of the Payment Gateway is opened by the customer's browser inside the web app and is therefore not shown as a service call.*

The rest of this section transcribes the content of the figure.

### Elements

| Group in the diagram | Element | Text in the element |
|---|---|---|
| Actors | Customer | |
| | Front Staff | scans at the door |
| | Manager | runs the back-office |
| | Time | scheduled triggers |
| Client applications | Customer Web App | (LIFF, inside LINE Messenger) |
| | Back-office Web App | rounds, live view, QR scan on phone |
| | API Gateway | routes requests, verifies caller identity and role |
| Internal services (one box = one business capability) | Table Availability Service, with Table Status DB | per-round table status, 15-minute holds, first lock wins |
| | Concert Round Service, with Round DB | venue zone map, tables, table types and photos; rounds, schedule, prices, check-in window, publish / draft |
| | Booking Service, with Booking DB | booking lifecycle: hold, fee, customer profile, terms, confirmation, e-ticket, check-in, no-show, escalation, expiry |
| | Payment Service, with Payment DB | payment requests, webhook, status polling, refunds, transfer-slip verification |
| | Notification Service, with Notification DB | LINE messages, retries, delivery status |
| Adapters | LINE Login, Media Storage, LINE Messaging, Payment Gateway | Adapter |
| External systems | LINE Login Platform, Cloud Object Storage, LINE Messaging API, Payment Gateway | external |

Every service hexagon has a REST tab on its left vertex.

### Arrows

| From | To | Label |
|---|---|---|
| Customer | Customer Web App | |
| Front Staff | Back-office Web App | |
| Manager | Back-office Web App | |
| Customer Web App | LINE Login Platform | LINE Login (LIFF) |
| Customer Web App | API Gateway | |
| Back-office Web App | API Gateway | |
| API Gateway | LINE Login Adapter | verify ID token |
| API Gateway | Table Availability Service | |
| API Gateway | Concert Round Service | |
| API Gateway | Booking Service | |
| API Gateway | Payment Service | |
| Table Availability Service | Customer Web App (dotted) | table status push (WebSocket) |
| Concert Round Service | Table Availability Service | initializeRoundTableStatus() |
| Concert Round Service | Booking Service | getConfirmedBookingCount() |
| Concert Round Service | Media Storage Adapter | |
| Booking Service | Concert Round Service | getRound() |
| Booking Service | Table Availability Service | |
| Booking Service | Payment Service | createPaymentRequest() |
| Booking Service | Notification Service | |
| Payment Service | Booking Service | confirmBookingPayment() |
| Payment Service | Media Storage Adapter | |
| Payment Service | Payment Gateway Adapter | |
| Notification Service | LINE Messaging Adapter | |
| LINE Login Adapter | LINE Login Platform | |
| Media Storage Adapter | Cloud Object Storage | |
| LINE Messaging Adapter | LINE Messaging API | |
| Payment Gateway Adapter | Payment Gateway (external) | |
| Payment Gateway (external) | API Gateway | payment result (signed webhook) |
| Time | Booking Service | expire holds, mark no-shows, poll payment results (one label for both arrows from Time) |
| Time | Payment Service | |

### Legend

| Symbol | Meaning |
|---|---|
| solid arrow | A → B means A invokes B (synchronous REST) |
| dotted arrow | server-initiated push to the client |
| dashed box | external system / external actor |
| hexagon | service core; REST tab on the left vertex = driving port |
| cylinder | data store owned privately by that service |
