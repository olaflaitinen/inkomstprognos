"""Forecast evaluation metrics."""

from __future__ import annotations

import numpy as np


def crps_sample(y_true: np.ndarray, y_samples: np.ndarray) -> float:
    """Compute the Continuous Ranked Probability Score from samples.

    Args:
        y_true: True values of shape (n,).
        y_samples: Forecast samples of shape (n, n_samples).

    Returns:
        Mean CRPS across observations.

    Raises:
        ValueError: If shapes are incompatible.

    Examples:
        >>> import numpy as np
        >>> y = np.array([1.0, 2.0])
        >>> samples = np.array([[1.1, 0.9, 1.0], [2.1, 1.9, 2.0]])
        >>> score = crps_sample(y, samples)
        >>> 0 <= score
        True
    """
    if y_true.ndim != 1:
        msg = "y_true must be 1-dimensional"
        raise ValueError(msg)
    if y_samples.ndim != 2 or y_samples.shape[0] != y_true.shape[0]:
        msg = "y_samples must have shape (n, n_samples)"
        raise ValueError(msg)

    n = y_true.shape[0]
    m = y_samples.shape[1]
    scores = np.zeros(n)
    for i in range(n):
        s = np.sort(y_samples[i])
        term1 = np.mean(np.abs(s - y_true[i]))
        term2 = 0.0
        for j in range(m):
            for k in range(j + 1, m):
                term2 += np.abs(s[j] - s[k])
        term2 /= m * (m - 1) if m > 1 else 1.0
        scores[i] = term1 - term2
    return float(np.mean(scores))


def pinball_loss(y_true: np.ndarray, y_quantile: np.ndarray, q: float) -> float:
    """Compute pinball (quantile) loss.

    Args:
        y_true: True values of shape (n,).
        y_quantile: Quantile predictions of shape (n,).
        q: Quantile level in (0, 1).

    Returns:
        Mean pinball loss.

    Raises:
        ValueError: If q is not in (0, 1).

    Examples:
        >>> import numpy as np
        >>> pinball_loss(np.array([1.0, 2.0]), np.array([1.1, 1.9]), 0.5)
        0.05...
    """
    if not 0 < q < 1:
        msg = f"q must be in (0, 1), got {q}"
        raise ValueError(msg)
    residual = y_true - y_quantile
    loss = np.where(residual >= 0, q * residual, (q - 1) * residual)
    return float(np.mean(loss))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute mean absolute error.

    Args:
        y_true: True values.
        y_pred: Predicted values.

    Returns:
        Mean absolute error.

    Examples:
        >>> import numpy as np
        >>> mae(np.array([1.0, 2.0]), np.array([1.1, 1.9]))
        0.1
    """
    return float(np.mean(np.abs(y_true - y_pred)))


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute root mean squared error.

    Args:
        y_true: True values.
        y_pred: Predicted values.

    Returns:
        Root mean squared error.

    Examples:
        >>> import numpy as np
        >>> rmse(np.array([1.0, 2.0]), np.array([1.0, 2.0]))
        0.0
    """
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute mean absolute percentage error.

    Args:
        y_true: True values (must be non-zero).
        y_pred: Predicted values.

    Returns:
        Mean absolute percentage error.

    Raises:
        ValueError: If any y_true value is zero.

    Examples:
        >>> import numpy as np
        >>> mape(np.array([100.0, 200.0]), np.array([110.0, 190.0]))
        0.05...
    """
    if np.any(y_true == 0):
        msg = "y_true must not contain zeros"
        raise ValueError(msg)
    return float(np.mean(np.abs((y_true - y_pred) / y_true)))


def coverage(y_true: np.ndarray, lo: np.ndarray, hi: np.ndarray) -> float:
    """Compute empirical coverage of prediction intervals.

    Args:
        y_true: True values.
        lo: Lower bounds of prediction intervals.
        hi: Upper bounds of prediction intervals.

    Returns:
        Fraction of observations covered by intervals.

    Examples:
        >>> import numpy as np
        >>> coverage(np.array([1.0, 2.0]), np.array([0.5, 1.5]), np.array([1.5, 2.5]))
        1.0
    """
    return float(np.mean((y_true >= lo) & (y_true <= hi)))


def interval_width(lo: np.ndarray, hi: np.ndarray) -> float:
    """Compute mean prediction interval width.

    Args:
        lo: Lower bounds.
        hi: Upper bounds.

    Returns:
        Mean interval width.

    Examples:
        >>> import numpy as np
        >>> interval_width(np.array([0.0, 1.0]), np.array([2.0, 3.0]))
        2.0
    """
    return float(np.mean(hi - lo))
