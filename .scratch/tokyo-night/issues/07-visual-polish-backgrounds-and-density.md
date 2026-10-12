# Visual polish: unified backgrounds & compact density

Status: claimed

## Background

Acceptance of the four variants (ticket 06) surfaced two visual gaps against the
Zed reference:

1. Backgrounds are not uniform: the editor text area inherits the parent scheme's
   background (the generator never emits the `TEXT` attribute), and the chrome
   bars (`SidePanel`, tool-window headers, status bar, main toolbar, editor tabs)
   use the darker surface shade (`#16161e`) while content uses the base
   (`#1a1b26`).
2. The owner wants IntelliJ's Compact Mode overall, but with project-tree rows at
   a comfortable Zed-like height rather than the compact default (~22px).

## Scope

- Emit an editor `TEXT` scheme attribute so the editor background comes from the
  palette instead of the inherited parent scheme.
- Unify all chrome/content surfaces on `bgBase`; keep popups/menus/tooltips on
  `bgElevated` so overlays still read as elevated.
- Add a declarative UI-metric override so Compact Mode keeps project-tree rows at
  30px while other compact spacing is unchanged.
- Regenerate all committed resources from `tools/generate.py`.

## Acceptance criteria

- [ ] Editor text area, sidebar/tree, titlebar/toolbar/status bar and editor tabs
      all resolve to `bgBase` (`#1a1b26` in Night); popups/menus/tooltips stay
      `bgElevated`.
- [ ] In Compact Mode, project-tree rows are ~30px (taller than the compact
      default); other compact spacing is unchanged.
- [ ] `mise run check` green.

## Commits

1. Unify backgrounds on `bgBase` (scheme `TEXT` attribute + chrome repoint).
2. Add a compact-mode project-tree row-height metric override.

## Comments

Started from ticket 06 acceptance feedback: editor background did not match the
chrome, and compact mode needed taller project-tree rows.

Decisions taken with the owner:

- Single flat background `#1a1b26` everywhere; popups/menus/tooltips stay
  elevated (`#14141b`).
- Compact tree row height target **30px**, applied to trees only (not lists).

Mechanism notes (researched against the owner's build-262 install):

- Editor background is the scheme `TEXT` attribute's `BACKGROUND`; we never set
  it, so it fell back to Darcula grey while our gutter was already `#1a1b26`.
- Chrome came from `ui_map.UI_MAP` mapping `SidePanel`, tool-window headers,
  status bar, toolbar and editor tabs to `bgSurface` (`#16161e`).
- Row height is themable via `.theme.json` `ui` nested groups; built-in themes
  set exactly these (`darcula.theme.json`: `ui.Tree.rowHeight`,
  `ui.Tree.rowHeight.compact`, `ui.ToolWindow.Header.height.compact`, ...). These
  metric keys are not in `IntelliJPlatform.themeMetadata.json`, so they are
  validated against built-in-theme precedent rather than that metadata.

What landed (version `0.8.0`):

- Commit 1: `tools/mappings/scheme_colors.py` (`SCHEME_BACKGROUND_ATTRIBUTE_MAP`
  emitting the editor `TEXT` attribute), `tools/generate.py` (emit attribute
  backgrounds), `tools/mappings/ui_map.py` (chrome + `Editor.background` moved to
  `bgBase`; removed the now-unused `bgSurface` UI targets and `tabBar` palette),
  regenerated resources.
- Commit 2: new `tools/mappings/ui_metrics.py` (`Tree.rowHeight.compact = 30`)
  merged into `theme.json` `ui`; regenerated resources.

Pending: the owner enables Compact Mode and confirms the unified backgrounds and
tree row height visually, then this ticket can be resolved.
