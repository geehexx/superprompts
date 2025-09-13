#!/usr/bin/env python3
"""Tests for the MCP-compliant server implementation."""

import pytest

from superprompts.mcp.server import (
    cursor_rules_prompt_handler,
    get_completion_suggestions,
    get_prompt_by_id,
    get_prompts_list,
    repo_docs_prompt_handler,
)


class TestMCPServer:
    """Test MCP server functionality."""

    def test_get_prompts_list(self) -> None:
        """Test getting list of all prompts."""
        prompts = get_prompts_list()

        assert isinstance(prompts, list)
        assert len(prompts) == 2

        # Check that both prompts are present
        prompt_ids = [p["id"] for p in prompts]
        assert "repo_docs" in prompt_ids
        assert "cursor_rules" in prompt_ids

        # Check MCP-compliant structure
        for prompt in prompts:
            assert "id" in prompt
            assert "name" in prompt
            assert "title" in prompt
            assert "description" in prompt
            assert "arguments" in prompt
            assert isinstance(prompt["arguments"], list)

    def test_get_prompt_by_id(self) -> None:
        """Test getting specific prompt by ID."""
        # Test existing prompt
        prompt = get_prompt_by_id("repo_docs")
        assert prompt is not None
        assert prompt["id"] == "repo_docs"
        assert prompt["name"] == "Repository Documentation Rebuilder"

        # Test non-existing prompt
        prompt = get_prompt_by_id("nonexistent")
        assert prompt is None

    def test_repo_docs_prompt_handler(self) -> None:
        """Test repository docs prompt handler."""
        # Test without parameters
        result = repo_docs_prompt_handler.fn()
        assert isinstance(result, str)
        assert len(result) > 0

        # Test with parameters
        result = repo_docs_prompt_handler.fn(
            {
                "batch_size": 3,
                "target_doc_types": ["README", "API"],
                "confidence_threshold": 0.9,
            }
        )
        assert isinstance(result, str)
        assert len(result) > 0

    def test_cursor_rules_prompt_handler(self) -> None:
        """Test cursor rules prompt handler."""
        # Test without parameters
        result = cursor_rules_prompt_handler.fn()
        assert isinstance(result, str)
        assert len(result) > 0

        # Test with parameters
        result = cursor_rules_prompt_handler.fn(
            {
                "target_categories": ["testing", "documentation"],
                "rule_types": ["Auto Attached"],
                "similarity_threshold": 0.8,
            }
        )
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_completion_suggestions_all_arguments(self) -> None:
        """Test getting completion suggestions for all arguments."""
        suggestions = get_completion_suggestions("repo_docs")

        assert isinstance(suggestions, list)
        assert len(suggestions) > 0

        # Check structure
        for suggestion in suggestions:
            assert "name" in suggestion
            assert "description" in suggestion
            assert "type" in suggestion
            assert "required" in suggestion

    def test_get_completion_suggestions_specific_argument(self) -> None:
        """Test getting completion suggestions for specific argument."""
        suggestions = get_completion_suggestions("cursor_rules", "target_categories")

        assert isinstance(suggestions, list)
        assert len(suggestions) > 0

        # Should have specific suggestions for target_categories
        suggestion_names = [s["name"] for s in suggestions]
        assert "testing" in suggestion_names
        assert "documentation" in suggestion_names
        assert "code_quality" in suggestion_names

    def test_get_completion_suggestions_nonexistent_prompt(self) -> None:
        """Test getting completion suggestions for non-existent prompt."""
        suggestions = get_completion_suggestions("nonexistent")
        assert suggestions == []

    def test_get_completion_suggestions_nonexistent_argument(self) -> None:
        """Test getting completion suggestions for non-existent argument."""
        suggestions = get_completion_suggestions("repo_docs", "nonexistent")
        assert suggestions == []

    def test_prompt_metadata_structure(self) -> None:
        """Test that prompt metadata has correct MCP-compliant structure."""
        prompts = get_prompts_list()

        for prompt in prompts:
            # Check required fields
            assert "id" in prompt
            assert "name" in prompt
            assert "title" in prompt
            assert "description" in prompt
            assert "arguments" in prompt

            # Check arguments structure
            for arg in prompt["arguments"]:
                assert "name" in arg
                assert "description" in arg
                assert "required" in arg
                assert "type" in arg
                assert arg["type"] in ["string", "number", "boolean", "array", "object"]

    def test_prompt_parameter_validation(self) -> None:
        """Test that prompts handle parameter validation correctly."""
        # Test with invalid parameters - should not crash
        result = repo_docs_prompt_handler.fn({"invalid_param": "value"})
        assert isinstance(result, str)

        result = cursor_rules_prompt_handler.fn({"invalid_param": "value"})
        assert isinstance(result, str)

    def test_prompt_with_empty_parameters(self) -> None:
        """Test prompts with empty parameter dictionaries."""
        result = repo_docs_prompt_handler.fn({})
        assert isinstance(result, str)
        assert len(result) > 0

        result = cursor_rules_prompt_handler.fn({})
        assert isinstance(result, str)
        assert len(result) > 0


if __name__ == "__main__":
    pytest.main([__file__])
