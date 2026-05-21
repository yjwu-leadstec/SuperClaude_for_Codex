---
name: superclaude-improve
description: Apply systematic improvements to code quality, performance, and maintainability
---

# /sc-improve

## When to Use

Use this skill when the user invokes `/sc-improve`.
Also activate when:
- Code quality enhancement and refactoring requests
- Performance optimization and bottleneck resolution needs
- Maintainability improvements and technical debt reduction
- Best practices application and coding standards enforcement

## Aliases

- `/sc-improve`
- `/sc:improve`
- `sc-improve`
- `sc:improve`
- `improve`

## Inputs

- `[target]` (optional): Code, module, API, or project area to improve.
- `--type` `quality|performance|maintainability|style|security`: Improvement category.
- `--safe`: Use conservative improvement with validation gates.
- `--interactive`: Ask before applying higher-impact improvements.
- `--preview`: Show proposed improvements without applying changes.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Workflow

1. Analyze
2. Plan
3. Execute
4. Validate
5. Document

## Personas

- Activate **system-architect** when relevant to the task.
- Activate **performance** when relevant to the task.
- Activate **quality-engineer** when relevant to the task.
- Activate **security** when relevant to the task.

## MCP Servers

Optionally leverage:
- sequential-thinking
- context7

## Safety

Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **improvement report** containing:
- Changes made
- Before after
- Metrics

## Completion

After completing `/sc-improve`, suggest relevant follow-up commands.
