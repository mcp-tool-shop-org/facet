"""E10 Step 0.2 - the contact mask: texels whose surface sits below `waterline_z`.

Geometry answers this, not keying. The question "is this texel below the plane" is a
per-texel query the prep bake already answers, exactly - the same family as the exact
silhouette, and the reason E10's charter said the mask is geometric.

⚠ THREE FRAMES LIVE IN THIS PIPELINE AND THEY ARE ALL CALLED "position".
  1. the GLB's own coordinates (Y-up)
  2. the CANONICAL mesh frame - texpass_iter.load_scene()'s [x, -z, y] / max|v| * 0.5.
     Every cam.json quantity is in this frame; `waterline_z` is ruled in it (ship.json).
  3. prep's pos.npy - the canonical frame's PERMUTED-BUT-UNNORMALISED bbox (meta.lo/hi)
     remapped per-axis into the UNIT CUBE. pos.npy holds numbers in [0,1], not world units.
E10 Ruling 2 measured what confusing 1 and 2 costs: every z on the wrong row, under a sheet
that looks entirely plausible. So the conversion here is CHECKED against the mesh before
it is used, and the finished mask is checked again end-to-end by rendering it.

THE ANCHORS, and what a failure of each would mean:
  A. frame     - z reconstructed from pos.npy must span the same range as the mesh's own
                 canonical z. A miss means the unit-cube conversion is wrong.
  B. stability - the mask is a pure function of (mesh, plane): computed twice from a fresh
                 read it must be identical, and the written bytes must hash equal across
                 two RUNS of this tool (the spec's byte-stability anchor).
  C. projection- every contact texel's world position, projected with commit's formula,
                 must land inside the exact silhouette. Tests frame correctness, and it is
                 NOT vacuous: a wrong frame puts texels outside the figure.
  D. end-to-end- the mask rendered THROUGH THE RAYCAST must have its top edge at the placed
                 line's row. This is the check that can really fail: it runs texel -> bake
                 -> mask -> atlas -> raycast -> rows, an entirely different path from the
                 z -> row arithmetic, so a wrong frame, a wrong axis or a UV mismatch all
                 surface here.

  Note on "mask subset of silhouette": measured through the RENDER that is near-vacuous -
  a raycast can only show the mask where surface exists. It is reported for the spec's
  sake, and anchor C is the version of that question that can fail.

Standards compliance:
  PIN_PER_STEP - waterline_z and its frame are READ from profiles/ship.json, never typed;
    every derived constant is echoed with its source.
  ANDON_AUTHORITY - four anchors, each with a describable non-zero failure; any halts.
  NAMED_COMPENSATORS - writes only into --out. Undo = delete it. The accepted base asset is
    never opened for writing; it is not read here either.
  EXTERNAL_VERIFIER - the mask is not graded here. Arm W1 measures it against the founding
    exemplar, and that prediction stays blind until then.

  e10_contact_mask.py [--out DIR] [--render/--no-render]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import distance_transform_edt

Image.MAX_IMAGE_PIXELS = None

# ---- E10 Ruling 4's two corrections, with their derivations -------------------------
# ON-SURFACE CUT. The mask intersects with "this texel's baked position is on the mesh".
# 2.5065% of the bake's uv-valid texels are not (median 46 px off, max 147), while the
# bake's clean median is 0.006 px - four orders of separation, which is why 5 px is a
# reporting cut rather than a tuned edge. E08 A27 one layer down: the trust question is
# only askable where surface exists, and the layer must not inherit paint-on-no-surface
# into its first texel.
ONSURFACE_MAX_PX = 5.0
# ANCHOR C, REPLACED (ledger forty). The old form - rounded-pixel membership in a binary
# raycast mask - has a correct-input score structurally below 100%: the mesh's OWN
# vertices below the line score 99.4506%, every miss at exactly 1.00 px. The property is
# containment; the honest form is DISTANCE. 1.5 px sits above the rasterization rim
# quantum (1.00 px, arithmetic) and 30x below the failure signal (46 px median). Neither
# side of that derivation is the fired number's to move.
ANCHOR_C_MAX_PX = 1.5

PY = r"E:\AI-Models\trellis2-env\Scripts\python.exe"
TOOL = r"E:\AI\facet\tools\texpass_iter.py"
REPO = r"E:\AI\facet"
STROKE = r"E:\AI\training\facet_next\E04_stroke"
ARMT = r"E:\AI\training\facet_next\E04_armT72"
PREP = r"E:\AI\training\facet_next\E04_shipprep"
CAMS = [("beam_y000_e00", 0, 0), ("deck_y000_e40", 0, 40), ("deck_y180_e40", 180, 40)]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def canonical_vertices(path):
    """texpass_iter.load_scene()'s frame. The fourth copy; see E10 Ruling 2."""
    m = trimesh.load(path, force="mesh", process=False)
    v = np.asarray(m.vertices, dtype=np.float64)
    return np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5


