#!/usr/bin/env python3
"""Tests for MCP configuration management functionality."""

import json
import shutil
import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from superprompts.mcp.config import (
    MCPConfigGenerator,
    MCPServerConfig,
    create_filesystem_server_config,
    create_github_server_config,
    create_superprompts_server_config,
    get_available_server_templates,
    validate_config,
)


class TestMCPServerConfig:
    """Test MCPServerConfig model."""

    def test_valid_server_config(self) -> None:
        """Test creating a valid server configuration."""
        config = MCPServerConfig(
            name="test-server",
            command="python",
            args=["-m", "test.server"],
            description="Test server",
            version="1.0.0",
        )

        assert config.name == "test-server"
        assert config.command == "python"
        assert config.args == ["-m", "test.server"]
        assert config.description == "Test server"
        assert config.version == "1.0.0"
        assert config.env is None
        assert config.cwd is None

    def test_minimal_server_config(self) -> None:
        """Test creating a minimal server configuration."""
        config = MCPServerConfig(name="minimal", command="echo")

        assert config.name == "minimal"
        assert config.command == "echo"
        assert config.args == []
        assert config.description is None
        assert config.version is None

    def test_invalid_server_config(self) -> None:
        """Test validation errors for invalid configurations."""
        with pytest.raises(ValidationError):
            MCPServerConfig()  # Missing required fields

        with pytest.raises(ValidationError):
            MCPServerConfig(name="test")  # Missing command


