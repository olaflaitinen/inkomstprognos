"""Ingestion module for Swedish tax register (IoT) data."""

from __future__ import annotations

import pathlib

import numpy as np
import polars as pl

from inkomstprognos.seeds import SYNTHETIC_SEED, derive_seed, set_global_seed

TAX_COLUMNS: list[str] = [
    "person_id",
    "year",
    "taxable_earned_income",
    "taxable_capital_income",
    "municipal_tax",
    "state_tax",
    "basic_deduction",
    "jobbskatteavdrag",
    "final_tax",
]


def read_tax_register(path: pathlib.Path) -> pl.DataFrame:
    """Read a tax-register-like Parquet file into a Polars DataFrame.

    Args:
        path: Path to the Parquet file.

    Returns:
        Polars DataFrame with tax register schema.

    Raises:
        FileNotFoundError: If the file does not exist.

    Examples:
        >>> import tempfile, pathlib
        >>> df = synthetic_tax_register(n=100, years=2)
        >>> p = pathlib.Path(tempfile.mktemp(suffix=".parquet"))
        >>> df.write_parquet(p)
        >>> result = read_tax_register(p)
        >>> len(result) > 0
        True
    """
    if not path.exists():
        msg = f"Tax register file not found: {path}"
        raise FileNotFoundError(msg)
    return pl.read_parquet(path)


def synthetic_tax_register(
    n: int = 50000,
    years: int = 10,
    seed: int = SYNTHETIC_SEED,
) -> pl.DataFrame:
    """Generate a synthetic tax-register-like fixture.

    Args:
        n: Number of synthetic individuals.
        years: Number of years to simulate.
        seed: Random seed for reproducibility.

    Returns:
        Polars DataFrame with synthetic tax register records.

    Raises:
        ValueError: If n or years is non-positive.

    Examples:
        >>> df = synthetic_tax_register(n=100, years=2, seed=42)
        >>> df.shape[0]
        200
    """
    if n <= 0:
        msg = "n must be positive"
        raise ValueError(msg)
    if years <= 0:
        msg = "years must be positive"
        raise ValueError(msg)

    set_global_seed(seed)
    rng = np.random.default_rng(derive_seed(seed, namespace="tax_register"))

    base_year = 2010
    records: dict[str, list[object]] = {col: [] for col in TAX_COLUMNS}

    for year_offset in range(years):
        year = base_year + year_offset
        earned = np.maximum(0, rng.normal(350000, 120000, size=n)).astype(np.float64)
        capital = np.maximum(0, rng.exponential(25000, size=n)).astype(np.float64)
        municipal = (earned * rng.uniform(0.29, 0.35, size=n)).astype(np.float64)
        state = np.where(earned > 540000, (earned - 540000) * 0.20, 0.0).astype(np.float64)
        basic_ded = np.minimum(earned * 0.10, 36000.0).astype(np.float64)
        jsa = np.minimum(earned * 0.07, 30000.0).astype(np.float64)
        final = np.maximum(0, municipal + state - basic_ded - jsa).astype(np.float64)

        for i in range(n):
            records["person_id"].append(i + 1)
            records["year"].append(year)
            records["taxable_earned_income"].append(float(earned[i]))
            records["taxable_capital_income"].append(float(capital[i]))
            records["municipal_tax"].append(float(municipal[i]))
            records["state_tax"].append(float(state[i]))
            records["basic_deduction"].append(float(basic_ded[i]))
            records["jobbskatteavdrag"].append(float(jsa[i]))
            records["final_tax"].append(float(final[i]))

    return pl.DataFrame(records)
