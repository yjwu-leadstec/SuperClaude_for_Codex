# Troubleshooting

## Installation Issues

### `superclaude-codex: command not found`

Ensure the package is installed and on your PATH:
```bash
pipx install superclaude-for-codex
# or
pip install superclaude-for-codex
```

### `superclaude-codex doctor` shows failures

Run `superclaude-codex install` to create or repair the installation.

### Custom install path

Set `CODEX_HOME` before running commands:
```bash
export CODEX_HOME=/path/to/custom/.codex
superclaude-codex install
```

## Command Routing

### `/sc:brainstorm` not recognized in Codex

1. Check installation: `superclaude-codex doctor`
2. Verify AGENTS.md has the SuperClaude routing block
3. Restart Codex after installation

### Commands show "Not implemented"

Run `superclaude-codex install` to update to the latest version.

## MCP Issues

### API key warnings

Some MCP servers require API keys:
```bash
export TAVILY_API_KEY=your_key
superclaude-codex mcp install tavily
```

## FAQ

**Q: Does this modify my Claude Code configuration?**
A: No. SuperClaude for Codex never reads or writes `~/.claude`. It only writes to `~/.codex`.

**Q: Can I use this alongside the original SuperClaude?**
A: Yes. The two packages are completely independent.

**Q: How do I uninstall?**
A: `superclaude-codex uninstall` removes all managed assets from `~/.codex`.
