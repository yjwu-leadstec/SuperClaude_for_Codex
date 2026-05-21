---
name: superclaude-cleanup
description: Systematically clean up code, remove dead code, and optimize project structure
---

# /sc-cleanup

## When to Use

Use this skill when the user invokes `/sc-cleanup`.
Also activate when:
- Code maintenance and technical debt reduction requests
- Dead code removal and import optimization needs
- Project structure improvement and organization requirements
- Codebase hygiene and quality improvement initiatives

## Aliases

- `/sc-cleanup`
- `/sc:cleanup`
- `sc-cleanup`
- `sc:cleanup`
- `cleanup`

## Inputs

- `[target]` (optional): File, directory, or project area to clean up.
- `--type` `code|imports|files|all`: Cleanup category.
- `--safe`: Use conservative cleanup with validation before removal.
- `--aggressive`: Apply broader cleanup when safe to do so.
- `--interactive`: Ask before applying risky cleanup decisions.
- `--preview`: Show cleanup candidates without applying changes.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

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

After completing `/sc-cleanup`, suggest relevant follow-up commands.
