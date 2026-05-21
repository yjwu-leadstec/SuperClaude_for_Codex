---
name: superclaude-research
description: Deep web research with adaptive planning and intelligent search
---

# /sc-research

## When to Use

Use this skill when the user invokes `/sc-research`.
Also activate when:
- Research questions beyond knowledge cutoff
- Complex research questions
- Current events and real-time information
- Academic or technical research requirements
- Market analysis and competitive intelligence

## Aliases

- `/sc-research`
- `/sc:research`
- `sc-research`
- `sc:research`
- `research`

## Inputs

- `[query]` (optional): Research question, topic, market, technology, or decision to investigate.
- `--depth` `quick|standard|deep|exhaustive`: Research depth.
- `--strategy` `planning|intent|unified`: Research strategy.

## Global Flags

All `/sc-*` commands accept shared SuperClaude global flags such as `--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, `--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, `--seq`, `--serena`, `--play`, and `--no-mcp`.

- Safety first: --safe-mode > --validate > optimization flags.
- Explicit override: user-provided flags take precedence over auto-detection.
- Depth hierarchy: --ultrathink > --think-hard > --think.
- MCP control: --no-mcp overrides individual MCP flags.
- Scope precedence: system > project > module > file.

## Codex Behavior

- Reasoning effort: **high**
- Web search: **required**

## Workflow

1. Analyze request
2. Execute
3. Validate

## Personas

- Activate **deep-research-agent** when relevant to the task.

## MCP Servers

Optionally leverage:
- tavily
- sequential-thinking
- playwright

## Safety

Do not write or modify code unless the user explicitly requests it.
Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **research report** containing:
- Findings
- Sources
- Synthesis
- Recommendations

## Completion

After completing `/sc-research`, suggest relevant follow-up commands.
