---
name: superclaude-git
description: Git operations with intelligent commit messages and workflow optimization
---

# /sc-git

## When to Use

Use this skill when the user invokes `/sc-git`.
Also activate when:
- Git repository operations: status, add, commit, push, pull, branch
- Need for intelligent commit message generation
- Repository workflow optimization requests
- Branch management and merge operations

## Aliases

- `/sc-git`
- `/sc:git`
- `sc-git`
- `sc:git`
- `git`

## Inputs

- `[operation]` (optional): Git operation such as status, diff, commit, branch, merge, or log.
- `[args]` (optional): Additional operation-specific arguments.
- `--smart-commit`: Generate an intelligent commit message from the current diff.
- `--interactive`: Use an interactive workflow for risky git operations.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Workflow

1. Analyze
2. Validate
3. Execute
4. Optimize
5. Report

## Safety

Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **git operations** containing:
- Changes summary
- Commit info

## Completion

After completing `/sc-git`, suggest relevant follow-up commands.
