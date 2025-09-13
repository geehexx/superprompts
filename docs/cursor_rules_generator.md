# Cursor Rules Generator

## Overview

The Cursor Rules Generator is a sophisticated prompt designed to create high-quality, non-duplicative Cursor IDE rules tailored to your specific technology stack and coding practices. It follows Cursor-first principles to generate rules that are scannable, focused, and maximally useful.

## Purpose

This prompt helps you:
- Generate comprehensive Cursor rules for your project
- Ensure rules are tailored to your specific stack and practices
- Avoid duplication and maintain high signal-to-noise ratio
- Create rules that integrate seamlessly with Cursor's workflow
- Maintain consistency across your development team

## Key Features

### Cursor-First Design
- **High-Signal Rules**: Generates focused, actionable rules rather than generic advice
- **Non-Duplicative**: Uses similarity thresholds to prevent rule overlap
- **Scannable Format**: Optimized for Cursor's rule display and interaction
- **Precise Globs**: Uses specific file patterns to minimize noise

### Comprehensive Coverage
- **Multiple Categories**: Testing, documentation, code quality, architecture, security, performance
- **Flexible Attachment**: Always, Auto Attached, Agent Requested, or Manual rules
- **Stack Detection**: Automatically detects languages, frameworks, and tools
- **Quality Assurance**: Built-in validation and confidence scoring

## Usage

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

### Advanced Configuration

```bash
# Generate testing-focused rules
superprompts get-prompt cursor_rules --parameters '{
  "target_categories": ["testing"],
  "rule_types": ["Auto Attached", "Manual"],
  "max_rules_per_category": 3,
  "confidence_threshold": 0.9
}'

# Generate comprehensive rules for full stack
superprompts get-prompt cursor_rules --parameters '{
  "target_categories": ["testing", "documentation", "code_quality", "architecture"],
  "rule_types": ["Always", "Auto Attached", "Agent Requested"],
  "similarity_threshold": 0.6,
  "max_rules_per_category": 5
}'
```

## Parameters

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

### Available Rule Types
- `Always` - Applied in all contexts
- `Auto Attached` - Automatically attached based on conditions
- `Agent Requested` - Shown when agent asks for guidance
- `Manual` - Shown on demand

## Output Structure

The prompt generates rules in a structured format:

1. **CursorProjectSignals** - Analysis of your project structure
2. **RulesPlan** - Strategic plan for rule generation
3. **GeneratedCursorRules** - JSON specification of rules
4. **RuleMarkdownFiles** - Ready-to-use `.cursor/rules/*.md` files
5. **PlacementPlan** - File organization strategy
6. **ProposedEdits** - Safe modifications to existing rules
7. **QA Checklist** - Quality assurance verification
8. **NextBatchRecommendation** - Suggestions for follow-up

## Integration with Cursor

### File Placement
Rules are placed in `.cursor/rules/` with the naming pattern:
```
.cursor/rules/<category>-<slug>.md
```

### Frontmatter Structure
Each rule includes comprehensive frontmatter:
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
```

## Best Practices

### Rule Design
- **Keep rules focused**: One concept per rule
- **Use precise globs**: Avoid overly broad file patterns
- **Provide examples**: Include 2-3 concrete examples
- **Explain rationale**: Why the rule matters and what risks it reduces

### Quality Assurance
- **Review generated rules**: Don't blindly apply all suggestions
- **Test attachment conditions**: Ensure Auto Attached rules trigger correctly
- **Validate globs**: Make sure file patterns match your project structure
- **Check for conflicts**: Ensure rules don't contradict each other

### Maintenance
- **Regular updates**: Re-run the generator as your stack evolves
- **Monitor effectiveness**: Track which rules are most helpful
- **Iterate on thresholds**: Adjust similarity and confidence thresholds based on results

## Examples

### Example 1: Testing Rules
```bash
superprompts get-prompt cursor_rules --parameters '{
  "target_categories": ["testing"],
  "rule_types": ["Auto Attached"],
  "max_rules_per_category": 3
}'
```

This generates focused testing rules that automatically attach to test files.

### Example 2: Documentation Rules
```bash
superprompts get-prompt cursor_rules --parameters '{
  "target_categories": ["documentation"],
  "rule_types": ["Manual", "Agent Requested"],
  "confidence_threshold": 0.9
}'
```

This generates high-confidence documentation rules for manual review.

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

## Related Documentation

- [Cursor Rules Usage Guide](rules_usage.md) - Detailed guide to Cursor rule syntax
- [AI Prompting Best Practices](ai_prompting_best_practices.md) - Core prompting principles
- [MCP Server Guide](mcp_server_guide.md) - Using the MCP server and CLI tools

## Cross-References

- [Repository Documentation Rebuilder](repo_docs_rebuilder.md) - For documentation-focused prompts
- [Main Project README](../README.md) - Project overview and navigation
- [Available Prompts](../README.md#available-prompts) - Complete list of all prompts
