---
name: update
description: Mid-session checkpoint — append progress to today's session log and update state files if a priority shifted, without ending the session.
disable-model-invocation: true
---

# /update — Quick Checkpoint

Save progress mid-session without closing. Fast and low-ceremony: a log line plus a state
touch only if something actually changed.

**Invocation:** user-only (`disable-model-invocation: true`) — checkpoints are timed by
you, and the flag keeps this skill out of ambient context.

## Configuration

Read the optional `workspace.yaml` at the project root. Below, `<state_dir>` and
`<sessions_dir>` are its resolved values; defaults are `state/` and `sessions/`. Full
reference: `docs/state-model.md`.

## Instructions

1. **Scan recent conversation.** Identify in ~30 seconds: what was worked on, any decisions
   made, any state changes needed.

2. **Append to session log.** Add to `<sessions_dir>/{TODAY}.md` (create it if absent):
   ```markdown
   ## Update: {TIME}
   - {what was worked on, 1–3 bullets max}
   ```

3. **Update state only if something changed.** Touch `<state_dir>/current.md` only if a
   priority shifted, a thread opened or closed, or a task completed. Skip otherwise — an
   `/update` with no real change writes only the log line.

4. **Confirm.** One line: "Checkpointed: {brief description}".

## Design principles

- **Fast.** A checkpoint should cost seconds, not minutes.
- **Skip what's clean.** Don't rewrite `current.md` for a checkpoint that changed nothing.
- **Standing rule.** Whenever you run `/update`, log first, then decide whether state
  actually moved — don't invent a state change to justify the run.
