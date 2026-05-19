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
make test          # Run full test suite (119 tests)
make lint          # Ruff linter
make format        # Ruff formatter
make doctor        # Health check
make clean         # Remove build artifacts
```

## Architecture

SuperClaude for Codex is a **Codex-native** Python package providing 30 structured `/sc:*` commands and 20 specialist agents for OpenAI Codex. It does **not** read or write `~/.claude`.

### CLI Entry Point

`superclaude-codex` command — defined in `src/superclaude_codex/cli/main.py` via Click. Subcommands: `install`, `doctor`, `verify`, `commands`, `mcp`, `uninstall`.

### Core Packages

- **`core/`** — Command IR system:
  - `command_ir.py` — CommandIR dataclass, YAML loading, serialization
  - `registry.py` — CommandRegistry: load, query, validate, export commands.json
  - `validation.py` — Schema validation (version, required fields, aliases)

- **`codex/`** — Codex integration:
  - `paths.py` — CODEX_HOME resolution + `~/.claude` guard
  - `installer.py` — Atomic installer (staging → commit → rollback)
  - `agents_md.py` — AGENTS.md marker-based renderer
  - `skills.py` — SKILL.md renderer from Command IR
  - `mcp.py` — MCP server config management for config.toml
  - `verify.py` — Doctor/verify health checks
  - `uninstall.py` — Clean removal of managed assets

- **`assets/commands/*.yaml`** — 30 Command IR definitions
- **`assets/agents/*.yaml`** — 20 Agent/persona definitions

### Installation Flow

`superclaude-codex install` loads all Command IR YAMLs → renders AGENTS.md route block + 30 SKILL.md files + commands.json → writes to `~/.codex/` via staging directory.

## Testing

```
tests/superclaude_codex/    # 87 functional tests
tests/golden/               # 32 golden snapshot tests
```

Key test files:
- `test_no_claude_touch.py` — Verifies no `~/.claude` access + import guard
- `test_installer.py` — Atomic install, dry-run, rollback, idempotency
- `test_command_registry.py` — IR loading, validation, duplicate detection

## Key Constraint

This project must **NEVER** import from old `superclaude` package or access `~/.claude`. Enforced by `test_no_claude_touch.py`.

## Key Documentation

- **docs/Development/superclaude-for-codex-rebuild-plan.md** — Rebuild plan (13 phases)
- **docs/codex/** — User documentation (installation, commands, troubleshooting)
