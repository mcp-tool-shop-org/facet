"""T75 - e08_ceiling's --cams and --restrict-mask (E42), exact by construction.

Same fixture T37 reads (tests/fixtures/make_measure_fixture.py): a flat quad
facing canonical +X. A yaw-90 camera sees every one of the 1024 texels at
facing 1.0; a yaw-0 camera sees it edge-on at facing exactly 0.0, which clears
no positive floor. Neither number can drift without the acceptance
construction itself changing - the same property T37 already leans on.

--cams REPLACES the ring entirely (no implicit yaws(n) flat ring underneath),
which --elev cannot do (it unconditionally ORs its pairs onto a full flat
ring - e08_ceiling.py's `if extra:` block runs `for y in yaws(n): R |= ...`
before ever reading `extra`). This file pins the population --cams reaches on
this fixture, that the flag is a pure ADD (absent, no 'custom' key at all -
T37/T08/T33/T53 already prove the REST of the output is untouched, this only
adds the negative-space check on the new key), and the population/shape ANDON
on --restrict-mask actually fires and actually raises (not a bare assert -
T33's `test_t33_no_instrument_gate_is_an_assert`-style discipline, applied to
a gate that test cannot see because it predates this commit).
"""
import json
import os

import numpy as np
import pytest

from conftest import run_py
from measure_support import PREP, call, payload, refusal

SCRIPT = "diagnostics/e08_ceiling.py"
PROD = "production (body 0.45 / head 0.18)"


def _ceiling_json(tmp_path, extra_args, name="c.json"):
    out_json = tmp_path / name
    rc, out, err = run_py(SCRIPT, ["--prep", PREP, "--sets", "2"] + extra_args
                          + ["--out-json", str(out_json)])
    assert rc == 0, "e08_ceiling exited %d\n%s\n%s" % (rc, out, err)
    return json.loads(out_json.read_text(encoding="utf-8")), out


# ---------------------------------------------------------------------------
# --cams: a pure ADD. Absent, the payload carries no 'custom' key anywhere,
# and the always-present echo fields are empty lists.
# ---------------------------------------------------------------------------

def test_t75_absent_cams_adds_no_custom_row(tmp_path):
    doc, out = _ceiling_json(tmp_path, [])
    assert doc["parsed_elev"] == [], doc["parsed_elev"]
    assert doc["parsed_cams"] == [], doc["parsed_cams"]
    assert "restrict_mask" not in doc, "no --restrict-mask was passed"
    for label, block in doc["settings"].items():
        assert "custom" not in block, "%s carries an uninvited 'custom' row" % label


# ---------------------------------------------------------------------------
# --cams: exact numbers, both cameras individually and their union
# ---------------------------------------------------------------------------

def test_t75_cams_single_camera_facing_dead_on_reaches_everything(tmp_path):
    doc, out = _ceiling_json(tmp_path, ["--cams", "90:0"])
    assert doc["parsed_cams"] == [{"yaw": 90.0, "el": 0.0}]
    row = doc["settings"][PROD]["custom"]
    assert row == {"cameras": 1, "reachable": 1024, "pct": 100.0,
                   "cams": [{"yaw": 90.0, "el": 0.0}]}


def test_t75_cams_single_camera_edge_on_reaches_nothing(tmp_path):
    doc, out = _ceiling_json(tmp_path, ["--cams", "0:0"])
    assert doc["parsed_cams"] == [{"yaw": 0.0, "el": 0.0}]
    row = doc["settings"][PROD]["custom"]
    assert row["reachable"] == 0, row
    assert row["pct"] == 0.0, row


def test_t75_cams_union_of_dead_and_edge_on_is_the_dead_ons_population(tmp_path):
    # two cameras, neither a ring: the edge-on one contributes nothing to the
    # union, so this must equal the single-camera dead-on result exactly - the
    # UNION law --cams exists to give (--elev, by construction, cannot ever
    # be tested this way: it always includes the full flat ring too)
    doc, out = _ceiling_json(tmp_path, ["--cams", "0:0,90:0"])
    assert doc["parsed_cams"] == [{"yaw": 0.0, "el": 0.0}, {"yaw": 90.0, "el": 0.0}]
    row = doc["settings"][PROD]["custom"]
    assert row["cameras"] == 2
    assert row["reachable"] == 1024, row


def test_t75_cams_does_not_disturb_the_flat_ring_rows(tmp_path):
    # N2 (yaws 0, 180) must still read exactly what T37 pins with --cams
    # present alongside it - the two code paths must not interact
    doc, out = _ceiling_json(tmp_path, ["--cams", "90:0"])
    assert doc["settings"][PROD]["N2"]["reachable"] == 0, (
        "the pre-existing N2 flat-ring row moved when --cams was added "
        "alongside it")


# ---------------------------------------------------------------------------
# --restrict-mask: nested under 'custom', a different denominator (pct is of
# the restricted population, not of NV), and a real ANDON on a shape mismatch.
# ---------------------------------------------------------------------------

