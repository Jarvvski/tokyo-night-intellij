"""Editor chrome mapping: Zed UI key -> editor scheme ``<colors>`` key.

Interface (fixed by the generator-core ticket): ``SCHEME_COLOR_MAP`` maps a Zed
source key, or a tuple of candidate keys, to one IntelliJ ``<colors>`` option
name. The generator resolves the first non-null candidate against the normalized
palette and writes it with the leading ``#`` stripped (IntelliJ expects bare
hex). Keep the table declarative; no side effects or I/O.

TODO(editor-chrome): caret row, selection (active/inactive), line numbers,
indent guides, gutter, added/modified/deleted line markers, console outputs.
"""

from __future__ import annotations

# Zed source key(s) -> IntelliJ <colors> option name.
SCHEME_COLOR_MAP: dict[object, str] = {
    "editor.active_line.background": "CARET_ROW_COLOR",
    "editor.line_number": "LINE_NUMBERS_COLOR",
    ("terminal.background", "terminal.ansi.background"): "CONSOLE_BACKGROUND_KEY",
    "editor.document_highlight.read_background": "SELECTION_BACKGROUND",
}
