"""E10 — the sea-occlusion composite: the water hides what sits below the line.

Dispatched by E10 Ruling 10. The coat-only toggle did not read as a floating ship because
a ship reads as floating when the water OCCLUDES the below-water hull, and a painted coat
leaves it fully visible. This builds the artifact the float question actually needs.

ZERO GENERATION. The base asset is opened read-only and hashed before and after.

⚠ THE SEA IS AN OPAQUE HALF-SPACE, NOT A SURFACE — and that is not a stylistic choice.
Under orthographic projection with a HORIZONTAL view direction, a zero-thickness horizontal
plane is edge-on: every ray runs parallel to it and never intersects it, so a rendered water
SURFACE would occlude nothing at the beam camera. The half-space `z <= waterline_z` has no
such degeneracy — a ray at height z is inside the water body for every z below the line, so
the water's image is exactly the rows below the projected line.

At elevation 0 the row is a function of world z ALONE (up = +Z exactly), so

    image row > line_row   <=>   world z < waterline_z

is EXACT, not approximate. That equivalence is the whole instrument, and it holds at
elevation 0 only — anchor A2 enforces the precondition rather than trusting it.

THE ANCHORS, and what a failure of each would mean:
  A1 row      - line_row computed from THIS render's own cam.json must match the row Step
                0.2 recorded (a different tool, a different session). A miss means this
                render is framed differently from the frame the line was measured in, and
                the sea would land on the wrong row under an entirely plausible sheet.
  A2 elevation- the camera must be level. At any other elevation a horizontal plane's image
                is not a row boundary and this composite would be a drawing, not a
                projection.
  A3 base     - galleon_final.png's sha256 must equal the recorded anchor, before AND after.
                W-H3: the base asset is untouchable.
  A4 chroma   - the derived sea colour must sit above the palette fixture's own chroma
                floor. Below it hue is not a colour - it is undefined and reads as a
                rotation - so "sea-blue" would not be a colour claim at all.

Standards compliance:
  PIN_PER_STEP - waterline_z, the recorded row, the base hash, the chroma floor and the blue
    band are all READ from their files, never typed. The row formula is reused from
    e10_contact_mask.py:233 rather than re-derived.
  ANDON_AUTHORITY - four anchors, each with a describable non-zero; every one halts in-tool.
  NAMED_COMPENSATORS - writes only into --out. Undo = delete it. The base asset is opened
    read-only; A3 measures it both ends.
  EXTERNAL_VERIFIER - the below-line extent is cross-checked against Step 0.2's rendered
    contact band, which reached the same property along a path sharing only the mesh.
    Nothing here grades the picture: the advisor looks, then the Director rules.

  e10_sea_composite.py [--out DIR]
"""
import argparse
import hashlib
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None

REPO = r"E:\AI\facet"
STROKE = r"E:\AI\training\facet_next\E04_stroke"
TASK4 = r"E:\AI\training\facet_next\E04_task4"
LAYER = os.path.join(STROKE, "e10_layer")
BASE = os.path.join(STROKE, "out", "galleon_final.png")
BEAM = "job_y+000_e+00"

ANCHOR_ROW_TOL_PX = 0.01          # A1. Pure arithmetic on both sides; nothing to absorb.
PAIR_VIEWS = [("1", "1_stern_three_quarter"), ("7", "7_bow_three_quarter")]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def lab(rgb):
    """sRGB [0,1] -> CIE Lab (D65). Verbatim from diagnostics/e04_bands.py, so the colour
    derived here lives in the same space the palette bands were measured in."""
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16, 500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


