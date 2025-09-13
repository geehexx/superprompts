# Architecture Guide

Understanding the SuperPrompts system architecture and design principles.

## System Overview

SuperPrompts is built around a modular architecture that separates concerns between prompt management, MCP server integration, and CLI tooling.

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CLI Tools     │    │   MCP Server     │    │  Prompt System  │
│                 │    │                  │    │                 │
│ • list-prompts  │◄──►│ • list_prompts   │◄──►│ • BasePrompt    │
│ • get-prompt    │    │ • get_prompt     │    │ • RepoDocsPrompt│
│ • config        │    │ • compose_prompt │    │ • CursorRules   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌──────────────────┐
                    │  Configuration   │
                    │  Management      │
                    │                  │
                    │ • MCPConfig      │
                    │ • ServerTemplates│
                    │ • Validation     │
                    └──────────────────┘
```

## Core Components

### 1. Prompt System (`superprompts/prompts/`)

**BasePrompt Class**
- Abstract base class for all prompts
- Defines common interface: `get_prompt()`, `get_metadata()`, `get_element()`
- Handles parameter validation and prompt generation

**Prompt Implementations**
- `RepoDocsPrompt`: Repository documentation rebuilder
- `CursorRulesPrompt`: Cursor IDE rules generator
- Each prompt is self-contained with its own logic and templates

### 2. MCP Server (`superprompts/mcp/`)

**MCP-Compliant Implementation**
- Uses FastMCP framework with proper MCP capabilities
- Declares `prompts` and `completions` capabilities
- Provides MCP-standard prompt handlers and completion support

**Server Architecture**
```python
# MCP server with proper capabilities
mcp = FastMCP("superprompts", capabilities=["prompts", "completions"])

@mcp.prompt
def repo_docs_prompt_handler(parameters: dict[str, Any] | None = None) -> str:
    """Repository Documentation Rebuilder prompt."""
    # Implementation details...

@mcp.prompt
def cursor_rules_prompt_handler(parameters: dict[str, Any] | None = None) -> str:
    """Cursor Rules Generator prompt."""
    # Implementation details...
```

**MCP Compliance Features**
- Proper argument definitions with types and descriptions
- Completion suggestions for prompt arguments
- MCP-standard metadata structure
- Support for `prompts/list` and `prompts/get` messages

### 3. Configuration Management (`superprompts/mcp/config.py`)

**MCPServerConfig**
- Pydantic model for server configuration
- Supports multiple MCP server types (superprompts, github, filesystem)
- Handles environment variables and working directories

**MCPConfigGenerator**
- Generates configurations for different formats (Cursor, VSCode, Generic)
- Validates existing configurations
- Supports merging and conversion between formats

### 4. CLI Interface (`superprompts/cli/main.py`)

**Command Structure**
- Click-based command groups
- Async operations for MCP server communication
- Rich console output with tables and panels

**Key Commands**
- `list-prompts`: Browse available prompts
- `get-prompt`: Generate specific prompts
- `config`: Manage MCP configurations
- `compose`: Create custom prompts

## Data Flow

### 1. Prompt Generation Flow
```
User Request → CLI/MCP → Prompt Class → Template Processing → Generated Prompt
```

### 2. Configuration Flow
```
Template Selection → Config Generation → Validation → Format Conversion → File Output
```

### 3. MCP Integration Flow
```
Cursor IDE → MCP Protocol → FastMCP Server → Prompt System → Response
```

## Design Principles

### 1. Modularity
- Each component has a single responsibility
- Clear interfaces between components
- Easy to extend with new prompt types

### 2. Type Safety
- Full type hints throughout the codebase
- Pydantic models for data validation
- MyPy strict mode compliance

### 3. Async-First
- All I/O operations are async
- Non-blocking MCP server operations
- Scalable for multiple concurrent requests

### 4. Configuration Flexibility
- Support for multiple MCP server formats
- Template-based configuration generation
- Validation and conversion utilities

## Extension Points

### Adding New Prompts
1. Create new class inheriting from `BasePrompt`
2. Implement required methods: `get_prompt()`, `get_metadata()`
3. Register in MCP server's `list_prompts()` function
4. Add to CLI help and documentation

### Adding New MCP Tools
1. Define new `@mcp.tool` function
2. Add CLI command if needed
3. Update documentation and help text

### Adding New Configuration Formats
1. Extend `MCPConfigGenerator` class
2. Add format-specific generation methods
3. Update validation logic
4. Add CLI options for new format

## Security Considerations

- No arbitrary code execution in prompt generation
- Parameter validation on all inputs
- Safe file operations with path validation
- No secrets or credentials in prompt content

## Performance Characteristics

- Fast prompt generation (in-memory templates)
- Efficient MCP server (FastMCP framework)
- Minimal dependencies for core functionality
- Async operations prevent blocking

## Future Architecture Considerations

- Plugin system for third-party prompts
- Caching layer for frequently used prompts
- Metrics and analytics collection
- Multi-language prompt support
