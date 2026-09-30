# 1 Change Log

## 1.1 Document Information

*Table 1.1 Document information*

| | |
|---|---|
| Document | Change Log of the Project Description, ADRs and Microservice Design of the Seating & Event Availability Tracking System (SEATS) |
| Applies to | SEATS project document, version 2.0 draft 23, 30 September 2026 (its Section 0.2 lists the drafts) |
| Group | SE 101 |
| Contents | Section 1.2: every change since version 1.1, with its type, section, description and source. Section 2.1: how each teacher comment and known issue of Deliverables #1 and #2 was resolved. Section 2.2: how to compare the versions. |

## 1.2 Changes

Each change of version 2.0 has an identifier. The commits that made it start with the same identifier, and the redline of Section 2.2 shows the exact text. In the Source column, FB-nn is teacher feedback, KI-nn a known issue of the submitted deliverables, "Req. update" a change of the system's requirements, and "owner" a request of the document owner.

*Table 1.2 Changes from version 1.1 to version 2.0*

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
| CH-48 | Modified | 0.1, 3, 5, A, B | The change log, the resolution of feedback and known issues, and how to compare the versions are this separate document; the operations-by-use-case matrix moves from Section 5.4 to Appendix A.1, with the step-by-step tables as A.2 (Section 5.5 becomes 5.4); the business rules move from Section 3.3 to Appendix B. | owner |
| CH-49 | Modified, Added | 6, 1 to 5 | The glossary is split: Table 6.1 business terms, set in bold in the text and linked; Table 6.2 technology and project terms (API Gateway, REST, gRPC, Protocol Buffers, webhook, adapter, polling, WebSocket, LIFF, LINE Login, ID token, LINE Messaging API, Rich Menu, hosted checkout, session token, MongoDB, node-cron, idempotent, bounded context, MVP, Increment), plain in the text. LIFF, Rich Menu and hosted checkout moved from the business table and are no longer bold. | owner |
| CH-50 | Added, Modified | 1.3, 2.1, 2.2, 2.3, 3.1, 5.1, 5.3, A | UC-09 Maintain Customer Profile (create with consent on the first booking, view and correct from My Bookings, BRULE-11) and UC-10 Pay the Full Table Fee (the payment steps and their Increment 2 flows) are use cases of their own, «included» by UC-01 at {Complete the Customer Profile} and {Pay the Full Table Fee}; UC-01 keeps the hold, the terms, the confirmation and the e-ticket, with steps 16 to 20 renumbered and AF-5 Profile Not Completed, EF-2 and EF-3 renumbered. Figure 2.1 shows the two «include» relationships and the Payment Gateway on UC-10. The scope table, the requirements' use-case column, the booking states, the matrix (ten use-case columns) and the trace tables (A.6, A.7) follow. | owner |
| CH-51 | Added, Modified | 2, 6, C | The body keeps what the deliverables ask for: the domain model leaves Section 2 and opens the new Chapter 6 Domain Model and API Specification (6.1 domain model, 6.2 data model per service with Figures 6.3 to 6.5, 6.3 from model to contract, 6.4 the REST routes and gRPC methods of every service); the glossary becomes Appendix C (Tables C.1 and C.2). | owner |
| CH-52 | Added, Modified | 4.8, 4.13, 5, 6, A | ADR-13: the Booking Service owns the hold through a unique index on active bookings per table per round, and the Table Availability Service keeps the read model of the table map, fed by gRPC calls in the MVP and by events from Increment 2; ADR-08's locking part is superseded, its timer job stays. initializeRoundTableStatus() is createRoundTableStatus(), the C of that service's CRUD, in Table 5.3, Figure 5.1, the contracts and the trace tables. | owner |
| CH-53 | Modified | 6.1, 6.3, 6.4 | Table 6.2 Associations and invariants is dropped: the class diagram shows every association and multiplicity, and the two rules the table carried (one zone map serves many rounds and is fixed once booking opens; a round uses the business parameters in force at its booking-open time) are in the definitions of Table 6.1. Tables 6.3 to 6.8 become 6.2 to 6.7. | owner |

# 2 Resolution of Feedback and Known Issues

## 2.1 Resolutions

The teacher feedback is kept as received in the group's workspace (received/teacher/), and the known issues are described in workspace/notes/known-issues.md.

*Table 2.1 Feedback and known issues, and the changes that resolve them*

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

## 2.2 How to See the Changes

- **Redline.** tools/redline.py writes a page that shows every deleted and inserted word between version 1.1 and this version, paragraph by paragraph, under its section heading.
- **Git.** The tag doc-v1.1-submitted holds the text as submitted, doc-v2.0-draft1 to doc-v2.0-draft22 the earlier drafts and doc-v2.0-draft23 this version; comparing the two tags on GitHub, or with git diff on the folder workspace/report/project-document, shows every change.
- **Commits.** Every commit of this revision starts with the change identifiers it applies, for example "doc v2.0 CH-13..CH-17".
