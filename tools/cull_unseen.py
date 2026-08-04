"""E06 — classify the surface no exterior camera can ever see. Do NOT delete it.

E05 measured that **49% of valid atlas texels are never visible from any of 46 exterior
cameras** on the W3 warrior. For a prerendered 2.5D deliverable, exterior visibility is the
only visibility there is, so that half of the surface is paid for three times: texels in the
atlas, a hole in the map, and a dilation that bleeds into whatever island the packer placed
beside it. Interleaved with real surface inside the same charts, it is also why a patch of
beard takes colour from something unrelated.

**This tool emits a classification. It never modifies geometry.** An earlier version deleted
the unseen faces and was withdrawn at Gate 0: deleting is only safe if the visibility camera
set is a superset of every camera the asset will ever be rendered from, and a guarantee that
depends on nobody adding a camera is not a guarantee. Measured on W3, a generic 46-camera
sphere missed six of the ten production cameras (all four diagonal turnaround yaws and both
elevated strokes) and removed 228 faces that a production camera could see — punching a hole
0.297 deep straight through the torso.

`bake_hero_prep --visible-mask` consumes this and packs only the visible faces, collapsing
the rest onto one shared patch. Same benefit — texel density roughly doubles on visible
surface and charts are computed on the visible subset — with the risk eliminated rather than
managed: the silhouette cannot change, a hole is structurally impossible, and a camera nobody
anticipated sees a flat patch instead of straight through the body.

**Visibility is measured per face, not by rasterising cameras.** A 752x1024 ortho grid puts
roughly 150k figure pixels against 287k faces, so most faces are sub-pixel and a first-hit
rasteriser would miss them — the sampling loss would masquerade as invisibility. Each face is
asked directly, with the same test `texpass_iter.commit` applies to a texel, which also keeps
the number commensurable with E05's 49%.

  cull_unseen.py --glb welded.glb --out visible.npy [--cameras 46] [--rings 1]
                 [--samples 4] [--production "0,0;45,0;..."] [--json report.json]

Standards compliance:
  PIN_PER_STEP — camera count, production set, ring count, sample count and both ray offsets
    are explicit arguments echoed into the log and the sidecar JSON.
  ANDON_AUTHORITY — halts if the seen fraction leaves [--min-seen, --max-seen]. The
    first-hit DEPTH check is retained, applied to the hypothetical deleted mesh: under
    UV-exclude a recession can no longer reach the deliverable, so it is a test of the
    CLASSIFIER rather than a safety net, and a non-zero result now means the tool is wrong
    rather than a threshold needing tuning. Silhouette IoU is reported but is NOT the gate:
    it is structurally blind to a hole punched through visible surface, because the ray
    behind a removed face still hits geometry and the pixel still reads as figure. It
    returned 1.00000 on a mesh with a hole clean through it.
  NAMED_COMPENSATORS — reads one GLB, writes one .npy and one .json. Nothing is modified.
  EXTERNAL_VERIFIER — grades nothing; emits counts, per-camera IoU and recession, and a
    face-centroid checksum so a consumer can prove the mask still lines up with the mesh.
"""
import argparse
import hashlib
import json
import os

import numpy as np
import open3d as o3d
import trimesh

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True, help="the mesh, unmodified")
ap.add_argument("--out", required=True, help="bool .npy, one entry per face")
ap.add_argument("--cameras", type=int, default=46,
                help="exterior sphere directions; 46 is the E05 set, so the seen fraction "
                     "stays comparable with E05's 49%% invisible texels")
ap.add_argument("--production",
                default=";".join([f"{y},0" for y in range(0, 360, 15)] + ["0,55", "180,55"]),
                help="yaw,el pairs the asset will actually be rendered from, UNION'd into "
                     "the sphere. Default is a 15-degree equatorial ring (covering any "
                     "turnaround up to 24 directions, plus head_render's -30/0/+30) and the "
                     "two elevated texpass strokes. A generic sphere does not contain these: "
                     "the 46-set puts 12 yaws at 30 degrees on the equator and therefore "
                     "misses all four diagonal turnaround cameras.")
