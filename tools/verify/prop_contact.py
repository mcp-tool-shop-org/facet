"""Contact gate for a held prop. A NUMBER, not an eye.

"Is the prop touching the hand" is a distance between two surfaces. Reading it off a render
is what produced four wrong placements in a row on the first subject: a render shows two
silhouettes from ONE direction, and two surfaces can share a silhouette edge with
centimetres between them. The fourth placement, accepted by eye, measured 1.29 mm of air
with a contact patch of 97 points out of 624,510 - a nine-millimetre kiss on one knuckle.

Reports, in the composite's own units (figure height = 1.0):

  * minimum point-to-SURFACE distance, prop -> figure
  * the contact patch: prop surface within --tol of the figure, and figure surface within
    --tol of the prop. A grip is two-sided; one touching vertex is not a grip.

ANDON when the minimum exceeds --tol, or the contact AREA is under --min-area. Both are stated on
the command line and are not derived from the result being judged.

THE AREA IS THE POINT, NOT THE MINIMUM. A minimum of zero says the surfaces meet somewhere.
Do NOT tune --min-area by maximising it: contact grows monotonically as the prop is driven
into the arm (97 -> 6,198 points over a 64 mm sweep on the first subject), so a placement
chosen to maximise contact impales the figure. Set the floor from what a grip needs; read the
minimum beside it.

THE FLOOR IS CALIBRATED, NOT ASSERTED. Measured on the first subject by sliding the same
shield back along the arm, contact tolerance 2 mm, 200k samples:

    fist kiss (as shipped)        0.000144 units^2      4.7 sq cm at 1.8 m
    sunk into the fist            0.002482             80.4
    against the forearm           0.011981            388.2
    at the torso                  0.025939            840.4

The default --min-area 0.0005 (16 sq cm) sits in an 80x gap between a kiss and a carry,
which is what makes it a usable line rather than a taste. The yes-population was measured
before the floor was trusted, per this repo's rule about calibrating a rule against what
the instrument returns when the answer is definitely yes and definitely no.

AND WATCH THE SAMPLE COUNT NEAR ZERO. That 0.000144 rests on about 46 of 200,000 samples,
so it carries roughly 15% relative noise - the same asset read 0.000097 on a run that also
counted vertices. Far from the floor this does not matter; a number within a factor of two
of --min-area should be re-read at a higher --samples. The tool prints the backing count
for exactly this reason.

AND THE FLOOR IS AN AREA, NOT A COUNT. A count is a fraction of however many samples the
prop happened to get, so the same physical contact scores far higher on a small prop than a
large one and the floor stops meaning one thing across a prop library. T100 found this the
honest way: it could not construct a point-touch that a count would refuse.

TESSELLATION INDEPENDENCE IS LOAD-BEARING, and T100 caught its absence on the first run. An
earlier core chose candidate points by nearest VERTEX. On a dense reconstruction that is
harmless; on a coarse prop it is wrong, because the closest point of a surface is usually not
a vertex - an eight-vertex slab sunk 2 mm into a box reported 201 mm. The route will carry
props from several sources and cannot assume anyone's vertex spacing, so this samples the
prop's surface BY AREA as well as taking its vertices, and every candidate gets an exact
point-to-triangle distance.

WHAT THIS REFUSES TO BE. It does not look at a render. The screen-space form of this check
was written first and is deliberately not the gate: it reports "overlapping" on all eight
facings of the asset this tool fails, because the prop overlaps the TORSO. That is a proxy
for the question, and this repo has paid for proxies.

  python prop_contact.py --glb <composite.glb> [--body body] [--prop shield]
                         [--tol 0.002] [--min-area 0.0005] [--samples 200000]
"""
import argparse
import json
import sys

import numpy as np
import open3d as o3d
import trimesh

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--body", default="body", help="node name of the figure")
ap.add_argument("--prop", default="shield", help="node name of the held prop")
ap.add_argument("--tol", type=float, default=0.002,
                help="contact tolerance in figure-height units. 0.002 = 2 mm on a 1.0 "
                     "figure, about 3.6 mm on a 1.8 m man. Stated, not derived from the "
                     "result being judged.")
ap.add_argument("--min-area", type=float, default=0.0005,
                help="minimum CONTACT AREA, in figure-height units squared, for this to "
                     "count as a grip rather than a touch. 0.0005 is about 16 sq cm on a "
                     "1.8 m figure - a palm and some fingers. AREA, NOT A POINT COUNT: a "
                     "count is a fraction of however many samples the prop got, so a small "
                     "prop scores high on the same physical contact and the floor stops "
                     "meaning one thing across a prop library. T100 found this by failing "
                     "to build a point-touch it could not construct under a count. Not "
                     "derived from the result being judged.")
ap.add_argument("--samples", type=int, default=200000,
                help="area-weighted surface samples taken IN ADDITION to each mesh's "
                     "vertices, so the answer does not depend on how finely either mesh "
                     "happens to be tessellated")
ap.add_argument("--json-out", default=None)
args = ap.parse_args()

scene = trimesh.load(args.glb, process=False)
if not hasattr(scene, "graph"):
    raise SystemExit("ANDON: %s is a single mesh; this gate needs the prop and the figure "
                     "as separate nodes" % args.glb)
