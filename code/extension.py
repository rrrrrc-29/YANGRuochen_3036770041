"""Independent extension: did restaurants pass the wage increase through to
menu prices?

The minimum-wage increase raised the cost of labour. A natural, testable
question the original paper does not answer with a formal DiD is whether any of
that cost was passed through to consumers via higher menu prices. We use the
three menu items recorded in both waves -- medium soda, small fries, and the
entree -- as outcomes and apply the same DiD design.

This module also produces a small robustness table (alternative samples and
outcomes) for the main employment result.
"""
from __future__ import annotations

import os

import pandas as pd
import statsmodels.formula.api as smf

from code.prep import balanced_sample, build_variables, load_data

RESULTS = os.path.join("outputs", "tables")

PRICE_LABELS = {
    "dPSODA": "Medium soda",
    "dPFRY": "Small fries",
    "dPENTREE": "Entree",
}


def _ensure_dir() -> None:
    os.makedirs(RESULTS, exist_ok=True)


def _did(outcome: str, data: pd.DataFrame, controls: str = "") -> dict:
    formula = f"{outcome} ~ nj" + controls
    m = smf.ols(formula, data=data).fit()  # conventional OLS s.e., as in the paper
    return {
        "coef": m.params["nj"],
        "se": m.bse["nj"],
        "t": m.tvalues["nj"],
        "n": int(m.nobs),
    }


def table5_price_passthrough(d: pd.DataFrame) -> pd.DataFrame:
    """DiD estimates of the minimum-wage effect on menu prices.

    Uses all stores with the relevant price recorded in both waves (the OLS
    routine drops observations with missing price changes).
    """
    rows = []
    for col, label in PRICE_LABELS.items():
        r = _did(col, d, " + chain2 + chain3 + chain4 + CO_OWNED")
        rows.append(
            {
                "Menu item": label,
                "NJ mean change": d.loc[d["nj"] == 1, col].mean(),
                "PA mean change": d.loc[d["nj"] == 0, col].mean(),
                "DiD": r["coef"],
                "s.e.": r["se"],
                "t-statistic": r["t"],
                "N": r["n"],
            }
        )
    out = pd.DataFrame(rows)
    out[["NJ mean change", "PA mean change", "DiD", "s.e.", "t-statistic"]] = out[
        ["NJ mean change", "PA mean change", "DiD", "s.e.", "t-statistic"]
    ].round(3)
    return out


def table6_robustness(d: pd.DataFrame, bal: pd.DataFrame) -> pd.DataFrame:
    """Robustness: alternative samples and outcomes for the employment DiD."""
    rows = []

    def add(label, outcome, data):
        r = _did(outcome, data)
        rows.append(
            {
                "Specification": label,
                "DiD": r["coef"],
                "s.e.": r["se"],
                "t-statistic": r["t"],
                "N": r["n"],
            }
        )

    # Compliers: stores paying exactly the old minimum before the increase.
    compliers = bal[bal["WAGE_ST"] == 4.25].copy()

    # Attrition check: treat stores that closed after wave 1 as having zero
    # wave-2 employment (the Card-Krueger "closed stores" robustness).
    closed_imp = d.copy()
    closed_imp["fte2"] = closed_imp["fte2"].where(
        closed_imp["STATUS2"] == 1, 0.0
    )
    closed_imp["dfte"] = closed_imp["fte2"] - closed_imp["fte1"]

    add("FTE, balanced sample", "dfte", bal)
    add("Headcount, balanced sample", "demp", bal)
    add("Full-time employees only", "EMPFT2 - EMPFT", bal)
    add("Part-time employees only", "EMPPT2 - EMPPT", bal)
    add("FTE, initial wage = $4.25 (compliers)", "dfte", compliers)
    add("FTE, closures treated as zero employment", "dfte", closed_imp)

    out = pd.DataFrame(rows)
    out[["DiD", "s.e.", "t-statistic"]] = out[["DiD", "s.e.", "t-statistic"]].round(3)
    return out


def main() -> None:
    _ensure_dir()
    df = load_data()
    d = build_variables(df)
    bal = balanced_sample(d)

    t5 = table5_price_passthrough(d)
    t5.to_csv(os.path.join(RESULTS, "table5_extension_prices.csv"))
    print("Table 5 - extension: price pass-through")
    print(t5.to_string(), "\n")

    t6 = table6_robustness(d, bal)
    t6.to_csv(os.path.join(RESULTS, "table6_robustness.csv"))
    print("Table 6 - robustness")
    print(t6.to_string(), "\n")


if __name__ == "__main__":
    main()
