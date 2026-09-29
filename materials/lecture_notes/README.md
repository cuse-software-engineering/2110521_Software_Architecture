# Lecture slides — 2110521 Software Architecture

One folder per lecture. Each folder holds the original PDF, a Markdown transcription with the same base name in `md/`, and a `png/` folder with one image per slide (rendered at 110 DPI). The transcription embeds a slide image only where the visual carries the meaning; the `png/` folder always has every page. The `png/` folders are not committed to git; regenerate them all with `python3 tools/render_pages.py --all` from the repository root.

| Folder | Lecture | Instructor | Slides | Transcription |
|---|---|---|---|---|
| [intro-swarch/](intro-swarch/) | Introduction to Software Architecture (lecture 1: syllabus, 5W2H of architecture) | Pittipol Kantavat and course team | 121 | [1_Intro_to_SWARCH-5208-17858972097633.md](intro-swarch/md/1_Intro_to_SWARCH-5208-17858972097633.md) |
| [adrs/](adrs/) | Architectural Decision Record (ADR) | Duangdao Wichadakul and course team | 81 | [ADRs_2026-13578-17883142164608.md](adrs/md/ADRs_2026-13578-17883142164608.md) |
| [ddd/](ddd/) | Domain Driven Design (DDD) | Duangdao Wichadakul | 91 | [DDD_2026-13578-17883142498154.md](ddd/md/DDD_2026-13578-17883142498154.md) |
| [microservice-patterns/](microservice-patterns/) | Introduction to Microservice Architecture (Richardson, Microservices Patterns ch. 1) | Pittipol Kantavat | 60 | [Intro_to_Microservice_Patterns-360766-17550117624043.md](microservice-patterns/md/Intro_to_Microservice_Patterns-360766-17550117624043.md) |
| [rest/](rest/) | REST API | Nuengwong Tuaycharoen | 54 | [REST_2023-336264-16934100818671.md](rest/md/REST_2023-336264-16934100818671.md) |
| [grpc/](grpc/) | gRPC | Nuengwong Tuaycharoen | 73 | [gRPC_2026-336264-17888710746387.md](grpc/md/gRPC_2026-336264-17888710746387.md) |

## Adding a new deck

1. Create a folder with a short lowercase slug and move the PDF into it.
2. Render the pages into `png/` next to the PDF (110 DPI, `page-NN.png`, three digits when the deck has 100 or more pages):

   ```sh
   python3 tools/render_pages.py materials/lecture_notes/<slug>/<deck>.pdf
   ```

3. Write `md/<same base name>.md` in the deck's folder, following the layout of the existing transcriptions: title, instructor, a "Transcribed from" note, then one `## Slide N — Title` section per slide grouped into `# Part N` sections, with `![Slide N](../png/page-NN.png)` embedded for diagram slides.
4. Add a row to the table above.
