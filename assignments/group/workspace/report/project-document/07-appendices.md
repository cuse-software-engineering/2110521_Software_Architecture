# Appendix A Use Case Traceability

## A.1 Operations by Use Case

Table A.1 traces the ten use cases to the operations of Table 5.3: a cell names the steps and flows of the use case that the operation serves, whether the actor invokes it through the API Gateway or another service invokes it as a collaborator; for UC-05 to UC-08, which have no description, a tick marks the operations they use. Every operation has at least one cell, and the two jobs on a timer are listed below the operations. Section A.2 gives the same trace step by step, with who invokes each operation, the collaborations it needs, the data it stores and the requirements it realises; only the flows that the MVP builds are traced (Section 1.3).

<div class="matrix" markdown="1">

*Table A.1 Operations by use case*

| Service | Operation | UC-01 | UC-02 | UC-03 | UC-04 | UC-05 | UC-06 | UC-07 | UC-08 | UC-09 | UC-10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Concert Round Service** | createZoneMap() |  |  |  | 1–2 |  |  |  |  |  |  |
|  | updateZoneMap() |  |  |  | 4; 5–6; AF-1; AF-3 |  |  |  |  |  |  |
|  | uploadZoneMapImage() |  |  |  | 3, EF-3 |  |  |  |  |  |  |
|  | defineTableType() |  |  |  | 5–6 |  |  |  |  |  |  |
|  | listTableTypes() |  |  |  | 5–6 |  |  |  |  |  |  |
|  | listZoneMaps() |  |  | 6 | AF-1 |  |  |  |  |  |  |
|  | getZoneMap() |  |  | 7 | 7; 10; AF-1 |  |  |  |  |  |  |
|  | validateZoneMap() |  |  |  | 8–9, S-1, EF-1 |  |  |  |  |  |  |
|  | activateZoneMap() |  |  |  | 11–12, EF-2 |  |  |  |  |  |  |
|  | getBusinessParameters() |  |  | 3–5 |  |  |  | ✓ |  |  |  |
|  | updateBusinessParameters() |  |  |  |  |  |  | ✓ |  |  |  |
|  | createRound() |  |  | 1–2 |  |  |  |  |  |  |  |
|  | updateRound() |  |  | 3–5; 8; 9–10; AF-1; AF-3 |  |  |  |  |  |  |  |
|  | validateRound() |  |  | 11–12, S-1, EF-1 |  |  |  |  |  |  |  |
|  | publishRound() |  |  | 14–15, EF-2 |  |  |  |  |  |  |  |
|  | getUpcomingRounds() | 3, AF-2 |  |  |  |  |  |  |  |  |  |
|  | getRound() | 4, AF-1; 6–8, AF-3 |  | 13; AF-3 |  |  |  |  |  |  |  |
|  | getRoundTables() | 5, AF-2 |  | 13 |  |  |  |  |  |  |  |
|  | getRoundPricing() | 10–11 |  |  |  |  |  |  |  |  |  |
|  | getCheckInWindow() | 13 | 2–4, S-1, AF-2, AF-3, AF-5, EF-1, EF-2 |  |  |  |  |  |  |  |  |
| **Table Availability Service** | createRoundTableStatus() |  |  | 14–15, EF-2 |  |  |  |  |  |  |  |
|  | getRoundTableStatus() | 5, AF-2 | 7 | AF-3 | AF-1 | ✓ |  |  |  |  |  |
|  | countAvailableTables() | 3, AF-2 |  |  |  |  |  |  |  |  |  |
|  | holdTable() | 6–8, AF-3 |  |  |  |  |  |  |  |  |  |
|  | releaseHold() | AF-4, AF-5; EF-1 |  |  |  |  |  |  |  |  |  |
|  | markTableBooked() | 16–17 |  |  |  |  |  |  |  |  |  |
|  | markTableOccupied() |  | 6, EF-5 |  |  |  |  |  |  |  |  |
| **Booking Service** | createHeldBooking() | 6–8, AF-3 |  |  |  |  |  |  |  |  |  |
|  | getBooking() | 9; 18 |  |  |  |  |  |  |  |  |  |
|  | setPartySize() | 10–11 |  |  |  |  |  |  |  |  |  |
|  | getCustomerProfile() |  |  |  |  |  |  |  |  | 1–2; 6–7, AF-2, EF-1 |  |
|  | createCustomerProfile() |  |  |  |  |  |  |  |  | 3–5, AF-1, AF-2, EF-1 |  |
|  | updateCustomerProfile() |  |  |  |  |  |  |  |  | 6–7, AF-2, EF-1 |  |
|  | getBookingTerms() | 13 |  |  |  |  |  |  |  |  |  |
|  | acceptBookingTerms() | 14 |  |  |  |  |  |  |  |  |  |
|  | startPayment() |  |  |  |  |  |  |  |  |  | 1–2 |
|  | confirmBookingPayment() | 16–17 |  |  |  |  |  |  |  |  | 5–6, AF-1 |
|  | getETicket() | 18 |  |  |  |  | ✓ |  |  |  |  |
|  | getCustomerBookings() |  |  |  |  |  | ✓ |  |  |  |  |
|  | cancelBooking() | AF-4, AF-5 |  |  |  |  |  |  |  |  |  |
|  | verifyBookingReference() |  | 2–4, S-1, AF-2, AF-3, AF-5, EF-1, EF-2 |  |  |  |  |  |  |  |  |
|  | checkInBooking() |  | 6, EF-5 |  |  |  |  |  |  |  |  |
|  | getRoundBookings() |  | 7 |  |  | ✓ |  |  |  |  |  |
| **Payment Service** | createPaymentRequest() |  |  |  |  |  |  |  |  |  | 1–2; 2 |
|  | receivePaymentResult() |  |  |  |  |  |  |  |  |  | 5–6, AF-1 |
|  | getPaymentStatus() |  |  |  |  |  |  |  |  |  | AF-1 |
| **Notification Service** | sendBookingConfirmation() | 19, S-1 |  |  |  |  |  |  |  |  |  |
|  | sendHoldExpiredNotice() | EF-1; EF-1, S-1 |  |  |  |  |  |  |  |  |  |
|  | sendPaymentFailedNotice() |  |  |  |  |  |  |  |  |  | 5–6, AF-1; AF-1 |
| **Staff Account Service** | signIn() |  |  |  |  |  |  |  | ✓ |  |  |
|  | signOut() |  |  |  |  |  |  |  | ✓ |  |  |
|  | createStaffAccount() |  |  |  |  |  |  |  | ✓ |  |  |
|  | listStaffAccounts() |  |  |  |  |  |  |  | ✓ |  |  |
|  | updateStaffAccount() |  |  |  |  |  |  |  | ✓ |  |  |
|  | disableStaffAccount() |  |  |  |  |  |  |  | ✓ |  |  |
| *Jobs on a timer (not operations)* | hold-expiry job of the Booking Service | EF-1 | | | | | | | | | EF-4 |
| | retry job of the Notification Service | EF-3 | | | | | | | | | |

