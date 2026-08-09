"""E13 A2 — the texel-allocation arithmetic, and the two frame checks it rides beside.

THE UNIT (pre-registered, handoff-13 predictions blob d2b102fa): **atlas texels per
crop-twin pixel, over the SAME PATCH OF SURFACE.**

  numerator   valid atlas texels whose 3-D position lies inside the measured head box
              AND which are first-hit visible from the camera in question
  denominator frame pixels whose first hit lies inside that same box

Both sides measure one physical patch, so neither can be moved by reframing alone — which is
the property CLAUDE.md's pass-condition law asks for. The ratio is dimensionless: below 1.0
the atlas under-resolves the paint, above 1.0 it over-resolves it. The SAME arithmetic runs
against the route's full-figure frame, because that comparison is what says whether the mush
is an allocation problem or a generation-frame problem.

Standards compliance:
  PIN_PER_STEP — every frame is printed with its derivation; the head box arrives from
    head_00003.json by path, never retyped; the std-frame convention is ASSERTED against the
    prep meta rather than assumed.
  ANDON_AUTHORITY — raises on a std-frame disagreement, since every number below would be
    measured against the wrong object if that convention were wrong.
  NAMED_COMPENSATORS — writes one JSON under --out. Undo = delete it. Nothing is modified.
  EXTERNAL_VERIFIER — it measures; it decides nothing. The registered rule and the Director
    decide.

  e13_a2_allocation.py --prep DIR --headbox head_00003.json --out a2.json
                       [--pad 1.12] [--crop-res 1360] [--yaws 0,45]
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
ap.add_argument("--headbox", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--pad", type=float, default=1.12,
                help="Gate 0's own head-crop padding, inherited not invented")
ap.add_argument("--crop-res", type=int, default=1360)
ap.add_argument("--yaws", default="0,45")
ap.add_argument("--route-aspect", default="1792,1024")
ap.add_argument("--route-margin", type=float, default=1.204)
ap.add_argument("--facing-min", type=float, default=0.45)
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--mask", action="append", default=[], metavar="IDX=PATH",
                help="silhouette_masks output for view IDX — the RENDER frame's ground "
                     "truth, used only for the frame-agreement check")
args = ap.parse_args()

AW, AH = [float(x) for x in args.route_aspect.split(",")]

meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
lo = np.array(meta["lo"], dtype=np.float64)
hi = np.array(meta["hi"], dtype=np.float64)
maxabs = float(meta["maxabs"])
pos_e = np.load(os.path.join(args.prep, "pos.npy"))
mask = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
valid = mask.reshape(-1)
# BLENDER-frame positions: exactly what head_box_blender is expressed in.
P_bl = pos_e.reshape(-1, 3)[valid].astype(np.float64) * (hi - lo) + lo
# STD frame, project_twins' convention.
P = P_bl / maxabs * 0.5
NV = P.shape[0]

hb = json.load(open(args.headbox))
bl, bh = [np.array(v, dtype=np.float64) for v in hb["head_box_blender"]]
d = bh - bl
c_bl = (bl + bh) / 2
c_std = c_bl / maxabs * 0.5

# ---- the mesh, in project_twins' std frame, and the convention ASSERTED ----
m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
vmax = np.abs(v).max()
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / vmax * 0.5
if not (abs(vmax - maxabs) < 1e-9):
    raise AssertionError(
        f"ANDON: prep_uv.glb |v|max {vmax:.9f} against meta maxabs {maxabs:.9f} — the std "
        f"frame is not the one the bake recorded, so every box test below is against the "
        f"wrong object")
blo, bhi = v.min(axis=0), v.max(axis=0)
_exp_lo, _exp_hi = lo / maxabs * 0.5, hi / maxabs * 0.5
if not (np.abs(blo - _exp_lo).max() < 1e-6 and np.abs(bhi - _exp_hi).max() < 1e-6):
    raise AssertionError(
        f"ANDON: std-frame bbox {blo.tolist()}..{bhi.tolist()} disagrees with the bake's "
        f"{_exp_lo.tolist()}..{_exp_hi.tolist()} — the axis convention is not what "
        f"project_twins assumes")
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))

N_e = np.load(os.path.join(args.prep, "nor.npy"))
N = N_e.reshape(-1, 3)[valid].astype(np.float64) * 2.0 - 1.0
N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12

in_box = ((P_bl >= bl).all(axis=1) & (P_bl <= bh).all(axis=1))
print(f"[a2] valid texels {NV:,}   inside the measured head box "
      f"{int(in_box.sum()):,} ({in_box.mean()*100:.3f}%)", flush=True)


def cam_axes(deg):
    """project_twins' own, snap included — copied so this instrument does not import a
    tool it is checking."""
    th = np.radians(deg)

    def snap(a):
        out = []
        for x in a:
            if abs(x) < 1e-12:
                out.append(0.0)
            elif abs(x - 1) < 1e-12:
                out.append(1.0)
            elif abs(x + 1) < 1e-12:
                out.append(-1.0)
            else:
                out.append(float(x))
        return np.array(out, dtype=np.float64)
    return snap([np.sin(th), -np.cos(th), 0.0]), snap([np.cos(th), np.sin(th), 0.0])


UP = np.array([0.0, 0.0, 1.0])


def visible(dtc):
    """First-hit visible from this direction — project_twins' own test, same epsilons."""
    facing = (N @ dtc).astype(np.float32)
    idx = np.where(facing > args.facing_min)[0]
    o = (P[idx] + N[idx] * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
    dirs = np.broadcast_to(dtc.astype(np.float32), o.shape)
    t = rs.cast_rays(o3d.core.Tensor(np.concatenate([o, dirs], axis=1)))["t_hit"].numpy()
    out = np.zeros(NV, dtype=bool)
    out[idx[~np.isfinite(t)]] = True
    return out


def frame_hits(cen, v_ext, h_ext, W, H, dtc, rgt):
    """Raycast a frame; return (hit mask HxW, hit points)."""
    look = -dtc
    upv = np.cross(rgt, look)
    upv /= np.linalg.norm(upv) + 1e-12
    gx = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
    gy = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
    g1, g2 = np.meshgrid(gx, gy)
    o = (cen[None, None, :] + g1[..., None] * rgt[None, None, :]
         + g2[..., None] * upv[None, None, :] - look[None, None, :] * 2.0)
    rays = np.concatenate([o, np.broadcast_to(look, o.shape)], axis=-1)
    t = rs.cast_rays(o3d.core.Tensor(rays.reshape(-1, 6).astype(np.float32)))["t_hit"] \
        .numpy().reshape(H, W)
    fin = np.isfinite(t)
    pts = o + look[None, None, :] * np.where(fin, t, 0.0)[..., None]
    return fin, pts


def hits_in_box(fin, pts):
    p = pts * (maxabs / 0.5)                 # std -> Blender, the box's own frame
    ib = ((p >= bl).all(axis=-1) & (p <= bh).all(axis=-1)) & fin
    return ib


# ---- the two frames ----
span_bl = max(float(np.hypot(d[0], d[1])), float(d[2])) * args.pad   # e12_head_render's rule
crop_v_std = span_bl / maxabs * 0.5                                  # sensor_fit VERTICAL
route_h_std = float(max(bhi[0] - blo[0], bhi[1] - blo[1])) * args.route_margin
route_v_std = route_h_std * (AH / AW)
pt_v_std = float(bhi[2] - blo[2]) * args.route_margin                # project_twins' :229
pt_h_std = pt_v_std * (AW / AH)
bmid = (blo + bhi) / 2

print(f"[a2] CROP frame: yaw-invariant span {span_bl:.6f} blender "
      f"(hypot({d[0]:.5f},{d[1]:.5f}) x pad {args.pad}) = {crop_v_std:.6f} std, "
      f"{args.crop_res}x{args.crop_res}", flush=True)
print(f"[a2] ROUTE frame (turn_render --fit-axis width): h_ext {route_h_std:.6f} "
      f"v_ext {route_v_std:.6f} std at {int(AW)}x{int(AH)}", flush=True)
print(f"[a2] project_twins' DERIVED frame (:229, height-fit, margin hardcoded): "
      f"h_ext {pt_h_std:.6f} v_ext {pt_v_std:.6f}  -> ratio to the route frame "
      f"{pt_h_std/route_h_std:.6f}", flush=True)

out = {
    "_what": "E13 A2 texel-allocation arithmetic. Unit: atlas texels per frame pixel over "
             "the same patch of head-box surface. Pre-registered before the number existed "
             "(handoff-13 predictions, git blob d2b102fa).",
    "prep": os.path.abspath(args.prep),
    "headbox": os.path.abspath(args.headbox),
    "valid_texels": int(NV),
    "texels_in_head_box": int(in_box.sum()),
    "frames": {
        "crop": {"span_blender": span_bl, "v_ext_std": crop_v_std,
                 "h_ext_std": crop_v_std, "res": [args.crop_res, args.crop_res],
                 "centre_std": c_std.tolist(), "centre_blender": c_bl.tolist(),
                 "pad": args.pad,
                 "derivation": "e12_head_render.py: span = max(hypot(dx,dy), dz) * pad, "
                               "sensor_fit VERTICAL, square frame"},
        "route": {"h_ext_std": route_h_std, "v_ext_std": route_v_std,
                  "res": [int(AW), int(AH)], "centre_std": bmid.tolist(),
                  "margin": args.route_margin,
                  "derivation": "turn_render.py:113 --fit-axis width: "
                                "ortho_scale = max(size.x,size.y) * margin"},
        "project_twins_derived": {
            "h_ext_std": pt_h_std, "v_ext_std": pt_v_std,
            "ratio_to_route_h": pt_h_std / route_h_std,
            "derivation": "project_twins.py:229 v_ext = bbox_z * 1.204 (height-fit, margin "
                          "hardcoded, no --fit-axis flag exists)"},
    },
    "views": {},
}

for yaw in [float(x) for x in args.yaws.split(",")]:
    dtc, rgt = cam_axes(yaw)
    vis = visible(dtc)
    n_head_vis = int((vis & in_box).sum())

    fin_c, pts_c = frame_hits(c_std, crop_v_std, crop_v_std,
                              args.crop_res, args.crop_res, dtc, rgt)
    ibx_c = hits_in_box(fin_c, pts_c)
    px_c = int(ibx_c.sum())

    fin_r, pts_r = frame_hits(bmid, route_v_std, route_h_std,
                              int(AW), int(AH), dtc, rgt)
    ibx_r = hits_in_box(fin_r, pts_r)
    px_r = int(ibx_r.sum())

    r_crop = n_head_vis / max(px_c, 1)
    r_route = n_head_vis / max(px_r, 1)
    print(f"[a2] yaw {yaw:+.0f}: head texels first-hit visible {n_head_vis:,}", flush=True)
    print(f"[a2]   CROP  {px_c:,} px land on head-box surface "
          f"({ibx_c.mean()*100:.2f}% of frame)  ->  texels/px = {r_crop:.4f}", flush=True)
    print(f"[a2]   ROUTE {px_r:,} px land on head-box surface "
          f"({ibx_r.mean()*100:.2f}% of frame)  ->  texels/px = {r_route:.4f}", flush=True)
    print(f"[a2]   crop/route pixel gain {px_c/max(px_r,1):.2f}x area, "
          f"{np.sqrt(px_c/max(px_r,1)):.2f}x linear", flush=True)
    out["views"][f"y{int(yaw)}"] = {
        "yaw": yaw,
        "head_texels_first_hit_visible": n_head_vis,
        "crop_px_on_head": px_c,
        "route_px_on_head": px_r,
        "texels_per_crop_px": r_crop,
        "texels_per_route_px": r_route,
        "crop_over_route_px": px_c / max(px_r, 1),
        "crop_frame_fraction_on_head": float(ibx_c.mean()),
        "crop_frame_fraction_any_hit": float(fin_c.mean()),
    }

# ---- the frame-agreement check (P4c), against silhouette_masks' recorded output ----
for spec in args.mask:
    k, _, p = spec.partition("=")
    i = int(k)
    yaw = i * 45.0
    dtc, rgt = cam_axes(yaw)
    ref = np.asarray(Image.open(p).convert("L"), dtype=np.uint8) > 127
    H, W = ref.shape
    fin_route, _ = frame_hits(bmid, route_v_std, route_h_std, W, H, dtc, rgt)
    fin_pt, _ = frame_hits(bmid, pt_v_std, pt_h_std, W, H, dtc, rgt)

    def _bb(msk):
        ys, xs = np.where(msk)
        return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]

    def _iou(a, b_):
        return float((a & b_).sum() / max((a | b_).sum(), 1))
    print(f"[a2] frame check view {i} (yaw {yaw:+.0f}) against {os.path.basename(p)}:",
          flush=True)
    print(f"[a2]   recorded mask   bbox {_bb(ref)}  {int(ref.sum()):,} px", flush=True)
    print(f"[a2]   route frame     bbox {_bb(fin_route)}  {int(fin_route.sum()):,} px  "
          f"IoU {_iou(ref, fin_route):.6f}", flush=True)
    print(f"[a2]   project_twins   bbox {_bb(fin_pt)}  {int(fin_pt.sum()):,} px  "
          f"IoU {_iou(ref, fin_pt):.6f}", flush=True)
    out.setdefault("frame_check", {})[f"view{i}"] = {
        "mask_path": os.path.abspath(p),
        "recorded": {"bbox": _bb(ref), "px": int(ref.sum())},
        "route_frame": {"bbox": _bb(fin_route), "px": int(fin_route.sum()),
                        "iou_vs_recorded": _iou(ref, fin_route)},
        "project_twins_frame": {"bbox": _bb(fin_pt), "px": int(fin_pt.sum()),
                                "iou_vs_recorded": _iou(ref, fin_pt)},
    }

os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
json.dump(out, open(args.out, "w"), indent=1)
print(f"[a2] wrote {args.out} — DONE (this tool decides nothing)", flush=True)
