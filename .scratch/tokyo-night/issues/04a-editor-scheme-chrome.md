# Editor scheme chrome (`<colors>`)

Status: ready-for-agent

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

- [ ] All applicable keys emitted per variant from the palette.
- [ ] Values stripped of leading `#` in XML, as IntelliJ expects.
- [ ] `mise run check` green.
