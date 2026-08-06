"""E12 handoff 3 - characterise a fired ANCHOR 1c, without re-running it for a pass.

`e04_frame_agree.py` halted at 1 differing px on view 5 of the beast's pair framing. Its
pre-registered readings (E04 Ruling 10) send BOTH the benign and the malign case to a halt:

    0 px                             -> anchor passes
    a few boundary px, uniform scatter -> float edge-ordering at the silhouette; report and halt
    a structural offset              -> the gate's real prey; the fit-axis change needs review

So the halt stands either way and this tool does not lift it. It answers the one question a
ruling needs and the gate itself does not report: WHICH of the two lower rows this is.

THE HYPOTHESIS IT TESTS, stated before it runs. The two implementations are not the same
arithmetic on the same numbers:

  silhouette_masks.py  normalises  v -> [x, -z, y] / max|v| * 0.5   then derives h_ext
  e04_frame_agree.py   does NOT normalise                          then derives h_ext

That is a uniform scale which the mesh AND the ray grid both carry, so it cancels
mathematically - and it does not cancel in float32, because the ray origins are cast at a
different magnitude and round differently. Measured here: does re-deriving the gate's grid on
the NORMALISED mesh drive the disagreement to zero? If yes, the 1 px is the gate's own third
implementation, not turn_render's framing.

  e12_agree_probe.py --glb prep_uv.glb --masks DIR --tag dragonclay --views 1,5
                     --aspect 1792,1024 --fit-axis width [--margin 1.204]

Standards compliance: PIN_PER_STEP - every camera parameter comes from the same flags the
gate takes. ANDON_AUTHORITY - it GRADES NOTHING and lifts nothing; the gate's exit code is
the gate. EXTERNAL_VERIFIER - it compares a third independent construction against both of
the first two, and it can return "the offset is structural", which would confirm the gate.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import binary_erosion

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--masks", required=True)
ap.add_argument("--tag", default="dragonclay")
ap.add_argument("--views", default="1,5")
ap.add_argument("--step", type=float, default=45.0)
ap.add_argument("--aspect", required=True)
ap.add_argument("--fit-axis", default="width", choices=["height", "width"])
ap.add_argument("--margin", type=float, default=1.204)
ap.add_argument("--out", default=None)
args = ap.parse_args()

W, H = (int(x) for x in args.aspect.split(","))
m = trimesh.load(args.glb, force="mesh", process=False)
v0 = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)


def cast(vb, ray_back, k):
    """One silhouette, from whatever frame `vb` is expressed in."""
    lo, hi = vb.min(0), vb.max(0)
    size = hi - lo
    mid = (lo + hi) / 2
    if args.fit_axis == "height":
        ortho = size[2] * args.margin
        v_ext, h_ext = ortho, ortho * (W / H)
    else:
        ortho = max(size[0], size[1]) * args.margin
        h_ext, v_ext = ortho, ortho * (H / W)
    rs = o3d.t.geometry.RaycastingScene()
    rs.add_triangles(o3d.core.Tensor(vb.astype(np.float32)),
                     o3d.core.Tensor(f.astype(np.uint32)))
    th = np.radians(k * args.step)
    right = np.array([np.cos(th), np.sin(th), 0.0])
    up = np.array([0.0, 0.0, 1.0])
    look = np.array([-np.sin(th), np.cos(th), 0.0])
    xs = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
    ys = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
    gx, gy = np.meshgrid(xs, ys)
    org = (mid[None, None, :] + gx[..., None] * right[None, None, :]
           + gy[..., None] * up[None, None, :] - look[None, None, :] * ray_back)
    ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
    return np.isfinite(ans["t_hit"].numpy().reshape(H, W)), h_ext, v_ext


# the Blender glTF import remap, applied by every consumer here
vb_raw = np.stack([v0[:, 0], -v0[:, 2], v0[:, 1]], axis=1)
# silhouette_masks' own normalisation, verbatim: scale computed on the PRE-remap vertices
vmax = np.abs(v0).max()
vb_norm = vb_raw / vmax * 0.5
radius_raw = max((vb_raw.max(0) - vb_raw.min(0))[0], (vb_raw.max(0) - vb_raw.min(0))[1]) * 3.0

print("[probe] uniform scale between the two frames: %.12f  (0.5 / %.9f)"
      % (0.5 / vmax, vmax), flush=True)

rows = []
for k in [int(x) for x in args.views.split(",")]:
    sil = np.asarray(Image.open(
        os.path.join(args.masks, "%s_%d.png" % (args.tag, k))).convert("L")) > 127

    gate, hg, vg = cast(vb_raw, radius_raw, k)        # e04_frame_agree's construction
    norm, hn, vn = cast(vb_norm, 2.0, k)              # silhouette_masks' construction

    d_gate = gate ^ sil
    d_norm = norm ^ sil
    row = {"view": k,
           "gate_h_ext": round(float(hg), 9), "norm_h_ext": round(float(hn), 9),
           "sil_px": int(sil.sum()),
           "gate_vs_sil_px": int(d_gate.sum()), "norm_vs_sil_px": int(d_norm.sum())}

    # where do the disagreeing pixels sit? A boundary pixel has a background 4-neighbour.
    interior = binary_erosion(sil, np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], bool))
    boundary_band = sil & ~interior
    for name, d in (("gate", d_gate), ("norm", d_norm)):
        n = int(d.sum())
        if not n:
            row[name + "_where"] = "none"
            continue
        ys, xs = np.nonzero(d)
        # distance from the disagreeing pixel to the nearest silhouette boundary pixel,
        # measured on the 8-neighbourhood - 0 means it touches the rim.
        touch = 0
        for y, x in zip(ys, xs):
            y0, y1 = max(0, y - 1), min(H, y + 2)
            x0, x1 = max(0, x - 1), min(W, x + 2)
            if boundary_band[y0:y1, x0:x1].any():
                touch += 1
        row[name + "_where"] = {
            "n": n, "touching_rim": touch, "interior": n - touch,
            "bbox": [int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())],
            "px": [[int(x), int(y)] for x, y in zip(xs[:8], ys[:8])]}
    rows.append(row)
    print("[probe] view %d: silhouette %d px" % (k, row["sil_px"]), flush=True)
    print("[probe]   gate construction (unnormalised, back %.3f): %d differing  %s"
          % (radius_raw, row["gate_vs_sil_px"], row["gate_where"]), flush=True)
    print("[probe]   same construction on the NORMALISED mesh (back 2.0): %d differing  %s"
          % (row["norm_vs_sil_px"], row["norm_where"]), flush=True)

worst_gate = max(r["gate_vs_sil_px"] for r in rows)
worst_norm = max(r["norm_vs_sil_px"] for r in rows)
print("", flush=True)
print("[probe] worst gate-construction disagreement: %d px" % worst_gate, flush=True)
print("[probe] worst normalised-construction disagreement: %d px" % worst_norm, flush=True)
print("[probe] READING: %s" % (
    "the disagreement is the GATE'S OWN third construction - float rounding at a different "
    "ray magnitude. It is not a framing difference between turn_render and silhouette_masks."
    if worst_norm == 0 < worst_gate else
    "the normalised construction does NOT agree either - this is not the scale hypothesis. "
    "Treat as the gate's real prey until ruled otherwise."), flush=True)
print("[probe] THE GATE'S EXIT CODE STANDS. This tool grades nothing and lifts nothing.",
      flush=True)

if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump({"glb": os.path.abspath(args.glb), "aspect": [W, H],
                   "fit_axis": args.fit_axis, "margin": args.margin,
                   "uniform_scale": 0.5 / float(vmax),
                   "worst_gate_px": worst_gate, "worst_norm_px": worst_norm,
                   "views": rows}, fh, indent=1)
    print("[probe] wrote %s" % args.out, flush=True)
