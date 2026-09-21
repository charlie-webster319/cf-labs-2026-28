# Lecture resources

Open a PDF below to read the slides. **You do not need to compile anything or use an AI tool.** These copies cover Lectures 0–3; check Moodle for later updates.

| Lecture | Slides | Key concepts and terms |
| --- | --- | --- |
| 0 — Orientation Week | [Lecture PDF](lecture-0/lecture-slides.pdf) | No separate deck supplied |
| 1 — Compounding, discounting and investments | [Lecture PDF](lecture-1/lecture-slides.pdf) | [Key concepts PDF](lecture-1/key-concepts/key-concepts-and-terms.pdf) |
| 2 — Discount factors and cost of capital | [Lecture PDF](lecture-2/lecture-slides.pdf) | [Key concepts PDF](lecture-2/key-concepts/key-concepts-and-terms.pdf) |
| 3 — Stocks and bonds | [Lecture PDF](lecture-3/lecture-slides.pdf) | [Key concepts PDF](lecture-3/key-concepts/key-concepts-and-terms.pdf) |

On GitHub, click a PDF to view it or use **Download raw file** to download it. In Codespaces, use the Explorer to find this folder and right-click a PDF to download it if it does not preview.

The `.tex` files contain the editable slides. The other folders contain their images, diagrams, themes and numerical inputs. They also give optional AI assistants course context. The leading dot in this folder's name does **not** make its contents private.

## Optional: editable sources

Each lecture has `lecture-slides.tex`; Lectures 1–3 also have `key-concepts/key-concepts-and-terms.tex`. The copied sources include their compilation dependencies. Generated numerical inputs are included as a snapshot; the original data-processing scripts and research material remain in the teaching source repository.

For readers who already use LaTeX, compile from the directory containing the relevant `.tex` file, using XeLaTeX through `latexmk`:

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build lecture-slides.tex
```

For a key-concepts deck, run the same command inside its `key-concepts` directory, replacing the filename with `key-concepts-and-terms.tex`. This requires a separate TeX installation with the required packages and fonts, including Fira Sans and Fira Mono. LaTeX is not part of the lab environment. Compiled output goes into `build/`, preserving the supplied PDF.

## Provenance and use by assistants

Copied from `corporate-finance-slides` on 21 September 2026. All supplied PDFs are unchanged. Lecture 1's source and figure paths were adjusted so that it compiles from its own folder. [The manifest](manifest.json) records each original path, copied-file checksum and any path adjustment.

Read the relevant source when explaining a concept, and use the PDF to check diagrams and slide context. Identify the lecture and slide title when referring to the material. Distinguish the slides' statements from additional examples or explanations. Respect each example's stated assumptions: for example, Lecture 2 and Lab 2 can use different illustrative risk-free rates. Do not change a lab assumption just to match a lecture example.

This folder is a snapshot, not a live link to Moodle or the source repository. Update the PDFs and their corresponding sources together when teaching materials change.
