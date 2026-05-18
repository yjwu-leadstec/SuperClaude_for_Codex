#!/usr/bin/env python3
"""One-time migration: convert old agent .md files to agent YAML definitions."""

import re
import sys
from pathlib import Path

import yaml

OLD_AGENTS_DIR = Path("src/superclaude/agents")
NEW_AGENTS_DIR = Path("src/superclaude_codex/assets/agents")
SKIP_FILES = {"README.md", "deep-research.md", "repo-index.md", "self-review.md"}


def parse_frontmatter(content: str) -> dict:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def extract_triggers(content: str) -> list[str]:
    match = re.search(r"## Triggers\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
    if not match:
        return []
    triggers = []
    for line in match.group(1).strip().splitlines():
        line = line.strip().lstrip("- ")
        if line and not line.startswith("#"):
            line = line.replace("Claude Code", "Codex")
            triggers.append(line)
    return triggers[:5]


def extract_expertise(content: str) -> list[str]:
    # Look for key expertise areas in the content
    expertise = []
    for section_name in ("## Core", "## Key", "## Expertise", "## Behavioral"):
        match = re.search(rf"{section_name}.*?\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
        if match:
            for line in match.group(1).strip().splitlines():
                line = line.strip().lstrip("- *")
                if line and not line.startswith("#") and not line.startswith("```"):
                    # Extract just the bold keyword if present
                    m = re.match(r"\*\*(.+?)\*\*", line)
                    if m:
                        expertise.append(m.group(1).lower())
            break
    return expertise[:8]


def convert_agent(md_path: Path) -> dict:
    content = md_path.read_text()
    fm = parse_frontmatter(content)
    name = fm.get("name", md_path.stem)
    desc = fm.get("description", "").strip('"')

    return {
        "schema_version": 1,
        "id": name,
        "name": name.replace("-", " ").title(),
        "description": desc,
        "triggers": extract_triggers(content),
        "expertise": extract_expertise(content),
        "output_expectations": [
            "explain tradeoffs",
            "prefer existing project patterns",
            "include tests for behavior changes",
        ],
    }


def main():
    if not OLD_AGENTS_DIR.exists():
        print(f"ERROR: {OLD_AGENTS_DIR} not found")
        sys.exit(1)

    NEW_AGENTS_DIR.mkdir(parents=True, exist_ok=True)

    agents = []
    for md_path in sorted(OLD_AGENTS_DIR.glob("*.md")):
        if md_path.name in SKIP_FILES:
            continue
        try:
            agent = convert_agent(md_path)
            out_path = NEW_AGENTS_DIR / f"{agent['id']}.yaml"
            with open(out_path, "w") as f:
                yaml.dump(agent, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            agents.append(agent)
            print(f"  ✅ {md_path.name} → {agent['id']}.yaml")
        except Exception as exc:
            print(f"  ❌ {md_path.name}: {exc}")

    # Generate agents.json
    agents_json = {
        "schema_version": 1,
        "package_version": "0.1.0",
        "agents": [{"id": a["id"], "name": a["name"], "description": a["description"]} for a in agents],
    }

    import json
    agents_json_path = NEW_AGENTS_DIR.parent.parent / "core" / "agents_registry.json"
    # We'll put it alongside the assets for now
    agents_json_path = NEW_AGENTS_DIR / "agents.json"
    with open(agents_json_path, "w") as f:
        json.dump(agents_json, f, indent=2, ensure_ascii=False)
    print(f"\n  📦 agents.json: {len(agents)} agents")
    print(f"\nConverted: {len(agents)} agents")


if __name__ == "__main__":
    main()
