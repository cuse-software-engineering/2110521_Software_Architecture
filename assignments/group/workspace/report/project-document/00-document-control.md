# 0 Document Control

## 0.1 Document Information

*Table 0.1 Document information*

| | |
|---|---|
| Document | Project Description, ADRs, Microservice Design and API Specification of the Seating & Event Availability Tracking System (SEATS) |
| Product name | SEATS; Deliverables #1 and #2 called the system Concert Table Reservation System (CTRS) |
| Course | 2110521 Software Architecture, Semester 1, Academic Year 2026 |
| Group | SE 101 |
| Version | 2.0 draft 33, 30 September 2026 |
| Status | Draft for review by the group; basis of the updated ADRs and microservice design of Deliverable #3 |
| Previous version | 1.1: Deliverable #1 (version 1.0) and Deliverable #2 as submitted on 8 September 2026 |
| Changes | The change log is a separate document of the same version, "SEATS Project Document — Change Log": every change since version 1.1 (CH-nn), how each teacher comment and known issue was resolved, and how to compare the versions |

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
| 2.0 draft 13 | 2026-09-30 | Watayut A. | Figure 5.1: the API Gateway carries the REST tab that the Frontend calls. Change CH-40. | owner |
| 2.0 draft 14 | 2026-09-30 | Watayut A. | Section 5.1 maps each service to its bounded context and subdomain. Change CH-41. | owner |
| 2.0 draft 15 | 2026-09-30 | Watayut A. | Table 5.3 lists exposed operations only: the two timer jobs and the two internal steps are described below it; previewRound() and editPublishedRound() removed, listTableTypes() added. Change CH-42. | owner |
| 2.0 draft 16 | 2026-09-30 | Watayut A. | Section 5.4 is a one-page matrix of operations by use case; the step-by-step trace tables move to Appendix D. Change CH-43. | owner |
| 2.0 draft 17 | 2026-09-30 | Watayut A. | Table 5.1 lists every component of each part with its responsibility, the API it offers and the data it owns. Change CH-44. | owner |
| 2.0 draft 18 | 2026-09-30 | Watayut A. | One term for each thing (concert round, zone map, e-ticket; UC-02 and UC-03 renamed); the domain model as Section 2.3 (class diagram, entities, booking state machine); UC-05 to UC-08 added by name to the diagram, Table 2.1 and the matrix. Changes CH-45 to CH-47. | owner |
| 2.0 draft 19 | 2026-09-30 | Watayut A. | The change log, the resolution table and the comparison note are a separate document; the operations-by-use-case matrix is Appendix A with the step-by-step tables; the business rules are Appendix B. Change CH-48. | owner |
| 2.0 draft 20 | 2026-09-30 | Watayut A. | Glossary split into business terms (Table 6.1, bold in the text) and technology and project terms (Table 6.2, 21 terms, plain in the text). Change CH-49. | owner |
| 2.0 draft 21 | 2026-09-30 | Watayut A. | UC-09 Maintain Customer Profile and UC-10 Pay the Full Table Fee, included by UC-01, with full descriptions; UC-01 renumbered from step 12; matrix and trace tables follow. Change CH-50. | owner |
| 2.0 draft 22 | 2026-09-30 | Watayut A. | Chapter 6 Domain Model and API Specification (the domain model moved from 2.3, the data model per service, the model-to-contract rule, the REST and gRPC contracts of every service); the glossary is Appendix C; ADR-13 makes the booking the owner of the hold and the table map a read model, and initializeRoundTableStatus() is createRoundTableStatus(). Changes CH-51, CH-52. | owner |
| 2.0 draft 23 | 2026-09-30 | Watayut A. | The associations table of the domain model is dropped; the two rules it carried are in the entity definitions. Change CH-53. | owner |
| 2.0 draft 24 | 2026-09-30 | Watayut A. | ADR-12 changed in place: the API Gateway is the only REST API and turns each route into one gRPC call, and every service has one gRPC API (Figure 5.1, Tables 5.1, 5.2 and 6.3 to 6.7, glossary). Change CH-54. | owner |
| 2.0 draft 25 | 2026-09-30 | Watayut A. | Section 6.4 reorganized: the gRPC API of each service with request and response messages in separate columns (Tables 6.4 to 6.7), the fields of the messages (Table 6.8) and the public routes of the API Gateway with their roles (Table 6.9). Change CH-55. | owner |
| 2.0 draft 26 | 2026-09-30 | Watayut A. | Table 6.9 names the web app that calls each route of the API Gateway. Change CH-56. | owner |
| 2.0 draft 27 | 2026-09-30 | Watayut A. | UC-01 restored: its preconditions, postconditions, Basic Flow heading and steps 1 to 11 had been lost in draft 21; Appendix D Screens and the Routes They Call. Changes CH-57, CH-58. | owner |
| 2.0 draft 28 | 2026-09-30 | Watayut A. | Chapter 6 grouped by service: after the domain model and the model-to-contract rule, one section per service with its data model, gRPC API and messages (6.3 to 6.6), then the API Gateway with its routes (6.7). Change CH-59. | owner |
| 2.0 draft 29 | 2026-09-30 | Watayut A. | Appendix D gains the wireframes of the sixteen screens (Figures D.1 to D.9). Change CH-60. | owner |
| 2.0 draft 30 | 2026-09-30 | Watayut A. | Table D.1 gives one page per customer screen with the wireframe beside its description; the back-office figures are D.1 to D.6. Change CH-61. | owner |
| 2.0 draft 31 | 2026-09-30 | Watayut A. | Appendix D: one page per screen for both web apps (Tables D.1 to D.16), each with the wireframe, one row per concern and an example call. Change CH-62. | owner |
| 2.0 draft 32 | 2026-09-30 | Watayut A. | Chapter 6 links each contract to its file in the code repository; Table 6.11 gains a Status column with the answers of each route. Change CH-63. | owner |
| 2.0 draft 33 | 2026-09-30 | Watayut A. | Table 6.11 is the public REST API alone; Table 6.12 maps the routes onto the gRPC methods. Change CH-64. | owner |
