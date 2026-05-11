"""Command-line interface for Inkomstprognos."""

from __future__ import annotations

import pathlib

import typer

from inkomstprognos._version import __version__
from inkomstprognos.config import Config

app = typer.Typer(
    name="inkomstprognos",
    help="Probabilistic disposable-income forecasting on Swedish administrative microdata.",
    no_args_is_help=True,
)


def _load_config(config: pathlib.Path | None) -> Config:
    if config is not None:
        return Config.from_file(config)
    return Config(data_root=pathlib.Path("data"))


def _version_callback(value: bool) -> None:
    if value:
        print(f"inkomstprognos {__version__}")  # noqa: T201
        raise typer.Exit


@app.callback()
def main_callback(
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Show version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    """Inkomstprognos CLI."""


@app.command()
def ingest(
    config: pathlib.Path | None = typer.Option(None, "--config", "-c", help="Config file."),
) -> None:
    """Ingest data sources."""
    cfg = _load_config(config)
    print(f"Ingesting data from {cfg.data_root}")  # noqa: T201


@app.command()
def train(
    config: pathlib.Path | None = typer.Option(None, "--config", "-c", help="Config file."),
) -> None:
    """Train forecasting models."""
    cfg = _load_config(config)
    print(f"Training {cfg.model} model with seed {cfg.seed}")  # noqa: T201


@app.command()
def predict(
    config: pathlib.Path | None = typer.Option(None, "--config", "-c", help="Config file."),
) -> None:
    """Generate predictions."""
    cfg = _load_config(config)
    print(f"Predicting {cfg.outcome} at horizon {cfg.horizon}")  # noqa: T201


@app.command()
def evaluate(
    config: pathlib.Path | None = typer.Option(None, "--config", "-c", help="Config file."),
) -> None:
    """Evaluate forecast quality."""
    cfg = _load_config(config)
    print(f"Evaluating {cfg.outcome} forecasts")  # noqa: T201


@app.command()
def report(
    config: pathlib.Path | None = typer.Option(None, "--config", "-c", help="Config file."),
) -> None:
    """Generate reports."""
    cfg = _load_config(config)
    print(f"Generating reports for {cfg.outcome}")  # noqa: T201


@app.command()
def repro(
    config: pathlib.Path | None = typer.Option(None, "--config", "-c", help="Config file."),
) -> None:
    """Run full reproducibility pipeline."""
    cfg = _load_config(config)
    print(f"Running reproducibility pipeline with seed {cfg.seed}")  # noqa: T201


@app.command()
def audit() -> None:
    """Run security audit."""
    print("Running security audit")  # noqa: T201


@app.command()
def sbom() -> None:
    """Generate CycloneDX SBOM."""
    print("Generating SBOM")  # noqa: T201


@app.command(name="reuse-check")
def reuse_check() -> None:
    """Check REUSE compliance."""
    print("Checking REUSE compliance")  # noqa: T201


def main() -> None:
    """Entry point for the CLI.

    Examples:
        >>> main()  # doctest: +SKIP
    """
    app()
