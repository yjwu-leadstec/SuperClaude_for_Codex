---
name: superclaude-recommend
description: Ultra-intelligent command recommendation engine - recommends the most suitable SuperClaude commands for any user input
---

# /sc-recommend

## Aliases

- `/sc-recommend`
- `/sc:recommend`
- `sc-recommend`
- `sc:recommend`
- `recommend`

## Inputs

- `[user-request]` (optional): Natural-language request to map to commands and flags.
- `--options` `<flags>`: Free-form recommendation options or constraints.
- `--estimate`: Include time or budget estimation.
- `--alternatives`: Return multiple command alternatives.
- `--stream`: Use continuous recommendation mode.
- `--community`: Include community pattern guidance.
- `--language` `tr|en|auto`: Recommendation language.
- `--expertise` `beginner|intermediate|expert`: User expertise level.

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

Return a structured **recommendations** containing:
- Suggested commands
- Rationale

## Completion

After completing `/sc-recommend`, suggest relevant follow-up commands.
