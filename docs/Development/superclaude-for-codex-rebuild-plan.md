# SuperClaude for Codex 重构计划

Generated: 2026-05-18
Status: Draft
Project: SuperClaude for Codex

## 1. 项目定位

SuperClaude for Codex 是一个全新的 Codex-native 项目，不是现有 SuperClaude 的多宿主适配层，也不是 Claude Code 配置的迁移工具。

项目目标是让新用户在 Codex 中获得 SuperClaude 风格的结构化工作流体验，同时保持熟悉的 `/sc:*` 命令入口：

```text
/sc:brainstorm "设计一个产品想法"
/sc:implement "实现登录功能"
/sc:analyze .
/sc:test
/sc:troubleshoot "这个错误"
```

核心约束：

- 只面向 Codex。
- 全新安装到 Codex 环境。
- 不读取、不修改、不依赖 `~/.claude`。
- 不提供 Claude legacy 安装路径。
- 不把 Claude Code 的工具名和运行假设带进 Codex。
- 用户输入习惯保持 `/sc:*`，底层实现完全 Codex-native。

最终产品一句话：

> SuperClaude for Codex 是一套为 OpenAI Codex 构建的结构化开发工作流、命令、skills、agents 和 MCP 配置包。

## 2. 用户体验目标

新机器上的理想路径：

```bash
pipx install superclaude-for-codex
superclaude-codex install
codex
```

进入 Codex 后，用户可以直接输入：

```text
/sc:brainstorm "AI 项目管理工具"
```

Codex 应识别为 SuperClaude brainstorm 工作流，并按对应 skill 执行。

安装后只允许写入 Codex 相关路径：

```text
~/.codex/
  AGENTS.md
  config.toml
  skills/
  superclaude-for-codex/
```

明确不允许读写：

```text
~/.claude/
~/.claude/commands/
~/.claude/skills/
~/.claude.json
```

## 3. 成功标准

项目完成的标准不是“能安装”，而是满足以下验收路径：

```text
1. 安装 Codex。
2. pipx install superclaude-for-codex。
3. superclaude-codex install。
4. 打开 Codex。
5. 输入 /sc:brainstorm "..."。
6. Codex 按 SuperClaude brainstorm 工作流执行。
7. 输入 /sc:implement "..."。
8. Codex 按 SuperClaude implement 工作流执行。
9. 整个过程没有读写 ~/.claude。
```

功能验收：

- 30 个 `/sc:*` 命令全部可用。
- 每个命令都有 Codex skill。
- 每个命令都在 `commands.json` 中注册。
- `AGENTS.md` 包含稳定的 `/sc:*` 路由规则。
- `superclaude-codex doctor` 能检查安装健康。
- `superclaude-codex verify` 能执行 smoke checks。
- MCP 配置写入 Codex config。
- 所有测试使用临时 `CODEX_HOME`，并验证不会触碰 `~/.claude`。

### 3.1 工程评审结论

本计划经过工程负责人视角复核后，方向成立，但必须补齐以下门禁后才能进入实现：

1. **安装必须原子化**：写入 `~/.codex/AGENTS.md`、`~/.codex/config.toml`、`~/.codex/skills/` 时必须先写临时文件和备份，全部成功后再提交。失败时必须回滚到安装前状态。
2. **新包必须和旧包硬隔离**：`src/superclaude_codex/` 不能 import `src/superclaude/cli/install_*`，因为旧代码里存在 `~/.claude` 和 `claude mcp` 假设。旧代码只能作为数据迁移来源，不能作为运行时依赖。
3. **Command IR 必须版本化**：`commands.json`、`agents.json`、每个 command YAML 都要带 `schema_version`，否则后续 30 个命令批量迁移后无法安全升级。
4. **`/sc:*` 无感体验必须有验收矩阵**：Codex 原生 custom slash 能力如果不满足要求，第一版必须明确 text-route 的最低体验和失败提示，不能把不确定性藏在“调研”里。
5. **发布流水线必须纳入 1.0 范围**：这是新的 PyPI 包和 CLI artifact，计划必须包含 build、publish、version、smoke install 的 CI/CD。
6. **测试计划必须覆盖安装副作用**：不只是函数单测，还要覆盖用户已有 `AGENTS.md`、已有 `config.toml`、无权限目录、部分写入失败、重复安装和卸载/清理策略。

Lake Score: 6/6 关键建议选择完整方案。原因：这些完整性检查用 AI 辅助实现成本很低，但能避免安装器和命令系统发布后伤害用户环境。

## 4. 新包结构

推荐新包名：

```text
superclaude-for-codex
```

推荐 CLI 名：

```text
superclaude-codex
```

推荐 Python 包结构：

```text
src/superclaude_codex/
  __init__.py
  __version__.py

  cli/
    __init__.py
    main.py
    doctor.py

  core/
    __init__.py
    command_ir.py
    registry.py
    validation.py

  codex/
    __init__.py
    paths.py
    installer.py
    agents_md.py
    skills.py
    commands.py
    mcp.py
    verify.py

  assets/
    commands/
      brainstorm.yaml
      implement.yaml
      analyze.yaml
      test.yaml
      troubleshoot.yaml
      ...

    agents/
      python-expert.yaml
      security-engineer.yaml
      frontend-architect.yaml
      ...

    skills/
      confidence-check/
        SKILL.md
        confidence.ts
```

