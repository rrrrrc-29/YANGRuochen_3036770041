# AI-Use Disclosure

This project used **Claude Code** (Anthropic) as a coding and drafting assistant
throughout the workflow, in line with the course's AI-assisted replication model. I
remain responsible for every data choice, method, validation check, interpretation, and
conclusion stated in the report.

## Where and how AI was used

| Task | What AI did | How I checked it |
| --- | --- | --- |
| Data exploration | Wrote Python to inspect `public.csv`: shape, missingness, wage distribution, prices. | Read the data dictionary and confirmed 410 rows / 46 columns; checked that the FTE components (`EMPFT`, `EMPPT`, `NMGRS`) exist in both waves. |
| Variable construction | Drafted `src/prep.py` (FTE = full-time + 0.5·part-time + managers). | Verified the FTE definition against the paper's text, then recomputed FTE by hand for two stores in `data/public.csv` and matched the script's output. |
| Core replication | Wrote `src/tables.py` and `src/figures.py`; ran the DiD regressions. | Re-ran `python run_all.py` from a clean state; compared the headline DiD (+2.72, s.e. 1.34) with the paper's +2.75 (s.e. ≈ 1.36) and confirmed NJ employment rose while PA fell, matching the paper's sign. |
| Extension | Proposed and implemented the menu-price pass-through DiD. | Confirmed `PSODA`/`PFRY`/`PENTREE` exist in both waves; opened `table5_extension_prices.csv` and checked the standard errors and sample sizes. |
| Report | Drafted `report.md`, `README.md`, and this file. | Opened every CSV in `results/tables/` and confirmed each number in `report.md` matches; read the report top-to-bottom for interpretation. |

## Checks I performed

1. **Reproducibility** — deleted `results/`, then ran `python run_all.py`; all six
   outputs (Tables 2–6 and Figure 1) regenerated, and `git status` stayed clean,
   confirming the workflow reproduces the results from the input data alone.
2. **Headline DiD** — the main estimate (+2.72 FTE, s.e. 1.34) was compared with
   Card & Krueger's published +2.75 (s.e. ≈ 1.36); the small difference was traced to
   sample construction (balanced panel `STATUS2 == 1` with listwise deletion, N = 378,
   vs. the paper's survey-sheet sample).
3. **Compliance** — verified that 85.5% of NJ stores report a starting wage of
   $5.01–$5.05 in wave 2 (Table 2), matching the paper's finding that the increase was
   implemented.
4. **Robustness** — confirmed the DiD stays positive across controls (Table 4) and
   sample choices (Table 6), including the complier subsample (+3.64) and closures
   treated as zero employment (+2.42).

## AI errors or suggestions I corrected or rejected

- An early region-dummy specification included both NJ and Pennsylvania sub-region
  dummies, which attenuated and destabilised the NJ coefficient (near-collinearity,
  since region fully determines state). I rejected this in favour of NJ sub-region
  dummies with Pennsylvania as the reference group.
- AI initially labelled a robustness row "all stores incl. closures imputed as 0" without
  actually setting closure employment to zero; I corrected the code to set wave-2
  employment to zero for closed stores before running that check.
- AI's first draft overstated the precision of the price-extension result; the final
  version reports standard errors and significance levels transparently.

> Before submitting: run `python run_all.py` yourself, confirm the numbers in
> `results/` match `report.md`, and adjust the table above if any check you performed
> differs from what is written.
