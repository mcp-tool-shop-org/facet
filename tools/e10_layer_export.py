"""E10 - export the contact layer as an engine-legal RGBA, and build W3's toggle sheets.

THE FILE CONTRACT is RG02 Q2's, adopted whole by E10 Ruling 1 decision 4:
  8-bit RGBA PNG, same dimensions and same UV1 as the base atlas; RGB in sRGB; alpha
  linear and STRAIGHT (never premultiplied - PNG 3rd Ed. 6.2 says colour values are not
  premultiplied, and Godot's process/premult_alpha pairs only with BLEND_MODE_PREMULT_ALPHA).

ALPHA IS THE GEOMETRY'S (Ruling 1 decision 3). The layer's alpha is the contact mask
intersected with what was actually committed - not a model-generated matte. LayerDiffuse's
alpha is rim-good and interior-bad (Lu et al. 2026), so a generated matte would have been
unreliable exactly where a boot-top is solid.

THE DILATION IS A GATED EXPORT STEP (Ruling 1 decision 5). Colour is flooded outward under
transparent texels before export - the only mip-bleed mitigation both engines share, and
Godot documents no alpha-coverage mip preservation at all. Its gate has two halves, and
the second is the one that matters: THE RING MUST EXIST, and THE ALPHA MUST BE UNTOUCHED
BY IT. A dilation that moved alpha would silently widen the layer.

  e10_layer_export.py [--ring 8]
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt

Image.MAX_IMAGE_PIXELS = None
STROKE = r"E:\AI\training\facet_next\E04_stroke"
LAYER = os.path.join(STROKE, "e10_layer")
BASE = os.path.join(STROKE, "out", "galleon_final.png")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ring", type=int, default=8, help="dilation ring, texels")
    ap.add_argument("--out", default=LAYER)
    args = ap.parse_args()
    J = os.path.join
    rep = {}

    base = np.asarray(Image.open(BASE).convert("RGB"))
    lay = np.asarray(Image.open(J(LAYER, "state", "atlas.png")).convert("RGB"))
    contact = np.load(J(STROKE, "e10_contact", "contact_mask.npy"))
    seeded = np.asarray(np.load(J(LAYER, "state", "styled_mask.npy")))

    # WHAT THE LAYER OWNS (E10 Ruling 8, correcting this file's own defect).
    # It was `contact & changed-vs-base`, which is right ONLY when the layer state was
    # seeded as a copy of the base. Under W2c's hole-fill seed every contact texel differs
    # from the base before a single one is painted, so that predicate would have exported
    # 85,707 texels of flat rgb(107,107,107) fill as layer content - and the same mistake,
    # made in the measurement, first read W2c as L* 45.2 / dL* +37.3, the fill masquerading
    # as the paint. The owned set is what the COMMIT WROTE:
    owned = contact & seeded
    changed = np.any(base != lay, axis=-1)
    # ANCHOR: on a base-copy seed the two predicates coincide by construction, because a
    # texel is only unequal to the base if the commit wrote it. W2's path is already run,
    # so the correction is checked against it rather than merely reasoned about.
    coincide = int((owned ^ (contact & changed)).sum())
    rep["texels"] = {"contact": int(contact.sum()), "changed_vs_base": int(changed.sum()),
                     "owned_by_layer": int(owned.sum()),
                     "changed_outside_contact": int((changed & ~contact).sum()),
                     "predicate_disagreement": coincide}
    print("[layer] contact %d | owned (contact AND committed) %d | changed-vs-base %d | "
          "changed OUTSIDE contact %d" % (contact.sum(), owned.sum(), changed.sum(),
                                          (changed & ~contact).sum()))
    print("[layer] predicate check: old and new definitions disagree on %d texels %s"
          % (coincide, "(base-copy seed: they must coincide)" if coincide == 0
             else "(hole-fill seed: the old one would have exported the fill)"))
    # ANDON: the restrict flag promised nothing lands outside the contact mask
    if int((changed & ~contact).sum()) != 0:
        print("ANDON: the layer changed texels outside the contact mask. --restrict did "
              "not hold. HALT.")
        return 1

    # ---- the dilation, and its gate --------------------------------------------------
    rgb = lay.copy()
    alpha = (owned * 255).astype(np.uint8)
    dist, (iy, ix) = distance_transform_edt(~owned, return_indices=True)
    ring = (~owned) & (dist <= args.ring)
    rgb[ring] = lay[iy[ring], ix[ring]]
    alpha_after = (owned * 255).astype(np.uint8)
    ring_px = int(ring.sum())
    alpha_moved = int((alpha_after != alpha).sum())
    rep["dilation"] = {"ring_texels": args.ring, "ring_px": ring_px,
                       "alpha_px_moved": alpha_moved}
    print("[dilate] ring %d texels -> %d px flooded under transparent texels; alpha moved "
          "%d px" % (args.ring, ring_px, alpha_moved))
    if ring_px == 0:
        print("ANDON: the dilation produced no ring. HALT.")
        return 1
    if alpha_moved != 0:
        print("ANDON: the dilation moved alpha - it would silently widen the layer. HALT.")
        return 1

    out = np.dstack([rgb, alpha_after])
    lp = J(args.out, "layer_boottop.png")
    Image.fromarray(out, mode="RGBA").save(lp)
    m = Image.open(lp)
    rep["file"] = {"path": lp, "mode": m.mode, "size": list(m.size),
                   "bytes": os.path.getsize(lp)}
    print("[export] %s  %s %s  %.1f MB" % (os.path.basename(lp), m.mode, m.size,
                                           os.path.getsize(lp) / 1e6))
    if m.mode != "RGBA" or m.size != (base.shape[1], base.shape[0]):
        print("ANDON: the exported layer is not RGBA at the atlas's dimensions. HALT.")
        return 1

    # ---- the composite the engine would produce, built here so the toggle is honest ---
    comp = base.copy()
    a = alpha_after[..., None].astype(np.float32) / 255.0
    comp = (base.astype(np.float32) * (1 - a) + rgb.astype(np.float32) * a)
    comp = np.clip(comp + 0.5, 0, 255).astype(np.uint8)
    cp = J(args.out, "composite_atlas.png")
    Image.fromarray(comp).save(cp)
    # straight-alpha `over` onto an opaque base is exactly a select where alpha is 0/255
    if not np.array_equal(comp[owned], rgb[owned]) or not np.array_equal(
            comp[~owned], base[~owned]):
        print("ANDON: the composite is not `over` with straight alpha. HALT.")
        return 1
    print("[composite] %s  (straight-alpha over onto the opaque base, verified exact)"
          % os.path.basename(cp))

    json.dump(rep, open(J(args.out, "layer_export.json"), "w"), indent=1)
    print("[json] %s" % J(args.out, "layer_export.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
