"""Flake control for the mutation results.

For every test package that failed on ANY compiling mutant, rerun that package k times on the
CLEAN tree. A package that fails on the clean tree at least once is flaky and is excluded from
every mutant's fail set by analyze.py. Conservative: it can only reduce detections.

Usage: python flake_check.py --repo PATH --results results/cli-mutants.jsonl --k 3 --out results/cli-flakes.json
Run only after the campaign has finished and the tree is clean.
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_mutation import run, parse_test_json, GO

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True); ap.add_argument("--results", required=True)
    ap.add_argument("--k", type=int, default=3); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    st = run(["git", "status", "--short", "--untracked-files=no"], a.repo).stdout.strip()
    if st: sys.exit("tree not clean:\n" + st)
    recs = [json.loads(l) for l in open(a.results, encoding="utf-8") if l.strip()]
    pkgs = sorted({p for r in recs if r.get("compiles") for p in r.get("fail_pkgs", [])})
    print(f"{len(pkgs)} distinct failing packages across compiling mutants; rerunning each {a.k}x on the clean tree", flush=True)
    flaky = {}
    for i in range(a.k):
        t = run([GO, "test", "-count=1", "-json"] + pkgs, a.repo, timeout=3600)
        status = parse_test_json(t.stdout)
        for p, s in status.items():
            if s == "fail": flaky[p] = flaky.get(p, 0) + 1
        print(f"  run {i+1}: {sum(1 for s in status.values() if s == 'fail')} failing on clean tree", flush=True)
    json.dump({"k": a.k, "checked_pkgs": pkgs, "flaky_pkgs": sorted(flaky), "clean_fail_counts": flaky},
              open(a.out, "w", encoding="utf-8"), indent=1)
    print("flaky:", sorted(flaky))

if __name__ == "__main__":
    main()
