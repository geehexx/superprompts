#!/usr/bin/env python3
"""MCP Configuration Models.

This module provides basic configuration models for MCP servers.
For detailed configuration instructions, see the documentation.
"""

from pydantic import BaseModel, Field


class MCPServerConfig(BaseModel):
    """MCP Server Configuration Model."""

    name: str = Field(..., description="Server name")
    command: str = Field(..., description="Command to run the server")
    args: list[str] = Field(default_factory=list, description="Command arguments")
    env: dict[str, str] | None = Field(default=None, description="Environment variables")
    cwd: str | None = Field(default=None, description="Working directory")
    description: str | None = Field(default=None, description="Server description")
    version: str | None = Field(default=None, description="Server version")
