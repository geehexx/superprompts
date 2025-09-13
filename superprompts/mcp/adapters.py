#!/usr/bin/env python3
"""MCP Configuration Adapters.

This module provides adapters for integrating with existing MCP tooling
and making it easier to adapt configurations to different specifications.
"""

import json
import logging
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .config import MCPConfigGenerator, MCPServerConfig

# Set up logging
logger = logging.getLogger(__name__)

console = Console()


def _save_or_display_config(config: dict[str, Any] | None, output: str | None, title: str) -> None:
    """Save config to file or display it."""
    if not config:
        console.print("[yellow]No configuration generated[/yellow]")
        return

    if output:
        try:
            output_path = Path(output)
            # Create parent directories if they don't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with output_path.open("w") as f:
                json.dump(config, f, indent=2)
            logger.info("Configuration saved to: %s", output)
            console.print(f"[green]Configuration saved to: {output}[/green]")
        except OSError as e:
            logger.exception("Error saving configuration to %s", output)
            console.print(f"[red]Error saving configuration: {e}[/red]")
        except (json.JSONDecodeError, TypeError) as e:
            logger.exception("Error encoding configuration as JSON")
            console.print(f"[red]Error encoding configuration: {e}[/red]")
    else:
        try:
            formatted_config = json.dumps(config, indent=2, ensure_ascii=False)
            console.print(Panel(formatted_config, title=title))
        except (json.JSONDecodeError, TypeError) as e:
            logger.exception("Error encoding configuration for display")
            console.print(f"[red]Error displaying configuration: {e}[/red]")


