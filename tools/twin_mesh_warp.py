# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Per-tile twin-to-mesh correspondence offsets (E45 task 2).

THE QUESTION. Global registration between a painted twin and the mesh silhouette
it was generated against is good (the prior reading was IoU 0.9203, centroid offset
2.88 x 2.60 px). That is a statement about the whole figure. This module asks a
different question per 64 px tile: WHERE, locally, does the twin's structure sit
relative to the mesh's? A 4-8 px local displacement puts a sample across a material
boundary while depth stays locally smooth - the blind spot callieri_border.py
declares in its own docstring.

    THE PRIOR NUMBERS ARE A HYPOTHESIS, NOT A BASELINE. The instrument that
    produced them is lost (it survives nowhere on disk or in git). Agreement with
    -8..+6 px in x, -8..+8 in y, std 3.71 / 4.09 is a continuity note. It is not a
    target and this module was written without reference to it.

THIS MODULE GRADES NOTHING AND HAS NO PASS CONDITION. It emits per-tile offsets,
peak confidences, a scope mask, pinning fractions and control readings. What they
mean is not its business.

TWO LEGS, ONE TWIN-SIDE FIELD.

  silhouette leg   mesh side = the figure's own outline (the 4-neighbour boundary
                   of `sil`). This is the leg the lost instrument measured.
  interior leg     mesh side = depth discontinuities that are NOT the outline -
                   `callieri_border.depth_edge_mask(depth)` minus the silhouette
                   boundary. Arm against torso, sword against body. This is the
                   leg that says whether silhouette agreement is enough, and
                   nothing in this repo had it.

  twin side        the SAME field for both legs: gradient magnitude of the twin in
                   CIE Lab, luminance and chroma together. Using one field is what
                   makes the two legs comparable - they differ only in what the
                   mesh offers as a template.

SIGN CONVENTION, and it is the Grok brief's `flow` convention exactly.

    flow(px, py) = (dx, dy)  means: the mesh structure at pixel (px, py) is found
    in the twin at (px + dx, py + dy).

A consumer sampling this view's twin for a mesh pixel therefore samples at
`(px + dx, py + dy)`. The convention is not asserted from the code's shape - it is
pinned by the injection leg, which shifts a real twin by a known amount and reads
the same amount back with the same sign.

METHOD, and why. Zero-mean normalised cross-correlation over an explicit integer
shift window (`cv2.matchTemplate`, `TM_CCOEFF_NORMED`), with a parabolic sub-pixel
fit on the 3x3 around the integer peak. Chosen over phase correlation because:
an explicit window makes PINNING VISIBLE (a tile whose peak sits on the boundary is
reporting a lower bound, not an offset), the peak value is a per-tile confidence
that phase correlation does not hand back as directly, and phase correlation's
cyclic assumption is wrong for sparse edge fields on a framed figure.

YES/NO INTERVALS (what the instrument reads when the answer is known).

  a field against ITSELF            offset exactly (0, 0), peak 1.0.
  a field against a copy shifted
    by an integer (dx, dy)          offset (dx, dy), peak 1.0, sub-pixel |err| < 0.5.
  a tile with no mesh-side
    structure                       out of scope. Not a reading of zero - a
                                    refusal. This is why the scope population is
                                    reported as its own number.
  a DELIBERATELY WRONG pairing
    (view i's mesh vs view j's
     twin)                          the control. If it reads like the right
                                    pairing, the measurement is not about
                                    correspondence. Reported, never gated.

SCOPE, and the local-normalisation law. A tile is in scope iff its mesh-side
template has non-zero variance AND its mesh-side edge count clears a floor that is
a fraction of THAT TILE'S OWN silhouette area (not a global pixel count) with a
small absolute floor beneath it so a 3-pixel tile cannot qualify on one edge pixel.
Both floor terms are parameters, both are reported per tile alongside the raw
counts, and the offsets are emitted for EVERY tile so the filter can be re-cut
without re-running.

Standards:
  ANDON_AUTHORITY   - Gate C (`gate_c`) `raise`s. Never a bare `assert`.
  PIN_PER_STEP      - every parameter rides in the output JSON.
  NAMED_COMPENSATORS- writes only new files under --out. Undo: delete --out.
  EXTERNAL_VERIFIER - grades nothing; emits arrays and controls.

  python tools/twin_mesh_warp.py --bundle DIR --out DIR [--tile 64] [--stride 32]
         [--radii 16,32,48] [--sigma 1.5] [--edge-frac 0.01] [--edge-abs 8]
  python tools/twin_mesh_warp.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

