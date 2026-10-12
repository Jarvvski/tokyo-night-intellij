# Development

## How it works

The upstream Zed palette is the single source of truth. A stdlib-only Python
generator reads the pinned copy and writes every resource file, so no colour is
typed by hand.

```
tools/vendor/tokyo-night.json   pinned upstream palette (source of truth)
tools/generate.py               generator (stdlib only)
tools/mappings/*.py             Zed -> IntelliJ key mappings per subsystem
src/main/resources/themes/*     generated theme.json + xml (committed)
dist/spotifast/*                generated Spotifast palettes (committed)
```

Generated outputs are committed, so building the plugin does not need Python.

## Build

Tooling is driven by [mise](https://mise.jdx.dev):

```bash
mise install        # pin JDK 21, Python and uv
mise run build      # ./gradlew buildPlugin
mise run check      # generator drift check + buildPlugin (the pre-land gate)
```

Plain Gradle works too:

```bash
./gradlew buildPlugin   # artifact at build/distributions/
```

## Regenerate resources

After changing the generator or its mappings:

```bash
uv run tools/generate.py
```

Commit the changed files under `src/main/resources/themes/`. Do not hand-edit
generated files - the next regeneration would discard the edit. See
[`CLAUDE.md`](../CLAUDE.md) for the full rule.

## Spotifast palettes

The generator also writes Spotifast custom palettes to `dist/spotifast/` from the
same pinned palette, via [`tools/mappings/spotifast_map.py`](../tools/mappings/spotifast_map.py).
Commit them alongside the IntelliJ resources. `mise run spotifast-install` copies
them into Spotifast's themes folder and runs `spotifast reload-themes`.

## Screenshots

`mise run demo` launches an isolated sandbox IDE - a separate copy of the pinned
EAP build, so your installed IDE and its settings are untouched - with the
throwaway sources in [`screenshots/sample-project`](../screenshots/sample-project)
open and Tokyo Night preselected.

Open a source file (for example `ExampleService.kt`), capture a window screenshot,
then switch variant under Settings > Appearance & Behavior > Appearance and
repeat. Save the images as `screenshots/<variant>.png`.

## Project conventions

Conventions and agent guidance live in [`CLAUDE.md`](../CLAUDE.md) and
[`AGENTS.md`](../AGENTS.md). The plan of record is [`plan.md`](../plan.md).
