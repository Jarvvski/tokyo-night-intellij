# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
