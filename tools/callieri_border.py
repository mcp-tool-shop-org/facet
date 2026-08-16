# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Callieri 2008 border mask + mixed-depth reject + facing weight.

WHY THIS EXISTS. Consult #1 found we closed a "border" lever on the WRONG
quantity: distance to a material/colour boundary in the twin (a dE threshold).
Callieri, Cignoni, Corsini, Scopigno 2008, Masked Photo Blending, section 4,
"Border mask" (preprint https://vcgdata.isti.cnr.it/Publications/2008/CCCS08/CG_textailor.pdf):

    this mask measures how far a pixel in the image is from both image borders
    and discontinuities in the depth map (silhouette borders). [...] To compute
    this mask, the first step is to mark as point of zero value both the image
    borders and the depth discontinuities. The latter can be calculated by
    simply using a Sobel filter on the non-normalized depth map.

We had never built that. This module is that quantity, plus the mixed-depth
2x2 reject from the same consult, kept as a SEPARATE function because they
are not the same lever (see below).

WHAT THE TWO DEPTH LEVERS ARE, AND ARE NOT.

  depth_edge_mask     the discontinuity SET. Binary. A pixel is on a jump.
  mixed_depth_reject  the SAMPLER gate. Binary. A 2x2 bilinear footprint
                      whose four taps are not one surface. One pixel of
                      morphological consequence of the edge set, plus the
                      last row/column (no complete footprint).
  border_weight       the QUALITY weight. Soft, Euclidean. Distance to
                      (image border UNION depth edges), locally scaled.

  mixed_depth_reject does NOT subsume border_weight: a pixel 5 px from an
  edge has mixed_depth False (its 2x2 is clean) and a low-ish border_weight.
  Image-border pixels with no depth jump have border_weight 0 and
  mixed_depth False. border_weight does NOT subsume mixed_depth: a 2x2 that
  straddles a jump must be a hard reject in the sampler, not a small weight
  on a mixed colour. Wiring one and omitting the other is how a material-dE
  quantity stood in for a depth one.

WHAT THIS CANNOT FIX. If the twin's paint is wrong at a location where depth
is locally smooth (no jump, no image border), border_weight is high,
mixed_depth_reject is False, and nothing here knows the paint is wrong.
ControlNet slip on a flat sleeve, a gold fleck in the middle of a tunic, a
wrong hue on a blade face seen head-on: not this instrument.

THE FIGURE OUTLINE. Depth jumping to background IS a Callieri discontinuity.
The entire silhouette is a zero of border_weight. That is intended. The band
width is NOT a global pixel radius: weight is edt / local_halfwidth, and
local_halfwidth is the EDT of the silhouette itself (distance to background).
On a 15 px blade the medial pixel can still reach 1. On a 200 px torso a
pixel 3 px from an internal occlusion is ~3/100. A global saturate-by-image-
diagonal would give the blade ~7/1024 and kill it; that is the constant this
file refuses to ship.

BACKGROUND SENTINEL. Prefer +inf (ray miss / far plane). NaN and -inf are
also treated as background. Do not use 0.0: a valid ortho Z can be near 0.

YES/NO INTERVALS.

  border_weight        0 = on a zero (image border or depth edge).
                       1 = at least one local-halfwidth from every zero
                           (medial interior, or a filled frame whose only
                           zeros are the image border).
  depth_edge_mask      True  = this pixel is on a marked discontinuity.
                       False = locally smooth finite depth, or background
                           that does not touch a figure pixel in 4-neighbours.
  mixed_depth_reject   True  = do not bilinear-sample here.
                       False = the 2x2 with this origin is one surface.
  facing_weight        0 = backfacing, invalid, or background.
                       1 = normal parallel to the view axis.

relative_jump is a fraction of THIS FRAME's finite-depth IQR (p75-p25 on the
silhouette). It is not a world-unit constant. Figure-vs-background (+inf) is
always an edge, regardless of relative_jump. A flat figure (IQR 0) therefore
has only silhouette edges, never finite-finite ones. The sword blade is ~15 px
wide in these frames: blade-vs-background is +inf and always fires; internal
blade dZ is a fraction of the figure IQR and stays under the default.

