---
name: superclaude-document
description: Generate focused documentation for components, functions, APIs, and features
---

# /sc-document

## When to Use

Use this skill when the user invokes `/sc-document`.
Also activate when:
- Documentation requests for specific components, functions, or features
- API documentation and reference material generation needs
- Code comment and inline documentation requirements
- User guide and technical documentation creation requests

## Aliases

- `/sc-document`
- `/sc:document`
- `sc-document`
- `sc:document`
- `document`

## Inputs

- `[target]` (optional): Code, component, API, module, or feature to document.
- `--type` `inline|external|api|guide`: Documentation type.
- `--style` `brief|detailed`: Documentation detail level.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Workflow

1. Analyze
2. Identify
3. Generate
4. Format
5. Integrate

## Safety

Do not write or modify code unless the user explicitly requests it.
Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **documentation** containing:
- Content
- Structure
- References

## Completion

After completing `/sc-document`, suggest relevant follow-up commands.
