# The Zed palette JSON is the single source of truth; generated resources are committed

The upstream Zed theme file (`themes/tokyo-night.json` from
`ssaunderss/zed-tokyo-night`) defines all four variants in one document. We treat
it as the authoritative color source: a pinned copy lives at
`tools/vendor/tokyo-night.json`, and a stdlib-only Python generator
(`tools/generate.py`) emits every IntelliJ resource from it.

We chose a generator over hand-authored resources because the surface is wide and
repetitive - four variants x (UI theme + editor scheme) - and the variants share
a key set but diverge in values, so hand-editing invites drift. A generator makes
the mapping auditable and regeneration deterministic.

We chose to **commit the generated outputs** rather than generate at build time.
The build then needs no Python toolchain, `./gradlew buildPlugin` works from a
clean checkout, and changes to generated colors are reviewable as ordinary
diffs. The cost is that regeneration must be checked for drift, which the
`mise run check` gate does.

## Consequences

- Never hand-edit anything under `src/main/resources/themes/`; edit the generator
  or its mappings and regenerate.
- `mise run check` fails if regenerating produces a diff against the committed
  outputs.
- Upstream quirks (a missing `#`, keys absent in some variants) are normalized in
  the generator as explicit "quirk fixes", not silently absorbed.

Status: accepted
