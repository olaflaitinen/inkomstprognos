# FAIR4RS self-assessment

## Findable

| Criterion | Status | Evidence |
|-----------|--------|----------|
| F1: Software has a globally unique and persistent identifier | Partial | Zenodo DOI to be minted on first release |
| F2: Software is described with rich metadata | Yes | CITATION.cff, .zenodo.json, pyproject.toml |
| F3: Metadata clearly includes the identifier of the software | Yes | Repository URL in all metadata files |
| F4: Metadata is offered in a searchable resource | Yes | PyPI, Zenodo, GitHub |

## Accessible

| Criterion | Status | Evidence |
|-----------|--------|----------|
| A1: Software is retrievable by its identifier using a standard protocol | Yes | HTTPS via GitHub and PyPI |
| A2: Metadata is accessible even when the software is no longer available | Yes | Zenodo preserves metadata independently |

## Interoperable

| Criterion | Status | Evidence |
|-----------|--------|----------|
| I1: Software reads, writes, and exchanges data in a format that follows community standards | Yes | Parquet, CSV, JSON |
| I2: Software includes qualified references to other objects | Yes | CITATION.cff references, .zenodo.json related_identifiers |
| I3: Software meets domain-relevant community standards | Yes | scikit-learn API; REUSE 3.0; Conventional Commits |

## Reusable

| Criterion | Status | Evidence |
|-----------|--------|----------|
| R1: Software is described with a plurality of accurate and relevant attributes | Yes | Comprehensive metadata in pyproject.toml, CITATION.cff |
| R2: Software includes a clear and accessible licence | Yes | EUPL-1.2 in LICENSE and .reuse/dep5 |
| R3: Software meets domain-relevant community standards | Yes | Google-style docstrings; type hints; 90%+ coverage |

Last updated: 2026-05-11
