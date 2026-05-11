"""Nox sessions for Inkomstprognos."""

from __future__ import annotations

import nox

nox.options.default_venv_backend = "uv"
nox.options.reuse_existing_virtualenvs = True

PYTHON_VERSIONS = ["3.11", "3.12"]
DEFAULT_PYTHON = "3.12"


@nox.session(python=DEFAULT_PYTHON)
def lint(session: nox.Session) -> None:
    """Run ruff linting and formatting checks."""
    session.install("ruff>=0.5")
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")


@nox.session(python=DEFAULT_PYTHON)
def type(session: nox.Session) -> None:
    """Run mypy strict type checking."""
    session.install(".[dev]")
    session.run("mypy", "--strict", "src")


@nox.session(python=PYTHON_VERSIONS)
def test(session: nox.Session) -> None:
    """Run the test suite."""
    session.install(".[dev]")
    session.run("pytest", "-x", "-q", *session.posargs)


@nox.session(python=DEFAULT_PYTHON)
def cov(session: nox.Session) -> None:
    """Run tests with coverage."""
    session.install(".[dev]")
    session.run(
        "pytest",
        "--cov=inkomstprognos",
        "--cov-fail-under=90",
        "--cov-branch",
        "--cov-report=term-missing",
        "--cov-report=xml:coverage.xml",
        *session.posargs,
    )


@nox.session(python=DEFAULT_PYTHON)
def docs(session: nox.Session) -> None:
    """Build MkDocs documentation."""
    session.install(".[docs]")
    session.run("mkdocs", "build", "--strict")


@nox.session(python=DEFAULT_PYTHON)
def build(session: nox.Session) -> None:
    """Build wheel and sdist."""
    session.install("build")
    session.run("python", "-m", "build")


@nox.session(python=DEFAULT_PYTHON)
def audit(session: nox.Session) -> None:
    """Run security audit with pip-audit and bandit."""
    session.install(".[dev]")
    session.run("pip-audit", "--strict")
    session.run("bandit", "-r", "src", "-lll")


@nox.session(python=DEFAULT_PYTHON)
def reuse(session: nox.Session) -> None:
    """Check REUSE compliance."""
    session.install("reuse>=4")
    session.run("reuse", "lint")


@nox.session(python=DEFAULT_PYTHON)
def sbom(session: nox.Session) -> None:
    """Generate CycloneDX SBOM."""
    session.install("cyclonedx-bom>=4")
    session.run("cyclonedx-py", "-o", "sbom.cdx.json")


@nox.session(python=DEFAULT_PYTHON)
def release(session: nox.Session) -> None:
    """Run the full release pipeline."""
    session.install(".[dev]")
    session.install("build", "twine")
    session.run("python", "-m", "build")
    session.run("twine", "check", "dist/*")
