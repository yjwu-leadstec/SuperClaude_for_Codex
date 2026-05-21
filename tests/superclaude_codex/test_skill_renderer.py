"""Tests for Skill renderer."""

import yaml

from superclaude_codex.codex.skills import (
    detect_ui_locale_from_env,
    get_short_description,
    normalize_ui_locale,
    render_all_skills,
    render_openai_yaml,
    render_skill,
    write_skill,
)
from superclaude_codex.core.command_ir import CommandIR
from superclaude_codex.core.registry import CommandRegistry

VALID_COMMAND = {
    "schema_version": 1,
    "id": "brainstorm",
    "display_name": "/sc-brainstorm",
    "category": "discovery",
    "description": "Brainstorm ideas.",
    "aliases": ["/sc-brainstorm", "/sc:brainstorm", "sc-brainstorm", "sc:brainstorm"],
    "triggers": ["user wants to brainstorm"],
    "inputs": {
        "positional": [
            {
                "name": "topic",
                "required": False,
                "description": "Idea or topic to explore.",
            }
        ],
        "flags": [
            {
                "name": "strategy",
                "values": ["systematic", "agile"],
                "description": "Discovery strategy.",
            },
            {
                "name": "parallel",
                "type": "boolean",
                "description": "Explore in parallel.",
            },
        ],
    },
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
        assert "# /sc-brainstorm" in content

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

    def test_has_inputs_and_global_flags(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        content = render_skill(cmd)
        assert "## Inputs" in content
        assert "`[topic]` (optional): Idea or topic to explore." in content
        assert "`--strategy` `systematic|agile`: Discovery strategy." in content
        assert "`--parallel`: Explore in parallel." in content
        assert "## Global Flags" in content
        assert "`--think-hard`" in content

    def test_stable_output(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        first = render_skill(cmd)
        second = render_skill(cmd)
        assert first == second


class TestRenderOpenAIYaml:
    def test_normalizes_locale(self):
        assert normalize_ui_locale("zh_CN") == "zh-CN"
        assert normalize_ui_locale("zh_TW") == "zh-TW"
        assert normalize_ui_locale("en-US") == "en"

    def test_detects_auto_locale_from_env(self):
        assert detect_ui_locale_from_env({"LANG": "zh_CN.UTF-8"}) == "zh-CN"
        assert detect_ui_locale_from_env({"LANG": "zh_TW.UTF-8"}) == "zh-TW"
        assert detect_ui_locale_from_env({"LANG": "zh_HK.UTF-8"}) == "zh-TW"
        assert detect_ui_locale_from_env({"LANG": "zh-Hant.UTF-8"}) == "zh-TW"
        assert detect_ui_locale_from_env({"LANG": "en_US.UTF-8"}) == "en"
        assert normalize_ui_locale("auto", {"LANG": "zh_Hans.UTF-8"}) == "zh-CN"

    def test_display_name_uses_short_sc_command_name(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        content = render_openai_yaml(cmd)
        data = yaml.safe_load(content)
        assert data["interface"]["display_name"] == "sc-brainstorm"
        assert data["interface"]["default_prompt"] == (
            "Use $superclaude-brainstorm for this task."
        )
        assert data["policy"]["allow_implicit_invocation"] is True

    def test_zh_cn_only_changes_short_description(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        content = render_openai_yaml(cmd, ui_locale="zh-CN")
        data = yaml.safe_load(content)
        assert data["interface"]["display_name"] == "sc-brainstorm"
        assert data["interface"]["short_description"] == (
            "通过提问和探索梳理需求、想法和方案"
        )
        assert data["interface"]["default_prompt"] == (
            "Use $superclaude-brainstorm for this task."
        )
        assert get_short_description(cmd, "en") == "Brainstorm ideas."

    def test_zh_tw_only_changes_short_description(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        content = render_openai_yaml(cmd, ui_locale="zh-TW")
        data = yaml.safe_load(content)
        assert data["interface"]["display_name"] == "sc-brainstorm"
        assert data["interface"]["short_description"] == (
            "透過提問和探索梳理需求、想法和方案"
        )


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
        assert "# /sc-brainstorm" in content

    def test_creates_openai_yaml(self, tmp_path):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        path = write_skill(tmp_path, cmd)
        openai_yaml = path.parent / "agents" / "openai.yaml"
        assert openai_yaml.exists()
        data = yaml.safe_load(openai_yaml.read_text())
        assert data["interface"]["display_name"] == "sc-brainstorm"

    def test_creates_zh_cn_openai_yaml(self, tmp_path):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        path = write_skill(tmp_path, cmd, ui_locale="zh-CN")
        openai_yaml = path.parent / "agents" / "openai.yaml"
        data = yaml.safe_load(openai_yaml.read_text())
        assert data["interface"]["short_description"] == (
            "通过提问和探索梳理需求、想法和方案"
        )


class TestRenderAllSkills:
    def test_renders_all(self, tmp_path):
        assets = tmp_path / "assets"
        assets.mkdir()
        (assets / "brainstorm.yaml").write_text(yaml.dump(VALID_COMMAND))
        impl = {
            **VALID_COMMAND,
            "id": "implement",
            "display_name": "/sc-implement",
            "aliases": ["/sc-implement", "/sc:implement"],
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
        assert (
            codex_home
            / "skills"
            / "superclaude-brainstorm"
            / "agents"
            / "openai.yaml"
        ).exists()
        assert (codex_home / "skills" / "superclaude-implement" / "SKILL.md").exists()
