.PHONY: help install install-dev test lint format clean build docs run-notebooks

help:  ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install:  ## Install package in production mode
	pip install .

install-dev:  ## Install package in development mode with all dependencies
	uv pip install -e '.[dev,test]'

test:  ## Run tests with pytest
	pytest -v

test-cov:  ## Run tests with coverage report
	pytest --cov=kub --cov-report=html --cov-report=term

lint:  ## Run linter (ruff)
	ruff check .

lint-fix:  ## Run linter and auto-fix issues
	ruff check --fix .

format:  ## Format code with ruff
	ruff format .

format-check:  ## Check code formatting without changes
	ruff format --check .

clean:  ## Clean build artifacts and cache files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build:  ## Build distribution packages
	python -m build

docs:  ## Generate documentation (placeholder)
	@echo "Documentation generation not yet implemented"
	@echo "See docs/API.md for API documentation"

run-notebooks:  ## Start Jupyter Lab
	jupyter lab --notebook-dir=notebooks

check-all: lint format-check test  ## Run all checks (lint, format, test)

dev-setup:  ## Complete development setup
	@echo "Setting up development environment..."
	@command -v uv >/dev/null 2>&1 || pip install uv
	uv pip install -e '.[dev,test]'
	@echo "✓ Development environment ready!"
	@echo "Run 'make help' to see available commands"

docker-build:  ## Build Docker container
	docker build -f .devcontainer/Dockerfile -t ktirio-ub-course:latest .

docker-run:  ## Run Docker container
	docker run -it --rm -v $(PWD):/workspace -p 8888:8888 ktirio-ub-course:latest
