"""Syntax mapping: Zed syntax key -> IntelliJ attribute ids (per language).

Filled in by the syntax ticket, gated on the Phase 0 attribute-id harvest.
Never invent an id: if a language role cannot be confidently enumerated, fall
back to a platform DEFAULT attribute rather than guessing.

TODO(syntax): role families (keyword/constant/string/function/type/comment/
punctuation/tag/variable/escape/link) plus platform DEFAULT and language-specific
id sets (Java, Kotlin, Python, JSON, JS/TS).
"""

from __future__ import annotations

# Zed syntax key -> tuple of IntelliJ attribute ids.
SYNTAX_MAP: dict[str, tuple[str, ...]] = {}

# Zed font_weight/font_style -> IntelliJ FONT_TYPE enum (0 plain, 1 bold,
# 2 italic, 3 bold+italic).
FONT_TYPE_MAP: dict[tuple[str | None, int | None], int] = {}
