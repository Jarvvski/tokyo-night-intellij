# Ticket Workflow

How an agent takes one ticket from `.scratch/<feature>/issues/` to landed. This
is the generic process; each ticket's Scope and Acceptance criteria are the
specifics.

## 1. Select

A ticket is the unit of execution. Pick the lowest-numbered ticket that is open,
unblocked (`Blocked by:` files are all resolved), and unclaimed - or use the path
or number the owner gives you. Claim it (`Status: claimed`) before editing when
working wayfinding-style; otherwise proceed directly.

## 2. Scope

The entire remaining ticket is this session's scope: satisfy every acceptance
criterion and land each `## Commits` item as its own focused commit. Do not stop
after the first green slice. Stop early only for a hard blocker or a required
human decision.

## 3. Read first

- `AGENTS.md` - landing rules, generated-output rule, toolchain.
- `CONTEXT.md` - domain vocabulary; use these terms in output.
- `plan.md` - the relevant phase for background and constraints.
- The ticket itself - its Scope and Acceptance criteria are authoritative.
- The code/mappings it touches.

If your approach contradicts an ADR in `docs/adr/`, surface it explicitly rather
than silently overriding it.

## 4. Do

Follow the ticket's Scope. Repo-wide invariants always apply:

- Never hand-edit generated outputs under `src/main/resources/themes/`; edit the
  generator or mappings and regenerate.
- Drive values from `tools/vendor/tokyo-night.json`; never assume variants share
  values (Moon diverges from Night/Storm in several roles).
- Python is stdlib-only via uv; Kotlin DSL for any Gradle change.
- Never invoke `git`.

## 5. Gate

Run `mise run check` (generator drift check + `buildPlugin`). It must pass before
landing. If the ticket adds verification (extra commands), run those too. If your
change alters generated output, regenerate and include it in the same commit:

```bash
uv run tools/generate.py          # regenerate resources
uv run tools/generate.py --check  # confirm no further drift
mise run check                    # drift check + buildPlugin (the gate)
```

## 6. Land (jj)

One focused change per commit:

```bash
jj describe -m "<imperative one-liner>"
jj bookmark set main --to @
jj new
```

Invariant: after main moves, run `jj new` so `@` is always an empty commit one
above main.

**Do not push.** The owner handles pushes unless they explicitly tell you to push.
Bump `gradle.properties` version + add a dated `CHANGELOG.md` entry in the same
commit only when the change is user-visible; skip pure internal refactors.

## 7. Report

Return: the ticket path; files changed; key decisions or accepted approximations;
the exact gate result; and confirmation of landing (commit description + that
`main` moved).

---

## Prompt template

Copy this block, replace `<TICKET>` with a ticket path (for example
`.scratch/tokyo-night/issues/02-generator-core.md`) and `<SUMMARY>` with what you
want reported back:

```text
Implement ticket `<TICKET>` in the tokyo-night-intellij repo at
/Users/jarvis/Code/personal/tokyo-night-intellij. The entire remaining ticket is
this session's scope - do not stop after the first slice.

Follow docs/agents/ticket-workflow.md end to end:
1. Read AGENTS.md, CONTEXT.md, plan.md (the relevant phase), <TICKET>, and the
   code/mappings it touches.
2. Satisfy every acceptance criterion in <TICKET>.
3. Keep repo invariants: never hand-edit src/main/resources/themes/, drive values
   from tools/vendor/tokyo-night.json, stdlib-only Python via uv, never invoke git.
4. Gate: uv run tools/generate.py && uv run tools/generate.py --check &&
   mise run check - all must pass before landing.
5. Land locally with jj (describe -> bookmark set main --to @ -> jj new). Do NOT
   push unless explicitly told to. Bump version + CHANGELOG only if user-visible.
6. Report <SUMMARY>: files changed, decisions/approximations, exact gate result,
   and confirmation that main moved.
```
