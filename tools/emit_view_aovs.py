# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Per-view G-buffer (AOV) emitter for an orthographic turnaround.

WHY THIS EXISTS. The S3 existence-proof compositor (grok-consult-5-brief) and the
twin-to-mesh warp instrument (E45 task 2) both consume the same per-view arrays:
depth, position, normal, silhouette, a stable surface id, and the two Callieri
weights. Nothing in this repo emitted them. `texpass_iter.py::emit` casts the same
rays but keeps only a render, a hole mask and `hit.png`; `silhouette_masks.py` keeps
only the mask (and an 8-bit depth PNG). This module keeps the float arrays.

WHAT IT IS NOT. It grades nothing. It does not blend, sample, or judge. It emits
arrays and a manifest, and it halts if its silhouette does not reproduce a recorded
one.

THE CAMERA IS A PORT, NOT A REIMPLEMENTATION. `basis()` below is
`tools/texpass_iter.py::basis` (:156-164) copied verbatim, because that is the
function that wrote every `state/job_*/cam.json` this module reads. At el = 0 it
agrees bit-for-bit with `tools/silhouette_masks.py` (:132-136), which wrote every
`masks/w3clay_*.png` - measured, not assumed: the six shared cameras produce
byte-identical PNGs on the shipped state. The verbatim-copy-with-citation pattern is
this repo's established answer to `project_twins.py` not being import-safe.

    ONE FLOAT DETAIL THAT IS LOAD-BEARING. Neither source snaps its trig
    (`project_twins.cam_axes` does, and is a THIRD construction). Do not add a snap
    here: the recorded masks were produced without one, and the ray origins are cast
    to float32 before open3d sees them, which is why the two unsnapped constructions
    already agree byte-for-byte.

