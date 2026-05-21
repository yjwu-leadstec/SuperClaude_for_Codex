---
name: superclaude-test
description: Execute tests with coverage analysis and automated quality reporting.
---

# /sc-test

## When to Use

Use this skill when the user invokes `/sc-test`.
Also activate when:
- user asks to run tests
- user asks to write tests
- user wants test coverage
- testing workflow request

## Aliases

- `/sc-test`
- `/sc:test`
- `sc-test`
- `sc:test`
- `test`

## Inputs

- `[target]` (optional): Test file, directory, component, or project area.
- `--type` / `--mode` `unit|integration|e2e|all`: Test type.
- `--coverage`: Include coverage reporting or analysis.
- `--watch`: Run tests in watch mode when supported.
- `--fix`: Attempt to fix failing tests when appropriate.
- `--framework` `pytest|jest|vitest|mocha`: Test framework to use when auto-detection is ambiguous.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Workflow

1. Detect test framework
2. Identify test scope
3. Run or generate tests
4. Analyze coverage
5. Report results

## Personas

- Activate **quality-engineer** when relevant to the task.
- Activate **python-expert** when relevant to the task.

## MCP Servers

Optionally leverage:
- context7

## Safety


## Output

Return a structured **test report** containing:
- Test results
- Coverage summary
- Failures and fixes

## Completion

After completing `/sc-test`, suggest relevant follow-up commands.
