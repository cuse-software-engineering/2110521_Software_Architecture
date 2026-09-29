# Known issues in the submitted deliverables

Inconsistencies found in [Deliverable-1.pdf](../../deliverables/report/Deliverable-1.pdf) (D1) and
[Deliverable-2.pdf](../../deliverables/report/Deliverable-2.pdf) (D2), recorded 2026-09-29. They are **not fixed**: the
submitted files stay as handed in for now. They are fixed in the project document, version 2.0 draft 1
(workspace/report/project-document/, Table 0.4 there); the Status column names the change that fixes each one. Page numbers are PDF pages. Teacher feedback that asks for changes is kept
separately in [../received/teacher/](../received/teacher/).

| ID | Issue | Where | Status |
|---|---|---|---|
| KI-01 | Use case names in the diagram differ from the descriptions | D1 p3; D1 p15, p19; D2 p2 | Resolved in doc 2.0 draft 1 (CH-04) |
| KI-02 | Actors in the diagram differ from the descriptions and the requirements | D1 p2, p3, p23, p25; D2 p7 | Resolved (CH-02, CH-04, CH-05, CH-11) |
| KI-03 | Two arrival models: cutoff with extensions, or check-in window with no-shows | D1 p2, p3, p13, p23–25, p28–29; D2 | Resolved: check-in window model kept (CH-02, CH-08, CH-11, CH-15) |
| KI-04 | Who asks for a postponement is stated two ways | D1 p2, p24, p29 | Resolved (CH-02) |
| KI-05 | The requirements leave out behaviour the use cases and D2 depend on | D1 p2, p23–25 | Resolved (CH-11, CH-02) |
| KI-06 | Three different mechanisms expire a table hold | D1 p27, p28, p31; D2 | Resolved: ADR-08 (CH-13, CH-14) |
| KI-07 | ADR-02 leaves its decision open | D1 p27 | Resolved: ADR-09 (CH-14) |
| KI-08 | ADR-04's Web Push channel is missing from D2 | D1 p29; D2 p5, p7 | Resolved: ADR-10 (CH-15) |
| KI-09 | D2 counts three business use cases but lists four | D2 p2; D1 p19 | Resolved (CH-18) |
| KI-10 | sendSlipDecisionNotice() has no caller | D2 p5, p7 | Resolved (CH-19, CH-20) |
| KI-11 | Two diagram arrows end on another service's private database | D2 p7 | Resolved (CH-20) |
| KI-12 | Section numbering and page layout of D2 | D2 p2, p3, p6, p8 | Resolved (CH-18) |
| KI-13 | Department name on both covers | D1 p1; D2 p1 | Resolved (CH-21) |
| KI-14 | The ADRs do not yet meet the syllabus minimum technology requirements | D1 p26–32; D2 p7; syllabus item 17 | Open: Deliverable #3 |

## KI-01 Use case names in the diagram differ from the descriptions

Found by Watayut: the names of UC-03 and UC-04 in the use case diagram differ from the use case descriptions.

| Use case | In the diagram (D1 p3) | In the descriptions (D1 p4, p10, p15, p19) and D2 p2 |
|---|---|---|
| UC-01 | Reserve a specific table | Reserve a Specific Table |
| UC-02 | Check in using digital QR ticket | Check In Using Digital QR Ticket |
| UC-03 | **Manage arrival and cutoff** | **Create Concert Event** |
| UC-04 | **Configure venue and floor plan** | **Create Venue Zone Map** |

UC-01 and UC-02 differ only in capitalization. No description exists for "Manage arrival and cutoff"; see KI-03.
The [Deliverable #1 brief](../../problem/deliverable-1/problem.md) asks for a use case diagram consistent with the use cases described.

## KI-02 Actors in the diagram differ from the descriptions and the requirements

- **Names.** The diagram (D1 p3) has Customer, Staff and Admin / Venue Owner. The descriptions have Customer, Front Staff and
  Manager as primary actors, and plain "Staff" in their stakeholder lists. Target Customer (D1 p2) has "Manager (Bar/Venue
  Owner)" and "Staff (Front-of-House / Host)". The functional requirements (D1 p23) say "allow admins to create and edit venue
  zone maps" but "allow managers to create a concert round", while the security requirement (D1 p25) knows only the roles
  Manager, Staff and Customer. D2 p7 uses Customer, Front Staff and Manager.
