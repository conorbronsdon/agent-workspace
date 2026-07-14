# Changelog

## 0.1.0 — 2026-07-13

Initial release. Consolidates the workspace-lifecycle skills that graduated from
[claude-code-skills](https://github.com/conorbronsdon/claude-code-skills): the bundled
`session-management` skill split into per-command skills, plus `reconcile` and `recover`.

- `skills/start`, `skills/update`, `skills/end`, `skills/today` — the session lifecycle,
  each `disable-model-invocation: true` (user-timed, zero ambient context). Carries the full
  rule set: the `Last Updated` chain protocol, the decision-log rejected-alternatives
  column, memory-proposal friction check, and the `/end` git safety check.
- `skills/reconcile`, `skills/recover` — read-only, model-invocable hygiene scans with
  approval-gated fixes. Includes the hardened default-branch detection, intent-over-recency
  drift rule, and unknown-activity classification for possibly-live worktrees.
- Configurable state layout via an optional `workspace.yaml` (`state_dir`, `sessions_dir`,
  `task_files`, staleness thresholds); documented in the README and `docs/state-model.md`.
  Skills default to `state/`, `sessions/`, `TODO.md` when absent.
- `templates/` — starter `current.md`, `decisions.md`, `weekly-priorities.md`,
  `blockers.md`.
- `docs/state-model.md` — the shared state model, referenced by every skill.
- `scripts/validate_skill.py` (vendored from agent-skill-builder @ 1337c4f) + `test` CI that
  validates all `skills/*`.
