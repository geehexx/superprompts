#!/usr/bin/env python3
"""CLI tool for SuperPrompts MCP Server."""

import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from superprompts.mcp.server import cursor_rules_prompt_handler, get_prompt_by_id, get_prompts_list, repo_docs_prompt_handler

console = Console()

# Constants
MAX_DESCRIPTION_LENGTH = 100


@click.group()
@click.version_option(version="1.0.0")
def main() -> None:
    """SuperPrompts CLI - Manage AI prompts and MCP server."""


@main.command()
@click.option(
    "--category",
    "-c",
    type=click.Choice(["docs", "rules", "all"]),
    default="all",
    help="Filter prompts by category",
)
def list_prompts_cmd(category: str) -> None:
    """List all available prompts."""
    try:
        prompts_data = get_prompts_list()

        # Filter by category if not "all"
        if category != "all":
            prompts_data = [p for p in prompts_data if p["category"] == category]

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
                (
                    prompt["description"][:MAX_DESCRIPTION_LENGTH] + "..."
                    if len(prompt["description"]) > MAX_DESCRIPTION_LENGTH
                    else prompt["description"]
                ),
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error listing prompts: {e}[/red]")
        sys.exit(1)


@main.command()
@click.argument("prompt_id")
@click.option("--parameters", "-p", help="JSON string of parameters to pass to the prompt")
@click.option("--output", "-o", type=click.Path(), help="Output file path (default: stdout)")
def get_prompt_cmd(prompt_id: str, parameters: str | None, output: str | None) -> None:
    """Get a specific prompt by ID."""
    try:
        # Parse parameters if provided
        params = {}
        if parameters:
            try:
                params = json.loads(parameters)
            except json.JSONDecodeError:
                console.print(f"[red]Invalid JSON in parameters: {parameters}[/red]")
                sys.exit(1)

        # Get the appropriate prompt handler
        if prompt_id == "repo_docs":
            prompt_text: str = repo_docs_prompt_handler.fn(params)  # type: ignore[assignment]
        elif prompt_id == "cursor_rules":
            prompt_text = cursor_rules_prompt_handler.fn(params)  # type: ignore[assignment]
        else:
            console.print(f"[red]Unknown prompt ID: {prompt_id}[/red]")
            sys.exit(1)

        if output:
            Path(output).write_text(prompt_text)
            console.print(f"[green]Prompt saved to {output}[/green]")
        else:
            console.print(Panel(prompt_text, title=f"Prompt: {prompt_id}"))

    except Exception as e:
        console.print(f"[red]Error getting prompt: {e}[/red]")
        sys.exit(1)


@main.command()
@click.argument("prompt_id")
def metadata(prompt_id: str) -> None:
    """Get detailed metadata about a specific prompt."""
    try:
        metadata = get_prompt_by_id(prompt_id)
        if not metadata:
            console.print(f"[red]Prompt not found: {prompt_id}[/red]")
            sys.exit(1)

        # Create a formatted display
        text = Text()
        text.append(f"Name: {metadata['name']}\n", style="bold green")
        text.append(f"Description: {metadata['description']}\n", style="white")
        text.append(f"Category: {metadata['category']}\n", style="yellow")
        text.append(f"Phases: {', '.join(metadata['phases'])}\n", style="cyan")
        text.append(f"Arguments: {', '.join([arg['name'] for arg in metadata['arguments']])}\n", style="magenta")

        console.print(Panel(text, title=f"Metadata: {prompt_id}"))

    except Exception as e:
        console.print(f"[red]Error getting metadata: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
