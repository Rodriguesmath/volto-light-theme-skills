---
description: Decide the lowest-rung VLT customization strategy before writing code
---

Analyze the requested feature or UI change and stop at the earliest possible rung of the Volto Light Theme Customization Ladder:

1. **Tokens & SCSS (`src/theme/_root.scss`)** — Can `--theme-*` / `--block-theme-*` or mixins solve it?
2. **VLT Slots (`src/config/slots.ts`)** — Can `aboveHeader`, `belowHeader`, `headerTools`, `preFooter`, `postFooter`, `footer`, `followUs`, or `footerLinks` solve it?
3. **Registry (`src/config/{components,views,blocks}.ts`)** — Can `registerComponent`, `layoutViews`, `contentTypesViews`, or `blocksConfig` / `variations` solve it?
4. **Shadowing (`src/customizations/`)** — Last resort only. Explicitly state why rungs 1–3 cannot solve it before proceeding.

Output the chosen rung, exact target files, and wait for confirmation if shadowing is required.
