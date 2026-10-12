"""Remap the parent Islands semantic palette names onto our palette.

The parent ``Islands Dark``/``Islands Light`` themes resolve their surfaces
through a named palette (``main-window-bg``, ``tool-window-bg``, ``popup-bg``,
``dialog-bg``, ...). Redefining those names in our theme's ``colors`` makes every
parent ``ui`` key that references them follow our colours automatically - so we
do not have to override each surface key individually (stripes, toolbars, menus,
dialogs).

Interface (declarative, no side effects or I/O):

* ``SEMANTIC_PALETTE_REMAP`` - Islands semantic colour name -> our palette name.
"""

from __future__ import annotations

SEMANTIC_PALETTE_REMAP: dict[str, str] = {
    # Window / tool-window / editor surfaces -> base background.
    "main-window-bg": "bgBase",
    "main-window-bg-alt": "bgBase",
    "tool-window-bg": "bgBase",
    "tool-window-bg-alt": "bgBase",
    "editor-bg": "bgBase",
    "editor-bg-inline": "bgBase",
    # Dialogs / settings.
    "dialog-bg": "bgBase",
    "dialog-bg-inline": "bgBase",
    # Popups / menus / tooltips float above the base.
    "popup-bg": "bgElevated",
    "popup-bg-inline": "bgElevated",
    # Flatten Islands' layered greys too: level 0 is our base surface, levels 1
    # and 2 are the elevated tone used by menus/popups/floating bars.
    "layer-0-bg": "bgBase",
    "layer-0-bg-inline": "bgBase",
    "layer-1-bg": "bgElevated",
    "layer-1-bg-inline": "bgElevated",
    "layer-2-bg": "bgElevated",
    "layer-2-bg-inline": "bgElevated",
}
