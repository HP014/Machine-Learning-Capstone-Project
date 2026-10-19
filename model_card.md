# Model Card

## Model Description

**Input:** For each of the eight functions, the model is fitted to every query made so far: a list of input points, each a vector of 2 to 8 numbers between 0 and 1 (F1 and F2 have 2, F3 has 3, F4 and F5 have 4, F6 has 5, F7 has 6, F8 has 8), together with the output each one returned. To make a prediction, it takes any candidate input point in the same range.

**Output:** For a candidate point, the models give a predicted output (a mean) and an uncertainty (a standard deviation). An acquisition function turns these into a score, and the final output of the process is the next point to query for each function, one per function per week.

**Model Architecture:**
- **Gaussian Process regression** (scikit-learn `GaussianProcessRegressor`). The kernel is RBF for F1 and F2 and Matern (smoothness 2.5 or 1.5) for F3 to F8. Kernel parameters are fitted by maximising the log marginal likelihood with 10 random restarts. Later refits use a floor of 0.05 on the length scale and normalised outputs.
- **Random Forest regression** (200 trees, seed 42). The mean is the average over trees and the uncertainty is the standard deviation across trees.
- **Acquisition:** Upper Confidence Bound (mean plus kappa times uncertainty) and Expected Improvement, applied to 10,000 random candidate points, with a rule that excludes any candidate within 0.001 of an already-sampled point.
- **Adaptations:** log-space versions of both models for F1 (the output is converted to the log of its absolute value), a local search in a ±0.04 box around the best point for F3 and F4, a small-step pattern search for F1, and in the final rounds a search for the highest predicted value within ±0.02 of each best point.

## Performance

**How performance is measured.** This is not a standard train/test problem. There are very few points and each new point is only available once I submit it, so I measure two things:

1. **Optimisation outcome:** the best output found so far per function. All eight functions improved over the eight weeks, and all eight set a new best in Week 8 (see the table in `README.md` and `results/figures/fig1_best_so_far.png`).
2. **Prediction quality:** before each weekly query, I recorded the model's predicted output and uncertainty for the point I chose. Once the real output came back, I measured the error in standard deviations, `(actual - predicted) / predicted std`. This is the only out-of-sample check available, because the real output was never used to fit the prediction it is compared with. The log is in `results/prediction_log.csv`.

| Model | Predictions | Within 1 std | Within 2 std | Mean absolute error in std |
|---|---|---|---|---|
| GP | 17 | 47% | 71% | 1.87 |
| Random Forest | 3 | 67% | 100% | 0.60 |

The data covers Weeks 6 to 8 and excludes F1, whose predictions are on a different scale. The Random Forest figures come from only three predictions, so they are not a reliable comparison with the GP. A well-calibrated model would be within one standard deviation about 68% of the time.

![Prediction error](results/figures/fig5_prediction_error.png)

## Limitations

- **Very little data.** Each function has between 18 and 48 points, in 2 to 8 dimensions. Every conclusion here is tentative.
- **Overconfidence.** The GP was wrong by a large amount for F3, F4 and F7, by up to about 6 standard deviations in earlier weeks, so its uncertainty is often too small.
- **Assumptions that do not hold for every function.** The GP assumes a smooth function with a moderate output range. F1 breaks this (outputs from about 1e-245 to 1e-3), and neither the GP nor the Random Forest learned anything useful from it on raw values. The log-space version drops the sign of the output, and F1 does change sign.
- **Random Forest extrapolation.** In Week 6 the Random Forest predicted values far outside anything observed for F4 (a mean of about -6.7 with a standard deviation of about 8.7, against observed values between -1.3 and 0.4).
- **Coarse candidate search.** Choosing from 10,000 random points is coarse in 4 to 8 dimensions, and the chosen points for F4, F5 and F8 changed when one extra model fit shifted the random numbers. The picks are better read as good directions than exact optima.
- **No noise check.** I treated the outputs as exactly repeatable because repeated queries returned identical values, but I have not tested this further.
- **Local searches cannot find new peaks.** The exploit steps refine around a known best point and could miss a better region elsewhere.
- **Duplicates.** Four early rows are repeated queries. They were kept and slightly over-weight those points.

## Trade-offs

- **Exploration versus exploitation.** Large kappa or xi values explore unfamiliar regions and risk wasted queries (a week spent on a poor point). Small steps around the best point were reliable in the final rounds, but they risk settling on a local peak. I chose this balance per function by judgement, not by search.
- **GP versus Random Forest.** The GP gives smoother, better-calibrated uncertainty when its assumptions hold, but fails on extreme scales and rough functions, and gets more expensive as data grows. The Random Forest is robust to scale and roughness, but it extrapolates poorly with little data in higher dimensions, as it did for F4.
- **Cost of a query.** Only one real query per function per week is allowed, so there is little room to test a model idea. This is why methods were checked on past data and with small steps before being used.
- **Where it performs poorly.** Functions with sharp, narrow features (F1, and the peak around F4's best point) and the higher-dimensional functions, where the data is thinnest.
