# Terminal ANSI

Status: ready-for-agent

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

- [ ] Both key families emitted for all 16 slots per variant.
- [ ] Bright-overrides applied where upstream differs.
- [ ] `mise run check` green.
