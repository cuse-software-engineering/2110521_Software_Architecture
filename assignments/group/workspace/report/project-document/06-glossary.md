# 6 Glossary

Table 6.1 lists the business terms of this document: the words of the venue, its customers and its rules. In the text they are set in bold, and in the PDF each bold term links to its entry. Table 6.2 lists the technology and project terms that the ADRs and the microservice design use; they are not set in bold in the text.

*Table 6.1 Business terms*

| Term | Definition |
|---|---|
| Back-office | The staff web application of the venue, used on a desktop or a phone by the Front Staff and the Manager; the Owner reads it without changing anything. |
| Booking | A Customer's reservation of one table for one concert round, the central record. Its states are Held, Confirmed, Checked-in, Expired, Cancelled and No-show; Transferred belongs to a later release. |
| Booking reference | The signed reference of a booking encoded in the QR code of its e-ticket, valid only for its concert round and table; it is printed under the code so that it can be typed when a scan fails. |
| Booking terms | The terms shown before payment and accepted by the Customer: full payment confirms the booking, the check-in window, the grace period, and no refund for a no-show (BRULE-16). |
| Booking-open time | The time, set by the Manager for each concert round, from which its tables can be selected; before it the round is visible but not bookable (BRULE-07). |
| Business parameters | The venue's settings that apply to every round opening for booking afterwards: hold period, grace period, check-in window and extra-person fee (FR-38). |
| Check-in window | The period in which an e-ticket can be checked in: from 2 hours before the concert start to the end of the grace period (BRULE-04, BRULE-05). |
| Concert round | One scheduled live performance on a given date and start time, featuring one artist, for which every table is sold in advance; it has a booking-open time and a fixed zone map. |
| Customer | A LINE user who reserves a table for a concert night, for a party of 1 to 6 people. |
| Customer profile | The Customer's name, phone and LINE user id, collected once with consent and pre-filled for later bookings (BRULE-11). |
| Degraded mode | The payment mode used while the payment gateway is unreachable: the Customer transfers the full table fee to the venue's bank account and attaches the transfer slip, and the Manager confirms or rejects it (Increment 2). |
| E-ticket | The electronic ticket with a QR code issued when a booking is confirmed; it carries the booking reference. |
| Escalation | The hand-over of an invalid or duplicate ticket from the Front Staff to the Manager, who accepts or refuses entry (Increment 2). |
| Extra-person fee | 600 THB for each person above the capacity of the table type, added to the full table fee at purchase (BRULE-09). |
| First lock wins | The rule that, of several customers selecting the same table, only the first successful hold keeps it; the others are told that the table was just taken (BRULE-03). |
| Front Staff | The venue staff who work the door on concert nights and check guests in with the back-office on a phone. |
| Full table fee | The whole price of the booked package plus any extra-person fees, paid in advance and in full; there is no deposit and nothing is paid at the venue (BRULE-01). |
| Grace period | The 30 minutes after the concert start during which a late Customer still gets the booked table (BRULE-05). |
| Hold | The temporary, exclusive lock a Customer obtains on a table by selecting it; it lasts the hold period and is released automatically when no payment is confirmed (BRULE-02). |
| Hold period | The 15 minutes a hold lasts from the selection of the table (BRULE-02). |
| LINE Official Account | The venue's account on LINE; Customers who are its friends open the web app from its Rich Menu and receive its messages. |
| LINE Platform | The external LINE services the system uses: LINE Login for the Customer's identity, LIFF and the Messaging API. |
| Live view | The back-office screen that shows the tables and bookings of the current concert round as they change; the Owner reads it read-only. |
| Manager | The venue manager who runs the back-office: zone maps, concert rounds and prices, the live view, and rulings on escalated tickets. |
| No-show | A confirmed booking whose Customer has not checked in by the end of the grace period; the fee is not refunded and the table is resold by hand to walk-in guests (BRULE-06). |
| Owner | The owner of the venue, who reads the back-office without changing anything. |
| Package | A table type as sold: its capacity, contents and package price; "package" and "table type" are used interchangeably (BRULE-08). |
| Package price | The price of a table type in a zone, maintained by the Manager for each round (BRULE-08). |
| Party size | The number of guests of a booking, entered by the Customer; it determines the extra-person fee. |
| Payment Gateway | The external payment service that takes the full table fee and reports the payment result by signed webhook: simulated in the MVP, Beam Checkout from Increment 2. |
| Table type | The type of a table, for example a 2-person round table, a 4-person square table or a 6-person sofa, which fixes its capacity and its package. |
| Transfer slip | The proof of a bank transfer attached by the Customer in degraded mode (Increment 2). |
| Waitlist | A queue of customers for a sold-out round, planned for a later release; a no-show table is never offered to it. |
| Walk-in | Guests without a booking; they can only take the tables of no-shows, seated and paid by hand at the venue (FR-72). |
| Zone | A pricing area of the venue, for example Zone A near the stage and Zone B behind it. |
| Zone map | The plan of the venue with its zones, tables and table types, drawn on an uploaded image of the venue and shown to the Customer as the real-time map of a concert round; the "floor plan" of ADR-02 and ADR-05. |

