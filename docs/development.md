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
- **uv**: For dependency management and packaging
- **Git**: For version control

## Initial Setup

### 1. Install uv

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (add to your shell profile)
export PATH="$HOME/.local/bin:$PATH"

# Verify installation
uv --version
```

### 2. Clone and Setup Project

```bash
# Clone the repository
git clone https://github.com/your-org/superprompts.git
cd superprompts

# Install dependencies
uv sync --dev

# Setup pre-commit hooks
uv run pre-commit install

# Verify setup
uv run invoke status
```

### 3. Development Environment

```bash
# Complete development setup
uv run invoke setup

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
| `uv run invoke test` | Run all tests | `uv run invoke test` |
| `uv run invoke format` | Format code | `uv run invoke format` |
| `uv run invoke lint` | Run linting | `uv run invoke lint` |
| `uv run invoke check_all` | Run all quality checks | `uv run invoke check_all` |
| `uv run invoke run_server` | Start MCP server | `uv run invoke run_server` |
| `uv run invoke clean` | Clean build artifacts | `uv run invoke clean` |

### Testing Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `uv run invoke test` | Run all tests | `uv run invoke test` |
| `uv run invoke test --startup` | Run startup tests | `uv run invoke test --startup` |
| `uv run invoke test --integration` | Run integration tests | `uv run invoke test --integration` |
| `uv run invoke test --coverage` | Run with coverage | `uv run invoke test --coverage` |
| `uv run nox` | Multi-environment testing | `uv run nox` |

### Code Quality Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `uv run invoke format` | Format code with Ruff | `uv run invoke format` |
| `uv run invoke lint` | Lint with Ruff | `uv run invoke lint` |
| `uv run invoke type-check` | Type checking with MyPy | `uv run invoke type-check` |
| `uv run invoke pre-commit` | Run pre-commit checks | `uv run invoke pre-commit` |

## Code Quality Tools

### Ruff (Linting and Formatting)

Ruff is our primary tool for linting and formatting, replacing flake8, isort, and black.

```bash
# Check for issues
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check . --fix

# Format code
uv run ruff format .

# Check formatting
uv run ruff format --check .
```

**Configuration**: See `[tool.ruff.lint]` section in `pyproject.toml`
- **Line Length**: 140 characters (increased from 88 for better readability)
- **Modern Structure**: Uses the new `[tool.ruff.lint]` configuration format
- **Comprehensive Rules**: Includes 50+ rule categories for thorough code quality
- **Per-file Ignores**: Customized rules for different file types (tests, prompts)

### MyPy (Type Checking)

```bash
# Run type checking
uv run mypy superprompts/

# Check specific file
uv run mypy superprompts/cli/main.py
```

**Configuration**: See `[tool.mypy]` section in `pyproject.toml`

### Pre-commit Hooks

Pre-commit hooks run automatically on every commit to ensure code quality.

```bash
# Install hooks
uv run pre-commit install

# Run on all files
uv run pre-commit run --all-files

# Run on staged files only
uv run pre-commit run
```

**Configuration**: See `.pre-commit-config.yaml`
- **Ruff**: Linting and formatting with 140 char line length
- **MyPy**: Type checking for comprehensive type safety
- **Black**: Additional code formatting (with 140 char line length)
- **isort**: Import organization and sorting
- **Standard Hooks**: Common pre-commit hooks for file validation

## Testing

### Unit and Integration Tests

```bash
# Run all tests
uv run invoke test

# Run specific test types
uv run invoke test --startup
uv run invoke test --integration
uv run invoke test --unit

# Run with coverage
uv run invoke test --coverage
```

### Multi-Environment Testing with Nox

Nox runs tests across multiple Python versions and environments.

```bash
# Run all Nox sessions
uv run nox

# Run specific session
uv run nox -s test
uv run nox -s lint
uv run nox -s type_check

# Run with specific Python version
uv run nox -s test-3.12
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
├── test_startup.py           # Startup regression tests
├── test_server.py            # Server functionality tests
└── test_startup.py           # Server startup and initialization tests
```

**Test Coverage**: 44 total tests
- **28 existing tests**: Core functionality and configuration
- **16 integration tests**: Comprehensive CLI command testing
- **100% passing**: All tests pass consistently

## Building and Publishing

### Building

```bash
# Build package
uv run invoke build

# This creates:
# - dist/superprompts-1.0.0-py3-none-any.whl
# - dist/superprompts-1.0.0.tar.gz
```

### Publishing

```bash
# Publish to PyPI
uv run invoke publish

# Note: Requires PyPI credentials configured
```

### Local Installation

```bash
# Install from source
uv sync --dev

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
uv sync --dev
```

#### Pre-commit Hook Failures
```bash
# Update hooks
uv run pre-commit autoupdate

# Run manually
uv run pre-commit run --all-files
```

#### Test Failures
```bash
# Run with verbose output
uv run pytest tests/ -v

# Run specific test
uv run pytest tests/test_startup.py -v

# Debug mode
uv run pytest tests/ --pdb
```

### Getting Help

```bash
# Show all available commands
uv run invoke --list

# Show help for specific command
uv run invoke help test

# Show project status
uv run invoke status
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
2. **Type Hints**: Use modern Python 3.10+ type hints (`str | None` instead of `Optional[str]`)
3. **Docstrings**: Document all public functions and classes
4. **Error Handling**: Use comprehensive exception handling with proper logging
5. **Logging**: Use structured logging instead of print statements
6. **Line Length**: 140 characters for better readability

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
uv run invoke help
uv run invoke test
uv run invoke clean
uv run invoke install
```

## Next Steps

- [Contributing Guide](contributing_guide.md) - How to contribute to the project
- [MCP Configuration Guide](mcp_configuration.md) - Using the MCP server
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
- [API](api.md) - Complete API documentation
