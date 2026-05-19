---
name: superclaude-analyze
description: Comprehensive code analysis across quality, security, performance, and architecture.
---

# /sc:analyze

## When to Use

Use this skill when the user invokes `/sc:analyze`.
Also activate when:
- user asks to analyze code
- user wants a code review
- user asks about code quality
- security or performance audit request

## Aliases

- `/sc:analyze`
- `sc:analyze`
- `analyze`

## Inputs

- **target** (optional): File, directory, or pattern to analyze (default ".")
- `--focus` [quality, security, performance, architecture, all] (default: all)
- `--depth` [quick, standard, deep] (default: standard)

## Codex Behavior

- Reasoning effort: **high**
- Web search: **optional**

## Workflow

1. Identify analysis scope
2. Read target files
3. Analyze code quality
4. Analyze security patterns
5. Analyze performance
6. Analyze architecture
7. Generate report

## Personas

- Activate **quality-engineer** when relevant to the task.
- Activate **security-engineer** when relevant to the task.
- Activate **performance-engineer** when relevant to the task.
- Activate **system-architect** when relevant to the task.

## MCP Servers

Optionally leverage:
- context7

## Safety

Do not write or modify code unless the user explicitly requests it.

## Output

Return a structured **analysis report** containing:
- Summary
- Findings
- Recommendations
- Severity breakdown

## Completion

After completing `/sc:analyze`, suggest relevant follow-up commands.
