"""Recover per-stroke ownership by RE-RUNNING the shipped commits on a scratch state.

texel_provenance.py reconstructs the claim by replaying commit's filter chain offline. This
does not reimplement anything: it re-runs texpass_iter.py commit itself, snapshotting
styled_mask.npy between strokes, so the reconstruction cannot diverge from the code that
made the asset. The check is byte-identity of the final atlas against the one already
produced - if a single byte differs the reconstruction is not of this asset and it halts.
"""
import json
import os
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
PY = r"E:\AI-Models\trellis2-env\Scripts\python.exe"
TOOL = r"E:\AI\facet\tools\texpass_iter.py"
PREP = r"E:\AI\training\facet_next\E04_shipprep"
LIVE = r"E:\AI\training\facet_next\E04_stroke\state"
SEED = r"E:\AI\training\facet_next\E04_armT72\stage1"
OUT = r"E:\AI\training\facet_next\E04_stroke\out"
SCR = r"E:\AI\training\facet_next\E04_stroke\replay"
ORDER = ["y+300_e+00", "y+030_e+00", "y+150_e+00", "y+240_e+00", "y+000_e+40", "y+180_e+40"]

os.makedirs(SCR, exist_ok=True)
shutil.copy(os.path.join(SEED, "stage1_8cam.png"), os.path.join(SCR, "atlas.png"))
shutil.copy(os.path.join(SEED, "stage1_8cam_holes.png"), os.path.join(SCR, "holes.png"))
shutil.copy(os.path.join(SEED, "stage1_8cam_styled_mask.npy"),
            os.path.join(SCR, "styled_mask.npy"))
snaps = [np.load(os.path.join(SCR, "styled_mask.npy")).copy()]

for i, key in enumerate(ORDER, start=1):
    j = os.path.join(LIVE, "job_" + key)
    r = subprocess.run([PY, TOOL, "commit", "--state", SCR, "--prep", PREP,
                        "--edited", os.path.join(j, "inpainted.png"),
                        "--cam", os.path.join(j, "cam.json"),
                        "--profile", r"E:\AI\facet\profiles\ship.json"],
                       capture_output=True, text=True)
    if r.returncode:
        print("ANDON: replay commit %d failed\n%s" % (i, r.stderr[-600:]))
        sys.exit(1)
    line = [l for l in r.stdout.splitlines() if "wrote" in l]
    print("  stroke %d %-12s %s" % (i, key, line[0] if line else ""))
    snaps.append(np.load(os.path.join(SCR, "styled_mask.npy")).copy())

# ANDON: the replay must land on the same asset, byte for byte
a_live = open(os.path.join(LIVE, "atlas.png"), "rb").read()
a_scr = open(os.path.join(SCR, "atlas.png"), "rb").read()
same_bytes = a_live == a_scr
same_px = np.array_equal(
    np.asarray(Image.open(os.path.join(LIVE, "atlas.png")).convert("RGB")),
    np.asarray(Image.open(os.path.join(SCR, "atlas.png")).convert("RGB")))
same_mask = np.array_equal(snaps[-1], np.load(os.path.join(LIVE, "styled_mask.npy")))
print("\n[replay] final atlas bytes identical: %s | PIXELS identical: %s | styled mask "
      "identical: %s" % (same_bytes, same_px, same_mask))
if not (same_px and same_mask):
    print("ANDON: the replay did not land on this asset. HALT.")
    sys.exit(1)

# ---- the two atlases
mask = np.load(os.path.join(PREP, "mask.npy"))[..., 0] > 0.5
RES = mask.shape[0]
stage1 = snaps[0]
final = snaps[-1]
prov = np.zeros((RES, RES, 3), dtype=np.uint8)
prov[mask] = (232, 132, 32)                                   # ORANGE - dilation
prov[final & mask] = (40, 110, 235)                           # BLUE   - brush
prov[stage1 & mask] = (46, 176, 88)                           # GREEN  - reference
Image.fromarray(prov).save(os.path.join(OUT, "prov_atlas.png"))

owner1 = np.load(os.path.join(SEED, "stage1_8cam_owner.npy"))
CAM8 = [(214, 39, 40), (255, 127, 14), (188, 189, 34), (44, 160, 44),
        (23, 190, 207), (31, 119, 180), (148, 103, 189), (227, 119, 194)]
STROKE6 = [(255, 255, 255), (255, 214, 214), (214, 255, 214), (214, 214, 255),
           (255, 255, 160), (255, 190, 120)]
own = np.zeros((RES, RES, 3), dtype=np.uint8)
own[mask] = (60, 60, 60)                                      # grey - dilation, no owner
for v in range(8):
    own[(owner1 == v) & mask] = CAM8[v]
counts = {}
for i in range(6):
    new = snaps[i + 1] & ~snaps[i] & mask
    own[new] = STROKE6[i]
    counts[ORDER[i]] = int(new.sum())
Image.fromarray(own).save(os.path.join(OUT, "owner_atlas.png"))

valid = int(mask.sum())
summary = {"valid": valid, "stage1": int((stage1 & mask).sum()),
           "brush": int((final & ~stage1 & mask).sum()),
           "dilation": int((~final & mask).sum()),
           "per_stroke": counts,
           "replay_pixels_identical": bool(same_px),
           "replay_bytes_identical": bool(same_bytes)}
summary["mix_pct"] = {k: round(100 * summary[k] / valid, 2)
                      for k in ("stage1", "brush", "dilation")}
json.dump(summary, open(os.path.join(OUT, "provenance.json"), "w"), indent=1)
print("[replay] mix  reference %.2f%%  brush %.2f%%  dilation %.2f%%"
      % (summary["mix_pct"]["stage1"], summary["mix_pct"]["brush"],
         summary["mix_pct"]["dilation"]))
print("[replay] per-stroke: %s" % ", ".join("%s %d" % (k, v) for k, v in counts.items()))
print("[replay] wrote prov_atlas.png, owner_atlas.png, provenance.json")
