# API Reference

Complete reference for the SuperPrompts Python API, CLI commands, and MCP server tools.

## Python API

### Core Classes

#### `BasePrompt`

Abstract base class for all prompt implementations.

```python
from superprompts.prompts.base import BasePrompt

class BasePrompt(ABC):
    """Abstract base class for all prompts."""

    @abstractmethod
    def get_prompt(self, parameters: dict[str, Any]) -> str:
        """Generate prompt text with given parameters."""
        pass

    @abstractmethod
    def get_metadata(self) -> dict[str, Any]:
        """Get prompt metadata including parameters and phases."""
        pass

    def get_element(self, element_type: str, element_name: str) -> str | None:
        """Get a specific element from the prompt."""
        pass
```

#### `PromptCategory`

Enumeration of prompt categories.

```python
from superprompts.prompts.base import PromptCategory

class PromptCategory(Enum):
    DOCS = "docs"
    RULES = "rules"
    OTHER = "other"
```

#### `PromptMetadata`

Data class for prompt metadata.

```python
from superprompts.prompts.base import PromptMetadata

@dataclass
class PromptMetadata:
    id: str
    name: str
    title: str  # Required by MCP spec
    description: str
    category: PromptCategory
    version: str
    phases: list[str]
    arguments: list[PromptArgument]  # MCP-compliant arguments
    examples: list[dict[str, Any]]
    usage_instructions: str
    customization_options: list[str]

@dataclass
class PromptArgument:
    """MCP-compliant prompt argument definition."""
    name: str
    description: str
    required: bool = False
    type: str = "string"  # string, number, boolean, array, object
```

### Prompt Implementations

#### `RepoDocsPrompt`

Repository documentation rebuilder prompt.

```python
from superprompts.prompts.repo_docs import RepoDocsPrompt

prompt = RepoDocsPrompt()

# Generate prompt with parameters
text = prompt.get_prompt({
    "batch_size": 5,
    "target_doc_types": ["README", "API"],
    "confidence_threshold": 0.8
})

# Get metadata
metadata = prompt.get_metadata()
```

**Parameters:**
- `batch_size` (int): Number of files to process per batch (default: 5)
- `target_doc_types` (list[str]): Types of documentation to focus on
- `confidence_threshold` (float): Minimum confidence for generated content (0-1)

#### `CursorRulesPrompt`

Cursor IDE rules generator prompt.

```python
from superprompts.prompts.cursor_rules import CursorRulesPrompt

prompt = CursorRulesPrompt()

# Generate rules for specific categories
text = prompt.get_prompt({
    "target_categories": ["python", "web", "testing"],
    "rule_types": ["Auto Attached", "Manual"],
    "similarity_threshold": 0.7
})

# Get metadata
metadata = prompt.get_metadata()
```

**Parameters:**
- `target_categories` (list[str]): Technology categories to focus on
- `rule_types` (list[str]): Types of rules to generate
- `similarity_threshold` (float): Threshold for similarity detection (0-1)

### MCP Server

## MCP Server (Model Context Protocol)

The SuperPrompts MCP server provides MCP-compliant prompts and completion capabilities.

### Server Capabilities

The server declares the following MCP capabilities:
- `prompts` - Provides access to prompt definitions and generation
- `completions` - Provides argument autocompletion for prompts

### Prompt Handlers

#### `repo_docs_prompt_handler`

Repository Documentation Rebuilder prompt handler.

```python
from superprompts.mcp.server import repo_docs_prompt_handler

# Generate prompt without parameters
prompt_text = repo_docs_prompt_handler()

# Generate prompt with parameters
prompt_text = repo_docs_prompt_handler({
    "batch_size": 5,
    "target_doc_types": ["README", "API"],
    "confidence_threshold": 0.8,
    "include_examples": True,
    "output_format": "markdown"
})
```

**Parameters:**
- `parameters` (dict[str, Any] | None): Optional parameters to customize the prompt

**Returns:** Generated prompt text

#### `cursor_rules_prompt_handler`

Cursor Rules Generator prompt handler.

```python
from superprompts.mcp.server import cursor_rules_prompt_handler

# Generate prompt without parameters
prompt_text = cursor_rules_prompt_handler()

# Generate prompt with parameters
prompt_text = cursor_rules_prompt_handler({
    "target_categories": ["testing", "documentation"],
    "rule_types": ["Auto Attached", "Manual"],
    "similarity_threshold": 0.7,
    "confidence_threshold": 0.8,
    "max_rules_per_category": 5
})
```

**Parameters:**
- `parameters` (dict[str, Any] | None): Optional parameters to customize the prompt

**Returns:** Generated prompt text

### Utility Functions

#### `get_prompts_list`

Get list of all available prompts with MCP-compliant metadata.

```python
from superprompts.mcp.server import get_prompts_list

prompts = get_prompts_list()
# Returns list of prompts with id, name, title, description, and arguments
```

