"""Gradient-boosted regression with monotonicity constraints."""

from __future__ import annotations

from typing import Literal

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin


class MonotonicGBM(BaseEstimator, RegressorMixin):  # type: ignore[misc]
    """Monotonic gradient-boosted model wrapping LightGBM or XGBoost.

    Args:
        engine: Backend engine ('lightgbm' or 'xgboost').
        monotonic_constraints: Dict mapping feature names to constraint
            directions (-1, 0, or 1).
        n_estimators: Number of boosting rounds.
        learning_rate: Step-size shrinkage.
        max_depth: Maximum tree depth.
        random_state: Random seed.

    Examples:
        >>> import numpy as np
        >>> model = MonotonicGBM(engine="lightgbm", n_estimators=10, random_state=42)
        >>> X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        >>> y = np.array([1.0, 2.0, 3.0, 4.0])
        >>> _ = model.fit(X, y)
        >>> model.predict(X).shape
        (4,)
    """

    def __init__(
        self,
        engine: Literal["lightgbm", "xgboost"] = "lightgbm",
        monotonic_constraints: dict[str, int] | None = None,
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 6,
        random_state: int = 0,
    ) -> None:
        self.engine = engine
        self.monotonic_constraints = monotonic_constraints or {}
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.random_state = random_state
        self._model: object = None
        self._n_features: int = 0

    def _build_constraints(self, n_features: int) -> list[int]:
        constraints = [0] * n_features
        for name, direction in self.monotonic_constraints.items():
            if name.isdigit():
                idx = int(name)
                if 0 <= idx < n_features:
                    constraints[idx] = direction
        return constraints

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
    ) -> MonotonicGBM:
        """Fit the gradient-boosted model.

        Args:
            X: Feature matrix of shape (n_samples, n_features).
            y: Target array of shape (n_samples,).

        Returns:
            Self.

        Raises:
            ValueError: If engine is not supported.
        """
        self._n_features = X.shape[1]
        constraints = self._build_constraints(self._n_features)

        if self.engine == "lightgbm":
            import lightgbm as lgb

            self._model = lgb.LGBMRegressor(
                n_estimators=self.n_estimators,
                learning_rate=self.learning_rate,
                max_depth=self.max_depth,
                monotone_constraints=constraints,
                random_state=self.random_state,
                verbose=-1,
            )
            self._model.fit(X, y)
        elif self.engine == "xgboost":
            import xgboost as xgb

            mc_str = "(" + ",".join(str(c) for c in constraints) + ")"
            self._model = xgb.XGBRegressor(
                n_estimators=self.n_estimators,
                learning_rate=self.learning_rate,
                max_depth=self.max_depth,
                monotone_constraints=mc_str,
                random_state=self.random_state,
                verbosity=0,
            )
            self._model.fit(X, y)
        else:
            msg = f"Unsupported engine: {self.engine!r}"
            raise ValueError(msg)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict target values.

        Args:
            X: Feature matrix of shape (n_samples, n_features).

        Returns:
            Predicted values of shape (n_samples,).

        Raises:
            RuntimeError: If the model has not been fitted.

        Examples:
            >>> import numpy as np
            >>> m = MonotonicGBM(engine="lightgbm", n_estimators=10, random_state=0)
            >>> X = np.array([[1, 2], [3, 4]])
            >>> y = np.array([1.0, 2.0])
            >>> _ = m.fit(X, y)
            >>> m.predict(X).shape
            (2,)
        """
        if self._model is None:
            msg = "Model has not been fitted"
            raise RuntimeError(msg)
        return np.asarray(self._model.predict(X))  # type: ignore[union-attr]

    def predict_quantile(self, X: np.ndarray, q: float) -> np.ndarray:
        """Predict a specific quantile using the fitted model.

        For GBM models this uses a simple normal approximation around the
        point prediction. For proper quantile estimates, use conformal
        prediction wrappers.

        Args:
            X: Feature matrix of shape (n_samples, n_features).
            q: Quantile level in (0, 1).

        Returns:
            Quantile predictions of shape (n_samples,).

        Raises:
            RuntimeError: If the model has not been fitted.
            ValueError: If q is not in (0, 1).

        Examples:
            >>> import numpy as np
            >>> m = MonotonicGBM(engine="lightgbm", n_estimators=10, random_state=0)
            >>> X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
            >>> y = np.array([1.0, 2.0, 3.0, 4.0])
            >>> _ = m.fit(X, y)
            >>> m.predict_quantile(X, 0.9).shape
            (4,)
        """
        if self._model is None:
            msg = "Model has not been fitted"
            raise RuntimeError(msg)
        if not 0 < q < 1:
            msg = f"q must be in (0, 1), got {q}"
            raise ValueError(msg)
        from scipy.stats import norm

        point = self.predict(X)
        residual_std = max(float(np.std(point)) * 0.1, 1e-6)
        return np.asarray(point + norm.ppf(q) * residual_std)
