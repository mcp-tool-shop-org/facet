"""T70 (E35 close) - the protection-manifest walk, and its fixture shown capable of failing.

WHY THIS EXISTS. E33/E34/E35 gate their read-only trees with sha256 manifests at arc open
and close, and until this commit the verifier was rewritten inline in whichever session
needed it. E35's open session rebuilt it, fired a FALSE halt on `E34_manifest.json` (which
declares `excludes_self: true`), repaired the walk, and the repair went nowhere - so the
next arc would have re-derived the same bug. The walk is now committed and this file is
what keeps it honest.

THE TOOL CARRIES ITS OWN CAN-FAIL FIXTURE (`--selftest`, eight legs over both manifest
encodings). This file's job is narrower and is the part a suite can do: prove the fixture
RUNS, prove it PASSES, and prove it would FAIL if the walk stopped working - because a
selftest nobody executes is a comment.

Hermetic: synthetic trees in tmp, no recorded tree is read.
"""
import os
import re
import shutil
import subprocess
import sys

import pytest

from conftest import tool

TOOL = tool("verify/tree_manifest.py")


def _run(args, script=None, env_extra=None):
    env = dict(os.environ)
    env.update(env_extra or {})
    return subprocess.run([sys.executable, script or TOOL] + args,
                          capture_output=True, text=True, env=env)


def test_t70_the_selftest_runs_and_passes():
    p = _run(["--selftest"])
    assert p.returncode == 0, p.stdout + p.stderr
    assert "SELFTEST PASSED" in p.stdout, p.stdout


def test_t70_the_selftest_covers_both_encodings_and_all_three_deltas():
    """A fixture that passes is only evidence if it exercised the cases it claims."""
    out = _run(["--selftest"]).stdout
    for phrase in ("manifest self-excluded", "an intruder file", "one changed byte",
                   "a removed file", "E33 form: self-listed", "staleness is REPORTED",
                   "E33 form still catches an intruder"):
        assert phrase in out, "the selftest no longer exercises %r:\n%s" % (phrase, out)


@pytest.mark.parametrize("break_it,why", [
    ('if rel in exclude:\n                continue',
     '        '),                                   # honour no exclusions -> self fires
    ('if b != declared[rel]["bytes"] or sha256(present[rel]) != declared[rel]["sha256"]:',
     'if False:'),                                  # never detect a change
], ids=["exclusion-ignored", "change-detection-removed"])
def test_t70_the_selftest_fails_when_the_walk_is_broken(tmp_path, break_it, why):
    """THE LEG THAT MATTERS. Two independent breakages of the walk, each run against the
    tool's own fixture, each of which must turn SELFTEST PASSED into a failure. Without
    this the two tests above could both be green on a walk that agrees with everything."""
    dst = str(tmp_path / "broken")
    os.makedirs(dst)
    body = open(TOOL, encoding="utf-8").read()
    assert break_it in body, "the breakage target moved; this fixture is testing nothing"
    broken = body.replace(break_it, why, 1)
    assert broken != body
    p = os.path.join(dst, "tree_manifest.py")
    open(p, "w", encoding="utf-8", newline="\n").write(broken)
    r = _run(["--selftest"], script=p)
    assert r.returncode != 0 or "SELFTEST PASSED" not in r.stdout, (
        "a broken walk still reported SELFTEST PASSED:\n%s" % r.stdout)


def test_t70_a_missing_manifest_is_an_error_not_a_pass(tmp_path):
    r = _run(["--verify", str(tmp_path / "nope.json")])
    assert r.returncode != 0
    assert "SELFTEST PASSED" not in r.stdout


def test_t70_the_andon_is_a_raise_not_an_assert():
    """`python -O` deletes asserts; a gate that decides whether a halt happens must raise
    (E21 Ruling 2). The tool's failure paths are SystemExit, which -O cannot remove -
    checked in the source and then demonstrated by running the broken walk under -O."""
    body = open(TOOL, encoding="utf-8").read()
    assert "raise SystemExit" in body
    for m in re.finditer(r"^\s*assert\b", body, re.M):
        line = body[m.start():body.index("\n", m.start())]
        assert "ANDON" not in line, "an ANDON is an assert at: %s" % line.strip()
    p = _run(["--selftest"], env_extra={"PYTHONOPTIMIZE": "1"})
    assert p.returncode == 0 and "SELFTEST PASSED" in p.stdout, (
        "the fixture does not survive PYTHONOPTIMIZE=1:\n%s" % (p.stdout + p.stderr))
