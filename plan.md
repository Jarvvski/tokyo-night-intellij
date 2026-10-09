# Plan: Tokyo Night theme plugin for IntelliJ IDEA

## Goal

Build an IntelliJ theme plugin that ports **all four variants** of the Zed theme
`ssaunderss/zed-tokyo-night` (`Tokyo Night`, `Tokyo Night Light`, `Tokyo Night Storm`,
`Tokyo Night Moon`), covering **UI chrome + syntax highlighting + terminal ANSI**.
The source of truth is the single Zed file `themes/tokyo-night.json`. Target
**IntelliJ IDEA 2026.3+**. The theme should feel native to IntelliJ where Zed has no
equivalent concept.

Project location: `/Users/jarvis/code/personal/tokyo-night-intellij/`.

## Locked decisions

| Decision | Value |
|---|---|
| Build strategy | Python generator reads the pinned Zed palette and emits all resource files; generated outputs are committed |
| Plugin display name | `Tokyo Night` |
| Plugin id | `dev.jarvis.tokyonight` |
| Vendor | `Adam Jarvis` |
| JS/TS syntax | Included in v1 (attribute ids must be harvested - see Phase 0) |
| Terminal fg/bright/dim | Derived (Zed leaves them null) |
| Target platform | 2026.3 line (build 263), pinned to a concrete EAP archive (e.g. `intellijIdea("263.6259.32-EAP") { useInstaller = false }`); `sinceBuild = "263"`, no `untilBuild` |
| Gradle | IntelliJ Platform Gradle Plugin 2.x (`org.jetbrains.intellij.platform`), Gradle >= 9, JDK >= 17 |
| UI base | Inherit Islands via `parentTheme` (`Islands Dark` / `Islands Light`) |

## Key architectural facts

- IntelliJ uses **two color systems**: UI colors live in `*.theme.json`; syntax +
  terminal + diff live in a separate editor color-scheme XML (`*.icls`, renamed
  `.xml`) linked from theme.json via top-level `"editorScheme": "/themes/X.xml"`.
- A theme-only plugin needs **no code** (confirmed by JetBrains docs and the
  zero-source repo `livewire-kt/livewire-intellij-theme`).
- Zed has no "surface" abstraction; many Zed keys map to several component-scoped
  IntelliJ keys, so some approximations are unavoidable.
- Modern IDE uses the new **block terminal** engine by default; classic console keys
  alone do NOT theme the terminal. Write ANSI to **both** key families.
- Islands landed in 2025.x and is default from 2025.3; classic UI restoration is gone
  after 2025.3.x.

## Toolchain notes

- Python via **uv** (`uv run tools/generate.py`), stdlib only (no third-party deps).
- Use `jq` for JSON inspection if helpful.
- Version control is **jj**; do not use raw `git`.

## Repository layout

```
tokyo-night-intellij/
├─ plan.md                         # this file
├─ README.md                       # build + install + regeneration steps
├─ LICENSE                         # our MIT + attribution to upstream MIT theme
├─ .gitignore                      # .gradle/ build/ .idea/ __pycache__/
├─ settings.gradle.kts
├─ build.gradle.kts
├─ gradle.properties               # version=0.1.0
├─ gradle/wrapper/{gradle-wrapper.jar,.properties}
├─ gradlew / gradlew.bat
├─ tools/
│  ├─ generate.py                  # uv run tools/generate.py ; stdlib only
│  ├─ mappings/
│  │   ├─ ui_map.py                # Zed UI key(s) -> palette name -> IntelliJ ui.* target(s)
│  │   ├─ syntax_map.py            # Zed syntax key -> IntelliJ attribute ids (per language)
│  │   ├─ scheme_colors.py         # .icls <colors> keys (editor chrome + console)
│  │   ├─ diff_vcs_map.py          # diff/VCS attribute + color keys
│  │   └─ ansi_map.py              # Zed ansi slot -> CONSOLE_* AND BLOCK_TERMINAL_*
│  └─ vendor/tokyo-night.json      # pinned upstream palette (76,972 bytes)
└─ src/main/resources/
   ├─ META-INF/
   │   ├─ plugin.xml              # one <themeProvider> per variant (+ icon)
   │   ├─ pluginIcon.svg          # ~40x40 viewBox, >=2px padding
   │   └─ pluginIcon_dark.svg     # optional
   └─ themes/
       ├─ TokyoNight.theme.json       + TokyoNight.xml
       ├─ TokyoNightStorm.theme.json  + TokyoNightStorm.xml
       ├─ TokyoNightMoon.theme.json   + TokyoNightMoon.xml
       └─ TokyoNightLight.theme.json  + TokyoNightLight.xml
```

