---
name: superclaude-test
description: Execute tests with coverage analysis and automated quality reporting.
---

# /sc:test

## When to Use

Use this skill when the user invokes `/sc:test`.
Also activate when:
- user asks to run tests
- user asks to write tests
- user wants test coverage
- testing workflow request

## Aliases

- `/sc:test`
- `sc:test`
- `test`

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

After completing `/sc:test`, suggest relevant follow-up commands.
