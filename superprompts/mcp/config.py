#!/usr/bin/env python3
"""MCP Configuration Management

This module provides functionality to create and update MCP server definitions
in various formats (Cursor mcp.json, VS Code, etc.).
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import click
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class MCPServerConfig(BaseModel):
    """MCP Server Configuration Model."""
    
    name: str = Field(..., description="Server name")
    command: str = Field(..., description="Command to run the server")
    args: List[str] = Field(default_factory=list, description="Command arguments")
    env: Optional[Dict[str, str]] = Field(default=None, description="Environment variables")
    cwd: Optional[str] = Field(default=None, description="Working directory")
    description: Optional[str] = Field(default=None, description="Server description")
    version: Optional[str] = Field(default=None, description="Server version")


class MCPConfig(BaseModel):
    """MCP Configuration Model for different formats."""
    
    servers: Dict[str, MCPServerConfig] = Field(default_factory=dict)
    format: str = Field(default="cursor", description="Configuration format")
    version: str = Field(default="1.0.0", description="MCP configuration version")


class MCPConfigGenerator:
    """Generator for MCP server configurations in different formats."""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.cwd()
        self.supported_formats = ["cursor", "vscode", "generic"]
    
    def generate_cursor_config(self, servers: Dict[str, MCPServerConfig]) -> Dict[str, Any]:
        """Generate Cursor-compatible mcp.json configuration."""
        return {
            "mcpServers": {
                name: {
                    "command": server.command,
                    "args": server.args,
                    "env": server.env or {},
                    "cwd": server.cwd,
                }
                for name, server in servers.items()
            }
        }
    
    def generate_vscode_config(self, servers: Dict[str, MCPServerConfig]) -> Dict[str, Any]:
        """Generate VS Code-compatible MCP configuration."""
        return {
            "mcp": {
                "servers": {
                    name: {
                        "command": server.command,
                        "args": server.args,
                        "env": server.env or {},
                        "cwd": server.cwd,
                    }
                    for name, server in servers.items()
                }
            }
        }
    
    def generate_generic_config(self, servers: Dict[str, MCPServerConfig]) -> Dict[str, Any]:
        """Generate generic MCP configuration."""
        return {
            "mcp": {
                "version": "1.0.0",
                "servers": {
                    name: {
                        "name": server.name,
                        "command": server.command,
                        "args": server.args,
                        "env": server.env or {},
                        "cwd": server.cwd,
                        "description": server.description,
                        "version": server.version,
                    }
                    for name, server in servers.items()
                }
            }
        }
    
    def save_config(
        self, 
        config: Dict[str, Any], 
        format_type: str, 
        output_path: Optional[Path] = None
    ) -> Path:
        """Save configuration to file."""
        if output_path is None:
            if format_type == "cursor":
                output_path = self.config_path / "mcp.json"
            elif format_type == "vscode":
                output_path = self.config_path / ".vscode" / "mcp.json"
            else:
                output_path = self.config_path / "mcp_config.json"
        
        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write configuration
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def load_existing_config(self, config_path: Path) -> Optional[Dict[str, Any]]:
        """Load existing configuration if it exists."""
        if not config_path.exists():
            return None
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            console.print(f"[yellow]Warning: Could not load existing config: {e}[/yellow]")
            return None
    
    def merge_configs(
        self, 
        existing: Dict[str, Any], 
        new_servers: Dict[str, MCPServerConfig],
        format_type: str
    ) -> Dict[str, Any]:
        """Merge new servers into existing configuration."""
        if format_type == "cursor":
            if "mcpServers" not in existing:
                existing["mcpServers"] = {}
            for name, server in new_servers.items():
                existing["mcpServers"][name] = {
                    "command": server.command,
                    "args": server.args,
                    "env": server.env or {},
                    "cwd": server.cwd,
                }
        elif format_type == "vscode":
            if "mcp" not in existing:
                existing["mcp"] = {}
            if "servers" not in existing["mcp"]:
                existing["mcp"]["servers"] = {}
            for name, server in new_servers.items():
                existing["mcp"]["servers"][name] = {
                    "command": server.command,
                    "args": server.args,
                    "env": server.env or {},
                    "cwd": server.cwd,
                }
        else:  # generic
            if "mcp" not in existing:
                existing["mcp"] = {"version": "1.0.0", "servers": {}}
            if "servers" not in existing["mcp"]:
                existing["mcp"]["servers"] = {}
            for name, server in new_servers.items():
                existing["mcp"]["servers"][name] = {
                    "name": server.name,
                    "command": server.command,
                    "args": server.args,
                    "env": server.env or {},
                    "cwd": server.cwd,
                    "description": server.description,
                    "version": server.version,
                }
        
        return existing


def create_superprompts_server_config() -> MCPServerConfig:
    """Create configuration for the SuperPrompts MCP server."""
    return MCPServerConfig(
        name="superprompts",
        command="poetry",
        args=["run", "python", "-m", "superprompts.mcp.server"],
        description="SuperPrompts MCP Server - Access to AI prompt collection",
        version="1.0.0"
    )


def create_github_server_config() -> MCPServerConfig:
    """Create configuration for GitHub MCP server."""
    return MCPServerConfig(
        name="github",
        command="npx",
        args=["-y", "github-mcp-server"],
        description="GitHub MCP Server - Repository operations",
        version="1.0.0"
    )


def create_filesystem_server_config() -> MCPServerConfig:
    """Create configuration for filesystem MCP server."""
    return MCPServerConfig(
        name="filesystem",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/path/to/your/project"],
        description="Filesystem MCP Server - File operations",
        version="1.0.0"
    )


def get_available_server_templates() -> Dict[str, MCPServerConfig]:
    """Get available server configuration templates."""
    return {
        "superprompts": create_superprompts_server_config(),
        "github": create_github_server_config(),
        "filesystem": create_filesystem_server_config(),
    }


def validate_config(config: Dict[str, Any], format_type: str) -> List[str]:
    """Validate MCP configuration and return any errors."""
    errors = []
    
    if format_type == "cursor":
        if "mcpServers" not in config:
            errors.append("Missing 'mcpServers' key in Cursor configuration")
        else:
            for name, server_config in config["mcpServers"].items():
                if "command" not in server_config:
                    errors.append(f"Server '{name}' missing 'command' field")
    elif format_type == "vscode":
        if "mcp" not in config:
            errors.append("Missing 'mcp' key in VS Code configuration")
        elif "servers" not in config["mcp"]:
            errors.append("Missing 'servers' key in VS Code configuration")
    else:  # generic
        if "mcp" not in config:
            errors.append("Missing 'mcp' key in generic configuration")
        elif "servers" not in config["mcp"]:
            errors.append("Missing 'servers' key in generic configuration")
        else:
            for name, server_config in config["mcp"]["servers"].items():
                if "name" not in server_config:
                    errors.append(f"Server '{name}' missing 'name' field in generic configuration")
                if "command" not in server_config:
                    errors.append(f"Server '{name}' missing 'command' field in generic configuration")
    
    return errors
