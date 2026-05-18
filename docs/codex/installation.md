# Installation Guide

## Prerequisites

- Python >= 3.10
- [pipx](https://pypa.github.io/pipx/) (recommended) or pip

## Install

```bash
pipx install superclaude-for-codex
superclaude-codex install
```

## Verify

```bash
superclaude-codex doctor
```

Expected output:
```
✅ Codex home: /home/user/.codex
✅ AGENTS.md: SuperClaude block present
✅ commands.json: valid, 30 commands
✅ Skills: 30/30 installed
✅ version.json: v0.1.0
✅ No ~/.claude references: clean

✅ All 6 checks passed.
```

## MCP Servers (Optional)

```bash
superclaude-codex mcp list              # List available servers
superclaude-codex mcp install context7  # Install specific server
superclaude-codex mcp install --all     # Install all servers
```

## Uninstall

```bash
superclaude-codex uninstall
```

## Important Notes

- SuperClaude for Codex is **Codex-only**. It does not read or write `~/.claude`.
- All assets are installed to `~/.codex/`.
- Set `CODEX_HOME` environment variable to use a custom install path.
