"""TEXTURE-SPACE PASS — finalize: fill the residual holes after the brush loop.

Remaining holes after the brush loop are undersides, crevices and the blade flank
(excluded from diffusion BY POLICY — thin hard-surface props take dilated projected
colour, never invented content).

Two fills, selected by --surface-aware:

  DEFAULT (E02..E06 behaviour, kept so those arms reproduce byte-for-byte)
    Iterative 4-neighbour average in ATLAS space from styled texels, then mean
    fallback + gutter dilation for mips.
    ! The docstring here used to claim this was "valid-island-constrained". It is
      not, and never was: the write predicate is `~grown & (cnt > 0)` with no
      `& valid`, so gutter texels are filled on the first iteration and become
      SOURCES on the second. E07 Gate 0 measured what that costs on E06's C1 —
      74.9% of dilated texels take colour from another island, from a median
      0.177 away on a figure ~1.0 tall.

  --surface-aware (E07 arm L1)
    Every hole texel takes the colour of its nearest painted texel IN 3D, by
    cKDTree over the baked positions. The atlas is an index; pos.npy is the
    neighbourhood. Measured on the same C1 state, the median source distance falls
    to 0.00253 — below one triangle edge, a 70x shrink. The 16-step gutter
    dilation still runs afterwards, into INVALID texels only, for mips; it cannot
    walk back into the surface because every valid texel already has colour.

  texpass_finalize.py --state DIR --prep DIR --out atlas_final.png [--surface-aware]

Reads --state, writes only --out: it cannot mutate the arm it is replayed from.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ap = argparse.ArgumentParser()
ap.add_argument("--state", required=True)
ap.add_argument("--prep", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--surface-aware", action="store_true",
                help="E07 L1: nearest painted texel in 3D instead of an atlas-space flood")
# The gate is on SOURCE DISTANCE, in median triangle edges — the failure mode itself.
# It replaces a back-facing-normal threshold withdrawn at E07 Gate 0.5: normal
# disagreement is a PROXY for "sourced from elsewhere on the figure", and the proxy
# inverts. Measured on C1, the back-facing class is the CLOSEST class (0.77 edges vs
# 1.16 for the agreeing class, 66.7% of it inside a single triangle), because a sheet
# thinner than its own tessellation has its opposite face as the nearest surface — and
# --thin-extent routes exactly that surface class here on purpose. Disagreement is
# still reported. It is never a halt.
ap.add_argument("--max-edge-median", type=float, default=3.0,
                help="ANDON: halt if the median source distance exceeds this many median "
                     "triangle edges")
ap.add_argument("--beyond-edges", type=float, default=20.0)
ap.add_argument("--max-frac-beyond", type=float, default=0.05,
                help="ANDON: halt if more than this share of lookups exceed --beyond-edges")
ap.add_argument("--json", help="write the lookup measurements here")
args = ap.parse_args()

atlas = np.asarray(Image.open(os.path.join(args.state, "atlas.png")).convert("RGB"),
                   dtype=np.float32) / 255.0
holes = np.asarray(Image.open(os.path.join(args.state, "holes.png")).convert("L"),
                   dtype=np.float32) / 255.0 > 0.5
valid = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
RES = atlas.shape[0]
have = valid & ~holes
need = valid & holes
img = atlas.copy()
print(f"[finalize] filling {int(need.sum()):,} hole texels "
      f"({'surface-aware' if args.surface_aware else 'atlas-space flood'})", flush=True)
rep = {"mode": "surface_aware" if args.surface_aware else "atlas_flood",
       "hole_texels": int(need.sum()), "painted_texels": int(have.sum())}

if args.surface_aware:
    from scipy.spatial import cKDTree
    if not (have.any()):
        raise AssertionError(
            "ANDON: nothing is painted — nowhere to source colour from")
    meta = json.load(open(os.path.join(args.prep, "meta.json")))
    lo = np.array(meta["lo"])
    hi = np.array(meta["hi"])
    P = (np.load(os.path.join(args.prep, "pos.npy")).astype(np.float64)
         * (hi - lo) + lo) / meta["maxabs"] * 0.5
    N = np.load(os.path.join(args.prep, "nor.npy")).astype(np.float64) * 2.0 - 1.0
    N /= np.linalg.norm(N, axis=-1, keepdims=True) + 1e-12
    src_i = np.flatnonzero(have.reshape(-1))
    tgt_i = np.flatnonzero(need.reshape(-1))
    Pf, Nf = P.reshape(-1, 3), N.reshape(-1, 3)
    tree = cKDTree(Pf[src_i])
    dist, j = tree.query(Pf[tgt_i], k=1, workers=-1)
    pick = src_i[j]
    img.reshape(-1, 3)[tgt_i] = atlas.reshape(-1, 3)[pick]

    # Report the operation's FAILURE mode, not its success mode: how far away, on the
    # actual surface, the colour came from. The scale must come from THIS mesh — a
    # hardcoded constant is the same family as the blade pixel-rectangle the loop was
    # rewritten to remove, and it is load-bearing now that the gate is stated in edges.
    import trimesh
    _m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
    _v = np.asarray(_m.vertices, dtype=np.float64)
    _f = np.asarray(_m.faces, dtype=np.int64)
    _vz = np.stack([_v[:, 0], -_v[:, 2], _v[:, 1]], axis=1) / np.abs(_v).max() * 0.5
    _t = _vz[_f]
    edge = float(np.median(np.linalg.norm(
        np.concatenate([_t[:, 1] - _t[:, 0], _t[:, 2] - _t[:, 1], _t[:, 0] - _t[:, 2]]),
        axis=1)))
    dot = np.einsum("ij,ij->i", Nf[tgt_i], Nf[pick])
    over60 = float((dot < 0.5).mean())
    back = float((dot < 0.0).mean())
    med_e = float(np.median(dist)) / edge
    beyond = float((dist > args.beyond_edges * edge).mean())
    rep.update(
        median_edge_len=round(edge, 6),
        dist_median=round(float(np.median(dist)), 6),
        dist_median_edges=round(med_e, 3),
        dist_p95=round(float(np.percentile(dist, 95)), 6),
        dist_max=round(float(dist.max()), 6),
        dist_gt_5edge_pct=round(float((dist > 5 * edge).mean() * 100), 2),
        dist_beyond_pct=round(beyond * 100, 3),
        normal_disagree_gt60_pct=round(over60 * 100, 2),
        normal_back_facing_pct=round(back * 100, 2))
    print(f"[finalize]   median triangle edge {edge:.5f}  (measured on this mesh)")
    print(f"[finalize]   source distance  median {np.median(dist):.5f} = "
          f"{med_e:.2f} edges   p95 {np.percentile(dist,95):.5f}   max {dist.max():.5f}")
    print(f"[finalize]   beyond 5 edges {(dist>5*edge).mean()*100:5.2f}%   "
          f"beyond {args.beyond_edges:.0f} edges {beyond*100:5.3f}%")
    print(f"[finalize]   normal disagrees >60deg {over60*100:5.2f}%   back-facing "
          f"{back*100:5.2f}%   (REPORTED, not gated — E07 Gate 0.5)")
    if not (med_e <= args.max_edge_median):
        raise AssertionError(
            f"ANDON: median source distance {med_e:.2f} edges, over the "
            f"{args.max_edge_median} limit — colour is coming from elsewhere on the figure.")
    if not (beyond <= args.max_frac_beyond):
        raise AssertionError(
            f"ANDON: {beyond*100:.2f}% of lookups source from beyond {args.beyond_edges:.0f} "
            f"edges, over the {args.max_frac_beyond*100:.0f}% limit.")
    grown = valid.copy()                 # every valid texel now carries colour
    STEPS = 16                           # gutter only, for mips
else:
    grown = have.copy()
    STEPS = 96

for step in range(STEPS):
    todo = valid & ~grown
    if not todo.any() and step >= 16:    # extra 16 = gutter dilation beyond islands
        break
    acc = np.zeros((RES, RES, 3), dtype=np.float32)
    cnt = np.zeros((RES, RES), dtype=np.float32)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nb_v = np.roll(grown, (dy, dx), axis=(0, 1))
        acc += np.roll(img, (dy, dx), axis=(0, 1)) * nb_v[..., None]
        cnt += nb_v
    fill = ~grown & (cnt > 0)
    img[fill] = acc[fill] / cnt[fill][..., None]
    grown |= fill
left = int((valid & ~grown).sum())
if left:
    img[valid & ~grown] = img[have].mean(axis=0)
rep["mean_fallback"] = left
if args.surface_aware:
    # E14 Ruling 31d.1. In this mode `grown = valid.copy()` runs BEFORE the loop
    # (line 135), so `valid & ~grown` is empty by construction and `left` is 0 on
    # every run regardless of the atlas. Three subjects quoted that zero as a
    # pass; the dragon's celebrated zero was structural, not earned. A check that
    # cannot fail is not a check, so this mode must not print the count as if it
    # were informative. The value is still shown — a non-zero here would mean the
    # construction above had changed and is worth being startled by — but it is
    # labelled for what it is. The mode's real gate is the source-distance
    # distribution printed above, which IS gated, by the two ANDONs at 129/132.
    print(f"[finalize] done, mean fallback {left:,} - STRUCTURAL in surface-aware "
          f"mode (grown = valid.copy() before the loop), not a measured pass; the "
          f"gated quantity is the source distance above  [E14 Ruling 31d]",
          flush=True)
else:
    print(f"[finalize] done, {left:,} texels took mean fallback", flush=True)
var = float(img[valid].var())
rep["atlas_variance"] = round(var, 5)
if not (var > 0.001):
    raise AssertionError("ANDON: final atlas uniform")
os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
Image.fromarray((img * 255).round().astype(np.uint8)).save(args.out)
if args.json:
    json.dump(rep, open(args.json, "w"), indent=1)
print(f"[finalize] wrote {args.out}  var {var:.5f}", flush=True)
