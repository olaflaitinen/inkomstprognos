"""Split and Mondrian conformal prediction wrappers."""

from __future__ import annotations

import numpy as np
from sklearn.base import BaseEstimator

from inkomstprognos.seeds import derive_seed


class SplitConformal(BaseEstimator):  # type: ignore[misc]
    """Split conformal prediction wrapper.

    Wraps any sklearn-compatible base estimator with split conformal
    calibration for prediction intervals.

    Args:
        base_estimator: A fitted sklearn-compatible regressor.
        random_state: Random seed for calibration splitting.

    Examples:
        >>> from sklearn.linear_model import LinearRegression
        >>> base = LinearRegression()
        >>> sc = SplitConformal(base_estimator=base, random_state=42)
    """

    def __init__(
        self,
        base_estimator: BaseEstimator | None = None,
        random_state: int = 0,
    ) -> None:
        self.base_estimator = base_estimator
        self.random_state = random_state
        self._residuals: np.ndarray | None = None

    def fit_calibrate(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_calib: np.ndarray,
        y_calib: np.ndarray,
    ) -> SplitConformal:
        """Fit the base estimator and calibrate residuals.

        Args:
            X_train: Training features.
            y_train: Training targets.
            X_calib: Calibration features.
            y_calib: Calibration targets.

        Returns:
            Self.

        Raises:
            ValueError: If base_estimator is None.

        Examples:
            >>> import numpy as np
            >>> from sklearn.linear_model import LinearRegression
            >>> sc = SplitConformal(base_estimator=LinearRegression(), random_state=0)
            >>> X_tr = np.array([[1], [2], [3], [4]])
            >>> y_tr = np.array([1.0, 2.0, 3.0, 4.0])
            >>> X_cal = np.array([[5], [6]])
            >>> y_cal = np.array([5.0, 6.0])
            >>> _ = sc.fit_calibrate(X_tr, y_tr, X_cal, y_cal)
        """
        if self.base_estimator is None:
            msg = "base_estimator must be provided"
            raise ValueError(msg)
        self.base_estimator.fit(X_train, y_train)
        preds = self.base_estimator.predict(X_calib)
        self._residuals = np.abs(y_calib - preds)
        return self

    def predict_interval(
        self,
        X: np.ndarray,
        alpha: float = 0.1,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Predict with conformal prediction intervals.

        Args:
            X: Feature matrix.
            alpha: Miscoverage level (e.g. 0.1 for 90% intervals).

        Returns:
            Tuple of (lower_bounds, upper_bounds) arrays.

        Raises:
            RuntimeError: If the model has not been calibrated.
            ValueError: If alpha is not in (0, 1).

        Examples:
            >>> import numpy as np
            >>> from sklearn.linear_model import LinearRegression
            >>> sc = SplitConformal(base_estimator=LinearRegression(), random_state=0)
            >>> X_tr = np.array([[1], [2], [3], [4]])
            >>> y_tr = np.array([1.0, 2.0, 3.0, 4.0])
            >>> _ = sc.fit_calibrate(X_tr, y_tr, X_tr, y_tr)
            >>> lo, hi = sc.predict_interval(X_tr, alpha=0.1)
            >>> lo.shape == hi.shape
            True
        """
        if self._residuals is None:
            msg = "Model has not been calibrated; call fit_calibrate first"
            raise RuntimeError(msg)
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        preds = self.base_estimator.predict(X)  # type: ignore[union-attr]
        q = np.quantile(self._residuals, 1 - alpha)
        return preds - q, preds + q


class MondrianConformal(BaseEstimator):  # type: ignore[misc]
    """Mondrian (stratified) split conformal prediction wrapper.

    Calibrates residuals per stratum for heterogeneous coverage.

    Args:
        base_estimator: A fitted sklearn-compatible regressor.
        random_state: Random seed.

    Examples:
        >>> from sklearn.linear_model import LinearRegression
        >>> mc = MondrianConformal(base_estimator=LinearRegression(), random_state=42)
    """

    def __init__(
        self,
        base_estimator: BaseEstimator | None = None,
        random_state: int = 0,
    ) -> None:
        self.base_estimator = base_estimator
        self.random_state = random_state
        self._strata_residuals: dict[int, np.ndarray] = {}
        self._global_residuals: np.ndarray | None = None

    def fit_calibrate(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_calib: np.ndarray,
        y_calib: np.ndarray,
        strata: np.ndarray | None = None,
    ) -> MondrianConformal:
        """Fit the base estimator and calibrate per-stratum residuals.

        Args:
            X_train: Training features.
            y_train: Training targets.
            X_calib: Calibration features.
            y_calib: Calibration targets.
            strata: Integer stratum labels for calibration points.

        Returns:
            Self.

        Raises:
            ValueError: If base_estimator is None.

        Examples:
            >>> import numpy as np
            >>> from sklearn.linear_model import LinearRegression
            >>> mc = MondrianConformal(base_estimator=LinearRegression(), random_state=0)
            >>> X = np.array([[1], [2], [3], [4]])
            >>> y = np.array([1.0, 2.0, 3.0, 4.0])
            >>> s = np.array([0, 0, 1, 1])
            >>> _ = mc.fit_calibrate(X, y, X, y, strata=s)
        """
        if self.base_estimator is None:
            msg = "base_estimator must be provided"
            raise ValueError(msg)

        _seed = derive_seed(self.random_state, namespace="conformal_calibration")
        self.base_estimator.fit(X_train, y_train)
        preds = self.base_estimator.predict(X_calib)
        residuals = np.abs(y_calib - preds)
        self._global_residuals = residuals

        if strata is not None:
            for s in np.unique(strata):
                mask = strata == s
                self._strata_residuals[int(s)] = residuals[mask]

        return self

    def predict_interval(
        self,
        X: np.ndarray,
        alpha: float = 0.1,
        strata: np.ndarray | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Predict with Mondrian conformal intervals.

        Args:
            X: Feature matrix.
            alpha: Miscoverage level.
            strata: Optional stratum labels for test points.

        Returns:
            Tuple of (lower_bounds, upper_bounds) arrays.

        Raises:
            RuntimeError: If the model has not been calibrated.
            ValueError: If alpha is not in (0, 1).

        Examples:
            >>> import numpy as np
            >>> from sklearn.linear_model import LinearRegression
            >>> mc = MondrianConformal(base_estimator=LinearRegression(), random_state=0)
            >>> X = np.array([[1], [2], [3], [4]])
            >>> y = np.array([1.0, 2.0, 3.0, 4.0])
            >>> _ = mc.fit_calibrate(X, y, X, y)
            >>> lo, hi = mc.predict_interval(X, alpha=0.1)
            >>> lo.shape == hi.shape
            True
        """
        if self._global_residuals is None:
            msg = "Model has not been calibrated; call fit_calibrate first"
            raise RuntimeError(msg)
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        preds = self.base_estimator.predict(X)  # type: ignore[union-attr]
        lo = np.empty_like(preds)
        hi = np.empty_like(preds)

        if strata is not None and self._strata_residuals:
            for s in np.unique(strata):
                mask = strata == s
                resid = self._strata_residuals.get(int(s), self._global_residuals)
                q = np.quantile(resid, 1 - alpha)
                lo[mask] = preds[mask] - q
                hi[mask] = preds[mask] + q
        else:
            q = np.quantile(self._global_residuals, 1 - alpha)
            lo = preds - q
            hi = preds + q

        return lo, hi
