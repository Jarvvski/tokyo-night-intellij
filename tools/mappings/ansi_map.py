"""Terminal ANSI mapping: Zed ansi slot -> classic AND block-terminal keys.

The modern IDE defaults to the block terminal engine, so every slot must be
written to BOTH key families:

* classic console index map (black0..white7, then bright black..bright white);
* block engine ``BLOCK_TERMINAL_{BLACK..WHITE}`` and their ``_BRIGHT`` variants.

Two interfaces (both declarative; no side effects or I/O):

* ``ANSI_MAP`` - Zed ansi slot -> ``(classic_id, block_id)`` pair. Both halves
  are IntelliJ ``TextAttributesKey`` ids (verified against the shipped build:
  ``com.intellij.execution.process.ConsoleHighlighter`` and
  ``com.intellij.terminal.BlockTerminalColors``), so the generator emits each as
  a FOREGROUND-only ``<attributes>`` entry - NOT a ``<colors>`` option. Either
  half may be ``None`` to omit it.
* ``ANSI_COLOR_MAP`` - Zed source key(s) -> block-terminal default ``ColorKey``
  (``BLOCK_TERMINAL_DEFAULT_FOREGROUND`` / ``..._BACKGROUND``). These two are
  genuine ``ColorKey`` objects, so they are emitted in the ``<colors>`` block.

The classic index names are non-obvious: base white (index 7) is ``..._GRAY``,
bright black (index 8) is ``..._DARKGRAY`` and bright white (index 15) is
``..._WHITE``.
"""

from __future__ import annotations

# Zed ansi slot -> (classic attribute id, block-terminal attribute id).
ANSI_MAP: dict[str, tuple[str | None, str | None]] = {
    # Base colours (classic indices 0..7).
    "terminal.ansi.black": ("CONSOLE_BLACK_OUTPUT", "BLOCK_TERMINAL_BLACK"),
    "terminal.ansi.red": ("CONSOLE_RED_OUTPUT", "BLOCK_TERMINAL_RED"),
    "terminal.ansi.green": ("CONSOLE_GREEN_OUTPUT", "BLOCK_TERMINAL_GREEN"),
    "terminal.ansi.yellow": ("CONSOLE_YELLOW_OUTPUT", "BLOCK_TERMINAL_YELLOW"),
    "terminal.ansi.blue": ("CONSOLE_BLUE_OUTPUT", "BLOCK_TERMINAL_BLUE"),
    "terminal.ansi.magenta": ("CONSOLE_MAGENTA_OUTPUT", "BLOCK_TERMINAL_MAGENTA"),
    "terminal.ansi.cyan": ("CONSOLE_CYAN_OUTPUT", "BLOCK_TERMINAL_CYAN"),
    # Base white is index 7; the classic family calls it GRAY.
    "terminal.ansi.white": ("CONSOLE_GRAY_OUTPUT", "BLOCK_TERMINAL_WHITE"),
    # Bright colours (classic indices 8..15). Bright black is DARKGRAY and
    # bright white is plain WHITE in the classic family.
    "terminal.ansi.bright_black": (
        "CONSOLE_DARKGRAY_OUTPUT",
        "BLOCK_TERMINAL_BLACK_BRIGHT",
    ),
    "terminal.ansi.bright_red": ("CONSOLE_RED_BRIGHT_OUTPUT", "BLOCK_TERMINAL_RED_BRIGHT"),
    "terminal.ansi.bright_green": (
        "CONSOLE_GREEN_BRIGHT_OUTPUT",
        "BLOCK_TERMINAL_GREEN_BRIGHT",
    ),
    "terminal.ansi.bright_yellow": (
        "CONSOLE_YELLOW_BRIGHT_OUTPUT",
        "BLOCK_TERMINAL_YELLOW_BRIGHT",
    ),
    "terminal.ansi.bright_blue": (
        "CONSOLE_BLUE_BRIGHT_OUTPUT",
        "BLOCK_TERMINAL_BLUE_BRIGHT",
    ),
    "terminal.ansi.bright_magenta": (
        "CONSOLE_MAGENTA_BRIGHT_OUTPUT",
        "BLOCK_TERMINAL_MAGENTA_BRIGHT",
    ),
    "terminal.ansi.bright_cyan": (
        "CONSOLE_CYAN_BRIGHT_OUTPUT",
        "BLOCK_TERMINAL_CYAN_BRIGHT",
    ),
    "terminal.ansi.bright_white": ("CONSOLE_WHITE_OUTPUT", "BLOCK_TERMINAL_WHITE_BRIGHT"),
}

# Zed source key(s) -> block-terminal default <colors> ColorKey.
ANSI_COLOR_MAP: dict[object, str] = {
    ("terminal.foreground",): "BLOCK_TERMINAL_DEFAULT_FOREGROUND",
    ("terminal.background", "terminal.ansi.background"): (
        "BLOCK_TERMINAL_DEFAULT_BACKGROUND"
    ),
}
