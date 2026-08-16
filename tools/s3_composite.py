# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""S3 existence proof: can the eight plates compose into one surface?

WHY THIS EXISTS. Consult #3's S3. The plates look clean; the asset does not.
No measurement this month has separated (1) plates fine, 3D path degrades them
(2) plates inconsistent across views (3) plates share the same defect. This
module is that discriminator. It is not a texture projector and it is not a
quality grade.

WHAT IT EMITS, ONE CALL.

  A  view-dependent still of a named target
  B  view-independent still of the same target
  C  owner map, disagreement map, coverage, fallback, per-view shares

POLICY, ARGUE-WITH-THE-BRIEF.

  Primary is the TARGET VIEW when that view is valid, not the global
  highest-facing plate. The brief's literal "highest-facing leads" is the
  shipped WTA and would make two targets of one plane collapse to the same
  still whenever one view dominates facing -- which makes the consistency
  leg's "VD stills MUST differ" unsatisfiable on the fixture that also has
  shared surfids. Target-first is the question S3-A actually asks: does
  THIS plate survive as the lead, with others filling only where it is
  weak (weight < primary_floor). Highest-facing remains available as
  primary_mode='facing' if a caller wants the shipped policy.

  Per-surfid argmax is the right GLOBAL field for S3-B. Waechter-style
  seam-level / Potts smoothing would hide the per-view disagreement S3
  exists to measure. If smoothing is added later it must be a per-surfid
  colour offset, computed once, applied to every target -- never a
  per-still reassignment of owner. It does not live in this module.

  Disagreement (colour dispersion across views at one surface point,
  after reprojection) does NOT subsume the warp seat's instrument (image-
  space correspondence offset of one twin against the mesh). Warp can
  cause disagreement; disagreement can exist without warp (twins painted
  differently); warp can exist without disagreement (only one view sees
  the point, or every view slips the same way). Two levers. The `flow`
  hook is how a measured warp enters this module; the disagreement map
  is how that warp, or any other inconsistency, is read in composite
  space.

  We blend in float sRGB because that is the shipped pipeline's space
  and the proof must be comparable to it. Linear-light would change
  seam brightness, not the three-world split (a 6 px slip across a
  material boundary is large in both spaces). Not switched.

WHAT THIS CANNOT SEE. A defect all eight plates share identically
produces zero disagreement and a clean-looking consensus of wrong paint.
This module proves the plates CAN or CANNOT compose. It never proves
they are right.

VISIBILITY tau. |analytic_depth(P) - sampled_depth_v| <= tau, with
    tau = max(relative_jump * IQR_v, 8 * typical_neighbour_|dZ|_v)
the same basis as callieri_border.jump (IQR of finite depth on the
silhouette; typical = median finite 4-neighbour |dZ|). Not a world-unit
constant. Figure-vs-background is already rejected by sil / reject.
A 15 px blade: internal dZ stays under typical*8; a true occluder is a
jump of the figure's depth IQR and fails the test.

PROJECTION (emitter contract, used verbatim):

    px(P) = ((P - bmid)·right / h_ext + 0.5) · W - 0.5
    py(P) = (0.5 - (P - bmid)·up / v_ext) · H - 0.5
    depth(P) = -(P - bmid)·dtc

Pixel centres sit at integer coordinates. Bilinear sample of the twin
is at (px + flow_x, py + flow_y). flow is looked up at the unwarped
(px, py). reject is the 2x2 origin (floor(py), floor(px)) from
callieri_border.mixed_depth_reject.

YES/NO INTERVALS.

  dependent / independent
      background = (0,0,0) where coverage is False.
      a plate colour in [0,1] where coverage is True.
  owner
      -1 = no valid source. 0..V-1 = view index.
  disagreement
      0 = all valid plates agree, OR only one valid plate.
      >0 = weighted RMS RGB deviation from the weighted mean.
      1 = the scale of a red-vs-green disagreement at equal weight
          (construction: two opposite unit colours, equal w).
  coverage
      True = at least one valid source. False = no plate.
  fallback
      True = target-primary weight was below primary_floor so others
      filled. False = primary used alone (or uncovered).

CALIBRATION CLAIM (run --selftest; T77 pins the same number).
  Fixture `shift_pair`: two +Z ortho cameras, 32x32, h_ext=v_ext=2,
  camera A bmid=(0,0,0), camera B bmid=(0.25,0,0), plane z=0 coloured
  ((x+1)/2, (y+1)/2, 0.25). Reproject A's plate into B. Pixel (16, 16)
  of B has red channel exactly 0.640625.
  Construction: u = ((16.5)/32 - 0.5)*2 = 0.03125; P_x = 0.25+0.03125
  = 0.28125; (0.28125+1)/2 = 0.640625. Bilinear is exact on a linear
  field; a broken inverse-projection cannot land this value.

  python tools/s3_composite.py --selftest [--out DIR]
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np
from scipy.ndimage import map_coordinates

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

TOOL_VERSION = "1.0.0"

DEFAULT_ALPHA = 6.0
DEFAULT_RELATIVE_JUMP = 0.05
DEFAULT_PRIMARY_FLOOR = 0.05
_SOBEL_L1 = 8.0

# Construction in the module docstring.
CALIBRATION_ROW = 16
CALIBRATION_COL = 16
CALIBRATION_RED = 0.640625


class Andon(ValueError):
    """A fired gate. Never an `assert`."""


