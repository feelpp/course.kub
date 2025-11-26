# Contributing to KUB Course

Thank you for your interest in contributing to KUB Course! This document provides guidelines for contributing to the project.

## Development Setup

### Using devcontainer (Recommended)

1. Install [Docker](https://www.docker.com/products/docker-desktop) and [VS Code](https://code.visualstudio.com/)
2. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. Open the project in VS Code
4. Click "Reopen in Container" when prompted (or use Command Palette: `Dev Containers: Reopen in Container`)

### Manual Setup

```bash
# Create virtual environment
uv venv --system-site-packages
source .venv/bin/activate

# Install package in development mode
uv pip install -e '.[dev,test]'
```

## Code Style

We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Fix auto-fixable issues
ruff check --fix .
```

## Testing

We use pytest for testing:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=kub --cov-report=html

# Run specific test file
pytest tests/test_simulation.py -v
```

## Submitting Changes

1. **Fork the repository** and create a feature branch
2. **Make your changes** following the code style guidelines
3. **Add tests** for new functionality
4. **Run tests** to ensure everything passes
5. **Commit with clear messages** following [Conventional Commits](https://www.conventionalcommits.org/)
6. **Submit a pull request** with a clear description

### Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat(simlib): add temperature conversion utility`
- `fix(plotlib): correct axis labels for heat flux`
- `docs: update README with installation instructions`

## Code Review Process

1. All PRs require at least one review
2. CI checks must pass (linting, tests)
3. Maintainers will provide feedback
4. Once approved, maintainers will merge

## Questions?

Feel free to open an issue or reach out to the maintainers.
