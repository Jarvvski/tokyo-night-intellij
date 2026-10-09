# Diff / VCS colors

Status: resolved

Blocked by: 02, 03

## Background

Diff and VCS colors span both `<colors>` (FILESTATUS_*) and `<attributes>`
(DIFF_*). Only the Night variant defines all ten `version_control.*` keys
upstream; the other three need the fallback family from ticket 02.

## Scope

`<colors>`: FILESTATUS_MODIFIED, FILESTATUS_IDEA_FILESTATUS_MERGED_WITH_CONFLICTS
(+ variants), FILESTATUS_MERGED/UNKNOWN,
FILESTATUS_addedOutside/DELETED_FROM_FILE_SYSTEM/IGNORED.

`<attributes>`: DIFF_CONFLICT / DIFF_DELETED / DIFF_MODIFIED as FOREGROUND +
BACKGROUND + ERROR_STRIPE_COLOR triples, plus DIFF_SEPARATORS_BACKGROUND.

Populate VCS annotation slots defensively (non-contiguous platform numbering).

## Acceptance criteria

- [x] All four variants emit diff/VCS keys from palette-derived values.
- [x] Non-Night variants use the documented fallback family.
- [x] `mise run check` green.

## Comments

Populated `diff_vcs_map.VCS_COLOR_MAP` and reshaped `DIFF_ATTRIBUTE_MAP`, and
regenerated the four `.xml` files; the `.theme.json` files are byte-identical
(diff/VCS is XML-only). Only `tools/mappings/diff_vcs_map.py`,
`tools/generate.py` and generated outputs changed (plus version + CHANGELOG).

What landed:

- `VCS_COLOR_MAP`: the `version_control.*` family (Night upstream, other
  variants via ticket 02 quirk fix 2a) drives the file-status colours -
  added/copied/addedOutside, deleted/DELETED_FROM_FILE_SYSTEM,
  modified/UNKNOWN/modifiedOutside, all merged-with-conflicts variants +
  MERGED + changelistConflict, renamed, ignored. Plus
  `DIFF_SEPARATORS_BACKGROUND` (editor background) and five
  `VCS_ANNOTATIONS_COLOR_1..5` blame-author slots.
- `DIFF_ATTRIBUTE_MAP` reshaped from a flat id map to attr-id ->
  {FOREGROUND/BACKGROUND/ERROR_STRIPE_COLOR: source(s)}; `generate.py`
  consumes it generically (dedupe/first-wins and ordering preserved) so no
  IntelliJ key literal entered the generator.
- New generator derivations (labelled heuristics, asserted by
  `REQUIRED_NORMALIZED_COLORS`): `diff.{added,deleted,modified,conflict}_background`
  = editor background blended 15% toward each status accent; `vcs.annotation_{1..5}`
  = first five upstream `accents`, alpha byte dropped to keep scheme values RGB.

Validation: a throwaway (uncommitted) script confirmed every emitted id exists in
the pinned 263 build - FILESTATUS_* / VCS_ANNOTATIONS_COLOR_* against
`DefaultColorSchemesManager.xml` + `IslandSchemeDark.xml`, DIFF_* against
`com/intellij/openapi/diff/DiffColors`, DIFF_SEPARATORS_BACKGROUND against the
shipped expUI scheme. Zero unresolved ids across all four files.

Decisions / accepted approximations:

- Emitted the annotation slots by exact name (`_1.._5`) rather than an index
  range, defensively per the platform's non-contiguous registration.
- Included the full file-status family (ADDED/COPIED/RENAMED/DELETED and the
  out-of-changelist states) beyond the ticket's terse list so the Git tool window
  is coherent rather than half-inheriting Darcula; edge states with no Zed
  analogue (HIJACKED/OBSOLETE/SUPPRESSED/SWITCHED/NOT_CHANGED*/ERRORS) are left
  inherited.
- Added `DIFF_INSERTED` alongside the mandated CONFLICT/DELETED/MODIFIED triples
  (Zed has no dedicated inserted key; uses the added accent).
- `FILESTATUS_UNKNOWN` -> modified accent and `FILESTATUS_MERGED` -> conflict
  accent (no direct Zed equivalents); line-tint blend factor (0.15) and light
  variant contrast are subject to visual tuning in ticket 06.

Gate: `uv run tools/generate.py && uv run tools/generate.py --check &&
mise run check` all green (`BUILD SUCCESSFUL`, drift check "8 files").
User-visible, so `gradle.properties` bumped to 0.5.0 with a dated CHANGELOG entry.
