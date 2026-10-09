# Syntax attributes (`<attributes>`)

Status: ready-for-agent

Blocked by: 02, 03, 01

## Background

Syntax highlighting is the largest attribute surface. Emit one parameterized
template per variant over role families derived from the palette's `syntax`
block (~96-100 keys).

## Scope

Role families: keyword (incl conditional/repeat/import/modifier), constant/number
(number/float/boolean/constant*/title), string (string*/character*/text.literal),
function (function*/constructor), type (type*/enum), comment (comment*/predoc),
punctuation (punctuation*/operator/keyword.operator), tag (tag*), variable/label
base-text, escape/macro/decorator specials, link/preproc teal.

Target attribute sets:

- Platform DEFAULT_* baseline (keyword, string, number, comments, identifier,
  constant, local variable, parameter, function decl/call, class/interface name,
  instance/static field/method, metadata, tag, attribute, escapes, reassigned
  vars, braces/brackets/parens/dot/semicolon/comma/operation_sign).
- Java full list; Kotlin confirmed anchors + ticket 01 harvest.
- Python dotted namespace (`PY.*`); JSON dotted namespace (`JSON.*`).
- JS/TS from ticket 01; incomplete roles inherit platform defaults.

FONT_TYPE: collapse Zed weights to enum (`700+` -> bold(1), italic -> italic(2),
both -> bold+italic(3)). Use EFFECT_TYPE only where meaningful.

## Acceptance criteria

- [ ] Each variant emits `<attributes>` for every confidently-enumerable role.
- [ ] JS/TS ids come only from the ticket 01 harvest.
- [ ] No invented ids; unresolved roles fall back to DEFAULT attributes.
- [ ] `mise run check` green.
