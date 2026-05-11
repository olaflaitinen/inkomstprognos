"""Tests for the reporting module."""

from __future__ import annotations

import pathlib

import matplotlib
import numpy as np
import pandas as pd
import pytest

matplotlib.use("Agg")

from inkomstprognos.reporting.figures import FigureBuilder
from inkomstprognos.reporting.pdf_a import render_pdf_a
from inkomstprognos.reporting.tables import to_csv_with_bom, to_parquet, to_pdf_a_table


class TestFigureBuilder:
    def test_fan_chart(self, tmp_path: pathlib.Path) -> None:
        fb = FigureBuilder(dpi=72)
        years = np.array([2020, 2021, 2022])
        median = np.array([100.0, 110.0, 120.0])
        intervals = [(np.array([80.0, 90.0, 100.0]), np.array([120.0, 130.0, 140.0]))]
        out = tmp_path / "fan.png"
        fig = fb.forecast_fan_chart(years, median, intervals, output=out)
        assert fig is not None
        assert out.exists()

    def test_calibration_plot(self, tmp_path: pathlib.Path) -> None:
        fb = FigureBuilder(dpi=72)
        nominal = np.linspace(0.1, 0.9, 5)
        observed = np.linspace(0.1, 0.9, 5)
        out = tmp_path / "calib.png"
        fig = fb.calibration_plot(nominal, observed, output=out)
        assert fig is not None
        assert out.exists()


class TestTables:
    def test_csv_with_bom(self, tmp_path: pathlib.Path) -> None:
        df = pd.DataFrame({"a": [1, 2], "b": [3.0, 4.0]})
        p = tmp_path / "out.csv"
        to_csv_with_bom(df, p)
        raw = p.read_bytes()
        assert raw[:3] == b"\xef\xbb\xbf"

    def test_to_parquet(self, tmp_path: pathlib.Path) -> None:
        df = pd.DataFrame({"a": [1, 2]})
        p = tmp_path / "out.parquet"
        to_parquet(df, p)
        assert p.exists()
        result = pd.read_parquet(p)
        assert len(result) == 2

    def test_to_pdf_a_table(self, tmp_path: pathlib.Path) -> None:
        df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
        p = tmp_path / "table.pdf"
        to_pdf_a_table(df, p)
        assert p.exists()
        assert p.stat().st_size > 0


class TestPdfA:
    def test_render(self, tmp_path: pathlib.Path) -> None:
        p = tmp_path / "report.pdf"
        render_pdf_a("Test content", p, title="Test")
        assert p.exists()
        assert p.stat().st_size > 0

    def test_empty_content_raises(self, tmp_path: pathlib.Path) -> None:
        p = tmp_path / "empty.pdf"
        with pytest.raises(ValueError, match="non-empty"):
            render_pdf_a("", p)
