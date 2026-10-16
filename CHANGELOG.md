# Changelog

## Week 8 - Model & Pipeline Changes

**Week 7 results against predictions:** Three functions set a new best: F1 (1.91e-6, up from 7.7e-16), F3 (-0.014985, up from -0.020138) and F8 (9.892785, up from 9.890584). The local searches added last week helped: F3 landed on target and F4 recovered from -2.83 to 0.271, although F4 was still 2.8 standard deviations below its prediction. F7 was the biggest miss, 4.1 standard deviations below prediction.

- F1: log-space GP predicted log10|y| of 4.3 (an extrapolation), actual 1.91e-6. New best.
- F2: GP predicted 0.465 (std 0.221), actual 0.605.
- F3: local GP predicted -0.0125 (std 0.0196), actual -0.0150. New best.
- F4: local GP predicted 0.799 (std 0.187), actual 0.271.
- F5: GP predicted 2610.5 (std 133.2), actual 2369.0, now my second best result.
- F6: GP predicted -0.337 (std 0.136), actual -0.434.
- F7: GP predicted 1.696 (std 0.187), actual 0.925.
- F8: GP predicted 9.833 (std 0.194), actual 9.893. New best.

**Exploit around the best point:** With most functions now having an established best region, this round I exploited instead of exploring. For each function I searched a box of ±0.02 around its best point and chose the highest predicted value, excluding anything within 0.003 of a sampled point. The GPs were refitted with a floor of 0.05 on the length scale and normalised outputs, because the previous fits for F2 and F5 collapsed into spiky, near white-noise kernels (length scales of 0.0085 and 1e-5) that made local predictions meaningless. Small steps were chosen on purpose, since F2, F4 and F7 have all dropped sharply when moving away from their best. Expected gains are small (about 1 to 3 percent where the model predicts any). These searches were run outside the main script, so the script itself has not changed beyond loading the Week 7 data.

**F1 is the exception:** I tried fitting a single Gaussian bump to F1's positive outputs, on the idea that log10(y) would then be a simple curved surface. It failed a hold-out test: fitted without the newest point, it predicted 10^-31 for a value that was actually 10^-5.7, and its centre estimate moved across x1 0.48 to 0.63 and x2 0.55 to 0.75 when resampled. F1 appears to have several narrow, separate features (a large negative spike near [0.650, 0.682] and a positive one near my best point) that a GP cannot pin down with this few points. Since F1's outputs are exact (repeated queries returned identical values), I am switching to a pattern search, a basic derivative-free method. A small step from the best point shows which direction the value climbs. Week 8 steps +0.012 in x2, Week 9 steps +0.012 in x1, and Week 10 jumps along the combined direction. A large rise means keep going that way, and a drop means reverse. The cost is that this takes about three weeks, with one query per week.

**Model choice per function (Week 8 queries):**

- F1: Pattern search probe, `[0.582552, 0.564941]`. A GP and a Gaussian bump both failed on this data, so I am measuring the direction of improvement directly with a small step in x2.
- F2: Exploit GP, `[0.699372, 0.911737]`. Predicted 0.587 (std 0.085), slightly below my best of 0.6112, so this is a close neighbour probe on a noisy peak (three points within 0.007 scored 0.611, 0.606 and 0.510) and not an expected gain.
- F3: Exploit GP, `[0.421890, 0.412697, 0.464681]`. Predicted -0.0133 (std 0.0115) against a best of -0.0150, continuing the trend of the last local search.
- F4: Gradient step, `[0.367331, 0.419785, 0.411319, 0.396967]`. The refitted GP predicts nothing above my best anywhere nearby, so I estimated a direction from the four nearest points instead. Every step towards higher x1 lost value, so this is a 0.02 step towards lower x1 and x2. Low confidence, since it is four equations for four unknowns.
- F5: Exploit GP, `[0.368833, 0.874433, 1.000000, 1.000000]`. Predicted 3023.6 (std 54.1) against a best of 2986.9. Two inputs sit at the upper limit of 1.0 because the search box was clipped there.
- F6: Exploit GP, `[0.451463, 0.383362, 0.638745, 0.795203, 0.137146]`. Predicted -0.1761 (std 0.0139) against a best of -0.1902. Last week's move away from the best lost value, so I am staying close to it.
- F7: Exploit GP, `[0.024039, 0.163217, 0.318627, 0.186638, 0.379364, 0.751014]`. Predicted 2.1007 (std 0.0787) against a best of 2.0242. Last week's global pick missed by 4.1 standard deviations, so I am staying within the best region.
- F8: Exploit GP, `[0.275641, 0.051067, 0.092131, 0.088784, 0.933418, 0.490818, 0.173071, 0.626653]`. Predicted 9.9197 (std 0.0153) against a best of 9.8928, continuing the steady climb.

