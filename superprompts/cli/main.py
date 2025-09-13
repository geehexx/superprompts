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

from superprompts.mcp.adapters import create_adapter_cli_commands
from superprompts.mcp.config import MCPConfigGenerator, MCPServerConfig, get_available_server_templates, validate_config
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
            prompt_text = repo_docs_prompt_handler.fn(params)
        elif prompt_id == "cursor_rules":
            prompt_text = cursor_rules_prompt_handler.fn(params)
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


# Compose command removed - not part of core MCP implementation


# Legacy tool commands removed - use the MCP server directly for tool functionality


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
def create(format_type: str, output: str | None, template: tuple, merge: bool, dry_run: bool) -> None:
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
        if format_type == "cursor":
            config = generator.generate_cursor_config(selected_servers)
        elif format_type == "vscode":
            config = generator.generate_vscode_config(selected_servers)
        else:  # generic
            config = generator.generate_generic_config(selected_servers)

        # Handle merging with existing config
        if merge:
            output_path = Path(output) if output else None
            if output_path is None:
                if format_type == "cursor":
                    output_path = Path("mcp.json")
                elif format_type == "vscode":
                    output_path = Path(".vscode/mcp.json")
                else:
                    output_path = Path("mcp_config.json")

            existing_config = generator.load_existing_config(output_path)
            if existing_config:
                config = generator.merge_configs(existing_config, selected_servers, format_type)

        # Validate configuration
        errors = validate_config(config, format_type)
        if errors:
            console.print("[red]Configuration validation errors:[/red]")
            for error in errors:
                console.print(f"  - {error}")
            return

        if dry_run:
            console.print(
                Panel(
                    json.dumps(config, indent=2),
                    title=f"MCP Configuration ({format_type}) - Dry Run",
                )
            )
        else:
            # Save configuration
            output_path = generator.save_config(config, format_type, Path(output) if output else None)
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
def validate(config_file: str, format_type: str) -> None:
    """Validate an existing MCP configuration file."""
    try:
        config_path = Path(config_file)

        # Load configuration
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)

        # Auto-detect format if needed
        if format_type == "auto":
            if "mcpServers" in config:
                format_type = "cursor"
            elif "mcp" in config and "servers" in config.get("mcp", {}):
                format_type = "vscode"
            else:
                format_type = "generic"

        # Validate configuration
        errors = validate_config(config, format_type)

        if not errors:
            console.print(f"[green]✓ Configuration is valid ({format_type} format)[/green]")

            # Show configuration summary
            if format_type == "cursor" and "mcpServers" in config:
                servers = config["mcpServers"]
            elif (format_type == "vscode" and "mcp" in config) or (format_type == "generic" and "mcp" in config):
                servers = config["mcp"].get("servers", {})
            else:
                servers = {}

            if servers:
                table = Table(title=f"Configured Servers ({format_type})")
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
def convert(config_file: str, format_type: str) -> None:
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
        if format_type == "cursor":
            new_config = generator.generate_cursor_config(servers)
        elif format_type == "vscode":
            new_config = generator.generate_vscode_config(servers)
        else:  # generic
            new_config = generator.generate_generic_config(servers)

        # Show converted configuration
        console.print(
            Panel(
                json.dumps(new_config, indent=2),
                title=f"Converted Configuration ({source_format} → {format_type})",
            )
        )

        # Offer to save
        if click.confirm(f"Save converted configuration as {format_type} format?"):
            output_path = generator.save_config(new_config, format_type)
            console.print(f"[green]Converted configuration saved to: {output_path}[/green]")

    except Exception as e:
        console.print(f"[red]Error converting configuration: {e}[/red]")
        sys.exit(1)


# Add adapter commands
create_adapter_cli_commands(main)


if __name__ == "__main__":
    main()