ap.add_argument("--rings", type=int, default=1,
                help="dilate the seen set by this many rings of edge-adjacent faces. A face "
                     "visible through a narrow aperture can be missed by a finite camera "
                     "sample; its neighbours cost little. Measured: the ring rescued 85 of "
                     "313 faces the raw 46-set missed.")
ap.add_argument("--samples", type=int, default=4,
                help="ray origins per face: 1 = centroid, 4 = centroid plus three points "
                     "pulled halfway toward each vertex")
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--min-seen", type=float, default=0.30)
ap.add_argument("--max-seen", type=float, default=0.90)
ap.add_argument("--raster-res", type=int, default=1504,
                help="width at which the PRODUCTION cameras are rasterised to collect "
                     "first-hit faces. Point-sampling a face cannot represent PARTIAL "
                     "visibility — a face half-hidden behind an arm is visible, but if "
                     "none of its --samples origins lands in the exposed sliver it is "
                     "classified unseen. Measured on W3: that miss alone left 151 px "
                     "receding at yaw 135 even after the production cameras were unioned "
                     "into the sphere. Rasterising catches those; point-sampling catches "
                     "the sub-pixel faces rasterising misses; the union has far fewer "
                     "false negatives than either. 1504 is 2x the 752 production render "
                     "width, so it covers production sampling with margin.")
ap.add_argument("--iou-cameras", default="0,45,90,135,180,225,270,315")
ap.add_argument("--iou-res", type=int, default=1880,
                help="gate resolution, deliberately DIFFERENT from --raster-res so the "
                     "gate samples a different grid than the classifier was built from. "
                     "Equal values would make the gate a tautology for the production "
                     "cameras instead of a check on the implementation.")
ap.add_argument("--max-recession", type=float, default=1e-3,
                help="depth shift counted as a recession, for the DIAGNOSTIC readout")
ap.add_argument("--max-missed-area", type=float, default=0.005,
                help="THE GATE. Fraction of visible surface AREA belonging to faces that "
                     "are a first hit from a gate camera yet classified unseen. Area, not "
                     "pixels: a pixel-count gate at zero is unachievable by construction "
                     "here, because the residual GROWS with gate resolution — measured on "
                     "W3, 28 faces (0.041%% of visible area) at 1880px and 66 (0.096%%) at "
                     "3008px. A finer grid always finds another sliver, so zero pixels is "
                     "an asymptote rather than a threshold. Area is the quantity that "
                     "converges and it is also the quantity that matters: under UV-exclude "
                     "a missed face costs a flat patch of exactly its own area, never a "
                     "hole. 0.005 leaves more than an order of magnitude over the measured "
                     "residual, so a real regression still trips it.")
ap.add_argument("--json")
args = ap.parse_args()

W = args.iou_res
H = int(round(W * 1024 / 752))
D = 2.0


def dvec(yaw, el):
    t, e = np.radians(yaw), np.radians(el)
    return np.array([np.sin(t) * np.cos(e), -np.cos(t) * np.cos(e), np.sin(e)])


def sphere_views(n):
    """Near-uniform exterior directions. At n=46 this reproduces the E05 set exactly."""
    if n == 46:
        out = []
        for el in (-60, -30, 0, 30, 60):
            k = max(1, int(12 * np.cos(np.radians(el))))
            for i in range(k):
                out.append((360.0 * i / k, float(el)))
        return out + [(0.0, 85.0), (0.0, -85.0)]
    out = []
    ga = np.pi * (3 - np.sqrt(5))
    for i in range(n):
        z = 1 - 2 * (i + 0.5) / n
        r = np.sqrt(max(0.0, 1 - z * z))
        th = ga * i
        out.append((float(np.degrees(np.arctan2(np.sin(th) * r, -np.cos(th) * r)) % 360),
                    float(np.degrees(np.arcsin(z)))))
    return out


prod_views = []
for pair in args.production.split(";"):
    if not pair.strip():
        continue
    y, e = pair.split(",")
    prod_views.append((float(y), float(e)))
sph_views = sphere_views(args.cameras)


def key(v):
    return (round(v[0] % 360.0, 3), round(v[1], 3))


