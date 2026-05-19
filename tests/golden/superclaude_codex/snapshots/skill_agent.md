---
name: superclaude-agent
description: AI agent delegation for specialized task execution
---

# /sc:agent

## Aliases

- `/sc:agent`
- `sc:agent`
- `agent`

## Workflow

1. Analyze request
2. Execute
3. Validate

## Safety

Do not write or modify code unless the user explicitly requests it.
Ask for user confirmation before changing scope beyond the original request.

## Output

Return a structured **agent result** containing:
- Delegation summary
- Output

## Completion

After completing `/sc:agent`, suggest relevant follow-up commands.
