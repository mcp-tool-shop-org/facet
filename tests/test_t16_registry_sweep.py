"""T16 - the registry sweep's committed end-state on all four profiles.

Source: E16-11's anchor, commit c284693 (the dispatch's conditional - "only
if E16-11 has committed by the time you reach it" - was met before the first
port: it committed while this session was reading the record).

NUMBERING NOTE: this session's blind predictions called this port T12 -
written before the E16 ruling amended the E17 kickoff in place and assigned
T12-T15 to four new items. The E16-11 port is unnumbered in the amendment
("the E16-11 exclusion is LIFTED"), so it carries T16 here and the
amendment's ids stay free.

The exit-1 profiles are pinned AS exit 1 with their exact UNDECIDED counts.
The test asserts the recorded end-state, not "sweep passes" - a profile
gaining or losing a decision moves these numbers, and the commit that moves
them updates this table in the same stroke, per the tests-ride-the-commit
law (that is exactly what E16-11 itself did when E16-10's two new flags
surfaced as UNDECIDED).
"""
import re

import pytest

from conftest import run_py

SWEEP = "diagnostics/e04_registry_sweep.py"

# profile -> (exit code, undecided count, _per_invocation count)
END_STATE = {
    "beast": (0, 0, 3),
    "ship": (0, 0, 3),
    "prop": (1, 1, 3),
    "character": (1, 18, 1),
}
# 84, not c284693's 85: T14 (E16 Ruling 4a) reclassified texpass_iter's
# edge-frac as CODE in the sweep's section-6 transcription, so it leaves the
# subject-data population on all four profiles. This pin moved in T14's own
# commit, which is the tests-ride-the-commit law doing its job.
TOTAL_FLAGS = 84


def _run_sweep(profile):
    return run_py(SWEEP, ["--profile", "profiles/%s.json" % profile, "--tools", "tools"])


@pytest.mark.parametrize("profile", sorted(END_STATE))
def test_t12_sweep_end_state(profile):
    want_rc, want_undecided, want_perinv = END_STATE[profile]
    rc, out, err = _run_sweep(profile)
    assert rc == want_rc, (
        "%s sweep exited %d, committed end-state is %d\n%s\n%s"
        % (profile, rc, want_rc, out, err))
    m = re.search(r"\[sweep\] (\d+) SUBJECT-DATA flags on this route; decided (\d+)\s+\((.*)\)", out)
    assert m, "decided line not found:\n%s" % out
    total, decided, how = int(m.group(1)), int(m.group(2)), m.group(3)
    assert total == TOTAL_FLAGS, (
        "%s: %d subject-data flags, the T14 end-state is %d"
        % (profile, total, TOTAL_FLAGS))
    assert total - decided == want_undecided, (
        "%s: %d undecided, committed end-state is %d\n%s"
        % (profile, total - decided, want_undecided, out))
    pm = re.search(r"_per_invocation (\d+)", how)
    got_perinv = int(pm.group(1)) if pm else 0
    assert got_perinv == want_perinv, (
        "%s: _per_invocation %d, committed end-state is %d (how: %s)"
        % (profile, got_perinv, want_perinv, how))
    if want_rc == 0:
        assert "every subject-data flag on this route carries an explicit decision." in out


def test_t12_prop_remainder_is_the_preexisting_one():
    """The one undecided flag on prop is pre-existing (texpass_brush prompt),
    named so a NEW undecided flag cannot hide behind the count staying 1."""
    rc, out, err = _run_sweep("prop")
    assert rc == 1
    undecided_lines = [ln for ln in out.splitlines()
                       if re.match(r"\[sweep\]\s{2,}\S", ln)]
    assert len(undecided_lines) == 1, (
        "expected exactly one undecided detail line:\n%s" % out)
    assert "texpass_brush.py" in undecided_lines[0] and "prompt" in undecided_lines[0]
