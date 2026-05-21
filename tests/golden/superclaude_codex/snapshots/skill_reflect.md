---
name: superclaude-reflect
description: Task reflection and validation using Serena MCP analysis capabilities
---

# /sc-reflect

## When to Use

Use this skill when the user invokes `/sc-reflect`.
Also activate when:
- Task completion requiring validation and quality assessment
- Session progress analysis and reflection on work accomplished
- Cross-session learning and insight capture for project improvement
- Quality gates requiring comprehensive task adherence verification

## Aliases

- `/sc-reflect`
- `/sc:reflect`
- `sc-reflect`
- `sc:reflect`
- `reflect`

## Inputs

- `--type` `task|session|completion`: Reflection type.
- `--analyze`: Analyze the work before reflecting.
- `--validate`: Validate outcomes and assumptions.

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
3. Reflect
4. Document
5. Optimize

## Safety

Do not write or modify code unless the user explicitly requests it.
Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **retrospective** containing:
- What worked
- What failed
- Action items

## Completion

After completing `/sc-reflect`, suggest relevant follow-up commands.
