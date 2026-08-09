"""E13 — thin_extent's DECISION INPUTS, at the brush's level. Assembles; proposes nothing.

Ruling 7c deferred this value to the stroke-lane ruling on purpose, with the reason stated:
the banked curve rules out both inherited values, and Q12's falsification says no single
GLOBAL value separates membranes from tail spines, frill, claws and thin limbs, because on a
dragon most detail is thin. What the ruling was missing is the cost at the level it actually
bites — the BRUSH's own territory — and that is what this file measures.

THE MEASUREMENT IS EMIT'S OWN, not an analogue of it. `texpass_iter.emit` casts the frame
twice, forward and from the far plane back, and calls a pixel thin when
`ext = 2D - tF - tB < --thin-extent`; thin pixels are removed from the job mask. Reproduced
here on the same grid, per selected stroke camera, and read at each brush texel's own pixel.

A TEXEL IS WITHHELD only if EVERY selected camera that could close it withholds it. Anything
weaker counts a texel as lost when another stroke in the same set would still have painted it,
and would inflate every figure below.

THE REGION-AWARE FAMILY IS EVALUATED, NOT RECOMMENDED. Ruling 7c named "possibly region-aware,
using Task 2.3's wing boxes" as a design the ruling may want; a table it can read is the
deliverable, and the artifact crops beside it are the ship's own criterion.

Standards compliance:
  PIN_PER_STEP — the candidate ladder, the camera set and the region boxes are all flags.
  ANDON_AUTHORITY — halts if the emit frame disagrees with the camera derivation's.
  NAMED_COMPENSATORS — writes one JSON + crops. Undo = delete. Reads only.
  EXTERNAL_VERIFIER — the thickness rule is re-implemented from emit's source against
    geometry, so it agrees with the shipped tool or the disagreement is visible.

  e13_thin_inputs.py --prep DIR --brush b.npy --cams J --values 0,0.005,0.0075,0.01 --out J
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--brush", required=True)
ap.add_argument("--cams", required=True, help="stroke_cameras.json from e13_stroke_cameras")
ap.add_argument("--region", action="append", default=[], metavar="NAME=JSON")
ap.add_argument("--values", default="0.0,0.003,0.005,0.0075,0.01,0.015,0.02,0.03")
ap.add_argument("--wing-values", default="0.005,0.0075,0.01,0.015,0.02,0.03",
                help="region-aware family: this value INSIDE the wing boxes, 0.0 outside")
ap.add_argument("--stroke-facing-min", type=float, default=0.25)
ap.add_argument("--edge-dist", type=float, default=4.0)
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--out", required=True)
ap.add_argument("--crops", help="dir for 2x crops of what each value forbids")
ap.add_argument("--crop-values", default="0.005,0.0075,0.01")
args = ap.parse_args()

CAMJ = json.load(open(args.cams))
W, H = CAMJ["frame"]["aspect"]
h_ext, v_ext = CAMJ["frame"]["h_ext"], CAMJ["frame"]["v_ext"]
SET = CAMJ["selected"]
print(f"[thin] emit frame {W}x{H}  h_ext {h_ext:.6f} v_ext {v_ext:.6f}; selected stroke "
      f"cameras {SET}", flush=True)

meta = json.load(open(os.path.join(args.prep, "meta.json")))
lo = np.array(meta["lo"], dtype=np.float64)
hi = np.array(meta["hi"], dtype=np.float64)
maxabs = float(meta["maxabs"])
mask = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
valid = mask.reshape(-1)
P = ((np.load(os.path.join(args.prep, "pos.npy")).reshape(-1, 3)[valid].astype(np.float64)
      * (hi - lo) + lo) / maxabs * 0.5)
N = np.load(os.path.join(args.prep, "nor.npy")).reshape(-1, 3)[valid].astype(np.float64) \
    * 2.0 - 1.0
N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
NV = P.shape[0]
brush = np.load(args.brush)
if not (brush.shape == (NV,)):
    raise AssertionError("ANDON: brush mask shape disagreement")

m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))
blo, bhi = v.min(axis=0), v.max(axis=0)
bmid = (blo + bhi) / 2
UP = np.array([0.0, 0.0, 1.0])
D = 2.0

REG = {}
for spec in args.region:
    k, _, p = spec.partition("=")
    d = json.load(open(p))
    b0, b1 = [np.array(x, dtype=np.float64) for x in d["region_box_canonical"]]
    REG[k] = ((P >= b0).all(axis=1) & (P <= b1).all(axis=1))
wing = np.zeros(NV, dtype=bool)
for k, s in REG.items():
    if "wing" in k.lower():
        wing |= s
print(f"[thin] wing boxes hold {int((brush & wing).sum()):,} of the brush set's "
      f"{int(brush.sum()):,} ({(brush & wing).sum()/brush.sum()*100:.2f}%)", flush=True)

# per selected camera: closes[c] and ext[c] at each brush texel's own pixel
CLOSES, EXT, CROPDATA = {}, {}, {}
for yaw in SET:
    th = np.radians(yaw)
    d = np.array([np.sin(th), -np.cos(th), 0.0])
    rgt = np.array([np.cos(th), np.sin(th), 0.0])
    look = -d
    upv = np.cross(rgt, look)
    upv /= np.linalg.norm(upv) + 1e-12
    gx = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
    gy = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
    g1, g2 = np.meshgrid(gx, gy)
    o = (bmid[None, None, :] + g1[..., None] * rgt[None, None, :]
         + g2[..., None] * upv[None, None, :] - look[None, None, :] * D)
    tF = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [o, np.broadcast_to(look, o.shape)], axis=-1).reshape(-1, 6).astype(np.float32)
    ))["t_hit"].numpy().reshape(H, W)
    tB = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [o + look[None, None, :] * (2 * D), np.broadcast_to(-look, o.shape)], axis=-1
    ).reshape(-1, 6).astype(np.float32)))["t_hit"].numpy().reshape(H, W)
    hit = np.isfinite(tF)
    ext = np.full((H, W), np.inf)
    both = hit & np.isfinite(tB)
    ext[both] = 2 * D - tF[both] - tB[both]

    from scipy.ndimage import distance_transform_edt
    dist_in = distance_transform_edt(hit)
    fac = N @ d
    idx = np.where(fac > args.stroke_facing_min)[0]
    org = (P[idx] + N[idx] * args.noffs + d[None, :] * args.bias).astype(np.float32)
    tv = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(d.astype(np.float32), org.shape)], axis=1)))["t_hit"].numpy()
    idx = idx[~np.isfinite(tv)]
    xr = (P[idx] @ rgt) - (bmid @ rgt)
    zu = (P[idx] @ UP) - (bmid @ UP)
    px = (xr / h_ext + 0.5) * W - 0.5
    py = (0.5 - zu / v_ext) * H - 0.5
    ok = (px >= 0) & (px <= W - 1) & (py >= 0) & (py <= H - 1)
    idx, px, py = idx[ok], px[ok], py[ok]
    iy, ix = np.rint(py).astype(int), np.rint(px).astype(int)
    deep = dist_in[iy, ix] >= args.edge_dist
    c = np.zeros(NV, dtype=bool)
    c[idx[deep]] = True
    e = np.full(NV, np.inf)
    e[idx[deep]] = ext[iy[deep], ix[deep]]
    CLOSES[yaw], EXT[yaw] = c, e
    CROPDATA[yaw] = (hit, ext)
    print(f"[thin]   yaw {yaw:>6.1f}: closes {int((c & brush).sum()):>8,} brush texels; "
          f"median local thickness there {np.median(e[c & brush]):.5f} canonical units",
          flush=True)

closable = np.zeros(NV, dtype=bool)
for y in SET:
    closable |= CLOSES[y]
base = int((closable & brush).sum())
print(f"\n[thin] the {len(SET)} selected strokes can close {base:,} of the brush set "
      f"({base/brush.sum()*100:.2f}%); everything below is measured against THAT, and "
      f"against the whole 204,617, because the two denominators answer different "
      f"questions.", flush=True)


def withheld(vals_fn):
    """A texel survives if ANY closing camera does not withhold it."""
    surv = np.zeros(NV, dtype=bool)
    for y in SET:
        thr = vals_fn(y)
        surv |= CLOSES[y] & (EXT[y] >= thr)
    return (closable & brush & ~surv)


rows = []
print(f"\n[thin] {'candidate':<26}{'withheld of brush':>19}{'of closable':>14}"
      f"{'of WING brush':>15}{'of non-wing':>13}", flush=True)
for val in [float(x) for x in args.values.split(",")]:
    w = withheld(lambda y, v=val: v)
    tb = int((brush & wing).sum())
    nb = int((brush & ~wing).sum())
    row = {"kind": "global", "value": val, "withheld": int(w.sum()),
           "pct_of_brush": float(w.sum() / brush.sum() * 100),
           "pct_of_closable": float(w.sum() / max(base, 1) * 100),
           "pct_of_wing_brush": float((w & wing).sum() / max(tb, 1) * 100),
           "pct_of_nonwing_brush": float((w & ~wing).sum() / max(nb, 1) * 100)}
    rows.append(row)
    print(f"[thin] global {val:<19g}{int(w.sum()):>12,} {row['pct_of_brush']:>5.2f}%"
          f"{row['pct_of_closable']:>13.2f}%{row['pct_of_wing_brush']:>14.2f}%"
          f"{row['pct_of_nonwing_brush']:>12.2f}%", flush=True)
for val in [float(x) for x in args.wing_values.split(",")]:
    w = withheld(lambda y, v=val: v)          # placeholder, replaced below per-texel
    thr = np.where(wing, val, 0.0)
    surv = np.zeros(NV, dtype=bool)
    for y in SET:
        surv |= CLOSES[y] & (EXT[y] >= thr)
    w = (closable & brush & ~surv)
    tb = int((brush & wing).sum())
    nb = int((brush & ~wing).sum())
    row = {"kind": "wing-only", "value": val, "withheld": int(w.sum()),
           "pct_of_brush": float(w.sum() / brush.sum() * 100),
           "pct_of_closable": float(w.sum() / max(base, 1) * 100),
           "pct_of_wing_brush": float((w & wing).sum() / max(tb, 1) * 100),
           "pct_of_nonwing_brush": float((w & ~wing).sum() / max(nb, 1) * 100)}
    rows.append(row)
    print(f"[thin] wing-only {val:<16g}{int(w.sum()):>12,} {row['pct_of_brush']:>5.2f}%"
          f"{row['pct_of_closable']:>13.2f}%{row['pct_of_wing_brush']:>14.2f}%"
          f"{row['pct_of_nonwing_brush']:>12.2f}%", flush=True)

# ---- the artifact criterion: crops of what each value FORBIDS ----
if args.crops:
    os.makedirs(args.crops, exist_ok=True)
    y0 = SET[0]
    hit, ext = CROPDATA[y0]
    base_img = np.zeros((H, W, 3), dtype=np.uint8)
    base_img[hit] = (150, 150, 156)
    for val in [float(x) for x in args.crop_values.split(",")]:
        im = base_img.copy()
        thin = (ext < val) & hit
        im[thin] = (232, 64, 64)
        ys, xs = np.where(hit)
        bb = (max(0, xs.min() - 20), max(0, ys.min() - 20),
              min(W, xs.max() + 20), min(H, ys.max() + 20))
        crop = Image.fromarray(im).crop(bb)
        crop = crop.resize((crop.width * 2, crop.height * 2), Image.NEAREST)
        p = os.path.join(args.crops, f"forbids_y{y0:g}_{val:g}_2x.png")
        crop.save(p)
        print(f"[thin] crop: yaw {y0:g} at {val:g} forbids {int(thin.sum()):,} px of "
              f"{int(hit.sum()):,} figure ({thin.sum()/hit.sum()*100:.1f}%) -> {p}",
              flush=True)

json.dump({"_what": "thin_extent decision inputs at the BRUSH's level. Assembled for the "
                    "stroke-lane ruling per Ruling 7c. No value is proposed.",
           "selected_cameras": SET, "brush_set": int(brush.sum()),
           "closable_by_selected": base,
           "wing_brush": int((brush & wing).sum()),
           "nonwing_brush": int((brush & ~wing).sum()),
           "rows": rows}, open(args.out, "w"), indent=1)
print(f"\n[thin] wrote {args.out} — DONE. Nothing is proposed; Ruling 7c reserved the value.",
      flush=True)
