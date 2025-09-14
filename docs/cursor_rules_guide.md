# Cursor Rules Guide

Complete guide to creating, using, and managing Cursor IDE rules for the SuperPrompts project.

## Overview

Cursor rules help maintain code quality and consistency by providing context-aware guidance. This project uses a **nested rules architecture** that automatically applies relevant rules based on your current working directory and file types. This guide covers both using the Cursor Rules Generator prompt and writing effective rules manually.

## Rule Architecture

### Nested Rules Structure

Following [Cursor's nested rules documentation](https://docs.cursor.com/en/context/rules#nested-rules), rules are organized in subdirectories:

```
project/
  .cursor/rules/                    # Project-wide rules (21 rules)
  superprompts/
    mcp/
      .cursor/rules/                # MCP-specific rules (2 rules)
    cli/
      .cursor/rules/                # CLI-specific rules (1 rule)
    prompts/
      .cursor/rules/                # Prompt-specific rules (1 rule)
  tests/
    .cursor/rules/                  # Test-specific rules (1 rule)
```

### Rule Types

1. **Always Rules** - Applied universally across the project
2. **Project-wide Auto-Attachment Rules** - Applied based on file patterns
3. **Nested Auto-Attachment Rules** - Applied when working in specific directories
4. **Agent Requested Rules** - Applied based on context and AI decision

## Rule Structure Overview

This project uses a **nested rules architecture** with rules organized by type and location:

### Always Rules
- Applied universally across the project
- Critical patterns that must always be followed
- Examples: Security patterns, async patterns

### Project-wide Auto-Attachment Rules
- Applied based on file patterns
- File-type specific guidance
- Examples: Python files, Markdown files, test files

### Nested Auto-Attachment Rules
- Applied when working in specific directories
- Directory-specific patterns and practices
- Examples: MCP server patterns, CLI development, testing patterns

### Agent Requested Rules
- Applied based on context and AI decision
- Context-dependent guidance
- Examples: Git workflow, project structure decisions

## How Nested Rules Work

### Automatic Rule Application

**When working in `superprompts/mcp/`:**
- MCP server patterns automatically apply
- Architecture patterns for MCP development apply
- All project-wide rules for Python files still apply

**When working in `superprompts/cli/`:**
- CLI development patterns automatically apply
- All project-wide rules for Python files still apply

**When working in `superprompts/prompts/`:**
- Prompt management patterns automatically apply
- All project-wide rules for Python files still apply

**When working in `tests/`:**
- Testing patterns automatically apply
- All project-wide testing rules still apply

### Rule Hierarchy

1. **Always Rules** - Applied everywhere (2 rules)
2. **Nested Rules** - Applied when working in their directory (5 rules)
3. **Project-wide Rules** - Applied based on file patterns (21 rules)
4. **Agent Requested Rules** - Applied based on context (2 rules)

### Benefits of Nested Rules

- **Precise Targeting** - Rules apply exactly when and where they should
- **Reduced Noise** - No over-application of irrelevant rules
- **Better Performance** - Auto-attachment is more efficient than intelligent matching
- **Clear Boundaries** - Easy to understand when each rule type applies
- **Easier Maintenance** - Rules are co-located with the code they govern

## Using the Cursor Rules Generator

### Basic Usage

```bash
# List available prompts
superprompts list-prompts

# Get the basic prompt
superprompts get-prompt cursor_rules

# Get prompt with custom parameters
superprompts get-prompt cursor_rules --parameters '{
  "target_categories": ["testing", "documentation"],
  "rule_types": ["Auto Attached"],
  "similarity_threshold": 0.7
}'
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `target_categories` | array | All categories | Categories to generate rules for |
| `rule_types` | array | All types | Types of rules to generate |
| `similarity_threshold` | float | 0.7 | Threshold for deduplication (0-1) |
| `confidence_threshold` | float | 0.8 | Minimum confidence for rules (0-1) |
| `max_rules_per_category` | int | 5 | Maximum rules per category (1-20) |

### Available Categories
- `testing` - Testing standards and practices
- `documentation` - Documentation requirements
- `code_quality` - Code quality and style rules
- `architecture` - Architectural patterns and decisions
- `security` - Security best practices
- `performance` - Performance optimization
- `general` - General development practices

## Rule Types

### Always Rules
- **Format**: `alwaysApply: true`, no `globs`, no `description`
- **Application**: Applied universally across the project
- **Use Case**: Critical patterns that must always be followed
- **Examples**: Security patterns, async patterns

### Auto-Attachment Rules
- **Format**: `alwaysApply: false`, has `globs`, no `description`
- **Application**: Applied when files match the glob patterns
- **Use Case**: File-type or directory-specific guidance
- **Examples**: Python files, test files, specific directories

### Agent Requested Rules
- **Format**: `alwaysApply: false`, has `description`, no `globs`
- **Application**: Applied when AI determines they're relevant
- **Use Case**: Context-dependent guidance
- **Examples**: Git workflow, project structure decisions

### Nested Rules
- **Location**: Subdirectories with `.cursor/rules/`
- **Application**: Automatically attach when working in their directory
- **Use Case**: Directory-specific patterns and practices
- **Examples**: MCP server patterns, CLI development, testing patterns

## Writing Rules Manually

### Frontmatter Fields

**Simplified Format:**
- `description` - Short purpose (1–2 sentences) - **Only for Agent Requested Rules**
- `globs` - Specific file globs affected by this rule - **Only for Auto-Attachment Rules**
- `alwaysApply` - true/false - **Always required**

**Note**: The frontmatter contains exactly 3 fields: `description`, `globs`, and `alwaysApply`. Each rule type uses a specific subset of these fields.

### Markdown Structure

**Always Rules:**
```yaml
---
alwaysApply: true
---
# <Title>
## Rule
- Rule content here
## Examples
## Rationale
```

**Auto-Attachment Rules:**
```yaml
---
globs: path/pattern/**/*.py
alwaysApply: false
---
# <Title>
## Rule
- Rule content here
## Examples
## Rationale
```

**Agent Requested Rules:**
```yaml
---
description: Clear description of when this rule applies
alwaysApply: false
---
# <Title>
## Rule
- Rule content here
## Examples
## Rationale
```

**Nested Rules:**
```yaml
---
globs: **/*.py
alwaysApply: false
---
# <Title>
## Rule
- Rule content here
## Examples
## Rationale
```

### File Organization

**Project-wide Rules:**
- **Location**: `.cursor/rules/`
- **Pattern**: `<category>-<slug>.mdc`
- **Slug**: derived from the H1 title, lowercase kebab-case
- **Example**: `testing-pytest-patterns.mdc`

**Nested Rules:**
- **Location**: `<directory>/.cursor/rules/`
- **Pattern**: `<purpose>.mdc`
- **Slug**: descriptive name for the rule's purpose
- **Example**: `mcp-server-patterns.mdc`

**File Extensions:**
- **Current**: `.mdc` (Markdown with frontmatter)
- **Legacy**: `.md` (deprecated)

## Best Practices

### Rule Design
- **Keep rules focused**: One concept per rule
- **Use precise globs**: Avoid overly broad file patterns
- **Provide examples**: Include 2-3 concrete examples
- **Explain rationale**: Why the rule matters and what risks it reduces
- **Prefer Auto Attached**: Use specific `when` predicates when possible

### Quality Assurance
- **Review generated rules**: Don't blindly apply all suggestions
- **Test attachment conditions**: Ensure Auto Attached rules trigger correctly
- **Validate globs**: Make sure file patterns match your project structure
- **Check for conflicts**: Ensure rules don't contradict each other

### Maintenance
- **Regular updates**: Re-run the generator as your stack evolves
- **Monitor effectiveness**: Track which rules are most helpful
- **Iterate on thresholds**: Adjust similarity and confidence thresholds based on results

## Validation

### Validation Tools
- **Script**: `scripts/validate_cursor_rules.py`
- **Schema**: `schemas/cursor_rule_frontmatter.schema.json`
- **Pre-commit**: Automatic validation on commit
- **CI/CD**: Validation in GitHub Actions

### Validation Options
- **Default**: Schema + semantic checks
- `--strict`: Also enforces filename pattern and requires `ruleType`
- `--fix`: With `--strict`, auto-renames files to expected pattern
- `--report-json <path>`: Writes machine-readable report

### Usage
```bash
# Basic validation
python3 scripts/validate_cursor_rules.py .cursor/rules

# Strict validation
python3 scripts/validate_cursor_rules.py --strict .cursor/rules

# Generate report
python3 scripts/validate_cursor_rules.py --report-json report.json .cursor/rules
```

## Troubleshooting

### Common Issues

**Rules not attaching automatically**
- Check that `ruleType` is set to "Auto Attached"
- Verify `when` conditions match your file patterns
- Ensure globs are specific enough

**Too many duplicate rules**
- Increase `similarity_threshold` to 0.8 or higher
- Review and merge similar rules manually
- Use more specific categories

**Rules too generic**
- Decrease `confidence_threshold` to 0.6 or lower
- Provide more context about your specific stack
- Use more targeted categories

### Getting Help

- Use `superprompts metadata cursor_rules` to see all available parameters
- Check the QA Checklist in the generated output
- Review the confidence scores for each rule
- Start with a small batch and iterate

## Cross-References

- [AI Prompting Best Practices](ai_prompting_best_practices.md) - Core prompting principles
- [JSON Schemas](../schemas/README.md) - Schema validation
- [Available Prompts](available_prompts.md) - Complete list of all prompts
