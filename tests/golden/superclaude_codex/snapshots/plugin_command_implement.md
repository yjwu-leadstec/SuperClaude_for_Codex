---
description: "Feature and code implementation with intelligent persona activation."
argument-hint: "[feature-description] [--type component|api|service|feature] [--framework react|vue|express] [--safe] [global-flags]"
allowed-tools: [Read, Glob, Grep, Bash, Write, Edit, WebFetch, TodoWrite]
---

# /sc-implement

Native Codex command for `/sc-implement`.

## Arguments

The user invoked this command with: $ARGUMENTS

## Parameters

Usage: `/sc-implement [feature-description] [--type component|api|service|feature] [--framework react|vue|express] [--safe] [global-flags]`

- `[feature-description]` (optional): Feature, behavior, bug fix, or implementation request.
- `--type` `component|api|service|feature`: Implementation target type.
- `--framework` `react|vue|express`: Primary framework or stack to use.
- `--safe`: Use conservative implementation with extra validation.
- `--with-tests`: Include or update tests as part of the implementation.

## Global Flags

These flags can be combined with this command when relevant:

- `--brainstorm`: Activate collaborative discovery and requirement elicitation.
- `--introspect`: Use a transparent meta-cognition mode when reasoning about the task.
- `--task-manage`: Organize work through task management and progressive execution.
- `--orchestrate`: Optimize tool selection and coordinate parallel work.
- `--token-efficient`: Use compressed communication while preserving essential detail.
- `--c7` / `--context7`: Prefer Context7 for curated documentation lookup.
- `--seq` / `--sequential`: Prefer Sequential for structured multi-step reasoning.
- `--magic`: Prefer Magic for modern UI generation patterns.
- `--morph` / `--morphllm`: Prefer Morphllm for efficient multi-file transformations.
- `--serena`: Prefer Serena for semantic code understanding and project memory.
- `--play` / `--playwright`: Prefer Playwright for browser automation and testing.
- `--chrome` / `--devtools`: Prefer Chrome DevTools for live browser inspection.
- `--tavily`: Prefer Tavily for web research and real-time information.
- `--frontend-verify`: Combine browser, devtools, and semantic checks for frontend validation.
- `--all-mcp`: Enable all relevant MCP capabilities.
- `--no-mcp`: Avoid MCP usage and rely on native Codex tools.
- `--think`: Use standard structured analysis.
- `--think-hard`: Use deeper structured analysis.
- `--ultrathink`: Use maximum-depth structured analysis.
- `--delegate` `auto|files|folders`: Use sub-agent delegation with the selected routing strategy.
- `--concurrency` `<n>`: Limit concurrent work, normally in the range 1-15.
- `--loop`: Use iterative improvement cycles with validation gates.
- `--iterations` `<n>`: Set the number of improvement cycles.
- `--validate`: Add pre-execution assessment and validation gates.
- `--safe-mode`: Use conservative execution with maximum validation.
- `--uc` / `--ultracompressed`: Use ultra-compressed output.
- `--scope` `file|module|project|system`: Define the operational or analysis scope.
- `--focus` `performance|security|quality|architecture|accessibility|testing`: Focus output and reasoning on the selected domain.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Examples

- `/sc-implement "user profile component" --type component --framework react`
- `/sc-implement "user authentication API" --type api --safe --with-tests`

## Instructions

When this command is invoked:

1. Read `~/.codex/skills/superclaude-implement/SKILL.md` for the full workflow.
2. Treat `$ARGUMENTS` as the input to `/sc-implement`, including command-specific and global flags.
3. Follow the skill workflow, safety rules, personas, and output contract.
4. Prefer project-local conventions and validate the result before finishing.

## Compatibility Aliases

`/sc-implement`, `/sc:implement`, `sc-implement`, `sc:implement`, `implement`
