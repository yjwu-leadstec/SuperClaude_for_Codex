---
name: superclaude-explain
description: Provide clear explanations of code, concepts, and system behavior with educational clarity
---

# /sc-explain

## When to Use

Use this skill when the user invokes `/sc-explain`.
Also activate when:
- Code understanding and documentation requests for complex functionality
- System behavior explanation needs for architectural components
- Educational content generation for knowledge transfer
- Framework-specific concept clarification requirements

## Aliases

- `/sc-explain`
- `/sc:explain`
- `sc-explain`
- `sc:explain`
- `explain`

## Inputs

- `[target]` (optional): Code, concept, architecture, error, or system behavior to explain.
- `--level` `basic|intermediate|advanced`: Explanation level.
- `--format` `text|examples|interactive`: Explanation format.
- `--context` `<domain>`: Domain or framework context for the explanation.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Workflow

1. Analyze
2. Assess
3. Structure
4. Generate
5. Validate

## Personas

- Activate **educator** when relevant to the task.
- Activate **system-architect** when relevant to the task.
- Activate **security** when relevant to the task.

## MCP Servers

Optionally leverage:
- sequential-thinking
- context7

## Safety

Do not write or modify code unless the user explicitly requests it.

## Output

Return a structured **explanation** containing:
- Overview
- Details
- Examples

## Completion

After completing `/sc-explain`, suggest relevant follow-up commands.
