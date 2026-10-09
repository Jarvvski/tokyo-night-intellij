# Inherit the Islands UI via parentTheme and support IDEA 2026.2+

IntelliJ's modern "Islands" layout landed in 2025.x and became the default from
2025.3; classic-UI restoration was removed after 2025.3.x. Rather than re-create
chrome from scratch, each generated UI theme declares a `parentTheme` of
`Islands Dark` (or `Islands Light` for the light variant) and overrides only the
colors Tokyo Night changes.

We build against the newest pinned `intellijIdea("<263.x>-EAP")` archive with
`useInstaller = false` (a bare `"2026.3"` is not a resolvable artifact version -
EAP builds publish as concrete `263.x-EAP` versions) and declare
`sinceBuild = "262"` with **no** `untilBuild`, so the plugin installs on IDEA
**2026.2 and later**. Building against a newer platform than the declared minimum
is safe here because the plugin ships no code - it is pure resources consumed by
the theme engine.

Inheriting a platform theme keeps the theme resilient to new components: anything
we do not override follows Islands' own defaults instead of breaking.

## Consequences

- Islands-related key literals are partially unverified during research; every
  emitted UI key is validated against current theme metadata before shipping.
- Do not add broad wildcard UI rules up front; use targeted overrides and add a
  wildcard only after deliberate visual review.
- The build uses IntelliJ Platform Gradle Plugin 2.19.0, Gradle >= 9, JDK 21.

## Amendment - widened to include build 262

Originally this ADR set `sinceBuild = "263"`. During acceptance verification an
install attempt on IU-262 (IDEA 2026.2) failed with "requires build 263 or
newer". The owner approved widening support to **2026.2+**, so `sinceBuild` is
now `"262"`. Resources are still built and Plugin-Verifier-checked against the
pinned 2026.3 EAP archive.

Status: accepted
