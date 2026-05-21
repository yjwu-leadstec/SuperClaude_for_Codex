# AGENTS.md

This file gives Codex agents project-specific guidance for working in this
repository.

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
make lint              # Ruff linter
make format            # Ruff formatter
make doctor            # Health check
make clean             # Remove build artifacts
uv run superclaude-codex commands validate
```

## Architecture

SuperClaude for Codex is a Codex-native Python package providing 30 structured
`/sc-*` commands and 20 specialist agents for OpenAI Codex. Legacy `/sc:*`
aliases remain supported for migration. It does not read or write `~/.claude`.
Installation also registers a local Codex plugin so `/sc-*` commands can appear
in native slash-command completion after Codex restarts.

### CLI Entry Point

`superclaude-codex` is defined in `src/superclaude_codex/cli/main.py` with
Click. Subcommands include `install`, `doctor`, `verify`, `commands`, `mcp`,
and `uninstall`.

### Core Packages

- `core/` - Command IR system:
  - `command_ir.py` - CommandIR dataclass, YAML loading, serialization
  - `registry.py` - CommandRegistry loading, query, validation, export
  - `validation.py` - schema validation for versions, required fields, aliases
- `codex/` - Codex integration:
  - `paths.py` - CODEX_HOME resolution and `~/.claude` guard
  - `installer.py` - atomic installer with staging, commit, rollback
  - `agents_md.py` - AGENTS.md marker-based renderer
  - `skills.py` - SKILL.md renderer from Command IR
  - `mcp.py` - MCP server config management for config.toml
  - `verify.py` - doctor and verify health checks
  - `uninstall.py` - clean removal of managed assets
- `assets/commands/*.yaml` - 30 Command IR definitions
- `assets/agents/*.yaml` - 20 agent/persona definitions

### Installation Flow

`superclaude-codex install` loads Command IR YAML files, renders the AGENTS.md
routing block, renders 30 `superclaude-*` SKILL.md directories, writes
`commands.json`, and commits everything to `~/.codex/` through a staging
directory.

## Testing

```text
tests/superclaude_codex/    # Functional tests
tests/golden/               # Golden snapshot tests
```

Key test files:

- `test_no_claude_touch.py` - verifies no `~/.claude` access and no old package imports
- `test_installer.py` - atomic install, dry-run, rollback, idempotency
- `test_command_registry.py` - IR loading, validation, duplicate detection

## Key Constraint

This project must never import from an old `superclaude` package or access
`~/.claude`. The boundary is enforced by tests and by guard code in
`src/superclaude_codex/codex/paths.py`.

## Current Documentation

- `docs/codex/installation.md`
- `docs/codex/commands.md`
- `docs/codex/troubleshooting.md`