def lab_to_srgb255(L, a, b):
    """The inverse of lab(), same constants. Returns uint8 sRGB."""
    fy = (L + 16) / 116
    fx, fz = fy + a / 500, fy - b / 200
    e, k = 216 / 24389, 24389 / 27
    f = np.array([fx, fy, fz])
    xyz = np.where(f ** 3 > e, f ** 3, (116 * f - 16) / k)
    xyz = xyz * np.array([0.95047, 1.0, 1.08883])
    Mi = np.array([[3.2404542, -1.5371385, -0.4985314],
                   [-0.9692660, 1.8760108, 0.0415560],
                   [0.0556434, -0.2040259, 1.0572252]])
    c = np.clip(Mi @ xyz, 0.0, 1.0)
    s = np.where(c <= 0.0031308, 12.92 * c, 1.055 * c ** (1 / 2.4) - 0.055)
    return np.clip(np.round(s * 255.0), 0, 255).astype(np.uint8)


def band_edges(palette):
    for b in palette["allowed_bands"]:
        if b["name"] == "blue":
            return b
    raise SystemExit("ANDON: no blue band in the palette fixture")


def derive_sea_colour(palette, rep):
    """G11's declared sea-blue, measured on the DIRECTOR-RATIFIED target pair.

    A DEMO CHOICE, recorded as one. Ruling 10 assigned the water's material to the scene
    (RG02 Q3), so this proposes no colour FOR water - it takes the one blue this subject has
    ever been measured to carry, so that no taste enters the fill. Measured on the pair,
    which is not a twin and is gated by nothing here: the palette fixture's own
    non-circularity, kept.
    """
    blue = band_edges(palette)
    floor = float(palette["min_chroma"])
    lo, hi = [float(v) for v in blue["hue_deg"]]
    Ls, Cs, Hs, tot = [], [], [], 0
    for key, stem in PAIR_VIEWS:
        img = np.asarray(Image.open(os.path.join(TASK4, "pair", "target_%s.png" % stem)
                                    ).convert("RGB"), dtype=np.float64) / 255.0
        msk = np.asarray(Image.open(os.path.join(TASK4, "masks1024", "galleonclay_%s.png"
                                                 % key)).convert("L")) > 127
        if msk.shape != img.shape[:2]:
            print("ANDON: mask %s is %s, target is %s - the pair and its mask disagree. HALT."
                  % (key, msk.shape, img.shape[:2]))
            sys.exit(1)
        Lab = lab(img)
        C = np.hypot(Lab[..., 1], Lab[..., 2])
        H = np.degrees(np.arctan2(Lab[..., 2], Lab[..., 1])) % 360.0
        sel = msk & (C >= floor) & (H >= lo) & (H <= hi)
        tot += int(sel.sum())
        Ls.append(Lab[..., 0][sel]); Cs.append(C[sel]); Hs.append(H[sel])
    L = np.concatenate(Ls); C = np.concatenate(Cs); H = np.concatenate(Hs)
    if not len(L):
        print("ANDON: no pixel on the ratified pair sits inside G11's declared blue band. "
              "HALT.")
        sys.exit(1)
    mL, mC, mH = float(np.median(L)), float(np.median(C)), float(np.median(H))
    rgb = lab_to_srgb255(mL, mC * np.cos(np.radians(mH)), mC * np.sin(np.radians(mH)))
    rep["sea_colour"] = {
        "kind": "DEMO CHOICE, derived - not canon, and not a claim about water",
        "derived_from": "G11 `a deep sea-blue frieze band along the bulwarks`, measured on "
                        "the Director-ratified target pair (E04_task4/pair), inside the "
                        "declared blue band",
        "band_hue_deg": [lo, hi], "chroma_floor": floor,
        "pixels_measured": tot,
        "median_Lstar": mL, "median_Cstar": mC, "median_hue_deg": mH,
        "srgb255": [int(v) for v in rgb],
        "fixture_measured_span_deg": blue["measured_span_deg"],
        "band_status": blue["status"]}
    print("[sea] G11 blue on the ratified pair: %d px | median L* %.1f  C* %.1f  h %.1f deg"
          % (tot, mL, mC, mH))
    print("      -> fill rgb(%d,%d,%d)   (a DEMO CHOICE, derived from the fixture)"
          % tuple(rgb))
    if mC < floor:
        print("ANDON A4: the derived colour's C* %.2f is below the fixture's own chroma "
              "floor %.1f. Below the floor hue is not a colour. HALT." % (mC, floor))
        sys.exit(1)
    return tuple(int(v) for v in rgb)


