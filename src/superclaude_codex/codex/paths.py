"""Codex home directory resolution and path safety guards.

All file operations in superclaude-for-codex MUST go through these
functions to ensure we never read or write ~/.claude or system paths.
"""

import os
from pathlib import Path


class ClaudePathError(ValueError):
    """Raised when an operation would touch ~/.claude."""


class UnsafePathError(ValueError):
    """Raised when CODEX_HOME points to a dangerous system path."""


# System paths that must never be used as CODEX_HOME
# Paths where rmtree/write could cause real damage.
# /tmp excluded: pytest tmp_path lives there and is safe for install tests.
_FORBIDDEN_PATHS = frozenset({
    "/", "/etc", "/usr", "/var", "/bin", "/sbin", "/lib",
    "/sys", "/proc", "/dev", "/boot", "/opt",
})


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
    assert_safe_path(path)
    return path


def assert_not_claude_path(path: Path) -> None:
    """Raise ClaudePathError if path is under ~/.claude."""
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
        raise ClaudePathError(
            f"Refusing to operate on ~/.claude path: {path}\n"
            "SuperClaude for Codex only writes to ~/.codex."
        )


def assert_safe_path(path: Path) -> None:
    """Raise UnsafePathError if path IS a system-critical directory.

    Blocks exact matches like /etc, /usr, / but allows subdirectories
    like /etc/superclaude-codex (a dedicated dir is fine to own).
    """
    try:
        resolved = path.resolve()
    except OSError:
        resolved = path

    # Build set of forbidden exact paths + macOS /private/* equivalents
    forbidden: set[Path] = set()
    for p in _FORBIDDEN_PATHS:
        forbidden.add(Path(p))
        try:
            forbidden.add(Path(p).resolve())
        except OSError:
            pass

    if resolved in forbidden:
        raise UnsafePathError(
            f"Refusing to use system path as CODEX_HOME: {path}\n"
            "Set CODEX_HOME to a user-writable directory like ~/.codex."
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
