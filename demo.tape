# demo.tape — canonical vhs recording script for docs/demo.gif
#
# Regenerate with vhs (https://github.com/charmbracelet/vhs):
#     vhs demo.tape
#
# NOTE: /start and /end are agent skills (instructions an AI coding agent
# follows), not shell scripts — there is no real stdout to capture. This tape
# echoes a representative briefing and session summary so the recording is
# reproducible; the content mirrors skills/start/SKILL.md and skills/end/SKILL.md.
# The committed docs/demo.gif is produced by the Pillow fallback renderer, which
# holds the same simulated frames:
#     python3 scripts/render_demo.py      # -> docs/demo.gif

Output docs/demo.gif

Set Shell "bash"
Set FontSize 18
Set Width 1200
Set Height 510
Set Theme "Dracula"
Set Padding 20
Set TypingSpeed 60ms

# --- Beat 1: /start produces a briefing --------------------------------------
Type "# /start  (simulated — the skill reads state and briefs you)"
Enter
Sleep 500ms
Type `cat <<'EOF'
  Monday, 2026-07-13
  State: current.md fresh  ·  weekly-priorities.md 6d old — stale
  Changed since last session: state/decisions.md, TODO.md

  Top priorities (from current.md):
    1. Ship the drift-auditor pre-commit hook
    2. Draft the season-3 guest outreach
    3. Reconcile the two parallel worktrees

  What's the focus today?
EOF`
Enter
Sleep 4s

# --- Beat 2: /end extracts a session summary ---------------------------------
Type "# /end  (simulated — the skill extracts and confirms a summary)"
Enter
Sleep 500ms
Type `cat <<'EOF'
  Session summary (confirm before writing):

  Topics
    - Wired the pre-commit hook to ssot_check.py; added a CI job
  Decisions
    - Hook runs check (not discover) so it stays deterministic in CI
      rejected: fuzzy discover in CI — too noisy, non-reproducible
  Next actions
    - Backfill .ssot.yaml for the media-kit copies

  Git: 2 uncommitted files — commit them? (y/n)
EOF`
Enter
Sleep 4s
