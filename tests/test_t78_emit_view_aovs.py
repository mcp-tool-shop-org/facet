"""T78 - the per-view AOV emitter (E45 task 1).

The instrument is tools/emit_view_aovs.py. Every hermetic number below is known by
construction on a synthetic box; the artifacts tier replays two RECORDED cameras
against the silhouettes those cameras themselves produced.

WHY EACH LEG IS SHAPED AS A FAILURE. A silhouette gate returned 1.00000 IoU on a
mesh with a hole through it once in this repo, and a dilation comparison returned
0.00% by construction. So every leg here is shown failing on input built to fail
it, not merely agreeing with the tool as it happens to behave.

THE ELEVATED LEG IS THE ONE NOTHING ELSE COVERS. `silhouette_masks.py` takes no
elevation, so no recorded mask in `masks/` is an el != 0 camera. The only recorded
elevated silhouettes on this route are `state/job_y+{000,180}_e+55/hit.png`, and
until E45 nothing had re-derived a camera against them.
"""
import os
import subprocess
import sys

import numpy as np
import pytest

from conftest import REPO, need, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import emit_view_aovs as EA  # noqa: E402

ARMB = os.path.join("facet_E08", "ARMB")
W, H = 752, 1024


# ---------------------------------------------------------------------------
# the module's own constructions
# ---------------------------------------------------------------------------

