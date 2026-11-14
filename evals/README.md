# VLT Skill Evaluations

`cases.json` defines 6 canonical Volto Light Theme tasks used to verify that an agent with `volto-light-theme` loaded:

1. Stops at the earliest valid rung of the **Customization Ladder** (Tokens → Slots → Registry → Shadowing).
2. Uses `--theme-*` / `--block-theme-*` semantic tokens instead of raw hex values.
3. Never imports `semantic-ui-react`, never writes `.ui.*` selectors, and never edits `frontend/core/`.
4. Strips `position: absolute` and fixed `px` dimensions from Figma Inspect snippets.
