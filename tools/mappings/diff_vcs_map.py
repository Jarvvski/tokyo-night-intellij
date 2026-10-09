"""Diff/VCS mapping: Zed version-control keys -> IntelliJ diff/VCS keys.

Filled in by the diff/VCS ticket. Populate FILESTATUS_* <colors> slots and the
DIFF_* <attributes> triples (FOREGROUND + BACKGROUND + ERROR_STRIPE_COLOR), plus
VCS annotation slots; handle non-contiguous platform slot numbering defensively.

TODO(diff-vcs): map created/deleted/modified/conflict/renamed/ignored families.
"""

from __future__ import annotations

# Zed VCS key -> IntelliJ <colors> option name.
VCS_COLOR_MAP: dict[str, str] = {}

# Zed VCS key -> IntelliJ DIFF_* attribute id.
DIFF_ATTRIBUTE_MAP: dict[str, str] = {}
