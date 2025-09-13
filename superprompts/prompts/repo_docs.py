"""Repository Documentation Rebuilder prompt handler.
"""

from typing import Any

from .base import BasePrompt, PromptCategory, PromptMetadata


class RepoDocsPrompt(BasePrompt):
    """Handler for the Repository Documentation Rebuilder prompt."""

    def _create_metadata(self) -> PromptMetadata:
        return PromptMetadata(
            id="repo_docs",
            name="Repository Documentation Rebuilder",
            description="Rebuilds and modernizes repository documentation safely with loss auditing and index rebuilding",
            category=PromptCategory.DOCS,
            version="1.0.0",
            phases=[
                "discovery",
                "gaps_analysis",
                "mapping",
                "generation",
                "qa",
                "index_rebuild",
            ],
            parameters=[
                "batch_size",
                "target_doc_types",
                "confidence_threshold",
                "include_examples",
                "output_format",
            ],
            examples=[
                {
                    "name": "Basic Documentation Rebuild",
                    "parameters": {
                        "batch_size": 3,
                        "target_doc_types": ["README", "API", "guides"],
                        "confidence_threshold": 0.8,
                    },
                },
                {
                    "name": "API Documentation Only",
                    "parameters": {
                        "batch_size": 5,
                        "target_doc_types": ["API"],
                        "include_examples": True,
                    },
                },
            ],
            usage_instructions="Use this prompt to systematically rebuild repository documentation with safety checks and loss auditing",
            customization_options=[
                "Adjust batch size for processing",
                "Select specific documentation types",
                "Set confidence thresholds",
                "Include or exclude examples",
                "Choose output format (JSON, Markdown, etc.)",
            ],
        )

    def get_prompt(self, parameters: dict[str, Any]) -> str:
        """Get the repository docs prompt with parameters applied."""
        params = self.validate_parameters(parameters)

        # Default parameters
        batch_size = params.get("batch_size", 5)
        target_doc_types = params.get("target_doc_types", ["all"])
        confidence_threshold = params.get("confidence_threshold", 0.8)
        include_examples = params.get("include_examples", True)
        output_format = params.get("output_format", "markdown")

        # Build the prompt
        prompt_parts = [
            "# Repo Documentation Rebuilder + Diff/Loss Auditor + Index Rebuilder (Docs‑Only)",
            "# Extended Quality Edition — prioritize clarity and completeness over token minimalism",
            "",
            "Quality-over-Tokens",
            "- Favor clarity, completeness, and correctness over brevity. Optimize tokens only where it does not reduce quality.",
            "",
            "Operating Mode & Output Contract (produce in this order; omit if N/A)",
            "1) RepoDocsInventory (JSON)",
            "2) DocGapsReport (JSON)",
            "3) MappingPlan (JSON) + BatchPlan (≤{batch_size} items)",
            "4) ProposedDocs (new files; full contents)",
            "5) ProposedEdits (existing files; minimal diffs or full contents)",
            "6) ContentAtRisk",
            "7) DocDiffReport + Recoverables",
            "8) IndexProposal",
            "9) QA Checklist",
            "10) Generic Commands",
            "11) NextBatchRecommendation",
            "",
            "Global Guardrails",
            "- No silent content loss. Any removal/condensing must appear in ContentAtRisk with reinsertion targets.",
            "- Batches ≤{batch_size} files per round; await approval.",
            "- Tooling-agnostic: suggest generic commands; never assume specific build tools or project-specific scripts.",
            "",
            "Advanced Prompting Controls",
            "- Plan then Act: think step-by-step, then produce outputs.",
            "- Self‑Critique pass: apply rubrics/checklists before finalizing each section; revise if needed.",
            "- Few‑Shot biasing: rely on exemplars embedded below to shape structure/quality.",
            "- Hallucination guard: when uncertain, state assumptions and verification steps.",
            "",
            "Phase 0 — Discovery & Signals",
            "- Detect: languages, frameworks, tests, docs (README, docs/**), docstring density, API surfaces.",
            "- Build RepoDocsInventory: [{{path, title, headings[], category(user|technical|api|dev|business|templates|other), status(active|archive|unknown), size_bytes}}]",
            "- Summarize signals: {{languages[], frameworks[], test_runners[], doc_roots[], ci_hints[], package_managers[]}}",
            "- List ambiguities/conflicts needing tie-breaks.",
            "",
            "Phase 1 — DocGapsReport",
            "- Identify missing or stale docs: getting-started, architecture, developer guide, API references, testing, changelog, templates.",
            "- Detect undocumented public APIs: classes/functions/modules (per language) lacking docstrings or reference pages.",
        ]

        # Add target doc types configuration
        if target_doc_types != ["all"]:
            prompt_parts.extend(
                [
                    "",
                    "Target Documentation Types",
                    f"- Focus on: {', '.join(target_doc_types)}",
                    "- Skip other documentation types unless critical for understanding.",
                ]
            )

        # Add confidence threshold
        prompt_parts.extend(
            [
                "",
                "Quality Thresholds",
                f"- Confidence threshold: {confidence_threshold}",
                "- Only propose changes above this threshold.",
                "- Mark uncertain proposals with explicit confidence scores.",
            ]
        )

        # Add examples configuration
        if include_examples:
            prompt_parts.extend(
                [
                    "",
                    "Examples & References",
                    "- Include concrete examples in all proposed documentation.",
                    "- Reference existing patterns and conventions from the codebase.",
                    "- Provide code snippets and usage examples where appropriate.",
                ]
            )

        # Add output format configuration
        if output_format != "markdown":
            prompt_parts.extend(
                [
                    "",
                    "Output Format",
                    f"- Generate outputs in {output_format} format where specified.",
                    "- Maintain consistency with existing documentation standards.",
                ]
            )

        # Join and format the prompt
        full_prompt = "\n".join(prompt_parts)
        return full_prompt.format(batch_size=batch_size)

    def get_element(self, element_type: str, element_name: str) -> str:
        """Get a specific element from the prompt."""
        elements = {
            "phase": {
                "discovery": "Phase 0 — Discovery & Signals\n- Detect: languages, frameworks, tests, docs (README, docs/**), docstring density, API surfaces.",
                "gaps_analysis": "Phase 1 — DocGapsReport\n- Identify missing or stale docs: getting-started, architecture, developer guide, API references, testing, changelog, templates.",
                "mapping": "Phase 2 — MappingPlan\n- Create systematic plan for documentation updates and new content creation.",
                "generation": "Phase 3 — ProposedDocs\n- Generate new documentation files with full contents.",
                "qa": "Phase 4 — QA Checklist\n- Verify quality, completeness, and consistency of generated documentation.",
            },
            "guardrail": {
                "no_silent_loss": "No silent content loss. Any removal/condensing must appear in ContentAtRisk with reinsertion targets.",
                "batch_approval": "Batches ≤5 files per round; await approval.",
                "tooling_agnostic": "Tooling-agnostic: suggest generic commands; never assume specific build tools or project-specific scripts.",
            },
            "output_contract": "1) RepoDocsInventory (JSON)\n2) DocGapsReport (JSON)\n3) MappingPlan (JSON) + BatchPlan (≤5 items)\n4) ProposedDocs (new files; full contents)\n5) ProposedEdits (existing files; minimal diffs or full contents)\n6) ContentAtRisk\n7) DocDiffReport + Recoverables\n8) IndexProposal\n9) QA Checklist\n10) Generic Commands\n11) NextBatchRecommendation",
        }

        return elements.get(element_type, {}).get(element_name, "")

    def validate_parameters(self, parameters: dict[str, Any]) -> dict[str, Any]:
        """Validate and sanitize parameters."""
        validated = parameters.copy()

        # Validate batch_size
        if "batch_size" in validated:
            batch_size = validated["batch_size"]
            if not isinstance(batch_size, int) or batch_size < 1 or batch_size > 10:
                validated["batch_size"] = 5

        # Validate target_doc_types
        if "target_doc_types" in validated:
            valid_types = [
                "README",
                "API",
                "guides",
                "architecture",
                "testing",
                "changelog",
                "templates",
                "all",
            ]
            doc_types = validated["target_doc_types"]
            if isinstance(doc_types, list):
                validated["target_doc_types"] = [
                    t for t in doc_types if t in valid_types
                ]
            else:
                validated["target_doc_types"] = ["all"]

        # Validate confidence_threshold
        if "confidence_threshold" in validated:
            threshold = validated["confidence_threshold"]
            if (
                not isinstance(threshold, (int, float))
                or threshold < 0
                or threshold > 1
            ):
                validated["confidence_threshold"] = 0.8

        return validated
