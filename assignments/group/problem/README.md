# Problem statements of the group deliverables

The briefs as posted in MyCourseVille, one folder per deliverable, kept as given (read-only). Due dates and weights come
from the syllabus weekly plan, week 5 (`materials/syllabus/md/` at the repository root).

| Deliverable | Brief | Due | Weight | Handed in |
|---|---|---|---|---|
| #1 Project Description and ADRs | [deliverable-1/problem.txt](deliverable-1/problem.txt): project name, members, problem description, target customers, at least 3 use cases with descriptions, a use case diagram consistent with them, functional and non-functional requirements, at least 3 ADRs (samples in [../workspace/received/examples/](../workspace/received/examples/)) | 8 / 12 Sep 2026 | 5% + 3% | [Deliverable-1.pdf](../deliverables/report/Deliverable-1.pdf) |
| #2 Microservice Design with Collaborations | [deliverable-2/problem.txt](deliverable-2/problem.txt): the Service–Operations–Collaborators table and the architecture diagram, covering the group's 3 business use cases, with ten design guidelines | Wednesday group 8 Sep, Sunday group 12 Sep 2026 | 2% | [Deliverable-2.pdf](../deliverables/report/Deliverable-2.pdf) |
| #3 Project progress 1 | [deliverable-3/problem.txt](deliverable-3/problem.txt): a demo video under 5 minutes of one or more REST services with CRUD and one or more gRPC services with CRUD, plus the project proposal with updated ADRs and an updated microservice design | 3 Oct 2026 for both sections: the Wednesday section's 29 Sep was extended because of the floods ([announcement](deliverable-3/due-date-extension.txt)) | 5% (progress 1 of 3, including Git contribution) | not yet |

Images posted with the Deliverable #2 announcement, all showing FTGO, the running example of Richardson's *Microservices
Patterns*:

| File | Content |
|---|---|
| [deliverable-2/Col.png](deliverable-2/Col.png) | FTGO Service–Operations–Collaborators table |
| [deliverable-2/Mic.png](deliverable-2/Mic.png) | FTGO microservice architecture diagram: API Gateway, services with REST APIs and private databases, adapters to Stripe, Twilio and Amazon SES |
| [deliverable-2/Microservice.png](deliverable-2/Microservice.png) | Lecture slide "Solution: microservice architecture": the same diagram with the actors (people) and the adapters to external systems marked |
| [deliverable-2/Monolith.png](deliverable-2/Monolith.png) | Lecture slide "Traditional: Monolithic architecture": FTGO as a monolith, with the actors, the logical view and the implementation view marked; a MyCourseVille tooltip covers part of it |

For #3, the updated ADRs and microservice design are where the teacher feedback in [../workspace/received/teacher/](../workspace/received/teacher/) and the open issues in [../workspace/notes/known-issues.md](../workspace/notes/known-issues.md) can be addressed.
