# Project Index — SuperClaude for Codex

> Codex-native structured development workflows
> Version: 0.1.0 | Tests: 146 | Commands: 30 | Agents: 20 | MCP: 8

## Source Modules (16 files)

### `src/superclaude_codex/`

| Module | Purpose |
|--------|---------|
| `__init__.py` | Package root, exports `__version__` |
| `__version__.py` | Version: `0.1.0` |

### `src/superclaude_codex/cli/`

| Module | Purpose |
|--------|---------|
| `main.py` | Click CLI entry point — `superclaude-codex` command with subcommands: install, doctor, verify, commands, mcp, uninstall |

### `src/superclaude_codex/core/`

| Module | Purpose |
|--------|---------|
| `command_ir.py` | CommandIR dataclass — YAML loading, full IR serialization |
| `registry.py` | CommandRegistry — load all YAMLs, query by id/alias, validate, export commands.json |
| `validation.py` | Schema validation — version, required fields, aliases, description, output_contract |

### `src/superclaude_codex/codex/`

| Module | Purpose |
|--------|---------|
| `paths.py` | CODEX_HOME resolution, `~/.claude` guard, system path guard (/, /etc, /usr...) |
| `installer.py` | Atomic installer — staging dir → commit → rollback. Backup/restore. --force, --dry-run |
| `agents_md.py` | AGENTS.md renderer — marker-based insert/replace, corruption detection, size limit |
| `skills.py` | SKILL.md renderer — frontmatter, inputs, flags, workflow, personas, codex behavior |
| `mcp.py` | MCP config — 8 servers, atomic TOML write, backup (0o600), corruption detection |
| `verify.py` | Doctor — 7 checks: home, AGENTS.md, commands.json, agents.json, skills, version, ~/.claude |
| `uninstall.py` | Clean removal — skills, data dir, AGENTS.md block, MCP block. Preserves user content |

## Assets

### Commands (30 YAML files in `assets/commands/`)

| Category | Commands |
|----------|----------|
| Discovery | brainstorm, design, estimate, business-panel, spec-panel |
| Development | implement, build, improve, cleanup, explain |
| Quality | test, analyze, troubleshoot, reflect |
| Documentation | document, help |
| Version Control | git |
| Project Mgmt | pm, task, workflow |
| Research | research |
| Utilities | agent, spawn, index-repo, index, recommend, select-tool, load, save, sc |

### Agents (20 YAML files in `assets/agents/`)

backend-architect, business-panel-experts, deep-research-agent, deep-research, devops-architect, frontend-architect, learning-guide, performance-engineer, pm-agent, python-expert, quality-engineer, refactoring-expert, repo-index, requirements-analyst, root-cause-analyst, security-engineer, self-review, socratic-mentor, system-architect, technical-writer

## Tests (146 total)

| File | Tests | Focus |
|------|:-----:|-------|
| `test_cli.py` | 12 | CLI entry points, help, version, subcommands |
| `test_command_registry.py` | 22 | CommandIR loading, validation, registry, export |
| `test_installer.py` | 12 | Atomic install, dry-run, rollback, --force, idempotency |
| `test_agents_md.py` | 13 | Marker insert/replace, preserve content, corruption |
| `test_skill_renderer.py` | 11 | SKILL.md rendering, frontmatter, stability |
| `test_paths.py` | 17 | CODEX_HOME resolution, ~/.claude guard, system paths |
| `test_no_claude_touch.py` | 8 | Sentinel file verification, import guard |
| `test_mcp_config.py` | 7 | MCP merge, backup, corruption, unknown servers |
| `test_uninstall.py` | 7 | MCP-only, skills, data dir, AGENTS block, dry-run |
| `test_rendered_assets.py` | 32 | Golden snapshots: 30 skills + AGENTS.md + commands.json |
| `conftest.py` | — | Fixtures: tmp_codex_home, fake_home |

## Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Package config (hatchling), deps, pytest, ruff |
| `Makefile` | install, test, lint, format, doctor, clean |
| `install-codex.sh` | One-line installer script |
| `.github/workflows/test-codex.yml` | CI: 3x Python matrix, lint, format, test, import guard, smoke |

## Documentation

| File | Purpose |
|------|---------|
| `README.md` | Project overview, quick start, 30 commands, credits |
| `README-zh.md` / `README-ja.md` / `README-kr.md` | Translations |
| `AGENTS.md` | Primary Codex agent guidance |
| `CLAUDE.md` | Compatibility guide for Claude Code users; Codex-only boundaries still apply |
| `docs/codex/installation.md` | Install, verify, MCP, uninstall guide |
| `docs/codex/commands.md` | Full 30-command reference |
| `docs/codex/troubleshooting.md` | FAQ and common issues |
