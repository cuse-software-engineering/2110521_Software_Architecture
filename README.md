# 2110521 Software Architecture

สถาปัตยกรรมซอฟต์แวร์ — Department of Computer Engineering, Chula Engineering, Chulalongkorn University.

## Course Information

| | |
|---|---|
| **Course code** | 2110521 |
| **Course title** | Software Architecture (สถาปัตยกรรมซอฟต์แวร์), 3 credits |
| **Academic year** | 2026 (2569) / Semester 1 |

## Staff

- **Course leader:** รศ.ดร.พิตติพล คันธวัฒน์ (Assoc. Prof. Dr. Pittipol Kantavat)
- Other instructors are listed in the syllabus transcription, `materials/syllabus/md/`.

## Student

- **Name:** Watayut Aiamanan
- **Student ID:** 6970267821

## Project Structure

Same layout as the 2110628 Requirements Engineering repository of the same student.

```
assignments/
  individual/<NN>/    Individual assignments
    01/               Homework 1: fifty keywords from lecture 1
    02/               Tutorial 1, REST: CTRS FloorPlan REST API (Node.js, Express, MongoDB) + demo video script
    03/               Tutorial 2, gRPC: the lecture's restaurant sample moved onto MongoDB + demo video script
  group/              The term project (CTRS): architecture deliverables of group SE 101
    problem/          The brief of each deliverable (deliverable-N/problem.txt + images); read-only
    workspace/        report/deliverable-N/ = markdown of each deliverable; notes/ = known issues;
                      received/teacher/ = feedback; received/examples/ = ADR samples
    deliverables/     What was handed in: report/ (Deliverable-1.pdf, Deliverable-2.pdf)
materials/
  syllabus/                  Course syllabus (3 Aug 2026): PDF + md/ transcription
  lecture_notes/<topic>/     Lecture deck PDFs, with md/ transcriptions and png/ page images; index in its README
tools/
  render_pages.py            Render PDF pages to png/ (110 DPI, page-NN.png), the images the transcriptions embed
```

Individual assignments follow a four-way split:

| Folder | Contents |
|---|---|
| `problem/` | The task as given: the assignment brief and any starter code handed out (03: `restaurant.zip`). Read-only reference, never edited. |
| `workspace/` | Everything used to work toward the answer: code, drafts, notes, source diagrams, video scripts. |
| `tools/` | Build scripts specific to that assignment. Scripts useful across *all* assignments live in the top-level `tools/` instead. |
| `report/` | Only the final deliverable(s) actually submitted, nothing else. |

The group project uses the same split once at `assignments/group/`, with `deliverables/` in place of `report/`
(see [assignments/group/README.md](assignments/group/README.md)).

## Conventions

- Every extracted document keeps its original file name; the transcription is `md/<same base name>.md` in the
  document's folder.
- Page images live in `png/` next to the source, rendered at 110 DPI, named `page-NN.png` (three digits when a
  document has 100 or more pages). These folders are generated locally and are not committed (`png/` is in
  `.gitignore`), so the images embedded in the transcriptions only render after `python3 tools/render_pages.py --all`.
- Transcriptions keep the authors' wording, including typos, and only repair extraction artifacts such as dropped
  Thai vowels and tone marks.
