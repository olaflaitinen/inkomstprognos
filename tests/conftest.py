"""Shared test fixtures for Inkomstprognos."""

from __future__ import annotations

import pathlib

import numpy as np
import polars as pl
import pytest

from inkomstprognos.config import Config
from inkomstprognos.ingestion.lisa import synthetic_lisa
from inkomstprognos.ingestion.tax_registers import synthetic_tax_register


@pytest.fixture
def tmp_path_factory_clean(tmp_path: pathlib.Path) -> pathlib.Path:
    """Provide a clean temporary directory."""
    return tmp_path


@pytest.fixture
def sample_config(tmp_path: pathlib.Path) -> Config:
    """Provide a sample Config for testing."""
    return Config(data_root=tmp_path, seed=42, horizon=1, n_jobs=1)


@pytest.fixture
def small_lisa() -> pl.DataFrame:
    """Provide a small synthetic LISA fixture."""
    return synthetic_lisa(n=200, years=3, seed=42)


@pytest.fixture
def small_tax() -> pl.DataFrame:
    """Provide a small synthetic tax register fixture."""
    return synthetic_tax_register(n=200, years=3, seed=42)


@pytest.fixture
def numpy_rng() -> np.random.Generator:
    """Provide a seeded numpy random generator."""
    return np.random.default_rng(42)
