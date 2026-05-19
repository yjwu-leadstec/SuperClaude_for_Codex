"""SuperClaude for Codex CLI entry point."""

import click

from superclaude_codex import __version__


@click.group()
@click.version_option(version=__version__, prog_name="superclaude-codex")
def main():
    """SuperClaude for Codex — structured development workflows for OpenAI Codex.

    Install and manage SuperClaude commands, skills, agents, and MCP
    configurations in your Codex environment.
    """


@main.command()
@click.option("--dry-run", is_flag=True, help="Preview changes without writing files.")
@click.option("--force", is_flag=True, help="Force reinstall if assets already exist.")
def install(dry_run: bool, force: bool):
    """Install SuperClaude commands and skills to Codex."""
    from superclaude_codex.codex.installer import Installer, InstallError

    installer = Installer(force=force, dry_run=dry_run)
    try:
        report = installer.run()
        if dry_run:
            click.echo(f"[dry-run] Would install to: {report.codex_home}")
            click.echo(f"[dry-run] Commands: {report.commands_installed}")
        else:
            click.echo(
                f"✅ Installed {report.commands_installed} commands to {report.codex_home}"
            )
            click.echo(f"   Files written: {len(report.files_written)}")
    except InstallError as exc:
        click.echo(f"❌ Installation failed: {exc}", err=True)
        raise SystemExit(1)


@main.command()
def doctor():
    """Check SuperClaude for Codex installation health."""
    from superclaude_codex.codex.verify import run_doctor

    passed, total = run_doctor()
    if passed == total:
        click.echo(f"\n✅ All {total} checks passed.")
    else:
        click.echo(f"\n⚠️  {passed}/{total} checks passed.")
        raise SystemExit(1)


@main.command()
def verify():
    """Run smoke checks on the installation."""
    from superclaude_codex.codex.verify import run_doctor

    passed, total = run_doctor()
    if passed < total:
        raise SystemExit(1)


@main.group()
def commands():
    """Manage SuperClaude command registry."""


@commands.command("list")
def commands_list():
    """List all registered commands."""
    from superclaude_codex.core.registry import CommandRegistry

    reg = CommandRegistry()
    reg.load_all()
    cats = reg.list_by_category()
    for cat, cmds in sorted(cats.items()):
        click.echo(f"\n{cat.upper()}")
        for cmd in cmds:
            click.echo(f"  {cmd.display_name:20s} {cmd.description}")


@commands.command("validate")
def commands_validate():
    """Validate all command IR schemas."""
    from superclaude_codex.core.registry import CommandRegistry

    reg = CommandRegistry()
    reg.load_all()
    result = reg.validate_all()
    cmds = reg.list_commands()
    if result.is_valid:
        click.echo(f"✅ {len(cmds)} commands validated successfully.")
    else:
        click.echo("❌ Validation errors:")
        for e in result.errors:
            click.echo(f"  {e.command_id}.{e.field}: {e.message}")
        raise SystemExit(1)


@commands.command("show")
@click.argument("command_id")
def commands_show(command_id: str):
    """Show details of a specific command."""
    from superclaude_codex.core.registry import CommandRegistry

    reg = CommandRegistry()
    reg.load_all()
    cmd = reg.get_command(command_id) or reg.get_command_by_alias(f"/sc:{command_id}")
    if not cmd:
        click.echo(f"❌ Command not found: {command_id}")
        raise SystemExit(1)
    click.echo(f"ID:          {cmd.id}")
    click.echo(f"Display:     {cmd.display_name}")
    click.echo(f"Category:    {cmd.category}")
    click.echo(f"Description: {cmd.description}")
    click.echo(f"Aliases:     {', '.join(cmd.aliases)}")
    click.echo(f"Skill:       {cmd.codex.skill_name}")
    click.echo(f"Workflow:    {' → '.join(cmd.workflow)}")
    click.echo(f"Personas:    {', '.join(cmd.personas)}")


@main.group()
def mcp():
    """Manage MCP server configurations."""


@mcp.command("list")
def mcp_list():
    """List available MCP servers."""
    from superclaude_codex.codex.mcp import list_servers

    for server in list_servers():
        key_note = (
            f" (requires {server.api_key_env})" if server.requires_api_key else ""
        )
        click.echo(f"  {server.id:25s} {server.description}{key_note}")


@mcp.command("install")
@click.argument("servers", nargs=-1)
@click.option("--dry-run", is_flag=True, help="Preview changes without writing files.")
@click.option(
    "--all", "install_all", is_flag=True, help="Install all available MCP servers."
)
def mcp_install(servers: tuple, dry_run: bool, install_all: bool):
    """Install MCP servers to Codex config."""
    from superclaude_codex.codex.mcp import (
        MCP_REGISTRY,
        get_api_key_warnings,
        render_mcp_block,
        update_config_toml,
    )
    from superclaude_codex.codex.paths import get_config_toml_path

    if install_all:
        server_ids = list(MCP_REGISTRY.keys())
    elif servers:
        server_ids = list(servers)
        unknown = [s for s in server_ids if s not in MCP_REGISTRY]
        if unknown:
            click.echo(f"❌ Unknown servers: {', '.join(unknown)}", err=True)
            raise SystemExit(1)
    else:
        click.echo("Specify servers or use --all")
        raise SystemExit(1)

    warnings = get_api_key_warnings(server_ids)
    for w in warnings:
        click.echo(f"⚠️  {w}")

    block = render_mcp_block(server_ids)
    config_path = get_config_toml_path()

    if dry_run:
        click.echo(f"[dry-run] Would write to: {config_path}")
        click.echo(block)
    else:
        update_config_toml(config_path, block)
        click.echo(f"✅ Installed {len(server_ids)} MCP servers to {config_path}")


@main.command()
@click.option("--dry-run", is_flag=True, help="Preview what would be removed.")
@click.confirmation_option(prompt="Remove SuperClaude for Codex assets?")
def uninstall(dry_run: bool):
    """Remove SuperClaude for Codex assets from Codex."""
    from superclaude_codex.codex.uninstall import uninstall as do_uninstall

    actions = do_uninstall(dry_run=dry_run)
    for action in actions:
        click.echo(f"  {action}")
    if not actions:
        click.echo("Nothing to remove.")
    elif not dry_run:
        click.echo("\n✅ Uninstalled SuperClaude for Codex.")