旧 `src/superclaude/` 可以作为内容来源参考，但新实现不应继续挂在旧包命名空间下。

### 4.1 代码隔离边界

新包的工程边界必须明确：

```text
src/superclaude_codex/       # 新运行时代码，允许发布
src/superclaude/             # 旧项目代码，只允许作为人工参考
tests/superclaude_codex/     # 新项目测试
```

禁止事项：

- `superclaude_codex` 运行时代码禁止 import `superclaude.cli.install_commands`。
- `superclaude_codex` 运行时代码禁止 import `superclaude.cli.install_mcp`。
- `superclaude_codex` 运行时代码禁止调用 `claude` CLI。
- `superclaude_codex` 测试必须有 import guard，确保新包不会加载旧 installer。

允许事项：

- 可以写一次性脚本从旧 `src/superclaude/commands/*.md` 生成初版 YAML。
- 可以在 `docs/` 中引用旧命令作为语义来源。
- 可以在测试 fixtures 中读取旧 markdown 做 equivalence checks，但不能把旧 markdown 作为运行时唯一真相。

验收：

```bash
rg -n "from superclaude|import superclaude|~/.claude|claude mcp" src/superclaude_codex tests/superclaude_codex
```

除文档字符串和明确的负向测试 fixture 外，结果必须为空。

## 5. CLI 设计

基础命令：

```bash
superclaude-codex install
superclaude-codex doctor
superclaude-codex verify
superclaude-codex commands list
superclaude-codex commands validate
superclaude-codex mcp list
superclaude-codex mcp install
superclaude-codex build
```

安装命令：

```bash
superclaude-codex install
superclaude-codex install --dry-run
superclaude-codex install --force
```

命令管理：

```bash
superclaude-codex commands list
superclaude-codex commands show brainstorm
superclaude-codex commands validate
```

MCP 管理：

```bash
superclaude-codex mcp list
superclaude-codex mcp install context7 playwright tavily
superclaude-codex mcp install --all
superclaude-codex mcp install --dry-run
```

验证：

```bash
superclaude-codex doctor
superclaude-codex verify
```

不要提供：

```bash
superclaude install --host codex
superclaude migrate --from claude --to codex
```

原因：这是全新 Codex 项目，不是旧 SuperClaude 的宿主切换功能。

## 6. Codex 安装目标

默认 Codex home 解析：

1. 优先使用 `CODEX_HOME`。
2. 没有设置时使用 `~/.codex`。

安装后结构：

```text
~/.codex/
  AGENTS.md
  config.toml

  skills/
    superclaude-brainstorm/
      SKILL.md
    superclaude-implement/
      SKILL.md
    superclaude-analyze/
      SKILL.md
    ...

  superclaude-for-codex/
    commands.json
    agents.json
    version.json
    install-report.json
```

`AGENTS.md` 更新规则：

- 不覆盖用户已有内容。
- 只插入或替换 marker 内的 SuperClaude block。
- marker 格式固定：

```markdown
<!-- BEGIN SUPERCLAUDE FOR CODEX -->
...
<!-- END SUPERCLAUDE FOR CODEX -->
```

### 6.1 原子安装与回滚

安装器必须按事务式流程执行：

```text
prepare
  ├── resolve CODEX_HOME
  ├── read existing files
  ├── create backup snapshot
  └── render all outputs in memory

stage
  ├── write temp AGENTS.md
  ├── write temp config.toml
  ├── write temp skills directory
  └── validate rendered files

commit
  ├── atomic replace AGENTS.md
  ├── atomic replace config.toml
  ├── atomic replace skills
  └── write install-report.json

rollback
  ├── restore backup files
  ├── remove temp files
  └── report failed step
```

必须覆盖的失败场景：

- `AGENTS.md` 可写但 `config.toml` 不可写。
- skill 写到一半失败。
- `commands.json` 渲染失败。
- 用户已有 marker block 但内容损坏。
- 重复执行 `install`。
- `--force` 执行时已有旧版本 assets。

安装报告：

```json
{
  "version": "0.1.0",
  "codex_home": "/Users/example/.codex",
  "files_written": [],
  "files_backed_up": [],
  "commands_installed": 30,
  "status": "success"
}
```

## 7. Command IR

所有 `/sc:*` 命令都必须迁移到结构化 Command IR。

示例：

```yaml
schema_version: 1
id: brainstorm
display_name: /sc:brainstorm
category: discovery
description: Interactive requirements discovery and ideation.

aliases:
  - /sc:brainstorm
  - sc:brainstorm
  - brainstorm

triggers:
  - user wants to explore an idea
  - user asks to brainstorm
  - user describes a product concept

inputs:
  positional:
    - name: topic
      required: false
  flags:
    - name: strategy
      values: [systematic, agile, enterprise]
    - name: depth
      values: [shallow, normal, deep]

workflow:
  - understand_request
  - inspect_project_context
  - ask_targeted_questions
  - generate_alternatives
  - challenge_assumptions
  - produce_design_doc

personas:
  - analyst
  - product
  - architect

mcp:
  optional:
    - context7
    - tavily

safety:
  writes_code: false
  writes_files: true
  requires_user_confirmation_for_scope_change: true

output_contract:
  primary: design_doc
  required_sections:
    - problem_statement
    - constraints
    - approaches_considered
    - recommended_approach
    - next_steps

codex:
  skill_name: superclaude-brainstorm
  default_reasoning: medium
  web_search: optional
```

