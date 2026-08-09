"""The `thin_extent` cost curve, measured on THIS mesh, with a region fraction beside it.

WHAT `thin_extent` ACTUALLY IS, because the curve is meaningless if this is wrong. It is not
a mesh property and not a thickness in the abstract: `texpass_iter.emit` fires the emit grid
twice - forward from the near plane and backward from the far plane - and forms
`ext = 2D - tF - tB` per PIXEL, the front-to-back extent of the object along that view ray.
Anything with `ext < thin_extent` is removed from the hole mask and takes projected/dilated
colour instead of diffusion. So the quantity is **per view, in screen space, in canonical
units**, and this file reproduces that computation exactly - same canonicalisation
(`(x,-z,y)/vmax*0.5`), same `D = 2.0`, same `basis()`, same fit-axis block, same grid - so a
value read off this curve means the same thing when `texpass_iter` receives it.

WHY THE REGION FRACTION CANNOT BE A THICKNESS CRITERION. The dispatch asks what fraction of
the MEMBRANE FIELDS a candidate withholds. Selecting the membranes by thinness and then
measuring how much of them is thin is circular and would report ~100% at every value. The
region is therefore **spatial**: an axis-aligned canonical-frame box derived from two pixel
rectangles read by eye on two orthogonal emit views, exactly as E12's head box was, and drawn
back onto every view so it can be checked rather than trusted.

STATE THE REGION'S KNOWN IMPURITY. A box around a wing contains the wing ARM and FINGER
STRUTS, which are thick rods, as well as the membrane sheet. Their presence can only push the
withheld fraction DOWN, so the region number is a conservative floor on what the membrane
proper loses - never an overstatement.

0.0 IS A CURVE POINT, not an absent one. The tool's own default is 0.0, so an undecided
profile runs the guard DISABLED; showing that row is showing what undecided actually does.

  e12_thin_curve.py --glb prep_uv.glb --aspect 1792,1024 --fit-axis width
                    [--views 0,45,90,135,180,225,270,315] [--values 0,0.001,...]
                    [--region-a VIEW:x0,y0,x1,y1 --region-b VIEW:x0,y0,x1,y1]
                    [--preview DIR] [--out j.json]

Standards compliance: PIN_PER_STEP - every framing operand is a flag and lands in the JSON.
ANDON_AUTHORITY - raises if the two region views are not orthogonal or disagree in z beyond
tolerance. EXTERNAL_VERIFIER - emits a curve; adopts nothing. The region overlay exists so a
human checks the region rather than believing this file about it.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh

D = 2.0

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--aspect", default="1792,1024")
ap.add_argument("--margin", type=float, default=1.204)
ap.add_argument("--fit-axis", default="width", choices=["height", "width"])
ap.add_argument("--views", default="0,45,90,135,180,225,270,315")
ap.add_argument("--el", type=float, default=0.0)
ap.add_argument("--values", default="0,0.0005,0.001,0.002,0.003,0.005,0.0075,0.01,0.015,0.02,0.03,0.05")
ap.add_argument("--region-a", default=None, help="VIEW:x0,y0,x1,y1 - pixel rect on that view")
ap.add_argument("--region-b", default=None, help="VIEW:x0,y0,x1,y1 - an orthogonal view")
ap.add_argument("--region-name", default="wing")
ap.add_argument("--z-tol", type=float, default=0.06)
ap.add_argument("--preview", default=None, help="dir for per-view hit/ext previews + overlay")
ap.add_argument("--out", default=None)
args = ap.parse_args()

W, H = (int(x) for x in args.aspect.split(","))
VIEWS = [float(v) for v in args.views.split(",")]
VALUES = [float(v) for v in args.values.split(",")]

m = trimesh.load(args.glb, force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
vmax = np.abs(v).max()
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / vmax * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)), o3d.core.Tensor(f.astype(np.uint32)))
blo, bhi = v.min(axis=0), v.max(axis=0)
bmid = (blo + bhi) / 2

if args.fit_axis == "height":
    v_ext = (bhi[2] - blo[2]) * args.margin
    h_ext = v_ext * (W / H)
else:
    h_ext = max(bhi[0] - blo[0], bhi[1] - blo[1]) * args.margin
    v_ext = h_ext * (H / W)
one_px = v_ext / H
print("[thin] canonical extent %s | h_ext %.6f v_ext %.6f | one emit px %.6e"
      % ([round(float(x), 5) for x in (bhi - blo)], h_ext, v_ext, one_px), flush=True)
print("[thin] values are in CANONICAL units; %g = %.1f emit px, %g = %.1f emit px"
      % (0.01, 0.01 / one_px, 0.03, 0.03 / one_px), flush=True)


def basis(yaw_d, el_d):
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    look = -cd / np.linalg.norm(cd)
    right = np.cross(look, [0.0, 0.0, 1.0])
    right /= np.linalg.norm(right) + 1e-12
    up = np.cross(right, look)
    return look, right, up / (np.linalg.norm(up) + 1e-12)


xs_ = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
ys_ = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
gx, gy = np.meshgrid(xs_, ys_)


def cast(yaw):
    look, right, up = basis(yaw, args.el)
    o = (bmid[None, None, :] + gx[..., None] * right[None, None, :]
         + gy[..., None] * up[None, None, :] - look[None, None, :] * D)
    aF = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [o, np.broadcast_to(look, o.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
    tF = aF["t_hit"].numpy().reshape(H, W).astype(np.float64)
    aB = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [o + look[None, None, :] * (2 * D), np.broadcast_to(-look, o.shape)],
        axis=-1).reshape(-1, 6).astype(np.float32)))
    tB = aB["t_hit"].numpy().reshape(H, W).astype(np.float64)
    hit = np.isfinite(tF)
    both = hit & np.isfinite(tB)
    ext = np.full((H, W), np.inf)
    ext[both] = 2 * D - tF[both] - tB[both]
    return hit, ext, (look, right, up)


# --- the spatial region, if one was given -------------------------------------------
box = None
if args.region_a or args.region_b:
    if not (args.region_a and args.region_b):
        raise AssertionError("ANDON: --region-a and --region-b come as a pair")

    def parse(spec):
        vw, _, rect = spec.partition(":")
        x0, y0, x1, y1 = [float(t) for t in rect.split(",")]
        yaw = float(vw)
        _, right, up = basis(yaw, args.el)
        ax = [i for i in (0, 1) if abs(abs(right[i]) - 1.0) < 1e-9]
        if not (ax and abs(up[2] - 1.0) < 1e-9):
            raise AssertionError(
                "ANDON: view %g has right %s / up %s - not an axis-aligned pair; a box cannot be "
                "read off it" % (yaw, np.round(right, 6).tolist(), np.round(up, 6).tolist()))
        ax = ax[0]
        sgn = float(np.sign(right[ax]))
        u0 = bmid[ax] + sgn * ((min(x0, x1) + 0.5 - W / 2.0) * (h_ext / W))
        u1 = bmid[ax] + sgn * ((max(x0, x1) + 0.5 - W / 2.0) * (h_ext / W))
        z1 = bmid[2] + (H / 2.0 - min(y0, y1) - 0.5) * one_px
        z0 = bmid[2] + (H / 2.0 - max(y0, y1) - 0.5) * one_px
        return yaw, ax, (min(u0, u1), max(u0, u1)), (min(z0, z1), max(z0, z1))

    ya, aa, ra, za = parse(args.region_a)
    yb, ab, rb, zb = parse(args.region_b)
    if not (aa != ab):
        raise AssertionError(
            "ANDON: both region views read world axis %s; need orthogonal views" % "xyz"[aa])
    zd = max(abs(za[0] - zb[0]), abs(za[1] - zb[1])) / (bhi[2] - blo[2])
    if not (zd <= args.z_tol):
        raise AssertionError(
            "ANDON: the two region views disagree about z by %.4f of height (tol %.4f): "
            "view %g says %s, view %g says %s" % (zd, args.z_tol, ya, np.round(za, 4).tolist(),
                                                  yb, np.round(zb, 4).tolist()))
    box = np.zeros((2, 3))
    box[:, aa] = ra
    box[:, ab] = rb
    box[:, 2] = (min(za[0], zb[0]), max(za[1], zb[1]))
    print("[thin] region '%s' box (canonical xyz) %s -> %s  (z views disagree %.4f of height)"
          % (args.region_name, [round(float(x), 5) for x in box[0]],
             [round(float(x), 5) for x in box[1]], zd), flush=True)

# --- sweep ---------------------------------------------------------------------------
per_view, tot_hit, tot_thin = {}, 0, {v_: 0 for v_ in VALUES}
reg_hit, reg_thin = 0, {v_: 0 for v_ in VALUES}
prev = {}
for yaw in VIEWS:
    hit, ext, (look, right, up) = cast(yaw)
    nh = int(hit.sum())
    tot_hit += nh
    row = {"hit_px": nh}
    inreg = None
    if box is not None:
        # a pixel is "in region" when its FIRST-HIT point lies inside the box
        # (the surface the camera actually sees there), not when the ray passes near it
        o = (bmid[None, None, :] + gx[..., None] * right[None, None, :]
             + gy[..., None] * up[None, None, :] - look[None, None, :] * D)
        aF = rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [o, np.broadcast_to(look, o.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
        t = aF["t_hit"].numpy().reshape(H, W)
        P = o + look[None, None, :] * np.where(np.isfinite(t), t, 0.0)[..., None]
        inreg = hit & np.all((P >= box[0]) & (P <= box[1]), axis=-1)
        reg_hit += int(inreg.sum())
        row["region_px"] = int(inreg.sum())
    for val in VALUES:
        th = (ext < val) & hit if val > 0.0 else np.zeros_like(hit)
        tot_thin[val] += int(th.sum())
        row["thin_%g" % val] = round(100.0 * th.sum() / max(nh, 1), 4)
        if inreg is not None:
            r = th & inreg
            reg_thin[val] += int(r.sum())
            row["region_thin_%g" % val] = round(100.0 * r.sum() / max(int(inreg.sum()), 1), 4)
    per_view["%g" % yaw] = row
    print("[thin] yaw %6.1f  hit %9s%s" % (yaw, f"{nh:,}",
          ("  region %9s" % f"{int(inreg.sum()):,}") if inreg is not None else ""), flush=True)
    if args.preview:
        from PIL import Image
        os.makedirs(args.preview, exist_ok=True)
        e = np.where(np.isfinite(ext), np.clip(ext / 0.05, 0, 1), 0.0)
        img = (np.dstack([e, e, e]) * 255).astype(np.uint8)
        img[~hit] = (28, 28, 32)
        if inreg is not None:
            edge = inreg ^ np.roll(inreg, 1, axis=0)
            img[edge] = (255, 90, 60)
        Image.fromarray(img).save(os.path.join(args.preview, "ext_y%03d.png" % int(yaw)))
        prev[str(yaw)] = os.path.join(args.preview, "ext_y%03d.png" % int(yaw))

print("\n[thin] COST CURVE - fraction of visible figure withheld from diffusion, all views pooled")
print("       %-12s %14s %10s %s" % ("thin_extent", "in emit px", "FIGURE", "REGION '%s'" % args.region_name if box is not None else ""))
curve = {}
for val in VALUES:
    fig = 100.0 * tot_thin[val] / max(tot_hit, 1)
    reg = 100.0 * reg_thin[val] / max(reg_hit, 1) if box is not None else float("nan")
    curve["%g" % val] = {"figure_pct": round(fig, 4), "region_pct": round(reg, 4),
                         "ratio_region_over_figure": round(reg / fig, 3) if fig > 0 else None}
    tag = ""
    if val == 0.0:
        tag = "  <- the TOOL default: undecided runs the guard DISABLED"
    print("       %-12g %14.1f %9.3f%%%s%s"
          % (val, val / one_px, fig,
             ("  %9.3f%%" % reg) if box is not None else "",
             tag))

rec = {"glb": os.path.abspath(args.glb), "aspect": [W, H], "margin": args.margin,
       "fit_axis": args.fit_axis, "views": VIEWS, "el": args.el, "one_px": one_px,
       "h_ext": h_ext, "v_ext": v_ext, "values": VALUES,
       "region_name": args.region_name if box is not None else None,
       "region_box_canonical": box.tolist() if box is not None else None,
       "region_spec": {"a": args.region_a, "b": args.region_b} if box is not None else None,
       "total_hit_px": tot_hit, "total_region_px": reg_hit if box is not None else None,
       "per_view": per_view, "curve": curve, "previews": prev,
       "region_caveat": ("The region is SPATIAL and contains the wing arm and finger struts "
                         "as well as the membrane sheet. Struts are thick, so they can only "
                         "lower the withheld fraction: this is a floor on what the membrane "
                         "proper loses, never an overstatement.")}
if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    json.dump(rec, open(args.out, "w"), indent=1)
    print("\n[thin] wrote %s" % os.path.abspath(args.out))
