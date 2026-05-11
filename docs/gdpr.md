# GDPR compliance

## Repository scope

This repository does **not** contain any personal data as defined by Article 4(1)
of Regulation (EU) 2016/679 (GDPR). All data fixtures are synthetic.

## Lawful basis for linked microdata processing

When the framework is applied to real microdata inside the SCB secure environment,
the following lawful bases apply:

### Article 6(1)(e) - Public task

Processing is necessary for the performance of a task carried out in the public
interest, specifically academic research at a public university (Stockholm
University).

### Article 9(2)(j) - Research purposes

Processing of special categories of data is permitted for scientific research
purposes, subject to appropriate safeguards under Article 89(1).

## Data protection principles

### Data minimisation (Article 5(1)(c))

Only variables necessary for the specified research questions are accessed.
Feature selection is documented in the pipeline configuration.

### Storage limitation (Article 5(1)(e))

No personal data is stored outside the SCB secure environment. Intermediate
results are deleted after the analysis session.

### Accuracy (Article 5(1)(d))

Administrative register data is maintained by Swedish government agencies with
established quality-assurance processes.

## Security of processing (Article 32)

- All processing occurs in SCB's secure environment (MONA/SAFE).
- Access is restricted to authorised researchers.
- Outputs are subject to statistical disclosure control.
- No individual-level data leaves the secure perimeter.

## DPIA threshold analysis (Article 35)

See `dpia-summary.md` for the Data Protection Impact Assessment summary.

## Research safeguards (Article 89)

- Pseudonymisation of all individual identifiers within the secure environment.
- Access controls limiting data availability to approved researchers.
- Statistical disclosure control on all exported aggregates.
- Ethical review where required under Etikprovningslagen (2003:460).

## Data subject rights

Under the public-task basis (Article 6(1)(e)), data subject rights are balanced
against the public interest in research. The right to erasure (Article 17) is
limited by Article 17(3)(d) for scientific research purposes. Data subjects may
exercise their rights by contacting SCB directly.

Last updated: 2026-05-11
