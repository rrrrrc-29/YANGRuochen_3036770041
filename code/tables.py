"""Generate Tables 2, 3, and 4 of the Card & Krueger (1994) replication.

Table 2 - descriptive means by state, wave 1 and wave 2.
Table 3 - average FTE employment per store before and after, by state and
          within New Jersey by wave-1 wage group (the main DiD).
Table 4 - reduced-form regressions of the change in FTE employment on the
          New Jersey dummy and the initial wage gap (GAP).
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

from code.prep import build_variables, load_data, regression_sample

RESULTS = os.path.join("outputs", "tables")


def _ensure_dir() -> None:
    os.makedirs(RESULTS, exist_ok=True)


def _tstat(a: pd.Series, b: pd.Series) -> float:
    """Welch t-statistic for equality of means (the paper's Table 2 test)."""
    a = a.dropna()
    b = b.dropna()
    if len(a) < 2 or len(b) < 2:
        return np.nan
    return float(stats.ttest_ind(a, b, equal_var=False)[0])


# --------------------------------------------------------------------------- #
# Table 2 - descriptive means
# --------------------------------------------------------------------------- #
def table2_means(d: pd.DataFrame) -> pd.DataFrame:
    """Descriptive statistics by state (NJ / PA) with t-statistics.

    Reproduces the paper's Table 2: store-type shares, then wave-1 and wave-2
    means. Percentages are reported in percentage points (0-100); the
    t-statistic tests equality of means across states.
    """
    nj = d["nj"] == 1

    rows: list[list] = []

    def add(name: str, values: pd.Series, pct: bool = False) -> None:
        a = values[nj]
        b = values[~nj]
        mult = 100.0 if pct else 1.0
        rows.append(
            [name, float(a.mean() * mult), float(b.mean() * mult), _tstat(a, b)]
        )

    # Section 1: distribution of store types (percentages).
    add("Burger King (%)", d["chain1"], pct=True)
    add("KFC (%)", d["chain2"], pct=True)
    add("Roy Rogers (%)", d["chain3"], pct=True)
    add("Wendy's (%)", d["chain4"], pct=True)
    add("Company-owned (%)", d["CO_OWNED"], pct=True)

    # Section 2: means in wave 1.
    add("FTE employment (wave 1)", d["fte1"])
    add("% full-time employees (wave 1)", d["pft1"])
    add("Starting wage (wave 1)", d["WAGE_ST"])
    add("% wage = $4.25 (wave 1)", d["WAGE_ST"] == 4.25, pct=True)
    add("Full meal price (wave 1)", d["meal1"])
    add("Hours open (wave 1)", d["HRSOPEN"])
    add("Recruiting bonus (wave 1)", d["BONUS"], pct=True)

    # Section 3: means in wave 2.
    add("FTE employment (wave 2)", d["fte2"])
    add("% full-time employees (wave 2)", d["pft2"])
    add("Starting wage (wave 2)", d["WAGE_ST2"])
    add("% wage = $4.25 (wave 2)", d["WAGE_ST2"] == 4.25, pct=True)
    add("% wage = $5.05 (wave 2)", d["WAGE_ST2"] == 5.05, pct=True)
    add("Full meal price (wave 2)", d["meal2"])
    add("Hours open (wave 2)", d["HRSOPEN2"])
    add("Recruiting bonus (wave 2)", d["SPECIAL2"], pct=True)

    out = pd.DataFrame(rows, columns=["Variable", "NJ", "PA", "t"])
    out["NJ"] = out["NJ"].round(2)
    out["PA"] = out["PA"].round(2)
    out["t"] = out["t"].round(2)
    return out


# --------------------------------------------------------------------------- #
# Table 3 - average employment before and after
# --------------------------------------------------------------------------- #
def _group_rows(d: pd.DataFrame, mask: pd.Series) -> list[float]:
    """The five Table 3 rows for one group of stores (all available / balanced /
    temp-closed-zero)."""
    g = d[mask]
    before = g["fte1"].mean()                       # row 1: all available
    after = g["fte2_all"].mean()                    # row 2: all available
    change = after - before                         # row 3: diff. of means
    chg_bal = (g["fte2_all"] - g["fte1"]).mean()    # row 4: balanced pairwise
    chg_t0 = (g["fte2_temp0"] - g["fte1"]).mean()   # row 5: temp-closed = 0
    return [before, after, change, chg_bal, chg_t0]


def table3_employment(d: pd.DataFrame) -> pd.DataFrame:
    """Average FTE employment per store, by state and NJ wage group.

    Columns (i)-(viii) follow the paper: PA, NJ, NJ-PA difference, and NJ
    stores split by the wave-1 starting wage ($4.25, $4.26-$4.99, $5.00+),
    with the low-high and midrange-high differences within New Jersey.
    """
    nj = d["nj"] == 1

    pa = _group_rows(d, ~nj)
    nj_total = _group_rows(d, nj)
    w425 = _group_rows(d, nj & (d["wage_group"] == "4.25"))
    w426 = _group_rows(d, nj & (d["wage_group"] == "4.26-4.99"))
    w500 = _group_rows(d, nj & (d["wage_group"] == "5.00+"))

    rows = [
        "1. FTE before, all available",
        "2. FTE after, all available",
        "3. Change in mean FTE",
        "4. Change in mean FTE, balanced sample",
        "5. Change in mean FTE, temp-closed = 0",
    ]

    out = pd.DataFrame(index=rows)
    out["PA"] = pa
    out["NJ"] = nj_total
    out["NJ-PA"] = [a - b for a, b in zip(nj_total, pa)]
    out["NJ: $4.25"] = w425
    out["NJ: $4.26-4.99"] = w426
    out["NJ: $5.00+"] = w500
    out["Low-High"] = [a - b for a, b in zip(w425, w500)]
    out["Mid-High"] = [a - b for a, b in zip(w426, w500)]
    return out.round(2)


def table3_did_se(d: pd.DataFrame) -> tuple[float, float, int]:
    """DiD estimate and conventional (homoskedastic) OLS standard error for the
    balanced first-difference regression (the paper's headline +2.76, t = 2.03).
    The paper reports conventional OLS standard errors, so we match that."""
    bal = d.dropna(subset=["fte1", "fte2"])
    m = smf.ols("dfte ~ nj", data=bal).fit()
    return float(m.params["nj"]), float(m.bse["nj"]), int(m.nobs)


# --------------------------------------------------------------------------- #
# Table 4 - reduced-form models for the change in employment
# --------------------------------------------------------------------------- #
TABLE4_SPECS = [
    ("(i) NJ dummy", "dfte ~ nj", "nj"),
    (
        "(ii) NJ + chain & ownership",
        "dfte ~ nj + chain2 + chain3 + chain4 + CO_OWNED",
        "nj",
    ),
    ("(iii) GAP", "dfte ~ gap", "gap"),
    (
        "(iv) GAP + chain & ownership",
        "dfte ~ gap + chain2 + chain3 + chain4 + CO_OWNED",
        "gap",
    ),
    (
        "(v) GAP + chain & ownership + region",
        "dfte ~ gap + chain2 + chain3 + chain4 + CO_OWNED"
        " + CENTRALJ + SOUTHJ + PA1 + PA2",
        "gap",
    ),
]


def table4_regression(d: pd.DataFrame) -> pd.DataFrame:
    """Reduced-form models for the change in FTE employment.

    Sample = stores with employment in both waves and a wave-1 starting wage
    (the paper's 357-store regression sample). Region dummies in column (v) are
    the three New Jersey regions (North omitted) plus the two eastern
    Pennsylvania regions, as in the paper.
    """
    s = regression_sample(d)
    rows = []
    for label, spec, key in TABLE4_SPECS:
        m = smf.ols(spec, data=s).fit()  # conventional OLS s.e., as in the paper
        rows.append(
            {
                "Model": label,
                "Coefficient": float(m.params[key]),
                "s.e.": float(m.bse[key]),
                "t": float(m.tvalues[key]),
                "N": int(m.nobs),
                "R-squared": float(m.rsquared),
            }
        )
    out = pd.DataFrame(rows)
    out[["Coefficient", "s.e.", "t", "R-squared"]] = out[
        ["Coefficient", "s.e.", "t", "R-squared"]
    ].round(3)
    return out


# --------------------------------------------------------------------------- #
# Run all
# --------------------------------------------------------------------------- #
def main() -> None:
    _ensure_dir()
    df = load_data()
    d = build_variables(df)

    t2 = table2_means(d)
    t2.to_csv(os.path.join(RESULTS, "table2_means.csv"))
    print("Table 2 - descriptive means")
    print(t2.to_string(), "\n")

    t3 = table3_employment(d)
    t3.to_csv(os.path.join(RESULTS, "table3_employment.csv"))
    print("Table 3 - average employment")
    print(t3.to_string(), "\n")

    did, did_se, n_bal = table3_did_se(d)
    print(
        f"Table 3 headline DiD (balanced first-difference): {did:.2f} "
        f"(s.e. {did_se:.2f}), N = {n_bal}\n"
    )

    t4 = table4_regression(d)
    t4.to_csv(os.path.join(RESULTS, "table4_regression.csv"))
    print("Table 4 - reduced-form models")
    print(t4.to_string(), "\n")


if __name__ == "__main__":
    main()
