#!/usr/bin/env bash
set -euo pipefail

# Runs check_vlt_conventions.py automatically after file edits inside a Volto addon.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECKER="${SCRIPT_DIR}/../skills/volto-light-theme/scripts/check_vlt_conventions.py"

if [ ! -f "$CHECKER" ]; then
  exit 0
fi

# Only run if the current working directory looks like a Volto Light Theme project
if compgen -G "frontend/packages/*/src" > /dev/null 2>&1; then
  python3 "$CHECKER" . || true
fi
