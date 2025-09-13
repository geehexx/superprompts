# MCP Configuration Management Guide

## Overview

The SuperPrompts CLI provides comprehensive tools for creating, managing, and validating MCP (Model Context Protocol) server configurations. This guide covers how to use these tools to set up MCP servers for various AI tools and IDEs.

## Features

- **Multi-format Support**: Generate configurations for Cursor, VS Code, and generic MCP clients
- **Template System**: Pre-configured templates for popular MCP servers
- **Configuration Validation**: Ensure your configurations are valid and properly formatted
- **Format Conversion**: Convert between different MCP configuration formats
- **Merge Capabilities**: Add new servers to existing configurations without overwriting

## Quick Start

### Basic Usage

```bash
# Create a basic MCP configuration for Cursor
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

## Configuration Formats

### Cursor Format (`.cursor/mcp.json`)

The Cursor IDE uses a specific format for MCP server configurations. **Important**: The configuration file must be placed in `.cursor/mcp.json` (not in the project root) and should not be committed to version control as it contains machine-specific paths.

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

**Setup Instructions:**
1. Create the `.cursor` directory in your project root
2. Place the `mcp.json` file inside `.cursor/mcp.json`
3. Update the `cwd` path to your actual project directory
4. Add `.cursor/mcp.json` to your `.gitignore` file
5. Restart Cursor IDE

### VS Code Format (`.vscode/mcp.json`)

VS Code uses a nested structure for MCP configurations:

```json
{
  "mcp": {
    "servers": {
      "superprompts": {
        "command": "uv",
        "args": ["run", "python", "-m", "superprompts.mcp.server"],
        "description": "SuperPrompts MCP Server - Access to AI prompt collection"
      }
    }
  }
}
```

### Generic Format (`mcp_config.json`)

A comprehensive format that includes metadata:

```json
{
  "mcp": {
    "version": "1.0.0",
    "servers": {
      "superprompts": {
        "name": "superprompts",
        "command": "uv",
        "args": ["run", "python", "-m", "superprompts.mcp.server"],
        "description": "SuperPrompts MCP Server - Access to AI prompt collection",
        "version": "1.0.0"
      }
    }
  }
}
```

## CLI Commands

### `config create`

Create or update MCP server configurations.

**Options:**
- `--format, -f`: Configuration format (`cursor`, `vscode`, `generic`)
- `--output, -o`: Output file path (auto-determined if not specified)
- `--template, -t`: Server templates to include (can be used multiple times)
- `--merge`: Merge with existing configuration instead of overwriting
- `--dry-run`: Show what would be generated without writing files

**Examples:**

```bash
# Create basic Cursor configuration
uv run superprompts config create

# Create with multiple servers
uv run superprompts config create --template superprompts --template github --template filesystem

# Create VS Code configuration
uv run superprompts config create --format vscode --template superprompts

# Merge with existing configuration
uv run superprompts config create --merge --template github

# Preview without saving
uv run superprompts config create --dry-run --template superprompts
```

### `config validate`

Validate existing MCP configuration files.

**Options:**
- `--format, -f`: Configuration format (`cursor`, `vscode`, `generic`, `auto`)

**Examples:**

```bash
# Validate with auto-detection
uv run superprompts config validate mcp.json

# Validate specific format
uv run superprompts config validate .vscode/mcp.json --format vscode

# Validate generic configuration
uv run superprompts config validate mcp_config.json --format generic
```

### `config templates`

List available server configuration templates.

**Examples:**

```bash
# List all available templates
uv run superprompts config templates
```

### `config convert`

Convert MCP configurations between different formats.

**Options:**
- `--format, -f`: Target format (`cursor`, `vscode`, `generic`, `auto`)

**Examples:**

```bash
# Convert Cursor config to VS Code format
uv run superprompts config convert mcp.json --format vscode

# Convert with auto-detection
uv run superprompts config convert .vscode/mcp.json --format cursor
```

## Available Templates

### SuperPrompts Server

The built-in SuperPrompts MCP server:

```bash
uv run superprompts config create --template superprompts
```

**Configuration:**
- **Command**: `uv run python -m superprompts.mcp.server`
- **Description**: SuperPrompts MCP Server - Access to AI prompt collection
- **Version**: 1.0.0

### GitHub Server

GitHub MCP server for repository operations:

```bash
uv run superprompts config create --template github
```

**Configuration:**
- **Command**: `npx -y github-mcp-server`
- **Description**: GitHub MCP Server - Repository operations
- **Version**: 1.0.0

### Filesystem Server

Filesystem MCP server for file operations:

```bash
uv run superprompts config create --template filesystem
```

**Configuration:**
- **Command**: `npx -y @modelcontextprotocol/server-filesystem /path/to/your/project`
- **Description**: Filesystem MCP Server - File operations
- **Version**: 1.0.0

## Advanced Usage

### Custom Server Configurations

You can create custom server configurations by modifying the generated files or using the API programmatically:

```python
from superprompts.mcp.config import MCPConfigGenerator, MCPServerConfig

# Create custom server configuration
custom_server = MCPServerConfig(
    name="my-custom-server",
    command="python",
    args=["-m", "my.custom.server"],
    env={"CUSTOM_VAR": "value"},
    cwd="/path/to/working/directory",
    description="My custom MCP server",
    version="1.0.0"
)

