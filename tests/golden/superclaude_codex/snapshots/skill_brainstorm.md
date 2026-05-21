---
name: superclaude-brainstorm
description: Interactive requirements discovery through Socratic dialogue and systematic exploration.
---

# /sc-brainstorm

## When to Use

Use this skill when the user invokes `/sc-brainstorm`.
Also activate when:
- user wants to explore an idea
- user asks to brainstorm
- user describes a product concept
- ambiguous project ideas requiring structured exploration
- requirements discovery and specification development

## Aliases

- `/sc-brainstorm`
- `/sc:brainstorm`
- `sc-brainstorm`
- `sc:brainstorm`
- `brainstorm`

## Inputs

- `[topic]` (optional): Idea, product, feature, or problem to explore.
- `--strategy` `systematic|agile|enterprise`: Discovery strategy.
- `--depth` `shallow|normal|deep`: Exploration depth.
- `--parallel`: Explore multiple lines of thinking in parallel.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Workflow

1. Understand request
2. Inspect project context
3. Ask targeted questions
4. Generate alternatives
5. Challenge assumptions
6. Produce design doc

## Personas

- Activate **analyst** when relevant to the task.
- Activate **product** when relevant to the task.
- Activate **architect** when relevant to the task.

## MCP Servers

Optionally leverage:
- context7
- tavily
- sequential-thinking

## Safety

Do not write or modify code unless the user explicitly requests it.
Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **design doc** containing:
- Problem statement
- Constraints
- Approaches considered
- Recommended approach
- Next steps

## Completion

After completing `/sc-brainstorm`, suggest relevant follow-up commands.
