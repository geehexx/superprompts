#!/usr/bin/env python3
"""Simple test script for the MCP server.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from superprompts.mcp.server import handle_call_tool, handle_list_tools


async def test_server():
    """Test the MCP server functionality."""
    print("Testing MCP Server for SuperPrompts")
    print("=" * 40)

    # Test list_tools
    print("\n1. Testing list_tools...")
    tools = await handle_list_tools()
    print(f"Found {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")

    # Test list_prompts
    print("\n2. Testing list_prompts...")
    result = await handle_call_tool("list_prompts", {"category": "all"})
    prompts = json.loads(result[0].text)
    print(f"Found {len(prompts)} prompts:")
    for prompt in prompts:
        print(f"  - {prompt['name']} ({prompt['id']})")

    # Test get_prompt_metadata
    print("\n3. Testing get_prompt_metadata...")
    result = await handle_call_tool("get_prompt_metadata", {"prompt_id": "repo_docs"})
    metadata = json.loads(result[0].text)
    print("Repository Docs Prompt:")
    print(f"  - Description: {metadata['description']}")
    print(f"  - Phases: {', '.join(metadata['phases'])}")
    print(f"  - Parameters: {', '.join(metadata['parameters'])}")

    # Test get_prompt with parameters
    print("\n4. Testing get_prompt with parameters...")
    result = await handle_call_tool(
        "get_prompt",
        {
            "prompt_id": "cursor_rules",
            "parameters": {
                "target_categories": ["testing", "documentation"],
                "batch_size": 3,
                "confidence_threshold": 0.9,
            },
        },
    )
    prompt_text = result[0].text
    print("Generated prompt (first 200 chars):")
    print(prompt_text[:200] + "..." if len(prompt_text) > 200 else prompt_text)

    # Test compose_prompt
    print("\n5. Testing compose_prompt...")
    result = await handle_call_tool(
        "compose_prompt",
        {
            "base_prompt_id": "repo_docs",
            "additions": [
                {
                    "source_prompt_id": "cursor_rules",
                    "element_type": "principle",
                    "element_name": "high_signal",
                }
            ],
            "customizations": {"batch_size": "3"},
        },
    )
    composed_text = result[0].text
    print("Composed prompt (first 200 chars):")
    print(composed_text[:200] + "..." if len(composed_text) > 200 else composed_text)

    print("\n✅ All tests completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_server())
