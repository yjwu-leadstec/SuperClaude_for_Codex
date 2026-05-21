"""Skill renderer — generates Codex SKILL.md files from Command IR.

Each command produces a skill directory:
    ~/.codex/skills/superclaude-{id}/SKILL.md
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path

from superclaude_codex.codex.parameters import (
    format_global_priority_lines,
    format_parameter_lines,
    yaml_quote,
)
from superclaude_codex.core.command_ir import CommandIR
from superclaude_codex.core.registry import CommandRegistry

SUPPORTED_UI_LOCALES = {"auto", "en", "zh-CN", "zh-TW"}

ZH_CN_SHORT_DESCRIPTIONS = {
    "agent": "委派专家代理，按任务类型分配专门执行者",
    "analyze": "分析代码质量、安全、性能和架构问题",
    "brainstorm": "通过提问和探索梳理需求、想法和方案",
    "build": "构建、编译和打包项目，并辅助处理构建错误",
    "business-panel": "多专家商业策略讨论与决策建议",
    "cleanup": "清理死代码、技术债和项目结构问题",
    "design": "设计系统架构、API 和组件接口",
    "document": "为组件、函数、API 或功能生成文档",
    "estimate": "评估任务、功能或项目的开发工作量",
    "explain": "解释代码、概念和系统行为",
    "git": "辅助 Git 操作、提交信息和工作流",
    "help": "查看可用 sc 命令及其用法",
    "implement": "实现功能、组件、API 或代码改动",
    "improve": "系统性改进代码质量、性能和可维护性",
    "index": "生成项目文档和知识库索引",
    "index-repo": "构建仓库索引，压缩上下文占用",
    "load": "加载项目上下文和会话状态",
    "pm": "项目经理代理，协调任务和子代理",
    "recommend": "根据需求推荐合适的 sc 命令",
    "reflect": "复盘任务并验证结果质量",
    "research": "深度网络研究与资料整理",
    "save": "保存会话上下文、学习记录和检查点",
    "sc": "命令分发器，用于访问所有 SuperClaude 功能",
    "select-tool": "根据任务复杂度选择合适工具",
    "spawn": "拆解复杂任务并进行并行编排",
    "spec-panel": "多专家规格评审和改进建议",
    "task": "执行复杂任务并管理工作流",
    "test": "运行测试、分析覆盖率和质量问题",
    "troubleshoot": "诊断并修复代码、构建或部署问题",
    "workflow": "根据需求生成结构化实施流程",
}


ZH_TW_SHORT_DESCRIPTIONS = {
    "agent": "委派專家代理，按任務類型分配專門執行者",
    "analyze": "分析程式碼品質、安全、效能和架構問題",
    "brainstorm": "透過提問和探索梳理需求、想法和方案",
    "build": "建置、編譯和打包專案，並輔助處理建置錯誤",
    "business-panel": "多專家商業策略討論與決策建議",
    "cleanup": "清理死碼、技術債和專案結構問題",
    "design": "設計系統架構、API 和元件介面",
    "document": "為元件、函式、API 或功能產生文件",
    "estimate": "評估任務、功能或專案的開發工作量",
    "explain": "解釋程式碼、概念和系統行為",
    "git": "輔助 Git 操作、提交訊息和工作流程",
    "help": "查看可用 sc 命令及其用法",
    "implement": "實作功能、元件、API 或程式碼改動",
    "improve": "系統性改進程式碼品質、效能和可維護性",
    "index": "產生專案文件和知識庫索引",
    "index-repo": "建立倉庫索引，壓縮上下文占用",
    "load": "載入專案上下文和會話狀態",
    "pm": "專案經理代理，協調任務和子代理",
    "recommend": "根據需求推薦合適的 sc 命令",
    "reflect": "覆盤任務並驗證結果品質",
    "research": "深度網路研究與資料整理",
    "save": "儲存會話上下文、學習記錄和檢查點",
    "sc": "命令分發器，用於存取所有 SuperClaude 功能",
    "select-tool": "根據任務複雜度選擇合適工具",
    "spawn": "拆解複雜任務並進行平行編排",
    "spec-panel": "多專家規格評審和改進建議",
    "task": "執行複雜任務並管理工作流程",
    "test": "執行測試、分析覆蓋率和品質問題",
    "troubleshoot": "診斷並修復程式碼、建置或部署問題",
    "workflow": "根據需求產生結構化實作流程",
}


def _resolve_chinese_locale(value: str) -> str:
    normalized = value.replace("_", "-").lower()
    if (
        normalized.startswith("zh-tw")
        or normalized.startswith("zh-hk")
        or normalized.startswith("zh-mo")
        or "hant" in normalized
    ):
        return "zh-TW"
    return "zh-CN"


def detect_ui_locale_from_env(env: Mapping[str, str] | None = None) -> str:
    """Detect the UI locale from shell locale environment variables."""
    source = os.environ if env is None else env
    for key in ("LC_ALL", "LC_MESSAGES", "LANG"):
        value = source.get(key, "").strip()
        if not value:
            continue
        if value.replace("_", "-").lower().startswith("zh"):
            return _resolve_chinese_locale(value)
        return "en"
    return "en"


def normalize_ui_locale(
    ui_locale: str = "auto", env: Mapping[str, str] | None = None
) -> str:
    """Normalize the install-time UI locale for generated skill metadata."""
    value = ui_locale.strip() if ui_locale else "auto"
    if value.lower() == "auto":
        return detect_ui_locale_from_env(env)
    if value.lower() in {"zh", "zh-cn", "zh_cn", "zh-hans", "zh_hans", "cn"}:
        return "zh-CN"
    if value.lower() in {"zh-tw", "zh_tw", "zh-hant", "zh_hant", "tw"}:
        return "zh-TW"
    if value.lower() in {"en", "en-us", "en_us"}:
        return "en"
    raise ValueError(
        f"Unsupported locale: {ui_locale}. Supported values: auto, en, zh-CN, zh-TW."
    )


def get_short_description(command: CommandIR, ui_locale: str = "en") -> str:
    """Return the UI-only short description for a command."""
    locale = normalize_ui_locale(ui_locale)
    if locale == "zh-CN":
        return ZH_CN_SHORT_DESCRIPTIONS.get(command.id, command.description)
    if locale == "zh-TW":
        return ZH_TW_SHORT_DESCRIPTIONS.get(command.id, command.description)
    return command.description


def render_skill(command: CommandIR) -> str:
    """Render a SKILL.md from a CommandIR."""
    lines = [
        "---",
        f"name: {command.codex.skill_name}",
        f"description: {command.description}",
        "---",
        "",
        f"# {command.display_name}",
        "",
    ]

    # When to use
    if command.triggers:
        lines.append("## When to Use")
        lines.append("")
        lines.append(f"Use this skill when the user invokes `{command.display_name}`.")
        lines.append("Also activate when:")
        for trigger in command.triggers:
            lines.append(f"- {trigger}")
        lines.append("")

    # Aliases
    if len(command.aliases) > 1:
        lines.append("## Aliases")
        lines.append("")
        for alias in command.aliases:
            lines.append(f"- `{alias}`")
        lines.append("")

    # Inputs
    inputs = command.inputs
    positional = inputs.get("positional", [])
    flags = inputs.get("flags", [])
    if positional or flags:
        lines.append("## Inputs")
        lines.append("")
        lines.extend(format_parameter_lines(inputs))
        lines.append("")

    lines.append("## Global Flags")
    lines.append("")
    lines.append(
        "All `/sc-*` commands accept shared SuperClaude global flags such as "
        "`--think`, `--think-hard`, `--ultrathink`, `--validate`, `--safe-mode`, "
        "`--uc`, `--scope`, `--focus`, and MCP selection flags like `--c7`, "
        "`--seq`, `--serena`, `--play`, and `--no-mcp`."
    )
    lines.append("")
    lines.extend(format_global_priority_lines())
    lines.append("")

    # Codex behavior
    if (
        command.codex.default_reasoning != "medium"
        or command.codex.web_search != "optional"
    ):
        lines.append("## Codex Behavior")
        lines.append("")
        lines.append(f"- Reasoning effort: **{command.codex.default_reasoning}**")
        lines.append(f"- Web search: **{command.codex.web_search}**")
        lines.append("")

    # Workflow
    if command.workflow:
        lines.append("## Workflow")
        lines.append("")
        for i, step in enumerate(command.workflow, 1):
            lines.append(f"{i}. {step.replace('_', ' ').capitalize()}")
        lines.append("")

    # Personas
    if command.personas:
        lines.append("## Personas")
        lines.append("")
        for persona in command.personas:
            lines.append(f"- Activate **{persona}** when relevant to the task.")
        lines.append("")

    # MCP
    optional_mcp = command.mcp.get("optional", [])
    if optional_mcp:
        lines.append("## MCP Servers")
        lines.append("")
        lines.append("Optionally leverage:")
        for server in optional_mcp:
            lines.append(f"- {server}")
        lines.append("")

    # Safety
    lines.append("## Safety")
    lines.append("")
    if not command.safety.writes_code:
        lines.append(
            "Do not write or modify code unless the user explicitly requests it."
        )
    if command.safety.requires_user_confirmation_for_scope_change:
        lines.append(
            "Ask for user confirmation before changing scope beyond the original request."
        )
    lines.append("")

    # Output contract
    if command.output_contract.primary:
        lines.append("## Output")
        lines.append("")
        lines.append(
            f"Return a structured **{command.output_contract.primary.replace('_', ' ')}**"
            " containing:"
        )
        for section in command.output_contract.required_sections:
            lines.append(f"- {section.replace('_', ' ').capitalize()}")
        lines.append("")

    # Completion
    lines.append("## Completion")
    lines.append("")
    lines.append(
        f"After completing `{command.display_name}`, suggest relevant follow-up commands."
    )
    lines.append("")

    return "\n".join(lines)


def render_openai_yaml(command: CommandIR, ui_locale: str = "en") -> str:
    """Render Codex UI metadata for a skill."""
    skill_name = command.codex.skill_name
    display_name = command.display_name.removeprefix("/")
    default_prompt = f"Use ${skill_name} for this task."
    short_description = get_short_description(command, ui_locale)
    lines = [
        "interface:",
        f"  display_name: {yaml_quote(display_name)}",
        f"  short_description: {yaml_quote(short_description)}",
        f"  default_prompt: {yaml_quote(default_prompt)}",
        "policy:",
        "  allow_implicit_invocation: true",
        "",
    ]
    return "\n".join(lines)


def write_skill(codex_home: Path, command: CommandIR, ui_locale: str = "en") -> Path:
    """Write a SKILL.md file for a command."""
    skill_dir = codex_home / "skills" / command.codex.skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_path = skill_dir / "SKILL.md"
    skill_path.write_text(render_skill(command))

    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (agents_dir / "openai.yaml").write_text(render_openai_yaml(command, ui_locale))
    return skill_path


def render_all_skills(
    registry: CommandRegistry, codex_home: Path, ui_locale: str = "en"
) -> list[Path]:
    """Render SKILL.md for all commands in the registry."""
    paths = []
    for cmd in registry.list_commands():
        paths.append(write_skill(codex_home, cmd, ui_locale))
    return paths