def _andon(msg):
    raise Andon("ANDON: " + msg)


def _as_cam(cam):
    need = ("right", "up", "dtc", "bmid", "h_ext", "v_ext", "W", "H")
    missing = [k for k in need if k not in cam]
    if missing:
        _andon("camera missing %s" % (missing,))
    out = {
        "right": np.asarray(cam["right"], dtype=np.float64).reshape(3),
        "up": np.asarray(cam["up"], dtype=np.float64).reshape(3),
        "dtc": np.asarray(cam["dtc"], dtype=np.float64).reshape(3),
        "bmid": np.asarray(cam["bmid"], dtype=np.float64).reshape(3),
        "h_ext": float(cam["h_ext"]),
        "v_ext": float(cam["v_ext"]),
        "W": int(cam["W"]),
        "H": int(cam["H"]),
    }
    if out["h_ext"] <= 0.0 or out["v_ext"] <= 0.0:
        _andon("h_ext/v_ext must be > 0")
    if out["W"] < 2 or out["H"] < 2:
        _andon("W,H must be >= 2, got %d,%d" % (out["W"], out["H"]))
    return out


def project_point(P, cam):
    """px, py, depth -- arrays broadcast over P (..., 3)."""
    c = _as_cam(cam)
    d = np.asarray(P, dtype=np.float64) - c["bmid"]
    px = ((d * c["right"]).sum(-1) / c["h_ext"] + 0.5) * c["W"] - 0.5
    py = (0.5 - (d * c["up"]).sum(-1) / c["v_ext"]) * c["H"] - 0.5
    depth = -(d * c["dtc"]).sum(-1)
    return px, py, depth


def pixel_ray(px, py, cam):
    """World point on the camera plane through bmid for pixel (px, py)."""
    c = _as_cam(cam)
    u = ((np.asarray(px, dtype=np.float64) + 0.5) / c["W"] - 0.5) * c["h_ext"]
    v = (0.5 - (np.asarray(py, dtype=np.float64) + 0.5) / c["H"]) * c["v_ext"]
    # reshape for broadcast
    return (c["bmid"]
            + u[..., None] * c["right"]
            + v[..., None] * c["up"])


def _typical_neighbour_abs(depth):
    fin = np.isfinite(depth)
    chunks = []
    pair = fin[:, :-1] & fin[:, 1:]
    if pair.any():
        chunks.append(np.abs(depth[:, :-1][pair] - depth[:, 1:][pair]))
    pair = fin[:-1, :] & fin[1:, :]
    if pair.any():
        chunks.append(np.abs(depth[:-1, :][pair] - depth[1:, :][pair]))
    if not chunks:
        return 0.0
    return float(np.median(np.concatenate(chunks)))


def _figure_iqr(depth, sil):
    z = depth[sil & np.isfinite(depth)]
    if z.size < 4:
        return 0.0
    q25, q75 = np.percentile(z, [25.0, 75.0])
    return float(q75 - q25)


def visibility_tau(depth, sil, relative_jump=DEFAULT_RELATIVE_JUMP):
    """World-unit depth tolerance, same basis as callieri_border."""
    if not np.isfinite(relative_jump) or relative_jump <= 0.0:
        _andon("relative_jump must be finite and > 0, got %r" % (relative_jump,))
    iqr = _figure_iqr(depth, sil)
    typical = _typical_neighbour_abs(depth)
    return max(relative_jump * iqr, _SOBEL_L1 * typical)


def _bilinear(arr, px, py, cval=0.0):
    """Sample arr at (px, py). arr is (H,W) or (H,W,C). px/py broadcast."""
    px = np.asarray(px, dtype=np.float64)
    py = np.asarray(py, dtype=np.float64)
    out_shape = np.broadcast(px, py).shape
    pxr = np.broadcast_to(px, out_shape).reshape(-1)
    pyr = np.broadcast_to(py, out_shape).reshape(-1)
    coords = np.vstack([pyr, pxr])
    if arr.ndim == 2:
        samp = map_coordinates(arr, coords, order=1, mode="constant",
                               cval=cval, prefilter=False)
        return samp.reshape(out_shape)
    chans = [
        map_coordinates(arr[..., c], coords, order=1, mode="constant",
                        cval=cval, prefilter=False)
        for c in range(arr.shape[-1])
    ]
    return np.stack(chans, axis=-1).reshape(out_shape + (arr.shape[-1],))


def _tap_origin_valid(px, py, reject, sil):
    """True where the bilinear 2x2 is inside the frame, on-figure, not reject."""
    h, w = sil.shape
    fx = np.floor(px).astype(np.int64)
    fy = np.floor(py).astype(np.int64)
    inside = (fx >= 0) & (fy >= 0) & (fx + 1 < w) & (fy + 1 < h)
    ok = np.zeros(np.broadcast(px, py).shape, dtype=bool)
    if not inside.any():
        return ok
    ii = fy[inside]
    jj = fx[inside]
    taps = (sil[ii, jj] & sil[ii, jj + 1] & sil[ii + 1, jj] & sil[ii + 1, jj + 1]
            & ~reject[ii, jj])
    ok[inside] = taps
    return ok


