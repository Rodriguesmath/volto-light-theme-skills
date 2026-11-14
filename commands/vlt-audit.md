---
description: Run VLT convention checker and React diagnostics on the current project
---

Run a full Volto Light Theme quality gate on the current repository:

1. Run `python3` against `check_vlt_conventions.py` (with `--strict`) on the addon `src/` directory.
2. Run `npx react-doctor@latest --verbose --scope changed` if React files changed.
3. Report violations grouped by severity (`error` vs `warning`) with exact `file:line` references and concrete fixes.
