# Frame spec for the agent-workspace demo GIF.
# Rendered by scripts/render_demo.py (canonical path: demo.tape via vhs).
#
# This is a SIMULATED Claude Code session, not captured command output — the
# skills are agent instructions, not scripts, so there is no real stdout to
# capture. The briefing/summary content mirrors what skills/start/SKILL.md and
# skills/end/SKILL.md actually instruct: /start reads state, flags staleness,
# surfaces top priorities and asks "What's the focus today?"; /end extracts a
# session summary (topics, decisions, rejected alternatives, next actions).

TITLE = "agent-workspace — simulated /start + /end"

FRAMES = [
    ("out", [
        [("# Simulated Claude Code session. /start and /end are agent skills, not", "dim")],
        [("# scripts — this shows the briefing and summary they produce, not stdout.", "dim")],
    ], 2000),

    ("cmd", "/start"),
    ("out", [
        "",
        [("  Monday, 2026-07-13", "cyan")],
        [("  State: ", "fg"), ("current.md fresh", "green"), ("  ·  ", "dim"),
         ("weekly-priorities.md 6d old — stale", "yellow")],
        [("  Changed since last session: ", "dim"), ("state/decisions.md, TODO.md", "fg")],
        "",
        [("  Top priorities (from current.md):", "fg")],
        [("    1. Ship the drift-auditor pre-commit hook", "fg")],
        [("    2. Draft the season-3 guest outreach", "fg")],
        [("    3. Reconcile the two parallel worktrees", "fg")],
        "",
        [("  ⚠ 1 overdue in TODO.md · 2 files in inbox/ to triage", "yellow")],
        "",
        [("  What's the focus today?", "green")],
    ], 3600),

    ("clear",),
    ("out", [
        [("# ...work happens... then close the session:", "dim")],
    ], 1500),
    ("cmd", "/end"),
    ("out", [
        "",
        [("  Session summary (confirm before writing):", "cyan")],
        "",
        [("  Topics", "magenta")],
        [("    - Wired the pre-commit hook to ssot_check.py; added a CI job", "fg")],
        "",
        [("  Decisions", "magenta")],
        [("    - Hook runs check (not discover) so it stays deterministic in CI", "fg")],
        [("      rejected: fuzzy discover in CI — too noisy, non-reproducible", "dim")],
        "",
        [("  Next actions", "magenta")],
        [("    - Backfill .ssot.yaml for the media-kit copies", "fg")],
        "",
        [("  Will write: sessions/2026-07-13.md · roll current.md · +1 decision", "dim")],
        [("  Git: ", "fg"), ("2 uncommitted files", "yellow"), (" — commit them? (y/n)", "fg")],
    ], 3800),
]
