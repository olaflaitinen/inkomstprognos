# Reproducibility

## Seeds

| Seed | Value | Usage |
|------|-------|-------|
| SYNTHETIC_SEED | 19960307 | Synthetic fixture generation |
| MODEL_SEED | 20251008 | Default model training seed |
| FOLD_SEED_NAMESPACE | "cross_fitted_encoder" | Cross-fitted target encoding |
| CONFORMAL_CALIB_SEED_NAMESPACE | "conformal_calibration" | Conformal calibration |

All randomness flows through `seeds.derive_seed` with SHA-256 domain separation.

## BLAS thread counts

For deterministic numerical results, set the following environment variables:

```bash
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
```

## Container image

A container image hash will be published with the v1.0.0 release for exact
environment reproduction.

## Hardware variance

Floating-point results may differ across CPU architectures (x86_64 vs. ARM64)
due to different instruction ordering and fused multiply-add behaviour. The
determinism tests in this repository verify bit-stability on the same platform
with the same wheel.

## Deterministic fixture reproduction

```bash
python scripts/make_synthetic_fixture.py
python scripts/make_synthetic_fixture.py --check
```

The `--check` flag verifies that regenerated fixtures are byte-identical to the
committed fixtures.

## Riksarkivet compatibility

Release artefacts are produced in formats compatible with Riksarkivet RA-FS
2009:1 preservation requirements:

- **PDF/A-2u** for reports (via `reporting.pdf_a`)
- **CSV with UTF-8 BOM** for tabular data (via `reporting.tables`)
- **Parquet** for analytical datasets

Last updated: 2026-05-11
