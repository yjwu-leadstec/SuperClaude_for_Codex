"""AGENTS.md renderer — generates and updates the SuperClaude routing block.

Only modifies content between the marker comments. Never overwrites
user-written content outside the markers.
"""

from __future__ import annotations

from pathlib import Path

from superclaude_codex.core.registry import CommandRegistry

BEGIN_MARKER = "<!-- BEGIN SUPERCLAUDE FOR CODEX -->"
END_MARKER = "<!-- END SUPERCLAUDE FOR CODEX -->"


def render_agents_block(registry: CommandRegistry) -> str:
    """Generate the AGENTS.md routing block from the command registry."""
    commands = registry.list_commands()
    lines = [
        BEGIN_MARKER,
        "## SuperClaude for Codex",
        "",
        "This Codex environment has SuperClaude for Codex installed.",
        "",
        "When the user invokes a command matching `/sc:*`, treat it as a SuperClaude command.",
        "Resolve the command through the installed SuperClaude command registry.",
        "Prefer the matching skill in `~/.codex/skills/superclaude-*`.",
        "",
        "### Available Commands",
        "",
    ]
    for cmd in sorted(commands, key=lambda c: c.display_name):
        lines.append(f"- `{cmd.display_name}` — {cmd.description}")
    lines.extend([
        "",
        "### Routing",
        "",
    ])
    for cmd in sorted(commands, key=lambda c: c.display_name):
        lines.append(
            f"- `{cmd.display_name}` uses the `{cmd.codex.skill_name}` skill."
        )
    lines.extend([
        "",
        "Do not look for or modify Claude Code configuration.",
        "Do not read or write `~/.claude`.",
        END_MARKER,
    ])
    return "\n".join(lines)


def extract_existing_block(content: str) -> str | None:
    """Extract the existing SuperClaude marker block, if present."""
    start = content.find(BEGIN_MARKER)
    end = content.find(END_MARKER)
    if start == -1 or end == -1:
        return None
    return content[start : end + len(END_MARKER)]


def update_agents_md(path: Path, block: str) -> None:
    """Insert or replace the SuperClaude block in AGENTS.md.

    - If file doesn't exist, creates it with just the block.
    - If marker block exists, replaces it.
    - If no marker block, appends to end.
    - Never modifies content outside the markers.
    """
    if path.exists():
        content = path.read_text()
        existing = extract_existing_block(content)
        if existing:
            new_content = content.replace(existing, block)
        else:
            sep = "\n\n" if content.strip() else ""
            new_content = content + sep + block + "\n"
    else:
        new_content = block + "\n"

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new_content)
