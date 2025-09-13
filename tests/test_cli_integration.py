#!/usr/bin/env python3
"""Integration tests for CLI commands.

These tests verify that the CLI commands work correctly
and handle various scenarios appropriately.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from superprompts.mcp.adapters import MCPFormatConverter, MCPToolingAdapter, create_adapter_cli_commands


class TestCLIIntegration:
    """Test CLI command integration."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_tools_command(self):
        """Test the tools command."""
        import click

        @click.group()
        def cli():
            pass

        create_adapter_cli_commands(cli)

        with patch.object(MCPToolingAdapter, "_detect_available_tools") as mock_detect:
            mock_detect.return_value = {"fastmcp": True, "mcp-cli": False, "mcp-tools-cli": True, "npm": True}

            result = self.runner.invoke(cli, ["adapt", "tools"])
            assert result.exit_code == 0
            assert "Available MCP Tools" in result.output
            assert "fastmcp" in result.output

    def test_fastmcp_command_success(self):
        """Test successful FastMCP configuration generation."""
        import click

        @click.group()
        def cli():
            pass

        create_adapter_cli_commands(cli)

        mock_config = {"mcpServers": {"test-server": {"command": "fastmcp", "args": ["test"]}}}

        with patch.object(MCPToolingAdapter, "generate_fastmcp_config") as mock_gen:
            mock_gen.return_value = mock_config

            result = self.runner.invoke(cli, ["adapt", "fastmcp", "test-server", "/path/to/server"])
            assert result.exit_code == 0
            mock_gen.assert_called_once()

    def test_fastmcp_command_with_output(self):
        """Test FastMCP configuration generation with output file."""
        import click

        @click.group()
        def cli():
            pass

        create_adapter_cli_commands(cli)

        mock_config = {"mcpServers": {"test-server": {"command": "fastmcp", "args": ["test"]}}}

        output_file = self.temp_dir / "config.json"

        with patch.object(MCPToolingAdapter, "generate_fastmcp_config") as mock_gen:
            mock_gen.return_value = mock_config

            result = self.runner.invoke(cli, ["adapt", "fastmcp", "test-server", "/path/to/server", "--output", str(output_file)])
            assert result.exit_code == 0
            assert output_file.exists()

            with output_file.open() as f:
                saved_config = json.load(f)
            assert saved_config == mock_config

    def test_fastmcp_command_failure(self):
        """Test FastMCP configuration generation failure."""
        import click

        @click.group()
        def cli():
            pass

        create_adapter_cli_commands(cli)

        with patch.object(MCPToolingAdapter, "generate_fastmcp_config") as mock_gen:
            mock_gen.return_value = None

            result = self.runner.invoke(cli, ["adapt", "fastmcp", "test-server", "/path/to/server"])
            assert result.exit_code == 0
            assert "No configuration generated" in result.output

    def test_install_command(self):
        """Test the install command."""
        import click

        @click.group()
        def cli():
            pass

        create_adapter_cli_commands(cli)

        with patch.object(MCPToolingAdapter, "install_mcp_server") as mock_install:
            mock_install.return_value = True

            result = self.runner.invoke(cli, ["adapt", "install", "test-package"])
            assert result.exit_code == 0
            mock_install.assert_called_once_with("test-package", "test-package")

    def test_list_servers_command(self):
        """Test the list servers command."""
        import click

        @click.group()
        def cli():
            pass

        create_adapter_cli_commands(cli)

        with patch.object(MCPToolingAdapter, "list_installed_servers") as mock_list:
            mock_list.return_value = ["server1", "server2"]

            result = self.runner.invoke(cli, ["adapt", "list-servers"])
            assert result.exit_code == 0
            assert "MCP" in result.output  # Less specific match to account for table formatting
            assert "server1" in result.output
            assert "server2" in result.output

    def test_list_servers_empty(self):
        """Test the list servers command with no servers."""
        import click

        @click.group()
        def cli():
            pass

        create_adapter_cli_commands(cli)

        with patch.object(MCPToolingAdapter, "list_installed_servers") as mock_list:
            mock_list.return_value = []

            result = self.runner.invoke(cli, ["adapt", "list-servers"])
            assert result.exit_code == 0
            assert "No installed servers found" in result.output

    def test_test_command(self):
        """Test the test command."""
        import click

        @click.group()
        def cli():
            pass

        create_adapter_cli_commands(cli)

        with patch.object(MCPToolingAdapter, "test_mcp_server") as mock_test:
            mock_test.return_value = True

            result = self.runner.invoke(cli, ["adapt", "test", "test-server"])
            assert result.exit_code == 0
            mock_test.assert_called_once_with("test-server", None)

    def test_test_command_with_tool(self):
        """Test the test command with specific tool."""
        import click

        @click.group()
        def cli():
            pass

        create_adapter_cli_commands(cli)

        with patch.object(MCPToolingAdapter, "test_mcp_server") as mock_test:
            mock_test.return_value = True

            result = self.runner.invoke(cli, ["adapt", "test", "test-server", "--tool", "test-tool"])
            assert result.exit_code == 0
            mock_test.assert_called_once_with("test-server", "test-tool")

    def test_from_openapi_command(self):
        """Test the from-openapi command."""
        import click

        @click.group()
        def cli():
            pass

        create_adapter_cli_commands(cli)

        mock_config = {"mcpServers": {"api-server": {"command": "npx", "args": ["-y", "openapi-mcp-server", "openapi.json"]}}}

        with patch.object(MCPFormatConverter, "convert_from_openapi") as mock_convert:
            mock_convert.return_value = mock_config

            result = self.runner.invoke(cli, ["adapt", "from-openapi", "openapi.json", "api-server"])
            assert result.exit_code == 0
            mock_convert.assert_called_once_with("openapi.json", "api-server")

    def test_from_docker_command(self):
        """Test the from-docker command."""
        import click

        @click.group()
        def cli():
            pass

        create_adapter_cli_commands(cli)

        mock_config = {"mcpServers": {"docker-service": {"command": "docker", "args": ["compose", "exec", "docker-service"]}}}

        with patch.object(MCPFormatConverter, "convert_from_docker_compose") as mock_convert:
            mock_convert.return_value = mock_config

            result = self.runner.invoke(cli, ["adapt", "from-docker", "docker-compose.yml", "docker-service"])
            assert result.exit_code == 0
            mock_convert.assert_called_once_with("docker-compose.yml", "docker-service")

    def test_from_npm_command(self):
        """Test the from-npm command."""
        import click

        @click.group()
        def cli():
            pass

        create_adapter_cli_commands(cli)

        mock_config = {"mcpServers": {"npm-script": {"command": "npm", "args": ["run", "npm-script"]}}}

        with patch.object(MCPFormatConverter, "convert_from_package_json") as mock_convert:
            mock_convert.return_value = mock_config

            result = self.runner.invoke(cli, ["adapt", "from-npm", "package.json", "npm-script"])
            assert result.exit_code == 0
            mock_convert.assert_called_once_with("package.json", "npm-script")

    def test_error_handling(self):
        """Test error handling in CLI commands."""
        import click

        @click.group()
        def cli():
            pass

        create_adapter_cli_commands(cli)

        with patch.object(MCPToolingAdapter, "generate_fastmcp_config") as mock_gen:
            mock_gen.side_effect = Exception("Test error")

            result = self.runner.invoke(cli, ["adapt", "fastmcp", "test-server", "/path/to/server"])
            assert result.exit_code == 0
            assert "Unexpected error" in result.output


