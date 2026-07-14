---
name: end
description: Close a work session — log what happened, update state and the decision log, propose durable memory updates, and check for uncommitted or unpushed work.
disable-model-invocation: true
---

# /end — Close Session

Capture the session and leave state ready for the next one: a session log, state updates,
a decision-log append, memory proposals, and a git safety check.

**Invocation:** user-only (`disable-model-invocation: true`) — session close is timed by
you, and the flag keeps this skill out of ambient context.

## Configuration

Read the optional `workspace.yaml` at the project root. Below, `<state_dir>` and
`<sessions_dir>` are its resolved values; defaults are `state/` and `sessions/`. Full
reference: `docs/state-model.md`, including the `Last Updated` chain protocol and the
decision-log schema used in steps 3–4.

## Instructions

1. **Auto-extract session summary.** Scan the full conversation and extract:
   - **Topics covered** — what was worked on
   - **Decisions made** — anything concluded or chosen, with rationale
   - **Rejected alternatives** — for each meaningful decision, what else was considered and
     why it lost. If a bug was fixed, note the wrong theory tried first. If an approach
     changed mid-session, capture the pivot. This is the failed-hypothesis record that
     keeps a future session from repeating the same wrong starting point.
   - **State changes** — priorities that shifted, threads that opened or closed
   - **Open threads** — unfinished items or things waiting on someone
   - **Next actions** — what needs to happen next session

   Present the summary for quick confirmation before writing.

2. **Write session log.** Append to `<sessions_dir>/{TODAY}.md`:
   ```markdown
   ## Session: {TIME}

   ### Topics
   - {topic}

   ### Decisions
   - {decision}

   ### Open Threads
   - {thread}

   ### Next Actions
   - {action}
   ```

3. **Update state files:**
   - **Always update `current.md`:** add new threads, remove completed items, refresh
     timestamps on touched items.
   - **Roll the `Last Updated` line through `current-log.md` (chain protocol).** Keep
     exactly one `**Last Updated:**` line at the top of `current.md`, the newest. Never
     stack extra lines and never build a single-line "previous-entry" chain — that breaks
     the Read tool, breaks `grep`, and splices parallel-session merges into single-line
     conflicts. Instead:
     1. Read the existing `**Last Updated:**` line from `current.md`.
     2. Prepend it as its own line at the top of `<state_dir>/current-log.md`, directly
        under the file header, newest first. Create the file with a
        `# current.md update log` header if it does not exist.
     3. Replace the `**Last Updated:**` line in `current.md` with today's entry.

     One entry per line keeps history append-only and merges line-based.
   - **Update `blockers.md` if needed:** add new dependencies, move resolved blockers to
     "Recently Unblocked."
   - **Update `weekly-priorities.md` if needed:** check off completed items. Only touch it
     if meaningful progress was made.

4. **Update the decision log.** If decisions were made, append to
   `<state_dir>/decisions.md`:
   ```markdown
   | {TODAY} | {decision} | {context / rationale} | {rejected alternatives} |
   ```
   Only log decisions future sessions need: source-of-truth changes, strategy pivots, scope
   calls, tool or process choices. Skip trivial ones. Fill the **rejected alternatives**
   column when there was a real branch point — what else was considered and why it lost;
   leave it blank when there was one obvious option.

5. **Propose auto-memory updates.** Beyond state files, scan the session for durable
   patterns worth preserving across *every* conversation in this project. If the agent
   auto-loads a project `MEMORY.md`, anything saved there compounds.

   Propose 0–2 additions. Good candidates: environment quirks or tool behaviors confirmed
   this session, workflow preferences the user stated ("always X", "never Y"), debugging
   fixes that will recur, stable facts about projects or people. Skip: today's work (that's
   the session log), anything already in `CLAUDE.md` or state files, and unverified
   single-observation conclusions.

   **Friction-point check:** before proposing, ask — *was there a friction point this
   session that a memory entry would have prevented?* A tool you had to re-learn, an error
   you had hit before, a convention you had to re-infer. If yes, write the entry; repeating
   a mistake is a system failure, so turn it into a durable rule.

   Present proposals inline and wait for approval — never write to memory automatically:
   ```
   MEMORY PROPOSALS:
   - [proposed addition]
   (Reply "save" to apply, or skip)
   ```
   If nothing qualifies, skip silently.

6. **Quick drift check (if parallel sessions ran).** In a git repository, run
   `git log --oneline --all --since="6 hours ago"` to catch commits from sessions working
   in parallel.
   - If any of those commits touched files this session also edited, flag the potential
     conflict: "Parallel session also edited [file], check for conflicts." Wait for the
     user before fixing anything.
   - If none are found, skip silently — do not mention this step.
   - This is a fast spot-check, not a full reconcile (see the `reconcile` skill for that).
   - Outside a git repository, skip this step.

7. **Git safety check (do not skip).** In a git repository, run `git status` and check for
   uncommitted or unpushed work:
   - Uncommitted changes? Show the files and ask whether to commit.
   - Unpushed commits? Show the count and ask whether to push.
   - Clean and pushed? Skip silently.
   - Outside a git repository, skip this step.

8. **Confirm.** Two-line summary: what was logged, and the top open thread or next action.
   If memory proposals are awaiting a save/skip reply, note that.

## Design principles

- **Propose, don't act.** State updates are confirmed; memory is never written without a
  "save"; commits and pushes need explicit approval.
- **Standing rule.** Every `/end` runs steps 1–8 in order; the chain protocol in step 3 is
  how the timestamp always rolls — never append a second `Last Updated` line as a shortcut.
