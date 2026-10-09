# Mapping modules

Status: resolved

## Background

Five declarative mapping modules exist as stubs under `tools/mappings/`. Each maps
one subsystem's Zed keys to IntelliJ keys. They are independent files once their
interfaces (dict shapes) are fixed by ticket 02.

## Scope

Populate each module as a declarative table:

- `ui_map.py` - Zed UI key(s) -> palette name -> IntelliJ `ui.*` target(s).
- `syntax_map.py` - Zed syntax key -> IntelliJ attribute ids (per language),
  gated on ticket 01 for JS/TS + Kotlin.
- `scheme_colors.py` - Zed UI key -> editor scheme `<colors>` key.
- `diff_vcs_map.py` - Zed VCS keys -> FILESTATUS_* / DIFF_* keys.
- `ansi_map.py` - Zed ansi slot -> classic AND block-terminal key pair.

## Constraints

- Never invent an IntelliJ attribute id; fall back to a platform DEFAULT when a
  role cannot be confidently enumerated.
- Keep tables declarative; no side effects or I/O in mapping modules.

## Acceptance criteria

- [x] Each module exports the table documented in its docstring.
- [x] Generator consumes them with no inline key literals left behind.
- [x] Every mapped IntelliJ key is validated against shipped theme metadata where
      applicable (UI); unresolved keys dropped or corrected before shipping.
- [x] `mise run check` green.

## Comments

Module ownership was read one-to-one against the PRD/plan: `ui_map.py` is this
ticket (plan Phase 3 UI chrome has no dedicated ticket), while
`scheme_colors.py` / `syntax_map.py` / `diff_vcs_map.py` / `ansi_map.py` belong to
04a / 04b / 04c / 04d respectively, consistent with ticket 02's deferral of the
diff-triple and ANSI-default table shapes "to their owning tickets". This ticket
therefore populates `ui_map.py` and leaves the other four modules exporting their
documented (still-stub) tables for their owners.

Interface correction: `resolve_ui` iterated `UI_MAP.values()` unpacking a
`(ref, targets)` pair, while the module docstring defines `UI_MAP` as
`palette-name/literal -> target(s)`. The table was empty so the mismatch never
ran; the generator now iterates `.items()` to match the documented contract.

What landed:

- `SEMANTIC_PALETTE` (27 names) and `PALETTE_FALLBACKS` (20 chained fallbacks,
  all pointing to earlier entries) covering surfaces, text, borders, interactive
  states, editor chrome and severities. Values are driven per variant from the
  pinned palette (Moon/Light/Storm diverge as upstream).
- `UI_MAP` (27 palette refs + one literal) emitting 69 targeted `ui.*` overrides:
  MainWindow/ToolWindow bodies, tool-window header and chrome bars, popups,
  editor tabs, search match, borders/focus, foregrounds, hover/selection states
  and severity colors. Islands recipe honoured: `StatusBar.borderColor`,
  `ToolWindow.Stripe.borderColor`, `MainToolbar.borderColor` are the literal
  transparent `#00000000`, and `Island.borderColor` tracks the tool-window body.
- Validation: every one of the 69 targets was checked against the shipped
  `IntelliJPlatform.themeMetadata.json` + `JDK.themeMetadata.json` at tag
  `idea/263.6259.32` (the pinned build line). All 69 resolve; none were dropped.
  The check was a throwaway script - mapping modules stay declarative/I/O-free.
- Accepted approximation: targeted overrides only. List/Tree/Table *backgrounds*
  are left to Islands defaults pending deliberate visual review (ADR-0003), as is
  a future wildcard pass; this ticket maps their foregrounds and state colors.

Generated output: only the four `.theme.json` files changed (`.xml` unchanged -
scheme colors are 04a's scope). User-visible, so `gradle.properties` bumped to
0.2.0 with a dated CHANGELOG entry.

Gate: `uv run tools/generate.py && uv run tools/generate.py --check &&
mise run check` all green (`BUILD SUCCESSFUL`, drift check "8 files").
