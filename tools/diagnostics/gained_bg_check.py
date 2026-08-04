"""E08 Amendment 28 Ruling 2 — did the intersection's GAINED texels admit background?

The standing rule: when you widen an acceptance mask, test that you did not admit background.
On eight cameras the intersection tightens five views and LOOSENS three — 9,053 gained samples
(8,920 on view 6, 87 on view 5, 46 on view 1) — because removing off-surface paint narrowed
`fig_w`, which scales `ed_body` globally in --edge-absolute mode. View 6's erosion fell from
5.36 px to 2.74 px. That is a widening, so it gets A2's check.

A2's construction, reproduced exactly for comparability: median CIE76 dE from the twin's
background colour, and the fraction within dE 10, reported against the texels that would have
been accepted anyway — a set already trusted in the SAME image rather than an invented
absolute. A2's ratified numbers were 257,506 admitted at median dE 38.31 with 0.18% inside
dE 10, against 0.32% for the already-trusted set.

Two background references, because A2's is not the better one and the difference is itself
evidence:
  CORNER  — the 8x8 corner median, exactly what project_twins' probe uses. Comparable to A2.
  FITTED  — the per-pixel quadratic ring fit, evaluated at each sample's own position. A
            diffusion backdrop has a gradient, so a single corner colour misstates the
            backdrop near the feet, which is precisely where the gained texels are.

The normative control is view 2 (Amendment 28): a 275-px-wide profile whose NATIVE erosion is
2.75 px — the same width and the same threshold view 6 arrives at after the correction. So
"what does a legitimately-2.75px-eroded profile accept" has an answer measured on a different
view than the one being judged.

  gained_bg_check.py --r0 diag_8cam_noTI.npz --r1 diag_8cam.npz --twins DIR
                     [--control 2] [--bg-de 10.0] [--max-pct 2.0] [--out-json j]
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--r0", required=True, help="dump WITHOUT --trust-intersect")
ap.add_argument("--r1", required=True, help="dump WITH --trust-intersect")
ap.add_argument("--twins", required=True)
ap.add_argument("--pattern", default="twin_{k}.png")
ap.add_argument("--step", type=float, default=45.0)
ap.add_argument("--control", type=int, default=2,
                help="view index whose accepted set is the normative control")
ap.add_argument("--bg-de", type=float, default=10.0,
                help="CIE76 dE below which a colour counts as the twin's background. 10 is "
                     "the external constant for 'plainly different colour'.")
ap.add_argument("--max-pct", type=float, default=2.0,
                help="ANDON: the shipped --bg-max-pct from project_twins, declared and "
                     "reasoned in that source BEFORE this run — A2's ratified relaxation "
                     "measured 0.18% against 0.32% for the already-trusted set, so 2% is "
                     "an order of magnitude above work already accepted. Not a number "
                     "chosen here.")
ap.add_argument("--out-json")
args = ap.parse_args()

Z0 = np.load(args.r0, allow_pickle=False)
Z1 = np.load(args.r1, allow_pickle=False)
views = [str(x) for x in Z0["__views__"]]
assert not bool(Z0["__trust_intersect__"]), "ANDON: --r0 has the intersection ON"
assert bool(Z1["__trust_intersect__"]), "ANDON: --r1 has the intersection OFF"


def srgb_to_lab(rgb):
    """project_twins' converter, verbatim. dE below is CIE76."""
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16, 500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


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


def fitted_bg_field(img):
    """The per-channel quadratic ring fit — the backdrop MODEL, evaluated everywhere."""
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


def view_index(nm):
    """'y+270.0' -> 6"""
    return int(round(float(nm[1:]) / args.step))


IMG, BGC, FLD = {}, {}, {}
for nm in views:
    k = view_index(nm)
    p = os.path.join(args.twins, args.pattern.format(k=k))
    img = np.asarray(Image.open(p).convert("RGB"), dtype=np.float32) / 255.0
    IMG[nm] = img
    BGC[nm] = np.median(np.concatenate([img[:8, :8].reshape(-1, 3),
                                        img[:8, -8:].reshape(-1, 3)]), axis=0)
    FLD[nm] = fitted_bg_field(img)


