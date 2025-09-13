"""Invoke tasks for SuperPrompts MCP Server.

This module provides task automation for the SuperPrompts project using Invoke.
All tasks can be run using `uv run invoke <task-name>` or `poetry run invoke <task-name>`.

## Available Tasks

### Development Setup
- `setup` - Complete development environment setup
- `install` - Install dependencies with Poetry
- `update` - Update dependencies with Poetry

### Testing
- `test` - Run tests with various options (--unit, --integration, --startup, --coverage)
- `nox` - Run Nox sessions for multi-environment testing

### Code Quality
- `format` - Format code with Ruff (--check for validation only)
- `lint` - Run linting with Ruff
- `type_check` - Run type checking with MyPy
- `check_all` - Run all code quality checks

### Validation
- `validate` - Run validation checks (--cursor-rules, --schemas)

### Server Management
- `run_server` - Run the MCP server (--debug for debug mode)

### Build and Distribution
- `build` - Build the package with Poetry
- `publish` - Publish package to PyPI with Poetry

### Maintenance
- `clean` - Clean build artifacts and temporary files (--cache, --all)
- `pre_commit` - Run pre-commit checks

### CI/CD
- `ci` - Run CI pipeline locally

### Project Status
- `status` - Show project status
- `help` - Show available tasks

## Usage Examples

```bash
# Development workflow
uv run invoke setup
uv run invoke format
uv run invoke check_all
uv run invoke test

# Run specific tests
uv run invoke test --unit
uv run invoke test --integration --coverage

# Run Nox sessions
uv run invoke nox
uv run invoke nox --session test

# Clean up
uv run invoke clean --all

# Run full CI locally
uv run invoke ci
```

## Configuration

Tasks are configured with the following constants:
- PROJECT_NAME: "superprompts"
- PACKAGE_NAME: "superprompts"
- TEST_DIR: "tests"
- SCRIPTS_DIR: "scripts"
- SCHEMAS_DIR: "schemas"
"""

import sys
from pathlib import Path
from typing import Any

from invoke import Context, task

# Project configuration
PROJECT_NAME = "superprompts"
PACKAGE_NAME = "superprompts"
TEST_DIR = "tests"
SCRIPTS_DIR = "scripts"
SCHEMAS_DIR = "schemas"


# Colors for output
class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color


def run_poetry(c: Context, command: str, *args: str) -> Any:
    """Run a poetry command with proper error handling."""
    full_command = f"poetry {command}"
    if args:
        full_command += " " + " ".join(args)

    result = c.run(full_command, warn=True)
    if result.exited != 0:
        sys.exit(1)
    return result


@task
def show_help(c: Context) -> None:
    """Show available tasks."""
    c.run("invoke --list")


@task
def install(c: Context) -> None:
    """Install dependencies with Poetry."""
    run_poetry(c, "install")


@task
def update(c: Context) -> None:
    """Update dependencies with Poetry."""
    run_poetry(c, "update")


@task
def test(c: Context, unit: bool = False, integration: bool = False, startup: bool = False, coverage: bool = False) -> None:
    """Run tests."""
    if unit:
        run_poetry(c, "run", "pytest", f"{TEST_DIR}/", "-v")
    elif integration:
        run_poetry(c, "run", "python", f"{TEST_DIR}/test_server.py")
    elif startup:
        run_poetry(c, "run", "python", f"{TEST_DIR}/test_startup.py")
    elif coverage:
        run_poetry(
            c,
            "run",
            "pytest",
            f"{TEST_DIR}/",
            "--cov",
            PACKAGE_NAME,
            "--cov-report=html",
            "--cov-report=term",
        )
    else:
        run_poetry(c, "run", "python", f"{TEST_DIR}/test_startup.py")
        run_poetry(c, "run", "python", f"{TEST_DIR}/test_server.py")


@task
def format_code(c: Context, check: bool = False) -> None:
    """Format code with Ruff."""
    if check:
        run_poetry(c, "run", "ruff", "format", "--check", ".")
    else:
        run_poetry(c, "run", "ruff", "check", ".", "--fix")
        run_poetry(c, "run", "ruff", "format", ".")


