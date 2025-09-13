# Security Guidelines

Security considerations and best practices for the SuperPrompts project.

## Security Principles

### Core Principles
1. **Defense in Depth** - Multiple layers of security controls
2. **Least Privilege** - Minimal necessary permissions
3. **Secure by Default** - Secure configuration out of the box
4. **Fail Secure** - System fails to secure state
5. **Input Validation** - Validate all inputs
6. **Output Encoding** - Encode all outputs

## Threat Model

### Identified Threats
- **Input Validation Attacks** - SQL injection, command injection, path traversal
- **Configuration Attacks** - Insecure configuration, sensitive data exposure
- **Network Attacks** - Man-in-the-middle, replay attacks, DoS
- **Application Attacks** - XSS, CSRF, session hijacking

## Security Measures

### Input Validation
```python
import re
from typing import Any, Dict

class InputValidator:
    """Validate and sanitize user inputs."""

    ALLOWED_PATTERNS = {
        'prompt_id': r'^[a-zA-Z0-9_-]+$',
        'file_path': r'^[a-zA-Z0-9_/.-]+$',
        'config_key': r'^[a-zA-Z0-9_.-]+$'
    }

    @classmethod
    def validate_prompt_id(cls, prompt_id: str) -> str:
        """Validate prompt ID."""
        if not isinstance(prompt_id, str):
            raise ValueError("Prompt ID must be a string")

        if not re.match(cls.ALLOWED_PATTERNS['prompt_id'], prompt_id):
            raise ValueError(f"Invalid prompt ID format: {prompt_id}")

        return prompt_id

    @classmethod
    def sanitize_string(cls, value: str) -> str:
        """Sanitize string input."""
        if not isinstance(value, str):
            raise ValueError("Value must be a string")

        # Remove null bytes and limit length
        value = value.replace('\x00', '')
        if len(value) > 10000:
            raise ValueError("String too long")

        return value
```

### Command Injection Prevention
```python
import shlex
from typing import List

class SecureCommandExecutor:
    """Execute commands securely."""

    @staticmethod
    def execute_command(command: str, args: List[str] = None) -> str:
        """Execute command with proper escaping."""
        # Validate command
        allowed_commands = ['python', 'uv', 'poetry', 'pytest', 'mypy', 'ruff']
        if command not in allowed_commands:
            raise ValueError(f"Command not allowed: {command}")

        # Escape arguments
        if args:
            escaped_args = [shlex.quote(arg) for arg in args]
            full_command = f"{command} {' '.join(escaped_args)}"
        else:
            full_command = command

        # Execute with subprocess
        import subprocess
        result = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {result.stderr}")

        return result.stdout
```

### Path Traversal Prevention
```python
import os
from pathlib import Path

class SecurePathHandler:
    """Handle file paths securely."""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()

    def get_secure_path(self, relative_path: str) -> Path:
        """Get secure path within base directory."""
        normalized_path = Path(relative_path).resolve()

        try:
            normalized_path.relative_to(self.base_path)
        except ValueError:
            raise ValueError(f"Path outside base directory: {relative_path}")

        return normalized_path
```

### Secure Configuration
```python
import os
from typing import Dict, Any

class SecureConfigManager:
    """Manage configuration securely."""

    def __init__(self, config_path: str):
        self.config_path = config_path

    def load_config(self) -> Dict[str, Any]:
        """Load configuration securely."""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            return config
        except FileNotFoundError:
            return self._create_default_config()
        except Exception as e:
            raise ValueError(f"Failed to load configuration: {e}")

    def _sanitize_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive data from configuration."""
        sensitive_keys = ['password', 'secret', 'key', 'token', 'credential']
        safe_config = {}

        for key, value in config.items():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                safe_config[key] = '[REDACTED]'
            else:
                safe_config[key] = value

        return safe_config
```

## Security Monitoring

### Security Logging
```python
import logging
import json
from datetime import datetime

class SecurityLogger:
    """Log security events."""

    def __init__(self):
        self.logger = logging.getLogger('security')
        self.logger.setLevel(logging.INFO)

    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security event."""
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'details': details,
            'severity': self._get_severity(event_type)
        }

        self.logger.info(json.dumps(event))

    def log_authentication_attempt(self, user: str, success: bool, ip: str = None):
        """Log authentication attempt."""
        self.log_security_event('authentication_attempt', {
            'user': user,
            'success': success,
            'ip': ip
        })
```

### Security Auditing
```python
class SecurityAuditor:
    """Audit security events and generate reports."""

    def __init__(self, log_file: str = 'security.log'):
        self.log_file = log_file

    def generate_security_report(self) -> Dict[str, Any]:
        """Generate security audit report."""
        events = self._parse_security_events()

        return {
            'total_events': len(events),
            'event_types': self._count_event_types(events),
            'failed_authentications': self._count_failed_auths(events),
            'authorization_failures': self._count_authz_failures(events),
            'recent_events': events[-10:] if events else []
        }
```

## Security Testing

### Automated Security Testing
```python
import pytest
from unittest.mock import patch, MagicMock

class TestSecurity:
    """Security test suite."""

    def test_input_validation(self):
        """Test input validation."""
        validator = InputValidator()

        # Test valid input
        assert validator.validate_prompt_id("test_prompt") == "test_prompt"

        # Test invalid input
        with pytest.raises(ValueError):
            validator.validate_prompt_id("test<script>")

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention."""
        malicious_input = "'; DROP TABLE users; --"
        sanitized = InputValidator.sanitize_string(malicious_input)
        assert "DROP TABLE" not in sanitized

    def test_path_traversal_prevention(self):
        """Test path traversal prevention."""
        handler = SecurePathHandler("/safe/base")

        # Test valid path
        assert handler.get_secure_path("config.json").name == "config.json"

        # Test path traversal
        with pytest.raises(ValueError):
            handler.get_secure_path("../../../etc/passwd")
```

### Security Scanning
```bash
# Install Bandit
uv add --dev bandit

# Run security scan
uv run bandit -r superprompts/ -f json -o bandit-report.json

# Install Safety
uv add --dev safety

# Scan dependencies
uv run safety check
```

## Best Practices

### Code Security
1. Always validate inputs
2. Use parameterized queries
3. Implement proper error handling
4. Use secure random number generation
5. Implement proper session management

### Configuration Security
1. Use environment variables for secrets
2. Validate configuration
3. Use secure defaults
4. Encrypt sensitive data
5. Rotate secrets regularly

### Deployment Security
1. Use secure file permissions
2. Validate SSL certificates
3. Implement health checks
4. Monitor security events
5. Keep dependencies updated

### Incident Response
1. Classify incidents by severity
2. Implement escalation procedures
3. Monitor security events in real-time
4. Document security procedures
5. Regular security audits
