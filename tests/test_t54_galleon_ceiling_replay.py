"""T54 - the galleon's ceiling re-derivation: the collapsed single setting,
exact.

E30's per-profile anchor gate for the ship's geometric reach. Every number is
LOADED FROM the recorded facet_next/E04_armT72/ceiling/ceiling.json; no
reachable-count literal appears in this file.

THE COLLAPSE IS THE INVOCATION'S EVIDENCE, and it runs both ways here.
profiles/ship.json pins project_twins' facing-min 0.45 AND head-facing-min 0.45
- equal floors - and E16-6's repair collapses the tool's three specs to one
block exactly when they are equal, printing a NOTE that says so. The recorded
payload, written before that repair, carries three blocks whose numbers are
IDENTICAL to each other: the floors-equal signature T8 names, since the
pre-repair tool computed all three captions at the same pair. So the profile
predicts the recorded structure and the recorded structure corroborates the
profile, neither of them looking at a replay.

The test therefore asserts the recorded three are identical (that is the
signature, and it is this anchor's can-fail leg), then compares the replay's
ONE block against them.

--prep is read-only and --out-json goes to tmp_path; the prep's five files are
re-hashed afterward.
"""
import hashlib
import json

import pytest

from conftest import need, run_py

PREP_FILES = ("mask.npy", "meta.json", "nor.npy", "pos.npy", "prep_uv.glb")
SETS = "2,4,6,8,12"
FACING_MIN = 0.45        # profiles/ship.json, project_twins.facing-min
HEAD_FACING_MIN = 0.45   # profiles/ship.json, head-facing-min


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.mark.artifacts
@pytest.mark.slow
def test_t54_galleon_collapsed_setting_exact(assets, tmp_path):
    prep = need(assets, "facet_next/E04_shipprep")
    rec = json.loads(
        need(assets, "facet_next/E04_armT72/ceiling/ceiling.json")
        .read_text(encoding="utf-8"))

    inputs = {n: _sha(prep / n) for n in PREP_FILES}

    out_json = tmp_path / "ceiling.json"
    rc, out, err = run_py(
        "diagnostics/e08_ceiling.py",
        ["--prep", prep, "--sets", SETS, "--facing-min", FACING_MIN,
         "--head-facing-min", HEAD_FACING_MIN, "--out-json", out_json],
        timeout=3600)
    assert rc == 0, "e08_ceiling exited %d\n%s\n%s" % (rc, out, err)
    got = json.loads(out_json.read_text(encoding="utf-8"))

    assert got["valid_texels"] == rec["valid_texels"], (
        "valid texel count moved: %d (recorded %d)"
        % (got["valid_texels"], rec["valid_texels"]))
    assert got["head_band"] == rec["head_band"], (
        "head band moved: %d (recorded %d)" % (got["head_band"], rec["head_band"]))

    rec_blocks = list(rec["settings"].values())
    keys = ["N" + n for n in SETS.split(",")]
    # the floors-equal signature in the RECORD, and this anchor's can-fail leg:
    # if these three ever differ, the recorded run had distinct floors and the
    # invocation below is the wrong one
    for k in keys:
        vals = {b[k]["reachable"] for b in rec_blocks}
        assert len(vals) == 1, (
            "the recorded ship blocks disagree at %s (%r) - the recorded run's "
            "floors were NOT equal and 0.45/0.45 is not its invocation" % (k, vals))

    assert "the three threshold settings collapse to 1" in out, (
        "collapse NOTE missing - the replay's floors were not equal:\n%s" % out)
    idx = got["settings_index"]
    assert len(idx) == 1 and idx[0]["facing_min"] == FACING_MIN \
        and idx[0]["head_facing_min"] == HEAD_FACING_MIN, (
        "settings_index is not the single 0.45/0.45 configuration: %r" % idx)

    blk = got["settings"][idx[0]["label"]]
    for k in keys:
        assert blk[k]["reachable"] == rec_blocks[0][k]["reachable"], (
            "%s: reachable %d != recorded %d"
            % (k, blk[k]["reachable"], rec_blocks[0][k]["reachable"]))

    after = {n: _sha(prep / n) for n in PREP_FILES}
    assert after == inputs, "the recorded shipprep changed during the replay"
