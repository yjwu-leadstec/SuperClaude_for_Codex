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
    click.echo("Not implemented yet. See issue #6")


@main.command()
def doctor():
    """Check SuperClaude for Codex installation health."""
    click.echo("Not implemented yet. See issue #9")


@main.command()
def verify():
    """Run smoke checks on the installation."""
    click.echo("Not implemented yet. See issue #9")


@main.group()
def commands():
    """Manage SuperClaude command registry."""


@commands.command("list")
def commands_list():
    """List all registered commands."""
    click.echo("Not implemented yet. See issue #4")


@commands.command("validate")
def commands_validate():
    """Validate all command IR schemas."""
    click.echo("Not implemented yet. See issue #4")


@commands.command("show")
@click.argument("command_id")
def commands_show(command_id: str):
    """Show details of a specific command."""
    click.echo(f"Not implemented yet. See issue #4 (command: {command_id})")


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
