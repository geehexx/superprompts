# Error Handling

Error handling patterns and debugging strategies for the SuperPrompts project.

## Exception Hierarchy

### Base Exceptions
- `SuperPromptsError` - Base exception for all SuperPrompts-specific errors
- `ConfigurationError` - Configuration-related errors
- `ValidationError` - Input validation errors
- `ServerError` - MCP server-related errors
- `PromptError` - Prompt-related errors
- `MCPError` - MCP protocol errors
- `CLIError` - CLI-related errors

## Error Handling Patterns

### Input Validation
```python
def validate_parameters(parameters: dict[str, Any]) -> dict[str, Any]:
    """Validate and sanitize parameters."""
    validated = parameters.copy()

    # Validate batch_size
    if "batch_size" in validated:
        batch_size = validated["batch_size"]
        if not isinstance(batch_size, int) or batch_size < 1 or batch_size > 10:
            raise ValidationError(f"Invalid batch_size: {batch_size}")

    return validated
```

### Resource Management
```python
def load_config_file(config_path: Path) -> dict[str, Any]:
    """Load configuration file with error handling."""
    try:
        if not config_path.exists():
            raise ConfigurationError(f"Configuration file not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        return config

    except json.JSONDecodeError as e:
        raise ConfigurationError(f"Invalid JSON in configuration file: {e}")
    except Exception as e:
        raise ConfigurationError(f"Error loading configuration file: {e}")
```

### Graceful Degradation
```python
def get_prompt_with_fallback(prompt_id: str, parameters: dict[str, Any]) -> str:
    """Get prompt with fallback to default."""
    try:
        return get_prompt(prompt_id, parameters)

    except PromptError as e:
        logger.warning(f"Failed to get prompt {prompt_id}: {e}")

        # Fallback to default prompt
        try:
            return get_prompt("default", {})
        except PromptError:
            raise PromptError("Failed to get prompt and fallback failed")
```

## Error Logging

### Basic Logging
```python
import logging

logger = logging.getLogger(__name__)

def handle_error(error: Exception, context: dict[str, Any] = None):
    """Handle and log errors with context."""
    logger.error(
        "Error occurred",
        error=str(error),
        error_type=type(error).__name__,
        context=context or {},
        exc_info=True
    )
```

### Structured Logging
```python
import structlog

logger = structlog.get_logger()

def log_performance(func):
    """Decorator to log function performance."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info("Function completed", function=func.__name__, duration=duration)
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error("Function failed", function=func.__name__, duration=duration, error=str(e))
            raise
    return wrapper
```

## Error Recovery

### Automatic Recovery
```python
def load_config_with_recovery(config_path: Path) -> dict[str, Any]:
    """Load configuration with automatic recovery."""
    try:
        return load_config_file(config_path)

    except ConfigurationError as e:
        logger.warning(f"Configuration error: {e}")

        # Try to create default configuration
        try:
            default_config = create_default_config()
            save_config_file(config_path, default_config)
            logger.info("Created default configuration")
            return default_config
        except Exception as recovery_error:
            logger.error(f"Failed to create default configuration: {recovery_error}")
            raise ConfigurationError(f"Configuration error and recovery failed: {e}")
```

### Manual Recovery
```python
def recover_from_error(error: Exception) -> bool:
    """Attempt to recover from error."""
    if isinstance(error, ConfigurationError):
        return recover_configuration()
    elif isinstance(error, ServerError):
        return recover_server()
    else:
        return False
```

## Debugging Strategies

### Debug Mode
```python
def enable_debug_mode():
    """Enable debug mode for troubleshooting."""
    import os
    import logging

    os.environ['SUPERPROMPTS_LOG_LEVEL'] = 'DEBUG'
    os.environ['PYTHONUNBUFFERED'] = '1'

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
```

### Error Reporting
```python
def generate_error_report(error: Exception, context: dict[str, Any] = None) -> dict[str, Any]:
    """Generate comprehensive error report."""
    return {
        'error': {
            'type': type(error).__name__,
            'message': str(error),
            'traceback': traceback.format_exc()
        },
        'context': context or {},
        'system_info': get_debug_info(),
        'timestamp': datetime.utcnow().isoformat(),
        'version': get_version()
    }
```

## Best Practices

### Exception Handling
1. Use specific exceptions - Don't catch generic Exception
2. Provide context - Include relevant information in error messages
3. Log errors - Always log errors with appropriate level
4. Handle gracefully - Provide fallbacks when possible
5. Document exceptions - Document when exceptions are raised

### Error Messages
1. Be descriptive - Explain what went wrong and why
2. Include context - Provide relevant context information
3. Suggest solutions - Offer potential fixes when possible
4. Use consistent format - Follow project conventions
5. Avoid technical jargon - Use user-friendly language

### Recovery
1. Plan for failures - Design with failure in mind
2. Implement fallbacks - Provide alternative approaches
3. Test recovery - Test error recovery scenarios
4. Monitor health - Implement health checks
5. Document recovery - Document recovery procedures
