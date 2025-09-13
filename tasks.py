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
        print(f"{Colors.RED}Command failed: {full_command}{Colors.NC}")
        sys.exit(1)
    return result


@task
def help(c):
    """Show available tasks."""
    print(f"{Colors.BLUE}SuperPrompts MCP Server - Available Tasks{Colors.NC}")
    print("=" * 50)
    c.run("invoke --list")


@task
def install(c):
    """Install dependencies with Poetry."""
    print(f"{Colors.BLUE}Installing dependencies...{Colors.NC}")
    run_poetry(c, "install")
    print(f"{Colors.GREEN}Dependencies installed{Colors.NC}")


@task
def update(c):
    """Update dependencies with Poetry."""
    print(f"{Colors.BLUE}Updating dependencies...{Colors.NC}")
    run_poetry(c, "update")
    print(f"{Colors.GREEN}Dependencies updated{Colors.NC}")


@task
def test(c, unit=False, integration=False, startup=False, coverage=False):
    """Run tests."""
    if unit:
        print(f"{Colors.BLUE}Running unit tests...{Colors.NC}")
        run_poetry(c, "run", "pytest", f"{TEST_DIR}/", "-v")
    elif integration:
        print(f"{Colors.BLUE}Running integration tests...{Colors.NC}")
        run_poetry(c, "run", "python", f"{TEST_DIR}/test_server.py")
    elif startup:
        print(f"{Colors.BLUE}Running startup regression tests...{Colors.NC}")
        run_poetry(c, "run", "python", f"{TEST_DIR}/test_startup.py")
    elif coverage:
        print(f"{Colors.BLUE}Running tests with coverage...{Colors.NC}")
        run_poetry(c, "run", "pytest", f"{TEST_DIR}/", "--cov", PACKAGE_NAME, "--cov-report=html", "--cov-report=term")
        print(f"{Colors.GREEN}Coverage report generated in htmlcov/{Colors.NC}")
    else:
        print(f"{Colors.BLUE}Running SuperPrompts MCP Server Tests{Colors.NC}")
        print("=" * 40)
        print(f"{Colors.BLUE}Running startup regression tests...{Colors.NC}")
        run_poetry(c, "run", "python", f"{TEST_DIR}/test_startup.py")
        print()
        print(f"{Colors.BLUE}Running server functionality tests...{Colors.NC}")
        run_poetry(c, "run", "python", f"{TEST_DIR}/test_server.py")
        print()
        print(f"{Colors.GREEN}All tests completed successfully! 🎉{Colors.NC}")


@task
def format(c, check=False):
    """Format code with Ruff."""
    if check:
        print(f"{Colors.BLUE}Checking code formatting...{Colors.NC}")
        run_poetry(c, "run", "ruff", "format", "--check", ".")
    else:
        print(f"{Colors.BLUE}Formatting code...{Colors.NC}")
        run_poetry(c, "run", "ruff", "check", ".", "--fix")
        run_poetry(c, "run", "ruff", "format", ".")
        print(f"{Colors.GREEN}Code formatted{Colors.NC}")


@task
def lint(c):
    """Run linting with Ruff."""
    print(f"{Colors.BLUE}Running linter...{Colors.NC}")
    run_poetry(c, "run", "ruff", "check", ".")
    print(f"{Colors.GREEN}Linting completed{Colors.NC}")


@task
def type_check(c):
    """Run type checking with mypy."""
    print(f"{Colors.BLUE}Running type checker...{Colors.NC}")
    run_poetry(c, "run", "mypy", f"{PACKAGE_NAME}/")
    print(f"{Colors.GREEN}Type checking completed{Colors.NC}")


@task
def check_all(c):
    """Run all code quality checks."""
    print(f"{Colors.BLUE}Running all code quality checks...{Colors.NC}")
    lint(c)
    type_check(c)
    print(f"{Colors.GREEN}All code quality checks passed{Colors.NC}")


@task
def validate(c, cursor_rules=False, schemas=False):
    """Run validation checks."""
    if cursor_rules:
        print(f"{Colors.BLUE}Validating cursor rules...{Colors.NC}")
        os.makedirs("artifacts", exist_ok=True)
        run_poetry(c, "run", "python", f"{SCRIPTS_DIR}/validate_cursor_rules.py",
                  "--strict", "--report-json", "artifacts/cursor_rules_report.json",
                  ".cursor/rules", "prompts/generate_cursor_rules.prompt.md")
        print(f"{Colors.GREEN}Cursor rules validation completed{Colors.NC}")
    elif schemas:
        print(f"{Colors.BLUE}Validating JSON schemas...{Colors.NC}")
        schema_files = list(Path(SCHEMAS_DIR).glob("*.json"))
        for schema_file in schema_files:
            print(f"Validating {schema_file}...")
            run_poetry(c, "run", "python", "-c", f"import json; json.load(open('{schema_file}'))")
        print(f"{Colors.GREEN}Schema validation completed{Colors.NC}")
    else:
        print(f"{Colors.BLUE}Running all validation checks...{Colors.NC}")
        validate(c, cursor_rules=True)
        validate(c, schemas=True)
        print(f"{Colors.GREEN}All validation checks passed{Colors.NC}")


