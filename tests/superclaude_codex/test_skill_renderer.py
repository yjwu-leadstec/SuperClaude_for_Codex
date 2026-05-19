"""Tests for Skill renderer."""

import yaml

from superclaude_codex.codex.skills import render_all_skills, render_skill, write_skill
from superclaude_codex.core.command_ir import CommandIR
from superclaude_codex.core.registry import CommandRegistry

VALID_COMMAND = {
    "schema_version": 1,
    "id": "brainstorm",
    "display_name": "/sc:brainstorm",
    "category": "discovery",
    "description": "Brainstorm ideas.",
    "aliases": ["/sc:brainstorm", "sc:brainstorm"],
    "triggers": ["user wants to brainstorm"],
    "workflow": ["understand_request", "generate_alternatives"],
    "personas": ["analyst", "product"],
    "mcp": {"optional": ["context7"]},
    "safety": {
        "writes_code": False,
        "requires_user_confirmation_for_scope_change": True,
    },
    "output_contract": {
        "primary": "design_doc",
        "required_sections": ["problem_statement"],
    },
    "codex": {"skill_name": "superclaude-brainstorm"},
}


class TestRenderSkill:
    def test_has_frontmatter(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        content = render_skill(cmd)
        assert content.startswith("---\n")
        assert "name: superclaude-brainstorm" in content

    def test_has_heading(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        content = render_skill(cmd)
        assert "# /sc:brainstorm" in content

    def test_has_workflow(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        content = render_skill(cmd)
        assert "## Workflow" in content
        assert "1. Understand request" in content

    def test_has_personas(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        content = render_skill(cmd)
        assert "**analyst**" in content

    def test_has_safety(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        content = render_skill(cmd)
        assert "Do not write or modify code" in content

    def test_has_output_contract(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        content = render_skill(cmd)
        assert "design doc" in content
        assert "Problem statement" in content

    def test_has_mcp(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        content = render_skill(cmd)
        assert "context7" in content

    def test_stable_output(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        first = render_skill(cmd)
        second = render_skill(cmd)
        assert first == second


class TestWriteSkill:
    def test_creates_skill_directory(self, tmp_path):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        path = write_skill(tmp_path, cmd)
        assert path.exists()
        assert path.name == "SKILL.md"
        assert path.parent.name == "superclaude-brainstorm"

    def test_skill_content(self, tmp_path):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        path = write_skill(tmp_path, cmd)
        content = path.read_text()
        assert "# /sc:brainstorm" in content


class TestRenderAllSkills:
    def test_renders_all(self, tmp_path):
        assets = tmp_path / "assets"
        assets.mkdir()
        (assets / "brainstorm.yaml").write_text(yaml.dump(VALID_COMMAND))
        impl = {
            **VALID_COMMAND,
            "id": "implement",
            "display_name": "/sc:implement",
            "aliases": ["/sc:implement"],
            "codex": {"skill_name": "superclaude-implement"},
            "output_contract": {"primary": "impl", "required_sections": ["code"]},
            "safety": {"writes_code": True},
        }
        (assets / "implement.yaml").write_text(yaml.dump(impl))

        reg = CommandRegistry(assets_dir=assets)
        reg.load_all()

        codex_home = tmp_path / "codex_home"
        codex_home.mkdir()
        paths = render_all_skills(reg, codex_home)
        assert len(paths) == 2
        assert (codex_home / "skills" / "superclaude-brainstorm" / "SKILL.md").exists()
        assert (codex_home / "skills" / "superclaude-implement" / "SKILL.md").exists()
