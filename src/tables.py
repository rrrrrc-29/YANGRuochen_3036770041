"""Generate Tables 2, 3, and 4 of the Card & Krueger (1994) replication.

Table 2 - distribution of starting wages by state and wave (compliance check).
Table 3 - average employment per store before and after (main DiD).
Table 4 - regression estimates of the minimum-wage effect on employment.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from src.prep import (
    WAGE_BIN_ORDER,
    balanced_sample,
    build_variables,
    load_data,
    wage_bin,
)

RESULTS = os.path.join("results", "tables")


def _ensure_dir() -> None:
    os.makedirs(RESULTS, exist_ok=True)


# --------------------------------------------------------------------------- #
# Table 2 - distribution of starting wages
# --------------------------------------------------------------------------- #
def table2_wage_distribution(d: pd.DataFrame) -> pd.DataFrame:
    """Share of stores in each starting-wage bin, by state and wave."""
    d = d.copy()
    d["wbin1"] = d["WAGE_ST"].apply(wage_bin)
    d["wbin2"] = d["WAGE_ST2"].apply(wage_bin)

    rows = {}
    for state, label in ((1, "NJ"), (0, "PA")):
        sub = d[d["STATE"] == state]
        vc1 = sub["wbin1"].value_counts(normalize=True)
        vc2 = sub["wbin2"].value_counts(normalize=True)
        for b in WAGE_BIN_ORDER:
            key = (label, "wave1", b)
            rows[key] = vc1.get(b, 0.0)
            key = (label, "wave2", b)
            rows[key] = vc2.get(b, 0.0)

    out = pd.DataFrame(index=WAGE_BIN_ORDER)
    out["NJ wave 1"] = [rows[("NJ", "wave1", b)] for b in WAGE_BIN_ORDER]
    out["NJ wave 2"] = [rows[("NJ", "wave2", b)] for b in WAGE_BIN_ORDER]
    out["PA wave 1"] = [rows[("PA", "wave1", b)] for b in WAGE_BIN_ORDER]
    out["PA wave 2"] = [rows[("PA", "wave2", b)] for b in WAGE_BIN_ORDER]
    out = (out * 100).round(1)

    # Add mean starting wage and observation count rows.
    means = []
    for state, label in ((1, "NJ"), (0, "PA")):
        sub = d[d["STATE"] == state]
        means += [sub["WAGE_ST"].mean(), sub["WAGE_ST2"].mean()]
    mean_row = pd.Series(
        {c: means[i] for i, c in enumerate(out.columns)}, name="Mean wage ($)"
    )
    out = pd.concat([out, mean_row.to_frame().T])

    return out


# --------------------------------------------------------------------------- #
# Table 3 - main DiD
# --------------------------------------------------------------------------- #
def _did_row(bal: pd.DataFrame, var1: str, var2: str) -> dict:
    """Mean levels, change, and DiD (with HC1 s.e.) for one outcome."""
    nj = bal[bal["nj"] == 1]
    pa = bal[bal["nj"] == 0]

    m_nj1, m_nj2 = nj[var1].mean(), nj[var2].mean()
    m_pa1, m_pa2 = pa[var1].mean(), pa[var2].mean()
    chg_nj = (nj[var2] - nj[var1]).mean()
    chg_pa = (pa[var2] - pa[var1]).mean()

    # DiD with HC1 standard error via OLS on first differences.
    chg = bal[var2] - bal[var1]
    reg = smf.ols("chg ~ nj", data=pd.DataFrame({"chg": chg, "nj": bal["nj"]})).fit(
        cov_type="HC1"
    )
    did = reg.params["nj"]
    did_se = reg.bse["nj"]
    n = int(reg.nobs)

    return {
        "var1_mean_nj": m_nj1,
        "var2_mean_nj": m_nj2,
        "chg_nj": chg_nj,
        "var1_mean_pa": m_pa1,
        "var2_mean_pa": m_pa2,
        "chg_pa": chg_pa,
        "did": did,
        "did_se": did_se,
        "n": n,
    }


def table3_did(bal: pd.DataFrame) -> pd.DataFrame:
    """Main DiD table: FTE and headcount employment, balanced sample."""
    fte = _did_row(bal, "fte1", "fte2")
    emp = _did_row(bal, "emp1", "emp2")

    data = []
    for name, r in (("FTE", fte), ("Headcount", emp)):
        data.append(
            {
                "Outcome": name,
                "NJ wave 1": r["var1_mean_nj"],
                "NJ wave 2": r["var2_mean_nj"],
                "NJ change": r["chg_nj"],
                "PA wave 1": r["var1_mean_pa"],
                "PA wave 2": r["var2_mean_pa"],
                "PA change": r["chg_pa"],
                "DiD": r["did"],
                "DiD s.e.": r["did_se"],
                "N": r["n"],
            }
        )
    out = pd.DataFrame(data)
    out = out.round(3)
    return out


# --------------------------------------------------------------------------- #
# Table 4 - regression estimates
# --------------------------------------------------------------------------- #
SPECS = [
    ("NJ only", "dfte ~ nj"),
    ("+ chain & ownership", "dfte ~ nj + chain2 + chain3 + chain4 + CO_OWNED"),
    (
        "+ region dummies",
        "dfte ~ nj + chain2 + chain3 + chain4 + CO_OWNED + SOUTHJ + CENTRALJ + SHORE",
    ),
    (
        "+ initial wage",
        "dfte ~ nj + chain2 + chain3 + chain4 + CO_OWNED + SOUTHJ + CENTRALJ + SHORE"
        " + WAGE_ST",
    ),
]


def table4_regression(bal: pd.DataFrame) -> pd.DataFrame:
    """Regression of the FTE change on the NJ dummy with successive controls."""
    rows = []
    for label, spec in SPECS:
        m = smf.ols(spec, data=bal).fit(cov_type="HC1")
        rows.append(
            {
                "Specification": label,
                "NJ coefficient": m.params["nj"],
                "s.e.": m.bse["nj"],
                "t-statistic": m.tvalues["nj"],
                "N": int(m.nobs),
                "R-squared": m.rsquared,
            }
        )
    out = pd.DataFrame(rows)
    out[["NJ coefficient", "s.e.", "t-statistic", "R-squared"]] = out[
        ["NJ coefficient", "s.e.", "t-statistic", "R-squared"]
    ].round(3)
    return out


# --------------------------------------------------------------------------- #
# Run all
# --------------------------------------------------------------------------- #
def main() -> None:
    _ensure_dir()
    df = load_data()
    d = build_variables(df)
    bal = balanced_sample(d)

    t2 = table2_wage_distribution(d)
    t2.to_csv(os.path.join(RESULTS, "table2_wage_distribution.csv"))
    print("Table 2 - wage distribution")
    print(t2.to_string(), "\n")

    t3 = table3_did(bal)
    t3.to_csv(os.path.join(RESULTS, "table3_did.csv"))
    print("Table 3 - main DiD")
    print(t3.to_string(), "\n")

    t4 = table4_regression(bal)
    t4.to_csv(os.path.join(RESULTS, "table4_regression.csv"))
    print("Table 4 - regression estimates")
    print(t4.to_string(), "\n")


if __name__ == "__main__":
    main()
