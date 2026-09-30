# 6 Domain Model and API Specification

This chapter is the bridge between the business and the code. It states the domain model that every part of the document shares (6.1), the slice of it that each service owns in its own database (6.2), the rule by which a model becomes a contract (6.3), and the contracts themselves: the REST routes and the gRPC methods of every service of the MVP (6.4). Deliverable #3 demonstrates these contracts: REST with create, read, update and delete on the Concert Round Service, and gRPC with the same four on the Table Availability Service.

## 6.1 Domain Model

The domain model is the conceptual model of the concert-table business: the things that exist in the domain, their attributes, how they relate, and the rules that constrain them. It is the shared vocabulary behind the use cases (Section 2), the requirements (Section 3), the glossary (Appendix C) and the services of Section 5: every entity is a glossary term, every invariant is a business rule of Appendix B, and the booking lifecycle supplies the alternative and exception flows of UC-01 and UC-02. Actors (**Customer**, **Manager**, **Front Staff**, **Owner**) are not entities; the **Customer** entity is the **customer profile** that a LINE account owns. The model is drawn without instance data: the current **zones**, **table types**, **package prices** and the **extra-person fee** are maintained by the **Manager** and stated as BRULE-08 and BRULE-09, not as values on the diagram.

![SEATS domain model](assets/domain-model.png)

*Figure 6.1 Domain model of SEATS (UML class diagram); WaitlistEntry and BookingTransfer belong to a later release*

*Table 6.1 Business entities*

| Entity | Definition | Key attributes | Glossary term |
|---|---|---|---|
| ConcertRound | One concert night at the venue, for which tables are sold in advance | name, date, doors-open time, start time, **booking-open time**, status (Draft, Published; then not yet open, open, sold out, finished, cancelled as seen by the **Customer**) | **concert round** |
| Artist | The performer of a concert night | name | — |
| ZoneMap | The plan of the venue; one map serves many rounds, and the map of a round is fixed once its booking opens (BRULE-07) | name, image of the venue | **zone map** |
| Zone | A pricing area of the **zone map**, defined by the **Manager** per map | name | **zone** |
| Table | A physical, numbered table inside a **zone** | number, capacity, position on the image | table |
| TableType | The kind of table with its **package**, defined by the **Manager**; the same type may have a different price in each **zone** | name, capacity, package content | **table type**, **package** |
| PackagePrice | The **package price** of one **table type** in one **zone** for one round (BRULE-08) | price, package content | **package price** |
| BusinessParameters | The venue's settings; a round uses the values in force at its **booking-open time** (FR-38) | **hold period**, **check-in window**, **grace period**, **extra-person fee** | **business parameters** |
| Customer | A person identified by a LINE account who reserves tables (BRULE-12) | LINE user id, name, phone, consent given at | **Customer**, **customer profile** |
| Booking | The reservation of one table for one round by one customer; the central record of the system | status (BookingStatus, Figure 6.2), **party size**, created at, **hold** expires at, confirmed at | booking, **hold** |
| Payment | The payment of the **full table fee** for a booking through the **Payment Gateway** | amount, method, gateway reference, paid at, status | **full table fee** |
| ETicket | The proof of a Confirmed booking, presented as a QR code at the door | **booking reference** (signed), QR code, issued at, valid for (round, table) | **e-ticket** |
| CheckIn | The event of admitting the **Customer** at the door | checked-in at, by staff, guests present | check-in |
| WaitlistEntry | A **Customer**'s request to be offered a table of a full round; later release | position, created at | **waitlist** |
| BookingTransfer | The official reassignment of a Confirmed booking to another **Customer**; later release | transferred at, to customer | — |

The invariants of the model are the business rules of Appendix B: a table has at most one active booking (Held, Confirmed or Checked-in) per round (BRULE-03, **first lock wins**); a booking is Confirmed only after the **full table fee** is verified (BRULE-01); a Held booking expires after the **hold period** (BRULE-02); check-in is accepted within the **check-in window** and the **grace period**, after which the booking is a **no-show** (BRULE-04, BRULE-05, BRULE-06); the **zone map** of a round does not change once booking is open (BRULE-07); and a customer is identified by exactly one LINE account (BRULE-12).

![Booking state machine](assets/booking-states.png)

*Figure 6.2 Lifecycle of a booking (UML state machine); Transferred belongs to a later release*

*Table 6.2 Booking states*

