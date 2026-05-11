"""Tests for the CLI module."""

from __future__ import annotations

from typer.testing import CliRunner

from inkomstprognos.cli import app

runner = CliRunner()


def test_version_flag() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_ingest_default() -> None:
    result = runner.invoke(app, ["ingest"])
    assert result.exit_code == 0
    assert "Ingesting" in result.output


def test_train_default() -> None:
    result = runner.invoke(app, ["train"])
    assert result.exit_code == 0
    assert "Training" in result.output


def test_predict_default() -> None:
    result = runner.invoke(app, ["predict"])
    assert result.exit_code == 0
    assert "Predicting" in result.output


def test_evaluate_default() -> None:
    result = runner.invoke(app, ["evaluate"])
    assert result.exit_code == 0
    assert "Evaluating" in result.output


def test_report_default() -> None:
    result = runner.invoke(app, ["report"])
    assert result.exit_code == 0
    assert "Generating" in result.output


def test_repro_default() -> None:
    result = runner.invoke(app, ["repro"])
    assert result.exit_code == 0
    assert "reproducibility" in result.output


def test_audit_command() -> None:
    result = runner.invoke(app, ["audit"])
    assert result.exit_code == 0


def test_sbom_command() -> None:
    result = runner.invoke(app, ["sbom"])
    assert result.exit_code == 0


def test_reuse_check_command() -> None:
    result = runner.invoke(app, ["reuse-check"])
    assert result.exit_code == 0


def test_no_args_shows_help() -> None:
    result = runner.invoke(app, [])
    assert result.exit_code == 0 or "Usage" in result.output
