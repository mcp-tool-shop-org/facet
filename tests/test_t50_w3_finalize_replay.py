"""T50 - W3's finalize replay: atlas_final.png byte-identical on the recorded
ARMB state.

E30's per-profile anchor gate for the character exemplar, built to T7's shape
(E14 Ruling 35: every polish lane opens with its subject's recorded artifacts
replayed against its citable tree). The anchor is the recorded artifact's OWN
BYTES - no sha256 literal appears here.

THE MODE WAS RECOVERED FROM THE RECORD, NOT GUESSED, and not chosen by trying
both. W3 has no finalize.json sidecar; what it has is E08-task3-report.md's
provenance block, which records "565 texels took the mean fallback". In
surface-aware mode that count is STRUCTURALLY zero - the tool says so itself
(`grown = valid.copy()` before the loop, E14 Ruling 31d), so a non-zero
fallback count can only come from the DEFAULT atlas-space flood. The recorded
run is therefore the default, and the replay reproduces 647,624 / 565 / 0.04329
exactly, which is the whole of that report's finalize row.

texpass_finalize reads --state and --prep and writes only --out/--json, both
pointed at tmp_path here, so the recorded trees are used in place as read-only
state; the test re-hashes the three state inputs afterward to prove the citable
tree did not move.

W3's state and its prep live in DIFFERENT trees (the strokes in facet_E08/ARMB,
the bake in facet_E06/C1) - the character's arc spans two experiments. Both are
re-hashed.
"""
import hashlib

import pytest

from conftest import need, run_py

STATE_FILES = ("atlas.png", "holes.png", "styled_mask.npy")


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.mark.artifacts
@pytest.mark.slow
def test_t50_w3_finalize_reproduces_the_recorded_atlas(assets, tmp_path):
    state = need(assets, "facet_E08/ARMB/state")
    prep = need(assets, "facet_E06/C1/prep")
    recorded = need(assets, "facet_E08/ARMB/out/atlas_final.png")

    inputs = {n: _sha(state / n) for n in STATE_FILES}

    out_png = tmp_path / "atlas_final.png"
    out_json = tmp_path / "finalize.json"
    rc, out, err = run_py(
        "texpass_finalize.py",
        ["--state", state, "--prep", prep, "--out", out_png, "--json", out_json])
    assert rc == 0, "finalize exited %d\n%s\n%s" % (rc, out, err)

    # the recorded mode, asserted rather than assumed: the flood, not
    # surface-aware, and the fallback count E08-task3-report.md records
    assert "atlas-space flood" in out, (
        "the replay did not run the recorded DEFAULT mode:\n%s" % out)
    assert "565 texels took mean fallback" in out, (
        "the mean-fallback count moved off E08-task3-report.md's 565:\n%s" % out)

    assert out_png.read_bytes() == recorded.read_bytes(), (
        "W3's atlas_final.png is not byte-identical to the recorded artifact "
        "(replay sha %s, recorded %s)" % (_sha(out_png), _sha(recorded)))

    after = {n: _sha(state / n) for n in STATE_FILES}
    assert after == inputs, "the recorded ARMB state changed during the replay"
