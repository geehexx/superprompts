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
    name: str
    description: str
    category: PromptCategory
    phases: list[str]
    parameters: list[str]
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

#### `list_prompts`

List all available prompts with metadata.

```python
from superprompts.mcp.server import list_prompts

# List all prompts
prompts = await list_prompts()

# List by category
docs_prompts = await list_prompts(category="docs")
rules_prompts = await list_prompts(category="rules")
```

**Returns:** List of prompt metadata dictionaries

#### `get_prompt`

Generate a specific prompt with optional parameters.

```python
from superprompts.mcp.server import get_prompt

# Basic usage
prompt_text = await get_prompt("repo_docs")

# With parameters
prompt_text = await get_prompt("cursor_rules", {
    "target_categories": ["python", "web"]
})
```

**Parameters:**
- `prompt_id` (str): ID of the prompt to generate
- `parameters` (dict[str, Any] | None): Optional parameters

**Returns:** Generated prompt text

#### `get_prompt_metadata`

Get detailed metadata about a specific prompt.

```python
from superprompts.mcp.server import get_prompt_metadata

metadata = await get_prompt_metadata("repo_docs")
```

**Returns:** Dictionary containing prompt metadata

#### `compose_prompt`

Compose a custom prompt by combining elements from different prompts.

```python
from superprompts.mcp.server import compose_prompt

# Basic composition
composed = await compose_prompt("repo_docs")

# With additions from other prompts
composed = await compose_prompt("repo_docs", additions=[
    {
        "source_prompt_id": "cursor_rules",
        "element_type": "section",
        "element_name": "Quality Standards"
    }
])

# With customizations
composed = await compose_prompt("repo_docs", customizations={
    "project_name": "MyProject",
    "focus_area": "API Documentation"
})
```

**Parameters:**
- `base_prompt_id` (str): Base prompt to start with
- `additions` (list[dict[str, str]] | None): Elements to add from other prompts
- `customizations` (dict[str, Any] | None): Custom modifications to apply

**Returns:** Composed prompt text

### Configuration Management

#### `MCPServerConfig`

Configuration for MCP servers.

```python
from superprompts.mcp.config import MCPServerConfig

config = MCPServerConfig(
    name="superprompts",
    command="uv",
    args=["run", "python", "-m", "superprompts.mcp.server"],
    env={"PYTHONPATH": "/path/to/project"},
    cwd="/path/to/project",
    description="SuperPrompts MCP Server",
    version="1.0.0"
)
```

#### `MCPConfig`

Main configuration container.

```python
from superprompts.mcp.config import MCPConfig

config = MCPConfig(
    mcp_servers={
        "superprompts": server_config
    }
)
```

#### `MCPConfigGenerator`

Generate and manage MCP configurations.

```python
from superprompts.mcp.config import MCPConfigGenerator

generator = MCPConfigGenerator()

# Generate Cursor configuration
cursor_config = generator.generate_cursor_config(servers)

# Generate VSCode configuration
vscode_config = generator.generate_vscode_config(servers)

# Validate configuration
errors = validate_config(config, "cursor")
```

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

```python
from superprompts.mcp.config import MCPConfigGenerator, get_available_server_templates

# Get available server templates
templates = get_available_server_templates()

# Create generator
generator = MCPConfigGenerator()

# Generate Cursor configuration
config = generator.generate_cursor_config(templates)

# Save configuration
generator.save_config(config, "cursor", Path("mcp.json"))
```

## Cross-References

- [Available Prompts](available_prompts.md) - Complete list of available prompts
- [MCP Server Guide](mcp_server_guide.md) - Detailed MCP server usage
- [Architecture Guide](architecture_guide.md) - System architecture overview
- [Development Guide](development_guide.md) - Development setup and workflow
