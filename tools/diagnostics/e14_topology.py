"""E14 Gate 0 - the topology facts `mesh_stats` does not print. NO VERDICT.

⚠ THE OPERAND WARNING THIS TOOL EXISTS TO CARRY. "Shells" has two definitions and they do
not agree. `mesh_stats.vertex_components` counts components joined by a SHARED VERTEX, and
every shell number in this repo's family table - character 40-191, ship 237-512, dragon 9-12
- is that quantity. `trimesh.graph.connected_components(m.face_adjacency)` counts components
joined by a SHARED MANIFOLD EDGE, which drops every non-manifold edge from the graph. On a
mesh that is pinched, the second number can be enormously larger than the first: this tool's
first draft reported "3 shells" for a longsword whose vertex-shell count is 1, and the repo's
own law - a number that reproduces exactly can still be measured against the wrong object -
is why that draft was thrown away rather than published.

So BOTH are computed and they are named differently. `shells` is `mesh_stats`' quantity and
is the only one comparable with the family table. `pieces_manifold_adjacency` is the other
one, and it is reported because on a pinched surface it is diagnostic rather than redundant.

FOUR QUESTIONS, none of which mesh_stats or e12_nonmanifold.py answers between them:

1. IS THE SURFACE OPEN? `watertight: False` does not say. An OPEN sheet carries a boundary
   loop around its perimeter (edges with exactly one adjacent face); a CLOSED slab carries
   none. E12's dragons measured 1 / 0 / 1 boundary edges, all of ZERO LENGTH - degenerate
   edges, not an opening. A zero-length boundary edge and a boundary loop around a hole are
   the same integer and different facts, so this reports count AND total length AND the
   longest single boundary edge.

2. IS THE SOLID HOLLOW? A closed surface can enclose a cavity, and nothing above would show
   it. If the two largest manifold-adjacency pieces are nested - one enclosing positive
   volume, the other enclosing NEGATIVE volume, i.e. inward-facing - the reconstruction is a
   double wall around a void, and the material volume is the difference rather than the
   outer volume. The wall gap is measured as the distance from each inner vertex to the
   nearest outer vertex (KD-tree; `trimesh.proximity` needs rtree, which is not installed).

3. WHERE ARE THE WALLS? A cross-section scan, derived per mesh rather than hand-picked: at
   evenly spaced heights, in a thin window at the bbox's horizontal centre, cluster the face
   centroids by their coordinate on the thin axis and report how many walls a ray would
   cross. Two walls is a solid; four is a hollow shell.

4. DID A FLOOR RECONSTRUCT? Every E14 clay stands on its tip over a soft cast shadow, so the
   live question is whether ground or shadow geometry came back. The test is E12's: take the
   outermost slab of each axis and ask what share of surface area is in it and how much of
   that area FACES along that axis. A subject merely touching its box shows a small share at
   low axis-facing; a flat wall - a cut, or a floor - shows a large share at high
   axis-facing. E12's dragon 00001 read 1.021% of area at 93.7% facing straight down and
   that was flat foot soles on the ground plane.

Welding matches `mesh_stats` exactly - merge_vertices(merge_tex=True, merge_norm=True) - so
face totals here are comparable with the stats table rather than a second opinion.

WHAT IT DOES NOT DO. It does not measure blade thickness as a subject value: `thin_extent`
derivation is post-designation and out of scope by the E14 dispatch. The cross-section scan
reports where surfaces are; turning that into a policy number is a later session's job. It
grades nothing and compares no candidates.

Standards compliance:
  PIN_PER_STEP - every threshold is a flag and is echoed into the JSON.
  ANDON_AUTHORITY - raises if the GLB has no faces, and if the two shell definitions are
    silently conflated (the `shells` key is always the vertex quantity). Reports otherwise.
  NAMED_COMPENSATORS - reads a GLB, writes one JSON. Undo = delete it. Owner: the session.
  DECOMPOSE_BY_SECRETS - no constant inherited from another subject; the slab depth and the
    cross-section window are fractions of THIS mesh's own extent.
  EXTERNAL_VERIFIER - reports numbers a human rules on. The boundary and non-manifold
    arithmetic is independent of e12_nonmanifold.py's and is meant to agree with it; the
    vertex-shell count is meant to agree with mesh_stats.

  e14_topology.py --glb m.glb [--label L] [--slab 0.005] [--face-deg 45]
                  [--sections 9] [--section-window 0.004] [--out t.json]
"""
import argparse
import json
import os

import numpy as np
import trimesh
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--label", default=None)
ap.add_argument("--slab", type=float, default=0.005,
                help="outermost slab depth as a fraction of the extent on that axis")
ap.add_argument("--face-deg", type=float, default=45.0,
                help="a face counts as axis-facing if its normal is within this of the axis")
ap.add_argument("--sections", type=int, default=9, help="cross-section scan levels")
ap.add_argument("--section-window", type=float, default=0.004,
                help="half-window of a cross-section, as a fraction of the tallest extent")
ap.add_argument("--wall-gap", type=float, default=0.0006,
                help="cluster break between walls, as a fraction of the tallest extent")
