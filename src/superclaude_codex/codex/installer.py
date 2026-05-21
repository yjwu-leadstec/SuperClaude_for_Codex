"""Atomic installer for SuperClaude for Codex.

Follows a transactional flow: prepare → stage → commit → rollback.
Ensures user environment is never left in a broken state.
"""

from __future__ import annotations

import json
import re
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
    get_config_toml_path,
    get_skills_dir,
    get_superclaude_dir,
    resolve_codex_home,
)
from superclaude_codex.codex.plugin import (
    BEGIN_MARKER as PLUGIN_BEGIN,
)
from superclaude_codex.codex.plugin import (
    END_MARKER as PLUGIN_END,
)
from superclaude_codex.codex.plugin import (
    get_installed_plugin_dir,
    install_plugin_cache,
    render_plugin_config_block,
    update_config_toml,
    write_plugin,
)
from superclaude_codex.codex.skills import normalize_ui_locale, render_all_skills
from superclaude_codex.core.registry import CommandRegistry


@dataclass
class InstallReport:
    version: str = __version__
    codex_home: str = ""
    files_written: list[str] = field(default_factory=list)
    files_backed_up: list[str] = field(default_factory=list)
    commands_installed: int = 0
    native_plugin_enabled: bool = False
    ui_locale: str = "en"
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
            "native_plugin_enabled": self.native_plugin_enabled,
            "ui_locale": self.ui_locale,
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
        native_plugin: bool = False,
        ui_locale: str = "auto",
    ):
        self.codex_home = codex_home or resolve_codex_home()
        self.force = force
        self.dry_run = dry_run
        self.native_plugin = native_plugin
        self.ui_locale = normalize_ui_locale(ui_locale)
        self.report = InstallReport(codex_home=str(self.codex_home))
        self.report.native_plugin_enabled = native_plugin
        self.report.ui_locale = self.ui_locale
        self._backups: dict[str, Path] = {}
        self._backup_dir: Path | None = None
        self._registry: CommandRegistry | None = None

    def run(self) -> InstallReport:
        """Execute the full install pipeline."""
        from superclaude_codex.codex.paths import assert_safe_path

        assert_not_claude_path(self.codex_home)
        assert_safe_path(self.codex_home)
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
        # Check if already installed (unless --force)
        sc_dir = get_superclaude_dir(self.codex_home)
        if sc_dir.exists() and not self.force and not self.dry_run:
            version_file = sc_dir / "version.json"
            if version_file.exists():
                import json as _json

                existing = _json.loads(version_file.read_text())
                if existing.get("version") == __version__:
                    raise InstallError(
                        f"SuperClaude for Codex v{__version__} is already installed. "
                        "Use --force to reinstall."
                    )

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

            config_toml = get_config_toml_path(self.codex_home)
            if config_toml.exists():
                backup = self._backup_dir / "config.toml"
                shutil.copy2(config_toml, backup)
                self._backups["config.toml"] = backup
                self.report.files_backed_up.append(str(config_toml))

            skills_dir = get_skills_dir(self.codex_home)
            if skills_dir.exists():
                backup = self._backup_dir / "skills"
                if backup.exists():
                    shutil.rmtree(backup)
                shutil.copytree(skills_dir, backup)
                self._backups["skills"] = backup
                self.report.files_backed_up.append(str(skills_dir))

            sc_dir = get_superclaude_dir(self.codex_home)
            if sc_dir.exists():
                backup = self._backup_dir / "superclaude-for-codex"
                if backup.exists():
                    shutil.rmtree(backup)
                shutil.copytree(sc_dir, backup)
                self._backups["superclaude-for-codex"] = backup
                self.report.files_backed_up.append(str(sc_dir))

    def _render_agents_json(self) -> str:
        """Load agent YAML definitions and render agents.json."""
        import yaml

        agents_dir = Path(__file__).resolve().parent.parent / "assets" / "agents"
        agents = []
        if agents_dir.is_dir():
            for f in sorted(agents_dir.glob("*.yaml")):
                with open(f) as fh:
                    data = yaml.safe_load(fh)
                if data and isinstance(data, dict) and "id" in data:
                    agents.append(
                        {
                            "id": data["id"],
                            "name": data.get("name", data["id"]),
                            "description": data.get("description", ""),
                            "triggers": data.get("triggers", []),
                            "expertise": data.get("expertise", []),
                            "output_expectations": data.get("output_expectations", []),
                        }
                    )
        return json.dumps(
            {"schema_version": 1, "package_version": __version__, "agents": agents},
            indent=2,
            ensure_ascii=False,
        )

    def _stage(self) -> None:
        """Validate all outputs can be rendered (in memory)."""
        # Render AGENTS.md block
        self._agents_block = render_agents_block(self._registry)

        # Render commands.json
        self._commands_json = self._registry.export_commands_json_str()

        # Render agents.json from asset files
        self._agents_json = self._render_agents_json()

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
            render_all_skills(self._registry, staging, self.ui_locale)

            # 3. Stage superclaude-for-codex data
            staged_sc = staging / "superclaude-for-codex"
            staged_sc.mkdir()
            (staged_sc / "commands.json").write_text(self._commands_json)
            (staged_sc / "agents.json").write_text(self._agents_json)
            (staged_sc / "version.json").write_text(self._version_json)
            if self.native_plugin:
                write_plugin(self._registry, staged_sc / "marketplace")

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
                dest = final_sc / f.name
                if f.is_dir():
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(f, dest)
                else:
                    shutil.copy2(f, dest)
                self.report.files_written.append(str(final_sc / f.name))

            config_path = get_config_toml_path(self.codex_home)
            if self.native_plugin:
                # Register and enable native Codex plugin commands.
                installed_plugin = install_plugin_cache(self.codex_home)
                self.report.files_written.append(str(installed_plugin))

                plugin_block = render_plugin_config_block(self.codex_home)
                update_config_toml(config_path, plugin_block)
                self.report.files_written.append(str(config_path))
            else:
                # Keep the default install identical to cc-switch-style standalone skills.
                stale_marketplace = final_sc / "marketplace"
                if stale_marketplace.exists():
                    shutil.rmtree(stale_marketplace)

                installed_plugin = get_installed_plugin_dir(self.codex_home)
                if installed_plugin.exists():
                    shutil.rmtree(installed_plugin)
                for parent in (installed_plugin.parent, installed_plugin.parent.parent):
                    if parent.exists() and not any(parent.iterdir()):
                        parent.rmdir()

                if config_path.exists():
                    content = config_path.read_text()
                    start = content.find(PLUGIN_BEGIN)
                    end = content.find(PLUGIN_END)
                    if start != -1 and end != -1:
                        new_content = content[:start] + content[end + len(PLUGIN_END) :]
                        new_content = re.sub(r"\n{3,}", "\n\n", new_content)
                        config_path.write_text(new_content)
                        self.report.files_written.append(str(config_path))

            # Write install report (after all moves succeed)
            self.report.status = "success"
            report_path = final_sc / "install-report.json"
            report_path.write_text(json.dumps(self.report.to_dict(), indent=2))
            self.report.files_written.append(str(report_path))

        finally:
            # Always clean up staging
            if staging.exists():
                shutil.rmtree(staging)

        # Clean up backup on success (non-critical — don't trigger rollback if this fails)
        try:
            if self._backup_dir and self._backup_dir.exists():
                shutil.rmtree(self._backup_dir)
        except OSError:
            pass  # Backup cleanup failure is non-critical after successful install

    def _rollback(self) -> None:
        """Restore backed-up files on failure, and clean up any new files written."""
        # 1. Restore backed-up files to their original state
        agents_backup = self._backups.get("AGENTS.md")
        agents_path = get_agents_md_path(self.codex_home)
        if agents_backup and agents_backup.exists():
            shutil.copy2(agents_backup, agents_path)
        elif agents_path.exists() and "AGENTS.md" not in self._backups:
            # File was newly created by this install — remove it
            agents_path.unlink()

        skills_backup = self._backups.get("skills")
        skills_dir = get_skills_dir(self.codex_home)
        if skills_backup and skills_backup.exists():
            if skills_dir.exists():
                shutil.rmtree(skills_dir)
            shutil.copytree(skills_backup, skills_dir)
        elif skills_dir.exists():
            # Remove only superclaude-managed skills created in this run
            for d in skills_dir.iterdir():
                if d.is_dir() and d.name.startswith("superclaude-"):
                    shutil.rmtree(d)

        config_backup = self._backups.get("config.toml")
        config_path = get_config_toml_path(self.codex_home)
        if config_backup and config_backup.exists():
            shutil.copy2(config_backup, config_path)
        elif config_path.exists() and "config.toml" not in self._backups:
            config_path.unlink()

        # 2. Restore or remove data dir
        sc_backup = self._backups.get("superclaude-for-codex")
        sc_dir = get_superclaude_dir(self.codex_home)
        if sc_backup and sc_backup.exists():
            if sc_dir.exists():
                shutil.rmtree(sc_dir)
            shutil.copytree(sc_backup, sc_dir)
        elif sc_dir.exists() and "superclaude-for-codex" not in self._backups:
            # Only remove if it was newly created (no prior backup means it didn't exist)
            shutil.rmtree(sc_dir)

        # 3. Clean up backup dir
        if self._backup_dir and self._backup_dir.exists():
            shutil.rmtree(self._backup_dir)