names = [n for n in scene.graph.nodes if n != "world"]
for want in (args.body, args.prop):
    if want not in names:
        raise SystemExit("ANDON: no node %r in %s (have %r)" % (want, args.glb, names))


def node_mesh(name):
    T, geom = scene.graph[name]
    m = scene.geometry[geom].copy()
    m.apply_transform(T)
    return m


body = node_mesh(args.body)
prop = node_mesh(args.prop)
print("figure %7d verts %7d faces  bbox %s"
      % (len(body.vertices), len(body.faces), np.round(body.bounds, 4).tolist()))
print("prop   %7d verts %7d faces  bbox %s"
      % (len(prop.vertices), len(prop.faces), np.round(prop.bounds, 4).tolist()))


def scene_of(mesh):
    rs = o3d.t.geometry.RaycastingScene()
    rs.add_triangles(o3d.t.geometry.TriangleMesh.from_legacy(
        o3d.geometry.TriangleMesh(o3d.utility.Vector3dVector(mesh.vertices),
                                  o3d.utility.Vector3iVector(mesh.faces))))
    return rs


def distances(rs, pts):
    t = o3d.core.Tensor(np.ascontiguousarray(pts, dtype=np.float32),
                        dtype=o3d.core.Dtype.Float32)
    return rs.compute_distance(t).numpy().astype(np.float64)


def candidates(mesh, n):
    """Vertices plus area-weighted surface samples: density-independent by construction."""
    pts = [np.asarray(mesh.vertices, dtype=np.float64)]
    if n > 0 and len(mesh.faces):
        pts.append(np.asarray(trimesh.sample.sample_surface(mesh, n)[0], dtype=np.float64))
    return np.vstack(pts)


q_prop = candidates(prop, args.samples)
d_prop = distances(scene_of(body), q_prop)
q_body = candidates(body, args.samples)
d_body = distances(scene_of(prop), q_body)

i = int(np.argmin(d_prop))
patch = int((d_prop <= args.tol).sum())
body_patch = int((d_body <= args.tol).sum())
# area-weighted samples make the in-contact FRACTION an unbiased estimate of the
# in-contact fraction of surface AREA; vertices are excluded from that estimate
# because vertex density is not area density.
nv = len(prop.vertices)
frac = float((d_prop[nv:] <= args.tol).mean()) if len(d_prop) > nv else 0.0
contact_area = frac * float(prop.area)
nvb = len(body.vertices)
frac_b = float((d_body[nvb:] <= args.tol).mean()) if len(d_body) > nvb else 0.0
body_area = frac_b * float(body.area)

print("\nexact point-to-surface over %d prop candidates (%d verts + %d area samples):"
      % (len(q_prop), len(prop.vertices), len(q_prop) - len(prop.vertices)))
print("  MIN %.5f   (%.2f mm on a 1.8 m figure)   at %s"
      % (d_prop.min(), d_prop.min() * 1800, np.round(q_prop[i], 4).tolist()))
print("  prop candidates within tol %.5f : %d of %d  (%.4f%%)"
      % (args.tol, patch, len(q_prop), 100.0 * patch / len(q_prop)))
print("  figure candidates within tol     : %d of %d" % (body_patch, len(q_body)))
if patch:
    pc = q_prop[d_prop <= args.tol]
    print("  contact patch extent %s" % np.round(pc.max(0) - pc.min(0), 4).tolist())
n_hit = int((d_prop[nv:] <= args.tol).sum())
per_sample = float(prop.area) / max(1, len(d_prop) - nv)
print("  CONTACT AREA  prop side %.6f   figure side %.6f   (units^2; prop total %.5f)"
      % (contact_area, body_area, prop.area))
print("                backed by %d of %d area samples, %.3e units^2 each"
      % (n_hit, len(d_prop) - nv, per_sample))
if n_hit and n_hit < 100:
    print("                ^ NOTE: an estimate resting on %d samples carries about "
          "%.0f%% relative noise (1/sqrt n). Raise --samples before reading a verdict "
          "off a number this close to zero." % (n_hit, 100.0 / (n_hit ** 0.5)))

result = {
    "glb": args.glb, "tol": args.tol, "min_area_required": args.min_area,
    "contact_area_prop_side": contact_area,
    "contact_area_figure_side": body_area,
    "prop_surface_area": float(prop.area),
    "min_surface_distance": float(d_prop.min()),
    "min_mm_at_1800": float(d_prop.min() * 1800),
    "prop_candidates": int(len(q_prop)),
    "prop_points_in_contact": patch,
    "area_samples_in_contact": n_hit,
    "units2_per_sample": per_sample,
    "body_points_in_contact": body_patch,
}
if args.json_out:
    with open(args.json_out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

fail = []
if d_prop.min() > args.tol:
    fail.append("minimum surface distance %.5f exceeds tol %.5f - there is AIR between the "
                "prop and the figure" % (d_prop.min(), args.tol))
if contact_area < args.min_area:
    fail.append("contact area %.6f < --min-area %.6f units^2 - the prop touches but is "
                "not gripped" % (contact_area, args.min_area))
print()
if fail:
    print("ANDON: " + "; ".join(fail))
    sys.exit(2)
print("CONTACT: min %.5f within tol %.5f, contact area %.6f units^2"
      % (d_prop.min(), args.tol, contact_area))
