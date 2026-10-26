# Changelog

## Week 10 - Model & Pipeline Changes

**Week 9 results against predictions:** Five functions set a new best: F3 (-0.0054, up from -0.0124), F4 (0.6169, up from 0.6082), F5 (3341.8, up from 3174.8), F7 (2.3325, up from 2.2010) and F8 (9.9276, up from 9.9100). F1, F2 and F6 did not improve. F5 and F8 landed almost exactly on their predictions, F3 and F7 beat theirs by about 1.3 and 1.1 standard deviations, and F2 landed 1.5 standard deviations below.

- F1: the +0.012 x1 probe returned -8.4e-5, so the sign flipped. The best is unchanged at 2.30e-5.
- F2: predicted 0.660 (std 0.078), actual 0.542.
- F3: predicted -0.0110 (std 0.0041), actual -0.0054.
- F4: direction step, actual 0.6169 (a gain of only 0.009, after 0.24 the week before).
- F5: predicted 3335.1 (std 24.7), actual 3341.8.
- F6: predicted -0.142 (std 0.054), actual -0.1838.
- F7: predicted 2.303 (std 0.027), actual 2.3325.
- F8: predicted 9.9287 (std 0.0136), actual 9.9276.

**F1 uses a smaller probe:** The x1 step flipped the sign of F1's output (positive at x1 = 0.5826, -8.4e-5 at 0.5946), so F1 changes sign on a scale finer than my 0.012 step. The next probe steps back by 0.006 in x1 and keeps x2 fixed. With three points along x1 at the same x2, the profile along that direction can be fitted and the positive peak located, if F1 behaves like a wave. The GP's own pick extrapolates to a predicted value of about 0.09, which I do not believe, so I did not use it.

**Pattern search when gains fade or fail (F4 and F6):** F4's gain shrank to +0.009 after +0.24 the week before, so I am halving the step along the same direction. F6 lost 0.08 on its last step. The refitted GP keeps proposing points next to that failed one, even with a larger exclusion zone, because it predicts everything nearby is worse than the best. I therefore halved the step that worked two weeks earlier (lower x1, x2, x3 and x4, higher x5). Both picks are low confidence.

**Dials unchanged:** kappa and xi were left at their script values for the same reasons as before: the picks come from small boxes where kappa barely moves them, and five functions improved under this approach.

**Documents and figures refreshed:** The README, model card, datasheet and figures now run to Week 9. The prediction-error check covers 23 GP predictions, 48% of them within one standard deviation.

**Model choice per function (Week 10 queries):**

- F1: Probe, `[0.576552, 0.564941]`. The sign flip shows the structure is finer than my step, so this steps back by 0.006 in x1 to give a third point along x1.
- F2: Exploit GP, `[0.702383, 0.911806]`. The peak is narrow (x2 = 0.912 gave 0.667, while 0.901 gave 0.542), so I am probing x1 only, with x2 held at the best value. Predicted 0.596 (std 0.071).
- F3: Exploit GP, `[0.382075, 0.373632, 0.475388]`. Continues the trend towards lower x1 and x2. Predicted +0.0015 (std 0.0087).
- F4: Halved step, `[0.341831, 0.406285, 0.414319, 0.402967]`. The gain is fading, so I halve the last step. No usable GP prediction.
- F5: Exploit GP, `[0.385328, 0.914392, 1.000000, 1.000000]`. Continues the climb towards higher x1 and x2. Predicted 3491.8 (std 21.6).
- F6: Halved step, `[0.443902, 0.374621, 0.630402, 0.785634, 0.146783]`. The last step failed, and the GP only proposes points next to it, so I halve the step that worked earlier. No usable GP prediction.
- F7: Exploit GP, `[0.000000, 0.190343, 0.312125, 0.219162, 0.339982, 0.712002]`. Continues the trend. Predicted 2.4005 (std 0.025). The first input reaches the lower limit of 0.
- F8: Exploit GP, `[0.235938, 0.086039, 0.079257, 0.113212, 0.959261, 0.496497, 0.186807, 0.647764]`. Continues the steady climb. Predicted 9.9451 (std 0.0138).

## Week 9 - Model & Pipeline Changes

