"""T2 - texpass_iter's selftest: exit 0, styled texels byte-identical
(max delta 0.000000), the write-head lossless.

Source: the tool's own selftest; E16-4's anchor table measured it on the
sword's anchor state (PASS, write-head lossless, 377 texels committed).

TIER CORRECTION, a finding against the dispatch: the kickoff lists this test
as hermetic and the tests-required law commit calls the selftest "re-runnable
from a fresh clone". It is not: --state, --prep and (via emit's unconditional
load_scene) --glb are required, and the repo tracks no fixture state - the
smallest real inputs are the recorded trees. Ported at the artifacts tier;
whether a tiny in-repo fixture state should exist is the advisor's call, not
a fixture this session invents.

The selftest COMMITS into --state, so the state is copied to scratch and the
recorded tree is read-only (Ruling 33's ledger).
"""
import re

import pytest

from conftest import copy_state, need, run_py, last_nonempty


@pytest.mark.artifacts
def test_t02_selftest_write_head_lossless(assets, tmp_path):
    prep = need(assets, "facet_next/E14_prep")
    glb = need(assets, "facet_next/E14_prep/prep_uv.glb")
    state_src = need(assets, "facet_next/E14_strokes/run/final/rstate_s8anchor")
    state = copy_state(state_src, tmp_path / "state")

    rc, out, err = run_py(
        "texpass_iter.py",
        ["selftest", "--state", state, "--prep", prep, "--glb", glb])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)

    delta_lines = [ln for ln in out.splitlines()
                   if ln.startswith("[selftest] styled-texel max delta")]
    assert len(delta_lines) == 1, "delta line not found:\n%s" % out
    assert "max delta 0.000000" in delta_lines[0], (
        "styled texels moved: %s" % delta_lines[0])

    assert last_nonempty(out).startswith("[selftest] PASS"), (
        "last line is not the selftest PASS:\n%s" % out)

    # reported, not asserted: the committed count (E16-4 measured 377 on this
    # state; the dispatch anchors exit code and delta, and the count depends
    # on the fake-inpaint blur, i.e. on scipy - a version drift there would
    # move the count without touching the write-head property under test)
    m = re.search(r"committed ([\d,]+)", delta_lines[0])
    print("T2 committed texels: %s (E16-4 recorded 377)" % (m.group(1) if m else "?"))
