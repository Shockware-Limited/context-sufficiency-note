"""Summarise mutation results into LaTeX macros (paper/results.tex) and a markdown table.

Usage: python analyze.py --results results/cli-mutants.jsonl --corpus-commit ec5b512045db \
                         --n-pkgs 310 --n-test-pkgs 237 --n-base-fail 13 --out ../paper/results.tex
"""
import argparse, json, statistics, pathlib

def pct(a, b):
    return f"{100.0 * a / b:.0f}" if b else "--"

def fmt_tok(n):
    return f"{n/1000:.0f}k" if n >= 10000 else f"{n:,}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--corpus-commit", required=True)
    ap.add_argument("--n-pkgs", type=int, required=True); ap.add_argument("--n-test-pkgs", type=int, required=True)
    ap.add_argument("--n-base-fail", type=int, required=True)
    a = ap.parse_args()
    recs = [json.loads(l) for l in open(a.results, encoding="utf-8") if l.strip()]
    comp = [r for r in recs if r.get("compiles")]
    det = [r for r in comp if r["detected_any"]]
    byW = [r for r in det if r["detected_W"]]
    fonly = [r for r in det if not r["detected_W"] and r["detected_F"]]
    other = [r for r in det if r["detected_other"]]
    fonly_notests = [r for r in fonly if not r["W_has_tests"]]
    tot_src = comp[0]["tok_total_src"] if comp else 0
    tot_tst = comp[0]["tok_total_tests"] if comp else 0
    med = lambda k: int(statistics.median([r[k] for r in comp])) if comp else 0
    kstar = [r["tok_W"] + r["tok_W_tests"] + r["tok_B"] + r["tok_F"] + r["tok_F_tests"] for r in comp]
    kstar_pct = [100.0 * k / (tot_src + tot_tst) for k in kstar] if (tot_src + tot_tst) else []
    p90F = int(sorted(r["tok_F"] for r in comp)[int(0.9 * (len(comp) - 1))]) if comp else 0
    fit128 = sum(1 for k in kstar if k <= 128_000); fit200 = sum(1 for k in kstar if k <= 200_000)
    macros = {
        "corpusCommit": a.corpus_commit, "nPkgs": a.n_pkgs, "nTestPkgs": a.n_test_pkgs, "nBaseFail": a.n_base_fail,
        "nMut": len(recs), "nCompile": len(comp), "nDet": len(det),
        "pctW": pct(len(byW), len(det)), "pctFonly": pct(len(fonly), len(det)), "pctOther": pct(len(other), len(det)),
        "pctWnoTests": pct(len(fonly_notests), len(fonly)),
        "medTokW": fmt_tok(med("tok_W")), "medTokB": fmt_tok(med("tok_B")), "medTokF": fmt_tok(med("tok_F")),
        "medTokFt": fmt_tok(med("tok_F_tests")), "pNinetyTokF": fmt_tok(p90F), "totTok": fmt_tok(tot_src),
        "medPctKstar": f"{statistics.median(kstar_pct):.0f}" if kstar_pct else "--",
        "pctFitSmall": pct(fit128, len(comp)), "pctFitLarge": pct(fit200, len(comp)),
    }
    out = pathlib.Path(a.out)
    out.write_text("".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in macros.items()), encoding="utf-8", newline="\n")
    print(f"wrote {out}")
    for k, v in macros.items(): print(f"  {k:14s} {v}")
    # operator breakdown
    from collections import Counter
    ops = Counter(r["operator"].split(":")[0] for r in comp)
    print("operators (compiling):", dict(ops))
    print("detected by operator:", dict(Counter(r["operator"].split(":")[0] for r in det)))
    print("elsewhere failures (pkg -> failing pkgs):")
    for r in other[:10]:
        print("   ", r["pkg"], "->", r["fail_pkgs"][:4])

if __name__ == "__main__":
    main()
