---
name: superclaude-estimate
description: Provide development estimates for tasks, features, or projects with intelligent analysis
---

# /sc-estimate

## When to Use

Use this skill when the user invokes `/sc-estimate`.
Also activate when:
- Development planning requiring time, effort, or complexity estimates
- Project scoping and resource allocation decisions
- Feature breakdown needing systematic estimation methodology
- Risk assessment and confidence interval analysis requirements

## Aliases

- `/sc-estimate`
- `/sc:estimate`
- `sc-estimate`
- `sc:estimate`
- `estimate`

## Inputs

- `[target]` (optional): Feature, task, project, or migration to estimate.
- `--type` `time|effort|complexity`: Estimate dimension.
- `--unit` `hours|days|weeks`: Time unit for estimates.
- `--breakdown`: Break the estimate into phases or work items.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Workflow

1. Analyze
2. Calculate
3. Validate
4. Present
5. Track

## Personas

- Activate **system-architect** when relevant to the task.
- Activate **performance** when relevant to the task.
- Activate **project-manager** when relevant to the task.

## MCP Servers

Optionally leverage:
- sequential-thinking
- context7

## Safety

Do not write or modify code unless the user explicitly requests it.
Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **estimate** containing:
- Scope
- Effort breakdown
- Risks
- Timeline

## Completion

After completing `/sc-estimate`, suggest relevant follow-up commands.
