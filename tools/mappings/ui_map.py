"""UI mapping: Zed UI key(s) -> palette name -> IntelliJ ``ui.*`` target(s).

Interfaces (fixed by the generator-core ticket; keep them declarative with no
side effects or I/O):

* ``SEMANTIC_PALETTE`` - the named palette written to ``theme.json`` ``colors``.
  Maps palette name -> ordered tuple of Zed source keys; the first non-null
  source wins.
* ``PALETTE_FALLBACKS`` - palette name -> earlier palette name used when every
  source in ``SEMANTIC_PALETTE`` is null, so the palette stays self-consistent.
* ``UI_MAP`` - component overrides written to ``theme.json`` ``ui``. Maps a
  palette name (or a literal ``#rrggbb[aa]`` color, used for Islands
  alpha-transparent borders) to a tuple of IntelliJ ``ui.*`` target keys; an
  empty map inherits everything from the parent Islands theme.

Populated by the mapping-modules ticket from ``plan.md`` Phase 3 and the Islands
recipe. Every target key was validated against the shipped
``IntelliJPlatform.themeMetadata.json`` / ``JDK.themeMetadata.json`` at tag
``idea/263.6259.32``; unresolved keys are not emitted. Overrides stay targeted -
broad wildcards are deferred until deliberate visual review.
"""

from __future__ import annotations

# Palette name -> ordered Zed source keys (first non-null wins).
SEMANTIC_PALETTE: dict[str, tuple[str, ...]] = {
    # Surfaces.
    "bgBase": ("background",),
    "bgSurface": ("surface.background", "panel.background"),
    "bgElevated": ("elevated_surface.background", "panel.overlay_background"),
    # Text.
    "fg": ("text", "editor.foreground"),
    "fgMuted": ("text.muted", "icon.muted", "hidden"),
    "fgDisabled": ("text.disabled", "element.disabled", "icon.disabled"),
    "accent": ("text.accent", "icon.accent"),
    # Borders.
    "border": ("border",),
    "borderVariant": ("border.variant",),
    "borderFocus": ("border.focused",),
    # Interactive states (element and ghost families mirror each other).
    "hover": ("element.hover", "ghost_element.hover"),
    "selection": ("element.selected", "ghost_element.selected"),
    # Editor chrome.
    "activeTab": ("tab.active_background",),
    "tabBar": ("tab_bar.background",),
    "searchMatch": ("search.match_background",),
    # Severities (base color, background and border).
    "error": ("error",),
    "errorBackground": ("error.background",),
    "errorBorder": ("error.border",),
    "warning": ("warning",),
    "warningBackground": ("warning.background",),
    "warningBorder": ("warning.border",),
    "success": ("success",),
    "successBackground": ("success.background",),
    "successBorder": ("success.border",),
    "info": ("info",),
    "infoBackground": ("info.background",),
    "infoBorder": ("info.border",),
}

# Palette name -> earlier palette name to inherit when all sources are null.
PALETTE_FALLBACKS: dict[str, str] = {
    "bgSurface": "bgBase",
    "bgElevated": "bgSurface",
    "activeTab": "bgSurface",
    "tabBar": "bgSurface",
    "searchMatch": "activeTab",
    "borderVariant": "border",
    "borderFocus": "borderVariant",
    "fgMuted": "fg",
    "fgDisabled": "fgMuted",
    "accent": "fg",
    "hover": "bgSurface",
    "selection": "hover",
    "errorBackground": "bgBase",
    "errorBorder": "borderVariant",
    "warningBackground": "bgBase",
    "warningBorder": "borderVariant",
    "successBackground": "bgBase",
    "successBorder": "borderVariant",
    "infoBackground": "bgBase",
    "infoBorder": "borderVariant",
}

# Palette name (or literal #rrggbb[aa]) -> IntelliJ ui.* target key(s).
UI_MAP: dict[str, tuple[str, ...]] = {
    # Main window and tool-window bodies; Island border tracks the body color.
    "bgBase": (
        "MainWindow.background",
        "ToolWindow.background",
        "Island.borderColor",
    ),
    # Tool-window headers and chrome bars (Zed surface family).
    "bgSurface": (
        "ToolWindow.Header.background",
        "ToolWindow.Header.inactiveBackground",
        "SidePanel.background",
        "StatusBar.background",
        "MainToolbar.background",
    ),
    # Popups and tooltips float above the surface.
    "bgElevated": (
        "Popup.background",
        "PopupMenu.background",
        "ToolTip.background",
        "Editor.ToolTip.background",
    ),
    # Editor tab strip background vs the selected tab.
    "tabBar": ("EditorTabs.background",),
    "activeTab": ("EditorTabs.selectedBackground",),
    # Search result highlighting.
    "searchMatch": (
        "SearchMatch.startBackground",
        "SearchMatch.endBackground",
    ),
    # Islands recipe: transparent sidebar/toolbar borders (Phase 3).
    "#00000000": (
        "StatusBar.borderColor",
        "ToolWindow.Stripe.borderColor",
        "MainToolbar.borderColor",
    ),
    # Borders.
    "border": (
        "Borders.color",
        "Window.border",
        "EditorTabs.borderColor",
        "ToolWindow.borderColor",
    ),
    "borderVariant": ("Borders.ContrastBorderColor",),
    "borderFocus": ("Component.focusedBorderColor",),
    # Foregrounds.
    "fg": (
        "Label.foreground",
        "Tree.foreground",
        "List.foreground",
        "Table.foreground",
    ),
    "fgMuted": ("Link.secondaryForeground",),
    "fgDisabled": ("Label.disabledForeground",),
    # Accent (focus rings / active links).
    "accent": (
        "Component.focusColor",
        "Link.activeForeground",
    ),
    # Hover and selection states.
    "hover": (
        "List.hoverBackground",
        "Tree.hoverBackground",
        "Table.hoverBackground",
    ),
    "selection": (
        "List.selectionBackground",
        "Tree.selectionBackground",
        "Table.selectionBackground",
        "List.selectionInactiveBackground",
        "Tree.selectionInactiveBackground",
        "Table.selectionInactiveBackground",
    ),
    # Severities.
    "error": (
        "Label.errorForeground",
        "ValidationTooltip.errorForeground",
        "Notification.errorForeground",
    ),
    "errorBackground": (
        "Banner.errorBackground",
        "ValidationTooltip.errorBackground",
        "Notification.errorBackground",
    ),
    "errorBorder": (
        "Banner.errorBorderColor",
        "ValidationTooltip.errorBorderColor",
        "Notification.errorBorderColor",
    ),
    "warning": (
        "Label.warningForeground",
        "ValidationTooltip.warningForeground",
        "Notification.ToolWindow.warningForeground",
    ),
    "warningBackground": (
        "Banner.warningBackground",
        "ValidationTooltip.warningBackground",
        "Notification.ToolWindow.warningBackground",
    ),
    "warningBorder": (
        "Banner.warningBorderColor",
        "ValidationTooltip.warningBorderColor",
        "Notification.ToolWindow.warningBorderColor",
    ),
    "success": ("Label.successForeground",),
    "successBackground": ("Banner.successBackground",),
    "successBorder": ("Banner.successBorderColor",),
    "info": (
        "Label.infoForeground",
        "Notification.ToolWindow.informativeForeground",
    ),
    "infoBackground": (
        "Banner.infoBackground",
        "Notification.ToolWindow.informativeBackground",
    ),
    "infoBorder": (
        "Banner.infoBorderColor",
        "Notification.ToolWindow.informativeBorderColor",
    ),
}
