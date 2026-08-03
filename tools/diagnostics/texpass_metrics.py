"""E05 — one metric table, computed identically for every arm.

Written so arms are comparable by construction rather than by care. Every number the
E05 spec asks for comes out of one invocation, against a finished arm (a state dir
after the loop, its prep, its final atlas, and one FLAT front render).

The load-bearing one is `holes closed by brush vs by dilation`. E02 measured 27%
brush / 73% dilation and that ratio is what produced the Director's verdict; an arm
is interesting only if it moves.

`islands containing zero styled texels` is the artifact mechanism. Atlas adjacency is
not surface adjacency, so a colourless island takes its colour across the 4 px gutter
from whichever island the packer happened to place beside it. Texel -> island is
resolved by closest-point query against the mesh (texel 3D position -> face -> island),
NOT by rasterising UV triangles: the positions are already baked in pos.npy and the
query is exact, where a rasteriser would need its own sampling convention and would
disagree with the bake at island borders.

Island partition is union-find over welded UV corners — the same construction
bake_hero_prep.py uses, so island counts here and there mean the same thing.

  texpass_metrics.py --prep DIR --state DIR --atlas final.png --render flat_0.png
                     --stage1-holes N [--label U3] [--json out.json]

--stage1-holes is the hole count project_twins reported for the arm's stage 1, which is
what the brush/dilation split is measured against.
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
ap.add_argument("--state", required=True, help="state dir AFTER the loop")
ap.add_argument("--atlas", required=True, help="finalized atlas")
ap.add_argument("--render", help="FLAT front render of the packed arm, for speckle")
ap.add_argument("--stage1-holes", type=int, required=True)
ap.add_argument("--label", default="arm")
ap.add_argument("--json")
args = ap.parse_args()

meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
valid = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
styled = np.load(os.path.join(args.state, "styled_mask.npy"))
holes = np.asarray(Image.open(os.path.join(args.state, "holes.png")).convert("L")) > 127
out = {"label": args.label}

m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
uv = np.asarray(m.visual.uv, dtype=np.float64)
nf = len(f)

# ---- island partition: union-find over welded UV corners (bake_hero_prep's construction)
lvert = f.reshape(-1)
luv = uv[f].reshape(-1, 2)
key = (lvert.astype(np.int64) << 44) \
      ^ ((luv[:, 0] * 5e5).round().astype(np.int64) << 22) \
      ^ (luv[:, 1] * 5e5).round().astype(np.int64)
loop_face = np.repeat(np.arange(nf, dtype=np.int64), 3)
order = np.argsort(key, kind="stable")
parent = np.arange(nf, dtype=np.int64)


def find(i):
    root = i
    while parent[root] != root:
        root = parent[root]
    while parent[i] != root:
        parent[i], i = root, parent[i]
    return root


sk, sf = key[order], loop_face[order]
run = 0
for j in range(1, len(sk) + 1):
    if j == len(sk) or sk[j] != sk[run]:
        if j - run > 1:
            r0 = find(sf[run])
            for t in range(run + 1, j):
                r = find(sf[t])
                if r != r0:
                    parent[r] = r0
        run = j
roots = np.array([find(i) for i in range(nf)], dtype=np.int64)
uniq, face_island = np.unique(roots, return_inverse=True)
n_isl = len(uniq)
out["islands"] = int(n_isl)
out["faces_per_island"] = round(nf / n_isl, 1)
out["atlas_coverage_pct"] = round(valid.sum() / (RES * RES) * 100, 2)
out["valid_texels"] = int(valid.sum())
print(f"[{args.label}] islands {n_isl:,}  faces/island {nf/n_isl:.1f}  "
      f"atlas coverage {valid.sum()/(RES*RES)*100:.2f}%  valid {int(valid.sum()):,}")

# ---- brush vs dilation
after = int(holes[valid].sum())
brush = args.stage1_holes - after
out["stage1_holes"] = args.stage1_holes
out["holes_after_loop"] = after
out["closed_by_brush"] = int(brush)
out["closed_by_dilation"] = int(after)
out["brush_share_pct"] = round(brush / max(args.stage1_holes, 1) * 100, 1)
print(f"[{args.label}] holes {args.stage1_holes:,} -> {after:,}   "
      f"brush closed {brush:,} ({brush/max(args.stage1_holes,1)*100:.1f}%)  "
      f"dilation closed {after:,} ({after/max(args.stage1_holes,1)*100:.1f}%)")

# ---- texel -> face -> island, by closest point (exact against the baked positions)
lo = np.array(meta["lo"]); hi = np.array(meta["hi"]); maxabs = meta["maxabs"]
pos_e = np.load(os.path.join(args.prep, "pos.npy"))
vflat = valid.reshape(-1)
P = (pos_e.reshape(-1, 3)[vflat].astype(np.float64) * (hi - lo) + lo) / maxabs * 0.5
vz = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(vz.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))
prim = np.empty(len(P), dtype=np.int64)
CH = 1_000_000
for s in range(0, len(P), CH):
    e = min(s + CH, len(P))
    prim[s:e] = rs.compute_closest_points(o3d.core.Tensor(
        P[s:e].astype(np.float32)))["primitive_ids"].numpy().astype(np.int64)
tex_island = face_island[prim]

styled_flat = styled.reshape(-1)[vflat]
hole_flat = holes.reshape(-1)[vflat]
n_styled = np.bincount(tex_island, weights=styled_flat.astype(np.float64), minlength=n_isl)
n_tex = np.bincount(tex_island, minlength=n_isl)
present = n_tex > 0
colourless = present & (n_styled == 0)
hole_in_colourless = int(hole_flat[colourless[tex_island]].sum())
out["islands_with_texels"] = int(present.sum())
out["colourless_islands"] = int(colourless.sum())
out["colourless_islands_pct"] = round(colourless.sum() / max(present.sum(), 1) * 100, 1)
out["hole_texels_in_colourless_islands"] = hole_in_colourless
out["hole_texels_in_colourless_pct"] = round(
    hole_in_colourless / max(int(hole_flat.sum()), 1) * 100, 1)
print(f"[{args.label}] colourless islands {int(colourless.sum()):,}/"
      f"{int(present.sum()):,} ({colourless.sum()/max(present.sum(),1)*100:.1f}%)  "
      f"holding {hole_in_colourless:,} hole texels "
      f"({hole_in_colourless/max(int(hole_flat.sum()),1)*100:.1f}% of holes)")

# ---- final styled share
out["styled_texels_final"] = int(styled_flat.sum())
out["styled_of_valid_pct"] = round(styled_flat.mean() * 100, 1)
print(f"[{args.label}] styled after loop {int(styled_flat.sum()):,}/{len(P):,} "
      f"= {styled_flat.mean()*100:.1f}% of valid")

a = np.asarray(Image.open(args.atlas).convert("RGB"), dtype=np.float32) / 255
out["atlas_variance"] = round(float(a[valid].var()), 5)
print(f"[{args.label}] final atlas variance {a[valid].var():.5f}")

# ---- speckle, against A0's 2.43%
if args.render:
    im = np.asarray(Image.open(args.render).convert("RGB"), dtype=np.float32) / 255
    bg = np.median(np.concatenate([im[:8, :8].reshape(-1, 3),
                                   im[:8, -8:].reshape(-1, 3)]), 0)
    fig = np.abs(im - bg).max(-1) > 0.03
    lum = im.mean(-1)
    dev = np.abs(lum - median_filter(lum, size=5))
    for t in (0.10, 0.15, 0.25):
        pct = round(float((fig & (dev > t)).sum() / max(int(fig.sum()), 1) * 100), 2)
        out[f"speckle_gt_{t:.2f}_pct"] = pct
    print(f"[{args.label}] speckle >0.10 {out['speckle_gt_0.10_pct']}%  "
          f">0.15 {out['speckle_gt_0.15_pct']}%  >0.25 {out['speckle_gt_0.25_pct']}%  "
          f"(A0 = 2.43 / 1.18 / 0.30)")

if args.json:
    json.dump(out, open(args.json, "w"), indent=1)
    print(f"[{args.label}] wrote {args.json}")
