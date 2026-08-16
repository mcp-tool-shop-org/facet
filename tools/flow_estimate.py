# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Per-view flow field for the s3_composite hook.

WHY THIS EXISTS. Consult #5: warp is image-space correspondence of one twin
to the mesh; the flow hook is how a measured warp enters the compositor.
This module is the correction tool. The E45 per-tile instrument is the
measurement of record for "is there a warp." Do not tune this file against
that seat's numbers.

SIGN. flow(px, py) answers: the paint that belongs at this geometric
position actually sits at (px + flow_x, py + flow_y). If the twin is the
mesh-side signal shifted +3 px in x (np.roll(..., +3, axis=1)), then
twin[x] = source[x-3] and flow_x = +3. A wrong sign makes the composite
worse while every magnitude statistic still looks fine. The calibration
leg pins the sign.

WHICH PAIR. The core is modality-agnostic: estimate_flow(source, dest).
  * gray  -- both as luminance. Used by the constructions (a linear ramp
    has an exact LK answer).
  * edge  -- Sobel magnitude of both. This is the real-data pair:
    mesh-side can be a canny control OR a depth_edge_mask; dest is the
    twin, reduced to its edges.

  Twin-vs-control (canny) measures generator-drift from the conditioning
  image. That IS the suspected mechanism, and it will fire where the twin
  painted structure the control never had -- those windows fail the
  both-signals floor and return confidence 0 (identity). It also
  confounds licensed ControlNet slack (the model is not pixel-exact even
  when "correct") with geometric warp. Depth-edge vs twin-edge is the
  cleaner mesh-side truth: it is the silhouette of the reconstructed
  surface, independent of the generator. Prefer depth-edge when the AOV
  bundle exists; use control when it does not. The estimator does not
  pick; the caller does.

DENSE VS TILE. Dense LK, sparse confidence. At this signal density
(canny is a 1-px set; paint edges are thin) a per-tile mean then
interpolated field would invent flow in empty windows and the
confidence map would mean "this tile had an edge somewhere." We evaluate
every pixel and refuse to interpolate into no-signal regions. Identity
(flow 0, confidence 0) is the compositor default there. The E45 tile
offsets remain the measurement of record; this field is the correction.

APERTURE. Along a straight edge only the normal component is observable.
The structure tensor's eigenvalues decide:
  l1, l2 = eigs, l1 >= l2
  l1 below the signal floor, or either image lacking structure in the
    window -> flow 0, confidence 0, confidence_xy 0
  l2 / l1 >= corner_rel -> full 2-D LK, both components live
  otherwise -> rank-1: flow is projected onto the observable eigenvector
    (normal to the edge); the tangential component is not written; its
    confidence_xy is ~0. A confident zero and a confident hallucination
    of the tangent are both refused.

WINDOW. Default 7, odd, exposed. Basis: the sword blade is ~15 px wide
in these frames; the window must be smaller than the thinnest structure
still resolved, so half-width. A window of 15 would average across the
blade and the gap.

YES/NO INTERVALS.

  flow_x, flow_y     0 = identity (or unmeasured, see confidence).
                     +3 on the calibration ramp = dest is source rolled
                     +3 in x. Sign is the claim.
  confidence         0 = nothing measured; compositor must leave identity.
                     1 = both components well observed (a corner).
  confidence_xy      0 on an axis = that component is unobservable.
                     1 on an axis = that component is well observed.

CALIBRATION CLAIM (run --selftest; T79 pins the same number).
  Canvas 64x64. source[y, x] = x / 64. dest = np.roll(source, +3, axis=1).
  At pixel (32, 32) -- six pixels from either wrap -- flow_x == 3.0.
  Construction: I0 - I1 = 3/64, dI/dx = 1/64, LK on a linear field is
  exact, u = 3. A sign error yields -3. A 0-flow stand-in yields 0.

  python tools/flow_estimate.py --selftest [--out DIR]
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np
from scipy.ndimage import sobel, uniform_filter

TOOL_VERSION = "1.0.0"

# Half of the 15 px blade. Must be odd.
DEFAULT_WINDOW = 7
# Weak-axis / strong-axis eigenvalue ratio below which we treat the
# window as rank-1 (aperture). Not a pixel constant.
DEFAULT_CORNER_REL = 0.15
# Gradient percentile on the figure that a window must beat, on BOTH
# images, to count as signal. Not a pixel constant.
DEFAULT_GRAD_PERCENTILE = 75.0

