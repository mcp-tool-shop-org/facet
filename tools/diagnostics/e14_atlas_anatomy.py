"""What IS the atlas, on a hollow double-walled mesh? Three linked questions, one pass.

E14 Ruling 3 banked the route-wide finding that every TRELLIS.2 `1024_cascade` reconstruction
this route has made is a hollow double-walled shell. That was measured on GEOMETRY. This asks
what it means for the ATLAS - the denominator every coverage number on this route is a
fraction of - and it exists because two numbers came in this session that a geometry finding
alone does not explain:

  1. THE CEILING'S MECHANISM. `e08_ceiling` casts a real first-hit ray, so an inner wall is
     unreachable BY CONSTRUCTION. If the reach ceiling is bounded by the hollow rather than by
     camera count, then the unreachable set should BE the inner wall - not merely be about the
     same size as it. Same size is a coincidence; identity is a mechanism. This measures which
     it is, per texel, instead of inferring it from a face-count ratio.

  2. THE OFF-SURFACE RATE. `e12_offsurface` measured 11.09% on this subject against a
     2.50-2.64% replication across three prior subjects. Before that becomes a subject
     property it has to survive the obvious alternative: bake margin. `scene.render.bake.margin
     = 8` dilates every island, and this subject packs 46,496 islands against the beast's
     28,870, so a larger share of its "valid" texels are margin rather than triangle interior.
     Eroding the valid mask and re-measuring separates the two readings.

  3. THE DENOMINATOR ITSELF. "% of valid" is only meaningful if you know what valid is made
     of. This subject bakes 21.83% of the atlas valid from 2.62% of triangle UV area - 8.3x,
     against the ship's 6.16x and the beast's 4.41x (E12 Task 2). Reported so no downstream
     percentage is read as a fraction of painted surface when it is a fraction of something
     else.

WHY THE TWO SHELL DEFINITIONS ARE BOTH HERE. E14 Ruling 2b banked that vertex-connected
components and manifold-edge components differ by hundreds on these meshes: the outer and
inner walls are ONE vertex-shell (they touch at pinches) and TWO manifold-edge pieces. This
file uses the manifold-edge partition, names it as such in every output, and decides which
piece is outer by SIGNED VOLUME - an inward-facing closed wall encloses negative volume - so
"outer" is measured rather than assumed from size.

  e14_atlas_anatomy.py --prep DIR [--views 0,45,...] [--facing-min 0.45] [--sample 300000]
                       [--erode 4,8,12] [--out j.json]

Standards compliance: PIN_PER_STEP - every threshold is a flag, sample size and seed echoed,
output JSON beside the bake. ANDON_AUTHORITY - none; this classifies and adopts nothing.
EXTERNAL_VERIFIER - the reachability computation is re-derived here from project_twins'
definition and is ASSERTED to reproduce e08_ceiling's own 8-camera total on the same bake,
so a divergence between the two files is caught rather than assumed away.
"""
import argparse
import json
import os

import cv2
import numpy as np
import open3d as o3d
import trimesh

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--views", default="0,45,90,135,180,225,270,315")
ap.add_argument("--facing-min", type=float, default=0.45)
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--sample", type=int, default=300000)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--erode", default="2,4,8,12",
                help="valid-mask erosion depths in texels, for the margin split")
ap.add_argument("--px-unit", type=float, default=None,
                help="one emit pixel in canonical units; required for the off-surface split")
ap.add_argument("--ceiling-json", default=None,
                help="e08_ceiling's output on the SAME bake; its 8-camera total is asserted")
ap.add_argument("--out", default=None)
args = ap.parse_args()

J = os.path.join
meta = json.load(open(J(args.prep, "meta.json"), encoding="utf-8"))
RES = meta["res"]
mask2d = np.load(J(args.prep, "mask.npy"))[..., 0] > 0.5
lo = np.array(meta["lo"], dtype=np.float64)
hi = np.array(meta["hi"], dtype=np.float64)
valid = mask2d.reshape(-1)
NV = int(valid.sum())
P = (np.load(J(args.prep, "pos.npy")).reshape(-1, 3)[valid].astype(np.float64)
     * (hi - lo) + lo) / meta["maxabs"] * 0.5
