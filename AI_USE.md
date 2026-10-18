# AI-Use Disclosure

This project used **Claude Code** (Anthropic) as a coding and drafting assistant
throughout the workflow, in line with the course's AI-assisted replication model. I
remain responsible for every data choice, method, validation check, interpretation, and
conclusion stated in the report.

## Where and how AI was used

| Task | What AI did | How I checked it |
| --- | --- | --- |
| Data exploration | Wrote Python to inspect `public.csv`: shape, missingness, wage distribution, prices. | Re-read the data dictionary and confirmed the 410 observations / 46 columns and the FTE components. |
| Variable construction | Drafted `src/prep.py` (FTE = full-time + 0.5·part-time + managers). | Verified the FTE definition against the paper's text and re-derived FTE by hand for a few stores. |
| Core replication | Wrote `src/tables.py` and `src/figures.py`; ran the DiD regressions. | Compared the headline DiD (+2.72) against the paper's published +2.75 and traced the small difference to sample construction. |
| Extension | Proposed and implemented the menu-price pass-through DiD. | Checked the price variables exist in both waves; the result is reported with standard errors. |
| Report | Drafted `report.md`, `README.md`, and this file. | Reviewed all numbers against the CSV outputs in `results/`; edited the text for accuracy. |

## Checks performed

- `python run_all.py` was run end-to-end from a clean state; all six outputs regenerated.
- The main DiD estimate (+2.72 FTE, s.e. 1.34) was compared with Card & Krueger's +2.75
  (s.e. ≈ 1.36) and the difference explained (balanced-panel construction with listwise
  deletion vs. the paper's survey-sheet sample).
- The compliance result (85.5% of NJ stores at $5.01–$5.05 in wave 2) was verified to
  match the wage-distribution table.
- Regression specifications were checked for perfect collinearity; the region-dummy
  specification uses NJ sub-region dummies with Pennsylvania as the reference group.

## AI errors or suggestions I corrected or rejected

- An early region-dummy specification included both NJ and Pennsylvania sub-region
  dummies, which attenuated and destabilised the NJ coefficient (perfect/near
  collinearity, since region fully determines state). This was rejected in favour of NJ
  sub-region dummies with PA as the reference.
- AI initially labelled a robustness row "all stores incl. closures imputed as 0" without
  actually imputing closure employment to zero; the code was corrected to set wave-2
  employment to zero for closed stores before running that check.
- AI's first draft overstated the precision of the price-extension result; the final
  version reports standard errors and significance levels transparently.

> To finalise before submission: re-run `python run_all.py` yourself, confirm the
> numbers in `results/` match the report, and adjust the "How I checked it" column above
> to reflect exactly the checks you personally performed.
