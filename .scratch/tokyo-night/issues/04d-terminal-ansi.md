# Terminal ANSI

Status: resolved

Blocked by: 02, 03

## Background

The modern IDE defaults to the block terminal engine, so classic console keys
alone do not theme the terminal. Every ANSI slot must be written to **both** key
families.

## Scope

For each provided base8/bright8 slot:

- classic engine index map: black0..white7 then darkgray8 (= bright black)
  .. white15 (= bright white);
- block engine: BLOCK_TERMINAL_{BLACK..WHITE} and their _BRIGHT variants;
- BLOCK_TERMINAL_DEFAULT_FOREGROUND/BACKGROUND from derived terminal fg/bg.

Use Zed bright values where they differ within-variant from base (Night green
bright differs); otherwise mirror base8 to match observed source behavior.

Dim ANSI is null in every variant and terminal foreground/bright/dim are null -
use the ticket 02 derivations.

## Acceptance criteria

- [x] Both key families emitted for all 16 slots per variant.
- [x] Bright-overrides applied where upstream differs.
- [x] `mise run check` green.

## Comments

Populated `ansi_map.py` and wired `generate.py`; only the four `.xml` files
changed (the `.theme.json` files are byte-identical - ANSI is XML-only). Plus
version + CHANGELOG (user-visible).

What landed:

- `ANSI_MAP`: 16 Zed slots -> `(classic_id, block_id)`, both halves TextAttributesKey
  ids. Base black..cyan -> `CONSOLE_{BLACK..CYAN}_OUTPUT` / `BLOCK_TERMINAL_{...}`;
  base white -> `CONSOLE_GRAY_OUTPUT` / `BLOCK_TERMINAL_WHITE`; bright black ->
  `CONSOLE_DARKGRAY_OUTPUT` / `BLOCK_TERMINAL_BLACK_BRIGHT`; bright white ->
  `CONSOLE_WHITE_OUTPUT` / `BLOCK_TERMINAL_WHITE_BRIGHT`.
- New `ANSI_COLOR_MAP`: derived `terminal.foreground` -> `BLOCK_TERMINAL_DEFAULT_FOREGROUND`,
  derived `terminal.background`/`terminal.ansi.background` -> `BLOCK_TERMINAL_DEFAULT_BACKGROUND`.
- `generate.py`: ANSI attribute ids now emitted FOREGROUND-only in `<attributes>`
  (appended after the console-output family, deduped); the two default ColorKeys
  emitted in `<colors>`. No IntelliJ key literals entered the generator.

Interface correction (flagged in the plan, owner-approved): ticket 02 fixed
`ANSI_MAP` as a colour pair consumed into `<colors>`. Verified against the
installed IDE that the classic (`ConsoleHighlighter.BLACK..WHITE`) and block
(`BlockTerminalColors.BLACK..WHITE_BRIGHT`) keys are **TextAttributesKey**, and
the shipped `DefaultColorSchemesManager.xml` places both under `<attributes>`;
only `BlockTerminalColors.DEFAULT_FOREGROUND/BACKGROUND` are `ColorKey`. Emitting
them as colours would have been unrecognized and tripped ticket 06's
unresolved-key check - the same class of correction as ticket 04a's console
output keys. No ADR conflict (ADR-0002 requires both key families, not a block).

Bright handling: each slot reads its own palette key, so Night green
(`73daca`) vs bright green (`41a6b5`) and the per-variant white/bright-white
differences are emitted automatically; where upstream sets bright equal to base
(Storm/Moon/Light) they mirror. No explicit mirroring logic was needed.

Accepted approximations:

- ANSI attribute keys are FOREGROUND-only (no BACKGROUND), consistent with the
  generated chrome/console attributes; background/reverse rendering left to
  ticket 06 visual review.
- Dim slots are unused (null upstream, no IntelliJ dim key); derived
  `terminal.bright_foreground`/`terminal.dim_foreground` have no IntelliJ target,
  so only `terminal.foreground` feeds the block default foreground.
- Membership check (throwaway, not committed): all 32 attribute ids present in
  the shipped scheme, both default ColorKeys registered in `BlockTerminalColors`.

Gate: `uv run tools/generate.py && uv run tools/generate.py --check &&
mise run check` all green (`BUILD SUCCESSFUL`, drift check "8 files").
