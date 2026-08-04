"""Identical measurement of any mesh — the numeric half of a comparison.

Comparisons across generation arms are only worth as much as the sameness of the
instrument. Every number here comes from one code path, so two meshes made months
apart by different tools are still measured the same way.

Two numbers carry the load:

  components          how many disconnected shells the surface is in. Collapse
                      decimation reallocates density by merging neighbours; shell
                      soup has no neighbours, so it tears holes instead. A budget
                      allocator needs this near 1.
  face_curvature_var  variance of discrete mean curvature inside the face rect. A
                      smooth blob scores near zero however many polygons it has;
                      eye sockets and a nose bridge score high. Polycount does not
                      answer "is there a face there" — this does.

Conventions, all deliberate:

  * The face is found by a FRONT-VIEW RECT, not a height band — a raised weapon
    rises above the crown, so a height band measures the blade. The projection is
    the one `smart_decimate.py` uses, unchanged, so "the face" means the same
    region to the allocator and to the instrument.
  * glTF is Y-up and Blender is Z-up. Vertices are rotated into Blender convention
    on load, because the rect was authored against Blender renders.
  * Vertices are WELDED before any topology or curvature number. A GLB export
    splits vertices at every UV seam, so an unwelded read of a textured mesh
    reports far more shells than the surface has. `components_unwelded` is kept
    beside the real number to make that visible rather than confusing.
  * Curvature is measured on the mesh scaled to the pipeline's std frame
    (maxabs = 0.5) so the value does not track how big the export happened to be.

  mesh_stats.py --glb a.glb b.glb [--out stats.json] [--label a b]
                [--crop 360,240,700,600] [--crop-res 1024] [--bound 0.55]
"""
import argparse
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import subject_profile
import json
import os
import sys

import numpy as np
import trimesh
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
from trimesh.curvature import line_ball_intersection

ap = argparse.ArgumentParser()
ap.add_argument("--glb", nargs="+", required=True)
ap.add_argument("--label", nargs="*", default=None, help="one per --glb; defaults to filename")
ap.add_argument("--out", default=None, help="write the JSON here as well as stdout")
ap.add_argument("--crop", default="360,240,700,600", help="face rect, front-view pixels")
ap.add_argument("--crop-res", type=int, default=1024)
ap.add_argument("--bound", type=float, default=0.55)
ap.add_argument("--grid", type=int, default=256,
                help="occupancy grid for the projected-silhouette area")
ap.add_argument("--curv-samples", type=int, default=4000,
                help="max curvature probe points inside the rect; deterministic stride")
ap.add_argument("--curv-radius-frac", type=float, default=0.01,
                help="ball radius as a fraction of the std-frame bbox diagonal")
args = ap.parse_args(subject_profile.bind(ap, "verify/mesh_stats.py", None))
CX0, CY0, CX1, CY1 = [float(v) for v in args.crop.split(",")]
labels = args.label or []
if labels and len(labels) != len(args.glb):
    print("[stats] ANDON: --label count must match --glb count", file=sys.stderr)
    sys.exit(2)

# glTF Y-up -> Blender Z-up, the convention the face rect was authored against
GLTF_TO_BLENDER = np.array([[1.0, 0.0, 0.0],
                            [0.0, 0.0, -1.0],
                            [0.0, 1.0, 0.0]])


