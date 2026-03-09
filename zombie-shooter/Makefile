.PHONY: help install run test lint format type-check clean all

# Default target - show help
help:
	@echo "🎮 Zombie Shooter - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install dependencies with uv"
	@echo ""
	@echo "Development:"
	@echo "  make run          Run the game"
	@echo "  make test         Run all tests"
	@echo "  make test-v       Run tests with verbose output"
	@echo "  make test-cov     Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         Run ruff linter (check only)"
	@echo "  make format       Format code with ruff"
	@echo "  make type-check   Run mypy type checker (if installed)"
	@echo "  make check        Run all checks (lint + test)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        Remove cache files and bytecode"
	@echo "  make clean-all    Remove cache + virtual environment"
	@echo ""
	@echo "Meta:"
	@echo "  make all          Run format + lint + test"

# Python and environment setup
PYTHON := .venv/bin/python
PYTEST := .venv/bin/pytest
RUFF := .venv/bin/ruff
MYPY := .venv/bin/mypy
UV := uv

# Install dependencies
install:
	@echo "📦 Installing dependencies with uv..."
	$(UV) venv
	$(UV) pip install -e .
	@echo "✅ Installation complete!"
	@echo "💡 Activate with: source .venv/bin/activate"

# Run the game
run:
	@echo "🎮 Starting Zombie Shooter..."
	@PYTHONPATH=src $(PYTHON) src/game/main.py

# Run tests
test:
	@echo "🧪 Running tests..."
	@PYTHONPATH=src $(PYTEST) tests/ -q

test-v:
	@echo "🧪 Running tests (verbose)..."
	@PYTHONPATH=src $(PYTEST) tests/ -v

test-cov:
	@echo "🧪 Running tests with coverage..."
	@PYTHONPATH=src $(PYTEST) tests/ --cov=game --cov-report=term-missing --cov-report=html
	@echo "📊 Coverage report: htmlcov/index.html"

# Code quality
lint:
	@echo "🔍 Running linter..."
	@$(RUFF) check src/ tests/

format:
	@echo "✨ Formatting code..."
	@$(RUFF) format src/ tests/
	@echo "✅ Code formatted!"

type-check:
	@echo "🔎 Running type checker..."
	@if command -v $(MYPY) >/dev/null 2>&1; then \
		$(MYPY) src/; \
	else \
		echo "⚠️  mypy not installed (optional)"; \
	fi

# Combined checks
check: lint test
	@echo "✅ All checks passed!"

all: format lint test
	@echo "✅ Format, lint, and test complete!"

# Cleanup
clean:
	@echo "🧹 Cleaning cache files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete!"

clean-all: clean
	@echo "🧹 Removing virtual environment..."
	@rm -rf .venv
	@echo "✅ Full cleanup complete!"
