---
name: superclaude-workflow
description: Generate structured implementation workflows from PRDs and feature requirements
---

# /sc:workflow

## When to Use

Use this skill when the user invokes `/sc:workflow`.
Also activate when:
- PRD and feature specification analysis for implementation planning
- Structured workflow generation for development projects
- Multi-persona coordination for complex implementation strategies
- Cross-session workflow management and dependency mapping

## Aliases

- `/sc:workflow`
- `sc:workflow`
- `workflow`

## Workflow

1. Analyze
2. Plan
3. Coordinate
4. Execute
5. Validate

## Personas

- Activate **system-architect** when relevant to the task.
- Activate **analyzer** when relevant to the task.
- Activate **frontend** when relevant to the task.
- Activate **backend** when relevant to the task.
- Activate **security** when relevant to the task.
- Activate **devops** when relevant to the task.
- Activate **project-manager** when relevant to the task.

## MCP Servers

Optionally leverage:
- sequential-thinking
- context7
- magic
- playwright

## Safety

Do not write or modify code unless the user explicitly requests it.
Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **workflow spec** containing:
- Steps
- Dependencies
- Automation

## Completion

After completing `/sc:workflow`, suggest relevant follow-up commands.
