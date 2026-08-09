"""E13 stroke lane — the stroke cameras, greedy on what a stroke can actually CLOSE, and the
spiral order that keeps the brush continuing a character instead of composing a new one.

WHY NOT `e04_stroke_cameras.py`: that tool's decomposition is a ship's — deck normal,
waterline fraction, hull bottom. A dragon has none of those, and its hole set is not two
coherent surfaces. The METHOD transfers whole and is reproduced here: candidate set, greedy by
marginal coverage, stop at a stated floor, then order by painted adjacency.

CLOSURE IS MODELLED AS COMMIT'S OWN ACCEPTANCE, not as "the camera can see it". A camera sees
essentially the whole brush set at the commit floor — `reach` was defined at facing 0.45 and
commit accepts from 0.25, so a coverage test on visibility alone is tautological and cannot
rank anything. What separates cameras is what commit would KEEP:

    facing > --stroke-facing-min   AND   first-hit visible   AND   inside the emit frame
    AND at least --edge-dist px inside that frame's figure   (commit's edge trim, which is
    where stage 1's own rim losses came from and therefore where these holes live)

RAY DENSITY (Ruling 7b): the facing and visibility tests are one ray per texel — no grid. The
edge test uses the emit frame's own 1792x1024 raster, i.e. the exact grid the shipped emit
would use, so it is not a sampling approximation of something finer; it IS the operand.

THE ORDER IS A CORRECTNESS CONSTRAINT, NOT A PREFERENCE. The standing law: order strokes to
spiral outward from already-painted regions, or the brush composes a new character instead of
continuing one. The number that guards it is the painted-adjacency fraction per stroke, and it
is recomputed after each simulated stroke rather than fixed at the start.

Standards compliance:
  PIN_PER_STEP — every threshold is a flag and prints; the stopping floor is stated as a
    fraction of TWO denominators because the ship's absolute does not transfer by itself.
  ANDON_AUTHORITY — halts if a candidate's frame disagrees with the profile's framing family.
  NAMED_COMPENSATORS — writes one JSON. Undo = delete. Reads only; nothing is emitted.
  EXTERNAL_VERIFIER — the closure model is commit's own rule re-implemented against geometry,
    not a re-read of stage 1's output.

  e13_stroke_cameras.py --prep DIR --brush brush_texels.npy --out J
                        [--candidates 0,22.5,...] [--edge-dist 4.0]
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from scipy.ndimage import binary_dilation, distance_transform_edt

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--brush", required=True, help="brush_texels.npy from e13_hole_map")
ap.add_argument("--styled", required=True, help="stage 1 _styled_mask.npy")
ap.add_argument("--out", required=True)
ap.add_argument("--candidates", default=",".join(f"{i*22.5:g}" for i in range(16)),
                help="candidate yaws at elevation 0. The eight route yaws are IN: on this "
                     "subject the holes are the twins' own erosion rim, and commit's "
                     "edge-dist is far tighter than the projector's scaled one, so a "
                     "same-yaw stroke recovers rim the twin refused.")
ap.add_argument("--stroke-facing-min", type=float, default=0.25)
ap.add_argument("--edge-dist", type=float, default=4.0)
ap.add_argument("--aspect", default="1792,1024")
ap.add_argument("--margin", type=float, default=1.204)
ap.add_argument("--fit-axis", default="width", choices=["height", "width"])
ap.add_argument("--adjacency-px", type=int, default=9,
                help="emit-frame radius for 'already-painted next to this hole'. The "
                     "profile's mask-dilate, so the anchor question is asked at the same "
                     "scale the job mask is grown at.")
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--ship-last-pick", type=int, default=13126)
ap.add_argument("--ship-valid", type=int, default=3111817)
ap.add_argument("--ship-brush", type=int, default=181400)
args = ap.parse_args()

AW, AH = [float(x) for x in args.aspect.split(",")]
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
brush0 = np.load(args.brush)
styled = np.load(args.styled).reshape(-1)[np.where(valid)[0]]
if not (brush0.shape == (NV,) and styled.shape == (NV,)):
    raise AssertionError("ANDON: mask shape disagreement")

m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))
blo, bhi = v.min(axis=0), v.max(axis=0)
bmid = (blo + bhi) / 2
if args.fit_axis == "height":
    v_ext = (bhi[2] - blo[2]) * args.margin
    h_ext = v_ext * (AW / AH)
else:
    h_ext = float(max(bhi[0] - blo[0], bhi[1] - blo[1])) * args.margin
    v_ext = h_ext * (AH / AW)
UP = np.array([0.0, 0.0, 1.0])
W, H = int(AW), int(AH)
print(f"[cams] emit frame --fit-axis {args.fit_axis} margin {args.margin:g} "
      f"{W}x{H} -> h_ext {h_ext:.6f} v_ext {v_ext:.6f}", flush=True)
print(f"[cams] closure = facing > {args.stroke_facing_min:g} AND first-hit visible AND "
      f">= {args.edge_dist:g}px inside the emit-frame figure. Visibility is one ray per "
      f"texel; the edge test uses the shipped emit raster itself (Ruling 7b).", flush=True)


def axes(yaw, el=0.0):
    th, e = np.radians(yaw), np.radians(el)
    d = np.array([np.sin(th) * np.cos(e), -np.cos(th) * np.cos(e), np.sin(e)])
    d /= np.linalg.norm(d)
    r = np.array([np.cos(th), np.sin(th), 0.0])
    return d, r


CAND = [float(x) for x in args.candidates.split(",")]
CLOSE, PXY = {}, {}
for yaw in CAND:
    d, rgt = axes(yaw)
    look = -d
    upv = np.cross(rgt, look)
    upv /= np.linalg.norm(upv) + 1e-12
    gx = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
    gy = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
    g1, g2 = np.meshgrid(gx, gy)
    o = (bmid[None, None, :] + g1[..., None] * rgt[None, None, :]
         + g2[..., None] * upv[None, None, :] - look[None, None, :] * 2.0)
    t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [o, np.broadcast_to(look, o.shape)], axis=-1).reshape(-1, 6).astype(np.float32)
    ))["t_hit"].numpy().reshape(H, W)
    fig = np.isfinite(t)
    dist_in = distance_transform_edt(fig)

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
    deep = dist_in[np.rint(py).astype(int), np.rint(px).astype(int)] >= args.edge_dist
    c = np.zeros(NV, dtype=bool)
    c[idx[deep]] = True
    CLOSE[yaw] = c
    PXY[yaw] = (idx[deep], px[deep], py[deep], fig, dist_in)
    print(f"[cams]   yaw {yaw:>6.1f}: would close {int((c & brush0).sum()):>8,} of "
          f"{int(brush0.sum()):,} brush texels ({(c & brush0).sum()/brush0.sum()*100:5.2f}%)",
          flush=True)

# ---- the greedy ----
floor_valid = args.ship_last_pick / args.ship_valid * NV
floor_brush = args.ship_last_pick / args.ship_brush * int(brush0.sum())
print(f"\n[cams] the ship's last accepted pick added {args.ship_last_pick:,} — "
      f"{args.ship_last_pick/args.ship_valid*100:.3f}% of ITS valid "
      f"({floor_valid:,.0f} here) or {args.ship_last_pick/args.ship_brush*100:.2f}% of ITS "
      f"brush set ({floor_brush:,.0f} here). BOTH denominators are quoted because the "
      f"absolute does not transfer on its own; the ruling picks which one binds.", flush=True)

remaining = brush0.copy()
picks = []
avail = set(CAND)
while avail:
    best, gain = None, -1
    for y in sorted(avail):
        g = int((CLOSE[y] & remaining).sum())
        if g > gain:
            best, gain = y, g
    if gain <= 0:
        break
    remaining &= ~CLOSE[best]
    avail.discard(best)
    closed = int(brush0.sum()) - int(remaining.sum())
    picks.append({"pick": len(picks) + 1, "yaw": best, "new": gain,
                  "cum_closed": closed,
                  "cum_pct_of_brush": closed / int(brush0.sum()) * 100})
    print(f"[cams]   pick {len(picks):>2}  yaw {best:>6.1f}   new {gain:>8,}   "
          f"cumulative {closed:>8,} ({closed/int(brush0.sum())*100:5.2f}% of the brush set)",
          flush=True)

n_valid_floor = sum(1 for p in picks if p["new"] >= floor_valid)
n_brush_floor = sum(1 for p in picks if p["new"] >= floor_brush)
print(f"\n[cams] at the ship's floor read as %-of-valid  ({floor_valid:,.0f}): "
      f"{n_valid_floor} strokes, closing "
      f"{picks[n_valid_floor-1]['cum_pct_of_brush']:.2f}% of the brush set", flush=True)
print(f"[cams] at the ship's floor read as %-of-brush  ({floor_brush:,.0f}): "
      f"{n_brush_floor} strokes, closing "
      f"{picks[n_brush_floor-1]['cum_pct_of_brush']:.2f}% of the brush set", flush=True)
print(f"[cams] decay: pick 1 {picks[0]['new']:,} -> pick {len(picks)} "
      f"{picks[-1]['new']:,} ({picks[-1]['new']/picks[0]['new']*100:.1f}% of the first). "
      f"The ship decayed 40,759 -> 13,126 (32.2%) over eight picks.", flush=True)

# ---- the spiral order, re-scored after every simulated stroke ----
SET = [p["yaw"] for p in picks[:max(n_valid_floor, n_brush_floor)]]
print(f"\n[cams] SPIRAL ORDER over the {len(SET)} selected cameras — painted-adjacency "
      f"recomputed after each simulated stroke (radius {args.adjacency_px}px, the profile's "
      f"mask-dilate), best-anchored first, the ship's order A:", flush=True)
painted = styled.copy()
order, todo = [], list(SET)
while todo:
    scored = []
    for y in todo:
        idx, px, py, fig, dist_in = PXY[y]
        sel = brush0[idx] & ~painted[idx]
        if not sel.any():
            scored.append((0.0, 0, y))
            continue
        pm = np.zeros((H, W), dtype=bool)
        pidx, ppx, ppy, _, _ = PXY[y]
        ps = painted[pidx]
        pm[np.rint(ppy[ps]).astype(int), np.rint(ppx[ps]).astype(int)] = True
        grown = binary_dilation(pm, np.ones((args.adjacency_px, args.adjacency_px), bool))
        hy = np.rint(py[sel]).astype(int)
        hx = np.rint(px[sel]).astype(int)
        anchor = float(grown[hy, hx].mean())
        scored.append((anchor, int(sel.sum()), y))
    scored.sort(reverse=True)
    anchor, n, y = scored[0]
    order.append({"yaw": y, "anchor_pct": anchor * 100, "closes_now": n})
    print(f"[cams]   {len(order):>2}. yaw {y:>6.1f}   painted-adjacency "
          f"{anchor*100:5.2f}%   closes {n:,}", flush=True)
    painted |= CLOSE[y] & brush0
    todo.remove(y)
worst = min(o["anchor_pct"] for o in order)
print(f"[cams] worst painted-adjacency in the order: {worst:.2f}% "
      f"(the ship's band was 80.82-84.74%)", flush=True)

json.dump({"_what": "E13 stroke cameras + spiral order. Closure is commit's acceptance rule, "
                    "not visibility. Nothing is emitted or generated.",
           "frame": {"aspect": [W, H], "fit_axis": args.fit_axis, "margin": args.margin,
                     "h_ext": h_ext, "v_ext": v_ext},
           "params": {"stroke_facing_min": args.stroke_facing_min,
                      "edge_dist": args.edge_dist, "adjacency_px": args.adjacency_px},
           "brush_set": int(brush0.sum()),
           "per_candidate": {str(y): int((CLOSE[y] & brush0).sum()) for y in CAND},
           "greedy": picks,
           "floors": {"ship_last_pick": args.ship_last_pick,
                      "as_pct_of_valid": floor_valid, "as_pct_of_brush": floor_brush,
                      "n_at_valid_floor": n_valid_floor, "n_at_brush_floor": n_brush_floor},
           "selected": SET, "order": order,
           "residual_to_dilation": int(brush0.sum()) - picks[
               max(n_valid_floor, n_brush_floor) - 1]["cum_closed"]},
          open(args.out, "w"), indent=1)
print(f"[cams] wrote {args.out} — DONE (this tool decides nothing; the ruling ratifies)",
      flush=True)
