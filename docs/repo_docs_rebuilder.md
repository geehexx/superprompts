# Repository Documentation Rebuilder

## Overview

The Repository Documentation Rebuilder is a comprehensive prompt designed to systematically rebuild and modernize repository documentation with safety checks, loss auditing, and index rebuilding. It prioritizes clarity and completeness over token minimalism, ensuring your documentation is both comprehensive and maintainable.

## Purpose

This prompt helps you:
- Systematically audit and rebuild repository documentation
- Identify gaps in existing documentation
- Generate new documentation with proper structure and examples
- Maintain safety through loss auditing and content recovery
- Create documentation that follows best practices and standards

## Key Features

### Safety-First Approach
- **No Silent Loss**: All content removal is tracked and reversible
- **Loss Auditing**: Comprehensive reporting of what's being changed
- **Content Recovery**: Recoverables and revert options for all changes
- **Batch Processing**: Controlled, reviewable changes in small batches

### Quality-Focused Design
- **Clarity Over Brevity**: Prioritizes completeness and correctness
- **Comprehensive Coverage**: Handles all types of documentation
- **Example-Rich**: Includes concrete examples and code snippets
- **Standards-Compliant**: Follows Diátaxis and Google Style guidelines

### Systematic Process
- **Discovery Phase**: Analyzes existing documentation and project structure
- **Gap Analysis**: Identifies missing or outdated documentation
- **Mapping Plan**: Creates systematic plan for updates
- **Generation**: Produces new documentation with full contents
- **Quality Assurance**: Built-in validation and review processes

## Usage

### Basic Usage

```bash
# List available prompts
superprompts list-prompts

# Get the basic prompt
superprompts get-prompt repo_docs

# Get prompt with custom parameters
superprompts get-prompt repo_docs --parameters '{
  "batch_size": 3,
  "target_doc_types": ["README", "API"],
  "confidence_threshold": 0.8
}'
```

### Advanced Configuration

