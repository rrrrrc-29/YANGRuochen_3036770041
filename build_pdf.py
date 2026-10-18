#!/usr/bin/env python3
"""Render report.md to report.pdf (markdown -> self-contained HTML -> Chrome).

Math is converted from LaTeX to Unicode/HTML so no JavaScript or network access is
needed at print time. Requires the ``markdown`` Python package and Google Chrome.

Run:

    python build_pdf.py
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
MD = ROOT / "report.md"
HTML = ROOT / "report.html"
PDF = ROOT / "report.pdf"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
:root { color-scheme: light; }
body {
  font-family: "Charter", Georgia, "Times New Roman", serif;
  color: #1a1a1a;
  line-height: 1.55;
  max-width: 46rem;
  margin: 0 auto;
  padding: 1rem 1.5rem 3rem;
}
h1, h2, h3, h4 { line-height: 1.2; color: #111; }
h1 { font-size: 1.6rem; border-bottom: 2px solid #1a1a1a; padding-bottom: .3rem; }
h2 { font-size: 1.25rem; margin-top: 1.8rem; }
h3 { font-size: 1.05rem; }
p { margin: .6rem 0; }
em { color: #333; }
blockquote {
  margin: .8rem 0; padding: .1rem 1rem;
  border-left: 3px solid #b0b0b0; color: #555; background: #f7f7f7;
}
code {
  font-family: "SF Mono", Menlo, Consolas, monospace; font-size: .9em;
  background: #f2f2f2; padding: 0 .25em; border-radius: 3px;
}
table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: .92rem; }
th, td { border: 1px solid #ccc; padding: .4rem .6rem; text-align: left; }
th { background: #efefef; font-weight: 600; }
tr:nth-child(even) td { background: #fafafa; }
hr { border: none; border-top: 1px solid #ccc; margin: 2rem 0; }
a { color: #0645ad; text-decoration: none; }
.math { font-family: Georgia, "Times New Roman", serif; font-style: italic; }
div.math { text-align: center; margin: .8rem 0; }
@media print {
  body { max-width: none; padding: 0; }
  @page { margin: 1.8cm; }
  a { color: inherit; }
}
"""

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Replication of Card &amp; Krueger (1994)</title>
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""

# LaTeX -> HTML replacements for the equations in this report. Each pattern is
# anchored on a unique LaTeX prefix and matches through the closing delimiter,
# so it is robust to line wrapping and never mistakes dollar amounts ($4.25,
# $5.05, ...) for math.
_MATH_REPLACEMENTS = [
    (
        r"\$\$ \\delta \\;=\\;[^$]*\$\$",
        '<div class="math">δ = (NJ<sub>after</sub> − NJ<sub>before</sub>) − '
        "(PA<sub>after</sub> − PA<sub>before</sub>)</div>",
    ),
    (
        r"\$\$ \\Delta\\text\{FTE\}_i[^$]*\$\$",
        '<div class="math">ΔFTE<sub>i</sub> = α + δ·NJ<sub>i</sub> + ε<sub>i</sub></div>',
    ),
    (
        r"\$\\text\{FTE\}_\{it\}[^$]*\$",
        '<span class="math">FTE<sub>it</sub> = β·NJ<sub>i</sub> + γ·After<sub>t</sub> + '
        "δ·(NJ<sub>i</sub> × After<sub>t</sub>) + ε<sub>it</sub></span>",
    ),
    (
        r"\$\$ \\Delta\\text\{Price\}_i[^$]*\$\$",
        '<div class="math">ΔPrice<sub>i</sub> = α + δ·NJ<sub>i</sub> + '
        "X<sub>i</sub>′γ + ε<sub>i</sub></div>",
    ),
]


def _replace_math(text: str) -> str:
    """Replace the report's LaTeX math with self-contained HTML."""
    for pattern, replacement in _MATH_REPLACEMENTS:
        text = re.sub(pattern, replacement, text, flags=re.S)
    return text


def main() -> None:
    text = MD.read_text(encoding="utf-8")
    text = _replace_math(text)
    md = markdown.Markdown(extensions=["tables", "sane_lists"])
    body = md.convert(text)

    HTML.write_text(TEMPLATE.format(css=CSS, body=body), encoding="utf-8")
    print("wrote", HTML)

    cmd = [
        CHROME,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--virtual-time-budget=5000",
        f"--print-to-pdf={PDF}",
        f"file://{HTML}",
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print("wrote", PDF)


if __name__ == "__main__":
    main()
