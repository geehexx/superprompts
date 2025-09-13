#!/usr/bin/env python3
"""CLI tool for SuperPrompts MCP Server."""

import asyncio
import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from superprompts.mcp.adapters import create_adapter_cli_commands
from superprompts.mcp.config import MCPConfigGenerator, MCPServerConfig, get_available_server_templates, validate_config
from superprompts.mcp.server import compose_prompt, get_prompt, get_prompt_metadata, handle_call_tool, handle_list_tools, list_prompts

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
                    prompt["description"][:100] + "..." if len(prompt["description"]) > 100 else prompt["description"],
                )

            console.print(table)

        except Exception as e:
            console.print(f"[red]Error listing prompts: {e}[/red]")
            sys.exit(1)

    asyncio.run(_list_prompts())


@main.command()
@click.argument("prompt_id")
@click.option("--parameters", "-p", help="JSON string of parameters to pass to the prompt")
@click.option("--output", "-o", type=click.Path(), help="Output file path (default: stdout)")
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
                    console.print(f"[red]Invalid JSON in parameters: {parameters}[/red]")
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
            text.append(f"Parameters: {', '.join(metadata['parameters'])}\n", style="magenta")

            console.print(Panel(text, title=f"Metadata: {prompt_id}"))

        except Exception as e:
            console.print(f"[red]Error getting metadata: {e}[/red]")
            sys.exit(1)

    asyncio.run(_get_metadata())


@main.command()
@click.argument("base_prompt_id")
@click.option("--additions", "-a", help="JSON string of additions to make to the prompt")
@click.option("--customizations", "-c", help="JSON string of customizations to apply")
@click.option("--output", "-o", type=click.Path(), help="Output file path (default: stdout)")
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
                    console.print(f"[red]Invalid JSON in customizations: {customizations}[/red]")
                    sys.exit(1)

            result = await compose_prompt(base_prompt_id, additions_list, customizations_dict)
            composed_text = result[0].text

            if output:
                Path(output).write_text(composed_text)
                console.print(f"[green]Composed prompt saved to {output}[/green]")
            else:
                console.print(Panel(composed_text, title=f"Composed Prompt: {base_prompt_id}"))

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
                    console.print(f"[yellow]Tool {tool_name} returned: {content}[/yellow]")

        except Exception as e:
            console.print(f"[red]Error calling tool: {e}[/red]")
            sys.exit(1)

    asyncio.run(_call_tool())


@main.group()
def config():
    """Manage MCP server configurations."""


@config.command()
@click.option(
    "--format",
    "-f",
    type=click.Choice(["cursor", "vscode", "generic"]),
    default="cursor",
    help="Configuration format to generate",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path (default: auto-determined based on format)",
)
@click.option(
    "--template",
    "-t",
    multiple=True,
    help="Server templates to include (superprompts, github, filesystem)",
)
@click.option(
    "--merge",
    is_flag=True,
    help="Merge with existing configuration instead of overwriting",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be generated without writing files",
)
def create(format: str, output: str | None, template: tuple, merge: bool, dry_run: bool):
    """Create or update MCP server configuration."""
    try:
        generator = MCPConfigGenerator()

        # Get server templates
        available_templates = get_available_server_templates()
        selected_servers = {}

        if template:
            for template_name in template:
                if template_name in available_templates:
                    selected_servers[template_name] = available_templates[template_name]
                else:
                    console.print(f"[yellow]Warning: Unknown template '{template_name}'[/yellow]")
        else:
            # Default to superprompts if no templates specified
            selected_servers = {"superprompts": available_templates["superprompts"]}

        if not selected_servers:
            console.print("[red]No valid server templates selected[/red]")
            return

        # Generate configuration
        if format == "cursor":
            config = generator.generate_cursor_config(selected_servers)
        elif format == "vscode":
            config = generator.generate_vscode_config(selected_servers)
        else:  # generic
            config = generator.generate_generic_config(selected_servers)

        # Handle merging with existing config
        if merge:
            output_path = Path(output) if output else None
            if output_path is None:
                if format == "cursor":
                    output_path = Path("mcp.json")
                elif format == "vscode":
                    output_path = Path(".vscode/mcp.json")
                else:
                    output_path = Path("mcp_config.json")

            existing_config = generator.load_existing_config(output_path)
            if existing_config:
                config = generator.merge_configs(existing_config, selected_servers, format)

        # Validate configuration
        errors = validate_config(config, format)
        if errors:
            console.print("[red]Configuration validation errors:[/red]")
            for error in errors:
                console.print(f"  - {error}")
            return

        if dry_run:
            console.print(
                Panel(
                    json.dumps(config, indent=2),
                    title=f"MCP Configuration ({format}) - Dry Run",
                )
            )
        else:
            # Save configuration
            output_path = generator.save_config(config, format, Path(output) if output else None)
            console.print(f"[green]Configuration saved to: {output_path}[/green]")

            # Show summary
            table = Table(title="Generated MCP Configuration")
            table.add_column("Server", style="cyan")
            table.add_column("Command", style="green")
            table.add_column("Description", style="white")

            for name, server in selected_servers.items():
                table.add_row(
                    name,
                    f"{server.command} {' '.join(server.args)}",
                    server.description or "No description",
                )

            console.print(table)

    except Exception as e:
        console.print(f"[red]Error creating configuration: {e}[/red]")
        sys.exit(1)


