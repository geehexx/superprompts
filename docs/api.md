# Python API Reference

Complete reference for the SuperPrompts Python API.

## Core Classes

### `BasePrompt`

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

### `PromptCategory`

Enumeration of prompt categories.

```python
from superprompts.prompts.base import PromptCategory

class PromptCategory(Enum):
    DOCS = "docs"
    RULES = "rules"
    OTHER = "other"
```

### `PromptMetadata`

Data class for prompt metadata.

```python
from superprompts.prompts.base import PromptMetadata

@dataclass
class PromptMetadata:
    id: str
    name: str
    title: str
    description: str
    category: PromptCategory
    phases: list[str]
    arguments: list[dict[str, Any]]
```

## Prompt Implementations

### `RepoDocsPrompt`

Repository Documentation Rebuilder prompt.

```python
from superprompts.prompts.repo_docs import RepoDocsPrompt

prompt = RepoDocsPrompt()
result = prompt.get_prompt({
    "target_doc_types": ["README", "API"],
    "output_format": "markdown"
})
```

**Parameters**:
- `target_doc_types` (list[str]): Types of documentation to rebuild
- `output_format` (str): Output format for documentation
- `project_name` (str): Name of the project
- `include_examples` (bool): Whether to include examples

### `CursorRulesPrompt`

Cursor Rules Generator prompt.

```python
from superprompts.prompts.cursor_rules import CursorRulesPrompt

prompt = CursorRulesPrompt()
result = prompt.get_prompt({
    "target_categories": ["python", "testing"],
    "rule_types": ["Always", "Auto Attached"]
})
```

**Parameters**:
- `target_categories` (list[str]): Categories of rules to generate
- `rule_types` (list[str]): Types of rules to include
- `project_type` (str): Type of project (web, cli, library, etc.)
- `include_examples` (bool): Whether to include examples

## MCP Server Functions

### `get_prompts_list()`

Get list of all available prompts with MCP-compliant metadata.

```python
from superprompts.mcp.server import get_prompts_list

prompts = get_prompts_list()
# Returns: [{"id": "repo_docs", "name": "Repository Documentation", ...}, ...]
```

### `get_prompt_by_id(prompt_id: str)`

Get a specific prompt by ID.

```python
from superprompts.mcp.server import get_prompt_by_id

metadata = get_prompt_by_id("repo_docs")
# Returns: {"id": "repo_docs", "name": "Repository Documentation", ...}
```

### `get_completion_suggestions(prompt_id: str, argument_name: str | None = None)`

Get completion suggestions for prompt arguments.

```python
from superprompts.mcp.server import get_completion_suggestions

suggestions = get_completion_suggestions("cursor_rules", "target_categories")
# Returns: [{"name": "python", "description": "Python-related rules"}, ...]
```

## Error Handling

### Common Exceptions

#### `ValueError`
Raised for invalid prompt parameters.

```python
try:
    prompt = RepoDocsPrompt()
    result = prompt.get_prompt({"invalid_param": "value"})
except ValueError as e:
    print(f"Invalid parameter: {e}")
```

#### `FileNotFoundError`
Raised when prompt files are not found.

```python
try:
    prompt = RepoDocsPrompt()
    result = prompt.get_prompt({})
except FileNotFoundError as e:
    print(f"Prompt file not found: {e}")
```

#### `ValidationError`
Raised by Pydantic for invalid prompt data.

```python
from pydantic import ValidationError

try:
    prompt = RepoDocsPrompt(**invalid_data)
except ValidationError as e:
    print(f"Prompt validation failed: {e}")
```

## Type Hints

All functions and classes include comprehensive type hints:

```python
from typing import Any, Dict, List, Optional, Union

def get_prompt(
    prompt_id: str,
    parameters: Optional[Dict[str, Any]] = None
) -> str:
    """Get a specific prompt with parameters."""
    pass
```

## Usage Examples

### Basic Usage

```python
from superprompts.prompts.repo_docs import RepoDocsPrompt

# Create prompt instance
prompt = RepoDocsPrompt()

# Generate prompt with parameters
result = prompt.get_prompt({
    "target_doc_types": ["README", "API"],
    "output_format": "markdown",
    "project_name": "MyProject"
})

print(result)
```

### Advanced Usage

```python
from superprompts.prompts.cursor_rules import CursorRulesPrompt

# Create prompt instance
prompt = CursorRulesPrompt()

# Get metadata
metadata = prompt.get_metadata()
print(f"Available arguments: {[arg['name'] for arg in metadata['arguments']]}")

# Generate prompt with all parameters
result = prompt.get_prompt({
    "target_categories": ["python", "testing", "security"],
    "rule_types": ["Always", "Auto Attached"],
    "project_type": "web",
    "include_examples": True
})
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

## Cross-References

- [CLI Reference](cli_reference.md) - CLI commands
- [MCP Server Reference](mcp_reference.md) - MCP server details
- [Available Prompts](available_prompts.md) - Complete list of available prompts
- [MCP Configuration Guide](mcp_configuration.md) - MCP server configuration
- [Architecture](architecture.md) - System architecture overview
- [Development](development.md) - Development setup and workflow
