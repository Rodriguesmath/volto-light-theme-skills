#!/usr/bin/env bash
set -euo pipefail

# Unified installer for Volto Light Theme + companion Plone/React/A11y skills.
# Override AGENT (e.g. AGENT=claude-code) to target a single agent instead of all ('*').
AGENT="${AGENT:-*}"

npx --yes skills add https://github.com/Rodriguesmath/volto-light-theme-skills -a "$AGENT" -g -s '*' -y
npx --yes skills add https://github.com/codesyntax/plone-expert-developer -a "$AGENT" -g -s '*' -y
npx --yes skills add https://github.com/vercel-labs/agent-skills -a "$AGENT" -g -s '*' -y
