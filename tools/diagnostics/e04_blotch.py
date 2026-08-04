"""E04 Task 1 - what is the crown blotch made of? Boundary alignment at an arbitrary camera.

The Director named one region on the accepted asset: a patchy, hard-edged blotch on the
crown and side of the head above the ear. The advisor's pre-registered prior is the
documented unlevelled stroke-seam defect. This instrument tests that prior and its
alternates without being written to any of their answers.

WHAT IT MEASURES, and why each layer exists
-------------------------------------------
E07's Gate 0 part B compared a render pixel's luminance against its 4-neighbour and
asked whether the pair straddled a PROVENANCE boundary. That instrument is fixed to the
FRONT head camera, which barely sees a crown. The statistic is carried over unchanged;
only the camera is generalised to (yaw, elevation), using texpass_iter's own basis() so
"yaw 90" means here exactly what it means on a stroke camera.

Three partitions are carried, not one, because a hard edge in this pipeline has three
candidate mechanisms and only the first is the prior:

  claim   provenance  - TWINS (stage 1) / BRUSH s1-7 / BRUSH s8 / DILATION.
                        Built EXACTLY from saved masks, no replay: stage-1 styled mask,
                        the post-stroke hole map, the final styled mask, and atlas vs
                        atlas.prev for stroke 8. Asserted against the run's own counts.
  owner   stage-1 camera ownership - project_twins assigns each texel the colour of the
                        ACCEPTED view with the largest facing (w = facing^power, and
                        argmax is invariant to a monotone power). Its sigma=16 levelling
                        corrects the LOW-frequency offset between ownership and the
                        facing-weighted blend; a sharp step at an ownership boundary is
                        high-frequency and survives it. So an inter-camera seam INSIDE
                        stage 1 is a real mechanism that a provenance map cannot see -
                        every texel on both sides is class TWINS.
  island  UV chart      - the chart-fragmentation alternate.

LUMINANCE IS SAMPLED FROM THE ATLAS, NOT FROM A BLENDER RENDER. E07 measured on an 8-bit
render under exposure 0.85 and the Standard view transform, and recorded that its own
denominator was 4.0 quanta with almost no room to fall. Sampling the atlas at the hit
texel removes the tone curve, removes the render's resampling, and pairs every luminance
with the exact texel it came from. The cost is that ratios here are NOT numerically
comparable to E07's 5.500 / 9.500 - numerator and denominator are reported separately so
that is visible rather than implied.

ALIGNMENT IS REPORTED AS A CURVE, NOT AT A CHOSEN THRESHOLD. "Is the patch edge on a
boundary" needs a definition of "patch edge", and any threshold picked after seeing the
image is a threshold picked to pass. So: rank every scalp pixel by |lum - median5| and
report, per decile, the share within N px of each of the three boundary types, against
that boundary type's own base rate over the same region. The operating point quoted is
E07's inherited --blotch 0.10, not a number chosen here.

  e04_blotch.py --prep DIR --armb DIR --atlas atlas_final.png --views 90,0 --out DIR
                [--roi cx,cy,r] [--cache DIR]

Standards compliance: PIN_PER_STEP - every input path and camera is an argument, the
claim map is asserted against the run's recorded counts before anything reads it.
ANDON_AUTHORITY - the assertions halt; this tool reports numbers and rules on nothing.
EXTERNAL_VERIFIER - measures, never judges. Whether a mechanism is worth fixing is the
Director's.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import distance_transform_edt, median_filter

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--armb", required=True, help="the run dir: stage1_8cam_styled_mask.npy, state/, diag_8cam.npz")
ap.add_argument("--atlas", required=True, help="the FINAL atlas (post-finalize)")
ap.add_argument("--views", default="90,0", help="yaw:el pairs, comma separated; el defaults to 0")
ap.add_argument("--res", type=int, default=1024)
ap.add_argument("--pad", type=float, default=1.25, help="head-crop span pad, as e07_gate0")
ap.add_argument("--bound", type=float, default=0.55)
ap.add_argument("--ray-d", type=float, default=4.0)
ap.add_argument("--blotch", type=float, default=0.10,
                help="INHERITED from e07_gate0's --blotch default. Not chosen here.")
ap.add_argument("--near", type=float, default=2.0, help="px: 'within N px of a boundary'")
ap.add_argument("--roi", action="append", default=[],
                help="name=cx,cy,r in camera pixels; repeatable")
ap.add_argument("--roi-view", help="the view an ROI disc is drawn on; default = first --views")
ap.add_argument("--centre", help="x,y,z in std space; default = e07_gate0's face-rect centre")
ap.add_argument("--span", type=float, help="override the face-rect span (world units)")
ap.add_argument("--cache", help="dir for the texel->island grid")
ap.add_argument("--out", required=True)
args = ap.parse_args()

os.makedirs(args.out, exist_ok=True)
meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
valid = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
vflat = valid.reshape(-1)
NV = int(vflat.sum())
lo = np.array(meta["lo"]); hi = np.array(meta["hi"])

m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
uv = np.asarray(m.visual.uv, dtype=np.float64)
nf = len(f)
vz = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(vz.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))
out = {"prep": args.prep, "armb": args.armb, "atlas": args.atlas}


def basis(yaw_d, el_d):
    """texpass_iter.basis, verbatim, so a yaw here means what it means on a stroke."""
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    look = -cd / np.linalg.norm(cd)
    up0 = np.array([0.0, 0.0, 1.0])
    right = np.cross(look, up0)
    right /= np.linalg.norm(right) + 1e-12
    up = np.cross(right, look)
    return cd, look, right, up / (np.linalg.norm(up) + 1e-12)


# ------------------------------------------------- the claim map, from saved masks only
S = os.path.join(args.armb, "state")
holes = np.asarray(Image.open(os.path.join(S, "holes.png")).convert("L")) > 127
s1 = np.load(os.path.join(args.armb, "stage1_8cam_styled_mask.npy"))
sf = np.load(os.path.join(S, "styled_mask.npy"))
atl = np.asarray(Image.open(os.path.join(S, "atlas.png")).convert("RGB"))
atp = np.asarray(Image.open(os.path.join(S, "atlas.prev.png")).convert("RGB"))
s8 = (atl != atp).any(-1)

claim = np.full((RES, RES), 255, dtype=np.uint8)     # DILATION
claim[valid & sf & ~s1] = 1                          # BRUSH, strokes 1-7
claim[valid & s8] = 8                                # BRUSH, stroke 8
claim[valid & s1] = 0                                # TWINS (stage 1)
claim[~valid] = 254                                  # not a texel
n_tw = int((claim == 0).sum()); n_b7 = int((claim == 1).sum())
n_b8 = int((claim == 8).sum()); n_di = int((claim == 255).sum())
print("[e04] claim  TWINS %d  BRUSH1-7 %d  BRUSH8 %d  DILATION %d  (valid %d)"
      % (n_tw, n_b7, n_b8, n_di, NV), flush=True)
assert n_tw == 1653659, "ANDON: stage-1 count %d != the run's 1,653,659" % n_tw
assert n_b7 + n_b8 == 101527, "ANDON: brush count %d != the run's 101,527" % (n_b7 + n_b8)
assert n_b8 == 25175, "ANDON: stroke-8 count %d != the run's 25,175" % n_b8
assert n_di == 647624, "ANDON: dilation count %d != the run's 647,624" % n_di
assert n_tw + n_b7 + n_b8 + n_di == NV, "ANDON: classes do not partition valid"
out["claim_counts"] = {"TWINS": n_tw, "BRUSH_1_7": n_b7, "BRUSH_8": n_b8, "DILATION": n_di}

# ------------------------------------------- stage-1 camera ownership, recomputed exactly
# project_twins: owner = the ACCEPTED view with the largest facing (w = facing^power, and
# argmax is invariant under a monotone power, so power never has to be guessed).
dz = np.load(os.path.join(args.armb, "diag_8cam.npz"))
views = [str(x) for x in dz["__views__"]]
pos_e = np.load(os.path.join(args.prep, "pos.npy")).reshape(-1, 3)[vflat].astype(np.float64)
nor_e = np.load(os.path.join(args.prep, "nor.npy")).reshape(-1, 3)[vflat].astype(np.float64)
N = nor_e * 2.0 - 1.0
N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
best_f = np.full(NV, -np.inf, dtype=np.float64)
owner_c = np.full(NV, -1, dtype=np.int8)
for vi, name in enumerate(views):
    yaw = float(name.replace("y", "").replace("+", ""))
    cd, look, right, up = basis(yaw, 0.0)
    dtc = -look
    fac = N @ dtc
    ci = dz["%s/cand_idx" % name]
    acc = dz["%s/accepted" % name]
    sel = ci[acc]
    take = fac[sel] > best_f[sel]
    best_f[sel[take]] = fac[sel][take]
    owner_c[sel[take]] = vi
owner = np.full(RES * RES, -1, dtype=np.int8)
owner[np.where(vflat)[0]] = owner_c
owner = owner.reshape(RES, RES)
n_own = int((owner >= 0).sum())
print("[e04] stage-1 ownership reconstructed: %d texels owned by %d views"
      % (n_own, len(views)), flush=True)
assert n_own == n_tw, ("ANDON: ownership covers %d texels but stage 1 styled %d - the "
                       "reconstruction is not the same set" % (n_own, n_tw))
ocount = {views[i]: int((owner == i).sum()) for i in range(len(views))}
print("[e04] per-view ownership: %s" % ocount, flush=True)
out["ownership"] = ocount

# ----------------------------------------------------------------- island partition
def build_islands():
    """union-find over welded UV corners - e07_gate0 / texpass_metrics construction"""
    lvert = f.reshape(-1)
    luv = uv[f].reshape(-1, 2)
    key = (lvert.astype(np.int64) << 44) \
          ^ ((luv[:, 0] * 5e5).round().astype(np.int64) << 22) \
          ^ (luv[:, 1] * 5e5).round().astype(np.int64)
    loop_face = np.repeat(np.arange(nf, dtype=np.int64), 3)
    order = np.argsort(key, kind="stable")
    parent = np.arange(nf, dtype=np.int64)

    def find(i):
        root = i
        while parent[root] != root:
            root = parent[root]
        while parent[i] != root:
            parent[i], i = root, parent[i]
        return root

    sk, sf_ = key[order], loop_face[order]
    run = 0
    for j in range(1, len(sk) + 1):
        if j == len(sk) or sk[j] != sk[run]:
            if j - run > 1:
                r0 = find(sf_[run])
                for t in range(run + 1, j):
                    r = find(sf_[t])
                    if r != r0:
                        parent[r] = r0
            run = j
    roots = np.array([find(i) for i in range(nf)], dtype=np.int64)
    uniq, face_island = np.unique(roots, return_inverse=True)
    return len(uniq), face_island


cache_f = os.path.join(args.cache, "isl_grid.npy") if args.cache else None
if cache_f and os.path.exists(cache_f):
    isl = np.load(cache_f)
    print("[e04] island grid from cache: %d islands" % (int(isl.max()) + 1), flush=True)
else:
    n_isl, face_island = build_islands()
    P = (pos_e * (hi - lo) + lo) / meta["maxabs"] * 0.5
    prim = np.empty(len(P), dtype=np.int64)
    CH = 1_000_000
    for s in range(0, len(P), CH):
        e = min(s + CH, len(P))
        prim[s:e] = rs.compute_closest_points(o3d.core.Tensor(
            P[s:e].astype(np.float32)))["primitive_ids"].numpy().astype(np.int64)
    isl = np.full(RES * RES, -1, dtype=np.int32)
    isl[np.where(vflat)[0]] = face_island[prim].astype(np.int32)
    isl = isl.reshape(RES, RES)
    if cache_f:
        os.makedirs(args.cache, exist_ok=True)
        np.save(cache_f, isl)
    print("[e04] islands %d  faces/island %.1f" % (n_isl, nf / n_isl), flush=True)

atlas = np.asarray(Image.open(args.atlas).convert("RGB"), dtype=np.float32) / 255.0
assert atlas.shape[0] == RES, "ANDON: atlas is %d, prep says %d" % (atlas.shape[0], RES)

# --------------------------------------------------------------- the head-crop camera
CX0, CY0, CX1, CY1 = [float(x) for x in meta["crop"]]
CR = float(meta["crop_res"]); b = args.bound
sx0 = (CX0 / CR) * 2 * b - b; sx1 = (CX1 / CR) * 2 * b - b
sz0 = b - (CY1 / CR) * 2 * b; sz1 = b - (CY0 / CR) * 2 * b
cx, cz = (sx0 + sx1) / 2, (sz0 + sz1) / 2
span = max(sx1 - sx0, sz1 - sz0) * args.pad
midy = (vz[:, 1].min() + vz[:, 1].max()) / 2
centre = np.array([cx, midy, cz])
if args.centre:
    centre = np.array([float(x) for x in args.centre.split(",")])
if args.span:
    span = args.span
R = args.res
print("[e04] head camera: centre %s span %.4f res %d" % (np.round(centre, 4), span, R),
      flush=True)


def cast(yaw, el):
    cd, look, right, up = basis(yaw, el)
    g = (np.arange(R) + 0.5) / R * span - span / 2
    gx, gy = np.meshgrid(g, -g)
    org = (centre[None, None, :] + gx[..., None] * right[None, None, :]
           + gy[..., None] * up[None, None, :] - look[None, None, :] * args.ray_d)
    dirs = np.broadcast_to(look, org.shape)
    ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, dirs], axis=-1).reshape(-1, 6).astype(np.float32)))
    prim = ans["primitive_ids"].numpy().reshape(R, R)
    buv = ans["primitive_uvs"].numpy().reshape(R, R, 2)
    hit = np.isfinite(ans["t_hit"].numpy().reshape(R, R))
    tx = np.full((R, R), -1, dtype=np.int64)
    if hit.any():
        tr = f[prim[hit]]
        wu, wv = buv[hit][:, 0:1], buv[hit][:, 1:2]
        uvp = (1 - wu - wv) * uv[tr[:, 0]] + wu * uv[tr[:, 1]] + wv * uv[tr[:, 2]]
        ax = np.clip((uvp[:, 0] * RES).astype(np.int64), 0, RES - 1)
        ay = np.clip(((1 - uvp[:, 1]) * RES).astype(np.int64), 0, RES - 1)
        tx[hit] = ay * RES + ax
    return hit, tx


PAL = {0: (60, 200, 110), 1: (70, 170, 255), 8: (20, 80, 200), 255: (235, 120, 40),
       254: (90, 90, 90)}
OWNPAL = np.array([(230, 80, 80), (230, 160, 60), (220, 220, 70), (110, 210, 90),
                   (70, 200, 200), (80, 130, 235), (170, 100, 220), (235, 110, 180)],
                  dtype=np.uint8)


def ratios(dl, k1, k2, ta, tb, label):
    """median |dL| across a k1!=k2 boundary over median |dL| within, different-texel.

    The denominator excludes pairs that sample the SAME texel: a cross-boundary pair maps
    to two texels by construction, a within pair need not, and including the identical-texel
    zeros measures the camera's magnification rather than the texture. E07's correction,
    carried over.
    """
    same = k1 == k2
    dt = ta != tb
    if (same & dt).sum() < 50 or (~same).sum() < 50:
        return None
    den = float(np.median(dl[same & dt]))
    num = float(np.median(dl[~same]))
    r = num / max(den, 1e-9)
    print("[e04]   %-28s pairs %8d cross %7d  num %.5f den %.5f  RATIO %.3f"
          % (label, len(dl), int((~same).sum()), num, den, r), flush=True)
    return {"pairs": int(len(dl)), "cross": int((~same).sum()),
            "num": round(num, 5), "den": round(den, 5), "ratio": round(r, 3)}


def lab(rgb):
    """sRGB -> CIE L*a*b*, gate1_sheet.py's function, so dE here means dE there."""
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16, 500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


