# Card & Krueger (1994) — Minimum Wage / DiD Replication

Replication of Card and Krueger (1994), "Minimum Wages and Employment: A Case Study of
the Fast-Food Industry in New Jersey and Pennsylvania," *American Economic Review*
84(4), 772–793. Reproduces Tables 2–4 and Figure 1 and adds one independent extension
(menu-price pass-through).

## Data

The store-level survey (`public.csv`, 410 stores, 46 columns) is included under
`data/raw/`. Column definitions are in `DATA_DICTIONARY.md`. Running the workflow also
writes the cleaned, variable-constructed dataset to
`data/processed/card_krueger_processed.csv`.

## Reproduce the results

Requires Python 3.11+.

```sh
python -m venv .venv
source .venv/bin/activate            # macOS/Linux  (Windows: .venv\Scripts\Activate.ps1)
python -m pip install -r requirements.txt
python code/run_all.py
```

`code/run_all.py` regenerates every table, figure, and the processed dataset from
`data/raw/public.csv` alone, without manual modification of the data or code.

## Outputs

| Output | Description |
| --- | --- |
| `outputs/tables/table2_means.csv` | Table 2: descriptive means by state and wave |
| `outputs/tables/table3_employment.csv` | Table 3: average FTE employment and the main DiD |
| `outputs/tables/table4_regression.csv` | Table 4: reduced-form models (NJ dummy and GAP) |
| `outputs/tables/table5_extension_prices.csv` | Extension: menu-price pass-through |
| `outputs/tables/table6_robustness.csv` | Robustness checks |
| `outputs/figures/figure1_wage_distribution.png` | Figure 1: wage distribution |

## Code layout

```
code/run_all.py        # one-command workflow (entry point)
code/prep.py           # data loading, cleaning, variable construction
code/tables.py         # Tables 2, 3, 4
code/figures.py        # Figure 1
code/extension.py      # independent extension + robustness (Tables 5, 6)
data/raw/              # original input data (public.csv)
data/processed/        # cleaned dataset written by run_all.py
outputs/tables/        # generated tables
outputs/figures/       # generated figures
skills/SKILL.md        # reusable skill for the main tables and figure
report.md              # empirical report (source)
report.pdf             # empirical report (rendered)
build_pdf.py           # render report.md -> report.pdf (requires Chrome)
AI_USE_DISCLOSURE.md   # AI-use disclosure
```

## Report and AI use

The empirical report is `report.pdf` (source: `report.md`). The AI-use disclosure is
`AI_USE_DISCLOSURE.md`.
