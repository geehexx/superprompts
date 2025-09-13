# MCP Server Guide

## Purpose

The SuperPrompts MCP (Model Context Protocol) Server provides programmatic access to the SuperPrompts collection through a standardized interface. This allows AI tools and applications to discover, retrieve, and compose prompts dynamically.

## Installation

### From Source (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd superprompts

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --dev

# Verify installation
uv run superprompts --help
```

### From PyPI (when published)
```bash
pip install superprompts
```

### Legacy Installation (Not Recommended)
```bash
# Using pip and virtual environment
python -m venv venv
source venv/bin/activate
pip install -e .
```

## Usage

### FastMCP Implementation

The SuperPrompts MCP server is built using **FastMCP**, a modern, high-performance framework for MCP servers. FastMCP provides:

- **Simplified Development**: Clean decorator-based API for defining tools
- **Better Performance**: Optimized for speed and efficiency
- **Type Safety**: Full type hints and validation with modern Python 3.10+ syntax
- **Modern Python**: Built for Python 3.10+ with async support
- **Rich Features**: Built-in logging, error handling, and debugging
- **Comprehensive Testing**: 44 tests including 16 integration tests for CLI commands
- **Code Quality**: Pre-commit hooks, automated linting, and comprehensive error handling

### Cursor IDE Integration

The SuperPrompts MCP server is designed to work seamlessly with Cursor IDE. Follow these steps to set it up:

#### 1. Create Cursor Configuration

Create the `.cursor` directory and MCP configuration file:

```bash
# Create .cursor directory
mkdir -p .cursor

# Create MCP configuration
cat > .cursor/mcp.json << 'EOF'
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
EOF
```

#### 2. Update Configuration

Replace `/absolute/path/to/your/project` with your actual project directory path.

#### 3. Add to .gitignore

Add the following line to your `.gitignore` file:

```
# Cursor MCP configuration (machine-specific)
.cursor/mcp.json
```

#### 4. Restart Cursor

Restart Cursor IDE to load the MCP server configuration.

#### 5. Verify Integration

Once Cursor restarts, you should see the SuperPrompts MCP server available with the following tools:
- `list_prompts` - List all available prompts with their metadata
- `get_prompt` - Get a specific prompt by ID with optional parameters
- `get_prompt_metadata` - Get detailed metadata about a specific prompt
- `compose_prompt` - Compose a custom prompt by combining elements from different prompts

### Starting the MCP Server Manually

#### Using uv (Recommended)
```bash
# Start the server
uv run superprompts-server

# Or using Python module
uv run python -m superprompts.mcp.server

# Start in development mode with debug logging
uv run invoke dev-server
```

#### Using Invoke Tasks
```bash
# Start server
uv run invoke run-server

# Start in development mode
uv run invoke dev-server
```

#### Legacy Methods (Not Recommended)
```bash
# Direct execution (requires manual dependency management)
superprompts-server

# Python module (requires manual dependency management)
python -m superprompts.mcp.server
```

### Using the CLI Tool

The `superprompts` CLI provides direct access to all server functionality:

#### With Poetry (Recommended)
```bash
# List all available prompts
uv run superprompts list-prompts

# List prompts by category
uv run superprompts list-prompts --category docs

# Get a specific prompt
uv run superprompts get-prompt repo_docs

# Get a prompt with parameters
uv run superprompts get-prompt cursor_rules --parameters '{"target_categories": ["testing"]}'

# Get prompt metadata
uv run superprompts metadata repo_docs

# Compose a custom prompt
uv run superprompts compose repo_docs --additions '[{"source_prompt_id": "cursor_rules", "element_type": "principle", "element_name": "high_signal"}]'

# List available MCP tools
uv run superprompts tools

# Call a specific tool
uv run superprompts call-tool list_prompts '{"category": "all"}'
```

#### With Invoke Tasks
```bash
# Run server tests
uv run invoke test startup
uv run invoke test integration

# Run validation
uv run invoke validate

# Show project status
uv run invoke status
```

#### Legacy Direct Usage (Not Recommended)
```bash
# Direct execution (requires manual dependency management)
superprompts list-prompts
superprompts get-prompt repo_docs
```

### MCP Protocol Integration

The server implements the Model Context Protocol, allowing integration with MCP-compatible clients:

```python
# Example client integration
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    async with stdio_client(StdioServerParameters(
        command="python",
        args=["-m", "superprompts.mcp.server"]
    )) as (read, write):
        async with ClientSession(read, write) as session:
            # List available tools
            tools = await session.list_tools()

            # Call a tool
            result = await session.call_tool("list_prompts", {"category": "all"})
            print(result)
