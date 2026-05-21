---
name: superclaude-sc
description: SuperClaude command dispatcher - Use /sc [command] to access all SuperClaude features
---

# /sc

## Aliases

- `/sc`
- `/sc-sc`
- `/sc:sc`
- `sc`

## Inputs

- `[command]` (optional): SuperClaude command to dispatch.
- `[arguments]` (optional): Arguments to forward to the dispatched command.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Workflow

1. Analyze request
2. Execute
3. Validate

## Safety

Do not write or modify code unless the user explicitly requests it.

## Output

Return a structured **command list** containing:
- Available commands

## Completion

After completing `/sc`, suggest relevant follow-up commands.
