"""Lifecycle and equivalisation feature engineering."""

from __future__ import annotations

from typing import Literal

import polars as pl


def compute_age_cohort(
    df: pl.DataFrame,
    *,
    age_col: str = "age",
    year_col: str = "year",
) -> pl.Series:
    """Compute birth-cohort labels from age and year columns.

    Args:
        df: Input DataFrame.
        age_col: Name of the age column.
        year_col: Name of the year column.

    Returns:
        Polars Series with birth-year cohort labels.

    Raises:
        KeyError: If required columns are missing.

    Examples:
        >>> import polars as pl
        >>> df = pl.DataFrame({"age": [30, 40], "year": [2020, 2020]})
        >>> cohort = compute_age_cohort(df)
        >>> cohort.to_list()
        [1990, 1980]
    """
    if age_col not in df.columns:
        msg = f"Column {age_col!r} not found in DataFrame"
        raise KeyError(msg)
    if year_col not in df.columns:
        msg = f"Column {year_col!r} not found in DataFrame"
        raise KeyError(msg)
    return (df[year_col] - df[age_col]).alias("birth_cohort")


def equivalise(
    df: pl.DataFrame,
    scale: Literal["oecd-modified", "square-root"] = "oecd-modified",
) -> pl.DataFrame:
    """Equivalise household income using a standard equivalence scale.

    The OECD-modified scale assigns 1.0 to the first adult, 0.5 to each
    additional adult (14+), and 0.3 to each child (<14). The square-root
    scale divides by the square root of household size.

    Args:
        df: DataFrame with 'disp_income' and 'household_size' columns.
        scale: Equivalence scale to apply.

    Returns:
        DataFrame with an added 'equiv_income' column.

    Raises:
        KeyError: If required columns are missing.
        ValueError: If scale is not recognised.

    Examples:
        >>> import polars as pl
        >>> df = pl.DataFrame(
        ...     {"disp_income": [100000.0], "household_size": [4],
        ...      "n_adults": [2], "n_children": [2]}
        ... )
        >>> result = equivalise(df, scale="oecd-modified")
        >>> "equiv_income" in result.columns
        True
    """
    if "disp_income" not in df.columns:
        msg = "Column 'disp_income' not found in DataFrame"
        raise KeyError(msg)
    if "household_size" not in df.columns:
        msg = "Column 'household_size' not found in DataFrame"
        raise KeyError(msg)

    if scale == "square-root":
        equiv = df["disp_income"] / df["household_size"].cast(pl.Float64).sqrt()
        return df.with_columns(equiv.alias("equiv_income"))

    if scale == "oecd-modified":
        if "n_adults" not in df.columns or "n_children" not in df.columns:
            msg = "OECD-modified scale requires 'n_adults' and 'n_children' columns"
            raise KeyError(msg)
        oecd_weight = (
            pl.lit(1.0)
            + (df["n_adults"].cast(pl.Float64) - 1.0) * 0.5
            + df["n_children"].cast(pl.Float64) * 0.3
        )
        equiv = df["disp_income"] / oecd_weight
        return df.with_columns(equiv.alias("equiv_income"))

    msg = f"Unknown equivalence scale: {scale!r}"
    raise ValueError(msg)
