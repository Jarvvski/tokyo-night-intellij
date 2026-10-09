# Generator core

Status: resolved

## Background

`tools/generate.py` is currently a bootstrap skeleton: it derives a small subset
directly and emits valid stub themes. This ticket turns it into the real core:
read the pinned palette, normalize it, and drive all emitted values from it.

## Scope

- Load `tools/vendor/tokyo-night.json`; iterate variants in canonical order.
- Normalize quirks:
  1. hex missing a leading `#` (Light `text.accent`);
  2. keys absent in Light/Storm/Moon filled from fallbacks (version_control.*,
     panel.indent_guide*, editor.indent_guide*, document_highlight bracket bg,
     panel.overlay_background / elevated fallbacks, pane_group.border,
     terminal.ansi.background);
  3. terminal derivation: `foreground := editor.fg`,
     `bright_foreground := base-text`, `dim_foreground := text.muted`
     (flag as heuristics).
- Refactor output generation to consume the mapping modules (`tools/mappings/*`)
  rather than inline literals.
- Keep deterministic output and the `--check` mode working.

## Critical rule

Do **not** assume the dark variants share values - Moon diverges from Night/Storm
in several roles while sharing others. Every value must come from the dump.

## Acceptance criteria

- [ ] All emitted values trace to the palette dump or an explicit fallback rule.
- [ ] Quirk fixes are explicit and commented as deviations from raw upstream.
- [ ] `uv run tools/generate.py --check` passes after regenerating.
- [ ] `mise run check` green.

## Comments

Engine-only boundary (confirmed with the owner): the generator core is now real;
full mapping coverage stays with tickets 03/04a-d.

- `tools/generate.py` loads the pinned palette in canonical order, normalizes
  every variant into a complete model (`normalize_variant`), and emits through
  the mapping tables. Quirk fixes 1, 2a-2g and 3 are implemented and labelled;
  `REQUIRED_NORMALIZED_COLORS` asserts every fallback/derivation is present and
  valid hex for all four variants on every run, so the fixes are exercised even
  before later tickets emit those keys.
- Interfaces fixed: `ui_map.SEMANTIC_PALETTE` / `PALETTE_FALLBACKS` / `UI_MAP`,
  `scheme_colors.SCHEME_COLOR_MAP`, `diff_vcs_map.VCS_COLOR_MAP` /
  `DIFF_ATTRIBUTE_MAP`, `ansi_map.ANSI_MAP`; all consumed generically by the
  engine. Today's inline literals moved into `ui_map`/`scheme_colors`, so no
  IntelliJ target key literal remains in the generator.
- Accepted approximations: version-control fallback uses the generic top-level
  family (Night keeps its own vc values); indent-guide fallbacks are a documented
  line-number/border blend subject to visual tuning; richer diff-triple and
  ANSI-default table shapes are deferred to their owning tickets while their
  placeholder constants stay inert.
- Generated output: theme JSON byte-identical; each XML changes only in the
  `<attributes>` block form (`<attributes/>` -> empty open/close pair) so later
  tickets append attributes without churn.
- Gate: `uv run tools/generate.py && uv run tools/generate.py --check &&
  mise run check` all green (`BUILD SUCCESSFUL`, drift check "8 files"). No
  version bump or CHANGELOG entry: internal refactor, not user-visible.
