"""E12 Gate 0 — where a reconstruction goes non-manifold, counted AND put on the picture.

WHY. `mesh_stats` reports `watertight: False` and stops there, which on these three
dragons is misleading by omission: they have **no open boundary at all** (0-1 boundary
edges, of zero length), so the surface is closed. What makes them non-watertight is edges
with MORE than two adjacent faces. That distinction matters for a subject built out of
sheets, because the obvious way for a membrane thinner than the voxel grid to fail is to
pinch — its two faces meeting along one edge instead of enclosing a thickness — and a pinch
reads as a non-manifold edge, not as a hole.

So the count is a candidate signature of membrane pinching, and a count alone cannot say
that: it is a proxy until somebody looks at WHERE the edges are. This tool therefore does
both — prints the count and projects every non-manifold edge midpoint back onto the
turnaround renders, using turn_render's own camera. The picture is the evidence; the number
is the summary.

It states a hypothesis and shows the data. It does not rule.

Camera convention: `silhouette_masks.py`'s, verified there against byte-identical anchors —
right = (cos th, sin th, 0), up = +Z, ortho_scale = size.z * margin on the vertical axis
under `--fit-axis height`.

Standards compliance:
  PIN_PER_STEP — frame, margin and step are flags; counts and paths are printed.
  ANDON_AUTHORITY — raises if a render's size does not match the declared frame, because a
    marker drawn on the wrong frame is worse than no marker.
  NAMED_COMPENSATORS — writes new PNGs (and an optional JSON). Undo = delete them.
  EXTERNAL_VERIFIER — reports and draws; judges nothing.

  e12_nonmanifold.py --glb m.glb --w 1664 --h 1024 --renders DIR --out DIR
                     [--margin 1.204] [--step 45] [--tag clay] [--json f.json]
"""
import argparse
import glob
import json
import os

import numpy as np
import trimesh
from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--label", default=None)
ap.add_argument("--w", type=int, required=True)
ap.add_argument("--h", type=int, required=True)
ap.add_argument("--margin", type=float, default=1.204)
ap.add_argument("--step", type=float, default=45.0)
ap.add_argument("--renders", required=True)
ap.add_argument("--tag", default="clay")
ap.add_argument("--out", required=True)
ap.add_argument("--json", default=None)
args = ap.parse_args()

GLTF_TO_BLENDER = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]])

m = trimesh.load(args.glb, force="mesh", process=False)
m.merge_vertices(merge_tex=True, merge_norm=True)
f = np.asarray(m.faces)
co = np.asarray(m.vertices, dtype=np.float64) @ GLTF_TO_BLENDER.T
lo, hi = co.min(axis=0), co.max(axis=0)
mid = (lo + hi) / 2.0
size = hi - lo
s = float(size[2] * args.margin) / args.h

e = np.sort(np.vstack([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]]), axis=1)
uniq, cnt = np.unique(e, axis=0, return_counts=True)
nm = uniq[cnt > 2]
bd = uniq[cnt == 1]
lab = args.label or os.path.splitext(os.path.basename(args.glb))[0]
print("[nm] %s: %d unique edges | boundary(1 face) %d | non-manifold(>2 faces) %d (%.5f%%)"
      % (lab, len(uniq), len(bd), len(nm), 100 * len(nm) / len(uniq)), flush=True)
mp = (co[nm[:, 0]] + co[nm[:, 1]]) / 2.0 if len(nm) else np.zeros((0, 3))

rec = {"label": lab, "edges_unique": int(len(uniq)), "boundary_edges": int(len(bd)),
       "nonmanifold_edges": int(len(nm)),
       "nonmanifold_frac": round(float(len(nm) / len(uniq)), 8),
       "nonmanifold_bbox": ([[round(float(v), 4) for v in mp.min(axis=0)],
                             [round(float(v), 4) for v in mp.max(axis=0)]]
                            if len(mp) else None),
       "mesh_extent_blender": [round(float(v), 4) for v in size],
       "frame": [args.w, args.h], "margin": args.margin, "step": args.step}

os.makedirs(args.out, exist_ok=True)
for p in sorted(glob.glob(os.path.join(args.renders, "%s_*.png" % args.tag)),
                key=lambda q: int(os.path.splitext(q)[0].rsplit("_", 1)[1])):
    idx = int(os.path.splitext(p)[0].rsplit("_", 1)[1])
    th = np.radians(idx * args.step)
    rgt = np.array([np.cos(th), np.sin(th), 0.0])
    im = Image.open(p).convert("RGB")
    if not (im.size == (args.w, args.h)):
        raise AssertionError(
            "ANDON: %s is %s but the projection was set up for %dx%d"
            % (os.path.basename(p), im.size, args.w, args.h))
    d = ImageDraw.Draw(im)
    if len(mp):
        px = args.w / 2.0 + ((mp - mid) @ rgt) / s - 0.5
        py = args.h / 2.0 - (mp[:, 2] - mid[2]) / s - 0.5
        for x, y in zip(px, py):
            d.point((x, y), fill=(255, 60, 40))
    d.text((10, 10), "%s view %d - every NON-MANIFOLD edge midpoint in red (%d of %d "
                     "unique edges). Depth is NOT tested: a marker may sit on surface "
                     "facing away from this camera." % (lab, idx, len(nm), len(uniq)),
           fill=(255, 200, 60))
    q = os.path.join(args.out, "nm_%d.png" % idx)
    im.save(q)
    print("[nm] view %d -> %s" % (idx, q), flush=True)

if args.json:
    os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)
    json.dump(rec, open(args.json, "w"), indent=1)
    print("[nm] wrote %s" % os.path.abspath(args.json), flush=True)
