# Packaging & registration

Status: ready-for-agent

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
- [ ] README reflects the actual commands and license attribution.
- [ ] `mise run check` green.
