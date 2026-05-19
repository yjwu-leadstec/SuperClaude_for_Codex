"""Tests for codex/paths.py — CODEX_HOME resolution and safety guards."""

import os
from pathlib import Path

import pytest

from superclaude_codex.codex.paths import (
    ClaudePathError,
    UnsafePathError,
    assert_not_claude_path,
    assert_safe_path,
    get_agents_md_path,
    get_config_toml_path,
    get_skills_dir,
    get_superclaude_dir,
    resolve_codex_home,
)


class TestResolveCodexHome:
    def test_uses_env_var(self, tmp_path):
        os.environ["CODEX_HOME"] = str(tmp_path / "custom")
        try:
            assert resolve_codex_home() == tmp_path / "custom"
        finally:
            os.environ.pop("CODEX_HOME")

    def test_defaults_to_home_codex(self, monkeypatch):
        monkeypatch.delenv("CODEX_HOME", raising=False)
        result = resolve_codex_home()
        assert result == Path.home() / ".codex"

    def test_rejects_claude_path(self, monkeypatch):
        claude = str(Path.home() / ".claude")
        monkeypatch.setenv("CODEX_HOME", claude)
        with pytest.raises(ClaudePathError):
            resolve_codex_home()

    def test_rejects_claude_subpath(self, monkeypatch):
        sub = str(Path.home() / ".claude" / "subdir")
        monkeypatch.setenv("CODEX_HOME", sub)
        with pytest.raises(ClaudePathError):
            resolve_codex_home()


class TestAssertNotClaudePath:
    def test_allows_codex_path(self, tmp_path):
        assert_not_claude_path(tmp_path / ".codex")

    def test_rejects_claude_dir(self):
        with pytest.raises(ClaudePathError):
            assert_not_claude_path(Path.home() / ".claude")

    def test_rejects_claude_child(self):
        with pytest.raises(ClaudePathError):
            assert_not_claude_path(Path.home() / ".claude" / "commands" / "sc")

    def test_allows_unrelated_path(self):
        assert_not_claude_path(Path("/tmp/whatever"))


class TestPathHelpers:
    def test_agents_md_path(self, tmp_codex_home):
        assert get_agents_md_path(tmp_codex_home) == tmp_codex_home / "AGENTS.md"

    def test_config_toml_path(self, tmp_codex_home):
        assert get_config_toml_path(tmp_codex_home) == tmp_codex_home / "config.toml"

    def test_skills_dir(self, tmp_codex_home):
        assert get_skills_dir(tmp_codex_home) == tmp_codex_home / "skills"

    def test_superclaude_dir(self, tmp_codex_home):
        expected = tmp_codex_home / "superclaude-for-codex"
        assert get_superclaude_dir(tmp_codex_home) == expected

    def test_helpers_use_env_var(self, tmp_codex_home):
        """All helpers should resolve via CODEX_HOME when no arg given."""
        assert get_agents_md_path() == tmp_codex_home / "AGENTS.md"
        assert get_skills_dir() == tmp_codex_home / "skills"


class TestSystemPathGuard:
    @pytest.mark.parametrize("dangerous", ["/", "/etc", "/usr", "/var", "/bin"])
    def test_rejects_exact_system_paths(self, dangerous):
        with pytest.raises(UnsafePathError):
            assert_safe_path(Path(dangerous))

    def test_allows_user_paths(self, tmp_path):
        assert_safe_path(tmp_path / ".codex")  # no exception

    def test_allows_subdirs_of_system_paths(self):
        # /etc/superclaude-codex is a dedicated subdir, not /etc itself
        assert_safe_path(Path("/etc/superclaude-codex"))  # no exception

    def test_resolve_rejects_system_codex_home(self, monkeypatch):
        monkeypatch.setenv("CODEX_HOME", "/etc")
        with pytest.raises(UnsafePathError):
            resolve_codex_home()
