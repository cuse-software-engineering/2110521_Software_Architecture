# Group project: SEATS, 2110521 Software Architecture

Term project of group SE 101: the Seating & Event Availability Tracking System (SEATS), called Concert Table Reservation System (CTRS) in Deliverables #1 and #2, the same system the 2110628 Requirements
Engineering and 2110722 Software Project Management courses work on. This course designs its architecture deliverable
by deliverable: use cases, requirements and Architectural Decision Records (ADRs) in Deliverable #1, services and the
architecture diagram in Deliverable #2.

One folder per kind of thing, as in the 2110628 repository. What is handed in lives only in `deliverables/`.

| Folder | What it holds | Edit? |
|---|---|---|
| `problem/` | The brief of each deliverable as posted in MyCourseVille, `deliverable-N/problem.md`, with the FTGO example images posted with Deliverable #2. See its README for due dates and weights. | no |
| `deliverables/report/` | What was handed in: `Deliverable-1.pdf` (32 pages: problem, use cases, requirements, ADRs) and `Deliverable-2.pdf` (8 pages: Service–Operations–Collaborators table, architecture diagram). | only by copying the submitted file |
| `workspace/report/deliverable-1/` | Frozen transcription of Deliverable #1 as submitted: `Deliverable-1.md`, split into `use-cases.md`, `requirements.md` and `adr.md`. `assets/` holds the use case diagram extracted from the PDF and the venue's printed zone map. | no (as submitted) |
| `workspace/report/deliverable-2/` | Frozen transcription of Deliverable #2 as submitted: `Deliverable-2.md`, with the service table and a transcription of the diagram. `assets/architecture-diagram.png` is the diagram extracted from the PDF. | no (as submitted) |
| `workspace/report/project-document/` | **The living project document** (version 2.0 draft 14): Deliverables #1 and #2 fixed after the teacher feedback and the known issues, one file per part (00 document control with document information and revision history, 01 project description, 02 use cases, 03 requirements with the business rules, 04 ADRs, 05 microservice design, 06 glossary, 07 appendices: change log, resolution of feedback and known issues, how to compare versions), figures and their sources in `assets/`. Baselines are git tags: `doc-v1.1-submitted` (as submitted), `doc-v2.0-draft1` to `doc-v2.0-draft10`. | yes (the source for Deliverable #3) |
| `workspace/report/build/` | Working builds (ignored): the PDF from `tools/build_report.py` and the redlines from the top-level `tools/redline.py`. | no |
| `tools/` | `build_report.py` (PDF of the project document, reusing the 2110628 report builder), `draw_use_case_diagram.py` (Figure 2.1 in the style of the 2110628 use case diagram), `draw_architecture.py` (Figure 5.1). | yes |
| `workspace/report/deliverable-N/png/` | Page images of each handed-in PDF (ignored). Render with `python3 tools/render_pages.py --all` from the repository root. | no |
| `workspace/notes/known-issues.md` | Inconsistencies found in the submitted deliverables (KI-01 to KI-13), not fixed yet. | yes |
| `workspace/received/teacher/` | Teacher feedback on each deliverable, kept as received, with the points still to act on. | no (except the points) |
| `workspace/received/examples/` | Material received with the ADR lecture, one folder per document with the original, its transcription in `md/` and page images in `png/` (ignored): the course's ADR template (Nygard), two example ADR sets, a counter-example and the gold-standard "Go Gold" proposal. See its README. | no |

The term-project requirements and deliverable schedule are in the syllabus transcription,
`materials/syllabus/md/` at the repository root.

Build and compare (from the repository root):

```
python3 assignments/group/tools/build_report.py              # PDF of the project document -> workspace/report/build/
python3 tools/redline.py --head doc-v2.0-draft1 --pdf        # what changed since the submitted version 1.1
python3 assignments/group/tools/draw_use_case_diagram.py      # redraw Figure 2.1
python3 assignments/group/tools/draw_architecture.py         # redraw Figure 5.1 after editing its coordinates
```
