"""E08 Amendment 29 — WHAT are the background-flagged rim texels?

The branch decider. The gained band's flagged subsets are either (A) the subject's own grey
materials at their own locations — steel blade, dark boots, which are background-like BY
CONSTRUCTION (§9a: blade paint at median residual 0.0657 from the backdrop; C* 1.6-2.8) — or
(B) backdrop tone mixed in along the rim of materials that are not grey at all.

A background-dE test cannot tell those apart, and neither can chroma alone: the palette gate's
own chroma floor (12.0) exists precisely because steel is neutral, so "below the floor" covers
grey material AND grey backdrop mix identically. Two things do separate them:

  LOCATION — the blade band (§9a's largest uncovered component) and the boots (bottom of the
             figure) are where grey material legitimately lives. Gold pauldrons, a green tunic
             and a wine-red skirt are not grey anywhere.

  WHAT THE RIM SITS ON — for each flagged texel, the twin's colour at its NEAREST DEEP pixel
             (trust-mask interior, past the whole 5.36px band). If the material a few px inboard
             is chromatic and in-palette, a neutral rim pixel on it is a MIX. If the material
             inboard is itself neutral, the rim pixel is that material. Direction-free, computed
             with one EDT that returns indices, so it cannot pick a bad normal.

Palette bands, min_chroma and the forbidden ranges are read from the pre-registered gate file —
declared from the spec's sixteen materials and cross-checked against a DIFFERENT image than the
twins, so this is not circular.

  flagged_identity.py --r0 diag_8cam_noTI.npz --r1 diag_8cam.npz --twins DIR
                      --palette docs/experiments/E08-W3-palette.json --view 6 [--out-json j]
"""
import argparse
import json
import os

import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt, label

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--r0", required=True)
ap.add_argument("--r1", required=True)
ap.add_argument("--twins", required=True)
ap.add_argument("--palette", required=True)
ap.add_argument("--view", type=int, default=6)
ap.add_argument("--step", type=float, default=45.0)
ap.add_argument("--pattern", default="twin_{k}.png")
ap.add_argument("--bg-de", type=float, default=10.0)
ap.add_argument("--deep-px", type=float, default=8.0,
                help="a pixel is DEEP if its trust-mask distance is at least this. 8 clears "
                     "the whole 2.74-5.36px gained band with margin.")
ap.add_argument("--boot-frac", type=float, default=0.85,
                help="height fraction below which the figure is boots, per the spec's "
                     "'heavy dark boots'. Reported, not gated.")
ap.add_argument("--out-json")
args = ap.parse_args()

PAL = json.load(open(args.palette))
MINC = float(PAL["min_chroma"])
BANDS = [(b["name"], float(b["hue_deg"][0]), float(b["hue_deg"][1]))
         for b in PAL["allowed_bands"]]
print(f"palette: min_chroma {MINC}  bands " +
      "  ".join(f"{n} {a:.0f}-{b:.0f}" for n, a, b in BANDS))

Z0 = np.load(args.r0, allow_pickle=False)
Z1 = np.load(args.r1, allow_pickle=False)
views = [str(x) for x in Z1["__views__"]]
nm = next(v for v in views if int(round(float(v[1:]) / args.step)) == args.view)
print(f"view {args.view} -> {nm}\n")


def srgb_to_lab(rgb):
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16, 500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


def lch(lab):
    C = np.hypot(lab[..., 1], lab[..., 2])
    h = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360.0
    return lab[..., 0], C, h


def classify(C, h):
    """below the floor -> unconstrained; else in a declared band or off-palette."""
    out = np.full(len(C), "offpalette", dtype=object)
    out[C <= MINC] = "neutral(below floor)"
    for name, a, b in BANDS:
        out[(C > MINC) & (h >= a) & (h <= b)] = f"in-palette:{name}"
    return out