CALIBRATION_ROW = 32
CALIBRATION_COL = 32
CALIBRATION_FLOW_X = 3.0


class Andon(ValueError):
    """A fired gate. Never an `assert`."""


def _andon(msg):
    raise Andon("ANDON: " + msg)


def to_gray(img):
    a = np.asarray(img, dtype=np.float64)
    if a.ndim == 2:
        return a
    if a.ndim == 3 and a.shape[-1] >= 3:
        return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    if a.ndim == 3 and a.shape[-1] == 1:
        return a[..., 0]
    _andon("image must be (H,W) or (H,W,C), got %s" % (a.shape,))


def to_edge(img):
    """Sobel magnitude. The edge pair (control or depth-edge vs twin)."""
    g = to_gray(img)
    gx = sobel(g, axis=1)
    gy = sobel(g, axis=0)
    return np.hypot(gx, gy)


def _odd_window(window):
    if window is None:
        window = DEFAULT_WINDOW
    w = int(window)
    if w < 3 or w % 2 == 0:
        _andon("window must be an odd integer >= 3 (half of the ~15 px "
               "blade), got %r" % (window,))
    return w


def estimate_flow(source, dest, sil=None, window=DEFAULT_WINDOW,
                  corner_rel=DEFAULT_CORNER_REL,
                  grad_percentile=DEFAULT_GRAD_PERCENTILE,
                  pair="gray"):
    """LK flow taking dest back onto source.

    source: mesh-side signal (control / depth-edge / luminance).
    dest:   twin (or a shifted copy of source, in the fixtures).
    pair:   'gray' (luminance) or 'edge' (Sobel magnitude of both).

    Returns dict:
      flow          (H, W, 2) float32
      confidence    (H, W)    float32 in [0, 1]
      confidence_xy (H, W, 2) float32 in [0, 1]
    """
    if pair not in ("gray", "edge"):
        _andon("pair must be 'gray' or 'edge', got %r" % (pair,))
    if not np.isfinite(corner_rel) or not (0.0 < corner_rel < 1.0):
        _andon("corner_rel must be in (0, 1), got %r" % (corner_rel,))
    if not np.isfinite(grad_percentile) or not (0.0 < grad_percentile < 100.0):
        _andon("grad_percentile must be in (0, 100), got %r" % (grad_percentile,))
    w = _odd_window(window)
    if pair == "edge":
        i0 = to_edge(source)
        i1 = to_edge(dest)
    else:
        i0 = to_gray(source)
        i1 = to_gray(dest)
    if i0.shape != i1.shape:
        _andon("source shape %s != dest shape %s" % (i0.shape, i1.shape))
    h, ww = i0.shape
    if sil is None:
        sil = np.ones((h, ww), dtype=bool)
    else:
        sil = np.asarray(sil, dtype=bool)
        if sil.shape != (h, ww):
            _andon("sil shape %s != image %s" % (sil.shape, i0.shape))
    if not sil.any():
        _andon("silhouette is empty")

    # dest gradients: paint lives here. np.gradient is exact on a linear
    # field, which is what the calibration construction is.
    gy, gx = np.gradient(i1)
    it = i0 - i1
    mask = sil.astype(np.float64)
    m = uniform_filter(mask, w)
    # normalised window sums; a pixel whose window is empty of figure is
    # no-signal regardless of the images
    denom = np.maximum(m, 1.0 / (w * w))

    def wsum(arr):
        return uniform_filter(arr * mask, w) / denom

    ixx = wsum(gx * gx)
    ixy = wsum(gx * gy)
    iyy = wsum(gy * gy)
    itx = wsum(gx * it)
    ity = wsum(gy * it)
    src_e = wsum(np.hypot(*np.gradient(i0)))
    dst_e = wsum(np.hypot(gy, gx))

    src_g = np.hypot(*np.gradient(i0))
    dst_g = np.hypot(gy, gx)
    floor_s = float(np.percentile(src_g[sil], grad_percentile))
    floor_d = float(np.percentile(dst_g[sil], grad_percentile))
    peak_s = float(np.max(src_g[sil]))
    peak_d = float(np.max(dst_g[sil]))
    # a constant image has peak 0: no-signal, even though percentile is 0
    # and `>= 0` would pass every pixel. A linear ramp has peak == percentile
    # and must pass, so the comparison is >= on a strictly positive floor.
    if peak_s < 1e-12 or peak_d < 1e-12:
        both = np.zeros((h, ww), dtype=bool)
    else:
        both = ((src_e >= floor_s) & (dst_e >= floor_d)
                & (m > 0.5) & sil)

    tr = ixx + iyy
    det = ixx * iyy - ixy * ixy
    disc = np.sqrt(np.maximum(tr * tr - 4.0 * det, 0.0))
    l1 = 0.5 * (tr + disc)
    l2 = 0.5 * (tr - disc)

    # reference scales for per-axis confidence: median of the observed
    # diagonal on both-signal pixels, so they are relative to this frame
    if both.any():
        ref_x = float(np.median(ixx[both]))
        ref_y = float(np.median(iyy[both]))
    else:
        ref_x = ref_y = 1.0
    ref_x = max(ref_x, 1e-12)
    ref_y = max(ref_y, 1e-12)
    conf_x = np.clip(ixx / (ixx + ref_x), 0.0, 1.0)
    conf_y = np.clip(iyy / (iyy + ref_y), 0.0, 1.0)
    conf_x = np.where(both, conf_x, 0.0)
    conf_y = np.where(both, conf_y, 0.0)

    # full 2-D LK where the tensor is well-conditioned
    det_ok = det > 1e-18
    ux = np.zeros((h, ww), dtype=np.float64)
    uy = np.zeros((h, ww), dtype=np.float64)
    ux_2d = np.divide(iyy * itx - ixy * ity, det, out=np.zeros_like(det),
                      where=det_ok)
    uy_2d = np.divide(ixx * ity - ixy * itx, det, out=np.zeros_like(det),
                      where=det_ok)

    # rank-1: project the residual onto the leading eigenvector
    # e1 ~ (ixy, l1 - ixx) or (l1 - iyy, ixy), pick the stable form
    e1x = np.where(np.abs(ixy) > np.abs(l1 - iyy), ixy, l1 - iyy)
    e1y = np.where(np.abs(ixy) > np.abs(l1 - iyy), l1 - ixx, ixy)
    e1n = np.hypot(e1x, e1y)
    e1x = np.divide(e1x, e1n, out=np.zeros_like(e1x), where=e1n > 1e-12)
    e1y = np.divide(e1y, e1n, out=np.zeros_like(e1y), where=e1n > 1e-12)
    # u = ((b · e1) / l1) e1, b = (itx, ity)
    amp = np.divide(itx * e1x + ity * e1y, l1, out=np.zeros_like(l1),
                    where=l1 > 1e-18)
    ux_1d = amp * e1x
    uy_1d = amp * e1y

    corner = both & (l1 > 0.0) & ((l2 / np.maximum(l1, 1e-18)) >= corner_rel)
    edge = both & ~corner
    ux = np.where(corner, ux_2d, 0.0)
    uy = np.where(corner, uy_2d, 0.0)
    ux = np.where(edge, ux_1d, ux)
    uy = np.where(edge, uy_1d, uy)

    # aperture: the tangent axis is unobservable -- force its confidence
    # to 0 (not a confident zero of the flow, a refused component)
    nx2 = e1x * e1x
    ny2 = e1y * e1y
    # observability of x/y from the tensor diagonals already in conf_x/y;
    # on rank-1, kill the weaker axis
    weaker_x = edge & (nx2 < ny2)  # normal is mostly y -> x unobservable
    weaker_y = edge & (ny2 <= nx2)
    conf_x = np.where(weaker_x, 0.0, conf_x)
    conf_y = np.where(weaker_y, 0.0, conf_y)
    # and do not report a tangential flow component even if 1-D projection
    # leaked a bit of the other axis through a noisy e1
    ux = np.where(weaker_x, 0.0, ux)
    uy = np.where(weaker_y, 0.0, uy)

    confidence = np.maximum(conf_x, conf_y).astype(np.float32)
    flow = np.stack([ux, uy], axis=-1).astype(np.float32)
    confidence_xy = np.stack([conf_x, conf_y], axis=-1).astype(np.float32)
    return {
        "flow": flow,
        "confidence": confidence,
        "confidence_xy": confidence_xy,
    }


