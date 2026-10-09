# Diff / VCS colors

Status: ready-for-agent

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

- [ ] All four variants emit diff/VCS keys from palette-derived values.
- [ ] Non-Night variants use the documented fallback family.
- [ ] `mise run check` green.
