# 0 Document Control

## 0.1 Document Information

*Table 0.1 Document information*

| | |
|---|---|
| Document | Project Description, ADRs and Microservice Design of the Seating & Event Availability Tracking System (SEATS) |
| Product name | SEATS; Deliverables #1 and #2 called the system Concert Table Reservation System (CTRS) |
| Course | 2110521 Software Architecture, Semester 1, Academic Year 2026 |
| Group | SE 101 |
| Version | 2.0 draft 12, 30 September 2026 |
| Status | Draft for review by the group; basis of the updated ADRs and microservice design of Deliverable #3 |
| Previous version | 1.1: Deliverable #1 (version 1.0) and Deliverable #2 as submitted on 8 September 2026 |
| Changes | Appendix A lists every change since version 1.1, Appendix B how each teacher comment and known issue was resolved, and Appendix C how to compare the versions |

## 0.2 Revision History

*Table 0.2 Revision history*

| Version | Date | By | Description | Source |
|---|---|---|---|---|
| 1.0 | 2026-09-08 | SE 101 | Deliverable #1 submitted: project description, four use cases, requirements, ADR-01 to ADR-07. | — |
| 1.1 | 2026-09-08 | SE 101 | Deliverable #2 submitted: microservice design version 1 (Service–Operations–Collaborators table, architecture diagram). | — |
| 2.0 draft 1 | 2026-09-29 | Watayut A. | Revision after the teacher's feedback on both deliverables and the known issues found in them: scope in increments with an MVP, use case diagram redrawn, requirements completed (payment, hold, check-in and no-show rules), ADR-06 corrected, ADR-08 to ADR-11 added, architecture version 2. Changes CH-01 to CH-21. | FB-D1-01, FB-D2-01, KI-01 to KI-13 |
| 2.0 draft 2 | 2026-09-29 | Watayut A. | Product name SEATS (Seating & Event Availability Tracking System) instead of CTRS. Change CH-22. | Req. update |
| 2.0 draft 3 | 2026-09-29 | Watayut A. | Use case descriptions as tables, grouped under 2.2; use case diagram redrawn. Changes CH-23, CH-24. | owner |
| 2.0 draft 4 | 2026-09-29 | Watayut A. | Every ADR written as a table of the template's five fields, each ADR on a new page. Change CH-25. | owner |
| 2.0 draft 5 | 2026-09-29 | Watayut A. | Figure 5.1 without overlaps: no arrow crosses a component or a label. Change CH-26. | owner |
| 2.0 draft 6 | 2026-09-29 | Watayut A. | Change log, resolution of feedback and known issues, and how to compare versions moved to Appendices A to C; open items removed; business rules listed in Section 3.3; the sources of the requirements are no longer cited. Change CH-27. | owner |
| 2.0 draft 7 | 2026-09-29 | Watayut A. | Glossary added as Section 6; business terms set in bold and linked to the glossary. Changes CH-28, CH-29. | owner |
| 2.0 draft 8 | 2026-09-29 | Watayut A. | The body no longer refers to the teacher's feedback outside the ADRs. Change CH-30. | owner |
| 2.0 draft 9 | 2026-09-29 | Watayut A. | Every use case description starts on a new page. Change CH-31. | owner |
| 2.0 draft 10 | 2026-09-29 | Watayut A. | Page layout: no heading alone at the foot of a page (5.3 now on the page of its figure, Figure 2.1 on the page of Section 2), contents on two pages. Change CH-32. | owner |
| 2.0 draft 11 | 2026-09-29 | Watayut A. | Parts of the system and how they communicate (Section 5.2; ADR-12: REST through the API Gateway, gRPC between the services). Section 5 limited to the MVP; the services completed by tracing the use cases through them, with the Staff Account Service added and traceability tables in Section 5.4; Figure 5.1 redrawn. Changes CH-33 to CH-38. | owner, KI-14, KI-15 |
| 2.0 draft 12 | 2026-09-30 | Watayut A. | Each operation of Table 5.3 is one function (create and update separated); the traceability tables follow the use cases step by step, one row per operation. Change CH-39. | owner |
