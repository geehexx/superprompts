# Environment Variables

Reference for environment variables used in the SuperPrompts project.

## Core Variables

### SUPERPROMPTS_LOG_LEVEL
Control logging verbosity level.

- **Type**: String
- **Default**: `INFO`
- **Values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

```bash
export SUPERPROMPTS_LOG_LEVEL=DEBUG
uv run superprompts --help
```

### SUPERPROMPTS_CONFIG_PATH
Specify custom configuration file path.

- **Type**: String
- **Default**: `None` (uses default locations)
- **Values**: Absolute or relative path to configuration file

```bash
export SUPERPROMPTS_CONFIG_PATH=/path/to/custom/config.json
uv run superprompts list-prompts
```

**Default locations:**
1. `./mcp.json` (current directory)
2. `~/.config/superprompts/mcp.json` (user config)
3. `/etc/superprompts/mcp.json` (system config)

## Development Variables

### PYTHONPATH
Add directories to Python module search path.

```bash
export PYTHONPATH=.
uv run python -c "import superprompts"
```

### PYTHONUNBUFFERED
Force stdout and stderr to be unbuffered.

```bash
export PYTHONUNBUFFERED=1
uv run superprompts-server
```

### PYTHONDONTWRITEBYTECODE
Prevent Python from writing .pyc files.

```bash
export PYTHONDONTWRITEBYTECODE=1
uv run superprompts list-prompts
```

## MCP Server Variables

### MCP_SERVER_HOST
Specify MCP server host address.

- **Type**: String
- **Default**: `localhost`
- **Values**: IP address or hostname

### MCP_SERVER_PORT
Specify MCP server port.

- **Type**: Integer
- **Default**: `8000`
- **Values**: Valid port number (1-65535)

### MCP_SERVER_DEBUG
Enable MCP server debug mode.

- **Type**: String
- **Default**: `False`
- **Values**: `True`, `False`, `1`, `0`

## Testing Variables

### PYTEST_CURRENT_TEST
Current test being executed (set by pytest).

### COVERAGE_RC
Specify coverage configuration file.

### NOX_SESSION
Current Nox session being executed.

## CI/CD Variables

### GITHUB_ACTIONS
Indicates if running in GitHub Actions.

### CI
Indicates if running in CI environment.

### GITHUB_WORKSPACE
GitHub Actions workspace directory.

## Usage Patterns

### Development Setup
```bash
export SUPERPROMPTS_LOG_LEVEL=DEBUG
export SUPERPROMPTS_CONFIG_PATH=./config/dev.json
export MCP_SERVER_DEBUG=True
export PYTHONUNBUFFERED=1
uv run superprompts-server
```

### Testing Setup
```bash
export SUPERPROMPTS_LOG_LEVEL=WARNING
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
uv run pytest tests/ -v
```

### Production Setup
```bash
export SUPERPROMPTS_LOG_LEVEL=ERROR
export SUPERPROMPTS_CONFIG_PATH=/etc/superprompts/mcp.json
export MCP_SERVER_HOST=0.0.0.0
export MCP_SERVER_PORT=8000
uv run superprompts-server
```

## Troubleshooting

### Common Issues

**Environment variable not set**
```bash
echo "Log level: ${SUPERPROMPTS_LOG_LEVEL:-not set}"
```

**Invalid environment variable value**
```bash
case "$SUPERPROMPTS_LOG_LEVEL" in
    DEBUG|INFO|WARNING|ERROR|CRITICAL)
        echo "Valid log level: $SUPERPROMPTS_LOG_LEVEL"
        ;;
    *)
        echo "Invalid log level: $SUPERPROMPTS_LOG_LEVEL"
        exit 1
        ;;
esac
```

### Debug Mode

```bash
# Enable debug output
SUPERPROMPTS_LOG_LEVEL=DEBUG uv run superprompts --help

# Check all variables
env | grep SUPERPROMPTS
env | grep MCP
env | grep PYTHON
```
