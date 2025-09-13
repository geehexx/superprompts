# AI‑Ready Documentation Standards (General Guide)

## Purpose

Provide practical, AI‑optimized documentation standards that improve discoverability, readability, and safe maintenance across repositories.

## Documentation Philosophy

- **Diátaxis (recommended)**: separate by purpose — Task (How‑to), Tutorial (Learning), Reference (Facts), Explanation (Why).
- **Google Style**: clarity, active voice, consistent terminology, audience‑first; small units with meaningful headings.
- **Safety and auditability**: prefer small changes with explicit risk callouts and easy reverts.

## Recommended Structure

- **Root README**: quick value, install/run basics, links to canonical docs.
- **Docs Index** (docs/README.md or similar): navigable tree to Task/Tutorial/Reference/Explanation.
- **Code-specific documentation**: Co-locate with code (e.g., `schemas/README.md`, `superprompts/mcp/README.md`)
- **Core topics** (suggested):
  - Getting Started (Task)
  - Architecture (Explanation/Reference)
  - Developer Guide (Task/Reference)
  - Testing Standards (Task/Reference)
  - Rules (Generated) (Reference)
  - Templates (Reference)

## Authoring Standards

- Headings: H1 unique per file; meaningful H2/H3; avoid mixing modes in one page.
- Paragraphs: short, scannable; one idea per paragraph; front‑load key info.
- Lists/Tables: prefer structured lists for actions, tables for matrices.
- Links: relative repo paths; stable anchors; avoid bare URLs in prose (use markdown links).
- Examples: short and runnable where feasible; show inputs/outputs.

## Change Safety (Loss Auditor)

- For edits that remove/condense content, generate a **DocDiffReport**: {removed_blocks[], modified_blocks[], moved_blocks[], risk_level(low|med|high)}.
- Provide **Recoverables** (exact snippets) and **Revert options** (per‑block restores with suggested placements).

## Index & Navigation

- Keep the index minimal; link only canonical docs; avoid duplicating content.
- If multiple roots exist, add a synthetic index that unifies them with relative links.

## Templates (Skeletons)

### Getting Started (Task)
```
# Getting Started
## Prerequisites
## Installation
## Quick Start
## Next Steps
```

### Architecture (Explanation/Reference)
```
# Architecture
## Overview
## Components
## Data Flows
## Constraints & Decisions
## Related Docs
```

### Developer Guide (Task/Reference)
```
# Developer Guide
## Local Development
## Testing
## Linting & Formatting
## Release/CI
## Troubleshooting
```

## QA Checklist (Docs)

- Clear mode (task/tutorial/reference/explanation) and consistent style.
- Headings are logical; links resolve; no duplicated sections.
- Key pages have short summaries and examples.

## Cross-References
- **AI Prompting Best Practices**: [`ai_prompting_best_practices.md`](ai_prompting_best_practices.md)
- **Available Prompts**: [`../prompts/`](../prompts/)
- **Main Project**: [`../README.md`](../README.md)

## References
- Diátaxis: https://diataxis.fr/
- Google Developer Documentation Style Guide: https://developers.google.com/style
- Write the Docs: https://www.writethedocs.org/guide/
- Markdownlint: https://github.com/DavidAnson/markdownlint
- Vale (style linter): https://vale.sh/
