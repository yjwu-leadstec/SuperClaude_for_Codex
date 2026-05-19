.PHONY: install test lint format clean doctor help

# Installation (editable mode with dev deps)
install:
	@echo "🔧 Installing SuperClaude for Codex (development mode)..."
	uv pip install -e ".[dev]"
	@echo ""
	@echo "✅ Installation complete!"
	@echo "   Run 'superclaude-codex --version' to verify."

# Run tests
test:
	@echo "Running tests..."
	uv run pytest tests/superclaude_codex/ tests/golden/ -v

# Linting (matches CI: src + tests)
lint:
	@echo "Running linter..."
	uv run ruff check src/superclaude_codex/ tests/

# Format code
format:
	@echo "Formatting code..."
	uv run ruff format src/superclaude_codex/ tests/

# Health check
doctor:
	@echo "Running health check..."
	superclaude-codex doctor

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +

# Show help
help:
	@echo "SuperClaude for Codex - Available commands:"
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  make install     - Install in development mode"
	@echo "  ./install-codex.sh - Full install with Codex setup"
	@echo ""
	@echo "🔧 Development:"
	@echo "  make test        - Run test suite"
	@echo "  make lint        - Run linter (ruff check, src + tests)"
	@echo "  make format      - Format code (ruff format)"
	@echo "  make doctor      - Run health check"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make help        - Show this help message"
