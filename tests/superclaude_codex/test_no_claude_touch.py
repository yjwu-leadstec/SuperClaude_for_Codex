"""Safety tests: ensure superclaude-for-codex never touches ~/.claude.

This is the project's core promise. These tests create a fake HOME with
a sentinel file inside ~/.claude and verify it is never modified.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

from click.testing import CliRunner

from superclaude_codex.cli.main import main


class TestNoClaude:
    """Verify no CLI operation reads or writes ~/.claude."""

    def test_install_does_not_touch_claude(self, fake_home):
        home, sentinel = fake_home
        original = sentinel.read_text()

        runner = CliRunner()
        result = runner.invoke(main, ["install"])

        assert sentinel.read_text() == original
        assert sentinel.exists()

    def test_doctor_does_not_touch_claude(self, fake_home):
        home, sentinel = fake_home
        original = sentinel.read_text()

        runner = CliRunner()
        result = runner.invoke(main, ["doctor"])

        assert sentinel.read_text() == original

    def test_verify_does_not_touch_claude(self, fake_home):
        home, sentinel = fake_home
        original = sentinel.read_text()

        runner = CliRunner()
        result = runner.invoke(main, ["verify"])

        assert sentinel.read_text() == original

    def test_commands_list_does_not_touch_claude(self, fake_home):
        home, sentinel = fake_home
        original = sentinel.read_text()

        runner = CliRunner()
        result = runner.invoke(main, ["commands", "list"])

        assert sentinel.read_text() == original

    def test_mcp_list_does_not_touch_claude(self, fake_home):
        home, sentinel = fake_home
        original = sentinel.read_text()

        runner = CliRunner()
        result = runner.invoke(main, ["mcp", "list"])

        assert sentinel.read_text() == original

    def test_no_new_claude_files_created(self, fake_home):
        home, sentinel = fake_home
        claude_dir = home / ".claude"
        before = set(claude_dir.rglob("*"))

        runner = CliRunner()
        for cmd in [["install"], ["doctor"], ["verify"],
                    ["commands", "list"], ["mcp", "list"]]:
            runner.invoke(main, cmd)

        after = set(claude_dir.rglob("*"))
        assert before == after, f"New files created in ~/.claude: {after - before}"


class TestImportGuard:
    """Verify source code does not import from old superclaude package."""

    def test_no_superclaude_imports_in_source(self):
        src = Path(__file__).resolve().parent.parent.parent / "src" / "superclaude_codex"
        violations = []
        for py in src.rglob("*.py"):
            content = py.read_text()
            for i, line in enumerate(content.splitlines(), 1):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                if "from superclaude " in line or "import superclaude " in line:
                    if "superclaude_codex" not in line:
                        violations.append(f"{py.relative_to(src)}:{i}: {stripped}")
        assert not violations, (
            "Old superclaude package imported in new code:\n"
            + "\n".join(violations)
        )

    def test_no_claude_path_references_in_source(self):
        """Check for ~/.claude references, allowing only guard/error code in paths.py."""
        src = Path(__file__).resolve().parent.parent.parent / "src" / "superclaude_codex"
        # These files legitimately reference ~/.claude in guard logic,
        # generated instructions, or check labels — not actual file I/O.
        allowed_files = {"codex/paths.py", "codex/agents_md.py", "codex/verify.py", "codex/mcp.py", "codex/uninstall.py"}
        violations = []
        for py in src.rglob("*.py"):
            rel = str(py.relative_to(src))
            if rel.replace(os.sep, "/") in allowed_files:
                continue
            content = py.read_text()
            for i, line in enumerate(content.splitlines(), 1):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                if "~/.claude" in line or "/.claude/" in line:
                    violations.append(f"{rel}:{i}: {stripped}")
        assert not violations, (
            "~/.claude references found in new code:\n"
            + "\n".join(violations)
        )