class TestFormatConverter:
    """Test format converter functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = MCPFormatConverter()
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_openapi_conversion(self):
        """Test OpenAPI to MCP conversion."""
        openapi_spec = {
            "openapi": "3.0.0",
            "info": {"title": "Test API", "version": "1.0.0"},
            "servers": [{"url": "https://api.example.com"}],
        }

        result = self.converter.convert_from_openapi(openapi_spec, "test-api")
        assert result is not None
        assert "mcpServers" in result
        assert "test-api" in result["mcpServers"]

    def test_docker_compose_conversion(self):
        """Test Docker Compose to MCP conversion."""
        compose_file = self.temp_dir / "docker-compose.yml"
        compose_data = {"services": {"web": {"image": "nginx", "command": ["nginx", "-g", "daemon off;"]}}}

        with compose_file.open("w") as f:
            json.dump(compose_data, f)

        result = self.converter.convert_from_docker_compose(str(compose_file), "web")
        assert result is not None
        assert "mcpServers" in result
        assert "web" in result["mcpServers"]

    def test_package_json_conversion(self):
        """Test package.json to MCP conversion."""
        package_file = self.temp_dir / "package.json"
        package_data = {"name": "test-package", "version": "1.0.0", "scripts": {"start": "node server.js", "test": "npm test"}}

        with package_file.open("w") as f:
            json.dump(package_data, f)

        result = self.converter.convert_from_package_json(str(package_file), "start")
        assert result is not None
        assert "mcpServers" in result
        assert "start" in result["mcpServers"]
