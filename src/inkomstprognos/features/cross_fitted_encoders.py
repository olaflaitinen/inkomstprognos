"""Cross-fitted target encoders with leakage control."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import KFold

from inkomstprognos.seeds import derive_seed


class CrossFittedTargetEncoder(BaseEstimator, TransformerMixin):  # type: ignore[misc]
    """Target encoder with cross-fitted leakage control.

    Encodes categorical features using the mean of the target variable,
    computed via cross-fitting to prevent information leakage.

    Args:
        cols: List of column names to encode.
        n_folds: Number of cross-validation folds.
        smoothing: Smoothing factor for the encoding.
        random_state: Random state for fold assignment.

    Examples:
        >>> import pandas as pd, numpy as np
        >>> enc = CrossFittedTargetEncoder(cols=["cat"], n_folds=2, random_state=0)
        >>> X = pd.DataFrame({"cat": ["a", "b", "a", "b"]})
        >>> y = np.array([1.0, 2.0, 3.0, 4.0])
        >>> enc.fit(X, y)
        CrossFittedTargetEncoder(cols=['cat'], n_folds=2, random_state=0)
        >>> result = enc.transform(X)
        >>> result.shape
        (4, 1)
    """

    def __init__(
        self,
        cols: list[str] | None = None,
        n_folds: int = 5,
        smoothing: float = 10.0,
        random_state: int = 0,
    ) -> None:
        self.cols = cols or []
        self.n_folds = n_folds
        self.smoothing = smoothing
        self.random_state = random_state
        self._encodings: dict[str, dict[object, float]] = {}
        self._global_mean: float = 0.0

    def fit(
        self,
        X: pd.DataFrame,
        y: np.ndarray | None = None,
    ) -> CrossFittedTargetEncoder:
        """Fit the encoder on training data.

        Args:
            X: Feature DataFrame.
            y: Target array.

        Returns:
            Self.

        Raises:
            ValueError: If y is None.
        """
        if y is None:
            msg = "y must be provided for target encoding"
            raise ValueError(msg)

        self._global_mean = float(np.mean(y))
        seed = derive_seed(self.random_state, namespace="cross_fitted_encoder")

        for col in self.cols:
            col_encodings: dict[object, float] = {}
            kf = KFold(n_splits=self.n_folds, shuffle=True, random_state=seed)
            accum: dict[object, list[float]] = {}

            for _, val_idx in kf.split(X):
                val_x = X.iloc[val_idx]
                val_y = y[val_idx]
                for cat_val in val_x[col].unique():
                    mask = val_x[col] == cat_val
                    cat_mean = float(np.mean(val_y[mask.values]))
                    cat_count = int(mask.sum())
                    smoothed = (cat_count * cat_mean + self.smoothing * self._global_mean) / (
                        cat_count + self.smoothing
                    )
                    if cat_val not in accum:
                        accum[cat_val] = []
                    accum[cat_val].append(smoothed)

            for cat_val, values in accum.items():
                col_encodings[cat_val] = float(np.mean(values))
            self._encodings[col] = col_encodings

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform categorical columns to target-encoded values.

        Args:
            X: Feature DataFrame.

        Returns:
            DataFrame with encoded columns.

        Raises:
            RuntimeError: If the encoder has not been fitted.

        Examples:
            >>> import pandas as pd, numpy as np
            >>> enc = CrossFittedTargetEncoder(cols=["cat"], n_folds=2, random_state=0)
            >>> X = pd.DataFrame({"cat": ["a", "b", "a", "b"]})
            >>> y = np.array([1.0, 2.0, 3.0, 4.0])
            >>> _ = enc.fit(X, y)
            >>> enc.transform(X).shape
            (4, 1)
        """
        if not self._encodings:
            msg = "Encoder has not been fitted"
            raise RuntimeError(msg)

        result = pd.DataFrame(index=X.index)
        for col in self.cols:
            enc = self._encodings.get(col, {})
            result[col] = X[col].map(enc).fillna(self._global_mean)
        return result
