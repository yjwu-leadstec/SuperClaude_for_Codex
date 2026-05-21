"""Doctor and verify checks for SuperClaude for Codex installation."""

from __future__ import annotations

import json
from pathlib import Path

import click

from superclaude_codex.codex.agents_md import (
    BEGIN_MARKER,
    END_MARKER,
    AgentsBlockError,
    extract_existing_block,
)
from superclaude_codex.codex.paths import resolve_codex_home
from superclaude_codex.codex.plugin import (
    BEGIN_MARKER as PLUGIN_BEGIN,
)
from superclaude_codex.codex.plugin import (
    END_MARKER as PLUGIN_END,
)
from superclaude_codex.codex.plugin import (
    get_installed_plugin_dir,
    get_plugin_dir,
)


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
    home: Path | None = None
    try:
        home = resolve_codex_home()
        if _check("Codex home", home.exists(), str(home)):
            passed += 1
    except Exception as exc:
        _check("Codex home", False, str(exc))

    if home is None or not home.exists():
        return passed, total

    # 2. AGENTS.md
    total += 1
    agents = home / "AGENTS.md"
    if agents.exists():
        content = agents.read_text()
        try:
            block = extract_existing_block(content)
            if block and BEGIN_MARKER in block and END_MARKER in block:
                if _check("AGENTS.md", True, "SuperClaude block present"):
                    passed += 1
            else:
                _check("AGENTS.md", False, "marker block missing")
        except AgentsBlockError as exc:
            _check("AGENTS.md", False, f"corrupt markers: {exc}")
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

    # 4. agents.json
    total += 1
    agents_json = sc_dir / "agents.json"
    if agents_json.exists():
        try:
            data = json.loads(agents_json.read_text())
            count = len(data.get("agents", []))
            if _check("agents.json", True, f"valid, {count} agents"):
                passed += 1
        except json.JSONDecodeError:
            _check("agents.json", False, "invalid JSON")
    else:
        _check("agents.json", False, "file not found")

    # 5. Skills
    total += 1
    skills_dir = home / "skills"
    if skills_dir.exists():
        skill_dirs = [
            d
            for d in skills_dir.iterdir()
            if d.is_dir() and d.name.startswith("superclaude-")
        ]
        skill_count = sum(1 for d in skill_dirs if (d / "SKILL.md").exists())
        metadata_count = sum(
            1 for d in skill_dirs if (d / "agents" / "openai.yaml").exists()
        )
        total_skills = len(skill_dirs)
        if _check(
            "Skills",
            skill_count == total_skills
            and metadata_count == total_skills
            and skill_count > 0,
            f"{skill_count}/{total_skills} installed, {metadata_count}/{total_skills} UI metadata",
        ):
            passed += 1
    else:
        _check("Skills", False, "directory not found")

    # 6. Native plugin
    total += 1
    plugin_dir = get_plugin_dir(home)
    installed_plugin_dir = get_installed_plugin_dir(home)
    commands_dir = plugin_dir / "commands"
    installed_commands_dir = installed_plugin_dir / "commands"
    source_skill_exports = plugin_dir / "skills"
    installed_skill_exports = installed_plugin_dir / "skills"
    plugin_json = plugin_dir / ".codex-plugin" / "plugin.json"
    installed_plugin_json = installed_plugin_dir / ".codex-plugin" / "plugin.json"
    config_toml = home / "config.toml"
    command_count = (
        len([p for p in commands_dir.glob("*.md") if p.is_file()])
        if commands_dir.exists()
        else 0
    )
    installed_command_count = (
        len([p for p in installed_commands_dir.glob("*.md") if p.is_file()])
        if installed_commands_dir.exists()
        else 0
    )
    config_ok = (
        config_toml.exists()
        and PLUGIN_BEGIN in config_toml.read_text()
        and PLUGIN_END in config_toml.read_text()
    )
    plugin_present = (
        plugin_json.exists()
        or installed_plugin_json.exists()
        or command_count > 0
        or installed_command_count > 0
        or config_ok
    )
    plugin_skills_hidden = (
        not source_skill_exports.exists() and not installed_skill_exports.exists()
    )
    if not plugin_present:
        plugin_ok = True
        plugin_detail = "disabled (standalone skills mode)"
    else:
        plugin_ok = (
            plugin_json.exists()
            and command_count == 30
            and installed_plugin_json.exists()
            and installed_command_count == 30
            and config_ok
            and plugin_skills_hidden
        )
        plugin_detail = (
            f"{command_count}/30 source, {installed_command_count}/30 installed, "
            "plugin skills hidden"
        )
        if not config_ok:
            plugin_detail = "config block missing"
        elif not plugin_skills_hidden:
            plugin_detail = "plugin skill exports present"
    if _check("Native plugin", plugin_ok, plugin_detail):
        passed += 1

    # 7. version.json
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

    # 8. No ~/.claude references — scan install artifacts
    total += 1
    claude_refs = []
    for f in sc_dir.rglob("*.json"):
        content = f.read_text()
        if "/.claude" in content:
            claude_refs.append(str(f))
    if agents.exists():
        content = agents.read_text()
        # The AGENTS.md legitimately tells Codex NOT to touch ~/.claude;
        # only flag if there's an actual path pointing into it.
        for line in content.splitlines():
            if (
                "/.claude/" in line
                and "Do not" not in line
                and "read or write" not in line
            ):
                claude_refs.append(f"AGENTS.md: {line.strip()}")
    if _check(
        "No ~/.claude references",
        len(claude_refs) == 0,
        "; ".join(claude_refs) if claude_refs else "clean",
    ):
        passed += 1

    return passed, total
