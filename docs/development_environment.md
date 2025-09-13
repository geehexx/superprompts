# Development Environment Guide

Complete guide to setting up and managing the development environment for the SuperPrompts project.

## Overview

The project uses a modern Python development stack with multiple tools for different purposes:

- **uv** - Primary package manager and Python version management
- **Poetry** - Alternative package management (legacy support)
- **Nox** - Multi-environment testing
- **Invoke** - Task automation
- **Pre-commit** - Code quality enforcement

## Tool Selection Guide

### When to Use Which Tool

#### uv (Primary)
**Use for:** Primary development, dependency management, Python version management

```bash
# Install dependencies
uv sync --dev

# Run commands
uv run superprompts --help
uv run pytest tests/
uv run nox -s test
```

**When to use:**
- Daily development work
- Installing dependencies
- Running Python commands
- Package management

#### Poetry (Legacy Support)
**Use for:** Legacy compatibility, CI/CD, alternative package management

```bash
# Install dependencies
poetry install --dev

# Run commands
poetry run superprompts --help
poetry run pytest tests/
poetry run nox -s test
```

**When to use:**
- CI/CD pipelines
- Legacy system compatibility
- When uv is not available

#### Nox (Multi-environment Testing)
**Use for:** Testing across multiple Python versions

```bash
# Run tests on all Python versions
uv run nox -s test

# Run specific session
uv run nox -s lint
uv run nox -s type-check
```

**When to use:**
- Testing compatibility across Python versions
- Running comprehensive test suites
- CI/CD validation

#### Invoke (Task Automation)
**Use for:** Common development tasks and automation

```bash
# Run common tasks
uv run invoke test
uv run invoke format
uv run invoke lint
uv run invoke ci
```

**When to use:**
- Common development workflows
- Task automation
- Project maintenance

#### Pre-commit (Code Quality)
**Use for:** Automatic code quality enforcement

```bash
# Install hooks
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files
```

**When to use:**
- Automatic code quality enforcement
- Pre-commit validation
- Code formatting and linting

## Environment Setup

### Prerequisites

#### Required Software
- **Python 3.10+** - Python runtime
- **Git** - Version control
- **uv** - Package manager (recommended)
- **Poetry** - Alternative package manager

#### Optional Software
- **Node.js** - For npm-based tools
- **Docker** - For containerized development
- **VS Code** - Recommended IDE

### Installation Steps

#### 1. Install uv (Recommended)
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

#### 2. Install Poetry (Alternative)
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Verify installation
poetry --version
```

#### 3. Clone Repository
```bash
# Clone the repository
git clone https://github.com/geehexx/superprompts.git
cd superprompts
```

#### 4. Install Dependencies
```bash
# Using uv (recommended)
uv sync --dev

# Using Poetry (alternative)
poetry install --dev
```

#### 5. Install Pre-commit Hooks
```bash
# Install pre-commit hooks
uv run pre-commit install

# Or using Poetry
poetry run pre-commit install
```

#### 6. Verify Installation
```bash
# Run tests
uv run invoke test

# Check project status
uv run invoke status
```

## Development Workflows

### Daily Development

#### 1. Start Development
```bash
# Pull latest changes
git pull origin main

# Install/update dependencies
uv sync --dev

# Run tests to ensure everything works
uv run invoke test
```

#### 2. Make Changes
```bash
# Make your changes
# ... edit files ...

# Format code
uv run invoke format

# Run linting
uv run invoke lint

# Run tests
uv run invoke test
```

#### 3. Commit Changes
```bash
# Stage changes
git add .

# Commit (pre-commit hooks run automatically)
git commit -m "feat(cli): add new command"

# Push changes
git push origin feature-branch
```

### Feature Development

#### 1. Create Feature Branch
```bash
# Create and switch to feature branch
git checkout -b feature/new-feature

# Ensure you're up to date
git pull origin main
```

#### 2. Develop Feature
```bash
# Make changes
# ... implement feature ...

# Test frequently
uv run invoke test
uv run invoke lint
uv run invoke format
```

#### 3. Test Thoroughly
```bash
# Run all tests
uv run invoke test

# Run multi-environment tests
uv run nox -s test

# Run full CI pipeline locally
uv run invoke ci
```

#### 4. Create Pull Request
```bash
# Push feature branch
git push origin feature/new-feature

# Create pull request on GitHub
# CI/CD will run automatically
```

### Bug Fix Development

#### 1. Create Bug Fix Branch
```bash
# Create and switch to bug fix branch
git checkout -b fix/bug-description

# Ensure you're up to date
git pull origin main
```

#### 2. Reproduce and Fix
```bash
# Reproduce the bug
# ... test reproduction ...

# Implement fix
# ... implement fix ...

# Test fix
uv run invoke test
```

#### 3. Add Tests
```bash
# Add test for the bug
# ... add test ...

