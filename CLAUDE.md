# CLAUDE.md

This file exists only as a compatibility guide for Claude Code users who open
this repository. The project itself is Codex-native: runtime installation,
generated skills, command routing, and documentation all target `~/.codex/`.

For Codex agents, use `AGENTS.md` as the primary project guidance.

## Python Environment

Use `uv` for Python commands. Avoid direct `python -m`, `pip install`, or
`python script.py` invocations when a `uv` equivalent exists.

```bash
uv run pytest                                           # Run all tests
uv run pytest tests/superclaude_codex/test_paths.py -v  # Single test file
uv pip install -e ".[dev]"                              # Install in dev mode
```

## Development Commands

```bash
make install           # Install in editable mode with dev deps
make test              # Run full test suite
make lint              # Ruff linter (src + tests)
make format            # Ruff formatter (src + tests)
make doctor            # Health check
make clean             # Remove build artifacts
uv run superclaude-codex commands validate
```

## Architecture

SuperClaude for Codex is a Codex-native Python package providing 30 structured
`/sc:*` commands and 20 specialist agents for OpenAI Codex. It does not read or
write `~/.claude`.

### CLI Entry Point

`superclaude-codex` is defined in `src/superclaude_codex/cli/main.py` with
Click. Subcommands include `install`, `doctor`, `verify`, `commands`, `mcp`,
and `uninstall`.

### Core Packages

- `core/` - Command IR system:
  - `command_ir.py` - CommandIR dataclass, YAML loading, full serialization
  - `registry.py` - CommandRegistry loading, query, validation, export
  - `validation.py` - schema validation for versions, required fields, aliases, description
- `codex/` - Codex integration:
  - `paths.py` - CODEX_HOME resolution, `~/.claude` guard, system path guard
  - `installer.py` - atomic installer with staging, commit, rollback, `--force`, `--dry-run`
  - `agents_md.py` - AGENTS.md marker-based renderer with corruption detection
  - `skills.py` - SKILL.md renderer from Command IR
  - `mcp.py` - MCP server config management with atomic write and backups
  - `verify.py` - doctor and verify health checks
  - `uninstall.py` - clean removal of managed assets
- `assets/commands/*.yaml` - 30 Command IR definitions
- `assets/agents/*.yaml` - 20 agent/persona definitions

### Installation Flow

`superclaude-codex install` loads Command IR YAML files, renders the AGENTS.md
routing block, renders 30 `superclaude-*` SKILL.md directories, writes
`commands.json` and `agents.json`, then commits everything to `~/.codex/`
through a staging directory.

## Testing

```
tests/superclaude_codex/    # Functional tests
tests/golden/               # Golden snapshot tests
```

Key test files:
- `test_no_claude_touch.py` — Verifies no `~/.claude` access + import guard
- `test_installer.py` — Atomic install, dry-run, rollback, --force, idempotency
- `test_command_registry.py` — IR loading, validation, duplicate detection
- `test_mcp_config.py` — MCP merge, backup, corruption detection
- `test_uninstall.py` — MCP-only uninstall, skills cleanup, AGENTS block removal

## Key Constraint

This project must never import from an old `superclaude` package or access
`~/.claude`. The boundary is enforced by tests and by guard code in
`src/superclaude_codex/codex/paths.py`.

Do not add Claude Code installation paths, `.claude/` assets, or migration
helpers back into this repository. If Claude Code users need project context,
keep this file as a lightweight compatibility guide only.

## Key Documentation

- `AGENTS.md` - primary Codex agent guidance
- `PROJECT_INDEX.md` - current repository inventory
- `docs/codex/` - user documentation for installation, commands, troubleshooting
