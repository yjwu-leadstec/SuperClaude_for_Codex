---
name: superclaude-research
description: Deep web research with adaptive planning and intelligent search
---

# /sc:research

## When to Use

Use this skill when the user invokes `/sc:research`.
Also activate when:
- Research questions beyond knowledge cutoff
- Complex research questions
- Current events and real-time information
- Academic or technical research requirements
- Market analysis and competitive intelligence

## Aliases

- `/sc:research`
- `sc:research`
- `research`

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

After completing `/sc:research`, suggest relevant follow-up commands.