# Ensure test passes
uv run invoke test
```

#### 4. Submit Fix
```bash
# Commit fix
git commit -m "fix(module): fix bug description"

# Push fix
git push origin fix/bug-description
```

## Environment Management

### Python Version Management

#### Using uv
```bash
# Check Python versions
uv python list

# Install specific Python version
uv python install 3.11

# Use specific Python version
uv run --python 3.11 python --version
```

#### Using pyenv (Alternative)
```bash
# Install pyenv
curl https://pyenv.run | bash

# Install Python versions
pyenv install 3.10.0
pyenv install 3.11.0
pyenv install 3.12.0

# Set local Python version
pyenv local 3.11.0
```

### Virtual Environment Management

#### Using uv
```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Deactivate virtual environment
deactivate
```

#### Using Poetry
```bash
# Create virtual environment
poetry install

# Activate virtual environment
poetry shell

# Deactivate virtual environment
exit
```

### Dependency Management

#### Using uv
```bash
# Add dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Update dependencies
uv sync --dev

# Remove dependency
uv remove package-name
```

#### Using Poetry
```bash
# Add dependency
poetry add package-name

# Add development dependency
poetry add --dev package-name

# Update dependencies
poetry update

# Remove dependency
poetry remove package-name
```

## IDE Configuration

### VS Code Setup

#### Extensions
Install recommended extensions:

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.pylint",
    "ms-python.black-formatter",
    "ms-python.isort",
    "ms-python.mypy-type-checker",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml"
  ]
}
```

#### Settings
Configure VS Code settings:

```json
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.ruffEnabled": true,
  "python.linting.mypyEnabled": true,
  "python.sortImports.args": ["--profile", "black"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

#### Launch Configuration
Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: MCP Server",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/superprompts/mcp/server.py",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}"
    },
    {
      "name": "Python: CLI",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/superprompts/cli/main.py",
      "args": ["--help"],
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

### PyCharm Setup

#### Project Interpreter
1. Open Project Settings
2. Go to Project Interpreter
3. Add interpreter from virtual environment
4. Select `.venv/bin/python`

#### Code Style
1. Go to Settings > Editor > Code Style > Python
2. Set line length to 140
3. Configure import organization

#### Run Configurations
1. Create new Python configuration
2. Set script path to `superprompts/mcp/server.py`
3. Set working directory to project root

## Troubleshooting

### Common Issues

#### uv Not Found
```bash
# Check if uv is installed
which uv

# Install uv if missing
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"
```

#### Python Version Issues
```bash
# Check Python version
python --version

# Install correct Python version
uv python install 3.11

# Use specific Python version
uv run --python 3.11 python --version
```

#### Dependency Issues
```bash
# Clean and reinstall
uv sync --dev --reinstall

# Or using Poetry
poetry install --dev --sync
```

#### Virtual Environment Issues
```bash
# Remove virtual environment
rm -rf .venv

# Recreate virtual environment
uv venv
uv sync --dev
```

#### Pre-commit Issues
```bash
# Reinstall pre-commit hooks
uv run pre-commit uninstall
uv run pre-commit install

# Update hooks
uv run pre-commit autoupdate
```

### Debug Mode

#### Enable Debug Logging
```bash
# Set debug environment variable
export SUPERPROMPTS_LOG_LEVEL=DEBUG

# Run with debug output
uv run superprompts --help
```

#### Verbose Output
```bash
# Run with verbose output
uv run pytest tests/ -v
uv run nox -s test --verbose
uv run invoke test --verbose
```

#### Check Environment
```bash
# Check Python environment
uv run python -c "import sys; print(sys.path)"

# Check installed packages
uv run pip list

# Check project status
uv run invoke status
```

## Best Practices

### Development
1. **Use uv for daily development** - Faster and more reliable
2. **Keep dependencies updated** - Regular `uv sync --dev`
3. **Run tests frequently** - Before and after changes
4. **Use pre-commit hooks** - Automatic code quality enforcement
5. **Test across Python versions** - Use Nox for multi-environment testing

### Environment
1. **Use virtual environments** - Isolate project dependencies
2. **Pin Python versions** - Ensure consistent environment
3. **Document environment setup** - Keep setup instructions updated
4. **Use consistent tools** - Stick to chosen toolset
5. **Regular cleanup** - Remove unused dependencies and files

### Troubleshooting
1. **Check tool versions** - Ensure compatibility
2. **Clean and reinstall** - When in doubt, start fresh
3. **Use debug mode** - Enable verbose output for debugging
4. **Check logs** - Look for error messages and warnings
5. **Ask for help** - Use project documentation and community

## Cross-References

- [Development](development.md) - Complete development setup
- [Invoke Tasks](tasks.py) - Task automation
- [Nox Sessions](noxfile.py) - Multi-environment testing
- [Pre-commit](pre_commit.md) - Code quality enforcement
- [Testing](testing.md) - Testing approach
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
