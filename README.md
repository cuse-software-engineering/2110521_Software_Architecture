# 2110521 Software Architecture — course materials

Chulalongkorn University, Department of Computer Engineering, first semester 2569 (2026). Course leader: Pittipol Kantavat.

| Folder | Contents |
|---|---|
| [syllabus/](syllabus/) | Course syllabus dated 3 Aug 2026: PDF, page images, and a [Markdown transcription](syllabus/2110521_SWARCH_Syllabus_2026_%283Aug2026%29-360766-17857484604550.md) with the grading scheme, 16-week plan, textbooks, and term-project requirements |
| [lecture-slide/](lecture-slide/) | One folder per lecture deck with the PDF, per-slide PNGs, and a Markdown transcription. See its [README](lecture-slide/README.md) for the index |
| [samples/](samples/) | ADR template and example ADRs (good, bad, and gold-standard) from the ADR lecture. See its [README](samples/README.md) |
| [assignments/individual/](assignments/individual/) | Individual assignments: `01-keywords` (homework 1, fifty keywords from lecture 1), `rest-api-demo` (Tutorial 1, REST) and `grpc-restaurant-demo` (Tutorial 2, gRPC) |
| [assignments/group/](assignments/group/) | Group term-project assignments: `deliverable-1` (project proposal, use cases, requirements, ADRs) |

## Conventions

- Every extracted document keeps its original file name; the transcription is `<same base name>.md` in the same folder.
- Page images live in `png/` next to the source, rendered at 110 DPI, named `page-NN.png` (three digits when a document has 100 or more pages). These folders are generated locally and are not committed (`png/` is in `.gitignore`), so the slide images embedded in the transcriptions only render after you regenerate them with the snippet in [lecture-slide/README.md](lecture-slide/README.md).
- Transcriptions keep the authors' wording, including typos, and only repair extraction artifacts such as dropped Thai vowels and tone marks.
