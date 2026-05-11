"""Feature engineering module."""

from __future__ import annotations

from inkomstprognos.features.cross_fitted_encoders import CrossFittedTargetEncoder
from inkomstprognos.features.lifecycle import compute_age_cohort, equivalise
from inkomstprognos.features.macro_join import join_macro

__all__ = [
    "CrossFittedTargetEncoder",
    "compute_age_cohort",
    "equivalise",
    "join_macro",
]
