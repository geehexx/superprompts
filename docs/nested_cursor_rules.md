# Nested Cursor Rules Documentation

Comprehensive documentation for the nested Cursor rules architecture implemented in the SuperPrompts project.

## Overview

This project implements a **nested rules architecture** following [Cursor's nested rules documentation](https://docs.cursor.com/en/context/rules#nested-rules). Rules are organized in subdirectories and automatically apply when working in their respective directories, providing precise, context-aware guidance.

## Architecture

### Directory Structure

```
superprompts/
├── .cursor/rules/                    # Project-wide rules
│   ├── critical-*.mdc               # Always rules
│   ├── testing-*.mdc                # Testing rules
│   ├── code-quality-*.mdc           # Code quality rules
│   ├── documentation-*.mdc          # Documentation rules
│   ├── architecture-*.mdc           # Architecture rules
│   ├── security-*.mdc               # Security rules
│   ├── performance-*.mdc            # Performance rules
│   └── general-*.mdc                # General rules
├── superprompts/
│   ├── mcp/
│   │   └── .cursor/rules/           # MCP-specific rules
│   │       ├── mcp-server-patterns.mdc
│   │       └── architecture-patterns.mdc
│   ├── cli/
│   │   └── .cursor/rules/           # CLI-specific rules
│   │       └── cli-development.mdc
│   └── prompts/
│       └── .cursor/rules/           # Prompt-specific rules
│           └── prompt-management.mdc
└── tests/
    └── .cursor/rules/               # Test-specific rules
        └── testing-patterns.mdc
```

### Rule Types

#### 1. Always Rules
- **Format**: `alwaysApply: true`, no `globs`, no `description`
- **Application**: Applied universally across the project
- **Location**: `.cursor/rules/`
- **Examples**:
  - `critical-security.mdc` - Essential security patterns
  - `critical-async.mdc` - Critical async patterns

#### 2. Project-wide Auto-Attachment Rules
- **Format**: `alwaysApply: false`, has `globs`, no `description`
- **Application**: Applied when files match the glob patterns
- **Location**: `.cursor/rules/`
- **Examples**:
  - `testing-pytest-patterns.mdc` - Applied to test files
  - `code-quality-python-typing.mdc` - Applied to Python files

#### 3. Nested Auto-Attachment Rules
- **Format**: `alwaysApply: false`, has `globs`, no `description`
- **Application**: Applied when working in their directory
- **Location**: `<directory>/.cursor/rules/`
- **Examples**:
  - `superprompts/mcp/.cursor/rules/mcp-server-patterns.mdc`
  - `tests/.cursor/rules/testing-patterns.mdc`

#### 4. Agent Requested Rules
- **Format**: `alwaysApply: false`, has `description`, no `globs`
- **Application**: Applied when AI determines they're relevant
- **Location**: `.cursor/rules/`
- **Examples**:
  - `general-git-workflow.mdc` - Applied when working with Git
  - `general-project-structure.mdc` - Applied when organizing project

## Rule Application Logic

### Automatic Rule Application

**When working in `superprompts/mcp/`:**
1. Always rules apply (2 rules)
2. Nested MCP rules apply (2 rules)
3. Project-wide Python rules apply (based on file patterns)
4. Agent Requested rules may apply (based on context)

**When working in `superprompts/cli/`:**
1. Always rules apply (2 rules)
2. Nested CLI rules apply (1 rule)
3. Project-wide Python rules apply (based on file patterns)
4. Agent Requested rules may apply (based on context)

**When working in `superprompts/prompts/`:**
1. Always rules apply (2 rules)
2. Nested prompt rules apply (1 rule)
3. Project-wide Python rules apply (based on file patterns)
4. Agent Requested rules may apply (based on context)

**When working in `tests/`:**
1. Always rules apply (2 rules)
2. Nested testing rules apply (1 rule)
3. Project-wide testing rules apply (based on file patterns)
4. Agent Requested rules may apply (based on context)

### Rule Hierarchy

Rules are applied in the following order of precedence:

1. **Always Rules** - Applied everywhere
2. **Nested Rules** - Applied when working in their directory
3. **Project-wide Rules** - Applied based on file patterns
4. **Agent Requested Rules** - Applied based on context

## Benefits of Nested Rules

### 1. Precise Targeting
- Rules apply exactly when and where they should
- No over-application of irrelevant rules
- Context-specific guidance based on your current working directory

### 2. Better Performance
- Auto-attachment is more efficient than intelligent matching
- Reduced computational overhead
- Faster rule evaluation

### 3. Clear Boundaries
- Easy to understand when each rule type applies
- Predictable rule behavior
- Clear separation of concerns

### 4. Easier Maintenance
- Rules are co-located with the code they govern
- Easier to find and update related rules
- Better organization and structure

### 5. Reduced Noise
- Only relevant rules are applied
- Cleaner AI context
- More focused guidance

## Implementation Details

### File Format

All rules use the `.mdc` format (Markdown with simplified frontmatter):

```yaml
---
globs: **/*.py
alwaysApply: false
---
# Rule Title

## Rule
- Rule content here

## Examples
- Example 1
- Example 2

## Rationale
- Why this rule matters
```

### Nested Rule Globs

Nested rules use relative globs from their directory:

```yaml
# In superprompts/mcp/.cursor/rules/mcp-server-patterns.mdc
---
globs: **/*.py
alwaysApply: false
---
```

This means the rule applies to all Python files in the `superprompts/mcp/` directory and its subdirectories.

### Rule Naming Convention

**Project-wide rules:**
- Pattern: `<category>-<slug>.mdc`
- Example: `testing-pytest-patterns.mdc`

**Nested rules:**
- Pattern: `<purpose>.mdc`
- Example: `mcp-server-patterns.mdc`

## Usage Examples

### Working on MCP Server Code

When you open a file in `superprompts/mcp/`:

1. **Always rules** provide critical security and async patterns
2. **Nested MCP rules** provide MCP-specific development guidance
3. **Project-wide rules** provide Python code quality guidance
4. **Agent Requested rules** may provide Git workflow guidance if relevant

### Working on CLI Code

When you open a file in `superprompts/cli/`:

1. **Always rules** provide critical security and async patterns
2. **Nested CLI rules** provide CLI-specific development guidance
3. **Project-wide rules** provide Python code quality guidance
4. **Agent Requested rules** may provide project structure guidance if relevant

### Working on Tests

When you open a file in `tests/`:

1. **Always rules** provide critical security and async patterns
2. **Nested testing rules** provide comprehensive testing guidance
3. **Project-wide testing rules** provide specific testing patterns
4. **Agent Requested rules** may provide Git workflow guidance if relevant

## Maintenance

### Adding New Nested Rules

1. Create the rule file in the appropriate directory:
   ```bash
   touch superprompts/mcp/.cursor/rules/new-rule.mdc
   ```

2. Add the frontmatter:
   ```yaml
   ---
   globs: **/*.py
   alwaysApply: false
   ---
   ```

3. Add the rule content following the established format

### Updating Existing Rules

1. Edit the rule file directly
2. Ensure the frontmatter format is correct
3. Test that the rule applies when expected

### Removing Rules

1. Delete the rule file
2. Update documentation if necessary
3. Verify no other rules depend on it

## Troubleshooting

### Rules Not Applying

1. **Check file location** - Ensure the rule is in the correct directory
2. **Check frontmatter** - Verify `globs` and `alwaysApply` are correct
3. **Check file extension** - Must be `.mdc`, not `.md`
4. **Check glob patterns** - Ensure they match your file structure

### Too Many Rules Applying

1. **Review glob patterns** - Make them more specific if needed
2. **Check rule hierarchy** - Ensure rules are in the right category
3. **Consider moving to nested rules** - If rules are directory-specific

### Rules Not Specific Enough

1. **Move to nested rules** - If rules are directory-specific
2. **Add more specific globs** - Target specific file patterns
3. **Split into multiple rules** - Break down broad rules

## Best Practices

### Rule Design

1. **Keep rules focused** - One concept per rule
2. **Use precise globs** - Avoid overly broad file patterns
3. **Provide examples** - Include concrete examples
4. **Explain rationale** - Why the rule matters

### Organization

1. **Use nested rules for directory-specific patterns**
2. **Use project-wide rules for file-type specific patterns**
3. **Use intelligent rules for context-dependent guidance**
4. **Use always rules sparingly for critical patterns only**

### Maintenance

1. **Regular review** - Periodically review rule effectiveness
2. **Update as needed** - Keep rules current with project evolution
3. **Test rule application** - Verify rules apply when expected
4. **Document changes** - Update documentation when rules change

## Cross-References

- [Cursor Rules Guide](cursor_rules_guide.md) - Complete guide to Cursor rules
- [Cursor Nested Rules Documentation](https://docs.cursor.com/en/context/rules#nested-rules) - Official Cursor documentation
- [Development Guide](development.md) - Development workflow and practices
- [Testing Guide](testing.md) - Testing practices and patterns
