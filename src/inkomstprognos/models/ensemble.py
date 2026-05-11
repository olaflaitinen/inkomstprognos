"""Stacking ensemble with non-negative least-squares meta-learner."""

from __future__ import annotations

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.model_selection import KFold

from inkomstprognos.seeds import derive_seed


class StackingEnsemble(BaseEstimator, RegressorMixin):  # type: ignore[misc]
    """Cross-fitted stacking ensemble with NNLS meta-learner.

    Args:
        base_estimators: List of sklearn-compatible regressors.
        n_folds: Number of cross-validation folds.
        random_state: Random seed.

    Examples:
        >>> from sklearn.linear_model import LinearRegression, Ridge
        >>> se = StackingEnsemble(base_estimators=[LinearRegression(), Ridge()], random_state=0)
    """

    def __init__(
        self,
        base_estimators: list[BaseEstimator] | None = None,
        n_folds: int = 5,
        random_state: int = 0,
    ) -> None:
        self.base_estimators = base_estimators or []
        self.n_folds = n_folds
        self.random_state = random_state
        self._meta_weights: np.ndarray | None = None
        self._fitted_estimators: list[BaseEstimator] = []

    def fit(self, X: np.ndarray, y: np.ndarray) -> StackingEnsemble:
        """Fit the stacking ensemble via cross-fitted base predictions.

        Args:
            X: Feature matrix of shape (n_samples, n_features).
            y: Target array of shape (n_samples,).

        Returns:
            Self.

        Raises:
            ValueError: If no base estimators are provided.

        Examples:
            >>> import numpy as np
            >>> from sklearn.linear_model import LinearRegression, Ridge
            >>> se = StackingEnsemble(
            ...     base_estimators=[LinearRegression(), Ridge()],
            ...     n_folds=2, random_state=0,
            ... )
            >>> X = np.array([[1], [2], [3], [4], [5], [6]])
            >>> y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
            >>> _ = se.fit(X, y)
        """
        if not self.base_estimators:
            msg = "At least one base estimator must be provided"
            raise ValueError(msg)

        from scipy.optimize import nnls

        seed = derive_seed(self.random_state, namespace="stacking_ensemble")
        n_samples = X.shape[0]
        n_estimators = len(self.base_estimators)
        meta_features = np.zeros((n_samples, n_estimators))

        kf = KFold(n_splits=self.n_folds, shuffle=True, random_state=seed)
        for train_idx, val_idx in kf.split(X):
            for j, est in enumerate(self.base_estimators):
                from sklearn.base import clone

                cloned = clone(est)
                cloned.fit(X[train_idx], y[train_idx])
                meta_features[val_idx, j] = cloned.predict(X[val_idx])

        self._meta_weights, _ = nnls(meta_features, y)
        weight_sum = self._meta_weights.sum()
        if weight_sum > 0:
            self._meta_weights = self._meta_weights / weight_sum

        self._fitted_estimators = []
        for est in self.base_estimators:
            from sklearn.base import clone

            cloned = clone(est)
            cloned.fit(X, y)
            self._fitted_estimators.append(cloned)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using the stacking ensemble.

        Args:
            X: Feature matrix of shape (n_samples, n_features).

        Returns:
            Predicted values of shape (n_samples,).

        Raises:
            RuntimeError: If the ensemble has not been fitted.

        Examples:
            >>> import numpy as np
            >>> from sklearn.linear_model import LinearRegression, Ridge
            >>> se = StackingEnsemble(
            ...     base_estimators=[LinearRegression(), Ridge()],
            ...     n_folds=2, random_state=0,
            ... )
            >>> X = np.array([[1], [2], [3], [4], [5], [6]])
            >>> y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
            >>> _ = se.fit(X, y)
            >>> se.predict(X).shape
            (6,)
        """
        if self._meta_weights is None or not self._fitted_estimators:
            msg = "Ensemble has not been fitted"
            raise RuntimeError(msg)

        preds = np.column_stack([est.predict(X) for est in self._fitted_estimators])
        return np.asarray(preds @ self._meta_weights)
