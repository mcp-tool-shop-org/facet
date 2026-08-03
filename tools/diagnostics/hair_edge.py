"""Extract the mesh's OWN hair/face boundary as a control hint.

Why this exists (measured 2026-08-02, Salt Road character 2): the restylize invents its own
hair boundary, which does not agree with the mesh's hair GEOMETRY, so on re-projection
hair-coloured pixels land on face surface — a dark smear across the cheek. The existing canny
branch does carry this edge, but it is released at 45% of denoising, after which the model is
free to move the boundary.

The fix this feeds: a SECOND control branch, hair edge only, held to end_percent 1.0. One
branch frees the surface, the other pins the one edge that must not move.

The hair mask is taken from the VOLUME-BAKED render, NOT from a restylized view or the
concept projection — the volume bake is the mesh's own colour, so its hair region is
registered to the hair geometry BY CONSTRUCTION. That is the whole point; a mask from any
generated image would carry the same disagreement we are trying to remove.

  hair_edge.py --render vol_0.png --out-edge edge_0.png [--out-mask mask_0.png]
               [--band 260] [--v-thresh 90] [--dilate 2]
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("--render", required=True, help="the VOLUME-BAKED view render")
ap.add_argument("--out-edge", required=True)
ap.add_argument("--out-mask", default=None)
ap.add_argument("--band", type=int, default=260,
                help="rows [0,band) searched for hair; the head sits in the top ~250px "
                     "of the 1024px frame at our standard framing")
ap.add_argument("--v-thresh", type=int, default=90,
                help="max V (of HSV, 0-255) counted as hair. Hair is the darkest thing on "
                     "the head; skin and the cream collar are far brighter.")
ap.add_argument("--bg-tol", type=float, default=18.0)
ap.add_argument("--dilate", type=int, default=2, help="thicken the edge so the control sees it")
ap.add_argument("--crop-w", type=int, default=752)
args = ap.parse_args()

im = Image.open(args.render).convert("RGB")
a = np.asarray(im).astype(np.float32)
corner = a[:12, :12].reshape(-1, 3).mean(axis=0)
fig = np.abs(a - corner).max(axis=-1) > args.bg_tol

hsv = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2HSV)
v = hsv[..., 2].astype(np.int16)

band = np.zeros(a.shape[:2], bool)
band[:args.band] = True
hair = band & fig & (v < args.v_thresh)

# largest connected component only — kills speckle in shadowed collar folds
n, lab, stats, _ = cv2.connectedComponentsWithStats(hair.astype(np.uint8), 8)
if n > 1:
    biggest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    hair = lab == biggest
hair_u8 = (hair.astype(np.uint8)) * 255
hair_u8 = cv2.morphologyEx(hair_u8, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
hair_u8 = cv2.morphologyEx(hair_u8, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

edge = cv2.Canny(hair_u8, 50, 150)
if args.dilate:
    edge = cv2.dilate(edge, np.ones((args.dilate * 2 + 1,) * 2, np.uint8))


def crop(arr):
    dx = (arr.shape[1] - args.crop_w) // 2
    return arr[:, dx:dx + args.crop_w]


Image.fromarray(np.dstack([crop(edge)] * 3), mode="RGB").save(args.out_edge)
if args.out_mask:
    Image.fromarray(np.dstack([crop(hair_u8)] * 3), mode="RGB").save(args.out_mask)

hp = hair.sum()
print(f"[hair] {hp:,} px ({100*hp/max(fig[:args.band].sum(),1):.1f}% of the head band's figure)")
print(f"[edge] {int((edge > 0).sum()):,} edge px")
print(f"[out ] {args.out_edge}" + (f"  {args.out_mask}" if args.out_mask else ""))
