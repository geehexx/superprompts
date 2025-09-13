#!/usr/bin/env python3
"""FastMCP Server for SuperPrompts
Provides tools for accessing and composing AI prompts from the superprompts collection.
"""

from typing import Any

from fastmcp import FastMCP

from superprompts.prompts.cursor_rules import CursorRulesPrompt
from superprompts.prompts.repo_docs import RepoDocsPrompt

# Initialize the FastMCP server
mcp = FastMCP("superprompts")

# Initialize prompt handlers
repo_docs_prompt = RepoDocsPrompt()
cursor_rules_prompt = CursorRulesPrompt()


@mcp.tool
def list_prompts(category: str = "all") -> list[dict[str, Any]]:
    """List all available prompts with their metadata.

    Args:
        category: Filter prompts by category (docs, rules, all)

    Returns:
        List of prompt metadata dictionaries

    """
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

    return prompts


@mcp.tool
def get_prompt(prompt_id: str, parameters: dict[str, Any] | None = None) -> str:
    """Get a specific prompt by ID with optional parameters.

    Args:
        prompt_id: The ID of the prompt to retrieve (repo_docs, cursor_rules)
        parameters: Optional parameters to customize the prompt

    Returns:
        The generated prompt text

    """
    if parameters is None:
        parameters = {}

    if prompt_id == "repo_docs":
        return repo_docs_prompt.get_prompt(parameters)
    if prompt_id == "cursor_rules":
        return cursor_rules_prompt.get_prompt(parameters)
    raise ValueError(f"Unknown prompt ID: {prompt_id}")


@mcp.tool
def get_prompt_metadata(prompt_id: str) -> dict[str, Any]:
    """Get detailed metadata about a specific prompt.

    Args:
        prompt_id: The ID of the prompt (repo_docs, cursor_rules)

    Returns:
        Dictionary containing prompt metadata

    """
    if prompt_id == "repo_docs":
        return repo_docs_prompt.get_metadata()
    if prompt_id == "cursor_rules":
        return cursor_rules_prompt.get_metadata()
    raise ValueError(f"Unknown prompt ID: {prompt_id}")


@mcp.tool
def compose_prompt(
    base_prompt_id: str,
    additions: list[dict[str, str]] | None = None,
    customizations: dict[str, Any] | None = None,
) -> str:
    """Compose a custom prompt by combining elements from different prompts.

    Args:
        base_prompt_id: Base prompt to start with (repo_docs, cursor_rules)
        additions: Elements to add from other prompts
        customizations: Custom modifications to apply

    Returns:
        The composed prompt text

    """
    if additions is None:
        additions = []
    if customizations is None:
        customizations = {}

    # Get base prompt
    if base_prompt_id == "repo_docs":
        base_prompt: RepoDocsPrompt | CursorRulesPrompt = repo_docs_prompt
    elif base_prompt_id == "cursor_rules":
        base_prompt = cursor_rules_prompt
    else:
        raise ValueError(f"Unknown base prompt ID: {base_prompt_id}")

    # Start with base prompt
    composed_text = base_prompt.get_prompt({})

    # Add elements from other prompts
    for addition in additions:
        source_prompt_id = addition.get("source_prompt_id")
        element_type = addition.get("element_type")
        element_name = addition.get("element_name")

        if source_prompt_id == "repo_docs":
            source_prompt: RepoDocsPrompt | CursorRulesPrompt = repo_docs_prompt
        elif source_prompt_id == "cursor_rules":
            source_prompt = cursor_rules_prompt
        else:
            continue

        if element_type and element_name:
            element = source_prompt.get_element(element_type, element_name)
        else:
            element = None
        if element:
            composed_text += f"\n\n## {element_name}\n{element}"

    # Apply customizations
    if customizations:
        # This is a simplified approach - in practice, you'd want more sophisticated customization
        for key, value in customizations.items():
            if isinstance(value, str):
                composed_text = composed_text.replace(f"{{{key}}}", value)

    return composed_text


def main() -> None:
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
