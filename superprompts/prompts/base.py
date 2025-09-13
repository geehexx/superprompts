"""Base classes for prompt handling in the MCP server."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any


class PromptCategory(Enum):
    DOCS = "docs"
    RULES = "rules"
    GENERAL = "general"


@dataclass
class PromptArgument:
    """MCP-compliant prompt argument definition."""

    name: str
    description: str
    required: bool = False
    type: str = "string"  # string, number, boolean, array, object


@dataclass
class PromptMetadata:
    """MCP-compliant metadata for a prompt."""

    id: str
    name: str
    title: str  # Required by MCP spec
    description: str
    category: PromptCategory
    version: str
    phases: list[str]
    arguments: list[PromptArgument]  # MCP-compliant arguments
    examples: list[dict[str, Any]]
    usage_instructions: str
    customization_options: list[str]


class BasePrompt(ABC):
    """Base class for all prompts."""

    def __init__(self) -> None:
        self.metadata = self._create_metadata()

    @abstractmethod
    def _create_metadata(self) -> PromptMetadata:
        """Create metadata for this prompt."""

    @abstractmethod
    def get_prompt(self, parameters: dict[str, Any]) -> str:
        """Get the full prompt text with parameters applied."""

    def get_metadata(self) -> dict[str, Any]:
        """Get prompt metadata as a dictionary."""
        return {
            "id": self.metadata.id,
            "name": self.metadata.name,
            "title": self.metadata.title,
            "description": self.metadata.description,
            "category": self.metadata.category.value,
            "version": self.metadata.version,
            "phases": self.metadata.phases,
            "arguments": [
                {
                    "name": arg.name,
                    "description": arg.description,
                    "required": arg.required,
                    "type": arg.type,
                }
                for arg in self.metadata.arguments
            ],
            "examples": self.metadata.examples,
            "usage_instructions": self.metadata.usage_instructions,
            "customization_options": self.metadata.customization_options,
        }

    def get_element(self, element_type: str, element_name: str) -> str | None:
        """Get a specific element from the prompt."""
        # Override in subclasses to provide element extraction
        return None

    def validate_parameters(self, parameters: dict[str, Any]) -> dict[str, Any]:
        """Validate and sanitize parameters."""
        # Override in subclasses to add validation logic
        return parameters
