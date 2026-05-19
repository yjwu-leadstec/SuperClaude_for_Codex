# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Python Environment

**Uses UV exclusively.** Never use `python -m`, `pip install`, or `python script.py` directly.

```bash
uv run pytest                                           # Run all tests
uv run pytest tests/superclaude_codex/test_paths.py -v  # Single test file
uv pip install -e ".[dev]"                              # Install in dev mode
```

## Development Commands

```bash
make install       # Install in editable mode with dev deps
make test          # Run full test suite
make lint          # Ruff linter (src + tests)
make format        # Ruff formatter (src + tests)
make doctor        # Health check
make clean         # Remove build artifacts
```

## Architecture

SuperClaude for Codex is a **Codex-native** Python package providing 30 structured `/sc:*` commands and 20 specialist agents for OpenAI Codex. It does **not** read or write `~/.claude`.

### CLI Entry Point

`superclaude-codex` command — defined in `src/superclaude_codex/cli/main.py` via Click. Subcommands: `install`, `doctor`, `verify`, `commands`, `mcp`, `uninstall`.

### Core Packages

- **`core/`** — Command IR system:
  - `command_ir.py` — CommandIR dataclass, YAML loading, full serialization
  - `registry.py` — CommandRegistry: load, query, validate, export commands.json
  - `validation.py` — Schema validation (version, required fields, aliases, description)

- **`codex/`** — Codex integration:
  - `paths.py` — CODEX_HOME resolution + `~/.claude` guard + system path guard
  - `installer.py` — Atomic installer (staging → commit → rollback, --force, --dry-run)
  - `agents_md.py` — AGENTS.md marker-based renderer with corruption detection
  - `skills.py` — SKILL.md renderer (inputs, flags, codex behavior, personas)
  - `mcp.py` — MCP server config management (atomic write, backup, 8 servers)
  - `verify.py` — Doctor/verify: 7 health checks
  - `uninstall.py` — Clean removal of managed assets

- **`assets/commands/*.yaml`** — 30 Command IR definitions
- **`assets/agents/*.yaml`** — 20 Agent/persona definitions

### Installation Flow

`superclaude-codex install` loads Command IR YAMLs → renders AGENTS.md route block + 30 SKILL.md files + commands.json + agents.json → writes to `~/.codex/` via staging directory.

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

This project must **NEVER** import from old `superclaude` package or access `~/.claude`. Enforced by `test_no_claude_touch.py`.

## Key Documentation

- **docs/codex/** — User documentation (installation, commands, troubleshooting)
- **docs/Development/** — Historical rebuild plan (archival)
