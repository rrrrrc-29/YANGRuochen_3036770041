"""Data loading, cleaning, and variable construction.

Replicates Card & Krueger (1994), "Minimum Wages and Employment: A Case
Study of the Fast-Food Industry in New Jersey and Pennsylvania," AER 84(4).

Source data: restaurant-level survey of 410 fast-food stores (Burger King, KFC,
Roy Rogers, Wendy's) in New Jersey and eastern Pennsylvania. Two survey waves:
wave 1 = February-March 1992 (before the April 1, 1992 minimum-wage increase
from $4.25 to $5.05), wave 2 = November-December 1992 (after).
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

CHAIN_NAMES = {1: "Burger King", 2: "KFC", 3: "Roy Rogers", 4: "Wendy's"}

# STATUS2 codes (wave-2 store status). 1 = open; 3 = permanently closed
# (employment recorded as zero); 0 = refused; 2, 4, 5 = temporarily closed
# (renovation / road construction / fire), wave-2 employment treated as missing.
_TEMP_CLOSED = (2, 4, 5)


def load_data(path: str = "data/raw/public.csv") -> pd.DataFrame:
    """Read the raw survey file."""
    return pd.read_csv(path)


PROCESSED = os.path.join("data", "processed", "card_krueger_processed.csv")


def save_processed() -> str:
    """Write the cleaned, variable-constructed dataset to data/processed/.

    Gives a one-file view of every constructed variable used in the analysis,
    so the processed data can be inspected independently of the code.
    """
    os.makedirs(os.path.dirname(PROCESSED), exist_ok=True)
    d = build_variables(load_data())
    d.to_csv(PROCESSED, index=False)
    return PROCESSED


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

    # Price of a full meal (medium soda + small fries + entree, incl. tax).
    d["meal1"] = d["PSODA"] + d["PFRY"] + d["PENTREE"]
    d["meal2"] = d["PSODA2"] + d["PFRY2"] + d["PENTREE2"]

    # Percentage full-time employees. Card & Krueger's Table 2 defines this as
    # full-time workers (excluding managers) as a share of FTE employment:
    # 100 * EMPFT / (EMPFT + NMGRS + 0.5 * EMPPT).
    d["pft1"] = 100.0 * d["EMPFT"] / d["fte1"]
    d["pft2"] = 100.0 * d["EMPFT2"] / d["fte2"]

    # Treatment intensity: the proportional increase in the starting wage needed
    # to reach the new $5.05 minimum (the paper's GAP variable). Zero for PA and
    # for NJ stores already paying at least $5.05.
    d["gap"] = np.where(
        (d["STATE"] == 1) & (d["WAGE_ST"] < 5.05),
        (5.05 - d["WAGE_ST"]) / d["WAGE_ST"],
        0.0,
    )

    # Wave-2 FTE with closures handled as in Table 3. The raw data already
    # records wave-2 employment of zero for the six permanently closed stores
    # (STATUS2 = 3) and missing for temporary closures and refusals.
    d["fte2_all"] = d["fte2"]

    # Wave-2 FTE with the four temporarily closed stores set to zero (Table 3,
    # row 5) rather than treated as missing.
    d["fte2_temp0"] = d["fte2"].where(
        ~d["STATUS2"].isin(_TEMP_CLOSED), 0.0
    )

    # NJ wage groups, classified by the wave-1 starting wage (Table 3 cols iv-vi).
    def _wage_group(w: float) -> str | None:
        if pd.isna(w):
            return None
        if w == 4.25:
            return "4.25"
        if w < 5.00:
            return "4.26-4.99"
        return "5.00+"

    d["wage_group"] = np.where(
        d["nj"] == 1, d["WAGE_ST"].apply(_wage_group), None
    )

    return d


def balanced_sample(d: pd.DataFrame) -> pd.DataFrame:
    """The paper's balanced subsample: stores with employment data in both waves.

    Permanently closed stores (wave-2 employment recorded as zero) are included;
    temporarily closed stores and refusals have missing wave-2 employment and are
    dropped. This is the sample underlying Table 3, row 4.
    """
    return d.dropna(subset=["fte1", "fte2"]).copy()


def regression_sample(d: pd.DataFrame) -> pd.DataFrame:
    """The Table 4 regression sample.

    Stores with employment in both waves and a valid wave-1 starting wage. The
    GAP variable requires only the wave-1 wage; requiring a wave-2 wage would
    discard stores whose wave-2 starting wage is legitimately missing and is not
    needed for any specification in Table 4.
    """
    return d.dropna(subset=["fte1", "fte2", "WAGE_ST"]).copy()


def wage_bin(w: float) -> str:
    """Map a starting wage to a labelled bin used in Figure 1."""
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
