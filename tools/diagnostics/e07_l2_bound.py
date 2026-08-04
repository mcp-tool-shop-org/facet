"""E07 L2 — the offline bound, before any GPU is spent.

texel_provenance.py already replays texpass_iter.commit's filter chain exactly from the
saved job directories. This does the same, but writes COLOUR rather than a claim label,
and optionally applies the §7 view-space seam levelling to each brush output first. The
result is a counterfactual atlas: levelled, but using the ORIGINAL brush outputs.

This is a BOUND, not a result. A true L2 rerun changes each stroke's context and therefore
what the brush paints. But if the counterfactual does not move the step ratio, either the
implementation is wrong or the premise is, and the GPU should not be spent.

The levelling, per §7:
  1. depth (t_hit) is recomputed offline by recasting emit's own rays from cam.json —
     emit never saved it, and it is needed for step 4.
  2. the ring just OUTSIDE the job mask (render.png — the colour already on the surface)
     is paired with the ring just INSIDE it (inpainted.png — the brush's own level);
     diff = outside - inside on that contour.
  3. a correction field O is solved over the masked region: O = diff on the contour,
     grad^2 O = 0 inside, by Jacobi iteration. This is the membrane form of Poisson seam
     levelling, in the space where adjacency IS surface adjacency.
  4. the membrane may not cross a depth discontinuity and may not leave `hit` — without
     that an arm's correction leaks onto the chest behind it.
  5. corrected = inpainted + O, then sampled as now.
  6. |O| is capped. A correction beyond ~0.15 is not a seam, it is a disagreement, and
     levelling it smears a wrong colour instead of revealing it. The share of each mask
     that hits the cap is reported per stroke — a stroke needing a large correction is a
     stroke that invented, which is worth knowing on its own.

  e07_l2_bound.py --prep DIR --state DIR --stage1 s1.png --order k1,k2,... --out DIR
                  [--no-level]   (--no-level reproduces the shipped atlas, as a check)
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import (binary_dilation, distance_transform_edt, minimum_filter)

Image.MAX_IMAGE_PIXELS = None
ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--state", required=True)
ap.add_argument("--stage1", required=True)
ap.add_argument("--order", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--no-level", action="store_true", help="replay unchanged, as a fidelity check")
ap.add_argument("--cap", type=float, default=0.15)
ap.add_argument("--depth-tol", type=float, default=0.02,
                help="membrane may not cross a depth jump larger than this (std frame)")
ap.add_argument("--iters", type=int, default=400)
ap.add_argument("--facing-min", type=float, default=0.25)
ap.add_argument("--edge-dist", type=float, default=4.0)
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
args = ap.parse_args()
D = 2.0
os.makedirs(args.out, exist_ok=True)

meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
valid = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
base = os.path.splitext(args.stage1)[0]
atlas = np.asarray(Image.open(args.stage1).convert("RGB"), dtype=np.float32) / 255.0
holes = np.asarray(Image.open(base + "_holes.png").convert("L"),
                   dtype=np.float32) / 255.0 > 0.5
styled = np.load(base + "_styled_mask.npy").copy()
pos_e = np.load(os.path.join(args.prep, "pos.npy"))
nor_e = np.load(os.path.join(args.prep, "nor.npy"))
lo = np.array(meta["lo"]); hi = np.array(meta["hi"])

m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
vz = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(vz.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))


def basis(yaw_d, el_d):
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    look = -cd / np.linalg.norm(cd)
    right = np.cross(look, [0.0, 0.0, 1.0])
    right /= np.linalg.norm(right) + 1e-12
    up = np.cross(right, look)
    return look, right, up / (np.linalg.norm(up) + 1e-12)


def bilin(img, x, y):
    Hh, Ww = img.shape[:2]
    x = np.clip(x, 0.0, Ww - 1.001); y = np.clip(y, 0.0, Hh - 1.001)
    x0, y0 = x.astype(np.int64), y.astype(np.int64)
    fx, fy = x - x0, y - y0
    if img.ndim == 3:
        fx, fy = fx[:, None], fy[:, None]
    return (img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy)
            + img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy)


def depth_of(cam, look, right, up):
    """emit's own rays, recast. emit never saved t_hit; §7 step 4 needs it."""
    W, H = int(cam["W"]), int(cam["H"])
    bmid = np.array(cam["bmid"])
    xs = (np.arange(W) + 0.5) / W * cam["h_ext"] - cam["h_ext"] / 2
    ys = cam["v_ext"] / 2 - (np.arange(H) + 0.5) / H * cam["v_ext"]
    gx, gy = np.meshgrid(xs, ys)
    org = (bmid[None, None, :] + gx[..., None] * right[None, None, :]
           + gy[..., None] * up[None, None, :] - look[None, None, :] * D)
    ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
    t = ans["t_hit"].numpy().reshape(H, W)
    return t, np.isfinite(t)


DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def level(render, inpainted, jm, hit, depth):
    """§7 steps 2-6. Returns corrected image and per-stroke stats."""
    dom = (jm > 0.5) & hit
    st = {"mask_px": int(dom.sum())}
    if not dom.any():
        return inpainted, st
    dep = np.where(hit, depth, np.inf)
    # neighbour is usable if on the figure and not across a depth jump
    nb_ok, nb_dom, nb_out = [], [], []
    for dy, dx in DIRS:
        okd = np.roll(hit, (dy, dx), axis=(0, 1)) & \
            (np.abs(np.roll(dep, (dy, dx), axis=(0, 1)) - dep) < args.depth_tol)
        nb_ok.append(okd)
        nb_dom.append(np.roll(dom, (dy, dx), axis=(0, 1)) & okd)
        nb_out.append((~np.roll(dom, (dy, dx), axis=(0, 1))) & okd)
    # Dirichlet band: masked pixels touching un-masked figure across a continuous surface
    acc = np.zeros(render.shape, np.float64)
    cnt = np.zeros(render.shape[:2], np.float64)
    for k, (dy, dx) in enumerate(DIRS):
        w = nb_out[k] & dom
        acc += np.roll(render, (dy, dx), axis=(0, 1)) * w[..., None]
        cnt += w
    bnd = dom & (cnt > 0)
    O = np.zeros(render.shape, np.float64)
    with np.errstate(invalid="ignore", divide="ignore"):
        O[bnd] = acc[bnd] / cnt[bnd][..., None] - inpainted[bnd]
    O = np.clip(O, -args.cap, args.cap)
    st["boundary_px"] = int(bnd.sum())
    interior = dom & ~bnd
    for _ in range(args.iters):
        a2 = np.zeros(render.shape, np.float64)
        c2 = np.zeros(render.shape[:2], np.float64)
        for k, (dy, dx) in enumerate(DIRS):
            w = nb_dom[k]
            a2 += np.roll(O, (dy, dx), axis=(0, 1)) * w[..., None]
            c2 += w
        upd = np.zeros_like(O)
        nz = c2 > 0
        upd[nz] = a2[nz] / c2[nz][..., None]
        O = np.where(interior[..., None], upd, O)
    hitcap = dom & (np.abs(O).max(-1) >= args.cap - 1e-6)
    st["cap_hit_pct"] = round(float(hitcap.sum() / max(int(dom.sum()), 1) * 100), 2)
    st["O_lum_median"] = round(float(np.median(np.abs(O[dom].mean(-1)))), 5)
    st["O_lum_p95"] = round(float(np.percentile(np.abs(O[dom].mean(-1)), 95)), 5)
    corr = inpainted.copy()
    corr[dom] = np.clip(inpainted[dom] + O[dom], 0.0, 1.0)
    return corr.astype(np.float32), st


order = [k.strip() for k in args.order.split(",") if k.strip()]
report = {"levelled": not args.no_level, "cap": args.cap, "depth_tol": args.depth_tol,
          "iters": args.iters, "strokes": {}}
print(f"[l2] replaying {len(order)} commits "
      f"({'UNCHANGED (fidelity check)' if args.no_level else 'WITH view-space levelling'})",
      flush=True)
