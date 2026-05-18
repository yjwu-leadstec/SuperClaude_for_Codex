"""Command IR (Intermediate Representation) data model.

Every /sc:* command is defined as a versioned YAML file and loaded
into a CommandIR dataclass. Renderers then produce Codex skills,
AGENTS.md routes, and commands.json from these IR objects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class SafetySpec:
    writes_code: bool = False
    writes_files: bool = False
    requires_user_confirmation_for_scope_change: bool = True


@dataclass
class OutputContract:
    primary: str = ""
    required_sections: list[str] = field(default_factory=list)


@dataclass
class CodexSpec:
    skill_name: str = ""
    default_reasoning: str = "medium"
    web_search: str = "optional"


@dataclass
class CommandIR:
    schema_version: int
    id: str
    display_name: str
    category: str = ""
    description: str = ""
    aliases: list[str] = field(default_factory=list)
    triggers: list[str] = field(default_factory=list)
    inputs: dict[str, Any] = field(default_factory=dict)
    workflow: list[str] = field(default_factory=list)
    personas: list[str] = field(default_factory=list)
    mcp: dict[str, list[str]] = field(default_factory=dict)
    safety: SafetySpec = field(default_factory=SafetySpec)
    output_contract: OutputContract = field(default_factory=OutputContract)
    codex: CodexSpec = field(default_factory=CodexSpec)

    @classmethod
    def from_yaml(cls, path: Path) -> CommandIR:
        """Load a CommandIR from a YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CommandIR:
        """Construct a CommandIR from a raw dictionary."""
        safety_data = data.get("safety", {})
        safety = SafetySpec(
            writes_code=safety_data.get("writes_code", False),
            writes_files=safety_data.get("writes_files", False),
            requires_user_confirmation_for_scope_change=safety_data.get(
                "requires_user_confirmation_for_scope_change", True
            ),
        )

        oc_data = data.get("output_contract", {})
        output_contract = OutputContract(
            primary=oc_data.get("primary", ""),
            required_sections=oc_data.get("required_sections", []),
        )

        codex_data = data.get("codex", {})
        codex = CodexSpec(
            skill_name=codex_data.get("skill_name", ""),
            default_reasoning=codex_data.get("default_reasoning", "medium"),
            web_search=codex_data.get("web_search", "optional"),
        )

        return cls(
            schema_version=data.get("schema_version", 0),
            id=data.get("id", ""),
            display_name=data.get("display_name", ""),
            category=data.get("category", ""),
            description=data.get("description", ""),
            aliases=data.get("aliases", []),
            triggers=data.get("triggers", []),
            inputs=data.get("inputs", {}),
            workflow=data.get("workflow", []),
            personas=data.get("personas", []),
            mcp=data.get("mcp", {}),
            safety=safety,
            output_contract=output_contract,
            codex=codex,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a dictionary for commands.json."""
        return {
            "id": self.id,
            "display_name": self.display_name,
            "category": self.category,
            "aliases": self.aliases,
            "skill_name": self.codex.skill_name,
        }
