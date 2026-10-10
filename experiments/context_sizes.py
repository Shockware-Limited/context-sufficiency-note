"""Exact context-size distribution over ALL candidate packages of a corpus (no sampling noise).

For each package p with non-test Go files: tokens of W = p (source), tests of W, backward slice
B(p) (transitive in-module deps), forward slice F(p) (transitive reverse test-time deps), tests of
F(p); and the transitive-slice context W + tests(W) + B + F + tests(F). Emits LaTeX macros and a JSON
table. Read-only with respect to the corpus.

Usage: python context_sizes.py --repo PATH --tag cli --out ../paper/sizes-cli.tex
"""
import argparse, json, os, statistics, sys, pathlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_mutation import load_packages, build_graph, tok_counts, tokenizer, run, GO

def fmt(n):
    return f"{n/1000:.0f}k" if n >= 10000 else f"{n:,}"

def q(xs, f):
    xs = sorted(xs); return xs[min(len(xs) - 1, int(f * (len(xs) - 1)))]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True); ap.add_argument("--tag", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    pk, mod = load_packages(a.repo)
    deps, tdeps, fwd = build_graph(pk, mod)
    tokname, count = tokenizer()
    src, tst = tok_counts(pk, a.repo, count)
    tot_src, tot_tst = sum(src.values()), sum(tst.values()); tot = tot_src + tot_tst
    cands = [p for p, o in pk.items() if o.get("GoFiles")]
    rows = []
    for p in cands:
        B, F = deps[p], fwd[p]
        tw, twt, tb = src[p], tst[p], sum(src[x] for x in B)
        tf, tft = sum(src[x] for x in F), sum(tst[x] for x in F)
        ctx = tw + twt + tb + tf + tft
        rows.append({"pkg": p, "tok_W": tw, "tok_W_tests": twt, "tok_B": tb, "tok_F": tf, "tok_F_tests": tft,
                     "n_B": len(B), "n_F": len(F), "ctx": ctx, "ctx_pct": 100.0 * ctx / tot})
    t = a.tag
    gover = run([GO, "version"], a.repo).stdout.strip().replace("go version ", "")
    med = lambda k: int(statistics.median(r[k] for r in rows))
    macros = {
        f"{t}GoVersion": gover, f"{t}Tokenizer": tokname,
        f"{t}TotTokSrc": fmt(tot_src), f"{t}TotTokTests": fmt(tot_tst), f"{t}TotTok": fmt(tot), f"{t}NCand": len(cands),
        f"{t}MedTokW": fmt(med("tok_W")), f"{t}MedTokB": fmt(med("tok_B")), f"{t}MedTokF": fmt(med("tok_F")),
        f"{t}MedTokFt": fmt(med("tok_F_tests")), f"{t}PNinetyTokF": fmt(q([r["tok_F"] for r in rows], 0.9)),
        f"{t}MedNF": med("n_F"), f"{t}PNinetyNF": q([r["n_F"] for r in rows], 0.9),
        f"{t}MedPctCtx": f"{statistics.median(r['ctx_pct'] for r in rows):.0f}",
        f"{t}PNinetyPctCtx": f"{q([r['ctx_pct'] for r in rows], 0.9):.0f}",
        f"{t}PctFitSmall": f"{100*sum(1 for r in rows if r['ctx'] <= 128_000)/len(rows):.0f}",
        f"{t}PctFitLarge": f"{100*sum(1 for r in rows if r['ctx'] <= 200_000)/len(rows):.0f}",
        f"{t}PctFEmpty": f"{100*sum(1 for r in rows if r['n_F'] == 0)/len(rows):.0f}",
    }
    out = pathlib.Path(a.out)
    out.write_text("".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in macros.items()), encoding="utf-8", newline="\n")
    json.dump(rows, open(out.with_suffix(".json"), "w", encoding="utf-8"), indent=0)
    print(f"wrote {out}")
    for k, v in macros.items(): print(f"  {k:18s} {v}")

if __name__ == "__main__":
    main()
