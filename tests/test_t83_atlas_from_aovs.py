"""T83 - rebuild the atlas from an AOV bundle (flow optional).

The instrument is tools/atlas_from_aovs.py. Every number below is known
by construction except the real-data anchor, which replays the recorded
E06 prep + E45 cams pairing T50 already pinned.

A forgotten flow, a flipped sign, a dropped *0.5 on the unit-cube
decode, or a hidden texel that still paints, fails at least one leg.

Hermetic tests do not open the E45 bundle. The artifacts leg does.
"""
import ast
import os
import sys

import numpy as np
import pytest

from conftest import REPO, need, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import atlas_from_aovs as A  # noqa: E402


def test_t83_selftest_exits_zero():
    rc, out, err = run_py("atlas_from_aovs.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "atlas[16,16,0] == 0.5" in out, out


def test_t83_calibration_atlas_red_is_half():
    pos, nor, mask, meta, views = A.fixture_sign(32, shift=3)
    atlas, _o, _w, _p = A._paint_prep(pos, nor, mask, meta, views)
    got = float(atlas[A.CALIBRATION_ROW, A.CALIBRATION_COL, 0])
    assert got == pytest.approx(A.CALIBRATION_RED, abs=1e-12), (
        "CALIBRATION: atlas[%d,%d,0] is %r, not 0.5 "
        "(forgotten flow is 0.40625; flipped sign is 0.3125)"
        % (A.CALIBRATION_ROW, A.CALIBRATION_COL, got))


def test_t83_flow_off_degrades_flow_on_recovers():
    pos, nor, mask, meta, off, on, truth = A.fixture_flow_ab(32, shift=3)
    a_off, _, _, _ = A._paint_prep(pos, nor, mask, meta, [off])
    a_on, _, _, _ = A._paint_prep(pos, nor, mask, meta, [on])
    a_true, _, _, _ = A._paint_prep(pos, nor, mask, meta, [truth])
    sl = (slice(4, 28), slice(4, 28), 0)
    err_off = float(np.max(np.abs(a_off[sl] - a_true[sl])))
    err_on = float(np.max(np.abs(a_on[sl] - a_true[sl])))
    assert err_off >= 0.05, err_off
    assert err_on <= 1e-12, err_on


def test_t83_occlusion_hidden_texel_takes_nothing():
    pos, nor, mask, meta, views = A.fixture_occlusion(32)
    _atlas, owner, _w, painted = A._paint_prep(pos, nor, mask, meta, views)
    assert int(painted["written"].sum()) == 0
    assert int(np.max(owner)) == -1


def test_t83_unit_cube_decode_is_half():
    meta = {"lo": [0.0, 0.0, 0.0], "hi": [2.0, 2.0, 2.0], "maxabs": 2.0}
    P = A.decode_pos(np.array([[[1.0, 1.0, 1.0]]]), meta)
    assert float(P[0, 0, 0]) == 0.5
    # the two one-factor mistakes both land on 1.0
    raw = (1.0 * 2.0 + 0.0)
    assert raw / 2.0 == 1.0
    assert raw * 0.5 == 1.0


def test_t83_empty_views_and_bad_maxabs_andon():
    with pytest.raises(A.Andon, match="maxabs"):
        A.decode_pos(np.zeros((1, 1, 3)),
                     {"lo": [0, 0, 0], "hi": [1, 1, 1], "maxabs": 0})
    with pytest.raises(A.Andon, match="no views"):
        A.paint(np.zeros((1, 3)), np.zeros((1, 3)), [])


def test_t83_no_andon_is_a_bare_assert():
    src = open(os.path.join(str(REPO), "tools", "atlas_from_aovs.py"),
               encoding="utf-8").read()
    tree = ast.parse(src)
    bares = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    assert bares == [], "bare assert at lines %s" % bares


@pytest.mark.artifacts
def test_t83_real_decode_matches_cams_frame(assets):
    """T50's prep + E45 cams. Mesh-frame extents match cams inside float32;
    decoded valid texels stay inside that mesh AABB."""
    prep = need(assets, "facet_E06/C1/prep")
    aov = need(assets, "facet_E45/aov")
    rc, out, err = run_py(
        "atlas_from_aovs.py",
        ["--anchor", "--aov", str(aov), "--prep", str(prep)])
    assert rc == 0, "anchor exited %d\n%s\n%s" % (rc, out, err)
    assert "anchor OK" in out, out
    assert "|bmid|=0.000e+00" in out or "|bmid|=0.00e+00" in out, out
