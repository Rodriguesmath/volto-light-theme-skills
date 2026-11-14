# VLT, `sc-volto-light-theme` & Addon Mixins and Tokens

## 1. Semantic Token Rules (`sc-volto-light-theme` / VLT)

- **Semantic only:** Read `--theme-*`, `--primary-color`, `--secondary-color`, `--accent-color` (`light-dark()` pairs). Never read base tokens (`--gray-80`, raw hex) inside components.
- **`@property` constraint:** Six tokens (`--primary-color`, `--primary-foreground-color`, `--secondary-color`, `--secondary-foreground-color`, `--accent-color`, `--accent-foreground-color`) are registered with `@property` and resolve at `:root`. Keep `color-scheme` on `<html>` (and on both `:root` + wrapper in Storybook).
- **Block theme contract:** Every `--theme-*` read in SCSS must be supplied by `createThemeDefinition` and declared in `src/theme/_root.scss`. Undefined `var()` without fallback is dropped silently at computed-value time.

## 2. Layout & Helper Mixins

- **VLT layout (`_layout.scss`):**
  - `narrow-container-width()` (`--narrow-container-width`, default `620px`)
  - `default-container-width()` (`--default-container-width`, default `940px`)
  - `layout-container-width()` (`--layout-container-width`, default `1440px`)
  - `variable-container-width()` (dynamic `--block-width`)
- **`sc-volto-light-theme` helpers (`_mixins.scss`, `_typography.scss`):**
  - `flex-center($direction, $inline)`, `sr-only()`, `focus-ring($color, $width, $offset)`
  - `hover-mix-darken()`, `divider-border()`, `muted-color()`, `dropdown-overlay()`
  - `h2_base()`, `h2_block()`, `h2_headline()`
- **Project addon mixins (`src/theme/mixins/_index.scss`):**
  Organize project-specific mixins by concern (e.g. `_typography.scss`, `_layout.scss`, `_forms.scss`, `_buttons.scss`, `_indicators.scss`, `_accessibility.scss`) rather than duplicating CSS across blocks.

## 3. Figma (Images + Layer CSS) Conversion

- Strip `position: absolute`, fixed `px` `width`/`height`, and `top`/`left` from Figma Inspect.
- Rebuild with Flexbox/Grid, `rem`, and `clamp()`.
- Map Figma colors, font sizes, and radii to `--theme-*`, `--block-theme-*`, and `--font-scale` steps in `_root.scss`.
