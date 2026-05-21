---
name: superclaude-load
description: Session lifecycle management with Serena MCP integration for project context loading
---

# /sc-load

## When to Use

Use this skill when the user invokes `/sc-load`.
Also activate when:
- Session initialization and project context loading requests
- Cross-session persistence and memory retrieval needs
- Project activation and context management requirements
- Session lifecycle management and checkpoint loading scenarios

## Aliases

- `/sc-load`
- `/sc:load`
- `sc-load`
- `sc:load`
- `load`

## Inputs

- `[target]` (optional): Project, config, dependency set, or checkpoint to load.
- `--type` `project|config|deps|checkpoint`: Load target type.
- `--refresh`: Refresh cached or saved context while loading.
- `--analyze`: Analyze the loaded context before proceeding.
- `--checkpoint` `<id>`: Checkpoint identifier to load.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Workflow

1. Initialize
2. Discover
3. Load
4. Activate
5. Validate

## Safety

Do not write or modify code unless the user explicitly requests it.

## Output

Return a structured **session state** containing:
- Restored context

## Completion

After completing `/sc-load`, suggest relevant follow-up commands.
