"""Project the 8 RESTYLIZED turnaround views back onto the mesh -> a finished GLB.

project_texture.py projects ONE image down +Z and covers ~15% of the atlas -- the front
shell. That is why the finished asset still carried the volume bake everywhere else. Eight
views at 45 deg cover the whole figure, and each one is already painted, so the atlas ends
up painted the whole way round instead of only where the concept camera could see.

CAMERA MODEL, derived not guessed. turn_render.py orbits an ORTHO camera about Blender +Z,
which is glTF +Y. For view i the camera axis is a = (sin t, 0, cos t), t = i*45 deg. Rotating
every position and normal about Y by -t maps a onto +Z, after which this is exactly the
single-view problem project_texture already solves -- so its projection, visibility, facing
and silhouette-IoU code is IMPORTED rather than reimplemented, and the two cannot drift.

    x' = x cos t - z sin t        y' = y        z' = x sin t + z cos t

The (cx, cy, side) seed is ANALYTIC, from the render settings themselves rather than from a
search: side = H_px / (y_extent * ortho_margin), cx = image centre, cy = image centre,
because the camera is centred on the bounding box. It is then refined against each view's
own silhouette and the achieved IoU is printed per view -- a view that fails to register is
reported, not silently smeared on.

Accumulation is a facing-weighted average across views, so a texel seen well by one camera
and edge-on by another takes the good one. Texels no view can see keep the existing atlas.

  project_multiview.py --glb <in.glb> --views <dir>/v{}.png --out <out.glb>
"""
import argparse
import math
import sys
from pathlib import Path

import numpy as np
import torch
import trimesh
import trimesh.visual
import cv2
from PIL import Image

sys.path.insert(0, r"E:/AI/sprite-foundry/3d-prerender")
import uv_rasterize                                                        # noqa: E402
from project_texture import (foreground_mask, project, silhouette_iou,     # noqa: E402
                             to_raster_rows)

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--views", required=True, help="format string, e.g. dir/v{}.png")
ap.add_argument("--out", required=True)
ap.add_argument("--n", type=int, default=8)
ap.add_argument("--ortho-margin", type=float, default=1.204,
                help="must match turn_render.py's ortho_scale multiplier")
ap.add_argument("--facing-min", type=float, default=0.15)
ap.add_argument("--facing-full", type=float, default=0.45)
ap.add_argument("--depth-tol", type=float, default=0.01)
ap.add_argument("--min-iou", type=float, default=0.80)
ap.add_argument("--blend-power", type=float, default=12.0,
                help="Exponent on the facing weight before normalising across views. "
                     "1.0 = a plain weighted average, which GHOSTS: a body-wide silhouette "
                     "fit leaves each view's FACE a few px off (measured elsewhere: body IoU "
                     "0.948 still put the eye 7 px low), the errors point different ways, and "
                     "averaging eight of them double-exposes the face. A high power is "
                     "effectively winner-take-all per texel, so each texel takes the ONE view "
                     "that saw it most squarely -- sharp, and it stops the colour regressing "
                     "to the mean across views.")
ap.add_argument("--head-views", default=None,
                help="comma-separated view indices allowed to paint the HEAD (body still "
                     "takes all views). Ignored when --keep-head 1. Use ONE view (e.g. '0') "
                     "when the restylized heads disagree on the hair boundary: with 8 views "
                     "the disagreement bakes hair colour onto the face. Requires "
                     "--keep-head 0.")
ap.add_argument("--keep-head", type=int, default=1,
                help="1 = leave head texels on the INCOMING atlas instead of repainting them "
                     "from the restylized views. Measured twice, once single-view and once "
                     "across eight: a restylized render moves facial features a few px, no "
                     "silhouette fit can see that (the CAP dominates the head outline, so head "
                     "IoU reads 0.96 while the face inside it is off), and projecting it back "
                     "ghosts the face. The incoming atlas carries the CONCEPT projection, and "
                     "the concept is what the mesh was generated from, so it is the one source "
                     "that registers by construction. Body and back still gain the 8-view paint.")
ap.add_argument("--debug-dir", default=None)
args = ap.parse_args()

head_views = None
if args.head_views:
    head_views = {int(v) for v in args.head_views.split(",")}
    if args.keep_head:
        raise SystemExit("--head-views requires --keep-head 0 (keep-head 1 already blocks "
                         "every view from the head)")
    print(f"[head] only view(s) {sorted(head_views)} may paint the head; "
          f"body takes all views", flush=True)

dev = "cuda" if torch.cuda.is_available() else "cpu"
scene = trimesh.load(args.glb)
mesh = scene.to_mesh() if isinstance(scene, trimesh.Scene) else scene
mat = mesh.visual.material
atlas_img = mat.baseColorTexture
atlas = to_raster_rows(np.asarray(atlas_img.convert("RGB")))
T = atlas.shape[0]

V = torch.as_tensor(np.asarray(mesh.vertices).copy(), dtype=torch.float32, device=dev)
F = torch.as_tensor(np.asarray(mesh.faces).copy(), dtype=torch.int64, device=dev)
UV = torch.as_tensor(np.asarray(mesh.visual.uv).copy(), dtype=torch.float32, device=dev)
N = torch.as_tensor(np.asarray(mesh.vertex_normals).copy(), dtype=torch.float32, device=dev)

