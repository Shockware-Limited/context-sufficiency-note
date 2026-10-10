# Review checklist for the author (your cold read before publishing)

Read the PDF, not the TeX. Tick each line only when you would defend it in public.
The AI-use disclosure at the end of the note says you did this. Do not publish until it is true.

## Definitions (Sections 3 and 4)
- [ ] Contract C = (Δ, D, I, W) with conditions (a) to (d). Is (b) the frame you meant, and does (d) confine the edit to W as you intend?
- [ ] Oracle: sound means pass ⇒ ⊨ C; complete means ⊨ C ⇒ pass. The residual is the unsoundness set. Check the direction twice; the first draft had it inverted.
- [ ] p* is a max over a stated candidate family K, not over the full repository.
- [ ] ε-sufficient: p_A(K, C) ≥ p* − ε. Cost-minimum, default cost = load (tokens).
- [ ] Assumption 1: coverage is DEFINED as p / g, so the factorisation is identified only once g is pinned down. Is that acceptable to you?
- [ ] The SWE-bench hidden-tests argument against binary coverage is stated and cited to Jimenez et al.
- [ ] Hypothesis 1 (portability of g) is labelled a hypothesis.

## Proposition and Lemma (Section 5)
- [ ] The prose Proposition matches `prop1` in `sufficiency/README.md` hypothesis for hypothesis.
- [ ] The drop formula r(K)(g|K| − g(|K|+|S|)) is stated and proved.
- [ ] The concrete example (g = 1/(ℓ+1), |O| = 1, three irrelevant units, 1/2 → 1/5) is arithmetically right.
- [ ] Lemma 1: constant g plus monotone coverage gives superset closure; monotone coverage is an assumption, motivated by Good's principle.
- [ ] Footnote: file path, commit hash, repository URL, "no sorry", axiom audit. Hash matches `git log` for the last change to NonMonotonic.lean.

## Forward slice and Properties (Sections 6 and 7)
- [ ] Hypothesis 2 states well-foundedness, compositionality, and sound over-approximation.
- [ ] Rothermel and Harrold's controlled regression testing assumption is described as "everything other than the code is held fixed", not as the over-approximation claim.
- [ ] Requirement 1 says soundness for the frame REQUIRES the F(W) checks and does not follow from them.
- [ ] The editor-side claim (seeing dependents helps) is labelled untested.
- [ ] P1 to P3 are Properties, not conjectures. P1 is about the behaviour set Φ_u. P3 uses the interface write-set W_I and is computable before the edit.

## Measurement (Section 8)
- [ ] The "what the package graph can and cannot see" paragraph: in Go, F(W) = packages whose test binaries link W, so in-process channels are inside F(W) by construction. Agree?
- [ ] Classes are exclusive; Wilson intervals are shown; the forward-slice-only rate is stratified by whether W has its own tests.
- [ ] Flake control: three clean-tree reruns of every failing package; flaky packages removed. The count of flaky packages appears in the text.
- [ ] Threats list includes: operator imbalance, vet, timeouts, concurrency interference, inherited HOME, one platform, package granularity, tokenizer proxy.
- [ ] "relates to" regression test selection, not "replicates".
- [ ] Every number in Table 1 comes from `experiments/results/` via `analyze.py` and `context_sizes.py`; re-run both yourself and compare.

## Related work and citations
- [ ] Every citation key appears in `paper/VERIFICATION.md` (32 entries). Spot-check three DOIs yourself.
- [ ] Joren et al. "Sufficient Context" is cited and distinguished in Section 1 and Section 10.
- [ ] Good's principle is stated with "cost-free".
- [ ] Slicing is not described as assuming "more information never hurts".
- [ ] The one-sentence gap appears once, in Section 1.

## Front matter and disclosure
- [ ] Name, email, ORCID correct. Title is the one you want; it goes into the DOI record permanently.
- [ ] The disclosure names the exact models, the sections affected, your review of the work, and that AI tools are not authors. The name "Lemma" appears as the name you gave the system, inside that disclosure, nowhere else.
- [ ] You have re-run `lake build` in `sufficiency/` and `analyze.py` yourself, because the disclosure says you did.

## Before publishing
- [ ] Repository made public; CI green on the final commit; the commit cited in the footnote is reachable on GitHub.
- [ ] `release/zenodo-metadata.json` title and abstract match the PDF.
- [ ] Final PDF re-stamped with OpenTimestamps.
- [ ] You have revoked the first Zenodo token pasted into chat (it was a production token) and minted a fresh one for the publish step.
