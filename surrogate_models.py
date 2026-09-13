"""
Alternative surrogate models for Bayesian optimization, for use alongside the
Gaussian Process models in "Improved RA_12_1.py". Each fit_* function returns
a fitted model; each predict_* function returns (mean, std) so the existing
acquisition functions (upper_confidence_bound, expected_improvement) in
plotting_utils.py can be reused unchanged.
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor


def fit_random_forest_surrogate(X_train, y_train, n_estimators=200, random_state=42):
    """
    Fit a Random Forest surrogate model.

    Random Forests split on relative order rather than magnitude, so they
    are much more robust than a GP to functions with extreme or wildly
    varying output scales.

    Parameters:
    -----------
    X_train : array-like, shape (n_samples, n_dims)
    y_train : array-like, shape (n_samples,)
    n_estimators : int, number of trees in the forest
    random_state : int, for reproducibility
    """
    model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train, y_train)
    return model


def random_forest_predict(model, X_test):
    """
    Predict mean and std from a fitted Random Forest.

    scikit-learn's RandomForestRegressor.predict() only returns the mean
    (the average across trees). To get an uncertainty estimate usable by
    UCB/EI, we instead collect each individual tree's prediction and take
    the mean and standard deviation across trees.

    Parameters:
    -----------
    model : fitted RandomForestRegressor
    X_test : array-like, shape (n_samples, n_dims)

    Returns:
    --------
    mean : array, shape (n_samples,)
    std : array, shape (n_samples,)
    """
    tree_predictions = np.stack([tree.predict(X_test) for tree in model.estimators_], axis=0)
    mean = tree_predictions.mean(axis=0)
    std = tree_predictions.std(axis=0)
    return mean, std
