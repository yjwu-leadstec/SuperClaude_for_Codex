---
name: superclaude-agent
description: AI agent delegation for specialized task execution
---

# /sc-agent

## Aliases

- `/sc-agent`
- `/sc:agent`
- `sc-agent`
- `sc:agent`
- `agent`

## Inputs

- `[agent-type]` (optional): Specialist agent or delegation type to use.
- `[task]` (optional): Task for the selected agent to execute.

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
Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **agent result** containing:
- Delegation summary
- Output

## Completion

After completing `/sc-agent`, suggest relevant follow-up commands.
