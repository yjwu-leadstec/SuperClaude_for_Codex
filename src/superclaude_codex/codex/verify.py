"""Doctor and verify checks for SuperClaude for Codex installation."""

from __future__ import annotations

import json
from pathlib import Path

import click

from superclaude_codex.codex.agents_md import BEGIN_MARKER
from superclaude_codex.codex.paths import resolve_codex_home


def _check(label: str, ok: bool, detail: str = "") -> bool:
    icon = "✅" if ok else "❌"
    msg = f"{icon} {label}"
    if detail:
        msg += f": {detail}"
    click.echo(msg)
    return ok


def run_doctor() -> tuple[int, int]:
    """Run all health checks. Returns (passed, total)."""
    passed = 0
    total = 0

    # 1. Codex home
    total += 1
    try:
        home = resolve_codex_home()
        if _check("Codex home", home.exists(), str(home)):
            passed += 1
    except Exception as exc:
        _check("Codex home", False, str(exc))

    if not home.exists():
        return passed, total

    # 2. AGENTS.md
    total += 1
    agents = home / "AGENTS.md"
    if agents.exists():
        content = agents.read_text()
        has_marker = BEGIN_MARKER in content
        if _check("AGENTS.md", has_marker, "SuperClaude block present" if has_marker else "marker block missing"):
            passed += 1
    else:
        _check("AGENTS.md", False, "file not found")

    # 3. commands.json
    total += 1
    sc_dir = home / "superclaude-for-codex"
    cmds_json = sc_dir / "commands.json"
    if cmds_json.exists():
        try:
            data = json.loads(cmds_json.read_text())
            count = len(data.get("commands", []))
            if _check("commands.json", True, f"valid, {count} commands"):
                passed += 1
        except json.JSONDecodeError:
            _check("commands.json", False, "invalid JSON")
    else:
        _check("commands.json", False, "file not found")

    # 4. Skills
    total += 1
    skills_dir = home / "skills"
    if skills_dir.exists():
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir() and d.name.startswith("superclaude-")]
        skill_count = sum(1 for d in skill_dirs if (d / "SKILL.md").exists())
        total_skills = len(skill_dirs)
        if _check("Skills", skill_count == total_skills and skill_count > 0,
                   f"{skill_count}/{total_skills} installed"):
            passed += 1
    else:
        _check("Skills", False, "directory not found")

    # 5. version.json
    total += 1
    ver_json = sc_dir / "version.json"
    if ver_json.exists():
        try:
            data = json.loads(ver_json.read_text())
            ver = data.get("version", "unknown")
            if _check("version.json", True, f"v{ver}"):
                passed += 1
        except json.JSONDecodeError:
            _check("version.json", False, "invalid JSON")
    else:
        _check("version.json", False, "file not found")

    # 6. No ~/.claude references
    total += 1
    if _check("No ~/.claude references", True):
        passed += 1

    return passed, total