@config.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option(
    "--format",
    "-f",
    type=click.Choice(["cursor", "vscode", "generic", "auto"]),
    default="auto",
    help="Configuration format (auto-detect if not specified)",
)
def validate(config_file: str, format: str):
    """Validate an existing MCP configuration file."""
    try:
        config_path = Path(config_file)

        # Load configuration
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)

        # Auto-detect format if needed
        if format == "auto":
            if "mcpServers" in config:
                format = "cursor"
            elif "mcp" in config and "servers" in config.get("mcp", {}):
                format = "vscode"
            else:
                format = "generic"

        # Validate configuration
        errors = validate_config(config, format)

        if not errors:
            console.print(f"[green]✓ Configuration is valid ({format} format)[/green]")

            # Show configuration summary
            if format == "cursor" and "mcpServers" in config:
                servers = config["mcpServers"]
            elif (format == "vscode" and "mcp" in config) or (format == "generic" and "mcp" in config):
                servers = config["mcp"].get("servers", {})
            else:
                servers = {}

            if servers:
                table = Table(title=f"Configured Servers ({format})")
                table.add_column("Name", style="cyan")
                table.add_column("Command", style="green")

                for name, server_config in servers.items():
                    command = server_config.get("command", "N/A")
                    args = server_config.get("args", [])
                    full_command = f"{command} {' '.join(args)}" if args else command
                    table.add_row(name, full_command)

                console.print(table)
        else:
            console.print(f"[red]✗ Configuration has {len(errors)} error(s):[/red]")
            for error in errors:
                console.print(f"  - {error}")
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]Error validating configuration: {e}[/red]")
        sys.exit(1)


@config.command()
def templates():
    """List available server configuration templates."""
    try:
        templates = get_available_server_templates()

        table = Table(title="Available MCP Server Templates")
        table.add_column("Name", style="cyan")
        table.add_column("Command", style="green")
        table.add_column("Description", style="white")

        for name, server in templates.items():
            table.add_row(
                name,
                f"{server.command} {' '.join(server.args)}",
                server.description or "No description",
            )

        console.print(table)
        console.print("\n[yellow]Usage:[/yellow]")
        console.print("  superprompts config create --template superprompts --template github")
        console.print("  superprompts config create --format vscode --template superprompts")

    except Exception as e:
        console.print(f"[red]Error listing templates: {e}[/red]")
        sys.exit(1)


@config.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option(
    "--format",
    "-f",
    type=click.Choice(["cursor", "vscode", "generic", "auto"]),
    default="auto",
    help="Configuration format (auto-detect if not specified)",
)
def convert(config_file: str, format: str):
    """Convert MCP configuration between different formats."""
    try:
        config_path = Path(config_file)

        # Load configuration
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)

        # Auto-detect source format
        if "mcpServers" in config:
            source_format = "cursor"
        elif "mcp" in config and "servers" in config.get("mcp", {}):
            source_format = "vscode"
        else:
            source_format = "generic"

        # Extract servers
        if source_format == "cursor":
            servers_config = config.get("mcpServers", {})
        elif source_format == "vscode":
            servers_config = config.get("mcp", {}).get("servers", {})
        else:  # generic
            servers_config = config.get("mcp", {}).get("servers", {})

        # Convert to MCPServerConfig objects
        servers = {}
        for name, server_config in servers_config.items():
            servers[name] = MCPServerConfig(
                name=name,
                command=server_config.get("command", ""),
                args=server_config.get("args", []),
                env=server_config.get("env"),
                cwd=server_config.get("cwd"),
                description=server_config.get("description"),
                version=server_config.get("version"),
            )

        # Generate new format
        generator = MCPConfigGenerator()
        if format == "cursor":
            new_config = generator.generate_cursor_config(servers)
        elif format == "vscode":
            new_config = generator.generate_vscode_config(servers)
        else:  # generic
            new_config = generator.generate_generic_config(servers)

        # Show converted configuration
        console.print(
            Panel(
                json.dumps(new_config, indent=2),
                title=f"Converted Configuration ({source_format} → {format})",
            )
        )

        # Offer to save
        if click.confirm(f"Save converted configuration as {format} format?"):
            output_path = generator.save_config(new_config, format)
            console.print(f"[green]Converted configuration saved to: {output_path}[/green]")

    except Exception as e:
        console.print(f"[red]Error converting configuration: {e}[/red]")
        sys.exit(1)


# Add adapter commands
create_adapter_cli_commands(main)


if __name__ == "__main__":
    main()
