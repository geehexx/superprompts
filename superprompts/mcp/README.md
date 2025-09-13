# MCP (Model Context Protocol) Module

This module provides MCP server functionality for the SuperPrompts project.

## Components

### Server (`server.py`)
FastMCP-based server that provides access to SuperPrompts functionality via MCP protocol.

**Available Prompts:**
- `repo_docs` - Repository Documentation Rebuilder prompt
- `cursor_rules` - Cursor Rules Generator prompt

### Configuration
For detailed MCP server configuration instructions, see the [MCP Configuration Guide](../../docs/mcp_configuration.md).

## Usage

### Server
```bash
# Start MCP server
uv run python -m superprompts.mcp.server

# With debug mode
SUPERPROMPTS_LOG_LEVEL=DEBUG uv run python -m superprompts.mcp.server
```

### CLI
```bash
# List available prompts
uv run superprompts list-prompts

# Get a specific prompt
uv run superprompts get-prompt repo_docs

# Get prompt metadata
uv run superprompts metadata cursor_rules
```

## Configuration

For detailed MCP server configuration instructions, see the [MCP Configuration Guide](../../docs/mcp_configuration.md).

### Basic Configuration Examples

#### Cursor IDE
```json
{
  "mcpServers": {
    "superprompts": {
      "command": "uv",
      "args": ["run", "python", "-m", "superprompts.mcp.server"],
      "description": "SuperPrompts MCP Server"
    }
  }
}
```

#### VS Code
```json
{
  "mcp": {
    "servers": {
      "superprompts": {
        "command": "uv",
        "args": ["run", "python", "-m", "superprompts.mcp.server"],
        "description": "SuperPrompts MCP Server"
      }
    }
  }
}
```

## Development

### Adding New Tools
1. Add tool function to `server.py`
2. Register with `@server.tool()` decorator
3. Update documentation

For detailed API documentation, see the [API Reference](../../docs/api.md), [CLI Reference](../../docs/cli_reference.md), and [MCP Server Reference](../../docs/mcp_reference.md).
