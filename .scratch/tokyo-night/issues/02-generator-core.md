# Generator core

Status: ready-for-agent

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
