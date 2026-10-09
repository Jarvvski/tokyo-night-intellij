# Phase 0 - Harvest JS/TS (+ Kotlin) attribute ids

Status: ready-for-agent

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

- [ ] Verified JS/TS id list recorded in `tools/mappings/syntax_map.py`.
- [ ] Verified Kotlin id list recorded (or anchors confirmed sufficient).
- [ ] Every id is attributable to a source (WebStorm export or named public port).
- [ ] Any role that cannot be confidently enumerated is explicitly listed to fall
      back to a platform DEFAULT attribute - no guessed ids.
- [ ] No color values copied; names only.
