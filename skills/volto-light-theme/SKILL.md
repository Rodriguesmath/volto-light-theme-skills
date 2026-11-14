---
name: volto-light-theme
description: >
  Plone 6 and Volto Light Theme (@kitconcept/volto-light-theme / Simples Consultoria /
  PortalBrasil) development rules. Enforces native local dev, pnpm, VLT layers,
  customization ladder (tokens -> slots -> registry -> shadowing last),
  semantic tokens, and block/slot/mixin patterns.
license: MIT
---

# Volto Light Theme (VLT) Development Rules

Terse rules for Plone 6 + Volto projects built on `@kitconcept/volto-light-theme` (and extensions such as `@portalbrasil/intranet` / `sc-volto-light-theme`). Keep diffs minimal and upgrade-safe.

## 1. Local Environment

- Prefer native local dev (e.g., `make backend-start` on `:8080` and `make frontend-start` on `:3000`). Avoid starting containerized stacks unless explicitly requested.
- Use `pnpm` in `frontend/` (`only-allow pnpm`). Never use `npm` or `yarn`.
- Query `graphify-out/` before broad codebase searches when present.
- Never edit `frontend/core/`; keep all frontend customizations inside your project addon (`frontend/packages/<addon-name>/`).

## 2. Customization Ladder (Stop at Earliest Rung)

1. **Tokens & SCSS (`src/theme/`):** Adjust `--theme-*` / `--block-theme-{name}-*` in `_root.scss` and reuse VLT mixins first.
2. **VLT Slots (`src/config/slots.ts`):** Inject, replace, or disable (`NullComponent = () => null` or `unRegisterSlotComponent`) in `aboveHeader`, `belowHeader`, `headerTools`, `preFooter`, `postFooter`, `footer`, `followUs`, `footerLinks`.
3. **Registry (`src/config/{components,views,blocks}.ts`):** Swap components via `config.registerComponent`, add views, or register blocks/listing variations.
4. **Shadowing (`src/customizations/`):** Last resort only. Document why rungs 1–3 cannot solve it before shadowing.

## 3. Canonical Registry & Block Patterns

```ts
// src/config/slots.ts
config.registerSlotComponent({ slot: 'headerTools', name: 'Anontools', component: Anontools });

// src/config/blocks.ts
installCustomBlock(config); // exported from src/components/Blocks/CustomBlock/
createThemeDefinition('brand', 'Brand'); // maps 14 --theme-* vars to --block-theme-brand-*
```

- Keep `applyConfig(config: ConfigType)` in `src/index.ts` thin; delegate to `install{Settings,Blocks,Components,Slots,Views}`.
- Guard listing variation additions for idempotency and compose with upstream `listing.schemaEnhancer` instead of replacing it.
- Verify active blocks against `config.blocks.blocksConfig` or Storybook (`pnpm storybook`).

## 4. SCSS, Mixins & Figma Handoff

- Strip `position: absolute`, fixed `px` sizes, and `top`/`left` from Figma Inspect CSS; rebuild with Flexbox/Grid, `rem`, and `clamp()`.
- Read semantic tokens only (`--theme-*`, `--primary-color`), never base tokens (`--gray-80`, raw hex).
- Reuse VLT, `sc-volto-light-theme`, and addon mixins (`src/theme/mixins/_index.scss`) before writing custom CSS. Read [mixins-and-tokens.md](references/mixins-and-tokens.md) for the full reference.

## 5. Verification

Run before finishing:

```bash
make check && make frontend-test
python3 scripts/check_vlt_conventions.py frontend/packages/<addon-name>/src
```

- Run `make backend-test` if `backend/` changed, and `npx react-doctor@latest --verbose --scope changed` for React changes.
- Never import `semantic-ui-react` or write `.ui.*` selectors.
