# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Python Environment

**Uses UV exclusively.** Never use `python -m`, `pip install`, or `python script.py` directly.

```bash
uv run pytest                          # Run tests
uv run pytest tests/unit/test_confidence.py -v  # Single test file
uv run pytest -m confidence_check      # By marker
uv pip install package                 # Install dependencies
```

## Development Commands

```bash
make install       # Install in editable mode with dev deps (uv pip install -e ".[dev]")
make test          # Run full test suite
make lint          # Ruff linter
make format        # Ruff formatter
make verify        # Verify package + plugin + health check
make doctor        # Health check diagnostics
make build-plugin  # Build plugin artefacts into dist/
make clean         # Remove build artifacts
```

## Architecture

SuperClaude is a **Python package** (hatchling build) that extends Claude Code with a pytest plugin, CLI tools, slash commands, and agents.

### Two Entry Points

1. **CLI** (`superclaude` command) — defined in `src/superclaude/cli/main.py` via Click. Subcommands: `install`, `doctor`, `mcp`, `skill`.
2. **Pytest Plugin** — auto-loaded via `[project.entry-points.pytest11]` in `pyproject.toml`. Provides 5 fixtures and auto-markers.

### Core Packages

- **`pm_agent/`** — Three core patterns exposed via `__init__.py`:
  - `ConfidenceChecker` — Pre-execution assessment (≥90% proceed, 70-89% investigate, <70% stop)
  - `SelfCheckProtocol` — Post-implementation validation with evidence
  - `ReflexionPattern` — Error learning across sessions
  - `TokenBudgetManager` — Token allocation by complexity level

- **`execution/`** — Parallel execution framework:
  - `parallel.py` — Wave → Checkpoint → Wave pattern
  - `reflection.py` — Meta-reasoning
  - `self_correction.py` — Error recovery

- **`cli/`** — CLI implementation:
  - `main.py` — Click group entry point
  - `doctor.py` — Health checks
  - `install_commands.py` — Installs commands + agents to `~/.claude/`
  - `install_mcp.py` — MCP server configuration
  - `install_skill.py` — Skill installation

- **`commands/`**, **`agents/`**, **`modes/`** — Markdown definitions (30 commands, 20 agents, 7 modes) installed to `~/.claude/` at install time
- **`core/`** — Reference markdown files (rules, principles, flags, research config)

### Installation Flow

`superclaude install` copies `.md` files from `src/superclaude/commands/` → `~/.claude/commands/sc/` and `src/superclaude/agents/` → `~/.claude/agents/`. The pytest plugin auto-loads via entry point — no manual registration needed.

### Plugin Build Pipeline

`make build-plugin` runs `scripts/build_superclaude_plugin.py` to assemble artefacts into `dist/plugins/superclaude/`. `make sync-plugin-repo` syncs these to the separate `SuperClaude_Plugin` repo.

## Testing

Tests live in `tests/unit/` and `tests/integration/`. The pytest plugin auto-marks tests based on directory:
- `tests/unit/` → `@pytest.mark.unit`
- `tests/integration/` → `@pytest.mark.integration`

Custom markers: `confidence_check`, `self_check`, `reflexion`, `complexity(level)`

Fixtures provided by the plugin: `confidence_checker`, `self_check_protocol`, `reflexion_pattern`, `token_budget`, `pm_context`

## Git Workflow

**Branch structure**: `master` (production) ← `integration` (testing) ← `feature/*`, `fix/*`, `docs/*`

Conventional commits: `feat:`, `fix:`, `docs:`, etc. Create branches from `integration`.

## SuperClaude for Codex (New Package)

A separate Codex-native package lives alongside the original. **Completely isolated** — no shared imports, no `~/.claude` access.

### Structure

```
pyproject-codex.toml                    # Independent package config
src/superclaude_codex/
├── cli/main.py                         # superclaude-codex CLI (Click)
├── core/                               # Command IR, registry, validation
├── codex/                              # paths, installer, agents_md, skills, mcp, verify, uninstall
└── assets/commands/*.yaml              # 30 Command IR definitions
         /agents/*.yaml                 # 20 Agent definitions
tests/superclaude_codex/                # 87 tests
tests/golden/superclaude_codex/         # 32 golden snapshot tests
```

### Commands

```bash
make dev-codex         # Install in editable mode
make test-codex        # Run tests (119 total)
make lint-codex        # Ruff linter
superclaude-codex install              # Install to ~/.codex
superclaude-codex doctor               # Health check
superclaude-codex commands validate    # Validate all 30 command YAMLs
superclaude-codex mcp list             # List MCP servers
superclaude-codex uninstall            # Remove managed assets
```

### Key Constraint

`src/superclaude_codex/` must NEVER import from `src/superclaude/`. Verified by `test_no_claude_touch.py`.

## Key Documentation

- **PLANNING.md** — Architecture decisions, design principles, absolute rules
- **TASK.md** — Current priorities and backlog
- **KNOWLEDGE.md** — Accumulated insights and troubleshooting
- **docs/Development/superclaude-for-codex-rebuild-plan.md** — Codex rebuild plan (13 phases)
- **docs/codex/** — Codex package user documentation
