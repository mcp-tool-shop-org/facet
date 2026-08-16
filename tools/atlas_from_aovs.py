# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Rebuild a 4096 atlas from the E45 AOV bundle. Texel-driven. Flow optional.

WHY THIS EXISTS. S3 stills answer "can the plates compose" in image space.
The current picture is a RENDER of the ATLAS. This tool closes that gap:
the same weighting logic as s3_composite, applied at every valid atlas
texel, flow off and flow on, so the warp hypothesis is tested on the
asset. It is project_twins with a flow hook, built from the contracts.
The shipped projector is not imported and not modified.

WHAT IT IS NOT. No island dilation, no gutter fill, no hole flood, no
brush strokes. The shipped finalize's machinery is not modelled, so
this atlas is not a rebuild of the shipped atlas and must not be
compared to it as one. The comparison it exists for is flow-off vs
flow-on under identical policy. Unwritten texels are the sentinel in
both arms equally. Identical speckle cancels in the A/B; filling it
would be the first step down the flood's road and is refused.

DESIGN. For every valid atlas texel: decode world P from the recorded
prep bake, project into each view by the cams contract, test visibility
against the bundle's depth (same local tau as the compositor), weight
by weight_border x facing^alpha at the projected position (reject and
off-silhouette take no contribution), sample the twin at
(px + flow_x, py + flow_y), resolve per texel.

  --mode owner   argmax weight. The compositor's VI logic. DEFAULT.
  --mode blend   weighted mean of valid views.

The A/B is the same command +/- --flow-dir. Everything else identical
by construction. Owner hides disagreement (one view wins). Blend shows
warp damage more legibly. The seat that runs the chain should run the
2x2 (owner/blend x off/on); this tool exposes both modes and does not
pick the matrix for them.

DECODE (do not re-derive). pos.npy is unit-cube [0,1] remapped from
the permuted-but-unnormalised bbox meta.lo/hi. Verbatim from
texpass_finalize.py:84-86 and e10_contact_mask.py:103-112:

    P = (pos * (hi - lo) + lo) / maxabs * 0.5
    N = normalise(nor * 2 - 1)

Valid texels: mask[..., 0] > 0.5 when mask is (H,W,3); mask > 0.5
when it is (H,W). That is bake_hero_fuse's rule, not a new one.

PROJECTION / VISIBILITY / FLOW. Imported from s3_composite so the
atlas and the stills cannot drift. Flow sign is flow_estimate's:
the paint that belongs at (px, py) sits at (px + flow_x, py + flow_y).
Looked up at the unwarped (px, py).

