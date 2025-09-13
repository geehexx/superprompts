# MCP (Model Context Protocol) Guide

Complete guide to using the SuperPrompts MCP server, configuration management, and integration with AI tools.

## Overview

The SuperPrompts MCP server provides programmatic access to the SuperPrompts collection through a standardized interface, allowing AI tools and applications to discover, retrieve, and compose prompts dynamically.

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

## MCP Server

### FastMCP Implementation

The SuperPrompts MCP server is built using **FastMCP**, providing:
- Simplified development with decorator-based API
- Better performance and efficiency
- Type safety with modern Python 3.10+ syntax
- Async support and rich features
- Comprehensive testing and code quality

### Available Tools

- `list_prompts` - List all available prompts
- `get_prompt` - Get specific prompt with parameters
- `get_prompt_metadata` - Get prompt metadata
- `compose_prompt` - Compose custom prompts

### Running the Server

```bash
# Start MCP server
uv run python -m superprompts.mcp.server

# With debug mode
SUPERPROMPTS_LOG_LEVEL=DEBUG uv run python -m superprompts.mcp.server

# Using Poetry (legacy)
poetry run python -m superprompts.mcp.server
```

## Configuration Management

For detailed MCP server configuration instructions, see the [MCP Configuration Guide](mcp_configuration.md).

### Quick Start

The SuperPrompts MCP server can be configured manually by creating the appropriate configuration file for your AI tool.

### Supported Formats

#### Cursor Format (`.cursor/mcp.json`)
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

#### VS Code Format
```json
{
  "mcp": {
    "servers": {
      "superprompts": {
        "command": "uv",
        "args": ["run", "python", "-m", "superprompts.mcp.server"],
        "env": {},
        "cwd": "/absolute/path/to/your/project"
      }
    }
  }
}
```

#### Generic Format
```json
{
  "mcp": {
    "version": "1.0.0",
    "servers": {
      "superprompts": {
        "name": "superprompts",
        "command": "uv",
        "args": ["run", "python", "-m", "superprompts.mcp.server"],
        "env": {},
        "cwd": "/absolute/path/to/your/project"
      }
    }
  }
}
```

### Configuration Commands

#### Create Configuration
```bash
# Create configuration manually
# See the MCP Configuration Guide for detailed instructions
```

#### Validate Configuration
Configuration validation is handled by the MCP client, not by this project.

#### Convert Configuration
Configuration conversion is handled by the MCP client, not by this project.

#### Merge Configurations
Configuration merging is handled by the MCP client, not by this project.

## Integration Examples

### Cursor IDE Integration

1. **Create Configuration**:
   - Create `.cursor/mcp.json` manually (see MCP Configuration Guide)

2. **Place Configuration**:
   - Place config in `.cursor/mcp.json`
   - Ensure absolute paths are correct
   - Don't commit to version control

3. **Restart Cursor**:
   - Close and reopen Cursor
   - Check MCP server status in settings

### VS Code Integration

1. **Create Configuration**:
   - Create `.vscode/mcp.json` manually (see MCP Configuration Guide)

2. **Add to Settings**:
   - Open VS Code settings
   - Add MCP configuration to settings.json
   - Restart VS Code

### Generic MCP Client Integration

1. **Create Configuration**:
   - Create MCP configuration manually (see MCP Configuration Guide)

2. **Use with Client**:
   - Configure your MCP client with the generated config
   - Ensure the server command is accessible

## Troubleshooting

### Common Issues

**Server not starting**
- Check Python path and dependencies
- Verify absolute paths in configuration
- Check environment variables

**Configuration validation fails**
- Verify JSON syntax
- Check required fields are present
- Ensure format matches expected structure

**Tools not available**
- Restart the MCP client
- Check server logs for errors
- Verify tool registration

### Debug Mode

```bash
# Enable debug logging
SUPERPROMPTS_LOG_LEVEL=DEBUG uv run python -m superprompts.mcp.server

# Check server status
# Use your MCP client's built-in validation tools
```

## Best Practices

### Configuration Management
- Use absolute paths for `cwd` in configurations
- Don't commit machine-specific configurations
- Validate configurations before deployment
- Use environment variables for sensitive data

### Server Management
- Monitor server logs for errors
- Use debug mode for troubleshooting
- Keep dependencies updated
- Test configurations regularly

### Integration
- Test with different MCP clients
- Document custom configurations
- Keep configurations minimal and focused
- Use templates for consistency

## Cross-References

- [MCP Module](../superprompts/mcp/README.md) - MCP server implementation
- [JSON Schemas](../schemas/README.md) - Configuration validation schemas
- [Available Prompts](available_prompts.md) - Complete list of prompts
- [Development](development.md) - Development setup
