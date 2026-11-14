---
name: accessible-component-review
description: >
  Reviews an interactive UI component's native semantics, keyboard behavior,
  focus management, contrast, motion, and ARIA announcements across all states.
  Use when building or auditing design-system widgets and reusable controls.
license: MIT
metadata:
  version: "1.0"
---

# Accessible component review

Review every supported state and input path of one reusable component.

## Workflow

1. Inventory states, variants, input methods, content slots, and expected
   semantics.
2. Select the native element that already provides the behavior. Use ARIA
   patterns only when native HTML cannot provide the required interaction.
3. Apply [references/component-checklist.md](references/component-checklist.md)
   to each state.
4. Run deterministic rules, keyboard behavior, forced-colors, reduced-motion,
   zoom/reflow, and pointer target checks. Record manual judgment separately.
5. Trace failures to the component source and repair the smallest shared layer
   that owns the defect.
6. Add tests for user-visible behavior and verify consuming examples do not
   regress.

## Boundaries

Do not add ARIA that duplicates or conflicts with native semantics. Do not treat
a single Storybook example as coverage of every consumer. Do not assert that an
accessible name is meaningful without content context.
