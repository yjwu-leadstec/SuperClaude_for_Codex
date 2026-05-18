---
name: superclaude-load
description: Session lifecycle management with Serena MCP integration for project context loading
---

# /sc:load

## When to Use

Use this skill when the user invokes `/sc:load`.
Also activate when:
- Session initialization and project context loading requests
- Cross-session persistence and memory retrieval needs
- Project activation and context management requirements
- Session lifecycle management and checkpoint loading scenarios

## Aliases

- `/sc:load`
- `sc:load`
- `load`

## Workflow

1. Initialize
2. Discover
3. Load
4. Activate
5. Validate

## Safety

Do not write or modify code unless the user explicitly requests it.

## Output

Return a structured **session state** containing:
- Restored context

## Completion

After completing `/sc:load`, suggest relevant follow-up commands.
