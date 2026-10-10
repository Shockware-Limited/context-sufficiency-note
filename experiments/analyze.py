"""Summarise mutation results into LaTeX macros and print tables.

Classes are EXCLUSIVE: W (mutated package's own tests fail), Fonly (W's tests pass, some test
package in F(W) fails), otheronly (failures only outside W and F(W)), undetected, timeout,
nocompile. An overlap count records mutants that fail both in W and in F(W).

Flake control: with --flakes FILE (output of flake_check.py), packages listed as flaky are removed
from every mutant's fail set before classification.

Usage: python analyze.py --results results/cli-mutants.jsonl [--flakes results/cli-flakes.json]
         --tag cli --corpus-commit SHA --n-pkgs 310 --n-test-pkgs 237 --n-base-fail 13 --out ../paper/results-cli.tex
"""
import argparse, json, math, os, pathlib
from collections import Counter

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))

def pct_ci(k, n):
    lo, hi = wilson(k, n)
    return f"{100*k/n:.0f}\\% [{100*lo:.0f}, {100*hi:.0f}]" if n else "--"

def classify(r, flaky):
    if not r.get("compiles"): return "nocompile"
    if r.get("timeout"): return "timeout"
    fails = set(r["fail_pkgs"]) - flaky
    if not fails: return "undetected"
    W = r["pkg"]
    if W in fails: return "W"
    # recorded flags were computed against the full fail set; after removing flaky packages,
    # F membership of the remaining failures is: detected_F held and some non-W failure remains
    if r["detected_F"] and (fails - {W}): return "Fonly"
    return "otheronly"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True); ap.add_argument("--flakes")
    ap.add_argument("--tag", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--corpus-commit", required=True)
    ap.add_argument("--n-pkgs", type=int, required=True); ap.add_argument("--n-test-pkgs", type=int, required=True)
    ap.add_argument("--n-base-fail", type=int, required=True)
    a = ap.parse_args()
    recs = [json.loads(l) for l in open(a.results, encoding="utf-8") if l.strip()]
    flaky = set()
    if a.flakes and os.path.exists(a.flakes):
        flaky = set(json.load(open(a.flakes, encoding="utf-8")).get("flaky_pkgs", []))
    for r in recs: r["cls"] = classify(r, flaky)
    C = Counter(r["cls"] for r in recs)
    comp = [r for r in recs if r["cls"] != "nocompile"]
    det = [r for r in comp if r["cls"] in ("W", "Fonly", "otheronly")]
    nW, nF, nO, nD = C["W"], C["Fonly"], C["otheronly"], len(det)
    overlap = sum(1 for r in det if r["cls"] == "W" and r["detected_F"])
    det_wt = [r for r in det if r["W_has_tests"]]; det_nt = [r for r in det if not r["W_has_tests"]]
    nF_wt = sum(1 for r in det_wt if r["cls"] == "Fonly"); nF_nt = sum(1 for r in det_nt if r["cls"] == "Fonly")
    t = a.tag
    macros = {
        f"{t}CorpusCommit": a.corpus_commit, f"{t}NPkgs": a.n_pkgs, f"{t}NTestPkgs": a.n_test_pkgs,
        f"{t}NBaseFail": a.n_base_fail, f"{t}NMut": len(recs), f"{t}NCompile": len(comp),
        f"{t}NTimeout": C["timeout"], f"{t}NDet": nD, f"{t}NFlaky": len(flaky),
        f"{t}PctDet": pct_ci(nD, len(comp)),
        f"{t}PctW": pct_ci(nW, nD), f"{t}PctFonly": pct_ci(nF, nD), f"{t}PctOther": pct_ci(nO, nD),
        f"{t}NOverlap": overlap,
        f"{t}NDetWt": len(det_wt), f"{t}PctFonlyWt": pct_ci(nF_wt, len(det_wt)),
        f"{t}NDetNt": len(det_nt), f"{t}PctFonlyNt": pct_ci(nF_nt, len(det_nt)),
    }
    out = pathlib.Path(a.out)
    out.write_text("".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in macros.items()), encoding="utf-8", newline="\n")
    print(f"wrote {out}")
    for k, v in macros.items(): print(f"  {k:16s} {v}")
    print("classes:", dict(C))
    print("per operator: n / detected / W / Fonly / other")
    for op in Counter(r["operator"].split(":")[0] for r in comp):
        rs = [r for r in comp if r["operator"].split(":")[0] == op]; cc = Counter(r["cls"] for r in rs)
        print(f"   {op:10s} {len(rs):3d} {sum(cc[c] for c in ('W','Fonly','otheronly')):3d} {cc['W']:3d} {cc['Fonly']:3d} {cc['otheronly']:3d}")
    print("Fonly / otheronly mutants (pkg -> failing pkgs):")
    for r in [r for r in det if r["cls"] in ("Fonly", "otheronly")][:20]:
        print(f"   [{r['cls']}] {r['pkg']} -> {sorted(set(r['fail_pkgs']) - flaky)[:4]}")

if __name__ == "__main__":
    main()
