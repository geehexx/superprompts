#!/usr/bin/env python3
"""MCP-compliant server for SuperPrompts.

Provides prompts and completion capabilities following MCP specification.
"""

from typing import Any

from fastmcp import FastMCP

from superprompts.prompts.cursor_rules import CursorRulesPrompt
from superprompts.prompts.repo_docs import RepoDocsPrompt

# Initialize the MCP server
mcp = FastMCP("superprompts")

# Initialize prompt handlers
repo_docs_prompt = RepoDocsPrompt()
cursor_rules_prompt = CursorRulesPrompt()

# Store prompts for easy access
PROMPTS = {
    "repo_docs": repo_docs_prompt,
    "cursor_rules": cursor_rules_prompt,
}


@mcp.prompt("repo_docs")  # type: ignore[misc]
def repo_docs_prompt_handler(parameters: dict[str, Any] | None = None) -> str:
    """Repository Documentation Rebuilder prompt.

    Rebuilds and modernizes repository documentation safely with loss auditing and index rebuilding.

    Args:
        parameters: Optional parameters to customize the prompt

    Returns:
        The generated prompt text

    """
    if parameters is None:
        parameters = {}
    return repo_docs_prompt.get_prompt(parameters)


@mcp.prompt("cursor_rules")  # type: ignore[misc]
def cursor_rules_prompt_handler(parameters: dict[str, Any] | None = None) -> str:
    """Cursor Rules Generator prompt.

    Generates high-quality, non-duplicative Cursor rules tailored to the detected stack.

    Args:
        parameters: Optional parameters to customize the prompt

    Returns:
        The generated prompt text

    """
    if parameters is None:
        parameters = {}
    return cursor_rules_prompt.get_prompt(parameters)


def get_prompts_list() -> list[dict[str, Any]]:
    """Get list of all available prompts with MCP-compliant metadata."""
    prompts = []

    for prompt_handler in PROMPTS.values():
        metadata = prompt_handler.get_metadata()
        prompts.append(
            {
                "id": metadata["id"],
                "name": metadata["name"],
                "title": metadata["title"],
                "description": metadata["description"],
                "arguments": metadata["arguments"],
            }
        )

    return prompts


def get_prompt_by_id(prompt_id: str) -> dict[str, Any] | None:
    """Get a specific prompt by ID."""
    if prompt_id in PROMPTS:
        return PROMPTS[prompt_id].get_metadata()
    return None


def get_completion_suggestions(prompt_id: str, argument_name: str | None = None) -> list[dict[str, Any]]:
    """Get completion suggestions for prompt arguments."""
    if prompt_id not in PROMPTS:
        return []

    prompt = PROMPTS[prompt_id]
    metadata = prompt.get_metadata()

    if argument_name:
        # Return suggestions for specific argument
        for arg in metadata["arguments"]:
            if arg["name"] == argument_name:
                return _get_argument_suggestions(arg)
    else:
        # Return all available arguments
        return [
            {
                "name": arg["name"],
                "description": arg["description"],
                "type": arg["type"],
                "required": arg["required"],
            }
            for arg in metadata["arguments"]
        ]

    return []


def _get_argument_suggestions(argument: dict[str, Any]) -> list[dict[str, Any]]:
    """Get specific suggestions for an argument based on its type and name."""
    suggestions = []

    if argument["name"] == "target_categories":
        suggestions = [
            {"name": "testing", "description": "Testing-related rules"},
            {"name": "documentation", "description": "Documentation rules"},
            {"name": "code_quality", "description": "Code quality rules"},
            {"name": "architecture", "description": "Architecture rules"},
            {"name": "security", "description": "Security rules"},
            {"name": "performance", "description": "Performance rules"},
            {"name": "general", "description": "General rules"},
        ]
    elif argument["name"] == "rule_types":
        suggestions = [
            {"name": "Always", "description": "Always applied rules"},
            {"name": "Auto Attached", "description": "Automatically attached rules"},
            {"name": "Agent Requested", "description": "Agent-requested rules"},
            {"name": "Manual", "description": "Manually applied rules"},
        ]
    elif argument["name"] == "target_doc_types":
        suggestions = [
            {"name": "README", "description": "README documentation"},
            {"name": "API", "description": "API documentation"},
            {"name": "guides", "description": "User guides"},
            {"name": "architecture", "description": "Architecture documentation"},
            {"name": "testing", "description": "Testing documentation"},
            {"name": "changelog", "description": "Changelog documentation"},
            {"name": "templates", "description": "Template documentation"},
            {"name": "all", "description": "All documentation types"},
        ]
    elif argument["name"] == "output_format":
        suggestions = [
            {"name": "markdown", "description": "Markdown format"},
            {"name": "json", "description": "JSON format"},
            {"name": "html", "description": "HTML format"},
        ]

    return suggestions


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
