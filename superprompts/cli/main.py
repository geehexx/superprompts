#!/usr/bin/env python3
"""CLI tool for SuperPrompts MCP Server.
"""

import asyncio
import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from superprompts.mcp.server import (
    compose_prompt,
    get_prompt,
    get_prompt_metadata,
    handle_call_tool,
    handle_list_tools,
    list_prompts,
)

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def main():
    """SuperPrompts CLI - Manage AI prompts and MCP server."""


@main.command()
@click.option(
    "--category",
    "-c",
    type=click.Choice(["docs", "rules", "all"]),
    default="all",
    help="Filter prompts by category",
)
def list_prompts_cmd(category: str):
    """List all available prompts."""

    async def _list_prompts():
        try:
            result = await list_prompts(category)
            prompts_data = json.loads(result[0].text)

            if not prompts_data:
                console.print("No prompts found for the specified category.")
                return

            table = Table(title=f"Available Prompts ({category})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Category", style="yellow")
            table.add_column("Description", style="white")

            for prompt in prompts_data:
                table.add_row(
                    prompt["id"],
                    prompt["name"],
                    prompt["category"],
                    prompt["description"][:100] + "..."
                    if len(prompt["description"]) > 100
                    else prompt["description"],
                )

            console.print(table)

        except Exception as e:
            console.print(f"[red]Error listing prompts: {e}[/red]")
            sys.exit(1)

    asyncio.run(_list_prompts())


@main.command()
@click.argument("prompt_id")
@click.option(
    "--parameters", "-p", help="JSON string of parameters to pass to the prompt"
)
@click.option(
    "--output", "-o", type=click.Path(), help="Output file path (default: stdout)"
)
def get_prompt_cmd(prompt_id: str, parameters: str | None, output: str | None):
    """Get a specific prompt by ID."""

    async def _get_prompt():
        try:
            # Parse parameters if provided
            params = {}
            if parameters:
                try:
                    params = json.loads(parameters)
                except json.JSONDecodeError:
                    console.print(
                        f"[red]Invalid JSON in parameters: {parameters}[/red]"
                    )
                    sys.exit(1)

            result = await get_prompt(prompt_id, params)
            prompt_text = result[0].text

            if output:
                Path(output).write_text(prompt_text)
                console.print(f"[green]Prompt saved to {output}[/green]")
            else:
                console.print(Panel(prompt_text, title=f"Prompt: {prompt_id}"))

        except Exception as e:
            console.print(f"[red]Error getting prompt: {e}[/red]")
            sys.exit(1)

    asyncio.run(_get_prompt())


@main.command()
@click.argument("prompt_id")
def metadata(prompt_id: str):
    """Get detailed metadata about a specific prompt."""

    async def _get_metadata():
        try:
            result = await get_prompt_metadata(prompt_id)
            metadata = json.loads(result[0].text)

            # Create a formatted display
            text = Text()
            text.append(f"Name: {metadata['name']}\n", style="bold green")
            text.append(f"Description: {metadata['description']}\n", style="white")
            text.append(f"Category: {metadata['category']}\n", style="yellow")
            text.append(f"Phases: {', '.join(metadata['phases'])}\n", style="cyan")
            text.append(
                f"Parameters: {', '.join(metadata['parameters'])}\n", style="magenta"
            )

            console.print(Panel(text, title=f"Metadata: {prompt_id}"))

        except Exception as e:
            console.print(f"[red]Error getting metadata: {e}[/red]")
            sys.exit(1)

    asyncio.run(_get_metadata())


@main.command()
@click.argument("base_prompt_id")
@click.option(
    "--additions", "-a", help="JSON string of additions to make to the prompt"
)
@click.option("--customizations", "-c", help="JSON string of customizations to apply")
@click.option(
    "--output", "-o", type=click.Path(), help="Output file path (default: stdout)"
)
def compose(
    base_prompt_id: str,
    additions: str | None,
    customizations: str | None,
    output: str | None,
):
    """Compose a custom prompt by combining elements."""

    async def _compose():
        try:
            # Parse additions and customizations
            additions_list = []
            customizations_dict = {}

            if additions:
                try:
                    additions_list = json.loads(additions)
                except json.JSONDecodeError:
                    console.print(f"[red]Invalid JSON in additions: {additions}[/red]")
                    sys.exit(1)

            if customizations:
                try:
                    customizations_dict = json.loads(customizations)
                except json.JSONDecodeError:
                    console.print(
                        f"[red]Invalid JSON in customizations: {customizations}[/red]"
                    )
                    sys.exit(1)

            result = await compose_prompt(
                base_prompt_id, additions_list, customizations_dict
            )
            composed_text = result[0].text

            if output:
                Path(output).write_text(composed_text)
                console.print(f"[green]Composed prompt saved to {output}[/green]")
            else:
                console.print(
                    Panel(composed_text, title=f"Composed Prompt: {base_prompt_id}")
                )

        except Exception as e:
            console.print(f"[red]Error composing prompt: {e}[/red]")
            sys.exit(1)

    asyncio.run(_compose())


@main.command()
def tools():
    """List all available MCP tools."""

    async def _list_tools():
        try:
            tools = await handle_list_tools()

            table = Table(title="Available MCP Tools")
            table.add_column("Name", style="cyan")
            table.add_column("Description", style="white")

            for tool in tools:
                table.add_row(tool.name, tool.description)

            console.print(table)

        except Exception as e:
            console.print(f"[red]Error listing tools: {e}[/red]")
            sys.exit(1)

    asyncio.run(_list_tools())


@main.command()
@click.argument("tool_name")
@click.argument("arguments", required=False)
def call_tool(tool_name: str, arguments: str | None):
    """Call a specific MCP tool with arguments."""

    async def _call_tool():
        try:
            # Parse arguments if provided
            args = {}
            if arguments:
                try:
                    args = json.loads(arguments)
                except json.JSONDecodeError:
                    console.print(f"[red]Invalid JSON in arguments: {arguments}[/red]")
                    sys.exit(1)

            result = await handle_call_tool(tool_name, args)

            # Display result
            for content in result:
                if hasattr(content, "text"):
                    console.print(Panel(content.text, title=f"Tool: {tool_name}"))
                else:
                    console.print(
                        f"[yellow]Tool {tool_name} returned: {content}[/yellow]"
                    )

        except Exception as e:
            console.print(f"[red]Error calling tool: {e}[/red]")
            sys.exit(1)

    asyncio.run(_call_tool())


if __name__ == "__main__":
    main()
