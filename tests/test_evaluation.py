"""Tests for the evaluation module."""

from __future__ import annotations

import numpy as np
import polars as pl
import pytest

from inkomstprognos.evaluation.calibration import pit_histogram, reliability_diagram
from inkomstprognos.evaluation.metrics import (
    coverage,
    crps_sample,
    interval_width,
    mae,
    mape,
    pinball_loss,
    rmse,
)
from inkomstprognos.evaluation.rolling_origin import rolling_origin_cv


class TestMetrics:
    def test_mae_perfect(self) -> None:
        y = np.array([1.0, 2.0, 3.0])
        assert mae(y, y) == 0.0

    def test_mae_known(self) -> None:
        y_true = np.array([1.0, 2.0])
        y_pred = np.array([1.1, 1.9])
        assert abs(mae(y_true, y_pred) - 0.1) < 1e-10

    def test_rmse_perfect(self) -> None:
        y = np.array([1.0, 2.0, 3.0])
        assert rmse(y, y) == 0.0

    def test_rmse_known(self) -> None:
        y_true = np.array([0.0, 0.0])
        y_pred = np.array([1.0, 1.0])
        assert abs(rmse(y_true, y_pred) - 1.0) < 1e-10

    def test_mape(self) -> None:
        y_true = np.array([100.0, 200.0])
        y_pred = np.array([110.0, 190.0])
        result = mape(y_true, y_pred)
        assert abs(result - 0.075) < 1e-10

    def test_mape_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="zeros"):
            mape(np.array([0.0, 1.0]), np.array([1.0, 1.0]))

    def test_coverage_full(self) -> None:
        y = np.array([1.0, 2.0, 3.0])
        lo = np.array([0.0, 1.0, 2.0])
        hi = np.array([2.0, 3.0, 4.0])
        assert coverage(y, lo, hi) == 1.0

    def test_coverage_partial(self) -> None:
        y = np.array([1.0, 5.0])
        lo = np.array([0.0, 0.0])
        hi = np.array([2.0, 3.0])
        assert coverage(y, lo, hi) == 0.5

    def test_interval_width(self) -> None:
        lo = np.array([0.0, 1.0])
        hi = np.array([2.0, 3.0])
        assert interval_width(lo, hi) == 2.0

    def test_pinball_loss_median(self) -> None:
        y_true = np.array([1.0, 2.0])
        y_q = np.array([1.1, 1.9])
        loss = pinball_loss(y_true, y_q, 0.5)
        assert loss >= 0

    def test_pinball_loss_invalid_q(self) -> None:
        with pytest.raises(ValueError, match="q must be in"):
            pinball_loss(np.array([1.0]), np.array([1.0]), 0.0)

    def test_crps_sample(self) -> None:
        y = np.array([1.0, 2.0])
        samples = np.array([[1.0, 1.0, 1.0], [2.0, 2.0, 2.0]])
        score = crps_sample(y, samples)
        assert score == 0.0

    def test_crps_sample_invalid_shape(self) -> None:
        with pytest.raises(ValueError):
            crps_sample(np.array([[1.0]]), np.array([[1.0]]))


class TestCalibration:
    def test_pit_histogram(self) -> None:
        y_true = np.array([1.0, 2.0, 3.0])
        F_pred = np.array([0.3, 0.5, 0.7])
        edges, counts = pit_histogram(y_true, F_pred, n_bins=5)
        assert len(counts) == 5
        assert counts.sum() == 3

    def test_pit_histogram_invalid_F(self) -> None:
        with pytest.raises(ValueError, match="\\[0, 1\\]"):
            pit_histogram(np.array([1.0]), np.array([1.5]))

    def test_pit_histogram_shape_mismatch(self) -> None:
        with pytest.raises(ValueError, match="same shape"):
            pit_histogram(np.array([1.0, 2.0]), np.array([0.5]))

    def test_reliability_diagram(self) -> None:
        y = np.array([1.0, 2.0, 3.0])
        q_grid = np.array([0.25, 0.5, 0.75])
        preds = np.array([[0.5, 1.0, 1.5], [1.5, 2.0, 2.5], [2.5, 3.0, 3.5]])
        nom, obs = reliability_diagram(y, preds, q_grid)
        assert len(nom) == 3
        assert len(obs) == 3

    def test_reliability_diagram_shape_mismatch(self) -> None:
        with pytest.raises(ValueError):
            reliability_diagram(np.array([1.0]), np.array([[1.0, 2.0]]), np.array([0.5]))


class TestRollingOrigin:
    def test_basic_splits(self) -> None:
        df = pl.DataFrame(
            {
                "year": [2010, 2011, 2012, 2013, 2014],
                "value": [1, 2, 3, 4, 5],
            }
        )
        splits = list(rolling_origin_cv(df, min_train_size=2, step=1))
        assert len(splits) == 3
        train0, test0 = splits[0]
        assert sorted(train0["year"].to_list()) == [2010, 2011]
        assert test0["year"].to_list() == [2012]

    def test_missing_column(self) -> None:
        df = pl.DataFrame({"value": [1, 2, 3]})
        with pytest.raises(KeyError):
            list(rolling_origin_cv(df, time_col="year"))

    def test_invalid_min_train(self) -> None:
        df = pl.DataFrame({"year": [2010]})
        with pytest.raises(ValueError, match="positive"):
            list(rolling_origin_cv(df, min_train_size=0))
