<div align="center">

# SuperClaude for Codex

### **Structured Development Workflows for OpenAI Codex**

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/Codex-only-green" alt="Codex Only">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/commands-30-orange" alt="30 Commands">
  <img src="https://img.shields.io/badge/agents-20-purple" alt="20 Agents">
</p>

<p align="center">
  <a href="README-zh.md">
    <img src="https://img.shields.io/badge/🇨🇳_中文-red" alt="中文">
  </a>
  <a href="README-ja.md">
    <img src="https://img.shields.io/badge/🇯🇵_日本語-green" alt="日本語">
  </a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-commands">Commands</a> •
  <a href="#-documentation">Docs</a> •
  <a href="#-contributing">Contributing</a>
</p>

</div>

---

## What is This?

SuperClaude for Codex brings **30 structured `/sc:*` commands** and **20 specialist agents** to OpenAI Codex. Type `/sc:brainstorm`, `/sc:implement`, or `/sc:test` in Codex to activate structured development workflows.

**Important**: This is a **Codex-only** project. It does **not** read, write, or depend on `~/.claude` in any way. All installation targets `~/.codex/`.

---

## Quick Start

```bash
git clone https://github.com/yjwu-leadstec/SuperClaude_for_Codex.git
cd SuperClaude_for_Codex
./install-codex.sh
```

After installation, open Codex and type:

```
/sc:brainstorm "design an API for user management"
/sc:implement "add authentication middleware"
/sc:test
/sc                    # list all 30 commands
```

### Verify Installation

```bash
superclaude-codex doctor
```

### MCP Servers (Optional)

```bash
superclaude-codex mcp list                    # List available servers
superclaude-codex mcp install context7        # Install specific server
superclaude-codex mcp install --all           # Install all 8 servers
```

### Uninstall

```bash
superclaude-codex uninstall
```

---

## Commands

30 commands covering the complete development lifecycle:

### Planning & Design
| Command | Description |
|---------|-------------|
| `/sc:brainstorm` | Interactive requirements discovery through Socratic dialogue |
| `/sc:design` | System architecture and component design |
| `/sc:estimate` | Development time and effort estimation |
| `/sc:business-panel` | Multi-expert business strategy analysis |
| `/sc:spec-panel` | Multi-expert specification review |

### Development
| Command | Description |
|---------|-------------|
| `/sc:implement` | Code implementation with persona activation |
| `/sc:build` | Build, compile, and package projects |
| `/sc:improve` | Systematic code improvements |
| `/sc:cleanup` | Code cleanup and dead code removal |
| `/sc:explain` | Code and concept explanation |

### Quality
| Command | Description |
|---------|-------------|
| `/sc:test` | Test execution, generation, and coverage |
| `/sc:analyze` | Code analysis (quality, security, performance) |
| `/sc:troubleshoot` | Diagnose and resolve issues |
| `/sc:reflect` | Task reflection and retrospectives |

### Documentation & Git
| Command | Description |
|---------|-------------|
| `/sc:document` | Generate documentation |
| `/sc:git` | Git operations with smart commit messages |
| `/sc:help` | List all commands |

### Project Management
| Command | Description |
|---------|-------------|
| `/sc:pm` | Project manager orchestration |
| `/sc:task` | Task tracking |
| `/sc:workflow` | Structured implementation workflows |
| `/sc:research` | Deep web research |

### Utilities
| Command | Description |
|---------|-------------|
| `/sc:agent` | AI agent delegation |
| `/sc:spawn` | Parallel task orchestration |
| `/sc:index-repo` | Repository indexing (94% token reduction) |
| `/sc:index` | Project knowledge base |
| `/sc:recommend` | Command recommendation |
| `/sc:select-tool` | MCP tool selection |
| `/sc:load` / `/sc:save` | Session management |
| `/sc` | Show all commands |

---

## Agents

20 specialist agents activate automatically based on task context:

- **Python Expert** — Production Python, pytest, packaging
- **Security Engineer** — Vulnerabilities, compliance, threat modeling
- **Frontend/Backend Architect** — UI patterns, API design, databases
- **System Architect** — Scalable architecture, long-term decisions
- **DevOps Architect** — CI/CD, infrastructure, observability
- **Quality Engineer** — Testing strategies, edge cases
- **Performance Engineer** — Profiling, bottleneck elimination
- **Deep Research** — External knowledge gathering
- **PM Agent** — Workflow orchestration, PDCA cycles
- And 11 more...

---

## MCP Servers

8 optional MCP servers for enhanced capabilities:

| Server | Description |
|--------|-------------|
| **context7** | Official documentation lookup |
| **tavily** | Web search (requires API key) |
| **playwright** | Browser automation |
| **sequential-thinking** | Multi-step reasoning |
| **magic** | UI component generation |
| **chrome-devtools** | Performance analysis |
| **serena** | Session persistence |
| **airis-gateway** | Unified gateway (60+ tools) |

---

## Documentation

| Document | Purpose |
|----------|---------|
| [Installation Guide](docs/codex/installation.md) | Detailed setup instructions |
| [Command Reference](docs/codex/commands.md) | All 30 commands |
| [Troubleshooting](docs/codex/troubleshooting.md) | Common issues and FAQ |
| [Rebuild Plan](docs/Development/superclaude-for-codex-rebuild-plan.md) | Architecture and design decisions |

---

## Development

```bash
make install           # Install in editable mode
make test              # Run 119 tests
make lint              # Ruff linter
```

### Project Structure

```
pyproject.toml                          # Package configuration
src/superclaude_codex/
├── cli/main.py                         # superclaude-codex CLI
├── core/                               # Command IR, registry, validation
├── codex/                              # paths, installer, renderers, mcp
└── assets/
    ├── commands/*.yaml                 # 30 Command IR definitions
    └── agents/*.yaml                   # 20 Agent definitions
tests/superclaude_codex/                # 87 functional tests
tests/golden/                           # 32 golden snapshot tests
```

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

| Priority | Area |
|:--------:|------|
| High | Command IR improvements, new agent definitions |
| Medium | MCP server integrations, test coverage |
| Low | Documentation, i18n |

---

## Origin & Acknowledgments

This project is a **Codex-native rewrite** based on the [SuperClaude Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework) — an excellent configuration framework that enhances Claude Code with structured commands, cognitive personas, and development methodologies.

We deeply appreciate the work of the original SuperClaude authors and contributors:

- **[Kazuki Nakai](https://github.com/SuperClaude-Org)** — Original creator and project lead
- **[NomenAK](https://github.com/NomenAK)** — Core contributor
- **[Mithun Gowda B](https://github.com/mithungowda)** — Core contributor
- And all the [SuperClaude community contributors](https://github.com/SuperClaude-Org/SuperClaude_Framework/graphs/contributors)

The original SuperClaude's command design, agent personas, and workflow patterns served as the semantic source for this project's Command IR definitions. The implementation is entirely new and Codex-native, but the ideas and developer experience goals originated from the SuperClaude community's pioneering work.

If you're using Claude Code rather than Codex, check out the original project — it's fantastic:
**[SuperClaude Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)**

---

## Disclaimer

This project is not affiliated with or endorsed by OpenAI, Anthropic, or the SuperClaude organization.
- Codex is a product built and maintained by [OpenAI](https://openai.com/).
- Claude Code is a product built and maintained by [Anthropic](https://www.anthropic.com/).
- SuperClaude Framework is maintained by [SuperClaude-Org](https://github.com/SuperClaude-Org).

## License

MIT License — see [LICENSE](LICENSE).

---

<div align="center">
  <sub>Built on the shoulders of SuperClaude, for developers who push boundaries</sub>
</div>
