"""Data loading, cleaning, and variable construction.

Replicates Card & Krueger (1994), "Minimum Wages and Employment: A Case
Study of the Fast-Food Industry in New Jersey and Pennsylvania," AER 84(4).

Source data: restaurant-level survey of 410 fast-food stores (Burger King, KFC,
Roy Rogers, Wendy's) in New Jersey and eastern Pennsylvania. Two survey waves:
wave 1 = February-March 1992 (before the April 1, 1992 minimum-wage increase
from $4.25 to $5.05), wave 2 = November-December 1992 (after).
"""
from __future__ import annotations

import pandas as pd

CHAIN_NAMES = {1: "Burger King", 2: "KFC", 3: "Roy Rogers", 4: "Wendy's"}


def load_data(path: str = "data/public.csv") -> pd.DataFrame:
    """Read the raw survey file."""
    return pd.read_csv(path)


def build_variables(df: pd.DataFrame) -> pd.DataFrame:
    """Construct analysis variables. Returns a copy with no columns dropped."""
    d = df.copy()

    # Full-time-equivalent (FTE) employment, the main outcome.
    # Card & Krueger define FTE = full-time employees + managers
    # + 0.5 * part-time employees.
    d["fte1"] = d["EMPFT"] + 0.5 * d["EMPPT"] + d["NMGRS"]
    d["fte2"] = d["EMPFT2"] + 0.5 * d["EMPPT2"] + d["NMGRS2"]

    # Headcount employment (alternative outcome).
    d["emp1"] = d["EMPFT"] + d["EMPPT"] + d["NMGRS"]
    d["emp2"] = d["EMPFT2"] + d["EMPPT2"] + d["NMGRS2"]

    # Employment changes (first differences).
    d["dfte"] = d["fte2"] - d["fte1"]
    d["demp"] = d["emp2"] - d["emp1"]

    # Treatment indicator: New Jersey.
    d["nj"] = (d["STATE"] == 1).astype(int)

    # Chain dummies (chain 1 = Burger King is the reference category).
    for c in (1, 2, 3, 4):
        d[f"chain{c}"] = (d["CHAIN"] == c).astype(int)

    # Menu-price changes (used in the extension).
    for price in ("PSODA", "PFRY", "PENTREE"):
        d[f"d{price}"] = d[f"{price}2"] - d[price]

    return d


def balanced_sample(d: pd.DataFrame) -> pd.DataFrame:
    """Stores that answered wave 2 and remained open (STATUS2 == 1).

    This is the main analysis sample: a balanced panel of stores observed in
    both waves. Stores that closed (STATUS2 = 3), refused (0), or were closed
    for renovation/construction/fire (2, 4, 5) are excluded from the core
    results and treated in the robustness checks.
    """
    return d[d["STATUS2"] == 1].copy()


def wage_bin(w: float) -> str:
    """Map a starting wage to a labelled bin used in Table 2 and Figure 1."""
    if pd.isna(w):
        return "missing"
    if w == 4.25:
        return "4.25"
    if w <= 4.50:
        return "4.26-4.50"
    if w <= 4.75:
        return "4.51-4.75"
    if w <= 5.00:
        return "4.76-5.00"
    if w <= 5.05:
        return "5.01-5.05"
    return "5.06+"


WAGE_BIN_ORDER = ["4.25", "4.26-4.50", "4.51-4.75", "4.76-5.00", "5.01-5.05", "5.06+"]
