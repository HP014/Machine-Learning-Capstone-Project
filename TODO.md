# TODO

- [ ] Fix up GitHub repo presentation (flesh out README.md — currently just a title, no description of the project, setup, or usage)
- [ ] Add plots to the repo/README, once Week 6 outputs are released:
  - [ ] Convergence plot (best value found per function, across weeks) — `plot_convergence()` already exists in `plotting_utils.py`, just needs wiring up with real week-by-week data
  - [ ] Random Forest feature importance bar chart per function (especially useful for func6/func7/func8, the higher-dimensional ones)
  - [ ] Parallel coordinates plot for higher-dimensional functions — `plot_parallel_coordinates()` already exists, unused so far
  - [ ] Model agreement plot: distance/gap between GP's and RF's chosen next-point per function/week
  - [ ] Calibration plot: each surrogate's predicted mean vs. actual observed value once Week 6 results come back
