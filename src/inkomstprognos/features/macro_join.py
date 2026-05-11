"""Macro-covariate join with vintage lag control."""

from __future__ import annotations

import polars as pl


def join_macro(
    df_micro: pl.DataFrame,
    df_macro: pl.DataFrame,
    *,
    on: tuple[str, ...] = ("year", "region"),
) -> pl.DataFrame:
    """Join macro covariates to micro data with a one-year lag.

    Macro covariates are joined with a one-year lag to avoid look-ahead
    bias: the macro data for year t-1 is joined to micro data for year t.

    Args:
        df_micro: Micro-level DataFrame.
        df_macro: Macro-level DataFrame with covariates.
        on: Tuple of column names to join on. The first element must be
            the time column (typically 'year').

    Returns:
        Joined DataFrame with macro covariates appended.

    Raises:
        KeyError: If join columns are not found.
        ValueError: If on tuple is empty.

    Examples:
        >>> import polars as pl
        >>> micro = pl.DataFrame(
        ...     {"year": [2020, 2021], "region": ["SE110", "SE110"],
        ...      "income": [100, 200]}
        ... )
        >>> macro = pl.DataFrame(
        ...     {"year": [2019, 2020], "region": ["SE110", "SE110"],
        ...      "gdp_growth": [1.5, 2.0]}
        ... )
        >>> result = join_macro(micro, macro)
        >>> "gdp_growth" in result.columns
        True
    """
    if not on:
        msg = "on must be a non-empty tuple"
        raise ValueError(msg)

    time_col = on[0]
    for col in on:
        if col not in df_micro.columns:
            msg = f"Column {col!r} not found in micro DataFrame"
            raise KeyError(msg)
        if col not in df_macro.columns:
            msg = f"Column {col!r} not found in macro DataFrame"
            raise KeyError(msg)

    df_macro_lagged = df_macro.with_columns((pl.col(time_col) + 1).alias(time_col))

    micro_cols = set(df_micro.columns)
    macro_join_cols = set(on)
    macro_data_cols = [
        c for c in df_macro_lagged.columns if c not in micro_cols or c in macro_join_cols
    ]

    result = df_micro.join(
        df_macro_lagged.select(macro_data_cols),
        on=list(on),
        how="left",
    )
    return result
