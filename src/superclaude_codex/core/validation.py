"""Command IR schema validation.

Validates that command YAML files meet the required schema before
they can be registered or rendered.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .command_ir import CommandIR

CURRENT_SCHEMA_VERSION = 1

REQUIRED_FIELDS = [
    "schema_version",
    "id",
    "display_name",
    "aliases",
    "workflow",
]


@dataclass
class ValidationError:
    command_id: str
    field: str
    message: str


@dataclass
class ValidationResult:
    errors: list[ValidationError] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add(self, command_id: str, fld: str, msg: str) -> None:
        self.errors.append(ValidationError(command_id, fld, msg))


def validate_command(cmd: CommandIR) -> ValidationResult:
    """Validate a single CommandIR against the schema."""
    result = ValidationResult()
    cid = cmd.id or "<unknown>"

    if not cmd.schema_version:
        result.add(cid, "schema_version", "missing or zero")
    elif cmd.schema_version > CURRENT_SCHEMA_VERSION:
        result.add(
            cid,
            "schema_version",
            f"unsupported version {cmd.schema_version} (max: {CURRENT_SCHEMA_VERSION})",
        )

    if not cmd.id:
        result.add(cid, "id", "missing")

    if not cmd.description:
        result.add(cid, "description", "missing — every command must have a description")

    if not cmd.display_name:
        result.add(cid, "display_name", "missing")

    if not cmd.aliases:
        result.add(cid, "aliases", "empty — must contain at least one alias")
    else:
        has_sc = any(a.startswith("/sc:") for a in cmd.aliases)
        if not has_sc:
            result.add(cid, "aliases", "must contain at least one /sc:* alias")

    if not cmd.workflow:
        result.add(cid, "workflow", "empty — must contain at least one step")

    if not cmd.codex.skill_name:
        result.add(cid, "codex.skill_name", "missing")

    if not cmd.output_contract.primary:
        result.add(cid, "output_contract.primary", "missing")

    if not cmd.safety:
        result.add(cid, "safety", "missing")

    return result


def validate_no_duplicates(commands: list[CommandIR]) -> ValidationResult:
    """Check for duplicate aliases across all commands."""
    result = ValidationResult()
    seen: dict[str, str] = {}
    for cmd in commands:
        for alias in cmd.aliases:
            if alias in seen:
                result.add(
                    cmd.id,
                    "aliases",
                    f"duplicate alias '{alias}' (already used by '{seen[alias]}')",
                )
            else:
                seen[alias] = cmd.id
    return result
