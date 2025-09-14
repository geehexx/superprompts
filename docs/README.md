# Documentation

This directory contains general documentation about AI prompting techniques, best practices, and documentation standards.

## Contents

### Core Guides

- **[Architecture](architecture.md)** - System architecture and design principles for understanding the SuperPrompts codebase.

- **[API](api.md)** - Python API documentation with examples, type hints, and usage patterns.
- **[CLI Reference](cli_reference.md)** - Complete CLI command reference and usage examples.
- **[MCP Server Reference](mcp_reference.md)** - MCP server details and integration guide.

- **[AI Prompting Best Practices](ai_prompting_best_practices.md)** - A comprehensive guide to designing robust prompts that generate accurate, auditable, and maintainable outputs across diverse repositories and tasks.

- **[AI-Ready Documentation Standards](ai_ready_documentation_standards.md)** - Practical, AI-optimized documentation standards that improve discoverability, readability, and safe maintenance across repositories.

### Usage Guides

- **[Getting Started](getting_started.md)** - Complete getting started guide for new users with quick setup and first steps.

- **[Installation Guide](installation_guide.md)** - Detailed installation instructions for all platforms and environments.

- **[Available Prompts](available_prompts.md)** - Complete index of all available prompts with quick reference and usage patterns.

- **[Cursor Rules Guide](cursor_rules_guide.md)** - Complete guide to Cursor IDE rules and the nested rules architecture.

- **[Nested Cursor Rules](nested_cursor_rules.md)** - Comprehensive documentation for the nested rules system.

- **[MCP Configuration Guide](mcp_configuration.md)** - Complete guide to configuring MCP servers for AI tools.

### Development Guides

- **[Development](development.md)** - Complete development setup and workflow using uv, Ruff, Nox, and Invoke.

- **[Contributing Guide](contributing_guide.md)** - How to contribute to the project with modern development tools and practices.

- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions for development environment and tools.

### Development Tools

- **[CI/CD Workflows Guide](ci_cd_workflows.md)** - GitHub Actions workflows and continuous integration pipeline.

- **[Invoke Tasks](tasks.py)** - Task automation (see `tasks.py` for complete reference)

- **[Nox Sessions](noxfile.py)** - Multi-environment testing (see `noxfile.py` for complete reference)

- **[JSON Schemas](../schemas/README.md)** - Validation schemas for Cursor rules and MCP configurations

### Advanced Topics

- **[MCP Configuration Guide](mcp_configuration.md)** - MCP server, configuration, and integration

- **[Cursor Rules Guide](cursor_rules_guide.md)** - Creating and managing Cursor IDE rules

- **[Nested Cursor Rules](nested_cursor_rules.md)** - Comprehensive documentation for the nested rules system

- **[Pre-commit](pre_commit.md)** - Code quality enforcement and pre-commit hooks

- **[Commit Standards](commit_standards.md)** - Git commit message conventions and validation

- **[Testing](testing.md)** - Comprehensive testing approach and best practices

- **[Development Environment](development_environment.md)** - Complete development environment setup and management

### Reference Documentation

- **[Environment Variables](environment_variables.md)** - Environment variables reference

- **[Error Handling](error_handling.md)** - Error handling strategies and debugging approaches

- **[Performance](performance.md)** - Performance optimization and monitoring strategies

- **[Security](security.md)** - Security considerations and best practices

### Project Management

- **[CHANGELOG](../CHANGELOG.md)** - Version history and change tracking for the project.

### Prompt Documentation

- **[Cursor Rules Guide](cursor_rules_guide.md)** - Comprehensive guide to generating Cursor IDE rules tailored to your stack.

- **[Available Prompts](available_prompts.md)** - Complete guide to rebuilding repository documentation with safety checks.

## Purpose

These guides provide the foundational knowledge and techniques that inform the design and implementation of the specific prompts available through the SuperPrompts package. They cover:

- **Prompting Principles**: Core principles like being explicit, planning then acting, structuring outputs, and iterative refinement
- **Reusable Patterns**: Operating contracts, self-critique & rubrics, few-shot biasing, and risk-first editing
- **Documentation Philosophy**: Diátaxis framework, Google Style guidelines, and safety-first documentation practices
- **Quality Standards**: Checklists and rubrics for both prompts and documentation

## How to Use

1. **For Prompt Design**: Start with [AI Prompting Best Practices](ai_prompting_best_practices.md) to understand core principles
2. **For Documentation**: Reference [AI-Ready Documentation Standards](ai_ready_documentation_standards.md) when creating or improving documentation
3. **For Specific Prompts**: See the [Available Prompts](available_prompts.md) index for ready-to-use prompts and their detailed documentation

## Cross-References

- [Available Prompts](available_prompts.md) - Complete index of all available prompts and their documentation
- [Main Project README](../README.md) - Project overview and navigation
