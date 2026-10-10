# ε-Sufficient Context: Definitions for Code Editing by Bounded Readers

Jude Castiel Johansen, Independent researcher. ORCID 0009-0002-5644-3073.

A four-page note fixing definitions for *context sufficiency* when the editor is a
language model whose accuracy falls as input grows. It defines the change contract
(Δ, D, I), the notion of an *ε-sufficient context* relative to the best context rather
than the full repository, proves and mechanises that sufficiency is not closed under
superset, states the forward slice as a frame requirement, defines *context-closed*
languages, and reserves the benchmark name **SuffBench**. No experiments are reported.

| Item | Where |
|---|---|
| The note (LaTeX) | `paper/main.tex`, bibliography `paper/refs.bib` |
| Citation verification log | `paper/VERIFICATION.md` |
| Lean 4 mechanisation | `sufficiency/` (see `sufficiency/README.md` for the theorem-to-prose map) |
| Reviewer checklist | `REVIEW.md` |
| Release metadata | `release/` |

Build the PDF with [Tectonic](https://tectonic-typesetting.github.io): `cd paper && tectonic main.tex`.
Build the proofs: `cd sufficiency && lake exe cache get && lake build`.

## Licence

Text and PDF: CC-BY-4.0 (`LICENSE-CC-BY-4.0`). Code, including the Lean development: Apache-2.0 (`LICENSE`).

## Citing

See `CITATION.cff`. A DOI will be added on release.