**Returns:** List of prompt metadata dictionaries

#### `get_prompt_by_id`

Get a specific prompt by ID.

```python
from superprompts.mcp.server import get_prompt_by_id

metadata = get_prompt_by_id("repo_docs")
# Returns full metadata for the prompt
```

**Parameters:**
- `prompt_id` (str): ID of the prompt to retrieve

**Returns:** Prompt metadata dictionary or None

#### `get_completion_suggestions`

Get completion suggestions for prompt arguments.

```python
from superprompts.mcp.server import get_completion_suggestions

# Get all available arguments for a prompt
suggestions = get_completion_suggestions("repo_docs")

# Get suggestions for a specific argument
suggestions = get_completion_suggestions("cursor_rules", "target_categories")
```

**Parameters:**
- `prompt_id` (str): ID of the prompt
- `argument_name` (str | None): Specific argument name (optional)

**Returns:** List of completion suggestions

### Configuration Management

For detailed MCP server configuration instructions, see the [MCP Configuration Guide](mcp_configuration.md).

### CLI Commands

#### `superprompts list-prompts`

List available prompts.

```bash
# List all prompts
superprompts list-prompts

# List by category
superprompts list-prompts --category docs
superprompts list-prompts --category rules
```

#### `superprompts get-prompt`

Generate a specific prompt.

```bash
# Basic usage
superprompts get-prompt repo_docs

# With parameters
superprompts get-prompt cursor_rules --parameters '{"target_categories": ["python"]}'

# Save to file
superprompts get-prompt repo_docs --output my_prompt.txt
```

#### `superprompts metadata`

Get prompt metadata.

```bash
superprompts metadata repo_docs
superprompts metadata cursor_rules
```

#### `superprompts compose`

Compose custom prompts.

```bash
# Basic composition
superprompts compose repo_docs

# With additions
superprompts compose repo_docs --additions '[{"source_prompt_id": "cursor_rules", "element_type": "section", "element_name": "Quality Standards"}]'

# With customizations
superprompts compose repo_docs --customizations '{"project_name": "MyProject"}'
```

#### `superprompts config`

Manage MCP configurations.

```bash
# Create configuration
superprompts config create --template superprompts

# Create with multiple templates
superprompts config create --template superprompts --template github

# Create for specific format
superprompts config create --format vscode --template superprompts

# Validate configuration
superprompts config validate mcp.json

# Convert between formats
superprompts config convert mcp.json --format vscode

# List available templates
superprompts config templates
```

## Error Handling

### Common Exceptions

#### `ValueError`
Raised for invalid prompt IDs or parameters.

```python
try:
    prompt = await get_prompt("invalid_id")
except ValueError as e:
    print(f"Invalid prompt ID: {e}")
```

#### `FileNotFoundError`
Raised when configuration files are not found.

```python
try:
    config = generator.load_existing_config("missing.json")
except FileNotFoundError:
    print("Configuration file not found")
```

#### `ValidationError`
Raised by Pydantic for invalid configuration data.

```python
from pydantic import ValidationError

try:
    config = MCPServerConfig(**invalid_data)
except ValidationError as e:
    print(f"Configuration validation failed: {e}")
```

## Type Hints

All functions and classes include comprehensive type hints:

```python
from typing import Any, Dict, List, Optional, Union

def get_prompt(
    prompt_id: str,
    parameters: Optional[Dict[str, Any]] = None
) -> str:
    """Generate a prompt with optional parameters."""
    pass
```

## Async/Await Support

All MCP server functions are async:

```python
import asyncio

async def main():
    prompts = await list_prompts()
    prompt_text = await get_prompt("repo_docs")
    metadata = await get_prompt_metadata("cursor_rules")

# Run async code
asyncio.run(main())
```

## Examples

### Basic Usage

```python
from superprompts.prompts.repo_docs import RepoDocsPrompt

# Create prompt instance
prompt = RepoDocsPrompt()

# Generate documentation prompt
text = prompt.get_prompt({
    "batch_size": 3,
    "target_doc_types": ["README", "API", "CHANGELOG"]
})

print(text)
```

### MCP Server Integration

```python
import asyncio
from superprompts.mcp.server import list_prompts, get_prompt

async def main():
    # List available prompts
    prompts = await list_prompts()
    print(f"Available prompts: {[p['id'] for p in prompts]}")

    # Generate a prompt
    prompt_text = await get_prompt("cursor_rules", {
        "target_categories": ["python", "testing"]
    })
    print(prompt_text)

asyncio.run(main())
```

### Configuration Management

For detailed MCP server configuration instructions, see the [MCP Configuration Guide](mcp_configuration.md).

## Cross-References

- [Available Prompts](available_prompts.md) - Complete list of available prompts
- [MCP Guide](mcp_guide.md) - Detailed MCP server usage
- [Architecture](architecture.md) - System architecture overview
- [Development](development.md) - Development setup and workflow
