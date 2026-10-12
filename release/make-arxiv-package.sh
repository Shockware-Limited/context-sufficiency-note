#!/usr/bin/env bash
# Build a self-contained arXiv source tarball (TeX + BBL + every \input file) and extract the abstract.
# Run from anywhere after the final compile of paper/main.tex.
set -euo pipefail
cd "$(dirname "$0")/../paper"
TECTONIC="${TECTONIC:-$(command -v tectonic || echo /c/Users/visci/tools/tectonic/tectonic.exe)}"
"$TECTONIC" --keep-intermediates --keep-logs main.tex >/dev/null
test -f main.bbl || { echo "main.bbl missing"; exit 1; }
mkdir -p ../release/arxiv
rm -f ../release/arxiv/*
cp main.tex main.bbl ../release/arxiv/
# every \input{name} in main.tex ships as name.tex
grep -o '\\input{[^}]*}' main.tex | sed 's/\\input{//; s/}//' | while read -r f; do
  if [ -f "$f.tex" ]; then cp "$f.tex" ../release/arxiv/; elif [ -f "$f" ]; then cp "$f" ../release/arxiv/; else echo "missing input: $f"; exit 1; fi
done
ls ../release/arxiv/
tar -czf ../release/arxiv-source.tar.gz -C ../release/arxiv .
echo "wrote release/arxiv-source.tar.gz"
python ../release/extract-abstract.py
