# Syntax attributes (`<attributes>`)

Status: resolved

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

## Comments

Populated `syntax_map.SYNTAX_MAP` (54 Zed roles -> 247 distinct IntelliJ
attribute ids per variant) and regenerated the four `.xml` files; the
`.theme.json` files are byte-identical (syntax is XML-only). Only
`tools/mappings/syntax_map.py`, `tools/generate.py` (dedupe) and generated
outputs changed.

Verified id sources (names only, no values copied):

- Platform `DEFAULT_*` + base-scheme punctuation keys: IDEA 2026.2.3
  `intellij.platform.core.jar`, `DefaultLanguageHighlighterColors`.
- Java `JAVA_*` + `*_ATTRIBUTES`: IDEA `JavaHighlightingColors`.
- JSON dotted `JSON.*`: IDEA `plugins/json/lib/intellij.json.jar`,
  `JsonSyntaxHighlighterFactory`.
- Python dotted `PY.*`: PyCharm OSS
  `python-syntax-core/.../PyHighlighter.java` (+ `PythonColorsPage.java`).
- JS/TS/Kotlin: ticket 01 harvest, unchanged.

A throwaway membership check (not committed) asserted every id in `SYNTAX_MAP`
is in its source set, and that the JS/TS/Kotlin pools still match the pre-change
commit exactly: all 274 ids across 54 roles verified.

Decisions / accepted approximations:

- Unresolved roles are routed to a semantically nearest verified platform DEFAULT
  where one exists (`link_text` -> `DEFAULT_HIGHLIGHTED_REFERENCE`,
  `embedded` -> `DEFAULT_TEMPLATE_LANGUAGE_COLOR`, structural meta roles ->
  `DEFAULT_IDENTIFIER`) rather than dropped. Roles with no dedicated key and no
  sensible default stay in `UNRESOLVED_ROLE_FALLBACKS`: prose emphasis, boolean,
  markdown title, comment todo/warning/error/hint/note, character, keyword.debug,
  regex/path/url string subroles, preproc, tag.delimiter/doctype,
  punctuation.list_marker.
- Python docstrings take the string-family colour (`string.doc` ->
  `PY.DOC_COMMENT`) because Zed tags them as strings, not comments.
- Generators dedupe attribute ids on emission (first occurrence wins), so ids
  shared across roles (metadata/decorator, attribute/tag.attribute, etc.) emit
  exactly once; no duplicate `<option>` ids appear in any variant.
- No mapped Zed role carries a bold/italic weight (only the unmapped emphasis
  roles do), so no `FONT_TYPE` options are emitted yet; the collapse logic and
  `FONT_TYPE_MAP` are in place for when a styled role gains a confident key.
- `diff.minus`/`diff.plus` are left to ticket 04c (diff/VCS).

Gate: `uv run tools/generate.py && uv run tools/generate.py --check &&
mise run check` all green (`BUILD SUCCESSFUL`, drift check "8 files").
User-visible, so `gradle.properties` bumped to 0.4.0 with a dated CHANGELOG entry.
