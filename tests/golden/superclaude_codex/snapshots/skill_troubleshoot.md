---
name: superclaude-troubleshoot
description: Diagnose and resolve issues in code, builds, deployments, and system behavior.
---

# /sc-troubleshoot

## When to Use

Use this skill when the user invokes `/sc-troubleshoot`.
Also activate when:
- user reports an error or bug
- user asks to debug something
- build or deployment failure
- system behavior issue

## Aliases

- `/sc-troubleshoot`
- `/sc:troubleshoot`
- `sc-troubleshoot`
- `sc:troubleshoot`
- `troubleshoot`

## Inputs

- `[issue]` (optional): Problem description, failing command, error message, or incident symptoms.
- `--type` `bug|build|performance|deployment`: Troubleshooting category.
- `--trace`: Trace the failure path in detail.
- `--fix`: Apply a fix after root cause is identified.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Codex Behavior

- Reasoning effort: **high**
- Web search: **optional**

## Workflow

1. Understand symptom
2. Gather context
3. Form hypothesis
4. Investigate root cause
5. Verify with evidence
6. Propose fix
7. Validate fix

## Personas

- Activate **root-cause-analyst** when relevant to the task.
- Activate **python-expert** when relevant to the task.
- Activate **devops-architect** when relevant to the task.

## MCP Servers

Optionally leverage:
- context7
- tavily

## Safety

Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **diagnosis report** containing:
- Symptom
- Root cause
- Fix applied
- Verification

## Completion

After completing `/sc-troubleshoot`, suggest relevant follow-up commands.
