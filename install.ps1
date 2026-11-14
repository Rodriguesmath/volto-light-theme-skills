$ErrorActionPreference = "Stop"

# Unified Windows PowerShell installer for Volto Light Theme + companion skills.
$Agent = if ($env:AGENT) { $env:AGENT } else { "*" }

npx --yes skills add https://github.com/Rodriguesmath/volto-light-theme-skills -a $Agent -g -s "*" -y
npx --yes skills add https://github.com/codesyntax/plone-expert-developer -a $Agent -g -s "*" -y
npx --yes skills add https://github.com/vercel-labs/agent-skills -a $Agent -g -s "*" -y
