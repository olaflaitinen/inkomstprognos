# Inkomstprognos

Probabilistic disposable-income forecasting on Swedish administrative microdata.

## Overview

Inkomstprognos is a research-software framework for individual-level and
household-level disposable-income forecasting on Swedish administrative microdata
as accessible inside the Statistiska centralbyran (SCB) secure environment.

## Key features

- **Gradient-boosted regression** with monotonicity constraints (LightGBM, XGBoost)
- **Hierarchical Bayesian state-space models** (NumPyro)
- **Mondrian split-conformal prediction** for calibrated prediction intervals
- **Cross-fitted target encoders** with leakage control
- **Rolling-origin evaluation** with proper scoring rules
- **Stacking ensemble** with NNLS meta-learner

## Quick links

- [Methodology](methodology.md)
- [API Reference](api.md)
- [Data](data.md)
- [Reproducibility](reproducibility.md)
- [EU Compliance](eu-compliance.md)

## Licence

Licensed under [EUPL-1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).

Last updated: 2026-05-11