IR 原则：

- 保留 `/sc:*` 用户接口。
- 保留原 SuperClaude 工作流语义。
- 删除 Claude-only 工具名。
- 输出 Codex 能理解的行为说明。
- 每个命令可被 renderer 生成 skill、command registry 和 AGENTS route。

### 7.1 IR 版本化和兼容合同

每个 command YAML 必须包含：

- `schema_version`
- `id`
- `display_name`
- `aliases`
- `workflow`
- `safety`
- `output_contract`
- `codex.skill_name`

`commands.json` 必须包含：

```json
{
  "schema_version": 1,
  "package_version": "0.1.0",
  "commands": []
}
```

兼容合同：

- `aliases` 中的 `/sc:*` 名称一旦发布不能删除，只能新增。
- `output_contract.primary` 一旦发布不能静默改变。
- 命令行为大改必须提升 `schema_version` 或在 changelog 中列为 breaking change。
- 30 个命令都必须有 golden render 输出，防止 renderer 改动悄悄改变用户体验。

命令迁移不是“复制 markdown”，而是三步：

```text
old command markdown
  ├── extract intent, flags, workflow, boundaries
  ├── remove Claude-only tool assumptions
  └── encode as versioned Command IR
        ├── render Codex skill
        ├── render AGENTS route
        └── render commands.json
```

## 8. Codex AGENTS.md Renderer

`AGENTS.md` 只做轻量全局路由和共同规则，不塞入 30 个命令全文。

生成内容应包含：

```markdown
## SuperClaude for Codex

This Codex environment has SuperClaude for Codex installed.

When the user invokes a command matching `/sc:*`, treat it as a SuperClaude command.
Resolve the command through the installed SuperClaude command registry.
Prefer the matching skill in `~/.codex/skills/superclaude-*`.

Examples:
- `/sc:brainstorm` uses the `superclaude-brainstorm` skill.
- `/sc:implement` uses the `superclaude-implement` skill.
- `/sc:analyze` uses the `superclaude-analyze` skill.
- `/sc:test` uses the `superclaude-test` skill.

Do not look for or modify Claude Code configuration.
Do not read or write `~/.claude`.
```

约束：

- 控制长度。
- 不写入 Claude 工具名。
- 不覆盖用户手写 Codex 指令。
- 可重复执行，结果稳定。

## 9. Codex Skill Renderer

每个 command IR 生成一个 Codex skill：

```text
~/.codex/skills/superclaude-{id}/SKILL.md
```

每个 `SKILL.md` 至少包含：

- command name
- aliases
- when to use
- workflow
- Codex tool behavior
- personas
- MCP recommendations
- safety rules
- output contract
- completion criteria
- follow-up command suggestions

示例 skill 结构：

```markdown
---
name: superclaude-brainstorm
description: SuperClaude brainstorm workflow for Codex.
---

# /sc:brainstorm

Use this skill when the user invokes `/sc:brainstorm` or asks to explore an idea.

## Workflow

1. Understand the request.
2. Inspect relevant project context.
3. Ask targeted questions only when needed.
4. Generate alternative approaches.
5. Challenge assumptions.
6. Produce a design document or requirements summary.

## Safety

Do not implement code unless the user explicitly changes from brainstorming to implementation.

## Output

Return a structured design document with problem, constraints, options, recommendation, and next steps.
```

## 10. /sc:* 无感体验

目标：用户直接输入 `/sc:brainstorm`，Codex 能按 SuperClaude workflow 执行。

实现优先级：

1. 优先使用 Codex 原生 slash/custom command 能力。
2. 如果原生能力不足，用 `AGENTS.md` 路由规则加 Codex skills 触发。
3. 保证文本形式 `/sc:*` 至少可被 Codex 正确解释。

不要把目标退化成：

```bash
superclaude-codex run brainstorm "..."
```

这个命令可以作为调试入口，但不能作为主用户体验。

### 10.1 `/sc:*` 验收矩阵

`/sc:*` 能力必须按矩阵验收，不能停留在“理论可触发”：

| 场景 | 期望 | 失败时行为 |
|------|------|------------|
| 用户输入 `/sc:brainstorm "x"` | Codex 使用 brainstorm skill | 输出明确提示：SuperClaude route 未加载，建议运行 `superclaude-codex doctor` |
| 用户输入 `/sc:implement "x"` | Codex 使用 implement skill，并允许代码修改 | 输出具体实施计划，不退化成泛泛建议 |
| 用户输入 `/sc:unknown` | Codex 列出相近命令 | 不应假装执行未知命令 |
| 用户输入 `/sc` | Codex 显示 30 个命令摘要 | 不应只返回普通聊天 |
| 用户已有 AGENTS.md 规则冲突 | SuperClaude block 不覆盖用户规则，但 route 明确 | `doctor` 标记冲突并给出修复建议 |

