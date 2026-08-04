"""E08 Gate 0, half 1 — how much of the figure can a styled reference physically reach?

`project_twins.py` already answers this for two cameras: `reachable` is the texel set a
view passes on facing AND depth, recorded before the edge test, so it is the ceiling a
projection route can reach rather than what it happened to paint. This runs the same
computation over camera LADDERS and reports where it saturates.

Pure geometry. No diffusion, no GPU, no twin images — a camera that does not exist yet
reaches exactly as much surface as one that does.

Camera direction is generalised from project_twins' two hardcoded entries via
texpass_iter's `basis()`: dtc(yaw, el) = normalize([sin y cos e, -cos y cos e, sin e]),
which returns (0,-1,0) at yaw 0 and (0,1,0) at yaw 180 — the hardcoded pair. The tool
ASSERTS that equivalence before reporting anything, so the generalisation is checked
against the shipped code rather than argued for.

  e08_ceiling.py --prep DIR [--sets 2,4,6,8,12] [--out-json c.json]

Standards compliance: PIN_PER_STEP — every threshold is a parameter and the defaults are
project_twins' own. EXTERNAL_VERIFIER — reports reachable share; it does not say whether
any of it is enough.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--sets", default="2,4,6,8,12")
ap.add_argument("--facing-min", type=float, default=0.45)
ap.add_argument("--head-facing-min", type=float, default=0.18)
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--elev", default="", help="extra elevated cameras, 'yaw:el,yaw:el'")
ap.add_argument("--out-json")
args = ap.parse_args()

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
CROP_RES = meta["crop_res"]
b_std = 0.55
px1k = (P[:, 0] + b_std) / (2 * b_std) * CROP_RES
py1k = (b_std - P[:, 2]) / (2 * b_std) * CROP_RES
headband = ((px1k >= CX0) & (px1k <= CX1) & (py1k >= CY0) & (py1k <= CY1))

m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))
print(f"[ceiling] valid texels {NV:,}   head band {int(headband.sum()):,}", flush=True)


def dtc_of(yaw_d, el_d=0.0):
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    return cd / np.linalg.norm(cd)


# the generalisation must reproduce project_twins' two hardcoded entries exactly
assert np.allclose(dtc_of(0.0), [0.0, -1.0, 0.0]), "ANDON: yaw 0 is not project_twins' front"
assert np.allclose(dtc_of(180.0), [0.0, 1.0, 0.0]), "ANDON: yaw 180 is not its back"

_cache = {}


def reach(yaw, el, fmin_body, fmin_head):
    key = (round(yaw, 4), round(el, 4), fmin_body, fmin_head)
    if key in _cache:
        return _cache[key]
    dtc = dtc_of(yaw, el)
    facing = N @ dtc
    fmin = np.where(headband, fmin_head, fmin_body)
    idx = np.where(facing > fmin)[0]
    if not len(idx):
        _cache[key] = np.zeros(NV, dtype=bool)
        return _cache[key]
    org = (P[idx] + N[idx] * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
    t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(dtc.astype(np.float32), org.shape)], axis=1)))["t_hit"].numpy()
    out = np.zeros(NV, dtype=bool)
    out[idx[~np.isfinite(t)]] = True
    _cache[key] = out
    return out


def yaws(n):
    return [i * 360.0 / n for i in range(n)]


extra = []
for spec in [s for s in args.elev.split(",") if s.strip()]:
    y, e = spec.split(":")
    extra.append((float(y), float(e)))

SETTINGS = [("production (body 0.45 / head 0.18)", args.facing_min, args.head_facing_min),
            ("uniform 0.45", args.facing_min, args.facing_min),
            ("uniform 0.18", args.head_facing_min, args.head_facing_min)]
sets = [int(s) for s in args.sets.split(",")]
out = {"valid_texels": int(NV), "head_band": int(headband.sum()), "settings": {}}

for label, fb, fh in SETTINGS:
    print(f"\n[ceiling] {label}")
    rows = {}
    for n in sets:
        R = np.zeros(NV, dtype=bool)
        for y in yaws(n):
            R |= reach(y, 0.0, fb, fh)
        rows[f"N{n}"] = {"cameras": n, "reachable": int(R.sum()),
                         "pct": round(float(R.mean() * 100), 2)}
        print(f"[ceiling]   {n:>3} cameras (equatorial)   {int(R.sum()):>9,}  "
              f"{R.mean()*100:5.2f}% of valid")
    if extra:
        for n in sets:
            if n < 8:
                continue
            R = np.zeros(NV, dtype=bool)
            for y in yaws(n):
                R |= reach(y, 0.0, fb, fh)
            for y, e in extra:
                R |= reach(y, e, fb, fh)
            rows[f"N{n}+{len(extra)}el"] = {"cameras": n + len(extra),
                                            "reachable": int(R.sum()),
                                            "pct": round(float(R.mean() * 100), 2)}
            print(f"[ceiling]   {n:>3}+{len(extra)} elevated       "
                  f"{int(R.sum()):>9,}  {R.mean()*100:5.2f}% of valid")
    out["settings"][label] = rows

# what a camera adds on its own, in production settings — is the gain the diagonals?
print(f"\n[ceiling] marginal gain per camera, production thresholds, added in "
      f"turnaround order:")
R = np.zeros(NV, dtype=bool)
order = [0.0, 180.0, 90.0, 270.0, 45.0, 135.0, 225.0, 315.0]
marg = {}
for i, y in enumerate(order, start=1):
    before = int(R.sum())
    R |= reach(y, 0.0, args.facing_min, args.head_facing_min)
    marg[f"yaw{int(y)}"] = {"after": int(R.sum()), "added": int(R.sum()) - before}
    print(f"[ceiling]   +yaw {int(y):>3}  -> {int(R.sum()):>9,}  "
          f"{R.mean()*100:5.2f}%   (+{int(R.sum())-before:,})")
out["marginal"] = marg

# the two twins, exactly as shipped — and whether hold-one-out has anything to compare
rf = reach(0.0, 0.0, args.facing_min, args.head_facing_min)
rb = reach(180.0, 0.0, args.facing_min, args.head_facing_min)
ov = int((rf & rb).sum())
out["twin_front_reachable"] = int(rf.sum())
out["twin_back_reachable"] = int(rb.sum())
out["twin_overlap"] = ov
print(f"\n[ceiling] the two shipped twins: front {int(rf.sum()):,}  back {int(rb.sum()):,}"
      f"  union {int((rf|rb).sum()):,} ({(rf|rb).mean()*100:.2f}%)")
print(f"[ceiling] front-back OVERLAP = {ov:,} texels — this is the population a "
      f"hold-one-out comparison at N=2 would have")

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
    print(f"\n[ceiling] wrote {args.out_json}")