```

## Available Tools

### `list_prompts`
Lists all available prompts with optional category filtering.

**Parameters:**
- `category` (optional): Filter by category ("docs", "rules", "all")

**Returns:** Array of prompt objects with metadata

### `get_prompt`
Retrieves a specific prompt with optional parameters.

**Parameters:**
- `prompt_id` (required): The ID of the prompt to retrieve
- `parameters` (optional): Customization parameters

**Returns:** The prompt text

### `get_prompt_metadata`
Gets detailed metadata about a specific prompt.

**Parameters:**
- `prompt_id` (required): The ID of the prompt

**Returns:** Prompt metadata object

### `compose_prompt`
Composes a custom prompt by combining elements from different prompts.

**Parameters:**
- `base_prompt_id` (required): Base prompt to start with
- `additions` (optional): Elements to add from other prompts
- `customizations` (optional): Custom modifications to apply

**Returns:** Composed prompt text

## Configuration

The server can be configured through environment variables:

- `SUPERPROMPTS_LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)
- `SUPERPROMPTS_CONFIG_PATH`: Path to custom configuration file

## Development

### Running Tests

#### Using Invoke (Recommended)
```bash
# Run all tests
uv run invoke test

# Run specific test types
uv run invoke test startup
uv run invoke test integration
uv run invoke test coverage

# Run multi-environment testing
uv run nox
```

#### Using Poetry Directly
```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test files
uv run python tests/test_startup.py
uv run python tests/test_server.py

# Run with coverage
uv run pytest tests/ --cov=superprompts --cov-report=html
```

#### Legacy Methods (Not Recommended)
```bash
# Legacy test runner (deprecated)
./tests/run_tests.sh

# Direct execution (requires manual dependency management)
python tests/test_startup.py
python tests/test_server.py
```

### Adding New Prompts

1. Create prompt files in `superprompts/prompts/`
2. Implement the prompt class following the base pattern
3. Register the prompt in the server's tool handlers
4. Update documentation

### Debugging

#### Using Poetry (Recommended)
```bash
# Enable debug logging
SUPERPROMPTS_LOG_LEVEL=DEBUG uv run superprompts-server

# Or using invoke
uv run invoke dev-server
```

#### Legacy Method (Not Recommended)
```bash
# Direct execution (requires manual dependency management)
SUPERPROMPTS_LOG_LEVEL=DEBUG superprompts-server
```

## Troubleshooting

### Common Issues

1. **Poetry Not Found**: Install uv and add to PATH
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   export PATH="$HOME/.local/bin:$PATH"
   ```

2. **Dependency Issues**: Reinstall dependencies
   ```bash
   uv sync --dev
   ```

3. **Virtual Environment Issues**: Recreate virtual environment
   ```bash
   poetry env remove python
   uv sync --dev
   ```

4. **Permission Issues**: Ensure scripts are executable (`chmod +x *.sh`)
5. **Port Conflicts**: The MCP server uses stdio, so no port conflicts should occur

### Getting Help

- Check the test output for specific error messages
- Review the server logs for detailed error information
- Ensure all required packages are installed and up to date

## MCP Configuration Management

The SuperPrompts CLI includes comprehensive tools for managing MCP server configurations:

### Configuration Commands

```bash
# Create MCP configurations
uv run superprompts config create --template superprompts --template github

# Validate configurations
uv run superprompts config validate mcp.json

# Convert between formats
uv run superprompts config convert mcp.json --format vscode

# List available templates
uv run superprompts config templates
```

### Tooling Adapters

Integrate with existing MCP tooling:

```bash
# List available MCP tools
uv run superprompts adapt tools

# Generate config with FastMCP
uv run superprompts adapt fastmcp my-server server.py --packages pandas

# Install MCP servers
uv run superprompts adapt install github-mcp-server

# Convert from other formats
uv run superprompts adapt from-openapi openapi.json my-api
uv run superprompts adapt from-docker docker-compose.yml my-service
uv run superprompts adapt from-npm package.json start-server
```

For detailed information, see the [MCP Configuration Guide](mcp_configuration_guide.md).

## Cross-References

- **[MCP Configuration Guide](mcp_configuration_guide.md)** - Complete MCP configuration management
- **AI Prompting Best Practices**: [`ai_prompting_best_practices.md`](ai_prompting_best_practices.md)
- **Available Prompts**: [`../prompts/`](../prompts/)
- **Main Project**: [`../README.md`](../README.md)
