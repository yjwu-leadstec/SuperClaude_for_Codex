---
name: superclaude-implement
description: Feature and code implementation with intelligent persona activation.
---

# /sc-implement

## When to Use

Use this skill when the user invokes `/sc-implement`.
Also activate when:
- user asks to implement a feature
- user wants to write code for a component
- feature development request
- code implementation need

## Aliases

- `/sc-implement`
- `/sc:implement`
- `sc-implement`
- `sc:implement`
- `implement`

## Inputs

- `[feature-description]` (optional): Feature, behavior, bug fix, or implementation request.
- `--type` `component|api|service|feature`: Implementation target type.
- `--framework` `react|vue|express`: Primary framework or stack to use.
- `--safe`: Use conservative implementation with extra validation.
- `--with-tests`: Include or update tests as part of the implementation.

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

1. Analyze requirements
2. Detect technology context
3. Plan implementation
4. Activate relevant personas
5. Generate code
6. Write tests
7. Validate security
8. Validate quality

## Personas

- Activate **architect** when relevant to the task.
- Activate **frontend-architect** when relevant to the task.
- Activate **backend-architect** when relevant to the task.
- Activate **security-engineer** when relevant to the task.
- Activate **quality-engineer** when relevant to the task.

## MCP Servers

Optionally leverage:
- context7
- sequential-thinking

## Safety

Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **implementation** containing:
- Implementation plan
- Code changes
- Tests
- Validation summary

## Completion

After completing `/sc-implement`, suggest relevant follow-up commands.
