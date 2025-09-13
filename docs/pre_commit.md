# Pre-commit Configuration Guide

Complete guide to the pre-commit hooks configuration and code quality enforcement.

## Overview

The project uses [pre-commit](https://pre-commit.com/) to enforce code quality and consistency. Pre-commit hooks run automatically on every commit to ensure code meets project standards.

## Configuration File

The pre-commit configuration is defined in `.pre-commit-config.yaml` and includes 8 hooks:

### Hook Overview

| Hook | Purpose | Tool | Configuration |
|------|---------|------|---------------|
| `ruff` | Linting | Ruff | `--fix --exit-non-zero-on-fix` |
| `ruff-format` | Formatting | Ruff | Default formatting |
| `mypy` | Type checking | MyPy | Default configuration |
| `black` | Code formatting | Black | `--line-length=140` |
| `isort` | Import organization | isort | `--profile=black --line-length=140` |
| `trailing-whitespace` | Whitespace cleanup | pre-commit-hooks | Default |
| `end-of-file-fixer` | File endings | pre-commit-hooks | Default |
| `check-yaml` | YAML validation | pre-commit-hooks | Default |
| `check-added-large-files` | File size check | pre-commit-hooks | Default |
| `check-merge-conflict` | Conflict detection | pre-commit-hooks | Default |
| `debug-statements` | Debug cleanup | pre-commit-hooks | Default |
| `check-docstring-first` | Docstring placement | pre-commit-hooks | Default |

## Detailed Hook Configuration

### Code Quality Hooks

#### Ruff (Linting)
```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.13.0
  hooks:
    - id: ruff
      args: [--fix, --exit-non-zero-on-fix]
    - id: ruff-format
```

**Purpose:** Fast Python linting and formatting
**Configuration:** Auto-fix issues and exit with error code if fixes applied
**Runs on:** All Python files

#### MyPy (Type Checking)
```yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v1.8.0
  hooks:
    - id: mypy
```

**Purpose:** Static type checking
**Configuration:** Uses project's mypy configuration
**Runs on:** All Python files

#### Black (Code Formatting)
```yaml
- repo: https://github.com/psf/black
  rev: 24.10.0
  hooks:
    - id: black
      args: [--line-length=140]
```

**Purpose:** Code formatting with consistent style
**Configuration:** 140 character line length
**Runs on:** All Python files

#### isort (Import Organization)
```yaml
- repo: https://github.com/pycqa/isort
  rev: 5.13.2
  hooks:
    - id: isort
      args: [--profile=black, --line-length=140]
```

**Purpose:** Import statement organization
**Configuration:** Black-compatible profile, 140 character line length
**Runs on:** All Python files

### File Quality Hooks

#### Trailing Whitespace
```yaml
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v5.0.0
  hooks:
    - id: trailing-whitespace
```

**Purpose:** Remove trailing whitespace
**Runs on:** All text files

#### End of File Fixer
```yaml
- id: end-of-file-fixer
```

**Purpose:** Ensure files end with newline
**Runs on:** All text files

#### Check YAML
```yaml
- id: check-yaml
```

**Purpose:** Validate YAML syntax
**Runs on:** YAML files

#### Check Added Large Files
```yaml
- id: check-added-large-files
```

**Purpose:** Prevent large files from being committed
**Runs on:** All files

#### Check Merge Conflict
```yaml
- id: check-merge-conflict
```

**Purpose:** Detect merge conflict markers
**Runs on:** All text files

#### Debug Statements
```yaml
- id: debug-statements
```

**Purpose:** Detect and remove debug statements
**Runs on:** Python files

#### Check Docstring First
```yaml
- id: check-docstring-first
```

**Purpose:** Ensure docstrings are at the beginning of files
**Runs on:** Python files

## Installation and Setup

### Initial Setup
```bash
# Install pre-commit
uv run pip install pre-commit

# Install pre-commit hooks
uv run pre-commit install

# Install pre-commit hooks for all files
uv run pre-commit install --hook-type pre-push
```

### Manual Installation
```bash
# Install using Poetry
poetry run pre-commit install

# Install using pip
pip install pre-commit
pre-commit install
```

## Usage

### Automatic Execution
Pre-commit hooks run automatically on every commit:

```bash
# Make changes and commit
git add .
git commit -m "Your commit message"
# Hooks run automatically
```

### Manual Execution

#### Run on All Files
```bash
# Run all hooks on all files
uv run pre-commit run --all-files

# Run specific hook on all files
uv run pre-commit run --all-files ruff
uv run pre-commit run --all-files mypy
```

#### Run on Staged Files
```bash
# Run hooks on staged files only
uv run pre-commit run

# Run specific hook on staged files
uv run pre-commit run ruff
uv run pre-commit run mypy
```

#### Run Specific Hooks
```bash
# Run multiple hooks
uv run pre-commit run ruff mypy black

# Run with verbose output
uv run pre-commit run --verbose
```

### Using Invoke Tasks
```bash
# Run pre-commit checks
uv run invoke pre_commit

# Run all quality checks
uv run invoke check_all
```

## Hook Behavior

### Auto-fixing Hooks
These hooks automatically fix issues:
- **Ruff**: Fixes linting issues
- **Black**: Formats code
- **isort**: Organizes imports
- **trailing-whitespace**: Removes trailing whitespace
- **end-of-file-fixer**: Adds missing newlines

### Validation Hooks
These hooks only report issues:
- **MyPy**: Type checking errors
- **check-yaml**: YAML syntax errors
- **check-added-large-files**: Large file warnings
- **check-merge-conflict**: Merge conflict detection
- **debug-statements**: Debug statement detection
- **check-docstring-first**: Docstring placement

### Hook Execution Order
1. **trailing-whitespace** - Clean whitespace
2. **end-of-file-fixer** - Fix file endings
3. **check-yaml** - Validate YAML
4. **check-added-large-files** - Check file sizes
5. **check-merge-conflict** - Check for conflicts
6. **debug-statements** - Remove debug code
7. **check-docstring-first** - Check docstring placement
8. **ruff** - Lint and fix code
9. **ruff-format** - Format code
10. **mypy** - Type checking
11. **black** - Code formatting
12. **isort** - Import organization

## Configuration Customization

### Adding New Hooks
Edit `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/example/pre-commit-hooks
  rev: v1.0.0
  hooks:
    - id: new-hook
      args: [--option=value]
```

### Modifying Existing Hooks
```yaml
- id: ruff
  args: [--fix, --exit-non-zero-on-fix, --select=E,W]
```

### Excluding Files
```yaml
- id: ruff
  exclude: ^tests/.*\.py$
```

### Language-specific Hooks
```yaml
- id: ruff
  types: [python]
  exclude: ^tests/.*\.py$
```

## Troubleshooting

### Common Issues

#### Hook Installation Fails
```bash
# Clean and reinstall
uv run pre-commit clean
uv run pre-commit install

# Update hooks
uv run pre-commit autoupdate
```

#### Hooks Fail on Commit
```bash
# Run hooks manually to see errors
uv run pre-commit run --all-files

# Fix issues and try again
uv run pre-commit run --all-files
git add .
git commit -m "Your commit message"
```

#### Performance Issues
```bash
# Run specific hooks only
uv run pre-commit run ruff mypy

# Skip slow hooks temporarily
SKIP=mypy uv run pre-commit run
```

#### Hook Conflicts
```bash
# Check hook versions
uv run pre-commit run --all-files --verbose

# Update conflicting hooks
uv run pre-commit autoupdate
```

### Debug Mode

#### Verbose Output
```bash
uv run pre-commit run --verbose
```

#### Debug Information
```bash
uv run pre-commit run --all-files --show-diff-on-failure
```

#### Hook Debugging
```bash
# Run specific hook with debug
uv run pre-commit run ruff --verbose
```

## Integration with Development Workflow

### Pre-commit Workflow
```bash
# 1. Make changes
# ... edit files ...

# 2. Stage changes
git add .

# 3. Commit (hooks run automatically)
git commit -m "Your changes"

# 4. If hooks fail, fix issues and repeat
uv run pre-commit run --all-files
git add .
git commit -m "Your changes"
```

### CI/CD Integration
Pre-commit hooks are also run in CI:

```yaml
# .github/workflows/ci.yml
- name: Run pre-commit
  uses: pre-commit/action@v3.0.0
```

### IDE Integration
Many IDEs can run pre-commit hooks:

- **VS Code**: Pre-commit extension
- **PyCharm**: Pre-commit plugin
- **Vim**: Pre-commit plugin
- **Emacs**: Pre-commit hook

## Best Practices

### Development
1. **Install hooks early** in project setup
2. **Run hooks manually** before committing
3. **Fix issues immediately** when hooks fail
4. **Use consistent configuration** across team

### Configuration
1. **Keep hooks updated** with `pre-commit autoupdate`
2. **Use specific versions** for reproducible builds
3. **Test hook changes** before committing
4. **Document custom hooks** in project README

### Performance
1. **Use fast hooks** (Ruff over flake8)
2. **Exclude unnecessary files** from slow hooks
3. **Run hooks in parallel** when possible
4. **Skip slow hooks** during development if needed

## Advanced Usage

### Custom Hooks
Create custom hooks in `.pre-commit-hooks.yaml`:

```yaml
- id: custom-hook
  name: Custom Hook
  entry: python scripts/custom_hook.py
  language: python
  types: [python]
```

### Local Hooks
Add local hooks to `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: custom-local-hook
      name: Custom Local Hook
      entry: python scripts/local_hook.py
      language: python
      types: [python]
```

### Conditional Hooks
```yaml
- id: ruff
  stages: [commit]
  exclude: ^tests/.*\.py$
```

### Hook Dependencies
```yaml
- id: ruff
  additional_dependencies: [ruff[target-version=py310]]
```

## Cross-References

- [Development](development.md) - Complete development setup
- [Invoke Tasks](tasks.py) - Task automation
- [CI/CD Workflows](ci_cd_workflows.md) - CI/CD integration
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