rast = uv_rasterize.rasterize(UV, F, T)
covered = rast[0, ..., 3] > 0
pos0, _ = uv_rasterize.interpolate(V, rast, F)
nrm0, _ = uv_rasterize.interpolate(N, rast, F)
pos0 = pos0[0][covered]
nrm0 = nrm0[0][covered]
nrm0 = nrm0 / nrm0.norm(dim=-1, keepdim=True).clamp(min=1e-8)
n_tex = pos0.shape[0]
print(f"[glb ] {Path(args.glb).name}  atlas {T}x{T}  covered texels {n_tex:,} "
      f"({100*n_tex/(T*T):.1f}%)")

y_extent = float(pos0[:, 1].max() - pos0[:, 1].min())
acc = torch.zeros((n_tex, 3), device=dev)
acc_w = torch.zeros(n_tex, device=dev)
report = []

for i in range(args.n):
    t = math.radians(i * 45.0)
    ct, st = math.cos(t), math.sin(t)
    pos = torch.stack([pos0[:, 0] * ct - pos0[:, 2] * st,
                       pos0[:, 1],
                       pos0[:, 0] * st + pos0[:, 2] * ct], dim=-1)
    nrm = torch.stack([nrm0[:, 0] * ct - nrm0[:, 2] * st,
                       nrm0[:, 1],
                       nrm0[:, 0] * st + nrm0[:, 2] * ct], dim=-1)

    img = Image.open(args.views.format(i)).convert("RGB")
    cimg = np.asarray(img)
    ih, iw = cimg.shape[:2]
    fg_small, sc = foreground_mask(img)
    fg = np.asarray(Image.fromarray(fg_small.astype(np.uint8) * 255).resize(
        (iw, ih), Image.Resampling.NEAREST)) > 127
    fg_t = torch.as_tensor(fg, device=dev)

    # analytic seed from the render settings, then refine
    side = ih / (y_extent * args.ortho_margin)
    cx, cy = iw / 2.0, ih / 2.0
    front = pos[nrm[:, 2] > 0]
    best = (silhouette_iou(front, cx, cy, side, fg_t, iw, ih), cx, cy, side)
    seed_iou = best[0]
    for step in (0.02, 0.005, 0.00125):
        improved = True
        while improved:
            improved = False
            for ds in (0.0, -step, step):
                for dx in (0.0, -step, step):
                    for dy in (0.0, -step, step):
                        s2 = best[3] * (1 + ds)
                        c2x, c2y = best[1] + dx * best[3], best[2] + dy * best[3]
                        v = silhouette_iou(front, c2x, c2y, s2, fg_t, iw, ih)
                        if v > best[0] + 1e-6:
                            best = (v, c2x, c2y, s2); improved = True
    iou, cx, cy, side = best

    # ---- SECOND fit, on the HEAD ONLY ------------------------------------------------
    # A body-wide fit is dominated by the skirt and satisfies it at the face's expense:
    # measured on this subject, body IoU 0.948 still left the eye 7 px low, most of an eye.
    # Feeding a restylized view back makes it worse, because the repaint moves the head a
    # little too. Projecting the whole figure on one calibration is what ghosted the face.
    # So fit the head separately and use it for head texels only.
    uvh = project(front, cx, cy, side, iw, ih)
    top = float(uvh[:, 1].min())
    hb = (0, max(int(top) - 8, 0), iw, min(int(top + 0.20 * side), ih))
    hbest = (silhouette_iou(front, cx, cy, side, fg_t, iw, ih, box=hb), cx, cy, side)
    h_before = hbest[0]
    for step in (0.01, 0.0025, 0.000625):
        improved = True
        while improved:
            improved = False
            for ds in (0.0, -step, step):
                for dx in (0.0, -step, step):
                    for dy in (0.0, -step, step):
                        s2 = hbest[3] * (1 + ds)
                        c2x, c2y = hbest[1] + dx * hbest[3], hbest[2] + dy * hbest[3]
                        v = silhouette_iou(front, c2x, c2y, s2, fg_t, iw, ih, box=hb)
                        if v > hbest[0] + 1e-6:
                            hbest = (v, c2x, c2y, s2); improved = True
    h_iou, hcx, hcy, hside = hbest

    if iou < args.min_iou:
        raise SystemExit(f"CALIBRATION FAILED on view {i}: silhouette IoU {iou:.4f} < "
                         f"{args.min_iou}. Projecting would paint this view onto the wrong "
                         f"geometry. Check that the render and the restylize still line up.")

    # Blend the two calibrations by height so there is no step at the neck. HEAD_Y/BODY_Y
    # are in glTF units on this figure's own bounding box, not magic numbers.
    y = pos0[:, 1]
    y_lo, y_hi = float(y.min()), float(y.max())
    head_y = y_lo + 0.84 * (y_hi - y_lo)
    body_y = y_lo + 0.78 * (y_hi - y_lo)
    a = ((y - body_y) / (head_y - body_y)).clamp(0, 1)
    uvp = (1 - a)[:, None] * project(pos, cx, cy, side, iw, ih) \
        + a[:, None] * project(pos, hcx, hcy, hside, iw, ih)
    inb = ((uvp[:, 0] >= 0) & (uvp[:, 0] <= iw - 1) &
           (uvp[:, 1] >= 0) & (uvp[:, 1] <= ih - 1))
    gx = uvp[:, 0].long().clamp(0, iw - 1)
    gy = uvp[:, 1].long().clamp(0, ih - 1)
    flat = gy * iw + gx
    depth = torch.full((ih * iw,), -1e9, device=dev)
    depth.scatter_reduce_(0, flat[inb], pos[inb, 2], reduce="amax", include_self=True)
    visible = pos[:, 2] >= depth[flat] - args.depth_tol

    w = ((nrm[:, 2] - args.facing_min) / (args.facing_full - args.facing_min)).clamp(0, 1)
    w = w * w * (3 - 2 * w)
    w = w * inb.float() * visible.float() * fg_t.reshape(-1)[flat].float()

    src = torch.as_tensor(cimg, dtype=torch.float32, device=dev).permute(2, 0, 1)[None] / 255.
    grid = torch.stack([(uvp[:, 0] / (iw - 1)) * 2 - 1,
                        (uvp[:, 1] / (ih - 1)) * 2 - 1], dim=-1)[None, None]
    samp = torch.nn.functional.grid_sample(src, grid, mode="bilinear",
                                           padding_mode="border", align_corners=True)[0, :, 0].permute(1, 0)

    # Gate on w (visibility / silhouette / not-edge-on), then weight by facing^p so the
    # squarest view wins outright instead of being averaged with worse-registered ones.
    wp = (w > 1e-3).float() * nrm[:, 2].clamp(min=0) ** args.blend_power
    if args.keep_head:
        # a is 1 on the head, 0 on the body, ramped across the neck -- reuse it to fade the
        # 8-view paint OUT exactly where the incoming atlas is the better-registered source.
        wp = wp * (1.0 - a)
    elif head_views is not None and i not in head_views:
        # Same fade, applied PER VIEW. Restylized views each invent their own hair boundary,
        # which does not match the mesh's hair geometry -- measured 2026-08-02, head IoU
        # 0.78-0.93 against body IoU 0.91-0.94. Accumulating them lands hair-coloured pixels
        # on surface that is FACE, which reads as a dark smear across the cheek/temple. One
        # view alone has no one to disagree with, so the face stays sharp and registered.
        wp = wp * (1.0 - a)
    acc += wp[:, None] * samp
    acc_w += wp
    report.append((i, seed_iou, iou, 100 * (w > 0.5).float().mean().item()))
    print(f"[view] {i}  body IoU {iou:.4f}   head IoU {h_before:.4f} -> {h_iou:.4f}   "
          f"covers {100*(w > 0.5).float().mean():.1f}% of atlas", flush=True)

