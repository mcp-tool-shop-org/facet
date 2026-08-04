"""Bound the brush arm before spending it — how many holes can the eight stroke cameras see?

CLAUDE.md: *bound an expensive arm before spending it. Compute the ceiling first.* Stage 1 now
covers all eight yaws instead of two, so the hole map is no longer "everything the front and
back twins missed" — it is what no eye-level camera can reach at all. The brush camera set was
designed against a TWO-camera stage 1, and whether it still covers the residual holes is
unmeasured.

Uses `texpass_iter`'s own acceptance construction — `basis(yaw, el)` verbatim, `facing >
--facing-min` (commit's 0.25, not project_twins' 0.45), and depth visibility by raycast — so the
number is what commit would accept, not an optimistic proxy.

  brush_reach.py --prep DIR --styled stage1_8cam_styled_mask.npy [--out-json j]
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--styled", required=True, help="the run's _styled_mask.npy")
ap.add_argument("--facing-min", type=float, default=0.25,
                help="texpass_iter commit's default. NOT project_twins' 0.45.")
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--cameras", default="90:0,270:0,45:0,135:0,225:0,315:0,0:55,180:55",
                help="yaw:el pairs, texpass_loop.ps1's shipped eight")
ap.add_argument("--out-json")
args = ap.parse_args()

meta = json.load(open(os.path.join(args.prep, "meta.json")))
mask = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
valid = mask.reshape(-1)
lo = np.array(meta["lo"], dtype=np.float64)
hi = np.array(meta["hi"], dtype=np.float64)
P = (np.load(os.path.join(args.prep, "pos.npy")).reshape(-1, 3)[valid].astype(np.float64)
     * (hi - lo) + lo) / meta["maxabs"] * 0.5
N = np.load(os.path.join(args.prep, "nor.npy")).reshape(-1, 3)[valid].astype(np.float64) * 2 - 1
N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
NV = P.shape[0]

styled = np.load(args.styled)
assert styled.size == mask.size, "ANDON: styled mask is not the prep's atlas resolution"
styled_v = styled.reshape(-1)[valid]
hole = ~styled_v
print(f"valid {NV:,}   styled {int(styled_v.sum()):,}   HOLES {int(hole.sum()):,} "
      f"({hole.mean()*100:.1f}% of valid)")

m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))


def basis_cd(yaw_d, el_d):
    """texpass_iter.basis's direction-to-camera, verbatim."""
    th, el = np.radians(yaw_d), np.radians(el_d)
    return np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])


CAMS = []
for spec in args.cameras.split(","):
    y, _, e = spec.partition(":")
    CAMS.append((float(y), float(e)))

union = np.zeros(NV, dtype=bool)
rows = {}
print(f"\n{'camera':>12} {'sees holes':>12} {'% of holes':>11} {'new vs union':>13}")
for yaw, el in CAMS:
    dtc = basis_cd(yaw, el)
    facing = (N @ dtc)
    cand = np.where((facing > args.facing_min) & hole)[0]
    if len(cand):
        org = (P[cand] + N[cand] * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
        t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [org, np.broadcast_to(dtc.astype(np.float32), org.shape)], axis=1)))["t_hit"].numpy()
        seen = cand[~np.isfinite(t)]
    else:
        seen = cand
    new = int((~union[seen]).sum())
    union[seen] = True
    key = f"y{int(yaw):+04d}_e{int(el):+03d}"
    rows[key] = {"sees_holes": int(len(seen)),
                 "pct_of_holes": round(len(seen) / max(int(hole.sum()), 1) * 100, 2),
                 "new_vs_running_union": new}
    print(f"{key:>12} {len(seen):>12,} {len(seen)/max(int(hole.sum()),1)*100:>10.2f}% {new:>13,}")

nu = int(union.sum())
nh = int(hole.sum())
print(f"\n{'='*54}")
print(f"  holes the eight stroke cameras can reach: {nu:,} of {nh:,} = {nu/max(nh,1)*100:.1f}%")
print(f"  holes NO stroke camera can reach:         {nh-nu:,} = {(nh-nu)/max(nh,1)*100:.1f}%")
print(f"  those go to finalize's dilation, which is the interpolation the route is trying")
print(f"  to reduce — so this is the ceiling on what eight strokes can convert.")
out = {"valid": NV, "styled": int(styled_v.sum()), "holes": nh,
       "reachable_by_strokes": nu,
       "pct_of_holes_reachable": round(nu / max(nh, 1) * 100, 2),
       "unreachable": nh - nu, "per_camera": rows, "facing_min": args.facing_min}
if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
    print(f"\n[reach] wrote {args.out_json}")