def fitted_field(img):
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    ring = np.zeros((H, W), dtype=bool)
    b = 24
    ring[:b, :] = ring[-b:, :] = ring[:, :b] = ring[:, -b:] = True
    cols = [np.ones(H * W), xx.ravel() / W, yy.ravel() / H,
            (xx.ravel() / W) ** 2, (yy.ravel() / H) ** 2,
            (xx.ravel() / W) * (yy.ravel() / H)]
    A = np.stack(cols, axis=1)
    Xr = A.reshape(H, W, -1)[ring]
    fld = np.zeros((H, W, 3), dtype=np.float32)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(Xr, img[..., c][ring], rcond=None)
        fld[..., c] = (A @ coef).reshape(H, W)
    return fld


def bilinear(img, x, y):
    H, W = img.shape[:2]
    x = np.clip(x, 0.0, W - 1.001)
    y = np.clip(y, 0.0, H - 1.001)
    x0, y0 = x.astype(np.int64), y.astype(np.int64)
    fx, fy = (x - x0)[:, None], (y - y0)[:, None]
    a, b_, c, d = img[y0, x0], img[y0, x0 + 1], img[y0 + 1, x0], img[y0 + 1, x0 + 1]
    if a.ndim == 1:
        fx, fy = fx[:, 0], fy[:, 0]
    return a * (1 - fx) * (1 - fy) + b_ * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy


k = args.view
img = np.asarray(Image.open(os.path.join(args.twins, args.pattern.format(k=k))
                            ).convert("RGB"), dtype=np.float32) / 255.0
mesh = Z1[f"{nm}/mesh_fm"]
twin = Z1[f"{nm}/twin_fm"]
trust = twin & mesh
dist = distance_transform_edt(trust).astype(np.float32)
corner = np.median(np.concatenate([img[:8, :8].reshape(-1, 3),
                                   img[:8, -8:].reshape(-1, 3)]), axis=0)
FLD = fitted_field(img)

# the §9a blade band: the largest region of surface the key does NOT cover
lab_u, n_u = label(mesh & ~twin)
blade = lab_u == (int(np.argmax(np.bincount(lab_u.ravel())[1:])) + 1)
d_blade = distance_transform_edt(~blade).astype(np.float32)
ys_m = np.where(mesh.any(axis=1))[0]
y0, y1 = int(ys_m.min()), int(ys_m.max())

# WHAT THE RIM SITS ON: nearest deep pixel, by EDT indices. Direction-free.
deep = trust & (dist >= args.deep_px)
assert deep.any(), "ANDON: no deep trust-mask pixels — cannot identify the underlying material"
_, inds = distance_transform_edt(~deep, return_indices=True)
deep_col = img[inds[0], inds[1]]                 # per-pixel: colour of nearest deep pixel
deep_dist = distance_transform_edt(~deep).astype(np.float32)

px, py = Z1[f"{nm}/px"], Z1[f"{nm}/py"]
a0, a1 = Z0[f"{nm}/accepted"], Z1[f"{nm}/accepted"]
gained = a1 & ~a0
col = bilinear(img, px, py).astype(np.float32)
L = srgb_to_lab(col)
dE_corner = np.linalg.norm(L - srgb_to_lab(corner[None, :]), axis=-1)
dE_fitted = np.linalg.norm(L - srgb_to_lab(bilinear(FLD, px, py).astype(np.float32)), axis=-1)

SETS = {
    "gained (all)": gained,
    "gained & CORNER-flagged": gained & (dE_corner < args.bg_de),
    "gained & FITTED-flagged": gained & (dE_fitted < args.bg_de),
    "gained & BOTH-flagged": gained & (dE_corner < args.bg_de) & (dE_fitted < args.bg_de),
}

out = {"view": args.view, "min_chroma": MINC, "bg_de": args.bg_de,
       "deep_px": args.deep_px, "corner_rgb": [int(c * 255) for c in corner], "sets": {}}

