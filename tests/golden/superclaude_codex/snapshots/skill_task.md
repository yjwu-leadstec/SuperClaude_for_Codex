---
name: superclaude-task
description: Execute complex tasks with intelligent workflow management and delegation
---

# /sc-task

## When to Use

Use this skill when the user invokes `/sc-task`.
Also activate when:
- Complex tasks requiring multi-agent coordination and delegation
- Projects needing structured workflow management and cross-session persistence
- Operations requiring intelligent MCP server routing and domain expertise
- Tasks benefiting from systematic execution and progressive enhancement

## Aliases

- `/sc-task`
- `/sc:task`
- `sc-task`
- `sc:task`
- `task`

## Inputs

- `[action]` (optional): Task action such as create, execute, update, or review.
- `[target]` (optional): Task, backlog, project, or feature target.
- `--strategy` `systematic|agile|enterprise`: Task execution strategy.
- `--parallel`: Execute independent task work in parallel.
- `--delegate`: Delegate suitable subtasks to agents.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

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

After completing `/sc-task`, suggest relevant follow-up commands.
