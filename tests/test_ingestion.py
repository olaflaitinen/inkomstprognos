"""Tests for the ingestion module."""

from __future__ import annotations

import pathlib
import tempfile

import pandas as pd
import pytest

from inkomstprognos.ingestion.lisa import LISA_COLUMNS, read_lisa, synthetic_lisa
from inkomstprognos.ingestion.manifest import Manifest, load_manifest, validate_against_schema
from inkomstprognos.ingestion.tax_registers import (
    TAX_COLUMNS,
    read_tax_register,
    synthetic_tax_register,
)


class TestSyntheticLisa:
    def test_shape(self) -> None:
        df = synthetic_lisa(n=100, years=2, seed=42)
        assert df.shape[0] == 200
        assert df.shape[1] == len(LISA_COLUMNS)

    def test_columns(self) -> None:
        df = synthetic_lisa(n=50, years=1, seed=42)
        assert set(df.columns) == set(LISA_COLUMNS)

    def test_deterministic(self) -> None:
        df1 = synthetic_lisa(n=100, years=2, seed=42)
        df2 = synthetic_lisa(n=100, years=2, seed=42)
        assert df1.equals(df2)

    def test_different_seeds(self) -> None:
        df1 = synthetic_lisa(n=100, years=1, seed=1)
        df2 = synthetic_lisa(n=100, years=1, seed=2)
        assert not df1.equals(df2)

    def test_invalid_n(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            synthetic_lisa(n=0)

    def test_invalid_years(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            synthetic_lisa(n=10, years=0)

    def test_non_negative_income(self) -> None:
        df = synthetic_lisa(n=500, years=1, seed=42)
        for col in ["disp_income", "gross_labour_income", "capital_income", "transfer_income"]:
            assert (df[col] >= 0).all()


class TestReadLisa:
    def test_roundtrip(self) -> None:
        df = synthetic_lisa(n=50, years=1, seed=42)
        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as f:
            p = pathlib.Path(f.name)
        df.write_parquet(p)
        result = read_lisa(p)
        assert result.equals(df)
        p.unlink()

    def test_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError):
            read_lisa(pathlib.Path("nonexistent.parquet"))

    def test_column_subset(self) -> None:
        df = synthetic_lisa(n=50, years=1, seed=42)
        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as f:
            p = pathlib.Path(f.name)
        df.write_parquet(p)
        result = read_lisa(p, columns=["person_id", "year"])
        assert set(result.columns) == {"person_id", "year"}
        p.unlink()


class TestSyntheticTaxRegister:
    def test_shape(self) -> None:
        df = synthetic_tax_register(n=100, years=2, seed=42)
        assert df.shape[0] == 200
        assert df.shape[1] == len(TAX_COLUMNS)

    def test_deterministic(self) -> None:
        df1 = synthetic_tax_register(n=100, years=2, seed=42)
        df2 = synthetic_tax_register(n=100, years=2, seed=42)
        assert df1.equals(df2)

    def test_invalid_n(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            synthetic_tax_register(n=0)


class TestReadTaxRegister:
    def test_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError):
            read_tax_register(pathlib.Path("nonexistent.parquet"))


class TestManifest:
    def test_load_manifest(self, tmp_path: pathlib.Path) -> None:
        content = (
            'name="test"\nsource="scb"\nversion="1"\nsha256="abc"\n\n[col_schema]\nid="int64"\n'
        )
        p = tmp_path / "manifest.toml"
        p.write_text(content, encoding="utf-8")
        m = load_manifest(p)
        assert m.name == "test"
        assert m.col_schema == {"id": "int64"}

    def test_manifest_not_found(self) -> None:
        with pytest.raises(FileNotFoundError):
            load_manifest(pathlib.Path("nonexistent.toml"))

    def test_validate_success(self) -> None:
        m = Manifest(name="t", source="s", version="1", sha256="h", col_schema={"a": "int64"})
        df = pd.DataFrame({"a": pd.array([1, 2, 3], dtype="int64")})
        result = validate_against_schema(df, m)
        assert result is None

    def test_validate_missing_column(self) -> None:
        m = Manifest(name="t", source="s", version="1", sha256="h", col_schema={"missing": "int64"})
        df = pd.DataFrame({"a": [1]})
        with pytest.raises(ValueError, match="Missing column"):
            validate_against_schema(df, m, strict=True)

    def test_validate_non_strict(self) -> None:
        m = Manifest(name="t", source="s", version="1", sha256="h", col_schema={"missing": "int64"})
        df = pd.DataFrame({"a": [1]})
        errors = validate_against_schema(df, m, strict=False)
        assert errors is not None
        assert len(errors) > 0
