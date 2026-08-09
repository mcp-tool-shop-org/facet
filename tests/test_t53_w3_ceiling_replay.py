"""T53 - W3's ceiling re-derivation: all three threshold settings, exact.

E30's per-profile anchor gate for the character's geometric reach. Every number
compared here is LOADED FROM the recorded facet_E08/gate0/ceiling.json - there
is no reachable-count literal in this file, which is what makes it an anchor
rather than a transcription. (T8, the sword's, carries its two counts as
literals; this is the stricter form and the one E30 builds to.)

W3 IS THE ONE SUBJECT WHOSE THREE SETTINGS DO NOT COLLAPSE, and the reason is
in its profile rather than in this test: profiles/character.json pins
project_twins' facing-min 0.45 and head-facing-min 0.18, while ship, beast and
prop all pin 0.45/0.45. E16-6's repair collapses the tool's three specs to one
block when the floors are equal - so the recorded payloads of the galleon, the
dragon and the sword carry three IDENTICAL blocks (T54/T55 and T8's docstring)
and W3's carries three DIFFERENT ones. The profile predicts the recorded block
structure for all four subjects, independently of any replay, which is what
licenses 0.45/0.18 as the recovered invocation here rather than a fitted one.

SELECTING THE BLOCKS. T8's law is: choose a configuration by its PROPERTY via
settings_index, never by caption. The replay obeys it directly. The RECORDED
payload predates settings_index and its captions are the pre-repair ones
("uniform 0.45"), so its blocks are taken in the tool's own _specs order -
production, uniform body-floor, uniform head-floor - which is the order the
tool constructs them in, in both versions. The floors are then asserted against
settings_index, so a reordering of either side fails rather than mis-pairs.

--prep is read-only and --out-json goes to tmp_path; the prep's five files are
re-hashed afterward.
"""
import hashlib
import json

import pytest

from conftest import need, run_py

PREP_FILES = ("mask.npy", "meta.json", "nor.npy", "pos.npy", "prep_uv.glb")
SETS = "2,4,6,8,12"          # the five equatorial rungs common to the record
FACING_MIN = 0.45            # profiles/character.json, project_twins.facing-min
HEAD_FACING_MIN = 0.18       # profiles/character.json, head-facing-min
EXPECTED_FLOORS = [(0.45, 0.18), (0.45, 0.45), (0.18, 0.18)]


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.mark.artifacts
@pytest.mark.slow
def test_t53_w3_three_settings_exact(assets, tmp_path):
    prep = need(assets, "facet_E06/C1/prep")
    rec = json.loads(
        need(assets, "facet_E08/gate0/ceiling.json").read_text(encoding="utf-8"))

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

    # the floors DO NOT collapse for this subject - the NOTE must be absent
    assert "collapse" not in out, (
        "the settings collapsed on W3 - the floors are no longer distinct:\n%s" % out)

    idx = got["settings_index"]
    assert [(r["facing_min"], r["head_facing_min"]) for r in idx] == EXPECTED_FLOORS, (
        "settings_index is not the three distinct character floors: %r" % idx)

    rec_blocks = list(rec["settings"].values())
    assert len(rec_blocks) == len(idx) == 3, (
        "expected three blocks on both sides; recorded %d, replay %d"
        % (len(rec_blocks), len(idx)))

    for row, rec_blk in zip(idx, rec_blocks):
        got_blk = got["settings"][row["label"]]
        for n in SETS.split(","):
            key = "N" + n
            assert got_blk[key]["reachable"] == rec_blk[key]["reachable"], (
                "floors %g/%g, %s: reachable %d != recorded %d"
                % (row["facing_min"], row["head_facing_min"], key,
                   got_blk[key]["reachable"], rec_blk[key]["reachable"]))

    # can-fail proof, on the RECORD: the three blocks must be distinct, or the
    # loop above would pass while pairing them arbitrarily
    n8 = [b["N8"]["reachable"] for b in rec_blocks]
    assert len(set(n8)) == 3, (
        "the recorded W3 blocks are no longer three distinct measurements "
        "(N8 %r) - this anchor cannot detect a mis-paired setting" % n8)

    after = {n: _sha(prep / n) for n in PREP_FILES}
    assert after == inputs, "the recorded C1 prep changed during the replay"
