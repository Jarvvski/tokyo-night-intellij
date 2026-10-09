# PRD: Tokyo Night theme plugin for IntelliJ IDEA

The full plan of record is [`plan.md`](../../plan.md) at the repo root. This PRD
is the working index for the implementation tickets under `issues/`.

## Summary

Port all four variants of the Zed theme `ssaunderss/zed-tokyo-night` (Tokyo
Night, Storm, Moon, Light) to a theme-only IntelliJ plugin targeting IDEA 2026.3
(build 263). A stdlib-only Python generator reads a pinned upstream palette and
emits committed resources.

## Locked decisions

See `docs/adr/`:

- ADR-0001 - palette JSON is the source of truth; generated resources committed.
- ADR-0002 - two color systems -> two artifacts per variant.
- ADR-0003 - inherit Islands; target the 2026.3 (263) EAP line.
- ADR-0004 - theme-only plugin; no application code.

## Bootstrap status (done)

The repo scaffold is in place and builds:

- jj colocated repo, agent docs (`AGENTS.md`, `CONTEXT.md`, `docs/`), skills.
- Kotlin DSL Gradle build on IPGP 2.19.0 / Kotlin 2.4.21 / JDK 21.
- Pinned upstream palette at `tools/vendor/tokyo-night.json`.
- Minimal generator (`tools/generate.py`, supports `--check`) emitting structurally
  valid stub themes so `buildPlugin` succeeds today.
- `mise run check` = generator drift check + `buildPlugin`.

## Tickets

| # | Ticket | Blocked by |
| --- | --- | --- |
| 01 | Phase 0 - attribute-id harvest | - |
| 02 | Generator core | - |
| 03 | Mapping modules | - |
| 04a | Editor scheme chrome | 02, 03 |
| 04b | Syntax attributes | 02, 03, 01 |
| 04c | Diff / VCS | 02, 03 |
| 04d | Terminal ANSI | 02, 03 |
| 05 | Packaging & registration | 04a-d |
| 06 | Build & acceptance verification | all |

## Gate

`mise run check` must be green (generator produces no diff; `buildPlugin`
succeeds) before any ticket is resolved.