# ---------------------------------------------------------------------------
# constructions
# ---------------------------------------------------------------------------

def fixture_ramp_shift(n=64, shift=3):
    """source[y,x] = x/n; dest = roll(source, +shift, axis=1)."""
    x = np.arange(n, dtype=np.float64)
    source = np.broadcast_to(x / float(n), (n, n)).copy()
    dest = np.roll(source, int(shift), axis=1)
    sil = np.ones((n, n), dtype=bool)
    # wrap columns are not the linear field
    sil[:, :int(shift)] = False
    sil[:, -int(shift):] = False
    return source, dest, sil


def fixture_identity_ramp(n=64):
    x = np.arange(n, dtype=np.float64)
    src = np.broadcast_to(x / float(n), (n, n)).copy()
    return src, src.copy(), np.ones((n, n), dtype=bool)


def fixture_flat(n=32):
    src = np.full((n, n), 0.5, dtype=np.float64)
    return src, src.copy(), np.ones((n, n), dtype=bool)


def fixture_vertical_edge_tangential(n=64, shift=4, c0=30, c1=34):
    """Vertical bar, dest rolled in y (tangent). Unobservable component is y."""
    src = np.zeros((n, n), dtype=np.float64)
    src[:, c0:c1] = 1.0
    dest = np.roll(src, int(shift), axis=0)
    sil = np.ones((n, n), dtype=bool)
    return src, dest, sil


