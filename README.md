# ε-Sufficient Context for Bounded Readers: Definitions and a Non-Monotonicity Result for Code Editing

Jude Castiel Johansen, Shockware Limited, independent researcher. ORCID 0009-0002-5644-3073.

A short note fixing definitions for *context sufficiency* when the editor is a
language model whose accuracy falls as input grows. It defines the change contract
(Δ, D, I), the notion of an *ε-sufficient context* relative to the best context rather
than the full repository, proves and mechanises that sufficiency is not closed under
superset, states the forward slice as a frame requirement, defines *context-closed*
languages, reports a mutation-based measurement of the forward-slice requirement on a real
Go repository, and reserves the benchmark name **SuffBench**. No language-model experiments
are reported.

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

Concept DOI (all versions): **[10.5281/zenodo.23282195](https://doi.org/10.5281/zenodo.23282195)**. Version 1.1 (current): [10.5281/zenodo.23282824](https://doi.org/10.5281/zenodo.23282824), tag `v1.1.0`. Version 1.0: [10.5281/zenodo.23282196](https://doi.org/10.5281/zenodo.23282196), tag `v1.0.0`. SuffBench specification: [10.5281/zenodo.23282863](https://doi.org/10.5281/zenodo.23282863). See `CITATION.cff`.
