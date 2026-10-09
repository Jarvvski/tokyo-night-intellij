# Packaging & registration

Status: resolved

Blocked by: 04a, 04b, 04c, 04d

## Background

The four `<themeProvider>` entries are already wired in `plugin.xml` and the
build produces a zip. This ticket verifies packaging is complete once all
resources are real.

## Scope

- Confirm each variant's `*.theme.json` references its own `.xml` via
  `editorScheme`.
- Confirm the built jar contains all eight resource files plus `plugin.xml`.
- Confirm `plugin.xml` category/depends/vendor are correct and the patched
  `idea-version` is `since-build="263"` with no until-build.
- Update `README.md` if build/install/regeneration steps drifted.

## Acceptance criteria

- [ ] `./gradlew buildPlugin` artifact contains four `.theme.json` + four `.xml`.
- [ ] Each theme selects its matching editor scheme at runtime.
- [x] README reflects the actual commands and license attribution.
- [x] `mise run check` green.

## Comments

Resolved as a packaging/registration verification. The build already assembled
correctly; the only real drift was in `README.md`.

Evidence (read from the built artifact, not hand-asserted):

- `build/distributions/tokyo-night-intellij-0.6.0.zip` -> inner jar contains
  exactly `META-INF/plugin.xml`, `META-INF/pluginIcon.svg`, four
  `themes/*.theme.json` and four `themes/*.xml` - the eight resources plus
  `plugin.xml`.
- Patched manifest inside the jar: `<idea-version since-build="263" />` with no
  until-build; `<category>Theme</category>`,
  `<depends>com.intellij.modules.platform</depends>`, vendor `Adam Jarvis`, id
  `dev.jarvis.tokyonight`, name `Tokyo Night`.
- Static editorScheme chain verified for all four variants: each
  `<themeProvider>` points at a `.theme.json` whose top-level `editorScheme`
  points at its own sibling `.xml`.

What landed:

- `README.md`: corrected the install-from-disk artifact name from
  `tokyo-night-<version>.zip` to `tokyo-night-intellij-<version>.zip` (the real
  name, driven by `settings.gradle.kts` `rootProject.name`, with no
  archiveBaseName override); corrected the `mise install` comment to note it also
  pins uv.

Decisions / accepted boundary:

- "Each theme selects its matching editor scheme at runtime" is verified
  statically here (the full registration chain). Runtime auto-apply belongs to
  ticket 06's manual install-and-visually-verify checklist and is not automatable.
- Docs-only change; the plugin artifact is byte-unchanged, so no version bump or
  CHANGELOG entry.

Gate: `uv run tools/generate.py && uv run tools/generate.py --check &&
mise run check` all green (`BUILD SUCCESSFUL`; drift check "8 files").
