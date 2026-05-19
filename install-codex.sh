#!/usr/bin/env bash
# SuperClaude for Codex — One-line installer
# Usage: ./install-codex.sh
#
# This script installs the superclaude-for-codex package and sets up
# Codex with all 30 /sc:* commands, skills, and routing.
#
# Requirements: Python >= 3.10, pip
#
# NOTE: This is Codex-only. It does NOT read or write ~/.claude.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYPROJECT_BACKUP=""

info()  { echo "  $*"; }
ok()    { echo "  ✅ $*"; }
fail()  { echo "  ❌ $*" >&2; }

cleanup() {
    if [ -n "$PYPROJECT_BACKUP" ] && [ -f "$PYPROJECT_BACKUP" ]; then
        mv "$PYPROJECT_BACKUP" "$SCRIPT_DIR/pyproject.toml"
    fi
}
trap cleanup EXIT

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

# 2. Swap pyproject.toml temporarily
info "Preparing package configuration..."
cd "$SCRIPT_DIR"

if [ ! -f pyproject-codex.toml ]; then
    fail "pyproject-codex.toml not found. Are you in the right directory?"
    exit 1
fi

PYPROJECT_BACKUP="$SCRIPT_DIR/pyproject.toml.install-bak"
cp pyproject.toml "$PYPROJECT_BACKUP"
cp pyproject-codex.toml pyproject.toml

# 3. Install package
info "Installing superclaude-for-codex..."
if command -v uv &>/dev/null; then
    uv pip install -e ".[dev]" 2>&1 | tail -3
elif command -v pip &>/dev/null; then
    pip install -e ".[dev]" 2>&1 | tail -3
else
    "$PYTHON" -m pip install -e ".[dev]" 2>&1 | tail -3
fi

# 4. Restore original pyproject.toml
mv "$PYPROJECT_BACKUP" pyproject.toml
PYPROJECT_BACKUP=""
ok "Package installed"

# 5. Verify CLI
if ! command -v superclaude-codex &>/dev/null; then
    fail "superclaude-codex command not found on PATH"
    info "You may need to add pip's bin directory to your PATH"
    exit 1
fi
ok "CLI available: $(superclaude-codex --version)"

# 6. Install to Codex
info "Installing commands and skills to Codex..."
superclaude-codex install
ok "Installation complete"

# 7. Doctor check
echo ""
info "Running health check..."
superclaude-codex doctor

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
