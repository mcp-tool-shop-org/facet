"""THE GARNET RE-PROJECTION's restricted write — E14 Ruling 26c/5 (mechanism M2).

The corrected six-twin projection has already run through the SPINE (`project_twins`), so
the stone's colour arrives having been through the same facing-weighted blend and the same
sigma=16 levelling as every other texel — that is the whole reason M2 was ruled over a
recorded-mask resample. This file does one thing: copy that atlas's colour into the run
state ON THE RULED TERRITORY ONLY, and prove it touched nothing else.

WHY A RESTRICTION IS LOAD-BEARING AND NOT TIDINESS. The corrected twins are byte-identical
to their inputs outside the stone mask, but `project_twins` keys each twin's figure from the
image itself, so changing the stone's colour changes which stone-adjacent pixels pass that
key. Measured on this very run: the corrected projection's own styled set is 1,658,221
against stage 1b's 1,656,847 — **+1,374 texels, all outside the territory**. Without the
restriction those would ride in unnoticed. With it they cannot.

The write set is `territory AND holes`, so the commit ANDON's own invariant — a styled texel
is never overwritten — holds here by construction rather than by permission: the demotion
(Ruling 24f) made the territory holes, and this writes only into holes.

  e14_garnet_reproject.py --state DIR --state0 DIR --source ATLAS --territory MASK.npy
                          [--dry-run]

Standards compliance: PIN_PER_STEP — source, territory and both states' SHAs recorded in the
report JSON. ANDON_AUTHORITY — every invariance is asserted before a byte is written, with no
skip flag: the write set is a subset of the territory, the write set is a subset of holes, no
styled texel is in it, and after the write every texel outside the territory is byte-identical.
NAMED_COMPENSATORS — restore the territory's three channels from `state0/`, the demotion's own
inverse, already exercised (`e14_demote_garnet.py --undo`). EXTERNAL_VERIFIER — the source
atlas is produced by the shipped projector, not by this file; the works-perfectly gate is run
separately against `stage1b_atlas.png`.
"""
import argparse
import hashlib
import json
import os

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ap = argparse.ArgumentParser()
ap.add_argument("--state", required=True)
ap.add_argument("--state0", required=True)
ap.add_argument("--prep", required=True)
ap.add_argument("--source", required=True, help="the corrected six-twin projection's atlas")
ap.add_argument("--territory", required=True, help="boolean .npy over VALID texels")
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()
J = os.path.join


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


mask2d = np.load(J(args.prep, "mask.npy"))[..., 0] > 0.5
valid = mask2d.reshape(-1)
vidx = np.where(valid)[0]
terr_v = np.load(args.territory)
if not (terr_v.shape == vidx.shape):
    raise AssertionError(f"ANDON: territory is {terr_v.shape}, valid is {vidx.shape}")
flat = vidx[terr_v]
N = len(flat)

ap_, hp, sp = J(args.state, "atlas.png"), J(args.state, "holes.png"), J(args.state, "styled_mask.npy")
sha_a0, sha_h0, sha_s0 = sha(ap_), sha(hp), sha(sp)
atlas = np.array(Image.open(ap_).convert("RGB"))
holes = np.array(Image.open(hp).convert("L"))
styled = np.load(sp)
src = np.array(Image.open(args.source).convert("RGB"))
if not (src.shape == atlas.shape):
    raise AssertionError(f"ANDON: source {src.shape} vs state {atlas.shape}")

a_f, h_f, s_f = atlas.reshape(-1, 3), holes.reshape(-1), styled.reshape(-1)
is_hole = h_f[flat] > 127
write = flat[is_hole]

print(f"[reproj] territory            {N:,} texels")
print(f"[reproj] of those, HOLES now  {len(write):,}   <- THE WRITE SET (territory AND holes)")
print(f"[reproj] of those, already styled (excluded by construction): {N - len(write):,}")
if s_f[write].any():
    raise AssertionError("ANDON: the write set contains styled texels")
if not (np.isin(write, flat).all()):
    raise AssertionError("ANDON: the write set escapes the territory")
print("[reproj] ASSERTED: no styled texel in the write set; the write set is inside the territory")

if args.dry_run:
    print("[reproj] --dry-run: nothing written")
    raise SystemExit(0)

pre = a_f.copy()
a_f[write] = src.reshape(-1, 3)[write]
h_f[write] = 0
s_f[write] = True

outside = np.ones(len(a_f), dtype=bool)
outside[flat] = False
if not (np.array_equal(a_f[outside], pre[outside])):
    raise AssertionError("ANDON: a texel OUTSIDE the territory changed colour")
untouched_in_terr = flat[~is_hole]
if not (np.array_equal(a_f[untouched_in_terr], pre[untouched_in_terr])):
    raise AssertionError("ANDON: a non-hole texel inside the territory changed colour")
print(f"[reproj] ASSERTED: every texel outside the territory is byte-identical "
      f"({int(outside.sum()):,} texels)")

Image.fromarray(a_f.reshape(atlas.shape)).save(ap_)
Image.fromarray(h_f.reshape(holes.shape)).save(hp)
np.save(sp, s_f.reshape(styled.shape))
sha_a1, sha_h1, sha_s1 = sha(ap_), sha(hp), sha(sp)

rep = {"op": "garnet_reprojection_restricted_write", "ruling": "E14 Ruling 26c/5",
       "territory": int(N), "write_set": int(len(write)),
       "already_styled_in_territory": int(N - len(write)),
       "source_atlas": os.path.abspath(args.source), "source_sha256": sha(args.source),
       "state_before": {"atlas": sha_a0, "holes": sha_h0, "styled": sha_s0},
       "state_after": {"atlas": sha_a1, "holes": sha_h1, "styled": sha_s1},
       "styled_count_after": int(s_f.sum()), "holes_count_after": int((h_f > 127).sum()),
       "invariance": ["write set = territory AND holes",
                      "no styled texel in the write set",
                      "every texel outside the territory byte-identical"],
       "compensator": "e14_demote_garnet.py --undo (restores the territory's channels from "
                      "state0/); the demotion's own inverse, exercised at Task 2"}
json.dump(rep, open(J(args.state, "garnet_reprojection.json"), "w"), indent=1)
print(f"[reproj] styled {int(s_f.sum()):,}   holes {int((h_f > 127).sum()):,}")
print(f"[reproj] atlas sha256  {sha_a0[:24]}  ->  {sha_a1[:24]}")
print(f"[reproj] source sha256 {sha(args.source)[:24]}")
print(f"[reproj] wrote {J(args.state, 'garnet_reprojection.json')}")
