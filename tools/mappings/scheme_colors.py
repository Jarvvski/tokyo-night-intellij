"""Editor chrome mapping: Zed UI key -> editor scheme ``<colors>`` key.

Interfaces (fixed by the generator-core ticket; extended by the editor-chrome
ticket; keep them declarative with no side effects or I/O):

* ``SCHEME_COLOR_MAP`` - maps a Zed source key, or a tuple of candidate keys,
  to one IntelliJ ``<colors>`` option name, or a tuple of option names when one
  source drives several keys (for example active/inactive selection). The
  generator resolves the first non-null candidate against the normalized palette
  and writes each option with the leading ``#`` stripped (IntelliJ expects bare
  hex).
* ``SCHEME_ATTRIBUTE_MAP`` - maps a Zed source key, or a tuple of candidate keys,
  to an IntelliJ ``<attributes>`` id for editor-chrome text attributes that are
  not syntax roles (the console output family). These are emitted
  FOREGROUND-only; their background is ``CONSOLE_BACKGROUND_KEY``.
"""

from __future__ import annotations

# Zed source key(s) -> IntelliJ <colors> option name(s).
SCHEME_COLOR_MAP: dict[object, str | tuple[str, ...]] = {
    # Editor chrome.
    "editor.active_line.background": "CARET_ROW_COLOR",
    ("editor.document_highlight.read_background",): (
        "SELECTION_BACKGROUND",
        "SELECTION_BACKGROUND_INACTIVE",
    ),
    "editor.line_number": "LINE_NUMBERS_COLOR",
    "editor.active_line_number": "LINE_NUMBER_ON_CARET_ROW_COLOR",
    # Indent guides (Night defines them; other variants are derived in the
    # generator's quirk fixes).
    "editor.indent_guide": "INDENT_GUIDE",
    "editor.indent_guide_active": "SELECTED_INDENT_GUIDE",
    # Gutter background: classic key plus the New UI variant.
    "editor.gutter.background": (
        "GUTTER_BACKGROUND",
        "EDITOR_GUTTER_BACKGROUND",
    ),
    # Changed-line gutter markers.
    "created": "ADDED_LINES_COLOR",
    "modified": "MODIFIED_LINES_COLOR",
    "deleted": "DELETED_LINES_COLOR",
    # Console background (terminal surface).
    ("terminal.background", "terminal.ansi.background"): "CONSOLE_BACKGROUND_KEY",
}

# Zed source key(s) -> IntelliJ <attributes> id (console output family).
SCHEME_ATTRIBUTE_MAP: dict[object, str | tuple[str, ...]] = {
    ("editor.foreground",): "CONSOLE_NORMAL_OUTPUT",
    ("error",): "CONSOLE_ERROR_OUTPUT",
    ("text.muted",): "CONSOLE_SYSTEM_OUTPUT",
}