for tag, sel in SETS.items():
    n = int(sel.sum())
    print("=" * 78)
    print(f"{tag}  —  n = {n:,}")
    print("=" * 78)
    if not n:
        continue
    pyi = np.clip(py[sel].round().astype(int), 0, mesh.shape[0] - 1)
    pxi = np.clip(px[sel].round().astype(int), 0, mesh.shape[1] - 1)
    Ls, Cs, hs = lch(L[sel])
    cls = classify(Cs, hs)
    # (b) IDENTITY — of the flagged pixel itself
    print(f"  the flagged pixel itself:  L* median {np.median(Ls):.1f}  "
          f"C* median {np.median(Cs):.1f}  ({float((Cs <= MINC).mean())*100:.1f}% below the "
          f"chroma floor, where hue is not a colour)")
    u, c_ = np.unique(cls, return_counts=True)
    for uu, cc in sorted(zip(u, c_), key=lambda t: -t[1]):
        print(f"      {uu:<24s} {cc:>7,}  {cc/n*100:5.1f}%")
    # WHAT IT SITS ON — nearest deep pixel's colour
    dc = deep_col[pyi, pxi]
    Ld, Cd, hd = lch(srgb_to_lab(dc))
    cls_d = classify(Cd, hd)
    print(f"  the material {args.deep_px:.0f}px+ INBOARD (nearest deep pixel, median "
          f"{np.median(deep_dist[pyi, pxi]):.1f}px away):")
    print(f"      L* median {np.median(Ld):.1f}  C* median {np.median(Cd):.1f}  "
          f"({float((Cd <= MINC).mean())*100:.1f}% below the floor)")
    ud, cd_ = np.unique(cls_d, return_counts=True)
    for uu, cc in sorted(zip(ud, cd_), key=lambda t: -t[1]):
        print(f"      {uu:<24s} {cc:>7,}  {cc/n*100:5.1f}%")
    chromatic_under = float(((Cd > MINC)).mean()) * 100
    print(f"  --> sits on CHROMATIC in-palette material: {chromatic_under:5.1f}%   "
          f"on NEUTRAL material: {100-chromatic_under:5.1f}%")
    # (a) LOCATION
    hf = (py[sel] - y0) / max(y1 - y0, 1)
    db = d_blade[pyi, pxi]
    print(f"  location: height fraction median {np.median(hf):.3f}   "
          f"in boots (>{args.boot_frac}) {float((hf > args.boot_frac).mean())*100:.1f}%")
    print(f"            distance to the §9a blade band: median {np.median(db):.0f}px   "
          f"within 5px {float((db <= 5).mean())*100:.1f}%   within 20px "
          f"{float((db <= 20).mean())*100:.1f}%")
    out["sets"][tag] = {
        "n": n,
        "self_L_median": round(float(np.median(Ls)), 1),
        "self_C_median": round(float(np.median(Cs)), 1),
        "self_pct_below_floor": round(float((Cs <= MINC).mean()) * 100, 1),
        "self_classes": {str(uu): int(cc) for uu, cc in zip(u, c_)},
        "inboard_L_median": round(float(np.median(Ld)), 1),
        "inboard_C_median": round(float(np.median(Cd)), 1),
        "inboard_pct_below_floor": round(float((Cd <= MINC).mean()) * 100, 1),
        "inboard_classes": {str(uu): int(cc) for uu, cc in zip(ud, cd_)},
        "pct_on_chromatic_material": round(chromatic_under, 1),
        "height_fraction_median": round(float(np.median(hf)), 3),
        "pct_in_boots": round(float((hf > args.boot_frac).mean()) * 100, 1),
        "blade_dist_median_px": round(float(np.median(db)), 0),
        "pct_within_5px_of_blade": round(float((db <= 5).mean()) * 100, 1),
        "pct_within_20px_of_blade": round(float((db <= 20).mean()) * 100, 1)}

print("\n" + "=" * 78)
print("The branch turns on 'sits on CHROMATIC in-palette material' for the FITTED set:")
print("  high  -> the rim is gold/green/red mixed toward the backdrop  = Branch B (mix)")
print("  low   -> the rim is grey material being grey                  = Branch A (subject)")
print("The reading is the advisor's; this tool reports the two candidate identities' evidence.")

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
    print(f"\n[identity] wrote {args.out_json}")
