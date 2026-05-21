"""Tests for the uninstaller, including MCP-only scenarios."""

from superclaude_codex.codex.agents_md import BEGIN_MARKER, END_MARKER
from superclaude_codex.codex.mcp import BEGIN_MARKER as MCP_BEGIN
from superclaude_codex.codex.mcp import END_MARKER as MCP_END
from superclaude_codex.codex.plugin import BEGIN_MARKER as PLUGIN_BEGIN
from superclaude_codex.codex.plugin import END_MARKER as PLUGIN_END
from superclaude_codex.codex.uninstall import uninstall


class TestUninstallMCPOnly:
    """Regression: uninstall must work when only MCP block exists (no AGENTS block)."""

    def test_mcp_only_uninstall(self, tmp_codex_home):
        config = tmp_codex_home / "config.toml"
        config.write_text(
            f"[other]\nkey = 'value'\n\n{MCP_BEGIN}\n\n[mcp.context7]\n"
            f'command = "npx"\n\n{MCP_END}\n'
        )
        actions = uninstall(codex_home=tmp_codex_home)
        content = config.read_text()
        assert MCP_BEGIN not in content
        assert MCP_END not in content
        assert "[other]" in content
        assert any("MCP block" in a for a in actions)

    def test_mcp_only_uninstall_dry_run(self, tmp_codex_home):
        config = tmp_codex_home / "config.toml"
        original = f"{MCP_BEGIN}\n[mcp.tavily]\n{MCP_END}\n"
        config.write_text(original)
        actions = uninstall(codex_home=tmp_codex_home, dry_run=True)
        assert config.read_text() == original
        assert any("dry-run" in a for a in actions)

    def test_plugin_block_uninstall(self, tmp_codex_home):
        config = tmp_codex_home / "config.toml"
        config.write_text(
            f"[other]\nkey = 'value'\n\n{PLUGIN_BEGIN}\n\n"
            "[marketplaces.superclaude-for-codex]\n"
            f'source_type = "local"\n\n{PLUGIN_END}\n'
        )
        actions = uninstall(codex_home=tmp_codex_home)
        content = config.read_text()
        assert PLUGIN_BEGIN not in content
        assert PLUGIN_END not in content
        assert "[other]" in content
        assert any("plugin block" in a for a in actions)


class TestUninstallFull:
    def test_removes_skills(self, tmp_codex_home):
        skills = tmp_codex_home / "skills" / "superclaude-brainstorm"
        skills.mkdir(parents=True)
        (skills / "SKILL.md").write_text("test")
        actions = uninstall(codex_home=tmp_codex_home)
        assert not skills.exists()
        assert any("superclaude-brainstorm" in a for a in actions)

    def test_removes_data_dir(self, tmp_codex_home):
        sc = tmp_codex_home / "superclaude-for-codex"
        sc.mkdir()
        (sc / "commands.json").write_text("{}")
        uninstall(codex_home=tmp_codex_home)
        assert not sc.exists()

    def test_removes_installed_plugin_cache(self, tmp_codex_home):
        plugin = (
            tmp_codex_home
            / "plugins"
            / "cache"
            / "superclaude-for-codex"
            / "superclaude-for-codex"
            / "local"
        )
        plugin.mkdir(parents=True)
        (plugin / "marker").write_text("installed")
        uninstall(codex_home=tmp_codex_home)
        assert not plugin.exists()

    def test_removes_agents_block(self, tmp_codex_home):
        agents = tmp_codex_home / "AGENTS.md"
        agents.write_text(
            f"# User rules\n\n{BEGIN_MARKER}\nstuff\n{END_MARKER}\n\nFooter\n"
        )
        uninstall(codex_home=tmp_codex_home)
        content = agents.read_text()
        assert BEGIN_MARKER not in content
        assert "User rules" in content
        assert "Footer" in content

    def test_preserves_non_superclaude_skills(self, tmp_codex_home):
        skills = tmp_codex_home / "skills"
        user_skill = skills / "my-custom-skill"
        user_skill.mkdir(parents=True)
        (user_skill / "SKILL.md").write_text("mine")
        sc_skill = skills / "superclaude-test"
        sc_skill.mkdir()
        (sc_skill / "SKILL.md").write_text("sc")
        uninstall(codex_home=tmp_codex_home)
        assert user_skill.exists()
        assert not sc_skill.exists()

    def test_empty_home_no_crash(self, tmp_codex_home):
        actions = uninstall(codex_home=tmp_codex_home)
        assert actions == []
