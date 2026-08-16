"""E08 Gate 0, half 1 — how much of the figure can a styled reference physically reach?

`project_twins.py` already answers this for two cameras: `reachable` is the texel set a
view passes on facing AND depth, recorded before the edge test, so it is the ceiling a
projection route can reach rather than what it happened to paint. This runs the same
computation over camera LADDERS and reports where it saturates.

Pure geometry. No diffusion, no GPU, no twin images — a camera that does not exist yet
reaches exactly as much surface as one that does.

Camera direction is generalised from project_twins' two hardcoded entries via
texpass_iter's `basis()`: dtc(yaw, el) = normalize([sin y cos e, -cos y cos e, sin e]),
which returns (0,-1,0) at yaw 0 and (0,1,0) at yaw 180 — the hardcoded pair. The tool
ASSERTS that equivalence before reporting anything, so the generalisation is checked
against the shipped code rather than argued for.

  e08_ceiling.py --prep DIR [--sets 2,4,6,8,12] [--elev yaw:el,...] [--cams yaw:el,...]
                 [--restrict-mask blade.npy] [--out-json c.json]

E42 added `--cams`: an explicit camera set that REPLACES the ring entirely (no implicit
yaws(n) flat ring underneath), for measuring a ring that is broken or absent rather than a
flat ring plus extras — which `--elev` cannot express, since it unconditionally ORs its
pairs onto a full flat ring. Absent, output is byte-identical to before the flag existed;
present, it only adds a `custom` row inside each settings block, plus `parsed_elev` /
`parsed_cams` echo fields at the top level so a consumer can verify what was actually
parsed without re-reading argv.

E42 Task 2 also added `--restrict-mask`: an externally-built boolean .npy over this
prep's own NV valid-texel population (e.g. "is this texel on the blade"), reported as a
nested `restricted` block inside the `custom` row only — pct there is of the restricted
population, not of NV. Absent, unused. Shape-checked against NV with a real ANDON (raises;
same-shape-wrong-order is a silent-wrong-number risk, not just a usage error).

Standards compliance: PIN_PER_STEP — every threshold is a parameter and the defaults are
project_twins' own. EXTERNAL_VERIFIER — reports reachable share; it does not say whether
any of it is enough.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--sets", default="2,4,6,8,12")
ap.add_argument("--facing-min", type=float, default=0.45)
ap.add_argument("--head-facing-min", type=float, default=0.18)
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--elev", default="", help="extra elevated cameras, 'yaw:el,yaw:el'")
ap.add_argument("--cams", default="",
                help="explicit camera set, REPLACING the ring entirely - "
                     "'yaw:el,yaw:el,...'. Unlike --elev (which ORs its pairs onto "
                     "an unconditional flat N-ring - see the yaws(n) loop below - and "
                     "so cannot express a ring with no flat component), this computes "
                     "reachability for EXACTLY the listed cameras and nothing else: "
                     "no implicit ring, any per-camera elevation. Absent, output is "
                     "byte-identical to before this flag existed - it only ADDS a "
                     "'custom' row inside settings when non-empty. E42.")
ap.add_argument("--restrict-mask", default="",
                help="path to a .npy boolean array over the SAME NV valid-texel "
                     "population this tool already builds (e.g. 'is this valid "
                     "texel on the blade'), built externally with e08_ceiling's "
                     "own valid-texel convention (mask.npy > 0.5, flattened). "
                     "When given, the 'custom' row (see --cams) ALSO reports "
                     "reachability restricted to this population, as a nested "
                     "'restricted' block. Absent, unused - byte-identical output. "
                     "E42 Task 2.")
ap.add_argument("--out-json")
args = ap.parse_args()

meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
mask = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
lo = np.array(meta["lo"], dtype=np.float64)
hi = np.array(meta["hi"], dtype=np.float64)
valid = mask.reshape(-1)
P = (np.load(os.path.join(args.prep, "pos.npy")).reshape(-1, 3)[valid].astype(np.float64)
     * (hi - lo) + lo) / meta["maxabs"] * 0.5
N = np.load(os.path.join(args.prep, "nor.npy")).reshape(-1, 3)[valid].astype(np.float64) \
    * 2.0 - 1.0
N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
NV = P.shape[0]

# E42 Task 2 - an optional population restriction, e.g. "which of these valid
# texels sit on the blade". This is NOT a new blade definition: the population
# is built externally (see E42's check_face_correspondence.py / build_blade_
# restrict_mask.py) from E40 Seat C's own blade_face_ids, transferred onto
# THIS prep's texels by nearest-face lookup - the geometric definition (which
# crop boxes, which faces) is entirely inherited, unchanged. Shape is checked
# because same-shape-wrong-content (a stale prep, a different valid-texel
# order) would silently produce plausible, wrong, unfalsifiable restricted
# numbers - the same risk class as a misparsed --cams, and the reason this one
# DOES raise (T33's SITES count for this file moves 2 -> 3 with this commit).
restrict_mask = None
if args.restrict_mask:
    restrict_mask = np.load(args.restrict_mask)
    if restrict_mask.shape != (NV,):
        raise AssertionError(
            "ANDON: --restrict-mask shape %r != this prep's valid-texel count "
            "(%d,) - population mismatch, likely a stale or wrong-prep mask"
            % (restrict_mask.shape, NV))
    restrict_mask = restrict_mask.astype(bool)
    print(f"[ceiling] --restrict-mask: {int(restrict_mask.sum()):,} / {NV:,} "
          f"valid texels in scope ({100.0*restrict_mask.mean():.2f}%)", flush=True)

CX0, CY0, CX1, CY1 = meta["crop"]
CROP_RES = meta["crop_res"]
b_std = 0.55
px1k = (P[:, 0] + b_std) / (2 * b_std) * CROP_RES
py1k = (b_std - P[:, 2]) / (2 * b_std) * CROP_RES
headband = ((px1k >= CX0) & (px1k <= CX1) & (py1k >= CY0) & (py1k <= CY1))

m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))
print(f"[ceiling] valid texels {NV:,}   head band {int(headband.sum()):,}", flush=True)


def dtc_of(yaw_d, el_d=0.0):
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    return cd / np.linalg.norm(cd)


# the generalisation must reproduce project_twins' two hardcoded entries exactly
if not (np.allclose(dtc_of(0.0), [0.0, -1.0, 0.0])):
    raise AssertionError("ANDON: yaw 0 is not project_twins' front")
if not (np.allclose(dtc_of(180.0), [0.0, 1.0, 0.0])):
    raise AssertionError("ANDON: yaw 180 is not its back")

_cache = {}


def reach(yaw, el, fmin_body, fmin_head):
    key = (round(yaw, 4), round(el, 4), fmin_body, fmin_head)
    if key in _cache:
        return _cache[key]
    dtc = dtc_of(yaw, el)
    facing = N @ dtc
    fmin = np.where(headband, fmin_head, fmin_body)
    idx = np.where(facing > fmin)[0]
    if not len(idx):
        _cache[key] = np.zeros(NV, dtype=bool)
        return _cache[key]
    org = (P[idx] + N[idx] * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
    t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(dtc.astype(np.float32), org.shape)], axis=1)))["t_hit"].numpy()
    out = np.zeros(NV, dtype=bool)
    out[idx[~np.isfinite(t)]] = True
    _cache[key] = out
    return out


def yaws(n):
    return [i * 360.0 / n for i in range(n)]


extra = []
for spec in [s for s in args.elev.split(",") if s.strip()]:
    y, e = spec.split(":")
    extra.append((float(y), float(e)))

# E42 - a fully explicit camera set, parsed the same permissive way as --elev
# above (plain unpack/float; a malformed spec raises a plain ValueError, same
# as --elev always has - no new ANDON here, so T33's gate census for this file
# does not move). Unlike `extra`, this list REPLACES the ring rather than
# joining it: see the `if custom_cams:` block below, which unions ONLY these
# cameras with no yaws(n) ring underneath.
custom_cams = []
for spec in [s for s in args.cams.split(",") if s.strip()]:
    y, e = spec.split(":")
    custom_cams.append((float(y), float(e)))

# E42 - ECHO what was actually parsed, unconditionally, for both flags. Both
# `extra` and `custom_cams` are parsed permissively (no ANDON) so a malformed
# spec silently drops a pair or misreads one instead of refusing; this run's
# entire output is camera sets, so a silent misparse would produce plausible,
# wrong, unfalsifiable numbers. The echo makes that visible in the transcript
# without adding a gate.
print(f"[ceiling] parsed --elev: {extra}", flush=True)
print(f"[ceiling] parsed --cams: {custom_cams}", flush=True)

# ---- E12 Ruling 6e(i): the captions state the floors they RAN, not the floors
# ---- one subject happened to have when the strings were typed ----------------
# The three captions used to be the literals "body 0.45 / head 0.18",
# "uniform 0.45", "uniform 0.18". When a profile sets head-facing-min equal to
# facing-min — which Ruling 4 does, and which prop.json does — all three tuples
# become the same tuple, so the tool measured one ladder and printed it three
# times under two captions that were simply false. Every caption is now built
# from the values in hand, and identical settings collapse to a single block
# with their names joined, so the output can no longer imply three measurements
# where there is one.
_specs = [("production", args.facing_min, args.head_facing_min),
          ("uniform body-floor", args.facing_min, args.facing_min),
          ("uniform head-floor", args.head_facing_min, args.head_facing_min)]
_names, _order = {}, []
for _n, _fb, _fh in _specs:
    _k = (_fb, _fh)
    if _k not in _names:
        _names[_k] = []
        _order.append(_k)
    _names[_k].append(_n)
SETTINGS = [(" = ".join(_names[k]) + " (body %g / head %g)" % k, k[0], k[1])
            for k in _order]
if len(SETTINGS) < len(_specs):
    print("[ceiling] NOTE: the three threshold settings collapse to %d - the body "
          "and head floors are equal (%g), so what follows is ONE measurement, not "
          "three. [E12 Ruling 6e]" % (len(SETTINGS), args.facing_min), flush=True)

# ---- E14 Ruling 10b: the ray bias against this route's wall thickness --------
# Every reconstruction on this route is a hollow double-walled shell with walls
# ~0.00196 across (Ruling 3, measured three independent ways). A near-face ray
# origin displaced further than that starts BEHIND its own wall, which reads as
# reach that geometry does not have: measured +0.97 points at eight cameras on
# the sword (51.33% at the shipped 3e-3 against 50.36-50.43% at 2e-4 to 5e-4,
# converged by 5e-4). The shipped default is deliberately left alone so the
# number stays comparable with every subject measured before it; the warning
# makes the caveat travel with the output instead of living in a ruling.
WALL_FLOOR = 0.00196
if args.bias > WALL_FLOOR:
    print("[ceiling] WARNING: --bias %g EXCEEDS this route's ~%g wall floor - "
          "near-face ray origins displace through their own wall and the reach is "
          "overstated (+0.97 points at N8 on the sword). The value is comparable "
          "with prior subjects and is NOT changed here; read every percentage "
          "below with this caveat. [E14 Ruling 10b]" % (args.bias, WALL_FLOOR),
          flush=True)
sets = [int(s) for s in args.sets.split(",")]
out = {"valid_texels": int(NV), "head_band": int(headband.sum()), "settings": {}}
# E42 - the echoed, parsed camera lists ride the JSON payload too, always
# present (even empty), so a consumer can verify what was actually measured
# without re-parsing the argv string itself.
out["parsed_elev"] = [{"yaw": y, "el": e} for y, e in extra]
out["parsed_cams"] = [{"yaw": y, "el": e} for y, e in custom_cams]
if restrict_mask is not None:
    out["restrict_mask"] = {"path": os.path.abspath(args.restrict_mask),
                            "in_scope_texels": int(restrict_mask.sum())}
# `settings` is keyed by the display label, and the labels move when the floors do
# — which is the whole point of the 6e(i) repair, but it means a consumer must not
# select a block by its caption. `e14_atlas_anatomy` did exactly that
# (`cj["settings"]["uniform 0.45"]`), which is the same defect one tool over: the
# caption was a PROXY for "the configuration whose floors are both 0.45", and the
# floors ARE the configuration. This index lets a consumer select on the property.
out["settings_index"] = [{"label": label, "facing_min": fb, "head_facing_min": fh,
                          "aliases": list(_names[(fb, fh)])}
                         for label, fb, fh in SETTINGS]

for label, fb, fh in SETTINGS:
    print(f"\n[ceiling] {label}")
    rows = {}
    for n in sets:
        R = np.zeros(NV, dtype=bool)
        for y in yaws(n):
            R |= reach(y, 0.0, fb, fh)
        rows[f"N{n}"] = {"cameras": n, "reachable": int(R.sum()),
                         "pct": round(float(R.mean() * 100), 2)}
        print(f"[ceiling]   {n:>3} cameras (equatorial)   {int(R.sum()):>9,}  "
              f"{R.mean()*100:5.2f}% of valid")
    if extra:
        for n in sets:
            if n < 8:
                continue
            R = np.zeros(NV, dtype=bool)
            for y in yaws(n):
                R |= reach(y, 0.0, fb, fh)
            for y, e in extra:
                R |= reach(y, e, fb, fh)
            rows[f"N{n}+{len(extra)}el"] = {"cameras": n + len(extra),
                                            "reachable": int(R.sum()),
                                            "pct": round(float(R.mean() * 100), 2)}
            print(f"[ceiling]   {n:>3}+{len(extra)} elevated       "
                  f"{int(R.sum()):>9,}  {R.mean()*100:5.2f}% of valid")
    if custom_cams:
        # E42 - a fully explicit camera set: UNION of exactly these cameras,
        # no yaws(n) ring underneath. This is the arm this flag exists for -
        # a ring that is broken (or not a ring at all) rather than a flat
        # ring plus extras.
        R = np.zeros(NV, dtype=bool)
        for y, e in custom_cams:
            R |= reach(y, e, fb, fh)
        rows["custom"] = {"cameras": len(custom_cams), "reachable": int(R.sum()),
                          "pct": round(float(R.mean() * 100), 2),
                          "cams": [{"yaw": y, "el": e} for y, e in custom_cams]}
        print(f"[ceiling]   custom {len(custom_cams):>3} cams          "
              f"{int(R.sum()):>9,}  {R.mean()*100:5.2f}% of valid  "
              f"{[(y, e) for y, e in custom_cams]}")
        if restrict_mask is not None:
            # E42 Task 2 - the SAME per-texel reachability R, intersected with
            # an externally-supplied population (e.g. blade texels). pct here
            # is of the RESTRICTED population, not of NV - a different
            # denominator, named explicitly so it cannot be misread as the
            # whole-figure pct two lines above.
            Rr = R & restrict_mask
            in_scope = int(restrict_mask.sum())
            rows["custom"]["restricted"] = {
                "in_scope_texels": in_scope, "reachable": int(Rr.sum()),
                "pct_of_restricted": round(float(Rr.sum() / max(in_scope, 1) * 100), 2)}
            print(f"[ceiling]   custom {len(custom_cams):>3} cams  RESTRICTED   "
                  f"{int(Rr.sum()):>9,} / {in_scope:>9,}  "
                  f"{100.0*Rr.sum()/max(in_scope,1):5.2f}% of restricted scope")
    out["settings"][label] = rows

# what a camera adds on its own, in production settings — is the gain the diagonals?
print(f"\n[ceiling] marginal gain per camera, production thresholds, added in "
      f"turnaround order:")
R = np.zeros(NV, dtype=bool)
order = [0.0, 180.0, 90.0, 270.0, 45.0, 135.0, 225.0, 315.0]
marg = {}
for i, y in enumerate(order, start=1):
    before = int(R.sum())
    R |= reach(y, 0.0, args.facing_min, args.head_facing_min)
    marg[f"yaw{int(y)}"] = {"after": int(R.sum()), "added": int(R.sum()) - before}
    print(f"[ceiling]   +yaw {int(y):>3}  -> {int(R.sum()):>9,}  "
          f"{R.mean()*100:5.2f}%   (+{int(R.sum())-before:,})")
out["marginal"] = marg

# the two twins, exactly as shipped — and whether hold-one-out has anything to compare
rf = reach(0.0, 0.0, args.facing_min, args.head_facing_min)
rb = reach(180.0, 0.0, args.facing_min, args.head_facing_min)
ov = int((rf & rb).sum())
out["twin_front_reachable"] = int(rf.sum())
out["twin_back_reachable"] = int(rb.sum())
out["twin_overlap"] = ov
print(f"\n[ceiling] the two shipped twins: front {int(rf.sum()):,}  back {int(rb.sum()):,}"
      f"  union {int((rf|rb).sum()):,} ({(rf|rb).mean()*100:.2f}%)")
# E12 Ruling 6e(ii). The old line called this "the population a hold-one-out
# comparison at N=2 would have", which cannot be true: opposed cameras test
# dot(n,d) and dot(n,-d), jointly passable only at a floor <= 0, so at any
# positive floor the overlap is zero by construction and was measured zero at
# 0.45, 0.18 and 0.00 alike. A check that cannot fail is not a check; it is
# repaired rather than deleted so the structural fact stays visible.
_floor_min = min(args.facing_min, args.head_facing_min)
if _floor_min > 0:
    print(f"[ceiling] front-back OVERLAP = {ov:,} texels - STRUCTURALLY zero at any "
          f"positive floor (lowest floor here {_floor_min:g}): opposed cameras test "
          f"dot(n,d) and dot(n,-d), jointly passable only at a floor <= 0. A "
          f"hold-one-out comparison at N=2 has NO population on this route. "
          f"[E12 Ruling 6e]")
else:
    print(f"[ceiling] front-back OVERLAP = {ov:,} texels - the population a "
          f"hold-one-out comparison at N=2 would have (the lowest floor is "
          f"{_floor_min:g}, so this one CAN be non-zero)")

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
    print(f"\n[ceiling] wrote {args.out_json}")
