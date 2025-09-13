# CLI Reference

Complete reference for SuperPrompts CLI commands.

## Overview

The SuperPrompts CLI provides commands to manage and interact with AI prompts.

## Commands

### `superprompts list-prompts`

List all available prompts.

```bash
# List all prompts
superprompts list-prompts

# List by category
superprompts list-prompts --category docs
superprompts list-prompts --category rules
```

**Options:**
- `--category, -c`: Filter prompts by category (docs, rules, all)

### `superprompts get-prompt`

Get a specific prompt by ID.

```bash
# Basic usage
superprompts get-prompt repo_docs

# With parameters
superprompts get-prompt cursor_rules --parameters '{"target_categories": ["python"]}'

# Save to file
superprompts get-prompt repo_docs --output my_prompt.txt
```

**Arguments:**
- `prompt_id`: ID of the prompt to retrieve

**Options:**
- `--parameters, -p`: JSON string of parameters to pass to the prompt
- `--output, -o`: Output file path (default: stdout)

### `superprompts metadata`

Get detailed metadata about a specific prompt.

```bash
superprompts metadata repo_docs
superprompts metadata cursor_rules
```

**Arguments:**
- `prompt_id`: ID of the prompt to get metadata for

## Examples

### Basic Usage

```bash
# List all available prompts
superprompts list-prompts

# Get a specific prompt
superprompts get-prompt repo_docs

# Get prompt with parameters
superprompts get-prompt cursor_rules --parameters '{"target_categories": ["python", "testing"]}'

# Save prompt to file
superprompts get-prompt repo_docs --output documentation_prompt.txt
```

### Advanced Usage

```bash
# List only documentation prompts
superprompts list-prompts --category docs

# Get prompt metadata
superprompts metadata cursor_rules

# Generate prompt with custom parameters
superprompts get-prompt cursor_rules --parameters '{
  "target_categories": ["python", "testing"],
  "rule_types": ["Always", "Auto Attached"]
}'
```

## Error Handling

The CLI provides clear error messages for common issues:

- **Invalid prompt ID**: Shows available prompts
- **Invalid parameters**: Validates JSON and parameter types
- **File errors**: Clear messages for permission and path issues

## Exit Codes

- `0`: Success
- `1`: General error (invalid arguments, file errors, etc.)
- `2`: Prompt not found
- `3`: Invalid parameters
