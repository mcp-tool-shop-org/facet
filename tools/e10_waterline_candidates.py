"""E10 Step 0.1 - derive candidate waterline_z lines from the mesh and draw them for the
Director's eye. His sentence is the gate; nothing here picks the line.

THE TWO ANCHORS ARE THE SPEC'S, NOT THIS TOOL'S (E10 Step 0.1):
  - the hull's lower extent, measured from the mesh;
  - the founding exemplar's band top, projected to z. The rejected view-7 twin
    (seed 770700) painted implied water at the hull's foot. Under E10 Ruling 1 that
    exemplar validates the band's GEOMETRY only - it is not a colour or content target,
    because what it painted was the dynamic half that now belongs to the shader.

The three candidates are evenly spaced across the span between those two anchors. THE
FRACTIONS ARE A RULER, NOT THRESHOLDS: 1/3, 2/3, 3/3 of a measured span, drawn so the
Director has something to point at. He may name any z, including one off the ladder.

WHY THE BEAM CAMERA. emit's projection is orthographic, and at elevation 0 the up vector
is exactly [0,0,1] (basis(): up = right x look, and right = look x [0,0,1] with look in
the xy-plane), so a world z-plane maps to an EXACTLY horizontal image row, at any yaw.
At the deck cameras (el +40) it does not - a z-plane becomes a slanted line whose row
depends on horizontal position - so the candidate render is the beam view.

The projection is CHECKED BEFORE IT IS USED: the mesh's vertices are projected with the
same formula texpass_iter's commit uses, and the resulting row extent is compared against
the render's own raycast silhouette. A projection that disagrees with the geometry it
claims to describe halts here rather than producing a plausible ladder on the wrong rows.

Standards compliance:
  PIN_PER_STEP - every number is read from cam.json, the mesh, or the exemplar image; the
    fractions are stated in the output and in the JSON.
  ANDON_AUTHORITY - the projection round-trip halts on disagreement; the exemplar band
    measurement halts if it finds nothing where the record says a band exists.
  NAMED_COMPENSATORS - writes only into --out. Undo = delete that directory. Owner: this
    session. Reads the accepted asset; opens nothing for writing.
  EXTERNAL_VERIFIER - decides no line. The Director's eye is the gate.

  e10_waterline_candidates.py [--out DIR]
"""
import argparse
import json
import os
import sys

import numpy as np
import trimesh
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import label

Image.MAX_IMAGE_PIXELS = None

STROKE = r"E:\AI\training\facet_next\E04_stroke"
ARMT = r"E:\AI\training\facet_next\E04_armT72"
PREP = r"E:\AI\training\facet_next\E04_shipprep"

# The exemplar's band, as the record describes it (E04 Ruling 19/20, E10 spec). Used as
# the SEARCH criteria, not as the answer - the band is re-measured from the artifact.
CHROMA_FLOOR = 12.0          # the subject's own floor, canon/E04-galleon-palette.json
BAND_HUE = (240.0, 273.0)    # Ruling 20's exact-band check


def load_emit_frame(path):
    """Load a GLB into the frame emit's cameras actually live in.

    ⚠ THE FOURTH COPY OF A SHARED CONVENTION. texpass_iter.load_scene() does not raycast
    the GLB's own coordinates: it re-axes Y-up -> Z-up AND normalises by max-abs, so
    every world quantity in a cam.json is in THIS frame and not the file's:

        vmax = np.abs(v).max()
        v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / vmax * 0.5

    Nothing outside texpass_iter.py documents it, and reading a cam.json against the raw
    GLB silently puts every z on the wrong row - which is what the projection ANDON below
    caught on this tool's first run (206 px). Verified: this transform reproduces the beam
    cam.json's bmid on all three axes and its h_ext exactly.
    """
    m = trimesh.load(path, force="mesh", process=False)
    v = np.asarray(m.vertices, dtype=np.float64)
    vmax = np.abs(v).max()
    return np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / vmax * 0.5, float(vmax)