## Week 7 - Model & Pipeline Changes

**Week 6 results against predictions:** Only F6 set a new best (-0.190210, up from -0.312637). The Random Forest's uncertainty held up well: all four RF picks landed within about 1.1 standard deviations of their prediction. The GP was overconfident on F3 (1.4 std below prediction) and F4 (about 6 std below), but did better than predicted on F6. With only eight points this is a hint rather than proof.

- F1: RF EI predicted -0.0004, actual ~0 (2.0e-160). Flat again.
- F2: RF predicted 0.489 (std 0.191), actual 0.510.
- F3: GP EI predicted -0.011 (std 0.070), actual -0.109.
- F4: GP predicted 2.191 (std 0.808), actual -2.828.
- F5: RF predicted 2478.8 (std 891.6), actual 1956.6, now my third best result.
- F6: GP EI predicted -0.397 (std 0.107), actual -0.190, a new best.
- F7: RF predicted 1.716 (std 0.593), actual 1.059.
- F8: GP EI predicted 9.878 (std 0.177), actual 9.733.

**F1 log-space surrogates:** F1's outputs range from 1e-245 up to 1e-3, so a GP or Random Forest fitted on the raw values cannot tell points apart, because squared error treats everything near zero as identical. Added `log_magnitude()` to `surrogate_models.py`, which converts outputs to log10 of their absolute value (exact zeros are floored at about 1e-323 so they do not become infinity). F1 now also has a GP and a Random Forest fitted on those log values, printed alongside the original raw-value models. In log terms there is a clear gradient, and the log-space GP points to `[0.582552, 0.552941]`, the middle of the cluster of my strongest-magnitude points, instead of the corners the raw-value GP kept choosing. Its predicted value there is an extrapolation, so only the location should be trusted. The sign of the output is dropped in this model, and F1 does change sign, so this finds the active region rather than the exact peak.