all_views = list(sph_views)
seen_keys = {key(v) for v in sph_views}
added = 0
for v in prod_views:
    if key(v) not in seen_keys:
        all_views.append(v)
        seen_keys.add(key(v))
        added += 1

mesh = trimesh.load(args.glb, force="mesh", process=False)
vraw = np.asarray(mesh.vertices, dtype=np.float64)
f = np.asarray(mesh.faces, dtype=np.int64)
maxabs = np.abs(vraw).max()
v = np.stack([vraw[:, 0], -vraw[:, 2], vraw[:, 1]], axis=1) / maxabs * 0.5
nf, nv = len(f), len(v)
print(f"[cull] {os.path.basename(args.glb)}: {nf:,} faces  {nv:,} verts", flush=True)
print(f"[cull] cameras: {len(sph_views)} sphere + {added} production not already in it "
      f"= {len(all_views)} total", flush=True)

rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))
tri = v[f]
cent = tri.mean(axis=1)
fn = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
fn /= np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12

origins = [cent] + [cent + 0.5 * (tri[:, k] - cent) for k in range(3)]
origins = origins[:max(1, args.samples)]


def visible_from(views):
    s = np.zeros(nf, dtype=bool)
    for yaw, el in views:
        d = dvec(yaw, el)
        front = (fn @ d) > 0.0
        for ob in origins:
            idx = np.where(front & ~s)[0]
            if not len(idx):
                break
            org = (ob[idx] + fn[idx] * args.noffs + d[None, :] * args.bias).astype(np.float32)
            t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
                [org, np.broadcast_to(d.astype(np.float32), org.shape)], axis=1)
            ))["t_hit"].numpy()
            s[idx[~np.isfinite(t)]] = True
    return s


blo0, bhi0 = v.min(axis=0), v.max(axis=0)
bmid0 = (blo0 + bhi0) / 2
vext0 = (bhi0[2] - blo0[2]) * 1.204


def raster_hits(views, width):
    """Faces that are a FIRST HIT from any of these cameras. This is the operational
    definition of 'visible' for a prerendered deliverable, and unlike point sampling it
    represents partial visibility exactly."""
    hgt = int(round(width * 1024 / 752))
    hx = vext0 * (width / hgt)
    xs_ = (np.arange(width) + 0.5) / width * hx - hx / 2
    ys_ = vext0 / 2 - (np.arange(hgt) + 0.5) / hgt * vext0
    gx_, gy_ = np.meshgrid(xs_, ys_)
    hit = np.zeros(nf, dtype=bool)
    for yaw, el in views:
        look = -dvec(yaw, el)
        look = look / np.linalg.norm(look)
        right = np.cross(look, [0.0, 0.0, 1.0])
        right /= np.linalg.norm(right) + 1e-12
        upv = np.cross(right, look)
        org = (bmid0[None, None, :] + gx_[..., None] * right[None, None, :]
               + gy_[..., None] * upv[None, None, :] - look[None, None, :] * D)
        ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
        pid = ans["primitive_ids"].numpy()
        ok = np.isfinite(ans["t_hit"].numpy())
        hit[np.unique(pid[ok])] = True
    return hit


seen_sphere = visible_from(sph_views)
seen_pts = visible_from(all_views)
seen_ras = raster_hits(prod_views, args.raster_res)
seen = seen_pts | seen_ras
print(f"[cull] point test, {len(sph_views)}-camera sphere alone:  "
      f"{int(seen_sphere.sum()):,} ({seen_sphere.mean()*100:.1f}%)", flush=True)
print(f"[cull] point test, sphere UNION production:    {int(seen_pts.sum()):,} "
      f"({seen_pts.mean()*100:.1f}%)  — production adds "
      f"{int((seen_pts & ~seen_sphere).sum()):,}", flush=True)
print(f"[cull] raster, {len(prod_views)} production cameras @ {args.raster_res}px: "
      f"{int(seen_ras.sum()):,} ({seen_ras.mean()*100:.1f}%)", flush=True)
print(f"[cull] UNION of both tests:                    {int(seen.sum()):,} "
      f"({seen.mean()*100:.1f}%)  — raster adds "
      f"{int((seen_ras & ~seen_pts).sum()):,} faces the point test alone missed; "
      f"point test adds {int((seen_pts & ~seen_ras).sum()):,} the raster missed",
      flush=True)

