"""Rolling-origin cross-validation for time-series evaluation."""

from __future__ import annotations

from collections.abc import Iterator

import polars as pl


def rolling_origin_cv(
    df: pl.DataFrame,
    *,
    time_col: str = "year",
    min_train_size: int = 3,
    step: int = 1,
) -> Iterator[tuple[pl.DataFrame, pl.DataFrame]]:
    """Generate rolling-origin train/test splits.

    Args:
        df: Input DataFrame with a time column.
        time_col: Name of the time column.
        min_train_size: Minimum number of time periods in the training set.
        step: Number of time periods to step forward each iteration.

    Yields:
        Tuple of (train_df, test_df) for each split.

    Raises:
        KeyError: If time_col is not in the DataFrame.
        ValueError: If min_train_size is non-positive.

    Examples:
        >>> import polars as pl
        >>> df = pl.DataFrame({"year": [2010, 2011, 2012, 2013, 2014], "v": [1, 2, 3, 4, 5]})
        >>> splits = list(rolling_origin_cv(df, min_train_size=2, step=1))
        >>> len(splits)
        3
    """
    if time_col not in df.columns:
        msg = f"Column {time_col!r} not found in DataFrame"
        raise KeyError(msg)
    if min_train_size <= 0:
        msg = "min_train_size must be positive"
        raise ValueError(msg)

    periods = sorted(df[time_col].unique().to_list())
    n_periods = len(periods)

    idx = min_train_size
    while idx < n_periods:
        train_periods = periods[:idx]
        test_periods = periods[idx : idx + step]
        if not test_periods:
            break
        train_df = df.filter(pl.col(time_col).is_in(train_periods))
        test_df = df.filter(pl.col(time_col).is_in(test_periods))
        yield train_df, test_df
        idx += step
