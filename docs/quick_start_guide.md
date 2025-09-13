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
git clone https://github.com/geehexx/superprompts.git
cd superprompts

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
export PATH="$HOME/.local/bin:$PATH"

# Install dependencies
uv sync --dev

# Verify installation
uv run superprompts --help
```

### Option 2: From PyPI (When Available)

```bash
uv add superprompts
```

## Basic Usage

### List Available Prompts

```bash
# List all prompts
uv run superprompts list-prompts

# List prompts by category
uv run superprompts list-prompts --category docs
uv run superprompts list-prompts --category rules
```

### Get a Specific Prompt

```bash
# Get repository documentation prompt
uv run superprompts get-prompt repo_docs

# Get cursor rules prompt
uv run superprompts get-prompt cursor_rules
```

### Use Prompts with Parameters

```bash
# Get cursor rules for testing category
uv run superprompts get-prompt cursor_rules --parameters '{"target_categories": ["testing"]}'

# Get repository docs with custom parameters
uv run superprompts get-prompt repo_docs --parameters '{"target_doc_types": ["README", "API"]}'
```

### Start the MCP Server

```bash
# Start server for AI tool integration
uv run superprompts-server

# Or using invoke
uv run invoke run-server
```

## Development Setup

### Complete Development Environment

```bash
# Setup everything
uv run invoke setup

# This will:
# - Install all dependencies
# - Format code
# - Run code quality checks
# - Verify everything is working
```

### Run Tests

```bash
# Run all tests
uv run invoke test

# Run specific test types
uv run invoke test --startup
uv run invoke test --integration

# Run with coverage
uv run invoke test --coverage
```

### Code Quality

```bash
# Format code
uv run invoke format

# Run linting
uv run invoke lint

# Run all quality checks
uv run invoke check_all
```

## Common Commands

### Development Workflow

| Command | Description |
|---------|-------------|
| `uv run invoke status` | Show project status |
| `uv run invoke test` | Run all tests |
| `uv run invoke format` | Format code |
| `uv run invoke lint` | Run linting |
| `uv run invoke clean` | Clean build artifacts |
| `uv run invoke setup` | Complete development setup |

### Server Commands

| Command | Description |
|---------|-------------|
| `uv run invoke run_server` | Start MCP server |
| `uv run invoke run_server --debug` | Start server in debug mode |
| `uv run superprompts-server` | Start server directly |

### Testing Commands

| Command | Description |
|---------|-------------|
| `uv run invoke test` | Run all tests |
| `uv run invoke test --startup` | Run startup tests |
| `uv run invoke test --integration` | Run integration tests |
| `uv run nox` | Multi-environment testing |

### CLI Commands

| Command | Description |
|---------|-------------|
| `uv run superprompts list-prompts` | List all prompts |
| `uv run superprompts get-prompt <id>` | Get specific prompt |
| `uv run superprompts metadata <id>` | Get prompt metadata |

## Next Steps

### For Users

1. **Browse Prompts**: Check [Available Prompts](available_prompts.md) for ready-to-use prompts
2. **Learn Techniques**: Read [AI Prompting Best Practices](ai_prompting_best_practices.md)
3. **Use MCP Server**: Follow the [MCP Configuration Guide](mcp_configuration.md)
4. **Customize Prompts**: Learn about parameters and customization options

### For Developers

1. **Development Setup**: Follow the [Development](development.md)
2. **Contributing**: Read the [Contributing Guide](contributing_guide.md)
3. **Troubleshooting**: Check the [Troubleshooting Guide](troubleshooting.md)
4. **API Reference**: Explore the codebase and documentation

### For Contributors

1. **Fork and Clone**: Fork the repository and clone your fork
2. **Setup Environment**: `uv sync --dev && uv run invoke setup`
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
├── development.md
├── contributing_guide.md
├── troubleshooting.md
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

- [Development](development.md) - Complete development setup
- [Contributing Guide](contributing_guide.md) - How to contribute
- [MCP Configuration Guide](mcp_configuration.md) - Using the MCP server
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

### Commands

```bash
# Show all available commands
uv run invoke --list

# Show help for specific command
uv run invoke help test

# Show project status
uv run invoke status

# Show CLI help
uv run superprompts --help
```

### Community

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

## Examples

### Basic Prompt Usage

```bash
# Get a simple prompt
uv run superprompts get-prompt repo_docs

# Get prompt with parameters
uv run superprompts get-prompt cursor_rules --parameters '{"target_categories": ["testing", "documentation"]}'

# Get prompt metadata
uv run superprompts metadata repo_docs
```

### Development Workflow

```bash
# Start development
uv run invoke setup

# Make changes to code
# ... edit files ...

# Format and lint
uv run invoke format
uv run invoke lint

# Run tests
uv run invoke test

# Commit changes (pre-commit hooks run automatically)
git add .
git commit -m "Your changes"
```

### Server Integration

```bash
# Start MCP server
uv run superprompts-server

# In another terminal, use CLI
uv run superprompts list-prompts
uv run superprompts get-prompt repo_docs
```

That's it! You're ready to start using SuperPrompts. 🚀