ap.add_argument("--out", default=None)
args = ap.parse_args()

GLTF_TO_BLENDER = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]])
AX = ["x", "y", "z"]

m = trimesh.load(args.glb, force="mesh", process=False)
m.merge_vertices(merge_tex=True, merge_norm=True)
if not (len(m.faces)):
    raise AssertionError("ANDON: %s has no faces" % args.glb)

f = np.asarray(m.faces)
co = np.asarray(m.vertices, dtype=np.float64) @ GLTF_TO_BLENDER.T
lo, hi = co.min(axis=0), co.max(axis=0)
ext = hi - lo
H = float(ext.max())
lab = args.label or os.path.splitext(os.path.basename(args.glb))[0]
area = np.asarray(m.area_faces, dtype=np.float64)
tot_faces, tot_area = len(f), float(area.sum())

# ---- 1. edges: boundary count, total length, longest; non-manifold -------------------------
e = np.sort(np.vstack([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]]), axis=1)
uniq, cnt = np.unique(e, axis=0, return_counts=True)
bd, nm = uniq[cnt == 1], uniq[cnt > 2]
bl = np.linalg.norm(co[bd[:, 0]] - co[bd[:, 1]], axis=1) if len(bd) else np.zeros(0)
print("[topo] %s  unique edges %d | boundary(1 face) %d | non-manifold(>2) %d (%.4f%%)"
      % (lab, len(uniq), len(bd), len(nm), 100 * len(nm) / len(uniq)), flush=True)
print("[topo]   boundary total length %.8f | longest single boundary edge %.8f"
      % (float(bl.sum()), float(bl.max()) if len(bl) else 0.0), flush=True)

# ---- 2a. SHELLS, mesh_stats' definition: components joined by a shared VERTEX ---------------
ev = np.vstack([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]])
g = coo_matrix((np.ones(len(ev), dtype=np.int8), (ev[:, 0], ev[:, 1])),
               shape=(len(m.vertices), len(m.vertices)))
_, vlab = connected_components(g, directed=False)
face_shell = vlab[f[:, 0]]
shell_ids, shell_counts = np.unique(face_shell, return_counts=True)
order = np.argsort(-shell_counts)
n_shells = int(len(shell_ids))
largest_frac = float(shell_counts[order[0]] / tot_faces)
sat = []
for i in order[1:]:
    sel = face_shell == shell_ids[i]
    pts = co[f[sel].reshape(-1)]
    sat.append({"faces": int(sel.sum()),
                "face_frac": round(float(sel.sum() / tot_faces), 8),
                "area_frac": round(float(area[sel].sum() / tot_area), 8),
                "extent": [round(float(v), 5) for v in (pts.max(axis=0) - pts.min(axis=0))],
                "centre": [round(float(v), 5) for v in (pts.max(axis=0) + pts.min(axis=0)) / 2]})
print("[topo]   SHELLS (shared-vertex, = mesh_stats) %d | largest %.6f of faces | satellites %d"
      % (n_shells, largest_frac, len(sat)), flush=True)
for i, s in enumerate(sat[:12]):
    print("[topo]     sat %2d  %6d faces  extent %s  centre %s"
          % (i, s["faces"], s["extent"], s["centre"]), flush=True)

# ---- 2b. the OTHER partition: components joined by a shared MANIFOLD EDGE -------------------
pieces = sorted(trimesh.graph.connected_components(m.face_adjacency,
                                                   nodes=np.arange(tot_faces)),
                key=len, reverse=True)
print("[topo]   pieces (manifold-adjacency, NOT the shells column) %d | top %s"
      % (len(pieces), [len(p) for p in pieces[:4]]), flush=True)

# ---- 2c. hollow test: are the two largest pieces nested walls? -----------------------------
hollow = None
if len(pieces) >= 2 and len(pieces[1]) > 0.01 * tot_faces:
    vols = []
    for p in pieces[:2]:
        try:
            vols.append(float(trimesh.Trimesh(vertices=co, faces=f[p], process=False).volume))
        except Exception:
            vols.append(float("nan"))
    vA = np.unique(f[pieces[0]].reshape(-1))
    vB = np.unique(f[pieces[1]].reshape(-1))
    d, _ = cKDTree(co[vA]).query(co[vB])
    hollow = {"outer_faces": len(pieces[0]), "inner_faces": len(pieces[1]),
              "outer_volume": round(vols[0], 9), "inner_volume": round(vols[1], 9),
              "material_volume": round(vols[0] + vols[1], 9),
              "material_frac_of_outer": (round((vols[0] + vols[1]) / vols[0], 6)
                                         if vols[0] else None),
              "wall_gap_median": round(float(np.median(d)), 8),
              "wall_gap_p5": round(float(np.percentile(d, 5)), 8),
              "wall_gap_p95": round(float(np.percentile(d, 95)), 8),
              "wall_gap_median_frac_of_height": round(float(np.median(d) / H), 8)}
    print("[topo]   NESTED-WALL TEST: outer vol %+.6f  inner vol %+.6f  material %+.6f "
          "(%.1f%% of outer)" % (vols[0], vols[1], vols[0] + vols[1],
                                 100 * (vols[0] + vols[1]) / vols[0] if vols[0] else 0),
          flush=True)
    print("[topo]     wall gap median %.5f (%.3f%% of height) p5 %.5f p95 %.5f"
          % (np.median(d), 100 * np.median(d) / H, np.percentile(d, 5),
             np.percentile(d, 95)), flush=True)

