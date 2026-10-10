# Lean mechanisation

Lean 4 + Mathlib development accompanying the note
*ε-Sufficient Context: Definitions for Code Editing by Bounded Readers*.

Build: `lake exe cache get && lake build`. The development contains no `sorry`
(checked in CI by `grep`).

## Correspondence between the note and the Lean source

File: `Sufficiency/NonMonotonic.lean`.

| In the note (Section 5) | In Lean | Notes |
|---|---|---|
| finite type of units | `U : Type*` with `[DecidableEq U]`, contexts are `Finset U` | finiteness of each context is built into `Finset` |
| oracle slice `O` | `O : Finset U` | |
| degradation curve `g : ℕ → ℚ`, `g ≥ 0` | `structure Reader` with fields `g` and `nonneg` | |
| `p(K) = g(|K|)` if `O ⊆ K`, else `0` | `def success` | |
| `p* = g(|O|)` | `def optimum` | |
| "if `g` is non-increasing then `p(K) ≤ g(|O|)`" | `theorem success_le_optimum` (hypothesis `Antitone R.g`) | justifies the name *optimum* |
| "`K` is ε-sufficient iff `p(K) ≥ g(|O|) − ε`" | `def sufficient` | |
| **Proposition** | `theorem not_superset_closed` | exactly the stated hypotheses `u ∉ O`, `0 ≤ ε`, `ε < g(|O|) − g(|O|+1)`; conclusion is the conjunction in the note |
| "let `g` be strictly decreasing" (non-vacuity) | `theorem not_superset_closed_of_strictAnti` | shows that under `StrictAnti g` some ε (namely 0) satisfies the Proposition's bound |
| **Lemma** (lossless case closed under superset) | `theorem const_superset_closed` | `g` constant with value `c`; any `ε` |

## What is and is not mechanised

Mechanised: the Proposition, its non-vacuity, the Lemma, and the optimum bound,
all in the simplest form of the coverage-times-degradation model (binary coverage).

Not mechanised, and not claimed to be: the general factoring (Assumption 1 of the note),
the contract definition, the forward-slice requirement, and conjectures P1–P3.
