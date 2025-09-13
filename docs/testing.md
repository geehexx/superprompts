# Testing Strategy Guide

Complete guide to the testing approach, organization, and best practices for the SuperPrompts project.

## Overview

The project uses a comprehensive testing strategy with multiple testing frameworks and approaches:

- **pytest** - Main testing framework
- **Nox** - Multi-environment testing
- **GitHub Actions** - CI/CD testing
- **Coverage reporting** - Test coverage analysis

## Test Organization

### Directory Structure
```
tests/
├── __pycache__/          # Python cache files
├── test_cli_integration.py  # CLI integration tests
├── test_mcp_config.py      # MCP configuration tests
├── test_server.py          # MCP server tests
└── test_startup.py         # Startup and initialization tests
```

### Test Categories

#### 1. Unit Tests
Test individual functions and classes in isolation.

**Location:** Individual test files
**Framework:** pytest
**Coverage:** High (90%+)

#### 2. Integration Tests
Test interaction between components.

**Location:** `test_cli_integration.py`, `test_server.py`
**Framework:** pytest
**Coverage:** Medium (70%+)

#### 3. Startup Tests
Test application initialization and startup.

**Location:** `test_startup.py`
**Framework:** pytest
**Coverage:** High (90%+)

#### 4. Configuration Tests
Test configuration loading and validation.

**Location:** `test_mcp_config.py`
**Framework:** pytest
**Coverage:** High (90%+)

## Test Files

### test_startup.py
Tests application startup and initialization.

**Key Tests:**
- Import validation
- Module loading
- Basic functionality
- Error handling

**Example:**
```python
def test_import_superprompts():
    """Test that superprompts can be imported."""
    import superprompts
    assert hasattr(superprompts, '__version__')

def test_mcp_server_startup():
    """Test MCP server can start."""
    from superprompts.mcp.server import main
    # Test server startup
```

### test_server.py
Tests MCP server functionality.

**Key Tests:**
- Server initialization
- Tool registration
- Request handling
- Error responses

**Example:**
```python
def test_list_prompts():
    """Test list_prompts tool."""
    from superprompts.mcp.server import list_prompts
    result = await list_prompts()
    assert isinstance(result, list)

def test_get_prompt():
    """Test get_prompt tool."""
    from superprompts.mcp.server import get_prompt
    result = await get_prompt("repo_docs")
    assert isinstance(result, str)
```

### test_cli_integration.py
Tests CLI integration and commands.

**Key Tests:**
- Command execution
- Parameter validation
- Output formatting
- Error handling

**Example:**
```python
def test_list_prompts_command():
    """Test list-prompts CLI command."""
    from superprompts.cli.main import list_prompts_cmd
    # Test command execution

def test_get_prompt_command():
    """Test get-prompt CLI command."""
    from superprompts.cli.main import get_prompt_cmd
    # Test command execution
```

### test_mcp_config.py
Tests MCP configuration management.

**Key Tests:**
- Configuration loading
- Validation
- Format conversion
- Error handling

**Example:**
```python
def test_config_validation():
    """Test MCP configuration validation."""
    # Configuration validation is now handled by the MCP client
    # See the MCP Configuration Guide for details

def test_config_generation():
    """Test MCP configuration generation."""
    from superprompts.mcp.config import MCPServerConfig
    config = MCPServerConfig(name="test", command="test")
    assert config.name == "test"
    assert config.command == "test"
```

## Running Tests

### Basic Test Execution

#### Run All Tests
```bash
# Using pytest directly
uv run pytest tests/ -v

# Using invoke
uv run invoke test

# Using nox
uv run nox -s test
```

#### Run Specific Test Files
```bash
# Run specific test file
uv run pytest tests/test_startup.py -v

# Run specific test function
uv run pytest tests/test_startup.py::test_import_superprompts -v
```

#### Run Tests by Category
```bash
# Run unit tests
uv run invoke test --unit

# Run integration tests
uv run invoke test --integration

# Run startup tests
uv run invoke test --startup
```

### Coverage Analysis

#### Run with Coverage
```bash
# Using pytest with coverage
uv run pytest tests/ --cov=superprompts --cov-report=html --cov-report=term

# Using invoke
uv run invoke test --coverage

# Using nox
uv run nox -s coverage
```

#### Coverage Reports
- **Terminal**: Shows coverage summary
- **HTML**: Generates `htmlcov/index.html` for detailed coverage
- **JSON**: Generates coverage data for CI/CD

### Multi-Environment Testing

#### Using Nox
```bash
# Run tests on all Python versions
uv run nox -s test

# Run tests on specific Python version
uv run nox -s test-3.11
uv run nox -s test-3.12
```

#### Python Versions Tested
- Python 3.10
- Python 3.11
- Python 3.12

## Test Configuration

