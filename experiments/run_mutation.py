"""Mutation-based measurement of the forward-slice requirement on a Go repository.

For each sampled mutant (one body-only, signature-preserving change in one non-test file):
  1. inject it, check that the module still compiles, run the FULL test suite once,
  2. record which test packages fail,
  3. revert.
Classification against the package import graph, with W = {mutated package}:
  detected_W      : W's own tests fail
  detected_F      : a test package in the forward slice F(W) (transitive reverse test-deps) fails
  detected_other  : a failing test package is neither W nor in F(W)  (channel outside the import graph)
Context sizes (tokens, tiktoken cl100k_base; falls back to bytes/4) are recorded for
W, backward slice B(W), forward slice F(W), and their tests, plus the whole module.

Usage:
  python run_mutation.py --repo PATH --n 100 --seed 1 --out results.jsonl --baseline baseline.json
Resumable: existing lines in --out are counted and skipped.
"""
import argparse, json, os, random, subprocess, sys, time, pathlib, collections

GOENV = {"GOFLAGS": "-mod=mod"}
GO = os.environ.get("GO", "go")
MUTATOR = os.environ.get("MUTATOR", "mutator")

def env():
    e = dict(os.environ); e.update(GOENV); return e

def run(cmd, cwd, timeout=None):
    return subprocess.run(cmd, cwd=cwd, env=env(), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=timeout)

def tokenizer():
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return ("cl100k_base", lambda s: len(enc.encode(s, disallowed_special=())))
    except Exception:
        return ("bytes/4", lambda s: len(s.encode("utf-8")) // 4)

def load_packages(repo):
    r = run([GO, "list", "-json", "./..."], repo)
    if r.returncode != 0:
        sys.exit("go list failed: " + r.stderr[:500])
    pk = {}
    dec = json.JSONDecoder(); s = r.stdout; i = 0
    while i < len(s):
        while i < len(s) and s[i].isspace(): i += 1
        if i >= len(s): break
        obj, j = dec.raw_decode(s, i); i = j
        pk[obj["ImportPath"]] = obj
    mod = run([GO, "list", "-m"], repo).stdout.strip()
    return pk, mod

def build_graph(pk, mod):
    inmod = lambda p: p in pk
    deps = {p: set(d for d in o.get("Deps", []) if inmod(d)) for p, o in pk.items()}
    # test-time dependency closure of each package: its own deps, plus deps of test imports
    tdeps = {}
    for p, o in pk.items():
        s = set(deps[p])
        for ti in o.get("TestImports", []) + o.get("XTestImports", []):
            if inmod(ti):
                s.add(ti); s |= deps[ti]
        s.discard(p)
        tdeps[p] = s
    fwd = {p: set(q for q in pk if q != p and p in tdeps[q]) for p in pk}
    return deps, tdeps, fwd

def tok_counts(pk, repo, count):
    src, tst = {}, {}
    for p, o in pk.items():
        d = o["Dir"]
        def tot(files):
            n = 0
            for f in files:
                try: n += count(open(os.path.join(d, f), encoding="utf-8", errors="replace").read())
                except FileNotFoundError: pass
            return n
        src[p] = tot(o.get("GoFiles", []))
        tst[p] = tot(o.get("TestGoFiles", []) + o.get("XTestGoFiles", []))
    return src, tst

def parse_test_json(text):
    status = {}
    for line in text.splitlines():
        try: e = json.loads(line)
        except Exception: continue
        if e.get("Test") is None and e.get("Action") in ("pass", "fail", "skip"):
            status[e["Package"]] = e["Action"]
    return status

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True); ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=1); ap.add_argument("--out", required=True)
    ap.add_argument("--baseline", required=True); ap.add_argument("--test-timeout", default="20m")
    a = ap.parse_args()
    repo = a.repo
    pk, mod = load_packages(repo)
    deps, tdeps, fwd = build_graph(pk, mod)
    tokname, count = tokenizer()
    src_tok, tst_tok = tok_counts(pk, repo, count)
    total_src = sum(src_tok.values()); total_tst = sum(tst_tok.values())
    base = parse_test_json(open(a.baseline, encoding="utf-8", errors="replace").read())
    testable = {p for p, s in base.items() if s == "pass"}
    base_fail = {p for p, s in base.items() if s == "fail"}
    print(f"packages={len(pk)} testable={len(testable)} baseline_fail={len(base_fail)} tokenizer={tokname} "
          f"src_tokens={total_src} test_tokens={total_tst}", flush=True)
    # candidate packages: have non-test Go files and are detectable by someone
    cands = [p for p, o in pk.items() if o.get("GoFiles") and (p in testable or (fwd[p] & testable))]
    rng = random.Random(a.seed)
    done = 0
    if os.path.exists(a.out):
        done = sum(1 for _ in open(a.out, encoding="utf-8"))
    print(f"candidates={len(cands)} already_done={done}", flush=True)
    out = open(a.out, "a", encoding="utf-8")
    attempt = done * 7 + a.seed
    while done < a.n:
        attempt += 1
        p = rng.choice(cands); o = pk[p]
        f = rng.choice(o["GoFiles"]); path = os.path.join(o["Dir"], f)
        rel = os.path.relpath(path, repo)
        m = run([MUTATOR, "-file", path, "-seed", str(attempt)], repo)
        if m.returncode != 0:
            run(["git", "checkout", "--", rel], repo); continue
        info = json.loads(m.stdout)
        t0 = time.time()
        b = run([GO, "build", "./..."], repo, timeout=900)
        if b.returncode != 0:
            run(["git", "checkout", "--", rel], repo)
            rec = {"pkg": p, "file": rel, **info, "compiles": False}
            out.write(json.dumps(rec) + "\n"); out.flush(); done += 1
            print(f"[{done}/{a.n}] {p} {info['operator']} -> does not compile", flush=True)
            continue
        try:
            t = run([GO, "test", "./...", "-count=1", "-json", "-timeout", a.test_timeout], repo, timeout=2400)
            status = parse_test_json(t.stdout)
        except subprocess.TimeoutExpired:
            status = {}
        run(["git", "checkout", "--", rel], repo)
        fails = {q for q, s in status.items() if s == "fail"} - base_fail
        F = fwd[p]; B = deps[p]
        rec = {
            "pkg": p, "file": rel, **info, "compiles": True, "secs": round(time.time() - t0, 1),
            "fail_pkgs": sorted(fails),
            "detected_any": bool(fails),
            "detected_W": p in fails,
            "detected_F": bool(fails & F),
            "detected_other": bool(fails - F - {p}),
            "W_has_tests": p in testable,
            "n_B": len(B), "n_F": len(F), "n_F_testable": len(F & testable),
            "tok_W": src_tok[p], "tok_W_tests": tst_tok[p],
            "tok_B": sum(src_tok[q] for q in B), "tok_F": sum(src_tok[q] for q in F),
            "tok_F_tests": sum(tst_tok[q] for q in F),
            "tok_total_src": total_src, "tok_total_tests": total_tst, "tokenizer": tokname,
        }
        out.write(json.dumps(rec) + "\n"); out.flush(); done += 1
        print(f"[{done}/{a.n}] {p} {info['operator']} fails={len(fails)} W={rec['detected_W']} "
              f"F={rec['detected_F']} other={rec['detected_other']} {rec['secs']}s", flush=True)
    # sanity: tree clean
    st = run(["git", "status", "--short"], repo).stdout.strip()
    print("tree clean" if not st else "WARNING tree dirty:\n" + st, flush=True)

if __name__ == "__main__":
    main()
