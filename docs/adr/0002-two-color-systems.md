# IntelliJ's two color systems map to two generated artifacts per variant

IntelliJ splits theming across two unrelated systems:

- **UI chrome** lives in a `*.theme.json`, whose `colors`/`ui` keys theme
  windows, toolbars, tabs, popups, and so on.
- **Syntax, terminal ANSI, and diff/VCS** live in a separate editor color scheme
  XML (`*.icls`, shipped renamed to `*.xml`), consisting of a `<colors>` block
  and an `<attributes>` block.

A theme only applies its editor scheme if the UI theme points at it via a
top-level `editorScheme` key. We therefore emit **two files per variant**:
`<Variant>.theme.json` (with `"editorScheme": "/themes/<Variant>.xml"`) and
`<Variant>.xml`.

This split is why the generator has distinct mapping modules for UI versus scheme
colors versus syntax attributes - they target different files with different key
grammars.

## Consequences

- Every variant produces exactly one `.theme.json` + one `.xml`.
- The `.xml` root uses `parent_scheme="Darcula"` so unspecified attributes
  inherit sensible defaults.
- Terminal ANSI must be written to both the classic console keys and the new
  block-terminal keys; see ADR-0004.

Status: accepted
