"""Extract the abstract from paper/main.tex into release/arxiv-abstract.txt (plain text for the arXiv form)."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
s = (root / "paper" / "main.tex").read_text(encoding="utf-8")
a = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", s, re.S).group(1).strip()
a = re.sub(r"\\emph\{([^}]*)\}", r"\1", a)
a = a.replace("$\\eps$", "ε").replace("$(\\Delta, D, I)$", "(Δ, D, I)").replace("$K$", "K").replace("$A$", "A").replace("$\\eps$", "ε")
a = re.sub(r"\s+", " ", a)
(root / "release" / "arxiv-abstract.txt").write_text(a, encoding="utf-8")
print("wrote release/arxiv-abstract.txt")
