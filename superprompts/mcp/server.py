#!/usr/bin/env python3
"""MCP Server for SuperPrompts
Provides tools for accessing and composing AI prompts from the superprompts collection.
"""

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    Tool,
)

from superprompts.prompts.cursor_rules import CursorRulesPrompt

# Import prompt modules
from superprompts.prompts.repo_docs import RepoDocsPrompt

# Initialize the server
server = Server("superprompts")

# Initialize prompt handlers
repo_docs_prompt = RepoDocsPrompt()
cursor_rules_prompt = CursorRulesPrompt()


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools for prompt management."""
    return [
        Tool(
            name="list_prompts",
            description="List all available prompts with their metadata",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter prompts by category (docs, rules, etc.)",
                        "enum": ["docs", "rules", "all"],
                    }
                },
            },
        ),
        Tool(
            name="get_prompt",
            description="Get a specific prompt by ID with optional parameters",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt_id": {
                        "type": "string",
                        "description": "The ID of the prompt to retrieve",
                        "enum": ["repo_docs", "cursor_rules"],
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Optional parameters to customize the prompt",
                        "properties": {
                            "batch_size": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 10,
                            },
                            "target_categories": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Target categories for the prompt",
                            },
                            "phases": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Specific phases to include",
                            },
                        },
                    },
                },
                "required": ["prompt_id"],
            },
        ),
        Tool(
            name="get_prompt_metadata",
            description="Get detailed metadata about a specific prompt",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt_id": {
                        "type": "string",
                        "description": "The ID of the prompt",
                        "enum": ["repo_docs", "cursor_rules"],
                    }
                },
                "required": ["prompt_id"],
            },
        ),
        Tool(
            name="compose_prompt",
            description="Compose a custom prompt by combining elements from different prompts",
            inputSchema={
                "type": "object",
                "properties": {
                    "base_prompt_id": {
                        "type": "string",
                        "description": "Base prompt to start with",
                        "enum": ["repo_docs", "cursor_rules"],
                    },
                    "additions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "source_prompt_id": {"type": "string"},
                                "element_type": {"type": "string"},
                                "element_name": {"type": "string"},
                            },
                        },
                        "description": "Elements to add from other prompts",
                    },
                    "customizations": {
                        "type": "object",
                        "description": "Custom modifications to apply",
                    },
                },
                "required": ["base_prompt_id"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    if name == "list_prompts":
        category = arguments.get("category", "all")
        return await list_prompts(category)

    if name == "get_prompt":
        prompt_id = arguments["prompt_id"]
        parameters = arguments.get("parameters", {})
        return await get_prompt(prompt_id, parameters)

    if name == "get_prompt_metadata":
        prompt_id = arguments["prompt_id"]
        return await get_prompt_metadata(prompt_id)

    if name == "compose_prompt":
        base_prompt_id = arguments["base_prompt_id"]
        additions = arguments.get("additions", [])
        customizations = arguments.get("customizations", {})
        return await compose_prompt(base_prompt_id, additions, customizations)

    raise ValueError(f"Unknown tool: {name}")


async def list_prompts(category: str) -> list[TextContent]:
    """List available prompts."""
    prompts = []

    if category in ["all", "docs"]:
        prompts.append(
            {
                "id": "repo_docs",
                "name": "Repository Documentation Rebuilder",
                "description": "Rebuilds and modernizes repository documentation safely with loss auditing",
                "category": "docs",
                "phases": ["discovery", "gaps_analysis", "mapping", "generation", "qa"],
                "parameters": [
                    "batch_size",
                    "target_doc_types",
                    "confidence_threshold",
                ],
            }
        )

    if category in ["all", "rules"]:
        prompts.append(
            {
                "id": "cursor_rules",
                "name": "Cursor Rules Generator",
                "description": "Generates high-quality Cursor rules tailored to the detected stack",
                "category": "rules",
                "phases": [
                    "signals",
                    "planning",
                    "generation",
                    "optimization",
                    "placement",
                ],
                "parameters": [
                    "target_categories",
                    "rule_types",
                    "similarity_threshold",
                ],
            }
        )

    return [TextContent(type="text", text=json.dumps(prompts, indent=2))]


async def get_prompt(prompt_id: str, parameters: dict[str, Any]) -> list[TextContent]:
    """Get a specific prompt with parameters."""
    if prompt_id == "repo_docs":
        prompt_text = repo_docs_prompt.get_prompt(parameters)
    elif prompt_id == "cursor_rules":
        prompt_text = cursor_rules_prompt.get_prompt(parameters)
    else:
        raise ValueError(f"Unknown prompt ID: {prompt_id}")

    return [TextContent(type="text", text=prompt_text)]


async def get_prompt_metadata(prompt_id: str) -> list[TextContent]:
    """Get detailed metadata about a prompt."""
    if prompt_id == "repo_docs":
        metadata = repo_docs_prompt.get_metadata()
    elif prompt_id == "cursor_rules":
        metadata = cursor_rules_prompt.get_metadata()
    else:
        raise ValueError(f"Unknown prompt ID: {prompt_id}")

    return [TextContent(type="text", text=json.dumps(metadata, indent=2))]


async def compose_prompt(
    base_prompt_id: str, additions: list[dict], customizations: dict
) -> list[TextContent]:
    """Compose a custom prompt."""
    # Get base prompt
    if base_prompt_id == "repo_docs":
        base_prompt = repo_docs_prompt
    elif base_prompt_id == "cursor_rules":
        base_prompt = cursor_rules_prompt
    else:
        raise ValueError(f"Unknown base prompt ID: {base_prompt_id}")

    # Start with base prompt
    composed_text = base_prompt.get_prompt({})

    # Add elements from other prompts
    for addition in additions:
        source_prompt_id = addition["source_prompt_id"]
        element_type = addition["element_type"]
        element_name = addition["element_name"]

        if source_prompt_id == "repo_docs":
            source_prompt = repo_docs_prompt
        elif source_prompt_id == "cursor_rules":
            source_prompt = cursor_rules_prompt
        else:
            continue

        element = source_prompt.get_element(element_type, element_name)
        if element:
            composed_text += f"\n\n## {element_name}\n{element}"

    # Apply customizations
    if customizations:
        # This is a simplified approach - in practice, you'd want more sophisticated customization
        for key, value in customizations.items():
            if isinstance(value, str):
                composed_text = composed_text.replace(f"{{{key}}}", value)

    return [TextContent(type="text", text=composed_text)]


async def main():
    """Main entry point."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