第一版允许 text-route 作为实现方式，但验收必须以用户体验为准：用户不需要输入额外 CLI，不需要知道 skill 路径。

## 11. Agents / Personas

旧项目中的 agents 要迁移成 Codex-neutral specialist definitions。

示例：

```yaml
id: python-expert
name: Python Expert
description: Production Python specialist.
triggers:
  - Python code changes
  - pytest failures
  - packaging issues
expertise:
  - typing
  - packaging
  - pytest
  - async Python
  - security
output_expectations:
  - explain tradeoffs
  - prefer existing project patterns
  - include tests for behavior changes
```

生成：

```text
~/.codex/superclaude-for-codex/agents.json
```

在 command skill 中引用：

```markdown
## Personas

Activate the Python Expert persona when the target codebase is Python or pytest is involved.
Activate the Security Engineer persona when authentication, authorization, secrets, or input validation are involved.
```

如果 Codex surface 支持 subagents，则映射为 subagent guidance。否则退化为 persona activation。

## 12. MCP for Codex

MCP 安装只写 Codex 配置，不调用 Claude CLI。

支持列表：

- context7
- playwright
- tavily
- serena
- chrome-devtools
- sequential-thinking
- magic
- AIRIS gateway

目标配置文件：

```text
~/.codex/config.toml
```

TODO：

- 抽 MCP registry。
- 实现 TOML merge。
- 支持 dry-run。
- 避免覆盖用户已有 MCP 配置。
- 对需要 API key 的 MCP 给出明确提示。
- 所有文案使用 Codex-first 表达。

### 12.1 Codex config 合并安全

`config.toml` 合并必须遵守：

- 解析失败时不写入。
- 写入前创建备份。
- 只管理 SuperClaude for Codex 自己声明的 MCP entries。
- 不删除用户已有 MCP。
- 不重排无关配置。
- `--dry-run` 输出 diff 摘要。

推荐 marker：

```toml
# BEGIN SUPERCLAUDE FOR CODEX MCP
# END SUPERCLAUDE FOR CODEX MCP
```

如果 Codex config 不支持 TOML 注释块稳定保留，则改用 sidecar manifest：

```text
~/.codex/superclaude-for-codex/managed-mcp.json
```

并在 merge 时只更新 manifest 中归属本项目的 servers。

## 13. 完整命令迁移清单

必须迁移的 30 个命令：

- [ ] `/sc`
- [ ] `/sc:help`
- [ ] `/sc:brainstorm`
- [ ] `/sc:design`
- [ ] `/sc:workflow`
- [ ] `/sc:implement`
- [ ] `/sc:build`
- [ ] `/sc:test`
- [ ] `/sc:analyze`
- [ ] `/sc:troubleshoot`
- [ ] `/sc:improve`
- [ ] `/sc:cleanup`
- [ ] `/sc:document`
- [ ] `/sc:git`
- [ ] `/sc:load`
- [ ] `/sc:save`
- [ ] `/sc:reflect`
- [ ] `/sc:explain`
- [ ] `/sc:recommend`
- [ ] `/sc:estimate`
- [ ] `/sc:task`
- [ ] `/sc:pm`
- [ ] `/sc:research`
- [ ] `/sc:index`
- [ ] `/sc:index-repo`
- [ ] `/sc:agent`
- [ ] `/sc:spawn`
- [ ] `/sc:select-tool`
- [ ] `/sc:business-panel`
- [ ] `/sc:spec-panel`

每个命令的迁移验收 checklist：

- [ ] 有 Command IR。
- [ ] IR schema 校验通过。
- [ ] 生成 Codex skill。
- [ ] 注册到 `commands.json`。
- [ ] 出现在 `AGENTS.md` route table。
- [ ] 不包含 `~/.claude`。
- [ ] 不包含 Claude-only 工具强绑定。
- [ ] 有 golden test。
- [ ] 有 smoke test prompt。
- [ ] 文档中有用法示例。

## 14. 阶段计划

### Phase 1: 项目重命名和包结构

目标：建立新项目骨架。

TODO：

- [ ] 新建 `src/superclaude_codex/`。
- [ ] 调整 `pyproject.toml`。
- [ ] 包名改为 `superclaude-for-codex`。
- [ ] CLI 改为 `superclaude-codex`。
- [ ] 移除新包的 pytest plugin auto-discovery，除非明确设计 Codex 专用 pytest plugin。
- [ ] 更新 coverage source 到 `src/superclaude_codex`。
- [ ] README 改为 Codex-first。
- [ ] 明确项目不会读写 `~/.claude`。

验收：

```bash
superclaude-codex --help
```

### Phase 2: Codex 路径和安装器

目标：完成 Codex home 写入能力。

TODO：

- [ ] 实现 `codex/paths.py`。
- [ ] 支持 `CODEX_HOME`。
- [ ] 实现 `codex/installer.py`。
- [ ] 实现安装事务、备份和回滚。
- [ ] 创建 `skills/`。
- [ ] 创建 `superclaude-for-codex/`。
- [ ] 写 `version.json`。
- [ ] 写 `install-report.json`。
- [ ] 支持 `--dry-run`。
- [ ] 安装时检测并拒绝触碰 `~/.claude`。

