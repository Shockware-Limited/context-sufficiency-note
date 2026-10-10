/-
Copyright (c) 2026 Jude Castiel Johansen. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Jude Castiel Johansen
-/
import Mathlib

/-!
# Non-monotonicity of ε-sufficient context

Mechanisation of the Proposition and the Lemma in Section 5 of
"ε-Sufficient Context: Definitions for Code Editing by Bounded Readers".

Model.  Units form a type `U`.  A context is a `Finset U`.  The oracle slice
`O : Finset U` is the set of units that determine the verdict.  A `Reader`
has a degradation curve `g : ℕ → ℚ`, non-negative, giving success as a
function of context size.  Success on `K` is `g |K|` if `O ⊆ K`, else `0`.
The optimum is `g |O|`.  `K` is ε-sufficient iff `success ≥ optimum − ε`.
-/

namespace Sufficiency

variable {U : Type*} [DecidableEq U]

/-- A bounded reader: a non-negative degradation curve over context size. -/
structure Reader where
  /-- success as a function of context size -/
  g : ℕ → ℚ
  /-- success is a non-negative quantity -/
  nonneg : ∀ n, 0 ≤ g n

/-- Coverage-times-degradation success, with binary coverage of the oracle slice `O`. -/
def success (R : Reader) (O K : Finset U) : ℚ :=
  if O ⊆ K then R.g K.card else 0

/-- The optimum `p*`, attained at `K = O` whenever `g` is antitone. -/
def optimum (R : Reader) (O : Finset U) : ℚ :=
  R.g O.card

/-- `K` is ε-sufficient for oracle slice `O` under reader `R`. -/
def sufficient (R : Reader) (ε : ℚ) (O K : Finset U) : Prop :=
  optimum R O - ε ≤ success R O K

/-- When `g` is antitone, no context beats `K = O`.  Justifies calling `g |O|` the optimum. -/
theorem success_le_optimum (R : Reader) (hg : Antitone R.g) (O K : Finset U) :
    success R O K ≤ optimum R O := by
  unfold success optimum
  split_ifs with h
  · exact hg (Finset.card_le_card h)
  · exact R.nonneg _

theorem success_self (R : Reader) (O : Finset U) : success R O O = R.g O.card := by
  simp [success]

/-- The oracle slice itself is ε-sufficient for every ε ≥ 0. -/
theorem self_sufficient (R : Reader) {ε : ℚ} (hε : 0 ≤ ε) (O : Finset U) :
    sufficient R ε O O := by
  unfold sufficient optimum
  rw [success_self]
  linarith

/-- **Proposition (sufficiency is not closed under superset).**
For `u ∉ O` and `0 ≤ ε < g |O| − g (|O|+1)`, `O` is ε-sufficient and `O ∪ {u}` is not. -/
theorem not_superset_closed (R : Reader) (O : Finset U) {u : U} (hu : u ∉ O)
    {ε : ℚ} (hε0 : 0 ≤ ε) (hε : ε < R.g O.card - R.g (O.card + 1)) :
    sufficient R ε O O ∧ ¬ sufficient R ε O (insert u O) := by
  refine ⟨self_sufficient R hε0 O, ?_⟩
  unfold sufficient success optimum
  rw [Finset.card_insert_of_notMem hu]
  split_ifs with hs
  · intro h
    linarith
  · exact absurd (Finset.subset_insert u O) hs

/-- The hypothesis of the Proposition is satisfiable whenever `g` is strictly decreasing:
`ε = 0` is a witness.  So the Proposition is not vacuous. -/
theorem not_superset_closed_of_strictAnti (R : Reader) (hg : StrictAnti R.g)
    (O : Finset U) {u : U} (hu : u ∉ O) :
    ∃ ε : ℚ, 0 ≤ ε ∧ sufficient R ε O O ∧ ¬ sufficient R ε O (insert u O) := by
  refine ⟨0, le_rfl, not_superset_closed R O hu le_rfl ?_⟩
  have : R.g (O.card + 1) < R.g O.card := hg (Nat.lt_succ_self _)
  linarith

/-- **Lemma (the lossless case is closed under superset).**
If `g` is constant, ε-sufficiency is preserved by taking supersets. -/
theorem const_superset_closed (R : Reader) (c : ℚ) (hc : ∀ n, R.g n = c) {ε : ℚ}
    (O K K' : Finset U) (hKK' : K ⊆ K') (h : sufficient R ε O K) :
    sufficient R ε O K' := by
  have hc0 : 0 ≤ c := by rw [← hc 0]; exact R.nonneg 0
  unfold sufficient success optimum at h ⊢
  simp only [hc] at h ⊢
  by_cases hO : O ⊆ K
  · simp only [hO, ↓reduceIte] at h
    simp only [hO.trans hKK', ↓reduceIte]
    exact h
  · simp only [hO, ↓reduceIte] at h
    split_ifs
    · linarith
    · exact h

end Sufficiency
