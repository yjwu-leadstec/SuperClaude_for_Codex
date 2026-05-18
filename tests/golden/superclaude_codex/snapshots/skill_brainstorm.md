---
name: superclaude-brainstorm
description: Interactive requirements discovery through Socratic dialogue and systematic exploration.
---

# /sc:brainstorm

## When to Use

Use this skill when the user invokes `/sc:brainstorm`.
Also activate when:
- user wants to explore an idea
- user asks to brainstorm
- user describes a product concept
- ambiguous project ideas requiring structured exploration
- requirements discovery and specification development

## Aliases

- `/sc:brainstorm`
- `sc:brainstorm`
- `brainstorm`

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

After completing `/sc:brainstorm`, suggest relevant follow-up commands.