验收：

```bash
CODEX_HOME=/tmp/sc-codex-home superclaude-codex install --dry-run
CODEX_HOME=/tmp/sc-codex-home superclaude-codex install
```

### Phase 3: Command IR Registry

目标：让命令成为结构化资产。

TODO：

- [ ] 实现 `core/command_ir.py`。
- [ ] 实现 `core/registry.py`。
- [ ] 实现 `core/validation.py`。
- [ ] 实现 schema version 校验。
- [ ] 实现 breaking-change 检测。
- [ ] 迁入 5 个核心命令：
  - [ ] `brainstorm`
  - [ ] `implement`
  - [ ] `analyze`
  - [ ] `test`
  - [ ] `troubleshoot`
- [ ] 实现 `commands list`。
- [ ] 实现 `commands validate`。

验收：

```bash
superclaude-codex commands list
superclaude-codex commands validate
superclaude-codex commands show brainstorm
```

### Phase 4: AGENTS.md Renderer

目标：Codex 能识别 SuperClaude 路由。

TODO：

- [ ] 实现 `codex/agents_md.py`。
- [ ] 生成 marker block。
- [ ] 幂等更新已有 `AGENTS.md`。
- [ ] 控制输出长度。
- [ ] 把所有已注册命令写入 route table。

验收：

```bash
CODEX_HOME=/tmp/sc-codex-home superclaude-codex install
grep "BEGIN SUPERCLAUDE FOR CODEX" /tmp/sc-codex-home/AGENTS.md
```

### Phase 5: Skill Renderer

目标：每个命令都有 Codex skill。

TODO：

- [ ] 实现 `codex/skills.py`。
- [ ] 为 5 个核心命令生成 skill。
- [ ] 生成 skill frontmatter。
- [ ] 生成 workflow。
- [ ] 生成 safety。
- [ ] 生成 output contract。

验收：

```text
~/.codex/skills/superclaude-brainstorm/SKILL.md
~/.codex/skills/superclaude-implement/SKILL.md
~/.codex/skills/superclaude-analyze/SKILL.md
```

### Phase 6: /sc:* 使用体验

目标：旧命令入口在 Codex 中可用。

TODO：

- [ ] 在 `AGENTS.md` 中声明 `/sc:*` 路由。
- [ ] 生成 `commands.json`。
- [ ] 验证 `/sc:brainstorm` 文本触发。
- [ ] 调研并接入 Codex 原生 slash/custom command 能力。
- [ ] 如果原生 slash 不可用，保留 text-route 作为最低可用体验。

验收：

```text
Codex 中输入 /sc:brainstorm "一个工具"
Codex 应使用 superclaude-brainstorm 工作流响应
```

### Phase 7: 30 命令全量迁移

目标：完整覆盖 SuperClaude 命令表。

TODO：

- [ ] Discovery / Planning 命令迁移。
- [ ] Coding 命令迁移。
- [ ] Quality 命令迁移。
- [ ] Research / Context 命令迁移。
- [ ] Meta / Agents 命令迁移。
- [ ] Utility 命令迁移。
- [ ] 所有命令加入 golden tests。

验收：

```bash
superclaude-codex commands validate
superclaude-codex verify
```

### Phase 8: Agents / Personas

目标：保留 SuperClaude 专家角色体验。

TODO：

- [ ] 新建 `assets/agents/*.yaml`。
- [ ] 迁移 20 个 specialist agents。
- [ ] 生成 `agents.json`。
- [ ] 在 command skills 中引用 personas。
- [ ] 支持 Codex subagent guidance。

验收：

```text
/sc:implement "FastAPI auth"
应自动激活 backend、security、python personas
```

### Phase 9: MCP 配置

目标：Codex 下可一键安装 MCP。

TODO：

- [ ] 实现 `codex/mcp.py`。
- [ ] 抽 MCP registry。
- [ ] 写入 `~/.codex/config.toml`。
- [ ] 支持 TOML merge。
- [ ] 支持 config 备份和失败回滚。
- [ ] 支持 dry-run。
- [ ] 支持 API key 提示。

验收：

```bash
CODEX_HOME=/tmp/sc-codex-home superclaude-codex mcp install context7 --dry-run
CODEX_HOME=/tmp/sc-codex-home superclaude-codex mcp install context7
```

### Phase 10: Doctor / Verify

目标：用户知道安装是否成功。

TODO：

- [ ] 检查 Codex CLI。
- [ ] 检查 Codex home。
- [ ] 检查 `AGENTS.md` marker。
- [ ] 检查 skills 完整性。
- [ ] 检查 `commands.json`。
- [ ] 检查 `agents.json`。
- [ ] 检查 `config.toml` 可解析。
- [ ] 检查没有触碰 `~/.claude`。

验收：

```bash
superclaude-codex doctor
superclaude-codex verify
```

### Phase 11: 测试体系

目标：迁移质量可持续验证。

TODO：

- [ ] paths 单测。
- [ ] installer dry-run 单测。
- [ ] AGENTS marker update 单测。
- [ ] skill rendering 单测。
- [ ] command registry validation 单测。
- [ ] MCP config merge 单测。
- [ ] 临时 `CODEX_HOME` 集成测试。
- [ ] 不触碰 fake `~/.claude` 集成测试。
- [ ] 30 个命令 golden tests。

