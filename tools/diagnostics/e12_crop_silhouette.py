"""An exact mesh silhouette at an ARBITRARY crop camera — the mask a head-crop control needs.

`silhouette_masks.py` derives its camera from the whole-mesh bbox, so it cannot frame a
sub-region; a head-crop companion needs a mask at the crop's own camera. Two ways to get one
were on the table and only this one is honest:

  * upscale a crop of the full-frame silhouette — REJECTED. The companion frame resolves
    ~4.1x finer than the route frame, so the mask's boundary would be a 4x blocky staircase
    and the contour term (a morphological gradient of exactly that boundary) would inherit it.
  * raycast at the crop camera — this file. The camera is `e12_head_render.py`'s, reproduced
    line for line, and the tool PRINTS both constructions' agreement so the reproduction is
    checked rather than asserted.

CAMERA, matched to e12_head_render exactly. Blender ORTHO, `sensor_fit = VERTICAL`, so
`ortho_scale` is the VERTICAL extent and the horizontal follows the resolution ratio. Camera
at `(cx + r sin th, cy - r cos th, cz)` with rotation `(90deg, 0, th)`, which looks along
`(-sin th, cos th, 0)` with right `(cos th, sin th, 0)` and up `(0, 0, 1)` — the same
construction silhouette_masks derives from turn_render, at a different centre and scale.

⚠ FRAME: this file works in the RAW Blender-import frame (the glTF remap `(x, -z, y)`, no
normalisation), because that is the frame `head_00003.json`'s boxes are stated in and the
frame Blender renders in. silhouette_masks normalises by `/vmax*0.5` for the whole-mesh case;
mixing the two would misregister the mask against the render by that factor.

  e12_crop_silhouette.py --glb m.glb --out mask.png --centre cx,cy,cz
                         --ortho-scale S --res-x N --res-y M [--yaw 0]

ANDON_AUTHORITY: raises if the silhouette is empty or fills the frame — the same bound
silhouette_masks asserts, for the same reason. NAMED_COMPENSATORS: writes one PNG.
EXTERNAL_VERIFIER: emits a mask and coverage numbers; grades nothing.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--centre", required=True, help="cx,cy,cz in the Blender-import frame")
ap.add_argument("--ortho-scale", type=float, required=True, help="VERTICAL extent")
ap.add_argument("--res-x", type=int, required=True)
ap.add_argument("--res-y", type=int, required=True)
ap.add_argument("--yaw", type=float, default=0.0)
ap.add_argument("--json", default=None)
args = ap.parse_args()

c = np.array([float(v) for v in args.centre.split(",")], dtype=np.float64)
m = trimesh.load(args.glb, force="mesh", process=False)
v0 = np.asarray(m.vertices, dtype=np.float64)
V = np.stack([v0[:, 0], -v0[:, 2], v0[:, 1]], axis=1)     # the Blender glTF import remap
F = np.asarray(m.faces, dtype=np.int64)
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(V.astype(np.float32)), o3d.core.Tensor(F.astype(np.uint32)))
print("[csil] mesh %d verts %d tris  bbox lo %s hi %s"
      % (len(V), len(F), np.round(V.min(0), 5).tolist(), np.round(V.max(0), 5).tolist()),
      flush=True)

W, H = args.res_x, args.res_y
v_ext = args.ortho_scale
h_ext = v_ext * (W / H)
th = np.radians(args.yaw)
rgt = np.array([np.cos(th), np.sin(th), 0.0])
look = np.array([-np.sin(th), np.cos(th), 0.0])
upv = np.array([0.0, 0.0, 1.0])
print("[csil] yaw %+.1f  centre %s  ortho_scale %.6f -> h_ext %.6f v_ext %.6f  frame %dx%d"
      % (args.yaw, np.round(c, 5).tolist(), args.ortho_scale, h_ext, v_ext, W, H), flush=True)

gx = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
gy = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
g1, g2 = np.meshgrid(gx, gy)
# start the rays well outside the mesh along -look, so nothing in front of the box is missed
back = float(np.abs(V).max()) * 4.0
o = (c[None, None, :] + g1[..., None] * rgt[None, None, :]
     + g2[..., None] * upv[None, None, :] - look[None, None, :] * back)
hit = np.isfinite(rs.cast_rays(o3d.core.Tensor(np.concatenate(
    [o, np.broadcast_to(look, o.shape)], axis=-1).reshape(-1, 6).astype(np.float32)
))["t_hit"].numpy().reshape(H, W))

pct = float(hit.mean() * 100)
if not (0.5 < pct < 99.5):
    raise AssertionError(
        "ANDON: silhouette is %.2f%% of frame - empty or runaway; the "
        "camera convention, the centre or the scale is wrong." % pct)
ys, xs = np.nonzero(hit)
bb = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
Image.fromarray((hit * 255).astype(np.uint8), mode="L").save(args.out)
print("[csil] %.3f%% of frame  %d px  bbox %dx%d at (%d,%d)  -> %s"
      % (pct, int(hit.sum()), bb[2] - bb[0] + 1, bb[3] - bb[1] + 1, bb[0], bb[1],
         os.path.basename(args.out)), flush=True)

if args.json:
    json.dump({"glb": os.path.abspath(args.glb), "centre": c.tolist(), "yaw": args.yaw,
               "ortho_scale": args.ortho_scale, "h_ext": h_ext, "v_ext": v_ext,
               "res": [W, H], "pct_of_frame": round(pct, 4), "px": int(hit.sum()),
               "bbox_xyxy": bb}, open(args.json, "w"), indent=1)
    print("[csil] wrote %s" % args.json)
