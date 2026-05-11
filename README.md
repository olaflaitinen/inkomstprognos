# Inkomstprognos

**Probabilistic disposable-income forecasting on Swedish administrative microdata**

[![CI](https://github.com/olaflaitinen/inkomstprognos/actions/workflows/ci.yml/badge.svg)](https://github.com/olaflaitinen/inkomstprognos/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/olaflaitinen/inkomstprognos/branch/main/graph/badge.svg)](https://codecov.io/gh/olaflaitinen/inkomstprognos)
[![REUSE](https://api.reuse.software/badge/github.com/olaflaitinen/inkomstprognos)](https://api.reuse.software/info/github.com/olaflaitinen/inkomstprognos)
[![Docs](https://readthedocs.org/projects/inkomstprognos/badge/?version=latest)](https://olaflaitinen.github.io/inkomstprognos)
[![PyPI](https://img.shields.io/pypi/v/inkomstprognos)](https://pypi.org/project/inkomstprognos/)
[![Zenodo](https://zenodo.org/badge/DOI/10.5281/zenodo.PLACEHOLDER.svg)](https://doi.org/10.5281/zenodo.PLACEHOLDER)
[![Licence: EUPL-1.2](https://img.shields.io/badge/licence-EUPL--1.2-blue.svg)](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/olaflaitinen/inkomstprognos/badge)](https://securityscorecards.dev/viewer/?uri=github.com/olaflaitinen/inkomstprognos)

---

**Maintainer:** Dr. Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom Imanov, MD, RA, PhD
(ORCID [0009-0006-5184-0810](https://orcid.org/0009-0006-5184-0810))

**Affiliation:** Department of Economics, Stockholm University (ROR [05f0yaq80](https://ror.org/05f0yaq80)), SE-106 91 Stockholm, Sweden

**Contact:** olaf.laitinen@su.se (institutional) | olaf.laitinen@gmail.com (personal mirror)

**GitHub:** [@olaflaitinen](https://github.com/olaflaitinen)

---

## Abstract

Inkomstprognos is a research-software framework for individual-level and household-level
disposable-income forecasting on Swedish administrative microdata as accessible inside the
Statistiska centralbyran (SCB) secure environment. The methodological toolbox includes
gradient-boosted regression with monotonicity constraints (LightGBM, XGBoost), hierarchical
Bayesian state-space models (NumPyro), Mondrian split-conformal prediction wrappers,
target-encoded categorical features with cross-fitted leakage controls, and rolling-origin
evaluation. Outcomes covered are disposable income, gross labour income, capital income, and
transfer income. Horizons covered are one, three, and five fiscal years. Disaggregation
supports age, gender, region (NUTS-3 Sweden), education (SUN 2020 levels), country of birth,
and household type. The framework also produces calibrated growth-incidence curves and
counterfactual decompositions consistent with the World Inequality Lab Distributional National
Accounts methodology.

This repository is the first module of a twenty-project research portfolio on income, wealth,
taxation, inequality, and intergenerational mobility in Sweden, with an explicit European
Union framing. It is developed at the Department of Economics, Stockholm University.

## Compliance matrix

| Framework | Status | Reference |
|---|---|---|
| EUPL-1.2 | Full compliance | `LICENSE`, `.reuse/dep5` |
| GDPR (Regulation (EU) 2016/679) | No personal data in repository | `docs/gdpr.md` |
| OSOR good practice | Catalogue metadata in `docs/osor.md` | `docs/osor.md` |
| EC OSS Strategy 2020-2023 | Six principles documented | `docs/eu-compliance.md` |
| Interoperable Europe Act (EU) 2024/903 | EIF layers documented | `docs/eu-compliance.md` |
| REUSE 3.0 (DEP5) | `reuse lint` clean | `.reuse/dep5` |
| FAIR4RS | Self-assessment in `docs/fair4rs.md` | `docs/fair4rs.md` |
| Swedish legal basis | OSL, SCB, Etikprovningslagen | `docs/swedish-legal-basis.md` |
| WCAG 2.2 AA | Documentation site conformance | `docs/accessibility.md` |
| NIS2 / Cyber Resilience Act | Supply-chain hardening | `SECURITY.md` |

## EUPL-1.2 compatibility

The EUPL-1.2 appendix lists the following compatible licences for downstream relicensing:

- GNU General Public License (GPL) v. 2, v. 3
- GNU Affero General Public License (AGPL) v. 3
- Open Software License (OSL) v. 2.1, v. 3.0
- Eclipse Public License (EPL) v. 1.0
- CeCILL v. 2.0, v. 2.1
- Mozilla Public Licence (MPL) v. 2
- GNU Lesser General Public Licence (LGPL) v. 2.1, v. 3
- Creative Commons Attribution-ShareAlike v. 3.0 Unported (CC BY-SA 3.0)
- European Union Public Licence (EUPL) v. 1.1, v. 1.2
- Quebec Free and Open-Source Licence - Reciprocity (LiLiQ-R) or Strong Reciprocity (LiLiQ-R+)

## Installation

```bash
# Install uv (if not already installed)
pip install --upgrade uv

# Clone and install
git clone https://github.com/olaflaitinen/inkomstprognos.git
cd inkomstprognos
uv sync --all-extras
```

## Quickstart with synthetic fixtures

```bash
# Generate synthetic data fixtures
uv run python scripts/make_synthetic_fixture.py

# Run a forecast on synthetic data
uv run inkomstprognos train --config examples/synthetic.toml
uv run inkomstprognos predict --config examples/synthetic.toml
uv run inkomstprognos evaluate --config examples/synthetic.toml
```

## Data policy and legal basis

This repository does **not** contain any personal data, real microdata, real tax returns,
real wealth records, or trained model artefacts that depend on real data. All data fixtures
distributed with this repository are deterministic synthetic fixtures generated from a fixed
seed and released under CC0-1.0.

All processing of register microdata is performed exclusively in the secure environment
provided by Statistiska centralbyran (SCB) under Lag (2001:99) om den officiella statistiken
and Offentlighets- och sekretesslagen (2009:400), chapter 24. Access is provided via the
MONA (Microdata Online Access) and SAFE remote-access platforms. No microdata, no derived
person-level outputs, and no model artefacts trained on real microdata ever leave the secure
perimeter.

## Methodology

The framework addresses six research questions covering predictive distributions of disposable
income, forecast accuracy decomposition, European macro covariate effects, model specification
sensitivity, income-shifting margins under the 3:12 rules, and counterfactual policy shocks.
See `docs/methodology.md` for the full treatment.

## Documentation

Full documentation is available at
[olaflaitinen.github.io/inkomstprognos](https://olaflaitinen.github.io/inkomstprognos).

## Citation

If you use this software, please cite it:

**BibTeX:**
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

**APA:**
Laitinen-Fredriksson Lundstrom Imanov, G. O. Y. (2026). *Inkomstprognos: probabilistic
disposable-income forecasting on Swedish administrative microdata* (Version 0.1.0) [Computer
software]. https://github.com/olaflaitinen/inkomstprognos

**Chicago:**
Laitinen-Fredriksson Lundstrom Imanov, Gustav Olaf Yunus. 2026. "Inkomstprognos:
Probabilistic Disposable-Income Forecasting on Swedish Administrative Microdata." Version
0.1.0. https://github.com/olaflaitinen/inkomstprognos.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## Security

See [SECURITY.md](SECURITY.md) for the vulnerability-reporting process and supply-chain
hardening posture.

## Governance

This project follows a lead-maintainer governance model with documented succession planning.
See [GOVERNANCE.md](GOVERNANCE.md) for details.

## Portfolio

Inkomstprognos is part of a twenty-project research portfolio:

- [Inkomstprognos](https://github.com/olaflaitinen/inkomstprognos) (this repository)
- [Formogenhetsanalys](https://github.com/olaflaitinen/formogenhetsanalys)
- [Skatteprogressivitet](https://github.com/olaflaitinen/skatteprogressivitet)
- [Arvsdynamik](https://github.com/olaflaitinen/arvsdynamik)
- [Mobilitetsmodellen](https://github.com/olaflaitinen/mobilitetsmodellen)
- [Inkomstklyftan](https://github.com/olaflaitinen/inkomstklyftan)
- [Pensionsrattvisa](https://github.com/olaflaitinen/pensionsrattvisa)
- [Kapitalinkomst](https://github.com/olaflaitinen/kapitalinkomst)
- [Lonedynamik](https://github.com/olaflaitinen/lonedynamik)
- [Hushallsekonomi](https://github.com/olaflaitinen/hushallsekonomi)
- [Skattereform](https://github.com/olaflaitinen/skattereform)
- [Valfardsmodellen](https://github.com/olaflaitinen/valfardsmodellen)
- [Generationsskifte](https://github.com/olaflaitinen/generationsskifte)
- [Demografiprognos](https://github.com/olaflaitinen/demografiprognos)
- [Mikrosimulering](https://github.com/olaflaitinen/mikrosimulering)
- [Toppinkomstandelen](https://github.com/olaflaitinen/toppinkomstandelen)
- [Bolagsskatteanalys](https://github.com/olaflaitinen/bolagsskatteanalys)
- [Skatteflyktsdetektor](https://github.com/olaflaitinen/skatteflyktsdetektor)
- [Formansanalys](https://github.com/olaflaitinen/formansanalys)
- [Omfordelningsmodellen](https://github.com/olaflaitinen/omfordelningsmodellen)

## Licence

This project is licensed under the [European Union Public Licence, version 1.2 (EUPL-1.2)](LICENSE).

Copyright 2025-2026 Dr. Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom Imanov, MD, RA, PhD
(ORCID 0009-0006-5184-0810), Department of Economics, Stockholm University.

**Note:** Python 3.14+ users: this package targets Python >=3.11,<3.13. If you are running
Python 3.13 or later, please use `uv` with `--python 3.12` to create a compatible virtual
environment.
