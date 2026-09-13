# Changelog

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
