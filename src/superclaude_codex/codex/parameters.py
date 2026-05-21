"""Helpers for rendering command parameters and argument hints."""

from __future__ import annotations

from typing import Any

from superclaude_codex.core.command_ir import CommandIR
from superclaude_codex.core.global_flags import load_global_flags

ARGUMENT_HINT_LIMIT = 120


def display_name(name: str) -> str:
    """Return a human-friendly argument token name."""
    return name.replace("_", "-")


def yaml_quote(value: str) -> str:
    """Quote a YAML frontmatter scalar."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def flag_name(flag: dict[str, Any]) -> str:
    return f"--{flag.get('name', '?')}"


def flag_names(flag: dict[str, Any]) -> str:
    names = [flag_name(flag)]
    names.extend(f"--{alias}" for alias in flag.get("aliases", []))
    return " / ".join(f"`{name}`" for name in names)


def is_boolean_flag(flag: dict[str, Any]) -> bool:
    return flag.get("type") == "boolean" or isinstance(flag.get("default"), bool)


def flag_value_hint(flag: dict[str, Any]) -> str:
    if flag.get("values"):
        return "|".join(str(v) for v in flag["values"])
    if is_boolean_flag(flag):
        return ""
    if flag.get("type") == "integer":
        return f"<{flag.get('value_name', 'n')}>"
    return f"<{flag.get('value_name', 'value')}>"


def format_argument_hint(
    command: CommandIR, max_length: int = ARGUMENT_HINT_LIMIT
) -> str:
    """Build the Codex argument-hint string for a command."""
    positionals = [
        f"[{display_name(p.get('name', 'argument'))}]"
        for p in command.inputs.get("positional", [])
    ]
    flags = []
    for flag in command.inputs.get("flags", []):
        value = flag_value_hint(flag)
        suffix = f" {value}" if value else ""
        flags.append(f"[{flag_name(flag)}{suffix}]")

    parts = positionals + flags
    if not parts:
        parts = ["[arguments]"]
    full = " ".join(parts + ["[global-flags]"])
    if len(full) <= max_length:
        return full

    compact_parts = positionals[:]
    for flag in flags:
        candidate = " ".join(compact_parts + [flag, "[global-flags]"])
        if len(candidate) > max_length:
            break
        compact_parts.append(flag)
    if not compact_parts:
        compact_parts = positionals[:1] or ["[arguments]"]
    return " ".join(compact_parts + ["[global-flags]"])


def format_usage(command: CommandIR) -> str:
    """Return a compact usage line using the generated argument hint."""
    return f"{command.display_name} {format_argument_hint(command)}".strip()


def format_parameter_lines(inputs: dict[str, Any]) -> list[str]:
    """Render command-specific positional and flag metadata."""
    lines: list[str] = []
    for positional in inputs.get("positional", []):
        req = "required" if positional.get("required") else "optional"
        desc = positional.get("description", "")
        lines.append(
            f"- `[{display_name(positional.get('name', 'argument'))}]` ({req}): {desc}"
        )

    for flag in inputs.get("flags", []):
        value = flag_value_hint(flag)
        value_text = f" `{value}`" if value else ""
        default = f" Default: `{flag['default']}`." if "default" in flag else ""
        desc = flag.get("description", "")
        lines.append(f"- {flag_names(flag)}{value_text}: {desc}{default}")
    return lines


def format_global_flag_lines(limit: int | None = None) -> list[str]:
    """Render shared global flag metadata."""
    flags = load_global_flags()["flags"]
    if limit is not None:
        flags = flags[:limit]
    lines: list[str] = []
    for flag in flags:
        value = flag_value_hint(flag)
        value_text = f" `{value}`" if value else ""
        lines.append(f"- {flag_names(flag)}{value_text}: {flag.get('description', '')}")
    return lines


def format_global_priority_lines() -> list[str]:
    return [f"- {rule}" for rule in load_global_flags().get("priority_rules", [])]


def format_examples(command: CommandIR) -> list[str]:
    """Return examples declared in command inputs, if present."""
    return list(command.inputs.get("examples", []))
