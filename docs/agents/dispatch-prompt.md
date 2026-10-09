You are picking up work in the tokyo-night-intellij repo at
/Users/jarvis/Code/personal/tokyo-night-intellij. Work autonomously through ONE
ticket end to end; derive everything from this repo's own docs - do not wait for
me to restate anything.

Read before anything else:
- AGENTS.md
- CONTEXT.md
- docs/agents/ticket-workflow.md   (the process you must follow)
- docs/agents/issue-tracker.md     (ticket conventions)
- .scratch/tokyo-night/PRD.md      (ticket index + gate)
- .scratch/tokyo-night/issues/*    (the tickets)

Selection:
1. List .scratch/tokyo-night/issues/. A ticket is eligible when its Status is not
   `resolved` and every path named on its `Blocked by:` line is resolved.
2. Pick the lowest-numbered eligible ticket; if several are eligible note the
   others but take only this one. If none are eligible, report that and stop.
3. Claim it (set `Status: claimed`) before editing anything.

Plan phase (you are in plan mode):
- Read the chosen ticket in full, plus the code/mappings it touches and the
  relevant plan.md phase.
- Produce a concise plan covering EVERY acceptance criterion and every
  `## Commits` item; name the exact files you will change; flag any ADR conflict
  rather than silently overriding it.
- Present that plan. Once approved (or if told to proceed), treat approval as
  blanket for the whole ticket and execute without further check-ins except for a
  hard blocker or a required human decision.

Execute phase:
- Follow docs/agents/ticket-workflow.md exactly: scope is the entire ticket;
  keep repo invariants (never hand-edit src/main/resources/themes/, drive values
  from tools/vendor/tokyo-night.json, stdlib-only Python via uv); never invoke git.
- Gate must pass before landing:
    uv run tools/generate.py && uv run tools/generate.py --check && mise run check
- Land locally with jj only:
    jj describe -m "<imperative one-liner>" && jj bookmark set main --to @ && jj new
  Do NOT push unless I explicitly say push.
- Set the ticket Status to `resolved` only after the gate passes.
- Bump gradle.properties version + CHANGELOG only if the change is user-visible.

Report at the end: chosen ticket; files changed; decisions or accepted
approximations; exact gate result; confirmation main moved; and which tickets are
now unblocked next.
