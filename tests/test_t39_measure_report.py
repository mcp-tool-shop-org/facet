"""T39 - measure_report: the sheet half on degenerate-by-design operands, and
the comparison half whose refusal IS the product.

The report fixture's twin and asset panels are UNIFORM colours under a 24x24
mask (tests/fixtures/make_measure_fixture.py), so the dE statistics are
degenerate on purpose: median == mean == p90 exactly, both over-threshold
percentages exactly 0.0, and figure_px exactly 576. The sheet math cannot
fake those identities.

The comparison half: two payloads of the SAME configuration compare; any
identity difference - here, a different subject path changing the config hash
- REFUSES naming the field. The spec's law: two assets measured by different
configurations of this server are not comparable.
"""
import os

import pytest

from measure_support import MESHES, REPORT, call, payload, refusal


@pytest.fixture(scope="module")
def sheet(tmp_path_factory):
    out = tmp_path_factory.mktemp("sheet")
    return payload(call("measure_report", {"sheet": {
        "twins": os.path.join(REPORT, "twins"),
        "asset": os.path.join(REPORT, "asset"),
        "prov": os.path.join(REPORT, "prov"),
        "masks": os.path.join(REPORT, "masks"),
        "views": "0",
        "out": str(out / "sheet.png"),
    }}))


def test_t39_sheet_stats_hold_their_analytic_identities(sheet):
    s = sheet["sheet"]["stats"]["0"]
    assert s["figure_px"] == 576, "the mask is a 24x24 square, exactly"
    assert s["dE_median"] == s["dE_mean"] == s["dE_p90"], (
        "uniform operands make every dE statistic the same number; a spread "
        "here means the panels stopped being read as constructed")
    assert s["pct_over_10"] == 0.0 and s["pct_over_23"] == 0.0
    assert os.path.exists(sheet["sheet"]["path"])


def test_t39_sheet_transcript_and_denominator_ride_the_payload(sheet):
    lines = sheet["sheet"]["transcript"]
    assert any("columns:" in ln for ln in lines)
    ratios = sheet["measure"]["ratios"]
    assert any("figure_px" in str(v) for v in ratios.values()), (
        "dE statistics are quoted over the exact silhouette; the payload "
        "names that denominator or the number floats free")


def test_t39_same_configuration_compares_with_deltas():
    a = payload(call("mesh_stats", {"glb": os.path.join(MESHES, "cube.glb")}))
    b = payload(call("mesh_stats", {"glb": os.path.join(MESHES, "cube.glb")}))
    doc = payload(call("measure_report", {"left": a, "right": b}))
    rows = doc["comparison"]["rows"]
    assert rows["mesh.faces"]["delta"] == 0
    assert rows["mesh.components"] == {"left": 1, "right": 1, "delta": 0}


def test_t39_mismatched_configurations_refuse_naming_the_field():
    a = payload(call("mesh_stats", {"glb": os.path.join(MESHES, "cube.glb")}))
    c = payload(call("mesh_stats", {"glb": os.path.join(MESHES,
                                                        "pinch.glb")}))
    err = refusal(call("measure_report", {"left": a, "right": c}))
    assert err["code"] == "MEASUREMENT_MISMATCH"
    assert err["exit_code"] == 4
    assert "config_hash" in err["message"], (
        "the refusal names WHICH identity field differs, or nobody can fix it")


def test_t39_bad_arguments_refuse():
    err = refusal(call("measure_report", {}))
    assert err["code"] == "BAD_ARGUMENT"
    a = payload(call("mesh_stats", {"glb": os.path.join(MESHES, "cube.glb")}))
    err = refusal(call("measure_report", {"left": a}))
    assert err["code"] == "BAD_ARGUMENT"
    assert "BOTH" in err["message"]
    err = refusal(call("measure_report", {"left": {"no": "envelope"},
                                          "right": {"no": "envelope"}}))
    assert err["code"] == "BAD_ARGUMENT"
    assert "envelope" in err["message"]
