"""Tests for deterministic output reproducibility."""

from __future__ import annotations

import numpy as np

from inkomstprognos.ingestion.lisa import synthetic_lisa
from inkomstprognos.ingestion.tax_registers import synthetic_tax_register
from inkomstprognos.seeds import SYNTHETIC_SEED, derive_seed, set_global_seed


class TestSeedDeterminism:
    def test_derive_seed_deterministic(self) -> None:
        s1 = derive_seed(42, namespace="test")
        s2 = derive_seed(42, namespace="test")
        assert s1 == s2

    def test_derive_seed_different_namespace(self) -> None:
        s1 = derive_seed(42, namespace="a")
        s2 = derive_seed(42, namespace="b")
        assert s1 != s2

    def test_set_global_seed_deterministic(self) -> None:
        import random

        set_global_seed(42)
        a = random.random()
        set_global_seed(42)
        b = random.random()
        assert a == b


class TestSyntheticDeterminism:
    def test_lisa_bit_stable(self) -> None:
        df1 = synthetic_lisa(n=500, years=3, seed=SYNTHETIC_SEED)
        df2 = synthetic_lisa(n=500, years=3, seed=SYNTHETIC_SEED)
        assert df1.equals(df2)

    def test_tax_register_bit_stable(self) -> None:
        df1 = synthetic_tax_register(n=500, years=3, seed=SYNTHETIC_SEED)
        df2 = synthetic_tax_register(n=500, years=3, seed=SYNTHETIC_SEED)
        assert df1.equals(df2)

    def test_lisa_float_columns_zero_tolerance(self) -> None:
        df1 = synthetic_lisa(n=100, years=2, seed=SYNTHETIC_SEED)
        df2 = synthetic_lisa(n=100, years=2, seed=SYNTHETIC_SEED)
        for col in ["disp_income", "gross_labour_income", "capital_income", "transfer_income"]:
            np.testing.assert_array_equal(df1[col].to_numpy(), df2[col].to_numpy())

    def test_tax_register_float_columns_zero_tolerance(self) -> None:
        df1 = synthetic_tax_register(n=100, years=2, seed=SYNTHETIC_SEED)
        df2 = synthetic_tax_register(n=100, years=2, seed=SYNTHETIC_SEED)
        for col in ["taxable_earned_income", "final_tax"]:
            np.testing.assert_array_equal(df1[col].to_numpy(), df2[col].to_numpy())