def sample_view(view, P, relative_jump=DEFAULT_RELATIVE_JUMP):
    """Sample one view at world points P (..., 3).

    Returns dict of arrays over P's leading shape:
      valid, colour (...,3), weight, facing, depth_err
    """
    cam = _as_cam(view["cam"])
    px, py, z_analytic = project_point(P, cam)
    flow = view.get("flow")
    if flow is None:
        sx, sy = px, py
    else:
        flow = np.asarray(flow, dtype=np.float64)
        if flow.shape[:2] != view["sil"].shape or flow.shape[-1] != 2:
            _andon("flow must be (H,W,2) matching the view, got %s"
                   % (flow.shape,))
        fxy = _bilinear(flow, px, py, cval=0.0)
        sx = px + fxy[..., 0]
        sy = py + fxy[..., 1]
    sil = np.asarray(view["sil"], dtype=bool)
    reject = np.asarray(view["reject"], dtype=bool)
    depth = np.asarray(view["depth"], dtype=np.float64)
    twin = np.asarray(view["twin"], dtype=np.float64)
    border = np.asarray(view["weight_border"], dtype=np.float64)
    tap = _tap_origin_valid(sx, sy, reject, sil)
    z_samp = _bilinear(depth, sx, sy, cval=np.inf)
    tau = visibility_tau(depth, sil, relative_jump=relative_jump)
    depth_err = np.abs(z_analytic - z_samp)
    # tau==0: only exact match (a constant-depth plane). occluders still
    # fail because their sampled depth differs by a finite amount.
    if tau <= 0.0:
        z_ok = np.isfinite(z_samp) & (depth_err <= 1e-9)
    else:
        z_ok = np.isfinite(z_samp) & (depth_err <= tau)
    valid = tap & z_ok
    colour = _bilinear(twin, sx, sy, cval=0.0)
    w_border = _bilinear(border, sx, sy, cval=0.0)
    n = np.asarray(view["normal_world"], dtype=np.float64)
    # facing at the SOURCE view's sample, from the SOURCE's stored normals
    # at the sample location -- but facing of P should use P's own normal.
    # The caller passes P from the TARGET; use target normals via a
    # separate argument. Here we only return geometric sample + border.
    return {
        "valid": valid,
        "colour": colour,
        "border": w_border,
        "px": sx,
        "py": sy,
        "depth_err": depth_err,
        "tau": tau,
    }


def facing_of(normal, dtc, exponent=DEFAULT_ALPHA):
    if not np.isfinite(exponent) or exponent < 0.0:
        _andon("exponent must be finite and >= 0, got %r" % (exponent,))
    n = np.asarray(normal, dtype=np.float64)
    v = np.asarray(dtc, dtype=np.float64).reshape(3)
    v = v / max(float(np.linalg.norm(v)), 1e-12)
    nlen = np.linalg.norm(n, axis=-1, keepdims=True)
    nn = np.divide(n, np.maximum(nlen, 1e-12))
    dot = (nn * v.reshape((1,) * (n.ndim - 1) + (3,))).sum(-1)
    return np.clip(dot, 0.0, 1.0) ** exponent


def _check_view(view, i):
    sil = np.asarray(view["sil"], dtype=bool)
    h, w = sil.shape
    cam = _as_cam(view["cam"])
    if cam["H"] != h or cam["W"] != w:
        _andon("view %d cam HxW %d,%d != array %d,%d" % (i, cam["H"], cam["W"], h, w))
    for key, ch in (("twin", 3), ("pos", 3), ("normal_world", 3)):
        a = np.asarray(view[key])
        if a.shape != (h, w, ch):
            _andon("view %d %s shape %s != (%d,%d,%d)" % (i, key, a.shape, h, w, ch))
    for key in ("depth", "weight_border", "surfid"):
        a = np.asarray(view[key])
        if a.shape != (h, w):
            _andon("view %d %s shape %s != (%d,%d)" % (i, key, a.shape, h, w))
    rej = np.asarray(view["reject"])
    if rej.shape != (h, w):
        _andon("view %d reject shape %s != (%d,%d)" % (i, rej.shape, h, w))
    if "flow" in view and view["flow"] is not None:
        f = np.asarray(view["flow"])
        if f.shape != (h, w, 2):
            _andon("view %d flow shape %s != (%d,%d,2)" % (i, f.shape, h, w))
    if not sil.any():
        _andon("view %d silhouette is empty" % i)


def _gather(views, target, P, n, alpha, relative_jump):
    """Per-source valid/colour/weight/facing at world points P of the target."""
    V = len(views)
    shape = P.shape[:-1]
    valid = np.zeros((V,) + shape, dtype=bool)
    colour = np.zeros((V,) + shape + (3,), dtype=np.float64)
    weight = np.zeros((V,) + shape, dtype=np.float64)
    facing = np.zeros((V,) + shape, dtype=np.float64)
    for v, view in enumerate(views):
        samp = sample_view(view, P, relative_jump=relative_jump)
        fac = facing_of(n, view["cam"]["dtc"], exponent=alpha)
        w = samp["border"] * fac
        m = samp["valid"]
        valid[v] = m
        colour[v] = samp["colour"]
        facing[v] = fac
        weight[v] = np.where(m, w, 0.0)
    return valid, colour, weight, facing


