# State Model

The shared vocabulary for the workspace-lifecycle skills (`start`, `update`, `end`,
`today`) and the hygiene skills (`reconcile`, `recover`). Each skill references this
document for the concepts below instead of redefining them.

## Configuration — `workspace.yaml`

The skills read an optional `workspace.yaml` at the **project root** to learn where
state lives and how aggressively to flag staleness. When the file is absent, or a key
is missing, the defaults below apply — so a fresh project works with zero config.

```yaml
# workspace.yaml — every key is optional; shown values are the defaults
state_dir: state/            # directory holding the state files below
sessions_dir: sessions/      # directory holding dated session logs
task_files: TODO.md          # file (or list of files) scanned for deadlines/overdue items
staleness:
  current_days: 3            # flag current.md when older than this
  weekly_days: 5             # flag weekly-priorities.md when older than this
  blockers_days: 7           # flag blockers.md when older than this
```

`task_files` accepts a single path or a YAML list:

```yaml
task_files:
  - TODO.md
  - planning/roadmap.md
```

Throughout the skills, `<state_dir>`, `<sessions_dir>`, and `<task_file>` mean the
resolved config values (or their defaults). Skills never hardcode `state/` or `TODO.md`.

## State files

All paths are relative to `<state_dir>` unless noted. Files marked *(auto-created)* are
created on first write by the skill that owns them — you do not need to pre-make them.

| File | Holds | Written by |
|------|-------|-----------|
| `current.md` | Active priorities, open threads, recent context | `start` reads; `update`/`end` write |
| `current-log.md` *(auto-created)* | History of past `Last Updated` lines, newest first | `end` |
| `decisions.md` | Decision log: date, decision, rationale, rejected alternatives | `end` appends |
| `weekly-priorities.md` | What matters this week | `end` checks off items |
| `blockers.md` | Things waiting on external dependencies | `end` updates |
| `heartbeat-log.md` *(auto-created)* | Record of `today` check-ins | `today` |
| `<sessions_dir>/{YYYY-MM-DD}.md` *(auto-created)* | Daily session logs | `update`/`end` append |

Starter versions of `current.md`, `decisions.md`, `weekly-priorities.md`, and
`blockers.md` live in `templates/` — copy them into `<state_dir>` to bootstrap.

## The `Last Updated` chain protocol

`current.md` carries exactly **one** `**Last Updated:**` line at the top — the newest.
Never stack extra `**Last Updated:**` lines, and never extend one line with a
"previous-entry" chain: that pattern breaks the Read tool, breaks `grep`, and turns
parallel-session merges into spliced single-line conflicts. To roll the timestamp:

1. Read the existing `**Last Updated:**` line from `current.md`.
2. Prepend it as its own line at the top of `<state_dir>/current-log.md`, directly under
   the file header, newest first. Create the file with a `# current.md update log`
   header if it does not exist.
3. Replace the `**Last Updated:**` line in `current.md` with today's new entry.

One entry per line keeps history append-only and merge conflicts line-based: two parallel
sessions both prepending produce a trivial both-lines merge instead of one clobbered line.

## The decision log & the rejected-alternatives column

`decisions.md` is a table: `| Date | Decision | Context / Rationale | Rejected Alternatives |`.

The last column is the **failed-hypothesis record**. Fill it whenever there was a real
branch point: what else was considered and why it lost. If a bug was fixed, note the wrong
theory tried first. If an approach changed mid-session, capture the pivot. Leave it blank
only when there was one obvious option. Capturing the non-chosen paths lets a future
session audit the reasoning, not just the outcome, and avoid re-litigating a settled path.

Only log decisions a future session needs: source-of-truth changes, strategy pivots, scope
calls, tool/process choices. Skip trivial ones.

## Staleness thresholds

`start` and `today` flag state files older than their configured threshold
(`staleness.current_days` / `weekly_days` / `blockers_days`). These measure **state-file
freshness**. Separately, `today` age-checks **open items** inside `current.md` by their
`*(created M/D)*` dates: >7 days → "stale, still relevant?"; >14 days → "likely stale,
remove or convert to a task?". Those open-item ages are fixed, not config keys.

## Default-branch detection

The hygiene skills never assume `main`. Resolve the default branch once and use it
everywhere:

```bash
DEFAULT=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
DEFAULT=${DEFAULT:-$(git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p')}
DEFAULT=${DEFAULT:-main}   # no remote at all — fall back and note it in the report
```

## Behavior outside a git repository

Several steps run `git log` / `git worktree`. When the project is not a git repo, those
steps are skipped, not errors:

```bash
git rev-parse --git-dir >/dev/null 2>&1 || { echo "not a git repository"; }
```

- `start` / `today` skip the "what changed since last session" git scan and continue with
  file-based freshness and deadline checks.
- `reconcile` / `recover` print "not a git repository — nothing to reconcile/recover" and
  exit cleanly. Their file-consistency and SSOT checks (reconcile) still run if state files
  exist.

## Design principles (shared)

- **Propose, don't act.** State and memory updates are presented for confirmation. Hygiene
  fixes are proposed individually and applied only on approval. Never silently edit state.
- **Skip what's clean.** If everything is fresh, say so in one line.
- **Compound over time.** Session and heartbeat logs become an episodic record.
- **Graceful degradation.** Missing files get created on write; a session that closed
  without `end` is caught by `today`. Nothing is catastrophic.
