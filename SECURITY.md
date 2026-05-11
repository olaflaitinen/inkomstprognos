# Security Policy

## Reporting vulnerabilities

Please report security vulnerabilities to:

- **Primary (institutional):** olaf.laitinen@su.se
- **Fallback (personal mirror):** olaf.laitinen@gmail.com

PGP key fingerprint: (to be published on first stable release)

For encrypted reports, request the PGP public key via the institutional email.

## Coordinated disclosure

- We follow a 90-day coordinated disclosure timeline.
- Extensions may be negotiated for complex issues.
- We will acknowledge receipt within 48 hours.
- We will provide a timeline for remediation within 7 days.

## Secure development lifecycle

This project adopts a supply-chain hardening posture aligned with the NIS2
Directive (Directive (EU) 2022/2555) and the EU Cyber Resilience Act:

- **Pinned dependencies:** All dependencies are locked via `uv.lock` with
  exact version pins and integrity hashes.
- **CycloneDX SBOM:** A Software Bill of Materials is generated for every
  release in CycloneDX 1.5 JSON format.
- **Sigstore signatures:** Release artefacts are signed using sigstore via
  GitHub OIDC trusted publishing.
- **OpenSSF Scorecard:** Weekly automated security scoring via the OpenSSF
  Scorecard GitHub Action.
- **CodeQL analysis:** Weekly static analysis of the Python codebase via
  GitHub CodeQL.
- **pip-audit:** Dependency vulnerability scanning gates every CI run.
- **bandit:** Static application security testing gates every CI run.
- **gitleaks:** Pre-commit hook and CI check for secrets and PII detection.

## Supply-chain attestation

Release artefacts include:

- Signed wheel and sdist via sigstore
- CycloneDX SBOM attached to the GitHub Release
- Provenance attestation via GitHub Actions OIDC

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |
