"""E07 — the render-side half of §5's table, computed identically for every arm.

texpass_metrics.py scores the ATLAS (islands, brush/dilation split, coverage, speckle,
variance). This scores the RENDER at the Director's head zoom, which is where the defect
class he named actually lives:

  * blotch pixels, and the provenance enrichment table (which source is over-represented
    among them)
  * the cross-provenance step ratio, numerator and denominator reported separately in
    8-bit quanta — E07 Gate 0.5 withdrew the ratio's pass condition as mis-formed, so the
    ratio is evidence for the Director and not a gate
  * the flattening guard: mean |L - median5| over the pixel set that was CLEAN in the
    baseline. Every arm renders the same mesh from the same camera, so that set is frozen
    by construction and the comparison is like-for-like. A correct low-frequency levelling
    leaves this untouched; a blur lowers it.

Reads claim.npy; writes nothing into --state, so an arm's own state directory stays
read-only input.

  e07_score_arm.py --prep DIR --claim claim.npy --render arm.png
                   --baseline-render L0.png [--label L1] [--out-json s.json]
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import median_filter

Image.MAX_IMAGE_PIXELS = None
ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--claim", required=True)
ap.add_argument("--render", required=True)
ap.add_argument("--baseline-render", help="the L0 render, for the frozen clean-pixel set")
ap.add_argument("--label", default="arm")
ap.add_argument("--head-crop", default="360,240,700,600")
ap.add_argument("--crop-res", type=int, default=1024)
ap.add_argument("--bound", type=float, default=0.55)
ap.add_argument("--pad", type=float, default=1.25)
ap.add_argument("--res", type=int, default=1024)
ap.add_argument("--blotch", type=float, default=0.10)
ap.add_argument("--out-json")
args = ap.parse_args()

meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
uv = np.asarray(m.visual.uv, dtype=np.float64)
vz = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(vz.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))

CX0, CY0, CX1, CY1 = [float(x) for x in args.head_crop.split(",")]
b = args.bound
sx0 = (CX0 / args.crop_res) * 2 * b - b
sx1 = (CX1 / args.crop_res) * 2 * b - b
sz0 = b - (CY1 / args.crop_res) * 2 * b
sz1 = b - (CY0 / args.crop_res) * 2 * b
cx, cz = (sx0 + sx1) / 2, (sz0 + sz1) / 2
span = max(sx1 - sx0, sz1 - sz0) * args.pad
R = args.res
midy = (vz[:, 1].min() + vz[:, 1].max()) / 2
xs = cx + (np.arange(R) + 0.5) / R * span - span / 2
zs = cz + span / 2 - (np.arange(R) + 0.5) / R * span
gx, gz = np.meshgrid(xs, zs)
org = np.stack([gx, np.full_like(gx, midy - 6.0), gz], axis=-1)
ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
    [org, np.broadcast_to(np.array([0.0, 1.0, 0.0]), org.shape)],
    axis=-1).reshape(-1, 6).astype(np.float32)))
prim = ans["primitive_ids"].numpy().reshape(R, R)
buv = ans["primitive_uvs"].numpy().reshape(R, R, 2)
hit = np.isfinite(ans["t_hit"].numpy().reshape(R, R))
tex = np.full((R, R), -1, dtype=np.int64)
tr = f[prim[hit]]
wu, wv = buv[hit][:, 0:1], buv[hit][:, 1:2]
uvp = (1 - wu - wv) * uv[tr[:, 0]] + wu * uv[tr[:, 1]] + wv * uv[tr[:, 2]]
ax = np.clip((uvp[:, 0] * RES).astype(np.int64), 0, RES - 1)
ay = np.clip(((1 - uvp[:, 1]) * RES).astype(np.int64), 0, RES - 1)
tex[hit] = ay * RES + ax

claim = np.load(args.claim).reshape(-1)
im = np.asarray(Image.open(args.render).convert("RGB"), dtype=np.float32) / 255
lum = im.mean(-1)
dev = np.abs(lum - median_filter(lum, size=5))
blotch = (dev > args.blotch) & hit
out = {"label": args.label, "figure_px": int(hit.sum()), "blotch_px": int(blotch.sum())}
print(f"[{args.label}] figure {int(hit.sum()):,} px   blotch {int(blotch.sum()):,} px "
      f"({blotch.sum()/max(int(hit.sum()),1)*100:.2f}%)")

# ---- provenance enrichment: share of blotch vs share of clean
LBL = {0: "TWINS", 255: "DILATION"}
clean = hit & ~blotch
cb = claim[tex[blotch]]
cc = claim[tex[clean]]
rows = {}
print(f"[{args.label}]   provenance          blotch%   clean%   enrichment")
for k in sorted(set(np.unique(cb)) | set(np.unique(cc))):
    nb = float((cb == k).mean() * 100)
    nc = float((cc == k).mean() * 100)
    lab = LBL.get(int(k), f"BRUSH s{int(k)}")
    rows[lab] = {"blotch_pct": round(nb, 1), "clean_pct": round(nc, 1),
                 "enrichment": round(nb / nc, 2) if nc > 0 else None}
    print(f"[{args.label}]     {lab:<16s} {nb:8.1f} {nc:8.1f}   "
          f"{(nb/nc if nc>0 else float('nan')):8.2f}x")
brush = np.isin(cb, list(range(1, 255)))
brush_c = np.isin(cc, list(range(1, 255)))
out["provenance"] = rows
out["brush_all"] = {"blotch_pct": round(float(brush.mean() * 100), 1),
                    "clean_pct": round(float(brush_c.mean() * 100), 1)}
print(f"[{args.label}]     {'BRUSH, all':<16s} {brush.mean()*100:8.1f} "
      f"{brush_c.mean()*100:8.1f}   {brush.mean()/max(brush_c.mean(),1e-9):8.2f}x")

# ---- step ratio, numerator and denominator separately (Gate 0.5: not a gate)
ok = hit & (tex >= 0)
t1s, t2s, dls = [], [], []
for ax_ in (0, 1):
    a = [slice(None)] * 2; c = [slice(None)] * 2
    a[ax_] = slice(0, -1); c[ax_] = slice(1, None)
    both = ok[tuple(a)] & ok[tuple(c)]
    t1s.append(tex[tuple(a)][both]); t2s.append(tex[tuple(c)][both])
    dls.append(np.abs(lum[tuple(a)][both] - lum[tuple(c)][both]))
t1 = np.concatenate(t1s); t2 = np.concatenate(t2s); dl = np.concatenate(dls)
p1, p2 = claim[t1], claim[t2]
same_p = p1 == p2
diff_t = t1 != t2
Q = 1.0 / 765.0
med_w = float(np.median(dl[same_p & diff_t]))
med_c = float(np.median(dl[~same_p]))
out["step_denom"] = round(med_w, 5)
out["step_numer"] = round(med_c, 5)
out["step_denom_quanta"] = round(med_w / Q, 1)
out["step_numer_quanta"] = round(med_c / Q, 1)
out["step_ratio"] = round(med_c / max(med_w, 1e-9), 3)
print(f"[{args.label}]   step: denom {med_w:.5f} ({med_w/Q:.1f}q)  "
      f"numer {med_c:.5f} ({med_c/Q:.1f}q)  ratio {med_c/max(med_w,1e-9):.3f}")

# ---- flattening guard, over the frozen clean set of the BASELINE
if args.baseline_render:
    imb = np.asarray(Image.open(args.baseline_render).convert("RGB"),
                     dtype=np.float32) / 255
    lb = imb.mean(-1)
    devb = np.abs(lb - median_filter(lb, size=5))
    frozen = hit & (devb <= args.blotch)
    a0 = float(devb[frozen].mean())
    a1 = float(dev[frozen].mean())
    out["guard_pixels"] = int(frozen.sum())
    out["guard_baseline"] = round(a0, 6)
    out["guard_arm"] = round(a1, 6)
    out["guard_change_pct"] = round((a1 - a0) / a0 * 100, 2)
    out["guard_baseline_blotch_px"] = int(((devb > args.blotch) & hit).sum())
    print(f"[{args.label}]   flattening guard over {int(frozen.sum()):,} frozen-clean px: "
          f"{a0:.6f} -> {a1:.6f}   {(a1-a0)/a0*100:+.2f}%  (ANDON at -5%)")
for t in (0.10, 0.15, 0.25):
    out[f"speckle_gt_{t:.2f}_pct"] = round(float((dev > t)[hit].mean() * 100), 2)
print(f"[{args.label}]   head speckle >0.10 {out['speckle_gt_0.10_pct']}%  "
      f">0.15 {out['speckle_gt_0.15_pct']}%  >0.25 {out['speckle_gt_0.25_pct']}%")

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
    print(f"[{args.label}] wrote {args.out_json}")