class TestMCPConfigGenerator:
    """Test MCPConfigGenerator functionality."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.generator = MCPConfigGenerator(self.temp_dir)

    def teardown_method(self) -> None:
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_generate_cursor_config(self) -> None:
        """Test generating Cursor-compatible configuration."""
        servers = {"test": MCPServerConfig(name="test", command="python", args=["-m", "test.server"])}

        config = self.generator.generate_cursor_config(servers)

        assert "mcpServers" in config
        assert "test" in config["mcpServers"]
        assert config["mcpServers"]["test"]["command"] == "python"
        assert config["mcpServers"]["test"]["args"] == ["-m", "test.server"]

    def test_generate_vscode_config(self) -> None:
        """Test generating VS Code-compatible configuration."""
        servers = {"test": MCPServerConfig(name="test", command="python", args=["-m", "test.server"])}

        config = self.generator.generate_vscode_config(servers)

        assert "mcp" in config
        assert "servers" in config["mcp"]
        assert "test" in config["mcp"]["servers"]
        assert config["mcp"]["servers"]["test"]["command"] == "python"

    def test_generate_generic_config(self) -> None:
        """Test generating generic configuration."""
        servers = {
            "test": MCPServerConfig(
                name="test",
                command="python",
                args=["-m", "test.server"],
                description="Test server",
                version="1.0.0",
            )
        }

        config = self.generator.generate_generic_config(servers)

        assert "mcp" in config
        assert config["mcp"]["version"] == "1.0.0"
        assert "servers" in config["mcp"]
        assert "test" in config["mcp"]["servers"]
        assert config["mcp"]["servers"]["test"]["name"] == "test"
        assert config["mcp"]["servers"]["test"]["description"] == "Test server"

    def test_save_config_cursor(self) -> None:
        """Test saving Cursor configuration."""
        servers = {"test": MCPServerConfig(name="test", command="python", args=["-m", "test.server"])}

        config = self.generator.generate_cursor_config(servers)
        output_path = self.generator.save_config(config, "cursor")

        assert output_path.name == "mcp.json"
        assert output_path.exists()

        with open(output_path) as f:
            saved_config = json.load(f)

        assert saved_config == config

    def test_save_config_vscode(self) -> None:
        """Test saving VS Code configuration."""
        servers = {"test": MCPServerConfig(name="test", command="python", args=["-m", "test.server"])}

        config = self.generator.generate_vscode_config(servers)
        output_path = self.generator.save_config(config, "vscode")

        assert output_path.parent.name == ".vscode"
        assert output_path.name == "mcp.json"
        assert output_path.exists()

    def test_save_config_generic(self) -> None:
        """Test saving generic configuration."""
        servers = {"test": MCPServerConfig(name="test", command="python", args=["-m", "test.server"])}

        config = self.generator.generate_generic_config(servers)
        output_path = self.generator.save_config(config, "generic")

        assert output_path.name == "mcp_config.json"
        assert output_path.exists()

    def test_save_config_custom_path(self) -> None:
        """Test saving configuration to custom path."""
        servers = {"test": MCPServerConfig(name="test", command="python", args=["-m", "test.server"])}

        config = self.generator.generate_cursor_config(servers)
        custom_path = self.temp_dir / "custom.json"
        output_path = self.generator.save_config(config, "cursor", custom_path)

        assert output_path == custom_path
        assert output_path.exists()

    def test_load_existing_config(self) -> None:
        """Test loading existing configuration."""
        # Create a test config file
        test_config = {"mcpServers": {"existing": {"command": "python", "args": ["-m", "existing.server"]}}}

        config_path = self.temp_dir / "mcp.json"
        with open(config_path, "w") as f:
            json.dump(test_config, f)

        loaded_config = self.generator.load_existing_config(config_path)
        assert loaded_config == test_config

    def test_load_nonexistent_config(self) -> None:
        """Test loading non-existent configuration."""
        config_path = self.temp_dir / "nonexistent.json"
        loaded_config = self.generator.load_existing_config(config_path)
        assert loaded_config is None

    def test_merge_configs_cursor(self) -> None:
        """Test merging configurations for Cursor format."""
        existing = {"mcpServers": {"existing": {"command": "python", "args": ["-m", "existing.server"]}}}

        new_servers = {"new": MCPServerConfig(name="new", command="node", args=["-e", "console.log('hello')"])}

        merged = self.generator.merge_configs(existing, new_servers, "cursor")

        assert "existing" in merged["mcpServers"]
        assert "new" in merged["mcpServers"]
        assert merged["mcpServers"]["new"]["command"] == "node"

    def test_merge_configs_vscode(self) -> None:
        """Test merging configurations for VS Code format."""
        existing = {"mcp": {"servers": {"existing": {"command": "python", "args": ["-m", "existing.server"]}}}}

        new_servers = {"new": MCPServerConfig(name="new", command="node", args=["-e", "console.log('hello')"])}

        merged = self.generator.merge_configs(existing, new_servers, "vscode")

        assert "existing" in merged["mcp"]["servers"]
        assert "new" in merged["mcp"]["servers"]
        assert merged["mcp"]["servers"]["new"]["command"] == "node"


class TestServerTemplates:
    """Test server configuration templates."""

    def test_superprompts_template(self) -> None:
        """Test SuperPrompts server template."""
        config = create_superprompts_server_config()

        assert config.name == "superprompts"
        assert config.command == "poetry"
        assert "superprompts.mcp.server" in " ".join(config.args)
        assert config.description is not None
        assert config.version == "1.0.0"

    def test_github_template(self) -> None:
        """Test GitHub server template."""
        config = create_github_server_config()

        assert config.name == "github"
        assert config.command == "npx"
        assert "github-mcp-server" in " ".join(config.args)
        assert config.description is not None

    def test_filesystem_template(self) -> None:
        """Test filesystem server template."""
        config = create_filesystem_server_config()

        assert config.name == "filesystem"
        assert config.command == "npx"
        assert "@modelcontextprotocol/server-filesystem" in " ".join(config.args)
        assert config.description is not None

    def test_get_available_templates(self) -> None:
        """Test getting available server templates."""
        templates = get_available_server_templates()

        assert "superprompts" in templates
        assert "github" in templates
        assert "filesystem" in templates

        for name, config in templates.items():
            assert isinstance(config, MCPServerConfig)
            assert config.name == name


class TestConfigValidation:
    """Test configuration validation."""

    def test_validate_cursor_config_valid(self) -> None:
        """Test validating valid Cursor configuration."""
        config = {"mcpServers": {"test": {"command": "python", "args": ["-m", "test.server"]}}}

        errors = validate_config(config, "cursor")
        assert len(errors) == 0

    def test_validate_cursor_config_invalid(self) -> None:
        """Test validating invalid Cursor configuration."""
        config = {"servers": {"test": {"command": "python"}}}  # Wrong key

        errors = validate_config(config, "cursor")
        assert len(errors) > 0
        assert any("mcpServers" in error for error in errors)

    def test_validate_vscode_config_valid(self) -> None:
        """Test validating valid VS Code configuration."""
        config = {"mcp": {"servers": {"test": {"command": "python", "args": ["-m", "test.server"]}}}}

        errors = validate_config(config, "vscode")
        assert len(errors) == 0

    def test_validate_vscode_config_invalid(self) -> None:
        """Test validating invalid VS Code configuration."""
        config = {"mcpServers": {"test": {"command": "python"}}}  # Wrong structure

        errors = validate_config(config, "vscode")
        assert len(errors) > 0

    def test_validate_generic_config_valid(self) -> None:
        """Test validating valid generic configuration."""
        config = {
            "mcp": {
                "version": "1.0.0",
                "servers": {
                    "test": {
                        "name": "test",
                        "command": "python",
                        "args": ["-m", "test.server"],
                    }
                },
            }
        }

        errors = validate_config(config, "generic")
        assert len(errors) == 0

    def test_validate_generic_config_invalid(self) -> None:
        """Test validating invalid generic configuration."""
        config = {
            "mcp": {
                "servers": {
                    "test": {
                        "command": "python"
                        # Missing required "name" field
                    }
                }
            }
        }

        errors = validate_config(config, "generic")
        assert len(errors) > 0


class TestIntegration:
    """Integration tests for MCP configuration management."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.generator = MCPConfigGenerator(self.temp_dir)

    def teardown_method(self) -> None:
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_full_workflow_cursor(self) -> None:
        """Test complete workflow for Cursor configuration."""
        # Create server configs
        servers = {
            "superprompts": create_superprompts_server_config(),
            "github": create_github_server_config(),
        }

        # Generate configuration
        config = self.generator.generate_cursor_config(servers)

        # Validate configuration
        errors = validate_config(config, "cursor")
        assert len(errors) == 0

        # Save configuration
        output_path = self.generator.save_config(config, "cursor")
        assert output_path.exists()

        # Load and verify configuration
        loaded_config = self.generator.load_existing_config(output_path)
        assert loaded_config == config

    def test_merge_workflow(self) -> None:
        """Test merging new servers into existing configuration."""
        # Create initial configuration
        initial_servers = {"existing": MCPServerConfig(name="existing", command="python", args=["-m", "existing.server"])}

        config = self.generator.generate_cursor_config(initial_servers)
        config_path = self.generator.save_config(config, "cursor")

        # Load existing configuration
        existing_config = self.generator.load_existing_config(config_path)
        assert existing_config is not None, "Failed to load existing config"

        # Add new servers
        new_servers = {
            "superprompts": create_superprompts_server_config(),
            "github": create_github_server_config(),
        }

        # Merge configurations
        merged_config = self.generator.merge_configs(existing_config, new_servers, "cursor")

        # Verify all servers are present
        assert "existing" in merged_config["mcpServers"]
        assert "superprompts" in merged_config["mcpServers"]
        assert "github" in merged_config["mcpServers"]

        # Validate merged configuration
        errors = validate_config(merged_config, "cursor")
        assert len(errors) == 0

    def test_format_conversion(self) -> None:
        """Test converting between different configuration formats."""
        # Start with Cursor format
        servers = {
            "test": MCPServerConfig(
                name="test",
                command="python",
                args=["-m", "test.server"],
                description="Test server",
                version="1.0.0",
            )
        }

        cursor_config = self.generator.generate_cursor_config(servers)

        # Convert to VS Code format
        vscode_config = self.generator.generate_vscode_config(servers)

        # Convert to generic format
        generic_config = self.generator.generate_generic_config(servers)

        # Validate all formats
        assert len(validate_config(cursor_config, "cursor")) == 0
        assert len(validate_config(vscode_config, "vscode")) == 0
        assert len(validate_config(generic_config, "generic")) == 0

        # Verify server is present in all formats
        assert "test" in cursor_config["mcpServers"]
        assert "test" in vscode_config["mcp"]["servers"]
        assert "test" in generic_config["mcp"]["servers"]