def composite_dependent(views, target, alpha=DEFAULT_ALPHA,
                        primary_floor=DEFAULT_PRIMARY_FLOOR,
                        relative_jump=DEFAULT_RELATIVE_JUMP,
                        primary_mode="target"):
    """View-dependent still of `target` (index into views).

    primary_mode:
      'target' -- the target view leads when valid (default; see module doc)
      'facing' -- highest-facing valid plate leads (shipped WTA)
    Fill from the weighted blend of all valid views where the primary
    weight is below primary_floor. Soft mix: mix = clip(w_p / floor, 0, 1).
    """
    if primary_mode not in ("target", "facing"):
        _andon("primary_mode must be 'target' or 'facing', got %r" % (primary_mode,))
    if not np.isfinite(primary_floor) or primary_floor <= 0.0:
        _andon("primary_floor must be finite and > 0")
    t = views[target]
    sil = np.asarray(t["sil"], dtype=bool)
    P = np.asarray(t["pos"], dtype=np.float64)
    n = np.asarray(t["normal_world"], dtype=np.float64)
    valid, colour, weight, facing = _gather(
        views, target, P, n, alpha, relative_jump)
    V = valid.shape[0]
    # force invalid off-silhouette
    valid[:, ~sil] = False
    weight[:, ~sil] = 0.0
    any_v = valid.any(axis=0)
    if primary_mode == "target":
        primary = np.full(sil.shape, target, dtype=np.int16)
        # where target is invalid, fall back to highest-facing valid
        need = sil & ~valid[target]
        if need.any() and V > 1:
            fac = np.where(valid, facing, -1.0)
            primary[need] = np.argmax(fac[:, need], axis=0)
    else:
        fac = np.where(valid, facing, -1.0)
        primary = np.argmax(fac, axis=0).astype(np.int16)
    # gather primary colour / weight
    yy, xx = np.indices(sil.shape)
    c_p = colour[primary, yy, xx]
    w_p = weight[primary, yy, xx]
    wsum = weight.sum(axis=0)
    blend = np.zeros(sil.shape + (3,), dtype=np.float64)
    nz = wsum > 0.0
    blend[nz] = (weight[:, nz, None] * colour[:, nz, :]).sum(axis=0) / wsum[nz, None]
    mix = np.clip(w_p / primary_floor, 0.0, 1.0)
    mix = np.where(valid[primary, yy, xx], mix, 0.0)
    out = mix[..., None] * c_p + (1.0 - mix)[..., None] * blend
    out[~any_v] = 0.0
    fallback = any_v & (w_p < primary_floor)
    contrib = np.zeros(V, dtype=np.float64)
    # share of dependent pixels whose primary is v, among covered
    cov_n = max(int(any_v.sum()), 1)
    for v in range(V):
        contrib[v] = float(((primary == v) & any_v).sum()) / cov_n
    return {
        "colour": out.astype(np.float32),
        "coverage": any_v,
        "fallback": fallback,
        "primary": primary,
        "contrib": contrib,
        "valid": valid,
        "weight": weight,
        "facing": facing,
        "samples": colour,
    }


def assign_owners(views, alpha=DEFAULT_ALPHA, relative_jump=DEFAULT_RELATIVE_JUMP):
    """Global owner(surfid) = argmax_v of that surfid's max weight in v.

    Canonical colour is the owner view's twin at the integer pixel where
    that surfid attains its max weight. Two targets then agree by
    construction at every shared surfid.
    """
    tables = []
    for v, view in enumerate(views):
        sil = np.asarray(view["sil"], dtype=bool)
        sid = np.asarray(view["surfid"], dtype=np.int64)
        n = np.asarray(view["normal_world"], dtype=np.float64)
        border = np.asarray(view["weight_border"], dtype=np.float64)
        reject = np.asarray(view["reject"], dtype=bool)
        fac = facing_of(n, view["cam"]["dtc"], exponent=alpha)
        w = np.where(sil & ~reject & (sid >= 0), border * fac, 0.0)
        # include Callieri-zero pixels: they still have a plate. A shared
        # surfid that only lives on a silhouette ring must still get an owner
        # or the consistency theorem is vacuous on the outline.
        on = sil & ~reject & (sid >= 0)
        if not on.any():
            tables.append((np.zeros(0, dtype=np.int64),
                           np.zeros(0, dtype=np.float64),
                           np.zeros(0, dtype=np.int64),
                           np.zeros(0, dtype=np.int64)))
            continue
        s_on = sid[on]
        w_on = w[on]
        ys, xs = np.nonzero(on)
        # one row per surfid: the pixel of max weight (lexsort is stable)
        order = np.lexsort((-w_on, s_on))
        s_s = s_on[order]
        keep = np.ones(s_s.size, dtype=bool)
        keep[1:] = s_s[1:] != s_s[:-1]
        tables.append((s_s[keep], w_on[order][keep],
                       ys[order][keep], xs[order][keep]))

    nonempty = [t[0] for t in tables if t[0].size]
    if not nonempty:
        _andon("no positive-weight surfid in any view")
    all_s = np.unique(np.concatenate(nonempty))
    best_w = np.full(all_s.size, -1.0, dtype=np.float64)
    best_v = np.full(all_s.size, -1, dtype=np.int16)
    best_y = np.zeros(all_s.size, dtype=np.int64)
    best_x = np.zeros(all_s.size, dtype=np.int64)
    for v, (sids, ws, ys, xs) in enumerate(tables):
        if sids.size == 0:
            continue
        idx = np.searchsorted(all_s, sids)
        better = ws > best_w[idx]
        ii = idx[better]
        best_w[ii] = ws[better]
        best_v[ii] = v
        best_y[ii] = ys[better]
        best_x[ii] = xs[better]
    colour = np.zeros((all_s.size, 3), dtype=np.float64)
    for v, view in enumerate(views):
        sel = best_v == v
        if not sel.any():
            continue
        twin = np.asarray(view["twin"], dtype=np.float64)
        colour[sel] = twin[best_y[sel], best_x[sel]]
    return {
        "surfid": all_s,
        "owner": best_v,
        "weight": best_w,
        "colour": colour,
    }


