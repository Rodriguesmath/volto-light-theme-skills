---
description: Convert Figma Inspect CSS into upgrade-safe VLT SCSS using semantic tokens and mixins
---

Convert the provided Figma Inspect CSS or screenshot requirements into Volto Light Theme SCSS:

1. Strip `position: absolute`, `top`/`left`, and fixed `px` `width`/`height` from Figma Inspect.
2. Rebuild layout with Flexbox or CSS Grid, `rem`, and `clamp()`.
3. Replace raw hex colors with `--theme-*`, `--primary-color`, or `--block-theme-*` semantic tokens.
4. Reuse VLT (`_layout.scss`), `sc-volto-light-theme` (`_mixins.scss`), and addon mixins (`src/theme/mixins/_index.scss`) before writing custom rules.
5. Never write `.ui.*` Semantic UI selectors.
