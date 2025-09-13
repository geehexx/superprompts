# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **MCP Configuration Management**: Comprehensive MCP server configuration system
- **Development Infrastructure**: GitHub Actions CI/CD, automated testing, and development tools
- **Git Configuration**: Pre-commit hooks, commitlint, and code quality automation

### Changed
- **Documentation Structure**: Complete reorganization and consolidation of docs
- **Code Quality**: Comprehensive type safety improvements and MyPy integration
- **Development Workflow**: Streamlined with uv-based environment management

### Fixed
- **Type Safety**: Resolved all MyPy type checking errors (100% type coverage)
- **Pre-commit Configuration**: Fixed MyPy hook to use uv environment
- **Import Organization**: Corrected import order and structure
- **Documentation References**: Fixed broken links and cross-references

### Removed
- **Legacy Files**: Removed old Makefile and consolidated documentation files
- **Redundant Configs**: Cleaned up duplicate configuration files

## [1.0.0] - 2025-09-13

### Added
- Initial release of SuperPrompts
- Repository Documentation Rebuilder prompt
- Cursor Rules Generator prompt
- FastMCP server integration
- CLI tools for prompt management
- Configuration management for MCP servers
- Comprehensive documentation suite
- Type safety with full type hints
- Async/await support throughout
- Rich console output with tables and panels
- Parameter validation and error handling
- Multi-format configuration support (Cursor, VSCode, Generic)
- Template-based configuration generation
- Configuration validation and conversion utilities
- Pre-commit hooks for code quality
- Multi-environment testing with Nox
- Comprehensive test suite (44 tests)
- Security analysis with Bandit
- Code formatting with Ruff and Black
- Import organization with isort
- MyPy type checking
- Modern Python development workflow with uv

### Features
- **Prompt System**: Modular prompt architecture with BasePrompt abstract class
- **MCP Integration**: FastMCP server with 2 core prompts (repo_docs, cursor_rules)
- **CLI Interface**: Click-based command groups with async operations
- **Configuration Management**: Support for multiple MCP server formats and templates
- **Type Safety**: Full type hints and Pydantic models for data validation
- **Documentation**: Comprehensive guides for users, developers, and contributors
- **Quality Assurance**: Built-in confidence scoring and validation checklists
- **Extensibility**: Easy to add new prompts and MCP tools

### Documentation
- Quick Start Guide with installation and basic usage
- Development Guide with complete setup instructions
- Contributing Guide with modern development practices
- MCP Server Guide for Cursor IDE integration
- MCP Configuration Guide for server management
- AI Prompting Best Practices for prompt design
- AI-Ready Documentation Standards for documentation quality
- Commit Message Standards for Git conventions
- Troubleshooting Guide for common issues
- Available Prompts index with usage patterns
- Individual guides for each prompt (Cursor Rules Generator, Repository Documentation Rebuilder)

### Technical Details
- **Python**: 3.10+ with modern syntax and type hints
- **Dependencies**: FastMCP, Pydantic, Click, Rich
- **Development Tools**: uv, Ruff, Black, isort, MyPy, pre-commit, Nox, Invoke
- **Testing**: pytest with async support, multi-environment testing
- **Code Quality**: Comprehensive linting, formatting, and type checking
- **Security**: Bandit security analysis, safe file operations
- **Performance**: Async operations, minimal dependencies, efficient MCP server

### API
- **BasePrompt**: Abstract base class for all prompts
- **PromptCategory**: Enumeration of prompt categories
- **PromptMetadata**: Data class for prompt metadata
- **RepoDocsPrompt**: Repository documentation rebuilder
- **CursorRulesPrompt**: Cursor IDE rules generator
- **MCP Server Prompts**: repo_docs, cursor_rules
- **Configuration**: External MCP client configuration only
- **CLI Commands**: list-prompts, get-prompt, metadata, compose, config


### Quality Assurance
- **Confidence Scoring**: All generated content includes confidence scores
- **Validation Checklists**: Built-in quality checklists for each prompt
- **Example Verification**: Examples are validated for correctness
- **Consistency Checks**: Cross-reference validation for related content
- **Review Process**: Generate, review, validate, iterate, apply workflow

### Development Workflow
- **Setup**: `uv sync --dev && uv run invoke setup`
- **Testing**: `uv run invoke test` and `uv run nox`
- **Code Quality**: `uv run invoke check-all`
- **Formatting**: `uv run invoke format`
- **Linting**: `uv run invoke lint`
- **Pre-commit Hooks**: Automated quality checks on every commit

### Installation
- **From Source**: `git clone && uv sync --dev`
- **From PyPI**: `pip install superprompts` (when available)
- **Development**: Complete development environment setup

### Usage
- **CLI**: `superprompts list-prompts`, `superprompts get-prompt <id>`
- **MCP Server**: `superprompts-server` or `python -m superprompts.mcp.server`
- **Configuration**: External MCP client configuration only
- **Programmatic**: Import and use prompt classes directly

### License
- MIT License - see LICENSE file for details

### Repository
- **GitHub**: https://github.com/geehexx/superprompts
- **Documentation**: Comprehensive guides in docs/ directory
- **Issues**: GitHub Issues for bug reports and feature requests
- **Discussions**: GitHub Discussions for questions and general discussion
- **Pull Requests**: GitHub Pull Requests for code contributions
