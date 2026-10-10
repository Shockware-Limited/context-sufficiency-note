import Sufficiency.NonMonotonic

/-! Axiom audit. CI runs `lake env lean Axioms.lean` and checks that every main theorem
depends only on `propext`, `Classical.choice`, and `Quot.sound`. -/

#print axioms Sufficiency.success_le_optimum
#print axioms Sufficiency.exists_maximiser
#print axioms Sufficiency.success_union_lt
#print axioms Sufficiency.not_superset_closed
#print axioms Sufficiency.not_superset_closed_nonvacuous
#print axioms Sufficiency.const_superset_closed
#print axioms Sufficiency.binCov_optimum
#print axioms Sufficiency.binCov_not_superset_closed
