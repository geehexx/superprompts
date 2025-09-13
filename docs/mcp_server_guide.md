# MCP Server Guide

## Purpose

The SuperPrompts MCP (Model Context Protocol) Server provides programmatic access to the SuperPrompts collection through a standardized interface. This allows AI tools and applications to discover, retrieve, and compose prompts dynamically.

## Installation

### From Source (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd superprompts

# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Verify installation
poetry run superprompts --help
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

### Starting the MCP Server

#### Using Poetry (Recommended)
```bash
# Start the server
poetry run superprompts-server

# Or using Python module
poetry run python -m superprompts.mcp.server

# Start in development mode with debug logging
poetry run invoke dev-server
```

#### Using Invoke Tasks
```bash
# Start server
poetry run invoke run-server

# Start in development mode
poetry run invoke dev-server
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
poetry run superprompts list-prompts

# List prompts by category
poetry run superprompts list-prompts --category docs

# Get a specific prompt
poetry run superprompts get-prompt repo_docs

# Get a prompt with parameters
poetry run superprompts get-prompt cursor_rules --parameters '{"target_categories": ["testing"]}'

# Get prompt metadata
poetry run superprompts metadata repo_docs

# Compose a custom prompt
poetry run superprompts compose repo_docs --additions '[{"source_prompt_id": "cursor_rules", "element_type": "principle", "element_name": "high_signal"}]'

# List available MCP tools
poetry run superprompts tools

# Call a specific tool
poetry run superprompts call-tool list_prompts '{"category": "all"}'
```

#### With Invoke Tasks
```bash
# Run server tests
poetry run invoke test startup
poetry run invoke test integration

# Run validation
poetry run invoke validate

# Show project status
poetry run invoke status
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
poetry run invoke test

# Run specific test types
poetry run invoke test startup
poetry run invoke test integration
poetry run invoke test coverage

# Run multi-environment testing
poetry run nox
```

#### Using Poetry Directly
```bash
# Run all tests
poetry run pytest tests/ -v

# Run specific test files
poetry run python tests/test_startup.py
poetry run python tests/test_server.py

# Run with coverage
poetry run pytest tests/ --cov=superprompts --cov-report=html
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
SUPERPROMPTS_LOG_LEVEL=DEBUG poetry run superprompts-server

# Or using invoke
poetry run invoke dev-server
```

#### Legacy Method (Not Recommended)
```bash
# Direct execution (requires manual dependency management)
SUPERPROMPTS_LOG_LEVEL=DEBUG superprompts-server
```

## Troubleshooting

### Common Issues

1. **Poetry Not Found**: Install Poetry and add to PATH
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   export PATH="$HOME/.local/bin:$PATH"
   ```

2. **Dependency Issues**: Reinstall dependencies
   ```bash
   poetry install
   ```

3. **Virtual Environment Issues**: Recreate virtual environment
   ```bash
   poetry env remove python
   poetry install
   ```

4. **Permission Issues**: Ensure scripts are executable (`chmod +x *.sh`)
5. **Port Conflicts**: The MCP server uses stdio, so no port conflicts should occur

### Getting Help

- Check the test output for specific error messages
- Review the server logs for detailed error information
- Ensure all required packages are installed and up to date

## Cross-References

- **AI Prompting Best Practices**: [`ai_prompting_best_practices.md`](ai_prompting_best_practices.md)
- **Available Prompts**: [`../prompts/`](../prompts/)
- **Main Project**: [`../README.md`](../README.md)
