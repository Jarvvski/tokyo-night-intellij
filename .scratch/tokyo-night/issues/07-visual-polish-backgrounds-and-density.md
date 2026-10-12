# Visual polish: unified backgrounds & compact density

Status: resolved

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

Commit 3 (owner feedback after installing a `0.8.0` artifact), released as
`0.8.1` - a patch bump so an already-installed `0.8.0` is seen as updatable:

- Window/panel edges looked wrong once flattened: we overrode platform chrome
  borders (`Borders.color`, `Borders.ContrastBorderColor`, `Window.border`,
  `ToolWindow.borderColor`, `EditorTabs.borderColor`) with near-black `#101014`,
  while Islands itself uses subtle values (`ToolWindow.borderColor` transparent).
  Dropped those overrides so Islands' subtle borders return; only `borderFocus`
  remains themed.
- The collapsed `import ...` chip showed Darcula's grey box because we never
  defined `FOLDED_TEXT_ATTRIBUTES`. Added it (`FOREGROUND = fgMuted`,
  `BACKGROUND = editor.folded_background`) plus `FOLDED_TEXT_BORDER_COLOR`, with
  both colours derived as blends of editor bg toward fg (0.10 / 0.18).

Commit 4 (owner asked whether Settings/Plugins is themed), released as `0.8.2`:

- Dialogs/Settings and content lists/trees/tables kept Islands' inherited tone:
  no `Dialog/Panel/List/Tree/Table` *background* keys exist in the metadata or in
  built-in themes because those surfaces draw transparent over their container.
  Verified they are real platform LaF keys (present in class constant pools;
  `LookAndFeelThemeAdapter` maps theme `ui` onto them), then mapped all five
  backgrounds to `bgBase`. Popups stay elevated; hover/selection unchanged.

Commit 5 (live screen exploration), released as `0.8.3`:

- Sampling the running IDE showed several surfaces still on Islands greys: the
  top toolbar/title band and the left tool-window stripe (`#25282c`), popup/context
  menus (`#373737`), etc. Root cause: the parent `Islands Dark` resolves these from
  its named palette (`main-window-bg` = stripe + toolbar + title band;
  `popup-bg` = menus/popups), which we never redefined.
- Fix: new `tools/mappings/islands_palette.py` redefines those semantic names in
  our theme `colors` (`main-window-bg*`, `tool-window-bg*`, `editor-bg*`,
  `dialog-bg*` -> `bgBase`; `popup-bg*` -> `bgElevated`), so every parent key that
  references them follows automatically instead of overriding each key.

Note: the macOS global menu bar (File/Edit/...) is OS-drawn and cannot be themed by
an IntelliJ theme plugin; only in-IDE menus/dropdowns are themable.

Resolved: owner confirmed on `0.8.3` that the backgrounds, tree rows, edges,
folded chip, dialogs/lists and toolbar/stripe/menu surfaces all read correctly.
