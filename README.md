# Bayesian Optimisation of Eight Black-Box Functions

## NON-TECHNICAL EXPLANATION OF YOUR PROJECT
Imagine eight mystery machines. For each one you pick the settings on a few dials, between two and eight of them, and the machine reports a score. The aim is to find the settings that give the highest score, but you only get one try per machine each week, so every try has to count. This project uses machine learning to study the results so far and suggest which settings to try next, balancing careful tweaks to the best settings with bold tests of unfamiliar ones. Over twelve weeks the best score for every machine improved, in some cases several times over.

## DATA
The data comes from eight unknown "black-box" functions that I could only learn about by querying them. Each week I submitted one input for each function and received its output. `[CONFIRM: name of the course/module and who provides the functions, plus any citation your course requires]`

| Function | Inputs | Initial points | Points after Week 12 | Best at start | Best after Week 12 |
|---|---|---|---|---|---|
| F1 | 2 | 10 | 22 | 7.71e-16 | 1.43e-04 |
| F2 | 2 | 10 | 22 | 0.6112 | 0.6670 |
| F3 | 3 | 15 | 27 | -0.0348 | -0.0054 |
| F4 | 4 | 30 | 42 | -4.0255 | 0.6566 |
| F5 | 4 | 20 | 32 | 1088.86 | 3984.69 |
| F6 | 5 | 20 | 32 | -0.7143 | -0.0575 |
| F7 | 6 | 30 | 42 | 1.3650 | 2.7158 |
| F8 | 8 | 40 | 52 | 9.5985 | 9.9634 |

- Every input value lies between 0 and 1. Outputs are not bounded. There are 271 observations in total.
- Outputs appear to be exactly repeatable: querying the same point twice returned identical values.
- F1 is unusual: its outputs range from about 1e-245 to 1e-3, so almost every point looks like zero.
- The data is stored cumulatively in `Data/Week_N/function_M/` as `updated_inputs.npy` and `updated_outputs.npy`. Each week's folder contains everything up to that week.
- Four rows are repeated queries (one in F1, one in F4, two in F5) from before the duplicate safeguard was added. They have been kept.

See `data_sheet.md` for the full datasheet.

## MODEL
I used **Bayesian optimisation**: fit a model to the points so far, then use it to choose the next point to query.

- **Gaussian Process (GP)** surrogate (scikit-learn), which predicts the output and how uncertain that prediction is. I chose it because it works well with very few points and gives a usable uncertainty.
- **Random Forest** surrogate (200 trees), added as a second opinion. Its uncertainty is the spread of the individual trees' predictions. I chose it because it is far less sensitive to extreme output scales and rough landscapes.
- **Acquisition functions** (UCB and Expected Improvement) turn those predictions into a score for each candidate point, and the highest score is queried next.
- **Extra safeguards and methods added along the way:**
  - A duplicate-query safeguard, so no point within 0.001 of an earlier one can be chosen. I added it because F1's Week 4 query was an exact repeat of Week 3's, which gave no new information.
  - A local search in a small box around the best point (used for F3 and F4), because the global search kept choosing far-off points that the models themselves predicted to be poor.
  - Log-space models for F1, because its outputs range from 1e-245 to 1e-3 and the raw models could not tell the points apart. When the models still gave no usable signal for F1, I switched to a small-step pattern search.
  - In the final rounds, exploiting around each best point (highest predicted value within a ±0.02 box), because several functions had dropped sharply when they moved away from their best.

The model card (`model_card.md`) has the details, limitations and trade-offs. The section below gives the evidence behind each choice.

## KEY DECISIONS AND WHY
Each decision below comes with the evidence and what it cost. The week is when the change was made. The full reasoning for every weekly query is in `CHANGELOG.md`.

