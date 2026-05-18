---
name: superclaude-task
description: Execute complex tasks with intelligent workflow management and delegation
---

# /sc:task

## When to Use

Use this skill when the user invokes `/sc:task`.
Also activate when:
- Complex tasks requiring multi-agent coordination and delegation
- Projects needing structured workflow management and cross-session persistence
- Operations requiring intelligent MCP server routing and domain expertise
- Tasks benefiting from systematic execution and progressive enhancement

## Aliases

- `/sc:task`
- `sc:task`
- `task`

## Workflow

1. Analyze
2. Delegate
3. Coordinate
4. Validate
5. Optimize

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

Return a structured **task list** containing:
- Tasks
- Priorities
- Assignments

## Completion

After completing `/sc:task`, suggest relevant follow-up commands.
