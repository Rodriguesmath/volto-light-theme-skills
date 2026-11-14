#!/usr/bin/env python3
"""Static convention checker for Volto Light Theme (VLT) addons.

Checks for:
  - [error]   semantic-ui-react imports in JS/TS files
  - [error]   .ui.* Semantic UI selectors in SCSS files
  - [warning] Hardcoded hex colors in SCSS outside _root.scss / token files
  - [warning] position: absolute in SCSS (common Figma Inspect copy-paste)
  - [warning] Shadowed files in src/customizations/ without a justification comment
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from dataclasses import asdict, dataclass

HEX_RE = re.compile(r"(?<![&\w])#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
UI_SELECTOR_RE = re.compile(r"(^|[\s,{])\.ui\.")
POS_ABS_RE = re.compile(r"position\s*:\s*absolute\b")


@dataclass
class Issue:
    path: str
    line: int
    severity: str  # "error" | "warning"
    rule: str
    message: str


def resolve_src_dirs(target: str) -> list[str]:
    norm = os.path.normpath(target)
    if os.path.basename(norm) == "src" and os.path.isdir(norm):
        return [norm]

    direct_src = os.path.join(norm, "src")
    if os.path.isdir(direct_src):
        return [direct_src]

    pkg_srcs = sorted(glob.glob(os.path.join(norm, "frontend/packages/*/src")))
    return [p for p in pkg_srcs if os.path.isdir(p)]


def is_token_file(rel_path: str) -> bool:
    name = os.path.basename(rel_path)
    return name in {"_root.scss", "_tokens.scss", "tokens.scss"}


def strip_scss_line_comment(line: str) -> str:
    idx = line.find("//")
    return line[:idx] if idx != -1 else line


def scan_src_dir(src: str) -> list[Issue]:
    issues: list[Issue] = []
    for root, _, files in os.walk(src):
        for name in sorted(files):
            if not name.endswith((".ts", ".tsx", ".js", ".jsx", ".scss")):
                continue
            path = os.path.join(root, name)
            rel = os.path.relpath(path, src)

            with open(path, encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            # Check shadowing justification in src/customizations/
            norm_rel = rel.replace(os.sep, "/")
            if norm_rel.startswith("customizations/"):
                header = "".join(lines[:15]).lower()
                if "shadow" not in header and "why:" not in header and "justificativa" not in header:
                    issues.append(
                        Issue(
                            path=path,
                            line=1,
                            severity="warning",
                            rule="shadowing-justification",
                            message="Shadowed file in customizations/ lacks a top comment explaining why rungs 1-3 could not solve it",
                        )
                    )

            for idx, raw_line in enumerate(lines, 1):
                if name.endswith((".ts", ".tsx", ".js", ".jsx")):
                    if "semantic-ui-react" in raw_line:
                        issues.append(
                            Issue(
                                path=path,
                                line=idx,
                                severity="error",
                                rule="no-semantic-ui-react",
                                message="Forbidden semantic-ui-react import",
                            )
                        )
                elif name.endswith(".scss"):
                    code = strip_scss_line_comment(raw_line)
                    if UI_SELECTOR_RE.search(code):
                        issues.append(
                            Issue(
                                path=path,
                                line=idx,
                                severity="error",
                                rule="no-ui-selector",
                                message="Avoid .ui.* Semantic UI selector",
                            )
                        )
                    if not is_token_file(rel) and "url(#" not in code and HEX_RE.search(code):
                        issues.append(
                            Issue(
                                path=path,
                                line=idx,
                                severity="warning",
                                rule="semantic-tokens-only",
                                message="Hardcoded hex color outside _root.scss; prefer --theme-* semantic tokens",
                            )
                        )
                    if POS_ABS_RE.search(code):
                        issues.append(
                            Issue(
                                path=path,
                                line=idx,
                                severity="warning",
                                rule="no-figma-absolute",
                                message="position: absolute detected; prefer Flexbox/Grid unless strictly required",
                            )
                        )
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check Volto Light Theme addon conventions.")
    parser.add_argument("target", nargs="?", default=os.getcwd(), help="Repo root or addon/src path")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Output format")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args(argv)

    src_dirs = resolve_src_dirs(args.target)
    if not src_dirs:
        msg = f"No addon src directory found under: {args.target}"
        if args.format == "json":
            print(json.dumps({"error": msg, "issues": []}))
        else:
            print(msg, file=sys.stderr)
        return 1

    issues: list[Issue] = []
    for src in src_dirs:
        issues.extend(scan_src_dir(src))

    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    failed = bool(errors) or (args.strict and bool(warnings))

    if args.format == "json":
        print(
            json.dumps(
                {
                    "src_dirs": src_dirs,
                    "errors": len(errors),
                    "warnings": len(warnings),
                    "issues": [asdict(i) for i in issues],
                },
                indent=2,
            )
        )
    else:
        for i in issues:
            print(f"{i.path}:{i.line}: [{i.severity}] ({i.rule}) {i.message}")
        if not issues:
            print(f"OK: 0 issues found in {', '.join(src_dirs)}.")
        else:
            print(f"\nSummary: {len(errors)} error(s), {len(warnings)} warning(s).")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
