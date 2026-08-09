"""E13 stroke lane — decompose stage 1's hole map, and answer Ruling 7's re-open check.

TWO HOLE SETS, AND CONFLATING THEM IS THE WHOLE POINT OF THIS FILE:

  the BRUSH's set      reachable but unstyled — some eye-level camera has this texel facing
                       and first-hit visible, and stage 1 rejected it anyway (trust mask or
                       edge erosion). A stroke can reach it.
  DILATION's set       not reachable at all. No exterior eye-level camera sees it; it is
                       self-occlusion, and finalize grows paint into it from neighbours.

The decomposition must close with no remainder against the ruled numbers (24e), and this
tool asserts that rather than printing two figures and letting a reader add them.

RULING 7'S RE-OPEN CHECK IS A FIRST-CLASS OUTPUT, answered in BOTH directions. 7a decided
elevated cameras NONE and named the re-open: "if a large unpainted up-facing field would be
served by an elevated stroke, that evidence re-opens the question at the ruling where stroke
cameras are chosen anyway." So this tool reports the up-facing brush set, its largest
connected component, and what the four measured elevated candidates ADD over the eight
eye-level yaws on the brush's set — including, separately, the up-facing brush set INSIDE THE
WING BOXES, which is the one place on this subject a big up-facing field could hide.

CONNECTED COMPONENTS ARE COMPUTED IN 3-D, NOT IN THE ATLAS. Atlas adjacency is not surface
adjacency — CLAUDE.md's standing rule, and the reason dilation is a defect class at all. The
grid is a voxel hash at --voxel units with 26-connectivity, and the voxel size is quoted
because a component count without its adjacency scale is not a number.

RAY DENSITY (Ruling 7b): every figure below is cast ONE RAY PER TEXEL against the texel set
itself, so there is no image grid to converge and no sampling sensitivity to quote. Where an
emit-grid figure is wanted it is a different measurement and is not made here.

Standards compliance:
  PIN_PER_STEP — every threshold is a flag and prints; regions arrive from recorded JSON.
  ANDON_AUTHORITY — halts if the decomposition leaves a remainder or if the recomputed reach
    disagrees with the banked ceiling; both would mean this is measuring a different object.
  NAMED_COMPENSATORS — writes one JSON (+ optional npy masks). Undo = delete. Reads only.
  EXTERNAL_VERIFIER — reach is recomputed here from geometry rather than read out of the run
    it is checking, so the two agree or the halt fires.

  e13_hole_map.py --prep DIR --styled A0_styled_mask.npy --headbox J
                  --region NAME=boxjson [...] --out J [--elev 0:40,0:55,180:40,180:55]
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--styled", required=True, help="stage 1 _styled_mask.npy (RES x RES bool)")
ap.add_argument("--headbox", help="head_00003.json — its head_box_blender becomes a region")
ap.add_argument("--region", action="append", default=[], metavar="NAME=JSON",
                help="a JSON carrying region_box_canonical (std frame). Repeatable.")
ap.add_argument("--yaws", default="0,45,90,135,180,225,270,315")
ap.add_argument("--facing-min", type=float, default=0.45,
                help="project_twins' floor — the one REACH was banked at")
ap.add_argument("--stroke-facing-min", type=float, default=0.25,
                help="texpass_iter commit's floor, the one a STROKE accepts at")
ap.add_argument("--elev", default="0:40,0:55,180:40,180:55",
                help="elevated candidates for the Ruling 7 check, yaw:el")
ap.add_argument("--up-normal", type=float, default=0.5)
ap.add_argument("--voxel", type=float, default=3e-3,
                help="3-D adjacency scale for connected components, in std units. ~3.5 "
                     "texel spacings at this atlas density; quoted with every count.")
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--banked-reach", type=int, default=1635304)
ap.add_argument("--banked-styled", type=int, default=1430687)
ap.add_argument("--out", required=True)
ap.add_argument("--save-masks", help="dir for brush.npy / reach.npy, for later tasks")
args = ap.parse_args()

meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
lo = np.array(meta["lo"], dtype=np.float64)
hi = np.array(meta["hi"], dtype=np.float64)
maxabs = float(meta["maxabs"])
mask = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
valid = mask.reshape(-1)
P = ((np.load(os.path.join(args.prep, "pos.npy")).reshape(-1, 3)[valid].astype(np.float64)
      * (hi - lo) + lo) / maxabs * 0.5)
N = np.load(os.path.join(args.prep, "nor.npy")).reshape(-1, 3)[valid].astype(np.float64) \
    * 2.0 - 1.0
N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
NV = P.shape[0]
styled = np.load(args.styled).reshape(-1)[np.where(valid)[0]]
if not (styled.shape == (NV,)):
    raise AssertionError(f"ANDON: styled mask has {styled.shape} for {NV:,} valid texels")

m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))


def dtc_of(yaw, el=0.0):
    th, e = np.radians(yaw), np.radians(el)
    d = np.array([np.sin(th) * np.cos(e), -np.cos(th) * np.cos(e), np.sin(e)])
    return d / np.linalg.norm(d)


_cache = {}


def seen(yaw, el, fmin):
    """facing + first-hit visible, one ray per texel. No image grid, no sampling."""
    k = (round(yaw, 4), round(el, 4), fmin)
    if k in _cache:
        return _cache[k]
    d = dtc_of(yaw, el)
    idx = np.where((N @ d) > fmin)[0]
    out = np.zeros(NV, dtype=bool)
    if len(idx):
        o = (P[idx] + N[idx] * args.noffs + d[None, :] * args.bias).astype(np.float32)
        t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [o, np.broadcast_to(d.astype(np.float32), o.shape)], axis=1)))["t_hit"].numpy()
        out[idx[~np.isfinite(t)]] = True
    _cache[k] = out
    return out


YAWS = [float(x) for x in args.yaws.split(",")]
reach = np.zeros(NV, dtype=bool)
for y in YAWS:
    reach |= seen(y, 0.0, args.facing_min)

brush = reach & ~styled
dil = ~reach                      # styled is a subset of reach, so this is dilation's set

print(f"[holes] valid {NV:,}   reach {int(reach.sum()):,}   styled {int(styled.sum()):,}",
      flush=True)
if not (int(reach.sum()) == args.banked_reach):
    raise AssertionError(
        f"ANDON: recomputed reach {int(reach.sum()):,} against the banked "
        f"{args.banked_reach:,} — this is measuring a different object than stage 1 was")
if not (int(styled.sum()) == args.banked_styled):
    raise AssertionError(
        f"ANDON: styled {int(styled.sum()):,} against the banked {args.banked_styled:,}")
if not (int(brush.sum()) + int(dil.sum()) == NV - int(styled.sum())):
    raise AssertionError("ANDON: the hole decomposition leaves a remainder")
print(f"[holes] BRUSH set (reachable, unstyled) {int(brush.sum()):,}   "
      f"DILATION set (unreachable)  {int(dil.sum()):,}   "
      f"total holes {int(brush.sum()) + int(dil.sum()):,}", flush=True)
print(f"[holes] {int(dil.sum())/(int(brush.sum())+int(dil.sum()))*100:.1f}% of holes are "
      f"geometry, not misses (the ship measured 91%)", flush=True)

out = {"_what": "E13 stroke-lane hole decomposition + the Ruling 7 elevated re-open check. "
                "One ray per texel; no image grid, so no ray-density figure applies (7b).",
       "valid": NV, "reach": int(reach.sum()), "styled": int(styled.sum()),
       "brush_set": int(brush.sum()), "dilation_set": int(dil.sum()),
       "voxel": args.voxel, "facing_min": args.facing_min,
       "stroke_facing_min": args.stroke_facing_min}

# ---- orientation ----
nz = N[:, 2]
print("\n[holes] orientation of the BRUSH set (std z is up):", flush=True)
orient = {}
for lab, sel in (("up  nz>+0.5", nz > 0.5), ("up  nz>+0.25", nz > 0.25),
                 ("side |nz|<=0.25", np.abs(nz) <= 0.25), ("down nz<-0.5", nz < -0.5)):
    b = int((brush & sel).sum())
    r = int((reach & sel).sum())
    print(f"[holes]   {lab:<16} brush {b:>9,} ({b/max(int(brush.sum()),1)*100:5.2f}% of "
          f"brush)   reach {r:>9,}   holed {b/max(r,1)*100:5.2f}% of that reach", flush=True)
    orient[lab] = {"brush": b, "reach": r, "holed_pct_of_reach": b / max(r, 1) * 100}
out["orientation"] = orient

# ---- regions ----
REG = {}
if args.headbox:
    hb = json.load(open(args.headbox))
    b0, b1 = [np.array(x, dtype=np.float64) / maxabs * 0.5 for x in hb["head_box_blender"]]
    REG["head"] = (b0, b1)
for spec in args.region:
    k, _, p = spec.partition("=")
    d = json.load(open(p))
    b0, b1 = [np.array(x, dtype=np.float64) for x in d["region_box_canonical"]]
    REG[k] = (b0, b1)
print("\n[holes] BRUSH set by region (spatial boxes; a box is a region of space, not a "
      "segmentation):", flush=True)
regs = {}
inreg = {}
for k, (b0, b1) in REG.items():
    sel = ((P >= b0).all(axis=1) & (P <= b1).all(axis=1))
    inreg[k] = sel
    b = int((brush & sel).sum())
    r = int((reach & sel).sum())
    s = int((styled & sel).sum())
    print(f"[holes]   {k:<12} valid {int(sel.sum()):>9,}  reach {r:>9,}  styled {s:>9,}  "
          f"BRUSH {b:>8,}   holed {b/max(r,1)*100:5.2f}% of its own reach", flush=True)
    regs[k] = {"valid": int(sel.sum()), "reach": r, "styled": s, "brush": b,
               "holed_pct_of_own_reach": b / max(r, 1) * 100}
rest = ~np.any(np.stack(list(inreg.values())), axis=0) if inreg else np.ones(NV, bool)
b = int((brush & rest).sum())
r = int((reach & rest).sum())
print(f"[holes]   {'rest':<12} valid {int(rest.sum()):>9,}  reach {r:>9,}  "
      f"styled {int((styled & rest).sum()):>9,}  BRUSH {b:>8,}   "
      f"holed {b/max(r,1)*100:5.2f}% of its own reach", flush=True)
regs["rest"] = {"valid": int(rest.sum()), "reach": r, "styled": int((styled & rest).sum()),
                "brush": b, "holed_pct_of_own_reach": b / max(r, 1) * 100}
out["regions"] = regs


# ---- 3-D connected components ----
def components(sel):
    pts = P[sel]
    if not len(pts):
        return np.array([], dtype=np.int64), {}
    q = np.floor(pts / args.voxel).astype(np.int64)
    keys, inv = np.unique(q, axis=0, return_inverse=True)
    lut = {tuple(k): i for i, k in enumerate(map(tuple, keys))}
    parent = np.arange(len(keys))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    offs = [(a, b_, c) for a in (-1, 0, 1) for b_ in (-1, 0, 1) for c in (-1, 0, 1)
            if (a, b_, c) > (0, 0, 0)]
    for i, k in enumerate(map(tuple, keys)):
        for o in offs:
            j = lut.get((k[0] + o[0], k[1] + o[1], k[2] + o[2]))
            if j is not None:
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[ri] = rj
    roots = np.array([find(i) for i in range(len(keys))])
    lab = roots[inv]
    _, sizes = np.unique(lab, return_counts=True)
    return np.sort(sizes)[::-1], {"n": int(len(sizes))}


sizes, info = components(brush)
tot = int(brush.sum())
print(f"\n[holes] BRUSH set 3-D connected components at voxel {args.voxel:g} "
      f"(~3.5 texel spacings): {info['n']:,} components", flush=True)
print(f"[holes]   largest {sizes[0]:,} ({sizes[0]/tot*100:.2f}% of the set); "
      f"top 5 {', '.join(f'{s:,}' for s in sizes[:5])}", flush=True)
for cut in (100, 1000, 10000):
    small = int(sizes[sizes < cut].sum())
    print(f"[holes]   in components under {cut:>6,} texels: {small:>9,} "
          f"({small/tot*100:5.2f}% of the set)", flush=True)
out["components"] = {"voxel": args.voxel, "n": info["n"],
                     "largest": int(sizes[0]), "top10": [int(s) for s in sizes[:10]],
                     "frac_in_components_under": {
                         str(c): float(sizes[sizes < c].sum()) / tot
                         for c in (100, 1000, 10000)}}

# ---- per view: which existing camera sees each brush hole best ----
print("\n[holes] which eye-level camera sees each BRUSH hole (at the STROKE floor "
      f"{args.stroke_facing_min:g}, one ray per texel):", flush=True)
best = np.full(NV, -1, dtype=np.int16)
bestf = np.zeros(NV, dtype=np.float64)
cover = {}
for i, y in enumerate(YAWS):
    s = seen(y, 0.0, args.stroke_facing_min)
    fac = N @ dtc_of(y, 0.0)
    take = s & brush & (fac > bestf)
    bestf[take] = fac[take]
    best[take] = i
    cover[y] = int((s & brush).sum())
for i, y in enumerate(YAWS):
    n = int((best == i).sum())
    print(f"[holes]   yaw {int(y):>3}  sees {cover[y]:>8,} of the brush set  "
          f"({cover[y]/tot*100:5.1f}%)   best-for {n:>8,}", flush=True)
unseen = int((brush & (best < 0)).sum())
print(f"[holes]   NO eye-level camera at the stroke floor: {unseen:,} "
      f"({unseen/tot*100:.2f}% of the brush set)", flush=True)
out["per_view"] = {str(int(y)): {"sees": cover[y], "best_for": int((best == i).sum())}
                   for i, y in enumerate(YAWS)}
out["brush_unseen_at_stroke_floor"] = unseen

# ---- RULING 7: the elevated re-open check, answered both ways ----
print("\n[holes] RULING 7 RE-OPEN CHECK — does an elevated stroke camera serve a large "
      "unpainted up-facing field?", flush=True)
eye = np.zeros(NV, dtype=bool)
for y in YAWS:
    eye |= seen(y, 0.0, args.stroke_facing_min)
base = int((eye & brush).sum())
# ⚠ THE BINARY COVERAGE FIGURE BELOW CANNOT FAIL, AND IT IS PRINTED SAYING SO.
# `reach` is the union of seen(yaw, 0, 0.45); the stroke floor is 0.25, and the visibility
# raycast is the same first-hit test, so seen(y, 0, 0.25) is a SUPERSET of seen(y, 0, 0.45)
# texel for texel. The eight eye-level yaws therefore cover 100% of the brush set BY
# CONSTRUCTION, and any elevated camera adds exactly 0 whatever the geometry does. A check
# that cannot fail is not a check (CLAUDE.md) — this one is retained only as the proof that
# no brush texel is out of eye-level reach, which is a real if trivial statement, and the
# ACTUAL question is answered below it.
print(f"[holes]   eight eye-level yaws cover {base:,} of {tot:,} "
      f"({base/tot*100:.2f}%) — TAUTOLOGICAL: the stroke floor {args.stroke_facing_min:g} "
      f"is looser than the {args.facing_min:g} reach was defined at, so this is 100% by "
      f"construction and adds nothing. The real check follows.", flush=True)
ev = {}
cum = eye.copy()
for spec in [s for s in args.elev.split(",") if s.strip()]:
    y, e = [float(x) for x in spec.split(":")]
    s = seen(y, e, args.stroke_facing_min)
    add = int((s & brush & ~cum).sum())
    cum |= s
    ev[spec] = {"adds_binary": add}
total_add = int((cum & brush).sum()) - base

# THE REAL CHECK: an elevated stroke earns its place by seeing a texel BETTER, not by being
# the only one that sees it. A grazing camera paints a stretched, low-confidence sample —
# that is why commit has a facing floor at all. So the population an elevated stroke would
# serve is: brush texels whose BEST eye-level facing is poor and whose best ELEVATED facing
# is materially better.
eye_best = np.zeros(NV)
for y in YAWS:
    fac = N @ dtc_of(y, 0.0)
    vis = seen(y, 0.0, args.stroke_facing_min)
    eye_best = np.where(vis & (fac > eye_best), fac, eye_best)
elev_best = np.zeros(NV)
for spec in [s for s in args.elev.split(",") if s.strip()]:
    y, e = [float(x) for x in spec.split(":")]
    fac = N @ dtc_of(y, e)
    vis = seen(y, e, args.stroke_facing_min)
    elev_best = np.where(vis & (fac > elev_best), fac, elev_best)
gain = elev_best - eye_best
print(f"[holes]   best eye-level facing over the brush set: median "
      f"{np.median(eye_best[brush]):.3f}, 10th pct "
      f"{np.percentile(eye_best[brush], 10):.3f}", flush=True)
srv = {}
for glo, flo in ((0.10, 0.60), (0.20, 0.60), (0.20, 0.50)):
    sel = brush & (gain > glo) & (eye_best < flo)
    csz, _ = components(sel) if sel.any() else (np.array([0]), {})
    print(f"[holes]   elevated beats eye-level by >{glo:.2f} where eye-level is <{flo:.2f}: "
          f"{int(sel.sum()):>8,} texels ({sel.sum()/tot*100:5.2f}% of brush), "
          f"largest 3-D component {int(csz[0]):,}", flush=True)
    srv[f"gain>{glo}_eyebest<{flo}"] = {"texels": int(sel.sum()),
                                        "pct_of_brush": float(sel.sum() / tot * 100),
                                        "largest_component": int(csz[0])}

up = brush & (nz > args.up_normal)
usz, uinfo = components(up)
print(f"[holes]   up-facing (nz>{args.up_normal:g}) brush set {int(up.sum()):,} "
      f"({up.sum()/tot*100:.2f}% of brush); largest 3-D component {usz[0]:,}"
      if len(usz) else "[holes]   up-facing brush set EMPTY", flush=True)
out["ruling7_check"] = {
    "_binary_coverage_is_tautological": (
        "reach is the union of seen(yaw,0,%g); the stroke floor is %g, a looser threshold on "
        "the same first-hit test, so eye-level coverage of the brush set is 100%% by "
        "construction and elevated additions are 0 whatever the geometry does. Retained as "
        "the proof that no brush texel is out of eye-level reach; it is not evidence."
        % (args.facing_min, args.stroke_facing_min)),
    "eye_level_cover": base, "eye_level_pct": base / tot * 100,
    "elevated_binary": ev, "elevated_total_add_binary": total_add,
    "eye_best_facing_median": float(np.median(eye_best[brush])),
    "eye_best_facing_p10": float(np.percentile(eye_best[brush], 10)),
    "served_by_elevated": srv,
    "up_facing_brush": int(up.sum()),
    "up_facing_largest_component": int(usz[0]) if len(usz) else 0}

# the named falsifier: up-facing brush INSIDE the wing boxes, reported separately
wing = np.zeros(NV, dtype=bool)
for k, sel in inreg.items():
    if "wing" in k.lower():
        wing |= sel
if wing.any():
    uw = up & wing
    wsz, _ = components(uw)
    print(f"[holes]   THE NAMED FALSIFIER — up-facing brush INSIDE the wing boxes: "
          f"{int(uw.sum()):,} texels, largest 3-D component "
          f"{int(wsz[0]) if len(wsz) else 0:,}", flush=True)
    out["ruling7_check"]["up_facing_in_wing_boxes"] = int(uw.sum())
    out["ruling7_check"]["up_facing_in_wing_largest_component"] = \
        int(wsz[0]) if len(wsz) else 0

if args.save_masks:
    os.makedirs(args.save_masks, exist_ok=True)
    np.save(os.path.join(args.save_masks, "brush_texels.npy"), brush)
    np.save(os.path.join(args.save_masks, "reach_texels.npy"), reach)
    np.save(os.path.join(args.save_masks, "valid_index.npy"), np.where(valid)[0])
    print(f"\n[holes] saved brush/reach texel masks to {args.save_masks}", flush=True)

os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
json.dump(out, open(args.out, "w"), indent=1)
print(f"[holes] wrote {args.out} — DONE (this tool decides nothing)", flush=True)
