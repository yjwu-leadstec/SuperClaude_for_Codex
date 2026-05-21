---
name: superclaude-build
description: Build, compile, and package projects with intelligent error handling and optimization
---

# /sc-build

## When to Use

Use this skill when the user invokes `/sc-build`.
Also activate when:
- Project compilation and packaging requests for different environments
- Build optimization and artifact generation needs
- Error debugging during build processes
- Deployment preparation and artifact packaging requirements

## Aliases

- `/sc-build`
- `/sc:build`
- `sc-build`
- `sc:build`
- `build`

## Inputs

- `[target]` (optional): Project, package, app, or component to build.
- `--type` `dev|prod|test`: Build type.
- `--clean`: Clean build artifacts before building.
- `--optimize`: Enable production optimization when building.
- `--verbose`: Show detailed build output and diagnostics.

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
5. Package

## Personas

- Activate **devops-engineer** when relevant to the task.

## MCP Servers

Optionally leverage:
- playwright

## Safety

Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **build report** containing:
- Build output
- Errors resolved
- Artifacts

## Completion

After completing `/sc-build`, suggest relevant follow-up commands.
