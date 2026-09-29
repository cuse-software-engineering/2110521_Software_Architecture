# 0 Document Control

## 0.1 Document Information

*Table 0.1 Document information*

| | |
|---|---|
| Document | Project Description, ADRs and Microservice Design of the Concert Table Reservation System (CTRS) |
| Course | 2110521 Software Architecture, Semester 1, Academic Year 2026 |
| Group | SE 101 |
| Version | 2.0 draft 1, 29 September 2026 |
| Status | Draft for review by the group; basis of the updated ADRs and microservice design of Deliverable #3 |
| Previous version | 1.1: Deliverable #1 (version 1.0) and Deliverable #2 as submitted on 8 September 2026 |
| Source of requirements | 2110628 Requirements Engineering project of the same system, there named SEATS: Vision 1.13, Software Requirements Specification 1.11, Supplementary Specification 1.9, Business Rules 1.7, use cases UC-01 1.14, UC-02 1.9 and UC-16 1.1 |

## 0.2 Revision History

*Table 0.2 Revision history*

| Version | Date | By | Description | Source |
|---|---|---|---|---|
| 1.0 | 2026-09-08 | SE 101 | Deliverable #1 submitted: project description, four use cases, requirements, ADR-01 to ADR-07. | — |
| 1.1 | 2026-09-08 | SE 101 | Deliverable #2 submitted: microservice design version 1 (Service–Operations–Collaborators table, architecture diagram). | — |
| 2.0 draft 1 | 2026-09-29 | Watayut A. | Revision after the teacher's feedback on both deliverables and the known issues found in them: scope in increments with an MVP, use case diagram redrawn, requirements aligned with the 2110628 artifacts, ADR-06 corrected, ADR-08 to ADR-11 added, architecture version 2. Changes CH-01 to CH-21. | FB-D1-01, FB-D2-01, KI-01 to KI-13 |

## 0.3 Change Log

Each change of version 2.0 has an identifier. The commits that made it start with the same identifier, and the redline of Section 0.6 shows the exact text. In the Source column, FB-nn is teacher feedback, KI-nn a known issue of the submitted deliverables, and "2110628" a change of the requirements in the Requirements Engineering project.

*Table 0.3 Changes from version 1.1 to version 2.0*

