---
name: superclaude-index-repo
description: Repository Indexing - 94% token reduction (58K → 3K)
---

# /sc-index-repo

## Aliases

- `/sc-index-repo`
- `/sc:index-repo`
- `sc-index-repo`
- `sc:index-repo`
- `index-repo`

## Inputs

- `[target]` (optional): Repository path or project root to index.
- `--mode` `create|update|quick`: Indexing mode. Default: `create`.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Workflow

1. Analyze request
2. Execute
3. Validate

## Safety

Do not write or modify code unless the user explicitly requests it.
Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **repository index** containing:
- Structure
- Key files
- Summary

## Completion

After completing `/sc-index-repo`, suggest relevant follow-up commands.
