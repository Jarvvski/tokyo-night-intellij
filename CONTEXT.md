# tokyo-night-intellij

A theme-only IntelliJ plugin that ports the four Zed Tokyo Night variants to
IntelliJ IDEA. It ships no application code: the artifact is a set of generated
resource files that IntelliJ's theme engine consumes.

## Language

### Core

**Variant**:
One of the four selectable themes - Tokyo Night, Tokyo Night Storm, Tokyo Night
Moon, or Tokyo Night Light - each a full UI + editor scheme pair.
_Avoid_: flavor, mode

**Palette JSON**:
The pinned upstream Zed theme file (`tools/vendor/tokyo-night.json`) that is the
single source of truth for every emitted color. It contains all four variants.
_Avoid_: source file, config

**Generator**:
`tools/generate.py`, the stdlib-only Python program that reads the Palette JSON
and writes every resource file. It is deterministic: same input, same output.
_Avoid_: script, compiler

**Mapping module**:
A declarative table under `tools/mappings/` that maps one subsystem's Zed keys to
IntelliJ keys. One module per subsystem (UI, syntax, scheme colors, diff/VCS,
ANSI).
_Avoid_: config, dictionary

**Quirk fix**:
A normalization the Generator applies because the upstream palette is imperfect
(missing `#`, keys absent in some variants, null terminal slots). Recorded so the
deviation from raw upstream is auditable.
_Avoid_: hack, workaround

### IntelliJ surfaces

**UI theme**:
The `*.theme.json` resource that themes IDE chrome (windows, toolbars, tabs,
popups). Names colors directly and points at an Editor scheme.
_Avoid_: UI scheme

**Editor scheme**:
The `*.xml` color-scheme resource (`<colors>` + `<attributes>`) that themes
syntax highlighting, terminal ANSI, and diff/VCS. Linked from a UI theme via
`editorScheme`.
_Avoid_: icls (the file extension), syntax theme

**Islands**:
The modern IntelliJ UI layout introduced in 2025.x and default from 2025.3. Every
variant inherits it via `parentTheme` (`Islands Dark` / `Islands Light`).
_Avoid_: new UI

**ANSI slot**:
One of the 16 terminal color positions (base black..white plus bright variants).
Written to **both** the classic console keys and the new block-terminal keys,
because the modern IDE defaults to the block engine.
_Avoid_: terminal color

### Sources of divergence

Night, Storm, and Moon are three *dark* variants with identical key sets but
**different values in several roles** (Moon diverges from Night/Storm in
base-text, type, and number, for example). Never assume dark variants share a
value; always drive from the Palette JSON.
