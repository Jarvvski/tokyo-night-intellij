# Editor scheme chrome (`<colors>`)

Status: resolved

Blocked by: 02, 03

## Background

The editor scheme XML `<colors>` block themes editor chrome (not syntax). Today
the generator emits four keys; this ticket completes the mapping.

## Scope

Map Zed sources to `.xml <colors>` keys:

| Zed source | IntelliJ `<colors>` key |
| --- | --- |
| editor.active_line.background | CARET_ROW_COLOR |
| editor.document_highlight.read_background | SELECTION_BACKGROUND (+ _INACTIVE) |
| editor.line_number | LINE_NUMBERS_COLOR |
| editor.active_line_number | LINE_NUMBER_ON_CARET_ROW_COLOR |
| editor.indent_guide(_active) | INDENT_GUIDE / SELECTED_INDENT_GUIDE |
| editor.gutter.background | GUTTER_BACKGROUND / EDITOR_GUTTER_BACKGROUND |
| created/modified/deleted blends | ADDED/MODIFIED/DELETED_LINES_COLOR |
| terminal.background / panel bg | CONSOLE_BACKGROUND_KEY |
| editor.fg / error / muted | CONSOLE_NORMAL/ERROR/SYSTEM_OUTPUT |

## Acceptance criteria

- [x] All applicable keys emitted per variant from the palette.
- [x] Values stripped of leading `#` in XML, as IntelliJ expects.
- [x] `mise run check` green.

## Comments

Implemented the editor scheme chrome mapping; only the four `.xml` files changed
(the `.theme.json` files are byte-identical - UI chrome is 03's surface).

What landed:

- `scheme_colors.SCHEME_COLOR_MAP` widened to `str | tuple[str, ...]` so one
  source can drive several keys, then populated: CARET_ROW_COLOR, selection
  active/inactive, LINE_NUMBERS_COLOR, LINE_NUMBER_ON_CARET_ROW_COLOR,
  INDENT_GUIDE / SELECTED_INDENT_GUIDE, GUTTER_BACKGROUND /
  EDITOR_GUTTER_BACKGROUND, ADDED/MODIFIED/DELETED_LINES_COLOR and
  CONSOLE_BACKGROUND_KEY. Non-Night indent guides resolve through the ticket 02
  derivation (Night defines them upstream).
- New declarative `scheme_colors.SCHEME_ATTRIBUTE_MAP` for the console output
  family; `generate.py` consumes it in `_attribute_options`.

Decision (owner-approved): `CONSOLE_NORMAL_OUTPUT` / `CONSOLE_ERROR_OUTPUT` /
`CONSOLE_SYSTEM_OUTPUT` are `TextAttributesKey`s (`ConsoleViewContentType`), not
`ColorKey`s, so they are emitted in the `<attributes>` block FOREGROUND-only -
correcting the ticket/plan table's grouping under `<colors>`. Emitting them as
colors would be unrecognized and would trip ticket 06's unresolved-key check.
Verified against `EditorColors.java` and real `.icls` exports.

Also corrected: the inactive-selection key is the real
`SELECTION_BACKGROUND_INACTIVE` (ticket's "+ _INACTIVE"), not `SELECTION_INACTIVE`.

Accepted approximation (owner-approved): ADDED/MODIFIED/DELETED_LINES_COLOR take
the created/modified/deleted palette values directly rather than a computed blend
(no distinct upstream blend source); visual tuning deferred to ticket 06.

Gate: `uv run tools/generate.py && uv run tools/generate.py --check &&
mise run check` all green (`BUILD SUCCESSFUL`, drift check "8 files").
User-visible, so `gradle.properties` bumped to 0.3.0 with a dated CHANGELOG entry.
