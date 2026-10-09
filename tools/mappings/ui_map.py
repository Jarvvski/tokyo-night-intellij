"""UI mapping: Zed UI key(s) -> palette name -> IntelliJ ``ui.*`` target(s).

Interfaces (fixed by the generator-core ticket; keep them declarative with no
side effects or I/O):

* ``SEMANTIC_PALETTE`` - the named palette written to ``theme.json`` ``colors``.
  Maps palette name -> ordered tuple of Zed source keys; the first non-null
  source wins.
* ``PALETTE_FALLBACKS`` - palette name -> earlier palette name used when every
  source in ``SEMANTIC_PALETTE`` is null, so the palette stays self-consistent.
* ``UI_MAP`` - component overrides. Maps a palette name (or a literal
  ``#rrggbb[aa]`` color, used for Islands alpha-transparent borders) to a tuple
  of IntelliJ ``ui.*`` target keys. Empty until the UI-mapping ticket populates
  it; an empty map inherits everything from the parent Islands theme.

TODO(ui-mapping): populate per-subsystem tables (window, tabs, toolbars, popups,
status bar, notifications, VCS) and the Islands override recipe.
"""

from __future__ import annotations

# Palette name -> ordered Zed source keys (first non-null wins).
SEMANTIC_PALETTE: dict[str, tuple[str, ...]] = {
    "bgBase": ("background", "editor.background"),
    "bgSurface": ("panel.background", "surface.background"),
    "bgElevated": ("elevated_surface.background", "panel.overlay_background"),
    "border": ("border",),
    "fg": ("text",),
    "fgMuted": ("text.muted", "icon.muted"),
    "accent": ("text.accent", "icon.accent"),
}

# Palette name -> earlier palette name to inherit when all sources are null.
PALETTE_FALLBACKS: dict[str, str] = {
    "bgSurface": "bgBase",
    "bgElevated": "bgSurface",
    "border": "bgSurface",
}

# Palette name (or literal #rrggbb[aa]) -> IntelliJ ui.* target key(s).
UI_MAP: dict[object, tuple[object, tuple[str, ...]]] = {}
