---
name: superclaude-estimate
description: Provide development estimates for tasks, features, or projects with intelligent analysis
---

# /sc:estimate

## When to Use

Use this skill when the user invokes `/sc:estimate`.
Also activate when:
- Development planning requiring time, effort, or complexity estimates
- Project scoping and resource allocation decisions
- Feature breakdown needing systematic estimation methodology
- Risk assessment and confidence interval analysis requirements

## Aliases

- `/sc:estimate`
- `sc:estimate`
- `estimate`

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

After completing `/sc:estimate`, suggest relevant follow-up commands.
