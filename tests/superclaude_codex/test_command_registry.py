"""Tests for Command IR, validation, and registry."""

import json
from pathlib import Path

import yaml

from superclaude_codex.core.command_ir import CommandIR
from superclaude_codex.core.registry import CommandRegistry
from superclaude_codex.core.validation import validate_command, validate_no_duplicates

VALID_COMMAND = {
    "schema_version": 1,
    "id": "brainstorm",
    "display_name": "/sc:brainstorm",
    "category": "discovery",
    "description": "Interactive requirements discovery.",
    "aliases": ["/sc:brainstorm", "sc:brainstorm", "brainstorm"],
    "triggers": ["user wants to explore an idea"],
    "workflow": ["understand_request", "generate_alternatives"],
    "personas": ["analyst", "product"],
    "mcp": {"optional": ["context7"]},
    "safety": {
        "writes_code": False,
        "writes_files": True,
        "requires_user_confirmation_for_scope_change": True,
    },
    "output_contract": {
        "primary": "design_doc",
        "required_sections": ["problem_statement", "recommended_approach"],
    },
    "codex": {
        "skill_name": "superclaude-brainstorm",
        "default_reasoning": "medium",
        "web_search": "optional",
    },
}


class TestCommandIR:
    def test_from_dict(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        assert cmd.id == "brainstorm"
        assert cmd.schema_version == 1
        assert cmd.display_name == "/sc:brainstorm"
        assert "/sc:brainstorm" in cmd.aliases
        assert cmd.safety.writes_code is False
        assert cmd.output_contract.primary == "design_doc"
        assert cmd.codex.skill_name == "superclaude-brainstorm"

    def test_from_yaml(self, tmp_path):
        f = tmp_path / "brainstorm.yaml"
        f.write_text(yaml.dump(VALID_COMMAND))
        cmd = CommandIR.from_yaml(f)
        assert cmd.id == "brainstorm"

    def test_to_dict(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        d = cmd.to_dict()
        assert d["id"] == "brainstorm"
        assert d["schema_version"] == 1
        assert d["skill_name"] == "superclaude-brainstorm"
        assert d["aliases"] == ["/sc:brainstorm", "sc:brainstorm", "brainstorm"]
        assert d["workflow"] == ["understand_request", "generate_alternatives"]
        assert "writes_code" in d["safety"]


class TestValidation:
    def test_valid_command_passes(self):
        cmd = CommandIR.from_dict(VALID_COMMAND)
        result = validate_command(cmd)
        assert result.is_valid, [str(e) for e in result.errors]

    def test_missing_schema_version(self):
        data = {**VALID_COMMAND, "schema_version": 0}
        cmd = CommandIR.from_dict(data)
        result = validate_command(cmd)
        assert not result.is_valid
        assert any("schema_version" in e.field for e in result.errors)

    def test_unsupported_schema_version(self):
        data = {**VALID_COMMAND, "schema_version": 99}
        cmd = CommandIR.from_dict(data)
        result = validate_command(cmd)
        assert not result.is_valid

    def test_missing_id(self):
        data = {**VALID_COMMAND, "id": ""}
        cmd = CommandIR.from_dict(data)
        result = validate_command(cmd)
        assert not result.is_valid

    def test_empty_aliases(self):
        data = {**VALID_COMMAND, "aliases": []}
        cmd = CommandIR.from_dict(data)
        result = validate_command(cmd)
        assert not result.is_valid

    def test_aliases_without_sc_prefix(self):
        data = {**VALID_COMMAND, "aliases": ["brainstorm", "bs"]}
        cmd = CommandIR.from_dict(data)
        result = validate_command(cmd)
        assert not result.is_valid
        assert any("/sc:" in e.message for e in result.errors)

    def test_empty_workflow(self):
        data = {**VALID_COMMAND, "workflow": []}
        cmd = CommandIR.from_dict(data)
        result = validate_command(cmd)
        assert not result.is_valid

    def test_missing_skill_name(self):
        data = {**VALID_COMMAND, "codex": {"skill_name": ""}}
        cmd = CommandIR.from_dict(data)
        result = validate_command(cmd)
        assert not result.is_valid

    def test_missing_output_contract_primary(self):
        data = {**VALID_COMMAND, "output_contract": {"primary": ""}}
        cmd = CommandIR.from_dict(data)
        result = validate_command(cmd)
        assert not result.is_valid

    def test_duplicate_aliases(self):
        cmd1 = CommandIR.from_dict(VALID_COMMAND)
        cmd2_data = {
            **VALID_COMMAND,
            "id": "design",
            "aliases": ["/sc:brainstorm", "/sc:design"],
        }
        cmd2 = CommandIR.from_dict(cmd2_data)
        result = validate_no_duplicates([cmd1, cmd2])
        assert not result.is_valid
        assert any("duplicate" in e.message for e in result.errors)


class TestRegistry:
    def _write_yaml(self, directory: Path, name: str, data: dict) -> Path:
        f = directory / f"{name}.yaml"
        f.write_text(yaml.dump(data))
        return f

    def test_load_all(self, tmp_path):
        self._write_yaml(tmp_path, "brainstorm", VALID_COMMAND)
        reg = CommandRegistry(assets_dir=tmp_path)
        reg.load_all()
        assert len(reg.list_commands()) == 1

    def test_get_command(self, tmp_path):
        self._write_yaml(tmp_path, "brainstorm", VALID_COMMAND)
        reg = CommandRegistry(assets_dir=tmp_path)
        reg.load_all()
        cmd = reg.get_command("brainstorm")
        assert cmd is not None
        assert cmd.id == "brainstorm"

    def test_get_command_by_alias(self, tmp_path):
        self._write_yaml(tmp_path, "brainstorm", VALID_COMMAND)
        reg = CommandRegistry(assets_dir=tmp_path)
        reg.load_all()
        cmd = reg.get_command_by_alias("/sc:brainstorm")
        assert cmd is not None
        assert cmd.id == "brainstorm"

    def test_get_unknown_returns_none(self, tmp_path):
        reg = CommandRegistry(assets_dir=tmp_path)
        reg.load_all()
        assert reg.get_command("nonexistent") is None
        assert reg.get_command_by_alias("/sc:nonexistent") is None

    def test_list_by_category(self, tmp_path):
        self._write_yaml(tmp_path, "brainstorm", VALID_COMMAND)
        impl = {**VALID_COMMAND, "id": "implement", "display_name": "/sc:implement",
                "category": "development", "aliases": ["/sc:implement"],
                "codex": {"skill_name": "superclaude-implement"}}
        self._write_yaml(tmp_path, "implement", impl)
        reg = CommandRegistry(assets_dir=tmp_path)
        reg.load_all()
        cats = reg.list_by_category()
        assert "discovery" in cats
        assert "development" in cats

    def test_validate_all(self, tmp_path):
        self._write_yaml(tmp_path, "brainstorm", VALID_COMMAND)
        reg = CommandRegistry(assets_dir=tmp_path)
        reg.load_all()
        result = reg.validate_all()
        assert result.is_valid

    def test_export_commands_json(self, tmp_path):
        self._write_yaml(tmp_path, "brainstorm", VALID_COMMAND)
        reg = CommandRegistry(assets_dir=tmp_path)
        reg.load_all()
        out = reg.export_commands_json()
        assert out["schema_version"] == 1
        assert len(out["commands"]) == 1
        assert out["commands"][0]["id"] == "brainstorm"

    def test_export_commands_json_str(self, tmp_path):
        self._write_yaml(tmp_path, "brainstorm", VALID_COMMAND)
        reg = CommandRegistry(assets_dir=tmp_path)
        reg.load_all()
        s = reg.export_commands_json_str()
        parsed = json.loads(s)
        assert parsed["schema_version"] == 1

    def test_empty_directory(self, tmp_path):
        reg = CommandRegistry(assets_dir=tmp_path)
        reg.load_all()
        assert len(reg.list_commands()) == 0
