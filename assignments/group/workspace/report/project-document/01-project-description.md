# 1 Project Description

## 1.1 Problem Description

Pubs and bars still rely on manual chat messaging and phone calls to handle table reservations, leading to delayed staff responses, lost bookings, lack of real-time **zone map** visibility, and frequent allocation errors where customers do not get their requested tables. Currently, handling table inquiries and confirming seat statuses manually consumes substantial staff time and often leads to miscommunications during peak hours. The system should streamline table reservations through a web app accessed via LINE Messenger, providing a real-time interactive **zone map**, payment of the **full table fee** when booking, **e-tickets** for check-in, and one clear arrival rule: check-in opens 2 hours before the show, the table is kept until 30 minutes after the start, and a booking not checked in by then becomes a **no-show**.

## 1.2 Target Customer

- **Manager (venue manager):** Full access to the **back-office**: create the venue **zone map** (**zones**, tables, and **table types**), create and publish **concert rounds** with their prices, follow bookings and table occupancy on the **live view**, and rule on check-in **escalations**. The venue owner uses the same **back-office** with read-only access.
- **Front Staff (front of house):** Scan the QR codes of **e-tickets** for fast check-in, monitor real-time table statuses, and seat **walk-in** guests at the tables of **no-shows**, paid by hand at the venue.
- **Customer:** Browse interactive **zone maps**, reserve and pay for a specific table, receive the **e-ticket** by LINE, and check in via digital QR pass.

## 1.3 Scope and Increments

The system is built in increments, so that a first working version fits a build of two to three months. The use case descriptions in Section 2 still describe the complete behaviour; every flow that the MVP does not build is marked *(Increment 2)*, and the requirements and ADRs carry the same marks. The microservice design of Section 5 shows the MVP only.

| Increment | What is built | Use cases and flows |
|---|---|---|
| MVP | Create a venue **zone map** on an uploaded image of the venue: **zones**, tables, **table types** and capacities; validate and activate it. | UC-04 basic flow, AF-1, AF-3, EF-1, EF-2, EF-3 |
| MVP | Create, validate and publish a **concert round** with its prices and **booking-open time**, or save it as a draft. | UC-03 basic flow, AF-1, AF-3, EF-1, EF-2 |
| MVP | Reserve a table: LINE Login, rounds, **zone map** refreshed within 2 seconds, 15-minute **hold** (**first lock wins**) with automatic expiry, **party size** and fee, profile and consent, **booking terms**, **simulated payment** (success or decline), confirmation, QR **e-ticket** and LINE confirmation message. | UC-01 basic flow, AF-1 to AF-7, EF-1, EF-5, EF-6 |
| MVP | Check in with the QR code or the typed **booking reference**, verified against the **check-in window** and the **grace period**; used, unknown and out-of-window tickets are refused. | UC-02 basic flow, AF-2 to AF-5, EF-1, EF-2, EF-5 |
| Increment 2 | Real payment gateway (Beam Checkout in its sandbox, the gateway selected for the system) with status polling, automatic refund of a late payment, and **degraded mode** with transfer-slip review by the **Manager**. | UC-01 EF-2, EF-3, EF-4 |
| Increment 2 | Table status pushed to open maps by WebSocket instead of polling. | ADR-09 |
| Increment 2 | Escalation of invalid tickets to the **Manager**, look-up by name or phone, automatic **no-show** marking. | UC-02 AF-1, EF-3, EF-4 |
| Increment 2 | Copy a round or a **zone map**; withdraw a published round; handle a **zone map** changed during editing. | UC-03 AF-2, AF-4, EF-3; UC-04 AF-2 |
| Out of scope | Planned for a later release: reminders and the "on my way" grace extension, **waitlist**, booking transfer, reports and analytics, and seat-view photographs of the tables. | — |

The product is named Seating & Event Availability Tracking System (SEATS); Deliverables #1 and #2 called it Concert Table Reservation System (CTRS). Requirements are identified as FR-nn (functional) and NFR-nn (non-functional), and business rules as BRULE-nn (Section 3).
