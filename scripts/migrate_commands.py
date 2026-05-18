#!/usr/bin/env python3
"""One-time migration script: convert old SuperClaude command .md files to Command IR YAML.

Reads src/superclaude/commands/*.md, extracts semantic information,
and generates src/superclaude_codex/assets/commands/*.yaml.

This script is a one-time tool, not a runtime dependency.
"""

import re
import sys
from pathlib import Path

import yaml

OLD_COMMANDS_DIR = Path("src/superclaude/commands")
NEW_COMMANDS_DIR = Path("src/superclaude_codex/assets/commands")
SKIP_FILES = {"README.md"}

# Already migrated in M1 (#5)
ALREADY_MIGRATED = {"brainstorm", "implement", "analyze", "test", "troubleshoot"}

# Category mapping from old category names to new ones
CATEGORY_MAP = {
    "orchestration": "discovery",
    "workflow": "development",
    "utility": "utility",
    "meta": "utility",
    "standard": "development",
    "enhanced": "development",
    "advanced": "quality",
}

# Claude-only tool references to remove
CLAUDE_TOOLS = {
    "TodoWrite", "Glob", "Grep", "Read", "Write", "Edit", "MultiEdit",
    "WebSearch", "WebFetch", "Task", "sequentialthinking",
}


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def extract_triggers(content: str) -> list[str]:
    """Extract trigger descriptions from ## Triggers section."""
    match = re.search(r"## Triggers\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
    if not match:
        return []
    triggers = []
    for line in match.group(1).strip().splitlines():
        line = line.strip().lstrip("- ")
        if line and not line.startswith("#") and not line.startswith("```"):
            # Clean up Claude-specific language
            line = line.replace("Claude Code", "Codex")
            triggers.append(line)
    return triggers[:5]  # Keep top 5


def extract_workflow(content: str) -> list[str]:
    """Extract workflow steps from ## Behavioral Flow section."""
    match = re.search(r"## Behavioral Flow\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
    if not match:
        return ["analyze_request", "execute", "validate"]
    steps = []
    for line in match.group(1).strip().splitlines():
        line = line.strip()
        # Match numbered steps like "1. **Analyze**: ..."
        m = re.match(r"\d+\.\s+\*\*(\w+)\*\*", line)
        if m:
            steps.append(m.group(1).lower().replace(" ", "_"))
    return steps or ["analyze_request", "execute", "validate"]


def extract_safety(content: str, name: str) -> dict:
    """Determine safety settings based on command nature."""
    code_commands = {
        "implement", "build", "improve", "cleanup", "test", "troubleshoot", "git",
    }
    file_commands = code_commands | {
        "brainstorm", "design", "document", "workflow", "research",
        "save", "index", "index-repo", "estimate", "spec-panel",
    }
    return {
        "writes_code": name in code_commands,
        "writes_files": name in file_commands,
        "requires_user_confirmation_for_scope_change": name not in {"help", "sc", "recommend", "select-tool", "load", "explain"},
    }


def extract_output_contract(content: str, name: str) -> dict:
    """Determine output contract based on command."""
    contracts = {
        "brainstorm": ("design_doc", ["problem_statement", "constraints", "approaches_considered", "recommended_approach", "next_steps"]),
        "design": ("architecture_spec", ["system_overview", "components", "interfaces", "data_flow", "deployment"]),
        "implement": ("implementation", ["implementation_plan", "code_changes", "tests", "validation_summary"]),
        "build": ("build_report", ["build_output", "errors_resolved", "artifacts"]),
        "test": ("test_report", ["test_results", "coverage_summary", "failures_and_fixes"]),
        "analyze": ("analysis_report", ["summary", "findings", "recommendations", "severity_breakdown"]),
        "troubleshoot": ("diagnosis_report", ["symptom", "root_cause", "fix_applied", "verification"]),
        "improve": ("improvement_report", ["changes_made", "before_after", "metrics"]),
        "cleanup": ("cleanup_report", ["removed_items", "refactored_items", "impact_summary"]),
        "document": ("documentation", ["content", "structure", "references"]),
        "research": ("research_report", ["findings", "sources", "synthesis", "recommendations"]),
        "estimate": ("estimate", ["scope", "effort_breakdown", "risks", "timeline"]),
        "reflect": ("retrospective", ["what_worked", "what_failed", "action_items"]),
        "explain": ("explanation", ["overview", "details", "examples"]),
        "git": ("git_operations", ["changes_summary", "commit_info"]),
        "workflow": ("workflow_spec", ["steps", "dependencies", "automation"]),
        "pm": ("project_status", ["progress", "blockers", "next_steps"]),
        "task": ("task_list", ["tasks", "priorities", "assignments"]),
        "recommend": ("recommendations", ["suggested_commands", "rationale"]),
        "select-tool": ("tool_selection", ["recommended_tool", "rationale"]),
        "business-panel": ("business_analysis", ["market_assessment", "strategy", "recommendations"]),
        "spec-panel": ("specification_review", ["feedback", "improvements", "approval_status"]),
        "agent": ("agent_result", ["delegation_summary", "output"]),
        "spawn": ("spawn_result", ["subtasks", "results"]),
        "index-repo": ("repository_index", ["structure", "key_files", "summary"]),
        "index": ("index", ["structure", "summary"]),
        "load": ("session_state", ["restored_context"]),
        "save": ("session_snapshot", ["saved_context"]),
        "sc": ("command_list", ["available_commands"]),
        "help": ("help_text", ["command_info"]),
    }
    primary, sections = contracts.get(name, ("result", ["output"]))
    return {"primary": primary, "required_sections": sections}


def convert_command(md_path: Path) -> dict | None:
    """Convert a single old command markdown to Command IR dict."""
    content = md_path.read_text()
    fm = parse_frontmatter(content)
    name = fm.get("name", md_path.stem)
    # Strip any existing sc: prefix from old names
    if name.startswith("sc:"):
        name = name[3:]

    if name in ALREADY_MIGRATED:
        return None

    desc = fm.get("description", "").strip('"')
    old_category = fm.get("category", "utility")
    personas_raw = fm.get("personas", [])
    mcp_raw = fm.get("mcp-servers", [])

    # Map personas
    personas = []
    for p in personas_raw:
        # Normalize persona names
        p = p.replace("qa-specialist", "quality-engineer")
        p = p.replace("quality", "quality-engineer")
        p = p.replace("architect", "system-architect")
        if p not in personas:
            personas.append(p)

    # Map MCP servers (remove Claude-only ones)
    mcp_optional = []
    for m in mcp_raw:
        if m in ("sequential", "sequential-thinking"):
            mcp_optional.append("sequential-thinking")
        elif m in ("context7", "tavily", "playwright", "magic", "chrome-devtools"):
            mcp_optional.append(m)
        # Skip morphllm, serena (Claude-specific)

    # Determine category
    category = CATEGORY_MAP.get(old_category, "utility")
    # Override specific commands
    if name in ("brainstorm", "design", "estimate", "spec-panel", "business-panel"):
        category = "discovery"
    elif name in ("implement", "build", "improve", "cleanup", "explain"):
        category = "development"
    elif name in ("test", "analyze", "troubleshoot", "reflect"):
        category = "quality"
    elif name in ("document", "help"):
        category = "documentation"
    elif name in ("git",):
        category = "version_control"
    elif name in ("pm", "task", "workflow"):
        category = "project_management"
    elif name in ("research",):
        category = "research"

    triggers = extract_triggers(content)
    workflow = extract_workflow(content)
    safety = extract_safety(content, name)
    output_contract = extract_output_contract(content, name)

    return {
        "schema_version": 1,
        "id": name,
        "display_name": f"/sc:{name}",
        "category": category,
        "description": desc,
        "aliases": [f"/sc:{name}", f"sc:{name}", name],
        "triggers": triggers,
        "workflow": workflow,
        "personas": personas,
        "mcp": {"optional": mcp_optional} if mcp_optional else {},
        "safety": safety,
        "output_contract": output_contract,
        "codex": {
            "skill_name": f"superclaude-{name}",
            "default_reasoning": "high" if name in ("implement", "troubleshoot", "analyze", "research", "design") else "medium",
            "web_search": "required" if name == "research" else "optional",
        },
    }


def main():
    if not OLD_COMMANDS_DIR.exists():
        print(f"ERROR: {OLD_COMMANDS_DIR} not found")
        sys.exit(1)

    NEW_COMMANDS_DIR.mkdir(parents=True, exist_ok=True)

    converted = 0
    skipped = 0
    errors = []

    for md_path in sorted(OLD_COMMANDS_DIR.glob("*.md")):
        if md_path.name in SKIP_FILES:
            continue

        try:
            result = convert_command(md_path)
            if result is None:
                skipped += 1
                continue

            out_path = NEW_COMMANDS_DIR / f"{result['id']}.yaml"
            with open(out_path, "w") as f:
                yaml.dump(result, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            converted += 1
            print(f"  ✅ {md_path.name} → {out_path.name}")
        except Exception as exc:
            errors.append(f"{md_path.name}: {exc}")
            print(f"  ❌ {md_path.name}: {exc}")

    print(f"\nConverted: {converted}, Skipped (already migrated): {skipped}, Errors: {len(errors)}")
    if errors:
        for e in errors:
            print(f"  ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
