---
name: superclaude-spawn
description: Meta-system task orchestration with intelligent breakdown and delegation
---

# /sc-spawn

## When to Use

Use this skill when the user invokes `/sc-spawn`.
Also activate when:
- Complex multi-domain operations requiring intelligent task breakdown
- Large-scale system operations spanning multiple technical areas
- Operations requiring parallel coordination and dependency management
- Meta-level orchestration beyond standard command capabilities

## Aliases

- `/sc-spawn`
- `/sc:spawn`
- `sc-spawn`
- `sc:spawn`
- `spawn`

## Inputs

- `[complex-task]` (optional): Complex task to break down and orchestrate.
- `--strategy` `sequential|parallel|adaptive`: Task breakdown strategy.
- `--depth` `normal|deep`: Planning and execution depth.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Workflow

1. Analyze
2. Decompose
3. Orchestrate
4. Monitor
5. Integrate

## Safety

Do not write or modify code unless the user explicitly requests it.
Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **spawn result** containing:
- Subtasks
- Results

## Completion

After completing `/sc-spawn`, suggest relevant follow-up commands.
