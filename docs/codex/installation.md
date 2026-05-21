# Installation Guide

## Prerequisites

- Python >= 3.10
- [pipx](https://pypa.github.io/pipx/) (recommended) or pip

## Install

```bash
pipx install superclaude-for-codex
superclaude-codex install
```

Skill UI descriptions use `--locale auto` by default. `auto` checks `LC_ALL`,
`LC_MESSAGES`, then `LANG`: `zh-CN`/`zh-Hans` install Simplified Chinese,
`zh-TW`/`zh-HK`/`zh-MO`/`zh-Hant` install Traditional Chinese, and all other
locales install English.

You can force the UI description language:

```bash
superclaude-codex install --locale zh-CN
superclaude-codex install --locale zh-TW
superclaude-codex install --locale en
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
✅ agents.json: valid, 20 agents
✅ Skills: 30/30 installed
✅ Native plugin: disabled (standalone skills mode)
✅ version.json: v0.1.0
✅ No ~/.claude references: clean

✅ All 8 checks passed.
```

The default installer uses standalone Codex skills in
`~/.codex/skills/superclaude-*`, which keeps completion labels short and avoids
plugin namespace prefixes.

To also install native plugin command files with `argument-hint` placeholders:

```bash
superclaude-codex install --native-plugin
```

Restart Codex after switching install modes so the skill and plugin indexes are
reloaded.

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