验收：

```bash
make test
make lint
make format
```

### Phase 12: 文档

目标：新用户不需要理解旧 SuperClaude。

TODO：

- [ ] README 改成 SuperClaude for Codex。
- [ ] 新增安装说明。
- [ ] 新增 `/sc:*` 命令说明。
- [ ] 新增 MCP 配置说明。
- [ ] 新增 troubleshooting。
- [ ] 新增 FAQ。
- [ ] 同步中文、日文、韩文 README 的安装段落。

必须写清楚：

- [ ] Codex only。
- [ ] 不读取、不修改 `~/.claude`。
- [ ] `~/.codex` 是唯一安装目标。
- [ ] `/sc:*` 是用户体验入口，不代表 Claude 依赖。

### Phase 13: 发布

目标：以新项目发布。

TODO：

- [ ] 版本从 `0.1.0` 开始。
- [ ] PyPI 名称：`superclaude-for-codex`。
- [ ] CLI 名称：`superclaude-codex`。
- [ ] GitHub repo 描述：`SuperClaude workflows for OpenAI Codex`。
- [ ] Alpha 版至少覆盖 5 个核心命令。
- [ ] `1.0.0` 必须覆盖全部 30 命令。
- [ ] CI 构建 wheel 和 sdist。
- [ ] CI 在临时 venv 中执行 `pip install dist/*.whl`。
- [ ] CI 执行 `superclaude-codex install --dry-run`。
- [ ] 发布前执行 TestPyPI smoke install。

建议版本线：

```text
0.1.0  新包骨架、安装器、5 个核心命令
0.2.0  AGENTS/skills/commands registry 稳定
0.3.0  MCP 和 doctor 完成
0.5.0  30 命令全部迁入
0.8.0  agents/personas 完成
1.0.0  Codex-only 稳定版
```

## 15. 测试策略

单测重点：

- `CODEX_HOME` 解析。
- 安装路径不越界。
- `AGENTS.md` marker 更新。
- Command IR schema 校验。
- Skill rendering。
- `commands.json` 完整性。
- TOML merge。
- 原子安装 rollback。
- `/sc:*` route table 生成。
- 旧包 import guard。

集成测试重点：

```bash
tmpdir=$(mktemp -d)
CODEX_HOME="$tmpdir/.codex" superclaude-codex install
test -f "$tmpdir/.codex/AGENTS.md"
test -f "$tmpdir/.codex/superclaude-for-codex/commands.json"
test -d "$tmpdir/.codex/skills/superclaude-brainstorm"
```

安全测试：

- 设置 fake HOME。
- 在 fake HOME 下创建 `.claude/sentinel.txt`。
- 执行安装。
- 验证 sentinel 未变化。

### 15.1 覆盖图

```text
CODE PATHS                                                     USER FLOWS
[+] codex/paths.py                                             [+] First install
  ├── [GAP] CODEX_HOME set                                       ├── [GAP] superclaude-codex install creates AGENTS block
  ├── [GAP] CODEX_HOME unset                                     ├── [GAP] existing AGENTS.md preserved
  └── [GAP] unwritable home                                      └── [GAP] no ~/.claude reads or writes

[+] codex/installer.py                                         [+] Repeat install
  ├── [GAP] prepare succeeds                                     ├── [GAP] idempotent marker replacement
  ├── [GAP] stage partial failure                                ├── [GAP] --force replaces managed assets only
  ├── [GAP] commit succeeds                                      └── [GAP] failed install rolls back visible files
  └── [GAP] rollback restores previous state

[+] core/registry.py                                           [+] Command use in Codex
  ├── [GAP] load valid command YAML                              ├── [GAP] /sc shows command list
  ├── [GAP] reject missing schema_version                        ├── [GAP] /sc:brainstorm routes to skill
  ├── [GAP] reject duplicate aliases                             ├── [GAP] /sc:unknown suggests closest commands
  └── [GAP] emit commands.json

[+] codex/agents_md.py
  ├── [GAP] insert marker block into empty file
  ├── [GAP] replace existing marker block
  ├── [GAP] preserve unrelated user content
  └── [GAP] detect conflicting rules for doctor

[+] codex/skills.py
  ├── [GAP] render SKILL.md for each command
  ├── [GAP] reject command without output_contract
  └── [GAP] golden output stable across runs

[+] codex/mcp.py
  ├── [GAP] parse existing config.toml
  ├── [GAP] merge managed MCP entries only
  ├── [GAP] preserve user MCP entries
  └── [GAP] rollback after failed write

COVERAGE TARGET: 0/30 paths currently planned as explicit tests (0%)
REQUIRED BEFORE ALPHA: all paths above must have unit or integration tests.
Legend: [GAP] = test must be added before implementation is considered complete.
```

### 15.2 推荐测试文件

- `tests/superclaude_codex/test_paths.py`
- `tests/superclaude_codex/test_installer.py`
- `tests/superclaude_codex/test_agents_md.py`
- `tests/superclaude_codex/test_command_registry.py`
- `tests/superclaude_codex/test_skill_renderer.py`
- `tests/superclaude_codex/test_mcp_config.py`
- `tests/superclaude_codex/test_no_claude_touch.py`
- `tests/golden/superclaude_codex/test_rendered_assets.py`

