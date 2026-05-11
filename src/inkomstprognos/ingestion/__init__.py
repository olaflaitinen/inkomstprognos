"""Data ingestion module for Swedish administrative microdata."""

from __future__ import annotations

from inkomstprognos.ingestion.lisa import read_lisa, synthetic_lisa
from inkomstprognos.ingestion.manifest import Manifest, load_manifest, validate_against_schema
from inkomstprognos.ingestion.tax_registers import read_tax_register, synthetic_tax_register

__all__ = [
    "Manifest",
    "load_manifest",
    "read_lisa",
    "read_tax_register",
    "synthetic_lisa",
    "synthetic_tax_register",
    "validate_against_schema",
]
