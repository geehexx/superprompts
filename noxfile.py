"""Nox configuration for SuperPrompts MCP Server."""

import nox

# Python versions to test against
PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]

# Default session
nox.options.sessions = ["lint", "type-check", "test"]


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """Run tests with pytest."""
    session.install("uv")
    session.run("uv", "sync", "--dev", external=True)
    session.run("uv", "run", "pytest", "tests/", "-v")


@nox.session(python="3.12")
def lint(session):
    """Run linting with ruff."""
    session.install("uv")
    session.run("uv", "sync", "--dev", external=True)
    session.run("uv", "run", "ruff", "check", ".")
    session.run("uv", "run", "ruff", "format", "--check", ".")


@nox.session(python="3.12")
def format(session):
    """Format code with ruff."""
    session.install("uv")
    session.run("uv", "install", external=True)
    session.run("uv", "run", "ruff", "check", ".", "--fix")
    session.run("uv", "run", "ruff", "format", ".")


@nox.session(python="3.12")
def type_check(session):
    """Run type checking with mypy."""
    session.install("uv")
    session.run("uv", "install", external=True)
    session.run("uv", "run", "mypy", "superprompts/")


@nox.session(python="3.12")
def security(session):
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


@nox.session(python="3.12")
def coverage(session):
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


@nox.session(python="3.12")
def docs(session):
    """Build documentation."""
    session.install("uv")
    session.run("uv", "install", external=True)
    # Add documentation building commands here when implemented
    session.log("Documentation building not yet implemented")


@nox.session(python="3.12")
def clean(session):
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


@nox.session(python=PYTHON_VERSIONS)
def ci(session):
    """Run CI pipeline."""
    session.install("uv")
    session.run("uv", "install", external=True)
    session.run("uv", "run", "ruff", "check", ".")
    session.run("uv", "run", "ruff", "format", "--check", ".")
    session.run("uv", "run", "mypy", "superprompts/")
    session.run("uv", "run", "pytest", "tests/", "-v")
