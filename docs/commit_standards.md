# Commit Message Standards

Complete guide to Git commit message conventions and best practices for the SuperPrompts project.

## Overview

The project uses [Conventional Commits](https://www.conventionalcommits.org/) specification with custom scope requirements. Commit messages are validated using [commitlint](https://commitlint.js.org/) to ensure consistency and quality.

## Configuration

The commit message standards are defined in `commitlint.config.js`:

```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', ['feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'build', 'ci', 'chore', 'revert']],
    'scope-enum': [2, 'always', ['cli', 'mcp', 'prompts', 'docs', 'tests', 'config', 'ci', 'deps', 'build', 'chore']],
    'subject-case': [2, 'always', 'lower-case'],
    'subject-max-length': [2, 'always', 50],
    'body-max-line-length': [2, 'always', 72],
    'header-max-length': [2, 'always', 50]
  }
};
```

## Commit Message Format

### Basic Structure
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Required Components

#### Type (Required)
The type of change being made:

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(cli): add new command for prompt generation` |
| `fix` | Bug fix | `fix(mcp): resolve server connection timeout` |
| `docs` | Documentation changes | `docs(api): update API reference with examples` |
| `style` | Code style changes (formatting, etc.) | `style(prompts): format prompt templates` |
| `refactor` | Code refactoring | `refactor(config): simplify configuration loading` |
| `perf` | Performance improvements | `perf(mcp): optimize server response time` |
| `test` | Test additions or changes | `test(cli): add integration tests for config commands` |
| `build` | Build system changes | `build(deps): update dependencies to latest versions` |
| `ci` | CI/CD changes | `ci(workflows): add security scanning to GitHub Actions` |
| `chore` | Maintenance tasks | `chore(deps): update development dependencies` |
| `revert` | Revert previous commit | `revert(cli): revert changes to command parsing` |

#### Scope (Required)
The area of the codebase affected:

| Scope | Description | Example |
|-------|-------------|---------|
| `cli` | Command-line interface | `feat(cli): add new command` |
| `mcp` | MCP server and tools | `fix(mcp): resolve server error` |
| `prompts` | Prompt system | `feat(prompts): add new prompt type` |
| `docs` | Documentation | `docs(api): update reference` |
| `tests` | Test suite | `test(integration): add server tests` |
| `config` | Configuration management | `refactor(config): simplify config loading` |
| `ci` | CI/CD pipeline | `ci(workflows): update GitHub Actions` |
| `deps` | Dependencies | `build(deps): update package versions` |
| `build` | Build system | `build(tools): update build configuration` |
| `chore` | Maintenance | `chore(cleanup): remove unused files` |

#### Subject (Required)
Brief description of the change:

- **Format**: Lowercase, no period at end
- **Length**: Maximum 50 characters
- **Content**: Imperative mood ("add feature" not "added feature")

**Examples:**
- ✅ `feat(cli): add new command for prompt generation`
- ✅ `fix(mcp): resolve server connection timeout`
- ❌ `feat(cli): Added new command for prompt generation.`
- ❌ `fix(mcp): resolves server connection timeout issue that was causing problems`

### Optional Components

#### Body (Optional)
Detailed explanation of the change:

- **Length**: Maximum 72 characters per line
- **Content**: Explain what and why, not how
- **Format**: Use blank line to separate from subject

**Example:**
```
feat(cli): add new command for prompt generation

Add a new 'generate' command that allows users to create
custom prompts with parameters. This command supports
interactive mode and batch processing.

The command integrates with the existing prompt system
and provides validation for user inputs.
```

#### Footer (Optional)
Additional metadata:

- **Breaking changes**: `BREAKING CHANGE: description`
- **Issue references**: `Closes #123`, `Fixes #456`
- **Co-authors**: `Co-authored-by: Name <email>`

**Example:**
```
feat(cli): add new command for prompt generation

Add a new 'generate' command that allows users to create
custom prompts with parameters.

BREAKING CHANGE: The 'create' command has been renamed to 'generate'
Closes #123
Co-authored-by: Jane Doe <jane@example.com>
```

## Validation Rules

### Type Validation
- **Required**: Must be one of the allowed types
- **Case**: Must be lowercase
- **Format**: Must be followed by colon and space

### Scope Validation
- **Required**: Must be one of the allowed scopes
- **Case**: Must be lowercase
- **Format**: Must be in parentheses

### Subject Validation
- **Required**: Must be present
- **Case**: Must be lowercase
- **Length**: Maximum 50 characters
- **Format**: No period at end

### Body Validation
- **Length**: Maximum 72 characters per line
- **Format**: Use blank line to separate from subject

### Header Validation
- **Length**: Maximum 50 characters total
- **Format**: `<type>(<scope>): <subject>`

## Examples

### Good Commit Messages

#### Simple Feature
```
feat(cli): add list-prompts command
```

#### Feature with Body
```
feat(mcp): add server health check endpoint

Add a new /health endpoint that returns server status
and version information. This endpoint can be used
for monitoring and load balancer health checks.
```

#### Bug Fix
```
fix(prompts): resolve parameter validation error

Fix issue where invalid parameters caused server to
crash instead of returning proper error message.
```

#### Documentation Update
```
docs(api): update MCP server API reference

Add comprehensive examples for all MCP server tools
and include parameter validation details.
```

#### Breaking Change
```
feat(cli): rename create command to generate

BREAKING CHANGE: The 'create' command has been renamed
to 'generate' for consistency with other commands.
```

### Bad Commit Messages

#### Missing Type
```
❌ add new command
```

#### Missing Scope
```
❌ feat: add new command
```

#### Wrong Case
```
❌ Feat(CLI): Add new command
```

#### Too Long Subject
```
❌ feat(cli): add new command for prompt generation with parameters and validation
```

#### Wrong Format
```
❌ feat(cli): Added new command for prompt generation.
```

## Usage

### Pre-commit Validation
Commit messages are automatically validated on commit:

```bash
# Commit with valid message
git commit -m "feat(cli): add new command"

# Commit with invalid message (will fail)
git commit -m "add new command"
```

### Manual Validation
```bash
# Validate last commit
npx commitlint --from HEAD~1 --to HEAD --verbose

# Validate specific commit
npx commitlint --from abc123 --to def456 --verbose
```

### Bypass Validation
```bash
# Skip validation (not recommended)
git commit -m "feat(cli): add new command" --no-verify
```

## Best Practices

### Writing Good Commit Messages

#### 1. Use Imperative Mood
- ✅ `feat(cli): add new command`
- ❌ `feat(cli): added new command`

#### 2. Be Specific and Concise
- ✅ `fix(mcp): resolve server timeout`
- ❌ `fix(mcp): fix server issues`

#### 3. Use Present Tense
- ✅ `feat(prompts): add new prompt type`
- ❌ `feat(prompts): added new prompt type`

#### 4. Capitalize Properly
- ✅ `feat(cli): add new command`
- ❌ `feat(cli): Add new command`

#### 5. Keep Subject Under 50 Characters
- ✅ `feat(cli): add new command`
- ❌ `feat(cli): add new command for prompt generation with parameters`

### Scope Selection

#### Choose the Most Specific Scope
- ✅ `feat(cli): add new command` (if it's CLI-specific)
- ✅ `feat(mcp): add new tool` (if it's MCP-specific)
- ❌ `feat(chore): add new command` (too generic)

#### Use Appropriate Scope for Changes
- **`cli`**: Command-line interface changes
- **`mcp`**: MCP server and tools
- **`prompts`**: Prompt system changes
- **`docs`**: Documentation updates
- **`tests`**: Test additions or changes
- **`config`**: Configuration management
- **`ci`**: CI/CD pipeline changes
- **`deps`**: Dependency updates
- **`build`**: Build system changes
- **`chore`**: Maintenance tasks

### Body Writing

#### Explain What and Why
```bash
feat(cli): add new command for prompt generation

Add a new 'generate' command that allows users to create
custom prompts with parameters. This command supports
interactive mode and batch processing.

The command integrates with the existing prompt system
and provides validation for user inputs.
```

#### Use Bullet Points for Multiple Changes
```bash
feat(cli): add new command for prompt generation

- Add interactive mode for parameter input
- Add batch processing for multiple prompts
- Add validation for user inputs
- Add help text and examples
```

## Common Patterns

### Feature Development
```bash
# Initial feature
feat(cli): add new command for prompt generation

# Add tests
test(cli): add tests for new command

# Add documentation
docs(cli): document new command usage

# Fix issues
fix(cli): resolve parameter validation error

# Refactor
refactor(cli): simplify command parsing
```

### Bug Fixes
```bash
# Fix bug
fix(mcp): resolve server connection timeout

# Add test for bug
test(mcp): add test for connection timeout

# Update documentation
docs(mcp): update server troubleshooting guide
```

### Documentation Updates
```bash
# Update API docs
docs(api): update MCP server API reference

# Update user guide
docs(guide): update quick start guide

# Fix documentation
docs(api): fix broken links in API reference
```

### Dependency Updates
```bash
# Update dependencies
build(deps): update dependencies to latest versions

# Update specific dependency
build(deps): update fastmcp to v2.12.0

# Security update
build(deps): update dependencies for security fixes
```

## Troubleshooting

### Common Validation Errors

#### Missing Type
```
❌ add new command
```
**Fix:** Add type prefix
```
✅ feat(cli): add new command
```

#### Missing Scope
```
❌ feat: add new command
```
**Fix:** Add scope in parentheses
```
✅ feat(cli): add new command
```

#### Wrong Case
```
❌ Feat(CLI): Add new command
```
**Fix:** Use lowercase
```
✅ feat(cli): add new command
```

#### Subject Too Long
```
❌ feat(cli): add new command for prompt generation with parameters and validation
```
**Fix:** Shorten subject
```
✅ feat(cli): add new command for prompt generation
```

#### Missing Colon
```
❌ feat(cli) add new command
```
**Fix:** Add colon and space
```
✅ feat(cli): add new command
```

### Getting Help

#### Check Configuration
```bash
# View commitlint configuration
cat commitlint.config.js
```

#### Validate Manually
```bash
# Validate specific message
echo "feat(cli): add new command" | npx commitlint
```

#### Debug Mode
```bash
# Run with debug output
npx commitlint --from HEAD~1 --to HEAD --verbose
```

## Integration

### Pre-commit Hooks
Commit message validation is integrated with pre-commit hooks:

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/commitlint/commitlint
  rev: v19.8.1
  hooks:
    - id: commitlint
```

### CI/CD Integration
Commit messages are validated in CI:

```yaml
# .github/workflows/ci.yml
- name: Validate commit messages
  run: npx commitlint --from HEAD~1 --to HEAD
```

### IDE Integration
Many IDEs support commit message validation:

- **VS Code**: Conventional Commits extension
- **PyCharm**: Commitlint plugin
- **Vim**: Commitlint plugin
- **Emacs**: Commitlint mode

## Cross-References

- [Development](development.md) - Complete development setup
- [Pre-commit](pre_commit.md) - Pre-commit hooks
- [CI/CD Workflows Guide](ci_cd_workflows.md) - CI/CD integration
- [Contributing Guide](contributing_guide.md) - How to contribute