def stats(nm, sel_mask, Z):
    """dE-from-background stats for a selected subset of a view's candidate samples."""
    px, py = Z[f"{nm}/px"][sel_mask], Z[f"{nm}/py"][sel_mask]
    if not len(px):
        return None
    col = bilinear(IMG[nm], px, py).astype(np.float32)
    lab = srgb_to_lab(col)
    d_corner = np.linalg.norm(lab - srgb_to_lab(BGC[nm][None, :]), axis=-1)
    fl = bilinear(FLD[nm], px, py).astype(np.float32)
    d_fitted = np.linalg.norm(lab - srgb_to_lab(fl), axis=-1)
    return {"n": int(len(px)),
            "corner_median_dE": round(float(np.median(d_corner)), 2),
            "corner_pct_within": round(float((d_corner < args.bg_de).mean() * 100), 3),
            "fitted_median_dE": round(float(np.median(d_fitted)), 2),
            "fitted_pct_within": round(float((d_fitted < args.bg_de).mean() * 100), 3)}


def show(label, s):
    if s is None:
        print(f"    {label:<34s} (empty)")
        return
    print(f"    {label:<34s} n {s['n']:>8,}   CORNER median dE {s['corner_median_dE']:>6.2f}  "
          f"within dE{args.bg_de:.0f} {s['corner_pct_within']:>6.3f}%   |   FITTED median dE "
          f"{s['fitted_median_dE']:>6.2f}  within {s['fitted_pct_within']:>6.3f}%")


# ---- the normative control: the control view's accepted set at its NATIVE erosion
ctrl_nm = next((nm for nm in views if view_index(nm) == args.control), None)
assert ctrl_nm, f"ANDON: control view {args.control} not in this dump"
ctrl = stats(ctrl_nm, Z1[f"{ctrl_nm}/accepted"], Z1)
print(f"NORMATIVE CONTROL — view {args.control} ({ctrl_nm}), accepted at its native "
      f"ed {float(np.max(Z1[f'{ctrl_nm}/ed'])):.2f}px")
show("accepted (control view)", ctrl)

out = {"bg_de": args.bg_de, "max_pct": args.max_pct, "control_view": args.control,
       "control": ctrl, "views": {}}
worst = 0.0
worst_nm = None
tot_gained = 0
for nm in views:
    a0, a1 = Z0[f"{nm}/accepted"], Z1[f"{nm}/accepted"]
    gained = a1 & ~a0
    ng = int(gained.sum())
    if not ng:
        continue
    tot_gained += ng
    ed0, ed1 = float(np.max(Z0[f"{nm}/ed"])), float(np.max(Z1[f"{nm}/ed"]))
    print(f"\nVIEW {nm} — GAINED {ng:,} samples   ed {ed0:.2f} -> {ed1:.2f}px")
    g = stats(nm, gained, Z1)
    kept = a1 & a0
    show("GAINED (newly admitted)", g)
    show("already trusted, same image", stats(nm, kept, Z1))
    out["views"][nm] = {"gained": ng, "ed_before": round(ed0, 2), "ed_after": round(ed1, 2),
                        "gained_stats": g,
                        "already_trusted_stats": stats(nm, kept, Z1)}
    for key, lbl in (("corner_pct_within", "CORNER"), ("fitted_pct_within", "FITTED")):
        if g[key] > worst:
            worst, worst_nm = g[key], f"{nm} ({lbl})"

print(f"\n{'='*78}")
print(f"total gained across views: {tot_gained:,}")
print(f"worst 'within dE {args.bg_de:.0f} of background' among gained sets: "
      f"{worst:.3f}%  [{worst_nm}]")
print(f"pre-registered bound (project_twins --bg-max-pct): {args.max_pct:.1f}%")
out["total_gained"] = tot_gained
out["worst_pct_within"] = round(worst, 3)
out["worst_view"] = worst_nm
out["verdict_vs_pre_registered_bound"] = "within" if worst <= args.max_pct else "OVER"
if worst > args.max_pct:
    print(f"\n!! OVER THE BOUND. Reporting, not proceeding — the gained texels are "
          f"approaching the twin's background, which would implicate width-scaled erosion "
          f"generally rather than just this view.")
else:
    print(f"\n   within the bound.")
print("   The bound is the SHIPPED --bg-max-pct, reasoned in project_twins before this run.")
print("   Whether the atlas is banked is the advisor's ruling, not this tool's.")

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
    print(f"\n[gained] wrote {args.out_json}")
