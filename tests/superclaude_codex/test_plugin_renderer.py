"""Tests for native Codex plugin rendering."""

import json

from superclaude_codex.codex.plugin import (
    PLUGIN_NAME,
    get_installed_plugin_dir,
    install_plugin_cache,
    render_plugin_command,
    render_plugin_config_block,
    render_plugin_manifest,
    write_plugin,
)
from superclaude_codex.core.registry import CommandRegistry


def test_manifest_declares_skills():
    data = json.loads(render_plugin_manifest())
    assert data["name"] == PLUGIN_NAME
    assert data["interface"]["displayName"] == "SuperClaude for Codex"
    assert "skills" not in data


def test_command_file_uses_dash_name():
    reg = CommandRegistry()
    reg.load_all()
    cmd = reg.get_command("implement")
    content = render_plugin_command(cmd)
    assert "# /sc-implement" in content
    assert "~/.codex/skills/superclaude-implement/SKILL.md" in content
    assert "`/sc:implement`" in content


def test_command_file_quotes_argument_hint_and_renders_parameters():
    reg = CommandRegistry()
    reg.load_all()
    cmd = reg.get_command("build")
    content = render_plugin_command(cmd)
    assert 'argument-hint: "[target] [--type dev|prod|test]' in content
    assert "[global-flags]" in content
    assert "## Parameters" in content
    assert "`--type` `dev|prod|test`" in content
    assert "`--clean`" in content
    assert "## Global Flags" in content
    assert "`--think-hard`" in content
    assert "## Examples" in content


def test_long_argument_hint_is_compacted():
    reg = CommandRegistry()
    reg.load_all()
    cmd = reg.get_command("business-panel")
    content = render_plugin_command(cmd)
    hint_line = next(
        line for line in content.splitlines() if line.startswith("argument-hint:")
    )
    assert len(hint_line.removeprefix("argument-hint: ").strip().strip('"')) <= 120
    assert "[global-flags]" in hint_line
    assert "`--synthesis-only`" in content


def test_free_value_and_alias_parameters_render():
    reg = CommandRegistry()
    reg.load_all()
    cmd = reg.get_command("test")
    content = render_plugin_command(cmd)
    assert "`--type` / `--mode` `unit|integration|e2e|all`" in content
    assert "`--framework` `pytest|jest|vitest|mocha`" in content


def test_write_plugin_creates_commands_and_manifest(tmp_path):
    reg = CommandRegistry()
    reg.load_all()
    written = write_plugin(reg, tmp_path)

    plugin = tmp_path / "plugins" / PLUGIN_NAME
    assert (plugin / ".codex-plugin" / "plugin.json").exists()
    assert (plugin / "commands" / "sc-implement.md").exists()
    assert not (plugin / "skills").exists()
    assert (tmp_path / ".agents" / "plugins" / "marketplace.json").exists()
    assert len([p for p in written if p.name.endswith(".md")]) == 30


def test_install_plugin_cache_copies_runtime_plugin(tmp_path):
    reg = CommandRegistry()
    reg.load_all()
    marketplace = tmp_path / "superclaude-for-codex" / "marketplace"
    write_plugin(reg, marketplace)

    installed = install_plugin_cache(tmp_path)

    assert installed == get_installed_plugin_dir(tmp_path)
    assert (installed / ".codex-plugin" / "plugin.json").exists()
    assert (installed / "commands" / "sc-implement.md").exists()
    assert not (installed / "skills").exists()


def test_plugin_config_block_registers_marketplace(tmp_path):
    block = render_plugin_config_block(tmp_path, timestamp="2026-05-21T00:00:00Z")
    assert "[marketplaces.superclaude-for-codex]" in block
    assert '[plugins."superclaude-for-codex@superclaude-for-codex"]' in block
    assert f'source = "{tmp_path}/superclaude-for-codex/marketplace"' in block
