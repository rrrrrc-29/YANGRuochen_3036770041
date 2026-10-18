# Replication of Card & Krueger (1994): Minimum Wages and Employment

*A Difference-in-Differences Analysis of the New Jersey Fast-Food Industry*

**YANG Ruochen** · Student ID: 3036770041

---

## 1. Research question and motivation

**Question.** Did New Jersey's April 1, 1992 increase in the minimum wage from $4.25 to
$5.05 per hour reduce employment in fast-food restaurants?

**Motivation.** The paper is the canonical application of the difference-in-differences
(DiD) design and the most influential empirical test of the competitive theory of the
labour market. A textbook competitive model predicts that a binding minimum wage
reduces employment along the labour-demand curve. Card and Krueger exploit a natural
experiment: New Jersey (NJ) raised its minimum wage while neighbouring eastern
Pennsylvania (PA), across the Delaware River, left its wage floor unchanged at $4.25.
The two states share a regional labour market, making PA a credible comparison group.

**Hypotheses.** Under the competitive benchmark the NJ–PA difference in employment
growth should be negative. Under monopsony or search-friction models, employment may be
unchanged or even rise. The paper's headline finding — no evidence of an employment
decline, and if anything a relative increase — is the result we set out to reproduce.

## 2. Data sources, sample construction, and variable definitions

**Source.** Public replication data from Card & Krueger (1994), distributed as the
Princeton restaurant survey (`public.csv`). The file contains 410 store-level
observations (46 columns): 331 stores in New Jersey (`STATE = 1`) and 79 in eastern
Pennsylvania (`STATE = 0`), from four chains — Burger King (171), KFC (80), Roy Rogers
(99), and Wendy's (60). Stores were surveyed twice: wave 1 in February–March 1992
(before the increase) and wave 2 in November–December 1992 (after).

**Sample construction.** The core analysis uses a balanced panel of stores that
answered wave 2 and remained open (`STATUS2 = 1`): 399 stores (321 NJ, 78 PA). Eleven
stores are excluded: 6 permanent closures, 2 renovation closures, 1 highway-construction
closure, 1 mall-fire closure, and 1 refusal. After listwise deletion of observations
missing employment components in either wave, the FTE regressions use 378 stores. We do
not publish the raw data; see `README.md` for access instructions.

**Variable definitions.**

| Variable | Definition |
| --- | --- |
| FTE employment | `EMPFT + 0.5 * EMPPT + NMGRS` (full-time + managers + half of part-time) |
| Headcount | `EMPFT + EMPPT + NMGRS` |
| `NJ` (treatment) | 1 if `STATE == 1`, 0 if Pennsylvania |
| Change in FTE, `dfte` | wave-2 FTE minus wave-1 FTE |
| Menu prices | `PSODA`, `PFRY`, `PENTREE` (medium soda, small fries, entree, incl. tax) |
| Controls | chain dummies (`CHAIN`), company-owned (`CO_OWNED`), NJ sub-region dummies (`SOUTHJ`, `CENTRALJ`, `SHORE`; north NJ omitted), initial wage `WAGE_ST` |

**Cleaning log.** All cleaning is coded in `src/prep.py` and reproduced by
`run_all.py`. Missing starting wages are kept as a separate "missing" category in
Table 2; employment outcomes are computed only from non-missing components, so stores
with a missing FTE component in either wave drop out of the corresponding regression
(378 of 399 balanced stores).

## 3. Empirical design

The DiD estimand is

$$ \delta \;=\; (\text{NJ}_{\text{after}} - \text{NJ}_{\text{before}}) \;-\; (\text{PA}_{\text{after}} - \text{PA}_{\text{before}}). $$

We estimate it by ordinary least squares on first differences,

$$ \Delta\text{FTE}_i = \alpha + \delta\,\text{NJ}_i + \varepsilon_i, $$

which is numerically identical, in a balanced panel, to the two-way fixed-effects
specification $\text{FTE}_{it} = \beta\,\text{NJ}_i + \gamma\,\text{After}_t +
\delta\,(\text{NJ}_i \times \text{After}_t) + \varepsilon_{it}$. Standard errors are
heteroskedasticity-robust (HC1). We then add controls successively (Table 4).

**Identification.** The identifying assumption is parallel trends: absent the wage
increase, employment in NJ and PA would have evolved identically. With only two waves
the assumption cannot be tested directly; we support it by (i) the regional proximity
of the two states, (ii) a compliance check showing the wage increase was actually
implemented (Table 2), and (iii) robustness of the estimate to controls and sample
choices (Table 6).

## 4. Core replication results and comparison with the original paper

**Table 2 — compliance.** Wave-1 starting wages are spread across $4.25–$5.06+ in both
states. In wave 2, 85.5% of NJ stores report a starting wage in $5.01–$5.05, and the NJ
mean wage rises from $4.61 to $5.08. Pennsylvania is unchanged (mean $4.63 → $4.62).
The treatment was implemented as intended (Figure 1).

**Table 3 — main DiD.**

