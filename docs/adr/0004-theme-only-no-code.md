# A theme-only plugin ships no application code

An IntelliJ theme plugin needs no compiled classes: registration is entirely
declarative via `plugin.xml`, which lists one `<themeProvider>` per variant, each
pointing at a `*.theme.json`. The plugin JAR is therefore pure resources.

We still apply the Kotlin JVM Gradle plugin proactively so that if a class ever
becomes genuinely necessary it can be written in Kotlin (the owner's convention)
without reworking the build. Today `src/main/kotlin/` is intentionally empty.

Because there is no application logic, the pre-land gate is not a test suite but
a **build + drift check**: regenerate resources and confirm no diff, then run
`buildPlugin` to prove the artifact assembles.

## Consequences

- Do not add source files speculatively; a class needs a real reason.
- CI runs `mise run check`, which is generator drift + `buildPlugin`.
- Acceptance is manual (install-from-disk on IDEA 2026.3 EAP and visually verify),
  not automated unit testing.

Status: accepted
