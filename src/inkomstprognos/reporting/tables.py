"""Table export functions for CSV (with BOM), Parquet, and PDF/A."""

from __future__ import annotations

import pathlib

import pandas as pd


def to_csv_with_bom(df: pd.DataFrame, path: pathlib.Path) -> None:
    """Export a DataFrame to CSV with UTF-8 BOM for Excel compatibility.

    Args:
        df: DataFrame to export.
        path: Output file path.

    Returns:
        None.

    Examples:
        >>> import pandas as pd, pathlib, tempfile
        >>> df = pd.DataFrame({"a": [1, 2]})
        >>> p = pathlib.Path(tempfile.mktemp(suffix=".csv"))
        >>> to_csv_with_bom(df, p)
        >>> p.read_bytes()[:3]
        b'\\xef\\xbb\\xbf'
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def to_parquet(df: pd.DataFrame, path: pathlib.Path) -> None:
    """Export a DataFrame to Parquet format.

    Args:
        df: DataFrame to export.
        path: Output file path.

    Returns:
        None.

    Examples:
        >>> import pandas as pd, pathlib, tempfile
        >>> df = pd.DataFrame({"a": [1, 2]})
        >>> p = pathlib.Path(tempfile.mktemp(suffix=".parquet"))
        >>> to_parquet(df, p)
        >>> p.exists()
        True
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False, engine="pyarrow")


def to_pdf_a_table(df: pd.DataFrame, path: pathlib.Path) -> None:
    """Export a DataFrame as a PDF/A-2u table.

    This is a simplified implementation using matplotlib for table
    rendering. For full PDF/A compliance, use the pdf_a module.

    Args:
        df: DataFrame to export.
        path: Output file path.

    Returns:
        None.

    Examples:
        >>> import pandas as pd, pathlib, tempfile
        >>> df = pd.DataFrame({"a": [1, 2]})
        >>> p = pathlib.Path(tempfile.mktemp(suffix=".pdf"))
        >>> to_pdf_a_table(df, p)
        >>> p.exists()
        True
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(max(8, len(df.columns) * 2), max(4, len(df) * 0.5 + 1)))
    ax.axis("off")
    table = ax.table(
        cellText=df.values,
        colLabels=list(df.columns),
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
