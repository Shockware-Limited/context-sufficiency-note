/-
Copyright (c) 2026 Jude Castiel Johansen. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Jude Castiel Johansen
-/
import Mathlib

/-!
# Non-monotonicity of ε-sufficient context

Mechanisation of Section 5 of
"ε-Sufficient Context for Bounded Readers: Definitions and a Non-Monotonicity Result for
Code Editing".

## Model

* Units form a finite type `U`; a context is a `Finset U`.
* A `Reader` has a degradation curve `g : ℕ → ℚ` with values in `[0,1]`.
* A `Coverage` is any function `r : Finset U → ℚ` with values in `[0,1]`.
  No shape is assumed; the binary form `[O ⊆ K]` is one instance (`binCov`).
* `success r K = r K * g |K|`.
* `optimum` is the **maximum** of `success` over all contexts (a genuine `sup'` over
  the powerset of `univ`), so `sufficient ε K ↔ optimum - ε ≤ success K` is exactly
  Definition 2 of the note.
* A set `S` is *irrelevant* to `K` when `r (K ∪ S) = r K`.

## Results

* `success_le_optimum`, `exists_maximiser`: `optimum` is attained and bounds `success`.
* `success_union_lt`: adding a non-empty irrelevant set to a context with positive
  coverage strictly lowers success when `g` is strictly decreasing.
* `not_superset_closed`: for a maximiser `K` and such an `S`, every `ε` below the drop
  makes `K` ε-sufficient and `K ∪ S` not. The drop grows with `|S|`, so this is the
  k-step statement, not a one-unit artefact.
* `const_superset_closed`: with constant `g` and monotone coverage (the lossless reader),
  ε-sufficiency is closed under superset for every `ε`.
* `binCov_optimum`, `binCov_not_superset_closed`: the binary instance, with the optimum
  computed to be `g |O|` and the Proposition specialised to it.
-/

namespace Sufficiency

variable {U : Type*} [DecidableEq U] [Fintype U]

/-- A bounded reader: a degradation curve over context size, valued in `[0,1]`. -/
structure Reader where
  /-- success multiplier as a function of context size -/
  g : ℕ → ℚ
  nonneg : ∀ n, 0 ≤ g n
  le_one : ∀ n, g n ≤ 1

/-- A coverage function on contexts, valued in `[0,1]`. No shape is assumed. -/
structure Coverage (U : Type*) where
  /-- coverage of a context -/
  r : Finset U → ℚ
  nonneg : ∀ K, 0 ≤ r K
  le_one : ∀ K, r K ≤ 1

/-- Coverage-times-degradation success. -/
def success (R : Reader) (C : Coverage U) (K : Finset U) : ℚ :=
  C.r K * R.g K.card

/-- The optimum `p*`: the maximum of `success` over all contexts. -/
def optimum (R : Reader) (C : Coverage U) : ℚ :=
  (Finset.univ : Finset U).powerset.sup' (Finset.powerset_nonempty _) (success R C)

/-- `K` is ε-sufficient iff its success is within `ε` of the optimum (Definition 2). -/
def sufficient (R : Reader) (C : Coverage U) (ε : ℚ) (K : Finset U) : Prop :=
  optimum R C - ε ≤ success R C K

/-- `S` is irrelevant to `K`: adding it does not change coverage. -/
def Irrelevant (C : Coverage U) (K S : Finset U) : Prop :=
  C.r (K ∪ S) = C.r K

theorem success_le_optimum (R : Reader) (C : Coverage U) (K : Finset U) :
    success R C K ≤ optimum R C :=
  Finset.le_sup' (success R C) (Finset.mem_powerset.mpr (Finset.subset_univ K))

theorem exists_maximiser (R : Reader) (C : Coverage U) :
    ∃ K : Finset U, success R C K = optimum R C := by
  obtain ⟨K, -, hK⟩ := Finset.exists_mem_eq_sup' (Finset.powerset_nonempty (Finset.univ : Finset U))
    (success R C)
  exact ⟨K, hK.symm⟩

/-- A maximiser is ε-sufficient for every `ε ≥ 0`. -/
theorem maximiser_sufficient (R : Reader) (C : Coverage U) {K : Finset U}
    (hmax : success R C K = optimum R C) {ε : ℚ} (hε : 0 ≤ ε) :
    sufficient R C ε K := by
  unfold sufficient; rw [hmax]; linarith

