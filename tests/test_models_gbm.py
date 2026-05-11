"""Tests for the GBM model module."""

from __future__ import annotations

import numpy as np
import pytest

from inkomstprognos.models.gbm import MonotonicGBM


class TestMonotonicGBM:
    def test_fit_predict_lightgbm(self) -> None:
        rng = np.random.default_rng(42)
        X = rng.normal(size=(100, 3))
        y = X[:, 0] * 2 + X[:, 1] + rng.normal(0, 0.1, size=100)
        model = MonotonicGBM(engine="lightgbm", n_estimators=10, random_state=42)
        model.fit(X, y)
        preds = model.predict(X)
        assert preds.shape == (100,)

    def test_fit_predict_xgboost(self) -> None:
        rng = np.random.default_rng(42)
        X = rng.normal(size=(100, 3))
        y = X[:, 0] * 2 + rng.normal(0, 0.1, size=100)
        model = MonotonicGBM(engine="xgboost", n_estimators=10, random_state=42)
        model.fit(X, y)
        preds = model.predict(X)
        assert preds.shape == (100,)

    def test_predict_unfitted_raises(self) -> None:
        model = MonotonicGBM()
        with pytest.raises(RuntimeError, match="not been fitted"):
            model.predict(np.array([[1, 2]]))

    def test_predict_quantile(self) -> None:
        rng = np.random.default_rng(42)
        X = rng.normal(size=(50, 2))
        y = X[:, 0] + rng.normal(0, 0.1, size=50)
        model = MonotonicGBM(engine="lightgbm", n_estimators=10, random_state=42)
        model.fit(X, y)
        q90 = model.predict_quantile(X, 0.9)
        q10 = model.predict_quantile(X, 0.1)
        assert q90.shape == (50,)
        assert np.all(q90 >= q10)

    def test_predict_quantile_invalid_q(self) -> None:
        rng = np.random.default_rng(42)
        X = rng.normal(size=(10, 2))
        y = X[:, 0]
        model = MonotonicGBM(engine="lightgbm", n_estimators=5, random_state=0)
        model.fit(X, y)
        with pytest.raises(ValueError, match="q must be in"):
            model.predict_quantile(X, 1.5)

    def test_unsupported_engine(self) -> None:
        model = MonotonicGBM(engine="invalid")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="Unsupported engine"):
            model.fit(np.array([[1]]), np.array([1.0]))

    def test_deterministic(self) -> None:
        rng = np.random.default_rng(42)
        X = rng.normal(size=(50, 2))
        y = X[:, 0] + 1
        m1 = MonotonicGBM(engine="lightgbm", n_estimators=10, random_state=99)
        m2 = MonotonicGBM(engine="lightgbm", n_estimators=10, random_state=99)
        m1.fit(X, y)
        m2.fit(X, y)
        np.testing.assert_array_equal(m1.predict(X), m2.predict(X))