def fixture_smooth_warp(n=64, amp=4.0):
    """Linear ramp in x, dest sampled at x - u(y), u = amp * sin(2 pi y / n).

    On a linear field LK is exact even when u varies with y, so the
    0.5 px ceiling is a real check on the windowed solver, not on
    first-order brightness-constancy bias.
    """
    y, x = np.mgrid[0:n, 0:n].astype(np.float64)
    source = np.broadcast_to(x / float(n), (n, n)).copy()
    ux = amp * np.sin(2.0 * np.pi * y / float(n))
    from scipy.ndimage import map_coordinates
    dest = map_coordinates(source, [y, x - ux], order=1, mode="nearest")
    sil = np.ones((n, n), dtype=bool)
    sil[:4, :] = sil[-4:, :] = sil[:, :4] = sil[:, -4:] = False
    return source, dest, sil, ux


# ---------------------------------------------------------------------------
# self-test
# ---------------------------------------------------------------------------

def _selftest_sign():
    src, dst, sil = fixture_ramp_shift(64, shift=3)
    out = estimate_flow(src, dst, sil=sil, window=7)
    got = float(out["flow"][CALIBRATION_ROW, CALIBRATION_COL, 0])
    if not np.isclose(got, CALIBRATION_FLOW_X, rtol=0.0, atol=1e-6):
        _andon("CALIBRATION: flow_x at (%d,%d) is %r, not %r "
               "(a sign error yields -3; a 0-flow stand-in yields 0)"
               % (CALIBRATION_ROW, CALIBRATION_COL, got, CALIBRATION_FLOW_X))
    if float(out["confidence_xy"][CALIBRATION_ROW, CALIBRATION_COL, 0]) < 0.4:
        _andon("calibration pixel has low conf_x; the ramp is fully observed")


def _selftest_identity():
    src, dst, sil = fixture_identity_ramp(64)
    out = estimate_flow(src, dst, sil=sil, window=7)
    fx = out["flow"][8:-8, 8:-8, 0]
    fy = out["flow"][8:-8, 8:-8, 1]
    if float(np.max(np.abs(fx))) > 0.05 or float(np.max(np.abs(fy))) > 0.05:
        _andon("identity ramp max |flow| is %r, %r; must stay ~0"
               % (float(np.max(np.abs(fx))), float(np.max(np.abs(fy)))))
    if float(out["confidence_xy"][32, 32, 0]) < 0.4:
        _andon("identity ramp has low conf_x; structure is present")


