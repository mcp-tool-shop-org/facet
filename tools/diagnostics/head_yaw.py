"""Locate the direction a MESH's head actually faces, by mirror symmetry.

Why this exists: the 8-direction convention assumes view 0 shows the head square-on. If
the mesh generator yawed the head relative to the body (measured on Salt Road character 2),
then view 0's "front" head is really a 3/4 head -- and the facing-chain correctness signal
("the two 3/4 views agree to ~1 pt") fails for a reason that has nothing to do with the
facing chain. So measure the yaw before trusting any per-view head statistic.

Method: a head is bilaterally symmetric. Crop the head from each rendered view, mirror it,
and score the disagreement. The view minimising it is the head's own axis (front or back;
disambiguate by which has more figure area forward of the crown, or just by eye).

Uses the CLAY render: texture would let albedo asymmetry (a parting, a shadow) outvote
geometry.

  head_yaw.py --glob "dir/clay_{}.png" --views 0,1,2,3,4,5,6,7
"""
import argparse
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--glob", required=True)
ap.add_argument("--views", default="0,1,2,3,4,5,6,7")
ap.add_argument("--head-frac", type=float, default=0.19)
ap.add_argument("--pad-up", type=float, default=0.02)
ap.add_argument("--bg-tol", type=float, default=18.0)
ap.add_argument("--out", default=None, help="optional mirror-overlay sheet")
args = ap.parse_args()

idxs = [int(v) for v in args.views.split(",")]
rows, overlays = [], []
for i in idxs:
    im = Image.open(args.glob.format(i)).convert("L")
    a = np.asarray(im).astype(np.float32)
    corner = a[:12, :12].mean()
    fig = np.abs(a - corner) > args.bg_tol
    r = np.where(fig.any(axis=1))[0]
    top, bot = r[0], r[-1]
    fh = bot - top
    y0 = max(0, int(top - args.pad_up * fh))
    y1 = int(top + args.head_frac * fh)
    band = fig[y0:y1]
    c = np.where(band.any(axis=0))[0]
    x0, x1 = c[0], c[-1]
    # centre the crop on the head's own silhouette so the mirror axis is the head's,
    # not the frame's
    head = a[y0:y1, x0:x1 + 1]
    m = fig[y0:y1, x0:x1 + 1]
    w = head.shape[1]
    if w % 2:
        head, m = head[:, :-1], m[:, :-1]
    mir = head[:, ::-1]
    mmir = m[:, ::-1]
    both = m & mmir
    # silhouette disagreement: fraction of head pixels with no mirror partner
    sil = 100.0 * (m ^ mmir).sum() / max(m.sum(), 1)
    # shading disagreement over the pixels present in both
    sh = float(np.abs(head - mir)[both].mean()) if both.sum() else 999.0
    rows.append((i, sil, sh, m.sum()))
    overlays.append((i, m, mmir))

print(f"{'view':>5} {'yaw':>6} {'silhouette_asym%':>18} {'shading_asym':>13}")
for i, sil, sh, n in rows:
    print(f"{i:>5} {i*45:>5}d {sil:>18.2f} {sh:>13.2f}")

best_sil = min(rows, key=lambda r: r[1])
best_sh = min(rows, key=lambda r: r[2])
print(f"\nmost symmetric by silhouette: view {best_sil[0]} ({best_sil[0]*45} deg), {best_sil[1]:.2f}%")
print(f"most symmetric by shading   : view {best_sh[0]} ({best_sh[0]*45} deg), {best_sh[2]:.2f}")
print("\nread: if the head were square to the body, views 0 and 4 would BOTH be near-minimal")
print("      and 2/6 maximal. A minimum sitting at 1/7 (or 3/5) means the head is yawed")
print("      ~45 deg toward that view.")
