"""MCP server configuration for Codex.

Manages MCP server entries in ~/.codex/config.toml without
calling Claude CLI or touching ~/.claude.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from superclaude_codex.codex.paths import assert_not_claude_path

BEGIN_MARKER = "# BEGIN SUPERCLAUDE FOR CODEX MCP"
END_MARKER = "# END SUPERCLAUDE FOR CODEX MCP"


@dataclass
class MCPServer:
    id: str
    name: str
    description: str
    config_template: str
    requires_api_key: bool = False
    api_key_env: str = ""


# Registry of supported MCP servers
MCP_REGISTRY: dict[str, MCPServer] = {
    "context7": MCPServer(
        id="context7",
        name="Context7",
        description="Official documentation lookup",
        config_template='[mcp.context7]\ncommand = "npx"\nargs = ["-y", "@context7/mcp"]',
    ),
    "tavily": MCPServer(
        id="tavily",
        name="Tavily",
        description="Web search for deep research",
        config_template='[mcp.tavily]\ncommand = "npx"\nargs = ["-y", "tavily-mcp"]',
        requires_api_key=True,
        api_key_env="TAVILY_API_KEY",
    ),
    "playwright": MCPServer(
        id="playwright",
        name="Playwright",
        description="Cross-browser automation",
        config_template='[mcp.playwright]\ncommand = "npx"\nargs = ["-y", "@anthropic/mcp-playwright"]',
    ),
    "sequential-thinking": MCPServer(
        id="sequential-thinking",
        name="Sequential Thinking",
        description="Multi-step reasoning",
        config_template='[mcp.sequential-thinking]\ncommand = "npx"\nargs = ["-y", "@anthropic/mcp-sequential-thinking"]',
    ),
    "magic": MCPServer(
        id="magic",
        name="Magic",
        description="UI component generation",
        config_template='[mcp.magic]\ncommand = "npx"\nargs = ["-y", "@anthropic/mcp-magic"]',
    ),
    "chrome-devtools": MCPServer(
        id="chrome-devtools",
        name="Chrome DevTools",
        description="Performance analysis",
        config_template='[mcp.chrome-devtools]\ncommand = "npx"\nargs = ["-y", "@anthropic/mcp-chrome-devtools"]',
    ),
    "serena": MCPServer(
        id="serena",
        name="Serena",
        description="Session persistence and code understanding",
        config_template='[mcp.serena]\ncommand = "npx"\nargs = ["-y", "serena-mcp"]',
    ),
    "airis-gateway": MCPServer(
        id="airis-gateway",
        name="AIRIS Gateway",
        description="Unified MCP gateway (60+ tools, single SSE endpoint)",
        config_template='[mcp.airis-gateway]\nurl = "http://localhost:3100/sse"',
    ),
}


def list_servers() -> list[MCPServer]:
    """List all available MCP servers."""
    return list(MCP_REGISTRY.values())


def render_mcp_block(server_ids: list[str]) -> str:
    """Render config.toml entries for selected servers.

    Raises KeyError for unknown server IDs to prevent silent misconfiguration.
    """
    unknown = [sid for sid in server_ids if sid not in MCP_REGISTRY]
    if unknown:
        raise KeyError(f"Unknown MCP server(s): {', '.join(unknown)}")

    lines = [BEGIN_MARKER]
    for sid in server_ids:
        server = MCP_REGISTRY[sid]
        lines.append("")
        lines.append(server.config_template)
    lines.append("")
    lines.append(END_MARKER)
    return "\n".join(lines)


class MCPConfigError(Exception):
    """Raised when config.toml cannot be safely updated."""


def update_config_toml(path: Path, block: str) -> None:
    """Insert or replace the MCP block in config.toml.

    Safety: backs up existing file before writing; aborts if
    existing content has only one marker (corrupt state).
    """
    assert_not_claude_path(path)

    if path.exists():
        content = path.read_text()

        # Backup before modifying
        backup = path.with_suffix(".toml.bak")
        backup.write_text(content)

        start = content.find(BEGIN_MARKER)
        end = content.find(END_MARKER)

        # Detect corrupt marker state
        if (start == -1) != (end == -1):
            raise MCPConfigError(
                f"Corrupt marker state in {path}: only one marker found. "
                "Fix manually or delete the file to reinstall."
            )

        if start != -1 and end != -1:
            new_content = content[:start] + block + content[end + len(END_MARKER):]
        else:
            sep = "\n\n" if content.strip() else ""
            new_content = content + sep + block + "\n"
    else:
        new_content = block + "\n"

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new_content)


def get_api_key_warnings(server_ids: list[str]) -> list[str]:
    """Return warnings for servers that need API keys."""
    warnings = []
    import os
    for sid in server_ids:
        server = MCP_REGISTRY.get(sid)
        if server and server.requires_api_key:
            if not os.environ.get(server.api_key_env):
                warnings.append(
                    f"{server.name} requires {server.api_key_env} environment variable"
                )
    return warnings
