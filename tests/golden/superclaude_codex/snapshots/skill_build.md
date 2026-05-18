---
name: superclaude-build
description: Build, compile, and package projects with intelligent error handling and optimization
---

# /sc:build

## When to Use

Use this skill when the user invokes `/sc:build`.
Also activate when:
- Project compilation and packaging requests for different environments
- Build optimization and artifact generation needs
- Error debugging during build processes
- Deployment preparation and artifact packaging requirements

## Aliases

- `/sc:build`
- `sc:build`
- `build`

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

After completing `/sc:build`, suggest relevant follow-up commands.
