"""E10 Arm W3 - the toggle sheet: the galleon with the contact layer OFF and ON.

GATE 1 OF E10 IS THE DIRECTOR'S EYE ON THIS PAIR, at his zoom, full size. Nothing here
grades anything. The renders are raycasts of the two atlases through the same camera, so
the ONLY difference between the panels is the layer.

Pre-registered by Ruling 5, so a panel is not misread: the hull hides its own waterline
from 40 degrees of elevation - the band renders 22,106 px from the beam against 789/770
from the deck pair. The BEAM is where the toggle is legible; sparse deck panels are
geometry, not a layer failure.

  e10_toggle_sheet.py
"""
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None
PY = r"E:\AI-Models\trellis2-env\Scripts\python.exe"
TOOL = r"E:\AI\facet\tools\texpass_iter.py"
REPO = r"E:\AI\facet"
STROKE = r"E:\AI\training\facet_next\E04_stroke"
ARMT = r"E:\AI\training\facet_next\E04_armT72"
PREP = r"E:\AI\training\facet_next\E04_shipprep"
LAYER = os.path.join(STROKE, "e10_layer")
CAMS = [("beam", 0, 0), ("deck_fwd", 0, 40), ("deck_aft", 180, 40)]


def render(atlas, tag, yaw, el):
    d = os.path.join(LAYER, "toggle", tag)
    os.makedirs(d, exist_ok=True)
    Image.open(atlas).convert("RGB").save(os.path.join(d, "atlas.png"))
    for src, dst in (("stage1_8cam_holes.png", "holes.png"),
                     ("stage1_8cam_styled_mask.npy", "styled_mask.npy")):
        p = os.path.join(d, dst)
        if not os.path.exists(p):
            import shutil
            shutil.copy(os.path.join(ARMT, "stage1", src), p)
    r = subprocess.run([PY, TOOL, "emit", "--state", d, "--prep", PREP,
                        "--glb", os.path.join(PREP, "prep_uv.glb"), "--yaw", str(yaw),
                        "--el", str(el), "--profile", os.path.join(REPO, "profiles",
                                                                   "ship.json")],
                       capture_output=True, text=True)
    if r.returncode:
        print("ANDON: emit failed %s %s\n%s" % (tag, yaw, r.stderr[-400:]))
        sys.exit(1)
    return os.path.join(d, "job_y%+04d_e%+03d" % (yaw, el), "render.png")


def main():
    os.makedirs(os.path.join(LAYER, "toggle"), exist_ok=True)
    try:
        F = ImageFont.truetype("arial.ttf", 30)
        Fs = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        F = Fs = ImageFont.load_default()

    for name, yaw, el in CAMS:
        off = render(os.path.join(STROKE, "out", "galleon_final.png"), "off", yaw, el)
        on = render(os.path.join(LAYER, "composite_atlas.png"), "on", yaw, el)
        a = Image.open(off).convert("RGB")
        b = Image.open(on).convert("RGB")
        W, H = a.size
        diff = int((np.asarray(a).astype(int) != np.asarray(b).astype(int)).any(-1).sum())
        sheet = Image.new("RGB", (W * 2 + 24, H + 70), (26, 26, 28))
        sheet.paste(a, (0, 62))
        sheet.paste(b, (W + 24, 62))
        d = ImageDraw.Draw(sheet)
        d.text((8, 8), "E10 W3 - does the ship float?   camera %s  y%+04d e%+03d"
               % (name, yaw, el), fill=(255, 255, 255), font=F)
        d.text((8, 40), "L1: a weathered tallow-white hull coat below the waterline  |  "
                        "waterline_z -0.43095 (the Director's line)  |  %d px differ"
               % diff, fill=(190, 190, 190), font=Fs)
        d.text((10, 66), "LAYER OFF", fill=(255, 120, 120), font=F)
        d.text((W + 26, 66), "LAYER ON", fill=(120, 255, 160), font=F)
        p = os.path.join(LAYER, "W3_toggle_%s.png" % name)
        sheet.save(p)
        print("[toggle] %-9s %6d px differ  ->  %s" % (name, diff, os.path.basename(p)))

        if name == "beam":
            # his zoom, on the hull foot where the decision lives
            crop = (60, 700, W - 60, 980)
            za = a.crop(crop).resize(((crop[2] - crop[0]) * 3, (crop[3] - crop[1]) * 3),
                                     Image.LANCZOS)
            zb = b.crop(crop).resize(za.size, Image.LANCZOS)
            zw, zh = za.size
            zs = Image.new("RGB", (zw, zh * 2 + 96), (26, 26, 28))
            zs.paste(za, (0, 40)); zs.paste(zb, (0, zh + 88))
            dz = ImageDraw.Draw(zs)
            dz.text((8, 6), "E10 W3 - beam, hull foot at 3x", fill=(255, 255, 255), font=F)
            dz.text((8, zh + 50), "LAYER ON", fill=(120, 255, 160), font=F)
            dz.text((8, 44), "LAYER OFF", fill=(255, 120, 120), font=F)
            pz = os.path.join(LAYER, "W3_toggle_beam_ZOOM.png")
            zs.save(pz)
            print("[toggle] beam zoom -> %s" % os.path.basename(pz))
    print("\nGate 1 of E10 is the Director's eye on these. Nothing here grades them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
