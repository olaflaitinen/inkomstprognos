.DEFAULT_GOAL := help

.PHONY: help install lint type test cov docs build release sbom reuse clean audit

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install the project with dev dependencies
	uv sync --all-extras

lint:  ## Run linting checks
	uv run nox -s lint

type:  ## Run type checking
	uv run nox -s type

test:  ## Run the test suite
	uv run nox -s test

cov:  ## Run tests with coverage
	uv run nox -s cov

docs:  ## Build documentation
	uv run nox -s docs

build:  ## Build wheel and sdist
	uv run nox -s build

release:  ## Run release pipeline
	uv run nox -s release

sbom:  ## Generate CycloneDX SBOM
	uv run nox -s sbom

reuse:  ## Check REUSE compliance
	uv run nox -s reuse

audit:  ## Run security audit
	uv run nox -s audit

clean:  ## Remove build artefacts
	rm -rf dist/ build/ site/ .nox/ .mypy_cache/ .ruff_cache/ .pytest_cache/
	rm -rf htmlcov/ coverage.xml sbom.cdx.json
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
