# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.8.2 - 2026-10-09

### Fixed

- **Dialogs and lists match the flat surface.** Settings/dialog panels and content
  lists, trees and tables now use the base Tokyo Night background instead of
  inheriting Islands' dialog tone (`Dialog`, `Panel`, `List`, `Tree` and `Table`
  backgrounds).

## 0.8.1 - 2026-10-09

### Fixed

- **Window and panel edges.** Platform chrome borders no longer use the near-black
  palette value; they inherit Islands' subtle borders, removing the hard black
  frames and separators that appeared once the surface was flattened.
- **Folded (condensed) text.** The collapsed-code chip no longer inherits
  Darcula's grey box; its background and border are subtle tints derived from the
  editor surface and foreground.

## 0.8.0 - 2026-10-09

### Changed

- **Unified backgrounds.** The editor text area now takes its background from the
  palette via a new `TEXT` scheme attribute instead of inheriting Darcula's grey,
  and every chrome surface - sidebar/tree, tool-window headers,
  titlebar/toolbar, status bar and editor tabs - now uses the base Tokyo Night
  background rather than the darker surface shade, matching Zed's single-surface
  look. Popups, menus and tooltips stay slightly elevated so overlays still read
  as such.
- **Comfortable compact tree rows.** In Compact Mode the project-tree row height
  is now 30px instead of the compact default (~22px), closer to Zed's project
  panel rhythm; other compact spacing is unchanged.

## 0.7.1 - 2026-10-09

### Fixed

- **Themes now register in the IDE.** The four `<themeProvider>` entries were
  declared directly under `<idea-plugin>`, which the platform rejects with
  `Unknown element: themeProvider`, so no Tokyo Night theme appeared under
  Settings > Appearance & Behavior > Appearance. They are now declared inside an
  `<extensions defaultExtensionNs="com.intellij">` block.

## 0.7.0 - 2026-10-09

### Changed

- **Supported IDE range widened to IntelliJ IDEA 2026.2+.** The plugin now declares
  `since-build="262"` (no until-build) instead of `263`, so it installs on the
  2026.2 line as well as newer builds and installs from disk without a version
  mismatch error on those IDEs.

## 0.6.0 - 2026-10-09

### Added

- **Terminal ANSI colors.** Each variant now themes all 16 terminal ANSI slots
  from the pinned palette in both terminal engines: the classic console index
  map (black..white, bright black..bright white) and the block terminal
  (`BLOCK_TERMINAL_*` and their bright variants), plus the block terminal's
  default foreground/background.

## 0.5.0 - 2026-10-09

### Added

- **Diff / VCS colors.** Each variant now themes diff and version-control
  surfaces from the pinned palette: file-status colors in the Git tool window
  and editor gutter (added/copied, deleted, modified, renamed, merged/conflict,
  ignored, out-of-changelist), VCS blame annotation author colors, the diff
  pane separator, and added/deleted/modified/conflict line triples
  (foreground, background tint, and error stripe).

## 0.4.0 - 2026-10-09

### Added

- **Syntax highlighting.** Each variant now themes the editor `<attributes>`
  block from the pinned palette: keywords, numbers and constants, strings and
  escapes, functions and constructors, types and enums, variables/fields/
  parameters, comments and documentation, punctuation and operators, tags and
  attributes. Coverage spans the platform default keys plus Java, Kotlin,
  JavaScript, TypeScript, JSON, and Python, using only verified attribute ids.

## 0.3.0 - 2026-10-09

### Added

- **Editor scheme chrome.** Each variant now themes its editor chrome from the
  pinned palette: caret row, active/inactive selection, line numbers and the
  active-line number, indent guides, gutter background, added/modified/deleted
  line markers, and console output colors (normal/error/system).

## 0.2.0 - 2026-10-09

### Added

- **UI chrome mapping.** Each variant now themes window and tool-window
  backgrounds, headers, editor tabs, popups, borders, selection/hover states,
  foregrounds, and severity colors from the pinned palette. Every emitted key is
  validated against the shipped theme metadata for build 263.

## 0.1.0 - 2026-10-09

### Added

- **Repository bootstrap.** Theme-only IntelliJ plugin scaffold targeting IDEA
  2026.3 (sinceBuild 263), with a stdlib-only Python generator and four variants
  (Tokyo Night, Storm, Moon, Light).