CONVENTIONS, stated because every consumer depends on them.

  frame        canonical, Z up. `v_canonical = [x, -z, y] / max|v| * 0.5`, the glTF
               Y-up remap this repo has applied since bake_hero_prep. A proper
               rotation composed with a uniform scale, so NORMALS take the same map.
  camera       orthographic. `dtc` is the unit direction from the scene TO the
               camera; `look = -dtc`; `right`, `up` complete a right-handed frame.
  projection   px = ((P - bmid).right / h_ext + 0.5) * W - 0.5
               py = (0.5 - (P - bmid).up   / v_ext) * H - 0.5
               depth = -(P - bmid).dtc
               `depth` equals `t_hit - D` for rays fired from `-look * D`; the two
               forms are the same number and the module asserts it on every view.
  background   depth +inf (callieri_border's declared sentinel), pos NaN,
               normal NaN, sil False, surfid -1.
  surfid       atlas texel linear index, `row * RES + col`, from the GLB's own UVs
               barycentrically interpolated at the hit, with
               col = clip(round(u * RES - 0.5)), row = clip(round((1 - v) * RES - 0.5)).
               That is `texpass_iter`'s own atlas sampling (:226-227) taken to the
               nearest texel, so a surfid indexes the texel the route would sample.

YES/NO INTERVALS for the checks this module performs.

  silhouette anchor   0 differing px = the emitted `sil` IS the recorded mask.
                      Any nonzero = it is not, and the number is the count.
                      Recorded precedent on the shipped state: 0 at views 0 and 4
                      (`silhouette_masks.py --anchor`, quoted in project_twins'
                      docstring and reproduced in masks/silhouettes.json).
  reprojection        0 px = every stored `pos` projects back onto its own pixel
                      centre. A wrong `right`/`up`/extent shows up here as a
                      systematic offset; float32 storage of `pos` alone costs
                      ~3e-5 px at this scale.
  depth identity      0 = the analytic depth and `t_hit - D` agree. A sign error in
                      `dtc` inverts this and shows up as ~2 * |depth| .

Standards:
  ANDON_AUTHORITY  - every gate `raise`s (Andon). Never a bare `assert`: -O and
    PYTHONOPTIMIZE=1 delete those silently, and 87 of this repo's ANDONs were once
    removable by an environment variable (E21 Ruling 2 / E22).
  PIN_PER_STEP     - the manifest carries the GLB sha256, this file's sha256, every
    library version (the identity-envelope law: open3d here is a git-suffixed devel
    wheel), and every camera block.
  NAMED_COMPENSATORS - writes only new files under --out. Undo: delete --out.
  EXTERNAL_VERIFIER - grades nothing; emits arrays.

  python tools/emit_view_aovs.py --glb W3_final.glb --out DIR
         --view 0=yaw:0,el:0,anchor:masks/w3clay_0.png,image:twins/twin_0.png
         [--atlas-res 4096] [--aspect 752,1024] [--no-gate]
  python tools/emit_view_aovs.py --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys

import numpy as np

TOOL_VERSION = "1.0.0"

# tools/texpass_iter.py:49 - ray origins sit at -look * D from bmid. Kept as the
# same literal so `depth == t_hit - D` is checkable rather than approximate.
RAY_ORIGIN_DISTANCE = 2.0

# tools/silhouette_masks.py:66 / texpass_iter's --margin. The framing margin on the
# fitted axis. THE THIRD COPY OF THE FIT-AXIS BLOCK IS IN turn_render.py; all of
# them move together or a mask and its render disagree (E04 Ruling 6).
FIT_MARGIN = 1.204

ATLAS_RES = 4096

# The dispatch's self-consistency tolerance. Half a pixel plus a hair, so a
# reprojection that lands on the WRONG pixel centre cannot pass.
REPROJECT_TOL_PX = 0.51


class Andon(RuntimeError):
    """A fired gate. Never an `assert` - the interpreter may delete those."""


def _andon(msg):
    raise Andon("ANDON: " + msg)


# ---------------------------------------------------------------------------
# camera
# ---------------------------------------------------------------------------

def basis(yaw_d, el_d):
    """(dtc, look, right, up) for a yaw/elevation orbit.

    VERBATIM PORT of tools/texpass_iter.py::basis (:156-164), the function that
    wrote the cam.json files this module reads. Body unchanged; only the docstring
    is new. At el = 0 this equals silhouette_masks.py's construction, which is why a
    mask written by one tool anchors a cast made by the other.
    """
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    look = -cd / np.linalg.norm(cd)
    up0 = np.array([0.0, 0.0, 1.0])
    right = np.cross(look, up0)
    right /= np.linalg.norm(right) + 1e-12
    up = np.cross(right, look)
    return cd, look, right, up / (np.linalg.norm(up) + 1e-12)


def canonical_vertices(v):
    """glTF Y-up -> this repo's canonical Z-up frame, maxabs-scaled to +-0.5.

    VERBATIM from silhouette_masks.py:92-93 / texpass_iter.py:172-173 /
    bake_hero_fuse.py:82-83 (three copies in the tree; this is a fourth reader of
    the same two lines, not a new convention).
    """
    v = np.asarray(v, dtype=np.float64)
    if v.ndim != 2 or v.shape[1] != 3:
        _andon("vertices must be (N, 3), got %s" % (v.shape,))
    vmax = np.abs(v).max()
    if not np.isfinite(vmax) or vmax <= 0.0:
        _andon("max|v| is %r - not a mesh this frame can normalise" % (vmax,))
    return np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / vmax * 0.5, float(vmax)


def canonical_normals(n):
    """The same rotation, applied to directions. Uniform scale drops out."""
    n = np.asarray(n, dtype=np.float64)
    if n.ndim != 2 or n.shape[1] != 3:
        _andon("normals must be (N, 3), got %s" % (n.shape,))
    out = np.stack([n[:, 0], -n[:, 2], n[:, 1]], axis=1)
    ln = np.linalg.norm(out, axis=1, keepdims=True)
    return out / np.maximum(ln, 1e-12)


def frame_extents(v_canon, W, H, fit_axis="height", margin=FIT_MARGIN):
    """(bmid, v_ext, h_ext) - the fit-axis block, fourth copy, same defaults."""
    blo, bhi = v_canon.min(axis=0), v_canon.max(axis=0)
    bmid = (blo + bhi) / 2
    if fit_axis == "height":
        v_ext = (bhi[2] - blo[2]) * margin
        h_ext = v_ext * (W / H)
    elif fit_axis == "width":
        h_ext = max(bhi[0] - blo[0], bhi[1] - blo[1]) * margin
        v_ext = h_ext * (H / W)
    else:
        _andon("fit_axis must be 'height' or 'width', got %r" % (fit_axis,))
    return bmid, float(v_ext), float(h_ext)


def make_cam(yaw, el, bmid, v_ext, h_ext, W, H):
    """The camera block the Grok brief's contract names, as plain floats/lists."""
    dtc, look, right, up = basis(yaw, el)
    return {
        "yaw": float(yaw), "el": float(el),
        "dtc": [float(x) for x in dtc], "look": [float(x) for x in look],
        "right": [float(x) for x in right], "up": [float(x) for x in up],
        "bmid": [float(x) for x in np.asarray(bmid, dtype=np.float64)],
        "v_ext": float(v_ext), "h_ext": float(h_ext),
        "W": int(W), "H": int(H),
    }


def _cam_vectors(cam):
    return (np.asarray(cam["right"], dtype=np.float64),
            np.asarray(cam["up"], dtype=np.float64),
            np.asarray(cam["dtc"], dtype=np.float64),
            np.asarray(cam["bmid"], dtype=np.float64))


def project(P, cam):
    """(px, py) under the declared contract. P is (..., 3) in the canonical frame."""
    right, up, _dtc, bmid = _cam_vectors(cam)
    d = np.asarray(P, dtype=np.float64) - bmid
    px = ((d @ right) / cam["h_ext"] + 0.5) * cam["W"] - 0.5
    py = (0.5 - (d @ up) / cam["v_ext"]) * cam["H"] - 0.5
    return px, py


def depth_of(P, cam):
    """-(P - bmid).dtc, the contract's depth. Larger = farther from the camera."""
    _right, _up, dtc, bmid = _cam_vectors(cam)
    return -((np.asarray(P, dtype=np.float64) - bmid) @ dtc)


# ---------------------------------------------------------------------------
# the cast
# ---------------------------------------------------------------------------

class Scene(object):
    """A raycasting scene plus the per-vertex attributes a hit interpolates."""

    def __init__(self, v_canon, faces, uv=None, vnormals_canon=None):
        import open3d as o3d
        self.v = np.asarray(v_canon, dtype=np.float64)
        self.f = np.asarray(faces, dtype=np.int64)
        if self.f.ndim != 2 or self.f.shape[1] != 3:
            _andon("faces must be (M, 3), got %s" % (self.f.shape,))
        self.uv = None if uv is None else np.asarray(uv, dtype=np.float64)
        if self.uv is not None and self.uv.shape[0] != self.v.shape[0]:
            _andon("uv has %d rows for %d vertices"
                   % (self.uv.shape[0], self.v.shape[0]))
        self.vn = None if vnormals_canon is None else np.asarray(
            vnormals_canon, dtype=np.float64)
        if self.vn is not None and self.vn.shape[0] != self.v.shape[0]:
            _andon("normals has %d rows for %d vertices"
                   % (self.vn.shape[0], self.v.shape[0]))
        self.rs = o3d.t.geometry.RaycastingScene()
        self.rs.add_triangles(o3d.core.Tensor(self.v.astype(np.float32)),
                              o3d.core.Tensor(self.f.astype(np.uint32)))


def cast_view(scene, cam, atlas_res=ATLAS_RES, origin_distance=RAY_ORIGIN_DISTANCE):
    """Raycast one orthographic view. Returns the AOV dict.

    The ray grid is silhouette_masks.py:123-124 / texpass_iter.py:207-211 - the
    same two lines that produced every recorded mask on this route.
    """
    import open3d as o3d
    W, H = int(cam["W"]), int(cam["H"])
    right, up, dtc, bmid = _cam_vectors(cam)
    look = np.asarray(cam["look"], dtype=np.float64)
    h_ext, v_ext = cam["h_ext"], cam["v_ext"]

    xs = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
    ys = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
    gx, gy = np.meshgrid(xs, ys)
    origins = (bmid[None, None, :] + gx[..., None] * right[None, None, :]
               + gy[..., None] * up[None, None, :]
               - look[None, None, :] * origin_distance)
    dirs = np.broadcast_to(look, origins.shape)
    ans = scene.rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [origins, dirs], axis=-1).reshape(-1, 6).astype(np.float32)))
    t_hit = ans["t_hit"].numpy().reshape(H, W).astype(np.float64)
    prim = ans["primitive_ids"].numpy().reshape(H, W)
    buv = ans["primitive_uvs"].numpy().reshape(H, W, 2).astype(np.float64)
    sil = np.isfinite(t_hit)

    depth = np.full((H, W), np.inf, dtype=np.float64)
    pos = np.full((H, W, 3), np.nan, dtype=np.float64)
    if sil.any():
        pos[sil] = origins[sil] + t_hit[sil][:, None] * look[None, :]
        depth[sil] = t_hit[sil] - origin_distance

    # THE IDENTITY CHECK, in scope, on every view: the analytic depth and the
    # ray-parameter depth are the same number. A sign error in dtc doubles this.
    if sil.any():
        d_analytic = depth_of(pos[sil], cam)
        dmax = float(np.abs(d_analytic - depth[sil]).max())
        if not (dmax < 1e-9):
            _andon("depth identity broken: max |-(P-bmid).dtc - (t_hit - D)| = "
                   "%.6e over %d hits. The camera frame is not orthonormal or "
                   "dtc is not -look." % (dmax, int(sil.sum())))
    else:
        dmax = 0.0

    normal = np.full((H, W, 3), np.nan, dtype=np.float64)
    surfid = np.full((H, W), -1, dtype=np.int64)
    if sil.any():
        tri = scene.f[prim[sil]]
        wu = buv[sil][:, 0:1]
        wv = buv[sil][:, 1:2]
        w0 = 1.0 - wu - wv
        if scene.vn is not None:
            n = (w0 * scene.vn[tri[:, 0]] + wu * scene.vn[tri[:, 1]]
                 + wv * scene.vn[tri[:, 2]])
            ln = np.linalg.norm(n, axis=1, keepdims=True)
            normal[sil] = n / np.maximum(ln, 1e-12)
        if scene.uv is not None:
            uvp = (w0 * scene.uv[tri[:, 0]] + wu * scene.uv[tri[:, 1]]
                   + wv * scene.uv[tri[:, 2]])
            col = np.clip(np.rint(uvp[:, 0] * atlas_res - 0.5), 0,
                          atlas_res - 1).astype(np.int64)
            row = np.clip(np.rint((1.0 - uvp[:, 1]) * atlas_res - 0.5), 0,
                          atlas_res - 1).astype(np.int64)
            surfid[sil] = row * atlas_res + col

    return {
        "sil": sil,
        "depth": depth.astype(np.float32),
        "pos": pos.astype(np.float32),
        "normal_world": normal.astype(np.float32),
        "surfid": surfid.astype(np.int32),
        "t_hit": t_hit,
        "prim": prim,
        "depth_identity_max": dmax,
    }


