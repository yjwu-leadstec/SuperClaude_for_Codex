"""Tests for MCP config management."""

import pytest

from superclaude_codex.codex.mcp import (
    BEGIN_MARKER,
    END_MARKER,
    MCPConfigError,
    render_mcp_block,
    update_config_toml,
)


class TestRenderMcpBlock:
    def test_renders_known_servers(self):
        block = render_mcp_block(["context7"])
        assert BEGIN_MARKER in block
        assert END_MARKER in block
        assert "context7" in block

    def test_rejects_unknown_server(self):
        with pytest.raises(KeyError, match="Unknown MCP"):
            render_mcp_block(["nonexistent"])

    def test_multiple_servers(self):
        block = render_mcp_block(["context7", "tavily"])
        assert "context7" in block
        assert "tavily" in block


class TestUpdateConfigToml:
    def test_creates_new_file(self, tmp_codex_home):
        path = tmp_codex_home / "config.toml"
        block = render_mcp_block(["context7"])
        update_config_toml(path, block)
        content = path.read_text()
        assert BEGIN_MARKER in content

    def test_replaces_existing_block(self, tmp_codex_home):
        path = tmp_codex_home / "config.toml"
        path.write_text(f"[user]\nkey='v'\n\n{BEGIN_MARKER}\nold\n{END_MARKER}\n")
        block = render_mcp_block(["context7"])
        update_config_toml(path, block)
        content = path.read_text()
        assert "old" not in content
        assert "context7" in content
        assert "[user]" in content

    def test_preserves_user_config(self, tmp_codex_home):
        path = tmp_codex_home / "config.toml"
        path.write_text("[my-settings]\nfoo = 'bar'\n")
        block = render_mcp_block(["context7"])
        update_config_toml(path, block)
        content = path.read_text()
        assert "[my-settings]" in content
        assert BEGIN_MARKER in content

    def test_single_marker_raises(self, tmp_codex_home):
        path = tmp_codex_home / "config.toml"
        path.write_text(f"stuff\n{BEGIN_MARKER}\nbroken")
        block = render_mcp_block(["context7"])
        with pytest.raises(MCPConfigError):
            update_config_toml(path, block)

    def test_creates_backup(self, tmp_codex_home):
        path = tmp_codex_home / "config.toml"
        path.write_text("[existing]\nkey = 'value'\n")
        block = render_mcp_block(["context7"])
        update_config_toml(path, block)
        backup = path.with_suffix(".toml.bak")
        assert backup.exists()
        assert "[existing]" in backup.read_text()
