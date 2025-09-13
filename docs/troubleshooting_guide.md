# Troubleshooting Guide

This guide helps you resolve common issues when working with the SuperPrompts project.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Poetry Issues](#poetry-issues)
- [Development Environment Issues](#development-environment-issues)
- [Testing Issues](#testing-issues)
- [Code Quality Issues](#code-quality-issues)
- [Server Issues](#server-issues)
- [Performance Issues](#performance-issues)
- [Getting Help](#getting-help)

## Installation Issues

### Poetry Not Found

**Error**: `poetry: command not found`

**Solution**:
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add to PATH (add to your shell profile)
export PATH="$HOME/.local/bin:$PATH"

# Verify installation
poetry --version
```

**Permanent Fix**: Add to your shell profile (`.bashrc`, `.zshrc`, etc.):
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Python Version Issues

**Error**: `The current project's supported Python range is not compatible`

**Solution**:
```bash
# Check Python version
python3 --version

# Install Python 3.10+ if needed
# On Ubuntu/Debian:
sudo apt update
sudo apt install python3.10 python3.10-venv

# On macOS with Homebrew:
brew install python@3.10

# On Windows with Chocolatey:
choco install python --version=3.10.0
```

### Dependency Resolution Issues

**Error**: `Resolving dependencies... failed`

**Solution**:
```bash
# Clear Poetry cache
poetry cache clear --all pypi

# Update Poetry
poetry self update

# Reinstall dependencies
poetry install
```

## Poetry Issues

### Virtual Environment Not Created

**Error**: `Virtual environment not found`

**Solution**:
```bash
# Create virtual environment manually
poetry env use python3.10

# Install dependencies
poetry install

# Verify
poetry env info
```

### Lock File Issues

**Error**: `poetry.lock file not found` or lock file conflicts

**Solution**:
```bash
# Regenerate lock file
poetry lock

# Update dependencies
poetry update

# Install with new lock file
poetry install
```

### Poetry Cache Issues

**Error**: `Failed to download` or `Cache corrupted`

**Solution**:
```bash
# Clear all caches
poetry cache clear --all pypi
poetry cache clear --all _default_cache

# Reinstall
poetry install
```

## Development Environment Issues

### Pre-commit Hook Failures

**Error**: Pre-commit hooks fail on commit

**Solution**:
```bash
# Update pre-commit hooks
poetry run pre-commit autoupdate

# Run hooks manually
poetry run pre-commit run --all-files

# Skip hooks temporarily (not recommended)
git commit --no-verify -m "Your commit message"
```

### Invoke Command Not Found

**Error**: `invoke: command not found`

**Solution**:
```bash
# Use Poetry to run invoke
poetry run invoke --list

# Or install invoke globally (not recommended)
pip install invoke
```

### Import Errors

**Error**: `ModuleNotFoundError` or import errors

**Solution**:
```bash
# Ensure you're using Poetry
poetry run python -c "import superprompts"

# Check virtual environment
poetry env info

# Reinstall dependencies
poetry install
```

## Testing Issues

### Test Failures

**Error**: Tests fail with various errors

**Solution**:
```bash
# Run tests with verbose output
poetry run invoke test --verbose

# Run specific test
poetry run invoke test startup

# Debug mode
poetry run pytest tests/ --pdb

# Check test environment
poetry run invoke status
```

### Nox Issues

**Error**: Nox sessions fail

**Solution**:
```bash
# Run specific Nox session
poetry run nox -s test

# Run with verbose output
poetry run nox -v

# Clean Nox environments
poetry run nox --reuse-existing-sessions
```

### Coverage Issues

**Error**: Coverage reports not generated

**Solution**:
```bash
# Install coverage dependencies
poetry add --group dev pytest-cov

# Run with coverage
poetry run invoke test coverage

# Check coverage report
open htmlcov/index.html
```

## Code Quality Issues

### Ruff Linting Errors

**Error**: Ruff finds many linting issues

**Solution**:
```bash
# Fix auto-fixable issues
poetry run ruff check . --fix

# Format code
poetry run ruff format .

# Check specific file
poetry run ruff check superprompts/cli/main.py

# Ignore specific rules (temporarily)
poetry run ruff check . --ignore E501,W503
```

### MyPy Type Errors

**Error**: MyPy type checking fails

**Solution**:
```bash
# Run MyPy with verbose output
poetry run mypy superprompts/ --verbose

# Check specific file
poetry run mypy superprompts/cli/main.py

# Ignore specific errors (temporarily)
poetry run mypy superprompts/ --ignore-missing-imports
```

### Black/Isort Conflicts

**Error**: Black and isort have conflicting formatting

**Solution**:
```bash
# Use Ruff instead (recommended)
poetry run ruff format .

# Or configure isort to work with Black
poetry run isort . --profile black
poetry run black .
```

## Server Issues

### MCP Server Won't Start

**Error**: Server fails to start

**Solution**:
```bash
# Check server status
poetry run invoke status

# Start in debug mode
poetry run invoke dev-server

# Check logs
SUPERPROMPTS_LOG_LEVEL=DEBUG poetry run superprompts-server
```

### CLI Tool Issues

**Error**: `superprompts` command not found

**Solution**:
```bash
# Use Poetry to run CLI
poetry run superprompts --help

# Check installation
poetry run invoke status

# Reinstall
poetry install
```

### Import Errors in Server

**Error**: Server fails with import errors

**Solution**:
```bash
# Check Python path
poetry run python -c "import sys; print(sys.path)"

# Verify installation
poetry run python -c "import superprompts"

# Reinstall
poetry install
```

## Performance Issues

### Slow Test Execution

**Problem**: Tests run slowly

**Solution**:
```bash
# Run tests in parallel
poetry run pytest tests/ -n auto

# Run specific tests only
poetry run invoke test startup

# Use Nox for multi-environment testing
poetry run nox -s test
```

### Slow Linting

**Problem**: Ruff is slow

**Solution**:
```bash
# Use Ruff's fast mode
poetry run ruff check . --no-cache

# Check specific files only
poetry run ruff check superprompts/

# Update Ruff
poetry add --group dev ruff@latest
```

### Memory Issues

**Problem**: Out of memory errors

**Solution**:
```bash
# Reduce parallel processes
poetry run pytest tests/ -n 1

# Use smaller test batches
poetry run nox -s test --reuse-existing-sessions

# Check memory usage
poetry run invoke status
```

## Getting Help

### Debug Information

When reporting issues, include:

```bash
# System information
poetry run invoke status

# Python version
python3 --version

# Poetry version
poetry --version

# Dependencies
poetry show

# Test output
poetry run invoke test --verbose
```

### Common Debug Commands

```bash
# Check project status
poetry run invoke status

# Show all available commands
poetry run invoke --list

# Run complete setup
poetry run invoke setup

# Clean and reinstall
poetry run invoke clean
poetry install
poetry run invoke setup
```

### Log Files

Check these locations for detailed error information:

- **Poetry logs**: `~/.cache/pypoetry/logs/`
- **Pre-commit logs**: `~/.cache/pre-commit/pre-commit.log`
- **Nox logs**: `.nox/` directory
- **Test logs**: Check test output for specific error messages

### Environment Variables

Useful environment variables for debugging:

```bash
# Enable debug logging
export SUPERPROMPTS_LOG_LEVEL=DEBUG

# Verbose Poetry output
export POETRY_VERBOSE=1

# Verbose pip output
export PIP_VERBOSE=1

# Disable pre-commit hooks
export SKIP=all
```

### Reset Everything

If all else fails, reset your development environment:

```bash
# Remove virtual environment
poetry env remove python

# Clear all caches
poetry cache clear --all

# Remove lock file
rm poetry.lock

# Clean build artifacts
poetry run invoke clean-all

# Reinstall everything
poetry install
poetry run invoke setup
```

### Still Need Help?

If you're still experiencing issues:

1. **Check the logs** for specific error messages
2. **Search existing issues** on GitHub
3. **Create a new issue** with:
   - Description of the problem
   - Steps to reproduce
   - Debug information from `poetry run invoke status`
   - Error messages and logs
4. **Join our community** discussions for help

### Useful Resources

- [Development Guide](development_guide.md) - Complete development setup
- [Contributing Guide](contributing_guide.md) - How to contribute
- [MCP Server Guide](mcp_server_guide.md) - Using the MCP server
- [Poetry Documentation](https://python-poetry.org/docs/) - Poetry usage
- [Ruff Documentation](https://docs.astral.sh/ruff/) - Ruff linting
- [Nox Documentation](https://nox.thea.codes/) - Nox testing
