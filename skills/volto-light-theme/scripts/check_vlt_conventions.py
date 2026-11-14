#!/usr/bin/env python3
"""Check a Volto Light Theme addon for Semantic UI remnants."""

import glob
import os
import re
import sys


def resolve_src_dirs(target: str) -> list[str]:
    if os.path.basename(os.path.normpath(target)) == "src" and os.path.isdir(target):
        return [target]

    direct_src = os.path.join(target, "src")
    if os.path.isdir(direct_src):
        return [direct_src]

    pkg_srcs = sorted(glob.glob(os.path.join(target, "frontend/packages/*/src")))
    return [p for p in pkg_srcs if os.path.isdir(p)]


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    src_dirs = resolve_src_dirs(target)
    if not src_dirs:
        print(
            f"No addon src directory found under: {target}\n"
            "Pass the path to your addon (or addon/src) or run from the repo root.",
            file=sys.stderr,
        )
        return 1

    issues = []
    for src in src_dirs:
        for root, _, files in os.walk(src):
            for name in files:
                if not name.endswith((".ts", ".tsx", ".js", ".jsx", ".scss")):
                    continue
                path = os.path.join(root, name)
                with open(path, encoding="utf-8", errors="ignore") as f:
                    for idx, line in enumerate(f, 1):
                        if "semantic-ui-react" in line:
                            issues.append(f"{path}:{idx}: forbidden semantic-ui-react import")
                        if name.endswith(".scss") and re.search(r"(^|[\s,{])\.ui\.", line):
                            issues.append(f"{path}:{idx}: avoid .ui.* Semantic UI selector")

    if issues:
        print("\n".join(issues))
        return 1
    print(f"OK: zero Semantic UI imports or .ui.* selectors found in {', '.join(src_dirs)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