class MCPToolingAdapter:
    """Adapter for integrating with existing MCP tooling."""

    def __init__(self) -> None:
        self.available_tools = self._detect_available_tools()

    def _detect_available_tools(self) -> dict[str, bool]:
        """Detect which MCP tools are available on the system."""
        tools = {}

        # Check for FastMCP
        fastmcp_path = shutil.which("fastmcp")
        if fastmcp_path:
            try:
                result = subprocess.run([fastmcp_path, "--version"], check=False, capture_output=True, text=True, timeout=5)
                tools["fastmcp"] = result.returncode == 0
            except (subprocess.TimeoutExpired, FileNotFoundError):
                tools["fastmcp"] = False
        else:
            tools["fastmcp"] = False

        # Check for mcp-cli
        mcp_path = shutil.which("mcp")
        if mcp_path:
            try:
                result = subprocess.run([mcp_path, "--version"], check=False, capture_output=True, text=True, timeout=5)
                tools["mcp-cli"] = result.returncode == 0
            except (subprocess.TimeoutExpired, FileNotFoundError):
                tools["mcp-cli"] = False
        else:
            tools["mcp-cli"] = False

        # Check for mcp-tools-cli
        mcp_tools_path = shutil.which("mcp-tools-cli")
        if mcp_tools_path:
            try:
                result = subprocess.run([mcp_tools_path, "--version"], check=False, capture_output=True, text=True, timeout=5)
                tools["mcp-tools-cli"] = result.returncode == 0
            except (subprocess.TimeoutExpired, FileNotFoundError):
                tools["mcp-tools-cli"] = False
        else:
            tools["mcp-tools-cli"] = False

        # Check for npm (for npx-based tools)
        npm_path = shutil.which("npm")
        if npm_path:
            try:
                result = subprocess.run([npm_path, "--version"], check=False, capture_output=True, text=True, timeout=5)
                tools["npm"] = result.returncode == 0
            except (subprocess.TimeoutExpired, FileNotFoundError):
                tools["npm"] = False
        else:
            tools["npm"] = False

        return tools

    def list_available_tools(self) -> None:
        """List available MCP tools on the system."""
        table = Table(title="Available MCP Tools")
        table.add_column("Tool", style="cyan")
        table.add_column("Available", style="green")
        table.add_column("Description", style="white")

        tool_descriptions = {
            "fastmcp": "FastMCP CLI - Fast MCP server generation and management",
            "mcp-cli": "AurraCloud MCP-CLI - MCP server installation and management",
            "mcp-tools-cli": "Python MCP tools CLI - MCP server interaction",
            "npm": "Node Package Manager - For npx-based MCP servers",
        }

        for tool, available in self.available_tools.items():
            status = "✓ Yes" if available else "✗ No"
            description = tool_descriptions.get(tool, "Unknown tool")
            table.add_row(tool, status, description)

        console.print(table)

    def _prepare_fastmcp_command(self, server_name: str, server_path: str, packages: list[str] | None = None) -> list[str]:
        """Prepare FastMCP command arguments."""
        cmd = ["fastmcp", "install", "mcp-json", server_path, "--name", server_name]
        if packages:
            cmd.extend(["--with", *packages])
        return cmd

    def _run_fastmcp_command(self, cmd: list[str], temp_path: Path) -> subprocess.CompletedProcess[str]:
        """Run FastMCP command and return result."""
        fastmcp_path = shutil.which("fastmcp")
        if not fastmcp_path:
            raise FileNotFoundError("FastMCP not found in PATH")
        cmd[0] = fastmcp_path
        return subprocess.run(cmd, check=False, cwd=temp_path, capture_output=True, text=True, timeout=30)

    def _load_fastmcp_config(self, temp_path: Path) -> dict[str, Any] | None:
        """Load configuration file generated by FastMCP."""
        config_files = list(temp_path.glob("*.json"))
        if not config_files:
            console.print("[yellow]No configuration file generated by FastMCP[/yellow]")
            return None

        # Load the first JSON file found
        with config_files[0].open() as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return None

    def generate_fastmcp_config(self, server_name: str, server_path: str, packages: list[str] | None = None) -> dict[str, Any] | None:
        """Generate MCP configuration using FastMCP."""
        if not self.available_tools.get("fastmcp"):
            console.print("[red]FastMCP is not available on this system[/red]")
            return None

        try:
            # Create temporary directory for FastMCP
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)

                # Prepare and run FastMCP command
                cmd = self._prepare_fastmcp_command(server_name, server_path, packages)
                result = self._run_fastmcp_command(cmd, temp_path)

                if result.returncode != 0:
                    console.print(f"[red]FastMCP error: {result.stderr}[/red]")
                    return None

                # Load generated configuration
                return self._load_fastmcp_config(temp_path)

        except subprocess.TimeoutExpired:
            console.print("[red]FastMCP command timed out[/red]")
            return None
        except Exception as e:
            console.print(f"[red]Error running FastMCP: {e}[/red]")
            return None

    def install_mcp_server(self, server_name: str, server_package: str) -> bool:
        """Install MCP server using mcp-cli."""
        if not self.available_tools.get("mcp-cli"):
            console.print("[red]mcp-cli is not available on this system[/red]")
            return False

        try:
            # Install server
            mcp_path = shutil.which("mcp")
            if not mcp_path:
                console.print("[red]MCP CLI not found in PATH[/red]")
                return False
            result = subprocess.run([mcp_path, "install", server_package], check=False, capture_output=True, text=True, timeout=60)

            if result.returncode != 0:
                console.print(f"[red]mcp-cli install error: {result.stderr}[/red]")
                return False
            console.print(f"[green]Successfully installed MCP server: {server_name}[/green]")
            return True

        except subprocess.TimeoutExpired:
            console.print("[red]mcp-cli install timed out[/red]")
            return False
        except Exception as e:
            console.print(f"[red]Error installing MCP server: {e}[/red]")
            return False

    def list_installed_servers(self) -> list[str]:
        """List installed MCP servers using mcp-cli."""
        if not self.available_tools.get("mcp-cli"):
            console.print("[red]mcp-cli is not available on this system[/red]")
            return []

        try:
            mcp_path = shutil.which("mcp")
            if not mcp_path:
                console.print("[red]MCP CLI not found in PATH[/red]")
                return []
            result = subprocess.run([mcp_path, "list"], check=False, capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                console.print(f"[red]mcp-cli list error: {result.stderr}[/red]")
                return []

            # Parse output to extract server names
            return [line.strip() for line in result.stdout.split("\n") if line.strip() and not line.startswith("Name")]

        except subprocess.TimeoutExpired:
            console.print("[red]mcp-cli list timed out[/red]")
            return []
        except Exception as e:
            console.print(f"[red]Error listing servers: {e}[/red]")
            return []

    def test_mcp_server(self, server_name: str, tool_name: str | None = None) -> bool:
        """Test MCP server using mcp-tools-cli."""
        if not self.available_tools.get("mcp-tools-cli"):
            console.print("[red]mcp-tools-cli is not available on this system[/red]")
            return False

        try:
            # List tools first
            mcp_tools_path = shutil.which("mcp-tools-cli")
            if not mcp_tools_path:
                console.print("[red]mcp-tools-cli not found in PATH[/red]")
                return False
            result = subprocess.run(
                [mcp_tools_path, "list-tools", "--mcp-name", server_name], check=False, capture_output=True, text=True, timeout=30
            )

            if result.returncode != 0:
                console.print(f"[red]Error listing tools for {server_name}: {result.stderr}[/red]")
                return False

            console.print(f"[green]Available tools for {server_name}:[/green]")
            console.print(result.stdout)

            # Test specific tool if provided
            if tool_name:
                test_result = subprocess.run(
                    [mcp_tools_path, "call-tool", "--mcp-name", server_name, "--tool-name", tool_name, "--tool-args", "{}"],
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if test_result.returncode != 0:
                    console.print(f"[red]Error testing tool {tool_name}: {test_result.stderr}[/red]")
                    return False
                console.print(f"[green]Tool {tool_name} test successful:[/green]")
                console.print(test_result.stdout)

            return True

        except subprocess.TimeoutExpired:
            console.print("[red]mcp-tools-cli command timed out[/red]")
            return False
        except Exception as e:
            console.print(f"[red]Error testing MCP server: {e}[/red]")
            return False


class MCPFormatConverter:
    """Converter for adapting MCP configurations between different formats."""

    def __init__(self) -> None:
        self.generator = MCPConfigGenerator()

    def convert_from_openapi(self, openapi_spec: str | dict[str, Any], server_name: str) -> dict[str, Any] | None:
        """Convert OpenAPI specification to MCP configuration."""
        try:
            if isinstance(openapi_spec, str):
                with Path(openapi_spec).open() as f:
                    spec = json.load(f)
            else:
                spec = openapi_spec

            # Extract server information
            servers = spec.get("servers", [])
            if not servers:
                console.print("[yellow]No servers found in OpenAPI spec[/yellow]")
                return None

            # Use first server as base
            base_server = servers[0]
            base_server.get("url", "")

            # Create MCP server configuration
            mcp_server = MCPServerConfig(
                name=server_name,
                command="npx",
                args=["-y", "openapi-mcp-server", openapi_spec if isinstance(openapi_spec, str) else "openapi.json"],
                description=f"MCP server for {spec.get('info', {}).get('title', server_name)}",
                version=spec.get("info", {}).get("version", "1.0.0"),
            )

            # Generate configuration
            return self.generator.generate_cursor_config({server_name: mcp_server})

        except Exception as e:
            console.print(f"[red]Error converting OpenAPI spec: {e}[/red]")
            return None

    def convert_from_docker_compose(self, compose_file: str, service_name: str) -> dict[str, Any] | None:
        """Convert Docker Compose service to MCP configuration."""
        try:
            with Path(compose_file).open() as f:
                compose_data = json.load(f)

            services = compose_data.get("services", {})
            if service_name not in services:
                console.print(f"[red]Service {service_name} not found in Docker Compose file[/red]")
                return None

            service = services[service_name]

            # Extract command and arguments
            command = service.get("command", "")
            if isinstance(command, list):
                command[0] if command else "docker"
                args = command[1:] if len(command) > 1 else []
            else:
                args = []

            # Add docker-compose specific arguments
            docker_args = ["compose", "exec", service_name, *args]

            mcp_server = MCPServerConfig(
                name=service_name,
                command="docker",
                args=docker_args,
                description=f"MCP server for Docker service: {service_name}",
                version="1.0.0",
            )

            # Generate configuration
            return self.generator.generate_cursor_config({service_name: mcp_server})

        except Exception as e:
            console.print(f"[red]Error converting Docker Compose service: {e}[/red]")
            return None

    def convert_from_package_json(self, package_file: str, script_name: str) -> dict[str, Any] | None:
        """Convert npm script to MCP configuration."""
        try:
            with Path(package_file).open() as f:
                package_data = json.load(f)

            scripts = package_data.get("scripts", {})
            if script_name not in scripts:
                console.print(f"[red]Script {script_name} not found in package.json[/red]")
                return None

            script_command = scripts[script_name]

            # Parse npm script
            if script_command.startswith("node "):
                cmd = "node"
                args = script_command[5:].split()
            elif script_command.startswith("npm "):
                cmd = "npm"
                args = script_command[4:].split()
            else:
                cmd = "npm"
                args = ["run", script_name]

            mcp_server = MCPServerConfig(
                name=script_name,
                command=cmd,
                args=args,
                description=f"MCP server for npm script: {script_name}",
                version=package_data.get("version", "1.0.0"),
            )

            # Generate configuration
            return self.generator.generate_cursor_config({script_name: mcp_server})

        except Exception as e:
            console.print(f"[red]Error converting npm script: {e}[/red]")
            return None


def _create_tools_commands(adapt: click.Group) -> None:
    """Create tools-related commands."""

    @adapt.command()
    def tools() -> None:
        """List available MCP tools on the system."""
        adapter = MCPToolingAdapter()
        adapter.list_available_tools()

    @adapt.command()
    @click.argument("server_name")
    @click.argument("server_path")
    @click.option("--packages", "-p", multiple=True, help="Additional packages to include")
    @click.option("--output", "-o", type=click.Path(), help="Output file path")
    def fastmcp(server_name: str, server_path: str, packages: tuple[str, ...], output: str | None) -> None:
        """Generate MCP configuration using FastMCP."""
        try:
            adapter = MCPToolingAdapter()
            config = adapter.generate_fastmcp_config(server_name, server_path, list(packages))
            _save_or_display_config(config, output, f"FastMCP Configuration: {server_name}")
        except Exception as e:
            logger.exception("Unexpected error in FastMCP command")
            console.print(f"[red]Unexpected error: {e}[/red]")

    @adapt.command()
    @click.argument("server_package")
    def install(server_package: str) -> None:
        """Install MCP server using mcp-cli."""
        try:
            adapter = MCPToolingAdapter()
            adapter.install_mcp_server(server_package, server_package)
        except Exception as e:
            logger.exception("Unexpected error in install command")
            console.print(f"[red]Unexpected error: {e}[/red]")

    @adapt.command()
    def list_servers() -> None:
        """List installed MCP servers using mcp-cli."""
        try:
            adapter = MCPToolingAdapter()
            servers = adapter.list_installed_servers()

            if servers:
                table = Table(title="Installed MCP Servers")
                table.add_column("Server Name", style="cyan")

                for server in servers:
                    table.add_row(server)

                console.print(table)
            else:
                console.print("[yellow]No installed servers found[/yellow]")
        except Exception as e:
            logger.exception("Unexpected error in list_servers command")
            console.print(f"[red]Unexpected error: {e}[/red]")

    @adapt.command()
    @click.argument("server_name")
    @click.option("--tool", "-t", help="Specific tool to test")
    def test(server_name: str, tool: str | None) -> None:
        """Test MCP server using mcp-tools-cli."""
        try:
            adapter = MCPToolingAdapter()
            adapter.test_mcp_server(server_name, tool)
        except Exception as e:
            logger.exception("Unexpected error in test command")
            console.print(f"[red]Unexpected error: {e}[/red]")


def _create_converter_commands(adapt: click.Group) -> None:
    """Create format converter commands."""

    @adapt.command()
    @click.argument("openapi_spec")
    @click.argument("server_name")
    @click.option("--output", "-o", type=click.Path(), help="Output file path")
    def from_openapi(openapi_spec: str, server_name: str, output: str | None) -> None:
        """Convert OpenAPI specification to MCP configuration."""
        try:
            converter = MCPFormatConverter()
            config = converter.convert_from_openapi(openapi_spec, server_name)
            _save_or_display_config(config, output, f"OpenAPI → MCP Configuration: {server_name}")
        except Exception as e:
            logger.exception("Unexpected error in from_openapi command")
            console.print(f"[red]Unexpected error: {e}[/red]")

    @adapt.command()
    @click.argument("compose_file")
    @click.argument("service_name")
    @click.option("--output", "-o", type=click.Path(), help="Output file path")
    def from_docker(compose_file: str, service_name: str, output: str | None) -> None:
        """Convert Docker Compose service to MCP configuration."""
        try:
            converter = MCPFormatConverter()
            config = converter.convert_from_docker_compose(compose_file, service_name)
            _save_or_display_config(config, output, f"Docker → MCP Configuration: {service_name}")
        except Exception as e:
            logger.exception("Unexpected error in from_docker command")
            console.print(f"[red]Unexpected error: {e}[/red]")

    @adapt.command()
    @click.argument("package_file")
    @click.argument("script_name")
    @click.option("--output", "-o", type=click.Path(), help="Output file path")
    def from_npm(package_file: str, script_name: str, output: str | None) -> None:
        """Convert npm script to MCP configuration."""
        try:
            converter = MCPFormatConverter()
            config = converter.convert_from_package_json(package_file, script_name)
            _save_or_display_config(config, output, f"npm → MCP Configuration: {script_name}")
        except Exception as e:
            logger.exception("Unexpected error in from_npm command")
            console.print(f"[red]Unexpected error: {e}[/red]")


def create_adapter_cli_commands(main_group: click.Group) -> None:
    """Add adapter CLI commands to the main CLI group."""

    @main_group.group()
    def adapt() -> None:
        """MCP tooling adapters and format converters."""

    _create_tools_commands(adapt)
    _create_converter_commands(adapt)
