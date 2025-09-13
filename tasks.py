"""Invoke tasks for SuperPrompts MCP Server."""

import os
import sys
from pathlib import Path

from invoke import task

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


def run_poetry(c, command, *args):
    """Run a poetry command with proper error handling."""
    full_command = f"poetry {command}"
    if args:
        full_command += " " + " ".join(args)

    result = c.run(full_command, warn=True)
    if result.exited != 0:
        sys.exit(1)
    return result


@task
def help(c):
    """Show available tasks."""
    c.run("invoke --list")


@task
def install(c):
    """Install dependencies with Poetry."""
    run_poetry(c, "install")


@task
def update(c):
    """Update dependencies with Poetry."""
    run_poetry(c, "update")


@task
def test(c, unit=False, integration=False, startup=False, coverage=False):
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
def format(c, check=False):
    """Format code with Ruff."""
    if check:
        run_poetry(c, "run", "ruff", "format", "--check", ".")
    else:
        run_poetry(c, "run", "ruff", "check", ".", "--fix")
        run_poetry(c, "run", "ruff", "format", ".")


@task
def lint(c):
    """Run linting with Ruff."""
    run_poetry(c, "run", "ruff", "check", ".")


@task
def type_check(c):
    """Run type checking with mypy."""
    run_poetry(c, "run", "mypy", f"{PACKAGE_NAME}/")


@task
def check_all(c):
    """Run all code quality checks."""
    lint(c)
    type_check(c)


@task
def validate(c, cursor_rules=False, schemas=False):
    """Run validation checks."""
    if cursor_rules:
        os.makedirs("artifacts", exist_ok=True)
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
def run_server(c, debug=False):
    """Run the MCP server."""
    if debug:
        run_poetry(c, "run", "python", "-m", f"{PACKAGE_NAME}.mcp.server", "--debug")
    else:
        run_poetry(c, "run", "python", "-m", f"{PACKAGE_NAME}.mcp.server")


@task
def build(c):
    """Build the package with Poetry."""
    run_poetry(c, "build")


@task
def publish(c):
    """Publish package to PyPI with Poetry."""
    run_poetry(c, "publish")


@task
def clean(c, cache=False, all=False):
    """Clean build artifacts and temporary files."""
    if all:
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
def setup(c):
    """Complete development setup."""
    install(c)
    format(c)
    check_all(c)


@task
def pre_commit(c):
    """Run pre-commit checks."""
    run_poetry(c, "run", "pre-commit", "run", "--all-files")


@task
def ci(c):
    """Run CI pipeline locally."""
    check_all(c)
    test(c)
    validate(c)


@task
def nox(c, session="test"):
    """Run Nox sessions."""
    run_poetry(c, "run", "nox", "-s", session)


@task
def status(c):
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
def default(c):
    """Default task - show help."""
    help(c)
