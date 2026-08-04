"""E08 Gate 0, half 2 — can the hold-one-out metric be validated at all, and on what?

Two preconditions, both measured rather than assumed, because E08's §4 halt turns on
whether the instrument can see the defect and §5 half 2 specifies a construction whose
population may be empty.

  A  HOLD-ONE-OUT VIABILITY. A texel is comparable only if at least TWO reference
     cameras pass it on facing and depth — otherwise leaving one out leaves nothing to
     compare against. Reports the multiplicity distribution for each camera ladder.
     project_twins' front/back pair is the N=2 case and the answer there is structural:
     facing_front = -Ny and facing_back = +Ny cannot both exceed a positive threshold.

  B  WHAT THE TWIN CAMERAS ACTUALLY IMAGE. A reference-agreement comparison against a
     twin image has signal only over surface the twin camera SEES but did not itself
     paint. Renders C1 from each twin's own camera through the atlas, classifies every
     figure pixel by provenance from claim.npy, and splits it by facing band — so the
     population any such metric would grade is known before a metric is built on it.

  e08_metric_probe.py --prep DIR --claim claim.npy --atlas final.png
                      --twins front.png,back.png [--sets 2,4,6,8,12]
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
ap.add_argument("--twins", required=True, help="front.png,back.png at yaw 0 / 180")
ap.add_argument("--sets", default="2,4,6,8,12")
ap.add_argument("--facing-min", type=float, default=0.45)
ap.add_argument("--head-facing-min", type=float, default=0.18)
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--aspect", default="752,1024")
ap.add_argument("--out-json")
args = ap.parse_args()
AW, AH = [float(x) for x in args.aspect.split(",")]

meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
mask = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
lo = np.array(meta["lo"], dtype=np.float64)
hi = np.array(meta["hi"], dtype=np.float64)
valid = mask.reshape(-1)
P = (np.load(os.path.join(args.prep, "pos.npy")).reshape(-1, 3)[valid].astype(np.float64)
     * (hi - lo) + lo) / meta["maxabs"] * 0.5
N = np.load(os.path.join(args.prep, "nor.npy")).reshape(-1, 3)[valid].astype(np.float64) \
    * 2.0 - 1.0
N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
NV = P.shape[0]
CX0, CY0, CX1, CY1 = meta["crop"]
b_std = 0.55
px1k = (P[:, 0] + b_std) / (2 * b_std) * meta["crop_res"]
py1k = (b_std - P[:, 2]) / (2 * b_std) * meta["crop_res"]
headband = ((px1k >= CX0) & (px1k <= CX1) & (py1k >= CY0) & (py1k <= CY1))

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
out = {}


def dtc_of(yaw_d, el_d=0.0):
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    return cd / np.linalg.norm(cd)


def reach(yaw, el=0.0):
    dtc = dtc_of(yaw, el)
    facing = N @ dtc
    idx = np.where(facing > np.where(headband, args.head_facing_min, args.facing_min))[0]
    org = (P[idx] + N[idx] * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
    t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(dtc.astype(np.float32), org.shape)], axis=1)))["t_hit"].numpy()
    r = np.zeros(NV, dtype=bool)
    r[idx[~np.isfinite(t)]] = True
    return r


# ---------------- A: hold-one-out viability
print("[probe] A — how many reference cameras pass each texel?  A hold-one-out")
print("[probe]     comparison exists only where that count is 2 or more.")
rowsA = {}
for n in [int(s) for s in args.sets.split(",")]:
    cnt = np.zeros(NV, dtype=np.int16)
    for i in range(n):
        cnt += reach(i * 360.0 / n)
    seen = cnt > 0
    comp = cnt >= 2
    rowsA[f"N{n}"] = {"reachable": int(seen.sum()),
                      "comparable": int(comp.sum()),
                      "comparable_pct_of_valid": round(float(comp.mean() * 100), 2),
                      "comparable_pct_of_reachable": round(
                          float(comp.sum() / max(int(seen.sum()), 1) * 100), 2)}
    print(f"[probe]   N={n:<3} reachable {int(seen.sum()):>9,}  "
          f"comparable (>=2 cams) {int(comp.sum()):>9,}  "
          f"{comp.sum()/max(int(seen.sum()),1)*100:5.1f}% of reachable, "
          f"{comp.mean()*100:5.1f}% of valid")
out["A_holdout_viability"] = rowsA

# ---------------- B: what a twin camera images, by provenance
claim = np.load(args.claim).reshape(-1)
atlas = np.asarray(Image.open(args.atlas).convert("RGB"), dtype=np.float32) / 255.0
LBL = {0: "TWINS", 255: "DILATION"}
W, H = int(AW), int(AH)
rowsB = {}
for name, yaw, tw in (("front", 0.0, args.twins.split(",")[0]),
                      ("back", 180.0, args.twins.split(",")[1])):
    dtc = dtc_of(yaw)
    look = -dtc
    right = np.cross(look, [0.0, 0.0, 1.0])
    right /= np.linalg.norm(right) + 1e-12
    up = np.cross(right, look)
    up /= np.linalg.norm(up) + 1e-12
    xs = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
    ys = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
    gx, gy = np.meshgrid(xs, ys)
    org = (bmid[None, None, :] + gx[..., None] * right[None, None, :]
           + gy[..., None] * up[None, None, :] - look[None, None, :] * 2.0)
    ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
    hit = np.isfinite(ans["t_hit"].numpy().reshape(H, W))
    prim = ans["primitive_ids"].numpy().reshape(H, W)
    buv = ans["primitive_uvs"].numpy().reshape(H, W, 2)
    tri = f[prim[hit]]
    wu, wv = buv[hit][:, 0:1], buv[hit][:, 1:2]
    uvp = (1 - wu - wv) * uv[tri[:, 0]] + wu * uv[tri[:, 1]] + wv * uv[tri[:, 2]]
    axp = np.clip((uvp[:, 0] * RES).astype(np.int64), 0, RES - 1)
    ayp = np.clip(((1 - uvp[:, 1]) * RES).astype(np.int64), 0, RES - 1)
    tex = np.full((H, W), -1, dtype=np.int64)
    tex[hit] = ayp * RES + axp
    # per-pixel facing, so the band the twin refused can be separated from its core
    nn = np.zeros((H, W, 3))
    NF = (np.load(os.path.join(args.prep, "nor.npy")).reshape(-1, 3).astype(np.float64)
          * 2.0 - 1.0)
    NF /= np.linalg.norm(NF, axis=1, keepdims=True) + 1e-12
    nn[hit] = NF[tex[hit]]
    face = np.zeros((H, W))
    face[hit] = nn[hit] @ dtc
    c = claim[tex[hit]]
    nfig = int(hit.sum())
    core = hit & (face > args.facing_min)
    graze = hit & (face <= args.facing_min)
    row = {"figure_px": nfig,
           "core_px": int(core.sum()), "graze_px": int(graze.sum())}
    print(f"\n[probe] B — {name} twin camera: {nfig:,} figure px  "
          f"(core facing>{args.facing_min}: {core.sum()/nfig*100:.1f}%, "
          f"grazing: {graze.sum()/nfig*100:.1f}%)")
    for lab, sel in (("ALL figure", hit), ("core", core), ("grazing band", graze)):
        cc = claim[tex[sel]]
        tw_p = float((cc == 0).mean() * 100)
        di_p = float((cc == 255).mean() * 100)
        br_p = 100.0 - tw_p - di_p
        row[lab.replace(" ", "_")] = {"twins_pct": round(tw_p, 1),
                                      "brush_pct": round(br_p, 1),
                                      "dilation_pct": round(di_p, 1)}
        print(f"[probe]     {lab:<14s} TWINS {tw_p:5.1f}%   BRUSH {br_p:5.1f}%   "
              f"DILATION {di_p:5.1f}%   -> non-reference {br_p+di_p:5.1f}%")
    rowsB[name] = row
    np.save(os.path.join(os.path.dirname(os.path.abspath(args.out_json or "./x")),
                         f"texmap_{name}.npy"), tex) if args.out_json else None
out["B_twin_camera_composition"] = rowsB

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
    print(f"\n[probe] wrote {args.out_json}")
