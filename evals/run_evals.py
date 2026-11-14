#!/usr/bin/env python3
"""Executable evaluation runner for volto-light-theme-skills.

Usage:
  python3 evals/run_evals.py --validate-only
  python3 evals/run_evals.py --responses evals/sample_responses
  python3 evals/run_evals.py --cli claude
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parent
DEFAULT_CASES = EVALS_DIR / "cases.json"
SKILL_MD = EVALS_DIR.parent / "skills" / "volto-light-theme" / "SKILL.md"


def load_cases(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("cases.json must be a non-empty JSON array")
    required = {"id", "category", "prompt", "expected_rung", "must_contain", "must_not_contain"}
    for case in data:
        missing = required - set(case.keys())
        if missing:
            raise ValueError(f"Case {case.get('id', '?')} missing keys: {sorted(missing)}")
    return data


def score_response(case: dict, text: str) -> tuple[bool, list[str]]:
    lower = text.lower()
    failures: list[str] = []
    for token in case["must_contain"]:
        if token.lower() not in lower:
            failures.append(f"missing required: {token!r}")
    for token in case["must_not_contain"]:
        if token.lower() in lower:
            failures.append(f"forbidden found: {token!r}")
    return (len(failures) == 0, failures)


def run_cli_case(cli: str, prompt: str, skill_text: str) -> str:
    full_prompt = f"{skill_text}\n\nTask:\n{prompt}"
    if cli == "claude":
        cmd = ["claude", "-p", full_prompt]
    elif cli == "gemini":
        cmd = ["gemini", "-p", full_prompt]
    else:
        raise ValueError(f"Unsupported CLI: {cli}")
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=120, check=False)
    return res.stdout + "\n" + res.stderr


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run or validate VLT skill evals.")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--validate-only", action="store_true", help="Validate cases.json schema only")
    parser.add_argument("--responses", type=Path, help="Directory with <case-id>.txt/.md response files")
    parser.add_argument("--cli", choices=("claude", "gemini"), help="Execute prompts live against an agent CLI")
    args = parser.parse_args(argv)

    cases = load_cases(args.cases)
    if args.validate_only:
        print(f"OK: validated {len(cases)} eval case(s) in {args.cases}.")
        return 0

    if not args.responses and not args.cli:
        parser.error("Provide --validate-only, --responses <dir>, or --cli <claude|gemini>")

    skill_text = SKILL_MD.read_text(encoding="utf-8") if args.cli else ""
    passed = 0
    for case in cases:
        cid = case["id"]
        if args.responses:
            candidates = [args.responses / f"{cid}.md", args.responses / f"{cid}.txt"]
            match = next((p for p in candidates if p.exists()), None)
            if not match:
                print(f"FAIL {cid}: missing response file in {args.responses}")
                continue
            text = match.read_text(encoding="utf-8")
        else:
            text = run_cli_case(args.cli, case["prompt"], skill_text)

        ok, failures = score_response(case, text)
        if ok:
            passed += 1
            print(f"PASS {cid}")
        else:
            print(f"FAIL {cid}: {', '.join(failures)}")

    print(f"\nScore: {passed}/{len(cases)} passed.")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