@task
def lint(c: Context) -> None:
    """Run linting with Ruff."""
    run_poetry(c, "run", "ruff", "check", ".")


@task
def type_check(c: Context) -> None:
    """Run type checking with mypy."""
    run_poetry(c, "run", "mypy", f"{PACKAGE_NAME}/")


@task
def check_all(c: Context) -> None:
    """Run all code quality checks."""
    lint(c)
    type_check(c)


@task
def validate(c: Context, cursor_rules: bool = False, schemas: bool = False) -> None:
    """Run validation checks."""
    if cursor_rules:
        Path("artifacts").mkdir(parents=True, exist_ok=True)
        run_poetry(
            c,
            "run",
            "python",
            f"{SCRIPTS_DIR}/validate_cursor_rules.py",
            "--strict",
            "--report-json",
            "artifacts/cursor_rules_report.json",
            ".cursor/rules",
            "prompts/generate_cursor_rules.prompt.md",
        )
    elif schemas:
        schema_files = list(Path(SCHEMAS_DIR).glob("*.json"))
        for schema_file in schema_files:
            run_poetry(
                c,
                "run",
                "python",
                "-c",
                f"import json; json.load(open('{schema_file}'))",
            )
    else:
        validate(c, cursor_rules=True)
        validate(c, schemas=True)


@task
def run_server(c: Context, debug: bool = False) -> None:
    """Run the MCP server."""
    if debug:
        run_poetry(c, "run", "python", "-m", f"{PACKAGE_NAME}.mcp.server", "--debug")
    else:
        run_poetry(c, "run", "python", "-m", f"{PACKAGE_NAME}.mcp.server")


@task
def build(c: Context) -> None:
    """Build the package with Poetry."""
    run_poetry(c, "build")


@task
def publish(c: Context) -> None:
    """Publish package to PyPI with Poetry."""
    run_poetry(c, "publish")


@task
def clean(c: Context, cache: bool = False, all_artifacts: bool = False) -> None:
    """Clean build artifacts and temporary files."""
    if all_artifacts:
        run_poetry(c, "cache", "clear", "--all", "pypi")
        clean(c, cache=True)
    elif cache:
        c.run("rm -rf .pytest_cache/ .mypy_cache/ __pycache__/", warn=True)
        c.run(
            "find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true",
            warn=True,
        )
        c.run("find . -type f -name '*.pyc' -delete 2>/dev/null || true", warn=True)
    else:
        c.run(
            "rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .mypy_cache/ htmlcov/ .coverage artifacts/",
            warn=True,
        )
        c.run("rm -rf __pycache__/", warn=True)
        c.run(
            "find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true",
            warn=True,
        )
        c.run("find . -type f -name '*.pyc' -delete 2>/dev/null || true", warn=True)
        c.run("find . -type f -name '*.pyo' -delete 2>/dev/null || true", warn=True)


@task
def setup(c: Context) -> None:
    """Complete development setup."""
    install(c)
    format_code(c)
    check_all(c)


@task
def pre_commit(c: Context) -> None:
    """Run pre-commit checks."""
    run_poetry(c, "run", "pre-commit", "run", "--all-files")


@task
def ci(c: Context) -> None:
    """Run CI pipeline locally."""
    check_all(c)
    test(c)
    validate(c)


@task
def nox(c: Context, session: str = "test") -> None:
    """Run Nox sessions."""
    run_poetry(c, "run", "nox", "-s", session)


@task
def status(c: Context) -> None:
    """Show project status."""
    # Python version
    c.run("poetry run python --version", hide=True)

    # Poetry version
    c.run("poetry --version", hide=True)

    # Dependencies
    if Path("pyproject.toml").exists():
        pass
    else:
        pass

    # Tests
    if Path(TEST_DIR).exists():
        pass
    else:
        pass

    # Virtual environment
    c.run("poetry env info --path", hide=True)


# Default task
@task(default=True)
def default(c: Context) -> None:
    """Show help by default."""
    show_help(c)
