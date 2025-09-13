# CI/CD Workflows Guide

Complete guide to the GitHub Actions workflows and continuous integration pipeline.

## Overview

The project uses GitHub Actions for continuous integration and deployment. There are two main workflows defined in `.github/workflows/`:

- **`ci.yml`** - Main CI pipeline for testing and validation
- **`validate.yml`** - Documentation and Cursor rules validation

## Main CI Workflow (`ci.yml`)

### Triggers
- **Push events**: `main` and `develop` branches
- **Pull requests**: Targeting `main` and `develop` branches

### Jobs

#### 1. Test Job
**Purpose**: Run tests across multiple Python versions

**Configuration:**
- **Matrix Strategy**: Python 3.10, 3.11, 3.12
- **Runner**: `ubuntu-latest`

**Steps:**
1. **Checkout Code**: Uses `actions/checkout@v4`
2. **Setup Python**: Uses `actions/setup-python@v5`
3. **Install Poetry**: Uses `snok/install-poetry@v1`
4. **Cache Dependencies**: Uses `actions/cache@v4` for `.venv`
5. **Install Dependencies**: `poetry install --no-interaction`
6. **Run Linting**: `poetry run ruff check .`
7. **Check Formatting**: `poetry run ruff format --check .`
8. **Type Checking**: `poetry run mypy superprompts/`
9. **Run Tests**: `poetry run pytest tests/ -v`
10. **Security Checks**: `poetry run bandit -r superprompts/ -f json -o bandit-report.json`
11. **Upload Security Report**: Uses `actions/upload-artifact@v4`

**Artifacts:**
- `bandit-report-{python-version}.json` - Security analysis reports

#### 2. Pre-commit Job
**Purpose**: Run pre-commit hooks validation

**Configuration:**
- **Python Version**: 3.12
- **Runner**: `ubuntu-latest`

**Steps:**
1. **Checkout Code**: Uses `actions/checkout@v4`
2. **Setup Python**: Uses `actions/setup-python@v5`
3. **Install Poetry**: Uses `snok/install-poetry@v1`
4. **Install Dependencies**: `poetry install --no-interaction`
5. **Run Pre-commit**: Uses `pre-commit/action@v3.0.0`

#### 3. Nox Job
**Purpose**: Run Nox multi-environment testing

**Configuration:**
- **Python Version**: 3.12
- **Runner**: `ubuntu-latest`

**Steps:**
1. **Checkout Code**: Uses `actions/checkout@v4`
2. **Setup Python**: Uses `actions/setup-python@v5`
3. **Install Poetry**: Uses `snok/install-poetry@v1`
4. **Install Dependencies**: `poetry install --no-interaction`
5. **Run Nox**: `poetry run nox`

#### 4. Build Job
**Purpose**: Build package for distribution

**Configuration:**
- **Python Version**: 3.12
- **Runner**: `ubuntu-latest`
- **Dependencies**: Requires `test`, `pre-commit`, and `nox` jobs to pass

**Steps:**
1. **Checkout Code**: Uses `actions/checkout@v4`
2. **Setup Python**: Uses `actions/setup-python@v5`
3. **Install Poetry**: Uses `snok/install-poetry@v1`
4. **Install Dependencies**: `poetry install --no-interaction`
5. **Build Package**: `poetry build`
6. **Upload Artifacts**: Uses `actions/upload-artifact@v4`

**Artifacts:**
- `dist` - Built package files (wheel and source distribution)

## Validation Workflow (`validate.yml`)

### Triggers
- **Pull requests**: All pull requests
- **Push events**: `main` branch only

### Jobs

#### 1. Validate Job
**Purpose**: Validate documentation and Cursor rules

**Configuration:**
- **Python Version**: 3.11
- **Runner**: `ubuntu-latest`

**Steps:**
1. **Checkout Code**: Uses `actions/checkout@v4`
2. **Setup Python**: Uses `actions/setup-python@v5`
3. **Install Dependencies**: `pip install -r requirements-dev.txt`
4. **Run PyMarkdown Scan**: `pymarkdown scan . || true`
5. **Validate Cursor Rules**: `python3 scripts/validate_cursor_rules.py --strict --report-json artifacts/cursor_rules_report.json .cursor/rules prompts/generate_cursor_rules.prompt.md`
6. **Upload Validator Report**: Uses `actions/upload-artifact@v4`

