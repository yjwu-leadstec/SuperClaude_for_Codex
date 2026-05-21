---
name: superclaude-help
description: List all available /sc commands and their functionality
---

# /sc-help

## When to Use

Use this skill when the user invokes `/sc-help`.
Also activate when:
- Command discovery and reference lookup requests
- Framework exploration and capability understanding needs
- Documentation requests for available SuperClaude commands

## Aliases

- `/sc-help`
- `/sc:help`
- `sc-help`
- `sc:help`
- `help`

## Inputs

- `[command]` (optional): Optional command name to show detailed help for.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Workflow

1. Display
2. Complete

## Safety

Do not write or modify code unless the user explicitly requests it.

## Output

Return a structured **help text** containing:
- Command info

## Completion

After completing `/sc-help`, suggest relevant follow-up commands.
