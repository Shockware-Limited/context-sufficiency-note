# Review checklist for the author (checkpoints C2 and C4)

Read the PDF, not the TeX. Tick each line only when you would defend it in public.

## Definitions (never cut)
- [ ] Contract C = (Δ, D, I) with conditions (a), (b), (c). Is (b) the frame you meant: behaviour unchanged outside D?
- [ ] Well-defined and precise are stated and are what you mean by "ambiguous request".
- [ ] Editor A is a distribution over edits; p_A(K, C) is success under oracle V.
- [ ] p*_A(C) is the max over all contexts, NOT the full repository. This is deliberate.
- [ ] ε-sufficient: p_A(K, C) ≥ p*_A(C) − ε. Minimal: no cheaper sufficient context.
- [ ] Assumption 1 (coverage × degradation) is labelled an assumption, not a theorem.
- [ ] The three reasons ε is irreducible are all present: stochastic editor, sampling, oracle incompleteness.

## Proposition and Lemma (Section 5)
- [ ] The prose model matches `sufficiency/README.md` line by line.
- [ ] Proposition hypotheses: u ∉ O, 0 ≤ ε < g(|O|) − g(|O|+1). Conclusion: O sufficient, O ∪ {u} not.
- [ ] The five-line proof reads correctly.
- [ ] Lemma: constant g gives closure under superset. Proof handles ε ≥ c and ε < c.
- [ ] Footnote cites file path, commit hash, repository URL, and "no sorry". Hash matches `git log`.

## Claims and wording
- [ ] No sentence says "without sacrificing correctness". Search the PDF for "sacrific".
- [ ] Every experimental statement is future tense. Search for "we show", "we found", "results".
- [ ] The forward-slice section is a Requirement, not a theorem, and says why.
- [ ] P1, P2, P3 are labelled Conjecture. No language is named.
- [ ] SuffBench is described as planned. "Nothing is released with this note" is present.
- [ ] Verification vs generation sufficiency distinction is present in Section 8.

## Related work and citations
- [ ] Every citation key in the PDF appears in `paper/VERIFICATION.md`.
- [ ] Spot-check three: open the DOI for Weiser 1984, Rothermel and Harrold 1997, and CodePlan 2024.
- [ ] Agentless is cited as the FSE 2025 published version "Demystifying LLM-Based Software Engineering Agents". OK?
- [ ] The MinCtx footnote is fair and factual.
- [ ] The one-sentence gap appears in Section 1 and again at the end of Section 9, and they agree.

## Front matter
- [ ] Name spelled exactly: Jude Castiel Johansen.
- [ ] Email castiel@shockware.co.uk. ORCID 0009-0002-5644-3073 links to your record.
- [ ] Title is the one you want. It will be in the DOI record forever.
- [ ] Page count is 4.

## Before C5 (publish)
- [ ] Cold read done on a different day from the first read.
- [ ] Repository made public. CI green.
- [ ] Zenodo metadata (`release/zenodo-metadata.json`) matches the PDF front matter.
- [ ] You have revoked the Zenodo token that was pasted into chat and minted a fresh one.
