"""E04 Gate 0 sheet — the source concept beside what it reconstructed into, per candidate.

ONE SHEET PER CANDIDATE, AT FULL SIZE. Not a contact sheet: the defects that decide
acceptance in this repo are invisible at thumbnail scale, and this sheet exists so the
Director designates a galleon from what the geometry actually is rather than from the
concept art. E01 is the reason all three are reconstructed before any is chosen -
reconstruction quality depends on the clay's own qualities, and which concept survives the
generator is not predictable from looking at it.

Renders are --clay by standing rule: texture hides geometry, and there is no texture here
anyway. The concept is shown at the render's own height so the eye compares like with like.

  gate0_sheet.py --concept c.png --renders DIR --tag clay --out sheet.png
                 [--label "..."] [--stats stats.json]

Standards compliance: UNCERTAINTY_GATED_HUMANS - this IS the checkpoint; it carries the
artifact at full size and no argument. EXTERNAL_VERIFIER - it renders and labels; it does
not score, rank or recommend a candidate.
"""
import argparse
import glob
import json
import os

from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--concept", required=True)
ap.add_argument("--renders", required=True, help="dir holding <tag>_N.png")
ap.add_argument("--tag", default="clay")
ap.add_argument("--out", required=True)
ap.add_argument("--label", default="")
ap.add_argument("--stats", help="mesh_stats JSON for this mesh; printed as a caption")
ap.add_argument("--cols", type=int, default=4)
# The caption used to state the SHIP's reason for not running gate_mesh.py as literal text.
# E12 reconstructs dragons, where "meaningless on a ship" and "profiles/ship.json" are both
# false, and a Director-facing designation sheet is the last place a wrong provenance
# sentence should sit. The default is that sentence VERBATIM, so every historical
# invocation reproduces the same pixels; only a caller that passes the flag changes.
ap.add_argument("--gate-note",
                default="gate_mesh.py was NOT run: its head/shoulder logic is meaningless "
                        "on a ship, and profiles/ship.json records mesh_gate: none as a "
                        "decision.",
                help="the why-no-mesh-gate line printed under the stats caption; defaults "
                     "to E04's ship wording so old invocations are unchanged")
args = ap.parse_args()

paths = sorted(glob.glob(os.path.join(args.renders, "%s_*.png" % args.tag)),
               key=lambda p: int(os.path.splitext(p)[0].rsplit("_", 1)[1]))
if not (paths):
    raise AssertionError("ANDON: no %s_*.png in %s" % (args.tag, args.renders))
views = [Image.open(p).convert("RGB") for p in paths]
vw, vh = views[0].size
cols = args.cols
rows = (len(views) + cols - 1) // cols

con = Image.open(args.concept).convert("RGB")
cw = int(con.size[0] * (vh * rows) / con.size[1])
con = con.resize((cw, vh * rows), Image.LANCZOS)

PAD, TOP, CAP = 8, 40, 96
W = cw + PAD + cols * vw + (cols - 1) * PAD
H = TOP + rows * vh + (rows - 1) * PAD + CAP
sheet = Image.new("RGB", (W, H), (16, 16, 18))
dr = ImageDraw.Draw(sheet)
dr.text((10, 12), args.label or os.path.basename(args.out), fill=(240, 240, 240))
dr.text((10, 26), "LEFT: source concept (as staged).   RIGHT: the reconstructed mesh, "
                  "--clay, %d views. Judge GEOMETRY here; there is no texture." % len(views),
        fill=(185, 190, 200))
sheet.paste(con, (0, TOP))
for i, im in enumerate(views):
    x = cw + PAD + (i % cols) * (vw + PAD)
    y = TOP + (i // cols) * (vh + PAD)
    sheet.paste(im, (x, y))
    dr.text((x + 6, y + 6), os.path.basename(paths[i]), fill=(230, 230, 120))

cy = TOP + rows * vh + (rows - 1) * PAD + 8
if args.stats and os.path.exists(args.stats):
    blob = json.load(open(args.stats))
    r = blob[0] if isinstance(blob, list) else (blob.get("meshes", [blob])[0]
                                               if isinstance(blob, dict) else blob)
    line = ("faces %s | verts %s | shells(welded) %s (largest %.4f) | shells(unwelded) %s"
            % (f"{r.get('faces', 0):,}", f"{r.get('verts', 0):,}",
               f"{r.get('components', 0):,}", r.get("largest_component_frac", 0.0),
               f"{r.get('components_unwelded', 0):,}"))
    dr.text((10, cy), line, fill=(210, 215, 225))
    ext = r.get("extent") or r.get("extents")
    if ext:
        dr.text((10, cy + 18), "extent (Blender xyz) %s" % (ext,), fill=(210, 215, 225))
dr.text((10, cy + 40), args.gate_note, fill=(190, 170, 140))
dr.text((10, cy + 58),
        "Designation is the Director's. This sheet ranks nothing.", fill=(190, 170, 140))
os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
sheet.save(args.out)
print("[gate0] wrote %s  %dx%d" % (args.out, sheet.size[0], sheet.size[1]))