def reprojection_error(pos, sil, cam):
    """Max |Delta| in px when every valid `pos` is projected back through `cam`.

    CAN-FAIL BY CONSTRUCTION: the expected value is each pixel's own (col, row).
    A right/up swap, a sign flip, or a wrong extent all land far outside 0.51 px.
    """
    sil = np.asarray(sil, dtype=bool)
    if not sil.any():
        return 0.0, 0.0
    H, W = sil.shape
    rows, cols = np.nonzero(sil)
    px, py = project(np.asarray(pos, dtype=np.float64)[sil], cam)
    ex = np.abs(px - cols)
    ey = np.abs(py - rows)
    return float(ex.max()), float(ey.max())


def compare_silhouette(sil, ref):
    """Pixel comparison of two boolean masks. NEVER a file-hash comparison:
    file bytes are not pixel values, and a PNG hash has produced two false halts
    in this repo (CLAUDE.md)."""
    sil = np.asarray(sil, dtype=bool)
    ref = np.asarray(ref, dtype=bool)
    if sil.shape != ref.shape:
        _andon("silhouette is %s, anchor is %s" % (sil.shape, ref.shape))
    diff = sil != ref
    inter = int((sil & ref).sum())
    union = int((sil | ref).sum())
    only_sil = sil & ~ref
    only_ref = ref & ~sil
    out = {
        "diff_px": int(diff.sum()),
        "sil_px": int(sil.sum()), "ref_px": int(ref.sum()),
        "iou": (inter / union) if union else 1.0,
        "only_in_emitted": int(only_sil.sum()),
        "only_in_anchor": int(only_ref.sum()),
    }
    if out["diff_px"]:
        rows, cols = np.nonzero(diff)
        out["diff_bbox_rows"] = [int(rows.min()), int(rows.max())]
        out["diff_bbox_cols"] = [int(cols.min()), int(cols.max())]
        out["diff_row_hist_16"] = _hist16(rows, sil.shape[0])
        out["diff_col_hist_16"] = _hist16(cols, sil.shape[1])
    return out