- **Associations.** The diagram links Customer and Staff to UC-03 and links Admin / Venue Owner to UC-04 only. In the
  descriptions the Manager is the primary actor of UC-03 and UC-04, reviews a transfer slip in degraded mode in UC-01 and
  rules on escalations in UC-02. LINE, the Payment Gateway and Time act in the descriptions but are not in the diagram.

Proposed alignment, drafted in an earlier transcription pass from the descriptions (not applied to any deliverable):

| Use case | Primary actor | Supporting actors |
|---|---|---|
| UC-01 Reserve a Specific Table | Customer | LINE Login, LINE Messaging API, Payment Gateway, Manager (degraded-mode slip review), Time (hold expiry) |
| UC-02 Check In Using Digital QR Ticket | Front Staff | Customer, Manager (escalation ruling), Time (no-show marking) |
| UC-03 Create Concert Event | Manager | — |
| UC-04 Create Venue Zone Map | Manager | — |

Dependencies between use cases: UC-04 produces the zone map required by UC-03; UC-03 produces the concert round used by UC-01 and the check-in window and grace period used by UC-02; UC-01 produces the Confirmed booking and e-ticket used by UC-02.

```mermaid
flowchart LR
    Customer(["Customer"])
    Staff(["Front Staff"])
    Manager(["Manager"])
    Time(["Time"])
    LINE(["LINE Login /<br/>Messaging API"])
    PG(["Payment Gateway"])

    subgraph CTRS["Concert Table Reservation System (CTRS)"]
        UC01(["UC-01<br/>Reserve a Specific Table"])
        UC02(["UC-02<br/>Check In Using Digital QR Ticket"])
        UC03(["UC-03<br/>Create Concert Event"])
        UC04(["UC-04<br/>Create Venue Zone Map"])
    end

    Customer --- UC01
    Customer --- UC02
    Staff --- UC02
    Manager --- UC01
    Manager --- UC02
    Manager --- UC03
    Manager --- UC04
    UC01 --- LINE
    UC01 --- PG
    UC01 --- Time
    UC02 --- Time

    UC04 -. "zone map" .-> UC03
    UC03 -. "concert round" .-> UC01
    UC03 -. "check-in window" .-> UC02
    UC01 -. "booking + e-ticket" .-> UC02
```

## KI-03 Two arrival models: cutoff with extensions, or check-in window with no-shows

- **Cutoff model.** Problem Description and Target Customer (D1 p2): "automated cutoff reminders with arrival confirmation
  and extension requests". Functional requirements (D1 p23–24): show the cutoff time before confirmation; "Arrival &
  Notification System" sends cutoff reminders through LINE, lets customers choose "I'm on my way" or a 30-minute extension,
  lets staff approve or reject it, and expires reservations after the effective cutoff. Non-functional requirements (D1 p25):
  cutoff times and extension request statuses. ADR-03 (D1 p28): node-cron for background cutoff scheduling. ADR-04
  (D1 p29): reminders before cutoff with "On My Way" / "Postpone 30 mins" cards. The diagram's UC-03 "Manage arrival and
  cutoff" (D1 p3).
- **Check-in window model.** UC-02 (D1 p10–14): the check-in window and grace period come from the round created in UC-03,
  and a booking not checked in by the end of the grace period becomes a no-show (p13 still says "at the cutoff"). D2 p2 and
  its services follow this model: getCheckInWindow(), markNoShows(), and no reminder, arrival-confirmation or extension
  operation.
- No use case description covers reminders or extensions.

## KI-04 Who asks for a postponement is stated two ways

Target Customer (D1 p2) says Staff "create cutoff/postponement requests". The functional requirements (D1 p24) and ADR-04
(D1 p29) say the customer requests the 30-minute extension and staff approve or reject it.

## KI-05 The requirements leave out behaviour the use cases and D2 depend on

- No requirement (D1 p23–25) mentions payment of the full table fee, the Payment Gateway, refunds, transfer slips and the
  degraded payment mode, the 15-minute hold, the waitlist, check-in escalation or no-shows. UC-01 and UC-02 specify all of
  them, and D2 has services and operations for them, for example the Payment Service, holdTable(), escalateCheckIn() and
  markNoShows().