## 16. 风险与处理

### 风险 1: Codex 原生 slash command 能力不足

处理：

- 第一版通过 `AGENTS.md` text-route 支持 `/sc:*`。
- 同时调研 Codex 原生 slash/custom command 扩展点。
- 不把 CLI wrapper 作为主路径。

### 风险 2: 原 SuperClaude markdown 中 Claude-only 假设太多

处理：

- 不逐字迁移。
- 提取语义到 IR。
- Renderer 输出 Codex-native 指令。

### 风险 3: AGENTS.md 过大

处理：

- AGENTS 只放路由。
- 命令细节放 skills。
- `commands.json` 放索引。

### 风险 4: 用户误以为会迁移 Claude 配置

处理：

- README 明确 Codex-only。
- CLI 输出明确“不读取、不修改 ~/.claude”。
- 测试保证不会触碰。

### 风险 5: 命令行为不等价

处理：

- 建立 golden tests。
- 每个命令有 output contract。
- Alpha 先覆盖 5 个核心命令，验证体验后再批量迁移。

### 风险 6: 安装器破坏用户 Codex 配置

处理：

- 原子写入。
- 安装前备份。
- 回滚测试。
- 只管理 marker block 或 manifest 中声明的 assets。

### 风险 7: 新包意外复用旧 Claude 运行时代码

处理：

- import guard 测试。
- `rg "~/.claude|claude mcp"` CI 检查。
- 旧代码只作为迁移输入，不作为 runtime dependency。

## 16.1 What Already Exists

当前仓库中已有可复用资产：

- `src/superclaude/commands/*.md`：可作为 30 个 Command IR 的语义来源，但不能直接作为 Codex runtime prompt。
- `src/superclaude/agents/*.md`：可作为 persona YAML 的语义来源。
- `src/superclaude/skills/confidence-check/` 和 `skills/confidence-check/`：可作为 Codex skill 迁移试点。
- `src/superclaude/cli/install_mcp.py` 的 MCP registry：可抽取服务器定义，但不能复用 Claude CLI 注册逻辑。
- `tests/unit/test_cli_install.py`：可参考安装器测试风格，但新测试必须使用临时 `CODEX_HOME`。
- `pyproject.toml` 的 hatchling/ruff/pytest 配置：可保留工具链，但 package metadata、entry points、coverage source 必须改成新项目。

不应复用的部分：

- `~/.claude/commands/sc` 安装路径。
- `claude mcp add` 调用。
- pytest plugin auto-discovery，除非重新定义为 Codex 项目能力。
- `uninstall-legacy` 这类 Claude 清理命令。

## 16.2 NOT in Scope

以下内容明确不在范围内：

- 迁移用户已有 `~/.claude` 配置。原因：项目定位是全新 Codex 安装。
- 提供 Claude legacy backend。原因：会把架构重新拉回多宿主适配层。
- 构建长期 CLI wrapper 作为主交互。原因：用户主体验必须在 Codex 内输入 `/sc:*`。
- 逐字复刻旧 markdown。原因：旧 markdown 包含 Claude-only 工具和运行假设。
- 自动删除用户旧 SuperClaude 安装。原因：本项目不拥有 `~/.claude`。

## 16.3 Failure Modes

| Codepath | Production failure | Test required | Error handling | User-visible result |
|----------|--------------------|---------------|----------------|---------------------|
| `codex/installer.py` commit | `AGENTS.md` replaced but skills write fails | rollback integration test | restore backup | clear install failure with restored files |
| `codex/mcp.py` merge | invalid TOML breaks Codex startup | invalid TOML test | abort before write | actionable parse error |
| `core/registry.py` load | duplicate alias routes `/sc:test` incorrectly | duplicate alias unit test | fail validation | command validation error |
| `codex/skills.py` render | missing output contract creates vague skill | schema validation test | reject command | build failure with command id |
| `codex/agents_md.py` update | user AGENTS content overwritten | preserve-content test | marker-only replacement | no unrelated diff |
| `/sc:*` text-route | Codex treats command as plain chat | smoke verification | doctor warning | user sees setup diagnosis |

Critical gap: installation rollback currently exists only as a requirement, not as a designed implementation. This must be implemented before any alpha release.

## 16.4 Worktree Parallelization Strategy

Dependency table:

| Step | Modules touched | Depends on |
|------|-----------------|------------|
| Package skeleton | `src/superclaude_codex/`, `pyproject.toml`, `README.md` | — |
| Command IR registry | `core/`, `assets/commands/` | Package skeleton |
| Codex installer and paths | `codex/paths.py`, `codex/installer.py` | Package skeleton |
| AGENTS renderer | `codex/agents_md.py` | Command IR registry |
| Skill renderer | `codex/skills.py` | Command IR registry |
| MCP config writer | `codex/mcp.py` | Package skeleton |
| Doctor/verify | `cli/doctor.py`, `codex/verify.py` | Installer, renderers, MCP |
| 30 command migration | `assets/commands/` | Command IR registry |
| Agents/personas migration | `assets/agents/` | Command IR registry |
| Docs and release | `README*`, `docs/`, CI config | Core behavior settled |