TOOL_VERSION = "1.0.0"

TILE = 64
STRIDE = 32
RADII = (16, 32, 48)
SIGMA = 1.5
EDGE_FRAC = 0.01          # of the tile's OWN silhouette area
EDGE_ABS = 8              # px, the floor under the floor
PEAK_FLOOR = -1.0         # no confidence filter is applied; the value is reported

# Gate C's tolerance, from the dispatch ("read them back within 0.5 px").
INJECT_TOL_PX = 0.5

# THE NULL LEG'S TOLERANCE IS THE SAME NUMBER, AND THAT IS DELIBERATE.
#
# The first draft of this file set it to 1e-9, reasoning that a field correlated
# against ITSELF has an exactly-zero answer. Run once on the synthetic fixture, the
# null leg FIRED at 0.018731 px on 35 of 35 tiles. That is not a bias in the
# correlator: the INTEGER peak is exactly (0, 0) on every tile and the peak value
# is 1.0. It is the parabolic sub-pixel fit, whose 3x3 neighbourhood is not
# symmetric on a real correlation surface, so it applies a small correction at the
# true zero. That is the estimator's own noise floor and it is a DIAGNOSTIC, not a
# halt (this repo's "a diagnostic and a gate are different objects").
#
# The repair keeps a gate that cannot be satisfied by a broken instrument, and does
# not invent a constant after seeing a result:
#   - the INTEGER offset must be exactly (0, 0) - bounded by construction, and it
#     is what "reads zero" actually means for a correlator;
#   - the peak must be ~1.0 on identical input;
#   - the SUB-PIXEL residual is gated at the dispatch's own 0.5 px, reused rather
#     than chosen, and its measured value is reported as the estimator's floor.
NULL_TOL_PX = INJECT_TOL_PX
NULL_PEAK_MIN = 0.999


class Andon(RuntimeError):
    """A fired gate. Never an `assert` - the interpreter may delete those."""


def _andon(msg):
    raise Andon("ANDON: " + msg)


# ---------------------------------------------------------------------------
# fields
# ---------------------------------------------------------------------------

def srgb_to_lab(rgb):
    """VERBATIM from tools/project_twins.py:380-390 (that file is not
    import-safe: argparse and a RaycastingScene run at module scope). Body
    unchanged. dE below would be CIE76; only the transform is used here."""
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16, 500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


def twin_edge_field(rgb01, sigma=SIGMA):
    """Gradient magnitude of the twin in Lab, luminance AND chroma.

    Chroma is not decoration here: a gold plate against a wine-red tunic can be
    nearly iso-luminant, and an L*-only field would miss exactly the material
    boundaries this measurement is about.
    """
    from scipy.ndimage import gaussian_filter, sobel
    rgb01 = np.asarray(rgb01, dtype=np.float64)
    if rgb01.ndim != 3 or rgb01.shape[-1] != 3:
        _andon("twin must be (H, W, 3), got %s" % (rgb01.shape,))
    lab = srgb_to_lab(rgb01)
    g2 = np.zeros(lab.shape[:2], dtype=np.float64)
    for k in range(3):
        gx = sobel(lab[..., k], axis=1, mode="nearest")
        gy = sobel(lab[..., k], axis=0, mode="nearest")
        g2 += gx * gx + gy * gy
    f = np.sqrt(g2)
    if sigma > 0:
        f = gaussian_filter(f, sigma)
    return f.astype(np.float32)


def silhouette_edge(sil):
    """The figure outline: 4-neighbour boundary of `sil`, marked on BOTH sides.

    Same construction as callieri_border._finite_nonfinite_edge, restated on the
    boolean mask so no private is imported and so it can be subtracted from the
    depth edge set to leave the interior.
    """
    s = np.asarray(sil, dtype=bool)
    if s.ndim != 2:
        _andon("sil must be 2-D, got %s" % (s.shape,))
    e = np.zeros(s.shape, dtype=bool)
    dx = s[:, :-1] ^ s[:, 1:]
    e[:, :-1] |= dx
    e[:, 1:] |= dx
    dy = s[:-1, :] ^ s[1:, :]
    e[:-1, :] |= dy
    e[1:, :] |= dy
    return e


