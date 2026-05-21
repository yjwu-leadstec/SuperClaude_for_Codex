---
name: superclaude-select-tool
description: Intelligent MCP tool selection based on complexity scoring and operation analysis
---

# /sc-select-tool

## When to Use

Use this skill when the user invokes `/sc-select-tool`.
Also activate when:
- Operations requiring optimal MCP tool selection between Serena and Morphllm
- Meta-system decisions needing complexity analysis and capability matching
- Tool routing decisions requiring performance vs accuracy trade-offs
- Operations benefiting from intelligent tool capability assessment

## Aliases

- `/sc-select-tool`
- `/sc:select-tool`
- `sc-select-tool`
- `sc:select-tool`
- `select-tool`

## Inputs

- `[operation]` (optional): Operation or edit scenario to choose tools for.
- `--analyze`: Analyze the operation before recommending tools.
- `--explain`: Explain why the selected tools fit the task.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Workflow

1. Parse
2. Score
3. Match
4. Select
5. Validate

## Safety

Do not write or modify code unless the user explicitly requests it.

## Output

Return a structured **tool selection** containing:
- Recommended tool
- Rationale

## Completion

After completing `/sc-select-tool`, suggest relevant follow-up commands.