CALIBRATION CLAIM (run --selftest; T76 pins the same number).
  Canvas 64x64. Figure = columns 30..34 inclusive, rows 8..55, depth 1.0,
  elsewhere +inf. border_weight at pixel (row=32, col=32) == 2.0/3.0.
  Construction: depth-edge zeros sit on cols 30 and 34, so edt at col 32
  is 2; silhouette EDT at col 32 is 3; 2/3. An image-size normalisation
  yields 2/64 = 0.03125 and fails this claim.

Standards:
  ANDON_AUTHORITY - shape / empty-silhouette / non-finite exponent / non-
    positive relative_jump all `raise`. Never `assert`: -O deletes those.
  EXTERNAL_VERIFIER - grades nothing. Emits arrays.
  NAMED_COMPENSATORS - pure functions, no I/O, no hidden state.

  python tools/callieri_border.py --selftest [--out DIR]
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np
from scipy.ndimage import distance_transform_edt

TOOL_VERSION = "1.0.0"

# Default view axis in CAMERA space: Blender camera looks down -Z, a
# front-facing surface has camera-space normal +Z. facing = max(0, n.view).
DEFAULT_VIEW_DIR = (0.0, 0.0, 1.0)

# Default jump as a fraction of this frame's finite-depth IQR. See module doc.
DEFAULT_RELATIVE_JUMP = 0.05

# Construction in the module docstring. T76 re-states the same number.
CALIBRATION_RC = 32
CALIBRATION_CC = 32
CALIBRATION_WEIGHT = 2.0 / 3.0


class Andon(ValueError):
    """A fired gate. Never an `assert`."""


def _andon(msg):
    raise Andon("ANDON: " + msg)


def _as_depth(depth):
    d = np.asarray(depth)
    if d.ndim != 2:
        _andon("depth must be 2-D, got shape %s" % (d.shape,))
    return d.astype(np.float64, copy=False)


def _as_silhouette(silhouette, shape):
    s = np.asarray(silhouette)
    if s.shape != shape:
        _andon("silhouette shape %s does not match depth %s" % (s.shape, shape))
    if s.dtype != bool:
        s = np.asarray(s, dtype=bool)
    if not s.any():
        _andon("silhouette is empty - nothing to weight")
    return s


def _finite(depth):
    return np.isfinite(depth)


def _figure_iqr(depth, silhouette):
    z = depth[silhouette & _finite(depth)]
    if z.size < 4:
        _andon("fewer than 4 finite-depth figure pixels (%d) - cannot form an IQR"
               % z.size)
    q25, q75 = np.percentile(z, [25.0, 75.0])
    return float(q75 - q25)


# Sobel 3x3 weights 1+2+1 on each side. A jump must beat the kernel's
# response to THIS FRAME's typical finite neighbour |dZ|, not a world-unit
# constant. Not a scene knob: it is the kernel's L1 scale.
_SOBEL_L1 = 8.0


def _typical_neighbour_abs(depth):
    """Median |dZ| over finite 4-neighbour pairs. 0 on a constant plane."""
    fin = _finite(depth)
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


def _jump_threshold(depth, silhouette, relative_jump):
    if not np.isfinite(relative_jump) or relative_jump <= 0.0:
        _andon("relative_jump must be finite and > 0, got %r" % (relative_jump,))
    iqr = _figure_iqr(depth, silhouette)
    typical = _typical_neighbour_abs(depth)
    return max(relative_jump * iqr, _SOBEL_L1 * typical)


def _image_border(shape):
    h, w = shape
    border = np.zeros(shape, dtype=bool)
    border[0, :] = True
    border[-1, :] = True
    border[:, 0] = True
    border[:, -1] = True
    return border


