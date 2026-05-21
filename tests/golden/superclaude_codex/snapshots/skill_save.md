---
name: superclaude-save
description: Session lifecycle management with Serena MCP integration for session context persistence
---

# /sc-save

## When to Use

Use this skill when the user invokes `/sc-save`.
Also activate when:
- Session completion and project context persistence needs
- Cross-session memory management and checkpoint creation requests
- Project understanding preservation and discovery archival scenarios
- Session lifecycle management and progress tracking requirements

## Aliases

- `/sc-save`
- `/sc:save`
- `sc-save`
- `sc:save`
- `save`

## Inputs

- `--type` `session|learnings|context|all`: Context to save.
- `--summarize`: Summarize saved context for later restoration.
- `--checkpoint`: Create a named checkpoint for later loading.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Workflow

1. Analyze
2. Persist
3. Checkpoint
4. Validate
5. Prepare

## Safety

Do not write or modify code unless the user explicitly requests it.
Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **session snapshot** containing:
- Saved context

## Completion

After completing `/sc-save`, suggest relevant follow-up commands.
