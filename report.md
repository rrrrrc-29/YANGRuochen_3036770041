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

**Sample construction.** We follow the paper's sample definitions. For the descriptive
means (Table 2) and the level/change tabulations (Table 3), each cell uses all stores
with non-missing data for the relevant variable; wave-2 employment is set to zero for
the six permanently closed stores and treated as missing for the four temporarily
closed stores and one refusal. The *balanced subsample* (Table 3, row 4) consists of the
384 stores with employment in both waves (309 NJ, 75 PA). The *regression sample*
(Table 4) further requires a valid wave-1 starting wage (needed to construct the wage
gap), leaving 365 stores; the paper's analogous sample is 357. The raw survey data are
included in the repository under `data/raw/`.

**Variable definitions.**

| Variable | Definition |
| --- | --- |
| FTE employment | `EMPFT + NMGRS + 0.5 * EMPPT` (full-time + managers + half of part-time) |
| Headcount | `EMPFT + EMPPT + NMGRS` |
| `NJ` (treatment) | 1 if `STATE == 1`, 0 if Pennsylvania |
| Change in FTE, `dfte` | wave-2 FTE minus wave-1 FTE |
| Wage gap, `GAP` | `(5.05 − W1)/W1` for NJ stores with wave-1 wage `W1 < 5.05`; 0 otherwise |
| % full-time | `100 * EMPFT / FTE` (full-time, excluding managers, as a share of FTE) |
| Full-meal price | `PSODA + PFRY + PENTREE` (medium soda + small fries + entree, incl. tax) |
| Controls | chain dummies (`CHAIN`), company-owned (`CO_OWNED`), NJ sub-region dummies (`CENTRALJ`, `SOUTHJ`, with north NJ omitted) and PA sub-region dummies (`PA1`, `PA2`) |

**Cleaning log.** All cleaning is coded in `src/prep.py` and reproduced by
`run_all.py`. Missing starting wages are kept as a separate category where the paper
reports wage distributions; employment outcomes are computed only from non-missing
components.

## 3. Empirical design

The DiD estimand is

$$ \delta \;=\; (\text{NJ}_{\text{after}} - \text{NJ}_{\text{before}}) \;-\; (\text{PA}_{\text{after}} - \text{PA}_{\text{before}}). $$

We estimate it by ordinary least squares on first differences,

$$ \Delta\text{FTE}_i = \alpha + \delta\,\text{NJ}_i + \varepsilon_i, $$

which is numerically identical, in a balanced panel, to the two-way fixed-effects
specification $\text{FTE}_{it} = \beta\,\text{NJ}_i + \gamma\,\text{After}_t +
\delta\,(\text{NJ}_i \times \text{After}_t) + \varepsilon_{it}$. Standard errors are
conventional (homoskedastic) OLS, matching the paper's Table 4. We then add controls
successively: chain and ownership dummies, then the wage gap (`GAP`) as a
treatment-intensity variable, then regional dummies.

**Identification.** The identifying assumption is parallel trends: absent the wage
increase, employment in NJ and PA would have evolved identically. With only two waves
the assumption cannot be tested directly; we support it by (i) the regional proximity
of the two states, (ii) a compliance check showing the wage increase was actually
implemented (Table 2), and (iii) robustness of the estimate to controls and sample
choices (Table 6). Within New Jersey, comparing low-wage stores (which should be
affected) with high-wage stores (which should not) provides a further specification
test, and the paper shows this comparison is passed.

## 4. Core replication results and comparison with the original paper

**Table 2 — descriptive means.** The table reproduces the paper's Table 2. Wave-1
starting wages average $4.61 in NJ and $4.63 in PA, with 30.5% of NJ stores and 32.9%
of PA stores paying exactly the old $4.25 minimum. After the increase, the NJ mean wage
rises to $5.08 while PA is unchanged at $4.62; 85.5% of NJ stores report a starting
wage of exactly $5.05 in wave 2, versus 1.3% in PA. The treatment was implemented as
intended (Figure 1). Employment in wave 1 averaged 20.4 FTE in NJ and 23.3 in PA; the
fraction full-time was 32.9% (NJ) and 35.0% (PA), rising to 35.9% and falling to 30.4%
in wave 2 — the two variables the paper flags as showing a relative NJ increase besides
wages. The full-meal price rose from $3.35 to $3.41 in NJ but was flat at $3.04 in PA.

**Table 3 — average employment and the main DiD.**

| FTE employment | PA | NJ | NJ−PA | NJ: $4.25 | NJ: $4.26–4.99 | NJ: ≥$5.00 | Low−High | Mid−High |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Before, all available | 23.33 | 20.44 | −2.89 | 19.56 | 20.08 | 22.25 | −2.69 | −2.17 |
| After, all available | 21.17 | 21.03 | −0.14 | 20.88 | 20.96 | 20.21 | +0.66 | +0.74 |
| Change in mean FTE | −2.17 | +0.59 | **+2.75** | +1.32 | +0.87 | −2.04 | +3.36 | +2.91 |
| Change, balanced sample | −2.28 | +0.47 | **+2.75** | +1.20 | +0.71 | −2.16 | +3.36 | +2.87 |
| Change, temp-closed = 0 | −2.28 | +0.23 | **+2.51** | +0.90 | +0.49 | −2.39 | +3.29 | +2.88 |