def test_t75_restrict_mask_all_true_matches_the_unrestricted_row(tmp_path):
    m = tmp_path / "mask_all_true.npy"
    np.save(m, np.ones(1024, dtype=bool))
    doc, out = _ceiling_json(tmp_path, ["--cams", "90:0", "--restrict-mask", str(m)],
                             name="c2.json")
    assert doc["restrict_mask"]["in_scope_texels"] == 1024
    restricted = doc["settings"][PROD]["custom"]["restricted"]
    assert restricted == {"in_scope_texels": 1024, "reachable": 1024,
                          "pct_of_restricted": 100.0}


def test_t75_restrict_mask_all_false_is_zero_over_zero_not_a_crash(tmp_path):
    m = tmp_path / "mask_all_false.npy"
    np.save(m, np.zeros(1024, dtype=bool))
    doc, out = _ceiling_json(tmp_path, ["--cams", "90:0", "--restrict-mask", str(m)],
                             name="c3.json")
    restricted = doc["settings"][PROD]["custom"]["restricted"]
    assert restricted == {"in_scope_texels": 0, "reachable": 0,
                          "pct_of_restricted": 0.0}, (
        "an empty restricted population must read 0%, not raise ZeroDivisionError")


def test_t75_restrict_mask_half_population_has_its_own_denominator(tmp_path):
    # the fixture's yaw-90 camera reaches ALL 1024 texels regardless, so a
    # 512-True mask exercises the RESTRICTED pct's denominator specifically:
    # 512/512 = 100%, not 512/1024 = 50% - the two percentages this arm exists
    # to keep from being conflated
    half = np.zeros(1024, dtype=bool)
    half[:512] = True
    m = tmp_path / "mask_half.npy"
    np.save(m, half)
    doc, out = _ceiling_json(tmp_path, ["--cams", "90:0", "--restrict-mask", str(m)],
                             name="c4.json")
    restricted = doc["settings"][PROD]["custom"]["restricted"]
    assert restricted["in_scope_texels"] == 512
    assert restricted["reachable"] == 512
    assert restricted["pct_of_restricted"] == 100.0
    # and the row it nests under still reports the WHOLE-figure pct beside it
    assert doc["settings"][PROD]["custom"]["pct"] == 100.0


def test_t75_restrict_mask_wrong_shape_andon_fires_and_raises(tmp_path):
    m = tmp_path / "mask_wrong_shape.npy"
    np.save(m, np.ones(500, dtype=bool))          # NV is 1024, not 500
    out_json = tmp_path / "c5.json"
    rc, out, err = run_py(SCRIPT, ["--prep", PREP, "--sets", "2", "--cams", "90:0",
                                   "--restrict-mask", str(m),
                                   "--out-json", str(out_json)])
    assert rc != 0, "a population-size mismatch must refuse, not silently pair wrong texels"
    assert "ANDON" in err or "ANDON" in out, (
        "the refusal must name itself an ANDON:\nSTDOUT:%s\nSTDERR:%s" % (out, err))
    assert not out_json.exists(), "a fired gate must not still write output"


def test_t75_restrict_mask_absent_cams_present_is_silently_unused(tmp_path):
    # --restrict-mask without --cams: the flag has nothing to attach to (only
    # the 'custom' row carries a 'restricted' block) - this must not crash,
    # and must not silently restrict anything else
    m = tmp_path / "mask.npy"
    np.save(m, np.ones(1024, dtype=bool))
    doc, out = _ceiling_json(tmp_path, ["--restrict-mask", str(m)], name="c6.json")
    assert doc["restrict_mask"]["in_scope_texels"] == 1024
    for label, block in doc["settings"].items():
        assert "custom" not in block


# ---------------------------------------------------------------------------
# the served wrapper: same two flags, passed through, envelope carries them
# ---------------------------------------------------------------------------

def test_t75_served_reach_ceiling_passes_cams_through():
    doc = payload(call("reach_ceiling", {"prep": PREP, "sets": "2", "cams": "90:0"}))
    row = doc["settings"][PROD]["custom"]
    assert row["reachable"] == 1024, row
    assert doc["measure"]["instrument"]["path"] == "tools/diagnostics/e08_ceiling.py"


def test_t75_served_reach_ceiling_passes_restrict_mask_through(tmp_path):
    m = tmp_path / "mask.npy"
    np.save(m, np.ones(1024, dtype=bool))
    doc = payload(call("reach_ceiling", {"prep": PREP, "sets": "2", "cams": "90:0",
                                         "restrict_mask": str(m)}))
    restricted = doc["settings"][PROD]["custom"]["restricted"]
    assert restricted["reachable"] == 1024


def test_t75_served_reach_ceiling_missing_restrict_mask_refuses_naming_the_file(tmp_path):
    missing = tmp_path / "does_not_exist.npy"
    err = refusal(call("reach_ceiling", {"prep": PREP, "sets": "2", "cams": "90:0",
                                         "restrict_mask": str(missing)}))
    assert "does_not_exist.npy" in err["message"], err
