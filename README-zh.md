<div align="center">

# SuperClaude for Codex

### **为 OpenAI Codex 打造的结构化开发工作流**

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/Codex-only-green" alt="Codex Only">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/commands-30-orange" alt="30 Commands">
</p>

<p align="center">
  <a href="README.md">English</a> •
  <a href="README-zh.md">中文</a> •
  <a href="README-ja.md">日本語</a>
</p>

</div>

---

## 这是什么？

SuperClaude for Codex 为 OpenAI Codex 提供 **30 个结构化 `/sc:*` 命令** 和 **20 个专家 Agent**。在 Codex 中输入 `/sc:brainstorm`、`/sc:implement` 或 `/sc:test` 即可激活对应工作流。

**重要**：这是一个 **Codex 专属** 项目。**不读取、不修改、不依赖** `~/.claude`。所有安装内容写入 `~/.codex/`。

---

## 快速开始

```bash
git clone https://github.com/yjwu-leadstec/SuperClaude_Framework.git
cd SuperClaude_Framework
./install-codex.sh
```

安装后，在 Codex 中输入：

```
/sc:brainstorm "设计一个用户管理 API"
/sc:implement "添加认证中间件"
/sc:test
/sc                    # 查看全部 30 个命令
```

### 验证安装

```bash
superclaude-codex doctor
```

### MCP 服务器（可选）

```bash
superclaude-codex mcp list                    # 列出可用服务器
superclaude-codex mcp install context7        # 安装指定服务器
superclaude-codex mcp install --all           # 安装全部 8 个
```

### 卸载

```bash
superclaude-codex uninstall
```

---

## 命令列表

30 个命令覆盖完整开发生命周期。详见 [命令参考](docs/codex/commands.md)。

| 类别 | 命令 |
|------|------|
| 规划与设计 | `/sc:brainstorm`, `/sc:design`, `/sc:estimate`, `/sc:business-panel`, `/sc:spec-panel` |
| 开发 | `/sc:implement`, `/sc:build`, `/sc:improve`, `/sc:cleanup`, `/sc:explain` |
| 质量 | `/sc:test`, `/sc:analyze`, `/sc:troubleshoot`, `/sc:reflect` |
| 文档与 Git | `/sc:document`, `/sc:git`, `/sc:help` |
| 项目管理 | `/sc:pm`, `/sc:task`, `/sc:workflow`, `/sc:research` |
| 工具 | `/sc:agent`, `/sc:spawn`, `/sc:index-repo`, `/sc:index`, `/sc:recommend`, `/sc:select-tool`, `/sc:load`, `/sc:save`, `/sc` |

---

## 文档

| 文档 | 说明 |
|------|------|
| [安装指南](docs/codex/installation.md) | 详细安装步骤 |
| [命令参考](docs/codex/commands.md) | 全部 30 个命令 |
| [故障排查](docs/codex/troubleshooting.md) | 常见问题与 FAQ |

---

## 声明

本项目与 OpenAI 或 Anthropic 无关。Codex 是 [OpenAI](https://openai.com/) 的产品。

## 许可

MIT License — 详见 [LICENSE](LICENSE)。