def _hist16(idx, n):
    """Coarse spatial distribution: counts in 16 equal bands. A rim disagreement
    spreads across bands; a systematic one concentrates."""
    b = np.clip((np.asarray(idx) * 16 // max(n, 1)), 0, 15)
    return [int(x) for x in np.bincount(b, minlength=16)]


def gate_silhouette(sil, ref, label):
    """ANDON. Halts before anything is emitted if `sil` is not the recorded mask.

    This is a `raise`, and it is inside the function that would otherwise return
    the arrays a caller writes - a shell chain cannot walk past it (E08 Amendment
    32: the check lives inside the step it gates).
    """
    r = compare_silhouette(sil, ref)
    if r["diff_px"]:
        _andon(
            "%s does not reproduce its anchor: %d differing px "
            "(emitted %d px, anchor %d px, IoU %.6f; %d only-emitted, %d "
            "only-anchor; rows %s cols %s). Do NOT tune the camera until this "
            "passes - report the count and its distribution."
            % (label, r["diff_px"], r["sil_px"], r["ref_px"], r["iou"],
               r["only_in_emitted"], r["only_in_anchor"],
               r.get("diff_bbox_rows"), r.get("diff_bbox_cols")))
    return r


# ---------------------------------------------------------------------------
# fixtures (hermetic; no GLB, no recorded tree)
# ---------------------------------------------------------------------------

def fixture_box(half=0.25):
    """An axis-aligned box in the canonical frame, with per-vertex normals that
    are the face normals (flat-shaded, one vertex per corner per face) and a UV
    that maps each face to a distinct atlas band.

    Known by construction: seen down -Y (yaw 0) the silhouette is exactly the
    x/z cross-section, so its area in pixels is computable from the extents.
    """
    s = float(half)
    # 6 faces x 4 corners, no sharing, so normals are exact
    quads = [
        # (+X, -X, +Y, -Y, +Z, -Z)
        ([(s, -s, -s), (s, s, -s), (s, s, s), (s, -s, s)], (1.0, 0.0, 0.0)),
        ([(-s, s, -s), (-s, -s, -s), (-s, -s, s), (-s, s, s)], (-1.0, 0.0, 0.0)),
        ([(s, s, -s), (-s, s, -s), (-s, s, s), (s, s, s)], (0.0, 1.0, 0.0)),
        ([(-s, -s, -s), (s, -s, -s), (s, -s, s), (-s, -s, s)], (0.0, -1.0, 0.0)),
        ([(-s, -s, s), (s, -s, s), (s, s, s), (-s, s, s)], (0.0, 0.0, 1.0)),
        ([(-s, s, -s), (s, s, -s), (s, -s, -s), (-s, -s, -s)], (0.0, 0.0, -1.0)),
    ]
    v, n, uv, f = [], [], [], []
    for k, (corners, nrm) in enumerate(quads):
        base = len(v)
        for j, c in enumerate(corners):
            v.append(c)
            n.append(nrm)
            # each face owns a 1/6 horizontal band of the atlas
            u0 = (k + 0.15) / 6.0
            u1 = (k + 0.85) / 6.0
            uu = u0 if j in (0, 3) else u1
            vv = 0.15 if j in (0, 1) else 0.85
            uv.append((uu, vv))
        f.append((base, base + 1, base + 2))
        f.append((base, base + 2, base + 3))
    return (np.array(v, dtype=np.float64), np.array(f, dtype=np.int64),
            np.array(uv, dtype=np.float64), np.array(n, dtype=np.float64))


def fixture_scene(half=0.25):
    v, f, uv, n = fixture_box(half)
    return Scene(v, f, uv=uv, vnormals_canon=n)


# ---------------------------------------------------------------------------
# self-test
# ---------------------------------------------------------------------------

def silhouette_masks_axes(yaw_d):
    """silhouette_masks.py:132-136, verbatim - the OTHER construction.

    Kept here so the two can be compared in code rather than by reading. That
    file writes the masks this module anchors on, and it takes no elevation.
    """
    th = np.radians(yaw_d)
    dtc = np.array([np.sin(th), -np.cos(th), 0.0])
    rgt = np.array([np.cos(th), np.sin(th), 0.0])
    look = -dtc
    upv = np.cross(rgt, look)
    upv /= np.linalg.norm(upv) + 1e-12
    return dtc, look, rgt, upv


def ray_origins(cam, origin_distance=RAY_ORIGIN_DISTANCE):
    """The ray grid, float64. silhouette_masks.py:123-139 / texpass_iter.py:207-211."""
    W, H = int(cam["W"]), int(cam["H"])
    right, up, _dtc, bmid = _cam_vectors(cam)
    look = np.asarray(cam["look"], dtype=np.float64)
    xs = (np.arange(W) + 0.5) / W * cam["h_ext"] - cam["h_ext"] / 2
    ys = cam["v_ext"] / 2 - (np.arange(H) + 0.5) / H * cam["v_ext"]
    gx, gy = np.meshgrid(xs, ys)
    return (bmid[None, None, :] + gx[..., None] * right[None, None, :]
            + gy[..., None] * up[None, None, :]
            - look[None, None, :] * origin_distance)


def _selftest_basis_matches_the_flat_ring():
    """At el = 0 the port must agree with silhouette_masks.py's construction.

    THE TWO ARE NOT BIT-IDENTICAL IN FLOAT64 AND THAT IS NOT A DEFECT. Both
    divide by `norm + 1e-12`, but they divide DIFFERENT vectors: texpass_iter
    normalises `right` (whose norm is 1), silhouette_masks normalises `up`. So
    texpass_iter's `right` is 1 - 1e-12 times silhouette_masks', a relative
    difference of exactly the guard epsilon.

    The property that decides whether a recorded mask anchors this cast is
    narrower and is checked below: the ray origins, CAST TO FLOAT32 as open3d
    receives them, must be bit-identical. They are - which is the mechanism
    behind the shipped state's six byte-identical hit.png/mask pairs.
    """
    for yaw in (0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0):
        dtc, look, right, up = basis(yaw, 0.0)
        want_dtc, want_look, want_rgt, want_up = silhouette_masks_axes(yaw)
        for got, want, nm in ((dtc, want_dtc, "dtc"), (look, want_look, "look"),
                              (right, want_rgt, "right"), (up, want_up, "up")):
            if not np.allclose(got, want, rtol=0.0, atol=1e-9):
                _andon("basis(%g, 0) %s %r != silhouette_masks' %r"
                       % (yaw, nm, got, want))
        if not np.allclose(look, -dtc, rtol=0.0, atol=1e-12):
            _andon("look is not -dtc at yaw %g" % yaw)


def _selftest_float32_origins_are_bit_identical_to_the_mask_tool():
    """THE LEG THAT MATTERS: at el = 0 the two constructions must produce the
    same float32 ray grid, or a recorded mask cannot anchor this cast.

    CAN FAIL: a 1e-5 perturbation of `right` is shown here to break the equality,
    so the leg is not vacuous. The size is not arbitrary - origins sit ~2 units
    from bmid (the -look * D offset), where float32 spacing is ~2.4e-7, and the
    grid multiplies a `right` perturbation by |gx| <= h_ext / 2 ~ 0.44. So 1e-7
    is BELOW half an ulp there and genuinely does not move the grid; 1e-5 does.
    That same arithmetic is why the 1e-12 relative difference between the two
    constructions cannot: it is five orders under float32 resolution here.
    """
    for yaw in (0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0):
        cam = make_cam(yaw, 0.0, [0.01, -0.02, 0.03], 1.1969748723526452,
                       0.8790284218839738, 64, 96)
        smd, sml, smr, smu = silhouette_masks_axes(yaw)
        alt = dict(cam)
        alt["dtc"], alt["look"] = [float(x) for x in smd], [float(x) for x in sml]
        alt["right"], alt["up"] = [float(x) for x in smr], [float(x) for x in smu]
        a = ray_origins(cam).astype(np.float32)
        b = ray_origins(alt).astype(np.float32)
        if not np.array_equal(a, b):
            _andon("yaw %g: the two constructions give %d differing float32 ray "
                   "origins (max %.3e) - a recorded mask cannot anchor this cast"
                   % (yaw, int((a != b).sum()), float(np.abs(a - b).max())))
        perturbed = dict(alt)
        perturbed["right"] = [float(x) + (1e-5 if i == 0 else 0.0)
                              for i, x in enumerate(smr)]
        c = ray_origins(perturbed).astype(np.float32)
        if np.array_equal(a, c):
            _andon("a 1e-5 perturbation of `right` left the float32 origins "
                   "unchanged at yaw %g - this leg cannot fail" % yaw)


def _selftest_basis_is_orthonormal_at_elevation():
    for el in (-89.0, -55.0, -20.0, 0.0, 20.0, 55.0, 89.0):
        for yaw in (0.0, 37.0, 180.0, 313.0):
            dtc, look, right, up = basis(yaw, el)
            for name, vec in (("dtc", dtc), ("right", right), ("up", up)):
                ln = float(np.linalg.norm(vec))
                if abs(ln - 1.0) > 1e-9:
                    _andon("basis(%g,%g) %s has length %.12f" % (yaw, el, name, ln))
            for a, b, nm in ((right, up, "right.up"), (right, look, "right.look"),
                             (up, look, "up.look")):
                d = float(abs(a @ b))
                if d > 1e-9:
                    _andon("basis(%g,%g) %s = %.3e, not orthogonal"
                           % (yaw, el, nm, d))
            # up must keep world +Z on the upper half of the frame
            if el < 89.0 and up[2] <= 0.0:
                _andon("basis(%g,%g) up points down (%r)" % (yaw, el, up))


def _selftest_projection_roundtrip():
    """A synthetic camera, and points whose pixel coordinates are known."""
    cam = make_cam(37.0, 22.0, [0.1, -0.2, 0.05], 1.0, 0.75, 64, 96)
    right, up, dtc, bmid = _cam_vectors(cam)
    rng = np.random.default_rng(0)
    a = rng.uniform(-0.4, 0.4, 500)
    b = rng.uniform(-0.4, 0.4, 500)
    c = rng.uniform(-0.4, 0.4, 500)
    P = bmid + a[:, None] * right + b[:, None] * up - c[:, None] * dtc
    px, py = project(P, cam)
    want_px = (a / cam["h_ext"] + 0.5) * cam["W"] - 0.5
    want_py = (0.5 - b / cam["v_ext"]) * cam["H"] - 0.5
    if not np.allclose(px, want_px, rtol=0.0, atol=1e-9):
        _andon("projection px is not the contract (max %.3e)"
               % float(np.abs(px - want_px).max()))
    if not np.allclose(py, want_py, rtol=0.0, atol=1e-9):
        _andon("projection py is not the contract (max %.3e)"
               % float(np.abs(py - want_py).max()))
    d = depth_of(P, cam)
    if not np.allclose(d, c, rtol=0.0, atol=1e-9):
        _andon("depth is not -(P-bmid).dtc (max %.3e)"
               % float(np.abs(d - c).max()))
    # a swapped right/up must NOT pass - the check can fail
    bad = dict(cam)
    bad["right"], bad["up"] = cam["up"], cam["right"]
    bpx, _bpy = project(P, bad)
    if np.allclose(bpx, want_px, rtol=0.0, atol=1e-6):
        _andon("a right/up swap produced the same px - the check cannot fail")


def _selftest_cast_and_reproject():
    scene = fixture_scene(0.25)
    cam = make_cam(0.0, 0.0, [0.0, 0.0, 0.0], 1.0, 0.75, 96, 128)
    aov = cast_view(scene, cam, atlas_res=64)
    if not aov["sil"].any():
        _andon("the box fixture produced an empty silhouette")
    # known by construction: a 0.5-wide box seen down -Y fills
    # (0.5 / h_ext) * W by (0.5 / v_ext) * H px, +-1 px of rasterisation
    want_w = 0.5 / cam["h_ext"] * cam["W"]
    want_h = 0.5 / cam["v_ext"] * cam["H"]
    rows, cols = np.nonzero(aov["sil"])
    got_w = cols.max() - cols.min() + 1
    got_h = rows.max() - rows.min() + 1
    if abs(got_w - want_w) > 1.5 or abs(got_h - want_h) > 1.5:
        _andon("box silhouette is %dx%d px, construction says %.1fx%.1f"
               % (got_w, got_h, want_w, want_h))
    ex, ey = reprojection_error(aov["pos"], aov["sil"], cam)
    if not (ex < REPROJECT_TOL_PX and ey < REPROJECT_TOL_PX):
        _andon("reprojection error %.4f / %.4f px exceeds %.2f"
               % (ex, ey, REPROJECT_TOL_PX))
    # the -Y face is the one facing a yaw-0 camera; its normal is (0,-1,0)
    n = aov["normal_world"][aov["sil"]]
    dtc = np.asarray(cam["dtc"], dtype=np.float64)
    if not np.allclose(n @ dtc, 1.0, rtol=0.0, atol=1e-5):
        _andon("the front face's normal is not the view axis (min %.6f)"
               % float((n @ dtc).min()))
    ids = np.unique(aov["surfid"][aov["sil"]])
    if ids.size < 2 or (ids < 0).any():
        _andon("surfid on a single face should span a band of texels, got %r"
               % (ids[:8],))
    if aov["depth"][~aov["sil"]].min() != np.inf:
        _andon("background depth is not +inf")
    if np.isfinite(aov["pos"][~aov["sil"]]).any():
        _andon("background pos is not NaN")
    if (aov["surfid"][~aov["sil"]] != -1).any():
        _andon("background surfid is not -1")


def _selftest_occlusion_orders_depth():
    """Two boxes, one behind the other: the near one wins every shared pixel."""
    v, f, uv, n = fixture_box(0.2)
    v2 = v.copy()
    v2[:, 1] += 0.6                      # farther along +Y, i.e. behind a yaw-0 cam
    V = np.concatenate([v, v2], axis=0)
    F = np.concatenate([f, f + len(v)], axis=0)
    UV = np.concatenate([uv, uv], axis=0)
    N = np.concatenate([n, n], axis=0)
    scene = Scene(V, F, uv=UV, vnormals_canon=N)
    cam = make_cam(0.0, 0.0, [0.0, 0.0, 0.0], 1.2, 0.9, 64, 64)
    aov = cast_view(scene, cam, atlas_res=64)
    d = aov["depth"][aov["sil"]]
    # every hit must be the NEAR box's front face: depth == -(P-bmid).dtc with
    # dtc = (0,-1,0) so depth = P_y, and the near front face is at y = -0.2
    if not np.allclose(d, -0.2, rtol=0.0, atol=1e-5):
        _andon("occlusion failed: depths span %.4f..%.4f, the near face is -0.2"
               % (float(d.min()), float(d.max())))


def _selftest_gate_can_fire():
    scene = fixture_scene(0.25)
    cam = make_cam(0.0, 0.0, [0.0, 0.0, 0.0], 1.0, 0.75, 48, 64)
    aov = cast_view(scene, cam, atlas_res=64)
    gate_silhouette(aov["sil"], aov["sil"], "identity")   # must not raise
    wrong = aov["sil"].copy()
    ys, xs = np.nonzero(wrong)
    wrong[ys[0], xs[0]] = ~wrong[ys[0], xs[0]]
    try:
        gate_silhouette(aov["sil"], wrong, "one-pixel")
    except Andon as e:
        if "1 differing px" not in str(e):
            _andon("the gate fired but did not report the count: %s" % e)
    else:
        _andon("the silhouette gate accepted a mask differing by 1 px - "
               "a check that cannot fail is not a check")


def selftest():
    _selftest_basis_matches_the_flat_ring()
    _selftest_float32_origins_are_bit_identical_to_the_mask_tool()
    _selftest_basis_is_orthonormal_at_elevation()
    _selftest_projection_roundtrip()
    _selftest_cast_and_reproject()
    _selftest_occlusion_orders_depth()
    _selftest_gate_can_fire()
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _versions():
    import numpy as _np
    out = {"python": platform.python_version(), "numpy": _np.__version__,
           "emit_view_aovs": TOOL_VERSION}
    for mod in ("scipy", "trimesh", "PIL", "open3d"):
        try:
            m = __import__(mod)
            out[mod] = getattr(m, "__version__", "unknown")
        except Exception as e:                          # noqa: BLE001
            out[mod] = "IMPORT FAILED: %s" % type(e).__name__
    return out


def _parse_view(spec):
    """`IDX=yaw:0,el:0,anchor:PATH,image:PATH,tag:NAME` -> dict."""
    key, _, rest = spec.partition("=")
    if not rest:
        _andon("--view wants IDX=key:value,... got %r" % (spec,))
    d = {"index": int(key), "yaw": None, "el": 0.0, "anchor": None,
         "image": None, "tag": None}
    for part in rest.split(","):
        k, _, val = part.partition(":")
        k = k.strip()
        if k not in d:
            _andon("--view %s: unknown key %r (known: yaw, el, anchor, image, tag)"
                   % (key, k))
        if k in ("yaw", "el"):
            d[k] = float(val)
        elif k == "index":
            d[k] = int(val)
        else:
            d[k] = val
    if d["yaw"] is None:
        _andon("--view %s has no yaw" % key)
    if d["tag"] is None:
        d["tag"] = "view_%d" % d["index"]
    return d


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="emit per-view AOVs (depth/pos/normal/sil/surfid/weights)")
    ap.add_argument("--glb", help="mesh; UVs are read from it for surfid")
    ap.add_argument("--out", help="output directory (created)")
    ap.add_argument("--view", action="append", default=[],
                    help="IDX=yaw:Y[,el:E][,anchor:PATH][,image:PATH][,tag:NAME]")
    ap.add_argument("--aspect", default="752,1024")
    ap.add_argument("--atlas-res", type=int, default=ATLAS_RES)
    ap.add_argument("--fit-axis", default="height", choices=["height", "width"])
    ap.add_argument("--margin", type=float, default=FIT_MARGIN)
    ap.add_argument("--relative-jump", type=float, default=0.05,
                    help="callieri_border's relative_jump for the two weights")
    ap.add_argument("--no-gate", action="store_true",
                    help="emit views whose --anchor disagrees. The disagreement is "
                         "still measured and written to the manifest; this only "
                         "stops the halt, and every such view is flagged "
                         "anchor_gate:'NOT GATED' in the manifest.")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        try:
            selftest()
        except Andon as e:
            sys.stderr.write(str(e) + "\n")
            return 2
        sys.stdout.write("emit_view_aovs selftest OK (v%s)\n" % TOOL_VERSION)
        return 0

    if not (args.glb and args.out and args.view):
        ap.error("need --glb, --out and at least one --view (or --selftest)")

    import trimesh
    from PIL import Image
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import callieri_border

    W, H = (int(x) for x in args.aspect.split(","))
    views = [_parse_view(s) for s in args.view]

    m = trimesh.load(args.glb, force="mesh", process=False)
    vraw = np.asarray(m.vertices, dtype=np.float64)
    faces = np.asarray(m.faces, dtype=np.int64)
    try:
        uv = np.asarray(m.visual.uv, dtype=np.float64)
    except Exception:                                   # noqa: BLE001
        uv = None
    vnraw = np.asarray(m.vertex_normals, dtype=np.float64)
    v_canon, vmax = canonical_vertices(vraw)
    vn_canon = canonical_normals(vnraw)
    bmid, v_ext, h_ext = frame_extents(v_canon, W, H, args.fit_axis, args.margin)
    scene = Scene(v_canon, faces, uv=uv, vnormals_canon=vn_canon)
    sys.stdout.write(
        "[aov] %s: %d v / %d f  vmax %.9f  bmid %s\n"
        "[aov] frame %dx%d  v_ext %.16f  h_ext %.16f\n"
        % (os.path.basename(args.glb), len(vraw), len(faces), vmax,
           np.round(bmid, 12).tolist(), W, H, v_ext, h_ext))

    os.makedirs(args.out, exist_ok=True)
    manifest = {
        "tool": "emit_view_aovs.py", "tool_version": TOOL_VERSION,
        "tool_sha256": sha256_file(os.path.abspath(__file__)),
        "versions": _versions(),
        "glb": os.path.abspath(args.glb), "glb_sha256": sha256_file(args.glb),
        "glb_verts": int(len(vraw)), "glb_faces": int(len(faces)),
        "glb_vmax": vmax,
        "atlas_res": int(args.atlas_res),
        "aspect": [W, H], "fit_axis": args.fit_axis, "margin": args.margin,
        "relative_jump": args.relative_jump,
        "ray_origin_distance": RAY_ORIGIN_DISTANCE,
        "frame": {"bmid": bmid.tolist(), "v_ext": v_ext, "h_ext": h_ext},
        "projection_contract": [
            "px = ((P - bmid).right / h_ext + 0.5) * W - 0.5",
            "py = (0.5 - (P - bmid).up / v_ext) * H - 0.5",
            "depth = -(P - bmid).dtc",
        ],
        "background": {"depth": "+inf", "pos": "NaN", "normal_world": "NaN",
                       "sil": False, "surfid": -1},
        "gated": not args.no_gate,
        "views": {},
    }
    cams = {}

    for spec in views:
        tag = spec["tag"]
        cam = make_cam(spec["yaw"], spec["el"], bmid, v_ext, h_ext, W, H)
        aov = cast_view(scene, cam, atlas_res=args.atlas_res)
        row = {"index": spec["index"], "yaw": spec["yaw"], "el": spec["el"],
               "sil_px": int(aov["sil"].sum()),
               "sil_pct_of_frame": round(float(aov["sil"].mean() * 100), 6),
               "depth_identity_max": aov["depth_identity_max"]}

        # ANDON first: nothing is written for this view until the anchor holds.
        if spec["anchor"]:
            ref = np.asarray(Image.open(spec["anchor"]).convert("L")) > 127
            if args.no_gate:
                row["anchor"] = compare_silhouette(aov["sil"], ref)
                row["anchor_gate"] = "NOT GATED"
            else:
                row["anchor"] = gate_silhouette(aov["sil"], ref,
                                                "%s (%s)" % (tag, spec["anchor"]))
                row["anchor_gate"] = "HELD"
            row["anchor_path"] = os.path.abspath(spec["anchor"])
            row["anchor_sha256"] = sha256_file(spec["anchor"])
        else:
            row["anchor_gate"] = "NO ANCHOR SUPPLIED"

        ex, ey = reprojection_error(aov["pos"], aov["sil"], cam)
        row["reproject_max_px"] = [ex, ey]
        row["reproject_tol_px"] = REPROJECT_TOL_PX
        if not (ex < REPROJECT_TOL_PX and ey < REPROJECT_TOL_PX):
            _andon("%s: reprojection error %.4f / %.4f px exceeds %.2f - the "
                   "stored positions do not land on their own pixel centres"
                   % (tag, ex, ey, REPROJECT_TOL_PX))

        wb = callieri_border.border_weight(
            aov["depth"].astype(np.float64), aov["sil"],
            relative_jump=args.relative_jump)
        rej = callieri_border.mixed_depth_reject(
            aov["depth"].astype(np.float64), relative_jump=args.relative_jump)
        edge = callieri_border.depth_edge_mask(
            aov["depth"].astype(np.float64), relative_jump=args.relative_jump)

        vd = os.path.join(args.out, tag)
        os.makedirs(vd, exist_ok=True)
        np.save(os.path.join(vd, "depth.npy"), aov["depth"])
        np.save(os.path.join(vd, "pos.npy"), aov["pos"])
        np.save(os.path.join(vd, "normal_world.npy"), aov["normal_world"])
        np.save(os.path.join(vd, "sil.npy"), aov["sil"])
        np.save(os.path.join(vd, "surfid.npy"), aov["surfid"])
        np.save(os.path.join(vd, "weight_border.npy"), wb)
        np.save(os.path.join(vd, "reject.npy"), rej)
        np.save(os.path.join(vd, "depth_edge.npy"), edge)
        Image.fromarray((aov["sil"] * 255).astype(np.uint8), mode="L").save(
            os.path.join(vd, "sil.png"))

        row["arrays"] = {
            "depth": "depth.npy", "pos": "pos.npy",
            "normal_world": "normal_world.npy", "sil": "sil.npy",
            "surfid": "surfid.npy", "weight_border": "weight_border.npy",
            "reject": "reject.npy", "depth_edge": "depth_edge.npy",
        }
        row["stats"] = {
            "surfid_valid_px": int((aov["surfid"] >= 0).sum()),
            "surfid_unique": int(np.unique(aov["surfid"][aov["sil"]]).size)
            if aov["sil"].any() else 0,
            "front_facing_px": int(
                (np.nansum(aov["normal_world"][aov["sil"]]
                           * np.asarray(cam["dtc"], dtype=np.float32), axis=1) > 0
                 ).sum()) if aov["sil"].any() else 0,
            "depth_edge_px": int(edge.sum()),
            "depth_edge_in_sil_px": int((edge & aov["sil"]).sum()),
            "reject_in_sil_px": int((rej & aov["sil"]).sum()),
            "weight_border_mean_in_sil": round(float(wb[aov["sil"]].mean()), 6)
            if aov["sil"].any() else 0.0,
            "depth_min": float(aov["depth"][aov["sil"]].min())
            if aov["sil"].any() else None,
            "depth_max": float(aov["depth"][aov["sil"]].max())
            if aov["sil"].any() else None,
        }

        if spec["image"]:
            im = Image.open(spec["image"])
            im.save(os.path.join(vd, "twin.png"))
            row["image_src"] = os.path.abspath(spec["image"])
            row["image_sha256"] = sha256_file(spec["image"])
            row["image_size"] = list(im.size)
            if list(im.size) != [W, H]:
                _andon("%s: image %s is %s, the frame is %dx%d"
                       % (tag, spec["image"], im.size, W, H))
        else:
            row["image_src"] = None

        cams[tag] = cam
        manifest["views"][tag] = row
        sys.stdout.write(
            "[aov] %-14s yaw %6.1f el %5.1f  sil %7d px (%6.3f%%)  "
            "anchor %s  reproj %.2e/%.2e px\n"
            % (tag, spec["yaw"], spec["el"], row["sil_px"],
               row["sil_pct_of_frame"],
               (str(row["anchor"]["diff_px"]) + " diff")
               if "anchor" in row else row["anchor_gate"], ex, ey))

    with open(os.path.join(args.out, "cams.json"), "w") as fh:
        json.dump(cams, fh, indent=1)
    with open(os.path.join(args.out, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)
    sys.stdout.write("[aov] wrote %d views + cams.json + manifest.json -> %s\n"
                     % (len(views), args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
