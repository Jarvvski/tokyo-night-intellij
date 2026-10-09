"""Diff/VCS mapping: Zed version-control keys -> IntelliJ diff/VCS keys.

Interfaces (fixed by the generator-core ticket; keep the tables declarative,
no side effects or I/O):

* ``VCS_COLOR_MAP`` - Zed source key (or tuple of candidates) -> tuple of
  IntelliJ ``<colors>`` option names (FILESTATUS_*).
* ``DIFF_ATTRIBUTE_MAP`` - Zed source key (or tuple of candidates) -> IntelliJ
  DIFF_* ``<attributes>`` id.

Filled in by the diff/VCS ticket. It must also populate FILESTATUS_* slots and
the DIFF_* triples (FOREGROUND + BACKGROUND + ERROR_STRIPE_COLOR) plus
DIFF_SEPARATORS_BACKGROUND, and handle non-contiguous platform slot numbering
defensively.

TODO(diff-vcs): map created/deleted/modified/conflict/renamed/ignored families.
"""

from __future__ import annotations

# Zed source key(s) -> IntelliJ <colors> option name(s).
VCS_COLOR_MAP: dict[object, tuple[str, ...]] = {}

# Zed source key(s) -> IntelliJ DIFF_* attribute id.
DIFF_ATTRIBUTE_MAP: dict[object, str] = {}
