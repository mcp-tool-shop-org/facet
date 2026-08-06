"""Does a prep bake's position map lie ON the mesh? E10 Ruling 4's question, any subject.

WHY THIS FILE EXISTS AND WHY IT IS NOT `e10_offsurface.py`. That instrument answers exactly
this question and its method is the one reproduced here - but it is hardcoded to the ship
(`PREP = ...E04_shipprep`, `STROKE = ...E04_stroke`, and it reads `ship.json`'s waterline),
and its second half needs an emitted stroke directory (`job_y+000_e+00/cam.json`,
`hit.png`) to compare the bake against painted coverage. **The beast has run no strokes**,
so that half cannot exist yet on this subject. Rather than edit a shipped instrument whose
numbers are cited in a closed ruling, this carries the bake half - the part the E12 dispatch
asks for - with the subject supplied by flags.

THE METHOD IS `e10_offsurface.py`'s, unchanged, so the numbers are comparable to the ship's:
world position per uv-valid texel is reconstructed as `(lo + pos*(hi-lo)) * (0.5/maxabs)`
from `meta.json`, and distance to the surface comes from open3d's raycasting scene over the
canonicalised mesh. A fixed-seed sample keeps it cheap and reproducible.

THE UNIT IS AN EMIT-IMAGE PIXEL, and it is derived, not inherited. `e10_offsurface` read
`one_px = v_ext / H` out of a stroke's `cam.json`. With no stroke, `--v-ext` is computed here
from the SUBJECT'S OWN ruled framing by `texpass_iter`'s rule: at `--fit-axis width`,
`h_ext = max(x,y extent) * margin` and `v_ext = h_ext * H/W`; at `height`,
`v_ext = z extent * margin`. Pass `--v-ext` directly to override. Getting this wrong scales
every threshold, so the derivation is printed with its operands.

WHAT IT DOES NOT DO. It halts nothing and classifies nothing as acceptable. E10 Ruling 4
established that off-surface texels on the ship were *painted, not padding*; whether that
holds here is a question for a ruling with a stroke in hand, not for this tool.

  e12_offsurface.py --prep DIR [--profile p.json] [--aspect 1792,1024] [--margin 1.204]
                    [--fit-axis width] [--v-ext X] [--sample 200000] [--out j.json]

Standards compliance: PIN_PER_STEP - every operand of the pixel unit is a flag and is
echoed. EXTERNAL_VERIFIER - reports distances; rules nothing. NAMED_COMPENSATORS - reads a
bake, writes one JSON.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--label", default=None)
ap.add_argument("--aspect", default="1792,1024")
ap.add_argument("--margin", type=float, default=1.204)
ap.add_argument("--fit-axis", default="width", choices=["height", "width"])
ap.add_argument("--v-ext", type=float, default=None,
                help="override the derived emit-camera vertical extent, canonical units")
ap.add_argument("--sample", type=int, default=200000)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--out", default=None)
args = ap.parse_args()

J = os.path.join
W, H = (int(x) for x in args.aspect.split(","))
meta = json.load(open(J(args.prep, "meta.json"), encoding="utf-8"))
s = 0.5 / meta["maxabs"]

m = trimesh.load(J(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
V = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
F = np.asarray(m.faces, dtype=np.int64)
ext = V.max(axis=0) - V.min(axis=0)

if args.v_ext is not None:
    v_ext, how = args.v_ext, "supplied by --v-ext"
elif args.fit_axis == "width":
    h_ext = max(ext[0], ext[1]) * args.margin
    v_ext = h_ext * (H / W)
    how = ("fit-axis width: h_ext = max(x,y)=%.6f * margin %.4f = %.6f; v_ext = h_ext * H/W"
           % (max(ext[0], ext[1]), args.margin, h_ext))
else:
    v_ext = ext[2] * args.margin
    how = "fit-axis height: v_ext = z extent %.6f * margin %.4f" % (ext[2], args.margin)
one_px = v_ext / H
lab = args.label or os.path.basename(os.path.abspath(args.prep))
print("[off] %s | canonical extent %s" % (lab, [round(float(x), 5) for x in ext]), flush=True)
print("[off] %s" % how, flush=True)
print("[off] v_ext %.6f over H=%d -> ONE EMIT PIXEL = %.6e canonical units"
      % (v_ext, H, one_px), flush=True)

rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(V.astype(np.float32)), o3d.core.Tensor(F.astype(np.uint32)))

pos = np.asarray(np.load(J(args.prep, "pos.npy"), mmap_mode="r"), dtype=np.float64)
uv = np.asarray(np.load(J(args.prep, "mask.npy"), mmap_mode="r")[..., 0]) > 0.5
lo, hi = np.array(meta["lo"]), np.array(meta["hi"])
ys, xs = np.where(uv)
k = np.random.default_rng(args.seed).choice(len(ys), min(args.sample, len(ys)), replace=False)
P = (lo + pos[ys[k], xs[k]] * (hi - lo)) * s
d = rs.compute_distance(o3d.core.Tensor(P.astype(np.float32))).numpy().astype(np.float64)

rec = {"label": lab, "prep": os.path.abspath(args.prep),
       "aspect": [W, H], "margin": args.margin, "fit_axis": args.fit_axis,
       "v_ext": v_ext, "one_px": one_px, "v_ext_derivation": how,
       "uv_valid_texels": int(uv.sum()), "sampled": int(len(k)),
       "median_distance": float(np.median(d)),
       "median_distance_px": float(np.median(d) / one_px),
       "pct_off_surface_gt_1px": float(100.0 * (d > one_px).mean()),
       "pct_off_surface_gt_5px": float(100.0 * (d > 5 * one_px).mean()),
       "max_distance_px": float(d.max() / one_px)}
print("[off] %s uv-valid texels, %s sampled (seed %d)"
      % (f"{rec['uv_valid_texels']:,}", f"{rec['sampled']:,}", args.seed), flush=True)
print("[off] median distance to surface %.3e  (%.4f px)"
      % (rec["median_distance"], rec["median_distance_px"]), flush=True)
print("[off] OFF-SURFACE (>1 px): %.4f%%   (>5 px): %.4f%%   max %.1f px"
      % (rec["pct_off_surface_gt_1px"], rec["pct_off_surface_gt_5px"],
         rec["max_distance_px"]), flush=True)
if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    json.dump(rec, open(args.out, "w"), indent=1)
    print("[off] wrote %s" % os.path.abspath(args.out), flush=True)