**Local search for F3 and F4:** The global search samples 10,000 random points across the whole range. For F3 and F4 it chose far-off points that the models themselves predicted to be poor (F4's GP predicted -13 at its pick, against a best of 0.3675), because uncertainty is highest in the empty regions. Added `local_candidates()` to `plotting_utils.py` and a local search block for each function, which samples 20,000 candidates within ±0.04 of the current best point, removes anything within 0.001 of a sampled point, and scores the rest with EI. It uses its own random generator, so it does not shift the random candidates for the other functions. This only refines around a known peak and cannot find a different one, so it is only suitable where the best region is already located.

**Model choice per function (Week 7 queries):**

- F1: Log-space GP, EI, `[0.582552, 0.552941]`. The raw-value models cannot see the gradient, and this is a new region in the middle of the best-magnitude points.
- F2: GP, UCB and EI agree, `[0.697363, 0.924057]`. The RF points to the same region, and the GP has the higher predicted mean (0.465 vs 0.368).
- F3: Local GP search, `[0.440115, 0.432545, 0.483849]`. The global picks went to the edges with worse predicted means than my best, so I refine around the best point instead (predicted -0.0125 against -0.0201).
- F4: Local GP search, `[0.403556, 0.394705, 0.411007, 0.391402]`. Both global picks were far-off exploration, and the output falls off sharply around the best point. The predicted 0.799 is optimistic and should not be taken at face value.
- F5: GP, UCB and EI agree, `[0.295410, 0.843355, 0.963558, 0.983218]`. The RF points to the same high-value corner, and the GP now has real signal there (2610.5, std 133.2).
- F6: GP, UCB and EI agree, `[0.462193, 0.356005, 0.790249, 0.946497, 0.010447]`. The GP was right last week. Its predicted mean (-0.337) is below my new best, so this is an exploration move.
- F7: GP, UCB, `[0.066665, 0.164650, 0.371860, 0.143913, 0.531545, 0.861796]`. Highest predicted mean (1.696) and close to my best region. The RF missed last week and its new pick wanders far from the productive region.
- F8: GP, EI, `[0.295487, 0.058669, 0.090934, 0.073349, 0.953221, 0.508102, 0.191138, 0.616910]`. Predicted mean 9.833 (std 0.194), a safe refinement near my current best.

**Limitation noted:** Picks for the higher-dimensional functions (F4, F5, F8) change when the random candidate set changes, because 10,000 random points is a coarse search in 4 to 8 dimensions. Adding one more GP fit earlier in the script shifted those three picks, so they should be read as good directions rather than exact optima.

## Week 6 - Model & Pipeline Changes

**Random Forest surrogate:** Up to now I'd only used a GP with UCB/EI, so I added a Random Forest as a second surrogate model to compare against on every function. Implemented in `surrogate_models.py` as `fit_random_forest_surrogate()` and `random_forest_predict()` — since sklearn's `RandomForestRegressor` doesn't give an uncertainty estimate directly, `random_forest_predict()` computes std as the spread across each individual tree's prediction, so it slots into the existing UCB/EI functions unchanged. Rolled out to func1 and func5 first, then func7/func8, then func2/func3/func4/func6, so all 8 functions now print a GP pick and an RF pick side by side.

- func1: RF proposed a genuinely different point to GP, which kept returning to the same known-flat corners regardless of kernel/κ changes.
- func5: RF was the clearest win — its predicted mean (2478.80) landed near my actual best known point, while GP had no real signal that far from data (mean 0, std 316).
- func4: RF's predictions here are not trustworthy — mean of -6.65 (std 8.71), way outside the observed range (-1.28 to 0.37). With only 35 points in 4D it looks like the RF is extrapolating noise rather than learning structure, so I'm ignoring RF for func4 until there's more data.

**Duplicate-query safeguard:** Realised GP had recommended a point I'd already sampled (func1's Week 4 query was an exact repeat of Week 3's). Added `unsampled_mask()` to `plotting_utils.py`, which excludes any candidate within 0.001 (Euclidean) of an already-sampled point before picking the argmax on UCB/EI, so acquisition can no longer suggest re-running an experiment I've already done. Applied across all 8 functions.

**Model choice per function (GP vs. RF):**

- F1: RF (EI). GP's UCB/EI both kept landing on points I'd already sampled or on the same flat corners; RF proposed genuinely new territory to explore instead.
- F2: RF (UCB/EI agree). RF's pick is almost identical to my current best point but with a higher predicted mean (0.4893 vs GP's 0.4105) — both models agree the region is good, RF is just more optimistic.
- F3: GP (EI). GP EI has the least-negative predicted mean of any of the four options (-0.0113 vs RF's -0.1121); the landscape here is flat enough that RF isn't adding real signal over GP.
- F4: GP (UCB/EI agree). RF's predictions are not trustworthy here — mean of -6.65 (std 8.71) is way outside anything ever observed (-1.28 to 0.37), which looks like extrapolation noise rather than learned structure given only 35 points in 4D.
- F5: RF (UCB/EI agree). RF's predicted mean (2478.80) sits near my actual best known point; GP has no real signal this far from data (mean 0, std 316 — essentially a blind guess).
- F6: GP (EI). Best predicted mean of all four candidates (-0.3970 vs RF's best of -0.8256).
- F7: RF (UCB/EI agree). Similar mean to GP (1.7164 vs 1.6919) but RF reports much higher, more honest uncertainty (std 0.5929 vs GP's 0.1918).
- F8: GP (EI). A safe refinement close to my current best (9.8906) rather than RF's much larger, riskier exploratory jump.
