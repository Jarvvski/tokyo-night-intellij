# Build & acceptance verification

Status: claimed

Blocked by: 01, 02, 03, 04a, 04b, 04c, 04d, 05

## Background

Automated verification stops at "it builds". Visual acceptance is manual and is
the final gate before declaring the port done.

## Scope

1. `./gradlew buildPlugin` -> confirm artifact at
   `build/distributions/<name>-<version>.zip`.
2. Install via Settings > Plugins > Install Plugin from Disk on IDEA **2026.3
   EAP**; restart; select each of the four themes and confirm its editor scheme
   auto-applies.
3. Per-variant checklist against upstream screenshots:
   - chrome backgrounds/borders look native under Islands;
   - tabs/status/tool windows correct;
   - syntax roles match family colors;
   - diffs/VCS colors correct in the Git tool window;
   - terminal ANSI correct in BOTH classic Run console and block Terminal tool
     window;
   - Light variant legible with correct contrast.
4. Read `idea.log` for unresolved-key warnings; fix before declaring done.
5. Optionally run the Plugin Verifier task once.

## Acceptance criteria

- [ ] All four variants verified visually per checklist.
- [ ] No unresolved-key warnings in idea.log.
- [x] Any accepted approximation documented (Zed key with no IntelliJ equivalent).
- [x] `mise run check` green.

## Comments

Claimed for automated verification; left `claimed` because criteria 1-2 are manual
acceptance (ADR-0004: install-from-disk on IDEA 2026.3 EAP and visually verify).
The two automatable criteria are satisfied; the visual pass and `idea.log` read
remain with the owner.

Automated evidence (read from the built artifact, not hand-asserted):

- Artifact: `build/distributions/tokyo-night-intellij-0.6.0.zip` -> inner jar
  `tokyo-night-intellij-0.6.0.jar` contains exactly `META-INF/plugin.xml`,
  `META-INF/pluginIcon.svg`, four `themes/*.theme.json` and four `themes/*.xml`.
- Patched `META-INF/plugin.xml`: `<idea-version since-build="263" />` with no
  until-build; `<category>Theme</category>`,
  `<depends>com.intellij.modules.platform</depends>`, id `dev.jarvis.tokyonight`,
  name `Tokyo Night`, vendor `Adam Jarvis`, four `<themeProvider>` entries.
  Manifest: `Platform-Version: 2026.3`, `Platform-Build: 263.6259.32`.
- Static editorScheme chain verified for all four variants: each `<themeProvider>`
  points at a `.theme.json` whose top-level `editorScheme` points at its own
  sibling `.xml`.
- Plugin Verifier (`./gradlew verifyPlugin`) once against IU-263.6259.32:
  **Compatible**, "can probably be enabled or disabled without IDE restart".
  Report: `build/reports/pluginVerifier/IU-263.6259.32`.
- Gate: `uv run tools/generate.py && uv run tools/generate.py --check &&
  mise run check` all green (`BUILD SUCCESSFUL`; drift check "8 files").