Generated outputs are committed so `./gradlew buildPlugin` needs no Python.

---

## Phase 0 - Resolve JS/TS (+ Kotlin) attribute-id dependency

JS/TS attribute ids are not in OSS intellij-community. Acquisition, in order:

1. Export a full scheme from an installed **WebStorm / IDEA Ultimate**:
   Settings > Editor > Color Scheme > Export, then extract every `<option name="...">`
   id containing `JS`, `JSX`, `TypeScript`, or `TS`. Use names only; values come from
   our palette.
2. Fallback: harvest key names from a public broad-coverage port
   (`junkfactory/tokydark-jetbrains` `.xml`) and public exported dotfile schemes.

Same method hardens Kotlin ids beyond the confirmed anchors `KDOC_TAG_NAME`,
`KDOC_LINK`, `KOTLIN_LABEL`.

Output: verified id lists checked into `tools/mappings/syntax_map.py`. If a language
role cannot be confidently enumerated, it falls back to platform DEFAULT attributes
rather than guessed ids.

---

## Phase 1 - Scaffold

1. Create tree; init Gradle wrapper at Gradle >= 9.
2. `build.gradle.kts`:
   - plugins: `kotlin("jvm")` + `org.jetbrains.intellij.platform` (2.19.0)
   - repositories: `mavenCentral()` + `intellijPlatform { defaultRepositories() }`
   - deps: `intellijPlatform { intellijIdea("<263 EAP build>") { useInstaller = false } }`.
     A bare `"2026.3"` is NOT resolvable - EAP builds are published as concrete
     `263.x-EAP` versions in the snapshots repo; pin the newest and re-pin over time.
   - config:
     ```kotlin
     intellijPlatform {
         instrumentCode = false
         buildSearchableOptions = false
         pluginConfiguration {
             id = "dev.jarvis.tokyonight"
             name = "Tokyo Night"
             version = project.version.toString()
             vendor { name = "Adam Jarvis"; url = "https://github.com/jarvvski" }
             ideaVersion { sinceBuild = "263"; untilBuild = provider { null } }
         }
     }
     ```
3. `plugin.xml`: `<id>`, `<name>`, `<vendor>`, `<category>Theme</category>`,
   `<depends>com.intellij.modules.platform</depends>`, then four:
   ```xml
   <themeProvider id="dev.jarvis.tokyonight.<variant>" path="/themes/<File>.theme.json"/>
   ```
4. Minimal SVG icon(s).

---

## Phase 2 - Generator (`tools/generate.py`)

Read pinned JSON; per variant build a normalized semantic-color model applying:

### Quirk fixes

1. Normalize any hex missing a leading `#` (Light `text.accent` = `0f4b6e` -> `#0f4b6e`).
2. Fill keys absent in Light/Storm/Moon using fallbacks:

| Missing key(s) | Fallback |
|---|---|
| all ten `version_control.*` | generic `created/deleted/modified/conflict/renamed/ignored (+_background)` |
| `panel.indent_guide(_active/_hover)` | derive from editor indent guide / muted |
| `editor.indent_guide(_active)` | blend of line number + border |
| `editor.document_highlight.bracket_background` | `search.match_background` |
| `panel.overlay_background`, elevated fallbacks | per-variant elevated/border value |
| `pane_group.border` | `border.variant` |
| `terminal.ansi.background` | variant panel background |

