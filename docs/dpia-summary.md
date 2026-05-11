# Data Protection Impact Assessment summary

## Scope

This DPIA covers the processing of Swedish administrative microdata (LISA, IoT,
FAD) for income-forecasting research within the SCB secure environment.

## Necessity and proportionality

The processing is necessary to answer the six research questions specified in
the project scope. Individual-level panel data is required because aggregate
statistics cannot capture heterogeneity across the income distribution.

## Risk analysis

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Re-identification from outputs | Low | High | Statistical disclosure control by SCB |
| Unauthorised access to microdata | Very low | High | SCB MONA/SAFE access controls |
| Model memorisation of individuals | Low | Medium | No trained models leave the secure perimeter |
| Data breach during transfer | Very low | High | No data transfer; processing in-situ |

## Mitigations

- All processing occurs within the SCB secure environment.
- No individual-level data leaves the secure perimeter.
- Outputs are reviewed by SCB for disclosure risk before release.
- Synthetic data is used for all development and testing outside the
  secure environment.
- The repository ships no personal data of any kind.

## Residual risk

After mitigations, the residual risk of harm to data subjects is assessed as
very low. The SCB secure environment provides robust technical and
organisational safeguards.

## Sign-off

This DPIA was prepared by the lead maintainer and reviewed in accordance with
the Department of Economics data governance procedures at Stockholm University.

Last updated: 2026-05-11