| Outcome | NJ wave 1 | NJ wave 2 | NJ change | PA wave 1 | PA wave 2 | PA change | **DiD** | s.e. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FTE employment | 20.60 | 21.36 | +0.66 | 23.40 | 21.44 | −2.06 | **+2.72** | 1.34 |
| Headcount | 29.99 | 30.64 | +0.49 | 33.13 | 31.55 | −1.84 | **+2.33** | 1.45 |

FTE employment rose in NJ and fell in PA, so the DiD estimate is positive: +2.72 FTE
workers (t = 2.04). There is no evidence of a negative employment effect.

**Table 4 — regression estimates (dependent variable: change in FTE).**

| Specification | NJ coefficient | s.e. | t | N |
| --- | --- | --- | --- | --- |
| NJ only | +2.722 | 1.335 | 2.04 | 378 |
| + chain & ownership | +2.780 | 1.344 | 2.07 | 378 |
| + region dummies | +3.097 | 1.462 | 2.12 | 378 |
| + initial wage | +2.628 | 1.469 | 1.79 | 359 |

The estimate remains positive and of similar magnitude across specifications.

**Comparison with the original paper.** Card & Krueger's Table 3 reports a balanced-panel
FTE DiD of **+2.75** (s.e. ≈ 1.36), with NJ employment rising about +0.6 FTE and PA
falling about −2.2 FTE. Our estimate of **+2.72** (s.e. 1.34) is essentially identical.
The small level differences (NJ change +0.66 vs. +0.59; PA change −2.06 vs. −2.16) arise
from a minor sample difference: we use the `STATUS2 == 1` balanced panel with listwise
deletion of missing employment components (N = 378), whereas the original paper's
balanced sample was constructed directly from the survey sheets. The headline
conclusion — no employment decline, a point estimate that is positive — is reproduced
exactly.

## 5. Independent extension: menu-price pass-through

**Question.** The minimum wage raised the cost of labour. Did restaurants pass any of
that cost through to consumers via higher menu prices? The original paper discusses
prices descriptively but does not estimate a formal DiD for them.

**Design.** We apply the same DiD design to the change in each of the three menu prices
recorded in both waves (medium soda, small fries, entree), with chain and ownership
controls:

$$ \Delta\text{Price}_i = \alpha + \delta\,\text{NJ}_i + X_i'\gamma + \varepsilon_i. $$

**Results.**

| Menu item | NJ mean change | PA mean change | **DiD** | s.e. | t | N |
| --- | --- | --- | --- | --- | --- | --- |
| Medium soda | +0.001 | +0.008 | −0.005 | 0.008 | −0.61 | 379 |
| Small fries | +0.017 | +0.019 | −0.001 | 0.008 | −0.11 | 365 |
| Entree | +0.043 | −0.033 | **+0.088** | 0.043 | 2.06 | 374 |

**Interpretation.** Soda and fries show no detectable pass-through. The entree — the
highest-priced item — rose by about 8.8 cents in NJ relative to PA (t = 2.06), roughly
6.5% of the ~$1.35 entree price. This is consistent with *partial, item-specific*
pass-through: restaurants absorbed most of the wage increase (in line with the finding
that employment did not fall) while adjusting a single higher-margin menu item. The
result is economically modest relative to the $0.80 wage increase, indicating that most
of the cost was absorbed through other margins (labour demand, hours, or margins).

## 6. Validation, limitations, and conclusion

**Validation.** (i) The compliance check (Table 2) confirms the treatment was binding
and implemented. (ii) The main DiD is stable across controls (Table 4). (iii) Robustness
checks (Table 6) confirm the result is not driven by sample choice: the estimate is
+2.72 for FTE, +2.33 for headcount, and +2.42 when closed stores are treated as having
zero wave-2 employment. Restricting to "compliers" — stores paying exactly the old $4.25
minimum before the increase — *strengthens* the result to +3.64 (t = 2.04), consistent
with a treatment-intensity story: the most-treated stores show the largest relative
employment gain. The full-time/part-time split (+0.92 full-time, −1.56 part-time, both
insignificant) suggests the relative gain was concentrated among full-time workers.

**Limitations.** (i) With only two waves, the parallel-trends assumption cannot be
tested; the design relies on the regional comparison. (ii) Treatment is assigned by
state, not at random, and the early 1990s recession may have hit the two states
differently. (iii) Some NJ stores already paid ≥ $5.05 before the increase, attenuating
the measured effect. (iv) Robust standard errors do not address spatial correlation
across stores within a labour market. (v) Survey non-response and store closures are
potential sources of selection, which we address but cannot fully rule out.

**Conclusion.** The replication reproduces Card & Krueger's central finding: New
Jersey's minimum-wage increase did not reduce fast-food employment relative to
Pennsylvania; the DiD point estimate is positive (+2.72 FTE, matching the paper's
+2.75). The extension adds a new, testable margin — menu-price pass-through — and finds
modest, item-specific pass-through concentrated in the entree, consistent with firms
absorbing the cost largely through margins rather than employment or prices.

---

## References

Card, David, and Alan B. Krueger. 1994. "Minimum Wages and Employment: A Case Study of
the Fast-Food Industry in New Jersey and Pennsylvania." *American Economic Review*
84(4): 772–793.