N = np.load(J(args.prep, "nor.npy")).reshape(-1, 3)[valid].astype(np.float64) * 2.0 - 1.0
N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12

m = trimesh.load(J(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
V = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(V.astype(np.float32)), o3d.core.Tensor(f.astype(np.uint32)))

out = {"prep": os.path.abspath(args.prep), "res": RES, "valid_texels": NV,
       "atlas_texels": RES * RES,
       "valid_pct_of_atlas": round(100.0 * NV / (RES * RES), 4),
       "faces": int(len(f)), "sample": args.sample, "seed": args.seed}
print("[anat] valid %,d of %,d atlas texels (%.2f%%);  %,d faces"
      .replace("%,d", "%s") % (f"{NV:,}", f"{RES*RES:,}",
                               100.0 * NV / (RES * RES), f"{len(f):,}"), flush=True)

# ---- the manifold-edge partition, and which piece is OUTER by signed volume ----
#
# ⚠ WELD FIRST, AND THE FIRST DRAFT OF THIS FILE DID NOT. `prep_uv.glb` is a Blender glTF
# round trip, so it arrives with a vertex split at every UV seam - 46,496 islands' worth.
# Computing `face_adjacency` on that unwelded mesh returns the UV ISLANDS, not the walls:
# measured 50,586 "pieces" with the largest at 28,534 faces, against Gate 0's 3 pieces on the
# welded raw mesh. The signed volumes of open island patches are not a nesting test and the
# outer/inner labels read off them were meaningless (they said 6.63% outer, which is the
# island-size distribution wearing a wall's name). Corrected in place rather than deleted,
# because this is the repo's own law arriving in a new costume: a number that reproduces
# exactly can still be measured against the wrong object. The adjacency is now computed on a
# WELDED COPY; `merge_vertices` remaps vertex indices and leaves the face array's order and
# length untouched, so the labels still index the same faces the raycast attributes to.
mw = m.copy()
mw.merge_vertices(merge_tex=True, merge_norm=True)
if not (len(mw.faces) == len(f)):
    raise AssertionError(
        f"ANDON: welding changed the face array ({len(mw.faces):,} vs {len(f):,}), so face "
        f"labels can no longer be indexed by the raycast's primitive ids")
print(f"[anat] welded for adjacency: {len(v):,} -> {len(mw.vertices):,} verts, "
      f"faces unchanged at {len(f):,}", flush=True)
comp = trimesh.graph.connected_components(mw.face_adjacency, min_len=1,
                                          nodes=np.arange(len(f)))
sizes = np.array([len(c) for c in comp])
order = np.argsort(-sizes)
lab = np.full(len(f), -1, dtype=np.int64)
for k, ci in enumerate(order):
    lab[comp[ci]] = k
n_pieces = len(comp)
print(f"[anat] manifold-edge pieces: {n_pieces}  (sizes "
      f"{', '.join(f'{s:,}' for s in sizes[order][:6])}"
      f"{' ...' if n_pieces > 6 else ''})", flush=True)


def signed_volume(face_idx):
    t = V[f[face_idx]]
    return float(np.einsum('ij,ij->i',
                           t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6.0)


vols = {k: signed_volume(np.where(lab == k)[0]) for k in range(min(n_pieces, 6))}
for k, vv in vols.items():
    print(f"[anat]   piece {k}: {int((lab == k).sum()):,} faces  signed volume {vv:+.6f}"
          f"   {'OUTER (encloses positive volume)' if vv > 0 else 'INNER (inward-facing wall)'}",
          flush=True)
out["pieces"] = {str(k): {"faces": int((lab == k).sum()), "signed_volume": round(v_, 6)}
                 for k, v_ in vols.items()}
OUTER = [k for k, v_ in vols.items() if v_ > 0]
INNER = [k for k, v_ in vols.items() if v_ <= 0]
face_outer = np.isin(lab, OUTER)
print(f"[anat] faces: outer {int(face_outer.sum()):,} ({face_outer.mean()*100:.2f}%)  "
      f"inner {int((~face_outer).sum()):,} ({(~face_outer).mean()*100:.2f}%)", flush=True)
out["face_outer_pct"] = round(float(face_outer.mean() * 100), 4)

# ---- sample valid texels; attribute each to its nearest triangle ----
rng = np.random.default_rng(args.seed)
n = min(args.sample, NV)
idx = rng.choice(NV, size=n, replace=False)
q = o3d.core.Tensor(P[idx].astype(np.float32))
cp = rs.compute_closest_points(q)
prim = cp["primitive_ids"].numpy().astype(np.int64)
dist = np.linalg.norm(cp["points"].numpy().astype(np.float64) - P[idx], axis=1)
tex_outer = face_outer[prim]
print(f"[anat] sampled {n:,} valid texels (seed {args.seed}); "
      f"nearest-triangle attribution -> outer {tex_outer.mean()*100:.2f}%  "
      f"inner {(~tex_outer).mean()*100:.2f}%", flush=True)
out["texel_outer_pct"] = round(float(tex_outer.mean() * 100), 4)


# ---- reachability, re-derived from project_twins' definition ----
def dtc_of(yaw_d, el_d=0.0):
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    return cd / np.linalg.norm(cd)


if not (np.allclose(dtc_of(0.0), [0.0, -1.0, 0.0])):
    raise AssertionError("ANDON: yaw 0 is not project_twins' front")

VIEWS = [float(x) for x in args.views.split(",")]
reach_all = np.zeros(NV, dtype=bool)
for y in VIEWS:
    d = dtc_of(y)
    facing = N @ d
    sel = np.where(facing > args.facing_min)[0]
    if not len(sel):
        continue
    org = (P[sel] + N[sel] * args.noffs + d[None, :] * args.bias).astype(np.float32)
    t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(d.astype(np.float32), org.shape)], axis=1)))["t_hit"].numpy()
    reach_all[sel[~np.isfinite(t)]] = True