def interior_depth_edge(depth_edge, sil):
    """Depth discontinuities that are NOT the figure's outline.

    `depth_edge` is callieri_border.depth_edge_mask(depth), whose set is the union
    of finite-finite jumps and the figure-vs-background cut. Removing the outline
    leaves internal occluding contours - the arm's edge against the torso, the
    blade against the body.
    """
    return np.asarray(depth_edge, dtype=bool) & ~silhouette_edge(sil)


def blur_binary(mask, sigma=SIGMA):
    """A binary edge set as a continuous field, so a correlation peak has a
    curvature to fit. sigma must stay well under the offsets being hunted."""
    from scipy.ndimage import gaussian_filter
    f = np.asarray(mask, dtype=np.float64)
    if sigma > 0:
        f = gaussian_filter(f, sigma)
    return f.astype(np.float32)


# ---------------------------------------------------------------------------
# correlation
# ---------------------------------------------------------------------------

def tile_origins(H, W, tile=TILE, stride=STRIDE):
    rows = list(range(0, H - tile + 1, stride))
    cols = list(range(0, W - tile + 1, stride))
    return rows, cols


def subpixel_peak(surf, i, j):
    """Parabolic fit in each axis on the 3x3 around the integer peak.

    Returns (dsub_y, dsub_x) in [-1, 1]. On the surface's boundary the fit is not
    defined and (0, 0) is returned - such tiles are flagged `pinned` and their
    integer peak is a bound, not an offset.
    """
    h, w = surf.shape
    if i <= 0 or j <= 0 or i >= h - 1 or j >= w - 1:
        return 0.0, 0.0
    out = []
    for a, b, c in ((surf[i - 1, j], surf[i, j], surf[i + 1, j]),
                    (surf[i, j - 1], surf[i, j], surf[i, j + 1])):
        den = (a - 2.0 * b + c)
        out.append(0.0 if abs(den) < 1e-12
                   else float(np.clip(0.5 * (a - c) / den, -1.0, 1.0)))
    return out[0], out[1]


def correlate_tiles(template_field, search_field, radius, tile=TILE,
                    stride=STRIDE, scope_count=None, scope_area=None,
                    edge_frac=EDGE_FRAC, edge_abs=EDGE_ABS):
    """Per-tile ZNCC offsets of `template_field` against `search_field`.

    Both fields are (H, W) float32 in the SAME frame. Both are zero-padded by
    `radius` so the tile grid does not change with the window - a pinning fraction
    measured at two radii must be measured over the same tiles.

    `scope_count` (per-pixel bool, e.g. the mesh-side edge set) and `scope_area`
    (per-pixel bool, e.g. the silhouette) define the scope floor:
        in_scope = template std > 0
                   AND count_in_tile >= max(edge_abs, edge_frac * area_in_tile)
    Every tile's offset is returned regardless; `in_scope` is a column.
    """
    import cv2
    t = np.asarray(template_field, dtype=np.float32)
    s = np.asarray(search_field, dtype=np.float32)
    if t.shape != s.shape:
        _andon("template %s and search %s are not the same frame"
               % (t.shape, s.shape))
    H, W = t.shape
    R = int(radius)
    sp = np.pad(s, R, mode="constant", constant_values=0.0)
    rows, cols = tile_origins(H, W, tile, stride)
    n = len(rows) * len(cols)
    out = {
        "row0": np.zeros(n, dtype=np.int32), "col0": np.zeros(n, dtype=np.int32),
        "dx": np.zeros(n, dtype=np.float64), "dy": np.zeros(n, dtype=np.float64),
        "dx_int": np.zeros(n, dtype=np.int32), "dy_int": np.zeros(n, dtype=np.int32),
        "peak": np.full(n, np.nan, dtype=np.float64),
        "pinned": np.zeros(n, dtype=bool),
        "in_scope": np.zeros(n, dtype=bool),
        "tmpl_std": np.zeros(n, dtype=np.float64),
        "count_px": np.zeros(n, dtype=np.int32),
        "area_px": np.zeros(n, dtype=np.int32),
        "floor_px": np.zeros(n, dtype=np.float64),
    }
    k = 0
    for r0 in rows:
        for c0 in cols:
            tpl = t[r0:r0 + tile, c0:c0 + tile]
            reg = sp[r0:r0 + tile + 2 * R, c0:c0 + tile + 2 * R]
            out["row0"][k] = r0
            out["col0"][k] = c0
            std = float(tpl.std())
            out["tmpl_std"][k] = std
            cnt = int(scope_count[r0:r0 + tile, c0:c0 + tile].sum()) \
                if scope_count is not None else tile * tile
            area = int(scope_area[r0:r0 + tile, c0:c0 + tile].sum()) \
                if scope_area is not None else tile * tile
            floor = max(float(edge_abs), edge_frac * area)
            out["count_px"][k] = cnt
            out["area_px"][k] = area
            out["floor_px"][k] = floor
            out["in_scope"][k] = (std > 0.0) and (cnt >= floor)
            if std <= 0.0:
                k += 1
                continue
            surf = cv2.matchTemplate(reg, tpl, cv2.TM_CCOEFF_NORMED)
            surf = np.where(np.isfinite(surf), surf, -1.0)
            i, j = np.unravel_index(int(np.argmax(surf)), surf.shape)
            out["peak"][k] = float(surf[i, j])
            out["dy_int"][k] = i - R
            out["dx_int"][k] = j - R
            out["pinned"][k] = (i == 0 or j == 0 or i == surf.shape[0] - 1
                                or j == surf.shape[1] - 1)
            sy, sx = subpixel_peak(surf, i, j)
            out["dy"][k] = (i - R) + sy
            out["dx"][k] = (j - R) + sx
            k += 1
    out["radius"] = R
    out["tile"] = tile
    out["stride"] = stride
    out["n_tiles"] = n
    out["grid"] = [len(rows), len(cols)]
    return out


