# volto-light-theme-skills

**Upgrade-safe AI agent skills for Plone 6, Volto, and Volto Light Theme.**

AI coding agents default to generic React patterns, inline hex colors, `semantic-ui-react` imports, and `src/customizations/` file shadowing—all of which break upgrades and violate `@kitconcept/volto-light-theme` and `sc-volto-light-theme` conventions. This repository encodes the exact customization ladder, token contracts, registry patterns, and static checks needed to ship clean Volto Light Theme addons on the first pass.

---

## Architecture

The suite pairs a core **Volto Light Theme** skill with specialized Plone, React, and accessibility skills. Every UI change is routed through the **Customization Ladder**—stopping at the lowest-cost, most upgrade-safe rung—before running deterministic verification.

```mermaid
flowchart TD
    Task["Feature / Fix / PR Review"] --> Core["volto-light-theme (Core Rules)"]

    Core --> Ladder{"Customization Ladder (Stop at Earliest Rung)"}
    Ladder -->|"1. Styling & Brand"| R1["Tokens & SCSS (src/theme/_root.scss)"]
    Ladder -->|"2. Layout Chrome"| R2["VLT Slots (src/config/slots.ts)"]
    Ladder -->|"3. Blocks / Views"| R3["Registry (blocks, views, components)"]
    Ladder -->|"4. Last Resort"| R4["Shadowing (src/customizations/)"]

    subgraph Stack["Companion Skills Loaded by Concern"]
        Plone["plone-expert-developer (Plone 6 / Dexterity / Volto)"]
        React["react-best-practices & composition-patterns"]
        A11y["accessibility-audit & accessible-component-review"]
        UX["web-design-guidelines"]
    end

    R1 & R2 & R3 & R4 --> Stack
    Stack --> Verify["Verification Gate"]

    Verify --> V1["check_vlt_conventions.py (No semantic-ui-react / .ui.*)"]
    Verify --> V2["npx react-doctor@latest (Lint, Bundle, A11y)"]
    Verify --> V3["make check && make frontend-test"]
```

---

## Install (Unified Command)

Install the core VLT + MIT-licensed skills from this repository together with the upstream Plone and Vercel companion skills globally across all detected agents (Claude Code, Antigravity, Codex, etc.):

```bash
npx skills add https://github.com/Rodriguesmath/volto-light-theme-skills -a '*' -g -s '*' -y \
  && npx skills add https://github.com/codesyntax/plone-expert-developer -a '*' -g -s '*' -y \
  && npx skills add https://github.com/vercel-labs/agent-skills -a '*' -g -s '*' -y
```

To target **Claude Code only**, replace `-a '*'` with `-a claude-code` (or run `install.sh` with `AGENT=claude-code`):

```bash
curl -fsSL https://raw.githubusercontent.com/Rodriguesmath/volto-light-theme-skills/main/install.sh | AGENT=claude-code bash
```

---

## Included Skills (MIT)

All skills bundled directly in `skills/` carry an explicit **MIT** license:

| Skill | Scope | Source / Maintainer |
| :--- | :--- | :--- |
| [`volto-light-theme`](skills/volto-light-theme/SKILL.md) | VLT customization ladder, `--theme-*` token contract, slots, block/listing registration, Figma-to-SCSS rules, and convention checker. | This repo (MIT) |
| [`react-best-practices`](skills/react-best-practices/SKILL.md) | 40+ React performance rules (bundle size, waterfalls, re-renders, SSR/hydration). | [Vercel Engineering](https://github.com/vercel-labs/agent-skills) (MIT) |
| [`composition-patterns`](skills/composition-patterns/SKILL.md) | Compound components, context interfaces, explicit variants over boolean prop proliferation. | [Vercel Engineering](https://github.com/vercel-labs/agent-skills) (MIT) |
| [`accessibility-audit`](skills/accessibility-audit/SKILL.md) | Deterministic WCAG / axe page and state audits with explicit manual-review boundaries. | MIT |
| [`accessible-component-review`](skills/accessible-component-review/SKILL.md) | Native semantics, keyboard interaction, focus management, contrast, and ARIA live regions. | MIT |

### Upstream Companion Skills (Installed via Unified Command)

- **`plone-expert-developer`** — [CodeSyntax](https://github.com/codesyntax/plone-expert-developer) (Plone 6 backend, Volto TypeScript, Classic UI, `6.docs.plone.org` retrieval protocol).
- **`web-design-guidelines`** — [Vercel Engineering](https://github.com/vercel-labs/agent-skills) (UI/UX compliance review).
- **`react-doctor`** — Invoked directly on demand via `npx react-doctor@latest --verbose --scope changed`.

---

## Convention Checker

`volto-light-theme` ships with a zero-dependency Python linter that catches `semantic-ui-react` imports and `.ui.*` Semantic UI CSS overrides across any Volto addon:

```bash
# Auto-discovers frontend/packages/*/src from a project root
python3 skills/volto-light-theme/scripts/check_vlt_conventions.py /path/to/plone-project

# Or target a specific addon directly
python3 skills/volto-light-theme/scripts/check_vlt_conventions.py frontend/packages/my-addon/src
```

Exit code is `0` when clean, `1` with `file:line` diagnostics on violations.

---

## Repository Layout

```text
volto-light-theme-skills/
├── LICENSE
├── README.md
├── install.sh
└── skills/
    ├── volto-light-theme/
    │   ├── SKILL.md
    │   ├── references/
    │   │   └── mixins-and-tokens.md
    │   └── scripts/
    │       └── check_vlt_conventions.py
    ├── react-best-practices/
    ├── composition-patterns/
    ├── accessibility-audit/
    └── accessible-component-review/
```

---

## Credits & Attribution

This repository builds on the work of the Plone, Volto, and React ecosystems:

- **Plone & Volto** — [Plone Foundation](https://plone.org/) and the [Volto](https://github.com/plone/volto) community.
- **Volto Light Theme** — [kitconcept GmbH](https://github.com/kitconcept/volto-light-theme) (`@kitconcept/volto-light-theme`).
- **PortalBrasil & `sc-volto-light-theme`** — [Simples Consultoria](https://github.com/simplesconsultoria) and [PortalBrasil](https://github.com/portalbrasil) (`@portalbrasil/intranet`, semantic token contracts, and SCSS mixin architecture).
- **Companion Skills** — [CodeSyntax](https://github.com/codesyntax/plone-expert-developer) (`plone-expert-developer`) and [Vercel Engineering](https://github.com/vercel-labs/agent-skills) (`react-best-practices`, `composition-patterns`, `web-design-guidelines`).
