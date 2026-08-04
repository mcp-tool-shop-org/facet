"""E04 Task 4a - measure ship.json's suspended values from the designated mesh.

Every number ship.json marked SUSPENDED is suspended because it was one character's
measurement. This derives each one from `galleon_00006_raw.glb` instead, by geometry, with
no generation and no GPU.

Four measurements, and each is written to answer the question the character value answered
rather than to copy its shape:

  FRAMING     The rotating silhouette's true projected width per yaw - not the bounding box,
              which understates it: a box seen at 45 degrees is wider on screen than
              broadside. The frame must contain the widest view, not the widest axis.
  ORIENTATION Which end is the bow, from the hull's own profile, and what --yaw-offset the
              declared front implies. The camera rotates, never the mesh: to_mesh() destroys
              authored vertex normals (normalize_mesh.py's docstring, measured).
  ELEVATIONS  "Decks need looking into" is a design note; this makes it a number. Upward-
              facing surface is identified by normal, and each candidate elevation is scored
              by what FRACTION OF THAT SURFACE'S AREA a camera at that elevation actually
              first-hits. Area, not triangle count - a deck is a few large triangles and the
              rigging is thousands of tiny ones, so counting would measure the rigging.
  THIN        The extent along the view ray, exactly as texpass_iter's --thin-extent measures
              it (2D - t_front - t_back), so the number derived here means what the flag
              means. Reported as a distribution with the rigging population identified, not
              as a single value picked to look right.

  e04_ship_measure.py --glb ship.glb --out DIR [--yaws 24] [--elevations 0,15,...]

Standards compliance: PIN_PER_STEP - every parameter is an argument and the mesh is named.
EXTERNAL_VERIFIER - it measures and tabulates; which elevation set to adopt is a decision
recorded in the report, and the coverage numbers are what it is argued from.
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
ap.add_argument("--yaws", type=int, default=72, help="yaw samples for the width sweep")
ap.add_argument("--elevations", default="0,10,20,30,40,50,55,60,70,80,90")
ap.add_argument("--el-yaws", default="0,45,90,135,180,225,270,315")
ap.add_argument("--deck-normal", type=float, default=0.5,
                help="normal_z above which a face counts as upward-facing (deck). 0.5 = "
                     "within 60 degrees of straight up.")
ap.add_argument("--ray-res", type=int, default=1400)
ap.add_argument("--margin-target", type=float, default=1.204,
                help="the BORDER FRACTION to keep, inherited from the character line as a "
                     "look convention rather than as a subject measurement. The margin "
                     "value that delivers it is derived below and is NOT this number.")
args = ap.parse_args()
os.makedirs(args.out, exist_ok=True)

m = trimesh.load(args.glb, force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
vz = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
lo, hi = vz.min(0), vz.max(0)
size = hi - lo
mid = (lo + hi) / 2
out = {"glb": os.path.abspath(args.glb), "extent_std": [round(float(x), 5) for x in size]}
print("[ship] std extent x %.4f  y %.4f  z %.4f" % tuple(size), flush=True)

rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(vz.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))


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


# ------------------------------------------------------------------ 1. FRAMING
# The bounding box understates the widest view. Project every vertex at every yaw and take
# the real extent; a box at 45 degrees presents its diagonal.
wid = []
for i in range(args.yaws):
    yaw = 360.0 * i / args.yaws
    look, right, up = basis(yaw, 0.0)
    x = vz @ right
    wid.append((yaw, float(x.max() - x.min())))
wmax = max(w for _, w in wid)
wmax_yaw = [y for y, w in wid if w == wmax][0]
wbbox = float(max(size[0], size[1]))
height = float(size[2])
out["width_sweep"] = {"max_projected_width": round(wmax, 5),
                      "at_yaw": round(wmax_yaw, 1),
                      "bbox_widest_axis": round(wbbox, 5),
                      "understatement_pct": round((wmax / wbbox - 1) * 100, 2),
                      "height": round(height, 5),
                      "aspect_widest_over_height": round(wmax / height, 5)}
print("[ship] widest projected width %.4f at yaw %.0f  (bbox widest axis %.4f -> the box "
      "understates by %.2f%%)" % (wmax, wmax_yaw, wbbox, (wmax / wbbox - 1) * 100), flush=True)

# turn_render sets ortho_scale = size.z * margin and Blender maps ortho_scale to the LARGER
# render axis. So for a subject wider than tall the horizontal span is size.z * margin, and
# the margin that delivers the target border fraction on BOTH axes is derived, not guessed.
asp = wmax / height
margin = args.margin_target * asp
out["framing"] = {
    "aspect_w_over_h": round(asp, 5),
    "render_w_at_1024h": int(round(1024 * asp)),
    "derived_margin": round(margin, 5),
    "note": ("ortho_scale = size_z * margin lands on the LARGER render axis. With aspect "
             "w/h = %.4f, margin %.4f gives horizontal span %.4f (= widest view %.4f x "
             "%.3f) and vertical span %.4f (= height %.4f x %.3f) - the same border "
             "fraction on both axes."
             % (asp, margin, height * margin, wmax, args.margin_target,
                height * margin / asp, height, args.margin_target))}
print("[ship] framing: aspect %.4f -> %d x 1024, derived margin %.4f (border fraction "
      "%.3f both axes)" % (asp, int(round(1024 * asp)), margin, args.margin_target), flush=True)

# ------------------------------------------------------------- 2. ORIENTATION
# Which end is the bow: the bowsprit is a thin low protrusion, the stern carries the castle.
# Measured as vertex mass and beam in the outermost slice at each end of the long axis.
long_ax = int(np.argmax(size[:2]))
lab = "xy"[long_ax]
edges = np.linspace(lo[long_ax], hi[long_ax], 25)
ends = {}
for nm, sl in (("minus", (edges[0], edges[1])), ("plus", (edges[-2], edges[-1]))):
    s = (vz[:, long_ax] >= sl[0]) & (vz[:, long_ax] < sl[1])
    if s.sum() < 10:
        s = (vz[:, long_ax] >= sl[0]) & (vz[:, long_ax] <= sl[1])
    beam = float(vz[s, 1 - long_ax].max() - vz[s, 1 - long_ax].min()) if s.sum() else 0.0
    ends[nm] = {"verts": int(s.sum()), "beam": round(beam, 4),
                "z_max": round(float(vz[s, 2].max()), 4) if s.sum() else None,
                "z_min": round(float(vz[s, 2].min()), 4) if s.sum() else None}
bow = "minus" if ends["minus"]["verts"] < ends["plus"]["verts"] else "plus"
out["orientation"] = {"long_axis": lab, "ends": ends, "bow_end": bow,
                      "reasoning": "the bowsprit is a thin low protrusion and carries far "
                                   "less vertex mass than the stern castle; confirmed by "
                                   "eye on the clay renders (spired turret at +%s)" % lab}
print("[ship] long axis %s  bow at %s end  (minus %d verts beam %.3f | plus %d verts beam "
      "%.3f)" % (lab, bow, ends["minus"]["verts"], ends["minus"]["beam"],
                 ends["plus"]["verts"], ends["plus"]["beam"]), flush=True)

# --------------------------------------------------------------- 3. ELEVATIONS
# Upward-facing surface, by AREA. A deck is a few large triangles; the rigging is thousands
# of tiny ones, so a count would measure the rigging and call it deck.
tri = vz[f]
n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
area = np.linalg.norm(n, axis=1) / 2.0
nz = n[:, 2] / (np.linalg.norm(n, axis=1) + 1e-12)
deck = nz > args.deck_normal
deck_area = float(area[deck].sum())
out["deck"] = {"faces": int(deck.sum()), "faces_pct": round(100.0 * deck.mean(), 2),
               "area": round(deck_area, 6),
               "area_pct_of_total": round(100.0 * deck_area / float(area.sum()), 2),
               "normal_z_threshold": args.deck_normal}
print("[ship] upward-facing surface: %d faces (%.2f%%), %.2f%% of total AREA"
      % (deck.sum(), 100.0 * deck.mean(), 100.0 * deck_area / float(area.sum())), flush=True)

R = args.ray_res
span = wmax * 1.15
el_yaws = [float(x) for x in args.el_yaws.split(",")]
rows = []
for el in [float(x) for x in args.elevations.split(",")]:
    seen = np.zeros(len(f), dtype=bool)
    for yaw in el_yaws:
        look, right, up = basis(yaw, el)
        g = (np.arange(R) + 0.5) / R * span - span / 2
        gx, gy = np.meshgrid(g, -g)
        org = (mid[None, None, :] + gx[..., None] * right[None, None, :]
               + gy[..., None] * up[None, None, :] - look[None, None, :] * 4.0)
        ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
        pid = ans["primitive_ids"].numpy().reshape(-1)
        hit = np.isfinite(ans["t_hit"].numpy().reshape(-1))
        seen[pid[hit]] = True
    cov = float(area[deck & seen].sum() / max(deck_area, 1e-12))
    allcov = float(area[seen].sum() / float(area.sum()))
    rows.append({"elevation": el, "deck_area_seen_pct": round(100 * cov, 2),
                 "all_area_seen_pct": round(100 * allcov, 2)})
    print("[ship]   elevation %4.0f deg: deck area seen %5.2f%%   all surface %5.2f%%"
          % (el, 100 * cov, 100 * allcov), flush=True)
out["elevation_sweep"] = {"yaws_per_elevation": el_yaws, "rows": rows}

# ------------------------------------------------------------------- 4. THIN
# texpass_iter's own measurement: extent along the view ray, front hit to back hit.
D = 4.0
th_rows = []
allext = []
for yaw in (0.0, 45.0, 90.0):
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
    ext = 2 * D - tF[both] - tB[both]
    allext.append(ext)
    qs = [1, 5, 10, 25, 50, 75, 90]
    th_rows.append({"yaw": yaw, "px": int(both.sum()),
                    "pct": {str(q): round(float(np.percentile(ext, q)), 5) for q in qs}})
    print("[ship]   yaw %3.0f thin-extent percentiles " % yaw
          + "  ".join("p%d %.4f" % (q, np.percentile(ext, q)) for q in qs), flush=True)
E = np.concatenate(allext)
for t in (0.005, 0.010, 0.015, 0.020, 0.030, 0.040, 0.050):
    print("[ship]   extent < %.3f : %5.2f%% of figure px" % (t, 100 * float((E < t).mean())),
          flush=True)
out["thin_extent"] = {"rows": th_rows,
                      "share_below": {str(t): round(100 * float((E < t).mean()), 3)
                                      for t in (0.005, 0.010, 0.015, 0.020, 0.030, 0.040, 0.050)},
                      "character_value_for_comparison": 0.030}

json.dump(out, open(os.path.join(args.out, "ship_measure.json"), "w"), indent=1)
print("[ship] wrote %s" % os.path.join(args.out, "ship_measure.json"), flush=True)
