"""Loading the weekly data, and adding a new week without overwriting an old one."""
import numpy as np

from paths import DATA, latest_week

FUNCTION_IDS = range(1, 9)


def load_week(week=None):
    """Load the cumulative inputs and outputs of every function from data/Week_<week> (default: the latest).

    Each week's folder holds everything up to that week: the course's initial points first, then one row per
    query. Returns {function number: (inputs, outputs)}.
    """
    week = latest_week() if week is None else week
    data = {}
    for f in FUNCTION_IDS:
        folder = DATA / f"Week_{week}" / f"function_{f}"
        data[f] = (np.load(folder / "updated_inputs.npy"), np.load(folder / "updated_outputs.npy"))
    return data


def append_week(new_week, queries, outputs):
    """Create data/Week_<new_week> from the previous week plus this week's queries and their outputs.

    queries: {function number: array of the submitted input}; outputs: {function number: returned output}.
    It refuses to write over an existing week, so a week's data can never be added twice.
    """
    previous = load_week(new_week - 1)
    target = DATA / f"Week_{new_week}"
    if target.exists():
        raise FileExistsError(f"{target} already exists, so it was not overwritten")
    for f, (inputs, results) in previous.items():
        folder = target / f"function_{f}"
        folder.mkdir(parents=True)
        np.save(folder / "updated_inputs.npy", np.vstack([inputs, queries[f]]))
        np.save(folder / "updated_outputs.npy", np.append(results, outputs[f]))
    return target
