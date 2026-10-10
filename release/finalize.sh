#!/usr/bin/env bash
# Finalise the measurement and the note once the mutation campaign has finished.
# Steps: flake control -> analysis macros -> exact context sizes -> compile -> arXiv package -> timestamp -> commit.
# Does NOT publish anything. Run from anywhere.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CORPUS="${CORPUS:-/c/Users/visci/tools/corpus/cli}"
TECTONIC="${TECTONIC:-/c/Users/visci/tools/tectonic/tectonic.exe}"
export PATH="/c/Users/visci/tools/ssl-shim:/c/Users/visci/Python/Python314/Scripts:/mingw64/bin:$PATH"

cd "$CORPUS"
if [ -n "$(git status --short --untracked-files=no)" ]; then
  echo "corpus tree dirty (campaign still running?)"; git status --short --untracked-files=no; exit 1
fi
git clean -fdq  # remove test artefacts left in the tree
CORPUS_SHA="$(git rev-parse HEAD)"

cd "$ROOT/experiments"
python flake_check.py --repo "$CORPUS" --results results/cli-mutants.jsonl --k 3 --out results/cli-flakes.json
python analyze.py --results results/cli-mutants.jsonl --flakes results/cli-flakes.json --tag cli \
  --corpus-commit "${CORPUS_SHA:0:12}" --n-pkgs 310 --n-test-pkgs 237 --n-base-fail 13 --out ../paper/results-cli.tex | tee results/cli-summary.txt
python context_sizes.py --repo "$CORPUS" --tag cli --out ../paper/sizes-cli.tex
# strip local absolute paths from the raw results before they are published
python - <<'PY'
import json, re, io
p = "results/cli-mutants.jsonl"
out = []
for line in io.open(p, encoding="utf-8"):
    if not line.strip(): continue
    r = json.loads(line)
    f = r.get("file", "")
    r["file"] = re.sub(r"^.*?[\\/]corpus[\\/]cli[\\/]", "", f).replace("\\", "/")
    out.append(json.dumps(r))
io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("paths normalised")
PY

cd "$ROOT/paper"
"$TECTONIC" --keep-logs main.tex
grep -o "Output written on main.xdv ([0-9]* pages" main.log | tail -1
echo "undefined: $(grep -ci 'undefined' main.log)"
cd "$ROOT" && bash release/make-arxiv-package.sh
cp paper/main.pdf release/final.pdf && ots stamp release/final.pdf && ots info release/final.pdf.ots | head -3
git add -A && git commit -q -m "Final measurement results, flake control, exact context sizes; final PDF timestamped" && git log --oneline | head -1
echo "FINALISED (not published). Next: human cold read (REVIEW.md), then release/zenodo_publish.py --publish on zenodo.org."