print(f"[anat] reachable over {len(VIEWS)} yaws at facing-min {args.facing_min}: "
      f"{int(reach_all.sum()):,}  ({reach_all.mean()*100:.2f}% of valid)", flush=True)
out["reachable"] = int(reach_all.sum())
out["reachable_pct"] = round(float(reach_all.mean() * 100), 4)

if args.ceiling_json and os.path.exists(args.ceiling_json):
    cj = json.load(open(args.ceiling_json, encoding="utf-8"))
    # Select e08_ceiling's block by the FLOORS IT RAN, not by its caption. This
    # line used to read cj["settings"]["uniform 0.45"] — a hardcoded string that
    # is only correct while this tool's --facing-min happens to be 0.45, which is
    # E12 Ruling 6e(i)'s defect wearing a different tool's clothes. E16-6 made
    # e08_ceiling's captions honest, and honest captions MOVE, so the lookup has
    # to be on the property. `settings_index` is absent from ceiling JSONs
    # written before that repair; those are read by their old caption.
    _want = (args.facing_min, args.facing_min)
    _lbl = next((s["label"] for s in cj.get("settings_index", [])
                 if (s["facing_min"], s["head_facing_min"]) == _want), None)
    if _lbl is None:
        _lbl = "uniform %g" % args.facing_min      # pre-E16-6 ceiling JSON
    if not (_lbl in cj["settings"]):
        raise AssertionError(
            f"ANDON: {os.path.basename(args.ceiling_json)} has no block run at floors "
            f"{_want} - blocks present: {sorted(cj['settings'])}. A cross-check against "
            f"a different configuration is not a cross-check.")
    ref = cj["settings"][_lbl][f"N{len(VIEWS)}"]["reachable"]
    if not (int(reach_all.sum()) == int(ref)):
        raise AssertionError(
            f"ANDON: this file's reachability ({int(reach_all.sum()):,}) disagrees with "
            f"e08_ceiling's ({int(ref):,}) on the same bake and the same floors")
    print(f"[anat] EXTERNAL CHECK: reproduces e08_ceiling's N{len(VIEWS)} total exactly "
          f"({int(ref):,})", flush=True)
    out["ceiling_cross_check"] = "exact"

