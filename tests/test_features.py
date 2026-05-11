"""Tests for the features module."""

from __future__ import annotations

import numpy as np
import pandas as pd
import polars as pl
import pytest

from inkomstprognos.features.cross_fitted_encoders import CrossFittedTargetEncoder
from inkomstprognos.features.lifecycle import compute_age_cohort, equivalise
from inkomstprognos.features.macro_join import join_macro


class TestCrossFittedTargetEncoder:
    def test_fit_transform(self) -> None:
        X = pd.DataFrame({"cat": ["a", "b", "a", "b", "a", "b"]})
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        enc = CrossFittedTargetEncoder(cols=["cat"], n_folds=2, random_state=0)
        enc.fit(X, y)
        result = enc.transform(X)
        assert result.shape == (6, 1)
        assert not result.isna().any().any()

    def test_no_y_raises(self) -> None:
        X = pd.DataFrame({"cat": ["a", "b"]})
        enc = CrossFittedTargetEncoder(cols=["cat"])
        with pytest.raises(ValueError, match="y must be provided"):
            enc.fit(X, None)

    def test_unfitted_raises(self) -> None:
        X = pd.DataFrame({"cat": ["a", "b"]})
        enc = CrossFittedTargetEncoder(cols=["cat"])
        with pytest.raises(RuntimeError, match="not been fitted"):
            enc.transform(X)

    def test_unseen_category(self) -> None:
        X_train = pd.DataFrame({"cat": ["a", "b", "a", "b"]})
        y = np.array([1.0, 2.0, 3.0, 4.0])
        enc = CrossFittedTargetEncoder(cols=["cat"], n_folds=2, random_state=0)
        enc.fit(X_train, y)
        X_new = pd.DataFrame({"cat": ["c"]})
        result = enc.transform(X_new)
        assert not result.isna().any().any()


class TestLifecycle:
    def test_compute_age_cohort(self) -> None:
        df = pl.DataFrame({"age": [30, 40], "year": [2020, 2020]})
        result = compute_age_cohort(df)
        assert result.to_list() == [1990, 1980]

    def test_missing_age_col(self) -> None:
        df = pl.DataFrame({"year": [2020]})
        with pytest.raises(KeyError):
            compute_age_cohort(df)

    def test_missing_year_col(self) -> None:
        df = pl.DataFrame({"age": [30]})
        with pytest.raises(KeyError):
            compute_age_cohort(df)

    def test_equivalise_sqrt(self) -> None:
        df = pl.DataFrame(
            {
                "disp_income": [100000.0],
                "household_size": [4],
            }
        )
        result = equivalise(df, scale="square-root")
        assert "equiv_income" in result.columns
        assert abs(result["equiv_income"][0] - 50000.0) < 1.0

    def test_equivalise_oecd(self) -> None:
        df = pl.DataFrame(
            {
                "disp_income": [100000.0],
                "household_size": [4],
                "n_adults": [2],
                "n_children": [2],
            }
        )
        result = equivalise(df, scale="oecd-modified")
        assert "equiv_income" in result.columns
        expected_weight = 1.0 + 0.5 + 0.6
        expected_income = 100000.0 / expected_weight
        assert abs(result["equiv_income"][0] - expected_income) < 1.0

    def test_equivalise_missing_income(self) -> None:
        df = pl.DataFrame({"household_size": [4]})
        with pytest.raises(KeyError):
            equivalise(df)

    def test_equivalise_unknown_scale(self) -> None:
        df = pl.DataFrame({"disp_income": [100.0], "household_size": [1]})
        with pytest.raises(ValueError, match="Unknown"):
            equivalise(df, scale="unknown")  # type: ignore[arg-type]


class TestMacroJoin:
    def test_join_with_lag(self) -> None:
        micro = pl.DataFrame(
            {
                "year": [2020, 2021],
                "region": ["SE110", "SE110"],
                "income": [100, 200],
            }
        )
        macro = pl.DataFrame(
            {
                "year": [2019, 2020],
                "region": ["SE110", "SE110"],
                "gdp_growth": [1.5, 2.0],
            }
        )
        result = join_macro(micro, macro)
        assert "gdp_growth" in result.columns
        assert result.shape[0] == 2

    def test_empty_on_raises(self) -> None:
        micro = pl.DataFrame({"year": [2020]})
        macro = pl.DataFrame({"year": [2019]})
        with pytest.raises(ValueError, match="non-empty"):
            join_macro(micro, macro, on=())

    def test_missing_column_raises(self) -> None:
        micro = pl.DataFrame({"year": [2020]})
        macro = pl.DataFrame({"year": [2019]})
        with pytest.raises(KeyError):
            join_macro(micro, macro, on=("year", "missing"))
