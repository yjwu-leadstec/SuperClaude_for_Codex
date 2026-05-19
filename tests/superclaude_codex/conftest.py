"""Shared test fixtures for superclaude_codex tests."""

import os

import pytest


@pytest.fixture
def tmp_codex_home(tmp_path):
    """Provide a temporary CODEX_HOME directory and set the env var."""
    codex_home = tmp_path / ".codex"
    codex_home.mkdir()
    old = os.environ.get("CODEX_HOME")
    os.environ["CODEX_HOME"] = str(codex_home)
    yield codex_home
    if old is None:
        os.environ.pop("CODEX_HOME", None)
    else:
        os.environ["CODEX_HOME"] = old


@pytest.fixture
def fake_home(tmp_path):
    """Provide a fake HOME directory with a sentinel ~/.claude file.

    Used to verify that no operation touches ~/.claude.
    """
    home = tmp_path / "fakehome"
    home.mkdir()
    claude_dir = home / ".claude"
    claude_dir.mkdir()
    sentinel = claude_dir / "sentinel.txt"
    sentinel.write_text("DO NOT MODIFY")

    old = os.environ.get("HOME")
    os.environ["HOME"] = str(home)
    yield home, sentinel
    if old is None:
        os.environ.pop("HOME", None)
    else:
        os.environ["HOME"] = old
