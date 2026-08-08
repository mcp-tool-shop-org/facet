"""THE PER-STROKE EYE-GATE WATCHES, measured and LOCATED - E14 handoff 8, Ruling 27e's form.

Every watch is measured on the newly-painted pixels and located to a STRUCTURE, never
reported as a bare total and never asserted. The structures come from GEOMETRY: this file
raycasts the job's own camera against the mesh and labels each pixel by the z of the surface
it hits, so "the crossing" and "the blade" are the mesh's crossing and blade rather than a row
band. That distinction is not pedantry here - a row band containing the gold collar
contaminated a stone measurement twice on this route (handoff 5, and again at Ruling 25b), and
the standing cut is to isolate structures by their own footprint.

THE STRUCTURE BANDS are derived once, from the mesh's own width profile, and frozen in
canon/E14-longsword-structures.json. Each boundary is a local minimum of the x-extent-vs-z
curve at 0.006 resolution, with the curve's values recorded beside it; the stone's lower bound
is the landmark the demotion and the collar repair already assert (z = 0.4340).

THE WATCHES:

  red outside L5   wine-band (332-32) pixels above the chroma floor, located. The oxblood wrap
                   owns that band legitimately; the signature is red arriving on the CROSSING
                   or the BLADE, which must read zero (Ruling 24g).
  12e gold         gold-band (42-104) pixels, located. Gold belongs to the collar, the mid ring
                   and the boss; anywhere else is the 12e watch firing.
  fifth signature  dark+desaturated share of the FILL against the CONTEXT'S OWN share
                   (Ruling 27e's adopted form: less-or-equal is clean). Reported across a GRID
                   of (L*, C*) cuts rather than at one threshold, because E12 Ruling 27d armed
                   no numeric gate and stroke 1's recorded 29.1/31.8 does not reproduce at any
                   single cut in this grid - so the honest statement is the RELATION, which
                   holds or fails independently of where the cut is put.
  forbidden        the palette's 104-290 span, above the floor, located.

  e14_stroke_watch.py --job DIR --prep DIR --structures JSON [--out JSON]

Standards compliance: PIN_PER_STEP - the camera is rebuilt from the job's own cam.json and the
structure bands from a frozen file, so a watch is replayable from what is on disk.
ANDON_AUTHORITY - this file MEASURES; it renders no verdict and halts nothing. The eye gate is
the Director's and the advisor's. DECOMPOSE_BY_SECRETS - every count is broken out by
structure, never summed into one number. EXTERNAL_VERIFIER - the bands come from the palette
fixture and the structures from the mesh; neither was written by the brush.
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
ap.add_argument("--job", required=True)
ap.add_argument("--prep", required=True)
ap.add_argument("--structures", required=True)
ap.add_argument("--palette", default="canon/E14-longsword-palette.json")
ap.add_argument("--out", default=None)
args = ap.parse_args()
J = os.path.join
D = 2.0


def to_lab(rgb):
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16, 500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


def lch(img):
    lab = to_lab(img)
    return (lab[..., 0], np.hypot(lab[..., 1], lab[..., 2]),
            np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360.0)


def inband(H, lo, hi):
    return (H >= lo) & (H <= hi) if lo <= hi else ((H >= lo) | (H <= hi))


pal = json.load(open(args.palette, encoding="utf-8"))
CMIN = pal["min_chroma"]
BANDS = {b["name"]: tuple(b["hue_deg"]) for b in pal["allowed_bands"]}
WINE, GOLD = BANDS["wine"], BANDS["gold"]
FORB = (104.0, 290.0)

ST = json.load(open(args.structures, encoding="utf-8"))
cam = json.load(open(J(args.job, "cam.json"), encoding="utf-8"))
W, H = int(cam["W"]), int(cam["H"])

# ---- the job's own camera, rebuilt: emit's basis(), unmodified ----
th, el = np.radians(cam["yaw"]), np.radians(cam["el"])
cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
look = -cd / (np.linalg.norm(cd) + 1e-12)
up0 = np.array([0.0, 0.0, 1.0])
right = np.cross(look, up0)
right /= np.linalg.norm(right) + 1e-12
up = np.cross(right, look)
up /= np.linalg.norm(up) + 1e-12

m = trimesh.load(J(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)), o3d.core.Tensor(f.astype(np.uint32)))

bmid = np.array(cam["bmid"])
xs = (np.arange(W) + 0.5) / W * cam["h_ext"] - cam["h_ext"] / 2
ys = cam["v_ext"] / 2 - (np.arange(H) + 0.5) / H * cam["v_ext"]
gx, gy = np.meshgrid(xs, ys)
origins = (bmid[None, None, :] + gx[..., None] * right[None, None, :]
           + gy[..., None] * up[None, None, :] - look[None, None, :] * D)
dirs = np.broadcast_to(look, origins.shape)
rays = o3d.core.Tensor(np.concatenate([origins, dirs], axis=-1).astype(np.float32))
res = rs.cast_rays(rays)
t = res["t_hit"].numpy()
hitmask = np.isfinite(t)
hz = np.full((H, W), np.nan)
hz[hitmask] = (origins[hitmask] + t[hitmask][:, None] * look[None, :])[:, 2]

LABELS = [s["name"] for s in ST["structures"]]
lab_img = np.full((H, W), "", dtype=object)
for s in ST["structures"]:
    sel = hitmask & (hz >= s["z_lo"]) & (hz < s["z_hi"])
    lab_img[sel] = s["name"]

em = np.asarray(Image.open(J(args.job, "render.png")).convert("RGB"), dtype=np.float64) / 255.0
ed = np.asarray(Image.open(J(args.job, "inpainted.png")).convert("RGB"), dtype=np.float64) / 255.0
mk = np.asarray(Image.open(J(args.job, "mask.png")).convert("L")) > 127
hit = np.asarray(Image.open(J(args.job, "hit.png")).convert("L")) > 127
ctx = hit & ~mk

Le, Ce, He = lch(ed)
Lm, Cm, Hm = lch(em)
rep = {"job": os.path.abspath(args.job), "yaw": cam["yaw"], "el": cam["el"],
       "job_mask_px": int(mk.sum()), "figure_px": int(hit.sum()),
       "context_px": int(ctx.sum()),
       "painted_pct_of_figure": round(100.0 * (hit.sum() - mk.sum()) / hit.sum(), 2)}

print(f"[watch] yaw {cam['yaw']:.0f}  job mask {int(mk.sum()):,} px of {int(hit.sum()):,} "
      f"figure px  ({rep['painted_pct_of_figure']:.1f}% of the figure already painted)")
print(f"[watch] structure labels on the job mask:")
for nm in LABELS:
    n = int((mk & (lab_img == nm)).sum())
    if n:
        print(f"[watch]     {nm:<14s} {n:>7,}  ({100.0 * n / mk.sum():5.1f}% of the mask)")
        rep.setdefault("mask_by_structure", {})[nm] = n
unl = int((mk & (lab_img == "")).sum())
rep["mask_unlabelled"] = unl
if unl:
    print(f"[watch]     {'(no hit)':<14s} {unl:>7,}  - mask px the raycast finds no surface "
          f"under (the mask is dilated past the silhouette by construction)")


def located(sel, title, floor=True):
    s = sel & mk
    n = int(s.sum())
    out = {"total": n, "by_structure": {}}
    print(f"[watch] {title}: {n:,} px of the {int(mk.sum()):,} newly-painted")
    if n:
        for nm in LABELS:
            k = int((s & (lab_img == nm)).sum())
            if k:
                out["by_structure"][nm] = k
                print(f"[watch]     {nm:<14s} {k:>7,}  ({100.0 * k / n:5.1f}%)")
        k = int((s & (lab_img == "")).sum())
        if k:
            out["by_structure"]["(no hit)"] = k
            print(f"[watch]     {'(no hit)':<14s} {k:>7,}  ({100.0 * k / n:5.1f}%)")
    return out


above = Ce > CMIN
rep["red_outside_L5"] = located(above & inband(He, *WINE), f"RED, wine band {WINE}, above C* {CMIN:g}")
rep["gold_12e"] = located(above & inband(He, *GOLD), f"GOLD, band {GOLD}, above C* {CMIN:g}")
rep["forbidden"] = located(above & inband(He, *FORB), f"FORBIDDEN, band {FORB}, above C* {CMIN:g}")

print("[watch] THE FIFTH SIGNATURE - dark+desaturated share, FILL vs the CONTEXT'S OWN share")
print(f"[watch]     {'L* <':>6s} {'C* <':>6s} {'fill %':>9s} {'context %':>11s}   verdict")
grid, worst = [], None
for Lt in (20, 25, 30, 35, 40):
    for Ct in (8, 10, 12, 15):
        fill = 100.0 * float(((Le < Lt) & (Ce < Ct) & mk).sum()) / max(int(mk.sum()), 1)
        con = 100.0 * float(((Lm < Lt) & (Cm < Ct) & ctx).sum()) / max(int(ctx.sum()), 1)
        ok = fill <= con
        grid.append({"L": Lt, "C": Ct, "fill_pct": round(fill, 2),
                     "context_pct": round(con, 2), "fill_le_context": ok})
        if not ok and (worst is None or fill - con > worst):
            worst = fill - con
        print(f"[watch]     {Lt:>6d} {Ct:>6d} {fill:>8.1f}% {con:>10.1f}%   "
              f"{'clean' if ok else 'ABOVE CONTEXT'}")
rep["fifth_signature_grid"] = grid
nclean = sum(1 for g in grid if g["fill_le_context"])
rep["fifth_signature_clean_cuts"] = f"{nclean}/{len(grid)}"
print(f"[watch]   the fill is at or below the context's share at {nclean} of {len(grid)} cuts"
      + ("" if nclean == len(grid) else f"; worst excess {worst:+.1f} points"))

if args.out:
    json.dump(rep, open(args.out, "w"), indent=1)
    print(f"[watch] wrote {args.out}")