def neighbour_incoherence(res, mask=None):
    """Mean |offset - mean(4-neighbour offsets)| over tiles whose neighbours are
    also included. Reported beside the SAME statistic on a shuffled assignment;
    a field with spatial structure separates the two, noise does not."""
    gr, gc = res["grid"]
    sel = np.ones(res["n_tiles"], dtype=bool) if mask is None else np.asarray(mask)
    dx = res["dx"].reshape(gr, gc)
    dy = res["dy"].reshape(gr, gc)
    ok = sel.reshape(gr, gc)
    vals = []
    for i in range(gr):
        for j in range(gc):
            if not ok[i, j]:
                continue
            nb = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
            nb = [(a, b) for a, b in nb if 0 <= a < gr and 0 <= b < gc and ok[a, b]]
            if not nb:
                continue
            mx = np.mean([dx[a, b] for a, b in nb])
            my = np.mean([dy[a, b] for a, b in nb])
            vals.append(float(np.hypot(dx[i, j] - mx, dy[i, j] - my)))
    return (float(np.mean(vals)) if vals else float("nan")), len(vals)


def shuffled_incoherence(res, mask=None, seed=0, trials=8):
    """The same statistic with the in-scope tiles' offsets randomly reassigned."""
    rng = np.random.default_rng(seed)
    sel = np.ones(res["n_tiles"], dtype=bool) if mask is None else np.asarray(mask)
    idx = np.nonzero(sel)[0]
    got = []
    for _ in range(trials):
        perm = rng.permutation(idx)
        sh = {k: (v.copy() if isinstance(v, np.ndarray) else v)
              for k, v in res.items()}
        sh["dx"][idx] = res["dx"][perm]
        sh["dy"][idx] = res["dy"][perm]
        got.append(neighbour_incoherence(sh, sel)[0])
    return float(np.mean(got)), float(np.std(got))


# ---------------------------------------------------------------------------
# Gate C - instrument validation on constructed truth
# ---------------------------------------------------------------------------

def shift_image(img, dx, dy):
    """Integer shift with zero fill. `out[y, x] = img[y - dy, x - dx]`, so the
    CONTENT moves by (+dx, +dy) - which is the direction `flow` reports."""
    a = np.asarray(img)
    out = np.zeros_like(a)
    H, W = a.shape[:2]
    ys0, ys1 = max(0, dy), min(H, H + dy)
    xs0, xs1 = max(0, dx), min(W, W + dx)
    if ys1 > ys0 and xs1 > xs0:
        out[ys0:ys1, xs0:xs1] = a[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx]
    return out