def _finite_neighbour_jump(depth, thr):
    """4-connected |dZ| between finite neighbours exceeds thr.

    Callieri names a Sobel on the non-normalised depth. For an axis-aligned
    step the 4-neighbour jump and a 3x3 Sobel mark the same cut; the jump
    form is the one a 1-px step fixture can state exactly. A 3x3 Sobel
    fattens that step and would make the construction unstateable, so it
    is not OR-ed into the set. thr == 0 means "no finite-finite edge"
    (a constant plane; float noise must not become a crease).
    """
    if thr <= 0.0:
        return np.zeros(depth.shape, dtype=bool)
    fin = _finite(depth)
    edge = np.zeros(depth.shape, dtype=bool)
    pair = fin[:, :-1] & fin[:, 1:]
    jump = np.abs(depth[:, :-1] - depth[:, 1:]) > thr
    hit = pair & jump
    edge[:, :-1] |= hit
    edge[:, 1:] |= hit
    pair = fin[:-1, :] & fin[1:, :]
    jump = np.abs(depth[:-1, :] - depth[1:, :]) > thr
    hit = pair & jump
    edge[:-1, :] |= hit
    edge[1:, :] |= hit
    return edge


def _finite_nonfinite_edge(depth):
    """Figure-vs-background. Always a Callieri discontinuity."""
    fin = _finite(depth)
    edge = np.zeros(depth.shape, dtype=bool)
    edge[:, :-1] |= fin[:, :-1] ^ fin[:, 1:]
    edge[:, 1:] |= fin[:, :-1] ^ fin[:, 1:]
    edge[:-1, :] |= fin[:-1, :] ^ fin[1:, :]
    edge[1:, :] |= fin[:-1, :] ^ fin[1:, :]
    return edge


def depth_edge_mask(depth, relative_jump=DEFAULT_RELATIVE_JUMP, silhouette=None):
    """Bool (H, W): pixels on a depth discontinuity.

    relative_jump is a fraction of this frame's finite-depth IQR on the
    silhouette (or on all finite pixels if silhouette is None). Figure-vs-
    background is always True on both sides of the cut. A perfectly flat
    figure therefore contributes only that silhouette, never a finite-finite
    edge.
    """
    d = _as_depth(depth)
    if silhouette is None:
        sil = _finite(d)
        if not sil.any():
            _andon("depth has no finite pixels - no figure")
    else:
        sil = _as_silhouette(silhouette, d.shape)
    thr = _jump_threshold(d, sil, relative_jump)
    return _finite_neighbour_jump(d, thr) | _finite_nonfinite_edge(d)


def mixed_depth_reject(depth, relative_jump=DEFAULT_RELATIVE_JUMP, silhouette=None):
    """Bool (H, W): True where a 2x2 bilinear footprint mixes two surfaces.

    reject[i, j] describes the unit square with origin (i, j) — pixels
    (i, j), (i, j+1), (i+1, j), (i+1, j+1). The last row and last column
    have no complete 2x2 and are True (refuse the tap).

    A window is mixed if it contains both finite and non-finite depth, or
    if its finite values span more than the same jump threshold depth_edge_mask
    uses. Same relative_jump, same IQR. Not a second constant.
    """
    d = _as_depth(depth)
    if silhouette is None:
        sil = _finite(d)
        if not sil.any():
            _andon("depth has no finite pixels - no figure")
    else:
        sil = _as_silhouette(silhouette, d.shape)
    thr = _jump_threshold(d, sil, relative_jump)
    h, w = d.shape
    reject = np.ones((h, w), dtype=bool)
    if h < 2 or w < 2:
        return reject
    a = d[:-1, :-1]
    b = d[:-1, 1:]
    c = d[1:, :-1]
    e = d[1:, 1:]
    fin = np.stack([_finite(a), _finite(b), _finite(c), _finite(e)], axis=0)
    any_f = fin.any(axis=0)
    all_f = fin.all(axis=0)
    any_bg = ~all_f
    span = np.zeros(a.shape, dtype=np.float64)
    if all_f.any():
        span[all_f] = (
            np.maximum.reduce([a[all_f], b[all_f], c[all_f], e[all_f]])
            - np.minimum.reduce([a[all_f], b[all_f], c[all_f], e[all_f]])
        )
    finite_jump = all_f & (thr > 0.0) & (span > thr)
    mixed = (any_f & any_bg) | (finite_jump if thr > 0.0 else False)
    reject[:-1, :-1] = mixed
    return reject