def panel(img, title, sub, colour, F, Fs):
    W, H = img.size
    p = Image.new("RGB", (W, H + 62), (26, 26, 28))
    p.paste(img, (0, 62))
    d = ImageDraw.Draw(p)
    d.text((8, 6), title, fill=colour, font=F)
    d.text((8, 38), sub, fill=(180, 180, 180), font=Fs)
    return p


def compose(sheet_parts, path, header, sub, F, Fs):
    W = sum(p.size[0] for p in sheet_parts) + 24 * (len(sheet_parts) - 1)
    H = max(p.size[1] for p in sheet_parts)
    s = Image.new("RGB", (W, H + 72), (26, 26, 28))
    x = 0
    for p in sheet_parts:
        s.paste(p, (x, 72)); x += p.size[0] + 24
    d = ImageDraw.Draw(s)
    d.text((8, 8), header, fill=(255, 255, 255), font=F)
    d.text((8, 42), sub, fill=(190, 190, 190), font=Fs)
    s.save(path)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(LAYER, "sea"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    J = os.path.join
    rep = {}

    # ---- everything READ, nothing typed ---------------------------------------------
    prof = json.load(open(J(REPO, "profiles", "ship.json"), encoding="utf-8"))
    WZ = float(prof["waterline"]["z"]["value"])
    contact = json.load(open(J(STROKE, "e10_contact", "contact_mask.json"),
                             encoding="utf-8"))
    recorded_row = float(contact["anchor_C_projection"]["placed_line_row"])
    recorded_band = int(contact["anchor_D_render"]["beam_y000_e00"]["band_px"])
    state = json.load(open(J(LAYER, "layer_state.json"), encoding="utf-8"))
    base_anchor = state["base_atlas_sha256"]
    palette = json.load(open(J(REPO, "canon", "E04-galleon-palette.json"), encoding="utf-8"))
    print("[line] waterline_z = %+.5f (profiles/ship.json, canonical mesh frame)" % WZ)
    print("[rec ] Step 0.2 recorded placed_line_row %.4f | rendered beam band %d px"
          % (recorded_row, recorded_band))

    # ---- ANCHOR A3 (before) ---------------------------------------------------------
    before = sha256(BASE)
    rep["anchor_A3_base"] = {"anchor": base_anchor, "before": before}
    print("[A3] base sha256 before: %s" % before[:16])
    if before != base_anchor:
        print("ANDON A3: galleon_final.png does not match the recorded anchor BEFORE this "
              "run. The base asset moved outside this session. HALT.")
        return 1

    # ---- P1: the reused render is a render of the ACCEPTED asset --------------------
    off_dir = J(LAYER, "toggle", "off", BEAM)
    on_dir = J(LAYER, "toggle", "on", BEAM)
    a1 = np.asarray(Image.open(J(LAYER, "toggle", "off", "atlas.png")).convert("RGB"))
    a2 = np.asarray(Image.open(BASE).convert("RGB"))
    same = a1.shape == a2.shape and bool((a1 == a2).all())
    ndiff = 0 if same else (int((a1 != a2).any(-1).sum()) if a1.shape == a2.shape else -1)
    rep["P1_reused_render_is_the_accepted_asset"] = {
        "compared": "toggle/off/atlas.png vs out/galleon_final.png, PIXELS (bytes are not "
                    "pixel values - the repo's own rule)",
        "shape_off": list(a1.shape), "shape_base": list(a2.shape),
        "pixel_identical": same, "differing_px": ndiff}
    print("[P1 ] toggle/off/atlas.png vs the accepted asset: %s (%d px differ)"
          % ("PIXEL-IDENTICAL" if same else "DIFFERENT", ndiff))
    del a1, a2

    # ---- the camera, and ANCHORS A2 + A1 --------------------------------------------
    cam = json.load(open(J(off_dir, "cam.json"), encoding="utf-8"))
    cam_on = json.load(open(J(on_dir, "cam.json"), encoding="utf-8"))
    if cam != cam_on:
        print("ANDON: the layer-off and layer-on beam renders do not share a camera. The "
              "panels would differ by more than the layer. HALT.")
        return 1
    rep["camera"] = dict(cam)
    if float(cam["el"]) != 0.0:
        print("ANDON A2: camera elevation is %.3f, not 0. The row-split predicate is exact "
              "at elevation 0 only - at any other elevation a horizontal plane's image is "
              "not a row boundary. HALT." % float(cam["el"]))
        return 1
    print("[A2 ] camera elevation 0.0 - the row-split predicate is exact here")

    # e10_contact_mask.py:233, reused rather than re-derived
    line_row = (0.5 - (WZ - cam["bmid"][2]) / cam["v_ext"]) * cam["H"] - 0.5
    drow = abs(line_row - recorded_row)
    rep["anchor_A1_row"] = {
        "formula": "e10_contact_mask.py:233 - (0.5 - (wz - bmid.z)/v_ext)*H - 0.5",
        "line_row": float(line_row), "recorded_row": recorded_row,
        "delta_px": float(drow), "tolerance_px": ANCHOR_ROW_TOL_PX}
    print("[A1 ] line_row %.4f vs Step 0.2's recorded %.4f -> delta %.2e px"
          % (line_row, recorded_row, drow))
    if drow > ANCHOR_ROW_TOL_PX:
        print("ANDON A1: this render is framed differently from the frame the line was "
              "measured in. HALT.")
        return 1

    first_sea_row = int(np.ceil(line_row))
    rep["split"] = {"line_row": float(line_row), "first_sea_row": first_sea_row,
                    "rule": "a pixel row r is underwater iff r > line_row; row centres, so "
                            "the last dry row is %d" % (first_sea_row - 1)}
    print("[row ] first underwater row %d (last dry row %d)"
          % (first_sea_row, first_sea_row - 1))

    # ---- P4: the below-line extent, cross-checked -----------------------------------
    hit = np.asarray(Image.open(J(off_dir, "hit.png")).convert("L")) > 0
    below = np.zeros_like(hit); below[first_sea_row:] = True
    n_below = int((hit & below).sum())
    rep["P4_below_line_extent"] = {
        "silhouette_px_below_line": n_below,
        "step0_2_rendered_contact_band_px": recorded_band,
        "delta_px": n_below - recorded_band,
        "delta_pct_of_recorded": 100.0 * (n_below - recorded_band) / recorded_band,
        "figure_px_total": int(hit.sum()),
        "REPORTED_NOT_GATED": "the two are not identical by construction - the contact mask "
                              "excludes 2,487 off-surface texels, the rendered mask has "
                              "rasterization gaps, and that render is thresholded at >127"}
    print("[P4 ] silhouette below the line %d px vs Step 0.2's rendered band %d px "
          "(%+d, %+.2f%%)  | figure %d px"
          % (n_below, recorded_band, n_below - recorded_band,
             100.0 * (n_below - recorded_band) / recorded_band, int(hit.sum())))

    # ---- the sea colour --------------------------------------------------------------
    SEA = derive_sea_colour(palette, rep)

    # ---- the composites --------------------------------------------------------------
    def flood(render_path, name):
        im = np.asarray(Image.open(render_path).convert("RGB")).copy()
        occluded = int((hit[first_sea_row:]).sum())
        im[first_sea_row:] = SEA
        out = J(args.out, "%s.png" % name)
        Image.fromarray(im).save(out)
        return Image.fromarray(im), occluded, out

    dry = Image.open(J(off_dir, "render.png")).convert("RGB")
    wet, occ, wet_path = flood(J(off_dir, "render.png"), "beam_floating")
    dry_layer = Image.open(J(on_dir, "render.png")).convert("RGB")
    wet_layer, _, wet_layer_path = flood(J(on_dir, "render.png"), "beam_floating_layer_on")
    rep["occlusion"] = {"hull_px_hidden_by_the_water": occ,
                        "pct_of_figure": 100.0 * occ / max(1, int(hit.sum()))}
    print("[sea ] the water hides %d px of hull (%.2f%% of the figure)"
          % (occ, 100.0 * occ / max(1, int(hit.sum()))))

    try:
        F = ImageFont.truetype("arial.ttf", 30)
        Fs = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        F = Fs = ImageFont.load_default()

    files = {}
    sub = ("waterline_z %+.5f (the Director's line) | first underwater row %d | ortho beam, "
           "elevation 0 - the row split is EXACT | sea rgb(%d,%d,%d), a demo choice derived "
           "from G11" % (WZ, first_sea_row, SEA[0], SEA[1], SEA[2]))

    files["toggle_pair"] = compose(
        [panel(dry, "DRY", "the accepted asset, no water", (255, 140, 140), F, Fs),
         panel(wet, "FLOATING", "sea occludes everything below the line", (130, 210, 255),
               F, Fs)],
        J(args.out, "E10_SEA_beam_toggle.png"),
        "E10 - does she float?   beam, y+000 e+00, full size", sub, F, Fs)

    files["layer_pair"] = compose(
        [panel(wet, "FLOATING, boot-top OFF", "base asset + water", (255, 140, 140), F, Fs),
         panel(wet_layer, "FLOATING, boot-top ON",
               "the W2d coat, now only visible AT the line", (130, 255, 170), F, Fs)],
        J(args.out, "E10_SEA_beam_layer.png"),
        "E10 - the boot-top, once the water hides the rest   beam, y+000 e+00",
        "the coat covers 6.7%% of the band (one view's share, Ruling 9's flag) - %s" % sub,
        F, Fs)

    # the Director's zoom: the line itself, where the decision lives
    crop = (60, max(0, first_sea_row - 120), cam["W"] - 60,
            min(cam["H"], first_sea_row + 60))
    zs = [(dry, "DRY", (255, 140, 140)), (wet, "FLOATING", (130, 210, 255)),
          (wet_layer, "FLOATING + boot-top", (130, 255, 170))]
    zp = []
    for im, lab_, col in zs:
        c = im.crop(crop)
        c = c.resize((c.size[0] * 3, c.size[1] * 3), Image.LANCZOS)
        zp.append(panel(c, lab_, "rows %d-%d at 3x" % (crop[1], crop[3]), col, F, Fs))
    W = max(p.size[0] for p in zp)
    Hh = sum(p.size[1] for p in zp) + 24 * (len(zp) - 1)
    z = Image.new("RGB", (W, Hh + 72), (26, 26, 28))
    y = 72
    for p in zp:
        z.paste(p, (0, y)); y += p.size[1] + 24
    d = ImageDraw.Draw(z)
    d.text((8, 8), "E10 - the waterline at 3x   beam, y+000 e+00", fill=(255, 255, 255),
           font=F)
    d.text((8, 42), sub, fill=(190, 190, 190), font=Fs)
    files["zoom"] = J(args.out, "E10_SEA_beam_ZOOM.png")
    z.save(files["zoom"])

    files["floating"] = wet_path
    files["floating_layer_on"] = wet_layer_path
    rep["files"] = files
    for k, v in files.items():
        print("[out ] %-18s %s" % (k, os.path.basename(v)))

    # ---- ANCHOR A3 (after) -----------------------------------------------------------
    after = sha256(BASE)
    rep["anchor_A3_base"]["after"] = after
    rep["anchor_A3_base"]["unchanged"] = after == base_anchor
    print("[A3 ] base sha256 after:  %s  %s"
          % (after[:16], "UNCHANGED" if after == base_anchor else "CHANGED"))
    if after != base_anchor:
        print("ANDON A3: the base asset changed during this run. HALT.")
        return 1

    json.dump(rep, open(J(args.out, "sea_composite.json"), "w"), indent=1)
    print("\n[json] %s" % J(args.out, "sea_composite.json"))
    print("Nothing here grades the picture. The advisor looks, then the Director rules.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