def _selftest_nosignal():
    src, dst, sil = fixture_flat(32)
    out = estimate_flow(src, dst, sil=sil, window=7)
    if float(np.max(np.abs(out["flow"]))) > 1e-6:
        _andon("flat pair produced flow %r; must be 0" % float(np.max(np.abs(out["flow"]))))
    if float(np.max(out["confidence"])) > 1e-6:
        _andon("flat pair produced confidence %r; must be 0"
               % float(np.max(out["confidence"])))


def _selftest_aperture():
    src, dst, sil = fixture_vertical_edge_tangential(64, shift=4)
    out = estimate_flow(src, dst, sil=sil, window=7)
    # the vertical faces of the bar: columns c0-1, c0, c1-1, c1
    edge = np.zeros((64, 64), dtype=bool)
    edge[:, 29:35] = True
    edge[4:-4, :] &= True
    cy = out["confidence_xy"][4:-4, 29:35, 1]
    # unobservable component must not be confidently answered
    if float(np.median(cy)) > 0.2:
        _andon("aperture: median conf_y on a vertical edge is %r; "
               "a tangential shift must not produce a confident y"
               % float(np.median(cy)))
    # and must not hallucinate the 4 px shift as a confident flow_y
    fy = out["flow"][4:-4, 29:35, 1]
    confy = out["confidence_xy"][4:-4, 29:35, 1]
    confident = confy > 0.5
    if confident.any() and float(np.median(np.abs(fy[confident]))) > 1.0:
        _andon("aperture: confident |flow_y| is %r on a purely tangential "
               "shift; that is a hallucination"
               % float(np.median(np.abs(fy[confident]))))


def _selftest_smooth_warp():
    src, dst, sil, ux = fixture_smooth_warp(64, amp=4.0)
    out = estimate_flow(src, dst, sil=sil, window=7)
    # recover where the x-structure is observed
    ok = sil & (out["confidence_xy"][..., 0] > 0.4)
    if ok.sum() < 64:
        _andon("smooth-warp: only %d pixels cleared conf_x" % int(ok.sum()))
    err = np.abs(out["flow"][..., 0] - ux)
    med = float(np.median(err[ok]))
    if med > 0.5:
        _andon("smooth-warp: median |flow_x - u| is %r px, ceiling 0.5" % med)


def _selftest_andon_can_fail():
    src, dst, sil = fixture_flat(8)
    try:
        estimate_flow(src, dst, sil=np.zeros_like(sil))
    except Andon:
        pass
    else:
        _andon("empty silhouette did not fire")
    try:
        estimate_flow(src, dst, window=4)
    except Andon:
        pass
    else:
        _andon("even window did not fire")


def selftest():
    _selftest_sign()
    _selftest_identity()
    _selftest_nosignal()
    _selftest_aperture()
    _selftest_smooth_warp()
    _selftest_andon_can_fail()
    return 0


def _write_debug(out_dir):
    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)

    def dump(name, arr):
        a = np.asarray(arr, dtype=np.float64)
        if a.ndim == 3:
            # flow: map 0 to 128, +/-8 px to 0/255
            vis = np.zeros(a.shape[:2] + (3,), dtype=np.uint8)
            vis[..., 0] = np.clip(128.0 + a[..., 0] * (127.0 / 8.0), 0, 255)
            vis[..., 1] = np.clip(128.0 + a[..., 1] * (127.0 / 8.0), 0, 255)
            vis[..., 2] = 128
            Image.fromarray(vis).save(os.path.join(out_dir, name + ".png"))
            return
        pix = np.clip(a * 255.0, 0, 255).astype(np.uint8)
        Image.fromarray(pix).save(os.path.join(out_dir, name + ".png"))

    src, dst, sil = fixture_ramp_shift(64, 3)
    out = estimate_flow(src, dst, sil=sil)
    dump("ramp_flow", out["flow"])
    dump("ramp_conf", out["confidence"])
    src, dst, sil = fixture_vertical_edge_tangential(64)
    out = estimate_flow(src, dst, sil=sil)
    dump("aperture_conf_xy", out["confidence_xy"])


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Flow estimator for the s3_composite hook")
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
        "flow_estimate selftest OK  calibration flow_x[%d,%d] == %s\n"
        % (CALIBRATION_ROW, CALIBRATION_COL, CALIBRATION_FLOW_X))
    return 0


if __name__ == "__main__":
    sys.exit(main())