- Target Customer (D1 p2) promises the Manager booking-traffic monitoring and booking analytics. No requirement, use case or
  D2 operation covers them.

## KI-06 Three different mechanisms expire a table hold

ADR-02 (D1 p27) uses short-term Redis distributed locks for table selection. ADR-06 (D1 p31) uses MongoDB TTL indexes for
"temporary reservation locks or draft bookings that expire if not checked out within a few minutes". ADR-03 (D1 p28) uses a
node-cron background task to release expired reservations. UC-01 and D2 specify a 15-minute hold, expired by Time through the
Booking Service, with "first lock wins" in the Table Availability Service. No ADR says which mechanism applies, "a few
minutes" does not match 15 minutes, and Redis does not appear in D2. The D2 feedback suggests leaving real-time updates
out of the MVP, which bears on ADR-02.

## KI-07 ADR-02 leaves its decision open

ADR-02 (D1 p27) decides "WebSocket (or Server-Sent Events - SSE)". ADR-03 (D1 p28) then picks Socket.io, and D2 p7 draws a
WebSocket push.

## KI-08 ADR-04's Web Push channel is missing from D2

ADR-04 (D1 p29) uses the LINE Messaging API "supplemented by Web Push notifications". In D2 (p5, p7) the Notification Service
calls only the LINE Messaging Adapter.

## KI-09 D2 counts three business use cases but lists four

D2 p2 refers to "the three business use cases of Deliverable #1", lists four (UC-01 to UC-04), and then says "Maintaining the
venue zone map is not itself one of the three business use cases". D1 p19 defines it as UC-04 Create Venue Zone Map with
use case type "Business / Creation".
The [Deliverable #2 brief](../../problem/deliverable-2/problem.md) asks for coverage of the group's 3 business use cases; the only use cases it rules out as non-business are
user-management ones such as registration and login (guideline 2).

## KI-10 sendSlipDecisionNotice() has no caller

The Notification Service offers sendSlipDecisionNotice() (D2 p5). The Payment Service reviews slips with
reviewTransferSlip(), but its collaborators are the Payment Gateway Adapter, the Media Storage Adapter and the Booking
Service. The Booking Service's Notification collaborators omit it, and the diagram (D2 p7) has no arrow from the Payment
Service to the Notification Service.
Guideline 7 of the [Deliverable #2 brief](../../problem/deliverable-2/problem.md): the table and the diagram must agree, checked from each use case through its operations and
collaborators.

## KI-11 Two diagram arrows end on another service's private database

In the diagram (D2 p7) the arrow from the Booking Service to the Table Availability Service ends beside the Table Status DB,
and the confirmBookingPayment() arrow from the Payment Service ends on the Booking DB. The legend says a cylinder is a data
store owned privately by its service, so the two arrows can be read as cross-service database access.
Guideline 4 of the [Deliverable #2 brief](../../problem/deliverable-2/problem.md): a service's data is private, and other services reach it through the service's API, not its
database.

## KI-12 Section numbering and page layout of D2

"Scope of this deliverable" (p2) and "Service–Operations–Collaborators" (p3) are both numbered 1, and "Architecture diagram"
(p7) has no number. Page 6 holds only the last two Notification Service operations, and page 8 is blank.

## KI-13 Department name on both covers

Both covers (D1 p1, D2 p1) say "Department of Software Engineering, Faculty of Engineering". The course belongs to the
Department of Computer Engineering: the syllabus (item 4) gives ภาควิชาวิศวกรรมคอมพิวเตอร์, and the page header of both
documents shows the CHULA ENGINEERING COMPUTER logo.

## KI-14 The ADRs do not yet meet the syllabus minimum technology requirements

The syllabus (item 17, minimum requirements for the term project) asks for at least one REST service, one gRPC service,
one service behind a message broker and an API gateway, a description of service discovery, and at least two types of
database, both relational and NoSQL. The ADRs (D1 p26–32) and the architecture (D2 p7) use REST only, no message broker and
MongoDB as the single database engine, and say nothing about service discovery. The Deliverable #2 brief (guideline 8)
allows REST only and a single database in the first architecture version and asks to revisit the technology requirements
later; Deliverable #3 already needs a REST service and a gRPC service with CRUD. Found 2026-09-29; to be decided with
Deliverable #3.

