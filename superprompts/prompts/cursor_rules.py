"""Cursor Rules Generator prompt handler."""

from typing import Any

from .base import BasePrompt, PromptCategory, PromptMetadata


class CursorRulesPrompt(BasePrompt):
    """Handler for the Cursor Rules Generator prompt."""

    def _create_metadata(self) -> PromptMetadata:
        return PromptMetadata(
            id="cursor_rules",
            name="Cursor Rules Generator",
            description="Generates high-quality, non-duplicative Cursor rules tailored to the detected stack",
            category=PromptCategory.RULES,
            version="1.0.0",
            phases=["signals", "planning", "generation", "optimization", "placement"],
            parameters=[
                "target_categories",
                "rule_types",
                "similarity_threshold",
                "confidence_threshold",
                "max_rules_per_category",
            ],
            examples=[
                {
                    "name": "Full Stack Rules Generation",
                    "parameters": {
                        "target_categories": [
                            "testing",
                            "documentation",
                            "code_quality",
                        ],
                        "rule_types": ["Auto Attached", "Manual"],
                        "similarity_threshold": 0.7,
                    },
                },
                {
                    "name": "Testing Rules Only",
                    "parameters": {
                        "target_categories": ["testing"],
                        "rule_types": ["Auto Attached"],
                        "max_rules_per_category": 3,
                    },
                },
            ],
            usage_instructions="Use this prompt to generate Cursor IDE rules that are tailored to your specific technology stack and coding practices",
            customization_options=[
                "Select target rule categories",
                "Choose rule attachment types",
                "Set similarity thresholds for deduplication",
                "Limit rules per category",
                "Configure confidence thresholds",
            ],
        )

    def get_prompt(self, parameters: dict[str, Any]) -> str:
        """Get the Cursor rules prompt with parameters applied."""
        params = self.validate_parameters(parameters)

        # Default parameters
        target_categories = params.get(
            "target_categories",
            [
                "testing",
                "documentation",
                "code_quality",
                "architecture",
                "security",
                "performance",
                "general",
            ],
        )
        rule_types = params.get("rule_types", ["Always", "Auto Attached", "Agent Requested", "Manual"])
        similarity_threshold = params.get("similarity_threshold", 0.7)
        confidence_threshold = params.get("confidence_threshold", 0.8)
        max_rules_per_category = params.get("max_rules_per_category", 5)

        # Build the prompt
        prompt_parts = [
            "# Cursor Rules Generator (Cursor‑Optimized) — `.cursor/rules` Authoring, Consolidation, and Quality Assurance",
            "",
            "Cursor‑First Principles",
            "- Generate high-signal, non-duplicative rules tailored to the detected stack.",
            "- Prefer small, focused rules over monoliths; make them scannable in Cursor.",
            "- Use precise globs and attachment modes to minimize noise and maximize utility.",
            "",
            "Operating Mode & Output Contract (produce in this order; omit if N/A)",
            "1) CursorProjectSignals (JSON)",
            "2) RulesPlan (JSON)",
            "3) GeneratedCursorRules (JSON)",
            "4) RuleMarkdownFiles (Markdown with Cursor frontmatter)",
            "5) PlacementPlan (JSON)",
            "6) ProposedEdits (safe)",
            "7) QA Checklist",
            "8) NextBatchRecommendation",
            "",
            "CursorProjectSignals",
            "- Detect: languages, frameworks, test runners, package managers, presence of `.cursor/`, existing rules, repo structure and common directories.",
            '- Output JSON: {{languages[], frameworks[], test_runners[], rule_roots:[".cursor/rules/"], existing_rules:[{{path, title}}], gaps[], assumptions[]}}.',
            "",
            "RulesPlan",
            f'- Output JSON: {{"target_categories":{target_categories}, "per_category_counts":{{...}}, "rationale":"...", "assumptions":[]}}.',
            "",
            "Cursor Rule Schema (JSON for planning)",
            "{{",
            '  "id": "cursor_<category>_<slug>",',
            '  "title": "...",',
            '  "description": "1–2 sentence purpose",',
            f'  "category": "{"|".join(target_categories)}",',
            '  "priority": "critical|high|medium|low",',
            '  "confidence": 0.0,',
            f'  "ruleType": "{"|".join(rule_types)}",',
            '  "frontmatter": {{',
            '    "description": "...",',
            '    "type": "<category>",',
            '    "globs": ["src/**/*.{{ts,tsx}}"],',
            '    "ruleType": "Auto Attached",',
            '    "alwaysApply": false,',
            '    "appliesTo": [],',
            '    "when": {{ "filesChanged": [], "pathsPresent": [], "languages": [] }},',
            '    "tags": [],',
            '    "severity": "",',
            '    "scope": []',
            "  }},",
            '  "content": "markdown rule body (concise but complete)",',
            '  "examples": ["short example 1","short example 2"],',
            '  "rationale": "why it matters; risks reduced",',
            '  "metadata": {{"ide": "cursor", "duplicatesWith": []}},',
            '  "source_context": {{"languages": [], "frameworks": [], "signals": []}}',
            "}}",
            "",
            "Cursor Rule Markdown Format (frontmatter + sections)",
            "---",
            "description: Short purpose",
            "type: <category>",
            "globs:",
            "  - src/**/*.{{ts,tsx}}",
            "ruleType: Auto Attached",
            "alwaysApply: false",
            "appliesTo: []",
            "when:",
            "  filesChanged: []",
            "  pathsPresent: []",
            "  languages: []",
            "tags: []",
            'severity: ""',
            "scope: []",
            "---",
            "# <Title>",
            "## Description",
            "## Rule",
            "## Examples",
            "## Rationale",
            "## Priority",
            "## Confidence",
            "",
            "Generation Pipeline",
            "1) Analyze signals → choose categories and counts.",
            "2) Draft rules (JSON) with concrete globs and `type`.",
            f"3) Optimize: deduplicate (threshold: {similarity_threshold}), reduce scope creep, improve scan-ability, ensure Cursor frontmatter correctness.",
            "4) Emit: Markdown bodies suitable for `.cursor/rules/*.md` with correct frontmatter.",
            "5) Evaluate with rubric; refine ≤3 iterations or stop at score ≥0.9.",
            "",
            "PlacementPlan",
            "- Plan file paths under `.cursor/rules/` using kebab-case filenames: `.cursor/rules/<category>-<slug>.md`.",
            f"- For existing rules, complement not duplicate; propose merges when similarity >{similarity_threshold}.",
            "",
            "ProposedEdits (safe)",
            "- For each new/updated rule, emit minimal diffs or full contents with rationale and impact.",
            "- Never delete existing rules silently; put removals in ContentAtRisk with reinsertion targets.",
            "",
            "QA Checklist (Cursor Rules)",
            "- Frontmatter fields valid and minimal.",
            "- Globs correct and not overly broad.",
            "- Duplicates merged/split; examples realistic and runnable where feasible.",
            "- Category and `ruleType` appropriate; confidence recorded.",
            "- Tags present when helpful; severity set (critical|high|medium|low|info) when appropriate.",
            "",
            "Rubrics & Scoring",
            "- Rule Quality (0–1): +structure +examples +rationale +stack relevance −duplication.",
            "- Confidence (0–1): base 0.5; +structure +relevance +examples; clamp 0–1.",
            "",
            "Quality Thresholds",
            f"- Confidence threshold: {confidence_threshold}",
            f"- Maximum rules per category: {max_rules_per_category}",
            "- Only propose rules above confidence threshold.",
            "- Mark uncertain rules with explicit confidence scores.",
        ]

        # Add rule type specific instructions
        if "Auto Attached" in rule_types:
            prompt_parts.extend(
                [
                    "",
                    "Auto Attached Rules",
                    "- Use `when` predicates to control automatic attachment.",
                    "- Ensure globs are specific to avoid noise.",
                    "- Test attachment conditions with common file patterns.",
                ]
            )

        if "Manual" in rule_types:
            prompt_parts.extend(
                [
                    "",
                    "Manual Rules",
                    "- Focus on comprehensive guidance and examples.",
                    "- Include clear usage instructions.",
                    "- Make them easily discoverable through good titles and descriptions.",
                ]
            )

        # Join and format the prompt
        return "\n".join(prompt_parts)

    def get_element(self, element_type: str, element_name: str) -> str:
        """Get a specific element from the prompt."""
        elements = {
            "phase": {
                "signals": "CursorProjectSignals\n- Detect: languages, frameworks, test runners, package managers, presence of `.cursor/`, existing rules, repo structure and common directories.",
                "planning": 'RulesPlan\n- Output JSON: {"target_categories":[...], "per_category_counts":{...}, "rationale":"...", "assumptions":[]}.',
                "generation": "GeneratedCursorRules\n- Draft rules (JSON) with concrete globs and type.",
                "optimization": "Optimization\n- Deduplicate, reduce scope creep, improve scan-ability, ensure Cursor frontmatter correctness.",
                "placement": "PlacementPlan\n- Plan file paths under `.cursor/rules/` using kebab-case filenames.",
            },
            "schema": {
                "json": '{\n  "id": "cursor_<category>_<slug>",\n  "title": "...",\n  "description": "1–2 sentence purpose",\n  "category": "testing|documentation|code_quality|architecture|security|performance|general",\n  "priority": "critical|high|medium|low",\n  "confidence": 0.0,\n  "ruleType": "Always|Auto Attached|Agent Requested|Manual"\n}',
                "frontmatter": "---\ndescription: Short purpose\ntype: <category>\nglobs:\n  - src/**/*.{ts,tsx}\nruleType: Auto Attached\nalwaysApply: false\n---",
            },
            "principle": {
                "high_signal": "Generate high-signal, non-duplicative rules tailored to the detected stack.",
                "focused_rules": "Prefer small, focused rules over monoliths; make them scannable in Cursor.",
                "precise_globs": "Use precise globs and attachment modes to minimize noise and maximize utility.",
            },
        }

        return elements.get(element_type, {}).get(element_name, "")

    def validate_parameters(self, parameters: dict[str, Any]) -> dict[str, Any]:
        """Validate and sanitize parameters."""
        validated = parameters.copy()

        # Validate target_categories
        if "target_categories" in validated:
            valid_categories = [
                "testing",
                "documentation",
                "code_quality",
                "architecture",
                "security",
                "performance",
                "general",
            ]
            categories = validated["target_categories"]
            if isinstance(categories, list):
                validated["target_categories"] = [c for c in categories if c in valid_categories]
            else:
                validated["target_categories"] = valid_categories

        # Validate rule_types
        if "rule_types" in validated:
            valid_types = ["Always", "Auto Attached", "Agent Requested", "Manual"]
            types = validated["rule_types"]
            if isinstance(types, list):
                validated["rule_types"] = [t for t in types if t in valid_types]
            else:
                validated["rule_types"] = valid_types

        # Validate similarity_threshold
        if "similarity_threshold" in validated:
            threshold = validated["similarity_threshold"]
            if not isinstance(threshold, (int, float)) or threshold < 0 or threshold > 1:
                validated["similarity_threshold"] = 0.7

        # Validate confidence_threshold
        if "confidence_threshold" in validated:
            threshold = validated["confidence_threshold"]
            if not isinstance(threshold, (int, float)) or threshold < 0 or threshold > 1:
                validated["confidence_threshold"] = 0.8

        # Validate max_rules_per_category
        if "max_rules_per_category" in validated:
            max_rules = validated["max_rules_per_category"]
            if not isinstance(max_rules, int) or max_rules < 1 or max_rules > 20:
                validated["max_rules_per_category"] = 5

        return validated
