"""T37 - reach_ceiling wrapped, on a ladder whose numbers are exact by
construction - plus the recorded anchor.

The fixture quad faces canonical +X (tests/fixtures/make_measure_fixture.py):
a yaw-90 camera sees every texel at facing 1.0 and the yaw-0/180 pair sees it
edge-on at facing 0.0. So N2 (yaws 0, 180) reaches NOTHING - 0.0 clears no
positive floor - and N4 (adds 90, 270) reaches ALL 1024 valid texels. Neither
number can drift without the acceptance construction itself changing, which is
exactly what this test exists to notice.

The artifacts-tier anchor at the bottom is the other half of the claim: the
SERVED tool, pointed at a recorded prep, reproduces the record's own numbers.
E12's stage-1 ceiling was pre-registered before any projection
(docs/experiments/E12-task2-report.md section 2.2) and is the acceptance
figure every downstream coverage number on that subject reads against - if
the wrap moved it, the wrap would be a new instrument wearing the old one's
name.
"""
import os
import shutil

import pytest

from conftest import need
from measure_support import PREP, call, payload, refusal


@pytest.fixture(scope="module")
def ceiling():
    return payload(call("reach_ceiling", {"prep": PREP, "sets": "2,4"}))


def test_t37_the_ladder_is_exact(ceiling):
    assert ceiling["valid_texels"] == 1024
    assert ceiling["head_band"] == 0, (
        "the fixture's crop selects no texels; a non-zero head band means "
        "the projection moved")
    prod = ceiling["settings"]["production (body 0.45 / head 0.18)"]
    assert prod["N2"]["reachable"] == 0, (
        "yaws 0/180 see the quad edge-on at facing exactly 0.0; any reach "
        "here means the facing floor stopped being applied")
    assert prod["N4"]["reachable"] == 1024, (
        "yaw 90 faces the quad at facing exactly 1.0; anything under 1024 "
        "means visibility rays started hitting phantom geometry")
    assert prod["N4"]["pct"] == 100.0


def test_t37_reachable_and_valid_ride_beside_every_pct(ceiling):
    # the denominator law: pct is quoted WITH its operands in the payload
    assert ceiling["settings"]["production (body 0.45 / head 0.18)"]["N2"][
        "reachable"] == 0
    assert "valid_texels" in ceiling
    ratios = ceiling["measure"]["ratios"]
    assert any("pct" in k for k in ratios), ratios


def test_t37_the_bias_wall_warning_travels_with_the_payload(ceiling):
    w = ceiling["measure"]["warnings"]
    assert any("wall floor" in ln for ln in w), (
        "e08_ceiling's E14 Ruling 10b caveat fired on stdout and must ride "
        "the payload: %r" % w)


def test_t37_missing_prep_member_refuses_naming_the_file(tmp_path):
    broken = tmp_path / "prep"
    shutil.copytree(PREP, str(broken))
    os.remove(str(broken / "pos.npy"))
    err = refusal(call("reach_ceiling", {"prep": str(broken)}))
    assert err["code"] == "PRECONDITION_MISSING"
    assert err["exit_code"] == 4
    assert "pos.npy" in err["message"]


def test_t37_meta_without_crop_refuses_naming_the_keys(tmp_path):
    import json
    broken = tmp_path / "prep"
    shutil.copytree(PREP, str(broken))
    meta_path = str(broken / "meta.json")
    with open(meta_path, encoding="utf-8") as fh:
        meta = json.load(fh)
    meta.pop("crop")
    with open(meta_path, "w", encoding="ascii", newline="\n") as fh:
        json.dump(meta, fh)
    err = refusal(call("reach_ceiling", {"prep": str(broken)}))
    assert err["code"] == "PRECONDITION_MISSING"
    assert "crop" in err["message"], (
        "e08_ceiling KeyErrors on a cropless meta; the wrapper must refuse "
        "with the name instead")


# ---------------------------------------------------------------------------
# the recorded anchor - the wrap reproduces the record's own number
# ---------------------------------------------------------------------------

@pytest.mark.artifacts
@pytest.mark.slow
def test_t37_served_tool_reproduces_e12s_preregistered_ceiling(assets):
    """E12-task2-report.md section 2.2, run through the SERVED tool with the
    recorded invocation's own floors (0.45/0.45, allocation NONE per E12
    Ruling 2). The five figures below are the record's, digit for digit; a
    drift here means the wrap changed the instrument, which is the one thing
    it exists not to do. N8 only - the stage-1 set, the pre-registered
    acceptance figure."""
    prep = need(assets, os.path.join("facet_next", "E12_prep"))
    doc = payload(call("reach_ceiling", {
        "prep": str(prep), "sets": "8",
        "facing_min": 0.45, "head_facing_min": 0.45}))
    assert doc["valid_texels"] == 3240510
    assert doc["head_band"] == 1358656
    # equal floors collapse the three settings to one (E12 Ruling 6e's
    # repair); the single block carries all three names joined
    labels = list(doc["settings"])
    assert len(labels) == 1, labels
    row = doc["settings"][labels[0]]["N8"]
    assert row["reachable"] == 1635304
    assert row["pct"] == 50.46
    assert doc["twin_front_reachable"] + doc["twin_back_reachable"] > 0
    assert doc["measure"]["instrument"]["path"] == \
        "tools/diagnostics/e08_ceiling.py"
