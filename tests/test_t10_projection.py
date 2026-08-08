"""T10 - the projection is unmoved: project_twins reproduces the recorded
stage1b outputs byte-identically on the sword's recorded twins.

Source: E16-8's anchor (Ruling 21e - the probe's corner-median reference
replaced by the fitted border ring, projection outputs proven byte-identical
across the change) - WITH ITS DISPATCH CORRECTION: the probe is NOT
report-only; project_twins:835 carries an ANDON, disarmed at bg-max-pct 100.0
on prop/beast/ship and ARMED at 2.0 on character.json.

The recorded run this ports is the six-view stage1b projection (E14 handoff
6's invocation, quoted in its report): views 0/1/3/4/5/7 - view 2 (y+090)
and view 6 (y+270) were inputs to nothing; y+270 is the edge-on blade the
stroke lane painted instead. All five outputs are compared byte-for-byte
against the recorded stage1b_* artifacts. E16-8 and E16-10 each re-ran this
projection today (across the probe repair and the local_thickness
extraction), all five outputs byte-identical both times.
"""
import hashlib

import pytest

from conftest import need, run_py

VIEWS = [0, 1, 3, 4, 5, 7]
OUTPUTS = ["stage1b_atlas.png", "stage1b_atlas_holes.png",
           "stage1b_atlas_styled_mask.npy", "stage1b_atlas_owner.npy",
           "stage1b_atlas_blend.png"]


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.mark.artifacts
@pytest.mark.slow
def test_t10_projection_reproduces_stage1b(assets, tmp_path):
    prep = need(assets, "facet_next/E14_prep")
    twins = need(assets, "facet_next/E14_prep/twins/out")
    recorded = {n: need(assets, "facet_next/E14_prep/stage1/" + n) for n in OUTPUTS}

    args = ["--profile", "profiles/prop.json", "--prep", prep]
    for i in VIEWS:
        twin = need(assets, "facet_next/E14_prep/twins/out/TWIN_swordclay_%d.png" % i)
        args += ["--view", "%d=%s" % (i, twin)]
    args += ["--out", tmp_path / "stage1b_atlas.png"]

    rc, out, err = run_py("project_twins.py", args, timeout=3600)
    assert rc == 0, "project_twins exited %d\n%s\n%s" % (rc, out, err)

    mismatched = []
    for n in OUTPUTS:
        got = tmp_path / n
        assert got.exists(), "expected output %s was not written" % n
        if got.read_bytes() != recorded[n].read_bytes():
            mismatched.append("%s (replay %s, recorded %s)"
                              % (n, _sha(got)[:16], _sha(recorded[n])[:16]))
    assert not mismatched, (
        "projection outputs differ from the recorded stage1b artifacts:\n  "
        + "\n  ".join(mismatched)
        + "\n(if a profile or twin moved under this run, git log the profiles "
          "first - the record moves under a shared working copy)")