- **Week 6: added a Random Forest as a second surrogate.** I had only used a GP. For F1 the GP kept returning to the same flat corners whatever the kernel or kappa. For F5 it had no signal far from the data (mean 0, std 316), while the Random Forest's prediction of 2478.8 landed near my best known point. The cost was that the Random Forest extrapolated noise for F4 (mean -6.65, std 8.71, against observed values of -1.28 to 0.37), so I ignored it there.
- **Week 6: excluded any candidate within 0.001 of a sampled point.** F1's Week 4 query was an exact repeat of Week 3's, because UCB and EI kept proposing known points and I followed them. A repeat gives no new information. Four earlier repeated rows remain in the data.
- **Week 7: modelled F1 on the log of its absolute output.** F1's outputs range from 1e-245 to 1e-3, so squared error treats everything near zero as identical and the raw models could not see a gradient. In log terms there is a clear one. The cost is that the sign is dropped, so this finds the active region and not the exact peak.
- **Week 7: searched a small box around the best point for F3 and F4.** The global search chose far-off points that the models themselves predicted to be poor (F4's GP predicted -13 against a best of 0.3675), because uncertainty is highest where there is no data. This refines a known peak and cannot find a different one.
- **Week 8: exploited around each best point (±0.02 box, highest predicted value).** Most functions now had an established best region. I chose small steps because F2, F4 and F7 had all dropped sharply when they moved away from their best. It risks settling on a local peak, but all eight functions set a new best in the following round.
- **Week 8: refitted the GPs with a length-scale floor of 0.05 and normalised outputs.** The previous fits for F2 and F5 collapsed into spiky kernels (length scales of 0.0085 and 1e-5) that made local predictions meaningless. The floor stops the model fitting very sharp features if they are real.
- **Week 8: switched F1 to a pattern search (small steps from the best point).** A GP failed, and a single-Gaussian-bump model failed a hold-out test: without the newest point it predicted 1e-31 for a value that was actually about 1e-5.7. F1's outputs are exact, so measuring the direction of improvement directly is reliable. It takes about three weeks, since only one query per week is allowed, but it produced a 12x gain in one week.
- **Weeks 8 onwards: stopped using the Random Forest for picks.** I added it in Week 6 out of curiosity, to see whether a second model could improve on the GP. In Week 6 the GP-picked functions produced one new best out of four and the Random Forest-picked ones none, and the GP kept producing better points afterwards, so I continued with it. This is a small sample and not a controlled comparison, and I never tuned the Random Forest. Later checks gave a likely reason: a Random Forest averages outputs it has already seen, so it can never predict above the best value found so far, and in the small boxes used from Week 8 its uncertainty was far too wide to rank nearby points (F5: std 468 against 3.4 for the GP).
- **Week 9: left kappa and xi unchanged.** In a ±0.02 box, moving kappa from 0 to 2 shifted most picks by under 0.03 and cost a few percent of predicted value. F4 did not move at all. Box size mattered more, and every function was improving. If a function stalls for about two weeks, I will widen the box to ±0.04 to ±0.08 and add a small kappa.
- **Weeks 10 to 12: used line searches and half steps for F4 and F6, and an anisotropic GP for F4.** The GP's picks sat next to a failed point or predicted nothing above the best, so where a step stopped working I halved it or fitted a curve along it. Once F4's line was used up, a GP with a length scale for each input predicted the last three points better than the plain one (errors of 0.14, 0.49 and 0.50 against 0.83, 0.59 and 0.57) and showed that x1 and x2 matter most. These picks are low confidence, and the anisotropic GP was overconfident on one of the three points (5.9 standard deviations).

## HYPERPARAMETER OPTIMSATION
| Function | Kernel (starting length scale) | UCB kappa | EI xi |
|---|---|---|---|
| F1 (raw models) | RBF (0.3) + white noise | 0.1 | 0.1 |
| F2 | RBF (0.2) | 2.0 | 0.1 |
| F3 | Matern 2.5 (0.1) | 1.5 | 0.01 |
| F4 | Matern 2.5 (0.1) | 1.5 | 0.01 |
| F5 | Matern 1.5 (0.2) | 1.5 | 0.01 |
| F6 | Matern 1.5 (0.1) | 2.5 | 0.01 |
| F7 | Matern 1.5 (0.15) | 1.7 | 0.01 |
| F8 | Matern 1.5 (0.2) | 3.0 | 0.02 |

- **GP kernel parameters** (length scale, amplitude, noise) are fitted automatically by maximising the log marginal likelihood, with 10 random restarts. The kernel type and starting length scale were chosen by hand. I assigned the kernels in order of function number: the smoother RBF kernel for the two 2D functions, which are the easiest to model, and Matern kernels for the rest. RBF assumes a very smooth function, while Matern allows a rougher one, and the higher-dimensional functions have sparser data and are less predictable. The starting length scales (0.1 to 0.3) are only starting points, because the fit then optimises them.
- **kappa and xi** control exploration against exploitation. I set them by judgement for each function and did not run a search, because each function allows only one real evaluation per week. I checked how sensitive the choices were: inside a small box around the best point, raising kappa from 0 to 2 moved most picks by under 0.03 and lowered the predicted value by a few percent, so the box size mattered more than kappa.
- **White noise (F1 only):** added in Week 5 to keep the fits stable and to allow for noise in the outputs. Almost all of F1's results were close to zero, so I tried adding something new there to stop the fit chasing tiny differences between near-zero values. Repeated queries returned identical outputs, so it is a precaution and not a measured noise level. The other functions' GPs do not include it.
- **Random Forest:** 200 trees, fixed random seed (42), other settings left at the scikit-learn defaults. I used more trees than the default of 100 because the uncertainty is the spread across trees, so more trees give a steadier estimate, and it costs little with this little data. I did not tune it.
- **10,000 random candidates:** a GP prediction is cheap, so 10,000 gives decent coverage in 2 to 3 dimensions. It is coarse in 8 dimensions, which is listed as a limitation in the model card.
- **Local search box of ±0.04 (Week 7, used for F3 and F4):** I chose those two functions because their best regions already seemed to be found. The size was a first judgement of "close to the best point". It is about a sixth of the typical spacing between my points (about 0.24), so it stays local without reaching other sampled points. I narrowed it to ±0.02 in Week 8 after several functions dropped sharply when they moved away from their best.
- **Later GP refits** used a floor of 0.05 on the length scale and normalised outputs, after the earlier fits for F2 and F5 collapsed into spiky kernels.

## RESULTS
All eight functions improved over the twelve weeks. Every function set a new best in Week 8, five of the eight did so again in Week 9, three did in Week 10, six did in Week 11, and four did in Week 12.

![Best output so far by week](results/figures/fig1_best_so_far.png)

![Progress for every function](results/figures/fig2_progress_all_functions.png)

- **Most of the gains came in bursts**, with long flat stretches in between. Several functions only improved again after the switch to small steps around the best point.

![Exploration versus exploitation](results/figures/fig3_exploration_vs_exploitation.png)

- **Prediction quality was mixed.** Comparing each model's prediction with the output that actually came back, the GP's prediction was within one standard deviation 47% of the time (36 predictions). The Random Forest was within one standard deviation in 2 of 3 predictions, which is too few to compare fairly.

![Prediction error](results/figures/fig5_prediction_error.png)

- **F1 is a very hard function.** Almost every output is effectively zero, so an ordinary GP learned nothing useful from it. A small-step search finally increased its best value by a factor of about 12 in one week. The next step flipped the sign of the output (-8.4e-5), which shows its structure is finer than the step size, so the search now uses smaller steps. A third point along x1 then showed that the positive stripe is only about 0.0135 wide, and the search is now climbing along it. The first step along the stripe raised the best value by about 6x, to 1.43e-4. The next step overshot and flipped the sign again (-2.1e-4), which puts the top of the stripe between those two points.

![F1 map](results/figures/fig4_f1_map.png)

What the results show:
- Models that look confident can be wrong. The GP was too sure of itself for F3, F4 and F7, missing by up to about 6 standard deviations in earlier weeks.
- Once a good region is found, careful small steps are an efficient way to improve.
- With only twelve weeks of data, these are best-so-far results, not proof that any function's true maximum has been found.

## (OPTIONAL: CONTACT DETAILS)
`[Add a link or email here if you make the repository public, or delete this section.]`

## REPOSITORY CONTENTS
- `Improved RA_12_1.py`: the weekly script that loads the data, fits the models and prints the next candidate points. It still uses fixed file paths and is due to be tidied. The final-round exploit searches, the F1 step search and the kappa sensitivity check were run as separate working scripts that have not yet been added to the repository.
- `plotting_utils.py`, `surrogate_models.py`: acquisition functions, plotting helpers, the Random Forest and log-space helpers.
- `make_figures.py`: rebuilds every figure in `results/figures/` from the data (`python make_figures.py`).
- `Data/`: the weekly data. `results/`: figures and a log of past predictions.
- `CHANGELOG.md`: what changed each week and why. `model_card.md` and `data_sheet.md`: the model card and datasheet.