# ---- 3. cross-section scan: how many walls would a ray cross? ------------------------------
thin = int(np.argmin(ext))          # the thinnest axis: the one a ray crosses walls along
tall = int(np.argmax(ext))          # the tallest axis: the one we scan along
wide = 3 - thin - tall
cen = co[f].mean(axis=1)
win, brk = args.section_window * H, args.wall_gap * H
mid_wide = (lo[wide] + hi[wide]) / 2.0
sections = []
print("[topo]   cross-sections: scanning along %s, window +-%.5f, thin axis %s"
      % (AX[tall], win, AX[thin]), flush=True)
for t in np.linspace(0.1, 0.9, args.sections):
    lvl = lo[tall] + t * ext[tall]
    sel = (np.abs(cen[:, tall] - lvl) < win) & (np.abs(cen[:, wide] - mid_wide) < win)
    if sel.sum() < 20:
        sections.append({"at_frac_of_height": round(float(t), 3), "faces": int(sel.sum()),
                         "walls": None})
        print("[topo]     %s=%.2f  %5d faces  - too few to cluster"
              % (AX[tall], t, sel.sum()), flush=True)
        continue
    v = np.sort(cen[sel][:, thin])
    grp = np.split(v, np.where(np.diff(v) > brk)[0] + 1)
    pos = [round(float(q.mean()), 5) for q in grp]
    sections.append({"at_frac_of_height": round(float(t), 3), "faces": int(sel.sum()),
                     "walls": len(grp), "wall_positions": pos})
    print("[topo]     %s=%.2f  %5d faces  %d wall(s) at %s = %s"
          % (AX[tall], t, sel.sum(), len(grp), AX[thin], pos), flush=True)

# ---- 4. the extremal slabs: is any bbox wall a flat surface? -------------------------------
nrm = np.asarray(m.face_normals, dtype=np.float64) @ GLTF_TO_BLENDER.T
cos_t = np.cos(np.radians(args.face_deg))
slabs = {}
for a in range(3):
    d0 = ext[a] * args.slab
    for side, sel in (("min", cen[:, a] <= lo[a] + d0), ("max", cen[:, a] >= hi[a] - d0)):
        key = "%s%s" % (AX[a], side)
        if not sel.any():
            slabs[key] = {"faces": 0, "area_frac": 0.0, "axis_facing_frac": 0.0}
            continue
        sa = float(area[sel].sum())
        fa = float(area[sel][np.abs(nrm[sel, a]) >= cos_t].sum())
        slabs[key] = {"faces": int(sel.sum()), "area_frac": round(sa / tot_area, 8),
                      "axis_facing_frac": round(fa / sa, 6) if sa else 0.0}
        print("[topo]   slab %s-%s  area %.4f%% of surface | %.1f%% of it faces along %s"
              % (AX[a], side, 100 * sa / tot_area, 100 * fa / sa if sa else 0.0, AX[a]),
              flush=True)

rec = {"label": lab, "glb": os.path.abspath(args.glb),
       "faces": tot_faces, "surface_area": round(tot_area, 8),
       "extent_blender": [round(float(v), 6) for v in ext],
       "bbox_blender": [[round(float(v), 6) for v in lo], [round(float(v), 6) for v in hi]],
       "edges_unique": int(len(uniq)), "boundary_edges": int(len(bd)),
       "boundary_total_length": round(float(bl.sum()), 10),
       "boundary_longest_edge": round(float(bl.max()) if len(bl) else 0.0, 10),
       "nonmanifold_edges": int(len(nm)),
       "nonmanifold_frac": round(float(len(nm) / len(uniq)), 8),
       "shells": n_shells,
       "shells_definition": "shared-vertex components, identical to mesh_stats.vertex_components",
       "largest_shell_frac": round(largest_frac, 8),
       "satellites": sat,
       "pieces_manifold_adjacency": len(pieces),
       "pieces_manifold_adjacency_sizes": [int(len(p)) for p in pieces[:8]],
       "pieces_definition": "shared-MANIFOLD-EDGE components; NOT the shells column; "
                            "non-manifold edges are absent from this graph",
       "nested_wall_test": hollow,
       "cross_sections": {"scan_axis": AX[tall], "thin_axis": AX[thin],
                          "window_frac": args.section_window,
                          "wall_break_frac": args.wall_gap, "levels": sections},
       "slab_depth_frac": args.slab, "face_deg": args.face_deg, "extremal_slabs": slabs}
if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(rec, open(args.out, "w"), indent=1)
    print("[topo] wrote %s" % os.path.abspath(args.out), flush=True)