</div>

## A.2 Step by Step

Tables A.2 to A.8 are the evidence behind Table A.1: each row follows one step, or the consecutive steps served by one operation, of a use case: who invokes the operation (an actor, through the API Gateway, or a service), the service and operation that carry the step out, the collaborations the operation needs, the data it stores, and the requirements it realises. Steps in which the actor acts without the system, such as UC-02 step 5, are left out unless a rule applies to them. Only the flows that the MVP builds are listed (Section 1.3), and Table A.8 covers UC-05 to UC-08, which have no description. Every operation of Table 5.3 appears in at least one row, the two jobs appear as jobs, and every MVP requirement of Section 3.1 is realised by at least one row.

<div class="trace" markdown="1">

*Table A.2 Traceability of Reserve a Specific Table*

| Steps | Invoked by | Operation | Collaborations | Data stored | Requirements |
|---|---|---|---|---|---|
| 1–2, EF-2 | **Customer** | API Gateway: check the LINE ID token that LINE Login gave the LIFF app | LINE Login Adapter, which asks the **LINE Platform** | — | FR-01, FR-02 |
| 3, AF-2 | **Customer** | Concert Round Service: getUpcomingRounds(), with the status of each round | Table Availability Service: countAvailableTables(), for the sold-out status | — | FR-03 |
| 4, AF-1 | **Customer** | Concert Round Service: getRound() | — | — | FR-03, FR-04 |
| 5, AF-2 | **Customer** | Concert Round Service: getRoundTables()<br>Table Availability Service: getRoundTableStatus(), polled every 2 seconds | — | — | FR-05, FR-06 |
| 6–8, AF-3 | **Customer** | Booking Service: createHeldBooking() | Concert Round Service: getRound(), to check that booking is open<br>Table Availability Service: holdTable() | Booking DB: booking Held until the end of the **hold** (one active booking per table per round, ADR-13)<br>Table Status DB: table held | FR-04, FR-07, FR-08 |
| 9 | **Customer** | Booking Service: getBooking(), the booking summary and the remaining **hold** time | — | — | FR-07 |
| 10–11 | **Customer** | Booking Service: setPartySize(), which computes the **full table fee** | Concert Round Service: getRoundPricing() | Booking DB: **party size** and **full table fee** | FR-09 |
| 12 | **Customer** | Included use case UC-09 Maintain Customer Profile (Table A.6) | — | — | FR-10 |
| 13 | **Customer** | Booking Service: getBookingTerms() | Concert Round Service: getCheckInWindow() | — | FR-12 |
| 14 | **Customer** | Booking Service: acceptBookingTerms() | — | Booking DB: **booking terms** accepted | FR-12 |
| 15 | **Customer** | Included use case UC-10 Pay the Full Table Fee (Table A.7) | — | — | FR-13 |
| 16–17 | Payment Service, at UC-10 step 6 | Booking Service: confirmBookingPayment(), which also issues the **e-ticket** | Table Availability Service: markTableBooked() | Booking DB: payment recorded, booking Confirmed, **e-ticket** with the signed **booking reference**<br>Table Status DB: table booked | FR-16, FR-19 |
| 18 | **Customer** | Booking Service: getBooking(), getETicket() | — | — | FR-19 |
| 19, S-1 | Booking Service | Notification Service: sendBookingConfirmation() | LINE Messaging Adapter: pushLineMessage() | Notification DB: message and delivery result | FR-20 |
| AF-4, AF-5 | **Customer** | Booking Service: cancelBooking() | Table Availability Service: releaseHold() | Booking DB: booking Cancelled<br>Table Status DB: table available | FR-10, FR-11 |
| EF-1 | Time | Booking Service: the hold-expiry job, every 5 seconds (ADR-08); not an operation | Table Availability Service: releaseHold()<br>Notification Service: sendHoldExpiredNotice() | Booking DB: booking Expired<br>Table Status DB: table available | FR-21, FR-23 |
| EF-1, S-1 | Booking Service | Notification Service: sendHoldExpiredNotice() | LINE Messaging Adapter: pushLineMessage() | Notification DB: message and delivery result | FR-21 |
| EF-3 | Time | Notification Service: the retry job, 3 times within 5 minutes; not an operation | LINE Messaging Adapter: pushLineMessage() | Notification DB: delivery result | FR-22 |