def composite_independent(views, target, assignment):
    """Paint target pixels from the global per-surfid canonical colour."""
    t = views[target]
    sid = np.asarray(t["surfid"], dtype=np.int64)
    sil = np.asarray(t["sil"], dtype=bool)
    h, w = sil.shape
    out = np.zeros((h, w, 3), dtype=np.float64)
    owner_map = np.full((h, w), -1, dtype=np.int16)
    coverage = np.zeros((h, w), dtype=bool)
    all_s = assignment["surfid"]
    colours = assignment["colour"]
    owners = assignment["owner"]
    on = sil & (sid >= 0)
    if on.any() and all_s.size:
        idx = np.searchsorted(all_s, sid)
        idx = np.clip(idx, 0, all_s.size - 1)
        found = on & (all_s[idx] == sid) & (owners[idx] >= 0)
        out[found] = colours[idx[found]]
        owner_map[found] = owners[idx[found]]
        coverage[found] = True
    return {
        "colour": out.astype(np.float32),
        "owner": owner_map,
        "coverage": coverage,
    }


def disagreement_map(valid, colour, weight):
    """Weighted RMS RGB deviation from the weighted mean, per pixel.

    0 if fewer than 2 valid plates. Scale: two opposite unit colours at
    equal weight give 1.0 (see fixture).
    """
    nval = valid.sum(axis=0)
    w = np.where(valid, weight, 0.0)
    wsum = w.sum(axis=0)
    mu = np.zeros(colour.shape[1:], dtype=np.float64)
    nz = wsum > 0.0
    mu[nz] = (w[:, nz, None] * colour[:, nz, :]).sum(axis=0) / wsum[nz, None]
    var = np.zeros(w.shape[1:], dtype=np.float64)
    for v in range(valid.shape[0]):
        d2 = ((colour[v] - mu) ** 2).sum(-1)
        var += np.where(valid[v], w[v] * d2, 0.0)
    rms = np.zeros_like(var)
    ok = (wsum > 0.0) & (nval >= 2)
    rms[ok] = np.sqrt(var[ok] / wsum[ok])
    return rms.astype(np.float32)


def s3_composite(views, target, alpha=DEFAULT_ALPHA,
                 primary_floor=DEFAULT_PRIMARY_FLOOR,
                 relative_jump=DEFAULT_RELATIVE_JUMP,
                 primary_mode="target"):
    """Run A+B+C for one target index. views is a list of view dicts."""
    if not views:
        _andon("no views")
    if target < 0 or target >= len(views):
        _andon("target %d out of range 0..%d" % (target, len(views) - 1))
    for i, v in enumerate(views):
        _check_view(v, i)
    dep = composite_dependent(
        views, target, alpha=alpha, primary_floor=primary_floor,
        relative_jump=relative_jump, primary_mode=primary_mode)
    asg = assign_owners(views, alpha=alpha, relative_jump=relative_jump)
    indep = composite_independent(views, target, asg)
    disp = disagreement_map(dep["valid"], dep["samples"], dep["weight"])
    return {
        "dependent": dep["colour"],
        "independent": indep["colour"],
        "owner": indep["owner"],
        "disagreement": disp,
        "coverage": dep["coverage"],
        "fallback": dep["fallback"],
        "contrib": dep["contrib"],
        "assignment": asg,
        "primary": dep["primary"],
    }


def reproject_plate(src, dst, relative_jump=DEFAULT_RELATIVE_JUMP):
    """src's twin, sampled at dst's world points. For the exactness leg."""
    P = np.asarray(dst["pos"], dtype=np.float64)
    samp = sample_view(src, P, relative_jump=relative_jump)
    out = samp["colour"].astype(np.float32)
    out[~samp["valid"]] = 0.0
    return out, samp["valid"]


# ---------------------------------------------------------------------------
# synthetic fixtures
# ---------------------------------------------------------------------------

def _cam_plus_z(W, H, bmid=(0.0, 0.0, 0.0), h_ext=2.0, v_ext=2.0):
    return {
        "right": np.array([1.0, 0.0, 0.0]),
        "up": np.array([0.0, 1.0, 0.0]),
        "dtc": np.array([0.0, 0.0, 1.0]),
        "bmid": np.asarray(bmid, dtype=np.float64),
        "h_ext": float(h_ext),
        "v_ext": float(v_ext),
        "W": int(W),
        "H": int(H),
    }


def _empty_view(H, W, cam):
    inf = np.full((H, W), np.inf, dtype=np.float64)
    return {
        "twin": np.zeros((H, W, 3), dtype=np.float64),
        "depth": inf.copy(),
        "sil": np.zeros((H, W), dtype=bool),
        "pos": np.full((H, W, 3), np.nan, dtype=np.float64),
        "normal_world": np.zeros((H, W, 3), dtype=np.float64),
        "surfid": np.full((H, W), -1, dtype=np.int32),
        "weight_border": np.zeros((H, W), dtype=np.float64),
        "reject": np.ones((H, W), dtype=bool),
        "flow": np.zeros((H, W, 2), dtype=np.float64),
        "cam": cam,
    }


