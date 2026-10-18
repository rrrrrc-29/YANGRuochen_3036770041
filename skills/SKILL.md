# Skill: Replicate Card & Krueger (1994) Tables 2–4 and Figure 1

## Description

A reusable procedure for reproducing the main descriptive table (Table 2), the
difference-in-differences employment tabulations (Table 3), the reduced-form
regressions (Table 4), and the wage-distribution figure (Figure 1) from Card and
Krueger (1994), "Minimum Wages and Employment," from the store-level survey in
`data/raw/public.csv`.

## When to use

Whenever the main results must be regenerated from scratch, audited, or extended to a
new outcome or sample definition.

## Prerequisites

- Python 3.11+ with `pandas`, `numpy`, `statsmodels`, `matplotlib` installed.
- `data/raw/public.csv` present (410 stores, 46 columns).

## Steps

### 1. Reproduce everything in one command

Run from the project root:

```sh
python code/run_all.py
```

This writes Tables 2–6 to `outputs/tables/`, Figure 1 to `outputs/figures/`, and the
cleaned dataset to `data/processed/card_krueger_processed.csv`.

### 2. Reusable building blocks

| Block | Function | Output |
| --- | --- | --- |
| Load & clean | `code/prep.py::load_data`, `build_variables` | constructed dataset |
| Table 2 | `code/tables.py::table2_means` | descriptive means by state and wave |
| Table 3 | `code/tables.py::table3_employment`, `table3_did_se` | FTE levels/changes + headline DiD |
| Table 4 | `code/tables.py::table4_regression` | reduced-form models (NJ dummy and GAP) |
| Figure 1 | `code/figures.py::figure1_wage_distribution` | wage-distribution PNG |
| Extension | `code/extension.py::table5_price_passthrough`, `table6_robustness` | menu prices + robustness |

### 3. Key definitions (do not change without re-checking against the paper)

- FTE employment = `EMPFT + NMGRS + 0.5 * EMPPT`.
- % full-time = `100 * EMPFT / FTE` (full-time, excluding managers, as a share of FTE).
- `GAP = (5.05 - WAGE_ST) / WAGE_ST` for NJ stores with `WAGE_ST < 5.05`, else 0.
- DiD = (NJ_after − NJ_before) − (PA_after − PA_before), estimated by OLS on first
  differences.
- Conventional (homoskedastic) OLS standard errors, matching the paper's Table 4.
- Table 4 regression sample = stores with `fte1`, `fte2`, and `WAGE_ST` non-missing.

## Verification

After running, the headline DiD should be **+2.75 FTE** (paper: +2.76), and Table 4
column (v) should give a GAP coefficient of **12.03 (s.e. 7.32)** against the paper's
11.91 (7.39). If these do not match, re-check the definitions above before debugging
the code.
