"""Nox configuration for SuperPrompts MCP Server.

This module provides multi-environment testing and development tasks using Nox.
All sessions can be run using `uv run nox -s <session-name>` or `poetry run nox -s <session-name>`.

## Available Sessions

### Testing
- `test` - Run tests across multiple Python versions (3.10, 3.11, 3.12)
- `ci` - Run CI pipeline across multiple Python versions

### Code Quality
- `lint` - Run linting with Ruff
- `format` - Format code with Ruff (--fix to auto-fix)
- `type_check` - Run type checking with MyPy

### Security and Coverage
- `security` - Run security checks with Bandit
- `coverage` - Run tests with coverage reporting

### Documentation
- `docs` - Build documentation (placeholder)

### Maintenance
- `clean` - Clean up build artifacts

## Usage Examples

```bash
# Run all default sessions
uv run nox

# Run specific session
uv run nox -s test
uv run nox -s lint
uv run nox -s type_check

# Run tests on specific Python version
uv run nox -s test-3.11
uv run nox -s test-3.12

# Run multiple sessions
uv run nox -s lint -s type_check -s test

# Run with verbose output
uv run nox -s test --verbose
```

## Configuration

- Python versions tested: 3.10, 3.11, 3.12
- Default sessions: lint, type-check, test
- All sessions use uv for dependency management
- Sessions run in isolated virtual environments
"""

from typing import Any

import nox  # type: ignore[import-not-found]

# Python versions to test against
PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]

# Default session
nox.options.sessions = ["lint", "type-check", "test"]


@nox.session(python=PYTHON_VERSIONS)  # type: ignore[misc]
def test(session: Any) -> None:
    """Run tests with pytest."""
    session.install("uv")
    session.run("uv", "sync", "--dev", external=True)
    session.run("uv", "run", "pytest", "tests/", "-v")


@nox.session(python="3.12")  # type: ignore[misc]
def lint(session: Any) -> None:
    """Run linting with ruff."""
    session.install("uv")
    session.run("uv", "sync", "--dev", external=True)
    session.run("uv", "run", "ruff", "check", ".")
    session.run("uv", "run", "ruff", "format", "--check", ".")


@nox.session(python="3.12")  # type: ignore[misc]
def format_code(session: Any) -> None:
    """Format code with ruff."""
    session.install("uv")
    session.run("uv", "install", external=True)
    session.run("uv", "run", "ruff", "check", ".", "--fix")
    session.run("uv", "run", "ruff", "format", ".")


@nox.session(python="3.12")  # type: ignore[misc]
def type_check(session: Any) -> None:
    """Run type checking with mypy."""
    session.install("uv")
    session.run("uv", "install", external=True)
    session.run("uv", "run", "mypy", "superprompts/")


@nox.session(python="3.12")  # type: ignore[misc]
def security(session: Any) -> None:
    """Run security checks with bandit."""
    session.install("uv")
    session.run("uv", "install", external=True)
    session.run(
        "uv",
        "run",
        "bandit",
        "-r",
        "superprompts/",
        "-f",
        "json",
        "-o",
        "bandit-report.json",
    )


@nox.session(python="3.12")  # type: ignore[misc]
def coverage(session: Any) -> None:
    """Run tests with coverage."""
    session.install("uv")
    session.run("uv", "install", external=True)
    session.run(
        "uv",
        "run",
        "pytest",
        "tests/",
        "--cov=superprompts",
        "--cov-report=html",
        "--cov-report=term",
    )


@nox.session(python="3.12")  # type: ignore[misc]
def docs(session: Any) -> None:
    """Build documentation."""
    session.install("uv")
    session.run("uv", "install", external=True)
    # Add documentation building commands here when implemented
    session.log("Documentation building not yet implemented")


@nox.session(python="3.12")  # type: ignore[misc]
def clean(session: Any) -> None:
    """Clean up build artifacts."""
    session.run(
        "rm",
        "-rf",
        "build/",
        "dist/",
        "*.egg-info/",
        ".pytest_cache/",
        ".mypy_cache/",
        "htmlcov/",
        ".coverage",
        external=True,
    )
    session.run(
        "find",
        ".",
        "-type",
        "d",
        "-name",
        "__pycache__",
        "-exec",
        "rm",
        "-rf",
        "{}",
        "+",
        external=True,
    )
    session.run("find", ".", "-type", "f", "-name", "*.pyc", "-delete", external=True)


@nox.session(python=PYTHON_VERSIONS)  # type: ignore[misc]
def ci(session: Any) -> None:
    """Run CI pipeline."""
    session.install("uv")
    session.run("uv", "install", external=True)
    session.run("uv", "run", "ruff", "check", ".")
    session.run("uv", "run", "ruff", "format", "--check", ".")
    session.run("uv", "run", "mypy", "superprompts/")
    session.run("uv", "run", "pytest", "tests/", "-v")
