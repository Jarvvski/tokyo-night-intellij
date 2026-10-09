"""Terminal ANSI mapping: Zed ansi slot -> classic AND block-terminal keys.

Interface (fixed by the generator-core ticket): ``ANSI_MAP`` maps a Zed ansi
slot key to a ``(classic_key, block_key)`` pair; either half may be ``None`` to
omit it. The modern IDE defaults to the block terminal engine, so every slot
must be written to BOTH key families:

- classic console index map (black0..white7, then bright black..bright white);
- block engine BLOCK_TERMINAL_{BLACK..WHITE} and their _BRIGHT variants.

Keep the table declarative; no side effects or I/O.

TODO(ansi): base8/bright8 slots plus BLOCK_TERMINAL_DEFAULT_FOREGROUND/BACKGROUND
derived from terminal fg/bg heuristics.
"""

from __future__ import annotations

# Zed ansi slot (e.g. "terminal.ansi.red") -> (classic_key, block_key).
ANSI_MAP: dict[str, tuple[str | None, str | None]] = {}