def gate_c(field, shifts, radius, tile=TILE, stride=STRIDE, margin=None,
           inject_tol=INJECT_TOL_PX, null_tol=NULL_TOL_PX, label="gate C",
           scope_count=None, scope_area=None, edge_frac=EDGE_FRAC,
           edge_abs=EDGE_ABS):
    """ANDON. Validate the instrument on constructed truth before any real
    measurement.

    `field` is a real twin's edge field (real texture statistics, known answer).
    Legs:
      NULL     field vs itself             -> every in-scope tile reads (0, 0)
      INJECT   field vs shift(field, s)    -> every in-scope tile reads s
    `margin` excludes tiles whose search region would reach the zero-filled band
    the shift introduces; it is derived from the largest |shift| and the radius,
    not chosen.

    Returns the per-leg readings. Raises Andon on any miss.
    """
    H, W = field.shape
    R = int(radius)
    if margin is None:
        # DERIVED, not chosen: a tile at r0 searches [r0 - R, r0 + tile + R), and
        # an integer shift of s leaves a |s|-wide zero band at one edge. Excluding
        # tiles whose search reaches that band needs exactly R + max|s|.
        margin = R + max(abs(int(x)) for s in shifts for x in s)
    rows, cols = tile_origins(H, W, tile, stride)
    r0 = np.array([r for r in rows for _ in cols])
    c0 = np.array([c for _ in rows for c in cols])
    interior = ((r0 >= margin) & (r0 + tile <= H - margin)
                & (c0 >= margin) & (c0 + tile <= W - margin))
    report = {"label": label, "radius": R, "tile": tile, "stride": stride,
              "margin": int(margin), "inject_tol_px": inject_tol,
              "null_tol_px": null_tol, "legs": []}

    _kw = dict(scope_count=scope_count, scope_area=scope_area,
               edge_frac=edge_frac, edge_abs=edge_abs)
    null = correlate_tiles(field, field, R, tile, stride, **_kw)
    sel = null["in_scope"] & interior
    if int(sel.sum()) < 8:
        _andon("%s NULL leg has only %d in-scope interior tiles - too few for "
               "the leg to mean anything" % (label, int(sel.sum())))
    err = np.hypot(null["dx"][sel], null["dy"][sel])
    int_bad = int(((null["dx_int"][sel] != 0) | (null["dy_int"][sel] != 0)).sum())
    peak = null["peak"][sel]
    report["legs"].append({
        "leg": "null", "tiles": int(sel.sum()),
        "tiles_with_nonzero_integer_peak": int_bad,
        "subpixel_floor_max_px": float(err.max()),
        "subpixel_floor_mean_px": float(err.mean()),
        "subpixel_floor_p99_px": float(np.percentile(err, 99)),
        "min_peak": float(peak.min()), "mean_peak": float(peak.mean())})
    if int_bad:
        _andon("%s NULL leg: a field correlated against ITSELF put the INTEGER "
               "peak somewhere other than (0, 0) on %d of %d tiles. The "
               "correlator's origin is wrong."
               % (label, int_bad, int(sel.sum())))
    if not (peak.min() > NULL_PEAK_MIN):
        _andon("%s NULL leg: self-correlation peak fell to %.6f. A peak below 1 "
               "on identical input means the surface is not what it should be."
               % (label, float(peak.min())))
    if not (err.max() <= null_tol):
        _andon("%s NULL leg: the sub-pixel estimator's floor on identical input "
               "is %.6f px, over the %.2f px tolerance on %d of %d tiles."
               % (label, float(err.max()), null_tol,
                  int((err > null_tol).sum()), int(sel.sum())))

    for (sdx, sdy) in shifts:
        moved = shift_image(field, int(sdx), int(sdy))
        res = correlate_tiles(field, moved, R, tile, stride, **_kw)
        sel = res["in_scope"] & interior
        if int(sel.sum()) < 8:
            _andon("%s INJECT (%+d, %+d): only %d in-scope interior tiles"
                   % (label, sdx, sdy, int(sel.sum())))
        ex = np.abs(res["dx"][sel] - sdx)
        ey = np.abs(res["dy"][sel] - sdy)
        e = np.hypot(res["dx"][sel] - sdx, res["dy"][sel] - sdy)
        bad = int((e > inject_tol).sum())
        report["legs"].append({
            "leg": "inject", "shift": [int(sdx), int(sdy)],
            "tiles": int(sel.sum()), "tiles_outside_tol": bad,
            "max_err_px": float(e.max()), "mean_err_px": float(e.mean()),
            "p99_err_px": float(np.percentile(e, 99)),
            "max_err_x_px": float(ex.max()), "max_err_y_px": float(ey.max()),
            "mean_peak": float(res["peak"][sel].mean()),
            "min_peak": float(res["peak"][sel].min())})
        if bad:
            _andon("%s INJECT (%+d, %+d): %d of %d in-scope tiles read the "
                   "injected shift wrong by more than %.2f px (max %.4f px). "
                   "Either the sub-pixel fit or the sign convention is wrong."
                   % (label, sdx, sdy, bad, int(sel.sum()), inject_tol,
                      float(e.max())))
    return report


