"""UI mapping: Zed UI key(s) -> palette name -> IntelliJ ``ui.*`` target(s).

Filled in by the UI-mapping ticket. Keep this table declarative; the generator
resolves each target against the semantic palette and validates emitted keys
against the shipped theme metadata before shipping.

TODO(ui-mapping): populate per-subsystem tables (window, tabs, toolbars, popups,
status bar, notifications, VCS) and the Islands override recipe.
"""

from __future__ import annotations

# (zed_key | tuple[zed_key, ...]) -> (palette_name, tuple[intellij_ui_key, ...])
UI_MAP: dict[object, tuple[str, tuple[str, ...]]] = {}