3. Terminal derivation:
   - `terminal.foreground := editor.fg`
   - `terminal.bright_foreground := label/variable base-text color`
   - `terminal.dim_foreground := text.muted`
   Flag these as heuristics subject to visual tuning.

### Critical data rule

Do NOT assume the three dark variants share values. Moon diverges from Night/Storm in
several roles (base-text, type, number, etc.) while sharing others (punctuation).
Drive every value from the dump.

Emit `<File>.theme.json` and `<File>.xml` per variant.

---

## Phase 3 - UI mapping (`*.theme.json`)

Per variant:

```jsonc
{
  "name": "<Variant Display Name>",
  "dark": true,                        // false for Light only
  "author": "Adam Jarvis",
  "parentTheme": "Islands Dark",       // "Islands Light" for Light variant
  "editorScheme": "/themes/<File>.xml",
  "colors": { /* named palette */ },
  "ui": { /* component overrides */ }
}
```

Define a stable semantic palette (`bgBase`, `bgSurface`, `bgElevated`, `border`,
`borderFocus`, `fg`, `fgMuted`, `fgDisabled`, `accent`, `accentAlt`, `selection`,
`hover`, `activeTab`, severities, VCS) and reference names from component keys.

| Zed source | Palette name | IntelliJ targets |
|---|---|---|
| background / element/gutter bg | bgBase | MainWindow/ToolWindow backgrounds; editor bg via `.icls TEXT.BACKGROUND` |
| surface / panel / status_bar / title_bar / toolbar / tab_bar / tab.inactive | bgSurface | SidePanel/ToolWindow.Header backgrounds |
| elevated_surface / panel overlay | bgElevated | Popup/Menu/ToolTip backgrounds |
| tab.active_background / search.match_background | activeTab | EditorTabs background / search result bg |
| border(.variant/.selected/.disabled/.transparent) | border | Window/Panel/Borders borderColor |
| border.focused | borderFocus | focusColor variants |
| text / editor.fg | fg | Label/Link foregrounds |
| text.muted / icon(.muted) / hidden | fgMuted | secondary foregrounds/icons |
| text.disabled / element.disabled / icon.disabled | fgDisabled | disabledForeground variants |
| text.accent / icon.accent / link_text.hover | accent | accent/focus/hyperlink colors |
| element.hover/selected (= ghost states) | hover/selection | component hoverBackground/selectionBackground |
| error/warning/success/info/hint (+ .background/.border) | severities | Notification/Banner/ValidationTooltip severity colors |

Islands recipe: transparent sidebar borders (`StatusBar.borderColor`,
`ToolWindow.Stripe.borderColor`, `MainToolbar.borderColor` = alpha-transparent); main
backgrounds via ToolWindow/MainWindow keys; `Island.borderColor` matched to tool-window
background.

### Gate

Validate every emitted UI key against the current shipped metadata
(`IntelliJPlatform.themeMetadata.json`) before shipping; unresolved-key warnings surface
in IDE logs via the theme inspection. Several Islands-related literals (selected-tab
subkeys especially) were unverified during research - confirm or drop them. Avoid broad
wildcard rules initially; use targeted component overrides, and add wildcard only after
deliberate visual review.

---

## Phase 4 - Editor scheme (`*.xml`)

Root `<scheme name="<Variant>" parent_scheme="Darcula" version="142">`, then `<colors>`
and `<attributes>` (options FOREGROUND/BACKGROUND/FONT_TYPE/EFFECT_TYPE/EFFECT_COLOR).

### 4a. Editor chrome `<colors>`

