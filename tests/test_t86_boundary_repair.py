"""T86 - atlas-space material-boundary repair.

The instrument is tools/boundary_repair.py. Every number below is known
by construction except the artifacts replay, which re-reads E45 surfid
and the E06 prep mask.

A near-boundary rewrite that eats a 2 px bar, a hue applied below the
chroma floor, a sleeve grown by snapping mix to green, a drifted
to_lab, or a bare assert fails at least one leg.

Hermetic tests do not open facet_E45 / facet_E06. The artifacts leg does,
read-only.
"""
import ast
import os
import sys

import numpy as np
import pytest

from conftest import REPO, need, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import boundary_repair as B  # noqa: E402

PAL = os.path.join(str(REPO), "docs", "experiments", "E08-W3-palette.json")


def _bands():
    _pal, bands, cmin = B.load_palette(PAL)
    return bands, cmin


def test_t86_selftest_exits_zero():
    rc, out, err = run_py("boundary_repair.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "out[8,15] == (180, 90, 50)" in out, out
    assert "thin bar held" in out, out
    assert "steel held" in out, out


def test_t86_calibration_mix_snaps_warm_not_green():
    bands, cmin = _bands()
    rgb, valid = B.fixture_calibration()
    out, rep = B.repair(rgb, valid, bands, cmin, sleeveless=True)
    got = tuple(int(v) for v in out[B.CALIBRATION_Y, B.CALIBRATION_X])
    assert got == B.WARM_RGB, got
    # the green-side mix must be refused or the tunic grows
    refused = tuple(int(v) for v in out[B.CALIBRATION_Y, 17])
    assert refused == B.MIX_RGB, refused
    assert rep["green_out"] <= rep["green_in"]
    assert rep["refused_green_growth"] > 0


def test_t86_thin_green_bar_survives():
    """Can-fail: a distance-to-boundary rewrite eats a 2 px structure."""
    bands, cmin = _bands()
    rgb, valid = B.fixture_calibration()
    out, _rep = B.repair(rgb, valid, bands, cmin, sleeveless=True)
    assert np.array_equal(out[28:30, 2:10], rgb[28:30, 2:10])


def test_t86_steel_below_chroma_floor_is_untouched():
    """Can-fail: treating hue as a colour on steel recolours the bar."""
    bands, cmin = _bands()
    rgb, valid = B.fixture_calibration()
    out, _rep = B.repair(rgb, valid, bands, cmin, sleeveless=True)
    assert np.array_equal(out[2:4, 2:10], rgb[2:4, 2:10])
    assert tuple(int(v) for v in out[2, 4]) == B.STEEL_RGB


def test_t86_sleeveless_andon_if_green_grows():
    """Can-fail: dropping the sleeveless check lets mix become a sleeve."""
    bands, cmin = _bands()
    rgb, valid = B.fixture_calibration()
    out_on, rep_on = B.repair(rgb, valid, bands, cmin, sleeveless=True)
    out_off, rep_off = B.repair(rgb, valid, bands, cmin, sleeveless=False)
    assert rep_on["green_out"] <= rep_on["green_in"]
    assert tuple(int(v) for v in out_on[8, 17]) == B.MIX_RGB
    # without the rule the green-side mix becomes green
    assert tuple(int(v) for v in out_off[8, 17]) == B.GREEN_RGB
    assert rep_off["green_out"] > rep_on["green_out"]


def test_t86_to_lab_is_palette_gate():
    theirs = B.palette_gate_to_lab_source()
    x = np.linspace(0.0, 1.0, 24, dtype=np.float64).reshape(2, 4, 3)
    assert np.array_equal(B.to_lab(x), theirs(x))


def test_t86_circular_hue_not_arithmetic_median():
    """Can-fail: arithmetic median of 350 and 10 is 180; circular is ~0."""
    # two unit chromatic vectors on either side of the wrap
    lab = np.zeros((2, 1, 3), dtype=np.float64)
    lab[0, 0, 1] = np.cos(np.deg2rad(350.0))
    lab[0, 0, 2] = np.sin(np.deg2rad(350.0))
    lab[1, 0, 1] = np.cos(np.deg2rad(10.0))
    lab[1, 0, 2] = np.sin(np.deg2rad(10.0))
    mask = np.ones((2, 1), dtype=bool)
    circ = B.circular_hue_deg(lab, mask)
    arith = float(np.median([350.0, 10.0]))
    assert arith == 180.0
    assert circ is not None
    # 0 degrees, wrapped; allow a degree
    wrapped = min(circ, 360.0 - circ)
    assert wrapped <= 1.0, circ


def test_t86_surfid_roundtrip():
    sid = np.array([[-1, 0, 4096, 4096 * 4095 + 4095]], dtype=np.int64)
    row, col = B.decode_surfid(sid, atlas_res=4096)
    assert int(row[0, 1]) == 0 and int(col[0, 1]) == 0
    assert int(row[0, 2]) == 1 and int(col[0, 2]) == 0
    assert int(row[0, 3]) == 4095 and int(col[0, 3]) == 4095
    assert int(row[0, 0]) == -1


def test_t86_writes_beside_not_over(tmp_path):
    bands, cmin = _bands()
    rgb, valid = B.fixture_calibration()
    src = tmp_path / "atlas.png"
    dst = tmp_path / "repaired.png"
    mask_p = tmp_path / "mask.npy"
    B.write_png(str(src), rgb)
    np.save(str(mask_p), valid.astype(np.uint8) * 255)
    rc, out, err = run_py("boundary_repair.py", [
        "--atlas", str(src),
        "--mask", str(mask_p),
        "--palette", PAL,
        "--out", str(src),
    ])
    assert rc == 2
    assert "must not be --atlas" in err
    rc, out, err = run_py("boundary_repair.py", [
        "--atlas", str(src),
        "--mask", str(mask_p),
        "--palette", PAL,
        "--out", str(dst),
    ])
    assert rc == 0, "%s\n%s" % (out, err)
    assert dst.is_file()
    reread = np.asarray(B.load_atlas(str(src)))
    assert np.array_equal(reread, rgb)


def test_t86_missing_atlas_andon(tmp_path):
    rc, out, err = run_py("boundary_repair.py", [
        "--atlas", str(tmp_path / "no.png"),
        "--mask", str(tmp_path / "no.npy"),
        "--out", str(tmp_path / "o.png"),
    ])
    assert rc == 2
    assert "ANDON" in err


def test_t86_no_andon_is_a_bare_assert():
    src = open(os.path.join(str(REPO), "tools", "boundary_repair.py"),
               encoding="utf-8").read()
    tree = ast.parse(src)
    bares = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    assert bares == [], "bare assert at lines %s" % bares


@pytest.mark.artifacts
def test_t86_e45_surfid_is_row_times_4096_plus_col(assets):
    """The brief's cited mechanism, re-measured on all 8 views."""
    aov = need(assets, "facet_E45/aov")
    prep = need(assets, "facet_E06/C1/prep")
    mask = np.load(str(prep / "mask.npy"))
    valid = mask[..., 0] > 0.5 if mask.ndim == 3 else mask > 0.5
    assert valid.shape == (4096, 4096)
    for i in range(8):
        sid = np.load(str(aov / ("view_%d" % i) / "surfid.npy"))
        row, col = B.decode_surfid(sid, atlas_res=4096)
        hit = sid >= 0
        assert int(hit.sum()) > 0
        # invertibility is the ANDON inside decode_surfid
        rr = row[hit]
        cc = col[hit]
        inside = valid[rr, cc]
        # gutter / rounding: a few unique IDs miss the prep mask
        miss = float((~inside).sum()) / float(inside.size)
        assert miss < 0.01, "view %d mask-miss %s" % (i, miss)
