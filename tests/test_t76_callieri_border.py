"""T76 - Callieri border mask, mixed-depth reject, facing weight.

The instrument is tools/callieri_border.py. Every number below is known by
construction on a synthetic fixture. A stand-in that returns all zeros, all
ones, a Gaussian, or an image-size-normalised EDT fails at least one.

Calibration (same claim as the module docstring): thin-bar medial weight
at (32, 32) is exactly 2/3.
"""
import ast
import os
import sys

import numpy as np
import pytest

from conftest import REPO, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import callieri_border as CB  # noqa: E402


def test_t76_selftest_exits_zero():
    rc, out, err = run_py("callieri_border.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "calibration" in out.lower() or "2/3" in out, out


def test_t76_calibration_thin_bar_medial_weight_is_two_thirds():
    depth, sil = CB.fixture_thin_bar()
    w = CB.border_weight(depth, sil)
    got = float(w[CB.CALIBRATION_RC, CB.CALIBRATION_CC])
    assert got == pytest.approx(CB.CALIBRATION_WEIGHT, abs=1e-6), (
        "CALIBRATION: (%d, %d) is %r, not 2/3. Image-size norm is ~2/64."
        % (CB.CALIBRATION_RC, CB.CALIBRATION_CC, got))


def test_t76_flat_plane_only_zeros_are_the_image_border():
    depth, sil = CB.fixture_flat_plane(32)
    w = CB.border_weight(depth, sil)
    edge = CB.depth_edge_mask(depth, silhouette=sil)
    assert float(w[16, 16]) == 1.0
    assert float(w[0, 16]) == 0.0
    assert float(w[16, 0]) == 0.0
    assert not edge.any()


def test_t76_step_edge_marks_the_known_column_only():
    depth, sil = CB.fixture_step_edge(32, col=16)
    edge = CB.depth_edge_mask(depth, silhouette=sil)
    assert edge[:, 15].all() and edge[:, 16].all()
    assert not edge[:, 8].any() and not edge[:, 24].any()
    rej = CB.mixed_depth_reject(depth, silhouette=sil)
    assert rej[10, 15]
    assert not rej[10, 4]


def test_t76_thin_bar_outline_is_zero_and_background_is_zero():
    depth, sil = CB.fixture_thin_bar()
    w = CB.border_weight(depth, sil)
    assert float(w[32, 30]) == 0.0
    assert float(w[32, 34]) == 0.0
    assert float(w[0, 0]) == 0.0
    edge = CB.depth_edge_mask(depth, silhouette=sil)
    assert edge[32, 30] and edge[32, 34]
    assert not edge[32, 32]


def test_t76_mixed_depth_is_not_the_border_weight():
    depth, sil = CB.fixture_thin_bar()
    w = CB.border_weight(depth, sil)
    rej = CB.mixed_depth_reject(depth, silhouette=sil)
    assert float(w[32, 32]) > 0.0
    assert not rej[32, 32]


def test_t76_ramp_is_not_an_edge():
    n = 32
    depth = np.tile(np.linspace(0.0, 1.0, n), (n, 1))
    sil = np.ones((n, n), dtype=bool)
    edge = CB.depth_edge_mask(depth, silhouette=sil)
    assert not edge.any()


def test_t76_facing_exponent_is_a_parameter():
    n = np.zeros((4, 4, 3), dtype=np.float64)
    n[..., 2] = 1.0
    assert np.allclose(CB.facing_weight(n, 6.0), 1.0)
    side = np.zeros_like(n)
    side[..., 0] = 1.0
    assert not CB.facing_weight(side, 6.0).any()
    g = np.zeros_like(n)
    s = np.sqrt(0.5)
    g[:] = (0.0, s, s)
    assert float(CB.facing_weight(g, 2.0)[0, 0]) == pytest.approx(0.5, abs=1e-6)


def test_t76_empty_silhouette_andon_fires():
    depth, sil = CB.fixture_flat_plane(8)
    with pytest.raises(CB.Andon, match="silhouette is empty"):
        CB.border_weight(depth, np.zeros_like(sil))


def test_t76_no_andon_is_a_bare_assert():
    src = open(os.path.join(str(REPO), "tools", "callieri_border.py"),
               encoding="utf-8").read()
    tree = ast.parse(src)
    bares = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            bares.append(node.lineno)
    assert bares == [], "bare assert at lines %s; -O deletes those" % bares


def test_t76_prefer_inf_background_nan_is_also_background():
    depth, sil = CB.fixture_thin_bar()
    w_inf = CB.border_weight(depth, sil)
    depth_nan = depth.copy()
    depth_nan[~sil] = np.nan
    w_nan = CB.border_weight(depth_nan, sil)
    assert np.allclose(w_inf, w_nan)