WHAT THIS ASSUMES, NAMED.

  * E06/C1/prep is the bake. T50 pins finalize's replay against it.
    Another prep is a different asset.
  * twin_i pairs with view_i in the bundle. Measured, not re-derived.
  * mask.npy is 3-channel float on the recorded bake. The brief did
    not say so; bake_hero_fuse did.
  * Texel Pmid is NOT cam bmid (z off by ~8e-4 on W3: texels do not
    hit the mesh AABB). The real-data anchor is: mesh-frame extents
    from prep_uv.glb match cams.json inside float32 (E45's 0.000e+00),
    AND every decoded valid P lies inside that mesh AABB. A
    texel-mid==cam-mid check would fail a correct decode.
  * This output is not atlas_final.png. Do not byte-compare them.

CALIBRATION CLAIM (run --selftest; T83 pins the same number).
  Atlas 32x32. One +Z ortho camera, h_ext=v_ext=2, W=H=32, bmid=0.
  Twin is a horizontal ramp twin[y, x] = x / 32. The plate is rolled
  +3 in x (dest[x] = source[x-3]) and flow_x = +3.
  Texel (16, 16) projects to pixel (16, 16). Sample at 16+3 = 19
  reads dest[19] = source[16] = 16/32 = 0.5.
  atlas[16, 16, 0] == 0.5.
  A forgotten flow lands 13/32 = 0.40625. A flipped sign lands
  10/32 = 0.3125.

  python tools/atlas_from_aovs.py --selftest

YES/NO INTERVALS.

  atlas            sentinel on unwritten (default magenta 255,0,255).
                   a plate colour in [0,1] on written texels.
  owner            -1 unwritten. 0..V-1 = winning view (argmax weight,
                   first view on a tie). Written in both modes.
  weight           best (max) weight. 0 on unwritten.
  coverage         written / valid, numerator and denominator.
  decode           P = (pos*(hi-lo)+lo)/maxabs*0.5. The synthetic
                   leg pins 0.5. The real-data --anchor pins the
                   mesh-frame vs cams.json.

  python tools/atlas_from_aovs.py --aov DIR --prep DIR --out DIR
         [--flow-dir DIR] [--mode owner|blend] [--alpha 6]
         [--sentinel 255,0,255]
  python tools/atlas_from_aovs.py --anchor --aov DIR --prep DIR
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

import numpy as np
from PIL import Image

_TOOLS = os.path.dirname(os.path.abspath(__file__))
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import s3_composite as S  # noqa: E402
import s3_run as R  # noqa: E402

TOOL_VERSION = "1.0.0"
DEFAULT_ALPHA = S.DEFAULT_ALPHA
DEFAULT_RELATIVE_JUMP = S.DEFAULT_RELATIVE_JUMP
DEFAULT_SENTINEL = (255, 0, 255)
CALIBRATION_ROW = 16
CALIBRATION_COL = 16
CALIBRATION_RED = 0.5
# Containment slop for decoded P vs the mesh AABB. float32 spacing on
# a ~1-unit mesh is ~1e-7; texels sit ~1e-6 to 1e-3 inside the box.
# 1e-4 fails a 2x decode and passes the recorded bake.
AABB_SLOP = 1e-4


class Andon(ValueError):
    """A fired gate. Never an `assert`."""


def _andon(msg):
    raise Andon("ANDON: " + msg)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def decode_pos(pos, meta):
    """Unit-cube pos.npy -> canonical world. finalize.py:84-86 verbatim."""
    if "lo" not in meta or "hi" not in meta or "maxabs" not in meta:
        _andon("meta.json missing lo/hi/maxabs")
    lo = np.asarray(meta["lo"], dtype=np.float64).reshape(3)
    hi = np.asarray(meta["hi"], dtype=np.float64).reshape(3)
    mx = float(meta["maxabs"])
    if not np.isfinite(mx) or mx <= 0.0:
        _andon("maxabs must be finite and > 0, got %r" % mx)
    p = np.asarray(pos, dtype=np.float64)
    if p.shape[-1] != 3:
        _andon("pos last axis must be 3, got %s" % (p.shape,))
    return (p * (hi - lo) + lo) / mx * 0.5


def decode_nor(nor):
    """nor.npy is *2-1 encoded. finalize.py:86-87."""
    n = np.asarray(nor, dtype=np.float64) * 2.0 - 1.0
    if n.shape[-1] != 3:
        _andon("nor last axis must be 3, got %s" % (n.shape,))
    ln = np.linalg.norm(n, axis=-1, keepdims=True)
    return n / (ln + 1e-12)


def valid_mask(mask):
    """bake_hero_fuse: mask[..., 0] > 0.5 on a 3-channel bake."""
    a = np.asarray(mask)
    if a.ndim == 2:
        return a > 0.5
    if a.ndim == 3 and a.shape[-1] >= 1:
        return a[..., 0] > 0.5
    _andon("mask must be (H,W) or (H,W,C), got %s" % (a.shape,))


def load_prep(prep_dir):
    meta_p = os.path.join(prep_dir, "meta.json")
    mask_p = os.path.join(prep_dir, "mask.npy")
    pos_p = os.path.join(prep_dir, "pos.npy")
    nor_p = os.path.join(prep_dir, "nor.npy")
    for p in (meta_p, mask_p, pos_p, nor_p):
        if not os.path.isfile(p):
            _andon("prep missing %s" % p)
    with open(meta_p, encoding="utf-8") as f:
        meta = json.load(f)
    mask = np.load(mask_p)
    pos = np.load(pos_p)
    nor = np.load(nor_p)
    valid = valid_mask(mask)
    if pos.shape[:2] != valid.shape or nor.shape[:2] != valid.shape:
        _andon(
            "prep shape mismatch: mask %s pos %s nor %s"
            % (mask.shape, pos.shape, nor.shape))
    if not valid.any():
        _andon("prep mask has no valid texels")
    return {
        "meta": meta,
        "valid": valid,
        "pos": pos,
        "nor": nor,
        "paths": {
            "meta": os.path.abspath(meta_p),
            "mask": os.path.abspath(mask_p),
            "pos": os.path.abspath(pos_p),
            "nor": os.path.abspath(nor_p),
        },
    }


def paint(P, N, views, mode="owner", alpha=DEFAULT_ALPHA,
          relative_jump=DEFAULT_RELATIVE_JUMP):
    """Per-texel resolve. P, N are (Ntex, 3). Returns colour, owner, weight, written."""
    if mode not in ("owner", "blend"):
        _andon("mode must be owner or blend, got %r" % (mode,))
    P = np.asarray(P, dtype=np.float64)
    N = np.asarray(N, dtype=np.float64)
    if P.ndim != 2 or P.shape[1] != 3 or N.shape != P.shape:
        _andon("P and N must be (N,3) and match, got %s %s" % (P.shape, N.shape))
    if not views:
        _andon("no views")
    n = P.shape[0]
    best_w = np.full(n, -1.0, dtype=np.float64)
    best_v = np.full(n, -1, dtype=np.int16)
    best_c = np.zeros((n, 3), dtype=np.float64)
    acc_c = np.zeros((n, 3), dtype=np.float64)
    acc_w = np.zeros(n, dtype=np.float64)
    for vi, view in enumerate(views):
        S._check_view(view, vi)
        samp = S.sample_view(view, P, relative_jump=relative_jump)
        fac = S.facing_of(N, view["cam"]["dtc"], exponent=alpha)
        w = np.where(samp["valid"], samp["border"] * fac, 0.0)
        acc_c += w[:, None] * samp["colour"]
        acc_w += w
        better = samp["valid"] & (w > best_w)
        if better.any():
            best_w[better] = w[better]
            best_v[better] = vi
            best_c[better] = samp["colour"][better]
    if mode == "owner":
        written = best_v >= 0
        colour = best_c
    else:
        written = acc_w > 0.0
        colour = np.zeros((n, 3), dtype=np.float64)
        if written.any():
            colour[written] = acc_c[written] / acc_w[written, None]
    return {
        "colour": colour.astype(np.float32),
        "owner": best_v,
        "weight": np.where(best_v >= 0, best_w, 0.0).astype(np.float32),
        "written": written,
    }


def scatter(valid, painted, sentinel=DEFAULT_SENTINEL):
    """Paint per-valid-texel results back onto the atlas grid."""
    h, w = valid.shape
    atlas = np.zeros((h, w, 3), dtype=np.float32)
    owner = np.full((h, w), -1, dtype=np.int8)
    weight = np.zeros((h, w), dtype=np.float32)
    sent = np.asarray(sentinel, dtype=np.float64).reshape(3)
    if sent.max() > 1.0:
        sent = sent / 255.0
    atlas[...] = sent.astype(np.float32)
    if not valid.any():
        return atlas, owner, weight
    atlas[valid] = painted["colour"]
    ys, xs = np.nonzero(valid)
    keep = painted["written"]
    atlas[ys[~keep], xs[~keep]] = sent.astype(np.float32)
    owner[ys[keep], xs[keep]] = painted["owner"][keep].astype(np.int8)
    weight[ys[keep], xs[keep]] = painted["weight"][keep]
    return atlas, owner, weight


def save_atlas_png(path, atlas_01):
    pix = np.clip(np.asarray(atlas_01) * 255.0, 0, 255).astype(np.uint8)
    Image.fromarray(pix).save(path)


def parse_sentinel(s):
    parts = [int(x) for x in str(s).split(",")]
    if len(parts) != 3 or any(c < 0 or c > 255 for c in parts):
        _andon("sentinel must be R,G,B in 0..255, got %r" % (s,))
    return tuple(parts)


def canonical_mesh_verts(glb_path):
    """texpass_iter / e10_contact_mask frame. trimesh only here."""
    import trimesh
    m = trimesh.load(glb_path, force="mesh", process=False)
    v = np.asarray(m.vertices, dtype=np.float64)
    if v.size == 0:
        _andon("mesh has no vertices: %s" % glb_path)
    return np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5


def frame_extents(v_canon, W, H, margin=1.204, fit_axis="height"):
    """Same block as emit_view_aovs.frame_extents."""
    blo, bhi = v_canon.min(axis=0), v_canon.max(axis=0)
    bmid = (blo + bhi) / 2.0
    if fit_axis == "height":
        v_ext = (bhi[2] - blo[2]) * margin
        h_ext = v_ext * (W / float(H))
    elif fit_axis == "width":
        h_ext = max(bhi[0] - blo[0], bhi[1] - blo[1]) * margin
        v_ext = h_ext * (H / float(W))
    else:
        _andon("fit_axis must be height or width")
    return bmid, float(v_ext), float(h_ext)


def _float32_tol(values):
    scale = max(1.0, float(np.max(np.abs(values))))
    return float(np.finfo(np.float32).eps) * 8.0 * scale


def anchor_real(aov_dir, prep_dir):
    """Real-data decode anchor. Cheap: prep + cams + prep_uv.glb. No twins."""
    cams_p = os.path.join(aov_dir, "cams.json")
    glb_p = os.path.join(prep_dir, "prep_uv.glb")
    if not os.path.isfile(cams_p):
        _andon("anchor: no cams.json under %s" % aov_dir)
    if not os.path.isfile(glb_p):
        _andon("anchor: no prep_uv.glb under %s" % prep_dir)
    with open(cams_p, encoding="utf-8") as f:
        cams = json.load(f)
    names = sorted(k for k in cams if k.startswith("view_"))
    if not names:
        _andon("anchor: cams.json has no view_* keys")
    cam0 = cams[names[0]]
    verts = canonical_mesh_verts(glb_p)
    bmid, v_ext, h_ext = frame_extents(verts, int(cam0["W"]), int(cam0["H"]))
    want_b = np.asarray(cam0["bmid"], dtype=np.float64)
    tb = _float32_tol(np.concatenate([bmid, want_b]))
    db = float(np.max(np.abs(bmid - want_b)))
    dv = abs(v_ext - float(cam0["v_ext"]))
    dh = abs(h_ext - float(cam0["h_ext"]))
    tv = _float32_tol([v_ext, cam0["v_ext"]])
    th = _float32_tol([h_ext, cam0["h_ext"]])
    if db > tb or dv > tv or dh > th:
        _andon(
            "mesh-frame vs cams.json exceeds float32: "
            "|bmid|=%.3e (tol %.3e) |v_ext|=%.3e (tol %.3e) |h_ext|=%.3e (tol %.3e)"
            % (db, tb, dv, tv, dh, th))
    prep = load_prep(prep_dir)
    P = decode_pos(prep["pos"][prep["valid"]], prep["meta"])
    blo, bhi = verts.min(0), verts.max(0)
    below = (blo - AABB_SLOP) - P.min(0)
    above = P.max(0) - (bhi + AABB_SLOP)
    if np.any(below > 0) or np.any(above > 0):
        _andon(
            "decoded texels leave the mesh AABB: below=%s above=%s"
            % (below, above))
    return {
        "bmid_abs": db,
        "v_ext_abs": dv,
        "h_ext_abs": dh,
        "n_valid": int(prep["valid"].sum()),
        "P_min": [float(x) for x in P.min(0)],
        "P_max": [float(x) for x in P.max(0)],
        "mesh_min": [float(x) for x in blo],
        "mesh_max": [float(x) for x in bhi],
    }


def run(aov_dir, prep_dir, out_dir, flow_dir=None, mode="owner",
        alpha=DEFAULT_ALPHA, relative_jump=DEFAULT_RELATIVE_JUMP,
        sentinel=DEFAULT_SENTINEL):
    prep = load_prep(prep_dir)
    views = R.load_bundle(aov_dir, flow_dir=flow_dir)
    valid = prep["valid"]
    P = decode_pos(prep["pos"][valid], prep["meta"])
    Nrm = decode_nor(prep["nor"][valid])
    painted = paint(
        P, Nrm, views, mode=mode, alpha=alpha, relative_jump=relative_jump)
    atlas, owner, weight = scatter(valid, painted, sentinel=sentinel)
    os.makedirs(out_dir, exist_ok=True)
    png_p = os.path.join(out_dir, "atlas.png")
    own_p = os.path.join(out_dir, "owner.npy")
    w_p = os.path.join(out_dir, "weight.npy")
    save_atlas_png(png_p, atlas)
    np.save(own_p, owner)
    np.save(w_p, weight)
    n_valid = int(valid.sum())
    n_written = int(painted["written"].sum())
    consumed = []
    for key, path in prep["paths"].items():
        consumed.append({"role": "prep_" + key, "path": path,
                         "sha256": sha256_file(path)})
    cams_p = os.path.join(aov_dir, "cams.json")
    consumed.append({"role": "cams", "path": os.path.abspath(cams_p),
                     "sha256": sha256_file(cams_p)})
    if flow_dir is not None:
        consumed.append({"role": "flow_dir", "path": os.path.abspath(flow_dir),
                         "sha256": None})
    man = {
        "tool": "atlas_from_aovs.py",
        "tool_version": TOOL_VERSION,
        "numpy_version": np.__version__,
        "aov": os.path.abspath(aov_dir),
        "prep": os.path.abspath(prep_dir),
        "flow_dir": None if flow_dir is None else os.path.abspath(flow_dir),
        "mode": mode,
        "alpha": float(alpha),
        "relative_jump": float(relative_jump),
        "sentinel": list(sentinel),
        "n_views": len(views),
        "valid_texels": n_valid,
        "written_texels": n_written,
        "coverage": "%d/%d" % (n_written, n_valid),
        "consumed": consumed,
        "outputs": {
            "atlas": os.path.abspath(png_p),
            "owner": os.path.abspath(own_p),
            "weight": os.path.abspath(w_p),
        },
    }
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(man, f, indent=1)
    return man


# ---------------------------------------------------------------------------
# fixtures and selftest
# ---------------------------------------------------------------------------

def _ramp_twin(h, w):
    """twin[y, x] = x / w. Integer sample at x is exact."""
    xs = np.arange(w, dtype=np.float64)
    ramp = np.broadcast_to(xs / float(w), (h, w)).copy()
    return np.stack([ramp, np.zeros_like(ramp), np.zeros_like(ramp)], axis=-1)


def _plane_prep(res, cam):
    """Texel (r, c) decodes to the world point that projects to pixel (c, r)."""
    rows, cols = np.indices((res, res))
    # invert the cams contract so px=c, py=r exactly at texel centres
    Px = ((cols.astype(np.float64) + 0.5) / cam["W"] - 0.5) * cam["h_ext"]
    Py = (0.5 - (rows.astype(np.float64) + 0.5) / cam["H"]) * cam["v_ext"]
    Pz = np.zeros_like(Px)
    # camera at origin, right=X, up=Y, so world = (Px, Py, 0)
    P = np.stack([Px, Py, Pz], axis=-1)
    # invert decode: lo=-1, hi=1, maxabs=1 => P = pos - 0.5 => pos = P + 0.5
    meta = {"lo": [-1.0, -1.0, -1.0], "hi": [1.0, 1.0, 1.0], "maxabs": 1.0}
    pos = P + 0.5
    # facing the camera: dtc = (0, 0, -1) => N = (0, 0, -1)
    # encoded: (N + 1) / 2
    n_world = np.zeros_like(P)
    n_world[..., 2] = -1.0
    nor = (n_world + 1.0) / 2.0
    mask = np.ones((res, res), dtype=np.float64)
    return pos, nor, mask, meta, P


def _z_cam(res):
    return {
        "right": [1.0, 0.0, 0.0],
        "up": [0.0, 1.0, 0.0],
        "dtc": [0.0, 0.0, -1.0],
        "bmid": [0.0, 0.0, 0.0],
        "h_ext": 2.0,
        "v_ext": 2.0,
        "W": int(res),
        "H": int(res),
    }


def _view_from(cam, twin, depth=None, sil=None, reject=None, border=None,
               flow=None):
    h, w = twin.shape[:2]
    if depth is None:
        depth = np.zeros((h, w), dtype=np.float64)
    if sil is None:
        sil = np.ones((h, w), dtype=bool)
    if reject is None:
        reject = np.zeros((h, w), dtype=bool)
    if border is None:
        border = np.ones((h, w), dtype=np.float64)
    pos = np.zeros((h, w, 3), dtype=np.float64)
    nrm = np.zeros((h, w, 3), dtype=np.float64)
    nrm[..., 2] = -1.0
    view = {
        "twin": np.asarray(twin, dtype=np.float64),
        "depth": np.asarray(depth, dtype=np.float64),
        "sil": np.asarray(sil, dtype=bool),
        "pos": pos,
        "normal_world": nrm,
        "surfid": np.zeros((h, w), dtype=np.int32),
        "weight_border": np.asarray(border, dtype=np.float64),
        "reject": np.asarray(reject, dtype=bool),
        "cam": cam,
    }
    if flow is not None:
        view["flow"] = np.asarray(flow, dtype=np.float64)
    return view


def fixture_sign(res=32, shift=3):
    cam = _z_cam(res)
    pos, nor, mask, meta, _P = _plane_prep(res, cam)
    src = _ramp_twin(res, res)
    dest = np.roll(src, shift, axis=1)
    flow = np.zeros((res, res, 2), dtype=np.float64)
    flow[..., 0] = float(shift)
    view = _view_from(cam, dest, flow=flow)
    return pos, nor, mask, meta, [view]


def fixture_flow_ab(res=32, shift=3):
    """Same plate, with and without the true flow."""
    cam = _z_cam(res)
    pos, nor, mask, meta, _P = _plane_prep(res, cam)
    src = _ramp_twin(res, res)
    dest = np.roll(src, shift, axis=1)
    flow = np.zeros((res, res, 2), dtype=np.float64)
    flow[..., 0] = float(shift)
    off = _view_from(cam, dest)
    on = _view_from(cam, dest, flow=flow)
    truth = _view_from(cam, src)
    return pos, nor, mask, meta, off, on, truth


def fixture_occlusion(res=32):
    """Back plane at z=0.5, front depth map at z=0. Back texels get nothing."""
    cam = _z_cam(res)
    pos, nor, mask, meta, P = _plane_prep(res, cam)
    # move every texel to z=0.5 (farther). depth map stays 0 (front).
    # decode uses pos; rewrite pos so decoded P.z = 0.5
    # P = pos - 0.5  => pos.z = P.z + 0.5 = 1.0
    pos = pos.copy()
    pos[..., 2] = 1.0
    twin = _ramp_twin(res, res)
    depth = np.zeros((res, res), dtype=np.float64)
    view = _view_from(cam, twin, depth=depth)
    return pos, nor, mask, meta, [view]


def _paint_prep(pos, nor, mask, meta, views, mode="owner"):
    valid = valid_mask(mask)
    P = decode_pos(pos[valid], meta)
    Nrm = decode_nor(nor[valid])
    painted = paint(P, Nrm, views, mode=mode)
    atlas, owner, weight = scatter(valid, painted)
    return atlas, owner, weight, painted


def _selftest_calibration():
    pos, nor, mask, meta, views = fixture_sign(32, shift=3)
    atlas, _o, _w, _p = _paint_prep(pos, nor, mask, meta, views)
    got = float(atlas[CALIBRATION_ROW, CALIBRATION_COL, 0])
    if abs(got - CALIBRATION_RED) > 1e-12:
        _andon(
            "calibration atlas[%d,%d,0] is %r, not %s"
            % (CALIBRATION_ROW, CALIBRATION_COL, got, CALIBRATION_RED))
    return got


def _selftest_flow_recovers():
    pos, nor, mask, meta, off, on, truth = fixture_flow_ab(32, shift=3)
    a_off, _, _, _ = _paint_prep(pos, nor, mask, meta, [off])
    a_on, _, _, _ = _paint_prep(pos, nor, mask, meta, [on])
    a_true, _, _, _ = _paint_prep(pos, nor, mask, meta, [truth])
    # interior, away from the roll wrap
    sl = (slice(4, 28), slice(4, 28), 0)
    err_off = float(np.max(np.abs(a_off[sl] - a_true[sl])))
    err_on = float(np.max(np.abs(a_on[sl] - a_true[sl])))
    if err_off < 0.05:
        _andon("flow-off atlas did not degrade (max abs %r)" % err_off)
    if err_on > 1e-12:
        _andon("flow-on atlas did not recover (max abs %r)" % err_on)


def _selftest_occlusion():
    pos, nor, mask, meta, views = fixture_occlusion(32)
    _atlas, owner, _w, painted = _paint_prep(pos, nor, mask, meta, views)
    if painted["written"].any():
        _andon(
            "occluded texels took a contribution (%d written)"
            % int(painted["written"].sum()))
    if np.any(owner >= 0):
        _andon("occluded owner is not -1")


def _selftest_decode():
    # lo=0, hi=2, maxabs=2, pos=1 -> P = (1*2+0)/2*0.5 = 0.5
    meta = {"lo": [0.0, 0.0, 0.0], "hi": [2.0, 2.0, 2.0], "maxabs": 2.0}
    pos = np.array([[[1.0, 1.0, 1.0]]])
    P = decode_pos(pos, meta)
    got = float(P[0, 0, 0])
    if got != 0.5:
        _andon("unit-cube decode P[0] is %r, not 0.5" % got)
    # drop *0.5 would be 1.0; drop /maxabs would be 1.0


def _selftest_andon_can_fail():
    try:
        decode_pos(np.zeros((1, 1, 3)), {"lo": [0, 0, 0], "hi": [1, 1, 1],
                                         "maxabs": 0})
    except Andon:
        pass
    else:
        _andon("maxabs=0 did not fire")
    try:
        paint(np.zeros((1, 3)), np.zeros((1, 3)), [], mode="owner")
    except Andon:
        pass
    else:
        _andon("empty views did not fire")


def selftest():
    got = _selftest_calibration()
    _selftest_flow_recovers()
    _selftest_occlusion()
    _selftest_decode()
    _selftest_andon_can_fail()
    return got


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Rebuild an atlas from an AOV bundle (flow optional)")
    p.add_argument("--aov", default=None)
    p.add_argument("--prep", default=None)
    p.add_argument("--out", default=None)
    p.add_argument("--flow-dir", default=None)
    p.add_argument("--mode", default="owner", choices=("owner", "blend"))
    p.add_argument("--alpha", type=float, default=DEFAULT_ALPHA)
    p.add_argument("--relative-jump", type=float, default=DEFAULT_RELATIVE_JUMP)
    p.add_argument("--sentinel", default="255,0,255")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--anchor", action="store_true")
    args = p.parse_args(argv)
    if args.selftest:
        try:
            selftest()
        except (Andon, S.Andon, R.Andon) as e:
            sys.stderr.write(str(e) + "\n")
            return 2
        sys.stdout.write(
            "atlas_from_aovs selftest OK  calibration atlas[%d,%d,0] == %s\n"
            % (CALIBRATION_ROW, CALIBRATION_COL, CALIBRATION_RED))
        return 0
    if args.anchor:
        if not args.aov or not args.prep:
            p.error("--anchor needs --aov and --prep")
        try:
            info = anchor_real(args.aov, args.prep)
        except (Andon, S.Andon, R.Andon) as e:
            sys.stderr.write(str(e) + "\n")
            return 2
        sys.stdout.write(
            "atlas_from_aovs anchor OK  |bmid|=%.3e  |v_ext|=%.3e  "
            "|h_ext|=%.3e  valid=%d\n"
            % (info["bmid_abs"], info["v_ext_abs"], info["h_ext_abs"],
               info["n_valid"]))
        return 0
    if not args.aov or not args.prep or not args.out:
        p.error("need --aov --prep --out (or --selftest / --anchor)")
    try:
        sent = parse_sentinel(args.sentinel)
        man = run(
            args.aov, args.prep, args.out, flow_dir=args.flow_dir,
            mode=args.mode, alpha=args.alpha,
            relative_jump=args.relative_jump, sentinel=sent)
    except (Andon, S.Andon, R.Andon) as e:
        sys.stderr.write(str(e) + "\n")
        return 2
    sys.stdout.write(
        "atlas_from_aovs wrote %s  coverage %s  mode=%s\n"
        % (man["outputs"]["atlas"], man["coverage"], man["mode"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
