# Tokyo Night for IntelliJ IDEA

A theme-only IntelliJ plugin that ports all four variants of the Zed theme
[`ssaunderss/zed-tokyo-night`](https://github.com/ssaunderss/zed-tokyo-night)
to IntelliJ IDEA: **Tokyo Night**, **Tokyo Night Storm**, **Tokyo Night Moon**,
and **Tokyo Night Light**.

Each variant ships UI chrome (`*.theme.json`), syntax highlighting plus terminal
and diff colors (`*.xml` editor scheme), so selecting a theme applies the editor
scheme automatically.

Target platform: **IntelliJ IDEA 2026.3** (`sinceBuild = 263`, no `untilBuild`).

## Variants

| Theme | Appearance | Base background |
| --- | --- | --- |
| Tokyo Night | dark | `#1a1b26` |
| Tokyo Night Storm | dark | `#24283b` |
| Tokyo Night Moon | dark | `#222436` |
| Tokyo Night Light | light | `#d5d6db` |

## How it works

The upstream Zed palette JSON is the single source of truth. A stdlib-only
Python generator reads the pinned copy at `tools/vendor/tokyo-night.json` and
emits every resource file. **Generated outputs are committed**, so building the
plugin does not require Python.

```
tools/vendor/tokyo-night.json   pinned upstream palette (source of truth)
tools/generate.py               generator (stdlib only)
tools/mappings/*.py             Zed -> IntelliJ key mappings per subsystem
src/main/resources/themes/*     generated theme.json + xml (committed)
```

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

## Install from disk

1. Settings > Plugins > (gear) > Install Plugin from Disk...
2. Select `build/distributions/tokyo-night-intellij-<version>.zip`.
3. Restart, then choose a theme under Settings > Appearance & Behavior > Appearance.

## Regenerate resources

After editing the generator or its mappings:

```bash
uv run tools/generate.py
```

Re-commit the changed files under `src/main/resources/themes/`. Never hand-edit
generated files - see [`CLAUDE.md`](CLAUDE.md).

## Contributing

Project conventions and agent guidance live in [`CLAUDE.md`](CLAUDE.md) and
[`AGENTS.md`](AGENTS.md). The plan of record is [`plan.md`](plan.md).

## License

MIT. See [`LICENSE`](LICENSE), which also records upstream attribution.
