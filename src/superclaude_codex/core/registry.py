"""Command registry — loads, indexes, and exports command IR assets.

The registry is the single source of truth for all /sc:* commands.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .command_ir import CommandIR
from .validation import ValidationResult, validate_command, validate_no_duplicates

# Default assets directory inside the package
_ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets" / "commands"


class CommandRegistry:
    """Load and query CommandIR definitions."""

    def __init__(self, assets_dir: Path | None = None):
        self._assets_dir = assets_dir or _ASSETS_DIR
        self._commands: dict[str, CommandIR] = {}
        self._alias_index: dict[str, str] = {}

    def load_all(self) -> None:
        """Load all YAML files from the assets directory."""
        self._commands.clear()
        self._alias_index.clear()
        if not self._assets_dir.is_dir():
            return
        for path in sorted(self._assets_dir.glob("*.yaml")):
            cmd = CommandIR.from_yaml(path)
            self._commands[cmd.id] = cmd
            for alias in cmd.aliases:
                self._alias_index[alias] = cmd.id

    def get_command(self, cmd_id: str) -> CommandIR | None:
        return self._commands.get(cmd_id)

    def get_command_by_alias(self, alias: str) -> CommandIR | None:
        cmd_id = self._alias_index.get(alias)
        if cmd_id:
            return self._commands.get(cmd_id)
        return None

    def list_commands(self) -> list[CommandIR]:
        return list(self._commands.values())

    def list_by_category(self) -> dict[str, list[CommandIR]]:
        groups: dict[str, list[CommandIR]] = {}
        for cmd in self._commands.values():
            cat = cmd.category or "uncategorized"
            groups.setdefault(cat, []).append(cmd)
        return groups

    def validate_all(self) -> ValidationResult:
        """Validate all loaded commands."""
        combined = ValidationResult()
        for cmd in self._commands.values():
            r = validate_command(cmd)
            combined.errors.extend(r.errors)
        dup = validate_no_duplicates(list(self._commands.values()))
        combined.errors.extend(dup.errors)
        return combined

    def export_commands_json(self, package_version: str = "0.1.0") -> dict[str, Any]:
        """Generate the commands.json structure."""
        return {
            "schema_version": 1,
            "package_version": package_version,
            "commands": [cmd.to_dict() for cmd in self._commands.values()],
        }

    def export_commands_json_str(self, package_version: str = "0.1.0") -> str:
        return json.dumps(
            self.export_commands_json(package_version), indent=2, ensure_ascii=False
        )