def cross_modal_delta(template_field, twin_field, shifts, radius, tile=TILE,
                      stride=STRIDE, scope_count=None, scope_area=None,
                      edge_frac=EDGE_FRAC, edge_abs=EDGE_ABS):
    """REPORTED, NEVER GATED. Does the instrument recover an injected shift in
    the configuration it is actually used in - a MESH-side template searching a
    TWIN-side field?

    Gate C's legs correlate the twin field against itself, which validates the
    correlator, the origin and the sign, and does NOT exercise the cross-modal
    template. This does. It is a diagnostic rather than a halt for one reason:
    a cross-modal delta that fails is a statement about the twin-to-mesh
    correspondence, which is the experiment's SUBJECT. Halting on it would be
    gating the result.
    """
    base = correlate_tiles(template_field, twin_field, radius, tile, stride,
                           scope_count=scope_count, scope_area=scope_area,
                           edge_frac=edge_frac, edge_abs=edge_abs)
    rows = []
    for (sdx, sdy) in shifts:
        moved = shift_image(twin_field, int(sdx), int(sdy))
        res = correlate_tiles(template_field, moved, radius, tile, stride,
                              scope_count=scope_count, scope_area=scope_area,
                              edge_frac=edge_frac, edge_abs=edge_abs)
        sel = base["in_scope"] & res["in_scope"] & ~base["pinned"] & ~res["pinned"]
        if not sel.any():
            rows.append({"shift": [int(sdx), int(sdy)], "tiles": 0})
            continue
        ddx = res["dx"][sel] - base["dx"][sel]
        ddy = res["dy"][sel] - base["dy"][sel]
        e = np.hypot(ddx - sdx, ddy - sdy)
        rows.append({
            "shift": [int(sdx), int(sdy)], "tiles": int(sel.sum()),
            "median_err_px": float(np.median(e)),
            "mean_err_px": float(e.mean()), "p90_err_px": float(np.percentile(e, 90)),
            "max_err_px": float(e.max()),
            "frac_within_0p5px": float((e <= 0.5).mean()),
            "frac_within_1px": float((e <= 1.0).mean()),
            "median_ddx": float(np.median(ddx)), "median_ddy": float(np.median(ddy)),
        })
    return {"base_in_scope": int(base["in_scope"].sum()), "rows": rows}


# ---------------------------------------------------------------------------
# fixtures + self-test
# ---------------------------------------------------------------------------

def fixture_texture(H=192, W=160, seed=0, sigma=1.0):
    """A band-limited random field: dense structure everywhere, so every tile has
    a template and a unique peak. Band-limiting is what makes the correlation
    surface smooth enough for a sub-pixel fit to mean anything."""
    from scipy.ndimage import gaussian_filter
    rng = np.random.default_rng(seed)
    f = gaussian_filter(rng.normal(size=(H, W)), sigma)
    f -= f.min()
    return (f / max(f.max(), 1e-12)).astype(np.float32)


def _selftest_null_and_inject():
    f = fixture_texture()
    rep = gate_c(f, [(3, 0), (-3, 0), (0, 5), (0, -5), (7, -4), (-6, 9)],
                 radius=16, tile=32, stride=16, label="selftest")
    if len(rep["legs"]) != 7:
        _andon("selftest ran %d legs, expected 7" % len(rep["legs"]))