def border_weight(depth, silhouette, relative_jump=DEFAULT_RELATIVE_JUMP):
    """float32 (H, W) in [0, 1]: Callieri border mask.

    Zeros at image borders and at depth discontinuities (including the
    figure's own silhouette against background). Weight is the Euclidean
    distance to the nearest zero, divided by the local silhouette half-width
    (EDT of the silhouette). Background is 0.

    When the silhouette fills the frame there is no background to measure a
    half-width against; then every non-zero pixel is 1 (the only zeros are
    the image border). That is the flat-plane fixture.
    """
    d = _as_depth(depth)
    sil = _as_silhouette(silhouette, d.shape)
    zeros = _image_border(d.shape) | depth_edge_mask(
        d, relative_jump=relative_jump, silhouette=sil)
    # distance_transform_edt wants 0 at the seeds.
    edt = distance_transform_edt(~zeros)
    weight = np.zeros(d.shape, dtype=np.float64)
    interior = sil & ~zeros
    # A silhouette that fills the frame has no background pixel, so there
    # is no half-width to measure. The only zeros are the image border;
    # every interior pixel is then 1. Do not ask EDT(all-True) what that
    # means - scipy's result on an input with no zeros is not a half-width.
    if not np.any(~sil):
        weight[interior] = 1.0
    else:
        half = distance_transform_edt(sil)
        has_half = interior & (half > 0.0)
        weight[has_half] = edt[has_half] / half[has_half]
    np.clip(weight, 0.0, 1.0, out=weight)
    weight[~sil] = 0.0
    weight[zeros] = 0.0
    return weight.astype(np.float32)


def facing_weight(normal, exponent, view_dir=DEFAULT_VIEW_DIR):
    """float32 (H, W): max(0, n.view) ** exponent.

    `normal` is (H, W, 3), camera-space. Non-finite or near-zero normals
    are 0. `view_dir` defaults to +Z (Blender camera space, toward camera).
    The exponent is a parameter, not a constant: the route ships 6.0 and
    wants 2 and 4 once welded-smooth normals exist.
    """
    if not np.isfinite(exponent) or exponent < 0.0:
        _andon("exponent must be finite and >= 0, got %r" % (exponent,))
    n = np.asarray(normal, dtype=np.float64)
    if n.ndim != 3 or n.shape[-1] != 3:
        _andon("normal must be (H, W, 3), got %s" % (n.shape,))
    view = np.asarray(view_dir, dtype=np.float64).reshape(3)
    vnorm = np.linalg.norm(view)
    if vnorm < 1e-12:
        _andon("view_dir has near-zero length")
    view = view / vnorm
    nlen = np.linalg.norm(n, axis=-1)
    valid = np.isfinite(nlen) & (nlen > 1e-8)
    # safe divide: invalid rows stay 0
    nn = np.zeros_like(n)
    nn[valid] = n[valid] / nlen[valid, None]
    dot = (nn * view.reshape(1, 1, 3)).sum(axis=-1)
    facing = np.clip(dot, 0.0, 1.0)
    out = np.zeros(n.shape[:2], dtype=np.float64)
    out[valid] = np.power(facing[valid], exponent)
    return out.astype(np.float32)


# ---------------------------------------------------------------------------
# fixtures + self-test (known by construction; each fails a trivial stand-in)
# ---------------------------------------------------------------------------

def fixture_flat_plane(n=32, z=1.0):
    """Filled frame, constant depth. The only zeros are the image border."""
    depth = np.full((n, n), z, dtype=np.float64)
    sil = np.ones((n, n), dtype=bool)
    return depth, sil


def fixture_step_edge(n=32, col=16, z0=1.0, z1=2.0):
    """Vertical step at `col` (right side starts here). All figure."""
    depth = np.full((n, n), z0, dtype=np.float64)
    depth[:, col:] = z1
    sil = np.ones((n, n), dtype=bool)
    return depth, sil


def fixture_thin_bar(n=64, c0=30, c1=35, r0=8, r1=56, z=1.0):
    """Vertical bar, columns [c0, c1), rows [r0, r1). Background +inf.

    Default is the calibration canvas: 5 px wide, centre column 32.
    """
    depth = np.full((n, n), np.inf, dtype=np.float64)
    sil = np.zeros((n, n), dtype=bool)
    sil[r0:r1, c0:c1] = True
    depth[sil] = z
    return depth, sil


