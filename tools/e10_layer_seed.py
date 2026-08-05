"""E10 Step 0.3 (second half) - seed the layer state.

THE LAYER IS A SEPARATE STATE DIRECTORY. That is the whole of base-invariance: commit
writes only inside --state, so the accepted base atlas is never opened for writing at
all. Ruling 5: the risk is eliminated rather than gated, and --base-guard then proves
what the construction already guarantees.

WHAT THE SEED CONTAINS, and why each piece is what it is:
  atlas.png       a COPY of the accepted base atlas. The brush must see the ship to paint
                  a waterline onto it - a transparent void gives the model no context and
                  no registration. Reading canon and writing a copy elsewhere is not
                  opening canon for writing.
  holes.png       the contact mask. "Holes" is emit's word for the region to paint, so
                  the layer's paintable region IS the geometric band, and W2's job mask
                  falls out of the geometry rather than out of a prompt.
  styled_mask.npy its complement inside the uv-valid set: everything outside the band is
                  already-painted as far as the layer is concerned.

ALPHA IS NOT CARRIED THROUGH PAINTING (Ruling 1 decision 3). The working layer atlas is
RGB. The layer's alpha is the contact mask intersected with what was actually committed,
applied at EXPORT - because a boot-top's top edge is a painted hard line and the geometry
already knows where it is. No model-generated alpha in v1.

ANCHOR: a layer no-op leaves base and layer byte-identical.

  e10_layer_seed.py [--out DIR] [--force]
"""
import argparse
import hashlib
import json
import os
import shutil
import sys

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
STROKE = r"E:\AI\training\facet_next\E04_stroke"
PREP = r"E:\AI\training\facet_next\E04_shipprep"
BASE_ATLAS = os.path.join(STROKE, "out", "galleon_final.png")
CONTACT = os.path.join(STROKE, "e10_contact", "contact_mask.npy")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(STROKE, "e10_layer"))
    ap.add_argument("--force", action="store_true", help="re-seed an existing state")
    args = ap.parse_args()
    J = os.path.join
    st = J(args.out, "state")
    if os.path.exists(st) and not args.force:
        print("ANDON: %s already exists. Re-seeding would discard committed layer work; "
              "pass --force only if that is what you mean." % st)
        return 1
    os.makedirs(st, exist_ok=True)

    base_sha_before = sha256(BASE_ATLAS)
    print("[base] galleon_final.png %s" % base_sha_before)

    contact = np.load(CONTACT)
    uv = np.asarray(np.load(J(PREP, "mask.npy"), mmap_mode="r")[..., 0]) > 0.5

    shutil.copyfile(BASE_ATLAS, J(st, "atlas.png"))
    Image.fromarray((contact * 255).astype(np.uint8)).save(J(st, "holes.png"))
    np.save(J(st, "styled_mask.npy"), uv & ~contact)

    # ---- ANCHOR: the base is byte-identical after the seed ---------------------------
    base_sha_after = sha256(BASE_ATLAS)
    if base_sha_before != base_sha_after:
        print("ANDON: the base atlas changed during the seed. HALT.")
        return 1

    # ---- ANCHOR: a no-op leaves the layer byte-identical -----------------------------
    # Seeding twice from the same inputs must produce the same bytes; if it does not, the
    # layer state is not a function of (base, mask) and no later invariance claim holds.
    probe = J(args.out, "_probe")
    os.makedirs(probe, exist_ok=True)
    shutil.copyfile(BASE_ATLAS, J(probe, "atlas.png"))
    Image.fromarray((contact * 255).astype(np.uint8)).save(J(probe, "holes.png"))
    np.save(J(probe, "styled_mask.npy"), uv & ~contact)
    same = all(sha256(J(st, f)) == sha256(J(probe, f))
               for f in ("atlas.png", "holes.png", "styled_mask.npy"))
    shutil.rmtree(probe)
    if not same:
        print("ANDON: the layer seed is not a pure function of its inputs. HALT.")
        return 1
    print("[anchor] re-seed byte-identical: True")

    meta = {
        "seeded": "E10 Step 0.3",
        "base_atlas": BASE_ATLAS,
        "base_atlas_sha256": base_sha_before,
        "base_guard_arg": "%s:%s" % (BASE_ATLAS, base_sha_before),
        "contact_mask": CONTACT,
        "contact_texels": int(contact.sum()),
        "alpha": "NOT carried through painting. The layer's alpha is the contact mask "
                 "intersected with what was committed, applied at export (Ruling 1 "
                 "decision 3: a boot-top's top edge is a painted hard line and the "
                 "geometry already knows where it is).",
        "base_invariance": "STRUCTURAL. commit writes only inside --state; the base atlas "
                           "is never opened for writing. --base-guard proves it.",
    }
    json.dump(meta, open(J(args.out, "layer_state.json"), "w"), indent=1)
    print("[seed] %s" % st)
    print("       atlas.png (base copy for context) | holes.png (%d contact texels) | "
          "styled_mask.npy" % contact.sum())
    print("[guard] pass to every layer commit:")
    print("        --base-guard \"%s:%s\"" % (BASE_ATLAS, base_sha_before))
    print("        --restrict \"%s\"" % CONTACT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