def _selftest_sign_convention():
    """The convention is PINNED here, not asserted in prose: content moved to the
    RIGHT by 5 px must read dx = +5."""
    f = fixture_texture()
    moved = shift_image(f, 5, 0)
    res = correlate_tiles(f, moved, 16, tile=32, stride=16)
    sel = res["in_scope"] & (res["col0"] > 48) & (res["col0"] < 96) \
        & (res["row0"] > 48) & (res["row0"] < 144)
    if not sel.any():
        _andon("no interior tile survived the sign-convention selection")
    dx = res["dx"][sel]
    if not np.all(np.abs(dx - 5.0) < 0.5):
        _andon("content shifted +5 px in x read dx = %r - the sign is inverted "
               "or the origin is off" % (np.unique(np.round(dx, 2))[:5],))
    if np.all(np.abs(dx + 5.0) < 0.5):
        _andon("dx reads -5 for a +5 shift; the convention is inverted")


def _selftest_pinning_is_visible():
    """A shift LARGER than the window must pin, and pinning must be reported
    rather than silently returning the boundary as an offset.

    THE FIXTURE'S CORRELATION LENGTH IS LOAD-BEARING AND IS A LIMIT OF THE
    SIGNAL. Pinning only detects an out-of-window peak while the surface still
    SLOPES toward it. Measured on the band-limited fixture at sigma = 1 (a
    correlation length of ~2 px), a 20 px shift inside an 8 px window pinned only
    15% of tiles - the surface inside the window is decorrelated noise and the
    argmax lands anywhere. So a low pinning fraction is NOT by itself evidence
    that the window is wide enough; the peak VALUE is the other half of that
    reading, and this module reports both per tile. The fixture below uses
    sigma = 6 so the slope survives to 20 px and the leg tests what it claims.
    """
    f = fixture_texture(sigma=6.0)
    moved = shift_image(f, 20, 0)
    res = correlate_tiles(f, moved, 8, tile=32, stride=16)
    sel = res["in_scope"] & (res["col0"] > 40) & (res["col0"] < 96)
    if not sel.any():
        _andon("no tile selected for the pinning leg")
    if not res["pinned"][sel].mean() > 0.5:
        _andon("a 20 px shift inside an 8 px window did not pin on most tiles "
               "(%.2f) - pinning is not being detected"
               % float(res["pinned"][sel].mean()))
    wide = correlate_tiles(f, moved, 32, tile=32, stride=16)
    selw = wide["in_scope"] & (wide["col0"] > 40) & (wide["col0"] < 96)
    if wide["pinned"][selw].any():
        _andon("widening to 32 px still pins - the widening leg cannot work")


def _selftest_scope_floor_is_local():
    """The floor is a fraction of the tile's OWN area plus an absolute floor.
    A tile with a big area needs proportionally more edge; a tiny one is held to
    the absolute floor rather than passing on one pixel."""
    H = W = 96
    cnt = np.zeros((H, W), dtype=bool)
    area = np.zeros((H, W), dtype=bool)
    cnt[0:32, 0:9] = True             # 288 px of "edge" in the first tile
    area[0:32, 0:32] = True           # 1024 px of "area"
    f = fixture_texture(H, W, seed=1)
    res = correlate_tiles(f, f, 8, tile=32, stride=32,
                          scope_count=cnt, scope_area=area,
                          edge_frac=0.5, edge_abs=8)
    first = 0
    if res["area_px"][first] != 1024 or res["count_px"][first] != 288:
        _andon("scope accounting is wrong: area %d count %d"
               % (res["area_px"][first], res["count_px"][first]))
    if res["floor_px"][first] != 512.0:
        _andon("floor should be 0.5 * 1024 = 512, got %r" % res["floor_px"][first])
    if res["in_scope"][first]:
        _andon("288 edge px cleared a 512 px floor - the floor is not applied")
    res2 = correlate_tiles(f, f, 8, tile=32, stride=32,
                           scope_count=cnt, scope_area=area,
                           edge_frac=0.2, edge_abs=8)
    if not res2["in_scope"][first]:
        _andon("288 edge px did not clear a 204.8 px floor - the floor is "
               "not a fraction of the tile's own area")


def _selftest_tolerance_separates_one_pixel():
    """A 4 px shift must NOT read as 3 px inside the 0.5 px tolerance, or the
    gate's tolerance is too loose to catch a sign or origin error."""
    f = fixture_texture()
    moved = shift_image(f, 4, 0)
    res = correlate_tiles(f, moved, 16, tile=32, stride=16)
    sel = res["in_scope"] & (res["col0"] > 48) & (res["col0"] < 96)
    e = np.abs(res["dx"][sel] - 3.0)
    if e.max() <= INJECT_TOL_PX:
        _andon("a 4 px shift read as 3 px within tolerance - the gate's "
               "tolerance cannot separate one pixel")