def to_lab(rgb):
    """sRGB -> Lab. Same transform as palette_gate.py / e08_deltaE.py."""
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16,
                     500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(STROKE, "e10_step0"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    J = os.path.join
    rep = {}

    # ---- 1. the beam camera, read from the render that exists -----------------------
    cam = json.load(open(J(STROKE, "sheet", "asset", "job_y+000_e+00", "cam.json")))
    V, BZ, W, H = cam["v_ext"], cam["bmid"][2], cam["W"], cam["H"]
    if abs(cam["el"]) > 1e-9:
        print("ANDON: the candidate camera must be at elevation 0; cam.json says %.3f"
              % cam["el"])
        return 1
    rep["camera"] = {"source": "sheet/asset/job_y+000_e+00/cam.json", "yaw": cam["yaw"],
                     "el": cam["el"], "v_ext": V, "bmid_z": BZ, "W": W, "H": H}

    def z_to_row(z):
        return (0.5 - (z - BZ) / V) * H - 0.5

    def row_to_z(py):
        return BZ + V * (0.5 - (py + 0.5) / H)

    # ---- 2. the mesh, measured ------------------------------------------------------
    vv, vmax = load_emit_frame(J(PREP, "prep_uv.glb"))
    vz = vv[:, 2]
    z_min, z_max = float(vz.min()), float(vz.max())
    vv2, vmax2 = load_emit_frame(J(STROKE, "out", "galleon_final.glb"))
    vz2 = vv2[:, 2]
    # the framing operands emit derived, recomputed here and checked against cam.json
    lo, hi = vv.min(axis=0), vv.max(axis=0)
    bmid_calc = (lo + hi) / 2
    h_ext_calc = max(hi[0] - lo[0], hi[1] - lo[1]) * 1.204   # ship.json margin, fit-axis width
    rep["frame_check"] = {
        "convention": "texpass_iter.load_scene(): [x, -z, y] / max(|v|) * 0.5",
        "vmax": vmax,
        "bmid_recomputed": bmid_calc.tolist(), "bmid_from_cam_json": cam["bmid"],
        "bmid_max_delta": float(np.max(np.abs(bmid_calc - np.array(cam["bmid"])))),
        "h_ext_recomputed": h_ext_calc, "h_ext_from_cam_json": cam["h_ext"],
        "h_ext_delta": abs(h_ext_calc - cam["h_ext"]),
    }
    print("[frame] emit convention reproduced: bmid delta %.2e, h_ext delta %.2e"
          % (rep["frame_check"]["bmid_max_delta"], rep["frame_check"]["h_ext_delta"]))
    rep["mesh"] = {
        "_frame": "emit frame (normalised, Z-up), NOT the GLB's raw coordinates",
        "prep_uv.glb": {"z_min": z_min, "z_max": z_max, "z_span": z_max - z_min,
                        "vertices": int(len(vz)), "vmax_raw": vmax},
        "galleon_final.glb": {"z_min": float(vz2.min()), "z_max": float(vz2.max()),
                              "z_span": float(vz2.max() - vz2.min()),
                              "vertices": int(len(vz2)), "vmax_raw": vmax2},
    }
    # cross-check: the accepted asset and the prep mesh should occupy the same z range
    dz = max(abs(z_min - float(vz2.min())), abs(z_max - float(vz2.max())))
    rep["mesh"]["max_z_disagreement"] = dz
    print("[mesh] prep z [%.5f, %.5f] span %.5f | final z [%.5f, %.5f] | max disagreement %.2e"
          % (z_min, z_max, z_max - z_min, float(vz2.min()), float(vz2.max()), dz))

    # ---- 3. ANDON: the projection is checked against the raycast silhouette ----------
    hit = np.asarray(Image.open(J(STROKE, "sheet", "asset", "job_y+000_e+00",
                                  "hit.png")).convert("L")) > 0
    rows = np.where(hit.any(axis=1))[0]
    sil_top, sil_bot = int(rows.min()), int(rows.max())
    proj_top, proj_bot = z_to_row(z_max), z_to_row(z_min)
    rep["projection_check"] = {
        "silhouette_row_top": sil_top, "silhouette_row_bottom": sil_bot,
        "projected_row_of_z_max": proj_top, "projected_row_of_z_min": proj_bot,
        "delta_top_px": abs(proj_top - sil_top), "delta_bottom_px": abs(proj_bot - sil_bot),
        "tolerance_px": 2.0,
    }
    print("[proj] mesh z_max -> row %.2f (silhouette top %d, d=%.2f) | z_min -> row %.2f "
          "(silhouette bottom %d, d=%.2f)"
          % (proj_top, sil_top, abs(proj_top - sil_top),
             proj_bot, sil_bot, abs(proj_bot - sil_bot)))
    if max(abs(proj_top - sil_top), abs(proj_bot - sil_bot)) > 2.0:
        print("ANDON: the projection disagrees with the raycast silhouette by more than "
              "2 px. Every z below would be on the wrong row. HALT.")
        json.dump(rep, open(J(args.out, "waterline_candidates.json"), "w"), indent=1)
        return 1

    # ---- 4. the founding exemplar's band, RE-MEASURED from the artifact --------------
    ex_path = J(ARMT, "twins", "twin_7_REJECTED_seed770700.png")
    ex = np.asarray(Image.open(ex_path).convert("RGB"), dtype=np.float32) / 255.0
    ex_sil = np.asarray(Image.open(J(ARMT, "masks", "galleonclay_7.png")).convert("L")) > 127
    if ex.shape[:2] != ex_sil.shape:
        print("ANDON: exemplar %s and its silhouette %s disagree" % (ex.shape[:2], ex_sil.shape))
        return 1
    lab = to_lab(ex)
    C = np.hypot(lab[..., 1], lab[..., 2])
    Hd = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360.0
    band = (C > CHROMA_FLOOR) & (Hd >= BAND_HUE[0]) & (Hd <= BAND_HUE[1]) & ex_sil
    n_band = int(band.sum())
    if n_band == 0:
        print("ANDON: no band found in the exemplar where the record says one exists. HALT.")
        return 1
    lbl, n_cc = label(band)
    sizes = np.bincount(lbl.ravel())[1:]
    big = int(np.argmax(sizes)) + 1
    cc = lbl == big
    ys, xs = np.where(band)
    cys, cxs = np.where(cc)
    band_top_row, band_bot_row = int(ys.min()), int(ys.max())
    rep["exemplar"] = {
        "artifact": ex_path,
        "criteria": {"chroma_floor": CHROMA_FLOOR, "hue_deg": list(BAND_HUE),
                     "inside": "masks/galleonclay_7.png (exact silhouette)"},
        "band_px": n_band, "components": int(n_cc),
        "largest_cc_px": int(sizes.max()),
        "bbox_all": {"x": [int(xs.min()), int(xs.max())],
                     "y": [band_top_row, band_bot_row]},
        "bbox_largest_cc": {"x": [int(cxs.min()), int(cxs.max())],
                            "y": [int(cys.min()), int(cys.max())]},
        "median_L": float(np.median(lab[..., 0][band])),
        "median_C": float(np.median(C[band])),
        "median_hue": float(np.median(Hd[band])),
        "record_says": "E10 spec: 2,002 px, x 398-686, y 896-939, h 262.6, C* 14.4, L* 31.7. "
                       "Ruling 20 quotes 2,272 px for the exact-band check. Two numbers in "
                       "the record; this is a third measurement, reported beside them, "
                       "not reconciled.",
    }
    print("[exemplar] band %d px in %d components (largest %d) | rows %d-%d | x %d-%d"
          % (n_band, n_cc, sizes.max(), band_top_row, band_bot_row, xs.min(), xs.max()))
    print("[exemplar] median L* %.1f  C* %.1f  hue %.1f"
          % (np.median(lab[..., 0][band]), np.median(C[band]), np.median(Hd[band])))

    z_band_top = row_to_z(band_top_row)
    z_band_bot = row_to_z(band_bot_row)
    rep["exemplar"]["z_band_top"] = z_band_top
    rep["exemplar"]["z_band_bottom"] = z_band_bot
    print("[exemplar] band top row %d -> z %.5f | band bottom row %d -> z %.5f"
          % (band_top_row, z_band_top, band_bot_row, z_band_bot))

    # ---- 5. the candidates: a ruler across the two anchors ---------------------------
    span = z_band_top - z_min
    cands = []
    for i, f in enumerate([1 / 3, 2 / 3, 1.0], start=1):
        z = z_min + span * f
        cands.append({"label": "ABC"[i - 1], "fraction_of_span": f, "z": z,
                      "row": z_to_row(z),
                      "height_above_keel": z - z_min,
                      "pct_of_mesh_z_span": 100.0 * (z - z_min) / (z_max - z_min)})
    rep["anchors"] = {"keel_z_min": z_min, "exemplar_band_top_z": z_band_top,
                      "span": span,
                      "_fractions_are_a_ruler": (
                          "1/3, 2/3, 3/3 of the measured span between the two anchors the "
                          "spec names. NOT thresholds and NOT derived from any outcome. The "
                          "Director may name any z, including one off this ladder.")}
    rep["candidates"] = cands
    print("\n[candidates] keel z %.5f -> exemplar band top z %.5f (span %.5f)"
          % (z_min, z_band_top, span))
    for c in cands:
        print("  %s  z %+.5f  row %7.2f  %5.1f%% of mesh z-span  (%.2f of the anchor span)"
              % (c["label"], c["z"], c["row"], c["pct_of_mesh_z_span"],
                 c["fraction_of_span"]))

    # ---- 6. how much of the figure sits below each line ------------------------------
    # A cheap diagnostic for his eye: a waterline is a statement about how deep she sits.
    fig_px = int(hit.sum())
    rr = np.arange(H)[:, None]
    for c in cands:
        c["silhouette_px_below"] = int((hit & (rr > c["row"])).sum())
        c["pct_of_figure_below"] = 100.0 * c["silhouette_px_below"] / fig_px
    rep["figure_px"] = fig_px
    for c in cands:
        print("  %s  %6d of %d silhouette px below it (%.2f%% of the figure)"
              % (c["label"], c["silhouette_px_below"], fig_px, c["pct_of_figure_below"]))

    # ---- 7. the sheets for his eye ---------------------------------------------------
    base = Image.open(J(STROKE, "out", "sheet_asset_y+000_e+00.png")).convert("RGB")
    COLS = {"A": (80, 200, 255), "B": (255, 205, 40), "C": (255, 80, 80)}
    keel_row = z_to_row(z_min)

    def fonts(px):
        try:
            return (ImageFont.truetype("arial.ttf", px),
                    ImageFont.truetype("arial.ttf", max(11, int(px * 0.72))))
        except OSError:
            return ImageFont.load_default(), ImageFont.load_default()

    def annotate(img, x0, y0, s, fpx, ruler):
        """Draw the ladder onto an already-cropped/scaled image.

        Labels are stacked in a legend rather than written on the lines: at 1/3 and 2/3
        of a 0.049 span the three rows sit ~14 px apart, and text on the lines collides
        into an unreadable smear (measured on this tool's first sheet).
        """
        d = ImageDraw.Draw(img)
        big, sml = fonts(fpx)
        Wd, Hd_ = img.size

        def R(row):
            return (row - y0) * s

        if ruler:
            # a scale so ANY answer is expressible, not just the three lines
            span = z_max - z_min
            pct = 0
            while pct <= 30:
                z = z_min + span * pct / 100.0
                r = R(z_to_row(z))
                if 0 <= r < Hd_:
                    d.line([(0, r), (14, r)], fill=(190, 190, 190), width=1)
                    d.text((18, r - fpx * 0.62), "%d%%" % pct, fill=(190, 190, 190), font=sml)
                pct += 5
        rk = R(keel_row)
        if 0 <= rk < Hd_:
            d.line([(0, rk), (Wd, rk)], fill=(150, 150, 150), width=1)
            d.text((Wd - 190, rk + 4), "keel  z %+.4f" % z_min, fill=(150, 150, 150), font=sml)
        for c in cands:
            r = R(c["row"])
            if -2 <= r < Hd_ + 2:
                d.line([(0, r), (Wd, r)], fill=COLS[c["label"]], width=max(1, int(s)))
                d.text((Wd - 34, r - fpx * 0.75), c["label"], fill=COLS[c["label"]], font=big)
        return d, big, sml

    # -- full sheet
    sheet = base.copy()
    d, big, sml = annotate(sheet, 0, 0, 1.0, 20, ruler=True)
    d.text((8, 8), "E10 Step 0.1 - waterline_z candidates - beam camera y+000 e+00",
           fill=(255, 255, 255), font=big)
    d.text((8, 32), "The ladder spans keel to the founding exemplar's painted band top - "
                    "5.06%% of the hull's z-span, so A/B/C sit %d px apart. Ruler ticks "
                    "every 5%%; name any height." % round(cands[1]["row"] - cands[2]["row"]),
           fill=(210, 210, 210), font=sml)
    ly = 60
    for c in cands:
        d.rectangle([8, ly + 4, 26, ly + 18], fill=COLS[c["label"]])
        d.text((32, ly), "%s   z %+.5f   %.2f%% of hull z-span   row %.1f   %.2f%% of "
                         "the figure below"
               % (c["label"], c["z"], c["pct_of_mesh_z_span"], c["row"],
                  c["pct_of_figure_below"]), fill=(235, 235, 235), font=sml)
        ly += 22
    d.text((32, ly), "C = the exemplar's band top (measured, not chosen). A/B = 1/3, 2/3 "
                     "of keel-to-C.", fill=(180, 180, 180), font=sml)
    sheet_path = J(args.out, "STEP0_waterline_candidates.png")
    sheet.save(sheet_path)

    # -- zoom: the hull foot at his zoom, with enough hull above to judge against
    cols = np.where(hit.any(axis=0))[0]
    x0, x1 = max(0, int(cols.min()) - 20), min(W, int(cols.max()) + 20)
    y0 = int(min(c["row"] for c in cands) - 150)
    y1 = int(min(H, keel_row + 30))
    zf = 5
    zoom = base.crop((x0, y0, x1, y1))
    zoom = zoom.resize(((x1 - x0) * zf, (y1 - y0) * zf), Image.LANCZOS)
    dz, bigz, smlz = annotate(zoom, x0 * 0 + 0, y0, zf, 34, ruler=False)
    # the annotate() helper works in full-frame rows; x is already cropped, which is fine
    # because every line spans the full width.
    dz.text((10, 10), "E10 Step 0.1 - hull foot at %dx - rows %d-%d" % (zf, y0, y1),
            fill=(255, 255, 255), font=bigz)
    zoom_path = J(args.out, "STEP0_waterline_candidates_ZOOM.png")
    zoom.save(zoom_path)
    rep["sheets"] = {"full": sheet_path, "zoom": zoom_path,
                     "zoom_crop": [x0, y0, x1, y1], "zoom_factor": zf}
    print("\n[sheet] %s" % sheet_path)
    print("[sheet] %s  (x %d-%d, rows %d-%d at %dx)" % (zoom_path, x0, x1, y0, y1, zf))

    json.dump(rep, open(J(args.out, "waterline_candidates.json"), "w"), indent=1)
    print("[json]  %s" % J(args.out, "waterline_candidates.json"))
    print("\nNo line is chosen here. The Director places it in one sentence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
