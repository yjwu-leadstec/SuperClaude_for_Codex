---
name: superclaude-cleanup
description: Systematically clean up code, remove dead code, and optimize project structure
---

# /sc:cleanup

## When to Use

Use this skill when the user invokes `/sc:cleanup`.
Also activate when:
- Code maintenance and technical debt reduction requests
- Dead code removal and import optimization needs
- Project structure improvement and organization requirements
- Codebase hygiene and quality improvement initiatives

## Aliases

- `/sc:cleanup`
- `sc:cleanup`
- `cleanup`

## Workflow

1. Analyze
2. Plan
3. Execute
4. Validate
5. Report

## Personas

- Activate **system-architect** when relevant to the task.
- Activate **quality-engineer** when relevant to the task.
- Activate **security** when relevant to the task.

## MCP Servers

Optionally leverage:
- sequential-thinking
- context7

## Safety

Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **cleanup report** containing:
- Removed items
- Refactored items
- Impact summary

## Completion

After completing `/sc:cleanup`, suggest relevant follow-up commands.