mask_np = valid
# same encoding texel_provenance uses: 0 = twins, 1..N = the stroke, 255 = dilation.
# Levelling can shift a pixel across the edge-distance guard's figure threshold, so the
# counterfactual's claim map is recomputed rather than borrowed from C1.
claim = np.full(RES * RES, 255, dtype=np.uint8)
claim[np.where(styled.reshape(-1))[0]] = 0
for si, keyname in enumerate(order, start=1):
    J = os.path.join(args.state, "job_" + keyname)
    cam = json.load(open(os.path.join(J, "cam.json")))
    edited = np.asarray(Image.open(os.path.join(J, "inpainted.png")).convert("RGB"),
                        dtype=np.float32) / 255
    render = np.asarray(Image.open(os.path.join(J, "render.png")).convert("RGB"),
                        dtype=np.float32) / 255
    jobmask = np.asarray(Image.open(os.path.join(J, "mask.png")).convert("L"),
                         dtype=np.float32) / 255
    look, right, up = basis(cam["yaw"], cam["el"])
    st = {}
    if not args.no_level:
        depth, hit = depth_of(cam, look, right, up)
        edited, st = level(render, edited, jobmask, hit, depth)

    hidx = np.where(holes.reshape(-1) & mask_np.reshape(-1))[0]
    P = (pos_e.reshape(-1, 3)[hidx].astype(np.float64) * (hi - lo) + lo) / meta["maxabs"] * 0.5
    N = nor_e.reshape(-1, 3)[hidx].astype(np.float64) * 2.0 - 1.0
    N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
    dtc = -look
    keep = (N @ dtc) > args.facing_min
    hidx, P, N = hidx[keep], P[keep], N[keep]
    org = (P + N * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
    t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(dtc.astype(np.float32), org.shape)], axis=1)))["t_hit"].numpy()
    vis = ~np.isfinite(t)
    hidx, P = hidx[vis], P[vis]
    bmid = np.array(cam["bmid"])
    px = ((P - bmid) @ right / cam["h_ext"] + 0.5) * cam["W"] - 0.5
    py = (0.5 - (P - bmid) @ up / cam["v_ext"]) * cam["H"] - 0.5
    inj = bilin(jobmask, px, py) > 0.5
    hidx, px, py = hidx[inj], px[inj], py[inj]
    c8 = np.concatenate([edited[:8, :8].reshape(-1, 3), edited[:8, -8:].reshape(-1, 3)])
    bg = np.median(c8, axis=0)
    fm = minimum_filter((np.abs(edited - bg).max(axis=-1) > 0.06).astype(np.float32), size=5)
    ok = bilin(distance_transform_edt(fm > 0.5).astype(np.float32), px, py) >= args.edge_dist
    hidx, px, py = hidx[ok], px[ok], py[ok]
    col = bilin(edited, px, py).astype(np.float32)

    a2 = atlas.reshape(-1, 3).copy()
    a2[hidx] = col
    # the live loop round-trips the atlas through an 8-bit PNG once per stroke; the
    # replay must too, or it drifts from the thing it is a counterfactual of
    atlas = (np.clip(a2.reshape(RES, RES, 3), 0, 1) * 255).round().astype(np.uint8) \
        .astype(np.float32) / 255.0
    h2 = holes.reshape(-1).copy(); h2[hidx] = False
    holes = h2.reshape(RES, RES)
    s2 = styled.reshape(-1).copy(); s2[hidx] = True
    styled = s2.reshape(RES, RES)
    claim[hidx] = si
    st["claimed"] = int(len(hidx))
    report["strokes"][keyname] = st
    print(f"[l2] stroke {si} {keyname}: claimed {len(hidx):,}"
          + ("" if args.no_level else
             f"   |O| lum median {st['O_lum_median']:.4f} p95 {st['O_lum_p95']:.4f}"
             f"   cap hit {st['cap_hit_pct']:.2f}%"), flush=True)

Image.fromarray((atlas * 255).round().astype(np.uint8)).save(
    os.path.join(args.out, "atlas.png"))
Image.fromarray((holes * 255).astype(np.uint8)).save(os.path.join(args.out, "holes.png"))
np.save(os.path.join(args.out, "styled_mask.npy"), styled)
np.save(os.path.join(args.out, "claim.npy"), claim.reshape(RES, RES))
report["holes_left"] = int((holes & valid).sum())
json.dump(report, open(os.path.join(args.out, "l2_bound.json"), "w"), indent=1)
print(f"[l2] holes left {int((holes & valid).sum()):,}; wrote {args.out}", flush=True)
