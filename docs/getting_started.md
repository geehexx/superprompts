# Getting Started with SuperPrompts

Welcome to SuperPrompts! This guide will help you get up and running quickly with our collection of high-quality AI prompts.

## What is SuperPrompts?

SuperPrompts is a collection of reusable AI prompts designed for practical use across diverse projects and tasks. It includes:

- **Repository Documentation Rebuilder**: Systematically rebuild and modernize documentation with safety checks
- **Cursor Rules Generator**: Create tailored Cursor IDE rules for your specific technology stack
- **MCP Server Integration**: Use prompts directly in AI tools like Cursor IDE
- **CLI Tools**: Command-line interface for all prompt functionality

## Quick Installation

### Prerequisites
- Python 3.10 or higher
- uv (recommended) or pip

### Install from Source
```bash
# Clone the repository
git clone https://github.com/geehexx/superprompts.git
cd superprompts

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --dev

# Verify installation
uv run superprompts --help
```

### Install from PyPI (when available)
```bash
pip install superprompts
```

## Your First Prompt

### 1. List Available Prompts
```bash
uv run superprompts list-prompts
```

### 2. Get a Simple Prompt
```bash
# Get the repository documentation prompt
uv run superprompts get-prompt repo_docs

# Get cursor rules prompt
uv run superprompts get-prompt cursor_rules
```

### 3. Use Prompts with Parameters
```bash
# Generate testing-focused cursor rules
uv run superprompts get-prompt cursor_rules --parameters '{
  "target_categories": ["testing"],
  "rule_types": ["Auto Attached"]
}'

# Generate API documentation
uv run superprompts get-prompt repo_docs --parameters '{
  "target_doc_types": ["API"],
  "include_examples": true
}'
```

## Using with Cursor IDE

### 1. Start the MCP Server
```bash
uv run superprompts-server
```

### 2. Configure Cursor IDE
Create `.cursor/mcp.json` in your project:
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

### 3. Use in Cursor
- Access prompts through Cursor's MCP integration
- Use `repo_docs` and `cursor_rules` prompts directly in your IDE

## Common Use Cases

### 1. Setting Up Cursor Rules for a New Project

```bash
# Generate comprehensive rules for a Python project
uv run superprompts get-prompt cursor_rules --parameters '{
  "target_categories": ["python", "testing", "documentation"],
  "rule_types": ["Auto Attached", "Manual"],
  "max_rules_per_category": 3
}'
```

### 2. Rebuilding Project Documentation

```bash
# Generate comprehensive documentation
uv run superprompts get-prompt repo_docs --parameters '{
  "target_doc_types": ["README", "API", "guides"],
  "batch_size": 3,
  "include_examples": true
}'
```

### 3. Creating API Documentation

```bash
# Focus on API documentation
uv run superprompts get-prompt repo_docs --parameters '{
  "target_doc_types": ["API"],
  "include_examples": true,
  "output_format": "markdown"
}'
```

## Understanding Prompt Parameters

### Repository Documentation Rebuilder (`repo_docs`)

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `target_doc_types` | array | Types of docs to generate | `["README", "API", "guides"]` |
| `batch_size` | number | Files per batch (1-10) | `3` |
| `include_examples` | boolean | Include code examples | `true` |
| `output_format` | string | Output format | `"markdown"` |

### Cursor Rules Generator (`cursor_rules`)

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `target_categories` | array | Rule categories | `["python", "testing"]` |
| `rule_types` | array | Types of rules | `["Auto Attached", "Manual"]` |
| `max_rules_per_category` | number | Max rules per category | `5` |
| `similarity_threshold` | number | Deduplication threshold | `0.7` |

## Next Steps

### For Users
1. **Explore Prompts**: Check [Available Prompts](available_prompts.md) for detailed usage
2. **Learn Techniques**: Read [AI Prompting Best Practices](ai_prompting_best_practices.md)
3. **Customize**: Learn about parameters and customization options
4. **Integrate**: Set up MCP server for your preferred AI tool

### For Developers
1. **Development Setup**: Follow the [Development Guide](development.md)
2. **Contributing**: Read the [Contributing Guide](contributing_guide.md)
3. **API Reference**: Explore the [Python API](api.md)
4. **Troubleshooting**: Check the [Troubleshooting Guide](troubleshooting.md)

## Getting Help

### Documentation
- **Quick Reference**: [Available Prompts](available_prompts.md)
- **Complete Setup**: [Installation Guide](installation_guide.md)
- **MCP Integration**: [MCP Configuration Guide](mcp_configuration.md)
- **CLI Commands**: [CLI Reference](cli_reference.md)

### Community
- **Issues**: Report bugs on [GitHub Issues](https://github.com/geehexx/superprompts/issues)
- **Discussions**: Ask questions in [GitHub Discussions](https://github.com/geehexx/superprompts/discussions)
- **Pull Requests**: Contribute improvements

## Examples

### Basic Workflow
```bash
# 1. List available prompts
uv run superprompts list-prompts

# 2. Get prompt metadata
uv run superprompts metadata repo_docs

# 3. Generate a prompt
uv run superprompts get-prompt cursor_rules --parameters '{
  "target_categories": ["python", "testing"],
  "rule_types": ["Auto Attached"]
}'

# 4. Save to file
uv run superprompts get-prompt repo_docs --output my_docs_prompt.txt
```

### Advanced Usage
```bash
# Generate comprehensive documentation with custom parameters
uv run superprompts get-prompt repo_docs --parameters '{
  "target_doc_types": ["README", "API", "guides", "architecture"],
  "batch_size": 5,
  "include_examples": true,
  "confidence_threshold": 0.8
}'

# Generate focused cursor rules
uv run superprompts get-prompt cursor_rules --parameters '{
  "target_categories": ["testing", "documentation"],
  "rule_types": ["Auto Attached"],
  "max_rules_per_category": 3,
  "similarity_threshold": 0.8
}'
```

### MCP Server Integration
```bash
# Start server in background
uv run superprompts-server &

# Use with MCP client
# (Configuration depends on your MCP client)
```

## Tips for Success

### 1. Start Simple
- Begin with basic prompts without parameters
- Gradually add parameters as you understand the system
- Use small batch sizes initially

### 2. Iterate and Refine
- Generate prompts, review results, and adjust parameters
- Use the confidence scores to guide your decisions
- Save successful parameter combinations for reuse

### 3. Customize for Your Needs
- Adjust parameters based on your project type
- Use appropriate categories for your technology stack
- Include examples when they add value

### 4. Integrate with Your Workflow
- Set up MCP server for seamless AI tool integration
- Use CLI commands in scripts and automation
- Create templates for common use cases

## Troubleshooting

### Common Issues
- **Command not found**: Ensure you're using `uv run superprompts`
- **Permission errors**: Check file permissions and paths
- **Parameter errors**: Validate JSON syntax in parameters
- **Server issues**: Check MCP server configuration

### Getting Help
- Check the [Troubleshooting Guide](troubleshooting.md)
- Review error messages carefully
- Search existing issues on GitHub
- Ask questions in community discussions

That's it! You're ready to start using SuperPrompts effectively. 🚀

For more detailed information, explore the comprehensive guides in the [docs/](docs/) directory.
