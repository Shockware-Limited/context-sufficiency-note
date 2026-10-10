# Lean mechanisation

Lean 4 + Mathlib development accompanying the note
*ε-Sufficient Context for Bounded Readers*.

Build: `lake exe cache get && lake build`. The development contains no `sorry`, `admit`,
or `native_decide` (checked in CI), and every theorem depends only on the standard axioms
`propext`, `Classical.choice`, `Quot.sound` (audited in CI via `Axioms.lean`).

## Model (file `Sufficiency/NonMonotonic.lean`)

| In the note (Section 5) | In Lean | Notes |
|---|---|---|
| finite set of units `U` | `U : Type*` with `[Fintype U] [DecidableEq U]`; contexts are `Finset U` | |
| degradation curve `g : ℕ → [0,1]` | `structure Reader` with `g`, `nonneg`, `le_one` | |
| coverage `r : 2^U → [0,1]`, no shape assumed | `structure Coverage` with `r`, `nonneg`, `le_one` | binary coverage is one instance, `binCov` |
| `p(K) = r(K) · g(|K|)` | `def success` | |
| `p* = max_K p(K)` | `def optimum` as `Finset.sup'` over the powerset of `univ` | a genuine maximum, so Definition 2 is mechanised as stated |
| `K` is ε-sufficient iff `p(K) ≥ p* − ε` | `def sufficient` | |
| `S` irrelevant to `K`: `r(K ∪ S) = r(K)` | `def Irrelevant` | |

## Results

| In the note | In Lean | Hypotheses |
|---|---|---|
| `p(K) ≤ p*`, and `p*` is attained | `success_le_optimum`, `exists_maximiser` | none |
| adding a non-empty irrelevant set strictly lowers success | `success_union_lt` | `StrictAnti g`, `r(K) > 0`, `S ≠ ∅`, `K ∩ S = ∅` |
| **Proposition** (k-step): maximiser `K`, any `K'` with lower success, every `ε` below the drop | `not_superset_closed` | `success K = optimum` |
| the Proposition is not vacuous | `not_superset_closed_nonvacuous` | as `success_union_lt` |
| **Lemma**: lossless reader ⇒ superset-closed | `const_superset_closed` | `g` constant, `r` monotone under `⊆` |
| binary instance: `p* = g(|O|)` | `binCov_optimum` | `Antitone g` |
| binary instance of the Proposition | `binCov_not_superset_closed` | `StrictAnti g`, `S ≠ ∅`, `O ∩ S = ∅`, `0 ≤ ε < g(|O|) − g(|O|+|S|)` |

## What is and is not mechanised

Mechanised: everything in the two tables above.

Not mechanised, and not claimed to be: the contract definition, the relation between the
oracle `V_C` and `⊨ C`, the forward-slice requirement, Properties P1–P3, and anything about
real editors or real repositories.
