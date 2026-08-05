"""E10 W2d - paste a projected twin into the layer state, under the contact mask only.

E10 Ruling 8 routed the layer's content back through the mode this repo already measured:
full-frame twin generation, where a prompt term competes as an OCCUPANT rather than as an
addition onto occupied surface. The twin is then projected by `project_twins.py` - the
stage-1 tool, unchanged - and THIS step takes only the texels the contact mask allows.

BASE-INVARIANCE IS STRUCTURAL AND PROVEN. The base atlas is read and never written; its
sha256 is asserted before and after, inside this tool, with no skip flag.

  e10_layer_paste.py --proj PROJ.png [--out DIR]
"""
import argparse
import hashlib
import json
import os
import sys

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
STROKE = r"E:\AI\training\facet_next\E04_stroke"
PREP = r"E:\AI\training\facet_next\E04_shipprep"
BASE = os.path.join(STROKE, "out", "galleon_final.png")
CONTACT = os.path.join(STROKE, "e10_contact", "contact_mask.npy")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--proj", required=True, help="project_twins output atlas")
    ap.add_argument("--out", default=os.path.join(STROKE, "e10_layer"))
    args = ap.parse_args()
    J = os.path.join
    st = J(args.out, "state")

    before = sha256(BASE)
    print("[guard] base %s" % before)

    base = np.asarray(Image.open(BASE).convert("RGB"))
    proj = np.asarray(Image.open(args.proj).convert("RGB"))
    pstyled = np.load(args.proj.replace(".png", "_styled_mask.npy"))
    contact = np.load(CONTACT)
    uv = np.asarray(np.load(J(PREP, "mask.npy"), mmap_mode="r")[..., 0]) > 0.5

    paste = contact & pstyled
    rep = {"contact": int(contact.sum()), "projection_styled": int(pstyled.sum()),
           "pasted": int(paste.sum()),
           "contact_reached_pct": 100.0 * paste.sum() / contact.sum(),
           "projection_outside_contact_discarded": int((pstyled & ~contact).sum())}
    print("[paste] contact %d | projection styled %d | PASTED %d (%.1f%% of the band) | "
          "discarded outside the band %d"
          % (contact.sum(), pstyled.sum(), paste.sum(),
             rep["contact_reached_pct"], (pstyled & ~contact).sum()))
    if paste.sum() == 0:
        print("ANDON: the projection reached none of the contact band. HALT.")
        return 1

    atlas = base.copy()
    atlas[paste] = proj[paste]
    Image.fromarray(atlas).save(J(st, "atlas.png"))
    np.save(J(st, "styled_mask.npy"), (uv & ~contact) | paste)
    Image.fromarray((contact * 255).astype(np.uint8)).save(J(st, "holes.png"))

    after = sha256(BASE)
    if before != after:
        print("ANDON: the base atlas changed. HALT.")
        return 1
    print("[guard] base byte-identical after the paste: True")
    json.dump(rep, open(J(args.out, "w2d_paste.json"), "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
