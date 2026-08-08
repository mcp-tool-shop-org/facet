"""T13 - two concurrent verifies in one working copy cannot collide.

Source: E16 Ruling 3 (the twelfth errand, hit independently by both seats on
2026-08-08: the advisor's fold verify collided with E16-1's own on the fixed
`facet.db.det_a`/`.det_b` scratch paths - leg 1's two temp files were the
same two names for every process, so concurrent verifies could read each
other's half-written bytes).

The repair makes the temp paths per-process unique (same directory), so the
collision is impossible BY CONSTRUCTION. This test runs the ruled collision
case: two verifies launched simultaneously against the SAME scratch DB path.
Before the repair this is the recorded race (timing-dependent - the recorded
instance failed once and retried clean); after it, both must pass every
time, and neither leaves a temp behind.
"""
import subprocess
import sys

import pytest

from conftest import REPO, tool, last_nonempty

PASSED_LINE = "VERIFY PASSED - all four legs"


@pytest.mark.fold
def test_t13_concurrent_verifies_do_not_collide(built_db):
    cmd = [sys.executable, tool("facet_index.py"), "verify", "--db", str(built_db)]
    procs = [subprocess.Popen(cmd, cwd=str(REPO), stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) for _ in range(2)]
    results = []
    for p in procs:
        out_b, err_b = p.communicate(timeout=1800)
        results.append((p.returncode,
                        out_b.decode("utf-8", errors="replace"),
                        err_b.decode("utf-8", errors="replace")))
    for i, (rc, out, err) in enumerate(results):
        assert rc == 0, (
            "concurrent verify %d exited %d - the det temp collision is back?\n%s\n%s"
            % (i, rc, out, err))
        assert last_nonempty(out) == PASSED_LINE, (
            "concurrent verify %d did not end at the PASSED line:\n%s" % (i, out))
        # byte-identity specifically - the leg the collision corrupts reads
        # half-written bytes, which surfaces as identity failure, not a crash
        assert any("BYTE-IDENTICAL" in ln for ln in out.splitlines()), (
            "concurrent verify %d: leg 1 did not report byte-identity\n%s" % (i, out))
    leftovers = sorted(p.name for p in built_db.parent.glob("*.det_*"))
    assert not leftovers, "verify left det temps behind: %s" % leftovers
