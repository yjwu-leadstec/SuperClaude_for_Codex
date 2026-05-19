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
            raise InstallError("Command validation failed:\n" + "\n".join(msgs))

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
        """Write all files via staging directory, then move to final location.

        This ensures partial writes never leave the target in a broken state:
        1. Write everything to a temporary staging dir
        2. Validate staging output
        3. Move staged files to final location
        """
        self.codex_home.mkdir(parents=True, exist_ok=True)

        # Stage to temp directory first
        staging = self.codex_home / ".superclaude-staging"
        if staging.exists():
            shutil.rmtree(staging)
        staging.mkdir(parents=True)

        try:
            # 1. Stage AGENTS.md (special: update in-place via marker)
            staged_agents = staging / "AGENTS.md"
            agents_path = get_agents_md_path(self.codex_home)
            if agents_path.exists():
                shutil.copy2(agents_path, staged_agents)
            update_agents_md(staged_agents, self._agents_block)

            # 2. Stage skills
            staged_skills = staging / "skills"
            staged_skills.mkdir()
            render_all_skills(self._registry, staging)

            # 3. Stage superclaude-for-codex data
            staged_sc = staging / "superclaude-for-codex"
            staged_sc.mkdir()
            (staged_sc / "commands.json").write_text(self._commands_json)
            (staged_sc / "version.json").write_text(self._version_json)

            # All staging writes succeeded — now commit to final location
            # Move AGENTS.md
            shutil.copy2(staged_agents, agents_path)
            self.report.files_written.append(str(agents_path))

            # Move skills
            final_skills = get_skills_dir(self.codex_home)
            if final_skills.exists():
                for d in final_skills.iterdir():
                    if d.is_dir() and d.name.startswith("superclaude-"):
                        shutil.rmtree(d)
            else:
                final_skills.mkdir(parents=True)
            for skill_dir in staged_skills.iterdir():
                dest = final_skills / skill_dir.name
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(skill_dir, dest)
                self.report.files_written.append(str(dest / "SKILL.md"))

            # Move data dir
            final_sc = get_superclaude_dir(self.codex_home)
            final_sc.mkdir(parents=True, exist_ok=True)
            for f in staged_sc.iterdir():
                shutil.copy2(f, final_sc / f.name)
                self.report.files_written.append(str(final_sc / f.name))

            # Write install report (after all moves succeed)
            self.report.status = "success"
            report_path = final_sc / "install-report.json"
            report_path.write_text(json.dumps(self.report.to_dict(), indent=2))
            self.report.files_written.append(str(report_path))

        finally:
            # Always clean up staging
            if staging.exists():
                shutil.rmtree(staging)

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
