# Contributing Guide

Thank you for your interest in contributing to SuperPrompts! This guide will help you get started with contributing to our project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)
- [Types of Contributions](#types-of-contributions)

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- Git (for version control)
- Basic understanding of Python development

### Fork and Clone

1. **Fork the Repository**
   - Go to [SuperPrompts on GitHub](https://github.com/your-org/superprompts)
   - Click the "Fork" button in the top-right corner
   - This creates a copy of the repository in your GitHub account

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/superprompts.git
   cd superprompts
   ```

3. **Add Upstream Remote**
   ```bash
   git remote add upstream https://github.com/your-org/superprompts.git
   ```

## Development Setup

### 1. Install Poetry

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add to PATH (add to your shell profile)
export PATH="$HOME/.local/bin:$PATH"

# Verify installation
poetry --version
```

### 2. Setup Development Environment

```bash
# Install dependencies
poetry install

# Setup pre-commit hooks
poetry run pre-commit install

# Run complete setup
poetry run invoke setup

# Verify everything is working
poetry run invoke status
```

### 3. Create Development Branch

```bash
# Create and switch to feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

## Making Changes

### 1. Code Quality Standards

Our project uses several tools to maintain code quality:

#### Ruff (Linting and Formatting)
```bash
# Check for issues
poetry run ruff check .

# Fix auto-fixable issues
poetry run ruff check . --fix

# Format code
poetry run ruff format .
```

#### MyPy (Type Checking)
```bash
# Run type checking
poetry run mypy superprompts/
```

#### Pre-commit Hooks
Pre-commit hooks run automatically on commit and include:
- Ruff linting and formatting
- MyPy type checking
- Security scanning with Bandit
- Markdown linting
- YAML/JSON validation

### 2. Testing Requirements

All changes must include appropriate tests:

```bash
# Run all tests
poetry run invoke test

# Run specific test types
poetry run invoke test startup
poetry run invoke test integration

# Run with coverage
poetry run invoke test coverage

# Multi-environment testing
poetry run nox
```

#### Test Coverage
- Aim for high test coverage (80%+)
- Write unit tests for new functions
- Write integration tests for complex features
- Test error conditions and edge cases

### 3. Documentation Requirements

Update documentation for all changes:

```bash
# Update relevant documentation files
# - README.md for major changes
# - docs/ directory for new features
# - Docstrings for new functions/classes
```

## Code Standards

### Python Code Style

1. **Follow PEP 8**: Use our Ruff configuration for consistent formatting
2. **Type Hints**: Use type hints for all function parameters and return values
3. **Docstrings**: Document all public functions and classes using Google style
4. **Error Handling**: Use appropriate exception handling with clear error messages

### Example Code Style

```python
def generate_prompt(
    prompt_id: str,
    parameters: dict[str, Any],
    customizations: dict[str, Any] | None = None
) -> str:
    """Generate a prompt with the given parameters.
    
    Args:
        prompt_id: The ID of the prompt to generate
        parameters: Parameters for the prompt
        customizations: Optional customizations to apply
        
    Returns:
        The generated prompt text
        
    Raises:
        ValueError: If prompt_id is invalid
        TypeError: If parameters are not a dictionary
    """
    if not prompt_id:
        raise ValueError("prompt_id cannot be empty")
    
    # Implementation here
    return generated_prompt
```

### File Organization

```
superprompts/
├── cli/           # Command-line interface
├── mcp/           # MCP server implementation
├── prompts/       # Prompt generators
└── schemas/       # JSON schemas

tests/
├── test_startup.py    # Startup tests
└── test_server.py     # Server tests

docs/
├── development_guide.md
├── contributing_guide.md
└── ...
```

## Submitting Changes

### 1. Commit Your Changes

We follow the [Conventional Commits](https://www.conventionalcommits.org/) standard for commit messages. See our [Commit Message Standards](commit_message_standards.md) for detailed guidelines.

```bash
# Stage your changes
git add .

# Commit with conventional format
git commit -m "feat(prompts): add API documentation generator"

# Push to your fork
git push origin feature/your-feature-name
```

#### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Common types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or correcting tests
- `chore`: Maintenance tasks

**Common scopes:**
- `cli`: Command-line interface
- `mcp`: MCP server functionality
- `prompts`: Prompt generators
- `docs`: Documentation files
- `tests`: Test files

**Examples:**
```bash
git commit -m "feat(prompts): add cursor rules generator"
git commit -m "fix(mcp): handle connection errors gracefully"
git commit -m "docs: update quick start guide"
```

### 2. Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Fill out the PR template
5. Submit the PR

### 3. PR Template

When creating a PR, please include:

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] All existing tests still pass

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## Review Process

### What We Look For

1. **Code Quality**
   - Follows project coding standards
   - Includes appropriate tests
   - Handles errors gracefully

2. **Functionality**
   - Solves the intended problem
   - Doesn't break existing functionality
   - Includes appropriate documentation

3. **Testing**
   - All tests pass
   - New functionality is tested
   - Test coverage is maintained

### Review Timeline

- **Initial Review**: Within 2-3 business days
- **Follow-up Reviews**: Within 1-2 business days
- **Merge**: After approval and all checks pass

### Addressing Feedback

1. **Make Requested Changes**: Update your code based on feedback
2. **Add Tests**: Include tests for any new functionality
3. **Update Documentation**: Update docs for any changes
4. **Respond to Comments**: Address any questions or concerns

## Types of Contributions

### Bug Fixes

1. **Identify the Issue**: Check existing issues or create a new one
2. **Reproduce the Bug**: Create a test case that reproduces the issue
3. **Fix the Bug**: Implement a fix that resolves the issue
4. **Add Tests**: Ensure the bug doesn't regress
5. **Submit PR**: Follow the standard PR process

### New Features

1. **Discuss First**: Open an issue to discuss the feature
2. **Plan Implementation**: Break down the feature into smaller tasks
3. **Implement**: Code the feature following our standards
4. **Test Thoroughly**: Include comprehensive tests
5. **Document**: Update all relevant documentation
6. **Submit PR**: Follow the standard PR process

### Documentation Improvements

1. **Identify Areas**: Look for unclear or missing documentation
2. **Improve Clarity**: Make documentation clearer and more comprehensive
3. **Add Examples**: Include practical examples where helpful
4. **Update Structure**: Improve organization and navigation
5. **Submit PR**: Follow the standard PR process

### Prompt Contributions

1. **Follow Structure**: Use the established prompt structure
2. **Include Documentation**: Document the prompt's purpose and usage
3. **Test Thoroughly**: Test the prompt with various inputs
4. **Validate**: Ensure the prompt follows our quality standards
5. **Submit PR**: Follow the standard PR process

## Development Tools

### Invoke Commands

```bash
# Development workflow
poetry run invoke setup          # Complete setup
poetry run invoke test           # Run tests
poetry run invoke format         # Format code
poetry run invoke lint           # Run linting
poetry run invoke check-all      # Run all quality checks
poetry run invoke clean          # Clean build artifacts

# Testing
poetry run invoke test startup   # Run startup tests
poetry run invoke test coverage  # Run with coverage
poetry run nox                   # Multi-environment testing

# Server
poetry run invoke run-server     # Start MCP server
poetry run invoke dev-server     # Start in debug mode
```

### Pre-commit Hooks

Pre-commit hooks run automatically and include:
- Ruff linting and formatting
- MyPy type checking
- Security scanning
- Markdown linting
- YAML/JSON validation

### GitHub Actions

Our CI/CD pipeline automatically:
- Runs tests on multiple Python versions
- Checks code quality
- Validates documentation
- Builds packages
- Runs security scans

## Getting Help

### Resources

- [Development Guide](development_guide.md) - Complete development setup
- [MCP Server Guide](mcp_server_guide.md) - Using the MCP server
- [Troubleshooting Guide](troubleshooting_guide.md) - Common issues and solutions
- [API Reference](api_reference.md) - Complete API documentation

### Community

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

### Questions?

If you have questions about contributing:

1. Check the [Development Guide](development_guide.md)
2. Look at existing issues and PRs
3. Open a new issue with your question
4. Join our community discussions

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to SuperPrompts! 🚀
