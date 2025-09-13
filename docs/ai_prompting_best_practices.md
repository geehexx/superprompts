# AI Prompting Best Practices (General Guide)

## Purpose

A reusable, high-signal reference for designing robust prompts that generate accurate, auditable, and maintainable outputs across diverse repositories and tasks.

## Core Principles

- **Be explicit**: define role, goals, constraints, outputs, and ordering.
- **Plan then act**: instruct the model to think step-by-step before emitting results.
- **Structure outputs**: specify exact sections and formats (JSON → Markdown → plan).
- **Iterate**: include evaluation and refinement passes; stop on quality threshold.
- **Grounding**: embed reference links and short takeaways to guide decisions.
- **Safety**: require risk callouts (e.g., Content-at-Risk) and revert options.

## Reusable Patterns

### 1) Operating Contract
- Define a fixed output order and what to omit if N/A.
- Example: the `generate_repo_docs.prompt.md` contract (docs-only) ensures consistent automation.

### 2) Self‑Critique & Rubrics
- Add a rubric (0–1) and a checklist the model must silently apply before finalizing.
- Example rubric dimensions: structure completeness, examples, rationale, stack relevance, duplication penalty.

### 3) Few‑Shot Biasing
- Provide 1–3 exemplars for the most important outputs (e.g., rules, index). Keep short but representative.
- Tie exemplars to your schema to promote valid outputs.

### 4) Heuristic Similarity for Duplicates
- Nudge the model to compare keyword/2–3-gram overlap and coarse cosine/Jaccard style reasoning.
- Act on a threshold (>0.7 is a useful default) to merge/split with preservation of unique content.

### 5) Risk-first Editing
- For any destructive change, require a loss auditor: {removed_blocks[], modified_blocks[], moved_blocks[], risk_level} and Recoverables + Revert options.

### 6) Tooling-Agnostic Commands
- Suggest common commands in order of likelihood; never assume specific build tools.
- Encourage graceful skipping if not present.

## Quality Checklists

### Output Structure
- Sections appear in the specified order; no extras.
- Each section is concise but complete; link paths resolve; headings scan well.

### Rules Quality
- Structure present, examples (2–3) present, rationale present.
- Relevant to detected stack; duplicates resolved; confidence recorded.

### Documentation Quality
- Diátaxis mode is clear (task/tutorial/reference/explanation).
- Google Style (clarity, active voice, consistent terminology).
- Summaries first; short paragraphs; explicit inputs/outputs.

## Anti‑Patterns and Safeguards
- Vague outputs: fix by adding a stronger operating contract and exemplars.
- Bloated reasoning in final output: instruct to plan silently, then output only requested sections.
- Silent deletions: mandate Content-at-Risk and Revert options.
- Hard-coded tools: keep commands generic; skip if absent.

## Applying to `generate_repo_docs.prompt.md`
- The docs-only prompt uses: plan-then-act, self-critique rubrics, few-shot exemplars, and a safety-first editing flow.
- Its contract enables incremental approvals and automated tooling around the output.
- **Location**: [`../prompts/generate_repo_docs.prompt.md`](../prompts/generate_repo_docs.prompt.md)
- **Documentation**: [`../prompts/generate_repo_docs.md`](../prompts/generate_repo_docs.md)

## Applying to `generate_cursor_rules.prompt.md`
- The Cursor rules prompt uses: plan-then-act, self-critique rubrics, few-shot exemplars, duplication heuristics, and Cursor-first frontmatter.
- Its contract enables incremental approvals and automated tooling around the output.
- **Location**: [`../prompts/generate_cursor_rules.prompt.md`](../prompts/generate_cursor_rules.prompt.md)
- **Documentation**: [`../prompts/generate_cursor_rules.md`](../prompts/generate_cursor_rules.md)

## Cross-References
- **AI-Ready Documentation Standards**: [`ai_ready_documentation_standards.md`](ai_ready_documentation_standards.md)
- **Available Prompts**: [`../prompts/`](../prompts/)
- **Main Project**: [`../README.md`](../README.md)

## References
- OpenAI Prompt Engineering: https://platform.openai.com/docs/guides/prompt-engineering
- Anthropic Prompting: https://docs.anthropic.com/claude/prompt-engineering
- Prompting Guide (CoT/Few-shot/ReAct/SC): https://www.promptingguide.ai/