### pytest Configuration
Located in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
asyncio_mode = "auto"
```

### Coverage Configuration
```toml
[tool.coverage.run]
source = ["superprompts"]
omit = ["tests/*", "venv/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

## Writing Tests

### Test Structure

#### Basic Test Function
```python
def test_function_name():
    """Test description."""
    # Arrange
    input_data = "test"

    # Act
    result = function_under_test(input_data)

    # Assert
    assert result == "expected"
```

#### Async Test Function
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await async_function_under_test()
    assert result is not None
```

#### Test Class
```python
class TestClassName:
    """Test class for specific functionality."""

    def test_method(self):
        """Test specific method."""
        assert True

    def test_another_method(self):
        """Test another method."""
        assert True
```

### Test Fixtures

#### Basic Fixture
```python
import pytest

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {"key": "value"}

def test_with_fixture(sample_data):
    """Test using fixture."""
    assert sample_data["key"] == "value"
```

#### Async Fixture
```python
@pytest.fixture
async def async_fixture():
    """Provide async fixture."""
    # Setup
    yield "async_data"
    # Teardown
```

### Assertions

#### Basic Assertions
```python
def test_basic_assertions():
    """Test basic assertions."""
    assert True
    assert 1 == 1
    assert "hello" in "hello world"
    assert isinstance([], list)
```

#### Exception Testing
```python
def test_exception():
    """Test exception handling."""
    with pytest.raises(ValueError):
        raise ValueError("test error")

    with pytest.raises(ValueError, match="test error"):
        raise ValueError("test error message")
```

#### Async Exception Testing
```python
@pytest.mark.asyncio
async def test_async_exception():
    """Test async exception handling."""
    with pytest.raises(ValueError):
        await async_function_that_raises()
```

## Test Best Practices

### Naming Conventions

#### Test Functions
- **Format**: `test_<function_name>_<scenario>`
- **Examples**:
  - `test_get_prompt_success`
  - `test_get_prompt_invalid_id`

#### Test Classes
- **Format**: `Test<ClassName>`
- **Examples**:
  - `TestMCPServer`
  - `TestConfigGenerator`
  - `TestPromptHandler`

### Test Organization

#### Group Related Tests
```python
class TestMCPServer:
    """Test MCP server functionality."""

    def test_server_initialization(self):
        """Test server initialization."""
        pass

    def test_tool_registration(self):
        """Test tool registration."""
        pass

    def test_request_handling(self):
        """Test request handling."""
        pass
```

#### Use Descriptive Names
```python
def test_get_prompt_returns_string_for_valid_id():
    """Test that get_prompt returns string for valid ID."""
    pass

def test_get_prompt_raises_error_for_invalid_id():
    """Test that get_prompt raises error for invalid ID."""
    pass
```

### Test Data

#### Use Fixtures for Common Data
```python
@pytest.fixture
def sample_prompt_data():
    """Provide sample prompt data."""
    return {
        "id": "test_prompt",
        "name": "Test Prompt",
        "description": "A test prompt"
    }
```

#### Use Parametrized Tests
```python
@pytest.mark.parametrize("input_data,expected", [
    ("valid", True),
    ("invalid", False),
    ("", False),
])
def test_validation(input_data, expected):
    """Test validation with different inputs."""
    result = validate_input(input_data)
    assert result == expected
```

### Mocking and Patching

#### Mock External Dependencies
```python
from unittest.mock import patch, MagicMock

@patch('superprompts.mcp.server.fastmcp')
def test_server_with_mock(mock_fastmcp):
    """Test server with mocked FastMCP."""
    mock_fastmcp.FastMCP.return_value = MagicMock()
    # Test server initialization
```

#### Mock Async Functions
```python
@pytest.mark.asyncio
async def test_async_with_mock():
    """Test async function with mock."""
    with patch('superprompts.mcp.server.async_function') as mock_func:
        mock_func.return_value = "mocked_result"
        result = await function_under_test()
        assert result == "mocked_result"
```

## CI/CD Integration

### GitHub Actions
Tests run automatically in CI:

```yaml
# .github/workflows/ci.yml
- name: Run tests
  run: poetry run pytest tests/ -v

- name: Run tests with coverage
  run: poetry run pytest tests/ --cov=superprompts --cov-report=html
```

### Pre-commit Hooks
Tests run before commit:

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: pytest
      name: pytest
      entry: pytest tests/ -v
      language: python
      types: [python]
```

## Troubleshooting

### Common Issues

#### Test Failures
```bash
# Run specific failing test
uv run pytest tests/test_specific.py::test_function -v

# Run with verbose output
uv run pytest tests/ -v -s

# Run with debug output
uv run pytest tests/ --pdb
```

#### Import Errors
```bash
# Check Python path
uv run python -c "import sys; print(sys.path)"

# Check module installation
uv run python -c "import superprompts; print(superprompts.__file__)"
```

#### Async Test Issues
```bash
# Run async tests specifically
uv run pytest tests/ -k "async" -v

# Check asyncio mode
uv run pytest tests/ --asyncio-mode=auto
```

### Debug Mode

#### Run with Debugger
```bash
# Run with Python debugger
uv run pytest tests/ --pdb

# Run specific test with debugger
uv run pytest tests/test_specific.py::test_function --pdb
```

#### Verbose Output
```bash
# Maximum verbosity
uv run pytest tests/ -vvv

# Show local variables on failure
uv run pytest tests/ -l
```

## Coverage Goals

### Current Coverage
- **Target**: 90%+ overall coverage
- **Critical modules**: 95%+ coverage
- **Test files**: Excluded from coverage

### Coverage by Module
- **superprompts.mcp.server**: 95%+
- **superprompts.cli.main**: 90%+
- **superprompts.prompts.base**: 95%+
- **superprompts.mcp.config**: 90%+

### Coverage Reports
- **Terminal**: Shows coverage summary
- **HTML**: Detailed coverage report in `htmlcov/`
- **CI/CD**: Coverage data uploaded as artifacts

## Cross-References

- [Development](development.md) - Complete development setup
- [Nox Sessions](noxfile.py) - Multi-environment testing
- [CI/CD Workflows Guide](ci_cd_workflows.md) - CI/CD integration
- [Contributing Guide](contributing_guide.md) - How to contribute
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
