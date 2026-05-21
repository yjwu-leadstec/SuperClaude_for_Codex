"""Tests for the superclaude-codex CLI entry point."""

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


def test_install_locale_zh_cn(tmp_codex_home):
    runner = CliRunner()
    result = runner.invoke(main, ["install", "--locale", "zh-CN"])
    assert result.exit_code == 0, result.output
    metadata = tmp_codex_home / "skills" / "superclaude-save" / "agents" / "openai.yaml"
    assert (
        'short_description: "保存会话上下文、学习记录和检查点"' in metadata.read_text()
    )


def test_install_locale_auto_zh_tw(tmp_codex_home):
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["install", "--locale", "auto"],
        env={"LC_ALL": "", "LC_MESSAGES": "", "LANG": "zh_TW.UTF-8"},
    )
    assert result.exit_code == 0, result.output
    metadata = tmp_codex_home / "skills" / "superclaude-save" / "agents" / "openai.yaml"
    assert (
        'short_description: "儲存會話上下文、學習記錄和檢查點"' in metadata.read_text()
    )


def test_install_dry_run(tmp_codex_home):
    runner = CliRunner()
    result = runner.invoke(main, ["install", "--dry-run"])
    assert result.exit_code == 0
    assert "dry-run" in result.output


def test_doctor_subcommand(tmp_codex_home):
    """Doctor on empty home should not crash."""
    runner = CliRunner()
    result = runner.invoke(main, ["doctor"])
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
    assert "/sc-brainstorm" in result.output


def test_commands_show_legacy_alias():
    runner = CliRunner()
    result = runner.invoke(main, ["commands", "show", "/sc:brainstorm"])
    assert result.exit_code == 0
    assert "/sc-brainstorm" in result.output


def test_mcp_list():
    runner = CliRunner()
    result = runner.invoke(main, ["mcp", "list"])
    assert result.exit_code == 0


def test_mcp_install(tmp_codex_home):
    """MCP install must use isolated CODEX_HOME."""
    runner = CliRunner()
    result = runner.invoke(main, ["mcp", "install", "context7"])
    assert result.exit_code == 0
    assert (tmp_codex_home / "config.toml").exists()


def test_mcp_install_all(tmp_codex_home):
    """MCP install --all must use isolated CODEX_HOME."""
    runner = CliRunner()
    result = runner.invoke(main, ["mcp", "install", "--all"])
    assert result.exit_code == 0
