# Commit Message Standards

This document outlines the standardized format and best practices for Git commit messages in the SuperPrompts project.

## Overview

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification to ensure consistent, clear, and machine-readable commit messages. This standard improves collaboration, enables automated changelog generation, and makes the project history more maintainable.

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Components

#### Type (Required)
The type of change being made. Must be one of:

- **`feat`**: A new feature for the user
- **`fix`**: A bug fix for the user
- **`docs`**: Documentation changes only
- **`style`**: Code style changes (formatting, missing semicolons, etc.)
- **`refactor`**: Code refactoring without adding features or fixing bugs
- **`perf`**: Performance improvements
- **`test`**: Adding or correcting tests
- **`build`**: Changes to build system or external dependencies
- **`ci`**: Changes to CI configuration files and scripts
- **`chore`**: Maintenance tasks, dependency updates, etc.
- **`revert`**: Reverting a previous commit

#### Scope (Optional)
The area of the codebase affected. Common scopes include:

- **`cli`**: Command-line interface changes
- **`mcp`**: MCP server functionality
- **`prompts`**: Prompt generators and templates
- **`docs`**: Documentation files
- **`tests`**: Test files and test utilities
- **`config`**: Configuration files (pyproject.toml, etc.)
- **`ci`**: CI/CD pipeline changes
- **`deps`**: Dependency updates

#### Subject (Required)
A concise description of the change, written in imperative mood:

- Use lowercase (except for proper nouns)
- No period at the end
- Maximum 50 characters
- Start with a verb (add, fix, update, remove, etc.)

#### Body (Optional)
A detailed explanation of the change:

- Wrap lines at 72 characters
- Explain the "what" and "why", not the "how"
- Include motivation and context
- Use blank lines to separate paragraphs

#### Footer (Optional)
Metadata about the commit:

- Issue references: `Closes #123`, `Fixes #456`
- Breaking changes: `BREAKING CHANGE: description`
- Co-authors: `Co-authored-by: Name <email>`

## Examples

### Feature Addition
```
feat(prompts): add cursor rules generator

Implement a new prompt generator that creates high-signal Cursor rules
tailored to specific technology stacks. The generator analyzes project
structure and dependencies to produce contextual rules.

Closes #42
```

### Bug Fix
```
fix(mcp): handle connection errors gracefully

Previously, the MCP server would crash when encountering network
timeouts. Now it logs the error and attempts to reconnect with
exponential backoff.

Fixes #23
```

### Documentation Update
```
docs: update quick start guide

Add step-by-step instructions for setting up the MCP server with
popular AI tools. Include troubleshooting section for common
connection issues.
```

### Refactoring
```
refactor(cli): extract prompt loading logic

Move prompt loading and validation into a separate module to improve
code organization and enable better testing of individual components.
```

### Breaking Change
```
feat(api): change prompt parameter structure

BREAKING CHANGE: The prompt parameters now use a nested structure
instead of flat key-value pairs. Update your code to use the new
format: `{category: {key: value}}` instead of `{category_key: value}`.
```

### Maintenance
```
chore(deps): update ruff to v0.8.4

Update Ruff linter to latest version for improved performance and
additional linting rules.
```

## Best Practices

### Writing Good Commit Messages

1. **Be Clear and Concise**
   - Use clear, descriptive language
   - Avoid technical jargon when possible
   - Focus on the user impact

2. **Use Imperative Mood**
   - "Add feature" not "Added feature"
   - "Fix bug" not "Fixed bug"
   - "Update docs" not "Updated docs"

3. **Keep It Focused**
   - One logical change per commit
   - If you need to make multiple changes, create multiple commits
   - Use `git add -p` to stage parts of files

4. **Provide Context**
   - Explain why the change was made
   - Reference related issues or discussions
   - Include any important considerations

### Commit Message Length

- **Subject**: Maximum 50 characters
- **Body**: Wrap at 72 characters
- **Total**: Keep commits focused and atomic

### Common Mistakes to Avoid

❌ **Too vague**
```
fix: stuff
```

✅ **Specific and clear**
```
fix(mcp): handle malformed JSON in server responses
```

❌ **Wrong mood**
```
Added new feature
```

✅ **Imperative mood**
```
feat: add new feature
```

❌ **Too long subject**
```
feat: implement comprehensive cursor rules generator with advanced pattern matching
```

✅ **Concise subject**
```
feat(prompts): add cursor rules generator
```

❌ **Multiple changes**
```
feat: add new prompt and fix CLI bug
```

✅ **Separate commits**
```
feat(prompts): add new prompt generator
fix(cli): resolve argument parsing issue
```

## Tooling

### Pre-commit Hooks

We use commitlint to automatically validate commit messages. The validation runs on every commit attempt and will reject messages that don't follow the standard.

### Manual Validation

You can manually validate a commit message:

```bash
# Validate the last commit message
poetry run commitlint --from HEAD~1 --to HEAD

# Validate a specific commit message
echo "feat: add new feature" | poetry run commitlint
```

### IDE Integration

Most modern IDEs support commit message templates and validation. Configure your IDE to:

- Show character count for subject and body
- Highlight validation errors
- Provide autocomplete for common types and scopes

## Enforcement

Commit message validation is enforced through:

1. **Pre-commit hooks**: Automatic validation on commit
2. **CI/CD pipeline**: Validation in GitHub Actions
3. **Code review**: Manual review of commit messages in PRs

## Migration Guide

If you have existing commits that don't follow this standard, you can:

1. **Leave them as-is**: Don't rewrite history for existing commits
2. **Use conventional commits going forward**: Apply the standard to all new commits
3. **Squash and rewrite**: For feature branches, consider squashing commits before merging

## Resources

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Commitlint Documentation](https://commitlint.js.org/)
- [Angular Commit Message Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
- [Git Best Practices](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project)

## Questions?

If you have questions about commit message standards:

1. Check this documentation
2. Look at recent commits for examples
3. Ask in project discussions
4. Open an issue for clarification

Remember: Good commit messages make the project history more valuable and easier to navigate for everyone involved.
