# MCP Server Configuration Guide

This guide explains how to configure MCP (Model Context Protocol) servers for use with AI tools like Cursor, VS Code, and other MCP-compatible applications.

## Overview

The Model Context Protocol (MCP) is a standard for connecting AI assistants to external tools and data sources. MCP servers provide tools and resources that AI assistants can use to perform tasks.

For detailed information about MCP, visit the [official MCP documentation](https://modelcontextprotocol.io/).

## Configuration Formats

MCP servers can be configured in different formats depending on your AI tool:

### Cursor IDE Format

For Cursor IDE, create a `mcp.json` file in your project root:

```json
{
  "mcpServers": {
    "superprompts": {
      "command": "uv",
      "args": ["run", "python", "-m", "superprompts.mcp.server"],
      "env": {
        "PYTHONPATH": "/path/to/your/project"
      },
      "cwd": "/path/to/your/project"
    }
  }
}
```

### VS Code Format

For VS Code with MCP extension, create `.vscode/mcp.json`:

```json
{
  "mcp": {
    "servers": {
      "superprompts": {
        "command": "uv",
        "args": ["run", "python", "-m", "superprompts.mcp.server"],
        "env": {
          "PYTHONPATH": "/path/to/your/project"
        },
        "cwd": "/path/to/your/project"
      }
    }
  }
}
```

### Generic MCP Format

For other MCP-compatible tools:

```json
{
  "mcp": {
    "version": "1.0.0",
    "servers": {
      "superprompts": {
        "name": "superprompts",
        "command": "uv",
        "args": ["run", "python", "-m", "superprompts.mcp.server"],
        "env": {
          "PYTHONPATH": "/path/to/your/project"
        },
        "cwd": "/path/to/your/project",
        "description": "SuperPrompts MCP Server - Access to AI prompt collection",
        "version": "1.0.0"
      }
    }
  }
}
```

## SuperPrompts MCP Server

### Installation

1. Install SuperPrompts:
   ```bash
   pip install superprompts
   # or
   uv add superprompts
   ```

2. Verify installation:
   ```bash
   uv run python -m superprompts.mcp.server --help
   ```

### Configuration

The SuperPrompts MCP server provides access to a collection of high-quality AI prompts. Here's how to configure it:

#### Basic Configuration

```json
{
  "mcpServers": {
    "superprompts": {
      "command": "uv",
      "args": ["run", "python", "-m", "superprompts.mcp.server"]
    }
  }
}
```

#### With Environment Variables

```json
{
  "mcpServers": {
    "superprompts": {
      "command": "uv",
      "args": ["run", "python", "-m", "superprompts.mcp.server"],
      "env": {
        "SUPERPROMPTS_LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

#### With Working Directory

```json
{
  "mcpServers": {
    "superprompts": {
      "command": "uv",
      "args": ["run", "python", "-m", "superprompts.mcp.server"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

### Available Tools

The SuperPrompts MCP server provides these tools:

- `list_prompts` - List all available prompts
- `get_prompt` - Get a specific prompt with parameters
- `get_prompt_metadata` - Get prompt metadata
- `compose_prompt` - Compose custom prompts

## Other MCP Servers

### GitHub MCP Server

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "github-mcp-server"],
      "env": {
        "GITHUB_TOKEN": "your_github_token"
      }
    }
  }
}
```

### Filesystem MCP Server

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/your/project"]
    }
  }
}
```

### Database MCP Server

```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:password@localhost/dbname"
      }
    }
  }
}
```

## Configuration Best Practices

### 1. Use Absolute Paths

Always use absolute paths for commands and working directories:

```json
{
  "mcpServers": {
    "superprompts": {
      "command": "/usr/local/bin/uv",
      "args": ["run", "python", "-m", "superprompts.mcp.server"],
      "cwd": "/home/user/my-project"
    }
  }
}
```

### 2. Set Environment Variables

Use environment variables for sensitive data:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "github-mcp-server"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### 3. Validate Configuration

Test your configuration by running the server manually:

```bash
# Test SuperPrompts server
uv run python -m superprompts.mcp.server

# Test other servers
npx -y github-mcp-server
```

### 4. Use Version Pinning

Pin specific versions for reproducible setups:

```json
{
  "mcpServers": {
    "superprompts": {
      "command": "uv",
      "args": ["run", "--python", "3.11", "python", "-m", "superprompts.mcp.server"]
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Server not starting**: Check that the command and arguments are correct
2. **Permission denied**: Ensure the command is executable and paths are accessible
3. **Environment variables not set**: Verify environment variables are properly configured
4. **Working directory issues**: Use absolute paths for the `cwd` field

### Debug Mode

Enable debug logging to troubleshoot issues:

```json
{
  "mcpServers": {
    "superprompts": {
      "command": "uv",
      "args": ["run", "python", "-m", "superprompts.mcp.server"],
      "env": {
        "SUPERPROMPTS_LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

### Testing Configuration

Test your MCP server configuration:

```bash
# Test server startup
uv run python -m superprompts.mcp.server

# Test with specific environment
SUPERPROMPTS_LOG_LEVEL=DEBUG uv run python -m superprompts.mcp.server
```

## Resources

- [Official MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP Server Examples](https://github.com/modelcontextprotocol/servers)
- [SuperPrompts GitHub Repository](https://github.com/geehexx/superprompts)

## Support

For issues with SuperPrompts MCP server:

1. Check the [troubleshooting section](#troubleshooting) above
2. Review the [official MCP documentation](https://modelcontextprotocol.io/)
3. Open an issue on the [SuperPrompts GitHub repository](https://github.com/geehexx/superprompts)