*Table A.3 Traceability of Check In with E-Ticket*

| Steps | Invoked by | Operation | Collaborations | Data stored | Requirements |
|---|---|---|---|---|---|
| 2–4, S-1, AF-2, AF-3, AF-5, EF-1, EF-2 | **Front Staff** | Booking Service: verifyBookingReference(), with the **booking reference** scanned (step 2) or typed (AF-2); its answer is the result of step 4 or the reason of AF-3, AF-5, EF-1 and EF-2 | Concert Round Service: getCheckInWindow() | — (verification changes nothing) | FR-24, FR-25, FR-26, FR-27 |
| 6, EF-5 | **Front Staff** | Booking Service: checkInBooking(); a retry finds the existing check-in and does not repeat it (EF-5) | Table Availability Service: markTableOccupied() | Booking DB: booking Checked-in with the time and the staff account<br>Table Status DB: table occupied | FR-28 |
| 7 | **Manager** | Booking Service: getRoundBookings()<br>Table Availability Service: getRoundTableStatus(), polled every 2 seconds | — | — | FR-06, FR-42 |
| AF-4 | **Front Staff** | No operation of SEATS: extra guests are handled by hand (BRULE-09) | — | — | — |

*Table A.4 Traceability of Create Concert Round*

| Steps | Invoked by | Operation | Collaborations | Data stored | Requirements |
|---|---|---|---|---|---|
| 1–2 | **Manager** | Concert Round Service: createRound() | — | Round DB: a new round, Draft | FR-34 |
| 3–5 | **Manager** | Concert Round Service: updateRound(), with the concert details, the times and the **booking-open time**; it derives the **check-in window** from getBusinessParameters() | — | Round DB: schedule, **booking-open time**, **check-in window** | FR-34, FR-38 |
| 6 | **Manager** | Concert Round Service: listZoneMaps(), the Active maps | — | — | FR-35 |
| 7 | **Manager** | Concert Round Service: getZoneMap() | — | — | FR-35 |
| 8 | **Manager** | Concert Round Service: updateRound(), with the **zone map** and the tables not for sale | — | Round DB: the round's **zone map** and tables for sale | FR-35 |
| 9–10 | **Manager** | Concert Round Service: updateRound(), with the **package price** and content of each **table type** in each **zone**; it answers with the tables for sale and the capacity of each **zone** | — | Round DB: **package prices** | FR-37 |
| 11–12, S-1, EF-1 | **Manager** | Concert Round Service: validateRound() | — | — | FR-75 |
| 13 | **Manager** | Concert Round Service: getRound(), getRoundTables(), the round as the **Customer** will see it | — | — | — |
| 14–15, EF-2 | **Manager** | Concert Round Service: publishRound(); a retry finds the published round and does not create a second one (EF-2) | Table Availability Service: createRoundTableStatus() | Round DB: round Published<br>Table Status DB: every table for sale available | FR-34, FR-75 |
| AF-1 | **Manager** | Concert Round Service: updateRound(); the round stays Draft | — | Round DB: the round as entered | FR-34 |
| AF-3 | **Manager** | Concert Round Service: getRound(), then updateRound(), which allows a Published round only the changes of AF-3 (BRULE-07) | Table Availability Service: getRoundTableStatus(), whose booked tables are the Confirmed bookings | Round DB: the changed fields | FR-34, FR-35 |

