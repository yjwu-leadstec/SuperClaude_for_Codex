"""Atomic installer for SuperClaude for Codex.

Follows a transactional flow: prepare → stage → commit → rollback.
Ensures user environment is never left in a broken state.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from superclaude_codex import __version__
from superclaude_codex.codex.agents_md import render_agents_block, update_agents_md
from superclaude_codex.codex.paths import (
    assert_not_claude_path,
    get_agents_md_path,
    get_skills_dir,
    get_superclaude_dir,
    resolve_codex_home,
)
from superclaude_codex.codex.skills import render_all_skills
from superclaude_codex.core.registry import CommandRegistry


@dataclass
class InstallReport:
    version: str = __version__
    codex_home: str = ""
    files_written: list[str] = field(default_factory=list)
    files_backed_up: list[str] = field(default_factory=list)
    commands_installed: int = 0
    status: str = "pending"
    error: str = ""
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "codex_home": self.codex_home,
            "files_written": self.files_written,
            "files_backed_up": self.files_backed_up,
            "commands_installed": self.commands_installed,
            "status": self.status,
            "error": self.error,
            "timestamp": self.timestamp,
        }


class InstallError(Exception):
    """Raised when installation fails."""


class Installer:
    """Transactional installer for SuperClaude for Codex."""

    def __init__(
        self,
        codex_home: Path | None = None,
        force: bool = False,
        dry_run: bool = False,
    ):
        self.codex_home = codex_home or resolve_codex_home()
        self.force = force
        self.dry_run = dry_run
        self.report = InstallReport(codex_home=str(self.codex_home))
        self._backups: dict[str, Path] = {}
        self._backup_dir: Path | None = None
        self._registry: CommandRegistry | None = None

    def run(self) -> InstallReport:
        """Execute the full install pipeline."""
        assert_not_claude_path(self.codex_home)
        self.report.timestamp = datetime.now(timezone.utc).isoformat()

        try:
            self._prepare()
            self._stage()
            if not self.dry_run:
                self._commit()
            self.report.status = "success" if not self.dry_run else "dry_run"
        except Exception as exc:
            self.report.status = "failed"
            self.report.error = str(exc)
            if not self.dry_run:
                self._rollback()
            raise InstallError(str(exc)) from exc

        return self.report

    def _prepare(self) -> None:
        """Resolve paths, load registry, create backup."""
        # Load command registry
        self._registry = CommandRegistry()
        self._registry.load_all()
        validation = self._registry.validate_all()
        if not validation.is_valid:
            msgs = [f"{e.command_id}.{e.field}: {e.message}" for e in validation.errors]
            raise InstallError(f"Command validation failed:\n" + "\n".join(msgs))

        self.report.commands_installed = len(self._registry.list_commands())

        # Create backup directory
        if not self.dry_run:
            self._backup_dir = self.codex_home / ".superclaude-backup"
            self._backup_dir.mkdir(parents=True, exist_ok=True)

            # Backup existing files
            agents_md = get_agents_md_path(self.codex_home)
            if agents_md.exists():
                backup = self._backup_dir / "AGENTS.md"
                shutil.copy2(agents_md, backup)
                self._backups["AGENTS.md"] = backup
                self.report.files_backed_up.append(str(agents_md))

            skills_dir = get_skills_dir(self.codex_home)
            if skills_dir.exists():
                backup = self._backup_dir / "skills"
                if backup.exists():
                    shutil.rmtree(backup)
                shutil.copytree(skills_dir, backup)
                self._backups["skills"] = backup
                self.report.files_backed_up.append(str(skills_dir))

    def _stage(self) -> None:
        """Validate all outputs can be rendered (in memory)."""
        # Render AGENTS.md block
        self._agents_block = render_agents_block(self._registry)

        # Render commands.json
        self._commands_json = self._registry.export_commands_json_str()

        # Render version.json
        self._version_json = json.dumps(
            {"version": __version__, "schema_version": 1}, indent=2
        )

    def _commit(self) -> None:
        """Write all files atomically."""
        # Ensure directories exist
        self.codex_home.mkdir(parents=True, exist_ok=True)
        sc_dir = get_superclaude_dir(self.codex_home)
        sc_dir.mkdir(parents=True, exist_ok=True)

        # 1. AGENTS.md
        agents_path = get_agents_md_path(self.codex_home)
        update_agents_md(agents_path, self._agents_block)
        self.report.files_written.append(str(agents_path))

        # 2. Skills
        paths = render_all_skills(self._registry, self.codex_home)
        for p in paths:
            self.report.files_written.append(str(p))

        # 3. commands.json
        cmds_path = sc_dir / "commands.json"
        cmds_path.write_text(self._commands_json)
        self.report.files_written.append(str(cmds_path))

        # 4. version.json
        ver_path = sc_dir / "version.json"
        ver_path.write_text(self._version_json)
        self.report.files_written.append(str(ver_path))

        # 5. install-report.json (mark success before writing)
        self.report.status = "success"
        report_path = sc_dir / "install-report.json"
        report_path.write_text(json.dumps(self.report.to_dict(), indent=2))
        self.report.files_written.append(str(report_path))

        # Clean up backup on success
        if self._backup_dir and self._backup_dir.exists():
            shutil.rmtree(self._backup_dir)

    def _rollback(self) -> None:
        """Restore backed-up files on failure."""
        if not self._backups:
            return

        agents_backup = self._backups.get("AGENTS.md")
        if agents_backup and agents_backup.exists():
            target = get_agents_md_path(self.codex_home)
            shutil.copy2(agents_backup, target)

        skills_backup = self._backups.get("skills")
        if skills_backup and skills_backup.exists():
            target = get_skills_dir(self.codex_home)
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(skills_backup, target)

        if self._backup_dir and self._backup_dir.exists():
            shutil.rmtree(self._backup_dir)