def raster_plane(cam, colour_fn, plane_p=(0.0, 0.0, 0.0),
                 plane_n=(0.0, 0.0, 1.0), surfid_scale=100):
    """Ortho-rasterise z-aligned or general plane. colour_fn(P)->(3,)."""
    c = _as_cam(cam)
    H, W = c["H"], c["W"]
    ys, xs = np.mgrid[0:H, 0:W]
    origin = pixel_ray(xs.astype(np.float64), ys.astype(np.float64), c)
    direction = -c["dtc"]
    n = np.asarray(plane_n, dtype=np.float64)
    n = n / max(float(np.linalg.norm(n)), 1e-12)
    p0 = np.asarray(plane_p, dtype=np.float64)
    denom = float(n.dot(direction))
    if abs(denom) < 1e-12:
        _andon("camera parallel to fixture plane")
    t = ((p0 - origin) * n).sum(-1) / denom
    P = origin + t[..., None] * direction
    # Ortho: the camera lives at +inf along dtc. The plane through bmid is
    # only a parameterisation, so t may be negative (surface on the camera
    # side of bmid). Every finite intersection is a hit.
    hit = np.isfinite(t)
    view = _empty_view(H, W, c)
    view["sil"][hit] = True
    view["pos"][hit] = P[hit]
    view["normal_world"][hit] = n
    z = np.full((H, W), np.inf, dtype=np.float64)
    _, _, z_hit = project_point(P, c)
    z[hit] = z_hit[hit]
    view["depth"] = z
    twin = np.zeros((H, W, 3), dtype=np.float64)
    twin[hit] = colour_fn(P[hit])
    view["twin"] = twin
    # surfid from quantised world position -- stable across views
    sid = np.full((H, W), -1, dtype=np.int32)
    q = np.round(P * surfid_scale).astype(np.int64)
    # pack 3 signed 10-bit-ish coords; scale=100, |P|<5 is safe
    sid[hit] = (((q[hit, 0] + 500) * 1001 + (q[hit, 1] + 500)) * 1001
                + (q[hit, 2] + 500)).astype(np.int32)
    view["surfid"] = sid
    # filled-frame-or-not border weight via callieri if available, else 1
    # on sil. Self-test imports callieri_border for the real quantity.
    try:
        from callieri_border import border_weight, mixed_depth_reject
        view["weight_border"] = border_weight(view["depth"], view["sil"])
        view["reject"] = mixed_depth_reject(view["depth"], silhouette=view["sil"])
    except Exception:
        view["weight_border"] = view["sil"].astype(np.float64)
        view["reject"] = ~view["sil"]
        view["reject"][-1, :] = True
        view["reject"][:, -1] = True
    return view


def _plane_colour(P):
    return np.stack([(P[..., 0] + 1.0) * 0.5,
                     (P[..., 1] + 1.0) * 0.5,
                     np.full(P.shape[:-1], 0.25)], axis=-1)


def fixture_shift_pair(n=32):
    """Two +Z cameras, B shifted +0.25 in x. Linear colour plane z=0."""
    cam_a = _cam_plus_z(n, n, bmid=(0.0, 0.0, 0.0))
    cam_b = _cam_plus_z(n, n, bmid=(0.25, 0.0, 0.0))
    a = raster_plane(cam_a, _plane_colour)
    b = raster_plane(cam_b, _plane_colour)
    return [a, b]


def fixture_disagree_pair(n=32):
    """Same geometry as shift_pair; plates are solid red vs solid green."""
    views = fixture_shift_pair(n)
    for v, rgb in zip(views, ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0))):
        c = np.zeros_like(v["twin"])
        c[v["sil"]] = rgb
        v["twin"] = c
    return views


def fixture_occluder(n=32):
    """Back plane z=0 plus a front slab z=0.5 covering x < 0.

    View A (+Z) sees the slab on the left and the back plane on the right.
    A point on the back plane at x=-0.4 is hidden from A (sampled depth is
    the slab) and is the occlusion-yes case.
    """
    cam = _cam_plus_z(n, n)

    def back_col(P):
        return np.stack([np.full(P.shape[:-1], 0.1),
                         (P[..., 1] + 1.0) * 0.5,
                         (P[..., 0] + 1.0) * 0.5], axis=-1)

    def front_col(P):
        return np.stack([np.full(P.shape[:-1], 0.9),
                         (P[..., 1] + 1.0) * 0.5,
                         np.full(P.shape[:-1], 0.1)], axis=-1)

    back = raster_plane(cam, back_col, plane_p=(0, 0, 0), plane_n=(0, 0, 1))
    front = raster_plane(cam, front_col, plane_p=(0, 0, 0.5), plane_n=(0, 0, 1))
    # merge: front wins where it exists AND x < 0
    # slab occupies x<0 AND is closer to the camera than the back plane
    use_f = (front["sil"] & (front["pos"][..., 0] < 0.0)
             & (front["depth"] < back["depth"]))
    view = _empty_view(n, n, cam)
    # start with back
    for k in ("twin", "depth", "sil", "pos", "normal_world", "surfid",
              "weight_border", "reject"):
        view[k] = back[k].copy()
    view["twin"][use_f] = front["twin"][use_f]
    view["depth"][use_f] = front["depth"][use_f]
    view["sil"][use_f] = True
    view["pos"][use_f] = front["pos"][use_f]
    view["normal_world"][use_f] = front["normal_world"][use_f]
    view["surfid"][use_f] = front["surfid"][use_f]
    try:
        from callieri_border import border_weight, mixed_depth_reject
        view["weight_border"] = border_weight(view["depth"], view["sil"])
        view["reject"] = mixed_depth_reject(view["depth"], silhouette=view["sil"])
    except Exception:
        pass
    return view


