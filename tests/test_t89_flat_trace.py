"""T89 - trace a render flat to the twin that painted it.

The instrument is tools/flat_trace.py. Same-xy comparison to the
render view's twin is the wrong plate unless that view owns the texel.

A tool that only compares same-xy, a fixture that cannot tell the
two twins apart, or a bare assert fails at least one leg.

Hermetic tests do not open facet_E45 / E49. The artifacts leg does,
read-only.
"""
import ast
import os
import sys

import numpy as np
import pytest

from conftest import REPO, need, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import flat_trace as F  # noqa: E402
import atlas_from_aovs as A  # noqa: E402


def test_t89_selftest_exits_zero():
    rc, out, err = run_py("flat_trace.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "owner-twin == (180, 90, 50)" in out, out
    assert "same-xy is not" in out, out


def test_t89_fixture_owner_twin_is_not_same_xy():
    """Can-fail: comparing only same-xy would call the front plate the source."""
    fx = F.fixture_calibration()
    P = A.decode_pos(fx["pos"], fx["meta"])
    tr = F.trace_pixels(
        np.array([8]), np.array([8]),
        fx["surfid"], fx["owner"], P, fx["cams"], fx["twins"],
        render_view=0)
    assert int(tr["owner"][0]) == 1
    assert tuple(int(c) for c in tr["owner_twin"][0]) == F.OLIVE_TWIN_RGB
    assert tuple(int(c) for c in tr["same_xy_twin"][0]) != F.OLIVE_TWIN_RGB


def test_t89_olive_spec_is_not_the_e50_box():
    """The box is a window. The spec is the colour predicate."""
    im = np.zeros((16, 16, 3), dtype=np.uint8)
    im[2, 2] = (120, 140, 80)
    im[10, 10] = (20, 50, 40)
    m = F.olive_mask(im)
    assert bool(m[2, 2])
    assert not bool(m[10, 10])
    m2 = F.olive_mask(im, box=(0, 5, 0, 5))
    assert bool(m2[2, 2])
    assert not bool(m2[10, 10])


def test_t89_missing_twin_andon(tmp_path):
    with pytest.raises(F.Andon, match="no twin"):
        F.load_twins(str(tmp_path))


def test_t89_no_andon_is_a_bare_assert():
    src = open(os.path.join(str(REPO), "tools", "flat_trace.py"),
               encoding="utf-8").read()
    tree = ast.parse(src)
    bares = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    assert bares == [], "bare assert at lines %s" % bares


@pytest.mark.artifacts
def test_t89_collar_olive_is_owned_by_view_6(assets):
    """The shaping number: 115 olive px, 97 owned by view 6."""
    rend_p = need(assets, "facet_E49/renders_owner_complete")
    aov = need(assets, "facet_E49/aov_eroded/view_0")
    atlas = need(assets, "facet_E49/atlas_owner_eroded")
    from PIL import Image
    rend = np.asarray(Image.open(
        str(rend_p / "owner_complete_0.png")).convert("RGB"))
    surfid = np.load(str(aov / "surfid.npy"))
    owner = np.load(str(atlas / "owner.npy"))
    m = F.olive_mask(rend, box=F.CALIBRATION_BOX)
    assert int(m.sum()) == F.CALIBRATION_OLIVE_N
    ys, xs = np.where(m)
    sil, row, col = F.decode_surfid(surfid)
    ow = owner[row[ys, xs], col[ys, xs]]
    assert int((ow == 6).sum()) == F.CALIBRATION_OWNER6
    assert int((ow == 0).sum()) < int((ow == 6).sum())