@task
def run_server(c, debug=False):
    """Run the MCP server."""
    if debug:
        print(f"{Colors.BLUE}Starting development server...{Colors.NC}")
        run_poetry(c, "run", "python", "-m", f"{PACKAGE_NAME}.mcp.server", "--debug")
    else:
        print(f"{Colors.BLUE}Starting MCP server...{Colors.NC}")
        run_poetry(c, "run", "python", "-m", f"{PACKAGE_NAME}.mcp.server")


@task
def build(c):
    """Build the package with Poetry."""
    print(f"{Colors.BLUE}Building package...{Colors.NC}")
    run_poetry(c, "build")
    print(f"{Colors.GREEN}Package built in dist/{Colors.NC}")


@task
def publish(c):
    """Publish package to PyPI with Poetry."""
    print(f"{Colors.BLUE}Publishing package...{Colors.NC}")
    run_poetry(c, "publish")
    print(f"{Colors.GREEN}Package published{Colors.NC}")


@task
def clean(c, cache=False, all=False):
    """Clean build artifacts and temporary files."""
    if all:
        print(f"{Colors.BLUE}Cleaning everything...{Colors.NC}")
        run_poetry(c, "cache", "clear", "--all", "pypi")
        clean(c, cache=True)
        print(f"{Colors.GREEN}Complete cleanup finished{Colors.NC}")
    elif cache:
        print(f"{Colors.BLUE}Cleaning cache files...{Colors.NC}")
        c.run("rm -rf .pytest_cache/ .mypy_cache/ __pycache__/", warn=True)
        c.run("find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true", warn=True)
        c.run("find . -type f -name '*.pyc' -delete 2>/dev/null || true", warn=True)
        print(f"{Colors.GREEN}Cache cleanup completed{Colors.NC}")
    else:
        print(f"{Colors.BLUE}Cleaning build artifacts...{Colors.NC}")
        c.run("rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .mypy_cache/ htmlcov/ .coverage artifacts/", warn=True)
        c.run("rm -rf __pycache__/", warn=True)
        c.run("find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true", warn=True)
        c.run("find . -type f -name '*.pyc' -delete 2>/dev/null || true", warn=True)
        c.run("find . -type f -name '*.pyo' -delete 2>/dev/null || true", warn=True)
        print(f"{Colors.GREEN}Cleanup completed{Colors.NC}")


@task
def setup(c):
    """Complete development setup."""
    print(f"{Colors.BLUE}Setting up development environment...{Colors.NC}")
    install(c)
    format(c)
    check_all(c)
    print(f"{Colors.GREEN}Development environment ready{Colors.NC}")


@task
def pre_commit(c):
    """Run pre-commit checks."""
    print(f"{Colors.BLUE}Running pre-commit checks...{Colors.NC}")
    run_poetry(c, "run", "pre-commit", "run", "--all-files")
    print(f"{Colors.GREEN}Pre-commit checks completed{Colors.NC}")


@task
def ci(c):
    """Run CI pipeline locally."""
    print(f"{Colors.BLUE}Running CI pipeline...{Colors.NC}")
    check_all(c)
    test(c)
    validate(c)
    print(f"{Colors.GREEN}CI pipeline completed successfully{Colors.NC}")


@task
def nox(c, session="test"):
    """Run Nox sessions."""
    print(f"{Colors.BLUE}Running Nox session: {session}{Colors.NC}")
    run_poetry(c, "run", "nox", "-s", session)
    print(f"{Colors.GREEN}Nox session completed{Colors.NC}")


@task
def status(c):
    """Show project status."""
    print(f"{Colors.BLUE}Project Status{Colors.NC}")
    print("=" * 15)

    # Python version
    result = c.run("poetry run python --version", hide=True)
    print(f"Python version: {result.stdout.strip()}")

    # Poetry version
    result = c.run("poetry --version", hide=True)
    print(f"Poetry version: {result.stdout.strip()}")

    # Dependencies
    if Path("pyproject.toml").exists():
        print(f"Dependencies: {Colors.GREEN}Configured{Colors.NC}")
    else:
        print(f"Dependencies: {Colors.RED}Missing{Colors.NC}")

    # Tests
    if Path(TEST_DIR).exists():
        print(f"Tests: {Colors.GREEN}Found{Colors.NC}")
    else:
        print(f"Tests: {Colors.RED}Missing{Colors.NC}")

    # Virtual environment
    result = c.run("poetry env info --path", hide=True)
    print(f"Virtual environment: {result.stdout.strip()}")


# Default task
@task(default=True)
def default(c):
    """Default task - show help."""
    help(c)
