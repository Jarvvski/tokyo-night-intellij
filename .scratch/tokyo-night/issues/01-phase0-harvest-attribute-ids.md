# Phase 0 - Harvest JS/TS (+ Kotlin) attribute ids

Status: resolved

## Background

JS/TS attribute ids are not present in OSS intellij-community, so they cannot be
read from a bundled scheme in this repo's build environment. They are needed by
ticket 04b (syntax attributes). Kotlin ids are only partially known (confirmed
anchors: `KDOC_TAG_NAME`, `KDOC_LINK`, `KOTLIN_LABEL`).

## Scope

Acquire verified id lists only - **names**, never values (values come from our
palette):

1. Primary: export a full color scheme from an installed **WebStorm / IDEA
   Ultimate** (Settings > Editor > Color Scheme > Export) and extract every
   `<option name="...">` id containing `JS`, `JSX`, `TypeScript`, or `TS`.
2. Fallback: harvest key names from a public broad-coverage port
   (`junkfactory/tokydark-jetbrains` `.xml`) and public exported schemes.

Same method hardens Kotlin ids beyond the confirmed anchors.

## Acceptance criteria

- [x] Verified JS/TS id list recorded in `tools/mappings/syntax_map.py`.
- [x] Verified Kotlin id list recorded (or anchors confirmed sufficient).
- [x] Every id is attributable to a source (WebStorm export or named public port).
- [x] Any role that cannot be confidently enumerated is explicitly listed to fall
      back to a platform DEFAULT attribute - no guessed ids.
- [x] No color values copied; names only.

## Comments

Method used was the primary one, satisfied without a GUI export because the IDEs
are installed locally and their registration is inspectable:

- JS (`JS_ATTRIBUTE_IDS`, 42 ids): WebStorm 2026.x
  `plugins/javascript-plugin/lib/modules/intellij.javascript.psi.impl.jar`,
  class `JavaScriptHighlightDescriptor` - external key is `"JS." + descriptor
  name` (prefix read from the `makeConcatWithConstants` recipe `JS.\u0001`), with
  six explicit suffix overrides.
- TS (`TS_ATTRIBUTE_IDS`, 41 ids): same jar, class `TypeScriptHighlighter` -
  literal `TS.*` names. `TS_ENUM`, `TS_ENUM_MEMBER`, `TS_TYPE_PARAMETER` are
  aliases (`getMappedKey`) and register no standalone external name, so omitted.
- Kotlin (`KOTLIN_ATTRIBUTE_IDS`, 72 ids incl. anchors `KDOC_LINK`,
  `KDOC_TAG_NAME`): IDEA-bundled Kotlin plugin
  `plugins/Kotlin/lib/kotlin-plugin-shared.jar`, class
  `KotlinHighlightingColors`; naming cross-checked against bundled
  `intellij.kotlin.base.resources.jar:/colorScheme/Darcula_Kotlin.xml`.
- Roles with no confident JS/TS/Kotlin id are listed in
  `UNRESOLVED_ROLE_FALLBACKS` for ticket 03 to route to platform DEFAULT.

Each recorded tuple was diffed against the jar-extracted set and matches exactly.
No values were read into the module.
