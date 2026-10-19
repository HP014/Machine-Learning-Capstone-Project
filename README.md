# Bayesian Optimisation of Eight Black-Box Functions

## NON-TECHNICAL EXPLANATION OF YOUR PROJECT
Imagine eight mystery machines. For each one you pick the settings on a few dials, between two and eight of them, and the machine reports a score. The aim is to find the settings that give the highest score, but you only get one try per machine each week, so every try has to count. This project uses machine learning to study the results so far and suggest which settings to try next, balancing careful tweaks to the best settings with bold tests of unfamiliar ones. Over eight weeks the best score for every machine improved, in some cases several times over.

## DATA
The data comes from eight unknown "black-box" functions that I could only learn about by querying them. Each week I submitted one input for each function and received its output. `[CONFIRM: name of the course/module and who provides the functions, plus any citation your course requires]`

| Function | Inputs | Initial points | Points after Week 8 | Best at start | Best after Week 8 |
|---|---|---|---|---|---|
| F1 | 2 | 10 | 18 | 7.71e-16 | 2.30e-05 |
| F2 | 2 | 10 | 18 | 0.6112 | 0.6670 |
| F3 | 3 | 15 | 23 | -0.0348 | -0.0124 |
| F4 | 4 | 30 | 38 | -4.0255 | 0.6082 |
| F5 | 4 | 20 | 28 | 1088.86 | 3174.77 |
| F6 | 5 | 20 | 28 | -0.7143 | -0.1036 |
| F7 | 6 | 30 | 38 | 1.3650 | 2.2010 |
| F8 | 8 | 40 | 48 | 9.5985 | 9.9100 |

- Every input value lies between 0 and 1. Outputs are not bounded. There are 239 observations in total.
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
  - A duplicate-query safeguard, so no point within 0.001 of an earlier one can be chosen.
  - A local search in a small box around the best point (used for F3 and F4).
  - Log-space models for F1, and a small-step pattern search once F1's models stopped helping.
  - In the final rounds, exploiting around each best point (highest predicted value within a ±0.02 box).

The model card (`model_card.md`) has the details, limitations and trade-offs.

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

- **GP kernel parameters** (length scale, amplitude, noise) are fitted automatically by maximising the log marginal likelihood, with 10 random restarts. The kernel type and starting length scale were chosen by hand, with the smoother RBF kernel for the 2D functions and Matern kernels for higher dimensions.
- **kappa and xi** control exploration against exploitation. I set them by judgement for each function and did not run a search, because each function allows only one real evaluation per week. I checked how sensitive the choices were: inside a small box around the best point, raising kappa from 0 to 2 moved most picks by under 0.03 and lowered the predicted value by a few percent, so the box size mattered more than kappa.
- **Random Forest:** 200 trees, fixed random seed (42), other settings left at the scikit-learn defaults.
- **Later GP refits** used a floor of 0.05 on the length scale and normalised outputs, after the earlier fits for F2 and F5 collapsed into spiky kernels.

## RESULTS
All eight functions improved, and in Week 8 every function set a new best.

![Best output so far by week](results/figures/fig1_best_so_far.png)

![Progress for every function](results/figures/fig2_progress_all_functions.png)

- **Most of the gains came in bursts**, with long flat stretches in between. Several functions only improved again after the switch to small steps around the best point.

![Exploration versus exploitation](results/figures/fig3_exploration_vs_exploitation.png)

- **Prediction quality was mixed.** Comparing each model's prediction with the output that actually came back, the GP's prediction was within one standard deviation 47% of the time (17 predictions). The Random Forest was within one standard deviation in 2 of 3 predictions, which is too few to compare fairly.

![Prediction error](results/figures/fig5_prediction_error.png)

- **F1 is a very hard function.** Almost every output is effectively zero, so an ordinary GP learned nothing useful from it. A small-step search finally increased its best value by a factor of about 12 in one week.

![F1 map](results/figures/fig4_f1_map.png)

What the results show:
- Models that look confident can be wrong. The GP was too sure of itself for F3, F4 and F7, missing by up to about 6 standard deviations in earlier weeks.
- Once a good region is found, careful small steps are an efficient way to improve.
- With only eight weeks of data, these are best-so-far results, not proof that any function's true maximum has been found.

## (OPTIONAL: CONTACT DETAILS)
`[Add a link or email here if you make the repository public, or delete this section.]`

## REPOSITORY CONTENTS
- `Improved RA_12_1.py`: the weekly script that loads the data, fits the models and prints the next candidate points. It still uses fixed file paths and is due to be tidied. The final-round exploit searches, the F1 step search and the kappa sensitivity check were run as separate working scripts that have not yet been added to the repository.
- `plotting_utils.py`, `surrogate_models.py`: acquisition functions, plotting helpers, the Random Forest and log-space helpers.
- `make_figures.py`: rebuilds every figure in `results/figures/` from the data (`python make_figures.py`).
- `Data/`: the weekly data. `results/`: figures and a log of past predictions.
- `CHANGELOG.md`: what changed each week and why. `model_card.md` and `data_sheet.md`: the model card and datasheet.