hit = acc_w > 1e-3
print(f"\n[cov ] texels painted by >=1 view: {100*hit.float().mean():.1f}%   "
      f"(single front view was ~15%)")
print(f"[cov ] texels still on the volume bake: {100*(~hit).float().mean():.1f}%")

old = torch.as_tensor(atlas, dtype=torch.float32, device=dev).reshape(-1, 3)
cov_flat = covered.reshape(-1)
base = old[cov_flat] / 255.0
new = base.clone()
new[hit] = acc[hit] / acc_w[hit][:, None]
old[cov_flat] = (new * 255.0).clamp(0, 255)
out_atlas = old.reshape(T, T, 3).to(torch.uint8).cpu().numpy()
out_atlas = cv2.inpaint(out_atlas, (~covered).cpu().numpy().astype(np.uint8), 3, cv2.INPAINT_TELEA)
out_atlas = to_raster_rows(out_atlas)

src_rgba = np.asarray(atlas_img)
out_img = (Image.fromarray(np.dstack([out_atlas, src_rgba[..., 3]]), mode="RGBA")
           if atlas_img.mode == "RGBA" else Image.fromarray(out_atlas, mode="RGB"))
new_mat = mat.copy()
new_mat.baseColorTexture = out_img
mesh.visual = trimesh.visual.TextureVisuals(uv=mesh.visual.uv, material=new_mat)
Path(args.out).parent.mkdir(parents=True, exist_ok=True)
mesh.export(args.out)
print(f"[out ] {args.out} ({Path(args.out).stat().st_size/1e6:.1f} MB)")

if args.debug_dir:
    dd = Path(args.debug_dir); dd.mkdir(parents=True, exist_ok=True)
    Image.fromarray(out_atlas).save(dd / "atlas_multiview.png")
    wm = torch.zeros(T * T, device=dev); wm[cov_flat] = acc_w.clamp(0, 1)
    Image.fromarray(to_raster_rows((wm.reshape(T, T).cpu().numpy() * 255).astype(np.uint8))
                    ).save(dd / "atlas_coverage.png")
    print(f"[dbg ] wrote {dd}/atlas_multiview.png, atlas_coverage.png")
