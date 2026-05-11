"""Calibration diagnostics for probabilistic forecasts."""

from __future__ import annotations

import numpy as np


def pit_histogram(
    y_true: np.ndarray,
    F_pred: np.ndarray,
    n_bins: int = 10,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute a Probability Integral Transform histogram.

    Args:
        y_true: True values of shape (n,).
        F_pred: CDF values evaluated at y_true, shape (n,).
        n_bins: Number of histogram bins.

    Returns:
        Tuple of (bin_edges, bin_counts) arrays.

    Raises:
        ValueError: If shapes are incompatible or F_pred values are outside [0, 1].

    Examples:
        >>> import numpy as np
        >>> edges, counts = pit_histogram(np.array([1.0, 2.0]), np.array([0.3, 0.7]))
        >>> len(counts) == 10
        True
    """
    if y_true.shape != F_pred.shape:
        msg = "y_true and F_pred must have the same shape"
        raise ValueError(msg)
    if np.any(F_pred < 0) or np.any(F_pred > 1):
        msg = "F_pred values must be in [0, 1]"
        raise ValueError(msg)

    counts, edges = np.histogram(F_pred, bins=n_bins, range=(0, 1))
    return edges, counts


def reliability_diagram(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    q_grid: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute a reliability diagram for quantile forecasts.

    For each nominal quantile level in q_grid, computes the observed
    fraction of y_true values below the corresponding quantile prediction.

    Args:
        y_true: True values of shape (n,).
        y_pred: Quantile predictions of shape (n, len(q_grid)).
        q_grid: Array of quantile levels in (0, 1).

    Returns:
        Tuple of (nominal_levels, observed_coverages) arrays.

    Raises:
        ValueError: If shapes are incompatible.

    Examples:
        >>> import numpy as np
        >>> y = np.array([1.0, 2.0, 3.0])
        >>> q = np.array([0.25, 0.5, 0.75])
        >>> preds = np.array([[0.5, 1.0, 1.5], [1.5, 2.0, 2.5], [2.5, 3.0, 3.5]])
        >>> nom, obs = reliability_diagram(y, preds, q)
        >>> len(nom) == 3
        True
    """
    if y_pred.ndim != 2 or y_pred.shape[0] != y_true.shape[0]:
        msg = "y_pred must have shape (n, len(q_grid))"
        raise ValueError(msg)
    if y_pred.shape[1] != len(q_grid):
        msg = "y_pred columns must match q_grid length"
        raise ValueError(msg)

    observed = np.zeros(len(q_grid))
    for j, _q in enumerate(q_grid):
        observed[j] = np.mean(y_true <= y_pred[:, j])

    return q_grid, observed
