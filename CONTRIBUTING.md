# Contributing to SuperClaude for Codex

Thanks for helping improve SuperClaude for Codex. This repository is a
Codex-native Python project that installs structured `/sc:*` workflows into
`~/.codex/`.

## Project Boundaries

- This project targets OpenAI Codex only.
- Do not read, write, migrate, or depend on `~/.claude`.
- Do not import from an old `superclaude` package.
- Keep command behavior driven by `src/superclaude_codex/assets/commands/*.yaml`
  and agent metadata driven by `src/superclaude_codex/assets/agents/*.yaml`.

## Development Setup

```bash
uv pip install -e ".[dev]"
uv run superclaude-codex --version
uv run superclaude-codex commands validate
```

Common commands:

```bash
make test
make lint
make format
make doctor
```

## Bug Reports

Before opening a bug report:

- Search existing issues for duplicates.
- Test with the latest `master`.
- Run `uv run superclaude-codex doctor` when the issue involves installation.

Useful report details:

- SuperClaude for Codex version
- Operating system
- Python version
- Exact command or `/sc:*` invocation
- Expected behavior
- Actual behavior and logs
- Whether `CODEX_HOME` is customized

## Feature Requests

Good feature requests describe:

- The developer workflow this improves
- Which command, agent, installer path, or MCP integration is affected
- Why the existing behavior is insufficient
- Any compatibility or migration concerns

Prefer small, focused changes. New commands should include Command IR YAML,
tests, and documentation updates.

## Code Contributions

Use a topic branch and keep each pull request focused on one purpose.

For implementation changes:

- Follow existing package boundaries in `src/superclaude_codex/`.
- Add or update tests in `tests/superclaude_codex/`.
- Update golden snapshots only when rendered user-facing assets intentionally
  change.
- Keep installer changes transactional and rollback-friendly.
- Preserve the `~/.claude` safety boundary.

For documentation changes:

- Current user docs live in `docs/codex/`.
- Keep examples using `superclaude-codex`, `uv`, and `~/.codex/`.
- Avoid Claude Code installation instructions in this repository.

## Required Checks

Run these before submitting a pull request:

```bash
uv run pytest tests/superclaude_codex/ tests/golden/ -q
uv run ruff check src/superclaude_codex/ tests/
uv run ruff format --check src/superclaude_codex/ tests/
uv run superclaude-codex commands validate
```

If rendered assets change intentionally, regenerate or update the relevant
golden snapshots and explain the reason in the pull request.

## Pull Request Checklist

- The change has one clear purpose.
- Tests or docs are updated when behavior changes.
- `superclaude-codex commands validate` passes.
- No secrets, local state, build artifacts, or user-specific files are committed.
- No new code path touches `~/.claude`.

## Review Focus

Maintainers review for correctness, stability of installed Codex assets,
transactional installer behavior, documentation clarity, and long-term
maintainability.
