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


class AgentsBlockError(ValueError):
    """Raised when AGENTS.md has corrupted marker state."""


def extract_existing_block(content: str) -> str | None:
    """Extract the existing SuperClaude marker block, if present.

    Raises AgentsBlockError if markers are in invalid state:
    - Only one marker present (BEGIN without END or vice versa)
    - Multiple BEGIN markers
    - END appears before BEGIN
    """
    begin_count = content.count(BEGIN_MARKER)
    end_count = content.count(END_MARKER)

    if begin_count == 0 and end_count == 0:
        return None

    if begin_count != end_count or begin_count > 1:
        raise AgentsBlockError(
            f"AGENTS.md has corrupted markers: {begin_count} BEGIN, {end_count} END. "
            "Fix manually or delete the file and reinstall."
        )

    start = content.find(BEGIN_MARKER)
    end = content.find(END_MARKER)

    if end < start:
        raise AgentsBlockError(
            "AGENTS.md markers are in wrong order (END before BEGIN). "
            "Fix manually or delete the file and reinstall."
        )

    return content[start : end + len(END_MARKER)]


def update_agents_md(path: Path, block: str) -> None:
    """Insert or replace the SuperClaude block in AGENTS.md.

    - If file doesn't exist, creates it with just the block.
    - If valid marker block exists, replaces it.
    - If no markers, appends to end.
    - Raises AgentsBlockError if markers are in invalid state.
    - Never modifies content outside the markers.
    """
    max_size = 1_048_576  # 1 MB
    if path.exists():
        if path.stat().st_size > max_size:
            raise AgentsBlockError(
                f"AGENTS.md is too large ({path.stat().st_size} bytes, max {max_size}). "
                "This may be a binary file or corrupted."
            )
        content = path.read_text()
        existing = extract_existing_block(content)  # may raise
        if existing:
            new_content = content.replace(existing, block)
        else:
            sep = "\n\n" if content.strip() else ""
            new_content = content + sep + block + "\n"
    else:
        new_content = block + "\n"

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new_content)
