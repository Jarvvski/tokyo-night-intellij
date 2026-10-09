# Inherit the Islands UI via parentTheme and target IDEA 2026.3

IntelliJ's modern "Islands" layout landed in 2025.x and became the default from
2025.3; classic-UI restoration was removed after 2025.3.x. Rather than re-create
chrome from scratch, each generated UI theme declares a `parentTheme` of
`Islands Dark` (or `Islands Light` for the light variant) and overrides only the
colors Tokyo Night changes.

We target `intellijIdea("2026.3")` with `sinceBuild = "263"` and **no**
`untilBuild`. 2026.3 is an EAP release, which ships no OS installer archive, so
the platform dependency sets `useInstaller = false`.

Inheriting a platform theme keeps the theme resilient to new components: anything
we do not override follows Islands' own defaults instead of breaking.

## Consequences

- Islands-related key literals are partially unverified during research; every
  emitted UI key is validated against current theme metadata before shipping.
- Do not add broad wildcard UI rules up front; use targeted overrides and add a
  wildcard only after deliberate visual review.
- The build uses IntelliJ Platform Gradle Plugin 2.19.0, Gradle >= 9, JDK 21.

Status: accepted
