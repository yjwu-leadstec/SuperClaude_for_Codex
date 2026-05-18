"""Codex home directory resolution and path safety guards.

All file operations in superclaude-for-codex MUST go through these
functions to ensure we never read or write ~/.claude.
"""

import os
from pathlib import Path


class ClaudePathViolation(ValueError):
    """Raised when an operation would touch ~/.claude."""


def resolve_codex_home() -> Path:
    """Resolve the Codex home directory.

    Priority:
        1. CODEX_HOME environment variable
        2. ~/.codex (default)
    """
    env = os.environ.get("CODEX_HOME")
    if env:
        path = Path(env)
    else:
        path = Path.home() / ".codex"
    assert_not_claude_path(path)
    return path


def assert_not_claude_path(path: Path) -> None:
    """Raise ClaudePathViolation if path is under ~/.claude."""
    try:
        resolved = path.resolve()
    except OSError:
        resolved = path

    claude_dir = Path.home() / ".claude"
    try:
        claude_resolved = claude_dir.resolve()
    except OSError:
        claude_resolved = claude_dir

    if resolved == claude_resolved or claude_resolved in resolved.parents:
        raise ClaudePathViolation(
            f"Refusing to operate on ~/.claude path: {path}\n"
            "SuperClaude for Codex only writes to ~/.codex."
        )


def get_agents_md_path(codex_home: Path | None = None) -> Path:
    """Return path to AGENTS.md."""
    home = codex_home or resolve_codex_home()
    assert_not_claude_path(home)
    return home / "AGENTS.md"


def get_config_toml_path(codex_home: Path | None = None) -> Path:
    """Return path to config.toml."""
    home = codex_home or resolve_codex_home()
    assert_not_claude_path(home)
    return home / "config.toml"


def get_skills_dir(codex_home: Path | None = None) -> Path:
    """Return path to skills directory."""
    home = codex_home or resolve_codex_home()
    assert_not_claude_path(home)
    return home / "skills"


def get_superclaude_dir(codex_home: Path | None = None) -> Path:
    """Return path to superclaude-for-codex data directory."""
    home = codex_home or resolve_codex_home()
    assert_not_claude_path(home)
    return home / "superclaude-for-codex"
