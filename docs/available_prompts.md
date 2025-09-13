# Available Prompts

This document provides a comprehensive index of all available prompts in the SuperPrompts collection, with quick reference information and links to detailed documentation.

## Quick Reference

| Prompt | Category | Purpose | CLI Command |
|--------|----------|---------|-------------|
| [Cursor Rules Generator](cursor_rules_guide.md) | Rules | Generate Cursor IDE rules | `superprompts get-prompt cursor_rules` |
| [Repository Documentation Rebuilder](#repository-documentation-rebuilder) | Docs | Rebuild repository documentation | `superprompts get-prompt repo_docs` |

## Detailed Descriptions

### Cursor Rules Generator

**Purpose**: Generate high-quality, non-duplicative Cursor IDE rules tailored to your specific technology stack and coding practices.

**Key Features**:
- Cursor-first design principles
- Automatic stack detection
- Duplication prevention
- Multiple rule types and categories
- Quality assurance and confidence scoring

**Best For**:
- Setting up Cursor IDE rules for new projects
- Standardizing development practices across teams
- Creating focused, actionable development guidelines
- Maintaining consistency in code quality

**Quick Start**:
```bash
# Basic usage
superprompts get-prompt cursor_rules

# Testing-focused rules
superprompts get-prompt cursor_rules --parameters '{
  "target_categories": ["testing"],
  "rule_types": ["Auto Attached"]
}'
```

**Documentation**: [Cursor Rules Guide](cursor_rules_guide.md)

---

### Repository Documentation Rebuilder

**Purpose**: Systematically rebuild and modernize repository documentation with safety checks, loss auditing, and index rebuilding.

**Key Features**:
- Safety-first approach with loss auditing
- Comprehensive gap analysis
- Quality-focused documentation generation
- Systematic batch processing
- Standards-compliant output

**Best For**:
- Auditing existing documentation
- Rebuilding outdated documentation
- Creating comprehensive API documentation
- Establishing documentation standards

**Quick Start**:
```bash
# Basic usage
superprompts get-prompt repo_docs

# API documentation focus
superprompts get-prompt repo_docs --parameters '{
  "target_doc_types": ["API"],
  "include_examples": true
}'
```

**Parameters**:
- `target_doc_types` - Types of documentation to generate (README, API, guides, architecture, testing, changelog, templates, all)
- `batch_size` - Number of documents to process per batch (1-10)
- `include_examples` - Whether to include code examples (true/false)
- `audit_existing` - Whether to audit existing documentation (true/false)
- `generate_index` - Whether to generate documentation index (true/false)

**Output Structure**:
1. **DocAuditReport** - Analysis of existing documentation
2. **DocGapsReport** - Identification of missing documentation
3. **DocMappingPlan** - Strategic plan for documentation generation
4. **GeneratedDocs** - New documentation content
5. **DocIndexUpdate** - Updated documentation index
6. **QAReview** - Quality assurance checklist

## Usage Patterns

### By Category

#### Rules Generation
- **Cursor Rules Generator**: For development workflow and coding standards
- Use when setting up new projects or standardizing practices
- Best combined with team review and iteration

#### Documentation
- **Repository Documentation Rebuilder**: For comprehensive documentation overhaul
- Use for API documentation, user guides, and technical references
- Best for maintaining documentation quality over time

### By Use Case

#### New Project Setup
1. Start with **Cursor Rules Generator** to establish development standards
2. Use **Repository Documentation Rebuilder** to create initial documentation
3. Iterate and refine based on team feedback

#### Existing Project Maintenance
1. Use **Repository Documentation Rebuilder** to audit and update documentation
2. Use **Cursor Rules Generator** to add new rules as practices evolve
3. Regular review and updates to maintain quality

#### Team Onboarding
1. Use **Cursor Rules Generator** to create consistent development guidelines
2. Use **Repository Documentation Rebuilder** to ensure comprehensive documentation
3. Both tools help new team members understand standards and practices

## Integration with Development Workflow

### CLI Integration
All prompts are available through the `superprompts` CLI:
```bash
# List all prompts
superprompts list-prompts

# Get prompt metadata
superprompts metadata <prompt_id>

# Generate prompt with parameters
superprompts get-prompt <prompt_id> --parameters '{"key": "value"}'
```

### MCP Server Integration
Prompts are also available through the MCP (Model Context Protocol) server:
```bash
# Start the MCP server
superprompts-server

# Or use Python module
python -m superprompts.mcp.server
```

### Programmatic Access
Access prompts programmatically in your applications:
```python
from superprompts.prompts.cursor_rules import CursorRulesPrompt
from superprompts.prompts.repo_docs import RepoDocsPrompt

# Create prompt instances
cursor_prompt = CursorRulesPrompt()
docs_prompt = RepoDocsPrompt()

# Generate prompts with parameters
rules_text = cursor_prompt.get_prompt({"target_categories": ["testing"]})
docs_text = docs_prompt.get_prompt({"batch_size": 3})
```

## Customization and Parameters

### Common Parameters
Most prompts support these common parameters:
- **Confidence Threshold**: Minimum confidence for generated content (0-1)
- **Batch Size**: Number of items to process at once
- **Target Categories**: Specific areas to focus on
- **Include Examples**: Whether to include concrete examples

### Parameter Validation
All prompts include built-in parameter validation:
- Type checking and range validation
- Default value assignment for invalid inputs
- Sanitization of user-provided parameters
- Clear error messages for invalid configurations

## Quality Assurance

### Built-in QA Features
- **Confidence Scoring**: All generated content includes confidence scores
- **Validation Checklists**: Built-in quality checklists for each prompt
- **Example Verification**: Examples are validated for correctness
- **Consistency Checks**: Cross-reference validation for related content

### Review Process
1. **Generate**: Use the prompt to generate initial content
2. **Review**: Check confidence scores and QA checklists
3. **Validate**: Test examples and verify accuracy
4. **Iterate**: Refine parameters and regenerate if needed
5. **Apply**: Implement the generated content in your project

## Best Practices

### General Guidelines
- **Start Small**: Begin with focused, specific use cases
- **Iterate**: Use small batches and iterate based on results
- **Review**: Always review generated content before applying
- **Customize**: Adjust parameters based on your specific needs

### Team Collaboration
- **Share Parameters**: Document successful parameter combinations
- **Review Together**: Collaborate on reviewing generated content
- **Establish Standards**: Use prompts to create team standards
- **Regular Updates**: Schedule regular reviews and updates

### Maintenance
- **Version Control**: Track prompt usage and parameter changes
- **Documentation**: Keep records of successful configurations
- **Feedback Loop**: Collect feedback and improve over time
- **Evolution**: Adapt prompts as your project and team evolve

## Getting Help

### Documentation
- **Individual Guides**: Detailed documentation for each prompt
- **Best Practices**: General guidance on effective prompt usage
- **Examples**: Concrete examples and use cases
- **Troubleshooting**: Common issues and solutions

### Support
- **CLI Help**: Use `superprompts --help` for command-line help
- **Metadata**: Use `superprompts metadata <prompt_id>` for parameter details
- **Examples**: Check the examples in each prompt's metadata
- **Community**: Share experiences and learn from others

## Cross-References

- [Main Project README](../README.md) - Project overview and navigation
- [AI Prompting Best Practices](ai_prompting_best_practices.md) - Core prompting principles
- [AI-Ready Documentation Standards](ai_ready_documentation_standards.md) - Documentation standards
- [MCP Configuration Guide](mcp_configuration.md) - Server and CLI usage
- [Cursor Rules Guide](cursor_rules_guide.md) - Cursor rule syntax and validation
