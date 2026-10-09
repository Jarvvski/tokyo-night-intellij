# Build & acceptance verification

Status: ready-for-agent

Blocked by: 01, 02, 03, 04a, 04b, 04c, 04d, 05

## Background

Automated verification stops at "it builds". Visual acceptance is manual and is
the final gate before declaring the port done.

## Scope

1. `./gradlew buildPlugin` -> confirm artifact at
   `build/distributions/<name>-<version>.zip`.
2. Install via Settings > Plugins > Install Plugin from Disk on IDEA **2026.3
   EAP**; restart; select each of the four themes and confirm its editor scheme
   auto-applies.
3. Per-variant checklist against upstream screenshots:
   - chrome backgrounds/borders look native under Islands;
   - tabs/status/tool windows correct;
   - syntax roles match family colors;
   - diffs/VCS colors correct in the Git tool window;
   - terminal ANSI correct in BOTH classic Run console and block Terminal tool
     window;
   - Light variant legible with correct contrast.
4. Read `idea.log` for unresolved-key warnings; fix before declaring done.
5. Optionally run the Plugin Verifier task once.

## Acceptance criteria

- [ ] All four variants verified visually per checklist.
- [ ] No unresolved-key warnings in idea.log.
- [ ] Any accepted approximation documented (Zed key with no IntelliJ equivalent).
- [ ] `mise run check` green.
