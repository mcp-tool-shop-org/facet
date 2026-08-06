"""Crop the SAME world-space region out of every view's image, under the route's own framing.

WHY THIS EXISTS. Ruling 9d requires a per-view stem drop to be *verified against each view's
actual render*, and handoff 11 adds a term for a structure — the nape crest — that no existing
instrument isolates. `e12_view_visibility.py` answers the geometric half for the HEAD BOX only,
and `e12_head_sheet.py` composes crops somebody else already made. Neither can answer "is this
region presented on this yaw" for an arbitrary region.

WHAT IT DOES. Takes a box in the Gate-0 **Blender frame** (the frame `head_*.json` records its
box in), carries it into the render frame by the SAME uniform scale and the SAME camera
arithmetic `silhouette_masks.py` uses (Ruling 9a: an instrument that must line up with a
recorded number is computed with the arithmetic that produced it), and writes one crop per view
per image set.

  e12_region_crops.py --glb prep_uv.glb --box x0,y0,z0,x1,y1,z1 --aspect 1792,1024
                      --fit-axis width --margin 1.204 --views 0,1,2,3,4,5,6,7 --step 45
                      --images DIR --tag dragonclay --out DIR [--scale 2] [--pad 1.0]
                      [--suffix ""] [--json OUT.json]

⚠ A BOX IS A REGION OF SPACE, NOT A SEGMENTATION — Gate 0's own caveat, carried verbatim.
Anything else occupying the box is inside it, so `first_hit_faces_in_box` bounds visibility
rather than measuring one element's. **The crop is the point**: the number says the region
faces the camera, the picture says what is standing there. Both, or neither.

Standards compliance: PIN_PER_STEP — framing comes from flags matching the profile's and is
echoed per view into the JSON alongside the derived rect. ANDON_AUTHORITY — gates nothing; a
drop-map decision is a ruling's and this is evidence for one. NAMED_COMPENSATORS — writes crops
and one optional JSON into --out; undo = delete that directory. EXTERNAL_VERIFIER — it emits a
number AND a picture on the same question, so the eye can contradict the raycast.
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
ap.add_argument("--glb", required=True)
ap.add_argument("--box", required=True, help="x0,y0,z0,x1,y1,z1 in the Gate-0 Blender frame")
ap.add_argument("--aspect", required=True)
ap.add_argument("--fit-axis", default="width", choices=["height", "width"])
ap.add_argument("--margin", type=float, default=1.204)
ap.add_argument("--views", default="0,1,2,3,4,5,6,7")
ap.add_argument("--step", type=float, default=45.0)
ap.add_argument("--images", required=True, help="dir holding <tag>_<view><suffix>.png")
ap.add_argument("--tag", default="dragonclay")
ap.add_argument("--suffix", default="")
ap.add_argument("--out", required=True)
ap.add_argument("--scale", type=int, default=2)
ap.add_argument("--pad", type=float, default=1.0, help="multiply the derived rect about its "
                                                       "centre before cropping")
ap.add_argument("--label", default="region")
ap.add_argument("--json", default=None)
# ⚠ THE BOX IS A REGION OF SPACE AND THAT IS ITS LIMIT. On this subject the wings arch over
# the neck, so a nape box counts wing membrane passing through it and the per-view number
# says nothing about the crest. These two filters narrow the box's face set to a RIDGE:
# on/near the midline, and facing up. Both are stated as flags rather than hardcoded so the
# filter is a recorded argument, and the crop is emitted either way so the eye can disagree.
ap.add_argument("--x-abs-max", type=float, default=None,
                help="keep only box faces whose centroid |x| (Blender frame, pre-scale) is "
                     "under this — a midline band, for a crest")
ap.add_argument("--nz-min", type=float, default=None,
                help="keep only box faces whose normal z (Blender frame) exceeds this — "
                     "up-facing, which a near-vertical membrane sheet is not")
args = ap.parse_args()

W, H = (int(x) for x in args.aspect.split(","))
BOX = np.asarray([float(x) for x in args.box.split(",")], dtype=np.float64).reshape(2, 3)

m = trimesh.load(args.glb, force="mesh", process=False)
v0 = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
vmax = np.abs(v0).max()
# gltf -> Blender frame, then the uniform 0.5/vmax scale: silhouette_masks' arithmetic
vb = np.stack([v0[:, 0], -v0[:, 2], v0[:, 1]], axis=1) / vmax * 0.5
SCALE = 0.5 / vmax
box = BOX * SCALE

blo, bhi = vb.min(0), vb.max(0)
bmid = (blo + bhi) / 2
if args.fit_axis == "height":
    v_ext = (bhi[2] - blo[2]) * args.margin
    h_ext = v_ext * (W / H)
else:
    h_ext = max(bhi[0] - blo[0], bhi[1] - blo[1]) * args.margin
    v_ext = h_ext * (H / W)

cent = vb[f].mean(axis=1)
in_box = np.all((cent >= box[0]) & (cent <= box[1]), axis=1)
print("[crop] box (scaled) %s .. %s" % (np.round(box[0], 6).tolist(),
                                        np.round(box[1], 6).tolist()), flush=True)
print("[crop] faces with centroid in box: %d / %d (%.4f%%)"
      % (in_box.sum(), len(f), in_box.mean() * 100), flush=True)
n_box = int(in_box.sum())
if args.x_abs_max is not None:
    in_box &= np.abs(cent[:, 0]) <= args.x_abs_max * SCALE
if args.nz_min is not None:
    tv = vb[f]
    nrm = np.cross(tv[:, 1] - tv[:, 0], tv[:, 2] - tv[:, 0])
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-12
    in_box &= np.abs(nrm[:, 2]) >= args.nz_min
if args.x_abs_max is not None or args.nz_min is not None:
    print("[crop] filters (|x| <= %s, |nz| >= %s): %d -> %d faces"
          % (args.x_abs_max, args.nz_min, n_box, int(in_box.sum())), flush=True)

rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(vb.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))

os.makedirs(args.out, exist_ok=True)
rows = {}
for k in [int(x) for x in args.views.split(",")]:
    th = np.radians(k * args.step)
    rgt = np.array([np.cos(th), np.sin(th), 0.0])
    dtc = np.array([np.sin(th), -np.cos(th), 0.0])
    look = -dtc
    up = np.cross(rgt, look)
    up = up / (np.linalg.norm(up) + 1e-12)
    gx = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
    gy = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
    g1, g2 = np.meshgrid(gx, gy)
    org = (bmid[None, None, :] + g1[..., None] * rgt[None, None, :]
           + g2[..., None] * up[None, None, :] - look[None, None, :] * 2.0)
    ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
    hit = np.isfinite(ans["t_hit"].numpy().reshape(H, W))
    pid = ans["primitive_ids"].numpy().reshape(H, W)
    inb = in_box[np.clip(pid, 0, len(f) - 1)]
    px_box = int((hit & inb).sum())
    seen_box = int(len(np.unique(pid[hit & inb]))) if px_box else 0

    corners = np.array([[x, y, z] for x in box[:, 0] for y in box[:, 1] for z in box[:, 2]])
    sx = (corners - bmid) @ rgt
    sy = (corners - bmid) @ up
    cx = (sx + h_ext / 2) / h_ext * W
    cy = (v_ext / 2 - sy) / v_ext * H
    x0, x1, y0, y1 = cx.min(), cx.max(), cy.min(), cy.max()
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    rw, rh = (x1 - x0) * args.pad / 2, (y1 - y0) * args.pad / 2
    rect = [int(max(0, mx - rw)), int(max(0, my - rh)),
            int(min(W, mx + rw)), int(min(H, my + rh))]

    src = os.path.join(args.images, "%s_%d%s.png" % (args.tag, k, args.suffix))
    wrote = None
    if os.path.exists(src):
        im = Image.open(src).convert("RGB")
        if im.size != (W, H):
            raise SystemExit("ANDON: %s is %s but the framing says %s — a rect derived under "
                             "one frame cannot crop another." % (src, im.size, (W, H)))
        c = im.crop(tuple(rect))
        c = c.resize((c.width * args.scale, c.height * args.scale), Image.LANCZOS)
        wrote = os.path.join(args.out, "%s_v%d_%dx.png" % (args.label, k, args.scale))
        c.save(wrote)

    rows[str(k)] = {"yaw": k * args.step, "figure_px": int(hit.sum()),
                    "region_first_hit_px": px_box,
                    "region_px_frac_of_figure": round(px_box / max(1, int(hit.sum())), 6),
                    "region_faces_seen": seen_box,
                    "region_faces_total": int(in_box.sum()),
                    "rect": rect, "crop": wrote}
    print("[crop] view %d yaw %5.1f  figure %7d px | region first-hit %6d px "
          "(%.3f%% of figure), %5d faces | rect %s%s"
          % (k, k * args.step, int(hit.sum()), px_box,
             px_box / max(1, int(hit.sum())) * 100, seen_box, rect,
             "" if wrote else "  [no source image]"), flush=True)

if args.json:
    os.makedirs(os.path.dirname(os.path.abspath(args.json)) or ".", exist_ok=True)
    with open(args.json, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"_what": "per-view first-hit coverage of ONE world box, with the crop rect "
                            "derived under the same framing. A box is a region of space, not a "
                            "segmentation (Gate 0's caveat) — the number bounds visibility and "
                            "the crop shows what is standing there.",
                   "_box_blender": BOX.tolist(), "_scale": SCALE,
                   "_framing": {"aspect": [W, H], "fit_axis": args.fit_axis,
                                "margin": args.margin, "step": args.step},
                   "views": rows}, fh, indent=1)
        fh.write("\n")
    print("[crop] wrote %s" % args.json, flush=True)
