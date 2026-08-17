"""T85 - plate disagreement inside named regions.

The instrument is tools/region_disagreement.py. Every number below is
known by construction except the artifacts replay, which re-reads the
E46 t00 arrays the brief nominated.

A share-of-nonzero, a region-derived threshold, a total that cannot
see speckle, a clamped oversized box, or a bare assert fails at least
one leg.

Hermetic tests do not open facet_E46. The artifacts leg does, read-only.
"""
import ast
import json
import os
import sys

import numpy as np
import pytest

from conftest import REPO, need, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import region_disagreement as R  # noqa: E402
import s3_sheet as S  # noqa: E402


def test_t85_selftest_exits_zero():
    rc, out, err = run_py("region_disagreement.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "field.hot_lcc == 16" in out, out
    assert "field.median == 0.04" in out, out
    assert "blob.median == 0.4" in out, out


def test_t85_calibration_field_and_blob():
    dis, own = R.fixture_calibration()
    fig = R.figure_stats(dis, own)
    field = R.region_row(dis, own, [8, 8, 24, 24], fig, "field", 0, "s3_off")
    blob = R.region_row(dis, own, [12, 12, 16, 16], fig, "blob", 0, "s3_off")
    assert fig["owned_px"] == R.CALIBRATION_OWNED
    assert field["owned_px"] == R.CALIBRATION_OWNED
    assert field["dis_median"] == pytest.approx(R.CALIBRATION_FIELD_MEDIAN)
    assert blob["dis_median"] == pytest.approx(R.CALIBRATION_BLOB_MEDIAN)
    assert field["hot_px"] == R.CALIBRATION_FIELD_HOT
    assert field["hot_lcc"] == R.CALIBRATION_FIELD_LCC
    assert blob["hot_px"] == R.CALIBRATION_BLOB_HOT
    assert blob["hot_lcc"] == R.CALIBRATION_BLOB_LCC
    # total-only would report 20 and could not say the coherent piece is 16
    assert field["hot_px"] != field["hot_lcc"]


def test_t85_region_threshold_would_miss_the_blob():
    """Can-fail: deriving p90 from the region under test reports hot=0
    on a uniform-hot blob. The figure-derived rule must not."""
    dis, own = R.fixture_calibration()
    fig = R.figure_stats(dis, own)
    blob = R.region_row(dis, own, [12, 12, 16, 16], fig, "blob", 0, "s3_off")
    blob_vals = dis[12:16, 12:16]
    own_p90 = float(np.percentile(blob_vals, 90))
    region_hot = int((blob_vals > own_p90).sum())
    assert own_p90 == pytest.approx(R.CALIBRATION_BLOB_MEDIAN)
    assert region_hot == 0
    assert blob["hot_px"] == R.CALIBRATION_BLOB_HOT
    assert blob["threshold"] == "figure_owned_p90"


def test_t85_figure_p90_not_region_p90_on_a_mid_block(tmp_path):
    """Can-fail: a mid-valued block is entirely above figure p90 and
    entirely equal to its own p90. Region-derived hot is 0; figure-
    derived hot is the whole block."""
    n = 32
    own = np.full((n, n), -1, dtype=np.int16)
    own[0:16, 0:16] = 0
    dis = np.zeros((n, n), dtype=np.float64)
    dis[0:16, 0:16] = 0.05
    dis[0:4, 0:4] = 0.20
    dis[14:16, 14:16] = 0.80
    fig = R.figure_stats(dis, own)
    mid = R.region_row(dis, own, [0, 0, 4, 4], fig, "mid", 0, "s3_off")
    assert fig["p90"] < 0.20
    assert mid["dis_median"] == pytest.approx(0.20)
    assert mid["hot_px"] == 16
    own_p90 = float(np.percentile(dis[0:4, 0:4], 90))
    assert own_p90 == pytest.approx(0.20)
    assert int((dis[0:4, 0:4] > own_p90).sum()) == 0


def test_t85_oversized_box_andon():
    dis, own = R.fixture_calibration()
    fig = R.figure_stats(dis, own)
    with pytest.raises(R.Andon, match="exceeds source"):
        R.region_row(dis, own, [0, 0, 40, 40], fig, "big", 0, "s3_off")
    with pytest.raises(S.Andon, match="exceeds source"):
        S.crop_array(dis, [0, 0, 40, 40], "big", "fixture")


def test_t85_empty_box_andon():
    with pytest.raises(S.Andon, match="empty box"):
        S.as_box([4, 4, 4, 8])


def test_t85_missing_tree_andon(tmp_path):
    with pytest.raises(R.Andon, match="no tree"):
        R.run(str(tmp_path / "missing"), "s3_off", figure_only=True)


def test_t85_shape_mismatch_andon(tmp_path):
    td = tmp_path / "s3_off" / "t00"
    td.mkdir(parents=True)
    np.save(str(td / "disagreement.npy"), np.zeros((8, 8), dtype=np.float32))
    np.save(str(td / "owner.npy"), np.zeros((4, 4), dtype=np.int16))
    with pytest.raises(R.Andon, match="differ"):
        R.load_view(str(tmp_path), "s3_off", 0)


def test_t85_nonzero_share_is_not_the_statistic():
    """Can-fail: 86%+ nonzero on a figure must not be what we report as hot."""
    dis, own = R.fixture_calibration()
    fig = R.figure_stats(dis, own)
    owned = own >= 0
    nonzero = int((dis[owned] > 0).sum())
    assert nonzero == R.CALIBRATION_OWNED
    assert fig["hot_px"] == R.CALIBRATION_FIELD_HOT
    assert fig["hot_px"] < nonzero


def test_t85_flicker_checkerboard_vs_solid():
    """Can-fail: a solid owner block has flicker 0; a checkerboard does not."""
    n = 16
    solid = np.zeros((n, n), dtype=np.int16)
    check = np.zeros((n, n), dtype=np.int16)
    yy, xx = np.indices((n, n))
    check[(yy + xx) % 2 == 1] = 1
    mask = np.ones((n, n), dtype=bool)
    s = R.flicker_rate(solid, mask)
    c = R.flicker_rate(check, mask)
    assert s["rate"] == 0.0
    assert c["rate"] == 1.0
    assert c["flips"] == c["pairs"]
    assert c["pairs"] > 0


def test_t85_empty_owned_reports_zero_not_a_ratio():
    dis = np.ones((8, 8), dtype=np.float64) * 0.3
    own = np.full((8, 8), -1, dtype=np.int16)
    own[6:8, 6:8] = 0
    fig = R.figure_stats(dis, own)
    miss = R.region_row(dis, own, [0, 0, 4, 4], fig, "miss", 0, "s3_off")
    assert miss["owned_px"] == 0
    assert miss["dis_median"] is None
    assert miss["hot_share"] is None
    assert miss["ratio_median"] is None
    assert miss["flicker_rate"] is None


def test_t85_cli_writes_json(tmp_path):
    dis, own = R.fixture_calibration()
    R.write_view_tree(str(tmp_path), "s3_off", 0, dis, own)
    regions = {
        "label": "t85",
        "views": {"0": [{"name": "blob", "box": [12, 12, 16, 16]}]},
    }
    rpath = tmp_path / "regions.json"
    rpath.write_text(json.dumps(regions), encoding="utf-8")
    outp = tmp_path / "out.json"
    rc, out, err = run_py("region_disagreement.py", [
        "--tree", str(tmp_path),
        "--mode", "s3_off",
        "--regions", str(rpath),
        "--json-out", str(outp),
    ])
    assert rc == 0, "%s\n%s" % (out, err)
    assert "not a spend recommendation" in out, out
    payload = json.loads(outp.read_text(encoding="utf-8"))
    names = [r["name"] for r in payload["rows"]]
    assert names == ["figure", "blob"]
    blob = payload["rows"][1]
    assert blob["hot_lcc"] == R.CALIBRATION_BLOB_LCC
    assert blob["denominator"] == "owned_px"


def test_t85_cli_missing_tree_exits_2(tmp_path):
    rc, out, err = run_py("region_disagreement.py", [
        "--tree", str(tmp_path / "nope"),
        "--figure-only",
    ])
    assert rc == 2
    assert "ANDON" in err


def test_t85_no_andon_is_a_bare_assert():
    src = open(os.path.join(str(REPO), "tools", "region_disagreement.py"),
               encoding="utf-8").read()
    tree = ast.parse(src)
    bares = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    assert bares == [], "bare assert at lines %s" % bares


@pytest.mark.artifacts
def test_t85_e46_t00_owned_count(assets):
    """The brief's shaping number, re-measured. Do not write the tree."""
    root = need(assets, "facet_E46")
    on = need(assets, "facet_E46/s3_on/t00")
    dis = np.load(str(on / "disagreement.npy"))
    own = np.load(str(on / "owner.npy"))
    assert dis.shape == (1024, 752)
    assert own.shape == (1024, 752)
    assert int((own == -1).sum()) == 628883
    assert int((own >= 0).sum()) == 141165
    assert int((dis > 0).sum()) == 122439
    assert int(((own >= 0) & (dis > 0)).sum()) == 121112
    rc, out, err = run_py("region_disagreement.py", [
        "--tree", str(root),
        "--mode", "s3_off",
        "--figure-only",
        "--views", "0",
    ])
    assert rc == 0, "%s\n%s" % (out, err)
    assert "141165" in out, out
