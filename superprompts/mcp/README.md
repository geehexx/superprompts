# MCP (Model Context Protocol) Module

This module provides MCP server functionality, configuration management, and tooling adapters for the SuperPrompts project.

## Components

### Server (`server.py`)
FastMCP-based server that provides access to SuperPrompts functionality via MCP protocol.

**Available Tools:**
- `list_prompts` - List all available prompts
- `get_prompt` - Get specific prompt with parameters
- `get_prompt_metadata` - Get prompt metadata
- `compose_prompt` - Compose custom prompts

### Configuration (`config.py`)
MCP configuration generation, validation, and management for different IDE formats.

**Supported Formats:**
- Cursor IDE format
- VS Code format
- Generic MCP format

**Key Classes:**
- `MCPConfigGenerator` - Generate configurations
- `MCPConfigValidator` - Validate configurations
- `MCPConfigConverter` - Convert between formats

### Adapters (`adapters.py`)
MCP tooling integration and format conversion utilities.

**Key Classes:**
- `MCPToolingAdapter` - Tool integration and server management
- `MCPFormatConverter` - Format conversion utilities

## Usage

### Server
```bash
# Start MCP server
uv run python -m superprompts.mcp.server

# With debug mode
SUPERPROMPTS_LOG_LEVEL=DEBUG uv run python -m superprompts.mcp.server
```

### Configuration
```bash
# Generate Cursor configuration
uv run superprompts config create --format cursor

# Validate configuration
uv run superprompts config validate mcp.json

# Convert between formats
uv run superprompts config convert mcp.json --format vscode
```

### Adapters
```bash
# List available MCP tools
uv run superprompts adapt tools

# Generate FastMCP configuration
uv run superprompts adapt fastmcp my-server /path/to/server.py

# Install MCP server
uv run superprompts adapt install github-mcp-server
```

## Configuration Examples

### Cursor IDE
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

### VS Code
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

### Adding New Formats
1. Add format support to `config.py`
2. Update validation schemas
3. Add conversion logic

For detailed API documentation, see the [main documentation](../../docs/README.md).