```bash
# Focus on API documentation
superprompts get-prompt repo_docs --parameters '{
  "batch_size": 5,
  "target_doc_types": ["API"],
  "include_examples": true,
  "output_format": "markdown"
}'

# Comprehensive documentation rebuild
superprompts get-prompt repo_docs --parameters '{
  "batch_size": 3,
  "target_doc_types": ["all"],
  "confidence_threshold": 0.9,
  "include_examples": true
}'
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `batch_size` | int | 5 | Number of files to process per batch (1-10) |
| `target_doc_types` | array | ["all"] | Types of documentation to focus on |
| `confidence_threshold` | float | 0.8 | Minimum confidence for proposals (0-1) |
| `include_examples` | bool | true | Whether to include examples in generated docs |
| `output_format` | string | "markdown" | Output format for generated documentation |

### Available Documentation Types
- `README` - Main project documentation
- `API` - API reference documentation
- `guides` - User guides and tutorials
- `architecture` - System architecture documentation
- `testing` - Testing documentation
- `changelog` - Change log and version history
- `templates` - Documentation templates
- `all` - All documentation types

## Output Structure

The prompt generates documentation in a structured workflow:

1. **RepoDocsInventory** - Complete inventory of existing documentation
2. **DocGapsReport** - Analysis of missing or outdated documentation
3. **MappingPlan** - Strategic plan for documentation updates
4. **ProposedDocs** - New documentation files with full contents
5. **ProposedEdits** - Modifications to existing files
6. **ContentAtRisk** - Items being removed or modified
7. **DocDiffReport** - Detailed change tracking
8. **IndexProposal** - Navigation and index improvements
9. **QA Checklist** - Quality assurance verification
10. **Generic Commands** - Tool-agnostic commands for implementation
11. **NextBatchRecommendation** - Suggestions for follow-up work

## Documentation Standards

### Diátaxis Framework
The prompt follows the Diátaxis documentation framework:
- **Tutorials** - Learning-oriented, step-by-step guides
- **How-to Guides** - Problem-oriented, task-focused instructions
- **Technical Reference** - Information-oriented, fact-based documentation
- **Explanation** - Understanding-oriented, conceptual documentation

### Google Style Guidelines
- **Clarity**: Clear, concise language
- **Active Voice**: Direct, actionable instructions
- **Consistent Terminology**: Standardized terms throughout
- **Audience-First**: Written for the intended audience

### Quality Standards
- **Short Paragraphs**: Scannable, digestible content
- **Meaningful Headings**: Clear navigation structure
- **Examples**: Concrete, runnable examples where possible
- **Cross-References**: Proper linking between related content

## Integration Workflow

### Phase 0: Discovery
- Analyzes project structure and existing documentation
- Detects languages, frameworks, and documentation patterns
- Identifies documentation roots and conventions
- Builds comprehensive inventory

### Phase 1: Gap Analysis
- Identifies missing documentation types
- Detects outdated or inconsistent content
- Finds undocumented public APIs
- Assesses documentation quality

### Phase 2: Planning
- Creates systematic update plan
- Prioritizes documentation by importance
- Plans batch processing approach
- Identifies dependencies and relationships

### Phase 3: Generation
- Generates new documentation files
- Updates existing files with minimal diffs
- Ensures consistency across all documentation
- Includes proper examples and references

### Phase 4: Quality Assurance
- Validates all generated content
- Checks for consistency and completeness
- Verifies examples and code snippets
- Ensures proper formatting and structure

## Best Practices

### Safety First
- **Always review changes**: Don't apply changes blindly
- **Use small batches**: Process 3-5 files at a time
- **Check ContentAtRisk**: Review all proposed removals
- **Test examples**: Verify all code examples work

### Quality Focus
- **Prioritize clarity**: Make documentation easy to understand
- **Include examples**: Provide concrete, working examples
- **Maintain consistency**: Use consistent terminology and style
- **Update regularly**: Keep documentation current with code changes

### Collaboration
- **Review with team**: Get feedback on proposed changes
- **Document decisions**: Explain why certain approaches were chosen
- **Version control**: Track documentation changes in git
- **Iterate**: Continuously improve based on feedback

## Examples

### Example 1: API Documentation
```bash
superprompts get-prompt repo_docs --parameters '{
  "batch_size": 3,
  "target_doc_types": ["API"],
  "include_examples": true,
  "confidence_threshold": 0.9
}'
```

This generates focused API documentation with comprehensive examples.

### Example 2: Complete Rebuild
```bash
superprompts get-prompt repo_docs --parameters '{
  "batch_size": 5,
  "target_doc_types": ["all"],
  "confidence_threshold": 0.8,
  "include_examples": true
}'
```

This performs a comprehensive documentation rebuild across all types.

## Troubleshooting

### Common Issues

**Generated documentation is too generic**
- Provide more context about your specific project
- Use more targeted `target_doc_types`
- Increase `confidence_threshold` for higher quality

**Too many changes proposed**
- Reduce `batch_size` to process smaller chunks
- Review `ContentAtRisk` carefully before applying
- Use more specific `target_doc_types`

**Missing project-specific context**
- Ensure the prompt has access to your codebase
- Provide additional context about your project structure
- Use the discovery phase to analyze your specific setup

### Getting Help

- Use `superprompts metadata repo_docs` to see all available parameters
- Check the QA Checklist in the generated output
- Review the confidence scores for each proposal
- Start with a small batch and iterate

## Related Documentation

- [AI-Ready Documentation Standards](ai_ready_documentation_standards.md) - Documentation standards and best practices
- [AI Prompting Best Practices](ai_prompting_best_practices.md) - Core prompting principles
- [MCP Server Guide](mcp_server_guide.md) - Using the MCP server and CLI tools

## Cross-References

- [Cursor Rules Generator](cursor_rules_generator.md) - For development workflow rules
- [Main Project README](../README.md) - Project overview and navigation
- [Available Prompts](../README.md#available-prompts) - Complete list of all prompts
