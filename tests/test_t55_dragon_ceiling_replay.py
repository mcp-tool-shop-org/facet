"""T55 - the dragon's ceiling re-derivation: the collapsed single setting,
exact.

E30's per-profile anchor gate for the beast's geometric reach, the same shape
as T54's. Every number is LOADED FROM the recorded
facet_next/E12_prep/ceiling.json; no reachable-count literal appears here.

profiles/beast.json pins project_twins' facing-min 0.45 and head-facing-min
0.45 - equal floors - and the recorded payload carries three blocks whose
numbers are identical to each other, which is E16-6's floors-equal signature.
Profile and record corroborate each other without a replay; the repaired tool
collapses to one block and says so.

The dragon's recorded set list stops at N12 (the ship and the character carry
two elevated rungs beyond it); the five equatorial rungs below are what all
three subjects share, so this anchor and T53/T54 measure the same thing.

--prep is read-only and --out-json goes to tmp_path. NOTE that E12_prep is the
one prep tree of the four that also HOLDS recorded outputs (ceiling.json,
elevated.json, offsurface.json, thin_curve.json) - so the re-hash leg below
covers the five prep inputs AND the recorded ceiling.json this test reads its
anchor from, because a tool writing its default output into that directory
would overwrite the anchor itself.
"""
import hashlib
import json

import pytest

from conftest import need, run_py

PREP_FILES = ("mask.npy", "meta.json", "nor.npy", "pos.npy", "prep_uv.glb",
              "ceiling.json")
SETS = "2,4,6,8,12"
FACING_MIN = 0.45        # profiles/beast.json, project_twins.facing-min
HEAD_FACING_MIN = 0.45   # profiles/beast.json, head-facing-min


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.mark.artifacts
@pytest.mark.slow
def test_t55_dragon_collapsed_setting_exact(assets, tmp_path):
    prep = need(assets, "facet_next/E12_prep")
    rec = json.loads(
        need(assets, "facet_next/E12_prep/ceiling.json").read_text(encoding="utf-8"))

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
    for k in keys:
        vals = {b[k]["reachable"] for b in rec_blocks}
        assert len(vals) == 1, (
            "the recorded beast blocks disagree at %s (%r) - the recorded run's "
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
    assert after == inputs, (
        "the recorded E12_prep changed during the replay - this tree holds "
        "recorded OUTPUTS beside its inputs, including this test's own anchor")