*Table A.5 Traceability of Create Venue Zone Map*

| Steps | Invoked by | Operation | Collaborations | Data stored | Requirements |
|---|---|---|---|---|---|
| 1–2 | **Manager** | Concert Round Service: createZoneMap() | — | Round DB: a new **zone map**, Draft | FR-37 |
| 3, EF-3 | **Manager** | Concert Round Service: uploadZoneMapImage() | Media Storage Adapter: storeZoneMapImage() | Cloud Object Storage: image of the venue<br>Round DB: its address | FR-39 |
| 4 | **Manager** | Concert Round Service: updateZoneMap(), with the **zones** drawn and named | — | Round DB: **zones** | FR-37 |
| 5–6 | **Manager** | Concert Round Service: listTableTypes() to choose a **table type**; updateZoneMap(), with each table's position, number, **table type** and capacity; defineTableType() for a **table type** the venue does not have yet | — | Round DB: tables and **table types** | FR-37, FR-39 |
| 7 | **Manager** | Concert Round Service: getZoneMap(), with the number of tables and the capacity of each **zone** | — | — | FR-37 |
| 8–9, S-1, EF-1 | **Manager** | Concert Round Service: validateZoneMap() | — | — | FR-74 |
| 10 | **Manager** | Concert Round Service: getZoneMap(), the preview | — | — | — |
| 11–12, EF-2 | **Manager** | Concert Round Service: activateZoneMap(); a retry finds the Active map and does not create a second one (EF-2) | — | Round DB: **zone map** Active | FR-74 |
| AF-1 | **Manager** | Concert Round Service: listZoneMaps(), getZoneMap(), then updateZoneMap(), which allows only the changes of AF-1 | Table Availability Service: getRoundTableStatus(), for the Published rounds that use the map | Round DB: the changed **zones** and tables | FR-37 |
| AF-3 | **Manager** | Concert Round Service: updateZoneMap(); the map stays Draft | — | Round DB: the map as entered | FR-37 |

