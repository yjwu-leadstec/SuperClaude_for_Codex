"""Uninstaller for SuperClaude for Codex.

Removes only SuperClaude-managed assets, preserving user content.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from superclaude_codex.codex.agents_md import BEGIN_MARKER, END_MARKER
from superclaude_codex.codex.mcp import BEGIN_MARKER as MCP_BEGIN
from superclaude_codex.codex.mcp import END_MARKER as MCP_END
from superclaude_codex.codex.paths import (
    assert_not_claude_path,
    get_agents_md_path,
    get_config_toml_path,
    get_skills_dir,
    get_superclaude_dir,
    resolve_codex_home,
)
from superclaude_codex.codex.plugin import BEGIN_MARKER as PLUGIN_BEGIN
from superclaude_codex.codex.plugin import END_MARKER as PLUGIN_END
from superclaude_codex.codex.plugin import get_installed_plugin_dir


def uninstall(codex_home: Path | None = None, dry_run: bool = False) -> list[str]:
    """Remove SuperClaude for Codex assets. Returns list of actions taken."""
    home = codex_home or resolve_codex_home()
    assert_not_claude_path(home)
    actions = []

    # 1. Remove skills directories
    skills_dir = get_skills_dir(home)
    if skills_dir.exists():
        for d in skills_dir.iterdir():
            if d.is_dir() and d.name.startswith("superclaude-"):
                if dry_run:
                    actions.append(f"[dry-run] Would remove: {d}")
                else:
                    shutil.rmtree(d)
                    actions.append(f"Removed: {d}")

    # 2. Remove superclaude-for-codex data directory
    sc_dir = get_superclaude_dir(home)
    if sc_dir.exists():
        if dry_run:
            actions.append(f"[dry-run] Would remove: {sc_dir}")
        else:
            shutil.rmtree(sc_dir)
            actions.append(f"Removed: {sc_dir}")

    installed_plugin_dir = get_installed_plugin_dir(home)
    if installed_plugin_dir.exists():
        if dry_run:
            actions.append(f"[dry-run] Would remove: {installed_plugin_dir}")
        else:
            shutil.rmtree(installed_plugin_dir)
            actions.append(f"Removed: {installed_plugin_dir}")

    # 3. Remove AGENTS.md marker block
    agents_path = get_agents_md_path(home)
    if agents_path.exists():
        content = agents_path.read_text()
        start = content.find(BEGIN_MARKER)
        end = content.find(END_MARKER)
        if start != -1 and end != -1:
            # Remove marker block while preserving surrounding whitespace
            new_content = content[:start] + content[end + len(END_MARKER) :]
            # Collapse multiple blank lines left by removal, but keep file format
            new_content = re.sub(r"\n{3,}", "\n\n", new_content)
            if not new_content.strip():
                new_content = ""
            if dry_run:
                actions.append(
                    "[dry-run] Would remove SuperClaude block from AGENTS.md"
                )
            else:
                agents_path.write_text(new_content)
                actions.append("Removed SuperClaude block from AGENTS.md")

    # 4. Remove MCP marker block from config.toml
    config_path = get_config_toml_path(home)
    if config_path.exists():
        content = config_path.read_text()
        start = content.find(PLUGIN_BEGIN)
        end = content.find(PLUGIN_END)
        if start != -1 and end != -1:
            new_content = content[:start] + content[end + len(PLUGIN_END) :]
            new_content = re.sub(r"\n{3,}", "\n\n", new_content)
            if not new_content.strip():
                new_content = ""
            if dry_run:
                actions.append("[dry-run] Would remove plugin block from config.toml")
            else:
                config_path.write_text(new_content)
                actions.append("Removed plugin block from config.toml")
            content = new_content

        start = content.find(MCP_BEGIN)
        end = content.find(MCP_END)
        if start != -1 and end != -1:
            new_content = content[:start] + content[end + len(MCP_END) :]
            new_content = re.sub(r"\n{3,}", "\n\n", new_content)
            if not new_content.strip():
                new_content = ""
            if dry_run:
                actions.append("[dry-run] Would remove MCP block from config.toml")
            else:
                config_path.write_text(new_content)
                actions.append("Removed MCP block from config.toml")

    return actions