| Zed source | `.icls <colors>` key |
|---|---|
| editor.active_line.background | CARET_ROW_COLOR |
| selection derived (recommend editor.document_highlight.read_background) | SELECTION_BACKGROUND (+ _INACTIVE) |
| editor.line_number | LINE_NUMBERS_COLOR |
| editor.active_line_number | LINE_NUMBER_ON_CARET_ROW_COLOR |
| editor.indent_guide(_active) | INDENT_GUIDE / SELECTED_INDENT_GUIDE |
| editor.gutter.background | GUTTER_BACKGROUND / EDITOR_GUTTER_BACKGROUND |
| created/modified/deleted blend | ADDED_LINES_COLOR / MODIFIED_LINES_COLOR / DELETED_LINES_COLOR |
| terminal background / panel bg | CONSOLE_BACKGROUND_KEY |
| editor.fg / error / muted system output | CONSOLE_NORMAL_OUTPUT / CONSOLE_ERROR_OUTPUT / CONSOLE_SYSTEM_OUTPUT |

### 4b. Syntax `<attributes>`

One parameterized template per variant over role families derived from the dump:
keyword-family (incl conditional/repeat/import/modifier), constant/number-family
(number/float/boolean/constant*/title), string-family (string*/character*/text.literal),
function-family (function*/constructor), type-family (type*/enum), comment-family
(comment*/predoc), punctuation-family (punctuation*/operator/keyword.operator),
tag-family (tag*), variable/label base-text family, escape/macro/decorator specials,
link/preproc teal family.

Target attribute sets:

- **Platform defaults** (automatic baseline in any language): DEFAULT_KEYWORD,
  DEFAULT_STRING, DEFAULT_NUMBER, DEFAULT_LINE_COMMENT, DEFAULT_BLOCK_COMMENT,
  DEFAULT_DOC_COMMENT, DEFAULT_IDENTIFIER, DEFAULT_CONSTANT, DEFAULT_LOCAL_VARIABLE,
  DEFAULT_PARAMETER, DEFAULT_FUNCTION_DECLARATION, DEFAULT_FUNCTION_CALL,
  DEFAULT_CLASS_NAME, DEFAULT_INTERFACE_NAME, DEFAULT_INSTANCE_FIELD/METHOD,
  DEFAULT_STATIC_FIELD/METHOD, DEFAULT_METADATA, DEFAULT_TAG, DEFAULT_ATTRIBUTE,
  DEFAULT_VALID_(INVALID_)STRING_ESCAPE, DEFAULT_REASSIGNED_LOCAL_VARIABLE/PARAMETER,
  braces/brackets/parenths/dot/semicolon/comma/operation_sign.
- **Java:** full JAVA_KEYWORD list incl LOCAL_VARIABLE/PARAMETER/INSTANCE_FIELD/
  FINAL_FIELD/STATIC_FIELD/FINAL_STATIC_FINAL CLASS_NAME ANONYMOUS_CLASS_NAME INTERFACE
  ENUM RECORD METHOD_CALL/DECLARATION STATIC_METHOD CONSTRUCTOR ANNOTATION_NAME
  ANNOTATION_ATTRIBUTE_NAME TYPE_PARAMETER ABSTRACT_METHOD INHERITED_METHOD visibility
  modifiers LAMBDA_PARAMETER RECORD_COMPONENT.
- **Kotlin:** confirmed anchors + Phase 0 harvest.
- **Python:** dotted namespace (`PY.KEYWORD`, `PY.STRING.B/U`, ...).
- **JSON:** dotted namespace (`JSON.STRING`, ...).
- **JS/TS:** Phase 0 harvest; incomplete roles inherit platform defaults.

FONT_TYPE: collapse Zed weights to enum (`700+` -> bold(1), italic stays italic(2),
both -> bold+italic(3)). Use EFFECT_TYPE only where meaningful.

### 4c. Diff/VCS

