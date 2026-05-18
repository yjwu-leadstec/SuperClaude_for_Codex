---
name: superclaude-select-tool
description: Intelligent MCP tool selection based on complexity scoring and operation analysis
---

# /sc:select-tool

## When to Use

Use this skill when the user invokes `/sc:select-tool`.
Also activate when:
- Operations requiring optimal MCP tool selection between Serena and Morphllm
- Meta-system decisions needing complexity analysis and capability matching
- Tool routing decisions requiring performance vs accuracy trade-offs
- Operations benefiting from intelligent tool capability assessment

## Aliases

- `/sc:select-tool`
- `sc:select-tool`
- `select-tool`

## Workflow

1. Parse
2. Score
3. Match
4. Select
5. Validate

## Safety

Do not write or modify code unless the user explicitly requests it.

## Output

Return a structured **tool selection** containing:
- Recommended tool
- Rationale

## Completion

After completing `/sc:select-tool`, suggest relevant follow-up commands.
