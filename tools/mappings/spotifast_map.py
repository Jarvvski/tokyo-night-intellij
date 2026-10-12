"""Spotifast mapping: normalized Zed model -> Spotifast custom-palette slots.

Spotifast (https://spotifast.rocks/settings-and-files/#custom-themes) reads plain
JSON palette files from its ``themes`` folder. Each file is a ``base`` plus up to
sixteen named colours; omitted colours inherit Spotifast's own defaults, so we
emit only the slots we derive.

Interface (declarative, no I/O):

* ``SLOTS`` - emission order of the Spotifast colour names.
* ``resolve_palette(style, blend)`` - build the slot -> ``#rrggbb`` map from one
  normalized variant. ``blend`` is the generator's linear-blend helper, passed
  in so this module owns no colour maths (the generator owns it).

Design notes:

* Surfaces follow Zed. ``panel``/``surface`` sit *darker* than ``window`` in dark
  mode, exactly as Zed renders its own panels against the editor background,
  rather than the ascending ramp Spotifast's hand-tuned built-in uses.
* ``surface_hover``/``surface_active``/``outline`` step along the surface ramp
  toward ``text``, which lightens them in dark mode and darkens them in light
  mode, so a single rule serves both appearances.
* The accent is the classic Tokyo Night blue (``terminal.ansi.blue``), matching
  the palette Spotifast ships, not Zed's ``text.accent`` cyan.
* ``overlay``/``shadow`` are omitted so Spotifast inherits its defaults, as its
  own built-in palettes do.
"""

from __future__ import annotations

# Emission order of the Spotifast colour names we derive.
SLOTS: tuple[str, ...] = (
    "window",
    "panel",
    "surface",
    "surface_hover",
    "surface_active",
    "outline",
    "text",
    "secondary",
    "dim",
    "accent",
    "accent_hover",
    "on_accent",
    "danger",
    "warning",
)

# Blend factors along the surface ramp. ``text`` is the contrast direction, so
# these lighten dark surfaces and darken light ones.
SURFACE_FALLBACK_STEP = 0.06  # panel -> surface when Zed gives no elevated tone
HOVER_STEP = 0.06
ACTIVE_STEP = 0.11
OUTLINE_STEP = 0.17
DIM_TO_BG = 0.35  # keep ``dim`` closer to the background than ``secondary``
ACCENT_HOVER_STEP = 0.12


def _first(style: dict, *keys: str) -> str | None:
    """First non-empty colour among ``keys`` in the normalized style."""
    for key in keys:
        value = style.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def resolve_palette(style: dict, blend) -> dict[str, str]:
    """Return the Spotifast slot -> colour map for a normalized variant.

    ``style`` is a normalized variant model (see ``generate.normalize_variant``);
    ``blend`` is ``generate.blend``. Slots whose source is absent are omitted so
    Spotifast inherits its default for them.
    """
    background = _first(style, "background")
    foreground = _first(style, "text", "editor.foreground")
    panel = _first(style, "surface.background", "panel.background") or background
    elevated = _first(style, "elevated_surface.background", "panel.overlay_background")
    muted = _first(style, "text.muted", "icon.muted")
    accent = _first(style, "terminal.ansi.blue", "text.accent")

    # Light's elevated surface equals its background, so fall back to a step off
    # the panel to keep ``surface`` distinct from ``window``.
    if elevated and elevated != background:
        surface = elevated
    else:
        surface = blend(panel, foreground, SURFACE_FALLBACK_STEP)

    palette: dict[str, str] = {
        "window": background,
        "panel": panel,
        "surface": surface,
        "surface_hover": blend(surface, foreground, HOVER_STEP),
        "surface_active": blend(surface, foreground, ACTIVE_STEP),
        "outline": blend(surface, foreground, OUTLINE_STEP),
        "text": foreground,
        "secondary": muted,
        "dim": blend(muted, background, DIM_TO_BG),
        "accent": accent,
        "accent_hover": blend(accent, foreground, ACCENT_HOVER_STEP),
        "on_accent": background,
        "danger": _first(style, "error"),
        "warning": _first(style, "warning"),
    }
    return {name: palette[name] for name in SLOTS if palette.get(name)}