def _selftest_flat_plane():
    depth, sil = fixture_flat_plane(32)
    w = border_weight(depth, sil)
    edge = depth_edge_mask(depth, silhouette=sil)
    if w[16, 16] != 1.0:
        _andon("flat-plane centre weight is %r, not 1.0 "
               "(a trivial all-zero stand-in fails here)" % (float(w[16, 16]),))
    if w[0, 16] != 0.0 or w[16, 0] != 0.0 or w[0, 0] != 0.0:
        _andon("flat-plane image-border is not zero "
               "(a trivial all-one stand-in fails here)")
    if edge.any():
        _andon("flat-plane depth_edge_mask has %d True pixels; a constant "
               "depth has no discontinuity" % int(edge.sum()))
    rej = mixed_depth_reject(depth, silhouette=sil)
    # interior 2x2s are one surface; last row/col are True by contract
    if rej[:31, :31].any():
        _andon("flat-plane mixed_depth_reject fired inside the complete "
               "2x2 region (%d)" % int(rej[:31, :31].sum()))
    if not rej[31, :].all() or not rej[:, 31].all():
        _andon("flat-plane last row/col must be True (no complete 2x2)")


def _selftest_step_edge():
    depth, sil = fixture_step_edge(32, col=16)
    edge = depth_edge_mask(depth, silhouette=sil)
    # columns 15 and 16 are the 4-neighbour pair across the jump
    if not edge[:, 15].all() or not edge[:, 16].all():
        _andon("step-edge at col 16 did not mark columns 15 and 16")
    if edge[:, 8].any() or edge[:, 24].any():
        _andon("step-edge marked a column that is not the step")
    w = border_weight(depth, sil)
    if w[16, 15] != 0.0 or w[16, 16] != 0.0:
        _andon("step-edge pixels themselves must be border_weight 0")
    rej = mixed_depth_reject(depth, silhouette=sil)
    if not rej[10, 15]:
        _andon("2x2 origin (10, 15) straddles the step and must reject")
    if rej[10, 4]:
        _andon("2x2 origin (10, 4) is entirely on the left plane and "
               "must not reject (a stand-in that rejects everywhere fails)")


def _selftest_thin_bar():
    depth, sil = fixture_thin_bar()
    w = border_weight(depth, sil)
    got = float(w[CALIBRATION_RC, CALIBRATION_CC])
    if not np.isclose(got, CALIBRATION_WEIGHT, rtol=0.0, atol=1e-6):
        _andon(
            "CALIBRATION: thin-bar medial weight at (%d, %d) is %r, "
            "not %r (2/3). An image-size normalisation yields ~2/64 = "
            "0.03125 and fails here; an all-one stand-in fails here; a "
            "Gaussian/dilation stand-in does not land on 2/3."
            % (CALIBRATION_RC, CALIBRATION_CC, got, CALIBRATION_WEIGHT))
    edge = depth_edge_mask(depth, silhouette=sil)
    if not edge[32, 30] or not edge[32, 34]:
        _andon("thin-bar silhouette columns 30 and 34 must be depth edges")
    if edge[32, 32]:
        _andon("thin-bar medial pixel is not a depth edge")
    # the two levers are not the same: medial pixel has weight 2/3, and
    # its 2x2 (32,32)-(33,33) is on-bar, same Z, so mixed_depth is False
    rej = mixed_depth_reject(depth, silhouette=sil)
    if rej[32, 32]:
        _andon("thin-bar medial 2x2 is one surface; mixed_depth_reject "
               "must be False there (if it tracked border_weight it "
               "would fire, and the two levers would be one)")
    if w[32, 32] == 0.0:
        _andon("thin-bar medial border_weight is 0; the outline band ate "
               "the structure (global saturate, or zeros too fat)")
    # outline is zero, as Callieri requires
    if w[32, 30] != 0.0 or w[32, 34] != 0.0:
        _andon("thin-bar silhouette is not border_weight 0")
    if w[0, 0] != 0.0:
        _andon("background must be border_weight 0")


