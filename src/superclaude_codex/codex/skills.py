"""Skill renderer — generates Codex SKILL.md files from Command IR.

Each command produces a skill directory:
    ~/.codex/skills/superclaude-{id}/SKILL.md
"""

from __future__ import annotations

from pathlib import Path

from superclaude_codex.core.command_ir import CommandIR
from superclaude_codex.core.registry import CommandRegistry


def render_skill(command: CommandIR) -> str:
    """Render a SKILL.md from a CommandIR."""
    lines = [
        "---",
        f"name: {command.codex.skill_name}",
        f"description: {command.description}",
        "---",
        "",
        f"# {command.display_name}",
        "",
    ]

    # When to use
    if command.triggers:
        lines.append("## When to Use")
        lines.append("")
        lines.append(f"Use this skill when the user invokes `{command.display_name}`.")
        lines.append("Also activate when:")
        for trigger in command.triggers:
            lines.append(f"- {trigger}")
        lines.append("")

    # Aliases
    if len(command.aliases) > 1:
        lines.append("## Aliases")
        lines.append("")
        for alias in command.aliases:
            lines.append(f"- `{alias}`")
        lines.append("")

    # Workflow
    if command.workflow:
        lines.append("## Workflow")
        lines.append("")
        for i, step in enumerate(command.workflow, 1):
            lines.append(f"{i}. {step.replace('_', ' ').capitalize()}")
        lines.append("")

    # Personas
    if command.personas:
        lines.append("## Personas")
        lines.append("")
        for persona in command.personas:
            lines.append(f"- Activate **{persona}** when relevant to the task.")
        lines.append("")

    # MCP
    optional_mcp = command.mcp.get("optional", [])
    if optional_mcp:
        lines.append("## MCP Servers")
        lines.append("")
        lines.append("Optionally leverage:")
        for server in optional_mcp:
            lines.append(f"- {server}")
        lines.append("")

    # Safety
    lines.append("## Safety")
    lines.append("")
    if not command.safety.writes_code:
        lines.append("Do not write or modify code unless the user explicitly requests it.")
    if command.safety.requires_user_confirmation_for_scope_change:
        lines.append(
            "Ask for user confirmation before changing scope beyond the original request."
        )
    lines.append("")

    # Output contract
    if command.output_contract.primary:
        lines.append("## Output")
        lines.append("")
        lines.append(
            f"Return a structured **{command.output_contract.primary.replace('_', ' ')}**"
            " containing:"
        )
        for section in command.output_contract.required_sections:
            lines.append(f"- {section.replace('_', ' ').capitalize()}")
        lines.append("")

    # Completion
    lines.append("## Completion")
    lines.append("")
    lines.append(
        f"After completing `{command.display_name}`, suggest relevant follow-up commands."
    )
    lines.append("")

    return "\n".join(lines)


def write_skill(codex_home: Path, command: CommandIR) -> Path:
    """Write a SKILL.md file for a command."""
    skill_dir = codex_home / "skills" / command.codex.skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_path = skill_dir / "SKILL.md"
    skill_path.write_text(render_skill(command))
    return skill_path


def render_all_skills(registry: CommandRegistry, codex_home: Path) -> list[Path]:
    """Render SKILL.md for all commands in the registry."""
    paths = []
    for cmd in registry.list_commands():
        paths.append(write_skill(codex_home, cmd))
    return paths
