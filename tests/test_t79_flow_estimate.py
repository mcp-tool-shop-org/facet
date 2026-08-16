"""T79 - flow estimator for the s3_composite hook.

The instrument is tools/flow_estimate.py. Every number below is known by
construction. A sign-flipped stand-in, a confident tangent, or a 0-flow
stand-in fails at least one leg.
"""
import ast
import os
import sys

import numpy as np
import pytest

from conftest import REPO, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import flow_estimate as F  # noqa: E402


def test_t79_selftest_exits_zero():
    rc, out, err = run_py("flow_estimate.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "3.0" in out, out


def test_t79_calibration_flow_x_is_plus_three():
    src, dst, sil = F.fixture_ramp_shift(64, shift=3)
    out = F.estimate_flow(src, dst, sil=sil, window=7)
    got = float(out["flow"][F.CALIBRATION_ROW, F.CALIBRATION_COL, 0])
    assert got == pytest.approx(F.CALIBRATION_FLOW_X, abs=1e-6), (
        "CALIBRATION: flow_x[%d,%d] is %r, not +3.0 (sign error is -3)"
        % (F.CALIBRATION_ROW, F.CALIBRATION_COL, got))


def test_t79_identity_reads_zero_flow_with_structure():
    src, dst, sil = F.fixture_identity_ramp(64)
    out = F.estimate_flow(src, dst, sil=sil, window=7)
    assert float(np.max(np.abs(out["flow"][8:-8, 8:-8]))) <= 0.05
    assert float(out["confidence_xy"][32, 32, 0]) >= 0.4


def test_t79_nosignal_is_identity_and_zero_confidence():
    src, dst, sil = F.fixture_flat(32)
    out = F.estimate_flow(src, dst, sil=sil, window=7)
    assert float(np.max(np.abs(out["flow"]))) <= 1e-6
    assert float(np.max(out["confidence"])) <= 1e-6


def test_t79_aperture_tangent_is_not_confident():
    src, dst, sil = F.fixture_vertical_edge_tangential(64, shift=4)
    out = F.estimate_flow(src, dst, sil=sil, window=7)
    cy = out["confidence_xy"][4:-4, 29:35, 1]
    assert float(np.median(cy)) <= 0.2
    fy = out["flow"][4:-4, 29:35, 1]
    confident = out["confidence_xy"][4:-4, 29:35, 1] > 0.5
    if confident.any():
        assert float(np.median(np.abs(fy[confident]))) <= 1.0


def test_t79_smooth_warp_recovered_within_half_pixel():
    src, dst, sil, ux = F.fixture_smooth_warp(64, amp=4.0)
    out = F.estimate_flow(src, dst, sil=sil, window=7)
    ok = sil & (out["confidence_xy"][..., 0] > 0.4)
    assert int(ok.sum()) >= 64
    med = float(np.median(np.abs(out["flow"][..., 0] - ux)[ok]))
    assert med <= 0.5, med


def test_t79_empty_sil_and_even_window_andon():
    src, dst, sil = F.fixture_flat(8)
    with pytest.raises(F.Andon, match="silhouette is empty"):
        F.estimate_flow(src, dst, sil=np.zeros_like(sil))
    with pytest.raises(F.Andon, match="odd"):
        F.estimate_flow(src, dst, window=4)


def test_t79_no_andon_is_a_bare_assert():
    src = open(os.path.join(str(REPO), "tools", "flow_estimate.py"),
               encoding="utf-8").read()
    tree = ast.parse(src)
    bares = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    assert bares == [], "bare assert at lines %s; -O deletes those" % bares
