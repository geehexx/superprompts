# Development Guide

This guide covers the complete development workflow for the SuperPrompts project, including setup, testing, code quality, and deployment.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [Development Workflow](#development-workflow)
- [Code Quality Tools](#code-quality-tools)
- [Testing](#testing)
- [Building and Publishing](#building-and-publishing)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

## Prerequisites

- **Python 3.10+**: Required for MCP compatibility
- **Poetry**: For dependency management and packaging
- **Git**: For version control

## Initial Setup

### 1. Install Poetry

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add to PATH (add to your shell profile)
export PATH="$HOME/.local/bin:$PATH"

# Verify installation
poetry --version
```

### 2. Clone and Setup Project

```bash
# Clone the repository
git clone https://github.com/your-org/superprompts.git
cd superprompts

# Install dependencies
poetry install

# Setup pre-commit hooks
poetry run pre-commit install

# Verify setup
poetry run invoke status
```

### 3. Development Environment

```bash
# Complete development setup
poetry run invoke setup

# This will:
# - Install all dependencies
# - Format code
# - Run code quality checks
# - Verify everything is working
```

## Development Workflow

### Daily Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `poetry run invoke test` | Run all tests | `poetry run invoke test` |
| `poetry run invoke format` | Format code | `poetry run invoke format` |
| `poetry run invoke lint` | Run linting | `poetry run invoke lint` |
| `poetry run invoke check-all` | Run all quality checks | `poetry run invoke check-all` |
| `poetry run invoke run-server` | Start MCP server | `poetry run invoke run-server` |
| `poetry run invoke clean` | Clean build artifacts | `poetry run invoke clean` |

### Testing Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `poetry run invoke test` | Run all tests | `poetry run invoke test` |
| `poetry run invoke test startup` | Run startup tests | `poetry run invoke test startup` |
| `poetry run invoke test integration` | Run integration tests | `poetry run invoke test integration` |
| `poetry run invoke test coverage` | Run with coverage | `poetry run invoke test coverage` |
| `poetry run nox` | Multi-environment testing | `poetry run nox` |

### Code Quality Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `poetry run invoke format` | Format code with Ruff | `poetry run invoke format` |
| `poetry run invoke lint` | Lint with Ruff | `poetry run invoke lint` |
| `poetry run invoke type-check` | Type checking with MyPy | `poetry run invoke type-check` |
| `poetry run invoke pre-commit` | Run pre-commit checks | `poetry run invoke pre-commit` |

## Code Quality Tools

### Ruff (Linting and Formatting)

Ruff is our primary tool for linting and formatting, replacing flake8, isort, and black.

```bash
# Check for issues
poetry run ruff check .

# Fix auto-fixable issues
poetry run ruff check . --fix

# Format code
poetry run ruff format .

# Check formatting
poetry run ruff format --check .
```

**Configuration**: See `[tool.ruff]` section in `pyproject.toml`

### MyPy (Type Checking)

```bash
# Run type checking
poetry run mypy superprompts/

# Check specific file
poetry run mypy superprompts/cli/main.py
```

**Configuration**: See `[tool.mypy]` section in `pyproject.toml`

### Pre-commit Hooks

Pre-commit hooks run automatically on every commit to ensure code quality.

```bash
# Install hooks
poetry run pre-commit install

# Run on all files
poetry run pre-commit run --all-files

# Run on staged files only
poetry run pre-commit run
```

**Configuration**: See `.pre-commit-config.yaml`

## Testing

### Unit and Integration Tests

```bash
# Run all tests
poetry run invoke test

# Run specific test types
poetry run invoke test startup
poetry run invoke test integration
poetry run invoke test unit

# Run with coverage
poetry run invoke test coverage
```

### Multi-Environment Testing with Nox

Nox runs tests across multiple Python versions and environments.

```bash
# Run all Nox sessions
poetry run nox

# Run specific session
poetry run nox -s test
poetry run nox -s lint
poetry run nox -s type_check

# Run with specific Python version
poetry run nox -s test-3.12
```

**Available Sessions**:
- `test`: Run tests on Python 3.10, 3.11, 3.12
- `lint`: Run linting with Ruff
- `format`: Format code with Ruff
- `type_check`: Run type checking with MyPy
- `security`: Run security checks with Bandit
- `coverage`: Run tests with coverage
- `validate`: Run validation checks
- `ci`: Run complete CI pipeline

### Test Structure

```
tests/
├── test_startup.py      # Startup regression tests
├── test_server.py       # Server functionality tests
└── run_tests.sh         # Legacy test runner (deprecated)
```

## Building and Publishing

### Building

```bash
# Build package
poetry run invoke build

# This creates:
# - dist/superprompts-1.0.0-py3-none-any.whl
# - dist/superprompts-1.0.0.tar.gz
```

### Publishing

```bash
# Publish to PyPI
poetry run invoke publish

# Note: Requires PyPI credentials configured
```

### Local Installation

```bash
# Install from source
poetry install

# Install built package
pip install dist/*.whl
```

## Troubleshooting

### Common Issues

#### Poetry Not Found
```bash
# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Or reinstall Poetry
curl -sSL https://install.python-poetry.org | python3 -
```

#### Virtual Environment Issues
```bash
# Recreate virtual environment
poetry env remove python
poetry install
```

#### Pre-commit Hook Failures
```bash
# Update hooks
poetry run pre-commit autoupdate

# Run manually
poetry run pre-commit run --all-files
```

#### Test Failures
```bash
# Run with verbose output
poetry run pytest tests/ -v

# Run specific test
poetry run pytest tests/test_startup.py -v

# Debug mode
poetry run pytest tests/ --pdb
```

### Getting Help

```bash
# Show all available commands
poetry run invoke --list

# Show help for specific command
poetry run invoke help test

# Show project status
poetry run invoke status
```

## Advanced Usage

### Custom Invoke Tasks

You can extend the task system by modifying `tasks.py`:

```python
@task
def my_custom_task(c):
    """My custom task description."""
    print("Running custom task...")
    # Your custom logic here
```

### Nox Customization

Modify `noxfile.py` to add custom sessions:

```python
@nox.session(python="3.12")
def my_custom_session(session):
    """My custom Nox session."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    # Your custom commands here
```

### Pre-commit Customization

Add custom hooks in `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: my-custom-hook
      name: My Custom Hook
      entry: my-custom-script
      language: system
```

### GitHub Actions

The CI/CD pipeline is configured in `.github/workflows/ci.yml` and includes:

- Multi-Python testing (3.10, 3.11, 3.12)
- Pre-commit checks
- Nox integration
- Security scanning
- Package building

## Development Best Practices

### Code Style

1. **Follow Ruff Rules**: Our Ruff configuration enforces consistent code style
2. **Type Hints**: Use type hints for all function parameters and return values
3. **Docstrings**: Document all public functions and classes
4. **Error Handling**: Use appropriate exception handling

### Git Workflow

1. **Feature Branches**: Create feature branches for all changes
2. **Commit Messages**: Use clear, descriptive commit messages
3. **Pre-commit**: Let pre-commit hooks format and lint your code
4. **Pull Requests**: Create PRs for all changes, even small ones

### Testing

1. **Write Tests**: Write tests for all new functionality
2. **Test Coverage**: Aim for high test coverage
3. **Multi-Environment**: Test across multiple Python versions
4. **Integration Tests**: Include integration tests for complex features

### Documentation

1. **Update Docs**: Update documentation for all changes
2. **Clear Examples**: Include clear examples in documentation
3. **API Documentation**: Document all public APIs
4. **README Updates**: Keep README files current

## Development Commands

Use Invoke for all development tasks:

```bash
poetry run invoke help
poetry run invoke test
poetry run invoke clean
poetry run invoke install
```

## Next Steps

- [Contributing Guide](contributing_guide.md) - How to contribute to the project
- [MCP Server Guide](mcp_server_guide.md) - Using the MCP server
- [Troubleshooting Guide](troubleshooting_guide.md) - Common issues and solutions
- [API Reference](api_reference.md) - Complete API documentation
