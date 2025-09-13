#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    print(
        "ERROR: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr
    )
    raise

try:
    from jsonschema import Draft202012Validator  # type: ignore
except Exception:
    print(
        "ERROR: jsonschema is required. Install with: pip install jsonschema",
        file=sys.stderr,
    )
    raise


SCHEMA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "schemas",
    "cursor_rule_frontmatter.schema.json",
)


def load_schema(schema_path: str) -> dict[str, Any]:
    with open(schema_path, encoding="utf-8") as f:
        return json.load(f)


def find_rule_markdown_files(root: str) -> list[str]:
    results: list[str] = []
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.lower().endswith(".md"):
                # Focus on .cursor/rules content, but allow override via CLI
                results.append(os.path.join(dirpath, name))
    return results


def parse_frontmatter(md_path: str) -> tuple[dict[str, Any], int, int]:
    """Return (frontmatter_dict, start_index, end_index). If none, return ({}, -1, -1)."""
    with open(md_path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    if len(lines) >= 3 and lines[0].strip() == "---":
        # find closing '---'
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                frontmatter_text = "\n".join(lines[1:idx])
                try:
                    data = yaml.safe_load(frontmatter_text)
                    if data is None:
                        data = {}
                    if not isinstance(data, dict):
                        raise ValueError("Frontmatter is not a mapping")
                    return data, 0, idx
                except Exception as exc:
                    raise ValueError(f"Failed to parse frontmatter in {md_path}: {exc}")
    return {}, -1, -1


def validate_frontmatter(
    data: dict[str, Any], validator: Draft202012Validator
) -> list[str]:
    errors: list[str] = []
    for err in validator.iter_errors(data):
        path = "/".join([str(p) for p in err.path])
        loc = f" at '{path}'" if path else ""
        errors.append(f"schema: {err.message}{loc}")
    # Additional semantic checks not easily captured by schema
    # 1) if alwaysApply is true, when must be empty or not present (enforced by schema's maxProperties=0)
    # 2) severity string normalization
    if "severity" in data and isinstance(data.get("severity"), str):
        allowed = {"critical", "high", "medium", "low", "info", ""}
        if data["severity"] not in allowed:
            errors.append(
                "semantic: severity must be one of critical|high|medium|low|info or empty"
            )
    # 3) globs should not be overly broad (heuristic)
    globs = data.get("globs") or []
    if isinstance(globs, list):
        for g in globs:
            if isinstance(g, str) and (g.strip() in {"**/*", "**", "*"}):
                errors.append(f"heuristic: overly broad glob '{g}'")
    # 4) ruleType vs alwaysApply/when coherence
    rt = data.get("ruleType")
    if rt == "Always" and data.get("alwaysApply") is not True:
        errors.append("semantic: ruleType 'Always' requires alwaysApply: true")
    if rt == "Auto Attached" and not data.get("when"):
        errors.append("semantic: ruleType 'Auto Attached' requires 'when' predicates")
    # 5) tags lowercase recommendation
    if isinstance(data.get("tags"), list):
        for t in data["tags"]:
            if isinstance(t, str) and t != t.lower():
                errors.append(f"style: tag '{t}' should be lowercase")
    return errors


def validate_markdown_body(md_path: str, start_idx: int, end_idx: int) -> list[str]:
    """Check required sections exist after frontmatter."""
    errors: list[str] = []
    with open(md_path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    body = lines[end_idx + 1 :] if end_idx >= 0 else lines
    text = "\n".join(body)
    required_sections = [
        "# ",
        "## Description",
        "## Rule",
        "## Examples",
        "## Rationale",
        "## Priority",
        "## Confidence",
    ]
    for sec in required_sections:
        if sec not in text:
            errors.append(f"structure: missing section '{sec.strip()}'")
    # Ensure Examples has some content (bullet or code fence) after the heading
    examples_index = text.find("## Examples")
    if examples_index >= 0:
        after = text[examples_index:].splitlines()[1:20]
        has_example = any(
            (
                ln.strip().startswith("-")
                or ln.strip().startswith("```")
                or ln.strip().startswith("~~~")
            )
            for ln in after
        )
        if not has_example:
            errors.append(
                "structure: '## Examples' should include at least one bullet or code block"
            )
    return errors


def slugify(title: str) -> str:
    lowered = title.strip().lower()
    # Replace non-alphanumeric with hyphen
    slug = re.sub(r"[^a-z0-9]+", "-", lowered)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def extract_title(md_path: str, end_idx: int) -> str:
    with open(md_path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    body = lines[end_idx + 1 :] if end_idx >= 0 else lines
    for ln in body:
        if ln.strip().startswith("# "):
            return ln.strip()[2:].strip()
        if ln.strip():
            # first non-empty line wasn't a title
            break
    return ""


def validate_filename(
    md_path: str, frontmatter: dict[str, Any], title: str
) -> list[str]:
    errors: list[str] = []
    # Only enforce for files under .cursor/rules/
    norm = md_path.replace("\\", "/")
    if "/.cursor/rules/" not in norm and not norm.endswith("/.cursor/rules"):
        return errors
    basename = os.path.basename(md_path)
    if not basename.endswith(".md"):
        errors.append("filename: rule files must end with .md")
        return errors
    name_without_ext = basename[:-3]
    # Expected: <category>-<slug>
    category = str(frontmatter.get("type", "")).strip()
    if not category:
        errors.append(
            "filename: frontmatter 'type' missing; cannot validate filename pattern"
        )
        return errors
    expected_prefix = category
    if title:
        expected_slug = slugify(title)
        expected = f"{expected_prefix}-{expected_slug}"
        if name_without_ext != expected:
            errors.append(f"filename: expected '{expected}.md' based on type and title")
    # enforce lowercase kebab-case
    if name_without_ext != name_without_ext.lower() or re.search(
        r"[^a-z0-9-]", name_without_ext
    ):
        errors.append("filename: must be lowercase kebab-case (a-z, 0-9, hyphen)")
    # ensure filename category matches frontmatter 'type'
    if not name_without_ext.startswith(f"{category}-"):
        errors.append("filename: file name category must match frontmatter 'type'")
    return errors


def compute_expected_filename(
    md_path: str, frontmatter: dict[str, Any], title: str
) -> str:
    norm = md_path.replace("\\", "/")
    if "/.cursor/rules/" not in norm and not norm.endswith("/.cursor/rules"):
        return ""
    category = str(frontmatter.get("type", "")).strip()
    if not category or not title:
        return ""
    expected_slug = slugify(title)
    expected = f"{category}-{expected_slug}.md"
    return os.path.join(os.path.dirname(md_path), expected)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Cursor rule frontmatter in Markdown files"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=[".cursor/rules"],
        help="Paths or files to validate (default: .cursor/rules)",
    )
    parser.add_argument(
        "--schema", default=SCHEMA_PATH, help="Path to JSON schema for frontmatter"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors and enforce filename conventions",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-rename files to expected '<type>-<slug>.md' when possible",
    )
    parser.add_argument(
        "--report-json", help="Write a JSON report of findings to this path"
    )
    args = parser.parse_args()

    schema = load_schema(args.schema)
    validator = Draft202012Validator(schema)

    targets: list[str] = []
    for p in args.paths:
        if os.path.isdir(p):
            targets.extend(find_rule_markdown_files(p))
        else:
            targets.append(p)

    if not targets:
        print("No Markdown files found to validate.")
        return 0

    any_errors = False
    report: dict[str, Any] = {"files": []}
    for md in sorted(set(targets)):
        try:
            fm, fm_start, fm_end = parse_frontmatter(md)
        except Exception as exc:
            print(f"{md}: ERROR: {exc}")
            any_errors = True
            continue
        file_entry: dict[str, Any] = {
            "path": md,
            "errors": [],
            "warnings": [],
            "fixed": [],
        }
        if not fm:
            msg = "WARNING: No frontmatter found; skipping schema validation"
            print(f"{md}: {msg}")
            file_entry["warnings"].append(msg)
            report["files"].append(file_entry)
            continue
        errs = validate_frontmatter(fm, validator)
        errs += validate_markdown_body(md, fm_start, fm_end)
        title = extract_title(md, fm_end)
        if args.strict:
            errs += validate_filename(md, fm, title)
            if args.fix:
                expected_path = compute_expected_filename(md, fm, title)
                if expected_path and os.path.abspath(expected_path) != os.path.abspath(
                    md
                ):
                    if os.path.exists(expected_path):
                        errs.append(
                            f"fix: cannot rename; target exists: {expected_path}"
                        )
                    else:
                        try:
                            os.rename(md, expected_path)
                            print(f"FIX: renamed {md} -> {expected_path}")
                            file_entry["fixed"].append(
                                {"action": "rename", "from": md, "to": expected_path}
                            )
                            # After rename, update md path for subsequent messages
                            md = expected_path
                        except Exception as exc:
                            errs.append(
                                f"fix: failed to rename to {expected_path}: {exc}"
                            )
        # Encourage ruleType presence in strict mode
        if args.strict and not fm.get("ruleType"):
            errs.append(
                "style: add 'ruleType' (Always | Auto Attached | Agent Requested | Manual)"
            )
        file_entry["errors"].extend(errs)
        report["files"].append(file_entry)
        if errs:
            any_errors = True
            for e in errs:
                print(f"{md}: {e}")
        else:
            print(f"{md}: OK")

    if args.report_json:
        try:
            with open(args.report_json, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
        except Exception as exc:
            print(f"ERROR: failed to write report to {args.report_json}: {exc}")
            any_errors = True

    return 1 if any_errors else 0


if __name__ == "__main__":
    sys.exit(main())
