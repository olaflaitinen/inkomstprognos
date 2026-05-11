"""Tests for the state-space model module."""

from __future__ import annotations

import numpy as np
import pytest

from inkomstprognos.models.state_space import HierarchicalStateSpace


class TestHierarchicalStateSpace:
    def test_fit(self) -> None:
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        model = HierarchicalStateSpace(num_warmup=5, num_samples=5, num_chains=1, random_state=42)
        model.fit(y)
        assert model._fitted

    def test_predict(self) -> None:
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        model = HierarchicalStateSpace(num_warmup=5, num_samples=5, num_chains=1, random_state=42)
        model.fit(y)
        preds = model.predict(horizon=3)
        assert preds.shape == (5, 3)

    def test_predict_unfitted_raises(self) -> None:
        model = HierarchicalStateSpace()
        with pytest.raises(RuntimeError, match="not been fitted"):
            model.predict(horizon=1)

    def test_predict_invalid_horizon(self) -> None:
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        model = HierarchicalStateSpace(num_warmup=5, num_samples=5, num_chains=1, random_state=42)
        model.fit(y)
        with pytest.raises(ValueError, match="positive"):
            model.predict(horizon=0)

    def test_fit_empty_raises(self) -> None:
        model = HierarchicalStateSpace()
        with pytest.raises(ValueError, match="non-empty"):
            model.fit(np.array([]))