def texel_z_canonical(meta):
    """pos.npy -> canonical z. Unit cube -> meta bbox -> max-abs normalisation."""
    pos_z = np.asarray(np.load(os.path.join(PREP, "pos.npy"), mmap_mode="r")[..., 2],
                       dtype=np.float64)
    lo, hi = meta["lo"][2], meta["hi"][2]
    return (lo + pos_z * (hi - lo)) * (0.5 / meta["maxabs"])


def texel_positions(meta, sel):
    """pos.npy -> canonical world positions, for the selected texels."""
    pos = np.asarray(np.load(os.path.join(PREP, "pos.npy"), mmap_mode="r"),
                     dtype=np.float64)[sel]
    lo, hi = np.array(meta["lo"]), np.array(meta["hi"])
    return (lo + pos * (hi - lo)) * (0.5 / meta["maxabs"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(STROKE, "e10_contact"))
    ap.add_argument("--no-render", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    J = os.path.join
    rep = {}

    # ---- the ruled value, read from the profile -------------------------------------
    prof = json.load(open(J(REPO, "profiles", "ship.json"), encoding="utf-8"))
    WZ = float(prof["waterline"]["z"]["value"])
    rep["waterline_z"] = {"value": WZ, "from": "profiles/ship.json waterline.z",
                          "frame": prof["waterline"]["z"]["frame"][:60] + "..."}
    print("[line] waterline_z = %+.5f (profiles/ship.json, canonical mesh frame)" % WZ)

    meta = json.load(open(J(PREP, "meta.json"), encoding="utf-8"))
    uv_valid = np.asarray(np.load(J(PREP, "mask.npy"), mmap_mode="r")[..., 0]) > 0.5
    n_valid = int(uv_valid.sum())

    # ---- ANCHOR A: the frame conversion, checked against the mesh -------------------
    zc = texel_z_canonical(meta)
    mesh_z = canonical_vertices(J(PREP, "prep_uv.glb"))[:, 2]
    tz = zc[uv_valid]
    dlo, dhi = abs(tz.min() - mesh_z.min()), abs(tz.max() - mesh_z.max())
    rep["anchor_A_frame"] = {
        "texel_z_range": [float(tz.min()), float(tz.max())],
        "mesh_z_range": [float(mesh_z.min()), float(mesh_z.max())],
        "delta_lo": float(dlo), "delta_hi": float(dhi), "tolerance": 2e-3}
    print("[A] texel z [%+.6f, %+.6f] vs mesh z [%+.6f, %+.6f]  (d_lo %.2e, d_hi %.2e)"
          % (tz.min(), tz.max(), mesh_z.min(), mesh_z.max(), dlo, dhi))
    if max(dlo, dhi) > 2e-3:
        print("ANDON A: pos.npy does not reconstruct the mesh's canonical z. HALT.")
        return 1

    # ---- the mask, with Ruling 4's on-surface intersection ---------------------------
    cam0 = json.load(open(J(STROKE, "sheet", "asset", "job_y+000_e+00", "cam.json")))
    one_px = cam0["v_ext"] / cam0["H"]
    scene = o3d.t.geometry.RaycastingScene()
    Vc = canonical_vertices(J(PREP, "prep_uv.glb"))
    Fc = np.asarray(trimesh.load(J(PREP, "prep_uv.glb"), force="mesh",
                                 process=False).faces, dtype=np.int64)
    scene.add_triangles(o3d.core.Tensor(Vc.astype(np.float32)),
                        o3d.core.Tensor(Fc.astype(np.uint32)))

    def build_mask():
        """The mask is a pure function of (bake, mesh, plane). Ruling 4 adds on-surface."""
        z = texel_z_canonical(meta)
        uv = np.asarray(np.load(J(PREP, "mask.npy"), mmap_mode="r")[..., 0]) > 0.5
        below = (z <= WZ) & uv
        P = texel_positions(meta, below)
        d = scene.compute_distance(o3d.core.Tensor(P.astype(np.float32))).numpy()
        keep = d <= ONSURFACE_MAX_PX * one_px
        out = np.zeros_like(below)
        ys, xs = np.where(below)
        out[ys[keep], xs[keep]] = True
        return out, int(below.sum()), d

    contact, n_below, d_surf = build_mask()
    n_contact = int(contact.sum())
    n_excluded = n_below - n_contact
    rep["mask"] = {
        "below_the_line": n_below, "excluded_off_surface": n_excluded,
        "contact_texels": n_contact, "uv_valid_texels": n_valid,
        "pct_of_uv_valid": 100.0 * n_contact / n_valid,
        "onsurface_cut_px": ONSURFACE_MAX_PX,
        "excluded_pct_of_below": 100.0 * n_excluded / max(1, n_below),
        "excluded_distance_median_px": float(
            np.median(d_surf[d_surf > ONSURFACE_MAX_PX * one_px]) / one_px)
        if n_excluded else None}
    print("[mask] %d texels below the line; %d excluded as off-surface (>%.0f px, %.3f%% "
          "of below); %d contact texels of %d uv-valid (%.3f%%)"
          % (n_below, n_excluded, ONSURFACE_MAX_PX,
             100.0 * n_excluded / max(1, n_below), n_contact, n_valid,
             100.0 * n_contact / n_valid))
    if n_contact == 0:
        print("ANDON: the contact mask is empty at the placed line. HALT.")
        return 1

    # ---- ANCHOR B (first half): pure function, recomputed from a fresh read ----------
    contact2, _, _ = build_mask()
    if not np.array_equal(contact, contact2):
        print("ANDON B: the mask is not a pure function of (mesh, plane). HALT.")
        return 1
    print("[B] recomputed from a fresh read: identical")

    npy_path = J(args.out, "contact_mask.npy")
    np.save(npy_path, contact)
    atlas = np.zeros(contact.shape + (3,), dtype=np.uint8)
    atlas[contact] = (255, 255, 255)
    Image.fromarray(atlas).save(J(args.out, "contact_mask_atlas.png"))
    rep["files"] = {"npy": npy_path, "npy_sha256": sha256(npy_path),
                    "atlas": J(args.out, "contact_mask_atlas.png")}
    print("[B] contact_mask.npy sha256 %s" % rep["files"]["npy_sha256"])
    print("    (run this tool twice and compare that line - the spec's two-run anchor)")

    # ---- ANCHOR C (Ruling 4's form): DISTANCE to the silhouette, not membership ------
    cam = cam0
    P = texel_positions(meta, contact)
    th = np.radians(cam["yaw"])
    cd = np.array([np.sin(th), -np.cos(th), 0.0])
    look = -cd / np.linalg.norm(cd)
    right = np.cross(look, [0, 0, 1.0]); right /= np.linalg.norm(right)
    up = np.cross(right, look); up /= np.linalg.norm(up)
    bmid = np.array(cam["bmid"])
    px = ((P - bmid) @ right / cam["h_ext"] + 0.5) * cam["W"] - 0.5
    py = (0.5 - (P - bmid) @ up / cam["v_ext"]) * cam["H"] - 0.5
    hit = np.asarray(Image.open(J(STROKE, "sheet", "asset", "job_y+000_e+00",
                                  "hit.png")).convert("L")) > 0
    xi = np.clip(np.round(px).astype(int), 0, cam["W"] - 1)
    yi = np.clip(np.round(py).astype(int), 0, cam["H"] - 1)
    # distance from each projection to the silhouette: 0 inside, >0 outside
    dsil = distance_transform_edt(~hit)[yi, xi]
    worst = float(dsil.max())
    inside = hit[yi, xi]
    line_row = (0.5 - (WZ - bmid[2]) / cam["v_ext"]) * cam["H"] - 0.5
    rep["anchor_C_projection"] = {
        "form": "distance to the exact silhouette (Ruling 4); the membership form was "
                "withdrawn on its own control at 99.4506%",
        "bound_px": ANCHOR_C_MAX_PX,
        "contact_texels_projected": int(len(dsil)),
        "max_distance_px": worst,
        "median_distance_px": float(np.median(dsil)),
        "p99_distance_px": float(np.percentile(dsil, 99)),
        "strictly_inside_pct": float(100.0 * inside.mean()),
        "projected_row_min": float(py.min()), "projected_row_max": float(py.max()),
        "placed_line_row": float(line_row)}
    print("[C] worst projection distance to the exact silhouette: %.3f px "
          "(bound %.1f) | median %.3f | p99 %.3f | strictly inside %.4f%%"
          % (worst, ANCHOR_C_MAX_PX, np.median(dsil), np.percentile(dsil, 99),
             100.0 * inside.mean()))
    print("    projected rows %.1f-%.1f; the placed line is row %.1f"
          % (py.min(), py.max(), line_row))
    if worst > ANCHOR_C_MAX_PX:
        print("ANDON C: a contact texel projects %.3f px outside the silhouette, past "
              "the %.1f px bound. Ruling 4 pre-stated this case: a NEW FINDING and a "
              "halt, not a tuning input. HALT." % (worst, ANCHOR_C_MAX_PX))
        return 1

    # ---- ANCHOR D: render the mask through the raycast ------------------------------
    if args.no_render:
        json.dump(rep, open(J(args.out, "contact_mask.json"), "w"), indent=1)
        print("[skip] --no-render: anchor D not run")
        return 0
    st = J(args.out, "state")
    os.makedirs(st, exist_ok=True)
    Image.fromarray(atlas).save(J(st, "atlas.png"))
    for src, dst in [("stage1_8cam_holes.png", "holes.png"),
                     ("stage1_8cam_styled_mask.npy", "styled_mask.npy")]:
        d = J(st, dst)
        if not os.path.exists(d):
            import shutil
            shutil.copy(J(ARMT, "stage1", src), d)
    rep["anchor_D_render"] = {}
    for name, yaw, el in CAMS:
        r = subprocess.run([PY, TOOL, "emit", "--state", st, "--prep", PREP,
                            "--glb", J(PREP, "prep_uv.glb"), "--yaw", str(yaw),
                            "--el", str(el), "--profile", J(REPO, "profiles", "ship.json")],
                           capture_output=True, text=True)
        if r.returncode:
            print("ANDON: emit failed for %s\n%s" % (name, r.stderr[-500:]))
            return 1
        job = J(st, "job_y%+04d_e%+03d" % (yaw, el))
        band = np.asarray(Image.open(J(job, "render.png")).convert("L")) > 127
        sil = np.asarray(Image.open(J(job, "hit.png")).convert("L")) > 0
        rows = np.where(band.any(axis=1))[0]
        outside = int((band & ~sil).sum())
        e = {"band_px": int(band.sum()), "top_row": int(rows.min()) if len(rows) else None,
             "bottom_row": int(rows.max()) if len(rows) else None,
             "px_outside_exact_silhouette": outside,
             "pct_of_silhouette": 100.0 * band.sum() / max(1, sil.sum())}
        rep["anchor_D_render"][name] = e
        print("[D] %-14s band %6d px  rows %s-%s  outside silhouette %d  (%.2f%% of figure)"
              % (name, e["band_px"], e["top_row"], e["bottom_row"], outside,
                 e["pct_of_silhouette"]))
        if outside:
            print("ANDON D: rendered contact mask falls outside the exact silhouette. HALT.")
            return 1
        if name == "beam_y000_e00":
            drow = abs(e["top_row"] - line_row)
            rep["anchor_D_render"][name]["top_row_vs_placed_line"] = float(drow)
            print("    beam band top row %d vs placed line row %.1f -> delta %.1f px"
                  % (e["top_row"], line_row, drow))
            if drow > 3.0:
                print("ANDON D: the rendered band's top edge is not at the placed line. "
                      "HALT.")
                return 1

    json.dump(rep, open(J(args.out, "contact_mask.json"), "w"), indent=1)
    print("\n[json] %s" % J(args.out, "contact_mask.json"))
    print("The mask is built and anchored. It is NOT graded here - Arm W1 does that, and "
          "W-H1's prediction stays blind until it runs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
