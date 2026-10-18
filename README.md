# Card & Krueger (1994) — Minimum Wage / DiD Replication

Replication of Card and Krueger (1994), "Minimum Wages and Employment: A Case Study of
the Fast-Food Industry in New Jersey and Pennsylvania," *American Economic Review*
84(4), 772–793. Reproduces Tables 2–4 and Figure 1 and adds one independent extension
(menu-price pass-through).

## Data access (do not commit raw data)

The raw data are **not** included in this repository. Obtain `public.csv` from the
Princeton public replication files or the course "Package 01" download, then place it at:

```
data/public.csv
```

The file is Card & Krueger's restaurant survey: 410 store-level observations, 46 columns.
Column definitions are in `DATA_DICTIONARY.md`. The data are for coursework only and
must not be redistributed.

## Reproduce the results

Requires Python 3.11+.

```sh
python -m venv .venv
source .venv/bin/activate            # macOS/Linux  (Windows: .venv\Scripts\Activate.ps1)
python -m pip install -r requirements.txt
python run_all.py
```

After the input data are in place, `run_all.py` regenerates every table and figure
without manual modification of the data or code.

## Outputs

| Output | Description |
| --- | --- |
| `results/tables/table2_means.csv` | Table 2: descriptive means by state and wave |
| `results/tables/table3_employment.csv` | Table 3: average FTE employment and the main DiD |
| `results/tables/table4_regression.csv` | Table 4: reduced-form models (NJ dummy and GAP) |
| `results/tables/table5_extension_prices.csv` | Extension: menu-price pass-through |
| `results/tables/table6_robustness.csv` | Robustness checks |
| `results/figures/figure1_wage_distribution.png` | Figure 1: wage distribution |

## Code layout

```
run_all.py             # one-command workflow (entry point)
src/prep.py            # data loading, cleaning, variable construction
src/tables.py          # Tables 2, 3, 4
src/figures.py         # Figure 1
src/extension.py       # independent extension + robustness (Tables 5, 6)
report.md              # empirical report (source)
report.pdf             # empirical report (rendered)
build_pdf.py           # render report.md -> report.pdf (requires Chrome)
AI_USE.md              # AI-use disclosure
```

## Report and AI use

The empirical report is `report.md`. The AI-use disclosure is `AI_USE.md`.