def _selftest_ramp_is_not_an_edge():
    """A smooth slant is not a Callieri discontinuity.

    A threshold of relative_jump * IQR alone fires on this ramp (neighbour
    dZ ~ 1/31, IQR ~ 0.5, 0.05*0.5 = 0.025 < 0.032). The typical-slope
    floor is what keeps a torso from being painted as all-edge.
    """
    n = 32
    depth = np.tile(np.linspace(0.0, 1.0, n), (n, 1))
    sil = np.ones((n, n), dtype=bool)
    edge = depth_edge_mask(depth, silhouette=sil)
    if edge.any():
        _andon("a linear ramp marked %d depth-edge pixels; the typical-slope "
               "floor is missing (IQR-only threshold fails here)"
               % int(edge.sum()))


def _selftest_facing():
    n = np.zeros((8, 8, 3), dtype=np.float64)
    n[..., 2] = 1.0
    w6 = facing_weight(n, 6.0)
    if not np.allclose(w6, 1.0):
        _andon("facing +Z ** 6 must be 1, got min %r max %r"
               % (float(w6.min()), float(w6.max())))
    w2 = facing_weight(n, 2.0)
    if not np.allclose(w2, 1.0):
        _andon("facing +Z ** 2 must be 1")
    side = n.copy()
    side[:] = (1.0, 0.0, 0.0)
    if facing_weight(side, 6.0).any():
        _andon("facing +X (side-on) ** 6 must be 0")
    g = n.copy()
    s = np.sqrt(0.5)
    g[:] = (0.0, s, s)
    got = float(facing_weight(g, 2.0)[0, 0])
    if not np.isclose(got, 0.5, rtol=0.0, atol=1e-6):
        _andon("facing (0, s2/2, s2/2) ** 2 must be 0.5, got %r" % got)
    try:
        facing_weight(n, float("nan"))
    except Andon:
        pass
    else:
        _andon("facing_weight accepted a NaN exponent")


def _selftest_andon_can_fail():
    depth, sil = fixture_flat_plane(8)
    try:
        border_weight(depth, np.zeros_like(sil))
    except Andon:
        pass
    else:
        _andon("empty silhouette did not fire (a check that cannot fail)")
    try:
        border_weight(depth, sil, relative_jump=0.0)
    except Andon:
        pass
    else:
        _andon("relative_jump=0 did not fire")


def selftest():
    """Run every construction. Raises Andon on the first miss. Returns 0."""
    _selftest_flat_plane()
    _selftest_step_edge()
    _selftest_thin_bar()
    _selftest_ramp_is_not_an_edge()
    _selftest_facing()
    _selftest_andon_can_fail()
    return 0


def _write_debug_pngs(out_dir):
    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)
    depth, sil = fixture_thin_bar()
    w = border_weight(depth, sil)
    edge = depth_edge_mask(depth, silhouette=sil)
    rej = mixed_depth_reject(depth, silhouette=sil)
    Image.fromarray(np.clip(w * 255.0, 0, 255).astype(np.uint8)).save(
        os.path.join(out_dir, "thin_bar_weight.png"))
    Image.fromarray(np.where(edge, 255, 0).astype(np.uint8)).save(
        os.path.join(out_dir, "thin_bar_edge.png"))
    Image.fromarray(np.where(rej, 255, 0).astype(np.uint8)).save(
        os.path.join(out_dir, "thin_bar_reject.png"))
    Image.fromarray(np.where(sil, 255, 0).astype(np.uint8)).save(
        os.path.join(out_dir, "thin_bar_sil.png"))


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Callieri border mask (self-test; functions are the API)")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--out", default=None,
                   help="with --selftest, write debug PNGs here")
    args = p.parse_args(argv)
    if not args.selftest:
        p.error("nothing to do: this module is imported. "
                "Pass --selftest to run the constructions.")
    try:
        selftest()
    except Andon as e:
        sys.stderr.write(str(e) + "\n")
        return 2
    if args.out:
        _write_debug_pngs(args.out)
    sys.stdout.write("callieri_border selftest OK  calibration %r == %s\n"
                     % (CALIBRATION_WEIGHT, "2/3"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
