# Command Reference

SuperClaude for Codex provides 30 `/sc-*` commands. Type `/sc` in Codex to see all commands.

Earlier releases used original SuperClaude-style `/sc:*` commands for migration compatibility. The recommended Codex syntax is now `/sc-*`; legacy aliases such as `/sc:implement` still work.

Default installation registers standalone Codex skills in `~/.codex/skills/superclaude-*`, so Codex shows them without a plugin namespace prefix. This matches the gstack/cc-switch style.

If you need native plugin command files and command-level `argument-hint`
placeholders, install with `superclaude-codex install --native-plugin`.
Codex currently exposes a short `argument-hint`, not a confirmed schema for
per-flag interactive autocomplete. The full parameter set is documented in each
generated SKILL.md.

Examples:

```bash
/sc-implement "user authentication API" --type api --safe --with-tests
/sc-analyze src/auth --focus security --depth deep --think-hard
/sc-build --type prod --clean --optimize --validate
/sc-test src/components --type unit --coverage
```

Shared global flags can be combined with any `/sc-*` command. Common examples
include `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`,
`--uc`, `--scope`, `--focus`, and MCP selection flags such as `--c7`, `--seq`,
`--serena`, `--play`, and `--no-mcp`.

## Discovery & Planning

| Command | Description |
|---------|-------------|
| `/sc-brainstorm` | Interactive requirements discovery through Socratic dialogue |
| `/sc-design` | System architecture, APIs, and component interface design |
| `/sc-estimate` | Development time and effort estimation |
| `/sc-business-panel` | Multi-expert business strategy analysis |
| `/sc-spec-panel` | Multi-expert specification review |

## Development

| Command | Description |
|---------|-------------|
| `/sc-implement` | Feature and code implementation with persona activation |
| `/sc-build` | Build, compile, and package projects |
| `/sc-improve` | Systematic code quality improvements |
| `/sc-cleanup` | Code cleanup, dead code removal, structure optimization |
| `/sc-explain` | Clear explanations of code, concepts, and system behavior |

## Quality

| Command | Description |
|---------|-------------|
| `/sc-test` | Test execution, generation, and coverage analysis |
| `/sc-analyze` | Code analysis across quality, security, and performance |
| `/sc-troubleshoot` | Diagnose and resolve issues |
| `/sc-reflect` | Task reflection and validation |

## Documentation

| Command | Description |
|---------|-------------|
| `/sc-document` | Generate focused documentation |
| `/sc-help` | List all available commands |

## Version Control

| Command | Description |
|---------|-------------|
| `/sc-git` | Git operations with intelligent commit messages |

## Project Management

| Command | Description |
|---------|-------------|
| `/sc-pm` | Project manager orchestration agent |
| `/sc-task` | Task tracking and workflow management |
| `/sc-workflow` | Structured implementation workflows |

## Research

| Command | Description |
|---------|-------------|
| `/sc-research` | Deep web research with adaptive planning |

## Utilities

| Command | Description |
|---------|-------------|
| `/sc-agent` | AI agent delegation |
| `/sc-spawn` | Parallel task orchestration |
| `/sc-index-repo` | Repository indexing (94% token reduction) |
| `/sc-index` | Project documentation and knowledge base |
| `/sc-recommend` | Command recommendation engine |
| `/sc-select-tool` | Intelligent MCP tool selection |
| `/sc-load` | Load session context |
| `/sc-save` | Save session context |
| `/sc` | Show all commands |
