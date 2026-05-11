# Contributing to Inkomstprognos

Thank you for your interest in contributing to Inkomstprognos. This document
describes the guidelines and procedures for contributing.

## Developer Certificate of Origin

All commits must include a DCO sign-off line:

```
Signed-off-by: Your Name <your.email@example.com>
```

Use `git commit -s` to add this automatically.

## Commit conventions

This project follows [Conventional Commits 1.0.0](https://www.conventionalcommits.org/).

Commit messages must follow the format:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
Signed-off-by: Your Name <your.email@example.com>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`,
`ci`, `chore`, `revert`.

## Signed commits

All commits must be cryptographically signed via SSH or GPG. Configure with:

```bash
git config commit.gpgsign true
```

## Branching policy

- `main` is protected; direct pushes are not allowed.
- Feature branches: `feat/<description>`
- Fix branches: `fix/<description>`
- Release branches: `release/<version>`

## Code review

- One approving review from CODEOWNERS is required.
- All CI checks must be green before merge.

## Development setup

```bash
git clone https://github.com/olaflaitinen/inkomstprognos.git
cd inkomstprognos
uv sync --all-extras
uv run pre-commit install
```

## Running checks locally

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict src
uv run pytest -x -q
uv run reuse lint
```

## Dependency policy

- All third-party dependencies must be compatible with EUPL-1.2.
- Dependencies are pinned via `uv.lock`.
- No incompatible (GPL-only without EUPL appendix coverage) dependencies.

## REUSE compliance

- Do not add SPDX identifier comment headers to source files.
- The `.reuse/dep5` file is the sole REUSE configuration.
- Run `reuse lint` before submitting a pull request.

## GDPR and PII

- Never commit personal data, real microdata, or personnummer.
- `gitleaks` runs in pre-commit and CI to detect potential PII leaks.

## Contact

- Institutional: olaf.laitinen@su.se
- Personal mirror: olaf.laitinen@gmail.com
- ORCID: [0009-0006-5184-0810](https://orcid.org/0009-0006-5184-0810)