*Table 6.2 Technology and project terms*

| Term | Definition |
|---|---|
| Adapter | A module of a service, or of the API Gateway, that talks to one external system (LINE Login, LINE Messaging, the Payment Gateway, Media Storage), so that the business logic never depends on the provider's API (ports and adapters, Section 5). |
| API Gateway | The single public entry of the Backend: it authenticates the caller, checks its role and routes the request to the service that owns the operation (ADR-07, ADR-12). |
| Bounded context | A part of the domain with its own model and vocabulary; each service owns one (Section 5.1). |
| gRPC | Remote procedure calls over HTTP/2 with Protocol Buffers messages; the way the services call each other (ADR-12). |
| Hosted checkout | The payment page of the Payment Gateway, opened inside the web app, where the Customer chooses a payment method and pays; no card data passes through the system (FR-71). |
| ID token | The signed token that LINE Login gives the web app; the API Gateway verifies it and reads the LINE user id from it (FR-01, NFR-36). |
| Idempotent | Said of an operation that can be repeated without changing the result, so that a retry is safe: releaseHold(), publishRound() and confirmBookingPayment() are idempotent (ADR-08, NFR-22). |
| Increment | A planned build of the system: the MVP first, then Increment 2 (Section 1.3). |
| LIFF | LINE Front-end Framework: the customer web app runs as a LIFF app inside LINE's in-app browser (ADR-01). |
| LINE Login | LINE's sign-in (OpenID Connect); the Customer's identity is the LINE user id it returns (BRULE-12). |
| LINE Messaging API | The API through which the Notification Service pushes messages to the Customer (ADR-10). |
| MongoDB | The document database of every service (ADR-06); a zone map or a round is stored as one document. |
| MVP | The first increment: the smallest system that runs the four business use cases end to end (Section 1.3). |
| node-cron | The scheduler in the Booking Service that runs the hold-expiry job every 5 seconds (ADR-03, ADR-08). |
| Polling | The web app asks the API Gateway for the table status every 2 seconds (ADR-09); the answer carries a version, so an unchanged map costs one small response. |
| Protocol Buffers | The typed message format of gRPC; the .proto file of a service is the contract of its gRPC API. |
| REST | HTTP requests with JSON bodies; the way the web apps call the API Gateway, the gateway calls the services, and the Payment Gateway sends its webhook (ADR-12). |
| Rich Menu | The menu of the LINE Official Account from which the Customer opens the web app. |
| Session token | The token that the Staff Account Service issues at sign-in and that the API Gateway checks on every back-office request (ADR-07). |
| Webhook | A call that an external system makes to the API Gateway when something happens; the Payment Gateway reports every payment result by a signed webhook (NFR-38). |
| WebSocket | A persistent connection over which the server pushes table status changes to the open maps; Increment 2 (ADR-09). |
