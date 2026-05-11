# Methodology

## Overview

Inkomstprognos implements a research-software framework for probabilistic
disposable-income forecasting. This page covers the core modelling approaches,
evaluation protocol, and known limitations.

## Monotonic gradient-boosted models

The `MonotonicGBM` class wraps LightGBM and XGBoost with monotonicity
constraints. Monotonicity ensures that predictions respect known economic
relationships (e.g. higher education correlates with higher income, all else
equal).

Hyperparameters include the number of boosting rounds, learning rate, maximum
tree depth, and per-feature monotonicity directions.

## Hierarchical Bayesian state-space model

The `HierarchicalStateSpace` class implements a local-level + trend + AR(1)
macro-effect model using NumPyro NUTS HMC. The model decomposes income
trajectories into a persistent level, a time-varying trend, and an
autoregressive macro-covariate effect.

Posterior inference uses No-U-Turn Sampling (NUTS), a variant of Hamiltonian
Monte Carlo.

## Conformal prediction

Split conformal and Mondrian split-conformal wrappers produce prediction
intervals with finite-sample coverage guarantees. The Mondrian variant
calibrates per stratum (e.g. income decile), yielding heterogeneous interval
widths that reflect differential predictability across the distribution.

## Stacking ensemble

The `StackingEnsemble` class combines base learners via cross-fitted predictions
and a non-negative least-squares (NNLS) meta-learner. This approach inherits
the strengths of individual models while controlling overfitting through the
NNLS constraint.

## Evaluation protocol

Rolling-origin cross-validation respects the temporal ordering of panel data.
The framework evaluates forecasts using:

- **CRPS** (Continuous Ranked Probability Score): a proper scoring rule for
  probabilistic forecasts.
- **Pinball loss**: quantile-specific loss for interval evaluation.
- **MAE, RMSE, MAPE**: standard point-forecast metrics.
- **Coverage and interval width**: calibration diagnostics for prediction
  intervals.

## Identification caveats

- Selection on observables only; no causal identification claimed.
- Forecast distributions are conditional on the policy regime in effect.
- Income-shifting margins under the 3:12 rules may distort the
  labour-versus-capital decomposition at the top of the distribution.

## Limitations

- Real microdata is not distributed; all shipped fixtures are synthetic.
- The state-space model assumes stationarity of the AR(1) macro effect.
- Conformal intervals assume exchangeability within strata.
- Cross-platform floating-point differences may affect exact reproducibility.

Last updated: 2026-05-11
