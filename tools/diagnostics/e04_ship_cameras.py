"""E04 Task 4a, part 2 - candidate CAMERA SETS by union coverage, and whether the
thin-extent distribution actually has a cut in it.

Two corrections to the first pass, both of which would have produced a wrong answer:

  A camera set is a UNION, not a per-elevation score. e04_ship_measure scored each
  elevation independently, which answers "what does one elevation see" - a question nobody
  asked. What decides the set is what the WHOLE set reaches together, and adding a camera
  to a set that already sees a surface buys nothing. Candidate sets are scored here as
  unions, with the marginal gain of the elevated pair reported separately so a camera that
  earns nothing is visible as earning nothing.

  A threshold needs a DENSITY, not a CDF. "16.55% of pixels are under 0.005" does not
  establish that 0.005 is a boundary - a monotone distribution gives that number too. This
  repo has already paid once for reading two distant medians as a gap where the density
  rose monotonically with no antimode at all. So the extent distribution is histogrammed in
  the thin region and the shape reported; if there is no antimode, the honest output is to
  say so and report numerator and denominator rather than invent a cut.

  e04_ship_cameras.py --glb ship.glb --out DIR

Standards compliance: EXTERNAL_VERIFIER - reports coverage and shape; adopting a set is a
decision argued in the report from these numbers. ANDON_AUTHORITY - no threshold is emitted
where the density does not support one.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--ray-res", type=int, default=1400)
ap.add_argument("--deck-normal", type=float, default=0.5)
args = ap.parse_args()
os.makedirs(args.out, exist_ok=True)

m = trimesh.load(args.glb, force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
vz = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
lo, hi = vz.min(0), vz.max(0)
mid = (lo + hi) / 2
span = float(max(hi[0] - lo[0], hi[1] - lo[1])) * 1.15
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(vz.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))
tri = vz[f]
nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
area = np.linalg.norm(nrm, axis=1) / 2.0
nz = nrm[:, 2] / (np.linalg.norm(nrm, axis=1) + 1e-12)
deck = nz > args.deck_normal
deck_area = float(area[deck].sum())
tot_area = float(area.sum())
R = args.ray_res


def basis(yaw_d, el_d):
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    look = -cd / np.linalg.norm(cd)
    up0 = np.array([0.0, 0.0, 1.0])
    right = np.cross(look, up0)
    if np.linalg.norm(right) < 1e-9:
        right = np.array([1.0, 0.0, 0.0])
    right /= np.linalg.norm(right)
    up = np.cross(right, look)
    return look, right, up / np.linalg.norm(up)


_cache = {}


def seen_by(yaw, el):
    key = (round(yaw, 3), round(el, 3))
    if key in _cache:
        return _cache[key]
    look, right, up = basis(yaw, el)
    g = (np.arange(R) + 0.5) / R * span - span / 2
    gx, gy = np.meshgrid(g, -g)
    org = (mid[None, None, :] + gx[..., None] * right[None, None, :]
           + gy[..., None] * up[None, None, :] - look[None, None, :] * 4.0)
    ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
    pid = ans["primitive_ids"].numpy().reshape(-1)
    hit = np.isfinite(ans["t_hit"].numpy().reshape(-1))
    s = np.zeros(len(f), dtype=bool)
    s[pid[hit]] = True
    _cache[key] = s
    return s


EYE8 = [(y, 0.0) for y in (0, 45, 90, 135, 180, 225, 270, 315)]
SETS = {
    "eye8 only": EYE8,
    "eye8 + character pair (0/180 @ 55)": EYE8 + [(0, 55), (180, 55)],
    "eye8 + pair @ 40": EYE8 + [(0, 40), (180, 40)],
    "eye8 + pair @ 30": EYE8 + [(0, 30), (180, 30)],
    "eye8 + beam pair @ 40 (90/270)": EYE8 + [(90, 40), (270, 40)],
    "eye8 + quad @ 40": EYE8 + [(0, 40), (90, 40), (180, 40), (270, 40)],
    "eye8 + quad @ 40 diagonal": EYE8 + [(45, 40), (135, 40), (225, 40), (315, 40)],
    "eye8 + quad @ 30": EYE8 + [(0, 30), (90, 30), (180, 30), (270, 30)],
    "eye8 + top (0 @ 90)": EYE8 + [(0, 90)],
}
rows = []
base = None
print("[cam] set coverage, as UNIONS (deck = upward-facing AREA, all = total AREA)", flush=True)
for nm, cams in SETS.items():
    s = np.zeros(len(f), dtype=bool)
    for y, e in cams:
        s |= seen_by(y, e)
    d = float(area[deck & s].sum() / max(deck_area, 1e-12)) * 100
    a = float(area[s].sum() / tot_area) * 100
    if base is None:
        base = (d, a)
    rows.append({"set": nm, "cameras": len(cams), "deck_pct": round(d, 2),
                 "all_pct": round(a, 2), "deck_gain_vs_eye8": round(d - base[0], 2),
                 "all_gain_vs_eye8": round(a - base[1], 2)})
    print("[cam]   %-36s %2d cams  deck %5.2f%% (%+5.2f)  all %5.2f%% (%+5.2f)"
          % (nm, len(cams), d, d - base[0], a, a - base[1]), flush=True)

# ---------------------------------------------------------- thin-extent DENSITY
D = 4.0
ext_all = []
for yaw in (0.0, 45.0, 90.0, 135.0):
    look, right, up = basis(yaw, 0.0)
    g = (np.arange(R) + 0.5) / R * span - span / 2
    gx, gy = np.meshgrid(g, -g)
    org = (mid[None, None, :] + gx[..., None] * right[None, None, :]
           + gy[..., None] * up[None, None, :] - look[None, None, :] * D)
    aF = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
    aB = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org + look[None, None, :] * (2 * D), np.broadcast_to(-look, org.shape)],
        axis=-1).reshape(-1, 6).astype(np.float32)))
    tF = aF["t_hit"].numpy().reshape(-1)
    tB = aB["t_hit"].numpy().reshape(-1)
    both = np.isfinite(tF) & np.isfinite(tB)
    ext_all.append(2 * D - tF[both] - tB[both])
E = np.concatenate(ext_all)
print("\n[cam] thin-extent DENSITY over %d figure px, 0 to 0.06 in 40 bins:" % len(E), flush=True)
hb = np.linspace(0, 0.06, 41)
h, _ = np.histogram(E, bins=hb)
mx = max(h.max(), 1)
dens = []
for i in range(len(h)):
    dens.append({"lo": round(float(hb[i]), 5), "hi": round(float(hb[i + 1]), 5),
                 "n": int(h[i])})
    bar = "#" * int(round(48 * h[i] / mx))
    print("[cam]   %.4f-%.4f  %7d  %s" % (hb[i], hb[i + 1], h[i], bar), flush=True)
# antimode search: is there a local minimum between the thin peak and the bulk?
i_pk = int(np.argmax(h))
tail = h[i_pk:]
anti = None
for j in range(1, len(tail) - 1):
    if tail[j] < tail[j - 1] and tail[j] <= tail[j + 1] and tail[j] < 0.5 * h[i_pk]:
        anti = float(hb[i_pk + j])
        break
print("\n[cam] thin peak bin %.4f-%.4f (n=%d).  antimode after it: %s"
      % (hb[i_pk], hb[i_pk + 1], h[i_pk], ("%.4f" % anti) if anti else "NONE FOUND"),
      flush=True)
json.dump({"sets": rows, "deck_area_frac_of_total": round(deck_area / tot_area, 5),
           "thin_density": dens, "thin_peak_bin": [round(float(hb[i_pk]), 5),
                                                   round(float(hb[i_pk + 1]), 5)],
           "antimode": anti, "n_px": int(len(E))},
          open(os.path.join(args.out, "ship_cameras.json"), "w"), indent=1)
print("[cam] wrote %s" % os.path.join(args.out, "ship_cameras.json"), flush=True)
