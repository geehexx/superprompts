#!/usr/bin/env python3
"""Simple test script for the MCP server."""

import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from superprompts.mcp.server import compose_prompt, get_prompt, get_prompt_metadata, list_prompts


async def test_server() -> None:
    """Test the MCP server functionality."""
    # Test list_prompts
    prompts = list_prompts.fn("all")
    for _prompt in prompts:
        pass

    # Test get_prompt_metadata
    get_prompt_metadata.fn("repo_docs")

    # Test get_prompt with parameters
    get_prompt.fn(
        "cursor_rules",
        {
            "target_categories": ["testing", "documentation"],
            "batch_size": 3,
            "confidence_threshold": 0.9,
        },
    )

    # Test compose_prompt
    compose_prompt.fn(
        "repo_docs",
        [
            {
                "source_prompt_id": "cursor_rules",
                "element_type": "principle",
                "element_name": "high_signal",
            }
        ],
        {"batch_size": "3"},
    )


if __name__ == "__main__":
    asyncio.run(test_server())
