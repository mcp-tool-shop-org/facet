"""E04 Task 1 - is the crown step a SOURCE SWITCH or a real change in the scalp?

e04_blotch.py locates the crown's hard edge on a stage-1 camera-ownership boundary: one
side of the seam is painted by the yaw-090 twin, the other by the yaw-135 twin. That is
where the pipeline switches sources. It is not yet proof that the SOURCES are what differ
- the surface itself could genuinely change colour at that line, and the boundary would
then be a coincidence.

This settles it by asking both twins the same question. For every texel in the region,
project it into BOTH twins with project_twins' own camera math and read the colour each
one paints there. If the two twins disagree by roughly the seam's own dE - and each twin
is internally flat across the line - then nothing changes at the boundary except which
image is being read, which is the definition of a source switch.

The prediction that would REFUTE the mechanism is stated in the report before this ran:
if each twin individually steps across the seam line, the surface changes there and the
ownership boundary is incidental.

  e04_seam_sources.py --prep DIR --armb DIR --views 90,135 --texels roi.npy --out J

Standards compliance: PIN_PER_STEP - camera math copied from project_twins with the source
line cited, every path an argument. EXTERNAL_VERIFIER - reports two colour distributions
and their separation; it does not rule on whether the seam matters.
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
ap.add_argument("--armb", required=True)
ap.add_argument("--twins", help="twin dir; default <armb>/twins")
ap.add_argument("--views", default="90,135", help="the two yaws either side of the seam")
ap.add_argument("--texels", required=True, help=".npy of flat texel indices (the ROI)")
ap.add_argument("--aspect", default="752,1024")
ap.add_argument("--facing-floor", type=float, default=0.45,
                help="project_twins' own --facing-min body floor; the fair-comparison set "
                     "is the texels BOTH cameras see above it. Inherited, not chosen here.")
ap.add_argument("--out", required=True)
args = ap.parse_args()

meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
valid = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
vflat = valid.reshape(-1)
lo = np.array(meta["lo"]); hi = np.array(meta["hi"])
tw_dir = args.twins or os.path.join(args.armb, "twins")

m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
vz = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
blo, bhi = vz.min(axis=0), vz.max(axis=0)
bmid = (blo + bhi) / 2
AW, AH = [float(x) for x in args.aspect.split(",")]
v_ext = (bhi[2] - blo[2]) * 1.204          # project_twins.py:193
h_ext = v_ext * (AW / AH)                  # project_twins.py:194
W, H = int(AW), int(AH)

pos_e = np.load(os.path.join(args.prep, "pos.npy")).reshape(-1, 3)
nor_e = np.load(os.path.join(args.prep, "nor.npy")).reshape(-1, 3)
roi = np.load(args.texels)
roi = roi[vflat[roi]]
P = (pos_e[roi].astype(np.float64) * (hi - lo) + lo) / meta["maxabs"] * 0.5
N = nor_e[roi].astype(np.float64) * 2.0 - 1.0
N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
print("[seam] ROI texels %d" % len(roi), flush=True)


def basis(yaw_d, el_d=0.0):
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    look = -cd / np.linalg.norm(cd)
    up0 = np.array([0.0, 0.0, 1.0])
    right = np.cross(look, up0); right /= np.linalg.norm(right) + 1e-12
    up = np.cross(right, look)
    return cd, look, right, up / (np.linalg.norm(up) + 1e-12)


def bilin(img, x, y):
    h, w = img.shape[:2]
    x0 = np.clip(np.floor(x).astype(np.int64), 0, w - 2)
    y0 = np.clip(np.floor(y).astype(np.int64), 0, h - 2)
    fx = np.clip(x - x0, 0, 1)[:, None]
    fy = np.clip(y - y0, 0, 1)[:, None]
    return (img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy)
            + img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy)


def lab(rgb):
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16, 500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


yaws = [float(x) for x in args.views.split(",")]
step = 45.0
cols = {}
for yaw in yaws:
    k = int(round(yaw / step))
    img = np.asarray(Image.open(os.path.join(tw_dir, "twin_%d.png" % k)
                                ).convert("RGB"), dtype=np.float32) / 255.0
    cd, look, right, up = basis(yaw)
    xr = (P @ right) - (bmid @ right)     # project_twins.py:537-540
    zu = (P @ up) - (bmid @ up)
    px = (xr / h_ext + 0.5) * W - 0.5
    py = (0.5 - zu / v_ext) * H - 0.5
    cols[yaw] = bilin(img, px, py)
    print("[seam] twin_%d (yaw %.0f) sampled at %d texels" % (k, yaw, len(roi)), flush=True)

# ownership, so each texel can be labelled with which side of the seam it is on
dz = np.load(os.path.join(args.armb, "diag_8cam.npz"))
vnames = [str(x) for x in dz["__views__"]]
NV = int(vflat.sum())
vidx = np.full(RES * RES, -1, dtype=np.int64)
vidx[np.where(vflat)[0]] = np.arange(NV)
Nall = np.load(os.path.join(args.prep, "nor.npy")).reshape(-1, 3)[vflat].astype(np.float64)
Nall = Nall * 2.0 - 1.0
Nall /= np.linalg.norm(Nall, axis=1, keepdims=True) + 1e-12
best = np.full(NV, -np.inf); own = np.full(NV, -1, dtype=np.int8)
for vi, nm in enumerate(vnames):
    yy = float(nm.replace("y", "").replace("+", ""))
    cd, look, right, up = basis(yy)
    fac = Nall @ (-look)
    ci = dz["%s/cand_idx" % nm]; acc = dz["%s/accepted" % nm]
    sel = ci[acc]
    tk = fac[sel] > best[sel]
    best[sel[tk]] = fac[sel][tk]; own[sel[tk]] = vi
own_roi = own[vidx[roi]]

out = {"roi_texels": int(len(roi)), "views": yaws, "sides": {}}
print("[seam] each twin's own colour, split by WHICH SIDE of the seam the texel is on:")
print("[seam]   a flat twin across the line means the twin does not change there;")
print("[seam]   the step is then only the switch between the two twins.")
for yaw in yaws:
    k = int(round(yaw / step))
    for side in yaws:
        ks = int(round(side / step))
        if ks >= len(vnames):
            continue
        sel = own_roi == ks
        if sel.sum() < 100:
            continue
        c = cols[yaw][sel]
        mn = np.median(c, axis=0)
        L = float(lab(mn[None, :])[0, 0])
        key = "twin%d_on_side%d" % (k, ks)
        out["sides"][key] = {"px": int(sel.sum()),
                             "rgb255": [int(round(x * 255)) for x in mn],
                             "L": round(L, 2)}
        print("[seam]   twin_%d sampled on the side owned by twin_%d: n=%6d  rgb%s  L*%.1f"
              % (k, ks, int(sel.sum()), tuple(out["sides"][key]["rgb255"]), L), flush=True)

# the two decisive numbers
a, b = yaws[0], yaws[1]
ka, kb = int(round(a / step)), int(round(b / step))
sa = own_roi == ka
sb = own_roi == kb
if sa.sum() > 100 and sb.sum() > 100:
    def med(x):
        return np.median(x, axis=0)
    dE = lambda p, q: float(np.linalg.norm(lab(p[None, :]) - lab(q[None, :])))
    # 1. how far apart the two TWINS are, measured on the SAME texels
    both = sa | sb
    d_tw = dE(med(cols[a][both]), med(cols[b][both]))
    # 2. how far each twin moves ACROSS the line, on its own
    d_a = dE(med(cols[a][sa]), med(cols[a][sb]))
    d_b = dE(med(cols[b][sa]), med(cols[b][sb]))
    out["dE_between_twins_same_texels"] = round(d_tw, 2)
    out["dE_twin%d_across_line" % ka] = round(d_a, 2)
    out["dE_twin%d_across_line" % kb] = round(d_b, 2)
    print("[seam] dE BETWEEN THE TWO TWINS, on the same texels:      %.2f" % d_tw, flush=True)
    print("[seam] dE twin_%d moves ACROSS the seam line, by itself:   %.2f" % (ka, d_a),
          flush=True)
    print("[seam] dE twin_%d moves ACROSS the seam line, by itself:   %.2f" % (kb, d_b),
          flush=True)

# ---------------------------------------------------------------- the fair comparison
# The pooled figures above are contaminated and the contamination has a direction. A
# texel on the far side of the seam is, BY THE DEFINITION OF THE SEAM, one the near
# camera sees at a lower angle - ownership is argmax(facing), so crossing the line means
# the other camera now faces it better. Sampling twin A there reads shading, not surface,
# and it reads it dark. So "does twin A change across the line" cannot be asked over
# texels twin A can barely see.
#
# The fair set is the texels BOTH cameras see properly. --facing-floor defaults to
# project_twins' own body floor (0.45), an inherited constant rather than one chosen here.
cd_a, la, ra, ua = basis(a)
cd_b, lb, rb, ub = basis(b)
fa = N @ (-la)
fb = N @ (-lb)
well = (fa > args.facing_floor) & (fb > args.facing_floor)
out["facing_floor"] = args.facing_floor
out["well_seen_px"] = int(well.sum())
print("[seam] fair set: %d of %d texels seen by BOTH cameras at facing > %.2f"
      % (int(well.sum()), len(roi), args.facing_floor), flush=True)
if well.sum() > 100:
    wa = well & sa
    wb = well & sb
    ma_ = np.median(cols[a][well], axis=0)
    mb_ = np.median(cols[b][well], axis=0)
    dEw = float(np.linalg.norm(lab(ma_[None, :]) - lab(mb_[None, :])))
    per = np.linalg.norm(lab(cols[a][well]) - lab(cols[b][well]), axis=-1)
    out["well_seen"] = {
        "twin_a_rgb255": [int(round(x * 255)) for x in ma_],
        "twin_b_rgb255": [int(round(x * 255)) for x in mb_],
        "twin_a_L": round(float(lab(ma_[None, :])[0, 0]), 2),
        "twin_b_L": round(float(lab(mb_[None, :])[0, 0]), 2),
        "dE_medians": round(dEw, 2),
        "dE_per_texel_median": round(float(np.median(per)), 2),
        "dE_per_texel_p90": round(float(np.percentile(per, 90)), 2)}
    print("[seam]   twin_%d rgb%s L*%.1f   vs   twin_%d rgb%s L*%.1f"
          % (ka, tuple(out["well_seen"]["twin_a_rgb255"]), out["well_seen"]["twin_a_L"],
             kb, tuple(out["well_seen"]["twin_b_rgb255"]), out["well_seen"]["twin_b_L"]),
          flush=True)
    print("[seam]   THE TWO SOURCES DISAGREE BY dE %.2f on surface both see properly"
          % dEw, flush=True)
    print("[seam]   per-texel dE median %.2f  p90 %.2f"
          % (out["well_seen"]["dE_per_texel_median"],
             out["well_seen"]["dE_per_texel_p90"]), flush=True)
    if wa.sum() > 50 and wb.sum() > 50:
        da_ = float(np.linalg.norm(lab(np.median(cols[a][wa], axis=0)[None, :])
                                   - lab(np.median(cols[a][wb], axis=0)[None, :])))
        db_ = float(np.linalg.norm(lab(np.median(cols[b][wa], axis=0)[None, :])
                                   - lab(np.median(cols[b][wb], axis=0)[None, :])))
        out["well_seen"]["dE_twin_a_across_line"] = round(da_, 2)
        out["well_seen"]["dE_twin_b_across_line"] = round(db_, 2)
        out["well_seen"]["a_px"] = int(wa.sum())
        out["well_seen"]["b_px"] = int(wb.sum())
        print("[seam]   within the fair set, twin_%d moves %.2f across the line, "
              "twin_%d moves %.2f  (n %d / %d)"
              % (ka, da_, kb, db_, int(wa.sum()), int(wb.sum())), flush=True)

json.dump(out, open(args.out, "w"), indent=1)
print("[seam] wrote %s" % args.out, flush=True)