FTE employment rose in NJ and fell in PA, so the DiD estimate is positive: **+2.75 FTE
workers**, essentially identical to the paper's headline +2.76. Our balanced
first-difference regression gives a conventional standard error of 1.15 (t = 2.38). The
estimate is unchanged when the sample is restricted to the balanced subsample (row 4)
and only slightly smaller when wave-2 employment at the temporarily closed stores is
set to zero (row 5, +2.51). Within New Jersey, employment expanded at the low-wage
stores (paying $4.25 in wave 1, +1.20 balanced) and contracted at the high-wage stores
(≥$5.00, −2.16 balanced) — the high-wage change is almost identical to the PA change of
−2.28, exactly as the paper reports, providing a within-state specification test.

**Table 4 — reduced-form models for the change in employment.** The dependent variable
is the change in FTE employment; sample N = 365 (the paper uses 357).

| Model | Coefficient | s.e. | t | N |
| --- | ---: | ---: | ---: | ---: |
| (i) NJ dummy | +2.36 | 1.15 | 2.06 | 365 |
| (ii) NJ + chain & ownership | +2.33 | 1.15 | 2.02 | 365 |
| (iii) GAP | +15.89 | 5.95 | 2.67 | 365 |
| (iv) GAP + chain & ownership | +15.19 | 6.08 | 2.50 | 365 |
| (v) GAP + chain & ownership + region | +12.03 | 7.32 | 1.64 | 365 |

The NJ dummy is positive and stable across specifications (2.36 and 2.33). The `GAP`
coefficient implies that a store initially paying the old $4.25 minimum (GAP = 0.188)
gained about 0.188 × 15.89 ≈ 3.0 FTE workers relative to an unaffected store. Adding
the regional dummies attenuates the GAP coefficient to 12.03 and raises its standard
error, so that column (v) is no longer significant at the 5% level — precisely the
pattern the paper reports and attributes to measurement error in the starting wage.

**Comparison with the original paper.** Every point estimate is reproduced to within
sampling noise:

| Estimate | Ours | Paper |
| --- | ---: | ---: |
| Table 3 DiD (change in mean FTE) | +2.75 | +2.76 (t = 2.03) |
| Table 4 (i) NJ dummy | +2.36 (1.15) | +2.33 (1.19) |
| Table 4 (iii) GAP | +15.89 (5.95) | +15.65 (6.08) |
| Table 4 (v) GAP + region | +12.03 (7.32) | +11.91 (7.39) |

The small residual differences are driven by the sample: our Table 4 regression sample
has 365 stores against the paper's 357, reflecting a few stores whose wave-2 starting
wage is missing in the public file. The headline conclusion — no employment decline,
and a positive point estimate — is reproduced exactly.

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
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Medium soda | +0.000 | +0.008 | −0.005 | 0.008 | −0.62 | 380 |
| Small fries | +0.017 | +0.019 | −0.001 | 0.009 | −0.10 | 366 |
| Entree | +0.043 | −0.033 | **+0.088** | 0.045 | 1.94 | 375 |

**Interpretation.** Soda and fries show no detectable pass-through. The entree — the
highest-priced item — rose by about 8.8 cents in NJ relative to PA (t = 1.94), roughly
6.5% of the ~$1.35 entree price. This is consistent with *partial, item-specific*
pass-through: restaurants absorbed most of the wage increase (in line with the finding
that employment did not fall) while adjusting a single higher-margin menu item. The
result is economically modest relative to the $0.80 wage increase, indicating that most
of the cost was absorbed through other margins (labour demand, hours, or margins).

## 6. Validation, limitations, and conclusion

**Validation.** (i) The compliance check (Table 2) confirms the treatment was binding
and implemented. (ii) The main DiD is stable across controls (Table 4) and sample
choices (Table 6): +2.75 for FTE, +2.41 for headcount, and +2.42 when closed stores
are treated as having zero wave-2 employment. Restricting to "compliers" — stores paying
exactly the old $4.25 minimum before the increase — *strengthens* the result to +3.22
(t = 1.81), consistent with a treatment-intensity story: the most-treated stores show
the largest relative employment gain. The full-time/part-time split (+0.69 full-time,
−1.36 part-time, both insignificant) suggests the relative gain was concentrated among
full-time workers.

**Limitations.** (i) With only two waves, the parallel-trends assumption cannot be
tested; the design relies on the regional comparison. (ii) Treatment is assigned by
state, not at random, and the early 1990s recession may have hit the two states
differently. (iii) Some NJ stores already paid ≥ $5.05 before the increase, attenuating
the measured effect. (iv) Conventional standard errors do not address spatial
correlation across stores within a labour market. (v) Survey non-response and store
closures are potential sources of selection, which we address but cannot fully rule
out.

**Conclusion.** The replication reproduces Card & Krueger's central finding: New
Jersey's minimum-wage increase did not reduce fast-food employment relative to
Pennsylvania; the DiD point estimate is positive (+2.75 FTE, matching the paper's
+2.76). The extension adds a new, testable margin — menu-price pass-through — and finds
modest, item-specific pass-through concentrated in the entree, consistent with firms
absorbing the cost largely through margins rather than employment or prices.

---

## References

Card, David, and Alan B. Krueger. 1994. "Minimum Wages and Employment: A Case Study of
the Fast-Food Industry in New Jersey and Pennsylvania." *American Economic Review*
84(4): 772–793.
