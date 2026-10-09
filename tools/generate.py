#!/usr/bin/env python3
"""Generate IntelliJ theme resources from the pinned Zed palette.

Stdlib only. Reads ``tools/vendor/tokyo-night.json`` and emits, per variant:

    src/main/resources/themes/<Slug>.theme.json   (UI chrome)
    src/main/resources/themes/<Slug>.xml          (editor scheme)

Generated outputs are committed; never hand-edit them (see AGENTS.md).

This is the bootstrap skeleton. The full mapping logic lives in
``tools/mappings/*.py`` and is filled in by the phase tickets under
``.scratch/tokyo-night/issues/``. For now it derives a small, valid subset so the
plugin builds end to end.

Usage:
    uv run tools/generate.py           # write resources
    uv run tools/generate.py --check   # exit 1 if committed output would change
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENDOR = ROOT / "tools" / "vendor" / "tokyo-night.json"
THEMES_DIR = ROOT / "src" / "main" / "resources" / "themes"

AUTHOR = "Adam Jarvis"

# Canonical emission order: display name -> file slug.
SLUGS = {
    "Tokyo Night": "TokyoNight",
    "Tokyo Night Storm": "TokyoNightStorm",
    "Tokyo Night Moon": "TokyoNightMoon",
    "Tokyo Night Light": "TokyoNightLight",
}


def normalize_hex(value: str | None) -> str | None:
    """Ensure a leading '#'. Upstream Light text.accent omits it."""
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    return value if value.startswith("#") else f"#{value}"


def pick(style: dict, *keys: str) -> str | None:
    """First present, non-null color among ``keys``."""
    for key in keys:
        if key in style and style[key] is not None:
            return normalize_hex(style[key])
    return None


def semantic_palette(style: dict) -> dict[str, str]:
    """A minimal semantic palette; expanded by the UI mapping ticket."""
    bg_base = pick(style, "background", "editor.background")
    bg_surface = pick(style, "panel.background", "surface.background") or bg_base
    palette = {
        "bgBase": bg_base,
        "bgSurface": bg_surface,
        "bgElevated": pick(style, "elevated_surface.background", "panel.overlay_background") or bg_surface,
        "border": pick(style, "border") or bg_surface,
        "fg": pick(style, "text"),
        "fgMuted": pick(style, "text.muted", "icon.muted"),
        "accent": pick(style, "text.accent", "icon.accent"),
    }
    return {name: color for name, color in palette.items() if color is not None}


def scheme_colors(style: dict) -> dict[str, str]:
    """A minimal <colors> subset; expanded by the scheme-colors ticket."""
    candidates = {
        "CARET_ROW_COLOR": pick(style, "editor.active_line.background"),
        "LINE_NUMBERS_COLOR": pick(style, "editor.line_number"),
        "CONSOLE_BACKGROUND_KEY": pick(style, "terminal.background", "terminal.ansi.background"),
        "SELECTION_BACKGROUND": pick(style, "editor.document_highlight.read_background"),
    }
    return {name: color for name, color in candidates.items() if color is not None}


def render_theme_json(theme: dict) -> str:
    style = theme["style"]
    slug = SLUGS[theme["name"]]
    is_dark = theme.get("appearance") == "dark"
    document = {
        "name": theme["name"],
        "dark": is_dark,
        "author": AUTHOR,
        "parentTheme": "Islands Dark" if is_dark else "Islands Light",
        "editorScheme": f"/themes/{slug}.xml",
        "colors": semantic_palette(style),
        # Component overrides land here; empty inherits the parent (Islands) theme.
        "ui": {},
    }
    return json.dumps(document, indent=2) + "\n"


def render_scheme_xml(theme: dict) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<scheme name="{theme["name"]}" parent_scheme="Darcula" version="142">',
        '  <colors>',
    ]
    for name, color in scheme_colors(theme["style"]).items():
        lines.append(f'    <option name="{name}" value="{color.lstrip("#")}"/>')
    lines += [
        '  </colors>',
        '  <attributes/>',
        '</scheme>',
        '',
    ]
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