| ID | Type | Section | Change | Source |
|---|---|---|---|---|
| CH-01 | Added | 0 | Document control: document information, revision history, this change log, resolution of the feedback and the known issues, open items. | — |
| CH-02 | Modified | 1.1, 1.2 | The problem description ends with full payment and one arrival rule (check-in window, grace period, no-show) instead of cutoff reminders and extension requests. Target customers are the Manager (the owner reads the same back-office), the Front Staff, who seat walk-ins at no-show tables and no longer create postponement requests, and the Customer; analytics and seat-view photographs are removed. | KI-02, KI-03, KI-04, KI-05, 2110628 |
| CH-03 | Added | 1.3 | Scope and increments: what the MVP builds, what Increment 2 adds and what is out of scope; the requirements' source and identifiers. | FB-D2-01 |
| CH-04 | Modified | 2.1 | Use case diagram redrawn: use case names as in the descriptions; actors Customer, Front Staff, Manager, LINE Platform, Payment Gateway and Time with the associations of the descriptions. Table 2.1 lists actors, traces and increments. | KI-01, KI-02 |
| CH-05 | Modified | 2.2 to 2.5 | "Front Staff" instead of "Staff" in the stakeholder lists; every use case header gains the rows "Traces to 2110628" and "Increment". | KI-02 |
| CH-06 | Modified | 2.2 to 2.5 | Flows that the MVP does not build are marked (Increment 2); UC-01 pays through the simulated gateway in the MVP. | FB-D2-01 |
| CH-07 | Modified | 2.2 | UC-01: the map is refreshed within 2 seconds; leaving the app does not release a hold; the hold timer keeps running during a correction; status polling runs until 10 minutes after the hold ends; the e-ticket stays under My Bookings when LINE fails. | 2110628 |
| CH-08 | Modified | 2.3 | UC-02: extra guests are handled by hand outside the system; latecomers of a booking are let through; a late party may be seated as walk-ins on the Manager's authority while the booking stays No-show; no-show tables are free for walk-ins and never waitlisted; "at the cutoff" is "at the end of the grace period". | KI-03, 2110628 |
| CH-09 | Modified | 2.4 | UC-03: package price per table type and zone; extra-person fee, check-in window and grace period are business parameters; zone map, tables and prices are fixed once booking opens. | 2110628 |
| CH-10 | Modified | 2.5 | UC-04: the zones are drawn on an uploaded image of the venue; seat-view photographs are out of scope; EF-3 is an image upload failure. | 2110628 |
| CH-11 | Modified | 3.1 | Functional requirements rebuilt from the 2110628 specification with their identifiers, use cases and increments: payment, hold, e-ticket, check-in, escalation, no-show and live view added; cutoff reminders, extensions and walk-in bookings replaced; "admins" is "Manager"; out-of-scope list added. | KI-02, KI-03, KI-05, 2110628 |
| CH-12 | Modified | 3.2 | Non-functional requirements with the identifiers and measures of the 2110628 Supplementary Specification (for example table status within 2 seconds instead of 3); Reliability and Interfaces added. | 2110628 |
| CH-13 | Modified | 4.6 | ADR-06: the need for a flexible schema for layouts moved from Consequences to Context; the consequences now include the negative ones; the TTL-index consequence is removed. | FB-D1-01, KI-06 |
| CH-14 | Added, Modified | 4, 4.2, 4.3, 4.8, 4.9 | ADR index (Table 4.1) and the rule that a changed decision gets a new ADR. ADR-08 Table Hold and Concurrency Control and ADR-09 Table Status Updates in the MVP: Polling added; ADR-02 superseded; ADR-03 amended. | KI-06, KI-07, FB-D2-01 |
| CH-15 | Added, Modified | 4.4, 4.10 | ADR-10 Customer Notifications through the LINE Messaging API Only added; ADR-04 superseded. | KI-03, KI-08 |
| CH-16 | Added | 4.11 | ADR-11 Simulated Payment Gateway for the MVP. | FB-D2-01 |
| CH-17 | Modified | 4.7 | ADR-07 includes the Owner's read-only account role. | 2110628 |
| CH-18 | Modified | 5.1 | The scope covers the four use cases; the sections are numbered 5.1 to 5.3. | KI-09, KI-12 |
| CH-19 | Modified | 5.2 | Table 5.1 marks the Increment 2 operations; the Payment Service calls the Notification Service for sendSlipDecisionNotice(); zone-map image operations replace the seat-view photo operations; recordAdditionalGuests() is removed. | KI-10, FB-D2-01, 2110628 |
| CH-20 | Modified | 5.3 | Figure 5.1 architecture version 2: arrows end on the services, not on their databases; Payment → Notification added; Increment 2 arrows grey and dashed; polling and simulated gateway in the MVP. | KI-10, KI-11, FB-D2-01 |
| CH-21 | Modified | cover | The cover names the Department of Computer Engineering. | KI-13 |

## 0.4 Resolution of Feedback and Known Issues

The teacher feedback is kept as received in the group's workspace (received/teacher/), and the known issues are described in workspace/notes/known-issues.md.

*Table 0.4 Feedback and known issues, and the changes that resolve them*

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
| KI-14 | The ADRs do not yet meet the syllabus minimum technology requirements. | Open: to be decided with Deliverable #3 |

## 0.5 Open Items

- **KI-14, technology minimums.** The syllabus asks for REST, gRPC and message-broker services, an API gateway, service discovery, and both a relational and a NoSQL database. Deliverable #3 needs at least a REST and a gRPC service with CRUD, so the ADRs for these choices come next.
- **Decisions for the group to confirm.** The MVP boundary of Section 1.3, in particular that seat-view photographs are out of scope and that the degraded payment mode comes after the MVP although the 2110628 requirements keep it in their Release 1.0. The product keeps the name CTRS here, while the 2110628 project now calls it SEATS.
- **Traceability.** The requirement identifiers follow the 2110628 artifact versions of Table 0.1; later changes there are not followed automatically.

## 0.6 How to See the Changes

- **Redline.** tools/redline.py writes a page that shows every deleted and inserted word between version 1.1 and this version, paragraph by paragraph, under its section heading.
- **Git.** The tag doc-v1.1-submitted holds the text as submitted and doc-v2.0-draft1 this version; comparing the two tags on GitHub, or with git diff on the folder workspace/report/project-document, shows every change.
- **Commits.** Every commit of this revision starts with the change identifiers it applies, for example "doc v2.0 CH-13..CH-17".
