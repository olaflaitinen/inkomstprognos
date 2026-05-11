"""Ingestion module for LISA panel data."""

from __future__ import annotations

import pathlib

import numpy as np
import polars as pl

from inkomstprognos.seeds import SYNTHETIC_SEED, derive_seed, set_global_seed

LISA_COLUMNS: list[str] = [
    "person_id",
    "year",
    "age",
    "gender",
    "region",
    "education_level",
    "country_of_birth",
    "household_type",
    "disp_income",
    "gross_labour_income",
    "capital_income",
    "transfer_income",
]

REGIONS: list[str] = [
    "SE110",
    "SE121",
    "SE122",
    "SE123",
    "SE124",
    "SE125",
    "SE211",
    "SE212",
    "SE213",
    "SE214",
    "SE221",
    "SE224",
    "SE231",
    "SE232",
    "SE311",
    "SE312",
    "SE313",
    "SE321",
    "SE322",
    "SE331",
    "SE332",
]

EDUCATION_LEVELS: list[int] = [1, 2, 3, 4, 5, 6, 7]

BIRTH_GROUPS: list[str] = [
    "sweden",
    "nordic",
    "eu_eea",
    "europe_non_eu",
    "mena",
    "rest_of_world",
]

HOUSEHOLD_TYPES: list[str] = [
    "single",
    "couple_no_children",
    "couple_with_children",
    "single_parent",
    "multi_adult",
]


def read_lisa(
    path: pathlib.Path,
    *,
    columns: list[str] | None = None,
) -> pl.DataFrame:
    """Read a LISA-like Parquet file into a Polars DataFrame.

    Args:
        path: Path to the Parquet file.
        columns: Optional subset of columns to read.

    Returns:
        Polars DataFrame with LISA-like schema.

    Raises:
        FileNotFoundError: If the file does not exist.

    Examples:
        >>> import tempfile, pathlib
        >>> df = synthetic_lisa(n=100, years=2)
        >>> p = pathlib.Path(tempfile.mktemp(suffix=".parquet"))
        >>> df.write_parquet(p)
        >>> result = read_lisa(p)
        >>> len(result) > 0
        True
    """
    if not path.exists():
        msg = f"LISA file not found: {path}"
        raise FileNotFoundError(msg)
    if columns is not None:
        return pl.read_parquet(path, columns=columns)
    return pl.read_parquet(path)


def synthetic_lisa(
    n: int = 50000,
    years: int = 10,
    seed: int = SYNTHETIC_SEED,
) -> pl.DataFrame:
    """Generate a synthetic LISA-like fixture.

    Args:
        n: Number of synthetic individuals.
        years: Number of years to simulate.
        seed: Random seed for reproducibility.

    Returns:
        Polars DataFrame with synthetic LISA-like records.

    Raises:
        ValueError: If n or years is non-positive.

    Examples:
        >>> df = synthetic_lisa(n=100, years=2, seed=42)
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
    rng = np.random.default_rng(derive_seed(seed, namespace="lisa"))

    base_year = 2010
    records: dict[str, list[object]] = {col: [] for col in LISA_COLUMNS}

    for year_offset in range(years):
        year = base_year + year_offset
        ages = rng.integers(18, 80, size=n)
        genders = rng.choice([0, 1], size=n)
        regions = rng.choice(REGIONS, size=n)
        edu = rng.choice(EDUCATION_LEVELS, size=n)
        cob = rng.choice(BIRTH_GROUPS, size=n)
        htype = rng.choice(HOUSEHOLD_TYPES, size=n)

        base_income = 200000 + ages * 3000 + edu * 15000
        noise = rng.normal(0, 30000, size=n)
        disp = np.maximum(0, base_income + noise).astype(np.float64)
        gross_labour = np.maximum(0, disp * rng.uniform(1.1, 1.5, size=n)).astype(np.float64)
        capital = np.maximum(0, rng.exponential(20000, size=n)).astype(np.float64)
        transfer = np.maximum(0, rng.exponential(10000, size=n)).astype(np.float64)

        for i in range(n):
            records["person_id"].append(i + 1)
            records["year"].append(year)
            records["age"].append(int(ages[i]))
            records["gender"].append(int(genders[i]))
            records["region"].append(str(regions[i]))
            records["education_level"].append(int(edu[i]))
            records["country_of_birth"].append(str(cob[i]))
            records["household_type"].append(str(htype[i]))
            records["disp_income"].append(float(disp[i]))
            records["gross_labour_income"].append(float(gross_labour[i]))
            records["capital_income"].append(float(capital[i]))
            records["transfer_income"].append(float(transfer[i]))

    return pl.DataFrame(records)
