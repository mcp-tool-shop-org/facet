"""E08 — reference agreement in CIE Lab dE, against a styled reference view.

E08 §5 half 2 specifies HOLD-ONE-OUT dE on C1's two twins. That construction has a
population of exactly ZERO on this asset and it is structural, not a bug: project_twins
accepts a texel at facing > 0.45, front dtc is (0,-1,0) and back is (0,1,0), so
facing_front = -Ny and facing_back = +Ny cannot both clear a positive threshold. Measured:
front 709,466 texels, back 555,925, overlap 0. Hold-one-out needs >=2 cameras per texel and
first has one at N=4 (496,399) — see e08_metric_probe.py.

So this runs the nearest construction that IS computable on the rejected asset, which is
what §4's validation requirement actually needs — does dE in Lab against a styled reference
fire on the regions the Director named:

  REFERENCE AGREEMENT. Sample the finished atlas through the reference camera's own rays,
  compare against that camera's styled reference image in Lab. Where a texel came FROM this
  twin the agreement is near-perfect by construction, so the population that carries signal
  is the 46% of the twin camera's figure that the twin did not paint — brush invention and
  interpolation, on surface the reference can see and therefore has an opinion about.

Sampling is straight from the atlas through the raycast, NOT through a Blender render: the
render applies exposure 0.85 under the Standard view transform, a nonlinear remap that would
land entirely in dE. Reference and asset are compared in the same sRGB space they are
stored in.

dE is CIE76 in Lab. The thresholds are external constants, not derived here: ~2.3 is a
just-noticeable difference, >10 is a plainly different colour.

  e08_deltaE.py --prep DIR --claim c.npy --atlas a.png --view front --twin t.png
                [--regions "blade:x0,y0,x1,y1;boot:..."] [--sheet out.png]
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--claim", required=True)
ap.add_argument("--atlas", required=True)
ap.add_argument("--twin", required=True)
ap.add_argument("--view", default="front", choices=["front", "back"])
ap.add_argument("--facing-min", type=float, default=0.45)
ap.add_argument("--aspect", default="752,1024")
ap.add_argument("--regions", default="", help="name:x0,y0,x1,y1;... in twin pixels")
ap.add_argument("--sheet", help="write a 4-panel diagnostic sheet here")
ap.add_argument("--out-json")
args = ap.parse_args()
AW, AH = [int(x) for x in args.aspect.split(",")]

meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
vv = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
uv = np.asarray(m.visual.uv, dtype=np.float64)
v = np.stack([vv[:, 0], -vv[:, 2], vv[:, 1]], axis=1) / np.abs(vv).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))
blo, bhi = v.min(axis=0), v.max(axis=0)
bmid = (blo + bhi) / 2
v_ext = (bhi[2] - blo[2]) * 1.204
h_ext = v_ext * (AW / AH)

yaw = 0.0 if args.view == "front" else 180.0
th = np.radians(yaw)
dtc = np.array([np.sin(th), -np.cos(th), 0.0])
look = -dtc
right = np.cross(look, [0.0, 0.0, 1.0]); right /= np.linalg.norm(right)
up = np.cross(right, look); up /= np.linalg.norm(up)
xs = (np.arange(AW) + 0.5) / AW * h_ext - h_ext / 2
ys = v_ext / 2 - (np.arange(AH) + 0.5) / AH * v_ext
gx, gy = np.meshgrid(xs, ys)
org = (bmid[None, None, :] + gx[..., None] * right[None, None, :]
       + gy[..., None] * up[None, None, :] - look[None, None, :] * 2.0)
ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
    [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
hit = np.isfinite(ans["t_hit"].numpy().reshape(AH, AW))
prim = ans["primitive_ids"].numpy().reshape(AH, AW)
buv = ans["primitive_uvs"].numpy().reshape(AH, AW, 2)
tri = f[prim[hit]]
wu, wv = buv[hit][:, 0:1], buv[hit][:, 1:2]
uvp = (1 - wu - wv) * uv[tri[:, 0]] + wu * uv[tri[:, 1]] + wv * uv[tri[:, 2]]
axp = np.clip((uvp[:, 0] * RES).astype(np.int64), 0, RES - 1)
ayp = np.clip(((1 - uvp[:, 1]) * RES).astype(np.int64), 0, RES - 1)
tex = np.full((AH, AW), -1, dtype=np.int64)
tex[hit] = ayp * RES + axp

atlas = np.asarray(Image.open(args.atlas).convert("RGB"), dtype=np.float32) / 255.0
claim = np.load(args.claim).reshape(-1)
asset = np.zeros((AH, AW, 3), dtype=np.float32)
asset[hit] = atlas.reshape(-1, 3)[tex[hit]]
twin = np.asarray(Image.open(args.twin).convert("RGB").resize((AW, AH)),
                  dtype=np.float32) / 255.0
mp = os.path.splitext(args.twin)[0] + "_mask.png"
tmask = (np.asarray(Image.open(mp).convert("L"), dtype=np.float32) / 255.0 > 0.5) \
    if os.path.exists(mp) else np.ones((AH, AW), bool)

NF = np.load(os.path.join(args.prep, "nor.npy")).reshape(-1, 3).astype(np.float64) * 2 - 1
NF /= np.linalg.norm(NF, axis=1, keepdims=True) + 1e-12
face = np.zeros((AH, AW))
face[hit] = NF[tex[hit]] @ dtc


def to_lab(rgb):
    """sRGB -> linear -> XYZ (D65) -> Lab"""
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16,
                     500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


dE = np.linalg.norm(to_lab(asset) - to_lab(twin), axis=-1)
dom = hit & tmask
cl = np.full((AH, AW), -1, dtype=np.int16)
cl[hit] = claim[tex[hit]]
nonref = dom & (cl != 0) & (cl >= 0)
out = {"view": args.view, "figure_px": int(dom.sum()),
       "nonreference_px": int(nonref.sum())}
print(f"[dE] {args.view}: {int(dom.sum()):,} px in the twin's own figure mask; "
      f"{int(nonref.sum()):,} ({nonref.sum()/max(int(dom.sum()),1)*100:.1f}%) of them "
      f"are NOT from this reference")


def stat(sel, name):
    if sel.sum() < 50:
        print(f"[dE]   {name:<26s} (only {int(sel.sum())} px)")
        return None
    d = dE[sel]
    # the reference's own median colour, so a hand-placed box can be checked against
    # what it is supposed to be sitting on rather than trusted
    ref = tuple(int(x) for x in (np.median(twin[sel], axis=0) * 255).round())
    got = tuple(int(x) for x in (np.median(asset[sel], axis=0) * 255).round())
    r = {"px": int(sel.sum()), "median": round(float(np.median(d)), 2),
         "mean": round(float(d.mean()), 2),
         "pct_over_2_3": round(float((d > 2.3).mean() * 100), 1),
         "pct_over_10": round(float((d > 10).mean() * 100), 1),
         "ref_rgb": list(ref), "asset_rgb": list(got)}
    print(f"[dE]   {name:<26s} {int(sel.sum()):>8,}px  median {r['median']:6.2f}  "
          f"mean {r['mean']:6.2f}   >2.3 {r['pct_over_2_3']:5.1f}%   "
          f">10 {r['pct_over_10']:5.1f}%   ref rgb {tuple(ref)} -> {tuple(got)}")
    return r


print(f"[dE] by provenance:")
out["all"] = stat(dom, "ALL figure")
out["twins"] = stat(dom & (cl == 0), "TWINS (this reference)")
out["brush"] = stat(dom & (cl > 0) & (cl < 255), "BRUSH (invention)")
out["dilation"] = stat(dom & (cl == 255), "DILATION (interpolation)")
print(f"[dE] by facing band:")
out["core"] = stat(dom & (face > args.facing_min), f"core facing>{args.facing_min}")
out["graze"] = stat(dom & (face <= args.facing_min), "grazing band")

regs = {}
if args.regions:
    print(f"[dE] by region (the Director's named regions first):")
    yy, xx = np.mgrid[0:AH, 0:AW]
    for spec in [s for s in args.regions.split(";") if s.strip()]:
        nm, rest = spec.split(":")
        x0, y0, x1, y1 = [int(t) for t in rest.split(",")]
        box = (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)
        regs[nm] = stat(dom & box, nm)
        regs[nm + "_nonref"] = stat(nonref & box, f"  {nm} (non-reference only)")
out["regions"] = regs

if args.sheet:
    def enc(a):
        return (np.clip(a, 0, 1) * 255).astype(np.uint8)
    pal = np.array([[70, 130, 200], [220, 90, 70], [240, 200, 60], [30, 30, 34]],
                   dtype=np.uint8)   # twins / brush / dilation / bg
    pv = np.full((AH, AW, 3), pal[3])
    pv[dom & (cl == 0)] = pal[0]
    pv[dom & (cl > 0) & (cl < 255)] = pal[1]
    pv[dom & (cl == 255)] = pal[2]
    hm = np.zeros((AH, AW, 3), dtype=np.uint8)
    t = np.clip(dE / 25.0, 0, 1)
    hm[..., 0] = (t * 255)
    hm[..., 1] = ((1 - np.abs(t - 0.5) * 2) * 200)
    hm[..., 2] = ((1 - t) * 180)
    hm[~dom] = (30, 30, 34)
    sheet = np.concatenate([enc(twin), enc(asset), pv, hm], axis=1)
    os.makedirs(os.path.dirname(os.path.abspath(args.sheet)), exist_ok=True)
    Image.fromarray(sheet).save(args.sheet)
    print(f"[dE] wrote {args.sheet}  (reference | asset | provenance | dE heat)")

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
