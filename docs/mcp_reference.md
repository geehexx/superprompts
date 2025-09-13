# MCP Server Reference

Complete reference for the SuperPrompts MCP server.

## Overview

The SuperPrompts MCP server provides access to AI prompts through the Model Context Protocol (MCP). It exposes prompts as MCP prompts that can be used by AI assistants.

## Server Details

- **Name**: `superprompts`
- **Transport**: STDIO
- **Protocol**: MCP (Model Context Protocol)
- **Implementation**: FastMCP

## Available Prompts

### `repo_docs`

Repository Documentation Rebuilder prompt.

**Description**: Rebuilds and modernizes repository documentation safely with loss auditing and index rebuilding.

**Parameters**:
- `target_doc_types` (list[str]): Types of documentation to rebuild
- `output_format` (str): Output format for documentation
- `project_name` (str): Name of the project
- `include_examples` (bool): Whether to include examples

**Example Usage**:
```python
# Via MCP client
result = await mcp_client.call_tool("repo_docs", {
    "target_doc_types": ["README", "API"],
    "output_format": "markdown",
    "project_name": "MyProject"
})
```

### `cursor_rules`

Cursor Rules Generator prompt.

**Description**: Generates high-quality, non-duplicative Cursor rules tailored to the detected stack.

**Parameters**:
- `target_categories` (list[str]): Categories of rules to generate
- `rule_types` (list[str]): Types of rules to include
- `project_type` (str): Type of project (web, cli, library, etc.)
- `include_examples` (bool): Whether to include examples

**Example Usage**:
```python
# Via MCP client
result = await mcp_client.call_tool("cursor_rules", {
    "target_categories": ["python", "testing"],
    "rule_types": ["Always", "Auto Attached"],
    "project_type": "web"
})
```

## Server Functions

### `get_prompts_list()`

Get list of all available prompts with MCP-compliant metadata.

**Returns**: List of prompt metadata dictionaries

**Example**:
```python
prompts = get_prompts_list()
# Returns: [{"id": "repo_docs", "name": "Repository Documentation", ...}, ...]
```

### `get_prompt_by_id(prompt_id: str)`

Get a specific prompt by ID.

**Parameters**:
- `prompt_id` (str): ID of the prompt to retrieve

**Returns**: Prompt metadata dictionary or None if not found

**Example**:
```python
metadata = get_prompt_by_id("repo_docs")
# Returns: {"id": "repo_docs", "name": "Repository Documentation", ...}
```

### `get_completion_suggestions(prompt_id: str, argument_name: str | None = None)`

Get completion suggestions for prompt arguments.

**Parameters**:
- `prompt_id` (str): ID of the prompt
- `argument_name` (str | None): Specific argument name (optional)

**Returns**: List of completion suggestions

**Example**:
```python
suggestions = get_completion_suggestions("cursor_rules", "target_categories")
# Returns: [{"name": "python", "description": "Python-related rules"}, ...]
```

## Configuration

The MCP server can be configured through environment variables:

- `SUPERPROMPTS_LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)
- `PYTHONPATH`: Python path for module resolution

## Error Handling

The server handles errors gracefully:

- **Invalid prompt ID**: Returns appropriate error message
- **Invalid parameters**: Validates and reports parameter errors
- **Server errors**: Logs errors and returns user-friendly messages

## Development

### Adding New Prompts

1. Create a new prompt class inheriting from `BasePrompt`
2. Add the prompt to the `PROMPTS` dictionary
3. Register with `@mcp.prompt()` decorator
4. Update documentation

### Testing

```bash
# Test server startup
uv run python -m superprompts.mcp.server

# Test with debug logging
SUPERPROMPTS_LOG_LEVEL=DEBUG uv run python -m superprompts.mcp.server
```

## Integration

For detailed integration instructions, see the [MCP Configuration Guide](mcp_configuration.md).
