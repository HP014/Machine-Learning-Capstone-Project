"""How close was the model's prediction to what actually came back?

For week N, fit the Gaussian Process on the data up to week N-1 (the same exploit-search model as
exploit_search.py), predict the query submitted in week N, and compare it with the output that came back. The error
is measured in standard deviations: (actual - predicted) / predicted std. This is how the prediction log in
results/prediction_log.csv was built, and why the Gaussian Process's uncertainty is treated with caution (only 49%
of 39 predictions landed within one standard deviation). F1 is on a very different scale, so it is left out of the
log.

Usage: python scripts/prediction_check.py [--week N] [--functions 5 7 8]   (default: the latest week, F2 to F8)
"""
import argparse
import sys
import warnings
from pathlib import Path

import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern, WhiteKernel

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from data_io import load_week  # noqa: E402
from paths import latest_week  # noqa: E402

warnings.filterwarnings("ignore")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--week", type=int, default=None, help="week whose query to check (default: the latest)")
    parser.add_argument("--functions", type=int, nargs="+", default=list(range(2, 9)))
    args = parser.parse_args()
    week = args.week or latest_week()
    before, after = load_week(week - 1), load_week(week)

    for f in args.functions:
        X, y = before[f]
        query, actual = after[f][0][-1], after[f][1][-1]
        kern = ConstantKernel(1.0, (1e-2, 1e3)) * Matern(0.3, (0.05, 3.0), nu=2.5) + WhiteKernel(1e-4, (1e-8, 1e-1))
        gp = GaussianProcessRegressor(kernel=kern, alpha=1e-8, normalize_y=True, n_restarts_optimizer=10,
                                      random_state=0).fit(X, y)
        m, s = gp.predict(np.array([query]), return_std=True)
        print(f"F{f}: predicted {m[0]:.6f} std {s[0]:.6f} | actual {actual:.6f} | z = {(actual - m[0]) / s[0]:+.2f}")


if __name__ == "__main__":
    main()