def test_t78_selftest_exits_zero():
    rc, out, err = run_py("emit_view_aovs.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "selftest OK" in out, out


def test_t78_basis_at_el_zero_agrees_with_the_mask_tool():
    """silhouette_masks.py wrote every recorded mask. If the port drifts from its
    construction, no recorded mask anchors anything."""
    for yaw in (0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0):
        dtc, look, right, up = EA.basis(yaw, 0.0)
        wd, wl, wr, wu = EA.silhouette_masks_axes(yaw)
        assert np.allclose(dtc, wd, rtol=0.0, atol=1e-9), yaw
        assert np.allclose(look, wl, rtol=0.0, atol=1e-9), yaw
        assert np.allclose(right, wr, rtol=0.0, atol=1e-9), yaw
        assert np.allclose(up, wu, rtol=0.0, atol=1e-9), yaw


def test_t78_basis_comparison_can_fail():
    """The leg above must not pass for the wrong yaw, or it is comparing nothing."""
    dtc, _l, _r, _u = EA.basis(45.0, 0.0)
    wd, _wl, _wr, _wu = EA.silhouette_masks_axes(46.0)
    assert not np.allclose(dtc, wd, rtol=0.0, atol=1e-9), (
        "a one-degree yaw error compares equal - the tolerance is meaningless")


def test_t78_float32_ray_origins_match_the_mask_tools_construction():
    """THE PROPERTY THAT DECIDES whether a recorded mask can anchor this cast.

    The two constructions differ by ~1e-12 in float64 (both divide by
    `norm + 1e-12`, but they normalise different vectors). What matters is the
    grid open3d receives, which is float32.
    """
    for yaw in (0.0, 45.0, 90.0, 180.0, 315.0):
        cam = EA.make_cam(yaw, 0.0, [0.01, -0.02, 0.03], 1.1969748723526452,
                          0.8790284218839738, 64, 96)
        wd, wl, wr, wu = EA.silhouette_masks_axes(yaw)
        alt = dict(cam)
        alt["dtc"] = [float(x) for x in wd]
        alt["look"] = [float(x) for x in wl]
        alt["right"] = [float(x) for x in wr]
        alt["up"] = [float(x) for x in wu]
        a = EA.ray_origins(cam).astype(np.float32)
        b = EA.ray_origins(alt).astype(np.float32)
        assert np.array_equal(a, b), (
            "yaw %g: %d float32 origins differ" % (yaw, int((a != b).sum())))


def test_t78_float32_origin_equality_can_fail():
    """A perturbation the float32 grid CAN see must break the equality, or the
    leg above is vacuous. 1e-5 on `right` moves origins by ~4e-6 world units
    against a ~2.4e-7 float32 spacing at |origin| ~ 2."""
    cam = EA.make_cam(0.0, 0.0, [0.0, 0.0, 0.0], 1.2, 0.9, 32, 32)
    bad = dict(cam)
    bad["right"] = [cam["right"][0] + 1e-5, cam["right"][1], cam["right"][2]]
    a = EA.ray_origins(cam).astype(np.float32)
    c = EA.ray_origins(bad).astype(np.float32)
    assert not np.array_equal(a, c)


def test_t78_projection_is_the_declared_contract():
    cam = EA.make_cam(37.0, 22.0, [0.1, -0.2, 0.05], 1.0, 0.75, 64, 96)
    right = np.asarray(cam["right"])
    up = np.asarray(cam["up"])
    dtc = np.asarray(cam["dtc"])
    bmid = np.asarray(cam["bmid"])
    a, b, c = 0.21, -0.13, 0.07
    P = bmid + a * right + b * up - c * dtc
    px, py = EA.project(P, cam)
    assert px == pytest.approx((a / cam["h_ext"] + 0.5) * cam["W"] - 0.5, abs=1e-9)
    assert py == pytest.approx((0.5 - b / cam["v_ext"]) * cam["H"] - 0.5, abs=1e-9)
    assert float(EA.depth_of(P, cam)) == pytest.approx(c, abs=1e-9)


def test_t78_projection_check_can_fail_on_a_right_up_swap():
    cam = EA.make_cam(37.0, 22.0, [0.1, -0.2, 0.05], 1.0, 0.75, 64, 96)
    swapped = dict(cam)
    swapped["right"], swapped["up"] = cam["up"], cam["right"]
    P = np.asarray(cam["bmid"]) + 0.21 * np.asarray(cam["right"])
    assert EA.project(P, cam)[0] != pytest.approx(EA.project(P, swapped)[0], abs=1e-6)


def test_t78_reprojection_lands_on_its_own_pixel_centre():
    scene = EA.fixture_scene(0.25)
    cam = EA.make_cam(0.0, 0.0, [0.0, 0.0, 0.0], 1.0, 0.75, 96, 128)
    aov = EA.cast_view(scene, cam, atlas_res=64)
    ex, ey = EA.reprojection_error(aov["pos"], aov["sil"], cam)
    assert ex < EA.REPROJECT_TOL_PX and ey < EA.REPROJECT_TOL_PX, (ex, ey)


def test_t78_reprojection_check_can_fail_on_a_wrong_extent():
    """A 2% extent error is invisible in a silhouette comparison and enormous
    here - which is the whole reason the reprojection leg exists beside the
    anchor leg."""
    scene = EA.fixture_scene(0.25)
    cam = EA.make_cam(0.0, 0.0, [0.0, 0.0, 0.0], 1.0, 0.75, 96, 128)
    aov = EA.cast_view(scene, cam, atlas_res=64)
    wrong = dict(cam)
    wrong["h_ext"] = cam["h_ext"] * 1.02
    ex, _ey = EA.reprojection_error(aov["pos"], aov["sil"], wrong)
    assert ex > EA.REPROJECT_TOL_PX, (
        "a 2%% extent error reprojected inside tolerance (%.4f px)" % ex)


def test_t78_background_sentinels_are_the_declared_ones():
    scene = EA.fixture_scene(0.2)
    cam = EA.make_cam(0.0, 0.0, [0.0, 0.0, 0.0], 1.2, 0.9, 48, 64)
    aov = EA.cast_view(scene, cam, atlas_res=64)
    bg = ~aov["sil"]
    assert bg.any(), "the fixture must leave background, or this proves nothing"
    assert np.isinf(aov["depth"][bg]).all() and (aov["depth"][bg] > 0).all()
    assert np.isnan(aov["pos"][bg]).all()
    assert np.isnan(aov["normal_world"][bg]).all()
    assert (aov["surfid"][bg] == -1).all()


def test_t78_occlusion_keeps_only_the_near_surface():
    v, f, uv, n = EA.fixture_box(0.2)
    v2 = v.copy()
    v2[:, 1] += 0.6
    scene = EA.Scene(np.concatenate([v, v2]), np.concatenate([f, f + len(v)]),
                     uv=np.concatenate([uv, uv]),
                     vnormals_canon=np.concatenate([n, n]))
    cam = EA.make_cam(0.0, 0.0, [0.0, 0.0, 0.0], 1.2, 0.9, 64, 64)
    aov = EA.cast_view(scene, cam, atlas_res=64)
    d = aov["depth"][aov["sil"]]
    assert np.allclose(d, -0.2, rtol=0.0, atol=1e-5), (d.min(), d.max())


def test_t78_surfid_is_the_texel_the_route_would_sample():
    """`texpass_iter.py:226-227` samples the atlas at
    (u * RES - 0.5, (1 - v) * RES - 0.5). surfid is that, rounded, as
    row * RES + col. A one-texel shift must change the id, or the mapping is
    not addressing texels."""
    res = 256
    # the mapping, stated once here so a change to the tool has to change this
    # line too: col = round(u*RES - 0.5), row = round((1-v)*RES - 0.5)
    for u, vv, want_col, want_row in ((0.5, 0.5, 128, 128),
                                      (0.0, 0.0, 0, 255),
                                      (1.0, 1.0, 255, 0)):
        col = int(np.clip(np.rint(u * res - 0.5), 0, res - 1))
        row = int(np.clip(np.rint((1.0 - vv) * res - 0.5), 0, res - 1))
        assert (col, row) == (want_col, want_row), (u, vv, col, row)
    scene = EA.fixture_scene(0.25)
    cam = EA.make_cam(0.0, 0.0, [0.0, 0.0, 0.0], 1.0, 0.75, 96, 128)
    a = EA.cast_view(scene, cam, atlas_res=res)
    ids = np.unique(a["surfid"][a["sil"]])
    assert ids.min() >= 0 and ids.max() < res * res
    rows = ids // res
    cols = ids % res
    # the fixture's -Y face owns a band around v in [0.15, 0.85], u in a
    # 1/6 slice; both spans must be more than one texel or the id is degenerate
    assert cols.max() > cols.min() and rows.max() > rows.min()
    b = EA.cast_view(scene, cam, atlas_res=res * 2)
    assert not np.array_equal(np.unique(b["surfid"][b["sil"]]), ids), (
        "doubling the atlas resolution left the surfid set unchanged - the id "
        "is not a texel index")


def test_t78_the_silhouette_gate_fires_on_one_pixel():
    scene = EA.fixture_scene(0.25)
    cam = EA.make_cam(0.0, 0.0, [0.0, 0.0, 0.0], 1.0, 0.75, 48, 64)
    aov = EA.cast_view(scene, cam, atlas_res=64)
    EA.gate_silhouette(aov["sil"], aov["sil"], "identity")
    wrong = aov["sil"].copy()
    ys, xs = np.nonzero(wrong)
    wrong[ys[0], xs[0]] = False
    with pytest.raises(EA.Andon) as e:
        EA.gate_silhouette(aov["sil"], wrong, "one-pixel")
    assert "1 differing px" in str(e.value)


def test_t78_the_gate_is_not_a_bare_assert():
    """-O and PYTHONOPTIMIZE=1 delete `assert`. This repo converted 278 sites on
    that fact (E21 Ruling 2 / E22). The gate must fire in all three modes."""
    src = (
        "import sys\n"
        "sys.path.insert(0, %r)\n"
        "import numpy as np\n"
        "import emit_view_aovs as EA\n"
        "a = np.zeros((4, 4), dtype=bool); a[1, 1] = True\n"
        "b = a.copy(); b[2, 2] = True\n"
        "try:\n"
        "    EA.gate_silhouette(a, b, 'probe')\n"
        "except EA.Andon:\n"
        "    sys.exit(7)\n"
        "sys.exit(0)\n" % os.path.join(str(REPO), "tools"))
    for flags, opt in (([], None), (["-O"], None), ([], "1")):
        env = dict(os.environ)
        env.pop("PYTHONOPTIMIZE", None)
        if opt is not None:
            env["PYTHONOPTIMIZE"] = opt
        p = subprocess.run([sys.executable] + flags + ["-c", src],
                           capture_output=True, env=env, timeout=600)
        assert p.returncode == 7, (
            "the gate did not fire under flags=%r PYTHONOPTIMIZE=%r (rc %d): %s"
            % (flags, opt, p.returncode, p.stderr.decode("ascii", "replace")))


def test_t78_canonical_normals_are_the_same_rotation_as_the_vertices():
    """[x, -z, y] is a proper rotation, so directions take it unchanged. If the
    two ever disagree, every facing weight is wrong by a rotation."""
    rng = np.random.default_rng(3)
    v = rng.normal(size=(64, 3))
    vc, vmax = EA.canonical_vertices(v)
    nc = EA.canonical_normals(v)
    assert np.allclose(nc, vc / (np.linalg.norm(vc, axis=1, keepdims=True)),
                       rtol=0.0, atol=1e-12)
    assert vmax == pytest.approx(float(np.abs(v).max()))


def test_t78_frame_extents_are_the_fit_axis_block():
    v = np.array([[-0.4, -0.3, -0.5], [0.4, 0.3, 0.5]], dtype=np.float64)
    bmid, v_ext, h_ext = EA.frame_extents(v, 752, 1024)
    assert np.allclose(bmid, [0.0, 0.0, 0.0])
    assert v_ext == pytest.approx(1.0 * EA.FIT_MARGIN)
    assert h_ext == pytest.approx(v_ext * (752 / 1024))


# ---------------------------------------------------------------------------
# artifacts tier - the RECORDED cameras
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def w3_scene(assets):
    import trimesh
    glb = need(assets, os.path.join(ARMB, "out", "W3_final.glb"))
    m = trimesh.load(str(glb), force="mesh", process=False)
    v = np.asarray(m.vertices, dtype=np.float64)
    vc, _vmax = EA.canonical_vertices(v)
    scene = EA.Scene(vc, np.asarray(m.faces, dtype=np.int64),
                     uv=np.asarray(m.visual.uv, dtype=np.float64),
                     vnormals_canon=EA.canonical_normals(
                         np.asarray(m.vertex_normals, dtype=np.float64)))
    bmid, v_ext, h_ext = EA.frame_extents(vc, W, H)
    return scene, bmid, v_ext, h_ext


@pytest.mark.parametrize("yaw,el,rel,px", [
    (90.0, 0.0, os.path.join(ARMB, "masks", "w3clay_2.png"), 90553),
    (0.0, 55.0, os.path.join(ARMB, "state", "job_y+000_e+55", "hit.png"), 108166),
])
def test_t78_recorded_camera_reproduces_its_own_silhouette(assets, w3_scene,
                                                           yaw, el, rel, px):
    """A flat camera against the mask tool's output, and an ELEVATED camera
    against `texpass_iter::emit`'s own hit mask - two different writers, one
    reader. The el-55 row is the only elevated silhouette anchor this route has.

    The px counts are pinned: a reproduction that agreed with a DIFFERENT mask
    would still read 0 differing px against that other mask, so the count is
    what says which silhouette this is.
    """
    from PIL import Image
    ref_path = need(assets, rel)
    scene, bmid, v_ext, h_ext = w3_scene
    cam = EA.make_cam(yaw, el, bmid, v_ext, h_ext, W, H)
    aov = EA.cast_view(scene, cam, atlas_res=4096)
    ref = np.asarray(Image.open(str(ref_path)).convert("L")) > 127
    r = EA.compare_silhouette(aov["sil"], ref)
    assert r["ref_px"] == px, (
        "the recorded anchor holds %d px, this test pins %d - the tree moved"
        % (r["ref_px"], px))
    assert r["diff_px"] == 0, (
        "yaw %g el %g does not reproduce %s: %d differing px, IoU %.6f"
        % (yaw, el, rel, r["diff_px"], r["iou"]))


def test_t78_the_flat_ring_and_the_elevated_camera_are_not_the_same_view(
        assets, w3_scene):
    """E45's premise finding, kept runnable. `masks/w3clay_0.png` is yaw 0 at
    el 0; `state/job_y+000_e+55/` is yaw 0 at el 55. Anything that pairs a
    twin with the elevated camera is pairing two different cameras, and this
    is the leg that says so in numbers rather than in prose."""
    from PIL import Image
    mask0 = need(assets, os.path.join(ARMB, "masks", "w3clay_0.png"))
    scene, bmid, v_ext, h_ext = w3_scene
    flat = EA.cast_view(scene, EA.make_cam(0.0, 0.0, bmid, v_ext, h_ext, W, H),
                        atlas_res=4096)
    elev = EA.cast_view(scene, EA.make_cam(0.0, 55.0, bmid, v_ext, h_ext, W, H),
                        atlas_res=4096)
    ref = np.asarray(Image.open(str(mask0)).convert("L")) > 127
    assert EA.compare_silhouette(flat["sil"], ref)["diff_px"] == 0
    d = EA.compare_silhouette(elev["sil"], ref)["diff_px"]
    assert d > 50000, (
        "the el-55 camera differs from the el-0 mask by only %d px; E45 measured "
        "96,024 and the two cameras are supposed to be plainly different" % d)
