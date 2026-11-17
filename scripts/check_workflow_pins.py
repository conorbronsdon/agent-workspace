#!/usr/bin/env python3
"""Check GitHub Actions supply-chain hardening. Stdlib only.

Run from anywhere: python3 scripts/check_workflow_pins.py
Exit 0 when every check passes, 1 otherwise.

Checks:
- every `uses:` in .github/workflows/* and .github/actions/** is pinned to a
  full 40-character commit SHA (local `./` actions and `docker://` are exempt);
- every workflow sets a top-level `permissions:` key;
- .github/dependabot.yml watches the `github-actions` ecosystem.

Each run first self-tests the parser (a tag, a short SHA and a branch ref must
be flagged; a full SHA pin and a local action must not), so a parser that
stopped matching cannot pass silently.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USES = re.compile(r"""^\s*(?:-\s+)?uses:\s*["']?([^\s"'#]+)""")
FULL_SHA = re.compile(r"@[0-9a-f]{40}$")


def unpinned_uses(text):
    bad = []
    for line in text.replace("\r\n", "\n").split("\n"):
        m = USES.match(line)
        if not m:
            continue
        ref = m.group(1)
        if ref.startswith("./") or ref.startswith("docker://"):
            continue
        if not FULL_SHA.search(ref):
            bad.append(ref)
    return bad


def has_top_level_permissions(text):
    return re.search(r"^permissions:", text, re.M) is not None


def self_test():
    errors = []
    sha = "11d5960a326750d5838078e36cf38b85af677262"
    must_fire = {
        "tag": "      - uses: actions/checkout@v4\n",
        "short SHA": "      - uses: actions/checkout@11d5960\n",
        "branch": "        uses: actions/setup-node@main\n",
    }
    for name, line in must_fire.items():
        if not unpinned_uses(line):
            errors.append("self-test: parser missed a %s ref" % name)
    must_not_fire = (
        "      - uses: actions/checkout@%s # v4.4.0\n" % sha
        + "      - uses: ./.github/actions/local\n"
        + "      - uses: docker://alpine:3.20\n"
    )
    if unpinned_uses(must_not_fire):
        errors.append("self-test: parser flagged a full SHA pin or local action")
    if has_top_level_permissions("jobs:\n  a:\n    permissions:\n      contents: read\n"):
        errors.append("self-test: job-level permissions counted as top-level")
    return errors


def main():
    errors = self_test()
    gh = ROOT / ".github"
    workflows = sorted(
        p for p in (gh / "workflows").glob("*") if p.suffix in (".yml", ".yaml")
    )
    if not workflows:
        errors.append("no workflows found under .github/workflows")
    actions = sorted(
        p for p in (gh / "actions").rglob("*") if p.suffix in (".yml", ".yaml")
    ) if (gh / "actions").is_dir() else []
    for path in workflows + actions:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for ref in unpinned_uses(text):
            errors.append("%s: not pinned to a full commit SHA: %s" % (rel, ref))
        if path in workflows and not has_top_level_permissions(text):
            errors.append("%s: no top-level permissions: key" % rel)
    dependabot = gh / "dependabot.yml"
    if not dependabot.is_file() or not re.search(
        r"package-ecosystem:\s*[\"']?github-actions\b",
        dependabot.read_text(encoding="utf-8"),
    ):
        errors.append(".github/dependabot.yml does not watch github-actions")
    for e in errors:
        print("FAIL " + e)
    if errors:
        return 1
    print("ok: %d workflow(s), %d action file(s) pinned; permissions and dependabot set"
          % (len(workflows), len(actions)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
