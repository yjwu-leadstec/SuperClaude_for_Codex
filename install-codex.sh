#!/usr/bin/env bash
# SuperClaude for Codex — One-line installer
# Usage: ./install-codex.sh
#
# This script installs the superclaude-for-codex package and sets up
# Codex with all 30 /sc:* commands, skills, and routing.
#
# Requirements: Python >= 3.10, pip or uv
#
# NOTE: This is Codex-only. It does NOT read or write ~/.claude.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

info()  { echo "  $*"; }
ok()    { echo "  ✅ $*"; }
fail()  { echo "  ❌ $*" >&2; }

# Helper: run superclaude-codex via the correct method
run_cli() {
    if [ -n "${USE_UV:-}" ]; then
        uv run superclaude-codex "$@"
    elif [ -f "$SCRIPT_DIR/.venv/bin/superclaude-codex" ]; then
        "$SCRIPT_DIR/.venv/bin/superclaude-codex" "$@"
    else
        superclaude-codex "$@"
    fi
}

echo ""
echo "🚀 SuperClaude for Codex Installer"
echo "==================================="
echo ""

# 1. Check Python version
info "Checking Python..."
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        version=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null)
        major=$("$cmd" -c "import sys; print(sys.version_info.major)" 2>/dev/null)
        minor=$("$cmd" -c "import sys; print(sys.version_info.minor)" 2>/dev/null)
        if [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
            PYTHON="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    fail "Python >= 3.10 required. Found: ${version:-none}"
    exit 1
fi
ok "Python $version ($PYTHON)"

# 2. Install package
info "Installing superclaude-for-codex..."
cd "$SCRIPT_DIR"

if command -v uv &>/dev/null; then
    USE_UV=1
    if [ ! -d ".venv" ]; then
        uv venv --python "$PYTHON" 2>&1 | tail -1
    fi
    uv pip install -e ".[dev]" 2>&1 | tail -3
else
    "$PYTHON" -m pip install -e ".[dev]" 2>&1 | tail -3
fi
ok "Package installed"

# 3. Verify CLI
ok "CLI available: $(run_cli --version)"

# 4. Install to Codex
info "Installing commands and skills to Codex..."
run_cli install
ok "Installation complete"

# 5. Doctor check
echo ""
info "Running health check..."
run_cli doctor

echo ""
echo "==================================="
echo "✅ SuperClaude for Codex is ready!"
echo ""
echo "Open Codex and try:"
echo "  /sc:brainstorm \"your idea here\""
echo "  /sc:implement \"feature description\""
echo "  /sc                                  # list all 30 commands"
echo ""
echo "Manage:"
echo "  superclaude-codex doctor             # health check"
echo "  superclaude-codex mcp list           # MCP servers"
echo "  superclaude-codex uninstall          # remove"
echo "==================================="
