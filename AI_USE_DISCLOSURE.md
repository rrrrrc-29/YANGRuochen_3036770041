# AI-Use Disclosure

This project used **Claude Code** (Anthropic) as a coding and drafting assistant
throughout the workflow, in line with the course's AI-assisted replication model. I
remain responsible for every data choice, method, validation check, interpretation, and
conclusion stated in the report.

## Where and how AI was used

| Task | What AI did | How I checked it |
| --- | --- | --- |
| Data exploration | Wrote Python to inspect `public.csv`: shape, missingness, wage distribution, prices. | Read the data dictionary and confirmed 410 rows / 46 columns; checked that the FTE components (`EMPFT`, `EMPPT`, `NMGRS`) exist in both waves. |
| Variable construction | Drafted `code/prep.py` (FTE = full-time + 0.5·part-time + managers). | Verified the FTE definition against the paper's text, then recomputed FTE by hand for two stores in `data/raw/public.csv` and matched the script's output. |
| Core replication | Wrote `code/tables.py` and `code/figures.py`; ran the DiD regressions. | Re-ran `python code/run_all.py` from a clean state; compared the headline DiD (+2.75 FTE) with the paper's +2.76 and confirmed NJ employment rose while PA fell, matching the paper's sign and magnitude. |
| Extension | Proposed and implemented the menu-price pass-through DiD. | Confirmed `PSODA`/`PFRY`/`PENTREE` exist in both waves; opened `outputs/tables/table5_extension_prices.csv` and checked the standard errors and sample sizes. |
| Report | Drafted `report.md`, `README.md`, and this file. | Opened every CSV in `outputs/tables/` and confirmed each number in `report.md` matches; read the report top-to-bottom for interpretation. |

## Checks I performed

1. **Reproducibility** — deleted `outputs/`, then ran `python code/run_all.py`; all six
   outputs (Tables 2–6 and Figure 1) regenerated, and `git status` stayed clean,
   confirming the workflow reproduces the results from the input data alone.
2. **Headline DiD** — the main estimate (+2.75 FTE) was compared with Card & Krueger's
   published +2.76. The small residual differences in the Table 4 regression sample
   (N = 365 vs. the paper's 357) were traced to a few stores whose wave-2 starting wage
   is missing in the public file.
3. **Compliance** — verified that 85.5% of NJ stores report a starting wage of exactly
   $5.05 in wave 2 (Table 2, wave-2 means), and that the NJ mean wage rose from $4.61 to
   $5.08 while PA was unchanged, confirming the increase was implemented.
4. **Robustness** — confirmed the DiD stays positive across controls (Table 4, including
   the GAP treatment-intensity specifications) and sample choices (Table 6), including
   the complier subsample (+3.22) and closures treated as zero employment (+2.42).

## AI errors or suggestions I corrected or rejected

- AI's first draft made Table 2 a starting-wage *distribution* table, but the paper's
  Table 2 is a table of *descriptive means* (store types, employment, wages, prices,
  hours, bonuses). I corrected the table to match the paper's structure.
- AI's first definition of "% full-time employees" used `(full-time + managers) / total
  headcount`; the paper's Table 2 actually defines it as full-time workers (excluding
  managers) as a share of FTE employment (`EMPFT / FTE`). Matching this definition
  reproduces the paper's 32.8% (wave 1) and 35.9% / 30.4% (wave 2) exactly.
- AI's region-dummy specification treated the NJ "Shore" flag as a fourth region and
  omitted the PA regions; the paper uses three NJ regions (North/Central/South) plus
  the two eastern PA regions. Fixing this reproduces the paper's footnote that the
  R² of GAP on region effects is about 0.30, and matches Table 4 column (v).
- AI initially reported heteroskedasticity-robust (HC1) standard errors; the paper's
  Table 4 uses conventional OLS standard errors. Switching to conventional errors
  reproduces the paper's reported standard errors (e.g. 7.32 vs. the paper's 7.39 in
  column v).
- AI's first draft overstated the precision of the price-extension result; the final
  version reports standard errors and significance levels transparently.

> Before submitting: run `python code/run_all.py` yourself, confirm the numbers in
> `outputs/` match `report.md`, and adjust the table above if any check you performed
> differs from what is written.
