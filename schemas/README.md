# JSON Schemas

This directory contains JSON schemas for validation and type checking in the SuperPrompts project.

## Schemas

### `cursor_rule_frontmatter.schema.json`
Validates the frontmatter section of Cursor IDE rule files (`.cursor/rules/*.md`).

**Required Properties:**
- `description` (string) - Short description of the rule
- `type` (string) - Rule category (testing, documentation, code_quality, architecture, security, performance, general)
- `globs` (array of strings) - File patterns the rule applies to

**Optional Properties:**
- `ruleType` (string) - Cursor attach mode (Always, Auto Attached, Agent Requested, Manual)
- `alwaysApply` (boolean) - Whether rule always applies
- `when` (object) - Conditional application criteria
- `tags` (array of strings) - Rule tags for categorization
- `severity` (string) - Rule severity level (critical, high, medium, low, info)

### `mcp_server_definition.schema.json`
Validates MCP (Model Context Protocol) server configuration files for different IDE formats.

**Supported Formats:**
- **Cursor Format**: `{"mcpServers": {...}}`
- **VS Code Format**: `{"mcp": {"servers": {...}}}`
- **Generic Format**: `{"mcp": {"version": "...", "servers": {...}}}`

**Required Properties:**
- `command` (string) - Command to run the MCP server

**Optional Properties:**
- `args` (array of strings) - Command line arguments
- `env` (object) - Environment variables
- `cwd` (string) - Working directory
- `description` (string) - Server description
- `version` (string) - Server version (semantic versioning)

## Usage

### Validation
```bash
# Validate Cursor rules
uv run invoke validate --cursor-rules

# Validate MCP configurations
uv run superprompts config validate mcp.json
```

### Examples

#### Cursor Rule Frontmatter
```yaml
---
description: Use type hints for all function parameters
type: code_quality
globs: ["src/**/*.py"]
ruleType: Auto Attached
when:
  filesChanged: ["src/**/*.py"]
  languages: ["python"]
tags: ["python", "type-hints"]
severity: medium
---
```

#### MCP Server Configuration
```json
{
  "mcpServers": {
    "superprompts": {
      "command": "uv",
      "args": ["run", "python", "-m", "superprompts.mcp.server"],
      "description": "SuperPrompts MCP Server",
      "version": "1.0.0"
    }
  }
}
```

## Integration

- **Pre-commit Hooks**: Automatic validation on commit
- **CI/CD Pipeline**: Validation in GitHub Actions
- **Development Workflow**: Manual validation with `uv run invoke validate`

For detailed usage and troubleshooting, see the [main documentation](../docs/README.md).