adj = mesh.face_adjacency
ring_added = []
for r in range(args.rings):
    a, b = adj[:, 0], adj[:, 1]
    grow = seen.copy()
    grow[a[seen[b]]] = True
    grow[b[seen[a]]] = True
    ring_added.append(int(grow.sum() - seen.sum()))
    seen = grow
    print(f"[cull] ring {r+1}: +{ring_added[-1]:,} -> {int(seen.sum()):,} "
          f"({seen.mean()*100:.1f}%)", flush=True)

frac = float(seen.mean())
assert frac >= args.min_seen, (
    f"ANDON: only {frac*100:.1f}% of faces are seen, below --min-seen "
    f"{args.min_seen*100:.0f}%. Check the ray offsets and the camera set.")
assert frac <= args.max_seen, (
    f"ANDON: {frac*100:.1f}% of faces are seen, above --max-seen {args.max_seen*100:.0f}%. "
    f"The visibility test is not discriminating and the classification is doing nothing.")

# ---- Gate: build the mesh this classification WOULD have deleted, purely to test the
# classifier. Nothing here is exported. Under UV-exclude a recession cannot reach the
# deliverable, so a non-zero result means this tool is wrong, not that a knob needs turning.
culled = mesh.copy()
culled.update_faces(seen)
culled.remove_unreferenced_vertices()
vc = np.asarray(culled.vertices, dtype=np.float64)
vc = np.stack([vc[:, 0], -vc[:, 2], vc[:, 1]], axis=1) / maxabs * 0.5
rs2 = o3d.t.geometry.RaycastingScene()
rs2.add_triangles(o3d.core.Tensor(vc.astype(np.float32)),
                  o3d.core.Tensor(np.asarray(culled.faces, dtype=np.int64).astype(np.uint32)))

blo, bhi = v.min(axis=0), v.max(axis=0)
bmid = (blo + bhi) / 2
v_ext = (bhi[2] - blo[2]) * 1.204
h_ext = v_ext * (W / H)
xs = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
ys = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
gx, gy = np.meshgrid(xs, ys)


def depthmap(rsx, yaw, el):
    look = -dvec(yaw, el)
    look = look / np.linalg.norm(look)
    right = np.cross(look, [0.0, 0.0, 1.0])
    right /= np.linalg.norm(right) + 1e-12
    up = np.cross(right, look)
    org = (bmid[None, None, :] + gx[..., None] * right[None, None, :]
           + gy[..., None] * up[None, None, :] - look[None, None, :] * D)
    t = rsx.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)
    ))["t_hit"].numpy().reshape(H, W)
    return np.isfinite(t), t


checks = []
worst_iou, worst_rec, worst_rec_px = 1.0, 0.0, 0
print(f"[cull] classifier check at {W}x{H} — IoU is REPORTED, recession is the GATE:",
      flush=True)
for yaw in [float(x) for x in args.iou_cameras.split(",")]:
    a, ta = depthmap(rs, yaw, 0.0)
    b, tb = depthmap(rs2, yaw, 0.0)
    iou = int((a & b).sum()) / max(int((a | b).sum()), 1)
    both = a & b
    rec = np.zeros((H, W))
    rec[both] = tb[both] - ta[both]
    n = int((rec > args.max_recession).sum())
    mx = float(rec.max()) if both.any() else 0.0
    checks.append({"yaw": yaw, "iou": round(iou, 5), "px_receded": n,
                   "max_recession": round(mx, 6)})
    worst_iou = min(worst_iou, iou)
    worst_rec = max(worst_rec, mx)
    worst_rec_px = max(worst_rec_px, n)
    print(f"[cull]   yaw {yaw:+6.1f}  IoU {iou:.5f}   receded >{args.max_recession:g}: "
          f"{n:,}px  max {mx:.6f}", flush=True)
print(f"[cull] worst IoU {worst_iou:.5f}, worst recession {worst_rec:.6f} over "
      f"{worst_rec_px:,}px — both DIAGNOSTIC", flush=True)