def fixture_warp_pair(n=32, shift=6, r0=8, r1=24, c0=8, c1=24):
    """Two identical +Z cameras; B's twin is shifted +shift px in x inside a tile."""
    cam = _cam_plus_z(n, n)
    a = raster_plane(cam, _plane_colour)
    b = raster_plane(cam, _plane_colour)
    # shift B's twin in the tile (roll +x, then restore outside)
    src = a["twin"].copy()
    rolled = np.roll(src, shift, axis=1)
    b["twin"] = src.copy()
    b["twin"][r0:r1, c0:c1] = rolled[r0:r1, c0:c1]
    flow = np.zeros((n, n, 2), dtype=np.float64)
    # to undo a +shift paint, sample at px+shift
    flow[r0:r1, c0:c1, 0] = float(shift)
    b["flow"] = flow
    return [a, b], (r0, r1, c0, c1, shift)


# ---------------------------------------------------------------------------
# self-test legs
# ---------------------------------------------------------------------------

def _selftest_reprojection():
    views = fixture_shift_pair(32)
    rec, valid = reproject_plate(views[0], views[1])
    # the calibration pixel must be valid and exact
    if not valid[CALIBRATION_ROW, CALIBRATION_COL]:
        _andon("calibration pixel (%d,%d) is not valid under reprojection"
               % (CALIBRATION_ROW, CALIBRATION_COL))
    got = float(rec[CALIBRATION_ROW, CALIBRATION_COL, 0])
    if not np.isclose(got, CALIBRATION_RED, rtol=0.0, atol=1e-6):
        _andon("CALIBRATION: reprojected red at (%d,%d) is %r, not %r"
               % (CALIBRATION_ROW, CALIBRATION_COL, got, CALIBRATION_RED))
    # bilinear is exact on the linear field wherever the 2x2 is valid
    truth = views[1]["twin"]
    sil = views[1]["sil"] & valid
    err = np.max(np.abs(rec[sil] - truth[sil])) if sil.any() else 0.0
    if err > 1e-5:
        _andon("reprojection max abs error %r exceeds 1e-5 on the linear field"
               % float(err))


def _selftest_occlusion():
    view = fixture_occluder(32)
    # a back-plane point hidden by the slab: x=-0.4, y=0, z=0
    hidden = np.array([-0.4, 0.0, 0.0])
    samp = sample_view(view, hidden)
    if samp["valid"]:
        _andon("hidden back-plane point (x=-0.4,z=0) was marked visible; "
               "the occluder depth test did not fire")
    # a back-plane point in the open: x=+0.4, y=0, z=0
    open_p = np.array([0.4, 0.0, 0.0])
    samp_o = sample_view(view, open_p)
    if not samp_o["valid"]:
        _andon("exposed back-plane point (x=+0.4,z=0) was marked invisible")
    # the slab itself is visible
    front = np.array([-0.4, 0.0, 0.5])
    samp_f = sample_view(view, front)
    if not samp_f["valid"]:
        _andon("front-slab point was marked invisible")


def _selftest_consistency():
    views = fixture_disagree_pair(32)
    r0 = s3_composite(views, 0, primary_mode="target")
    r1 = s3_composite(views, 1, primary_mode="target")
    sid0 = np.asarray(views[0]["surfid"])
    sid1 = np.asarray(views[1]["surfid"])
    raw_shared = set(sid0[sid0 >= 0].tolist()) & set(sid1[sid1 >= 0].tolist())
    assigned = set(r0["assignment"]["surfid"].tolist())
    # last-row/col reject pixels carry a surfid but cannot be sampled;
    # the theorem is about compositable shared surfids.
    shared = sorted(raw_shared & assigned)
    if len(shared) < 16:
        _andon("consistency fixture has only %d compositable shared surfids "
               "(%d raw shared, %d assigned)"
               % (len(shared), len(raw_shared), len(assigned)))
    all_s = r0["assignment"]["surfid"]
    col = r0["assignment"]["colour"]
    # VI colours at shared surfids -- compare the canonical table, and
    # the two stills at one pixel of each surfid
    for s in shared:
        loc = np.searchsorted(all_s, s)
        if loc >= all_s.size or all_s[loc] != s:
            _andon("shared surfid %d missing from assignment" % int(s))
        i = loc
        # both stills: pick one pixel of s in each target
        p0 = np.argwhere((sid0 == s) & r0["coverage"])
        p1 = np.argwhere((sid1 == s) & r1["coverage"])
        if p0.size == 0 or p1.size == 0:
            continue
        y0, x0 = p0[0]
        y1, x1 = p1[0]
        c0 = r0["independent"][y0, x0]
        c1 = r1["independent"][y1, x1]
        if not np.allclose(c0, c1, rtol=0.0, atol=1e-6):
            _andon("VI stills disagree at surfid %d: %s vs %s"
                   % (int(s), c0, c1))
        if not np.allclose(c0, col[i], rtol=0.0, atol=1e-6):
            _andon("VI still does not match canonical colour at surfid %d"
                   % int(s))
    # VD stills MUST differ (target-first + disagreeing plates)
    sil = views[0]["sil"] & views[1]["sil"]
    vd_delta = np.max(np.abs(r0["dependent"][sil] - r1["dependent"][sil]))
    if vd_delta < 0.5:
        _andon("VD stills differ by only %r on a red-vs-green fixture; "
               "leg 3 cannot fail if they match (per-target argmax bug "
               "class, or primary_mode collapsed both to one plate)"
               % float(vd_delta))
    # a per-target argmax VI would pick view 0 for target 0 (red) and
    # view 1 for target 1 (green). We already asserted they match; if
    # they matched AND were different from each other that would be
    # impossible -- the check above is the real one.


