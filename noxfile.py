"""Nox configuration for SuperPrompts MCP Server."""

import nox

# Python versions to test against
PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]

# Default session
nox.options.sessions = ["lint", "type-check", "test"]


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """Run tests with pytest."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "pytest", "tests/", "-v")


@nox.session(python="3.12")
def lint(session):
    """Run linting with ruff."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "ruff", "check", ".")
    session.run("poetry", "run", "ruff", "format", "--check", ".")


@nox.session(python="3.12")
def format(session):
    """Format code with ruff."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "ruff", "check", ".", "--fix")
    session.run("poetry", "run", "ruff", "format", ".")


@nox.session(python="3.12")
def type_check(session):
    """Run type checking with mypy."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "mypy", "superprompts/")


@nox.session(python="3.12")
def security(session):
    """Run security checks with bandit."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "bandit", "-r", "superprompts/", "-f", "json", "-o", "bandit-report.json")


@nox.session(python="3.12")
def coverage(session):
    """Run tests with coverage."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "pytest", "tests/", "--cov=superprompts", "--cov-report=html", "--cov-report=term")


@nox.session(python="3.12")
def validate(session):
    """Run all validation checks."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "python", "scripts/validate_cursor_rules.py", "--strict", "--report-json", "artifacts/cursor_rules_report.json", ".cursor/rules", "prompts/generate_cursor_rules.prompt.md")


@nox.session(python="3.12")
def docs(session):
    """Build documentation."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    # Add documentation building commands here when implemented
    session.log("Documentation building not yet implemented")


@nox.session(python="3.12")
def clean(session):
    """Clean up build artifacts."""
    session.run("rm", "-rf", "build/", "dist/", "*.egg-info/", ".pytest_cache/", ".mypy_cache/", "htmlcov/", ".coverage", "artifacts/", external=True)
    session.run("find", ".", "-type", "d", "-name", "__pycache__", "-exec", "rm", "-rf", "{}", "+", external=True)
    session.run("find", ".", "-type", "f", "-name", "*.pyc", "-delete", external=True)


@nox.session(python=PYTHON_VERSIONS)
def ci(session):
    """Run CI pipeline."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "ruff", "check", ".")
    session.run("poetry", "run", "ruff", "format", "--check", ".")
    session.run("poetry", "run", "mypy", "superprompts/")
    session.run("poetry", "run", "pytest", "tests/", "-v")
