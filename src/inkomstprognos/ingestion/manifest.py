"""Declarative ingestion manifest for data-source validation."""

from __future__ import annotations

import pathlib

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]

import pandas as pd
from pydantic import BaseModel


class Manifest(BaseModel):
    """Declarative manifest describing a data source.

    Attributes:
        name: Human-readable name of the data source.
        source: Origin identifier (e.g. SCB register name).
        version: Version string of the data source.
        sha256: Expected SHA-256 hash of the source file.
        col_schema: Mapping of column names to expected dtypes.

    Examples:
        >>> m = Manifest(
        ...     name="test", source="scb", version="1.0",
        ...     sha256="abc", col_schema={"id": "int64"},
        ... )
        >>> m.name
        'test'
    """

    name: str
    source: str
    version: str
    sha256: str
    col_schema: dict[str, str]


def load_manifest(path: pathlib.Path) -> Manifest:
    """Load an ingestion manifest from a TOML file.

    Args:
        path: Path to the manifest TOML file.

    Returns:
        Parsed Manifest instance.

    Raises:
        FileNotFoundError: If the manifest file does not exist.

    Examples:
        >>> import tempfile, pathlib
        >>> p = pathlib.Path(tempfile.mktemp(suffix=".toml"))
        >>> content = 'name="t"\\nsource="s"\\nversion="1"\\nsha256="h"\\n[col_schema]\\nid="int64"'
        >>> _ = p.write_text(content)
        >>> m = load_manifest(p)
        >>> m.name
        't'
    """
    if not path.exists():
        msg = f"Manifest file not found: {path}"
        raise FileNotFoundError(msg)
    with open(path, "rb") as f:
        raw = tomllib.load(f)
    return Manifest(**raw)


def validate_against_schema(
    df: pd.DataFrame,
    manifest: Manifest,
    *,
    strict: bool = True,
) -> list[str] | None:
    """Validate a DataFrame against a manifest schema.

    Args:
        df: DataFrame to validate.
        manifest: Manifest containing the expected schema.
        strict: If True, raise on mismatch; if False, return list of errors.

    Returns:
        None if valid (strict mode) or list of error strings (non-strict mode).

    Raises:
        ValueError: If strict is True and validation fails.

    Examples:
        >>> import pandas as pd
        >>> m = Manifest(name="t", source="s", version="1", sha256="h", col_schema={"a": "int64"})
        >>> df = pd.DataFrame({"a": [1, 2, 3]})
        >>> validate_against_schema(df, m)
    """
    errors: list[str] = []
    for col, expected_dtype in manifest.col_schema.items():
        if col not in df.columns:
            errors.append(f"Missing column: {col}")
        elif str(df[col].dtype) != expected_dtype:
            errors.append(f"Column {col}: expected {expected_dtype}, got {df[col].dtype}")
    if errors and strict:
        msg = f"Schema validation failed for {manifest.name}: {'; '.join(errors)}"
        raise ValueError(msg)
    return errors if errors else None