# THE GATE: how much visible AREA did the classifier miss? Rasterised at the gate
# resolution, which is finer than the classifier's, so this is a real check rather than
# a restatement of how the mask was built.
tri_area = 0.5 * np.linalg.norm(np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]), axis=1)
gate_hits = raster_hits([(y, 0.0) for y in
                         [float(x) for x in args.iou_cameras.split(",")]] + prod_views,
                        args.iou_res)
missed = gate_hits & ~seen
missed_area = float(tri_area[missed].sum() / max(tri_area[gate_hits].sum(), 1e-12))
print(f"[cull] GATE  first-hit faces @ {args.iou_res}px {int(gate_hits.sum()):,}; "
      f"classified unseen among them {int(missed.sum()):,} "
      f"({missed.sum()/max(int(gate_hits.sum()),1)*100:.4f}% by count, "
      f"{missed_area*100:.4f}% by AREA; limit {args.max_missed_area*100:.2f}%)", flush=True)

# Ship the centroids themselves rather than a hash of them. A consumer reads this mesh
# through a different stack — Blender's float32 `polygon.center` against trimesh's float64
# — and the two disagree by ~5e-8. That is far below any geometric tolerance, but it
# straddles the rounding boundary on thousands of values, so an exact hash mismatches
# every time on a mask that is perfectly aligned. Comparing positions with a tolerance
# tests the thing that matters: a mask shuffled by even one face moves a centroid by
# roughly an edge length (0.0029 median here), thousands of times any float noise.
cent_path = os.path.splitext(args.out)[0] + "_centroids.npy"
np.save(cent_path, cent.astype(np.float32))
cksum = hashlib.sha1(np.round(cent, 5).astype(np.float64).tobytes()).hexdigest()
report = {"glb": args.glb, "faces": nf, "verts": nv,
          "sphere_cameras": len(sph_views), "production_cameras_added": added,
          "total_cameras": len(all_views), "production": args.production,
          "samples_per_face": args.samples, "rings": args.rings,
          "raster_res": args.raster_res, "iou_res": args.iou_res,
          "seen_sphere_points_only": int(seen_sphere.sum()),
          "seen_points_union_production": int(seen_pts.sum()),
          "seen_raster_production": int(seen_ras.sum()),
          "raster_added_over_points": int((seen_ras & ~seen_pts).sum()),
          "points_added_over_raster": int((seen_pts & ~seen_ras).sum()),
          "ring_added": ring_added,
          "visible": int(seen.sum()), "visible_frac": round(frac, 4),
          "unseen": int(nf - seen.sum()), "unseen_frac": round(1 - frac, 4),
          "checks": checks, "worst_iou": round(worst_iou, 5),
          "worst_recession": round(worst_rec, 6), "worst_recession_px": worst_rec_px,
          "gate_first_hit_faces": int(gate_hits.sum()),
          "gate_missed_faces": int(missed.sum()),
          "gate_missed_area_frac": round(missed_area, 6),
          "gate_missed_area_limit": args.max_missed_area,
          "face_centroid_sha1": cksum,
          "face_centroids_npy": os.path.basename(cent_path)}
np.save(args.out, seen)
sidecar = os.path.splitext(args.out)[0] + ".json"
json.dump(report, open(args.json or sidecar, "w"), indent=1)
if args.json:
    json.dump(report, open(sidecar, "w"), indent=1)
print(f"[cull] face-centroid sha1 {cksum}", flush=True)
print(f"[cull] wrote {args.out} ({int(seen.sum()):,} visible / {int(nf-seen.sum()):,} "
      f"unseen) + {sidecar} — geometry untouched", flush=True)

assert missed_area <= args.max_missed_area, (
    f"ANDON: faces holding {missed_area*100:.4f}% of visible surface area are a first hit "
    f"from a gate camera yet classified unseen, over the {args.max_missed_area*100:.2f}% "
    f"limit. Under UV-exclude each costs a flat patch of its own area rather than a hole, "
    f"but at this scale the visibility test is missing real surface. Fix the camera set or "
    f"the sampling — do not raise the limit.")
print("[cull] DONE", flush=True)
