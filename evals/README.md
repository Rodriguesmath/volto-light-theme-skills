# VLT Skill Evaluations

`cases.json` defines 6 canonical Volto Light Theme tasks used to verify that an agent with `volto-light-theme` loaded:

1. Stops at the earliest valid rung of the **Customization Ladder** (Tokens → Slots → Registry → Shadowing).
2. Uses `--theme-*` / `--block-theme-*` semantic tokens instead of raw hex values.
3. Never imports `semantic-ui-react`, never writes `.ui.*` selectors, and never edits `frontend/core/`.
4. Strips `position: absolute` and fixed `px` dimensions from Figma Inspect snippets.

## Running

```bash
# Validate eval schema
python3 evals/run_evals.py --validate-only

# Score saved response files (<case-id>.md or .txt)
python3 evals/run_evals.py --responses /path/to/responses

# Run live against Claude Code or Gemini CLI
python3 evals/run_evals.py --cli claude
```