def vertex_components(faces, n_verts):
    """Connected components by SHARED VERTICES, returned as a per-face label."""
    if len(faces) == 0:
        return np.zeros(0, dtype=np.int64), 0
    e = np.vstack([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
    g = coo_matrix((np.ones(len(e), dtype=np.int8), (e[:, 0], e[:, 1])),
                   shape=(n_verts, n_verts))
    _, lab = connected_components(g, directed=False)
    face_lab = lab[faces[:, 0]]
    return face_lab, int(len(np.unique(face_lab)))


def project(co, maxabs):
    """Front-view pixel projection — verbatim from smart_decimate.py."""
    b = args.bound
    px = (co[:, 0] / maxabs * 0.5 + b) / (2 * b) * args.crop_res
    py = (b - co[:, 2] / maxabs * 0.5) / (2 * b) * args.crop_res
    return px, py


def mean_curvature(verts, adj_edges, adj_angles, adj_convex, points, radius):
    """trimesh's discrete mean curvature measure, KD-tree candidate query.

    trimesh.curvature.discrete_mean_curvature_measure needs `rtree` for its
    bbox query. A KD-tree on edge midpoints with radius + max half-edge gives the
    same candidate superset, and line_ball_intersection zeroes every edge that
    does not actually meet the ball — so the value is unchanged, minus a
    dependency this repo does not otherwise carry.
    """
    if len(adj_edges) == 0:
        return np.zeros(len(points))
    ep = verts[adj_edges]
    mid = ep.mean(axis=1)
    half = np.linalg.norm(ep[:, 1] - ep[:, 0], axis=1) * 0.5
    tree = cKDTree(mid)
    cand = tree.query_ball_point(points, radius + float(half.max()))
    out = np.zeros(len(points))
    for i, (x, c) in enumerate(zip(points, cand)):
        if not c:
            continue
        c = np.asarray(c)
        lengths = line_ball_intersection(ep[c, 0], ep[c, 1], center=x, radius=radius)
        signs = np.where(adj_convex[c], 1, -1)
        out[i] = (lengths * adj_angles[c] * signs).sum() / 2
    return out


def measure(path, label):
    m = trimesh.load(path, force="mesh", process=False)
    raw_faces, raw_verts = len(m.faces), len(m.vertices)
    _, comp_unwelded = vertex_components(np.asarray(m.faces), raw_verts)

    # UV seams split vertices on export; weld before any topology claim
    m.merge_vertices(merge_tex=True, merge_norm=True)
    faces = np.asarray(m.faces)
    n_faces = len(faces)
    n_verts = int(len(np.unique(faces)))
    face_lab, n_comp = vertex_components(faces, len(m.vertices))
    counts = np.bincount(face_lab)
    largest = float(counts.max() / n_faces) if n_faces else 0.0

    co = np.asarray(m.vertices, dtype=np.float64) @ GLTF_TO_BLENDER.T
    lo, hi = co.min(axis=0), co.max(axis=0)
    ext = hi - lo
    maxabs = float(np.abs(co).max())
    px, py = project(co, maxabs)

    cen = co[faces].mean(axis=1)
    cpx, cpy = project(cen, maxabs)
    in_rect = (cpx >= CX0) & (cpx <= CX1) & (cpy >= CY0) & (cpy <= CY1)
    rect_faces = int(in_rect.sum())

    # projected silhouette area by occupancy grid, from vertices + face centroids
    s = args.grid / args.crop_res
    gx = np.concatenate([px, cpx]) * s
    gy = np.concatenate([py, cpy]) * s
    keep = (gx >= 0) & (gx < args.grid) & (gy >= 0) & (gy < args.grid)
    cells = np.unique(gy[keep].astype(np.int64) * args.grid + gx[keep].astype(np.int64))
    px_per_cell = (args.crop_res / args.grid) ** 2
    figure_area = float(len(cells) * px_per_cell)
    rect_area = (CX1 - CX0) * (CY1 - CY0)
    rect_frac = rect_area / figure_area if figure_area else float("nan")
    density = rect_faces / rect_frac if rect_frac else float("nan")

    # is the occupancy grid a fair stand-in for a rasteriser on this mesh?
    tri = np.stack([px[faces], py[faces]], axis=-1)
    edge_px = np.linalg.norm(tri - np.roll(tri, 1, axis=1), axis=2).max(axis=1)
    med_tri_cells = float(np.median(edge_px) * s)

    # curvature in the pipeline std frame so scale does not leak into the number
    sc = co * (0.5 / maxabs)
    diag = float(np.linalg.norm(ext * (0.5 / maxabs)))
    radius = args.curv_radius_frac * diag
    v_rect = np.where((px >= CX0) & (px <= CX1) & (py >= CY0) & (py <= CY1))[0]
    if len(v_rect) > args.curv_samples:
        v_rect = v_rect[np.linspace(0, len(v_rect) - 1, args.curv_samples).astype(np.int64)]
    if len(v_rect):
        cv = mean_curvature(sc, np.asarray(m.face_adjacency_edges),
                            np.asarray(m.face_adjacency_angles),
                            np.asarray(m.face_adjacency_convex),
                            sc[v_rect], radius)
        curv_var, curv_mean = float(cv.var()), float(cv.mean())
    else:
        curv_var, curv_mean = float("nan"), float("nan")

    return {
        "label": label,
        "path": os.path.abspath(path),
        "faces": n_faces,
        "verts": n_verts,
        "components": n_comp,
        "largest_component_frac": round(largest, 6),
        "watertight": bool(m.is_watertight),
        "face_rect_faces": rect_faces,
        "face_rect_density": round(density, 1),
        "face_curvature_var": curv_var,
        "face_curvature_mean": curv_mean,
        "curv_samples": int(len(v_rect)),
        "curv_radius": round(radius, 6),
        "bbox_blender": [[round(float(v), 4) for v in lo], [round(float(v), 4) for v in hi]],
        "extent_blender": [round(float(v), 4) for v in ext],
        "maxabs": round(maxabs, 6),
        "rect_frac_of_figure": round(rect_frac, 6),
        "figure_area_px2": round(figure_area, 1),
        "components_unwelded": comp_unwelded,
        "faces_unwelded": raw_faces,
        "verts_unwelded": raw_verts,
        "up_axis_dominant": bool(ext[2] >= ext[0] and ext[2] >= ext[1]),
        "median_tri_cells": round(med_tri_cells, 3),
    }


rows = []
for i, p in enumerate(args.glb):
    lab = labels[i] if labels else os.path.splitext(os.path.basename(p))[0]
    r = measure(p, lab)
    rows.append(r)
    print(f"[stats] {r['label']}: {r['faces']:,}f {r['verts']:,}v | "
          f"components {r['components']:,} (largest {r['largest_component_frac']:.3f}) | "
          f"watertight {r['watertight']} | rect {r['face_rect_faces']:,}f "
          f"density {r['face_rect_density']:,.0f} | curv_var {r['face_curvature_var']:.6g}",
          flush=True)
    if not r["up_axis_dominant"]:
        print(f"[stats] WARNING {r['label']}: vertical extent is not the largest "
              f"({r['extent_blender']}) — the front-view rect may not be on the head",
              flush=True)
    if r["median_tri_cells"] > 1.5:
        print(f"[stats] WARNING {r['label']}: median triangle spans "
              f"{r['median_tri_cells']:.2f} occupancy cells — silhouette area is "
              f"under-counted; raise --grid or treat density as approximate", flush=True)

blob = {"meshes": rows, "params": {"crop": args.crop, "crop_res": args.crop_res,
                                   "bound": args.bound, "grid": args.grid,
                                   "curv_samples": args.curv_samples,
                                   "curv_radius_frac": args.curv_radius_frac}}
print(json.dumps(blob, indent=1))
if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(blob, open(args.out, "w"), indent=1)
    print(f"[stats] wrote {os.path.abspath(args.out)}", flush=True)
