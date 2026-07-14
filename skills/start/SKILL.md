---
name: start
description: Load project state and get a briefing at the start of a work session — reads state files, flags staleness, surfaces top priorities, deadlines, and blockers.
disable-model-invocation: true
---

# /start — Begin Session

Load your workspace state so the session begins where the last one left off, then give a
short briefing. User-timed, so nothing runs ambiently.

**Invocation:** user-only (`disable-model-invocation: true`) — you decide when a session
starts, and the flag keeps this skill out of ambient context.

## Configuration

Read the optional `workspace.yaml` at the project root. Below, `<state_dir>`,
`<sessions_dir>`, and `<task_file>` are its resolved values; defaults are `state/`,
`sessions/`, and `TODO.md`. Staleness thresholds come from `staleness.current_days` (3),
`weekly_days` (5), `blockers_days` (7). Full reference: `docs/state-model.md`.

## Instructions

1. **Get today's date.** Run `date +%Y-%m-%d`. Note the day of week.

2. **Check what changed since last session.** If this is a git repository, find the most
   recent session log in `<sessions_dir>` and run:
   ```bash
   git log --oneline --since="<last session date>"
   ```
   Flag any state or context files modified since the last session — they may hold updates
   from other sessions or manual edits. If not a git repository
   (`git rev-parse --git-dir` fails), skip this step and continue.

3. **Load context (read in order):**
   - `<state_dir>/current.md` — active priorities, open threads
   - `<state_dir>/decisions.md` — scan the last 5 entries for awareness
   - `<state_dir>/weekly-priorities.md` — what matters this week
   - `<state_dir>/blockers.md` — things waiting on dependencies
   - `<sessions_dir>/{TODAY}.md` — if it exists, you are resuming today

4. **Health checks.** Flag anything that needs attention; skip silently if all clean:
   - `current.md` older than `staleness.current_days` — flag it
   - `weekly-priorities.md` older than `staleness.weekly_days` — flag it
   - `blockers.md` older than `staleness.blockers_days` — flag it
   - **Inbox:** if the project keeps a drop-zone (e.g. `inbox/`) and it holds files, note
     the count and suggest triaging them
   - **Overdue items:** scan `<task_file>` for unchecked items with a date that has passed

5. **Give a briefing.** Keep it short:
   - Date and day of week
   - State freshness (one line if all fresh, individual flags if stale)
   - Files changed since last session
   - Top 2–3 priorities from `current.md`
   - Any time-sensitive open threads
   - Any blockers worth flagging
   - Ask: "What's the focus today?"

   If resuming today's session, acknowledge what was already covered.

## Design principles

- **Fast.** Under 60 seconds. If it's slow, it won't get used.
- **Skip what's clean.** All fresh, no near deadlines → say so in one line.
- **Graceful degradation.** If state files don't exist yet, note it and point to
  `templates/`; outside a git repo, run the file-based checks only.