Unresolved-key warnings: not automatable from a build (they surface in a running
IDE's `idea.log` via the theme inspection), so criterion 2 stays open for the
owner's run. Every emitted key was already validated against shipped build-263
metadata per-ticket (03 UI keys; 04a-d scheme keys; each check was a throwaway
script, not committed) - see those tickets' Comments for the id sources.

Accepted approximations (cumulative, carried from prior tickets):

- UI: targeted component overrides only; List/Tree/Table *backgrounds* inherit
  Islands defaults pending deliberate visual review (03).
- Editor chrome: ADDED/MODIFIED/DELETED_LINES_COLOR use the created/modified/
  deleted palette values directly rather than a computed blend (04a).
- Syntax: unresolved roles route to a nearest verified platform DEFAULT, or stay
  in `UNRESOLVED_ROLE_FALLBACKS` where none exists; Python docstrings use the
  string-family colour; no `FONT_TYPE` emitted yet (04b).
- Diff/VCS: line-tint blend factor (0.15) and light-variant contrast subject to
  visual tuning; edge file states with no Zed analogue left inherited (04c).
- ANSI: attribute keys are FOREGROUND-only; dim slots unused (null upstream) (04d).

Manual checklist for the owner (complete, then set this ticket `resolved`):

1. Settings > Plugins > Install Plugin from Disk ->
   `build/distributions/tokyo-night-intellij-0.6.0.zip`; restart.
2. Select each of Tokyo Night / Storm / Moon / Light under Settings > Appearance;
   confirm the matching editor scheme auto-applies each time.
3. Per variant, verify: chrome backgrounds/borders native under Islands;
   tabs/status/tool windows correct; syntax family colours; diff/VCS in the Git
   tool window; terminal ANSI in BOTH the classic Run console and the block
   Terminal tool window; Light legible with correct contrast.
4. Read `idea.log` for unresolved-key warnings; fix before resolving.

No version bump or CHANGELOG entry was needed for the automated verification
itself; see the follow-up below.

Follow-up (owner-driven): an install attempt on IU-262 (IDEA 2026.2) failed with
"requires build 263 or newer". The owner approved widening support to 2026.2+
(`sinceBuild = "262"`, still built and Plugin-Verifier-checked against the pinned
2026.3 EAP archive). That is a user-visible change, landed separately with a
version bump to 0.7.0, a CHANGELOG entry, and plan.md / ADR-0003 / README updates.
The manual visual pass and `idea.log` read can now run on IU-262 or later;
criteria 1-2 stay open until then.

Install verification (owner's IDEA, IU-262/2026.2.3): after installing 0.7.0, no
Tokyo Night entry appeared under Settings > Appearance, and `idea.log` showed
`SEVERE - PluginParser - Unknown element: themeProvider`. Root cause: the four
`<themeProvider>` entries were direct children of `<idea-plugin>`, but on this
platform `themeProvider` is a `com.intellij` extension point, so the descriptor
parser dropped them and registered no themes (the `TokyoNightNight` scheme in the
dropdown is a pre-existing user scheme, not ours). Fixed in 0.7.1 by wrapping them
in `<extensions defaultExtensionNs="com.intellij">`. This also shows ticket 05's
registration check was static-only (theme.json -> xml chain) and did not exercise
descriptor parsing; reinstall the 0.7.1 zip to complete the manual pass.

Offline key validation against build **262** (owner's IU-262 install at
`/Applications/IntelliJ IDEA.app`) - the static stand-in for criterion 2:

- UI keys: all 69 `ui.*` keys in each of the four `.theme.json` resolve against
  the shipped `themes/metadata/*.themeMetadata.json` (IntelliJPlatform + JDK +
  plugin metadata; 1352 valid keys). Zero unresolved across all four variants.
- `<colors>` keys: all 36 per variant are valid ColorKeys - 32 appear in
  `DefaultColorSchemesManager.xml`, and the other four were confirmed as class
  constants: `BLOCK_TERMINAL_DEFAULT_FOREGROUND/BACKGROUND`
  (`BlockTerminalColors`), `DIFF_SEPARATORS_BACKGROUND`
  (`DiffLineSeparatorRenderer`), `EDITOR_GUTTER_BACKGROUND` (`EditorColors`).
- `<attributes>` ids: language ids are not conclusively enumerable from shipped
  scheme resources alone (JS builds ids at runtime as `"JS." + name`; some
  plugins register in code), so they remain covered by tickets 01/04b's
  class-level validation plus spot checks here (JAVA_KEYWORD, KOTLIN_KEYWORD,
  JSON.STRING, TS.STRING, TS.PRIMITIVE.TYPES, DEFAULT_KEYWORD all present).

No mapping changes resulted - nothing that is actually invalid was found.

Follow-ups filed as ticket **07** (visual polish): unify backgrounds on `bgBase`
(the editor text area previously inherited Darcula's grey; chrome used the darker
surface shade) and keep compact-mode project-tree rows at ~30px.
