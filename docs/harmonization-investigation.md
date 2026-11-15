# Investigating the rejected harmonization candidate

## Confirmed result

This is a debugging handoff, not a new calibration approval. Both frozen models
were trained and evaluated in Actions run 43719416857. The combined forward
candidate failed two registered checks. The backward combined experiment passed
its registered checks; that does not override forward failure.

| Forward metric | Frozen result | Registered criterion |
| --- | --- | --- |
| Paired days / eligible weeks | 286 / 25 | At least 120 / 25 |
| Weekly Spearman | 0.866923 | At least 0.75 |
| Weekly PBias | −0.365777 | Absolute value at most 0.25: FAILED |
| Weekly MAE | 7,164.8183 MW | Strictly improve the matched naive MAE: FAILED |
| Naive MAE, identical cohort | 4,716.0188 MW | Reference benchmark |
| Relative MAE | 0.375023 | At most 0.45 |
| Daily PICP | 0.709790 | Between 0.70 and 0.92 |
| Median relative interval width | 1.135305 | At most 2.0 |

The candidate has higher absolute error than the benchmark. Correlation measures
ranking/co-movement, not agreement in magnitude: good Spearman does not cancel
negative bias. PBias −36.58% means the sum of the candidate's eligible weekly
means is about 36.58% below the sum of their observed S-NPP counterparts. It is
not a statement that every day is underestimated by that amount.

## What was actually fitted

The target is observed S-NPP FRP sum for the fixed official Pantanal reference,
with separate day/night turns. Terra and Aqua have their own models, stratified
by dry (July–November) / wet (December–June) season. Daily estimates require both
turns. Native positive observations do not establish cloud-free coverage.

- Forward fit uses available 2012–2015 and 2017–2019 training dates, within the
  registered 2012–2019 window. Test observations are fixed seasonal windows in
  2020–2024, not every date through 2026.
- Backward fit uses available seasonal windows in 2017–2024; its requested
  backward-test input spans January 20, 2012 through December 31, 2015.
- LOYO selection chooses median ratio or 99-quantile monotone EQM inside training.
  Quantiles use linear type-7 interpolation; duplicate X knots average target
  quantiles; EQM values outside the knot range clamp to endpoints.
- Nested outer LOYO excludes a year from method selection and weight estimation
  before collecting that year's residuals. Recompute same-platform/turn season
  fallback inside each selection fold; retain 30 dates and three training years.
- Inverse daily OOF MAE determines convex platform weights. Terra and Aqua
  estimates are averaged with those weights, never added as duplicate targets.
- The same frozen weights combine the native uncalibrated benchmark, with the
  same missing-platform fallback and exactly the same eligible paired weeks.
- Residual pools retain view, actual combination regime and season. Diagnostic
  Terra-only predictions do not add days to natural combined Terra-only fallback.

Forward weights: Terra 0.3851122187579056; Aqua 0.6148877812420944.
Backward weights: Terra 0.3923415904130353; Aqua 0.6076584095869647.
Forward selected five EQM and three median-ratio strata; backward six and two.

## Concrete leads, not established causes

1. **EQM endpoint saturation.** Clamping can limit predictions for extreme X.
   The forward Terra day/dry fit has X upper knot 8,668.328 MW and corresponding
   Y upper knot 23,021.4032 MW. Aqua day/dry has upper X 17,838.72 and upper
   Y 22,433.166 MW. These numbers make clipping worth measuring; they do not prove
   clipping caused the observed bias. First measure saturation in training OOF.
2. **Stratum direction.** Forward Terra night/wet median ratio is
   0.3581005586592179; Aqua day/wet is 1.2415487977369166 and night/wet
   1.3894472361809045. Scaling can decrease one component while increasing another.
   Inspect contributions and training ratios before attributing an aggregate bias.
3. **Selection objective.** Turn-level pooled OOF MAE chooses each candidate,
   whereas final acceptance includes daily combination and weekly bias. A method
   that wins that training objective need not improve the final held-out metric.
4. **Distribution and sampling.** Training contains complete backward years plus
   selected later windows. Forward test is seasonal and has only positive paired
   days. Orbit, detection capability, cloud/missingness and season/year composition
   are possible influences, not explanations established by this experiment.
5. **Implementation reconciliation.** Check routing, reference D/N sums, units,
   exclusion order and identical benchmark cohorts before proposing a new model.

## Investigation order

1. Reproduce the frozen report before editing anything. Preserve all source hashes,
   target values, model parameters, thresholds and the existing result.
2. Use the committed `frozen-models.json` to inspect per-stratum selection folds,
   OOF candidate MAE, routing, quantile knots, training dates, weights and residuals.
3. For training-only OOF diagnostics, summarize error/bias by year, season, turn,
   platform and availability regime; record sample sizes and excluded years.
4. Count EQM values at/beyond fitted endpoint knots in training OOF. Compare
   candidate-versus-naive errors on identical training cohorts and inspect extremes.
5. Reconcile selected native D/N values, complete-platform rules and convex sums.
   Missing turns must stay missing; raw negative/zero FRP is scientifically rejected.
6. A read-only breakdown of the spent holdout can describe the existing failure.
   Do not use it to select new coefficients, windows, thresholds or methods and then
   claim a fresh independent validation on the same records.
7. If code is wrong, report the exact defect and preserve the previous result.
   A revised scientific method needs a new evaluation plan and independent evidence.

Do not raise acceptance limits, replace missing observations with zeros, remove
unfavorable dates, borrow residual regimes, merge the native sensor scales, or
apply a post-hoc bias multiplier merely to turn the decision into Plan A.

## Files and reproducibility

- `docs/multiyear-evidence/experiment-summary.json`: all views, checks and denominators.
- `docs/multiyear-evidence/frozen-models.json`: exact parameters, folds and source/code hashes.
- `docs/multiyear-evidence/freeze-receipt.json`: pre-scoring receipt.
- `science/configs/thresholds.json`: unchanged registered acceptance criteria.
- `science/scripts/calibration_models.py`: fitting, routing, weights, intervals.
- `science/scripts/scientific_thresholds.py`: paired-week and decision evaluation.
- Model SHA-256: `145ca3df4e9a5b622b24a977ebf56b83639f59176c7d0bc7c2adaf29f2761ecd`.
- Source observation SHA-256: `142195cca6c1365f1d07c0507cc2c4c3a6e62932e73a7337cae021e90084863d`.

```sh
git switch -c research/harmonization-diagnostics origin/main
gh run download 43719416857 --name scientific-experiment-evidence --dir science/outputs/harmonization-review
```

The artifact includes `source-reconstruction/observations.json`, both prediction
files, frozen models and receipt. Reading these derived JSONs does not require
loading the 146 MB raw CSV set or querying NASA again. Keep local artifacts out of
Git. If a clean source rebuild is needed, use the source artifact from run
43716076914 and the documented scientific pipeline. Artifacts expire after 90 days.
Work in the research branch independently of the delivery UI branch; bring findings
back as a small reproducible report or isolated fix, not an overwritten final model.