/-- Adding a non-empty irrelevant set to a context with positive coverage strictly lowers
success when the degradation curve is strictly decreasing. -/
theorem success_union_lt (R : Reader) (C : Coverage U) (hg : StrictAnti R.g)
    {K S : Finset U} (hirr : Irrelevant C K S) (hpos : 0 < C.r K) (hS : S.Nonempty)
    (hdisj : Disjoint K S) :
    success R C (K ∪ S) < success R C K := by
  unfold success
  rw [hirr, Finset.card_union_of_disjoint hdisj]
  have hlt : R.g (K.card + S.card) < R.g K.card :=
    hg (Nat.lt_add_of_pos_right (Finset.card_pos.mpr hS))
  exact mul_lt_mul_of_pos_left hlt hpos

/-- **Proposition (sufficiency is not closed under superset), k-step form.**
Let `K` be a maximiser and `K'` any context whose success is strictly lower (for instance
`K' = K ∪ S` with `S` irrelevant, by `success_union_lt`). Then for every `ε` with
`0 ≤ ε < success K - success K'`, `K` is ε-sufficient and `K'` is not. -/
theorem not_superset_closed (R : Reader) (C : Coverage U)
    {K K' : Finset U} (hmax : success R C K = optimum R C)
    {ε : ℚ} (hε0 : 0 ≤ ε) (hε : ε < success R C K - success R C K') :
    sufficient R C ε K ∧ ¬ sufficient R C ε K' := by
  refine ⟨maximiser_sufficient R C hmax hε0, ?_⟩
  unfold sufficient
  rw [← hmax]
  intro h
  linarith

/-- The hypotheses of the Proposition are jointly satisfiable for `K' = K ∪ S`: the admissible
`ε` form a non-empty interval, since the drop is strictly positive. -/
theorem not_superset_closed_nonvacuous (R : Reader) (C : Coverage U) (hg : StrictAnti R.g)
    {K S : Finset U} (hmax : success R C K = optimum R C)
    (hirr : Irrelevant C K S) (hpos : 0 < C.r K) (hS : S.Nonempty) (hdisj : Disjoint K S) :
    ∃ ε : ℚ, 0 ≤ ε ∧ sufficient R C ε K ∧ ¬ sufficient R C ε (K ∪ S) := by
  have hdrop := success_union_lt R C hg hirr hpos hS hdisj
  exact ⟨0, le_rfl, not_superset_closed R C hmax le_rfl (by linarith)⟩

omit [DecidableEq U] in
/-- **Lemma (the lossless reader is closed under superset).**
If `g` is constant and coverage is monotone under inclusion, then ε-sufficiency is preserved
by supersets, for every `ε`. -/
theorem const_superset_closed (R : Reader) (C : Coverage U) (c : ℚ) (hc : ∀ n, R.g n = c)
    (hmono : ∀ K K' : Finset U, K ⊆ K' → C.r K ≤ C.r K') {ε : ℚ} {K K' : Finset U}
    (hKK' : K ⊆ K') (h : sufficient R C ε K) :
    sufficient R C ε K' := by
  have hc0 : 0 ≤ c := by rw [← hc 0]; exact R.nonneg 0
  unfold sufficient success at h ⊢
  rw [hc] at h ⊢
  have := mul_le_mul_of_nonneg_right (hmono K K' hKK') hc0
  linarith

/-! ## The binary instance -/

/-- Binary coverage of an oracle slice `O`: `1` if `O ⊆ K`, else `0`. -/
def binCov (O : Finset U) : Coverage U where
  r K := if O ⊆ K then 1 else 0
  nonneg K := by split_ifs <;> norm_num
  le_one K := by split_ifs <;> norm_num

omit [Fintype U] in
theorem binCov_success (R : Reader) (O K : Finset U) :
    success R (binCov O) K = if O ⊆ K then R.g K.card else 0 := by
  by_cases h : O ⊆ K <;> simp [success, binCov, h]

/-- With antitone `g`, the optimum of the binary instance is `g |O|`, attained at `K = O`. -/
theorem binCov_optimum (R : Reader) (hg : Antitone R.g) (O : Finset U) :
    optimum R (binCov O) = R.g O.card := by
  apply le_antisymm
  · apply Finset.sup'_le
    intro K _
    rw [binCov_success]
    split_ifs with h
    · exact hg (Finset.card_le_card h)
    · exact R.nonneg _
  · have := success_le_optimum R (binCov O) O
    rwa [binCov_success, if_pos (Finset.Subset.refl O)] at this

omit [Fintype U] in
/-- Any set disjoint from `O` is irrelevant to `O` under binary coverage. -/
theorem binCov_irrelevant (O S : Finset U) : Irrelevant (binCov O) O S := by
  unfold Irrelevant binCov
  simp [Finset.subset_union_left]

/-- **Proposition, binary instance.** For `S` non-empty and disjoint from `O`, and `g`
strictly decreasing, every `ε` with `0 ≤ ε < g |O| - g (|O| + |S|)` makes `O` ε-sufficient
and `O ∪ S` not. -/
theorem binCov_not_superset_closed (R : Reader) (hg : StrictAnti R.g) {O S : Finset U}
    (hS : S.Nonempty) (hdisj : Disjoint O S) {ε : ℚ} (hε0 : 0 ≤ ε)
    (hε : ε < R.g O.card - R.g (O.card + S.card)) :
    sufficient R (binCov O) ε O ∧ ¬ sufficient R (binCov O) ε (O ∪ S) := by
  have hmax : success R (binCov O) O = optimum R (binCov O) := by
    rw [binCov_optimum R hg.antitone, binCov_success, if_pos (Finset.Subset.refl O)]
  have hpos : 0 < (binCov O).r O := by
    unfold binCov; simp
  have hdrop : success R (binCov O) O - success R (binCov O) (O ∪ S)
      = R.g O.card - R.g (O.card + S.card) := by
    rw [binCov_success, binCov_success, if_pos (Finset.Subset.refl O),
      if_pos Finset.subset_union_left, Finset.card_union_of_disjoint hdisj]
  exact not_superset_closed R (binCov O) hmax hε0 (by rw [hdrop]; exact hε)

/-! ## Proposition 1 exactly as stated in the note, and a concrete witness -/

/-- **Proposition 1 (note, Section 5).** Under the stated hypotheses: success strictly drops,
the drop equals `r(K) · (g|K| − g(|K|+|S|))`, and every `ε` in `[0, drop)` separates `K`
(ε-sufficient) from `K ∪ S` (not ε-sufficient). Load is `|K|` and values are in `ℚ`. -/
theorem prop1 (R : Reader) (C : Coverage U) (hg : StrictAnti R.g)
    {K S : Finset U} (hmax : success R C K = optimum R C)
    (hirr : Irrelevant C K S) (hpos : 0 < C.r K) (hS : S.Nonempty) (hdisj : Disjoint K S) :
    success R C (K ∪ S) < success R C K ∧
    success R C K - success R C (K ∪ S) = C.r K * (R.g K.card - R.g (K.card + S.card)) ∧
    ∀ ε : ℚ, 0 ≤ ε → ε < C.r K * (R.g K.card - R.g (K.card + S.card)) →
      sufficient R C ε K ∧ ¬ sufficient R C ε (K ∪ S) := by
  have hdrop : success R C K - success R C (K ∪ S)
      = C.r K * (R.g K.card - R.g (K.card + S.card)) := by
    unfold success
    rw [hirr, Finset.card_union_of_disjoint hdisj]
    ring
  refine ⟨success_union_lt R C hg hirr hpos hS hdisj, hdrop, fun ε hε0 hε => ?_⟩
  exact not_superset_closed R C hmax hε0 (by rw [hdrop]; exact hε)

/-- The harmonic reader `g n = 1/(n+1)`: a concrete strictly decreasing curve in `[0,1]`. -/
def harmonic : Reader where
  g n := 1 / ((n : ℚ) + 1)
  nonneg n := by positivity
  le_one n := by
    rw [div_le_one (by positivity)]
    linarith [(Nat.cast_nonneg n : (0 : ℚ) ≤ n)]

theorem harmonic_strictAnti : StrictAnti harmonic.g := by
  intro a b hab
  simp only [harmonic]
  apply one_div_lt_one_div_of_lt (by positivity)
  have : (a : ℚ) < b := by exact_mod_cast hab
  linarith

/-- Concrete witness: two units, oracle slice `{0}`, harmonic reader, `ε = 0`.
`{0}` is 0-sufficient and `{0} ∪ {1}` is not. The hypotheses are jointly satisfiable. -/
example : sufficient harmonic (binCov ({0} : Finset (Fin 2))) 0 {0} ∧
    ¬ sufficient harmonic (binCov ({0} : Finset (Fin 2))) 0 ({0} ∪ {1}) :=
  binCov_not_superset_closed harmonic harmonic_strictAnti (Finset.singleton_nonempty 1)
    (by decide) le_rfl (by simp [harmonic]; norm_num)

end Sufficiency