# An ROI is a REGION OF SURFACE, not a disc of pixels. It is drawn once on an anchor
# camera, converted to the set of texels that disc covers, and then applied as
# "texel in that set" on every view -- so "the crown" means the same patch of scalp from
# yaw 90 and from yaw 270, instead of whatever happens to sit at those pixels.
roi_texels = {}
if args.roi:
    aspec = (args.roi_view or args.views.split(",")[0])
    ay, ae = (aspec.split(":") + ["0"])[:2]
    ahit, atx = cast(float(ay), float(ae))
    aok = ahit & (atx >= 0)
    for spec in args.roi:
        nm, rest = spec.split("=")
        rcx, rcy, rr = [float(x) for x in rest.split(",")]
        yy, xx = np.mgrid[0:R, 0:R]
        disc = (((xx - rcx) ** 2 + (yy - rcy) ** 2) <= rr * rr) & aok
        roi_texels[nm] = np.unique(atx[disc])
        np.save(os.path.join(args.out, "roi_%s_texels.npy" % nm), roi_texels[nm])
        print("[e04] ROI %s drawn on anchor view %s: %d px -> %d texels (saved)"
              % (nm, aspec, int(disc.sum()), len(roi_texels[nm])), flush=True)

res_all = {}
for spec in args.views.split(","):
    yaw, el = (spec.split(":") + ["0"])[:2]
    yaw, el = float(yaw), float(el)
    tag = "y%+04d_e%+03d" % (int(yaw), int(el))
    hit, tx = cast(yaw, el)
    cf0 = claim.reshape(-1)
    # A hit pixel can land in the UV gutter, where there is no texel the pipeline owns.
    # finalize's flood writes colour there, so those pixels carry a value but no
    # provenance; E07's claim map defaulted them to DILATION and silently mixed them in.
    # They are excluded here instead - they are not part of any of the three partitions.
    ok = hit & (tx >= 0)
    ok[ok] = cf0[tx[ok]] != 254
    print("[e04] %s: %d hit px, %d on a valid texel (%d gutter px excluded)"
          % (tag, int(hit.sum()), int(ok.sum()), int(hit.sum()) - int(ok.sum())), flush=True)

    cf = claim.reshape(-1); of = owner.reshape(-1); isf = isl.reshape(-1)
    af = atlas.reshape(-1, 3)
    rgb = np.zeros((R, R, 3), dtype=np.uint8)
    rgb[ok] = (af[tx[ok]] * 255).round().astype(np.uint8)
    lum = np.zeros((R, R), dtype=np.float32)
    lum[ok] = af[tx[ok]].mean(-1)
    prov = np.zeros((R, R, 3), dtype=np.uint8)
    ownim = np.zeros((R, R, 3), dtype=np.uint8)
    for k, c in PAL.items():
        sel = ok & (cf[tx] == k) if ok.any() else np.zeros_like(ok)
        prov[sel] = c
    for i in range(len(views)):
        sel = ok & (of[tx] == i)
        ownim[sel] = OWNPAL[i]

    # 4-neighbour pairs, both endpoints on surface
    p1 = []; p2 = []; o1 = []; o2 = []; j1 = []; j2 = []; dls = []; t1 = []; t2 = []
    for ax_ in (0, 1):
        a = [slice(None)] * 2; c = [slice(None)] * 2
        a[ax_] = slice(0, -1); c[ax_] = slice(1, None)
        both = ok[tuple(a)] & ok[tuple(c)]
        ta = tx[tuple(a)][both]; tb = tx[tuple(c)][both]
        t1.append(ta); t2.append(tb)
        p1.append(cf[ta]); p2.append(cf[tb])
        o1.append(of[ta]); o2.append(of[tb])
        j1.append(isf[ta]); j2.append(isf[tb])
        dls.append(np.abs(lum[tuple(a)][both] - lum[tuple(c)][both]))
    tt1 = np.concatenate(t1); tt2 = np.concatenate(t2)
    dl = np.concatenate(dls)
    cc1 = np.concatenate(p1); cc2 = np.concatenate(p2)
    oo1 = np.concatenate(o1); oo2 = np.concatenate(o2)
    jj1 = np.concatenate(j1); jj2 = np.concatenate(j2)

    r = {"hit_px": int(hit.sum())}
    print("[e04] %s WHOLE HEAD CAMERA" % tag, flush=True)
    r["claim"] = ratios(dl, cc1, cc2, tt1, tt2, "claim (provenance)")
    same_c = cc1 == cc2
    # the stage-1 seam is measured INSIDE one provenance class, so a provenance step
    # cannot contribute to it; likewise the island control is measured inside one class
    # AND one owner, so neither of the other two mechanisms can contribute to it.
    sub = same_c & (oo1 >= 0) & (oo2 >= 0)
    if sub.sum() > 100:
        r["owner_within_claim"] = ratios(dl[sub], oo1[sub], oo2[sub], tt1[sub], tt2[sub],
                                         "stage-1 camera seam")
    sub2 = same_c & (oo1 == oo2)
    if sub2.sum() > 100:
        r["island_within_claim_owner"] = ratios(dl[sub2], jj1[sub2], jj2[sub2],
                                                tt1[sub2], tt2[sub2],
                                                "island (chart) boundary")

    # per boundary type on the claim map
    LBL = {0: "TWINS", 1: "BRUSH1-7", 8: "BRUSH8", 255: "DILATION"}
    dtm = tt1 != tt2
    den = float(np.median(dl[same_c & dtm]))
    bt = {}
    loq = np.minimum(cc1, cc2).astype(np.int64)
    hiq = np.maximum(cc1, cc2).astype(np.int64)
    for k in np.unique((loq * 256 + hiq)[~same_c]):
        sel = ((loq * 256 + hiq) == k) & ~same_c
        if sel.sum() < 200:
            continue
        nmm = "%s|%s" % (LBL.get(int(k // 256), "?"), LBL.get(int(k % 256), "?"))
        bt[nmm] = {"pairs": int(sel.sum()),
                   "ratio": round(float(np.median(dl[sel])) / max(den, 1e-9), 3)}
        print("[e04]     %-22s %7d pairs  ratio %.3f" % (nmm, int(sel.sum()), bt[nmm]["ratio"]),
              flush=True)
    r["claim_boundary_types"] = bt

    # ------------------------------------------------- alignment, as a curve
    cb = np.zeros((R, R), dtype=bool); ob = np.zeros((R, R), dtype=bool)
    ib = np.zeros((R, R), dtype=bool)
    for ax_ in (0, 1):
        a = [slice(None)] * 2; c = [slice(None)] * 2
        a[ax_] = slice(0, -1); c[ax_] = slice(1, None)
        both = ok[tuple(a)] & ok[tuple(c)]
        dc = both & (cf[tx][tuple(a)] != cf[tx][tuple(c)])
        do = both & (of[tx][tuple(a)] != of[tx][tuple(c)])
        di = both & (isf[tx][tuple(a)] != isf[tx][tuple(c)])
        cb[tuple(a)] |= dc; cb[tuple(c)] |= dc
        ob[tuple(a)] |= do; ob[tuple(c)] |= do
        ib[tuple(a)] |= di; ib[tuple(c)] |= di
    # NULL CONTROL. "90% of the strong steps are within 2 px of an owner boundary" is only
    # evidence if it would NOT be true of a boundary set with the same shape and density
    # placed somewhere else. ob_shift is the owner boundary map displaced 8 px diagonally -
    # same curves, same length, same density, wrong location. If the enrichment survives
    # the shift, this instrument is measuring density and not alignment.
    ob_shift = np.roll(ob, (8, 8), axis=(0, 1))
    dist = {"claim": distance_transform_edt(~cb), "owner": distance_transform_edt(~ob),
            "island": distance_transform_edt(~ib),
            "owner_shift8_NULL": distance_transform_edt(~ob_shift)}
    hp = np.abs(lum - median_filter(lum, size=5))

    def align(region, nm):
        n = int(region.sum())
        if n < 200:
            return None
        vals = hp[region]
        q = np.argsort(vals)
        d = {k: dist[k][region] for k in dist}
        base = {k: float((d[k] <= args.near).mean() * 100) for k in dist}
        top = q[int(len(q) * 0.9):]
        dec = {k: float((d[k][top] <= args.near).mean() * 100) for k in dist}
        op = vals > args.blotch
        opr = {k: (float((d[k][op] <= args.near).mean() * 100) if op.sum() > 20 else None)
               for k in dist}
        # THE DECIDING BREAKDOWN. "Within 2 px of a claim boundary" and "within 2 px of an
        # owner boundary" are not exclusive, and the two have very different base rates, so
        # neither percentage alone separates the hypotheses. This does: of the strong-step
        # pixels, how many are explained by ONLY one of the two.
        excl = None
        if op.sum() > 20:
            nc = d["claim"][op] <= args.near
            no = d["owner"][op] <= args.near
            excl = {"n": int(op.sum()),
                    "claim_only_pct": round(float((nc & ~no).mean() * 100), 1),
                    "owner_only_pct": round(float((no & ~nc).mean() * 100), 1),
                    "both_pct": round(float((nc & no).mean() * 100), 1),
                    "neither_pct": round(float((~nc & ~no).mean() * 100), 1)}
            print("[e04]     strong steps by cause: owner-only %.1f%%  claim-only %.1f%%  "
                  "both %.1f%%  neither %.1f%%"
                  % (excl["owner_only_pct"], excl["claim_only_pct"], excl["both_pct"],
                     excl["neither_pct"]), flush=True)
        print("[e04]   ALIGNMENT %s (n=%d, within %.0f px)" % (nm, n, args.near), flush=True)
        print("[e04]     base rate       claim %5.1f%%  owner %5.1f%%  island %5.1f%%  "
              "NULL(own+8) %5.1f%%"
              % (base["claim"], base["owner"], base["island"], base["owner_shift8_NULL"]),
              flush=True)
        print("[e04]     top decile |dL| claim %5.1f%%  owner %5.1f%%  island %5.1f%%  "
              "NULL(own+8) %5.1f%%"
              % (dec["claim"], dec["owner"], dec["island"], dec["owner_shift8_NULL"]),
              flush=True)
        if op.sum() > 20:
            print("[e04]     hp>%.2f (n=%d)  claim %5.1f%%  owner %5.1f%%  island %5.1f%%  "
                  "NULL(own+8) %5.1f%%"
                  % (args.blotch, int(op.sum()), opr["claim"], opr["owner"], opr["island"],
                     opr["owner_shift8_NULL"]), flush=True)
        else:
            print("[e04]     hp>%.2f: only %d px - operating point not evaluable"
                  % (args.blotch, int(op.sum())), flush=True)
        return {"n": n, "base_pct": base, "top_decile_pct": dec,
                "op_point_pct": opr, "op_n": int(op.sum()), "exclusive": excl,
                "hp_median": round(float(np.median(vals)), 5),
                "hp_p99": round(float(np.percentile(vals, 99)), 5)}

    r["align_all"] = align(ok, "whole head camera")
    r["rois"] = {}
    for nm, tset in roi_texels.items():
        reg = ok.copy()
        reg[ok] = np.isin(tx[ok], tset)
        if reg.sum() < 200:
            print("[e04]   ROI %s: %d px on this view - skipped" % (nm, int(reg.sum())),
                  flush=True)
            continue
        cls = {LBL.get(int(k), str(int(k))): int(((cf[tx] == k) & reg).sum())
               for k in (0, 1, 8, 255)}
        tot = max(sum(cls.values()), 1)
        print("[e04]   ROI %s: %d px  %s" % (
            nm, int(reg.sum()),
            "  ".join("%s %.1f%%" % (k, 100.0 * n / tot) for k, n in cls.items())),
            flush=True)
        own_r = {views[i]: int(((of[tx] == i) & reg).sum()) for i in range(len(views))}
        own_r = {k: nn for k, nn in own_r.items() if nn}
        print("[e04]   ROI %s owners: %s" % (nm, own_r), flush=True)
        # WHAT THE SEAM IS WORTH, in the unit the eye reads. The two dominant owners in
        # this region are two different twins painting the same scalp; the median colour
        # of each side and the dE between them is the size of the step a levelling pass
        # would have to close. Reported per side so a shift in one is visible.
        seam = None
        top2 = sorted(own_r.items(), key=lambda kv: -kv[1])[:2]
        if len(top2) == 2 and top2[1][1] >= 200:
            ia = views.index(top2[0][0]); ib = views.index(top2[1][0])
            col_a = af[tx[reg & (of[tx] == ia)]]
            col_b = af[tx[reg & (of[tx] == ib)]]
            ma = np.median(col_a, axis=0); mb = np.median(col_b, axis=0)
            de = float(np.linalg.norm(lab(ma[None, :]) - lab(mb[None, :])))
            seam = {"a": top2[0][0], "b": top2[1][0],
                    "a_px": top2[0][1], "b_px": top2[1][1],
                    "a_rgb255": [int(round(x * 255)) for x in ma],
                    "b_rgb255": [int(round(x * 255)) for x in mb],
                    "a_L": round(float(lab(ma[None, :])[0, 0]), 2),
                    "b_L": round(float(lab(mb[None, :])[0, 0]), 2),
                    "dE_median_colours": round(de, 2)}
            print("[e04]   ROI %s seam: %s rgb%s L*%.1f  vs  %s rgb%s L*%.1f   dE %.2f"
                  % (nm, seam["a"], tuple(seam["a_rgb255"]), seam["a_L"],
                     seam["b"], tuple(seam["b_rgb255"]), seam["b_L"], de), flush=True)
        r["rois"][nm] = {"px": int(reg.sum()), "classes": cls, "class_pct":
                         {k: round(100.0 * n / tot, 2) for k, n in cls.items()},
                         "owners": own_r, "seam": seam, "align": align(reg, "ROI " + nm)}

    Image.fromarray(rgb).save(os.path.join(args.out, "asset_%s.png" % tag))
    Image.fromarray(prov).save(os.path.join(args.out, "prov_%s.png" % tag))
    Image.fromarray(ownim).save(os.path.join(args.out, "owner_%s.png" % tag))
    hpv = np.clip(hp / 0.15, 0, 1)
    Image.fromarray((hpv * 255).astype(np.uint8)).save(
        os.path.join(args.out, "highpass_%s.png" % tag))
    ovr = rgb.copy()
    ovr[ob] = (255, 255, 0)
    ovr[cb] = (255, 0, 255)
    Image.fromarray(ovr).save(os.path.join(args.out, "overlay_%s.png" % tag))
    res_all[tag] = r

out["views"] = res_all
json.dump(out, open(os.path.join(args.out, "e04_blotch.json"), "w"), indent=1)
print("[e04] wrote %s" % os.path.join(args.out, "e04_blotch.json"), flush=True)