**Week 8 results against predictions:** All eight functions set a new best for the first time: F1 (2.30e-5, up from 1.91e-6), F2 (0.6670, up from 0.6112), F3 (-0.0124, up from -0.0150), F4 (0.6082, up from 0.3675), F5 (3174.8, up from 2986.9), F6 (-0.1036, up from -0.1902), F7 (2.2010, up from 2.0242) and F8 (9.9100, up from 9.8928). Five picks beat their prediction, F3 landed on it, and F8 was marginally under (9.910 against 9.920) while still improving. F6 beat its prediction by 5 standard deviations and F5 by 2.8, so the models are being too cautious about these peaks.

- F1: x2 probe of +0.012 multiplied the output by 12.1 (1.91e-6 to 2.30e-5).
- F2: predicted 0.587 (std 0.085), actual 0.667.
- F3: predicted -0.0133 (std 0.0115), actual -0.0124.
- F4: direction step from the nearest points, actual 0.608 against a previous best of 0.368.
- F5: predicted 3023.6 (std 54.1), actual 3174.8.
- F6: predicted -0.1761 (std 0.0139), actual -0.1036.
- F7: predicted 2.1007 (std 0.0787), actual 2.2010.
- F8: predicted 9.9197 (std 0.0153), actual 9.9100.

**Why kappa and xi were not changed:** The Week 9 picks come from a ±0.02 box around each best point, where the GP's uncertainty is small. I checked how far the UCB pick moves as kappa goes from 0 to 2 in that box. For most functions it moves by under 0.03 in input space and costs only a few percent of predicted value (for example F2 falls from 0.660 to 0.616). F4 does not move at all, because its GP is about equally uncertain everywhere nearby (std about 0.54), so adding uncertainty cannot change the ranking. F8 moves the most (0.04 to 0.07), but only because it has eight inputs. Since all eight functions improved under pure exploitation, there is no evidence that more exploration is needed. The box size is the exploration dial I would turn first, and if a function stalls for about two weeks I will widen the box to ±0.04 to ±0.08 and add a small kappa of 0.5 to 1.0. The kappa and xi values in the script are unchanged.

**F4 repeats a successful step:** The GP predicts nothing above F4's best anywhere nearby and its pick goes against the move that worked, so I am repeating the successful step (lower x1 and x2, slightly higher x3 and x4) in the pattern-search style. The nearest-neighbour gradient estimate is badly conditioned (F4 also contains a duplicated row), so I am not using it.

**F1 continues the pattern search:** The x2 probe worked, so the next step probes x1 by +0.012 from the new best. If the value rises, I keep going that way, and if it drops I reverse. The GP alternative `[0.579743, 0.584776]` (continuing in x2) was noted but not chosen, since the x1 probe gives the second direction needed.

**Model choice per function (Week 9 queries):**

- F1: Pattern search probe, `[0.594552, 0.564941]`. The x2 step multiplied the output by 12, and the x1 step gives the second direction.
- F2: Exploit GP, `[0.698109, 0.901314]`. Predicted 0.660 (std 0.078), continuing towards lower x2, which is the direction that worked.
- F3: Exploit GP, `[0.401915, 0.392969, 0.455665]`. Predicted -0.0110 (std 0.0041), continuing towards lower x1 and x2.
- F4: Repeated step, `[0.350331, 0.410785, 0.413319, 0.400967]`. Low confidence, since the GP gives no usable signal here.
- F5: Exploit GP, `[0.371546, 0.894421, 1.000000, 1.000000]`. Predicted 3335.1 (std 24.7). Inputs 3 and 4 stay at the 1.0 limit, so the peak may lie at or beyond it.
- F6: Exploit GP, `[0.443605, 0.375980, 0.622451, 0.802268, 0.156989]`. Predicted -0.142, slightly below the best, but it moves in the same direction as the step that worked.
- F7: Exploit GP, `[0.004450, 0.176780, 0.315376, 0.202900, 0.359673, 0.731508]`. Predicted 2.303 (std 0.027). The first input is close to the lower limit of 0.
- F8: Exploit GP, `[0.255752, 0.070913, 0.098188, 0.104820, 0.944183, 0.507066, 0.169066, 0.638957]`. Predicted 9.9287 (std 0.0136), continuing the steady climb.

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
