"""Diff/VCS mapping: Zed version-control keys -> IntelliJ diff/VCS keys.

Interfaces (fixed by the generator-core ticket; populated by the diff/VCS
ticket; keep the tables declarative with no side effects or I/O):

* ``VCS_COLOR_MAP`` - Zed source key (or tuple of candidates) -> tuple of
  IntelliJ ``<colors>`` option names (FILESTATUS_*, VCS annotation slots,
  DIFF_SEPARATORS_BACKGROUND). One source drives several keys when several
  platform statuses share a Zed colour.
* ``DIFF_ATTRIBUTE_MAP`` - IntelliJ DIFF_* ``<attributes>`` id -> ordered map of
  attribute option name (FOREGROUND / BACKGROUND / ERROR_STRIPE_COLOR) to a Zed
  source key or tuple of candidate keys. The generator resolves each option and
  emits it as part of that id's ``<value>`` block.

All emitted ids were validated against the shipped 263 build line
(``DefaultColorSchemesManager.xml`` / ``IslandSchemeDark.xml`` and
``com/intellij/openapi/diff/DiffColors``); no invented ids.
"""

from __future__ import annotations

# Zed source key(s) -> IntelliJ <colors> option name(s).
VCS_COLOR_MAP: dict[object, tuple[str, ...]] = {
    # File status colours (Git tool window + editor gutter annotations).
    "version_control.added": (
        "FILESTATUS_ADDED",
        "FILESTATUS_COPIED",
        "FILESTATUS_addedOutside",
    ),
    "version_control.deleted": (
        "FILESTATUS_DELETED",
        "FILESTATUS_IDEA_FILESTATUS_DELETED_FROM_FILE_SYSTEM",
    ),
    # ``UNKNOWN`` has no Zed equivalent; routed to the modified accent.
    # ``modifiedOutside`` is an out-of-changelist modification.
    "version_control.modified": (
        "FILESTATUS_MODIFIED",
        "FILESTATUS_UNKNOWN",
        "FILESTATUS_modifiedOutside",
    ),
    # All merged-with-conflicts variants plus MERGED share the conflict accent.
    # The current platform registers three conflict variants (BOTH / PROPERTY /
    # plain); emit exactly those names rather than guessing further slots.
    "version_control.conflict": (
        "FILESTATUS_IDEA_FILESTATUS_MERGED_WITH_CONFLICTS",
        "FILESTATUS_IDEA_FILESTATUS_MERGED_WITH_PROPERTY_CONFLICTS",
        "FILESTATUS_IDEA_FILESTATUS_MERGED_WITH_BOTH_CONFLICTS",
        "FILESTATUS_MERGED",
        "FILESTATUS_changelistConflict",
    ),
    "version_control.renamed": ("FILESTATUS_RENAMED",),
    "version_control.ignored": ("FILESTATUS_IDEA_FILESTATUS_IGNORED",),
    # Fill colour between the two diff panes: the editor surface.
    "editor.background": ("DIFF_SEPARATORS_BACKGROUND",),
    # VCS annotation (blame) author slots. The platform registers a fixed set of
    # five named slots; emit exactly those by name rather than deriving an index
    # range. Sources are derived from the upstream ``accents`` ramp.
    "vcs.annotation_1": ("VCS_ANNOTATIONS_COLOR_1",),
    "vcs.annotation_2": ("VCS_ANNOTATIONS_COLOR_2",),
    "vcs.annotation_3": ("VCS_ANNOTATIONS_COLOR_3",),
    "vcs.annotation_4": ("VCS_ANNOTATIONS_COLOR_4",),
    "vcs.annotation_5": ("VCS_ANNOTATIONS_COLOR_5",),
}

# IntelliJ DIFF_* attribute id -> ordered {option name: Zed source key(s)}.
DIFF_ATTRIBUTE_MAP: dict[str, dict[str, object]] = {
    "DIFF_CONFLICT": {
        "FOREGROUND": ("version_control.conflict",),
        "BACKGROUND": ("diff.conflict_background",),
        "ERROR_STRIPE_COLOR": ("version_control.conflict",),
    },
    "DIFF_DELETED": {
        "FOREGROUND": ("version_control.deleted",),
        "BACKGROUND": ("diff.deleted_background",),
        "ERROR_STRIPE_COLOR": ("version_control.deleted",),
    },
    "DIFF_MODIFIED": {
        "FOREGROUND": ("version_control.modified",),
        "BACKGROUND": ("diff.modified_background",),
        "ERROR_STRIPE_COLOR": ("version_control.modified",),
    },
    # Inserted lines pair with deleted; Zed has no dedicated vc.inserted so use
    # the added accent (matches ``syntax.diff.plus``).
    "DIFF_INSERTED": {
        "FOREGROUND": ("version_control.added",),
        "BACKGROUND": ("diff.added_background",),
        "ERROR_STRIPE_COLOR": ("version_control.added",),
    },
}