# ---- THE CROSS-TAB: is the unreachable set the inner wall? ----
r_s = reach_all[idx]
tab = {}
print("\n[anat] IS THE UNREACHABLE SET THE INNER WALL?  (sampled texels)")
print("[anat] %-22s %12s %12s %10s" % ("", "reachable", "unreachable", "row %"))
for nm, sel in (("OUTER wall", tex_outer), ("INNER wall", ~tex_outer)):
    a = int((sel & r_s).sum())
    b = int((sel & ~r_s).sum())
    print("[anat] %-22s %12s %12s %9.2f%%"
          % (nm, f"{a:,}", f"{b:,}", 100.0 * (a + b) / n))
    tab[nm] = {"reachable": a, "unreachable": b,
               "reach_rate_pct": round(100.0 * a / max(a + b, 1), 3)}
print("[anat]   outer-wall texels that ARE reachable : %.2f%%" % tab["OUTER wall"]["reach_rate_pct"])
print("[anat]   inner-wall texels that are reachable : %.2f%%" % tab["INNER wall"]["reach_rate_pct"])
unreach = ~r_s
if unreach.sum():
    print("[anat]   of everything UNREACHABLE, %.2f%% is inner wall"
          % (100.0 * float((unreach & ~tex_outer).sum()) / float(unreach.sum())))
    tab["unreachable_is_inner_pct"] = round(
        100.0 * float((unreach & ~tex_outer).sum()) / float(unreach.sum()), 3)
out["cross_tab"] = tab

# ---- the off-surface split: interior vs bake margin ----
if args.px_unit:
    dpx = dist / args.px_unit
    print("\n[anat] OFF-SURFACE, SPLIT BY DISTANCE INTO THE ISLAND  (one px = %.6e)"
          % args.px_unit)
    print("[anat] %-26s %12s %10s %10s" % ("population", "texels", ">1px", ">5px"))
    print("[anat] %-26s %12s %9.4f%% %9.4f%%"
          % ("all valid (sampled)", f"{n:,}", 100.0 * (dpx > 1).mean(),
             100.0 * (dpx > 5).mean()))
    rows = [{"population": "all valid", "texels": int(n),
             "gt1px_pct": round(100.0 * float((dpx > 1).mean()), 4),
             "gt5px_pct": round(100.0 * float((dpx > 5).mean()), 4)}]
    flat_idx = np.where(valid)[0]
    for k in [int(x) for x in args.erode.split(",")]:
        er = cv2.erode(mask2d.astype(np.uint8),
                       np.ones((2 * k + 1, 2 * k + 1), np.uint8), iterations=1) > 0
        keep = er.reshape(-1)[flat_idx[idx]]
        if keep.sum() < 100:
            print("[anat] %-26s %12s   (too few to report)" % (f"eroded {k} texels", f"{int(keep.sum()):,}"))
            continue
        print("[anat] %-26s %12s %9.4f%% %9.4f%%"
              % (f"eroded {k} texels", f"{int(keep.sum()):,}",
                 100.0 * (dpx[keep] > 1).mean(), 100.0 * (dpx[keep] > 5).mean()))
        rows.append({"population": f"eroded {k}", "texels": int(keep.sum()),
                     "gt1px_pct": round(100.0 * float((dpx[keep] > 1).mean()), 4),
                     "gt5px_pct": round(100.0 * float((dpx[keep] > 5).mean()), 4)})
        if k == 2:
            ring = ~keep
            if ring.sum() > 100:
                print("[anat] %-26s %12s %9.4f%% %9.4f%%"
                      % ("the 2-texel RING only", f"{int(ring.sum()):,}",
                         100.0 * (dpx[ring] > 1).mean(), 100.0 * (dpx[ring] > 5).mean()))
                rows.append({"population": "2-texel ring only", "texels": int(ring.sum()),
                             "gt1px_pct": round(100.0 * float((dpx[ring] > 1).mean()), 4),
                             "gt5px_pct": round(100.0 * float((dpx[ring] > 5).mean()), 4)})
    out["offsurface_by_erosion"] = rows

if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(out, open(args.out, "w"), indent=1)
    print("\n[anat] wrote %s" % args.out)
