"""Reporting module for figures, tables, and PDF/A outputs."""

from __future__ import annotations

from inkomstprognos.reporting.figures import FigureBuilder
from inkomstprognos.reporting.pdf_a import render_pdf_a
from inkomstprognos.reporting.tables import to_csv_with_bom, to_parquet, to_pdf_a_table

__all__ = [
    "FigureBuilder",
    "render_pdf_a",
    "to_csv_with_bom",
    "to_parquet",
    "to_pdf_a_table",
]
