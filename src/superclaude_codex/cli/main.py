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
    from superclaude_codex.codex.installer import InstallError, Installer

    installer = Installer(force=force, dry_run=dry_run)
    try:
        report = installer.run()
        if dry_run:
            click.echo(f"[dry-run] Would install to: {report.codex_home}")
            click.echo(f"[dry-run] Commands: {report.commands_installed}")
        else:
            click.echo(f"✅ Installed {report.commands_installed} commands to {report.codex_home}")
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
        click.echo(f"❌ Validation errors:")
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
    click.echo("Not implemented yet. See issue #17")


@mcp.command("install")
@click.argument("servers", nargs=-1)
@click.option("--dry-run", is_flag=True, help="Preview changes without writing files.")
@click.option("--all", "install_all", is_flag=True, help="Install all available MCP servers.")
def mcp_install(servers: tuple, dry_run: bool, install_all: bool):
    """Install MCP servers to Codex config."""
    click.echo("Not implemented yet. See issue #17")
