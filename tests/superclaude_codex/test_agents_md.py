"""Tests for AGENTS.md renderer."""


import yaml

from superclaude_codex.codex.agents_md import (
    BEGIN_MARKER,
    END_MARKER,
    extract_existing_block,
    render_agents_block,
    update_agents_md,
)
from superclaude_codex.core.registry import CommandRegistry


def _make_registry(tmp_path):
    data = {
        "schema_version": 1, "id": "brainstorm", "display_name": "/sc:brainstorm",
        "category": "discovery", "description": "Brainstorm ideas.",
        "aliases": ["/sc:brainstorm"], "workflow": ["explore"],
        "output_contract": {"primary": "design_doc", "required_sections": ["summary"]},
        "codex": {"skill_name": "superclaude-brainstorm"},
        "safety": {"writes_code": False},
    }
    (tmp_path / "brainstorm.yaml").write_text(yaml.dump(data))
    reg = CommandRegistry(assets_dir=tmp_path)
    reg.load_all()
    return reg


class TestRenderAgentsBlock:
    def test_contains_markers(self, tmp_path):
        reg = _make_registry(tmp_path)
        block = render_agents_block(reg)
        assert BEGIN_MARKER in block
        assert END_MARKER in block

    def test_contains_command_route(self, tmp_path):
        reg = _make_registry(tmp_path)
        block = render_agents_block(reg)
        assert "`/sc:brainstorm`" in block
        assert "superclaude-brainstorm" in block

    def test_no_claude_reference(self, tmp_path):
        reg = _make_registry(tmp_path)
        block = render_agents_block(reg)
        assert "Do not read or write `~/.claude`." in block


class TestExtractExistingBlock:
    def test_extracts_block(self):
        content = f"User content\n\n{BEGIN_MARKER}\nstuff\n{END_MARKER}\n\nMore user content"
        block = extract_existing_block(content)
        assert block is not None
        assert block.startswith(BEGIN_MARKER)
        assert block.endswith(END_MARKER)

    def test_returns_none_when_no_markers(self):
        assert extract_existing_block("no markers here") is None


class TestUpdateAgentsMd:
    def test_creates_new_file(self, tmp_path):
        path = tmp_path / "AGENTS.md"
        reg = _make_registry(tmp_path)
        block = render_agents_block(reg)
        update_agents_md(path, block)
        content = path.read_text()
        assert BEGIN_MARKER in content

    def test_replaces_existing_block(self, tmp_path):
        path = tmp_path / "AGENTS.md"
        path.write_text(f"User rules\n\n{BEGIN_MARKER}\nold\n{END_MARKER}\n\nMore rules")
        reg = _make_registry(tmp_path)
        block = render_agents_block(reg)
        update_agents_md(path, block)
        content = path.read_text()
        assert "old" not in content
        assert "superclaude-brainstorm" in content

    def test_preserves_user_content(self, tmp_path):
        path = tmp_path / "AGENTS.md"
        path.write_text(f"My custom rules\n\n{BEGIN_MARKER}\nold\n{END_MARKER}\n\nFooter")
        reg = _make_registry(tmp_path)
        block = render_agents_block(reg)
        update_agents_md(path, block)
        content = path.read_text()
        assert "My custom rules" in content
        assert "Footer" in content

    def test_appends_if_no_markers(self, tmp_path):
        path = tmp_path / "AGENTS.md"
        path.write_text("Existing user content")
        reg = _make_registry(tmp_path)
        block = render_agents_block(reg)
        update_agents_md(path, block)
        content = path.read_text()
        assert "Existing user content" in content
        assert BEGIN_MARKER in content

    def test_idempotent(self, tmp_path):
        path = tmp_path / "AGENTS.md"
        reg = _make_registry(tmp_path)
        block = render_agents_block(reg)
        update_agents_md(path, block)
        first = path.read_text()
        update_agents_md(path, block)
        second = path.read_text()
        assert first == second


class TestCorruptMarkers:
    def test_single_begin_raises(self, tmp_path):
        import pytest

        from superclaude_codex.codex.agents_md import AgentsBlockError
        path = tmp_path / "AGENTS.md"
        path.write_text(f"Content\n{BEGIN_MARKER}\nstuff\n")
        reg = _make_registry(tmp_path)
        block = render_agents_block(reg)
        with pytest.raises(AgentsBlockError):
            update_agents_md(path, block)

    def test_single_end_raises(self, tmp_path):
        import pytest

        from superclaude_codex.codex.agents_md import AgentsBlockError
        path = tmp_path / "AGENTS.md"
        path.write_text(f"Content\n{END_MARKER}\n")
        reg = _make_registry(tmp_path)
        block = render_agents_block(reg)
        with pytest.raises(AgentsBlockError):
            update_agents_md(path, block)

    def test_duplicate_begin_raises(self, tmp_path):
        import pytest

        from superclaude_codex.codex.agents_md import AgentsBlockError
        path = tmp_path / "AGENTS.md"
        path.write_text(f"{BEGIN_MARKER}\nfoo\n{BEGIN_MARKER}\nbar\n{END_MARKER}\n")
        reg = _make_registry(tmp_path)
        block = render_agents_block(reg)
        with pytest.raises(AgentsBlockError):
            update_agents_md(path, block)
