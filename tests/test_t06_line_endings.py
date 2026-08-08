"""T6 - the LF pin holds: no CRLF in tracked text files, .gitattributes present.

Source: E16-2 (no .gitattributes existed, core.autocrlf=true, 17 text files
carried CRLF; the pin ratified the LF state the record already was, both
index-side and worktree-side, with db/png/npy/glb marked binary).

The check is git's own accounting - `git ls-files --eol` reports the index
and worktree line endings per tracked file - not a re-scan that could drift
from what git enforces. Files git treats as binary report `-text` and carry
no eol; everything else must be lf on both sides.
"""
import subprocess

from conftest import REPO


def _git(args):
    p = subprocess.run(["git"] + args, cwd=str(REPO), capture_output=True)
    assert p.returncode == 0, "git %s failed: %s" % (args, p.stderr.decode("utf-8", "replace"))
    return p.stdout.decode("utf-8", "replace")


def test_t06_gitattributes_present_and_pinning():
    tracked = _git(["ls-files", "--", ".gitattributes"]).strip()
    assert tracked == ".gitattributes", ".gitattributes is not tracked"
    body = (REPO / ".gitattributes").read_text(encoding="utf-8")
    assert "* text=auto eol=lf" in body, (
        "the catch-all LF pin is missing from .gitattributes:\n%s" % body)


def test_t06_no_crlf_in_tracked_text_files():
    out = _git(["ls-files", "--eol"])
    rows = [ln for ln in out.splitlines() if ln.strip()]
    # the check must be able to fail: prove it is looking at real rows
    assert len(rows) > 100, "ls-files --eol returned %d rows - parsing broke" % len(rows)
    assert any(ln.split("\t")[-1] == "tools/facet_index.py" for ln in rows), (
        "known tracked file missing from ls-files output - parsing broke")
    offenders = []
    for ln in rows:
        attrs, path = ln.split("\t", 1)
        fields = attrs.split()
        index_eol = fields[0]    # i/<eol>
        work_eol = fields[1]     # w/<eol>
        if index_eol == "i/crlf" or index_eol == "i/mixed":
            offenders.append("%s (index %s)" % (path, index_eol))
        if work_eol == "w/crlf" or work_eol == "w/mixed":
            offenders.append("%s (worktree %s)" % (path, work_eol))
    assert not offenders, "CRLF in tracked text files:\n  " + "\n  ".join(offenders)