`<colors>`: FILESTATUS_MODIFIED, FILESTATUS_IDEA_FILESTATUS_MERGED_WITH_CONFLICTS (+
variants), FILESTATUS_MERGED/UNKNOWN,
FILESTATUS_addedOutside/DELETED_FROM_FILE_SYSTEM/IGNORED from version-control family.
`<attributes>`: DIFF_CONFLICT / DIFF_DELETED / DIFF_MODIFIED as FOREGROUND+BACKGROUND+
ERROR_STRIPE_COLOR triples plus DIFF_SEPARATORS_BACKGROUND. Populate VCS annotation slots
defensively handling non-contiguous platform slot numbering.

### 4d. Terminal ANSI

For each provided base8/bright8:

- classic engine index map: black0..white7 then darkgray8(= bright black)..white15(=
  bright white);
- block engine: BLOCK_TERMINAL_{BLACK..WHITE} and _BRIGHT variants;

plus BLOCK_TERMINAL_DEFAULT_FOREGROUND/BACKGROUND from derived terminal fg/bg.
Use Zed bright values where they differ within-variant from base (Night green bright
differs); otherwise mirror base8 to match observed source behavior.

---

## Phase 5 - Packaging & registration

Four `<themeProvider>` entries, each theme referencing its own `.xml` via
`editorScheme`. README documents build, install-from-disk, regeneration
(`uv run tools/generate.py`), and license attribution to the upstream MIT theme plus the
reference ports consulted for key names only.

---

## Phase 6 - Build & acceptance verification

1. `./gradlew buildPlugin` -> confirm artifact at
   `build/distributions/<name>-<version>.zip`.
2. Install via Settings > Plugins > Install Plugin from Disk on IDEA **2026.3 EAP**;
   restart; select each of the four themes and confirm its editor scheme auto-applies.
3. Per-variant checklist against upstream screenshots (`screenshots/*.png`):
   - chrome backgrounds/borders look native under Islands;
   - tabs/status/tool windows correct;
   - syntax roles match family colors;
   - diffs/VCS colors correct in Git tool window;
   - terminal ANSI correct in BOTH classic Run console and new block Terminal tool window;
   - Light variant legible with correct contrast.
4. Read idea.log for unresolved-key warnings; fix before declaring done.
5. Optionally run the Plugin Verifier task once.

---

## Risks

| Risk | Mitigation |
|---|---|
| Islands-related key literals partially unverified (selected-tab subkeys) | Validate every emitted key against current metadata before shipping |
| JS/TS (+ some Kotlin) ids need external harvest | Phase 0 gate before scheme authoring |
| Broad wildcard UI rules can over-paint components subtly and are hard to spot manually | Use targeted overrides first; only add wildcard after deliberate visual review |
| Light variant low-contrast combos may be illegible even if technically correct | Verify legibility manually in acceptance step; allow small contrast tuning |

---

## Reference: upstream palette summary

Source file: `https://raw.githubusercontent.com/ssaunderss/zed-tokyo-night/main/themes/tokyo-night.json`
(76,972 bytes). Four variants with identical key sets but different values:

| Variant | Appearance | Base background |
|---|---|---|
| Tokyo Night | dark | #1a1b26 |
| Tokyo Night Storm | dark | #24283b |
| Tokyo Night Moon | dark | #222436 |
| Tokyo Night Light | light | #d5d6db |

Per variant there are ~140 UI keys, a `syntax` block of exactly **100 token keys**
(identical across variants), and terminal ANSI base/bright slots (dim all null).

Confirmed source quirks:

1. Light `text.accent` is missing its leading `#`.
2. Only the Night variant defines all ten `version_control.*`,
   `panel.indent_guide*`, `panel.overlay_background`, `pane_group.border`,
   `editor.indent_guide*`, `editor.document_highlight.bracket_background`, and
   `terminal.ansi.background`. The other three omit them entirely.
3. Dim ANSI is null in every variant; terminal foreground/bright/dim are null everywhere.
