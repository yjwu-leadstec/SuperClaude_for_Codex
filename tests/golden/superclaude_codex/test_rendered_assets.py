"""Golden tests: verify rendered assets are stable across runs.

These tests render all commands and compare the output to golden snapshots.
Run with --update-golden to regenerate snapshots.
"""

from pathlib import Path

import pytest

from superclaude_codex.codex.agents_md import render_agents_block
from superclaude_codex.codex.skills import render_skill
from superclaude_codex.core.registry import CommandRegistry

GOLDEN_DIR = Path(__file__).parent / "snapshots"


def _get_registry() -> CommandRegistry:
    reg = CommandRegistry()
    reg.load_all()
    return reg


def _read_or_create_golden(name: str, content: str, update: bool) -> str:
    """Read golden file, or create it if --update-golden is set."""
    path = GOLDEN_DIR / name
    if update:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return content
    if not path.exists():
        pytest.fail(
            f"Golden file missing: {path}\n"
            f"Run: uv run pytest tests/golden/ --update-golden"
        )
    return path.read_text()


@pytest.fixture
def update_golden(request):
    return request.config.getoption("--update-golden", default=False)


class TestAgentsMdGolden:
    def test_agents_block_stable(self, update_golden):
        reg = _get_registry()
        rendered = render_agents_block(reg)
        golden = _read_or_create_golden("agents_block.md", rendered, update_golden)
        assert rendered == golden, (
            "AGENTS.md block changed. Run --update-golden to accept."
        )


class TestCommandsJsonGolden:
    def test_commands_json_stable(self, update_golden):
        reg = _get_registry()
        rendered = reg.export_commands_json_str()
        golden = _read_or_create_golden("commands.json", rendered, update_golden)
        assert rendered == golden, (
            "commands.json changed. Run --update-golden to accept."
        )


class TestSkillGolden:
    """Test each command's SKILL.md is stable."""

    @pytest.fixture(autouse=True)
    def _setup(self, update_golden):
        self.update = update_golden
        self.reg = _get_registry()

    def _check_skill(self, cmd_id: str):
        cmd = self.reg.get_command(cmd_id)
        assert cmd is not None, f"Command {cmd_id} not found"
        rendered = render_skill(cmd)
        golden = _read_or_create_golden(f"skill_{cmd_id}.md", rendered, self.update)
        assert rendered == golden, (
            f"SKILL.md for {cmd_id} changed. Run --update-golden."
        )

    def test_brainstorm(self):
        self._check_skill("brainstorm")

    def test_implement(self):
        self._check_skill("implement")

    def test_analyze(self):
        self._check_skill("analyze")

    def test_test(self):
        self._check_skill("test")

    def test_troubleshoot(self):
        self._check_skill("troubleshoot")

    def test_design(self):
        self._check_skill("design")

    def test_build(self):
        self._check_skill("build")

    def test_improve(self):
        self._check_skill("improve")

    def test_cleanup(self):
        self._check_skill("cleanup")

    def test_explain(self):
        self._check_skill("explain")

    def test_reflect(self):
        self._check_skill("reflect")

    def test_document(self):
        self._check_skill("document")

    def test_help(self):
        self._check_skill("help")

    def test_git(self):
        self._check_skill("git")

    def test_pm(self):
        self._check_skill("pm")

    def test_task(self):
        self._check_skill("task")

    def test_workflow(self):
        self._check_skill("workflow")

    def test_research(self):
        self._check_skill("research")

    def test_business_panel(self):
        self._check_skill("business-panel")

    def test_spec_panel(self):
        self._check_skill("spec-panel")

    def test_estimate(self):
        self._check_skill("estimate")

    def test_agent(self):
        self._check_skill("agent")

    def test_index_repo(self):
        self._check_skill("index-repo")

    def test_index(self):
        self._check_skill("index")

    def test_recommend(self):
        self._check_skill("recommend")

    def test_select_tool(self):
        self._check_skill("select-tool")

    def test_spawn(self):
        self._check_skill("spawn")

    def test_load(self):
        self._check_skill("load")

    def test_save(self):
        self._check_skill("save")

    def test_sc(self):
        self._check_skill("sc")
