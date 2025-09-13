# superprompts

A collection of reusable AI prompts for everyday tasks, along with comprehensive documentation on prompting techniques and best practices.

## Purpose

This repository serves as a curated collection of high-quality AI prompts designed for practical use across diverse projects and tasks. Each prompt is accompanied by detailed documentation explaining its purpose, usage, customization options, and the techniques used in its design.

## Repository Structure

### 📁 [superprompts/](superprompts/)
Python package with dynamic prompt generators and CLI tools.

- **Cursor Rules Generator** - Generates high-signal Cursor rules tailored to your stack
- **Repository Documentation Rebuilder** - Rebuilds documentation safely with loss auditing
- **CLI Tools** - Command-line interface for all prompt functionality
- **MCP Server** - Model Context Protocol server for AI tool integration
- **MCP Configuration Management** - Tools for creating and managing MCP server definitions

### 📁 [docs/](docs/)
General documentation on prompting techniques, best practices, and standards.

- **[Available Prompts](docs/available_prompts.md)** - Complete index of all available prompts with usage patterns
- **[Architecture](docs/architecture.md)** - System architecture and design principles
- **[API](docs/api.md)** - Complete API documentation with examples
- **[AI Prompting Best Practices](docs/ai_prompting_best_practices.md)** - Core principles and reusable patterns for designing robust prompts
- **[AI-Ready Documentation Standards](docs/ai_ready_documentation_standards.md)** - Standards for creating maintainable, discoverable documentation
- **[Commit Standards](docs/commit_standards.md)** - Git commit message conventions and best practices
- **[MCP Guide](docs/mcp_guide.md)** - Complete guide to using the MCP server and CLI tools

## Quick Start

### Using Prompts Directly
1. **Quick Start**: Follow the [Quick Start Guide](docs/quick_start_guide.md) to get up and running in minutes
2. **Browse Prompts**: Check the [Available Prompts](docs/available_prompts.md) index for ready-to-use prompts
3. **Learn Architecture**: Read the [Architecture Guide](docs/architecture_guide.md) to understand the system design
4. **API Reference**: Check the [API Reference](docs/api_reference.md) for detailed usage examples
5. **Learn Techniques**: Read the guides in [docs/](docs/) to understand the underlying principles
6. **Use CLI Tools**: Use `uv run superprompts get-prompt <prompt_id>` to generate prompts with parameters
7. **Customize**: Adjust parameters to adapt prompts to your specific needs

### Using the MCP Server with Cursor IDE
1. **Install**: `uv sync` (from source) or `pip install superprompts` (from PyPI)
2. **Setup Cursor**: Create `.cursor/mcp.json` with the server configuration:
   ```json
   {
     "mcpServers": {
       "superprompts": {
         "command": "uv",
         "args": ["run", "python", "-m", "superprompts.mcp.server"],
         "env": {},
         "cwd": "/absolute/path/to/your/project"
       }
     }
   }
   ```
3. **Add to .gitignore**: Add `.cursor/mcp.json` to prevent committing machine-specific paths
4. **Restart Cursor**: Restart Cursor IDE to load the MCP server
5. **Use Tools**: Access 4 MCP tools in Cursor: `list_prompts`, `get_prompt`, `get_prompt_metadata`, `compose_prompt`

### MCP Configuration Management
1. **Configure MCP Client**: Follow the [MCP Configuration Guide](docs/mcp_configuration.md)
2. **Use Prompts**: Access prompts through your MCP client or CLI

See the [MCP Server Guide](docs/mcp_server_guide.md) and [MCP Configuration Guide](docs/mcp_configuration_guide.md) for detailed usage instructions.

### Development Setup

This project uses a modern Python development workflow with `uv`, Ruff, Nox, and Invoke:

1. **Install uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. **Install Dependencies**: `uv sync --dev`
3. **Install Pre-commit Hooks**: `uv run pre-commit install`
4. **Run Tests**: `uv run invoke test`
5. **Format Code**: `uv run invoke format`
6. **Run Linting**: `uv run invoke lint`

See the [Development Guide](docs/development_guide.md) for comprehensive setup and usage instructions.

### Code Quality & Validation

- **Pre-commit Hooks**: Automated code quality checks on every commit
  - Ruff linting and formatting (140 char line length)
  - MyPy type checking with comprehensive type annotations
  - Standard pre-commit hooks for common issues
- **Multi-environment Testing**: `uv run nox` (tests across Python 3.10, 3.11, 3.12)
- **CI/CD**: GitHub Actions workflow with comprehensive testing and validation
- **Code Quality**:
  - Ruff for fast linting and formatting (reduced from 62 to 20 minor warnings)
  - MyPy for comprehensive type checking (92 type annotation errors resolved)
  - Bandit for security analysis
  - 54 comprehensive tests (100% pass rate)
- **Modern Python**: Full type hints with Python 3.10+ syntax, comprehensive error handling
- **Code Maintainability**: Refactored complex functions, improved error handling, enhanced security

## Key Features

- **Self-Contained Prompts**: Each prompt includes everything needed for immediate use
- **Comprehensive Documentation**: Detailed explanations of purpose, usage, and customization
- **Best Practices Integration**: Prompts built using proven techniques and patterns
- **Safety-First Design**: Emphasis on auditable, reversible operations
- **AI-Ready Standards**: Documentation optimized for AI consumption and maintenance

## Design Philosophy

Our prompts are built on core principles:
- **Explicit Instructions**: Clear roles, goals, constraints, and output formats
- **Plan-Then-Act**: Structured thinking before execution
- **Safety Rails**: Content-at-risk reporting and revert options
- **Quality Over Tokens**: Clarity and completeness over brevity
- **Iterative Refinement**: Built-in evaluation and improvement cycles

## Contributing

We welcome contributions! Please see our [Contributing Guide](docs/contributing_guide.md) for detailed instructions.

### Quick Start for Contributors
1. **Fork and Clone**: Fork the repository and clone your fork
2. **Setup Development Environment**: `uv sync --dev && uv run invoke setup`
3. **Create Feature Branch**: `git checkout -b feature/your-feature-name`
4. **Make Changes**: Follow our coding standards and run `uv run invoke check-all`
5. **Test Changes**: `uv run invoke test` and `uv run nox`
6. **Submit Pull Request**: Create a PR with a clear description

### Development Workflow
- **Code Quality**: Pre-commit hooks ensure consistent code quality
- **Testing**: Multi-environment testing with Nox
- **Documentation**: Comprehensive guides for all development tasks
- **CI/CD**: Automated testing and validation on every PR

See the [Development Guide](docs/development_guide.md) for complete setup instructions.

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for the full license text.
