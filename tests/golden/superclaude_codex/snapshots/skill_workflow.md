---
name: superclaude-workflow
description: Generate structured implementation workflows from PRDs and feature requirements
---

# /sc-workflow

## When to Use

Use this skill when the user invokes `/sc-workflow`.
Also activate when:
- PRD and feature specification analysis for implementation planning
- Structured workflow generation for development projects
- Multi-persona coordination for complex implementation strategies
- Cross-session workflow management and dependency mapping

## Aliases

- `/sc-workflow`
- `/sc:workflow`
- `sc-workflow`
- `sc:workflow`
- `workflow`

## Inputs

- `[prd-or-feature]` (optional): PRD file, feature description, project brief, or implementation request.
- `--strategy` `systematic|agile|enterprise`: Workflow planning strategy.
- `--depth` `shallow|normal|deep`: Workflow detail level.
- `--parallel`: Identify parallelizable implementation work.

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
3. Coordinate
4. Execute
5. Validate

## Personas

- Activate **system-architect** when relevant to the task.
- Activate **analyzer** when relevant to the task.
- Activate **frontend** when relevant to the task.
- Activate **backend** when relevant to the task.
- Activate **security** when relevant to the task.
- Activate **devops** when relevant to the task.
- Activate **project-manager** when relevant to the task.

## MCP Servers

Optionally leverage:
- sequential-thinking
- context7
- magic
- playwright

## Safety

Do not write or modify code unless the user explicitly requests it.
Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **workflow spec** containing:
- Steps
- Dependencies
- Automation

## Completion

After completing `/sc-workflow`, suggest relevant follow-up commands.