def _selftest_gate_c_fires_on_an_unrecoverable_field():
    """THE GATE MUST BE ABLE TO FIRE. Horizontal stripes carry no x information:
    an x-shift of such a field is not recoverable by any correlator, so gate_c's
    inject leg must halt rather than report a confident wrong number.

    This is the shape a real failure would take - a template whose structure
    cannot constrain the offset in one axis - and it is exactly what a thin
    horizontal feature does to a vertical search.
    """
    H, W = 160, 160
    y = np.arange(H)[:, None].astype(np.float64)
    f = (0.5 + 0.5 * np.sin(y / 5.0)) * np.ones((1, W))
    f = f.astype(np.float32)
    try:
        gate_c(f, [(5, 0)], radius=16, tile=32, stride=16, label="cannot-fail probe")
    except Andon:
        return
    _andon("gate_c accepted an x-shift on a field with no x structure - the "
           "gate cannot fire")


def _selftest_interior_edge_excludes_the_outline():
    sil = np.zeros((32, 32), dtype=bool)
    sil[8:24, 8:24] = True
    dedge = silhouette_edge(sil).copy()
    dedge[15:17, 12:20] = True                # a fake internal crease
    inner = interior_depth_edge(dedge, sil)
    if silhouette_edge(sil)[8, 8] and inner[8, 8]:
        _andon("the outline survived into the interior set")
    if not inner[15, 14]:
        _andon("the internal crease was removed with the outline")
    if inner.sum() >= dedge.sum():
        _andon("removing the outline removed nothing")


def _selftest_twin_field_sees_isoluminant_chroma():
    """An L*-only field would miss this edge entirely, which is the reason the
    chroma channels are in the sum."""
    left = np.array([0.55, 0.42, 0.42])

    def lstar(rgb):
        return float(srgb_to_lab(np.asarray(rgb).reshape(1, 1, 3))[0, 0, 0])

    # ISOLUMINANT BY CONSTRUCTION, not by a lucky triple: bisect the green channel
    # of a desaturated-green until its L* matches the left side's.
    target = lstar(left)
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if lstar([0.44, mid, 0.44]) < target:
            lo = mid
        else:
            hi = mid
    right = np.array([0.44, 0.5 * (lo + hi), 0.44])
    img = np.zeros((32, 32, 3), dtype=np.float64)
    img[:, :16] = left
    img[:, 16:] = right
    lab = srgb_to_lab(img)
    dL = abs(float(lab[0, 0, 0] - lab[0, 31, 0]))
    if dL > 0.05:
        _andon("the fixture is not isoluminant (dL* = %.4f); it cannot show the "
               "chroma channels mattering" % dL)
    dC = float(np.hypot(lab[0, 0, 1] - lab[0, 31, 1],
                        lab[0, 0, 2] - lab[0, 31, 2]))
    if dC < 10.0:
        _andon("the fixture's chroma step is only dC = %.2f - too small to "
               "separate a chroma-blind field from a chroma-aware one" % dC)
    f = twin_edge_field(img, sigma=0.0)
    if not f[:, 15:17].max() > 5.0 * max(f[:, 2:6].max(), 1e-6):
        _andon("the near-isoluminant chroma edge did not register (edge %.4f "
               "vs flat %.4f)" % (f[:, 15:17].max(), f[:, 2:6].max()))


def selftest():
    _selftest_null_and_inject()
    _selftest_sign_convention()
    _selftest_pinning_is_visible()
    _selftest_scope_floor_is_local()
    _selftest_tolerance_separates_one_pixel()
    _selftest_gate_c_fires_on_an_unrecoverable_field()
    _selftest_interior_edge_excludes_the_outline()
    _selftest_twin_field_sees_isoluminant_chroma()
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="per-tile twin-to-mesh warp offsets")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if not args.selftest:
        ap.error("this module is imported; the E45 driver script calls it. "
                 "Pass --selftest to run the constructions.")
    try:
        selftest()
    except Andon as e:
        sys.stderr.write(str(e) + "\n")
        return 2
    sys.stdout.write("twin_mesh_warp selftest OK (v%s)\n" % TOOL_VERSION)
    return 0


if __name__ == "__main__":
    sys.exit(main())