def _selftest_warp():
    views, (r0, r1, c0, c1, shift) = fixture_warp_pair(32, shift=6)
    # without flow
    raw = [dict(views[0]), dict(views[1])]
    raw[1] = dict(views[1])
    raw[1]["flow"] = np.zeros_like(views[1]["flow"])
    r_off = s3_composite(raw, 0, primary_mode="target")
    r_on = s3_composite(views, 0, primary_mode="target")
    tile = np.zeros((32, 32), dtype=bool)
    # pixels whose SAMPLE (px+shift) still lands inside the painted-shift
    # tile, eroded 1 px so bilinear does not see the seam
    tile[r0 + 1:r1 - 1, c0 + 1:c1 - 1 - shift] = True
    ring = np.ones((32, 32), dtype=bool)
    ring[r0:r1, c0:c1] = False
    outside = views[0]["sil"] & ring
    d_in = float(r_off["disagreement"][tile].mean()) if tile.any() else 0.0
    d_out = float(r_off["disagreement"][outside].mean()) if outside.any() else 0.0
    if d_in <= d_out + 1e-6:
        _andon("warp-off disagreement inside the tile (%r) did not exceed "
               "outside (%r)" % (d_in, d_out))
    if d_out > 1e-4:
        _andon("warp-off disagreement outside the tile is %r; must stay quiet"
               % d_out)
    # handing the true flow back must make view 1 sample the unwarped field
    P = views[0]["pos"]
    samp = sample_view(views[1], P)
    truth = views[0]["twin"]
    rec = samp["colour"]
    ok = tile & samp["valid"]
    err = float(np.max(np.abs(rec[ok] - truth[ok]))) if ok.any() else 1.0
    if err > 1e-4:
        _andon("warp-on sample of the slipped plate max abs error %r "
               "exceeds 1e-4 (flow did not undo the shift)" % err)
    d_on = float(r_on["disagreement"][tile].mean()) if tile.any() else 0.0
    if d_on >= d_in:
        _andon("warp-on disagreement %r did not drop below warp-off %r"
               % (d_on, d_in))


def _selftest_andon_can_fail():
    views = fixture_shift_pair(8)
    try:
        s3_composite(views, 9)
    except Andon:
        pass
    else:
        _andon("out-of-range target did not fire")
    try:
        visibility_tau(views[0]["depth"], views[0]["sil"], relative_jump=0.0)
    except Andon:
        pass
    else:
        _andon("relative_jump=0 did not fire")


def selftest():
    _selftest_reprojection()
    _selftest_occlusion()
    _selftest_consistency()
    _selftest_warp()
    _selftest_andon_can_fail()
    return 0


def _write_debug(out_dir):
    import os
    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)

    def dump(name, arr):
        if arr.ndim == 2:
            a = arr.astype(np.float64)
            if a.dtype == bool or a.max() <= 1.0:
                pix = np.clip(a * 255.0, 0, 255).astype(np.uint8)
            else:
                m = a.max() if a.max() > 0 else 1.0
                pix = np.clip(a / m * 255.0, 0, 255).astype(np.uint8)
            Image.fromarray(pix).save(os.path.join(out_dir, name + ".png"))
        else:
            pix = np.clip(arr * 255.0, 0, 255).astype(np.uint8)
            Image.fromarray(pix).save(os.path.join(out_dir, name + ".png"))

    views = fixture_disagree_pair(32)
    r = s3_composite(views, 0)
    dump("vi_t0", r["independent"])
    dump("vd_t0", r["dependent"])
    r1 = s3_composite(views, 1)
    dump("vi_t1", r1["independent"])
    dump("vd_t1", r1["dependent"])
    dump("disagreement_t0", r["disagreement"])
    wv, box = fixture_warp_pair(32)
    roff = dict(wv[1])
    roff["flow"] = np.zeros_like(wv[1]["flow"])
    d_off = s3_composite([wv[0], roff], 0)
    dump("warp_disagreement_off", d_off["disagreement"])
    d_on = s3_composite(wv, 0)
    dump("warp_disagreement_on", d_on["disagreement"])


def main(argv=None):
    p = argparse.ArgumentParser(
        description="S3 existence-proof compositor (self-test; functions are the API)")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--out", default=None)
    args = p.parse_args(argv)
    if not args.selftest:
        p.error("nothing to do: this module is imported. Pass --selftest.")
    try:
        selftest()
    except Andon as e:
        sys.stderr.write(str(e) + "\n")
        return 2
    if args.out:
        _write_debug(args.out)
    sys.stdout.write(
        "s3_composite selftest OK  calibration red[%d,%d] == %s\n"
        % (CALIBRATION_ROW, CALIBRATION_COL, CALIBRATION_RED))
    return 0


if __name__ == "__main__":
    sys.exit(main())
