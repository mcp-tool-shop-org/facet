"""E06 — delete the surface no exterior camera can ever see.

E05 measured that **49% of valid atlas texels are never visible from any of 46 exterior
cameras** on the W3 warrior. For a prerendered 2.5D deliverable, exterior visibility is
the only visibility there is, so that half of the surface is paid for three times: texels
in the atlas, a hole in the map, and a dilation that bleeds into whatever island the
packer placed beside it. Interleaved with real surface inside the same charts, it is also
why a patch of beard takes colour from something unrelated.

This runs on the WELDED, DECIMATED mesh BEFORE any UV work, so the unwrapper sees only
surface that can be painted.

**Visibility is measured per face, not by rasterising cameras.** A 752x1024 ortho grid
puts roughly 150k figure pixels against 287k faces, so most faces are sub-pixel and would
be missed by a first-hit rasteriser — the sampling loss would masquerade as invisibility
and the cull would eat real surface. Instead each face is asked directly, using the SAME
test `texpass_iter.commit` applies to a texel: offset along the normal, offset toward the
camera, cast, and see whether the ray escapes. That also keeps this number commensurable
with E05's 49%, which was measured that way per texel.

  cull_unseen.py --glb welded.glb --out culled.glb [--cameras 46] [--rings 1]
                 [--samples 4] [--iou-cameras 0,45,90,135,180,225,270,315]

Standards compliance:
  PIN_PER_STEP — camera count, ring count, sample count and the ray offsets are explicit
    arguments echoed into the log and the sidecar JSON.
  ANDON_AUTHORITY — halts if the seen fraction lands above --max-seen (the visibility test
    is not discriminating and the cull is doing nothing) or below --min-seen (it is eating
    real surface), and halts if the silhouette from any production camera moves by more
    than --max-iou-drop. That last one is the load-bearing check: culling must be invisible
    from outside BY DEFINITION, so silhouette IoU is a direct test of whether the operation
    did what it claims rather than a proxy for it.
  NAMED_COMPENSATORS — reads one GLB, writes another. The input is never modified. Undo is
    deleting the output and pointing the pipeline back at the input.
  EXTERNAL_VERIFIER — grades nothing; emits counts, IoU per camera and a sidecar JSON.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True, help="welded, decimated, PRE-UV-work mesh")
ap.add_argument("--out", required=True)
ap.add_argument("--cameras", type=int, default=46,
                help="exterior directions; 46 is the E05 set, so the seen fraction here "
                     "is directly comparable with E05's 49%% invisible texels")
ap.add_argument("--rings", type=int, default=1,
                help="dilate the seen set by this many rings of edge-adjacent faces "
                     "before deleting. A face visible only through a narrow aperture can "
                     "be missed by a finite camera sample; its neighbours cost little.")
ap.add_argument("--samples", type=int, default=4,
                help="ray origins per face: 1 = centroid only, 4 = centroid plus three "
                     "points pulled halfway toward each vertex (protects large faces "
                     "whose centroid happens to be occluded)")
ap.add_argument("--noffs", type=float, default=1.5e-3, help="offset along the normal")
ap.add_argument("--bias", type=float, default=3e-3, help="offset toward the camera")
ap.add_argument("--min-seen", type=float, default=0.30)
ap.add_argument("--max-seen", type=float, default=0.90)
ap.add_argument("--iou-cameras", default="0,45,90,135,180,225,270,315")
ap.add_argument("--iou-el", default="0,0,0,0,0,0,0,0")
ap.add_argument("--max-iou-drop", type=float, default=0.01)
ap.add_argument("--iou-res", type=int, default=1504,
                help="silhouette raster width; 2x the production 752 so a one-pixel "
                     "rounding difference cannot spend the whole IoU budget")
ap.add_argument("--json")
args = ap.parse_args()

W = args.iou_res
H = int(round(W * 1024 / 752))
D = 2.0


def load_std(path):
    m = trimesh.load(path, force="mesh", process=False)
    v = np.asarray(m.vertices, dtype=np.float64)
    f = np.asarray(m.faces, dtype=np.int64)
    v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
    return m, v, f


def scene(v, f):
    rs = o3d.t.geometry.RaycastingScene()
    rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                     o3d.core.Tensor(f.astype(np.uint32)))
    return rs


def sphere_dirs(n):
    """Near-uniform exterior directions. At n=46 this reproduces the E05 set exactly."""
    if n == 46:
        out = []
        for el in (-60, -30, 0, 30, 60):
            k = max(1, int(12 * np.cos(np.radians(el))))
            for i in range(k):
                out.append((360 * i / k, el))
        out += [(0, 85), (0, -85)]
    else:
        out = []
        ga = np.pi * (3 - np.sqrt(5))
        for i in range(n):
            z = 1 - 2 * (i + 0.5) / n
            r = np.sqrt(max(0.0, 1 - z * z))
            th = ga * i
            out.append((np.degrees(np.arctan2(np.sin(th) * r, -np.cos(th) * r)) % 360,
                        np.degrees(np.arcsin(z))))
    dirs = []
    for yaw, el in out:
        t, e = np.radians(yaw), np.radians(el)
        dirs.append(np.array([np.sin(t) * np.cos(e), -np.cos(t) * np.cos(e), np.sin(e)]))
    return out, dirs


mesh, v, f = load_std(args.glb)
nf, nv = len(f), len(v)
has_uv = getattr(mesh.visual, "uv", None) is not None
def shells(msh, n):
    return len(trimesh.graph.connected_components(msh.face_adjacency,
                                                  nodes=np.arange(n)))


comps_in = shells(mesh, nf)
print(f"[cull] in  {nf:,} faces  {nv:,} verts  shells {comps_in}  uv {has_uv}", flush=True)

rs = scene(v, f)
tri = v[f]
cent = tri.mean(axis=1)
fn = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
fn /= np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12

if args.samples <= 1:
    origins_base = [cent]
else:
    origins_base = [cent] + [cent + 0.5 * (tri[:, k] - cent) for k in range(3)]

views, dirs = sphere_dirs(args.cameras)
seen = np.zeros(nf, dtype=bool)
for dtc in dirs:
    front = (fn @ dtc) > 0.0
    for ob in origins_base:
        idx = np.where(front & ~seen)[0]
        if not len(idx):
            break
        org = (ob[idx] + fn[idx] * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
        t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [org, np.broadcast_to(dtc.astype(np.float32), org.shape)], axis=1)
        ))["t_hit"].numpy()
        seen[idx[~np.isfinite(t)]] = True
raw_seen = int(seen.sum())
print(f"[cull] seen by {len(dirs)} exterior cameras "
      f"({args.samples} sample(s)/face): {raw_seen:,}/{nf:,} = {raw_seen/nf*100:.1f}%",
      flush=True)

# ---- ring dilation over edge adjacency
adj = mesh.face_adjacency
ring_added = []
for r in range(args.rings):
    a, b = adj[:, 0], adj[:, 1]
    grow = seen.copy()
    grow[a[seen[b]]] = True
    grow[b[seen[a]]] = True
    added = int(grow.sum() - seen.sum())
    ring_added.append(added)
    seen = grow
    print(f"[cull] ring {r+1}: +{added:,} faces -> {int(seen.sum()):,} "
          f"({seen.mean()*100:.1f}%)", flush=True)

frac = float(seen.mean())
assert frac >= args.min_seen, (
    f"ANDON: only {frac*100:.1f}% of faces are seen — below --min-seen "
    f"{args.min_seen*100:.0f}%. The cull would eat real surface; check the ray offsets "
    f"and the camera set before trusting this.")
assert frac <= args.max_seen, (
    f"ANDON: {frac*100:.1f}% of faces are seen — above --max-seen {args.max_seen*100:.0f}%. "
    f"The visibility test is not discriminating and the cull is doing nothing.")

# ---- delete, drop unreferenced verts. UVs are per-vertex and trimesh carries them.
culled = mesh.copy()
culled.update_faces(seen)
culled.remove_unreferenced_vertices()
nf2, nv2 = len(culled.faces), len(culled.vertices)
comps_out = shells(culled, nf2)
uv_out = getattr(culled.visual, "uv", None)
print(f"[cull] out {nf2:,} faces  {nv2:,} verts  shells {comps_out}  "
      f"uv {uv_out is not None}"
      f"{'' if uv_out is None else f' ({np.asarray(uv_out).shape[0]:,} coords)'}",
      flush=True)
assert uv_out is not None and len(uv_out) == nv2, \
    "ANDON: the cull lost or desynchronised the native UV layer"

# The input is already welded, and deleting faces cannot create a duplicate vertex, so
# a merge here is a no-op by construction. Report it rather than performing it blind.
dup = nv2 - len(np.unique(np.round(np.asarray(culled.vertices), 9), axis=0))
print(f"[cull] duplicate-position verts after cull: {dup:,} "
      f"(input was welded; a re-weld is a no-op unless this is non-zero)", flush=True)

# ---- silhouette IoU, production cameras, framing taken from the UNCUT mesh for BOTH
blo, bhi = v.min(axis=0), v.max(axis=0)
bmid = (blo + bhi) / 2
v_ext = (bhi[2] - blo[2]) * 1.204
h_ext = v_ext * (W / H)
vc = np.asarray(culled.vertices, dtype=np.float64)
vc = np.stack([vc[:, 0], -vc[:, 2], vc[:, 1]], axis=1) / np.abs(np.asarray(
    mesh.vertices)).max() * 0.5           # SAME scale divisor as the uncut mesh
rs2 = scene(vc, np.asarray(culled.faces, dtype=np.int64))

yaws = [float(x) for x in args.iou_cameras.split(",")]
els = [float(x) for x in args.iou_el.split(",")]
if len(els) == 1:
    els = els * len(yaws)
xs = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
ys = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
gx, gy = np.meshgrid(xs, ys)


def silhouette(rsx, yaw, el):
    t, e = np.radians(yaw), np.radians(el)
    cd = np.array([np.sin(t) * np.cos(e), -np.cos(t) * np.cos(e), np.sin(e)])
    look = -cd / np.linalg.norm(cd)
    right = np.cross(look, [0.0, 0.0, 1.0])
    right /= np.linalg.norm(right) + 1e-12
    up = np.cross(right, look)
    org = (bmid[None, None, :] + gx[..., None] * right[None, None, :]
           + gy[..., None] * up[None, None, :] - look[None, None, :] * D)
    ans = rsx.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
    return np.isfinite(ans["t_hit"].numpy().reshape(H, W))


ious = []
worst = 1.0
print(f"[cull] silhouette IoU, uncut vs culled, {W}x{H}, framing from the uncut mesh:",
      flush=True)
for yaw, el in zip(yaws, els):
    a = silhouette(rs, yaw, el)
    b = silhouette(rs2, yaw, el)
    inter = int((a & b).sum())
    union = int((a | b).sum())
    iou = inter / max(union, 1)
    lost = int((a & ~b).sum())
    gained = int((b & ~a).sum())
    ious.append({"yaw": yaw, "el": el, "iou": round(iou, 5),
                 "px_uncut": int(a.sum()), "px_culled": int(b.sum()),
                 "px_lost": lost, "px_gained": gained})
    worst = min(worst, iou)
    print(f"[cull]   yaw {yaw:+6.1f} el {el:+5.1f}  IoU {iou:.5f}  "
          f"uncut {int(a.sum()):,}px  culled {int(b.sum()):,}px  "
          f"lost {lost:,}  gained {gained:,}", flush=True)

print(f"[cull] worst IoU {worst:.5f}  (halt threshold {1-args.max_iou_drop:.5f})",
      flush=True)
report = {"glb_in": args.glb, "glb_out": args.out, "cameras": len(dirs),
          "samples_per_face": args.samples, "rings": args.rings,
          "faces_in": nf, "verts_in": nv, "shells_in": comps_in,
          "seen_raw": raw_seen, "seen_raw_frac": round(raw_seen / nf, 4),
          "ring_added": ring_added, "seen_final": int(seen.sum()),
          "seen_final_frac": round(frac, 4),
          "faces_out": nf2, "verts_out": nv2, "shells_out": comps_out,
          "faces_removed": nf - nf2, "removed_frac": round((nf - nf2) / nf, 4),
          "duplicate_pos_verts_after": int(dup),
          "silhouette_iou": ious, "worst_iou": round(worst, 5)}
if args.json:
    json.dump(report, open(args.json, "w"), indent=1)
    print(f"[cull] wrote {args.json}", flush=True)

assert worst >= 1.0 - args.max_iou_drop, (
    f"ANDON: silhouette IoU fell to {worst:.5f}, more than {args.max_iou_drop*100:.0f}% "
    f"below 1.0. Culling must be invisible from outside by definition, so this means the "
    f"cull removed surface that shows. The mesh was NOT written.")

culled.export(args.out)
print(f"[cull] wrote {args.out} ({os.path.getsize(args.out)//1024} KB) — DONE", flush=True)
