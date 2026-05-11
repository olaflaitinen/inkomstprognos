# EU compliance

## EUPL-1.2

This project is licensed under the European Union Public Licence, version 1.2
(EUPL-1.2). The licence text is available in the `LICENSE` file and the
`LICENSES/EUPL-1.2.txt` REUSE-stored copy.

## European Commission Open Source Software Strategy 2020-2023

The strategy (C(2020)7149 final) defines six operational principles. This
project addresses each:

### Think Open

Inkomstprognos is designed from the outset as open-source software. All source
code, documentation, and governance artefacts are publicly available on GitHub.
The project uses open standards (Parquet, CycloneDX, REUSE, CFF) throughout.

### Transform

The project demonstrates how open-source research software can transform
public-sector analytical capacity by providing reusable income-forecasting
tools to government agencies and academic institutions.

### Share

All code is shared under the EUPL-1.2, a copyleft licence with broad
compatibility provisions. Synthetic data fixtures are shared under CC0-1.0.
Documentation is shared under CC-BY-4.0.

### Contribute

The project welcomes contributions under the DCO sign-off and Conventional
Commits conventions documented in CONTRIBUTING.md. Upstream contributions to
dependencies are encouraged.

### Secure

The supply chain is hardened via pinned dependencies (uv.lock), CycloneDX SBOM,
sigstore-signed releases, OpenSSF Scorecard, CodeQL analysis, pip-audit, bandit,
and gitleaks.

### Stay in control

The project retains full autonomy over its digital infrastructure by using
standard open-source tooling, avoiding vendor lock-in, and maintaining the
ability to self-host all components.

## Interoperable Europe Act (Regulation (EU) 2024/903)

The repository is contributed to the Interoperable Europe Portal under the EUPL.
The metadata is harmonised with the European Interoperability Framework (EIF).

### EIF interoperability layers

| Layer | How addressed |
|-------|---------------|
| Legal | EUPL-1.2 with documented compatibility matrix |
| Organisational | Open governance model; CONTRIBUTING.md; GOVERNANCE.md |
| Semantic | Standardised variable names; CITATION.cff; .zenodo.json |
| Technical | Python packaging (PEP 517/518/621); Parquet; CycloneDX; REUSE 3.0 |

## REUSE 3.0

This project uses the REUSE Specification version 3.0 via the legacy DEP5
mechanism only. The `.reuse/dep5` file declares copyright and licence for every
file. Per-file SPDX headers are not used.

## FAIR4RS

See `fair4rs.md` for the full FAIR for Research Software self-assessment.

Last updated: 2026-05-11
