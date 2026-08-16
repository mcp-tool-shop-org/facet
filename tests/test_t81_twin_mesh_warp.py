"""T81 - the twin-to-mesh warp instrument (E45 task 2).

The instrument is tools/twin_mesh_warp.py. It has no pass condition and grades
nothing, so what has to be tested is that its READINGS mean what they claim: the
sign, the origin, the scope floor's locality, the pinning flag, and that Gate C
can fire.

TWO PROPERTIES ARE PINNED HERE BECAUSE THEY ARE THE ONES THAT COULD BE SILENTLY
WRONG.

  the SIGN. `flow(px,py) = (dx,dy)` means the mesh structure at (px,py) is found in
  the twin at (px+dx, py+dy) - the Grok brief's convention. An inverted sign
  produces a plausible, well-formed, exactly-wrong field, and no aggregate
  statistic would notice.

  the LIMIT OF PINNING. Pinning detects an out-of-window peak only while the
  correlation surface still slopes toward it. On a rapidly decorrelating field a
  large true offset reads as a random IN-window peak with low confidence instead.
  The measurement's stopping rule depends on this, so it is a test rather than a
  remark.
"""
import os
import subprocess
import sys

import numpy as np
import pytest

from conftest import REPO, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import twin_mesh_warp as TW  # noqa: E402


