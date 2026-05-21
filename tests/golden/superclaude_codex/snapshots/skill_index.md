---
name: superclaude-index
description: Generate comprehensive project documentation and knowledge base with intelligent organization
---

# /sc-index

## When to Use

Use this skill when the user invokes `/sc-index`.
Also activate when:
- Project documentation creation and maintenance requirements
- Knowledge base generation and organization needs
- API documentation and structure analysis requirements
- Cross-referencing and navigation enhancement requests

## Aliases

- `/sc-index`
- `/sc:index`
- `sc-index`
- `sc:index`
- `index`

## Inputs

- `[target]` (optional): Project path, source directory, API, or documentation area to index.
- `--type` `docs|api|structure|readme`: Index type.
- `--format` `md|json|yaml`: Index output format.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Workflow

1. Analyze
2. Organize
3. Generate
4. Validate
5. Maintain

## Personas

- Activate **system-architect** when relevant to the task.
- Activate **scribe** when relevant to the task.
- Activate **quality-engineer** when relevant to the task.

## MCP Servers

Optionally leverage:
- sequential-thinking
- context7

## Safety

Do not write or modify code unless the user explicitly requests it.
Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **index** containing:
- Structure
- Summary

## Completion

After completing `/sc-index`, suggest relevant follow-up commands.
