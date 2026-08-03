"""Per-view foreshortening table for the HEAD region.

Reports the same statistic the character-1 table did: the fraction of visible head
surface whose normal is worse than 60 deg off the projection axis (facing < cos60 = 0.5).
That band is where the smear lives.

Head region = the mask band (default 288 px, matching build_masks.py) intersected with the
figure silhouette, so it means the same thing here as it does there.

  foreshorten_table.py --renders "dir/tex_{}.png" --facing dir --views 7,0,1 --label name
"""
import argparse
from pathlib import Path
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--renders", required=True)
ap.add_argument("--facing", required=True)
ap.add_argument("--views", default="7,0,1")
ap.add_argument("--band", type=int, default=288)
ap.add_argument("--label", default="")
args = ap.parse_args()

print(f"{args.label}")
print(f"{'view':>6} {'head px':>9} {'mean facing':>12} {'/255':>7} {'>60deg':>8} {'>80deg':>8}")
rows = []
for v in [int(x) for x in args.views.split(",")]:
    a = np.asarray(Image.open(args.renders.format(v)).convert("RGB"), dtype=np.int16)
    f = np.asarray(Image.open(Path(args.facing) / f"face_{v}.png").convert("L"), dtype=np.float32) / 255.0
    fig = np.abs(a - a[0, 0]).sum(-1) > 18
    band = np.zeros(a.shape[:2], bool)
    band[:args.band] = True
    head = band & fig
    fh = f[head]
    p60 = 100.0 * (fh < 0.5).mean()
    p80 = 100.0 * (fh < 0.17).mean()
    rows.append((v, head.sum(), fh.mean(), p60, p80))
    print(f"{v:>6} {head.sum():>9,} {fh.mean():>12.3f} {fh.mean()*255:>7.1f} {p60:>7.1f}% {p80:>7.1f}%")

d = {v: r for v, *r in [(r[0], *r[1:]) for r in rows]}
if 7 in d and 1 in d:
    a7, a1 = d[7][2], d[1][2]
    print(f"\n3/4 symmetry check: v7 {a7:.1f}%  vs  v1 {a1:.1f}%   delta {abs(a7-a1):.1f} pt")
    print("  (the facing chain is correct when a near-symmetric head gives these to ~1 pt)")
