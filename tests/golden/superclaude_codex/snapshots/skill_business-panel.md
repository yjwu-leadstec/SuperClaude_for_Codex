---
name: superclaude-business-panel
description: Multi-expert business strategy panel with sequential, debate, and Socratic modes
---

# /sc-business-panel

## Aliases

- `/sc-business-panel`
- `/sc:business-panel`
- `sc-business-panel`
- `sc:business-panel`
- `business-panel`

## Inputs

- `[content]` (optional): Document path, pasted content, business idea, or strategic question.
- `--mode` `discussion|debate|socratic|adaptive`: Panel interaction mode.
- `--experts` `<names>`: Comma-separated expert names to include.
- `--focus` `<domain>`: Business domain or strategic focus.
- `--all-experts`: Include the full expert panel.
- `--synthesis-only`: Return only the synthesis rather than full expert analysis.
- `--structured`: Use a structured output format.
- `--verbose`: Return detailed expert reasoning and recommendations.
- `--questions`: Focus the panel on strategic questions.

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

Return a structured **business analysis** containing:
- Market assessment
- Strategy
- Recommendations

## Completion

After completing `/sc-business-panel`, suggest relevant follow-up commands.
