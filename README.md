# Tokyo Night for IntelliJ IDEA

<div align="center">
  <a href="https://plugins.jetbrains.com/plugin/35030">
    <img src="screenshots/logo.svg" width="160" alt="Tokyo Night logo">
  </a>
</div>

[![Install from JetBrains Marketplace](https://img.shields.io/badge/JetBrains%20Marketplace-install-blue?logo=jetbrains&logoColor=white)](https://plugins.jetbrains.com/plugin/35030)

![Tokyo Night](screenshots/tokyo-night.png)

Tokyo Night is a theme plugin for IntelliJ IDEA. It ports the four variants of
the Zed theme
[`ssaunderss/zed-tokyo-night`](https://github.com/ssaunderss/zed-tokyo-night):
**Tokyo Night**, **Tokyo Night Storm**, **Tokyo Night Moon**, and **Tokyo Night
Light**.

Each variant themes the whole IDE: window chrome, syntax highlighting, terminal
ANSI colors, and diff/VCS colors. Selecting one also applies its matching editor
scheme.

It works on IntelliJ IDEA 2026.2 and later.

## Install

From the IDE: **Settings > Plugins > Marketplace**, search for Tokyo Night,
install, restart, then pick a variant under **Settings > Appearance & Behavior >
Appearance**.

The plugin page is <https://plugins.jetbrains.com/plugin/35030>. Every release is
also a signed zip on the
[Releases](https://github.com/Jarvvski/tokyo-night-intellij/releases) page, and you
can install one from disk via **Settings > Plugins > gear > Install Plugin from
Disk**.

## Variants

| Theme | Appearance | Base background |
| --- | --- | --- |
| Tokyo Night | dark | `#1a1b26` |
| Tokyo Night Storm | dark | `#24283b` |
| Tokyo Night Moon | dark | `#222436` |
| Tokyo Night Light | light | `#d5d6db` |

## Screenshots

The default variant is shown at the top. The other three:

<details>
<summary>Tokyo Night Storm</summary>

![Tokyo Night Storm](screenshots/tokyo-night-storm.png)

</details>

<details>
<summary>Tokyo Night Moon</summary>

![Tokyo Night Moon](screenshots/tokyo-night-moon.png)

</details>

<details>
<summary>Tokyo Night Light</summary>

![Tokyo Night Light](screenshots/tokyo-night-light.png)

</details>

## Spotifast

The same four variants are also emitted as [Spotifast](https://spotifast.rocks)
custom palettes, driven by the same pinned Zed palette. The generator writes
them to `dist/spotifast/`, and `mise run spotifast-install` copies them into
Spotifast's themes folder and reloads them (no restart needed).

`dist/spotifast/Tokyo Night.json` intentionally replaces the palette Spotifast
ships under that name.

## Development

How the generator works, and how to build, regenerate and capture screenshots:
[docs/development.md](docs/development.md).

Cutting a release: [docs/releasing.md](docs/releasing.md).

Conventions and agent guidance are in [`CLAUDE.md`](CLAUDE.md) and
[`AGENTS.md`](AGENTS.md); the plan of record is [`plan.md`](plan.md).

## License

MIT. See [`LICENSE`](LICENSE), which also records upstream attribution.