*Table A.6 Traceability of Maintain Customer Profile*

| Steps | Invoked by | Operation | Collaborations | Data stored | Requirements |
|---|---|---|---|---|---|
| 1–2 | **Customer** | Booking Service: getCustomerProfile(), which tells whether a profile exists | — | — | FR-10 |
| 3–5, AF-1, AF-2, EF-1 | **Customer** | Booking Service: createCustomerProfile(), with the consent, the name and the phone; AF-2 is its validation; AF-1 stores nothing | — | Booking DB: **customer profile** and consent | FR-10 |
| 6–7, AF-2, EF-1 | **Customer** | Booking Service: getCustomerProfile(), then updateCustomerProfile() when the **Customer** corrects the profile | — | Booking DB: **customer profile** | FR-10 |

*Table A.7 Traceability of Pay the Full Table Fee*

| Steps | Invoked by | Operation | Collaborations | Data stored | Requirements |
|---|---|---|---|---|---|
| 1–2 | **Customer** | Booking Service: startPayment() | Payment Service: createPaymentRequest() | Booking DB: payment started | FR-13 |
| 2 | Booking Service | Payment Service: createPaymentRequest() | Payment Gateway Adapter: createCheckoutSession() | Payment DB: payment request | FR-13 |
| 3–4 | **Customer** | No operation of SEATS: the **Customer** pays in the hosted checkout of the **Payment Gateway**, simulated in the MVP (ADR-11) | — | — | FR-13 |
| 5–6, AF-1 | **Payment Gateway** | Payment Service: receivePaymentResult(), the signed webhook routed by the API Gateway; a duplicate result is ignored | Payment Gateway Adapter: verifyWebhookSignature()<br>Booking Service: confirmBookingPayment(), when paid (UC-01 step 16)<br>Notification Service: sendPaymentFailedNotice(), when declined | Payment DB: payment result, processed once | FR-14, FR-16, FR-21 |
| AF-1 | **Customer** | Payment Service: getPaymentStatus(), the decline and the remaining **hold** time | — | — | FR-14 |
| AF-1 | Payment Service | Notification Service: sendPaymentFailedNotice() | LINE Messaging Adapter: pushLineMessage() | Notification DB: message and delivery result | FR-21 |
| EF-4 | Time, through UC-01 EF-1 | The hold-expiry job of the Booking Service; not an operation | — | — | FR-23 |

*Table A.8 Traceability of UC-05 to UC-08, the use cases without a description*

| Use case | Invoked by | Operation | Collaborations | Data stored | Requirements |
|---|---|---|---|---|---|
| UC-07 | **Manager** | Concert Round Service: getBusinessParameters(), updateBusinessParameters() | — | Round DB: the **business parameters**; a round uses the values in force at its **booking-open time** | FR-38 |
| UC-06 | **Customer** | Booking Service: getCustomerBookings(), getETicket() | — | — | FR-40 |
| UC-05 | **Manager**, **Owner** | Booking Service: getRoundBookings()<br>Table Availability Service: getRoundTableStatus() | — | — | FR-42 |
| UC-08 | **Manager** | Staff Account Service: createStaffAccount(), listStaffAccounts(), updateStaffAccount() for the role, disableStaffAccount() | — | Staff Account DB: accounts, roles and password hashes | FR-65 |
| UC-08 | **Front Staff**, **Manager**, **Owner** | Staff Account Service: signIn(); the API Gateway checks the role of every request | — | — | FR-65, FR-66 |
| UC-08 | All users | Staff Account Service: signOut(); a **Customer** logs out of LINE Login in the web app | — | — | FR-73 |

