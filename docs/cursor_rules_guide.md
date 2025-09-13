# Cursor Rules Guide

Complete guide to creating, using, and managing Cursor IDE rules for the SuperPrompts project.

## Overview

Cursor rules help maintain code quality and consistency by providing context-aware guidance. This guide covers both using the Cursor Rules Generator prompt and writing effective rules manually.

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

- **Always** - Applied in all contexts; avoid broad globs
- **Auto Attached** - Attach automatically when `when` predicates match (preferred default)
- **Agent Requested** - Shown when the agent asks for specific guidance
- **Manual** - Shown on demand

## Writing Rules Manually

### Frontmatter Fields

- `description` - Short purpose (1–2 sentences)
- `type` - One of testing|documentation|code_quality|architecture|security|performance|general
- `globs` - Specific file globs affected by this rule
- `ruleType` - One of Always | Auto Attached | Agent Requested | Manual
- `alwaysApply` - true/false (if true, omit `when`)
- `appliesTo` - Optional list of targets/audiences
- `when` - Predicate with `filesChanged`, `pathsPresent`, `languages` arrays
- `tags` - Optional labels to aid discovery
- `severity` - critical|high|medium|low|info (empty if unclear)
- `scope` - Optional granular scope labels (e.g., unit-tests, e2e, api-design)

### Markdown Structure

```yaml
---
description: Short purpose
type: <category>
globs:
  - src/**/*.{ts,tsx}
ruleType: Auto Attached
alwaysApply: false
appliesTo: []
when:
  filesChanged: []
  pathsPresent: []
  languages: []
tags: []
severity: ""
scope: []
---
# <Title>
## Description
## Rule
## Examples
## Rationale
## Priority
## Confidence
```

### File Organization

- **Location**: `.cursor/rules/`
- **Pattern**: `<type>-<slug>.md` where `type` matches frontmatter `type`
- **Slug**: derived from the H1 title, lowercase kebab-case
- **Example**: `testing-js-ts-testing-standards.md`

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
