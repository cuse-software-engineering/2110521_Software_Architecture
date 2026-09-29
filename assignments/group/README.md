# Group project: CTRS, 2110521 Software Architecture

Term project of group SE 101: the Concert Table Reservation System (CTRS), the same system the 2110628 Requirements
Engineering and 2110722 Software Project Management courses work on. This course designs its architecture deliverable
by deliverable: use cases, requirements and Architectural Decision Records (ADRs) in Deliverable #1, services and the
architecture diagram in Deliverable #2.

One folder per kind of thing, as in the 2110628 repository. What is handed in lives only in `deliverables/`.

| Folder | What it holds | Edit? |
|---|---|---|
| `problem/` | The brief of each deliverable as posted in MyCourseVille, `deliverable-N/problem.txt`, with the FTGO example images posted with Deliverable #2. See its README for due dates and weights. | no |
| `deliverables/report/` | What was handed in: `Deliverable-1.pdf` (32 pages: problem, use cases, requirements, ADRs) and `Deliverable-2.pdf` (8 pages: Service–Operations–Collaborators table, architecture diagram). | only by copying the submitted file |
| `workspace/report/deliverable-1/` | Markdown transcription of Deliverable #1: `Deliverable-1.md`, split into `use-cases.md`, `requirements.md` and `adr.md`. `assets/` holds the use case diagram extracted from the PDF and the venue's printed zone map. | yes (base for the next deliverables) |
| `workspace/report/deliverable-2/` | Markdown transcription of Deliverable #2: `Deliverable-2.md`, with the service table and a transcription of the diagram. `assets/architecture-diagram.png` is the diagram extracted from the PDF. | yes |
| `workspace/report/deliverable-N/png/` | Page images of each handed-in PDF (ignored). Render with `python3 tools/render_pages.py --all` from the repository root. | no |
| `workspace/notes/known-issues.md` | Inconsistencies found in the submitted deliverables (KI-01 to KI-13), not fixed yet. | yes |
| `workspace/received/teacher/` | Teacher feedback on each deliverable, kept as received, with the points still to act on. | no (except the points) |
| `workspace/received/examples/` | Material received with the ADR lecture, one folder per document with the original, its transcription in `md/` and page images in `png/` (ignored): the course's ADR template (Nygard), two example ADR sets, a counter-example and the gold-standard "Go Gold" proposal. See its README. | no |

The term-project requirements and deliverable schedule are in the syllabus transcription,
`materials/syllabus/md/` at the repository root.
