"""Tests for the superclaude-codex CLI entry point."""

import os

from click.testing import CliRunner

from superclaude_codex.cli.main import main


def test_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "SuperClaude for Codex" in result.output


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_install_subcommand(tmp_codex_home):
    runner = CliRunner()
    result = runner.invoke(main, ["install"])
    assert result.exit_code == 0, result.output


def test_install_dry_run(tmp_codex_home):
    runner = CliRunner()
    result = runner.invoke(main, ["install", "--dry-run"])
    assert result.exit_code == 0
    assert "dry-run" in result.output


def test_doctor_subcommand(tmp_codex_home):
    """Doctor on empty home should not crash (checks will fail gracefully)."""
    runner = CliRunner()
    result = runner.invoke(main, ["doctor"])
    # May exit non-zero if not installed, but should not crash
    assert result.exception is None or isinstance(result.exception, SystemExit)


def test_verify_subcommand(tmp_codex_home):
    runner = CliRunner()
    result = runner.invoke(main, ["verify"])
    assert result.exception is None or isinstance(result.exception, SystemExit)


def test_commands_list():
    runner = CliRunner()
    result = runner.invoke(main, ["commands", "list"])
    assert result.exit_code == 0


def test_commands_validate():
    runner = CliRunner()
    result = runner.invoke(main, ["commands", "validate"])
    assert result.exit_code == 0


def test_commands_show():
    runner = CliRunner()
    result = runner.invoke(main, ["commands", "show", "brainstorm"])
    assert result.exit_code == 0
    assert "brainstorm" in result.output


def test_mcp_list():
    runner = CliRunner()
    result = runner.invoke(main, ["mcp", "list"])
    assert result.exit_code == 0


def test_mcp_install():
    runner = CliRunner()
    result = runner.invoke(main, ["mcp", "install", "context7"])
    assert result.exit_code == 0


def test_mcp_install_all():
    runner = CliRunner()
    result = runner.invoke(main, ["mcp", "install", "--all"])
    assert result.exit_code == 0
