"""Tests for the conformal prediction module."""

from __future__ import annotations

import numpy as np
import pytest
from sklearn.linear_model import LinearRegression

from inkomstprognos.models.conformal import MondrianConformal, SplitConformal


class TestSplitConformal:
    def test_fit_calibrate_predict(self) -> None:
        rng = np.random.default_rng(42)
        X_train = rng.normal(size=(50, 2))
        y_train = X_train[:, 0] + rng.normal(0, 0.1, size=50)
        X_calib = rng.normal(size=(20, 2))
        y_calib = X_calib[:, 0] + rng.normal(0, 0.1, size=20)
        sc = SplitConformal(base_estimator=LinearRegression(), random_state=0)
        sc.fit_calibrate(X_train, y_train, X_calib, y_calib)
        lo, hi = sc.predict_interval(X_calib, alpha=0.1)
        assert lo.shape == (20,)
        assert hi.shape == (20,)
        assert np.all(hi >= lo)

    def test_no_estimator_raises(self) -> None:
        sc = SplitConformal(base_estimator=None)
        with pytest.raises(ValueError, match="base_estimator"):
            sc.fit_calibrate(
                np.array([[1]]),
                np.array([1.0]),
                np.array([[2]]),
                np.array([2.0]),
            )

    def test_uncalibrated_raises(self) -> None:
        sc = SplitConformal(base_estimator=LinearRegression())
        with pytest.raises(RuntimeError, match="not been calibrated"):
            sc.predict_interval(np.array([[1]]))

    def test_invalid_alpha(self) -> None:
        rng = np.random.default_rng(0)
        X = rng.normal(size=(20, 1))
        y = X[:, 0]
        sc = SplitConformal(base_estimator=LinearRegression())
        sc.fit_calibrate(X, y, X, y)
        with pytest.raises(ValueError, match="alpha"):
            sc.predict_interval(X, alpha=0.0)


class TestMondrianConformal:
    def test_fit_calibrate_predict_with_strata(self) -> None:
        rng = np.random.default_rng(42)
        X = rng.normal(size=(40, 2))
        y = X[:, 0] + rng.normal(0, 0.1, size=40)
        strata = np.array([0] * 20 + [1] * 20)
        mc = MondrianConformal(base_estimator=LinearRegression(), random_state=0)
        mc.fit_calibrate(X, y, X, y, strata=strata)
        lo, hi = mc.predict_interval(X, alpha=0.1, strata=strata)
        assert lo.shape == (40,)
        assert np.all(hi >= lo)

    def test_fit_calibrate_predict_without_strata(self) -> None:
        rng = np.random.default_rng(42)
        X = rng.normal(size=(40, 2))
        y = X[:, 0]
        mc = MondrianConformal(base_estimator=LinearRegression(), random_state=0)
        mc.fit_calibrate(X, y, X, y)
        lo, hi = mc.predict_interval(X, alpha=0.1)
        assert lo.shape == (40,)

    def test_no_estimator_raises(self) -> None:
        mc = MondrianConformal(base_estimator=None)
        with pytest.raises(ValueError, match="base_estimator"):
            mc.fit_calibrate(
                np.array([[1]]),
                np.array([1.0]),
                np.array([[2]]),
                np.array([2.0]),
            )

    def test_uncalibrated_raises(self) -> None:
        mc = MondrianConformal(base_estimator=LinearRegression())
        with pytest.raises(RuntimeError, match="not been calibrated"):
            mc.predict_interval(np.array([[1]]))
