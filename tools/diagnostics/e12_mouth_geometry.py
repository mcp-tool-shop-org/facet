"""Is there a TONGUE inside this mesh's mouth, and can any exterior camera see it?

E12 Ruling 11c: the Director's "the tongue is missing" is a claim about a painted artifact,
and paint never restores geometry the mesh does not have (the throat crevice, designated-in
at Ruling 1, is the standing precedent). So the question is answered from the MESH. Gate 0 §6
recorded a tongue visible on candidates 00001 and 00002 and said nothing about 00003 — a
render observation by a previous seat, which is a hypothesis wearing a fact's clothes until
geometry is asked.

THREE INSTRUMENTS, because "present" and "reachable" and "shaped like a tongue" are three
different questions and one number answers none of them:

  SECTION    a mid-sagittal slice through the mouth, plotted in the (y, z) plane. This is the
             decisive one for FORM: a tongue is a raised, tapered body rising off the jaw
             floor, and a slice either shows one or does not. Immune to occlusion, immune to
             shading, immune to what any camera can reach.
  CENSUS     for every triangle whose centroid lies in the cavity box, is it first-hit
             REACHABLE from any of N directions on a sphere — cast outward from the centroid
             along d (with dot(n,d) > 0) and ask whether the ray escapes. Ruling 10f's method
             for the satellite shells, pointed at a region instead of a shell.
  (the render leg is e12_head_render.py with a mouth box; kept out of here because Blender's
   bundled Python has no Pillow and this file runs under the pipeline interpreter.)

WORKS-PERFECTLY, stated before reading: a cavity with a tongue returns a section curve with a
closed or near-closed raised lobe on the floor and a non-zero reachable count; a cavity with a
bare floor returns a monotone floor curve; an absent cavity returns no interior surface at
all. Three different readings, so the instruments have content.

  e12_mouth_geometry.py --glb m.glb --out DIR --box x0,y0,z0,x1,y1,z1
                        [--section-x -0.0121] [--dirs 98] [--sections -0.05,-0.012,0.03]

ANDON_AUTHORITY: raises on a degenerate box or an empty section rather than emitting an
empty plot for a human to misread. NAMED_COMPENSATORS: writes only under --out.
EXTERNAL_VERIFIER: emits a curve, a census and a picture; it adopts nothing and scores
nothing. The Director's eye is the verifier, and the section exists so the eye is looking at
geometry rather than at paint.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--box", required=True, help="x0,y0,z0,x1,y1,z1 in the Blender-import frame")
ap.add_argument("--sections", required=True,
                help="comma-separated x values to slice at, in the Blender-import frame")
ap.add_argument("--dirs", type=int, default=98, help="sphere directions for the census")
ap.add_argument("--eps", type=float, default=1e-4, help="ray start offset along the normal")
ap.add_argument("--plot-px", type=int, default=1400)
args = ap.parse_args()

os.makedirs(args.out, exist_ok=True)
b = [float(v) for v in args.box.split(",")]
if not (len(b) == 6):
    raise AssertionError("ANDON: --box wants x0,y0,z0,x1,y1,z1")
lo, hi = np.array(b[:3]), np.array(b[3:])
if not ((hi > lo).all()):
    raise AssertionError("ANDON: degenerate cavity box %s" % (b,))

# --- geometry, in the frame head_00003.json speaks -----------------------------------
# The Blender glTF import remap (x, -z, y), which is also the remap silhouette_masks and
# project_twins apply. head_00003.json's boxes are in THIS frame (its mesh_bbox_blender
# reproduces here exactly), so no normalisation is applied and none is needed.
m = trimesh.load(args.glb, force="mesh", process=False)
v0 = np.asarray(m.vertices, dtype=np.float64)
V = np.stack([v0[:, 0], -v0[:, 2], v0[:, 1]], axis=1)
F = np.asarray(m.faces, dtype=np.int64)
mesh = trimesh.Trimesh(vertices=V, faces=F, process=False)
print("[mouth] mesh %d verts %d tris  bbox lo %s hi %s"
      % (len(V), len(F), np.round(V.min(0), 5).tolist(), np.round(V.max(0), 5).tolist()),
      flush=True)

rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(V.astype(np.float32)), o3d.core.Tensor(F.astype(np.uint32)))

# --- CENSUS: what surface is in the cavity, and what of it is reachable ---------------
cent = V[F].mean(axis=1)
inbox = np.all((cent >= lo) & (cent <= hi), axis=1)
n_in = int(inbox.sum())
print("[mouth] triangles with centroid inside the cavity box: %d (%.4f%% of mesh)"
      % (n_in, 100.0 * n_in / len(F)), flush=True)
if not (n_in > 0):
    raise AssertionError(
        "ANDON: the cavity box contains no triangle centroids. The box is in the "
        "wrong frame or the wrong place; nothing was measured.")

nrm = mesh.face_normals[inbox]
cin = cent[inbox]
# a Fibonacci sphere -- deterministic, no RNG, and it does not privilege the pole axes the
# way a 26-direction cube census does
k = np.arange(args.dirs) + 0.5
phi = np.arccos(1.0 - 2.0 * k / args.dirs)
gold = np.pi * (1.0 + 5.0 ** 0.5)
D = np.stack([np.cos(gold * k) * np.sin(phi), np.sin(gold * k) * np.sin(phi),
              np.cos(phi)], axis=1)

reach = np.zeros(n_in, dtype=bool)
best_dir = np.full(n_in, -1, dtype=np.int64)
for di, d in enumerate(D):
    facing = nrm @ d > 0.0                     # only a face pointing at the camera can be seen
    if not facing.any():
        continue
    idx = np.nonzero(facing & ~reach)[0]
    if not len(idx):
        continue
    o = cin[idx] + nrm[idx] * args.eps
    rays = np.concatenate([o, np.broadcast_to(d, o.shape)], axis=-1).astype(np.float32)
    t = rs.cast_rays(o3d.core.Tensor(rays))["t_hit"].numpy()
    esc = ~np.isfinite(t)                      # the ray leaves the mesh -> the face is exposed
    reach[idx[esc]] = True
    best_dir[idx[esc]] = di

n_reach = int(reach.sum())
print("[mouth] reachable from at least one of %d directions: %d / %d  (%.2f%%)"
      % (args.dirs, n_reach, n_in, 100.0 * n_reach / n_in), flush=True)

# how much of the cavity's AREA is reachable -- a face count over-weights small triangles
area = mesh.area_faces[inbox]
print("[mouth] by AREA: %.6f of %.6f reachable  (%.2f%%)"
      % (area[reach].sum(), area.sum(), 100.0 * area[reach].sum() / max(area.sum(), 1e-12)),
      flush=True)

# --- SECTIONS: the decisive instrument for FORM ---------------------------------------
XS = [float(x) for x in args.sections.split(",")]
curves = {}
for x in XS:
    sec = mesh.section(plane_origin=[x, 0, 0], plane_normal=[1, 0, 0])
    if not (sec is not None):
        raise AssertionError("ANDON: section at x=%.5f returned nothing" % x)
    segs = []
    for ent in sec.entities:
        pts = sec.vertices[ent.points]
        segs.append(pts[:, 1:3])               # (y, z)
    curves[x] = segs
    n_pts = sum(len(s) for s in segs)
    inb = sum(int(np.all((s >= lo[1:3]) & (s <= hi[1:3]), axis=1).sum()) for s in segs)
    print("[mouth] section x=%+.5f: %d polylines, %d points, %d inside the cavity box"
          % (x, len(segs), n_pts, inb), flush=True)

# plot each section over the cavity box, y right / z up, one panel per x
PAD = 0.02
y0, y1 = lo[1] - PAD, hi[1] + PAD
z0, z1 = lo[2] - PAD, hi[2] + PAD
W = args.plot_px
H = int(round(W * (z1 - z0) / (y1 - y0)))
hdr = 26
sheet = Image.new("RGB", (W, (H + hdr) * len(XS)), (16, 16, 18))
dr = ImageDraw.Draw(sheet)


def px(p, oy):
    return ((p[0] - y0) / (y1 - y0) * W, oy + H - (p[1] - z0) / (z1 - z0) * H)


for i, x in enumerate(XS):
    oy = i * (H + hdr) + hdr
    dr.text((6, i * (H + hdr) + 5),
            "mid-sagittal section at x = %+.5f   (y right, z up; cavity box in grey)" % x,
            fill=(255, 210, 90))
    bx0, by0 = px((lo[1], hi[2]), oy)
    bx1, by1 = px((hi[1], lo[2]), oy)
    dr.rectangle([bx0, by0, bx1, by1], outline=(70, 70, 80))
    for s in curves[x]:
        pts = [px(p, oy) for p in s]
        if len(pts) > 1:
            dr.line(pts, fill=(120, 220, 255), width=2)
p = os.path.join(args.out, "MOUTH_SECTIONS.png")
sheet.save(p)
print("[mouth] wrote %s" % p, flush=True)

json.dump({"glb": os.path.abspath(args.glb), "box": b, "sections_x": XS, "dirs": args.dirs,
           "tris_in_box": n_in, "tris_reachable": n_reach,
           "area_in_box": float(area.sum()), "area_reachable": float(area[reach].sum()),
           "reach_frac_by_count": round(float(n_reach) / n_in, 6),
           "reach_frac_by_area": round(float(area[reach].sum() / max(area.sum(), 1e-12)), 6)},
          open(os.path.join(args.out, "mouth_geometry.json"), "w"), indent=1)
print("[mouth] wrote %s" % os.path.join(args.out, "mouth_geometry.json"))
