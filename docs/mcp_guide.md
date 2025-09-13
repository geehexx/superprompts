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

### Quick Start

```bash
# Create basic MCP configuration for Cursor
uv run superprompts config create

# Create configuration with specific templates
uv run superprompts config create --template superprompts --template github

# Create VS Code configuration
uv run superprompts config create --format vscode --template superprompts

# Validate existing configuration
uv run superprompts config validate mcp.json

# List available templates
uv run superprompts config templates
```

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
# Basic creation
uv run superprompts config create

# With specific format
uv run superprompts config create --format cursor

# With templates
uv run superprompts config create --template superprompts --template github

# Output to specific file
uv run superprompts config create --output my-config.json
```

#### Validate Configuration
```bash
# Basic validation
uv run superprompts config validate mcp.json

# With specific format
uv run superprompts config validate mcp.json --format cursor

# Auto-detect format
uv run superprompts config validate mcp.json --format auto
```

#### Convert Configuration
```bash
# Convert to VS Code format
uv run superprompts config convert mcp.json --format vscode

# Convert with output file
uv run superprompts config convert mcp.json --format vscode --output vscode-config.json
```

#### Merge Configurations
```bash
# Add server to existing configuration
uv run superprompts config merge existing.json --template github

# Merge multiple configurations
uv run superprompts config merge base.json additional.json --output merged.json
```

## Integration Examples

### Cursor IDE Integration

1. **Create Configuration**:
   ```bash
   uv run superprompts config create --format cursor --template superprompts
   ```

2. **Place Configuration**:
   - Move generated config to `.cursor/mcp.json`
   - Ensure absolute paths are correct
   - Don't commit to version control

3. **Restart Cursor**:
   - Close and reopen Cursor
   - Check MCP server status in settings

### VS Code Integration

1. **Create Configuration**:
   ```bash
   uv run superprompts config create --format vscode --template superprompts
   ```

2. **Add to Settings**:
   - Open VS Code settings
   - Add MCP configuration to settings.json
   - Restart VS Code

### Generic MCP Client Integration

1. **Create Configuration**:
   ```bash
   uv run superprompts config create --format generic --template superprompts
   ```

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
uv run superprompts config validate .cursor/mcp.json --verbose
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
