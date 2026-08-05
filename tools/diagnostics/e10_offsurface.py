"""Does the prep bake's position map lie on the mesh? Measured, because E10's Step 0.2
anchor C fired and the cause had to be read before anything was decided.

WHAT THIS ASKS. `pos.npy` gives a world position per texel and `mask.npy` says which
texels are uv-valid. Every consumer of the bake has assumed a uv-valid texel's position
is ON the surface. Nothing had ever measured it. This asks the question directly -
distance from each reconstructed texel position to the mesh, via open3d's raycasting
scene - rather than through a proxy.

WHY IT IS ITS OWN FILE. e10_contact_mask.py's anchor C fired as specified. Adding a
diagnostic to a gate after watching it fire is how a gate quietly becomes whatever passes,
so the gate is untouched and the new instrument lives here. It reports; it halts nothing.

  e10_offsurface.py [--sample N]
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import distance_transform_edt

Image.MAX_IMAGE_PIXELS = None
PREP = r"E:\AI\training\facet_next\E04_shipprep"
STROKE = r"E:\AI\training\facet_next\E04_stroke"


def canonical(v):
    return np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=200000)
    ap.add_argument("--out", default=os.path.join(STROKE, "e10_contact",
                                                  "offsurface.json"))
    args = ap.parse_args()
    J = os.path.join
    rep = {}

    meta = json.load(open(J(PREP, "meta.json"), encoding="utf-8"))
    cam = json.load(open(J(STROKE, "sheet", "asset", "job_y+000_e+00", "cam.json")))
    one_px = cam["v_ext"] / cam["H"]
    rep["one_image_px_in_canonical_units"] = one_px

    m = trimesh.load(J(PREP, "prep_uv.glb"), force="mesh", process=False)
    V = canonical(np.asarray(m.vertices, dtype=np.float64))
    F = np.asarray(m.faces, dtype=np.int64)
    rs = o3d.t.geometry.RaycastingScene()
    rs.add_triangles(o3d.core.Tensor(V.astype(np.float32)),
                     o3d.core.Tensor(F.astype(np.uint32)))

    pos = np.asarray(np.load(J(PREP, "pos.npy"), mmap_mode="r"), dtype=np.float64)
    uv = np.asarray(np.load(J(PREP, "mask.npy"), mmap_mode="r")[..., 0]) > 0.5
    lo, hi, s = np.array(meta["lo"]), np.array(meta["hi"]), 0.5 / meta["maxabs"]

    # --- the bake, sampled ---------------------------------------------------------
    ys, xs = np.where(uv)
    k = np.random.default_rng(0).choice(len(ys), min(args.sample, len(ys)), replace=False)
    P = (lo + pos[ys[k], xs[k]] * (hi - lo)) * s
    d = rs.compute_distance(o3d.core.Tensor(P.astype(np.float32))).numpy()
    rep["bake"] = {
        "uv_valid_texels": int(uv.sum()), "sampled": int(len(k)),
        "median_distance": float(np.median(d)),
        "pct_off_surface_gt_1px": float(100.0 * (d > one_px).mean()),
        "pct_off_surface_gt_5px": float(100.0 * (d > 5 * one_px).mean()),
        "max_distance_px": float(d.max() / one_px)}
    print("[bake] %d uv-valid texels, %d sampled" % (uv.sum(), len(k)))
    print("       median distance to surface %.2e (%.3f px)"
          % (np.median(d), np.median(d) / one_px))
    print("       OFF-SURFACE (>1 px): %.4f%%   (>5 px): %.4f%%   max %.1f px"
          % (rep["bake"]["pct_off_surface_gt_1px"], rep["bake"]["pct_off_surface_gt_5px"],
             rep["bake"]["max_distance_px"]))

    # --- the control: the mesh's own vertices through anchor C's check ---------------
    prof = json.load(open(r"E:\AI\facet\profiles\ship.json", encoding="utf-8"))
    WZ = float(prof["waterline"]["z"]["value"])
    th = np.radians(cam["yaw"])
    look = -np.array([np.sin(th), -np.cos(th), 0.0])
    look /= np.linalg.norm(look)
    right = np.cross(look, [0, 0, 1.0]); right /= np.linalg.norm(right)
    up = np.cross(right, look); up /= np.linalg.norm(up)
    bmid = np.array(cam["bmid"])
    hit = np.asarray(Image.open(J(STROKE, "sheet", "asset", "job_y+000_e+00",
                                  "hit.png")).convert("L")) > 0
    dout = distance_transform_edt(~hit)

    def containment(Q):
        px = ((Q - bmid) @ right / cam["h_ext"] + 0.5) * cam["W"] - 0.5
        py = (0.5 - (Q - bmid) @ up / cam["v_ext"]) * cam["H"] - 0.5
        xi = np.clip(np.round(px).astype(int), 0, cam["W"] - 1)
        yi = np.clip(np.round(py).astype(int), 0, cam["H"] - 1)
        ins = hit[yi, xi]
        return ins, dout[yi[~ins], xi[~ins]] if (~ins).any() else np.zeros(0)

    sub = V[V[:, 2] <= WZ]
    ins, dd = containment(sub)
    rep["control_mesh_vertices"] = {
        "vertices_below_line": int(len(sub)), "inside_pct": float(100.0 * ins.mean()),
        "outside": int((~ins).sum()),
        "outside_distance_max_px": float(dd.max()) if len(dd) else 0.0,
        "outside_distance_median_px": float(np.median(dd)) if len(dd) else 0.0}
    print("\n[control] THE MESH'S OWN VERTICES below the placed line, through anchor C:")
    print("          %d vertices, %.4f%% inside, %d outside, every miss at %.2f px"
          % (len(sub), 100 * ins.mean(), (~ins).sum(),
             dd.max() if len(dd) else 0.0))
    print("          -> the check cannot be passed by the geometry it validates.")

    json.dump(rep, open(args.out, "w"), indent=1)
    print("\n[json] %s" % args.out)
    print("Reported, not ruled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
