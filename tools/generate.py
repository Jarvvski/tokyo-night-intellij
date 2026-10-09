#!/usr/bin/env python3
"""Generate IntelliJ theme resources from the pinned Zed palette.

Stdlib only. Reads ``tools/vendor/tokyo-night.json`` and emits, per variant:

    src/main/resources/themes/<Slug>.theme.json   (UI chrome)
    src/main/resources/themes/<Slug>.xml          (editor scheme)

Generated outputs are committed; never hand-edit them (see AGENTS.md).

The generator is the core: it loads the pinned palette, normalizes the upstream
quirks into a complete per-variant model, and drives every emitted value from
that model through the declarative tables in ``tools/mappings/*.py``. No Zed or
IntelliJ key literals live in this file.

Usage:
    uv run tools/generate.py           # write resources
    uv run tools/generate.py --check   # exit 1 if committed output would change
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT / "tools"
VENDOR = TOOLS_DIR / "vendor" / "tokyo-night.json"
THEMES_DIR = ROOT / "src" / "main" / "resources" / "themes"

AUTHOR = "Adam Jarvis"

# Canonical emission order: display name -> file slug.
SLUGS = {
    "Tokyo Night": "TokyoNight",
    "Tokyo Night Storm": "TokyoNightStorm",
    "Tokyo Night Moon": "TokyoNightMoon",
    "Tokyo Night Light": "TokyoNightLight",
}

# ``tools/`` is sys.path[0] when this file runs as a script, but insert it
# defensively so alternate invocation styles resolve ``mappings`` too.
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from mappings import ansi_map, diff_vcs_map, scheme_colors, syntax_map, ui_map  # noqa: E402

_HEX_RE = re.compile(r"^(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")

# Keys that upstream omits in some variants and that the quirk fixes below must
# leave present and well formed in every normalized variant. Asserting them keeps
# the fallback rules honest even before a later ticket emits them.
REQUIRED_NORMALIZED_COLORS: tuple[str, ...] = (
    "version_control.added",
    "version_control.added_background",
    "version_control.conflict",
    "version_control.conflict_background",
    "version_control.deleted",
    "version_control.deleted_background",
    "version_control.ignored",
    "version_control.modified",
    "version_control.modified_background",
    "version_control.renamed",
    "editor.indent_guide",
    "editor.indent_guide_active",
    "panel.indent_guide",
    "panel.indent_guide_active",
    "panel.indent_guide_hover",
    "editor.document_highlight.bracket_background",
    "panel.overlay_background",
    "pane_group.border",
    "terminal.ansi.background",
    "terminal.foreground",
    "terminal.bright_foreground",
    "terminal.dim_foreground",
    # Derived diff-line tints and VCS annotation slots (heuristics below).
    "diff.added_background",
    "diff.deleted_background",
    "diff.modified_background",
    "diff.conflict_background",
    "vcs.annotation_1",
    "vcs.annotation_2",
    "vcs.annotation_3",
    "vcs.annotation_4",
    "vcs.annotation_5",
)


# --------------------------------------------------------------------------- #
# Color helpers
# --------------------------------------------------------------------------- #


def normalize_hex(value: object) -> object:
    """Add a leading ``#`` to a bare hex color; leave other tokens untouched.

    Quirk fix 1: upstream Light ``text.accent`` is ``0f4b6e`` with no ``#``.
    Non-color strings (for example ``background.appearance = opaque``) pass
    through unchanged so they are never mistaken for a color.
    """
    if not isinstance(value, str):
        return value
    value = value.strip()
    if not value:
        return None
    if value.startswith("#"):
        return value
    if _HEX_RE.match(value):
        return f"#{value}"
    return value


def _rgb(color: str) -> tuple[int, int, int]:
    bare = color.lstrip("#")
    return (int(bare[0:2], 16), int(bare[2:4], 16), int(bare[4:6], 16))


def blend(a: str, b: str, t: float = 0.5) -> str:
    """Linear blend of two hex colors; ``t`` = 0 -> ``a``, ``t`` = 1 -> ``b``."""
    ra, rb = _rgb(a), _rgb(b)
    mixed = tuple(round(x + (y - x) * t) for x, y in zip(ra, rb))
    return "#" + "".join(f"{c:02x}" for c in mixed)


def _as_tuple(value: object) -> tuple:
    if isinstance(value, (list, tuple)):
        return tuple(value)
    return (value,)


def _first_color(style: dict, sources: object) -> str | None:
    """First non-null candidate among ``sources`` in the normalized style."""
    for source in _as_tuple(sources):
        color = style.get(source)
        if isinstance(color, str) and color:
            return color
    return None


def _fill(style: dict, key: str, *candidates: object) -> None:
    """Set ``key`` from the first non-null candidate if it is currently unset."""
    if style.get(key) is not None:
        return
    for candidate in candidates:
        if candidate is not None:
            style[key] = candidate
            return


def _font_type(role: dict) -> int:
    """Collapse Zed weight/style to the IntelliJ FONT_TYPE enum.

    0 plain, 1 bold, 2 italic, 3 bold+italic.
    """
    weight = role.get("font_weight")
    bold = isinstance(weight, int) and weight >= 700
    italic = role.get("font_style") == "italic"
    return (1 if bold else 0) | (2 if italic else 0)


# --------------------------------------------------------------------------- #
# Normalization (quirk fixes)
# --------------------------------------------------------------------------- #


def normalize_variant(theme: dict) -> dict:
    """Return a complete style model with every documented quirk fix applied.

    Deviations from raw upstream are marked ``Quirk fix`` and recorded here so
    the generated resources stay auditable against ADR-0001.
    """
    raw = theme["style"]

    style: dict[str, object] = {}
    for key, value in raw.items():
        style[key] = normalize_hex(value)

    syntax: dict[str, dict] = {}
    for role, role_value in raw.get("syntax", {}).items():
        entry = dict(role_value)
        entry["color"] = normalize_hex(role_value.get("color"))
        syntax[role] = entry
    style["syntax"] = syntax

    def get(key: str):
        return style.get(key)

    # Quirk fix 2a: the version_control.* family exists only in Tokyo Night
    # upstream. For every other variant fall back to the generic top-level
    # created/deleted/modified/conflict/renamed/ignored (+ _background) family.
    # Note upstream names the vc variant of ``created`` ``added``. Deliberate
    # deviation: Night keeps its own vc values (its renamed/ignored differ from
    # the generic family), so we only fill what is missing.
    vc_fallbacks = (
        ("added", "created"),
        ("deleted", "deleted"),
        ("modified", "modified"),
        ("conflict", "conflict"),
        ("renamed", "renamed"),
        ("ignored", "ignored"),
    )
    for vc_name, base in vc_fallbacks:
        _fill(style, f"version_control.{vc_name}", get(base))
        if base != "renamed":  # upstream defines no version_control.renamed_background
            _fill(style, f"version_control.{vc_name}_background", get(f"{base}.background"))

    # Quirk fix 2b: editor indent guides are defined only for Night; derive them
    # as a blend of line number + border (active pulled toward the more
    # contrasted line number). Heuristic - subject to visual tuning.
    line_number, border = get("editor.line_number"), get("border")
    if line_number and border:
        _fill(style, "editor.indent_guide", blend(line_number, border))
        _fill(style, "editor.indent_guide_active", blend(line_number, border, t=0.2))

    # Quirk fix 2c: panel indent guides derive from the editor guide / muted.
    _fill(style, "panel.indent_guide", get("editor.indent_guide"))
    _fill(
        style,
        "panel.indent_guide_active",
        get("text.muted") or get("editor.indent_guide_active"),
    )
    _fill(style, "panel.indent_guide_hover", get("panel.indent_guide_active"))

    # Quirk fix 2d: bracket-highlight background -> search match background.
    _fill(
        style,
        "editor.document_highlight.bracket_background",
        get("search.match_background"),
    )

    # Quirk fix 2e: overlay/elevated surface -> per-variant elevated/border.
    _fill(
        style,
        "panel.overlay_background",
        get("elevated_surface.background") or get("border.variant"),
    )

    # Quirk fix 2f: pane group border -> border variant.
    _fill(style, "pane_group.border", get("border.variant"))

    # Quirk fix 2g: terminal ANSI background -> variant panel background.
    _fill(
        style,
        "terminal.ansi.background",
        get("panel.background") or get("surface.background") or get("background"),
    )

    # Quirk fix 3: terminal derivation heuristics (Zed leaves these null).
    base_text = (
        syntax.get("label", {}).get("color")
        or syntax.get("variable", {}).get("color")
    )
    _fill(style, "terminal.foreground", get("editor.foreground") or get("text"))
    _fill(style, "terminal.bright_foreground", base_text)
    _fill(style, "terminal.dim_foreground", get("text.muted"))

    # Derivation (heuristic): diff-line tints. IntelliJ paints changed diff lines
    # with a BACKGROUND plus an ERROR_STRIPE_COLOR; Zed has no dedicated diff
    # background key, so blend the editor surface toward each status accent.
    # The blend factor is deliberately shallow to match the platform's subtle
    # line tints; subject to visual tuning.
    editor_bg = get("editor.background") or get("background")
    for name in ("added", "deleted", "modified", "conflict"):
        accent = get(f"version_control.{name}")
        if isinstance(editor_bg, str) and isinstance(accent, str):
            _fill(
                style,
                f"diff.{name}_background",
                blend(editor_bg, accent, t=0.15),
            )

    # Derivation (heuristic): VCS blame annotation author slots. Upstream
    # ``accents`` supplies a ramp of tinted hues; take the first five as opaque
    # RGB (the trailing alpha byte is dropped because scheme colour values are
    # RGB).
    accents = raw.get("accents") or []
    for index in range(5):
        value = accents[index] if index < len(accents) else None
        if isinstance(value, str):
            _fill(style, f"vcs.annotation_{index + 1}", normalize_hex(value[:7]))

    validate_normalized(theme["name"], style)
    return style


def validate_normalized(name: str, style: dict) -> None:
    """Fail loudly if a quirk fix left a required color missing or malformed."""
    for key in REQUIRED_NORMALIZED_COLORS:
        value = style.get(key)
        if not isinstance(value, str) or not re.fullmatch(
            r"#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?", value
        ):
            raise ValueError(f"{name}: normalized key {key!r} is not a valid color")


# --------------------------------------------------------------------------- #
# Emission
# --------------------------------------------------------------------------- #


def resolve_palette(style: dict) -> dict[str, str]:
    """Build the named palette written to ``theme.json`` ``colors``."""
    palette: dict[str, str] = {}
    for name, sources in ui_map.SEMANTIC_PALETTE.items():
        color = _first_color(style, sources)
        if color is None:
            fallback_name = ui_map.PALETTE_FALLBACKS.get(name)
            if fallback_name is not None:
                color = palette.get(fallback_name)
        if color is not None:
            palette[name] = color
    return palette


def resolve_ui(style: dict, palette: dict[str, str]) -> dict[str, str]:
    """Resolve UI component overrides against the palette."""
    ui: dict[str, str] = {}
    for ref, targets in ui_map.UI_MAP.items():
        if isinstance(ref, str) and ref.startswith("#"):
            color = ref
        else:
            color = palette.get(ref)
        if color is None:
            continue
        for target in _as_tuple(targets):
            ui[target] = color
    return ui


def render_theme_json(theme: dict) -> str:
    slug = SLUGS[theme["name"]]
    is_dark = theme.get("appearance") == "dark"
    style = normalize_variant(theme)
    palette = resolve_palette(style)
    document = {
        "name": theme["name"],
        "dark": is_dark,
        "author": AUTHOR,
        "parentTheme": "Islands Dark" if is_dark else "Islands Light",
        "editorScheme": f"/themes/{slug}.xml",
        "colors": palette,
        # Component overrides come from ui_map.UI_MAP; empty inherits Islands.
        "ui": resolve_ui(style, palette),
    }
    return json.dumps(document, indent=2) + "\n"


def _scheme_color_options(style: dict) -> list[tuple[str, str]]:
    """Ordered ``<colors>`` options from scheme chrome + VCS + terminal maps."""
    options: list[tuple[str, str]] = []

    for source, targets in scheme_colors.SCHEME_COLOR_MAP.items():
        color = _first_color(style, source)
        if color is None:
            continue
        for target in _as_tuple(targets):
            options.append((target, color))

    for source, targets in diff_vcs_map.VCS_COLOR_MAP.items():
        color = _first_color(style, source)
        if color is not None:
            for target in _as_tuple(targets):
                options.append((target, color))

    for slot, keys in ansi_map.ANSI_MAP.items():
        color = _first_color(style, slot)
        if color is None:
            continue
        classic_key, block_key = keys
        if classic_key:
            options.append((classic_key, color))
        if block_key:
            options.append((block_key, color))

    return options


def _attribute_options(style: dict) -> list[tuple[str, dict[str, object]]]:
    """Ordered ``<attributes>`` entries as (attribute_id, option map).

    Each entry's option map is ordered (FOREGROUND first, then any FONT_TYPE or
    BACKGROUND / ERROR_STRIPE_COLOR) and holds either an int (FONT_TYPE) or a hex
    string. Attribute ids may be shared by several Zed roles (for example the
    platform metadata colour covers macros and decorators); the first occurrence
    wins so each id is written exactly once.
    """
    entries: list[tuple[str, dict[str, object]]] = []
    seen: set[str] = set()
    syntax = style.get("syntax", {})

    def add(attr_id: str, options: dict[str, object]) -> None:
        if attr_id in seen:
            return
        seen.add(attr_id)
        entries.append((attr_id, options))

    for role, ids in syntax_map.SYNTAX_MAP.items():
        role_value = syntax.get(role)
        if not role_value:
            continue
        color = role_value.get("color")
        if not isinstance(color, str) or not color:
            continue
        font_type = _font_type(role_value)
        for attr_id in _as_tuple(ids):
            options: dict[str, object] = {"FOREGROUND": color}
            if font_type:
                options["FONT_TYPE"] = font_type
            add(attr_id, options)

    for attr_id, option_sources in diff_vcs_map.DIFF_ATTRIBUTE_MAP.items():
        options = {}
        for option_name, sources in option_sources.items():
            color = _first_color(style, sources)
            if color is not None:
                options[option_name] = color
        if options:
            add(attr_id, options)

    for source, attr_ids in scheme_colors.SCHEME_ATTRIBUTE_MAP.items():
        color = _first_color(style, source)
        if color is None:
            continue
        for attr_id in _as_tuple(attr_ids):
            add(attr_id, {"FOREGROUND": color})

    return entries


def render_scheme_xml(theme: dict) -> str:
    style = normalize_variant(theme)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<scheme name="{theme["name"]}" parent_scheme="Darcula" version="142">',
        "  <colors>",
    ]
    for name, color in _scheme_color_options(style):
        lines.append(f'    <option name="{name}" value="{color.lstrip("#")}"/>')
    lines.append("  </colors>")
    lines.append("  <attributes>")
    for attr_id, options in _attribute_options(style):
        lines.append(f'    <option name="{attr_id}">')
        lines.append("      <value>")
        for option_name, option_value in options.items():
            if isinstance(option_value, int):
                value = str(option_value)
            else:
                value = option_value.lstrip("#")
            lines.append(f'        <option name="{option_name}" value="{value}"/>')
        lines.append("      </value>")
        lines.append("    </option>")
    lines.append("  </attributes>")
    lines.append("</scheme>")
    lines.append("")
    return "\n".join(lines)


def build_outputs() -> dict[Path, str]:
    themes = json.loads(VENDOR.read_text())["themes"]
    by_name = {theme["name"]: theme for theme in themes}
    outputs: dict[Path, str] = {}
    for display_name, slug in SLUGS.items():
        theme = by_name[display_name]
        outputs[THEMES_DIR / f"{slug}.theme.json"] = render_theme_json(theme)
        outputs[THEMES_DIR / f"{slug}.xml"] = render_scheme_xml(theme)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify committed resources match generated output; do not write",
    )
    args = parser.parse_args()

    outputs = build_outputs()

    if args.check:
        drift = []
        for path, content in outputs.items():
            current = path.read_text() if path.exists() else None
            if current != content:
                drift.append(path)
        if drift:
            print("Generated resources are out of date:", file=sys.stderr)
            for path in drift:
                print(f"  {path.relative_to(ROOT)}", file=sys.stderr)
            print("Run: uv run tools/generate.py", file=sys.stderr)
            return 1
        print(f"Generator output up to date ({len(outputs)} files).")
        return 0

    THEMES_DIR.mkdir(parents=True, exist_ok=True)
    for path, content in outputs.items():
        path.write_text(content)
        print(f"wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