| State | Entered when | Leaves when |
|---|---|---|
| Held | the **Customer** selects a free table (UC-01 step 7) | the payment is verified (UC-10 step 6), or the **Manager** confirms the **transfer slip** in **degraded mode** (UC-10 EF-2, Increment 2) → Confirmed; the **hold period** ends with no payment verified → Expired (EF-1); the **Customer** cancels or the profile is not completed → Cancelled (AF-4, AF-5) |
| Confirmed | the payment result is verified and the **e-ticket** issued (UC-01 steps 16–17) | the **e-ticket** is scanned within the **check-in window** → Checked-in (UC-02); the **grace period** passes → **No-show** (UC-02 EF-4, Increment 2); the **Manager** cancels as an exception → Cancelled |
| Checked-in | **Front Staff** confirms the entry (UC-02 step 6) | final |
| Expired | the **hold** ends with no payment verified; the table is released and the **Customer** notified (UC-01 EF-1) | a successful payment result arrives late while the table is still available → Confirmed (UC-10 EF-1, BRULE-17, Increment 2); otherwise final |
| No-show | the **grace period** ends without a check-in; the table is shown as free, the fee is forfeited (BRULE-06) | final |
| Cancelled | the **Customer** cancels during the **hold**, or the **Manager** cancels as an exception | final |
| Transferred | later release: the booking is reassigned and its **e-ticket** invalidated | final |

## 6.2 Data Model per Service

Each service owns one database and one slice of the domain model (ADR-06, Table 5.1); a service never reads another service's database, so a `roundId` in the Booking DB is a reference by identifier, not a foreign key, and what a service needs from another it asks by gRPC. Figures 6.3 to 6.5 give the slices of the three services of the MVP demo; the Payment, Notification and Staff Account databases are drawn when those services are built.

![Round DB](assets/data-model-round.png)

*Figure 6.3 Round DB of the Concert Round Service*

A **zone map** is one document with its **zones** and tables embedded; a round embeds its **package prices**, its **check-in window** and the snapshot of the **business parameters** in force when it was published (FR-38). The tables of a round are the tables of its map minus those not for sale.

![Table Status DB](assets/data-model-table-status.png)

*Figure 6.4 Table Status DB of the Table Availability Service*

One document per round with its tables embedded: the read model of the table map (ADR-13). Its version grows on every change and is the ETag of the polled read (ADR-09).

![Booking DB](assets/data-model-booking.png)

*Figure 6.5 Booking DB of the Booking Service*

The booking is the source of truth of a table's occupation: at most one active booking (Held, Confirmed, Checked-in) exists per table per round, enforced by a unique index (ADR-13, BRULE-03), and every state change is appended to the booking's history. The booking copies zone, **table type** and capacity from the round when the table is held, so that the fee and the ticket do not change if the map is edited later (BRULE-07).

## 6.3 From Model to Contract

The types of the code, the gRPC messages and the routes of the API Gateway are all derived from the model, in that order, and a change is made in that order too:

*Table 6.3 From the domain model to the contracts*

| Step | Artifact | What it holds | Example: the booking |
|---|---|---|---|
| 1 | Domain model (6.1) | The business entity, its attributes and its rules | Booking: status, **party size**, **hold** end; one active booking per table per round (BRULE-03) |
| 2 | Data model of the owning service (6.2) | The entity as stored, with the copies and references the service needs | Booking DB: `zoneId`, `tableTypeId` and `capacity` copied from the round; `history` of state changes; unique index on (`roundId`, `tableNumber`, active) |
| 3 | Type in the service (`model.ts`) | The stored shape, used by the operations and the store | `Booking`, `BookingStatus`, `Fee`, `CustomerProfile` |
| 4 | gRPC message (`.proto`) | Only what a caller needs, the API Gateway or another service: a projection of the model, never the stored document | `Booking` carries the fee and the remaining hold seconds; `HoldTableRequest` carries only `round_id`, `table_number`, `booking_id`, `hold_ends_at`, nothing of the customer |
| 5 | Route of the API Gateway (6.4) | The method and path the web app calls, mapped one to one onto a gRPC method: the JSON body is the request message and the JSON answer the response message | `POST /bookings {roundId, tableNumber}` is CreateHeldBooking and answers the booking with `remainingHoldSeconds`; the unique index and the store stay inside the service |

Two consequences of the rule shape the design. First, a gRPC message is owned by the service that serves it: `concert_round.proto`, `table_availability.proto` and `booking.proto` are the contracts of the three services, and a change to a message is a compile error in every caller, the API Gateway included. Second, the table map is a read model and not a second truth: the Booking Service decides who holds a table, and the Table Availability Service keeps the projection that the web apps poll (ADR-13). The projection is created from the round when it is published (createRoundTableStatus()), because which tables exist and which are not for sale come from the round, not from any booking; from then on every booking transition updates it, by a gRPC call in the MVP and by an event on the message broker from Increment 2.

## 6.4 API Specification per Service

