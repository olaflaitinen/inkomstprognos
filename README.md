<div align="center">

# Inkomstprognos

### Probabilistic Disposable-Income Forecasting on Swedish Administrative Microdata

<br>

[![CI](https://github.com/olaflaitinen/inkomstprognos/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/olaflaitinen/inkomstprognos/actions/workflows/ci.yml)
[![CodeQL](https://github.com/olaflaitinen/inkomstprognos/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/olaflaitinen/inkomstprognos/actions/workflows/codeql.yml)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/olaflaitinen/inkomstprognos/badge)](https://securityscorecards.dev/viewer/?uri=github.com/olaflaitinen/inkomstprognos)
[![REUSE](https://api.reuse.software/badge/github.com/olaflaitinen/inkomstprognos)](https://api.reuse.software/info/github.com/olaflaitinen/inkomstprognos)
<br>
[![Licence: EUPL-1.2](https://img.shields.io/badge/licence-EUPL--1.2-blue.svg)](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)
[![Python 3.11 | 3.12](https://img.shields.io/badge/python-3.11%20%7C%203.12-3776ab.svg?logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/package%20manager-uv-de5fe9.svg?logo=uv&logoColor=white)](https://docs.astral.sh/uv/)
[![FAIR4RS](https://img.shields.io/badge/FAIR4RS-self--assessed-2ea44f.svg)](docs/fair4rs.md)

<br>

*Department of Economics, Stockholm University*

</div>

---

<table>
<tr>
<td><strong>Maintainer</strong></td>
<td>Dr. Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom Imanov, MD, RA, PhD</td>
</tr>
<tr>
<td><strong>ORCID</strong></td>
<td><a href="https://orcid.org/0009-0006-5184-0810">0009-0006-5184-0810</a></td>
</tr>
<tr>
<td><strong>Affiliation</strong></td>
<td>Department of Economics, Stockholm University (ROR <a href="https://ror.org/05f0yaq80">05f0yaq80</a>), SE-106 91 Stockholm, Sweden</td>
</tr>
<tr>
<td><strong>Contact</strong></td>
<td><a href="mailto:olaf.laitinen@su.se">olaf.laitinen@su.se</a> (institutional) | <a href="mailto:olaf.laitinen@gmail.com">olaf.laitinen@gmail.com</a> (personal)</td>
</tr>
<tr>
<td><strong>Repository</strong></td>
<td><a href="https://github.com/olaflaitinen/inkomstprognos">github.com/olaflaitinen/inkomstprognos</a></td>
</tr>
</table>

---

## 1. Abstract

**Inkomstprognos** is a research-software framework for individual-level and
household-level disposable-income forecasting on Swedish administrative microdata
as accessible inside the Statistiska centralbyran (SCB) secure environment.

The methodological toolbox comprises:

- **Gradient-boosted regression** with monotonicity constraints (LightGBM, XGBoost)
- **Hierarchical Bayesian state-space models** (NumPyro / JAX)
- **Mondrian split-conformal prediction** wrappers for calibrated prediction intervals
- **Cross-fitted target encoding** with leakage controls for categorical features
- **Stacking ensemble** with non-negative least-squares meta-learner
- **Rolling-origin evaluation** with proper scoring rules (CRPS, pinball loss, MAPE)

**Outcomes:** disposable income, gross labour income, capital income, transfer income.
**Horizons:** one, three, and five fiscal years.
**Disaggregation:** age, gender, region (NUTS-3), education (SUN 2020), country of
birth, household type.

The framework also produces calibrated growth-incidence curves and counterfactual
decompositions consistent with the World Inequality Lab Distributional National
Accounts methodology.

> This repository is the first module of a twenty-project research portfolio on
> income, wealth, taxation, inequality, and intergenerational mobility in Sweden,
> developed at the Department of Economics, Stockholm University, with an explicit
> European Union regulatory and open-source framing.

## 2. Regulatory and standards compliance

| Framework | Status | Evidence |
|:---|:---|:---|
| **EUPL-1.2** | Full compliance | [`LICENSE`](LICENSE), [`.reuse/dep5`](.reuse/dep5) |
| **REUSE 3.0** (DEP5) | `reuse lint` clean | [`.reuse/dep5`](.reuse/dep5) |
| **GDPR** (Regulation (EU) 2016/679) | No personal data in repository | [`docs/gdpr.md`](docs/gdpr.md) |
| **DPIA** (Article 35) | Threshold analysis documented | [`docs/dpia-summary.md`](docs/dpia-summary.md) |
| **EC OSS Strategy** 2020--2023 | Six principles documented | [`docs/eu-compliance.md`](docs/eu-compliance.md) |
| **Interoperable Europe Act** (EU) 2024/903 | EIF layers documented | [`docs/eu-compliance.md`](docs/eu-compliance.md) |
| **OSOR** good practice | Catalogue metadata | [`docs/osor.md`](docs/osor.md) |
| **FAIR4RS** | Self-assessment | [`docs/fair4rs.md`](docs/fair4rs.md) |
| **Swedish legal basis** | OSL, SCB, Etikprovningslagen | [`docs/swedish-legal-basis.md`](docs/swedish-legal-basis.md) |
| **WCAG 2.2 AA** | Documentation site conformance | [`docs/accessibility.md`](docs/accessibility.md) |
| **NIS2 / Cyber Resilience Act** | Supply-chain hardening | [`SECURITY.md`](SECURITY.md) |
| **OpenSSF Scorecard** | Automated weekly assessment | [Scorecard viewer](https://securityscorecards.dev/viewer/?uri=github.com/olaflaitinen/inkomstprognos) |

## 3. Architecture overview

```
inkomstprognos/
  src/inkomstprognos/
    ingestion/          SCB register loaders, manifest validation
    features/           lifecycle, macro join, cross-fitted encoders
    models/             GBM, state-space, conformal, stacking ensemble
    pipelines/          DAG execution engine, receipt generation
    evaluation/         metrics, calibration diagnostics, rolling origin
    reporting/          figures, tables (CSV/Parquet), PDF/A rendering
    cli.py              Typer CLI with subcommands
    config.py           Pydantic configuration model
    seeds.py            SHA-256 domain-separated seed derivation
```

## 4. Installation

**Prerequisites:** Python 3.11 or 3.12, [uv](https://docs.astral.sh/uv/) package manager.

```bash
git clone https://github.com/olaflaitinen/inkomstprognos.git
cd inkomstprognos
uv sync --all-extras
```

To verify the installation:

```bash
uv run inkomstprognos --version
uv run pytest tests -q --ignore=tests/test_models_state_space.py
```

## 5. Quickstart with synthetic data

All distributed data fixtures are **deterministic synthetic data** generated from
`SYNTHETIC_SEED = 19960307` and released under CC0-1.0. No real microdata is
included in this repository.

```bash
# Generate or verify synthetic fixtures
uv run python scripts/make_synthetic_fixture.py
uv run python scripts/make_synthetic_fixture.py --check

# Run a forecast pipeline on synthetic data
uv run inkomstprognos train --config examples/synthetic.toml
uv run inkomstprognos predict --config examples/synthetic.toml
uv run inkomstprognos evaluate --config examples/synthetic.toml
uv run inkomstprognos report --config examples/synthetic.toml
```

## 6. Data policy and legal basis

This repository does **not** contain any personal data, real microdata, real tax
returns, real wealth records, or trained model artefacts that depend on real data.

All processing of register microdata is performed exclusively in the secure
environment provided by Statistiska centralbyran (SCB) under:

- **Lag (2001:99)** om den officiella statistiken
- **Offentlighets- och sekretesslagen (2009:400)**, chapter 24
- **Etikprovningslagen (2003:460)**

Access is provided via the MONA (Microdata Online Access) and SAFE remote-access
platforms. No microdata, no derived person-level outputs, and no model artefacts
trained on real microdata ever leave the secure perimeter.

## 7. Methodology

The framework addresses six research questions:

1. Predictive distributions of individual disposable income
2. Forecast accuracy decomposition by demographic strata
3. European macro covariate effects on Swedish household income
4. Model specification sensitivity and ensemble robustness
5. Income-shifting margins under the 3:12 rules for closely held firms
6. Counterfactual policy shocks and distributional effects

See [`docs/methodology.md`](docs/methodology.md) for the full methodological treatment.

## 8. Documentation

Full documentation is available at
**[olaflaitinen.github.io/inkomstprognos](https://olaflaitinen.github.io/inkomstprognos)**.

| Document | Description |
|:---|:---|
| [`docs/methodology.md`](docs/methodology.md) | Modelling approaches and evaluation protocol |
| [`docs/api.md`](docs/api.md) | API reference (auto-generated from docstrings) |
| [`docs/data.md`](docs/data.md) | Data sources and synthetic fixture specification |
| [`docs/reproducibility.md`](docs/reproducibility.md) | Seeds, BLAS threading, container images |
| [`docs/glossary.md`](docs/glossary.md) | Swedish administrative and statistical terminology |
| [`docs/deviations.md`](docs/deviations.md) | Documented deviations from build specification |

## 9. Quality assurance

| Check | Tool | CI Job |
|:---|:---|:---|
| Linting and formatting | Ruff | `ci / lint` |
| Static type checking | mypy --strict | `ci / typecheck` |
| Unit and integration tests | pytest (108 tests) | `ci / test` |
| Licence compliance | REUSE 3.0 | `ci / reuse` |
| Dependency audit | pip-audit, Bandit | `ci / security` |
| Lockfile integrity | `uv lock --check` | `ci / lockfile` |
| Documentation build | MkDocs Material | `ci / docs` |
| Supply-chain security | OpenSSF Scorecard | `scorecard / analysis` |
| Code scanning | GitHub CodeQL | `codeql / analyze` |

## 10. Citation

If you use this software in academic work, please cite it using one of the
following formats. Additional formats are available in
[`docs/citation.md`](docs/citation.md) and [`CITATION.cff`](CITATION.cff).

```bibtex
@software{laitinen_fredriksson_2026_inkomstprognos,
  author       = {Laitinen-Fredriksson Lundstrom Imanov, Gustav Olaf Yunus},
  title        = {Inkomstprognos: probabilistic disposable-income forecasting
                  on Swedish administrative microdata},
  year         = {2026},
  version      = {0.1.0},
  publisher    = {Zenodo},
  licence      = {EUPL-1.2},
  url          = {https://github.com/olaflaitinen/inkomstprognos}
}
```

> Laitinen-Fredriksson Lundstrom Imanov, G. O. Y. (2026). *Inkomstprognos:
> probabilistic disposable-income forecasting on Swedish administrative
> microdata* (Version 0.1.0) [Computer software].
> https://github.com/olaflaitinen/inkomstprognos

## 11. EUPL-1.2 compatibility

The EUPL-1.2 appendix enumerates the following compatible licences for
downstream relicensing:

GPL v.2, GPL v.3, AGPL v.3, OSL v.2.1, OSL v.3.0, EPL v.1.0, CeCILL v.2.0,
CeCILL v.2.1, MPL v.2, LGPL v.2.1, LGPL v.3, CC BY-SA 3.0 Unported,
EUPL v.1.1, EUPL v.1.2, LiLiQ-R, LiLiQ-R+.

All third-party dependencies use licences compatible with EUPL-1.2. The full
dependency licence audit is documented in [`docs/governance.md`](docs/governance.md).

## 12. Contributing, security, and governance

| Topic | Document |
|:---|:---|
| Contribution guidelines | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Code of conduct | [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) |
| Vulnerability reporting | [`SECURITY.md`](SECURITY.md) |
| Governance model | [`GOVERNANCE.md`](GOVERNANCE.md) |
| Maintainer roster | [`MAINTAINERS.md`](MAINTAINERS.md) |
| Changelog | [`CHANGELOG.md`](CHANGELOG.md) |

## 13. Research portfolio

Inkomstprognos is the first module of a twenty-project research portfolio on
income, wealth, taxation, inequality, and intergenerational mobility in Sweden.

| # | Repository | Domain |
|--:|:---|:---|
| 1 | **[inkomstprognos](https://github.com/olaflaitinen/inkomstprognos)** | Income forecasting (this repository) |
| 2 | [formogenhetsanalys](https://github.com/olaflaitinen/formogenhetsanalys) | Wealth analysis |
| 3 | [skatteprogressivitet](https://github.com/olaflaitinen/skatteprogressivitet) | Tax progressivity |
| 4 | [arvsdynamik](https://github.com/olaflaitinen/arvsdynamik) | Inheritance dynamics |
| 5 | [mobilitetsmodellen](https://github.com/olaflaitinen/mobilitetsmodellen) | Income mobility |
| 6 | [inkomstklyftan](https://github.com/olaflaitinen/inkomstklyftan) | Income inequality |
| 7 | [pensionsrattvisa](https://github.com/olaflaitinen/pensionsrattvisa) | Pension equity |
| 8 | [kapitalinkomst](https://github.com/olaflaitinen/kapitalinkomst) | Capital income |
| 9 | [lonedynamik](https://github.com/olaflaitinen/lonedynamik) | Wage dynamics |
| 10 | [hushallsekonomi](https://github.com/olaflaitinen/hushallsekonomi) | Household economics |
| 11 | [skattereform](https://github.com/olaflaitinen/skattereform) | Tax reform simulation |
| 12 | [valfardsmodellen](https://github.com/olaflaitinen/valfardsmodellen) | Welfare modelling |
| 13 | [generationsskifte](https://github.com/olaflaitinen/generationsskifte) | Generational transfers |
| 14 | [demografiprognos](https://github.com/olaflaitinen/demografiprognos) | Demographic forecasting |
| 15 | [mikrosimulering](https://github.com/olaflaitinen/mikrosimulering) | Microsimulation |
| 16 | [toppinkomstandelen](https://github.com/olaflaitinen/toppinkomstandelen) | Top income shares |
| 17 | [bolagsskatteanalys](https://github.com/olaflaitinen/bolagsskatteanalys) | Corporate tax analysis |
| 18 | [skatteflyktsdetektor](https://github.com/olaflaitinen/skatteflyktsdetektor) | Tax evasion detection |
| 19 | [formansanalys](https://github.com/olaflaitinen/formansanalys) | Fringe benefit analysis |
| 20 | [omfordelningsmodellen](https://github.com/olaflaitinen/omfordelningsmodellen) | Redistribution modelling |

## 14. Licence

This project is licensed under the
[European Union Public Licence, version 1.2 (EUPL-1.2)](LICENSE).

Copyright 2025--2026 Dr. Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom
Imanov, MD, RA, PhD (ORCID [0009-0006-5184-0810](https://orcid.org/0009-0006-5184-0810)),
Department of Economics, Stockholm University.

---

<div align="center">
<sub>
Built with Python, uv, Polars, LightGBM, NumPyro, and MkDocs Material.
Licensed under EUPL-1.2. REUSE 3.0 compliant.
</sub>
</div>
