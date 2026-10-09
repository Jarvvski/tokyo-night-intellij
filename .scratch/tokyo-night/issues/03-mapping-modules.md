# Mapping modules

Status: ready-for-agent

## Background

Five declarative mapping modules exist as stubs under `tools/mappings/`. Each maps
one subsystem's Zed keys to IntelliJ keys. They are independent files once their
interfaces (dict shapes) are fixed by ticket 02.

## Scope

Populate each module as a declarative table:

- `ui_map.py` - Zed UI key(s) -> palette name -> IntelliJ `ui.*` target(s).
- `syntax_map.py` - Zed syntax key -> IntelliJ attribute ids (per language),
  gated on ticket 01 for JS/TS + Kotlin.
- `scheme_colors.py` - Zed UI key -> editor scheme `<colors>` key.
- `diff_vcs_map.py` - Zed VCS keys -> FILESTATUS_* / DIFF_* keys.
- `ansi_map.py` - Zed ansi slot -> classic AND block-terminal key pair.

## Constraints

- Never invent an IntelliJ attribute id; fall back to a platform DEFAULT when a
  role cannot be confidently enumerated.
- Keep tables declarative; no side effects or I/O in mapping modules.

## Acceptance criteria

- [ ] Each module exports the table documented in its docstring.
- [ ] Generator consumes them with no inline key literals left behind.
- [ ] Every mapped IntelliJ key is validated against shipped theme metadata where
      applicable (UI); unresolved keys dropped or corrected before shipping.
- [ ] `mise run check` green.