The API Gateway is the only REST API of the system (ADR-12). Each route of Tables 6.4 to 6.7 is one gRPC method of the owning service: the gateway checks the caller's role (the roles of Table 5.2, FR-66), turns the path parameters, the query and the JSON body into the request message, passes the caller's identity and role as the gRPC metadata `x-user-id` and `x-role`, and answers with the response message as JSON. A service's API is the service of its `.proto` file, and a service is never called by REST. An error is a gRPC status with a message and, where useful, details, which the gateway maps to an HTTP status and a JSON body `{error, details?}`: INVALID_ARGUMENT to 400 (invalid input), UNAUTHENTICATED to 401 (no identity), PERMISSION_DENIED to 403 (role), NOT_FOUND to 404, FAILED_PRECONDITION to 409 (a rule refuses the change, for example the table was just taken), UNIMPLEMENTED to 501 (not built in this increment) and UNAVAILABLE to 502 (the service or one of its collaborators is down). A dash in the route column marks a method that only another service calls.

<div class="api" markdown="1">

*Table 6.4 Concert Round Service, gRPC (port 5001) and its routes at the API Gateway*

| Operation | gRPC method | Route at the API Gateway | Request and response |
|---|---|---|---|
| createZoneMap() | CreateZoneMap | `POST /zone-maps` | `{name}` → ZoneMap (Draft) |
| listZoneMaps() | ListZoneMaps | `GET /zone-maps?status=` | → [ZoneMap summary] |
| getZoneMap() | GetZoneMap | `GET /zone-maps/{id}` | → ZoneMap with the tables and capacity per **zone** |
| updateZoneMap() | UpdateZoneMap | `PUT /zone-maps/{id}` | `{name?, zones?, tables?}` → ZoneMap; a field left out is unchanged; on an Active map only the changes of UC-04 AF-1 |
| uploadZoneMapImage() | UploadZoneMapImage | `POST /zone-maps/{id}/image` | `{fileName}` → ZoneMap with `imageUrl` |
| validateZoneMap() | ValidateZoneMap | `POST /zone-maps/{id}/validate` | → `{valid, problems[]}` |
| activateZoneMap() | ActivateZoneMap | `POST /zone-maps/{id}/activate` | → ZoneMap (Active); 400 with the problems when not valid |
| discardDraftZoneMap() | DiscardDraftZoneMap | `DELETE /zone-maps/{id}` | → `{removed}`; 409 unless Draft |
| defineTableType(), listTableTypes() | DefineTableType, ListTableTypes | `PUT /table-types/{id}`, `GET /table-types` | `{name, capacity, packageContent}` → TableType; → [TableType] |
| getBusinessParameters(), updateBusinessParameters() | GetBusinessParameters, UpdateBusinessParameters | `GET`, `PUT /business-parameters` | BusinessParameters; every field of the update is optional |
| createRound() | CreateRound | `POST /rounds` | `{name?}` → Round (Draft) |
| getUpcomingRounds() | GetUpcomingRounds | `GET /rounds` | → [Round summary with status not yet open, open or sold out] |
| getRound(), getRoundTables() | GetRound, GetRoundTables | `GET /rounds/{id}`, `GET /rounds/{id}/tables` | → Round with its tables and `holdPeriodMinutes`; → [RoundTable with **zone**, **table type**, capacity, **package price**] |
| updateRound() | UpdateRound | `PUT /rounds/{id}` | Round fields → Round; a field left out is unchanged; a Published round accepts only the changes of UC-03 AF-3 |
| validateRound() | ValidateRound | `POST /rounds/{id}/validate` | → `{valid, problems[]}` |
| publishRound() | PublishRound | `POST /rounds/{id}/publish` | → Round (Published); calls CreateRoundTableStatus; idempotent |
| discardDraftRound() | DiscardDraftRound | `DELETE /rounds/{id}` | → `{removed}`; 409 unless Draft |
| getRoundPricing() | GetRoundPricing | — (the Booking Service) | `{round_id}` → `{prices[], extra_person_fee}` |
| getCheckInWindow() | GetCheckInWindow | — (the Booking Service) | `{round_id}` → `{opens_at, start_at, grace_ends_at}` |

*Table 6.5 Table Availability Service, gRPC (port 5003) and its route at the API Gateway*

