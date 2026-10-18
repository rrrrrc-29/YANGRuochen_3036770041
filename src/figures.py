"""Generate Figure 1: distribution of starting wages, by state and wave.

Four panels show the share of stores at each starting-wage level. The
post-policy New Jersey panel (top-right) shows the compliance spike at the new
$5.05 minimum, which is absent in Pennsylvania (bottom row).
"""
from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np

from src.prep import WAGE_BIN_ORDER, build_variables, load_data, wage_bin

RESULTS = os.path.join("results", "figures")


def figure1_wage_distribution(d: "pd.DataFrame", path: str | None = None) -> str:
    import pandas as pd

    d = d.copy()
    d["wbin1"] = d["WAGE_ST"].apply(wage_bin)
    d["wbin2"] = d["WAGE_ST2"].apply(wage_bin)

    panels = [
        ("New Jersey, wave 1", "STATE", 1, "wbin1"),
        ("New Jersey, wave 2", "STATE", 1, "wbin2"),
        ("Pennsylvania, wave 1", "STATE", 0, "wbin1"),
        ("Pennsylvania, wave 2", "STATE", 0, "wbin2"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(9, 6.5), sharey=False)
    highlight = "5.01-5.05"

    for ax, (title, key, val, col) in zip(axes.ravel(), panels):
        sub = d[d[key] == val]
        counts = sub[col].value_counts(normalize=True)
        heights = [counts.get(b, 0.0) * 100 for b in WAGE_BIN_ORDER]
        colors = ["#c0392b" if b == highlight else "#4c72b0" for b in WAGE_BIN_ORDER]
        ax.bar(range(len(WAGE_BIN_ORDER)), heights, color=colors, edgecolor="white")
        ax.set_xticks(range(len(WAGE_BIN_ORDER)))
        ax.set_xticklabels(WAGE_BIN_ORDER, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel("Percent of stores")
        ax.set_ylim(0, 100)
        ax.set_title(title, fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)

    fig.suptitle(
        "Distribution of starting wages before and after the minimum-wage increase",
        fontsize=12,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.97])

    os.makedirs(RESULTS, exist_ok=True)
    out = path or os.path.join(RESULTS, "figure1_wage_distribution.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    df = load_data()
    d = build_variables(df)
    out = figure1_wage_distribution(d)
    print("Figure 1 saved to", out)


if __name__ == "__main__":
    main()
