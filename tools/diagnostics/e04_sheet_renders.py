"""Render asset / provenance / owner at the Gate-1 sheet's cameras.

turn_render fixes its camera at mid.z and has no elevation argument (E04 Amendment 1), so it
cannot reach the two deck cameras at all. texpass_iter's emit CAN - it takes --el, it is the
renderer the strokes already used, and its output is a raycast of the atlas with no lighting,
which is exactly the FLAT readout CLAUDE.md requires for judging texture. Using it for every
row keeps one renderer, one frame and one convention across the sheet.
"""
import os
import shutil
import subprocess
import sys

PY = r"E:\AI-Models\trellis2-env\Scripts\python.exe"
TOOL = r"E:\AI\facet\tools\texpass_iter.py"
PREP = r"E:\AI\training\facet_next\E04_shipprep"
GLB = os.path.join(PREP, "prep_uv.glb")
OUT = r"E:\AI\training\facet_next\E04_stroke\out"
SEED = r"E:\AI\training\facet_next\E04_armT72\stage1"
BASE = r"E:\AI\training\facet_next\E04_stroke\sheet"

LAYERS = {"asset": os.path.join(OUT, "galleon_final.png"),
          "prov": os.path.join(OUT, "prov_atlas.png"),
          "owner": os.path.join(OUT, "owner_atlas.png")}
CAMS = [(0, 0), (0, 40), (180, 40)]

for name, atlas in LAYERS.items():
    d = os.path.join(BASE, name)
    os.makedirs(d, exist_ok=True)
    shutil.copy(atlas, os.path.join(d, "atlas.png"))
    shutil.copy(os.path.join(SEED, "stage1_8cam_holes.png"), os.path.join(d, "holes.png"))
    shutil.copy(os.path.join(SEED, "stage1_8cam_styled_mask.npy"),
                os.path.join(d, "styled_mask.npy"))
    for yaw, el in CAMS:
        r = subprocess.run([PY, TOOL, "emit", "--state", d, "--prep", PREP, "--glb", GLB,
                            "--yaw", str(yaw), "--el", str(el),
                            "--profile", r"E:\AI\facet\profiles\ship.json"],
                           capture_output=True, text=True)
        if r.returncode:
            print("ANDON: emit failed for %s %s %s\n%s" % (name, yaw, el, r.stderr[-500:]))
            sys.exit(1)
        src = os.path.join(d, "job_y%+04d_e%+03d" % (yaw, el), "render.png")
        dst = os.path.join(OUT, "sheet_%s_y%+04d_e%+03d.png" % (name, yaw, el))
        shutil.copy(src, dst)
        print("  %-6s y%+04d e%+03d -> %s" % (name, yaw, el, os.path.basename(dst)))
print("[renders] done")
