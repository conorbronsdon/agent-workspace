---
name: today
description: Morning heartbeat — staleness checks, deadline surfacing, and memory curation for your workspace state. Run at the start of each day or after a 12+ hour gap.
disable-model-invocation: true
---

# /today — Morning Heartbeat

A daily check-in that catches staleness, surfaces deadlines, and proposes updates —
including gaps left by sessions that closed without `/end`. Designed to run in under 60
seconds.

**Invocation:** user-only (`disable-model-invocation: true`) — the heartbeat is timed by
you (mornings, or after a gap), and the flag keeps this skill out of ambient context.

## Configuration

Read the optional `workspace.yaml` at the project root. Below, `<state_dir>`,
`<sessions_dir>`, and `<task_file>` are its resolved values; defaults are `state/`,
`sessions/`, and `TODO.md`. Staleness thresholds come from `staleness.current_days` (3),
`weekly_days` (5), `blockers_days` (7). Full reference: `docs/state-model.md`.

## Instructions

1. **Establish context.** Get today's date. Read `<state_dir>/heartbeat-log.md` to find the
   last check-in date.

2. **Scan recent activity.** In a git repository, run:
   ```bash
   git log --oneline --since="3 days ago"
   ```
   Then check `<sessions_dir>` for recent logs. This captures work even from sessions that
   closed without `/end`. Outside a git repository, rely on the session logs alone.

3. **Check state freshness.** Same thresholds as `start` step 4 (`staleness.*` from config).

4. **Surface deadlines.** Read `<task_file>` and scan for:
   - Items with dates in the next 7 days
   - Items marked urgent or time-sensitive

5. **Age-check open items.** Read `<state_dir>/current.md` and check the `*(created M/D)*`
   dates on open threads:
   - Items >7 days old: flag as "stale — still relevant?"
   - Items >14 days old: escalate as "likely stale — remove or convert to task?"
   Present proposals. **Do not auto-update.**

6. **Identify memory gaps.** Compare git-log activity against state files:
   - Decisions committed but not in `<state_dir>/decisions.md`?
   - Completed work not reflected in `<state_dir>/current.md`?
   List proposed updates. **Do not auto-update. Wait for approval.**

7. **Output format:**
   ```
   MORNING CHECK-IN — [DATE] ([day of week])
   Last heartbeat: [date] ([N] days ago)

   SINCE LAST CHECK-IN:
   - [N] commits: [brief themes]
   - Session logs: [found/none]

   STATE:
   - current.md — [fresh/N days stale]
   - weekly-priorities.md — [fresh/N days stale]
   - blockers.md — [fresh/N days stale]

   DEADLINES (next 7 days):
   - [items, most urgent first]

   [If stale items found:]
   STALE ITEMS:
   - [item] — [N] days old. [Propose: remove / convert to task]

   [If memory gaps found:]
   MEMORY GAPS:
   - [proposed update]
   ```

8. **Log the heartbeat.** Append to `<state_dir>/heartbeat-log.md`:
   ```markdown
   ## [DATE]
   - Commits since last: [N]
   - State staleness: [summary]
   - Deadlines flagged: [count]
   - Stale items flagged: [count]
   - Memory gaps found: [count]
   - Updates applied: [list or "none — awaiting response"]
   ```

9. **Transition.** Ask: "What's the focus today?"

## Design principles

- **Fast.** Under 60 seconds. If it's slow, it won't get used.
- **Propose, don't act.** Never silently edit state or write memory during the heartbeat.
- **Skip what's clean.** All fresh and no near deadlines → say so in one line.
- **Graceful degradation.** A session that closed without `/end` is caught here; missing
  files are noted, not fatal.
