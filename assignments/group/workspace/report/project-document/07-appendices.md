# Appendix A Change Log

Each change of version 2.0 has an identifier. The commits that made it start with the same identifier, and the redline of Appendix C shows the exact text. In the Source column, FB-nn is teacher feedback, KI-nn a known issue of the submitted deliverables, "Req. update" a change of the system's requirements, and "owner" a request of the document owner.

*Table A.1 Changes from version 1.1 to version 2.0*

| ID | Type | Section | Change | Source |
|---|---|---|---|---|
| CH-01 | Added | 0, A to C | Document control (document information, revision history) and, in the appendices, this change log, the resolution of the feedback and the known issues, and how to compare the versions. | — |
| CH-02 | Modified | 1.1, 1.2 | The problem description ends with full payment and one arrival rule (check-in window, grace period, no-show) instead of cutoff reminders and extension requests. Target customers are the Manager (the owner reads the same back-office), the Front Staff, who seat walk-ins at no-show tables and no longer create postponement requests, and the Customer; analytics and seat-view photographs are removed. | KI-02, KI-03, KI-04, KI-05, Req. update |
| CH-03 | Added | 1.3 | Scope and increments: what the MVP builds, what Increment 2 adds and what is out of scope. | FB-D2-01 |
| CH-04 | Modified | 2.1 | Use case diagram redrawn: use case names as in the descriptions; actors Customer, Front Staff, Manager, LINE Platform, Payment Gateway and Time with the associations of the descriptions. Table 2.1 lists actors, traces and increments. | KI-01, KI-02 |
| CH-05 | Modified | 2.2 | "Front Staff" instead of "Staff" in the stakeholder lists; every use case states its increment and the business rules it follows. | KI-02 |
| CH-06 | Modified | 2.2 | Flows that the MVP does not build are marked (Increment 2); UC-01 pays through the simulated gateway in the MVP. | FB-D2-01 |
| CH-07 | Modified | 2.2.1 | UC-01: the map is refreshed within 2 seconds; leaving the app does not release a hold; the hold timer keeps running during a correction; status polling runs until 10 minutes after the hold ends; the e-ticket stays under My Bookings when LINE fails. | Req. update |
| CH-08 | Modified | 2.2.2 | UC-02: extra guests are handled by hand outside the system; latecomers of a booking are let through; a late party may be seated as walk-ins on the Manager's authority while the booking stays No-show; no-show tables are free for walk-ins and never waitlisted; "at the cutoff" is "at the end of the grace period". | KI-03, Req. update |
| CH-09 | Modified | 2.2.3 | UC-03: package price per table type and zone; extra-person fee, check-in window and grace period are business parameters; zone map, tables and prices are fixed once booking opens. | Req. update |
| CH-10 | Modified | 2.2.4 | UC-04: the zones are drawn on an uploaded image of the venue; seat-view photographs are out of scope; EF-3 is an image upload failure. | Req. update |
| CH-11 | Modified | 3.1 | Functional requirements completed and given identifiers, use cases and increments: payment, hold, e-ticket, check-in, escalation, no-show and live view added; cutoff reminders, extensions and walk-in bookings replaced; "admins" is "Manager"; out-of-scope list added. | KI-02, KI-03, KI-05, Req. update |
| CH-12 | Modified | 3.2 | Non-functional requirements with identifiers and measurable targets (for example table status within 2 seconds instead of 3); Reliability and Interfaces added. | Req. update |
| CH-13 | Modified | 4.6 | ADR-06: the need for a flexible schema for **zone maps** moved from Consequences to Context; the consequences now include the negative ones; the TTL-index consequence is removed. | FB-D1-01, KI-06 |
| CH-14 | Added, Modified | 4, 4.2, 4.3, 4.8, 4.9 | ADR index (Table 4.1) and the rule that a changed decision gets a new ADR. ADR-08 Table Hold and Concurrency Control and ADR-09 Table Status Updates in the MVP: Polling added; ADR-02 superseded; ADR-03 amended. | KI-06, KI-07, FB-D2-01 |
| CH-15 | Added, Modified | 4.4, 4.10 | ADR-10 Customer Notifications through the LINE Messaging API Only added; ADR-04 superseded. | KI-03, KI-08 |
| CH-16 | Added | 4.11 | ADR-11 Simulated Payment Gateway for the MVP. | FB-D2-01 |
| CH-17 | Modified | 4.7 | ADR-07 includes the Owner's read-only account role. | Req. update |
| CH-18 | Modified | 5.1 | The scope covers the four use cases; the sections are numbered 5.1 to 5.3. | KI-09, KI-12 |
| CH-19 | Modified | 5.2 | Table 5.1 marks the Increment 2 operations; the Payment Service calls the Notification Service for sendSlipDecisionNotice(); zone-map image operations replace the seat-view photo operations; recordAdditionalGuests() is removed. | KI-10, FB-D2-01, Req. update |
| CH-20 | Modified | 5.3 | Figure 5.1 architecture version 2: arrows end on the services, not on their databases; Payment → Notification added; Increment 2 arrows grey and dashed; polling and simulated gateway in the MVP. | KI-10, KI-11, FB-D2-01 |
| CH-21 | Modified | cover | The cover names the Department of Computer Engineering. | KI-13 |
| CH-22 | Modified | 0.1, 1.3, 2.1, 5.1, 5.3, cover | The product is named Seating & Event Availability Tracking System (SEATS) instead of Concert Table Reservation System (CTRS); the use case diagram's system boundary, the figure captions, the cover and the running header follow. | Req. update |
| CH-23 | Modified | 2.2 | The four use case descriptions are tables (name, ID, importance with increment; primary and secondary actors, type; stakeholders; brief description; trigger with its type; relationships as association, include, extend, generalization, related use cases and business rules; pre- and postconditions; basic flow with phases and extension points; subflows S-1; alternative and exception flows), grouped as 2.2.1 to 2.2.4 under 2.2 Use Case Descriptions. The wording of the flows is unchanged. | owner |
| CH-24 | Modified | 2.1 | Figure 2.1 redrawn as a generated diagram (SVG: actors as stick figures, external systems as «actor» boxes, Time as «timer»), with the same use cases, actors and associations. | owner |
| CH-25 | Modified | 4.1 to 4.11 | Every ADR is a table of the template's five fields (Title, Context, Decision, Status, Consequences), Tables 4.2 to 4.12, and starts on a new page. The wording of the ADRs is unchanged. | owner |
| CH-26 | Modified | 5.3 | Figure 5.1 re-laid so that no arrow crosses a component or a label: the Booking → Notification call crossed the Notification hexagon and now enters its REST tab directly (the Notification Service moved up beside the Booking Service); the LINE Login line crossed the "Client applications" label, which moved to the bottom of its group. The drawing tool now checks every arrow against every component and label. | owner |
| CH-27 | Modified | 0, 1.3, 2, 3, 4, A to C | Section 0 keeps the document information and the revision history; the change log, the resolution table and how to compare the versions moved to Appendices A to C, and the open items are removed. The sources of the requirements are no longer cited: the requirements, their identifiers and the business rules (new Section 3.3) are part of this document, and requirements SA-01 to SA-05 are renumbered FR-73 to FR-75, NFR-44 and NFR-45. | owner |
| CH-28 | Added | 6 | Glossary of the business terms (Table 6.1, 40 terms, including those the business rules use); the appendices move to the end of the document. | owner |
| CH-29 | Modified | 1 to 5 | Business terms set in bold wherever they occur in the text and the tables, except in headings, captions, names of use cases and services, and phase names; in the PDF each bold term links to its glossary entry. The very frequent words booking and table are defined but not set in bold. | owner |
| CH-30 | Modified | 1.3, 5.1 | The text states the increments without referring to the teacher's feedback; only the ADRs, the revision history and these appendices cite it. | owner |
| CH-31 | Modified | 2.2.1 to 2.2.4 | Every use case description (heading and table) starts on a new page. | owner |
| CH-32 | Modified | 5.1, 5.3 | The heading of 5.3 is printed on the landscape page of Figure 5.1 instead of alone on the page before; the explanation of the diagram moved to the end of 5.1. Figure 2.1 stays on the portrait page of Section 2 instead of a landscape page that left the headings of Section 2 alone. Headings are kept with the text that follows them, and the contents fit on two pages. | owner |
| CH-33 | Added | 5.2, 4 | Section 5.2 Parts of the System and Communication: the Frontend, the Backend and the External systems (Table 5.1) and how they communicate (Table 5.2). Table 4.1 names the part of the system that each ADR concerns. | owner |
| CH-34 | Added | 4.12 | ADR-12 Communication: REST through the API Gateway, gRPC between Services; no message broker in the MVP. | owner, KI-14 |
| CH-35 | Modified | 5.1, 5.3 | Section 5 shows the MVP only, with a note that the operations of Increment 2 and later increments are not listed. Table 5.3 completed by tracing the use cases through it: the Staff Account Service owns the back-office accounts, sign-in and roles of ADR-07; verifyBookingReference(), getRoundBookings(), getBooking(), getCustomerProfile(), countAvailableTables(), listing, reading, validating and activating a zone map, the business parameters and sendPaymentFailedNotice() added. The Concert Round Service reads the booked tables from the Table Availability Service instead of calling getConfirmedBookingCount() of the Booking Service, which removes the two-way dependency between the two services. getDeliveryStatus(), which no flow uses, removed. | KI-15, owner |
| CH-36 | Added | 5.4 | Use case traceability: Tables 5.4 to 5.8 trace every MVP step of the four use cases, and the requirements not tied to one step, from the actor to the operation, its collaborations, the data stored and the requirements realised. | KI-15 |
| CH-37 | Modified | 5.5 | Figure 5.1 redrawn for the MVP: the three parts as dashed boundaries; REST and gRPC tabs on the services and gRPC calls as purple arrows (ADR-12); the Staff Account Service and the Payment → Notification call added; the Increment 2 arrows removed; the payment webhook drawn along the top. | owner, KI-15 |
| CH-38 | Modified | 1.3, 4.10 | Section 1.3 lists UC-04 EF-3 (image upload failure) in the MVP and states that Section 5 shows the MVP only. ADR-10 names the payment-failed notice among the messages in scope (FR-21), a correction of the record. | KI-15 |
| CH-39 | Modified | 5.3, 5.4 | Each operation is one function: createZoneMap() and updateZoneMap() replace createOrUpdateZoneMap(), updateRound() replaces saveRoundAsDraft(), createCustomerProfile() and updateCustomerProfile() replace saveCustomerProfile(), defineTableType() replaces setTableType(), and getBookingTerms() is added for UC-01 step 13. The traceability tables follow the use cases step by step with one row per operation, including the steps without an operation and the retries of EF-2 and EF-5. | owner |
| CH-40 | Modified | 5.1, 5.5 | Figure 5.1: the API Gateway carries a REST tab on its left edge and both web-app arrows end on it, as the teacher's FTGO figure draws the gateway; the legend and Section 5.1 say that a tab is an API a component offers. | owner |
| CH-41 | Added | 5.1 | The services are mapped to the bounded contexts of the domain and to the core, supporting and generic subdomains, with the reason for keeping Table Availability and Booking as two services. | owner |
| CH-42 | Modified | 5.3, 5.4 | Table 5.3 lists only the operations a service exposes: expireUnpaidBookings() and retryFailedMessages() are the jobs of a timer, and calculateTableFee() and issueETicket() are steps inside setPartySize() and confirmBookingPayment(); all four are described below the table. previewRound() is removed (the preview is getRound() and getRoundTables()), editPublishedRound() is folded into updateRound() (one operation per resource, rules by status), and listTableTypes() is added for the map editor. 55 operations; the traceability rows follow. | owner |
| CH-43 | Modified, Added | 5.4, D | Section 5.4 is a one-page matrix of the operations by use case (Table 5.4), with a System-wide column for the functions not tied to one step; the step-by-step tables with the collaborations, the data stored and the requirements move to Appendix D (Tables D.1 to D.5) as the evidence. | owner |
| CH-44 | Modified | 5.2 | Table 5.1 has one row per deployable component, grouped by part (two web apps, the API Gateway, six services, three external systems), with the responsibility, the API it offers (REST, gRPC or the provider's API) and the data it owns; the trust properties of the parts (untrusted Frontend, the gateway as the only public entry, private network, third parties) move to the paragraph above the table. | owner |
| CH-45 | Modified | 1, 2, 3, 4, 5, 6 | One term for each thing: "concert round" (UC-03 is Create Concert Round; "concert event" removed), "zone map" ("floor plan", "layout" and "table map" replaced in the bodies; the titles of ADR-02 and ADR-05 stay as written and the glossary notes the term), and "e-ticket" (UC-02 is Check In with E-Ticket; "digital QR ticket" and "digital ticket" replaced). The phase {View the Table Map} of UC-01 is {View the Zone Map}. | owner |
| CH-46 | Added | 2.3 | Domain model: the class diagram (Figure 2.2), the business entities (Table 2.6), the associations and invariants (Table 2.7), and the booking state machine (Figure 2.3) with its states (Table 2.8); WaitlistEntry, BookingTransfer and the Transferred state are marked as a later release. | owner |
| CH-47 | Added, Modified | 2.1, 5.4, D | UC-05 View Live Booking Status, UC-06 View My Bookings, UC-07 Set Business Parameters and UC-08 Manage Staff Accounts added by name to Figure 2.1 and Table 2.1, with the Owner as an actor; Table 5.4 has one column per use case instead of a System-wide column, and Table D.5 traces UC-05 to UC-08. | owner |

# Appendix B Resolution of Feedback and Known Issues

The teacher feedback is kept as received in the group's workspace (received/teacher/), and the known issues are described in workspace/notes/known-issues.md.

*Table B.1 Feedback and known issues, and the changes that resolve them*

| Item | Summary | Resolution |
|---|---|---|
| FB-D1-01 | ADR-06: "Flexible Schema for Layouts" belongs in Context rather than Consequences. | Done: CH-13 |
| FB-D2-01 | The scope is large for 2–3 months; the MVP should cover rounds, table selection and booking, simulated payment and QR check-in; automatic refund, transfer-slip review, real-time WebSocket and degraded payment mode later. | Done: CH-03, CH-06, CH-14, CH-16, CH-19, CH-20 |
| KI-01 | Use case names in the diagram differ from the descriptions. | Resolved: CH-04 |
| KI-02 | Actors in the diagram differ from the descriptions and the requirements. | Resolved: CH-02, CH-04, CH-05, CH-11 |
| KI-03 | Two arrival models: cutoff with extensions, or check-in window with no-shows. | Resolved: the check-in window model is kept; reminders and the extension are out of scope (CH-02, CH-08, CH-11, CH-15) |
| KI-04 | Who asks for a postponement is stated two ways. | Resolved: postponement requests are removed with the extension (CH-02) |
| KI-05 | The requirements leave out behaviour the use cases depend on. | Resolved: CH-11; analytics out of scope (CH-02) |
| KI-06 | Three different mechanisms expire a table hold. | Resolved: ADR-08 (CH-13, CH-14) |
| KI-07 | ADR-02 leaves its decision open. | Resolved: ADR-09 supersedes it (CH-14) |
| KI-08 | ADR-04's Web Push channel is missing from the architecture. | Resolved: ADR-10 (CH-15) |
| KI-09 | Deliverable #2 counts three business use cases but lists four. | Resolved: CH-18 |
| KI-10 | sendSlipDecisionNotice() has no caller. | Resolved: CH-19, CH-20 |
| KI-11 | Two diagram arrows end on another service's private database. | Resolved: CH-20 |
| KI-12 | Section numbering and page layout of Deliverable #2. | Resolved: CH-18 and the layout of this document |
| KI-13 | Department name on both covers. | Resolved: CH-21 |
| KI-14 | The ADRs do not yet meet the syllabus minimum technology requirements. | Partly resolved: REST and gRPC chosen in ADR-12 (CH-34); the message broker, service discovery and a second type of database stay open for Deliverable #3 |
| KI-15 | The Service–Operations–Collaborators table misses operations that the use cases need. | Resolved: CH-35 to CH-39 |

# Appendix C How to See the Changes

- **Redline.** tools/redline.py writes a page that shows every deleted and inserted word between version 1.1 and this version, paragraph by paragraph, under its section heading.
- **Git.** The tag doc-v1.1-submitted holds the text as submitted, doc-v2.0-draft1 to doc-v2.0-draft17 the earlier drafts and doc-v2.0-draft18 this version; comparing the two tags on GitHub, or with git diff on the folder workspace/report/project-document, shows every change.
- **Commits.** Every commit of this revision starts with the change identifiers it applies, for example "doc v2.0 CH-13..CH-17".

# Appendix D Use Case Traceability, Step by Step

Tables D.1 to D.5 are the evidence behind Table 5.4: each row follows one step, or the consecutive steps served by one operation, of a use case: who invokes the operation (an actor, through the API Gateway, or a service), the service and operation that carry the step out, the collaborations the operation needs, the data it stores, and the requirements it realises. Steps in which the actor acts without the system, such as UC-02 step 5, are left out unless a rule applies to them. Only the flows that the MVP builds are listed (Section 1.3), and Table D.5 covers UC-05 to UC-08, which have no description. Every operation of Table 5.3 appears in at least one row, the two jobs appear as jobs, and every MVP requirement of Section 3.1 is realised by at least one row.

<div class="trace" markdown="1">

*Table D.1 Traceability of Reserve a Specific Table*

| Steps | Invoked by | Operation | Collaborations | Data stored | Requirements |
|---|---|---|---|---|---|
| 1–2, EF-5 | **Customer** | API Gateway: check the LINE ID token that LINE Login gave the **LIFF** app | LINE Login Adapter, which asks the **LINE Platform** | — | FR-01, FR-02 |
| 3, AF-2 | **Customer** | Concert Round Service: getUpcomingRounds(), with the status of each round | Table Availability Service: countAvailableTables(), for the sold-out status | — | FR-03 |
| 4, AF-1 | **Customer** | Concert Round Service: getRound() | — | — | FR-03, FR-04 |
| 5, AF-2 | **Customer** | Concert Round Service: getRoundTables()<br>Table Availability Service: getRoundTableStatus(), polled every 2 seconds | — | — | FR-05, FR-06 |
| 6–8, AF-3 | **Customer** | Booking Service: createHeldBooking() | Concert Round Service: getRound(), to check that booking is open<br>Table Availability Service: holdTable() | Booking DB: booking Held until the end of the **hold**<br>Table Status DB: table held | FR-04, FR-07, FR-08 |
| 9 | **Customer** | Booking Service: getBooking(), the booking summary and the remaining **hold** time | — | — | FR-07 |
| 10–11 | **Customer** | Booking Service: setPartySize(), which computes the **full table fee** | Concert Round Service: getRoundPricing() | Booking DB: **party size** and **full table fee** | FR-09 |
| 12 | **Customer** | Booking Service: getCustomerProfile(), which tells whether a profile exists | — | — | FR-10 |
| 12a, AF-7 | **Customer** | Booking Service: createCustomerProfile(), with the consent, the name and the phone; AF-7 is its validation | — | Booking DB: **customer profile** and consent | FR-10 |
| 12b | **Customer** | Booking Service: updateCustomerProfile(), when the **Customer** corrects the pre-filled profile | — | Booking DB: **customer profile** | FR-10 |
| 13 | **Customer** | Booking Service: getBookingTerms() | Concert Round Service: getCheckInWindow() | — | FR-12 |
| 14 | **Customer** | Booking Service: acceptBookingTerms() | — | Booking DB: **booking terms** accepted | FR-12 |
| 15 | **Customer** | Booking Service: startPayment() | Payment Service: createPaymentRequest() | Booking DB: payment started | FR-13 |
| 15 | Booking Service | Payment Service: createPaymentRequest() | Payment Gateway Adapter: createCheckoutSession() | Payment DB: payment request | FR-13 |
| 16–17 | **Customer** | No operation of SEATS: the **Customer** pays in the **hosted checkout** of the **Payment Gateway**, simulated in the MVP (ADR-11) | — | — | FR-13 |
| 18, AF-5 | **Payment Gateway** | Payment Service: receivePaymentResult(), the signed webhook routed by the API Gateway; a duplicate result is ignored | Payment Gateway Adapter: verifyWebhookSignature()<br>Booking Service: confirmBookingPayment(), when paid<br>Notification Service: sendPaymentFailedNotice(), when declined | Payment DB: payment result, processed once | FR-14, FR-16, FR-21 |
| 19–20 | Payment Service | Booking Service: confirmBookingPayment(), which also issues the **e-ticket** | Table Availability Service: markTableBooked() | Booking DB: payment recorded, booking Confirmed, **e-ticket** with the signed **booking reference**<br>Table Status DB: table booked | FR-16, FR-19 |
| 21, AF-5 | **Customer** | Payment Service: getPaymentStatus()<br>Booking Service: getBooking(), getETicket() | — | — | FR-14, FR-19 |
| 22, S-1 | Booking Service | Notification Service: sendBookingConfirmation() | LINE Messaging Adapter: pushLineMessage() | Notification DB: message and delivery result | FR-20 |
| AF-4, AF-6 | **Customer** | Booking Service: cancelBooking() | Table Availability Service: releaseHold() | Booking DB: booking Cancelled<br>Table Status DB: table available | FR-10, FR-11 |
| AF-5 | Payment Service | Notification Service: sendPaymentFailedNotice() | LINE Messaging Adapter: pushLineMessage() | Notification DB: message and delivery result | FR-21 |
| EF-1 | Time | Booking Service: the hold-expiry job, every 5 seconds (ADR-08); not an operation | Table Availability Service: releaseHold()<br>Notification Service: sendHoldExpiredNotice() | Booking DB: booking Expired<br>Table Status DB: table available | FR-21, FR-23 |
| EF-1, S-1 | Booking Service | Notification Service: sendHoldExpiredNotice() | LINE Messaging Adapter: pushLineMessage() | Notification DB: message and delivery result | FR-21 |
| EF-6 | Time | Notification Service: the retry job, 3 times within 5 minutes; not an operation | LINE Messaging Adapter: pushLineMessage() | Notification DB: delivery result | FR-22 |

*Table D.2 Traceability of Check In with E-Ticket*

| Steps | Invoked by | Operation | Collaborations | Data stored | Requirements |
|---|---|---|---|---|---|
| 2–4, S-1, AF-2, AF-3, AF-5, EF-1, EF-2 | **Front Staff** | Booking Service: verifyBookingReference(), with the **booking reference** scanned (step 2) or typed (AF-2); its answer is the result of step 4 or the reason of AF-3, AF-5, EF-1 and EF-2 | Concert Round Service: getCheckInWindow() | — (verification changes nothing) | FR-24, FR-25, FR-26, FR-27 |
| 6, EF-5 | **Front Staff** | Booking Service: checkInBooking(); a retry finds the existing check-in and does not repeat it (EF-5) | Table Availability Service: markTableOccupied() | Booking DB: booking Checked-in with the time and the staff account<br>Table Status DB: table occupied | FR-28 |
| 7 | **Manager** | Booking Service: getRoundBookings()<br>Table Availability Service: getRoundTableStatus(), polled every 2 seconds | — | — | FR-06, FR-42 |
| AF-4 | **Front Staff** | No operation of SEATS: extra guests are handled by hand (BRULE-09) | — | — | — |

*Table D.3 Traceability of Create Concert Round*

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
| 14–15, EF-2 | **Manager** | Concert Round Service: publishRound(); a retry finds the published round and does not create a second one (EF-2) | Table Availability Service: initializeRoundTableStatus() | Round DB: round Published<br>Table Status DB: every table for sale available | FR-34, FR-75 |
| AF-1 | **Manager** | Concert Round Service: updateRound(); the round stays Draft | — | Round DB: the round as entered | FR-34 |
| AF-3 | **Manager** | Concert Round Service: getRound(), then updateRound(), which allows a Published round only the changes of AF-3 (BRULE-07) | Table Availability Service: getRoundTableStatus(), whose booked tables are the Confirmed bookings | Round DB: the changed fields | FR-34, FR-35 |

*Table D.4 Traceability of Create Venue Zone Map*

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

*Table D.5 Traceability of UC-05 to UC-08, the use cases without a description*

| Use case | Invoked by | Operation | Collaborations | Data stored | Requirements |
|---|---|---|---|---|---|
| UC-07 | **Manager** | Concert Round Service: getBusinessParameters(), updateBusinessParameters() | — | Round DB: the **business parameters**; a round uses the values in force at its **booking-open time** | FR-38 |
| UC-06 | **Customer** | Booking Service: getCustomerBookings(), getETicket() | — | — | FR-40 |
| UC-05 | **Manager**, **Owner** | Booking Service: getRoundBookings()<br>Table Availability Service: getRoundTableStatus() | — | — | FR-42 |
| UC-08 | **Manager** | Staff Account Service: createStaffAccount(), listStaffAccounts(), updateStaffAccount() for the role, disableStaffAccount() | — | Staff Account DB: accounts, roles and password hashes | FR-65 |
| UC-08 | **Front Staff**, **Manager**, **Owner** | Staff Account Service: signIn(); the API Gateway checks the role of every request | — | — | FR-65, FR-66 |
| UC-08 | All users | Staff Account Service: signOut(); a **Customer** logs out of LINE Login in the web app | — | — | FR-73 |

</div>
