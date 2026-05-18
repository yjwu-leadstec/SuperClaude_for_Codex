"""Tests for the atomic installer."""

import json
from pathlib import Path

import pytest

from superclaude_codex.codex.installer import InstallError, Installer
from superclaude_codex.codex.agents_md import BEGIN_MARKER, END_MARKER


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

    def test_creates_version_json(self, tmp_codex_home):
        installer = Installer(codex_home=tmp_codex_home)
        installer.run()
        ver = tmp_codex_home / "superclaude-for-codex" / "version.json"
        assert ver.exists()
        data = json.loads(ver.read_text())
        assert data["version"] == "0.1.0"

    def test_creates_install_report(self, tmp_codex_home):
        installer = Installer(codex_home=tmp_codex_home)
        installer.run()
        report = tmp_codex_home / "superclaude-for-codex" / "install-report.json"
        assert report.exists()
        data = json.loads(report.read_text())
        assert data["status"] == "success"
        assert data["commands_installed"] == 30

    def test_report_success(self, tmp_codex_home):
        installer = Installer(codex_home=tmp_codex_home)
        report = installer.run()
        assert report.status == "success"
        assert len(report.files_written) > 0


class TestInstallerIdempotent:
    def test_repeat_install(self, tmp_codex_home):
        Installer(codex_home=tmp_codex_home).run()
        first_content = (tmp_codex_home / "AGENTS.md").read_text()
        Installer(codex_home=tmp_codex_home).run()
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
