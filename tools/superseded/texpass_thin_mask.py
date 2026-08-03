"""SUPERSEDED — surface-normal thickness probe. It measures the TESSELLATION.

Kept because the failure is the lesson and because it is cheap to re-derive this
idea and expensive to re-falsify it. Written and falsified in the same session
(E02, 2026-08-04). The working replacement is `--thin-extent` in
`tools/texpass_iter.py`, which fires the CAMERA's rays from the front plane and
again from the back plane and takes the difference — no surface normal and no
interior test, so neither failure below can reach it.

**Why it fails, measured on W3 (`facet_E01/tex_W3/prepV2`):**

1. *The probe resolves the triangle spacing, not the body.* Fired from just below
   the surface along -N, the ray hits a NEIGHBOURING triangle rather than the far
   wall: median reported thickness **0.00204** against a median mesh edge length of
   **0.00290**. The distribution is far too tight to be anatomy — p5 0.00179, p50
   0.00204, p75 0.00238 — and the ANDON below fires correctly, calling 95.24% of
   the surface "thin" at a 0.02 threshold. Pushing the ray start to eps 3e-3 does
   recover real body depth (p50 0.0444, p90 0.159), but that start depth is
   *thicker than a blade*, so the probe stops resolving the only thing it exists to
   find. Corroborating: only **37% of outward rays escape**, where a figure should
   be near 100% outside arm-over-torso occlusion — the surface is re-entrant at the
   triangle scale.

2. *There is no interior to test.* The obvious repair is a containment predicate
   instead of a first-hit ray. It cannot work here: `prep_uv.glb` carries **293,099
   verts for 287,170 faces** because the glTF export splits a vertex at every UV
   seam, so every island boundary is a topological crack and ray-parity leaks
   through it. `compute_signed_distance` at the figure's own bounding-box centre —
   the middle of a standing warrior's chest — returns **+0.0019**, i.e. *outside*.
   Occupancy marching inherits the same defect. No volumetric predicate is
   available on this representation, at any threshold.

Both faults are properties of the asset, not of the threshold, which is why this
file is superseded rather than retuned.

---

Original docstring follows.

TEXTURE-SPACE PASS — derive the diffusion-exclusion mask from GEOMETRY.

POLICY (unchanged): thin hard-surface props take projected/dilated colour, never
invented content. A greatsword blade is a few pixels wide in the emitted view; a
diffusion model handed that as a hole invents a corroded wavy edge, because a
straight steel blade is not what the denoiser wants there.

The FIRST implementation of this policy was a hardcoded pixel rectangle in
texpass_loop.ps1 (`m[80:580, 385:470] = 0` on the yaw-270 job). That is
character-specific, camera-specific, and silently wrong on the next mesh. This tool
replaces it with the property the policy is actually about: LOCAL SURFACE THICKNESS.

Method — one raycast per valid texel:
  origin = P - N*eps   (just inside the surface)
  dir    = -N          (straight through)
  thickness = t_hit + eps
A plate has two nearly-parallel faces a blade-width apart, so the ray exits almost
immediately. A torso, limb or skull exits at the body diameter. Rays that never
exit (open boundary, non-manifold) report inf and are NOT thin.

Units are the std frame the whole texture stage uses: mesh scaled so max|coord| =
0.5, i.e. a standing figure is ~1.0 tall. So --thin 0.02 means "under 2% of figure
height thick" — about 3.5 cm on a 1.8 m character.

  texpass_thin_mask.py --prep DIR --out thin.npy [--thin 0.02] [--preview DIR]
                       [--preview-yaws 270,90,0]

Emits thin.npy (RES x RES bool, True = excluded from diffusion), a texel-space
preview PNG, a printed thickness histogram, and optionally view-space previews at
the emit camera convention so the exclusion can be LOOKED AT before it is used.

Standards compliance: PIN_PER_STEP — the threshold is an explicit argument recorded
in the report, not a literal buried in a loop script. ANDON_AUTHORITY — halts if the
mask covers an implausible fraction of the surface, because a threshold that
excludes the whole character is a broken derivation rather than a strict policy.
EXTERNAL_VERIFIER — this tool measures and does not grade; the view-space preview
exists so a human checks where the exclusion actually landed.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
W, H = 752, 1024
D = 2.0

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--thin", type=float, default=0.02,
                help="thickness below this (std-frame units, figure ~1.0 tall) is "
                     "excluded from diffusion")
ap.add_argument("--eps", type=float, default=3e-4,
                help="ray start depth below the surface; must be << --thin")
ap.add_argument("--preview", help="directory for view-space preview PNGs")
ap.add_argument("--preview-yaws", default="270,90,0")
ap.add_argument("--preview-el", type=float, default=0.0)
ap.add_argument("--max-frac", type=float, default=0.35,
                help="ANDON: refuse a mask covering more than this fraction of "
                     "valid texels — the derivation, not the character, is wrong")
args = ap.parse_args()

meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
pos_e = np.load(os.path.join(args.prep, "pos.npy"))
nor_e = np.load(os.path.join(args.prep, "nor.npy"))
mask = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
lo = np.array(meta["lo"], dtype=np.float64)
hi = np.array(meta["hi"], dtype=np.float64)
maxabs = meta["maxabs"]

valid = mask.reshape(-1)
P = (pos_e.reshape(-1, 3)[valid].astype(np.float64) * (hi - lo) + lo) / maxabs * 0.5
N = nor_e.reshape(-1, 3)[valid].astype(np.float64) * 2.0 - 1.0
N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
NV = P.shape[0]

# same load + swizzle as project_twins / texpass_iter: glTF is Y-up, std is Z-up
m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))
print(f"[thin] atlas {RES}  valid texels {NV:,}  faces {len(f):,}", flush=True)

thick = np.empty(NV, dtype=np.float64)
CH = 2_000_000
for s in range(0, NV, CH):
    e = min(s + CH, NV)
    org = (P[s:e] - N[s:e] * args.eps).astype(np.float32)
    dr = (-N[s:e]).astype(np.float32)
    t = rs.cast_rays(o3d.core.Tensor(
        np.concatenate([org, dr], axis=1)))["t_hit"].numpy()
    thick[s:e] = t.astype(np.float64) + args.eps

fin = np.isfinite(thick)
print(f"[thin] rays exiting the far side: {int(fin.sum()):,}/{NV:,} "
      f"({fin.mean() * 100:.1f}%) — the rest are open/non-manifold and read as thick",
      flush=True)
qs = [1, 5, 10, 25, 50, 75, 90, 99]
qv = np.percentile(thick[fin], qs)
print("[thin] thickness percentiles (std frame, figure ~1.0 tall):", flush=True)
for q, val in zip(qs, qv):
    print(f"[thin]   p{q:<3d} {val:.5f}", flush=True)
for t in (0.005, 0.01, 0.015, 0.02, 0.03, 0.05):
    n = int((thick < t).sum())
    print(f"[thin]   < {t:.3f} -> {n:,} texels ({n / NV * 100:.2f}% of valid)",
          flush=True)

thin = thick < args.thin
frac = thin.mean()
print(f"[thin] THRESHOLD {args.thin}: {int(thin.sum()):,} texels excluded "
      f"({frac * 100:.2f}% of valid)", flush=True)
assert frac < args.max_frac, (
    f"ANDON: thin mask covers {frac * 100:.1f}% of the surface at --thin "
    f"{args.thin} — that is a broken derivation, not a thin character")

out = np.zeros(RES * RES, dtype=bool)
out[np.where(valid)[0]] = thin
out = out.reshape(RES, RES)
np.save(args.out, out)
Image.fromarray((out * 255).astype(np.uint8)).save(
    os.path.splitext(args.out)[0] + "_texelspace.png")
print(f"[thin] wrote {args.out} + _texelspace.png", flush=True)


def basis(yaw_d, el_d):
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    look = -cd / np.linalg.norm(cd)
    up0 = np.array([0.0, 0.0, 1.0])
    right = np.cross(look, up0)
    right /= np.linalg.norm(right) + 1e-12
    up = np.cross(right, look)
    return look, right, up / (np.linalg.norm(up) + 1e-12)


if args.preview:
    # Same camera convention as texpass_iter.emit, so a preview pixel means exactly
    # what the job mask will mean.
    os.makedirs(args.preview, exist_ok=True)
    uv = np.asarray(m.visual.uv, dtype=np.float64)
    blo, bhi = v.min(axis=0), v.max(axis=0)
    bmid = (blo + bhi) / 2
    v_ext = (bhi[2] - blo[2]) * 1.204
    h_ext = v_ext * (W / H)
    thinf = out.astype(np.float32)
    for yaw in [float(y) for y in args.preview_yaws.split(",")]:
        look, right, up = basis(yaw, args.preview_el)
        xs = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
        ys = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
        gx, gy = np.meshgrid(xs, ys)
        org = (bmid[None, None, :] + gx[..., None] * right[None, None, :]
               + gy[..., None] * up[None, None, :] - look[None, None, :] * D)
        dr = np.broadcast_to(look, org.shape)
        ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [org, dr], axis=-1).reshape(-1, 6).astype(np.float32)))
        prim = ans["primitive_ids"].numpy().reshape(H, W)
        buv = ans["primitive_uvs"].numpy().reshape(H, W, 2)
        hit = np.isfinite(ans["t_hit"].numpy().reshape(H, W))
        img = np.zeros((H, W, 3), dtype=np.float32)
        img[hit] = 0.35
        nex = 0
        if hit.any():
            tri = f[prim[hit]]
            wu, wv = buv[hit][:, 0:1], buv[hit][:, 1:2]
            uvp = (1 - wu - wv) * uv[tri[:, 0]] + wu * uv[tri[:, 1]] + wv * uv[tri[:, 2]]
            ax = np.clip((uvp[:, 0] * RES).astype(np.int64), 0, RES - 1)
            ay = np.clip(((1.0 - uvp[:, 1]) * RES).astype(np.int64), 0, RES - 1)
            s = thinf[ay, ax]
            nex = int((s > 0.5).sum())
            c = img[hit]
            c[:, 0] = np.maximum(c[:, 0], s)
            c[:, 1] = c[:, 1] * (1 - s)
            c[:, 2] = c[:, 2] * (1 - s)
            img[hit] = c
        p = os.path.join(args.preview, f"thin_y{int(yaw):+04d}.png")
        Image.fromarray((img * 255).round().astype(np.uint8)).save(p)
        print(f"[thin] preview {p}  ({int(hit.sum()):,} figure px, "
              f"{nex:,} excluded px)", flush=True)
print("[thin] DONE", flush=True)
