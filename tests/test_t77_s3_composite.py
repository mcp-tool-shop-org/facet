"""T77 - S3 existence-proof compositor.

The instrument is tools/s3_composite.py. Every number below is known by
construction. A stand-in that skips reprojection, assigns owners per target,
or ignores flow fails at least one leg.
"""
import ast
import os
import sys

import numpy as np
import pytest

from conftest import REPO, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import s3_composite as S  # noqa: E402


def test_t77_selftest_exits_zero():
    rc, out, err = run_py("s3_composite.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "0.640625" in out, out


def test_t77_calibration_reprojected_red_is_0_640625():
    views = S.fixture_shift_pair(32)
    rec, valid = S.reproject_plate(views[0], views[1])
    assert valid[S.CALIBRATION_ROW, S.CALIBRATION_COL]
    got = float(rec[S.CALIBRATION_ROW, S.CALIBRATION_COL, 0])
    assert got == pytest.approx(S.CALIBRATION_RED, abs=1e-6), (
        "CALIBRATION: red[%d,%d] is %r, not %r"
        % (S.CALIBRATION_ROW, S.CALIBRATION_COL, got, S.CALIBRATION_RED))


def test_t77_reprojection_exact_on_linear_field():
    views = S.fixture_shift_pair(32)
    rec, valid = S.reproject_plate(views[0], views[1])
    sil = views[1]["sil"] & valid
    err = float(np.max(np.abs(rec[sil] - views[1]["twin"][sil])))
    assert err <= 1e-5, err


def test_t77_occluder_hides_the_back_plane():
    view = S.fixture_occluder(32)
    hidden = S.sample_view(view, np.array([-0.4, 0.0, 0.0]))
    assert not hidden["valid"]
    opened = S.sample_view(view, np.array([0.4, 0.0, 0.0]))
    assert opened["valid"]
    front = S.sample_view(view, np.array([-0.4, 0.0, 0.5]))
    assert front["valid"]


def test_t77_vi_agrees_at_every_shared_surfid_vd_differs():
    views = S.fixture_disagree_pair(32)
    r0 = S.s3_composite(views, 0)
    r1 = S.s3_composite(views, 1)
    sid0 = views[0]["surfid"]
    sid1 = views[1]["surfid"]
    shared = (set(sid0[sid0 >= 0].tolist()) & set(sid1[sid1 >= 0].tolist())
              & set(r0["assignment"]["surfid"].tolist()))
    assert len(shared) >= 16
    all_s = r0["assignment"]["surfid"]
    n_checked = 0
    for s in shared:
        p0 = np.argwhere((sid0 == s) & r0["coverage"])
        p1 = np.argwhere((sid1 == s) & r1["coverage"])
        if p0.size == 0 or p1.size == 0:
            continue
        assert np.allclose(r0["independent"][tuple(p0[0])],
                           r1["independent"][tuple(p1[0])], atol=1e-6)
        n_checked += 1
    assert n_checked >= 16
    sil = views[0]["sil"] & views[1]["sil"]
    vd_delta = float(np.max(np.abs(r0["dependent"][sil] - r1["dependent"][sil])))
    assert vd_delta >= 0.5, vd_delta


def test_t77_warp_disagreement_fires_in_tile_and_flow_recovers():
    views, (r0, r1, c0, c1, shift) = S.fixture_warp_pair(32, shift=6)
    raw = [views[0], dict(views[1])]
    raw[1]["flow"] = np.zeros_like(views[1]["flow"])
    off = S.s3_composite(raw, 0)
    on = S.s3_composite(views, 0)
    tile = np.zeros((32, 32), dtype=bool)
    tile[r0 + 1:r1 - 1, c0 + 1:c1 - 1 - shift] = True
    ring = np.ones((32, 32), dtype=bool)
    ring[r0:r1, c0:c1] = False
    outside = views[0]["sil"] & ring
    d_in = float(off["disagreement"][tile].mean())
    d_out = float(off["disagreement"][outside].mean())
    assert d_in > d_out + 1e-6
    assert d_out <= 1e-4
    P = views[0]["pos"]
    rec = S.sample_view(views[1], P)["colour"]
    ok = tile & S.sample_view(views[1], P)["valid"]
    err = float(np.max(np.abs(rec[ok] - views[0]["twin"][ok])))
    assert err <= 1e-4, err
    assert float(on["disagreement"][tile].mean()) < d_in


def test_t77_disagreement_is_zero_when_plates_agree():
    views = S.fixture_shift_pair(32)
    r = S.s3_composite(views, 0)
    sil = views[0]["sil"] & r["coverage"]
    assert float(r["disagreement"][sil].max()) <= 1e-5


def test_t77_out_of_range_target_andon():
    views = S.fixture_shift_pair(8)
    with pytest.raises(S.Andon, match="out of range"):
        S.s3_composite(views, 9)


def test_t77_no_andon_is_a_bare_assert():
    src = open(os.path.join(str(REPO), "tools", "s3_composite.py"),
               encoding="utf-8").read()
    tree = ast.parse(src)
    bares = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    assert bares == [], "bare assert at lines %s; -O deletes those" % bares
