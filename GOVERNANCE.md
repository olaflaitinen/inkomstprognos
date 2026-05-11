# Governance

## Model

Inkomstprognos follows a lead-maintainer governance model. The lead maintainer
has final decision-making authority on technical and strategic matters.

## Lead maintainer

Dr. Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom Imanov, MD, RA, PhD
(ORCID [0009-0006-5184-0810](https://orcid.org/0009-0006-5184-0810)),
Research Assistant, Department of Economics, Stockholm University.

## Decision process

- **Lazy consensus:** Proposals are accepted if no objections are raised within
  a two-week comment window on the relevant GitHub issue or pull request.
- **Major changes:** Changes to the public API, licensing, governance model, or
  dependency policy require an explicit approval from the lead maintainer.
- **Minor changes:** Bug fixes, documentation improvements, and non-breaking
  enhancements follow the standard pull-request review process.

## Succession plan

If the lead maintainer becomes unavailable for more than 90 days:

1. The Department of Economics, Stockholm University, may appoint a successor.
2. If no successor is appointed, the project is placed in maintenance-only mode.
3. The community may fork under the EUPL-1.2 terms at any time.

## Transparency

- All decisions are documented in GitHub issues and pull requests.
- The project roadmap is maintained as a public GitHub project board.
- Financial conflicts of interest must be disclosed in pull requests.

## Institutional ties

This project is developed at the Department of Economics, Stockholm University
(ROR [05f0yaq80](https://ror.org/05f0yaq80)). The governance model respects
the institutional policies of Stockholm University while maintaining open-source
community participation.

## Dependency compatibility

All third-party dependencies must be EUPL-1.2 compatible per the EUPL appendix.
The following licence families are compatible: MIT, BSD-2-Clause, BSD-3-Clause,
Apache-2.0, ISC, PSF-2.0, GPL-2.0, GPL-3.0, AGPL-3.0, LGPL-2.1, LGPL-3.0,
MPL-2.0, EPL-1.0, OSL-3.0, CeCILL-2.1. Dependencies under incompatible
licences are rejected during code review.
