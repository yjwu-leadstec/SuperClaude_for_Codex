"""Codex plugin rendering for native slash command discovery."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from superclaude_codex import __version__
from superclaude_codex.codex.parameters import (
    format_argument_hint,
    format_examples,
    format_global_flag_lines,
    format_global_priority_lines,
    format_parameter_lines,
    format_usage,
    yaml_quote,
)
from superclaude_codex.codex.paths import assert_not_claude_path, get_superclaude_dir
from superclaude_codex.core.command_ir import CommandIR
from superclaude_codex.core.registry import CommandRegistry

PLUGIN_NAME = "superclaude-for-codex"
MARKETPLACE_NAME = "superclaude-for-codex"
BEGIN_MARKER = "# BEGIN SUPERCLAUDE FOR CODEX PLUGIN"
END_MARKER = "# END SUPERCLAUDE FOR CODEX PLUGIN"


class PluginConfigError(RuntimeError):
    """Raised when Codex plugin config cannot be updated safely."""


def get_plugin_marketplace_dir(codex_home: Path | None = None) -> Path:
    """Return the local marketplace root used for the SuperClaude plugin."""
    return get_superclaude_dir(codex_home) / "marketplace"


def get_plugin_dir(codex_home: Path | None = None) -> Path:
    """Return the native Codex plugin source root in the local marketplace."""
    return get_plugin_marketplace_dir(codex_home) / "plugins" / PLUGIN_NAME


def get_installed_plugin_dir(codex_home: Path | None = None) -> Path:
    """Return the installed plugin copy that Codex loads at runtime."""
    home = codex_home or Path.home() / ".codex"
    return home / "plugins" / "cache" / MARKETPLACE_NAME / PLUGIN_NAME / "local"


def render_plugin_manifest() -> str:
    """Render .codex-plugin/plugin.json."""
    manifest = {
        "name": PLUGIN_NAME,
        "version": __version__,
        "description": (
            "Codex-native SuperClaude workflows with 30 slash commands, "
            "specialist skills, and compatibility aliases."
        ),
        "author": {"name": "SuperClaude for Codex"},
        "homepage": "https://github.com/yjwu-leadstec/SuperClaude_for_Codex",
        "repository": "https://github.com/yjwu-leadstec/SuperClaude_for_Codex",
        "license": "MIT",
        "keywords": [
            "codex",
            "superclaude",
            "slash-commands",
            "workflow",
            "agents",
        ],
        "interface": {
            "displayName": "SuperClaude for Codex",
            "shortDescription": "Structured development workflows for Codex",
            "longDescription": (
                "Use SuperClaude for Codex to run structured planning, "
                "implementation, testing, review, documentation, and project "
                "management workflows from native slash commands. Skills are "
                "installed as standalone Codex skills to keep completion names short."
            ),
            "developerName": "SuperClaude for Codex",
            "category": "Engineering",
            "capabilities": ["Interactive", "Read", "Write"],
            "websiteURL": "https://github.com/yjwu-leadstec/SuperClaude_for_Codex",
            "privacyPolicyURL": "https://openai.com/policies/privacy-policy/",
            "termsOfServiceURL": "https://openai.com/policies/row-terms-of-use/",
            "defaultPrompt": [
                '/sc-brainstorm "design a user management API"',
                '/sc-implement "add authentication middleware"',
                "/sc-test",
            ],
            "brandColor": "#2563EB",
            "screenshots": [],
        },
    }
    return json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"


def render_marketplace_json() -> str:
    """Render the local marketplace entry that exposes the plugin."""
    marketplace = {
        "name": MARKETPLACE_NAME,
        "interface": {"displayName": "SuperClaude for Codex"},
        "plugins": [
            {
                "name": PLUGIN_NAME,
                "source": {"source": "local", "path": f"./plugins/{PLUGIN_NAME}"},
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Engineering",
            }
        ],
    }
    return json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n"


def render_plugin_command(command: CommandIR) -> str:
    """Render a native Codex slash command markdown file."""
    aliases = ", ".join(f"`{alias}`" for alias in command.aliases)
    argument_hint = format_argument_hint(command)

    lines = [
        "---",
        f"description: {yaml_quote(command.description)}",
        f"argument-hint: {yaml_quote(argument_hint)}",
        "allowed-tools: [Read, Glob, Grep, Bash, Write, Edit, WebFetch, TodoWrite]",
        "---",
        "",
        f"# {command.display_name}",
        "",
        f"Native Codex command for `{command.display_name}`.",
        "",
        "## Arguments",
        "",
        "The user invoked this command with: $ARGUMENTS",
        "",
        "## Parameters",
        "",
        f"Usage: `{format_usage(command)}`",
        "",
    ]

    parameter_lines = format_parameter_lines(command.inputs)
    if parameter_lines:
        lines.extend(parameter_lines)
    else:
        lines.append("- `[arguments]` (optional): Free-form command input.")
    lines.append("")

    lines.extend(
        [
            "## Global Flags",
            "",
            "These flags can be combined with this command when relevant:",
            "",
        ]
    )
    lines.extend(format_global_flag_lines())
    lines.append("")
    lines.extend(format_global_priority_lines())
    lines.append("")

    examples = format_examples(command)
    if examples:
        lines.extend(["## Examples", ""])
        lines.extend(f"- `{example}`" for example in examples)
        lines.append("")

    lines.extend(
        [
            "## Instructions",
            "",
            "When this command is invoked:",
            "",
            f"1. Read `~/.codex/skills/{command.codex.skill_name}/SKILL.md` for the full workflow.",
            f"2. Treat `$ARGUMENTS` as the input to `{command.display_name}`, including command-specific and global flags.",
            "3. Follow the skill workflow, safety rules, personas, and output contract.",
            "4. Prefer project-local conventions and validate the result before finishing.",
            "",
        ]
    )

    if len(command.aliases) > 1:
        lines.extend(["## Compatibility Aliases", "", aliases, ""])

    return "\n".join(lines)


def write_plugin(registry: CommandRegistry, marketplace_dir: Path) -> list[Path]:
    """Write the native plugin marketplace, manifest, and commands."""
    assert_not_claude_path(marketplace_dir)
    written: list[Path] = []

    plugin_dir = marketplace_dir / "plugins" / PLUGIN_NAME
    if plugin_dir.exists():
        shutil.rmtree(plugin_dir)

    marketplace_meta = marketplace_dir / ".agents" / "plugins"
    manifest_dir = plugin_dir / ".codex-plugin"
    commands_dir = plugin_dir / "commands"

    marketplace_meta.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    commands_dir.mkdir(parents=True, exist_ok=True)

    marketplace_path = marketplace_meta / "marketplace.json"
    marketplace_path.write_text(render_marketplace_json())
    written.append(marketplace_path)

    manifest_path = manifest_dir / "plugin.json"
    manifest_path.write_text(render_plugin_manifest())
    written.append(manifest_path)

    for command in registry.list_commands():
        command_name = command.display_name.removeprefix("/")
        command_path = commands_dir / f"{command_name}.md"
        command_path.write_text(render_plugin_command(command))
        written.append(command_path)

    return written


def install_plugin_cache(codex_home: Path) -> Path:
    """Copy the source plugin into Codex's installed plugin cache."""
    assert_not_claude_path(codex_home)
    source = get_plugin_dir(codex_home)
    installed = get_installed_plugin_dir(codex_home)
    if installed.exists():
        shutil.rmtree(installed)
    installed.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, installed)
    return installed


