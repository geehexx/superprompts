# Cursor Rules Usage Guide

## Purpose

Explain Cursor rule types, frontmatter fields, and how to write effective rules under `.cursor/rules/`.

## Rule Types

- Always: Apply in all contexts; avoid broad globs.
- Auto Attached: Attach automatically when `when` predicates match (preferred default).
- Agent Requested: Shown when the agent asks for specific guidance.
- Manual: Shown on demand.

## Frontmatter Fields

- description: Short purpose (1–2 sentences).
- type: One of testing|documentation|code_quality|architecture|security|performance|general.
- globs: Specific file globs affected by this rule.
- ruleType: One of Always | Auto Attached | Agent Requested | Manual.
- alwaysApply: true/false (if true, omit `when`).
- appliesTo: Optional list of targets/audiences.
- when: Predicate with `filesChanged`, `pathsPresent`, `languages` arrays.
- tags: Optional labels to aid discovery.
- severity: critical|high|medium|low|info (empty if unclear).
- scope: Optional granular scope labels (e.g., unit-tests, e2e, api-design).

## Markdown Structure

```
---
description: Short purpose
type: <category>
globs:
  - src/**/*.{ts,tsx}
alwaysApply: false
appliesTo: []
when:
  filesChanged: []
  pathsPresent: []
  languages: []
tags: []
severity: ""
scope: []
---
# <Title>
## Description
## Rule
## Examples
## Rationale
## Priority
## Confidence
```

## Writing Effective Rules

- Prefer narrow, precise globs.
- Keep rules short and scannable.
- Provide 1–2 runnable examples.
- Use Auto Attached with specific `when` predicates when possible.
- Avoid duplication; propose merges when overlap >0.7.

## Filenames

- Location: `.cursor/rules/`
- Pattern: `<type>-<slug>.md` where `type` matches frontmatter `type`
- Slug: derived from the H1 title, lowercase kebab-case
- Example: `testing-js-ts-testing-standards.md`

## Validator Options

- Default: schema + semantic checks
- `--strict`: also enforces filename pattern and requires `ruleType`
- `--fix`: with `--strict`, auto-renames files to expected `<type>-<slug>.md` (safe; no content changes)
- `--report-json <path>`: writes a machine-readable report with per-file errors, warnings, and fixes

## Validation

- Use `scripts/validate_cursor_rules.py` to validate frontmatter against `schemas/cursor_rule_frontmatter.schema.json`.
- Pre-commit and CI run this validator automatically.

## Cross-References

- AI Prompting Best Practices: [`ai_prompting_best_practices.md`](ai_prompting_best_practices.md)
- Cursor Rules Prompt: [`../prompts/generate_cursor_rules.prompt.md`](../prompts/generate_cursor_rules.prompt.md)