def test_t81_selftest_exits_zero():
    rc, out, err = run_py("twin_mesh_warp.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "selftest OK" in out, out


# ---------------------------------------------------------------------------
# the sign and the origin
# ---------------------------------------------------------------------------

def test_t81_a_field_against_itself_reads_exactly_zero():
    f = TW.fixture_texture()
    res = TW.correlate_tiles(f, f, 16, tile=32, stride=16)
    sel = res["in_scope"]
    assert sel.any()
    assert (res["dx_int"][sel] == 0).all()
    assert (res["dy_int"][sel] == 0).all()
    assert res["peak"][sel].min() > 0.999


@pytest.mark.parametrize("sdx,sdy", [(5, 0), (-5, 0), (0, 6), (0, -6), (4, -7)])
def test_t81_an_injected_shift_reads_back_with_the_declared_sign(sdx, sdy):
    """`shift_image(f, dx, dy)` moves CONTENT by (+dx, +dy); the reading must be
    (+dx, +dy). A sign inversion passes every magnitude statistic and fails here."""
    f = TW.fixture_texture()
    moved = TW.shift_image(f, sdx, sdy)
    res = TW.correlate_tiles(f, moved, 16, tile=32, stride=16)
    m = 16 + max(abs(sdx), abs(sdy))
    H, W = f.shape
    sel = (res["in_scope"] & (res["row0"] >= m) & (res["row0"] + 32 <= H - m)
           & (res["col0"] >= m) & (res["col0"] + 32 <= W - m))
    assert sel.sum() >= 8, "only %d interior tiles" % int(sel.sum())
    assert np.all(np.abs(res["dx"][sel] - sdx) < 0.5), (
        "dx read %r for an injected %+d" % (np.unique(np.round(res["dx"][sel], 2)),
                                            sdx))
    assert np.all(np.abs(res["dy"][sel] - sdy) < 0.5)


def test_t81_the_sign_test_can_fail():
    """If the reading were inverted it must NOT also satisfy the assertion above,
    or the parametrised test proves nothing."""
    f = TW.fixture_texture()
    moved = TW.shift_image(f, 5, 0)
    res = TW.correlate_tiles(f, moved, 16, tile=32, stride=16)
    sel = res["in_scope"] & (res["col0"] > 48) & (res["col0"] < 96)
    assert sel.any()
    assert not np.all(np.abs(res["dx"][sel] + 5.0) < 0.5), (
        "a +5 shift also satisfies the -5 assertion - the test cannot fail")


# ---------------------------------------------------------------------------
# scope: the floor is a fraction of the tile's OWN area
# ---------------------------------------------------------------------------

def test_t81_the_scope_floor_is_local_not_global():
    H = W = 96
    cnt = np.zeros((H, W), dtype=bool)
    area = np.zeros((H, W), dtype=bool)
    cnt[0:32, 0:9] = True
    area[0:32, 0:32] = True
    f = TW.fixture_texture(H, W, seed=1)
    tight = TW.correlate_tiles(f, f, 8, tile=32, stride=32, scope_count=cnt,
                               scope_area=area, edge_frac=0.5, edge_abs=8)
    loose = TW.correlate_tiles(f, f, 8, tile=32, stride=32, scope_count=cnt,
                               scope_area=area, edge_frac=0.2, edge_abs=8)
    assert tight["area_px"][0] == 1024 and tight["count_px"][0] == 288
    assert tight["floor_px"][0] == 512.0
    assert not tight["in_scope"][0], "288 px cleared a 512 px floor"
    assert loose["in_scope"][0], "288 px did not clear a 204.8 px floor"


def test_t81_the_absolute_floor_stops_a_tiny_tile_qualifying():
    """A tile with almost no figure in it has a tiny fractional floor; the
    absolute floor is what keeps it out."""
    H = W = 64
    cnt = np.zeros((H, W), dtype=bool)
    area = np.zeros((H, W), dtype=bool)
    cnt[0, 0:3] = True        # 3 "edge" px
    area[0, 0:20] = True      # 20 px of figure -> fractional floor 0.2
    f = TW.fixture_texture(H, W, seed=2)
    r = TW.correlate_tiles(f, f, 8, tile=32, stride=32, scope_count=cnt,
                           scope_area=area, edge_frac=0.01, edge_abs=8)
    assert r["floor_px"][0] == 8.0
    assert not r["in_scope"][0], (
        "3 edge px entered scope on a 0.2 px fractional floor - the absolute "
        "floor is not applied")


def test_t81_every_tile_is_returned_regardless_of_scope():
    """The filter must be a column, not a deletion, or it cannot be re-cut
    without re-running."""
    f = TW.fixture_texture(96, 96, seed=3)
    cnt = np.zeros((96, 96), dtype=bool)
    cnt[:8, :8] = True
    r = TW.correlate_tiles(f, f, 8, tile=32, stride=32, scope_count=cnt,
                           scope_area=np.ones((96, 96), dtype=bool))
    # 96 px, tile 32, stride 32 -> origins 0, 32, 64 on each axis = 3 x 3
    assert r["grid"] == [3, 3]
    assert r["n_tiles"] == 9
    assert len(r["dx"]) == 9
    assert r["in_scope"].sum() < r["n_tiles"], "the fixture must exclude something"


# ---------------------------------------------------------------------------
# pinning, and its limit
# ---------------------------------------------------------------------------

def test_t81_an_out_of_window_offset_pins_when_the_surface_still_slopes():
    f = TW.fixture_texture(sigma=6.0)
    moved = TW.shift_image(f, 20, 0)
    narrow = TW.correlate_tiles(f, moved, 8, tile=32, stride=16)
    sel = narrow["in_scope"] & (narrow["col0"] > 40) & (narrow["col0"] < 96)
    assert sel.any()
    assert narrow["pinned"][sel].mean() > 0.5, (
        "a 20 px offset in an 8 px window pinned only %.2f of tiles"
        % float(narrow["pinned"][sel].mean()))
    wide = TW.correlate_tiles(f, moved, 32, tile=32, stride=16)
    selw = wide["in_scope"] & (wide["col0"] > 40) & (wide["col0"] < 96)
    assert not wide["pinned"][selw].any(), "widening did not clear the pinning"


def test_t81_pinning_is_not_a_complete_out_of_window_detector():
    """THE LIMIT, pinned as a test because the measurement's stopping rule leans
    on it. On a rapidly decorrelating field a 20 px offset inside an 8 px window
    pins only a minority of tiles - the rest report a random in-window peak. So
    "no tile pins" does not mean "the window is wide enough", and the peak value
    is the other half of that reading."""
    f = TW.fixture_texture(sigma=1.0)
    moved = TW.shift_image(f, 20, 0)
    r = TW.correlate_tiles(f, moved, 8, tile=32, stride=16)
    sel = r["in_scope"] & (r["col0"] > 40) & (r["col0"] < 96)
    assert sel.any()
    frac = float(r["pinned"][sel].mean())
    assert frac < 0.5, (
        "pinning caught %.2f of tiles on a short-correlation field; if this "
        "ever becomes a complete detector, the caveat in the module docstring "
        "and in E45's report is stale and must be re-read" % frac)
    assert float(r["peak"][sel].max()) < 0.9, (
        "an out-of-window offset produced a high-confidence in-window peak; "
        "the peak value is then not the second signal it is claimed to be")


# ---------------------------------------------------------------------------
# the interior leg's mesh side
# ---------------------------------------------------------------------------

def test_t81_interior_edges_exclude_the_outline_and_keep_the_crease():
    sil = np.zeros((32, 32), dtype=bool)
    sil[8:24, 8:24] = True
    outline = TW.silhouette_edge(sil)
    dedge = outline.copy()
    dedge[15:17, 12:20] = True
    inner = TW.interior_depth_edge(dedge, sil)
    assert not (inner & outline).any(), "the outline survived into the interior set"
    assert inner[15, 14], "the internal crease was removed with the outline"
    assert inner.sum() < dedge.sum()


def test_t81_silhouette_edge_marks_both_sides_of_the_cut():
    sil = np.zeros((8, 8), dtype=bool)
    sil[:, 4:] = True
    e = TW.silhouette_edge(sil)
    assert e[0, 3] and e[0, 4], "the cut is not marked on both sides"
    assert not e[0, 0] and not e[0, 7]


# ---------------------------------------------------------------------------
# the twin-side field
# ---------------------------------------------------------------------------

def test_t81_the_twin_field_registers_an_isoluminant_chroma_edge():
    """An L*-only field misses this entirely. A gold plate against a wine tunic
    can be near-isoluminant, which is exactly the material boundary class the
    measurement is about."""
    left = np.array([0.55, 0.42, 0.42])

    def lstar(rgb):
        return float(TW.srgb_to_lab(np.asarray(rgb).reshape(1, 1, 3))[0, 0, 0])

    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if lstar([0.44, mid, 0.44]) < lstar(left):
            lo = mid
        else:
            hi = mid
    right = np.array([0.44, 0.5 * (lo + hi), 0.44])
    img = np.zeros((32, 32, 3), dtype=np.float64)
    img[:, :16] = left
    img[:, 16:] = right
    lab = TW.srgb_to_lab(img)
    assert abs(float(lab[0, 0, 0] - lab[0, 31, 0])) < 0.05, "fixture not isoluminant"
    f = TW.twin_edge_field(img, sigma=0.0)
    assert f[:, 15:17].max() > 5.0 * max(f[:, 2:6].max(), 1e-6)


def test_t81_an_l_star_only_field_would_miss_it():
    """The discriminator: the same fixture measured on L* alone must NOT show the
    edge, or the previous test does not demonstrate the chroma channels matter."""
    from scipy.ndimage import sobel
    left = np.array([0.55, 0.42, 0.42])

    def lstar(rgb):
        return float(TW.srgb_to_lab(np.asarray(rgb).reshape(1, 1, 3))[0, 0, 0])

    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if lstar([0.44, mid, 0.44]) < lstar(left):
            lo = mid
        else:
            hi = mid
    img = np.zeros((32, 32, 3), dtype=np.float64)
    img[:, :16] = left
    img[:, 16:] = np.array([0.44, 0.5 * (lo + hi), 0.44])
    L = TW.srgb_to_lab(img)[..., 0]
    gl = np.hypot(sobel(L, axis=1, mode="nearest"), sobel(L, axis=0, mode="nearest"))
    full = TW.twin_edge_field(img, sigma=0.0)
    assert gl[:, 15:17].max() < 0.05 * full[:, 15:17].max(), (
        "the L*-only gradient also sees this edge (%.4f vs %.4f), so the fixture "
        "does not separate the two fields" % (gl[:, 15:17].max(),
                                              full[:, 15:17].max()))


# ---------------------------------------------------------------------------
# Gate C
# ---------------------------------------------------------------------------

def test_t81_gate_c_holds_on_a_field_it_should_hold_on():
    f = TW.fixture_texture()
    rep = TW.gate_c(f, [(3, 0), (0, -5)], radius=16, tile=32, stride=16,
                    label="t81")
    assert len(rep["legs"]) == 3
    assert rep["legs"][0]["leg"] == "null"
    assert rep["legs"][0]["tiles_with_nonzero_integer_peak"] == 0


def test_t81_gate_c_fires_on_a_field_with_no_information_in_one_axis():
    """THE GATE MUST BE ABLE TO FIRE. Horizontal stripes carry no x information,
    so an x-shift of them is unrecoverable and gate_c must halt rather than
    report a confident wrong number."""
    H = W = 160
    y = np.arange(H)[:, None].astype(np.float64)
    f = ((0.5 + 0.5 * np.sin(y / 5.0)) * np.ones((1, W))).astype(np.float32)
    with pytest.raises(TW.Andon):
        TW.gate_c(f, [(5, 0)], radius=16, tile=32, stride=16, label="t81 probe")


def test_t81_gate_c_is_not_a_bare_assert():
    """-O and PYTHONOPTIMIZE=1 delete `assert`. 278 sites in this repo were
    converted on that fact (E21 Ruling 2 / E22)."""
    src = (
        "import sys\n"
        "sys.path.insert(0, %r)\n"
        "import numpy as np\n"
        "import twin_mesh_warp as TW\n"
        "H = W = 160\n"
        "y = np.arange(H)[:, None].astype(np.float64)\n"
        "f = ((0.5 + 0.5 * np.sin(y / 5.0)) * np.ones((1, W))).astype(np.float32)\n"
        "try:\n"
        "    TW.gate_c(f, [(5, 0)], radius=16, tile=32, stride=16, label='p')\n"
        "except TW.Andon:\n"
        "    sys.exit(7)\n"
        "sys.exit(0)\n" % os.path.join(str(REPO), "tools"))
    for flags, opt in (([], None), (["-O"], None), ([], "1")):
        env = dict(os.environ)
        env.pop("PYTHONOPTIMIZE", None)
        if opt is not None:
            env["PYTHONOPTIMIZE"] = opt
        p = subprocess.run([sys.executable] + flags + ["-c", src],
                           capture_output=True, env=env, timeout=900)
        assert p.returncode == 7, (
            "gate_c did not fire under flags=%r PYTHONOPTIMIZE=%r (rc %d): %s"
            % (flags, opt, p.returncode, p.stderr.decode("ascii", "replace")))


def test_t81_the_null_leg_tolerance_is_the_inject_tolerance():
    """E45 measured the sub-pixel estimator's own floor at 0.0187 px on the
    synthetic fixture and 0.067-0.217 px on real twins. The null leg gates the
    INTEGER peak (exactly zero by construction) and reuses the dispatch's 0.5 px
    for the sub-pixel residual rather than inventing a constant after the fact."""
    assert TW.NULL_TOL_PX == TW.INJECT_TOL_PX == 0.5


# ---------------------------------------------------------------------------
# the cross-modal delta is structurally near-vacuous, and says so
# ---------------------------------------------------------------------------

def test_t81_shifting_the_search_field_translates_the_correlation_surface():
    """THE MECHANISM E45'S WARNING RESTS ON, tested exactly rather than by a rate.

    Shifting the search field by (dx, dy) translates the whole ZNCC surface by
    (dx, dy) - independently of whether the template has anything to do with the
    search field. So a cross-modal delta that "recovers the injected shift"
    recovers it from ANY dominant peak, real correspondence or stable artefact.
    That is why E45 reports its 96-100% delta recovery as a diagnostic and leans
    on the wrong-pairing control for the cross-modal evidence.

    The template here is unrelated noise, which is the point: if the identity
    below held only for a matching template, the warning would be wrong.
    """
    import cv2
    from scipy.ndimage import gaussian_filter
    rng = np.random.default_rng(11)
    twin = TW.fixture_texture(200, 200, seed=5)
    unrelated = gaussian_filter(rng.normal(size=(32, 32)), 1.0).astype(np.float32)
    R, sdx, sdy = 16, 6, -3
    r0 = c0 = 80                       # far from every frame edge and the zero band
    base_reg = twin[r0 - R:r0 + 32 + R, c0 - R:c0 + 32 + R]
    moved = TW.shift_image(twin, sdx, sdy)
    moved_reg = moved[r0 - R:r0 + 32 + R, c0 - R:c0 + 32 + R]
    a = cv2.matchTemplate(base_reg, unrelated, cv2.TM_CCOEFF_NORMED)
    b = cv2.matchTemplate(moved_reg, unrelated, cv2.TM_CCOEFF_NORMED)
    n = a.shape[0]
    # b[i, j] must equal a[i - sdy, j - sdx] wherever both indices exist
    i0, i1 = max(0, sdy), min(n, n + sdy)
    j0, j1 = max(0, sdx), min(n, n + sdx)
    lhs = b[i0:i1, j0:j1]
    rhs = a[i0 - sdy:i1 - sdy, j0 - sdx:j1 - sdx]
    assert lhs.shape == rhs.shape and lhs.size > 100
    assert np.allclose(lhs, rhs, rtol=0.0, atol=1e-5), (
        "the surface did not translate: max |diff| %.3e" % float(np.abs(lhs - rhs).max()))
    # can-fail: the identity must NOT hold for a wrong claimed shift
    i0b, i1b = max(0, sdy + 1), min(n, n + sdy + 1)
    j0b, j1b = max(0, sdx), min(n, n + sdx)
    lhs2 = b[i0b:i1b, j0b:j1b]
    rhs2 = a[i0b - sdy - 1:i1b - sdy - 1, j0b - sdx:j1b - sdx]
    assert not np.allclose(lhs2, rhs2, rtol=0.0, atol=1e-5), (
        "the surface also matches a one-pixel-wrong translation, so this test "
        "cannot distinguish the right shift from a neighbouring one")


def test_t81_the_delta_leg_is_weaker_than_it_looks_on_an_unrelated_template():
    """The rate half of the same warning, measured rather than asserted.

    With an unrelated template the delta still recovers a large majority of tiles
    (the surface translates), but materially less than the 96-100% E45 measured on
    real data - because a near-random surface lets a value newly entering the
    window beat the translated peak, while a dominant real peak is not beaten.
    Both halves are reported in E45; neither is offered as evidence about the
    twin-to-mesh correspondence.
    """
    from scipy.ndimage import gaussian_filter
    rng = np.random.default_rng(11)
    twin = TW.fixture_texture(160, 160, seed=5)
    unrelated = gaussian_filter(rng.normal(size=(160, 160)), 1.0).astype(np.float32)
    d = TW.cross_modal_delta(unrelated, twin, [(6, -3)], 16, tile=32, stride=16)
    row = d["rows"][0]
    assert row["tiles"] > 20
    assert 0.4 < row["frac_within_1px"] < 0.96, (
        "an unrelated template recovered %.2f of the injected shift; outside "
        "0.40-0.96 the warning E45 attaches to this leg needs re-reading"
        % row["frac_within_1px"])