def render_plugin_config_block(codex_home: Path, timestamp: str | None = None) -> str:
    """Render config.toml entries that register and enable the local plugin."""
    assert_not_claude_path(codex_home)
    marketplace_dir = get_plugin_marketplace_dir(codex_home)
    timestamp = timestamp or datetime.now(timezone.utc).isoformat()
    source = json.dumps(str(marketplace_dir))

    return "\n".join(
        [
            BEGIN_MARKER,
            f"[marketplaces.{MARKETPLACE_NAME}]",
            f'last_updated = "{timestamp}"',
            'source_type = "local"',
            f"source = {source}",
            "",
            f'[plugins."{PLUGIN_NAME}@{MARKETPLACE_NAME}"]',
            "enabled = true",
            END_MARKER,
        ]
    )


def update_config_toml(path: Path, block: str) -> None:
    """Insert or replace the SuperClaude plugin block in config.toml."""
    assert_not_claude_path(path)

    if path.exists():
        content = path.read_text()
        backup = path.with_suffix(".toml.bak")
        fd = os.open(str(backup), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            os.write(fd, content.encode())
        finally:
            os.close(fd)

        start = content.find(BEGIN_MARKER)
        end = content.find(END_MARKER)
        if (start == -1) != (end == -1):
            raise PluginConfigError(
                f"Corrupt marker state in {path}: only one plugin marker found. "
                "Fix manually or delete the file to reinstall."
            )
        if start != -1 and end != -1:
            new_content = content[:start] + block + content[end + len(END_MARKER) :]
        else:
            sep = "\n\n" if content.strip() else ""
            new_content = content + sep + block + "\n"
    else:
        new_content = block + "\n"

    path.parent.mkdir(parents=True, exist_ok=True)
    original_mode = path.stat().st_mode if path.exists() else 0o600
    tmp_fd, tmp_path = tempfile.mkstemp(
        dir=str(path.parent), prefix=".config-", suffix=".tmp"
    )
    try:
        with os.fdopen(tmp_fd, "w") as tmp_f:
            tmp_f.write(new_content)
        os.chmod(tmp_path, original_mode)
        os.replace(tmp_path, str(path))
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