# Generate configuration
generator = MCPConfigGenerator()
servers = {"my-custom": custom_server}
config = generator.generate_cursor_config(servers)

# Save configuration
output_path = generator.save_config(config, "cursor")
```

### Environment Variables

You can set environment variables for MCP servers:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my.server"],
      "env": {
        "API_KEY": "your-api-key",
        "DEBUG": "true"
      }
    }
  }
}
```

### Working Directory

Specify a working directory for MCP servers:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my.server"],
      "cwd": "/path/to/project"
    }
  }
}
```

## Integration with AI Tools

### Cursor IDE

1. Create the `.cursor` directory in your project root:
   ```bash
   mkdir -p .cursor
   ```

2. Create MCP configuration file `.cursor/mcp.json`:
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

3. Update the `cwd` path to your actual project directory

4. Add `.cursor/mcp.json` to your `.gitignore` file:
   ```
   # Cursor MCP configuration (machine-specific)
   .cursor/mcp.json
   ```

5. Restart Cursor IDE

6. The MCP servers will be available in Cursor's AI features

### VS Code

1. Create MCP configuration:
   ```bash
   uv run superprompts config create --format vscode
   ```

2. The configuration will be saved to `.vscode/mcp.json`

3. Install the MCP extension for VS Code

4. Restart VS Code

### Other MCP Clients

1. Create generic configuration:
   ```bash
   uv run superprompts config create --format generic
   ```

2. Use the generated `mcp_config.json` with your MCP client

## Troubleshooting

### Common Issues

#### Configuration Not Loading

**Problem**: MCP servers not appearing in your AI tool.

**Solutions**:
1. Validate your configuration:
   ```bash
   uv run superprompts config validate mcp.json
   ```

2. Check file location:
   - Cursor: `.cursor/mcp.json` in project root (not `mcp.json`)
   - VS Code: `.vscode/mcp.json` in project root

3. Restart your AI tool/IDE

#### Command Not Found

**Problem**: MCP server command not found.

**Solutions**:
1. Ensure the command is available in your PATH
2. Use absolute paths for commands
3. Check that required dependencies are installed

#### Permission Issues

**Problem**: Permission denied when running MCP servers.

**Solutions**:
1. Ensure the command is executable
2. Check file permissions
3. Run with appropriate user permissions

### Debugging

#### Enable Debug Logging

Set environment variables for detailed logging:

```bash
export SUPERPROMPTS_LOG_LEVEL=DEBUG
uv run superprompts config create --template superprompts
```

#### Validate Configuration

Always validate your configuration before using:

```bash
uv run superprompts config validate mcp.json
```

#### Test Server Connection

Test if your MCP server is working:

```bash
# Test SuperPrompts server
uv run superprompts tools

# Test specific tool
uv run superprompts call-tool list_prompts '{"category": "all"}'
```

## Best Practices

### Configuration Management

1. **Version Control**: Commit your MCP configurations to version control
2. **Environment-Specific**: Use different configurations for different environments
3. **Documentation**: Document custom server configurations
4. **Validation**: Always validate configurations before deployment

### Server Selection

1. **Minimal Set**: Only include servers you actually need
2. **Performance**: Consider the performance impact of multiple servers
3. **Compatibility**: Ensure servers are compatible with your AI tool
4. **Updates**: Keep server configurations up to date

### Security

1. **Credentials**: Use environment variables for sensitive information
2. **Permissions**: Limit server permissions to necessary operations
3. **Validation**: Validate all server configurations
4. **Monitoring**: Monitor server behavior and logs

## Schema Reference

The MCP configuration follows a JSON schema for validation. The schema is available at:

- **Schema File**: `schemas/mcp_server_definition.schema.json`
- **Schema ID**: `https://superprompts.dev/schemas/mcp_server_definition.schema.json`

### Schema Validation

You can validate configurations against the schema:

```bash
# Using the CLI
uv run superprompts config validate mcp.json

# Using a JSON schema validator
npx ajv validate -s schemas/mcp_server_definition.schema.json -d mcp.json
```

## Examples

### Complete Workflow

```bash
# 1. List available templates
uv run superprompts config templates

# 2. Create configuration with multiple servers
uv run superprompts config create \
  --template superprompts \
  --template github \
  --template filesystem

# 3. Validate the configuration
uv run superprompts config validate mcp.json

# 4. Convert to VS Code format
uv run superprompts config convert mcp.json --format vscode

# 5. Validate VS Code configuration
uv run superprompts config validate .vscode/mcp.json --format vscode
```

### Custom Server Setup

```bash
# 1. Create base configuration
uv run superprompts config create --template superprompts

# 2. Edit mcp.json to add custom server
# {
#   "mcpServers": {
#     "superprompts": { ... },
#     "my-custom": {
#       "command": "python",
#       "args": ["-m", "my.custom.server"],
#       "env": {"API_KEY": "secret"},
#       "description": "My custom server"
#     }
#   }
# }

# 3. Validate updated configuration
uv run superprompts config validate mcp.json
```

## Cross-References

- **[MCP Server Guide](mcp_server_guide.md)** - Using the MCP server and CLI tools
- **[Development Guide](development_guide.md)** - Development setup and workflows
- **[Troubleshooting Guide](troubleshooting_guide.md)** - Common issues and solutions
- **[Available Prompts](available_prompts.md)** - List of available prompts through MCP