Parallel lanes:

- Lane A: Package skeleton -> installer/paths -> doctor/verify.
- Lane B: Command IR registry -> 5 core command YAML -> 30 command migration.
- Lane C: AGENTS renderer + Skill renderer after B's schema lands.
- Lane D: MCP config writer after package skeleton lands.
- Lane E: Agents/personas migration after B's schema lands.
- Lane F: Docs/release after A-D stabilize.

Execution order:

1. Start Lane A and Lane B in parallel only after agreeing on package metadata.
2. Start Lane C after Command IR schema is stable.
3. Start Lane D in parallel with Lane C.
4. Start Lane E once persona schema is agreed.
5. Run Lane F last, because docs should reflect actual command behavior.

Conflict flags:

- Lane C and Lane B both touch command schema assumptions. Keep schema changes in Lane B only.
- Lane A and Lane D may both touch install report format. Define `install-report.json` schema before parallel work.

## 17. 近期第一批 TODO

建议先做以下最小闭环：

- [ ] 新建 `src/superclaude_codex/`。
- [ ] 修改 `pyproject.toml`，新增 `superclaude-codex` CLI。
- [ ] 实现 `codex/paths.py`。
- [ ] 实现 `codex/installer.py`。
- [ ] 实现 `core/command_ir.py`。
- [ ] 添加 `assets/commands/brainstorm.yaml`。
- [ ] 添加 `assets/commands/implement.yaml`。
- [ ] 实现 `codex/agents_md.py`。
- [ ] 实现 `codex/skills.py`。
- [ ] 安装生成：
  - [ ] `AGENTS.md`
  - [ ] `skills/superclaude-brainstorm/SKILL.md`
  - [ ] `skills/superclaude-implement/SKILL.md`
  - [ ] `superclaude-for-codex/commands.json`
- [ ] 实现 `doctor`。
- [ ] 加临时 `CODEX_HOME` 集成测试。
- [ ] 加“不触碰 ~/.claude”测试。

完成后即可得到第一个可验证版本：

```bash
CODEX_HOME=/tmp/sc-codex-home superclaude-codex install
CODEX_HOME=/tmp/sc-codex-home superclaude-codex doctor
```

## 18. 最终原则

这个项目的终点不是“让 SuperClaude 能在 Codex 里凑合用”，而是：

> 旧的 `/sc:*` 使用体验保持不变，内部实现彻底 Codex-native。

不要做：

- 不做 `~/.claude` 迁移。
- 不做 Claude legacy backend。
- 不做 `superclaude install --host codex`。
- 不把 Claude 工具名原样塞进 Codex。
- 不把 CLI wrapper 当主体验。

必须做：

- Codex-only。
- 新包名。
- 新 CLI。
- 新安装路径。
- Command IR。
- Codex skills。
- Codex AGENTS route。
- 全量 30 命令。
- 不触碰 `~/.claude` 的自动化测试。

## GSTACK REVIEW REPORT

| Review | Trigger | Why | Runs | Status | Findings |
|--------|---------|-----|------|--------|----------|
| CEO Review | `/plan-ceo-review` | Scope & strategy | 0 | NOT RUN | Optional. Product positioning is already narrow: Codex-only, new install, no Claude migration. |
| Codex Review | `/codex review` | Independent 2nd opinion | 0 | NOT RUN | Not run in this pass. |
| Eng Review | `/plan-eng-review` | Architecture & tests (required) | 1 | ISSUES ADDRESSED IN PLAN | 8 engineering issues found, 1 critical gap retained as implementation gate. |
| Design Review | `/plan-design-review` | UI/UX gaps | 0 | NOT APPLICABLE | No UI scope in this plan. |
| DX Review | `/plan-devex-review` | Developer experience gaps | 0 | NOT RUN | Recommended later after CLI prototype exists. |

- **ENG:** Added source isolation, atomic install/rollback, IR versioning, `/sc:*` acceptance matrix, config merge safety, coverage diagram, failure modes, existing-code reuse, NOT in scope, and worktree parallelization.
- **UNRESOLVED:** 1 implementation gate remains: rollback is specified but not yet implemented.
- **VERDICT:** ENG PLAN CLEARED FOR IMPLEMENTATION once Phase 1 starts with rollback and no-`~/.claude` tests included from the first PR.

Completion summary:

- Step 0: Scope Challenge — scope accepted as a full Codex-native rebuild, with Claude migration explicitly out of scope.
- Architecture Review: 5 issues found and incorporated into the plan.
- Code Quality Review: 3 issues found and incorporated into the plan.
- Test Review: coverage diagram produced, 30 gaps identified as required tests.
- Performance Review: 0 runtime performance issues; install-time IO rollback and config parsing risks captured under architecture/failure modes.
- NOT in scope: written.
- What already exists: written.
- TODOS.md updates: 0 items proposed; all durable work belongs in this plan, not a separate TODO list yet.
- Failure modes: 1 critical gap flagged.
- Outside voice: skipped.
- Parallelization: 6 lanes, 4 parallel after schema/package boundaries are agreed, 2 sequential.
- Lake Score: 6/6 recommendations chose complete option.