</div>

# Appendix B Business Rules

The business rules that the use cases (Section 2), the requirements (Section 3) and the domain model (Section 6.1) refer to. Each rule is a policy of the venue, not a design decision; the design realises it (for example BRULE-03 in ADR-08).


*Table B.1 Business rules*

| ID | Rule |
|---|---|
| BRULE-01 | Full fee confirms: a booking is confirmed only once the **full table fee**, the **package price** plus any **extra-person fees**, has been received and verified; there is no deposit and no balance to pay at the venue. While a **transfer slip** awaits the **Manager**'s decision in **degraded mode**, the **hold** does not expire. |
| BRULE-02 | 15-minute **hold**: selecting a table gives a **hold** of 15 minutes from the moment of selection. If no payment is confirmed within the **hold**, it expires, the table returns to available and the customer is notified; an expired hold costs the customer nothing. |
| BRULE-03 | First hold wins: when several customers try to take the same table for the same round, the first successful hold wins; the later customer is told that the table was just taken and sees a refreshed map. A second hold on a held or confirmed table is never granted. |
| BRULE-04 | Check-in window: the **check-in window** opens 2 hours before the concert start time; before that time an **e-ticket** cannot be checked in. |
| BRULE-05 | Grace period: a customer who arrives late is still given the booked table up to 30 minutes after the concert start. |
| BRULE-06 | **No-show**: when the **grace period** ends without a check-in, the booking is marked **No-show** and the table is shown as free; the fee is not refunded. The table is resold by hand to **walk-in** guests, who pay at the venue outside the system, and it is never offered to a **waitlist**. |
| BRULE-07 | Booking-open time: the tables of a round can be selected only from the **booking-open time** set by the **Manager**; before it the round is visible but not bookable. The **zone map**, the table numbers and the prices are complete before booking opens and do not change during the round. |
| BRULE-08 | Package pricing: the price of a table is the **package price** of its **table type** in its **zone**, for example 2,400 THB for a 2-person round table, 4,800 THB for a 4-person square table and 7,200 THB for a 6-person sofa in Zone A. The **Manager** maintains the prices and the **package** contents per round. |
| BRULE-09 | Extra-person fee: each person above the capacity of the **table type** costs 600 THB, added to the table fee before payment. Extra guests at the door are handled by hand, outside the system. |
| BRULE-11 | Personal data: name, phone, LINE user id and booking and payment history are collected once into a **customer profile**, for booking, payment, check-in and contact about the booking. The purpose is shown and consent obtained before the first booking; the customer can view and correct the profile; the data is deleted or anonymised after the retention period. |
| BRULE-12 | Identity: one LINE account is one customer. LINE Login is the customer's identity; there is no separate registration, and bookings and **e-tickets** are always tied to a LINE account. |
| BRULE-16 | Terms before paying: before paying, the customer is shown and must accept the **booking terms** (full payment confirms the booking, the **check-in window**, the **grace period**, no refund for a **no-show**); the same terms are repeated in the confirmation message. |
| BRULE-17 | Late payment: if a successful payment result arrives after the **hold** expired, the booking is confirmed anyway when the table is still available; if the table was taken meanwhile, the payment is refunded automatically through the gateway and the customer is told by LINE. |

# Appendix C Glossary

Table C.1 lists the business terms of this document: the words of the venue, its customers and its rules. In the text they are set in bold, and in the PDF each bold term links to its entry. Table C.2 lists the technology and project terms that the ADRs and the microservice design use; they are not set in bold in the text.

*Table C.1 Business terms*

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

*Table C.2 Technology and project terms*

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
