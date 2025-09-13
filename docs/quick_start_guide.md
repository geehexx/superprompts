# Quick Start Guide

Get up and running with SuperPrompts in minutes!

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Development Setup](#development-setup)
- [Common Commands](#common-commands)
- [Next Steps](#next-steps)

## Installation

### Option 1: From Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/superprompts.git
cd superprompts

# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"

# Install dependencies
poetry install

# Verify installation
poetry run superprompts --help
```

### Option 2: From PyPI (When Available)

```bash
pip install superprompts
```

## Basic Usage

### List Available Prompts

```bash
# List all prompts
poetry run superprompts list-prompts

# List prompts by category
poetry run superprompts list-prompts --category docs
poetry run superprompts list-prompts --category rules
```

### Get a Specific Prompt

```bash
# Get repository documentation prompt
poetry run superprompts get-prompt repo_docs

# Get cursor rules prompt
poetry run superprompts get-prompt cursor_rules
```

### Use Prompts with Parameters

```bash
# Get cursor rules for testing category
poetry run superprompts get-prompt cursor_rules --parameters '{"target_categories": ["testing"]}'

# Get repository docs with custom parameters
poetry run superprompts get-prompt repo_docs --parameters '{"target_doc_types": ["README", "API"]}'
```

### Start the MCP Server

```bash
# Start server for AI tool integration
poetry run superprompts-server

# Or using invoke
poetry run invoke run-server
```

## Development Setup

### Complete Development Environment

```bash
# Setup everything
poetry run invoke setup

# This will:
# - Install all dependencies
# - Format code
# - Run code quality checks
# - Verify everything is working
```

### Run Tests

```bash
# Run all tests
poetry run invoke test

# Run specific test types
poetry run invoke test startup
poetry run invoke test integration

# Run with coverage
poetry run invoke test coverage
```

### Code Quality

```bash
# Format code
poetry run invoke format

# Run linting
poetry run invoke lint

# Run all quality checks
poetry run invoke check-all
```

## Common Commands

### Development Workflow

| Command | Description |
|---------|-------------|
| `poetry run invoke status` | Show project status |
| `poetry run invoke test` | Run all tests |
| `poetry run invoke format` | Format code |
| `poetry run invoke lint` | Run linting |
| `poetry run invoke clean` | Clean build artifacts |
| `poetry run invoke setup` | Complete development setup |

### Server Commands

| Command | Description |
|---------|-------------|
| `poetry run invoke run-server` | Start MCP server |
| `poetry run invoke dev-server` | Start server in debug mode |
| `poetry run superprompts-server` | Start server directly |

### Testing Commands

| Command | Description |
|---------|-------------|
| `poetry run invoke test` | Run all tests |
| `poetry run invoke test startup` | Run startup tests |
| `poetry run invoke test integration` | Run integration tests |
| `poetry run nox` | Multi-environment testing |

### CLI Commands

| Command | Description |
|---------|-------------|
| `poetry run superprompts list-prompts` | List all prompts |
| `poetry run superprompts get-prompt <id>` | Get specific prompt |
| `poetry run superprompts metadata <id>` | Get prompt metadata |
| `poetry run superprompts tools` | List MCP tools |

## Next Steps

### For Users

1. **Browse Prompts**: Check [Available Prompts](available_prompts.md) for ready-to-use prompts
2. **Learn Techniques**: Read [AI Prompting Best Practices](ai_prompting_best_practices.md)
3. **Use MCP Server**: Follow the [MCP Server Guide](mcp_server_guide.md)
4. **Customize Prompts**: Learn about parameters and customization options

### For Developers

1. **Development Setup**: Follow the [Development Guide](development_guide.md)
2. **Contributing**: Read the [Contributing Guide](contributing_guide.md)
3. **Troubleshooting**: Check the [Troubleshooting Guide](troubleshooting_guide.md)
4. **API Reference**: Explore the codebase and documentation

### For Contributors

1. **Fork and Clone**: Fork the repository and clone your fork
2. **Setup Environment**: `poetry install && poetry run invoke setup`
3. **Create Branch**: `git checkout -b feature/your-feature-name`
4. **Make Changes**: Follow coding standards and run tests
5. **Submit PR**: Create a pull request with your changes

## Quick Reference

### Project Structure

```
superprompts/
├── cli/           # Command-line interface
├── mcp/           # MCP server implementation
├── prompts/       # Prompt generators
└── schemas/       # JSON schemas

docs/
├── development_guide.md
├── contributing_guide.md
├── troubleshooting_guide.md
└── ...

tests/
├── test_startup.py
└── test_server.py
```

### Key Files

- `pyproject.toml` - Project configuration and dependencies
- `tasks.py` - Invoke task definitions
- `noxfile.py` - Nox testing configuration
- `.pre-commit-config.yaml` - Pre-commit hooks

### Environment Variables

- `SUPERPROMPTS_LOG_LEVEL` - Set logging level (DEBUG, INFO, WARNING, ERROR)
- `SUPERPROMPTS_CONFIG_PATH` - Path to custom configuration file

## Getting Help

### Documentation

- [Development Guide](development_guide.md) - Complete development setup
- [Contributing Guide](contributing_guide.md) - How to contribute
- [MCP Server Guide](mcp_server_guide.md) - Using the MCP server
- [Troubleshooting Guide](troubleshooting_guide.md) - Common issues and solutions

### Commands

```bash
# Show all available commands
poetry run invoke --list

# Show help for specific command
poetry run invoke help test

# Show project status
poetry run invoke status

# Show CLI help
poetry run superprompts --help
```

### Community

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

## Examples

### Basic Prompt Usage

```bash
# Get a simple prompt
poetry run superprompts get-prompt repo_docs

# Get prompt with parameters
poetry run superprompts get-prompt cursor_rules --parameters '{"target_categories": ["testing", "documentation"]}'

# Get prompt metadata
poetry run superprompts metadata repo_docs
```

### Development Workflow

```bash
# Start development
poetry run invoke setup

# Make changes to code
# ... edit files ...

# Format and lint
poetry run invoke format
poetry run invoke lint

# Run tests
poetry run invoke test

# Commit changes (pre-commit hooks run automatically)
git add .
git commit -m "Your changes"
```

### Server Integration

```bash
# Start MCP server
poetry run superprompts-server

# In another terminal, use CLI
poetry run superprompts list-prompts
poetry run superprompts get-prompt repo_docs
```

That's it! You're ready to start using SuperPrompts. 🚀
