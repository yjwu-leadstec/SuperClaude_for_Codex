"""Tests for the atomic installer."""

import json

import pytest

from superclaude_codex.codex.agents_md import BEGIN_MARKER, END_MARKER
from superclaude_codex.codex.installer import Installer


class TestInstallerDryRun:
    def test_dry_run_no_files_written(self, tmp_codex_home):
        installer = Installer(codex_home=tmp_codex_home, dry_run=True)
        report = installer.run()
        assert report.status == "dry_run"
        assert not (tmp_codex_home / "AGENTS.md").exists()
        assert not (tmp_codex_home / "superclaude-for-codex").exists()

    def test_dry_run_reports_command_count(self, tmp_codex_home):
        installer = Installer(codex_home=tmp_codex_home, dry_run=True)
        report = installer.run()
        assert report.commands_installed == 30


class TestInstallerCommit:
    def test_creates_agents_md(self, tmp_codex_home):
        installer = Installer(codex_home=tmp_codex_home)
        installer.run()
        agents = tmp_codex_home / "AGENTS.md"
        assert agents.exists()
        content = agents.read_text()
        assert BEGIN_MARKER in content
        assert END_MARKER in content

    def test_creates_skills(self, tmp_codex_home):
        installer = Installer(codex_home=tmp_codex_home)
        installer.run()
        skills = tmp_codex_home / "skills"
        assert skills.exists()
        assert (skills / "superclaude-brainstorm" / "SKILL.md").exists()
        assert (skills / "superclaude-implement" / "SKILL.md").exists()

    def test_creates_commands_json(self, tmp_codex_home):
        installer = Installer(codex_home=tmp_codex_home)
        installer.run()
        cmds = tmp_codex_home / "superclaude-for-codex" / "commands.json"
        assert cmds.exists()
        data = json.loads(cmds.read_text())
        assert data["schema_version"] == 1
        assert len(data["commands"]) == 30

    def test_default_install_does_not_enable_native_plugin(self, tmp_codex_home):
        installer = Installer(codex_home=tmp_codex_home)
        installer.run()
        assert not (tmp_codex_home / "superclaude-for-codex" / "marketplace").exists()
        assert not (
            tmp_codex_home / "plugins" / "cache" / "superclaude-for-codex"
        ).exists()

        config = tmp_codex_home / "config.toml"
        if config.exists():
            content = config.read_text()
            assert "[marketplaces.superclaude-for-codex]" not in content
            assert (
                '[plugins."superclaude-for-codex@superclaude-for-codex"]' not in content
            )

    def test_creates_native_plugin_commands_when_enabled(self, tmp_codex_home):
        installer = Installer(codex_home=tmp_codex_home, native_plugin=True)
        installer.run()
        plugin = (
            tmp_codex_home
            / "superclaude-for-codex"
            / "marketplace"
            / "plugins"
            / "superclaude-for-codex"
        )
        assert (plugin / ".codex-plugin" / "plugin.json").exists()
        assert (plugin / "commands" / "sc-implement.md").exists()
        assert (plugin / "commands" / "sc-test.md").exists()
        assert not (plugin / "skills").exists()
        installed_plugin = (
            tmp_codex_home
            / "plugins"
            / "cache"
            / "superclaude-for-codex"
            / "superclaude-for-codex"
            / "local"
        )
        assert (installed_plugin / ".codex-plugin" / "plugin.json").exists()
        assert (installed_plugin / "commands" / "sc-implement.md").exists()
        assert not (installed_plugin / "skills").exists()

    def test_enables_native_plugin_in_config_when_enabled(self, tmp_codex_home):
        installer = Installer(codex_home=tmp_codex_home, native_plugin=True)
        installer.run()
        config = tmp_codex_home / "config.toml"
        assert config.exists()
        content = config.read_text()
        assert "[marketplaces.superclaude-for-codex]" in content
        assert '[plugins."superclaude-for-codex@superclaude-for-codex"]' in content

    def test_creates_version_json(self, tmp_codex_home):
        installer = Installer(codex_home=tmp_codex_home)
        installer.run()
        ver = tmp_codex_home / "superclaude-for-codex" / "version.json"
        assert ver.exists()
        data = json.loads(ver.read_text())
        assert data["version"] == "0.1.0"

    def test_creates_install_report(self, tmp_codex_home):
        installer = Installer(codex_home=tmp_codex_home, ui_locale="en")
        installer.run()
        report = tmp_codex_home / "superclaude-for-codex" / "install-report.json"
        assert report.exists()
        data = json.loads(report.read_text())
        assert data["status"] == "success"
        assert data["commands_installed"] == 30
        assert data["native_plugin_enabled"] is False
        assert data["ui_locale"] == "en"

    def test_locale_zh_cn_writes_ui_description(self, tmp_codex_home):
        installer = Installer(codex_home=tmp_codex_home, ui_locale="zh-CN")
        installer.run()
        metadata = (
            tmp_codex_home / "skills" / "superclaude-save" / "agents" / "openai.yaml"
        )
        content = metadata.read_text()
        assert 'display_name: "sc-save"' in content
        assert 'short_description: "保存会话上下文、学习记录和检查点"' in content

    def test_locale_auto_writes_traditional_chinese_description(
        self, tmp_codex_home, monkeypatch
    ):
        monkeypatch.delenv("LC_ALL", raising=False)
        monkeypatch.delenv("LC_MESSAGES", raising=False)
        monkeypatch.setenv("LANG", "zh_TW.UTF-8")
        installer = Installer(codex_home=tmp_codex_home, ui_locale="auto")
        installer.run()
        metadata = (
            tmp_codex_home / "skills" / "superclaude-save" / "agents" / "openai.yaml"
        )
        content = metadata.read_text()
        assert 'display_name: "sc-save"' in content
        assert 'short_description: "儲存會話上下文、學習記錄和檢查點"' in content

    def test_report_success(self, tmp_codex_home):
        installer = Installer(codex_home=tmp_codex_home)
        report = installer.run()
        assert report.status == "success"
        assert len(report.files_written) > 0


class TestInstallerIdempotent:
    def test_repeat_install_blocked_without_force(self, tmp_codex_home):
        Installer(codex_home=tmp_codex_home).run()
        with pytest.raises(Exception, match="already installed"):
            Installer(codex_home=tmp_codex_home).run()

    def test_repeat_install_with_force(self, tmp_codex_home):
        Installer(codex_home=tmp_codex_home).run()
        first_content = (tmp_codex_home / "AGENTS.md").read_text()
        Installer(codex_home=tmp_codex_home, force=True).run()
        second_content = (tmp_codex_home / "AGENTS.md").read_text()
        assert first_content == second_content

    def test_preserves_user_agents_content(self, tmp_codex_home):
        agents = tmp_codex_home / "AGENTS.md"
        agents.write_text("# My Custom Rules\n\nDo something custom.\n")
        Installer(codex_home=tmp_codex_home).run()
        content = agents.read_text()
        assert "My Custom Rules" in content
        assert BEGIN_MARKER in content


class TestInstallerClaude:
    def test_rejects_claude_home(self, fake_home):
        home, sentinel = fake_home
        claude = home / ".claude"
        with pytest.raises(Exception):
            Installer(codex_home=claude).run()
