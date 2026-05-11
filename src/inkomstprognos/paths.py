"""Path constants resolved from environment variables with fallbacks."""

from __future__ import annotations

import os
import pathlib


def _resolve(env_var: str, fallback: str) -> pathlib.Path:
    return pathlib.Path(os.environ.get(env_var, fallback)).resolve()


DATA_ROOT: pathlib.Path = _resolve("INKOMSTPROGNOS_DATA_ROOT", "data")
"""Root directory for input data."""

SYNTHETIC_ROOT: pathlib.Path = _resolve("INKOMSTPROGNOS_SYNTHETIC_ROOT", "data/synthetic")
"""Root directory for synthetic data fixtures."""

REPORTS_ROOT: pathlib.Path = _resolve("INKOMSTPROGNOS_REPORTS_ROOT", "reports")
"""Root directory for generated reports."""