| Operation | gRPC method | Route at the API Gateway | Request and response |
|---|---|---|---|
| createRoundTableStatus() | CreateRoundTableStatus | — (the Concert Round Service) | `{round_id, tables[{table_number, for_sale}]}` → RoundTableStatus; idempotent on retry |
| getRoundTableStatus() | GetRoundTableStatus | `GET /rounds/{id}/table-status` | `{round_id}` → RoundTableStatus `{round_id, version, tables[{table_number, status, booking_id, hold_ends_at}]}`; the gateway answers 304 to `If-None-Match: <version>` (ADR-09) |
| countAvailableTables() | CountAvailableTables | — (the Concert Round Service) | `{round_ids[]}` → `{counts[{round_id, available, for_sale}]}` |
| holdTable() | HoldTable | — (the Booking Service) | `{round_id, table_number, booking_id, hold_ends_at}` → TableStatus; AVAILABLE → HELD |
| releaseHold() | ReleaseHold | — (the Booking Service) | `{round_id, table_number, booking_id}` → TableStatus; HELD → AVAILABLE, a no-op when already AVAILABLE |
| markTableBooked(), markTableOccupied() | MarkTableBooked, MarkTableOccupied | — (the Booking Service) | `{round_id, table_number, booking_id}` → TableStatus; HELD → BOOKED, BOOKED → OCCUPIED |
| removeRoundTableStatus() | RemoveRoundTableStatus | — (the Concert Round Service) | `{round_id}` → `{removed}`; refused while a table is held or booked |

*Table 6.6 Booking Service, gRPC (port 5002) and its routes at the API Gateway*

| Operation | gRPC method | Route at the API Gateway | Request and response |
|---|---|---|---|
| createHeldBooking() | CreateHeldBooking | `POST /bookings` | `{roundId, tableNumber}` → Booking (Held) with `remainingHoldSeconds`; 409 when the table was just taken |
| getBooking() | GetBooking | `GET /bookings/{id}` | → Booking; own bookings only |
| setPartySize() | SetPartySize | `PUT /bookings/{id}/party-size` | `{partySize}` → Booking with `fee {packagePrice, extraPersons, extraPersonFee, fullTableFee}` |
| getCustomerProfile(), createCustomerProfile(), updateCustomerProfile() | GetCustomerProfile, CreateCustomerProfile, UpdateCustomerProfile | `GET`, `POST`, `PUT /customers/me` | `{name, phone, consent}` → CustomerProfile; 404 before the first booking |
| getBookingTerms(), acceptBookingTerms() | GetBookingTerms, AcceptBookingTerms | `GET /bookings/{id}/terms`, `POST /bookings/{id}/terms-acceptance` | → `{terms[], checkInWindow}`; → Booking with `termsAccepted` |
| startPayment() | StartPayment | `POST /bookings/{id}/payment` | → payment request of the Payment Service (Increment 1 answers 501) |
| cancelBooking() | CancelBooking | `POST /bookings/{id}/cancel` | → Booking (Cancelled) |
| getCustomerBookings(), getETicket() | GetCustomerBookings, GetETicket | `GET /customers/me/bookings`, `GET /bookings/{id}/e-ticket` | → [Booking]; → ETicket |
| verifyBookingReference(), checkInBooking() | VerifyBookingReference, CheckInBooking | `POST /check-ins/verify`, `POST /check-ins` | `{bookingReference}` → verification result; → Booking (Checked-in) |
| getRoundBookings() | GetRoundBookings | `GET /rounds/{id}/bookings` | → [Booking] for the **live view** |
| confirmBookingPayment() | ConfirmBookingPayment | — (the Payment Service) | `{booking_id, payment_id, amount}` → Booking (Confirmed) with its **e-ticket**; idempotent |

</div>

<div class="api5" markdown="1">

*Table 6.7 Payment, Notification and Staff Account Services (MVP contracts)*

| Service | Operation | gRPC method | Route at the API Gateway | Request and response |
|---|---|---|---|---|
| Payment (gRPC 5004) | createPaymentRequest() | CreatePaymentRequest | — (the Booking Service) | `{booking_id, amount, customer_id}` → `{payment_id, checkout_url}` |
| | receivePaymentResult() | ReceivePaymentResult | `POST /payments/webhook` | the signed result of the **Payment Gateway** → 200 once verified; a duplicate is ignored |
| | getPaymentStatus() | GetPaymentStatus | `GET /payments/{id}` | → `{paymentId, bookingId, status, amount}` |
| Notification (gRPC 5005) | sendBookingConfirmation(), sendHoldExpiredNotice(), sendPaymentFailedNotice() | SendBookingConfirmation, SendHoldExpiredNotice, SendPaymentFailedNotice | — (the Booking and Payment Services) | `{customer_id, booking_id, …}` → `{message_id, delivered}` |
| Staff Account (gRPC 5006) | signIn(), signOut() | SignIn, SignOut | `POST /sessions`, `DELETE /sessions/current` | `{username, password}` → `{token, role}` |
| | createStaffAccount(), listStaffAccounts(), updateStaffAccount(), disableStaffAccount() | CreateStaffAccount, ListStaffAccounts, UpdateStaffAccount, DisableStaffAccount | `POST`, `GET /staff-accounts`; `PUT`, `DELETE /staff-accounts/{id}` | `{username, role}` → StaffAccount |

</div>
