"""UI metric overrides merged into ``theme.json`` ``ui``.

Unlike ``ui_map.UI_MAP`` (colour keys), these are component-scoped numeric values
written as nested groups under ``ui`` - the shape the built-in themes use (see
``darcula.theme.json`` ``ui.Tree.rowHeight`` / ``rowHeight.compact`` and
``ui.ToolWindow.Header.height.compact``). Those metric keys are not enumerated by
``IntelliJPlatform.themeMetadata.json``, so they are justified by built-in-theme
precedent rather than that metadata.

Interface (declarative, no side effects or I/O):

* ``UI_METRICS`` - component group -> {metric key -> value}, merged into the
  ``ui`` block last so it never clashes with a colour key.
"""

from __future__ import annotations

UI_METRICS: dict[str, dict[str, object]] = {
    # Compact mode shrinks tree rows to ~22px; raise the project/structure trees
    # to a Zed-like rhythm without changing any other compact spacing.
    "Tree": {"rowHeight.compact": 30},
}
