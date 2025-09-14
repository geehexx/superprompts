# Cursor Rules for SuperPrompts MCP Server

This directory contains Cursor IDE rules organized by functionality and trigger type to provide comprehensive guidance for the SuperPrompts MCP server project.

## Rule Categories

### 🚨 Always Rules (Always Applied)
These rules are automatically applied to all files (`alwaysApply: true`):
- No `globs` or `description` fields
- Applied universally across the project

- **`critical-security.mdc`** - Essential security patterns that must always be enforced
- **`critical-async.mdc`** - Critical async patterns for MCP server development

### 🎯 Auto-Attachment Rules (File Match)
These rules are triggered when working with specific file patterns (`alwaysApply: false`):
- Has `globs` field with file patterns
- No `description` field
- Automatically applied when files match the patterns

**Project-wide Rules:**
- **`testing-*.mdc`** - Testing patterns (pytest, async, MCP-specific, Nox)
- **`code-quality-*.mdc`** - Code quality patterns (typing, async, error handling, logging, Pydantic)
- **`documentation-*.mdc`** - Documentation standards (markdown, API, README)
- **`architecture-*.mdc`** - Architecture patterns (module structure, dependency injection)
- **`security-*.mdc`** - Security patterns (input validation)
- **`performance-*.mdc`** - Performance patterns (async optimization, memory management)
- **`general-python-best-practices.mdc`** - Python best practices (`superprompts/**/*.py`, `tests/**/*.py`)

**Nested Directory Rules:**
- **`superprompts/mcp/.cursor/rules/`** - MCP server development patterns
- **`superprompts/cli/.cursor/rules/`** - CLI development patterns
- **`superprompts/prompts/.cursor/rules/`** - Prompt management patterns
- **`tests/.cursor/rules/`** - Testing patterns

### 🧠 Intelligent Rules (Context-Aware)
These rules are triggered intelligently based on context (`alwaysApply: false`):
- Has `description` field for context matching
- No `globs` field
- Applied when the AI determines they're relevant

- **`general-git-workflow.mdc`** - Git workflow when working with version control
- **`general-project-structure.mdc`** - Project structure when organizing or restructuring

## How These Rules Work

### Always Rules
- Automatically applied to every file in the project
- No user action required
- Critical patterns that must always be followed

### Auto-Attachment Rules
- Automatically applied when you open files matching the `globs` patterns
- Context-specific guidance based on what you're working on
- **Nested rules** automatically attach when files in their directory are referenced
- Examples:
  - Working in `superprompts/mcp/` → MCP server rules apply (nested)
  - Working in `superprompts/cli/` → CLI development rules apply (nested)
  - Working in `tests/` → Testing rules apply (nested)
  - Working with Python files → Code quality rules apply (project-wide)
  - Working with Markdown files → Documentation rules apply (project-wide)

### Intelligent Rules
- Applied when the AI determines they're relevant to your current task
- Based on the `description` field and context
- Examples:
  - Working with version control → Git workflow rules may apply
  - Organizing project structure → Project structure rules may apply

## Rule Structure

### Always Rules Format
```yaml
---
alwaysApply: true
---
# Rule content
```

### Auto-Attachment Rules Format
```yaml
---
globs: path/pattern/**/*.py
alwaysApply: false
---
# Rule content
```

### Intelligent Rules Format
```yaml
---
description: Clear description of when this rule applies
alwaysApply: false
---
# Rule content
```

## Nested Rules Structure

Following [Cursor's nested rules documentation](https://docs.cursor.com/en/context/rules#nested-rules), rules are organized in subdirectories:

```
project/
  .cursor/rules/                    # Project-wide rules
  superprompts/
    mcp/
      .cursor/rules/                # MCP-specific rules
    cli/
      .cursor/rules/                # CLI-specific rules
    prompts/
      .cursor/rules/                # Prompt-specific rules
  tests/
    .cursor/rules/                  # Test-specific rules
```

**Benefits of Nested Rules:**
- **Automatic scoping** - Rules apply only when working in their directory
- **Better organization** - Related rules are grouped together
- **Reduced noise** - Only relevant rules are applied
- **Easier maintenance** - Rules are co-located with the code they govern

## Best Practices

1. **Always rules** - Follow critical security and async patterns automatically
2. **Auto-attachment rules** - Get context-specific guidance based on your current file
3. **Agent Requested rules** - Receive relevant guidance based on your current task
4. **Update rules as needed** - Keep rules current with project evolution
5. **Monitor effectiveness** - Ensure rules improve code quality and development experience

This rule system provides comprehensive, context-aware guidance while maintaining the flexibility to apply the right rules at the right time.

## Cross-References

- [Cursor Rules Guide](../docs/cursor_rules_guide.md) - Complete guide to Cursor rules
- [Nested Cursor Rules](../docs/nested_cursor_rules.md) - Comprehensive nested rules documentation
- [Development Guide](../docs/development.md) - Development workflow and practices
- [Testing Guide](../docs/testing.md) - Testing practices and patterns