**Artifacts:**
- `cursor-rules-report` - Cursor rules validation report

## Workflow Dependencies

### Job Dependencies
```
test (parallel) → build
pre-commit (parallel) → build
nox (parallel) → build
```

### Artifact Dependencies
- Security reports are generated for each Python version
- Build artifacts depend on all validation jobs passing

## Usage Patterns

### For Contributors

#### Pull Request Workflow
1. Create feature branch
2. Make changes
3. Push to GitHub
4. **Automatic triggers**:
   - `ci.yml` runs on push to PR
   - `validate.yml` runs on PR creation/update
5. Check workflow results in GitHub Actions tab
6. Fix any failures before requesting review

#### Pre-commit Workflow
```bash
# Run pre-commit hooks locally
uv run invoke pre_commit

# Or run specific checks
uv run invoke lint
uv run invoke type_check
uv run invoke test
```

### For Maintainers

#### Release Workflow
1. Merge PR to `main` branch
2. **Automatic triggers**:
   - `ci.yml` runs full pipeline
   - `validate.yml` validates documentation
3. Check all jobs pass
4. Build artifacts are available for download
5. Proceed with release process

#### Manual Workflow Triggers
- Workflows can be manually triggered from GitHub Actions tab
- Useful for testing changes or re-running failed jobs

## Monitoring and Debugging

### Workflow Status
- Check workflow status in GitHub Actions tab
- Green checkmark: All jobs passed
- Red X: One or more jobs failed
- Yellow circle: Workflow in progress

### Job Logs
- Click on any job to view detailed logs
- Logs show step-by-step execution
- Error messages help identify issues

### Common Failure Points

#### Test Failures
- **Linting errors**: Fix with `uv run invoke format`
- **Type errors**: Fix type annotations
- **Test failures**: Check test code and dependencies

#### Security Issues
- **Bandit warnings**: Review security report
- **Dependency vulnerabilities**: Update dependencies

#### Build Failures
- **Dependency issues**: Check `pyproject.toml`
- **Python version compatibility**: Verify Python version support

## Configuration Files

### Workflow Configuration
- **`.github/workflows/ci.yml`**: Main CI pipeline
- **`.github/workflows/validate.yml`**: Validation pipeline

### Dependencies
- **`pyproject.toml`**: Python dependencies and project configuration
- **`requirements-dev.txt`**: Development dependencies for validation

### Scripts
- **`scripts/validate_cursor_rules.py`**: Cursor rules validation script

## Best Practices

### For Contributors
1. **Run locally first**: Use `uv run invoke ci` to test locally
2. **Check pre-commit**: Ensure pre-commit hooks pass
3. **Test multiple Python versions**: Use `uv run nox -s test`
4. **Review security reports**: Check Bandit output for issues

### For Maintainers
1. **Monitor workflow health**: Check for recurring failures
2. **Update dependencies**: Keep GitHub Actions up to date
3. **Review security reports**: Address security vulnerabilities
4. **Maintain build artifacts**: Ensure build process works

## Troubleshooting

### Common Issues

**Workflow fails to start:**
- Check branch triggers in workflow files
- Verify GitHub Actions is enabled for repository

**Dependency installation fails:**
- Check `pyproject.toml` for syntax errors
- Verify Python version compatibility

**Tests fail in CI but pass locally:**
- Check Python version differences
- Verify environment variables
- Check for missing dependencies

**Security checks fail:**
- Review Bandit report for specific issues
- Update dependencies if vulnerabilities found
- Add security suppressions if false positives

### Getting Help

- Check workflow logs for detailed error messages
- Review GitHub Actions documentation
- Check project's troubleshooting guide
- Open an issue for persistent problems

## Cross-References

- [Development](development.md) - Complete development setup
- [Invoke Tasks](tasks.py) - Local task automation
- [Nox Sessions](noxfile.py) - Multi-environment testing
- [Contributing Guide](contributing_guide.md) - How to contribute
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
