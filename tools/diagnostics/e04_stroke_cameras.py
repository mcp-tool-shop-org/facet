"""E04 stage 2 - STROKE cameras, derived from the hole map the way Task 4a derived the
deck cameras (E04 Ruling 23 section 2).

WHAT A STROKE CAN ACTUALLY COMMIT, not what a camera can see. Task 4a scored candidate
camera sets by first-hit FACE AREA, which is the right instrument for "can a camera look
into this deck" and the wrong one for "how many hole texels would this stroke write". A
stroke writes a texel only if it survives, in this order, what texpass_iter.py's commit
path tests:

  1. facing = N . dtc > --facing-min              (texpass_iter --facing-min, 0.25)
  2. unoccluded along dtc                          (the visibility raycast)
  3. NOT thin-withheld                             (emit: hm = hm & ~thin, commit: injob)
  4. at least --edge-dist px from the figure edge  (commit's distance transform)

Steps 3 and 4 are the two that a pure reach calculation misses, and on a subject with 512
rigging shells they are not small. Both are modelled here on emit's own image grid, at
emit's own frame, so the numbers are the tool's arithmetic rather than an analogue of it.

TWO STATED APPROXIMATIONS, because a number whose error direction is unknown is not a
measurement:

  * step 4 runs against emit's GEOMETRY hit mask. The shipped guard runs against the brush
    output's KEYED mask intersected with that hit mask, which is a subset - so a smaller
    figure, a nearer boundary, and fewer survivors. This tool's step-4 survivor set is an
    UPPER BOUND.
  * the 9 px job-mask dilation is omitted. It only ever admits more, so it too makes this
    an upper bound rather than an optimistic guess in an unknown direction.

A CAMERA SET IS A UNION (Task 4a's own correction, kept). Greedy marginal coverage is
computed against a base of {what stage 1 painted} UNION {what the ruled deck pair will
paint}, because a camera added to a set that already reaches a surface buys nothing.

  e04_stroke_cameras.py --prep DIR --styled stage1_styled_mask.npy --glb prep_uv.glb
                        --out DIR [--facing-min 0.25] [--thin-extent 0.01]
                        [--edge-dist 4.0] [--aspect 1072,1024] [--fit-axis width]

Standards compliance: PIN_PER_STEP - every threshold is a flag and every default is the
value ship.json carries for the tool it comes from; the frame, fit-axis and margin are
arguments, not literals. ANDON_AUTHORITY - the inherited stage-1 figures are recomputed
from the artifacts and any disagreement is printed as a MISMATCH row rather than absorbed;
no threshold is emitted and no set is chosen here. EXTERNAL_VERIFIER - this reports
coverage ladders; which prefix to adopt is a ruling, and the tool says so.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from scipy.ndimage import distance_transform_edt

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--styled", required=True, help="stage 1 styled_mask.npy (RES x RES bool)")
ap.add_argument("--glb", default=None, help="emit's scene GLB; defaults to prep_uv.glb")
ap.add_argument("--out", required=True)
ap.add_argument("--facing-min", type=float, default=0.25,
                help="ship.json texpass_iter.facing-min - commit acceptance")
ap.add_argument("--thin-extent", type=float, default=0.01,
                help="ship.json texpass_iter.thin-extent - emit withholds below this")
ap.add_argument("--edge-dist", type=float, default=4.0,
                help="ship.json texpass_iter.edge-dist - commit's edge trim, in px")
ap.add_argument("--aspect", default="1072,1024", help="ship.json emit frame")
ap.add_argument("--fit-axis", default="width", choices=["height", "width"])
ap.add_argument("--margin", type=float, default=1.204)
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--deck-normal", type=float, default=0.5,
                help="|nz| above this is deck (nz>0) or hull bottom (nz<0); the stage-1 "
                     "report's own class boundary")
ap.add_argument("--waterline-frac", type=float, default=0.07,
                help="lowest fraction of the mesh height = the hull foot / waterline rim")
ap.add_argument("--deck-cams", default="0:40,180:40",
                help="RULED, not derived - Task 4a's elevated pair (E04 Ruling 23 s1)")
ap.add_argument("--side-cams", default=",".join("%d:0" % y for y in range(0, 360, 15)),
                help="side-stroke CANDIDATES. Default is the 24-yaw eye-level grid, which "
                     "is exactly the subset of ship.json's cull_unseen.production superset "
                     "at elevation 0. A candidate outside that superset is a ruling.")
ap.add_argument("--extra-cams", default="0:55,180:55,90:40,270:40,0:20,90:20,180:20,270:20",
                help="reported as DIAGNOSTICS only, never entered into the greedy")
ap.add_argument("--profile", default="profiles/ship.json",
                help="read cull_unseen.production from here so the superset membership "
                     "column is the profile's own list, not a transcription of it")
ap.add_argument("--picks", type=int, default=8, help="how far to run the greedy ladder")
args = ap.parse_args()
os.makedirs(args.out, exist_ok=True)
W, H = (int(x) for x in args.aspect.split(","))
D = 2.0                                   # texpass_iter's emit plane distance

# THE CULL SUPERSET IS A CONSTRAINT ON THE CANDIDATE LIST, not a footnote (E06 rule: the
# exterior-visibility superset must COVER every production camera). A stroke camera outside
# it would need the superset widened, which is a ruling. Read from the profile rather than
# retyped, so the column cannot drift from the file it claims to describe.
SUPERSET = set()
try:
    _pf = json.load(open(args.profile, encoding="utf-8"))
    for _s in _pf["tools"]["cull_unseen.py"]["production"]["value"].split(";"):
        _y, _e = _s.split(",")
        SUPERSET.add((float(_y), float(_e)))
    print("[stroke] cull superset from %s: %d cameras" % (args.profile, len(SUPERSET)),
          flush=True)
except Exception as exc:                                   # reported, never silent
    print("[stroke] WARNING: could not read the superset from %s (%s) - membership "
          "columns read EMPTY, not False" % (args.profile, exc), flush=True)
    SUPERSET = None

# ------------------------------------------------------------------ the prep, as loaded
meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
mask = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
valid = mask.reshape(-1)
lo = np.array(meta["lo"], dtype=np.float64)
hi = np.array(meta["hi"], dtype=np.float64)
P = (np.load(os.path.join(args.prep, "pos.npy")).reshape(-1, 3)[valid].astype(np.float64)
     * (hi - lo) + lo) / meta["maxabs"] * 0.5
N = np.load(os.path.join(args.prep, "nor.npy")).reshape(-1, 3)[valid].astype(np.float64) \
    * 2.0 - 1.0
N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
NV = P.shape[0]

styled = np.load(args.styled)
assert styled.shape == (RES, RES), "ANDON: styled mask is %s, prep says %d" % (
    styled.shape, RES)
styled_v = styled.reshape(-1)[valid]
hole = ~styled_v

nz = N[:, 2]
cls_up = nz > args.deck_normal
cls_dn = nz < -args.deck_normal
cls_side = ~(cls_up | cls_dn)
z = P[:, 2]
zlo, zhi = float(z.min()), float(z.max())
foot = z <= zlo + args.waterline_frac * (zhi - zlo)


def pct(a, b):
    return 100.0 * a / b if b else 0.0


print("[stroke] valid %d   styled %d (%.2f%%)   holes %d (%.2f%%)"
      % (NV, int(styled_v.sum()), pct(styled_v.sum(), NV), int(hole.sum()),
         pct(hole.sum(), NV)), flush=True)
print("[stroke] --- inherited stage-1 figures, RECOMPUTED from the artifacts ---",
      flush=True)
INHERIT = [("valid texels", NV, 3111817),
           ("styled texels", int(styled_v.sum()), 1147959),
           ("holes", int(hole.sum()), 1963858),
           ("upward-facing texels", int(cls_up.sum()), 653140),
           ("upward-facing holes", int((cls_up & hole).sum()), 489889),
           ("downward-facing holes", int((cls_dn & hole).sum()), 515329),
           ("side-facing holes", int((cls_side & hole).sum()), 958640),
           ("hull-foot texels", int(foot.sum()), 117682)]
mismatch = 0
for name, got, want in INHERIT:
    flag = "ok" if got == want else "MISMATCH"
    if got != want:
        mismatch += 1
    print("[stroke]   %-24s %10d   report says %10d   %s" % (name, got, want, flag),
          flush=True)
print("[stroke]   deck styled %.2f%%  (report 24.99)   other styled %.2f%%  (report 40.05)"
      % (pct((cls_up & styled_v).sum(), cls_up.sum()),
         pct((~cls_up & styled_v).sum(), (~cls_up).sum())), flush=True)
print("[stroke]   hull-foot styled %.2f%%  (report 19.44)"
      % pct((foot & styled_v).sum(), foot.sum()), flush=True)
print("[stroke]   %d MISMATCH row(s)" % mismatch, flush=True)

# ------------------------------------------------------------------------ the ray scene
m = trimesh.load(args.glb or os.path.join(args.prep, "prep_uv.glb"), force="mesh",
                 process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))
blo, bhi = v.min(axis=0), v.max(axis=0)
bmid = (blo + bhi) / 2
if args.fit_axis == "height":
    v_ext = (bhi[2] - blo[2]) * args.margin
    h_ext = v_ext * (W / H)
else:
    h_ext = max(bhi[0] - blo[0], bhi[1] - blo[1]) * args.margin
    v_ext = h_ext * (H / W)
print("[stroke] frame %dx%d  fit-axis %s  h_ext %.5f  v_ext %.5f"
      % (W, H, args.fit_axis, h_ext, v_ext), flush=True)


def basis(yaw_d, el_d):
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    look = -cd / np.linalg.norm(cd)
    up0 = np.array([0.0, 0.0, 1.0])
    right = np.cross(look, up0)
    right /= np.linalg.norm(right) + 1e-12
    up = np.cross(right, look)
    return cd / np.linalg.norm(cd), look, right, up / (np.linalg.norm(up) + 1e-12)


# project_twins' two hardcoded camera axes, reproduced - the same assert e08_ceiling makes
assert np.allclose(basis(0.0, 0.0)[0], [0.0, -1.0, 0.0]), "ANDON: yaw 0 is not front"
assert np.allclose(basis(180.0, 0.0)[0], [0.0, 1.0, 0.0]), "ANDON: yaw 180 is not back"


def bilin(img, x, y):
    Hh, Ww = img.shape[:2]
    x = np.clip(x, 0.0, Ww - 1.001)
    y = np.clip(y, 0.0, Hh - 1.001)
    x0, y0 = x.astype(np.int64), y.astype(np.int64)
    fx, fy = x - x0, y - y0
    return (img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy)
            + img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy)


_cache = {}


def stroke_reach(yaw, el):
    """Boolean over all valid texels: would a stroke from here COMMIT this texel?

    Returns (final, stages) where stages counts the funnel over HOLE texels only."""
    key = (round(yaw, 3), round(el, 3))
    if key in _cache:
        return _cache[key]
    dtc, look, right, up = basis(yaw, el)
    # --- emit's own image grid: hit, thin, and the distance field commit erodes with
    xs = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
    ys = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
    gx, gy = np.meshgrid(xs, ys)
    org = (bmid[None, None, :] + gx[..., None] * right[None, None, :]
           + gy[..., None] * up[None, None, :] - look[None, None, :] * D)
    aF = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
    tF = aF["t_hit"].numpy().reshape(H, W)
    hit = np.isfinite(tF)
    aB = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org + look[None, None, :] * (2 * D), np.broadcast_to(-look, org.shape)],
        axis=-1).reshape(-1, 6).astype(np.float32)))
    tB = aB["t_hit"].numpy().reshape(H, W)
    both = hit & np.isfinite(tB)
    ext = np.full((H, W), np.inf, dtype=np.float64)
    ext[both] = 2 * D - tF[both] - tB[both]
    thin = (ext < args.thin_extent) & hit
    job = ((hit & ~thin)).astype(np.float32)
    dist = distance_transform_edt(hit).astype(np.float32)
    # --- the texel funnel, over HOLES only (a stroke writes nothing else)
    hidx = np.where(hole)[0]
    facing = N[hidx] @ dtc
    k1 = facing > args.facing_min
    i1 = hidx[k1]
    org2 = (P[i1] + N[i1] * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
    t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org2, np.broadcast_to(dtc.astype(np.float32), org2.shape)], axis=1)))
    i2 = i1[~np.isfinite(t["t_hit"].numpy())]
    px = ((P[i2] - bmid) @ right / h_ext + 0.5) * W - 0.5
    py = (0.5 - (P[i2] - bmid) @ up / v_ext) * H - 0.5
    i3 = i2[bilin(job, px, py) > 0.5]
    px = ((P[i3] - bmid) @ right / h_ext + 0.5) * W - 0.5
    py = (0.5 - (P[i3] - bmid) @ up / v_ext) * H - 0.5
    i4 = i3[bilin(dist, px, py) >= args.edge_dist]
    out = np.zeros(NV, dtype=bool)
    out[i4] = True
    stages = {"facing": int(len(i1)), "visible": int(len(i2)),
              "after_thin": int(len(i3)), "after_edge": int(len(i4)),
              "thin_cost": int(len(i2) - len(i3)), "edge_cost": int(len(i3) - len(i4)),
              "thin_cost_pct": round(pct(len(i2) - len(i3), max(len(i2), 1)), 2),
              "edge_cost_pct": round(pct(len(i3) - len(i4), max(len(i3), 1)), 2),
              "figure_px": int(hit.sum())}
    # how much of what this camera can SEE at all is already painted - the spiral's operand
    org3 = (P + N * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
    seenf = (N @ dtc) > args.facing_min
    j = np.where(seenf)[0]
    tv = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org3[j], np.broadcast_to(dtc.astype(np.float32), org3[j].shape)], axis=1)))
    vis = j[~np.isfinite(tv["t_hit"].numpy())]
    stages["visible_valid"] = int(len(vis))
    stages["visible_styled"] = int(styled_v[vis].sum())
    stages["visible_styled_pct"] = round(pct(styled_v[vis].sum(), max(len(vis), 1)), 2)
    _cache[key] = (out, stages)
    return _cache[key]


# ------------------------------------------------- 0. does this ray setup reproduce E04's
# pre-registered ceiling? Written because a new tool's geometry is an inherited claim about
# bias, normal offset, normalisation and camera axes until something it did not compute
# agrees with it. 1,329,359 came from e08_ceiling.py on a different day and project_twins
# printed the same 42.7% from the inside.
def reach_valid(yaw, el, fmin):
    dtc = basis(yaw, el)[0]
    j = np.where((N @ dtc) > fmin)[0]
    org = (P[j] + N[j] * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
    t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(dtc.astype(np.float32), org.shape)], axis=1)))["t_hit"].numpy()
    out = np.zeros(NV, dtype=bool)
    out[j[~np.isfinite(t)]] = True
    return out


_ceil = np.zeros(NV, dtype=bool)
for _y in range(0, 360, 45):
    _ceil |= reach_valid(float(_y), 0.0, 0.45)
print("[stroke] ANCHOR: eight eye-level yaws at facing 0.45 reach %d (%.2f%%); "
      "e08_ceiling pre-registered 1329359 (42.72%%) -> %s"
      % (int(_ceil.sum()), pct(_ceil.sum(), NV),
         "MATCH" if int(_ceil.sum()) == 1329359 else "DIFFERS"), flush=True)


def parse_cams(s):
    out = []
    for spec in [x for x in s.split(",") if x.strip()]:
        y, e = spec.split(":")
        out.append((float(y), float(e)))
    return out


def label(y, e):
    return "y%+04d_e%+03d" % (int(y), int(e))


def profile_of(sel, base=None):
    """Counts for a texel selection, by class and region."""
    n = int(sel.sum())
    return {"texels": n,
            "side": int((sel & cls_side).sum()), "deck": int((sel & cls_up).sum()),
            "bottom": int((sel & cls_dn).sum()), "foot": int((sel & foot).sum())}


# --------------------------------------------------------------- 1. the RULED deck pair
print("\n[stroke] === 1. DECK strokes: RULED (Task 4a's pair), not derived ===", flush=True)
deck_cams = parse_cams(args.deck_cams)
deck_union = np.zeros(NV, dtype=bool)
deck_rows = []
for y, e in deck_cams:
    r, st = stroke_reach(y, e)
    before = int(deck_union.sum())
    deck_union |= r
    st.update({"cam": label(y, e), "yaw": y, "el": e, "commit": int(r.sum()),
               "marginal": int(deck_union.sum()) - before})
    st.update(profile_of(r))
    deck_rows.append(st)
    print("[stroke]   %s  commit %8d  (+%8d new)  deck %7d  side %7d  bottom %7d  foot %6d"
          % (st["cam"], st["commit"], st["marginal"], st["deck"], st["side"],
             st["bottom"], st["foot"]), flush=True)
    print("[stroke]        funnel  facing %8d -> visible %8d -> thin %8d (-%.2f%%) "
          "-> edge %8d (-%.2f%%)"
          % (st["facing"], st["visible"], st["after_thin"], st["thin_cost_pct"],
             st["after_edge"], st["edge_cost_pct"]), flush=True)
dk_h = int((cls_up & hole).sum())
dk_got = int((deck_union & cls_up).sum())
print("[stroke]   deck pair union %d texels; upward-facing holes closed %d of %d = %.2f%%, "
      "REMAINING %.2f%%" % (int(deck_union.sum()), dk_got, dk_h, pct(dk_got, dk_h),
                            100 - pct(dk_got, dk_h)), flush=True)
deck_after = int(((cls_up & styled_v) | (cls_up & deck_union)).sum())
print("[stroke]   deck styled after the pair: %.2f%% (was %.2f%%)"
      % (pct(deck_after, cls_up.sum()), pct((cls_up & styled_v).sum(), cls_up.sum())),
      flush=True)

# ------------------------------------------------- 2. SIDE strokes, greedy from the union
print("\n[stroke] === 2. SIDE strokes: greedy marginal coverage on side-class holes ===",
      flush=True)
base = styled_v | deck_union
side_cams = parse_cams(args.side_cams)
if SUPERSET is not None:
    outside = [label(y, e) for y, e in (side_cams + deck_cams)
               if (float(y), float(e)) not in SUPERSET]
    print("[stroke]   candidates outside the cull superset: %s"
          % (", ".join(outside) if outside else "NONE - every candidate is covered"),
          flush=True)
stand = []
for y, e in side_cams:
    r, st = stroke_reach(y, e)
    row = {"cam": label(y, e), "yaw": y, "el": e, "commit": int(r.sum()),
           "side_new_vs_base": int((r & ~base & cls_side).sum()),
           "all_new_vs_base": int((r & ~base).sum()),
           "foot_new_vs_base": int((r & ~base & foot).sum())}
    row.update({k: st[k] for k in ("thin_cost_pct", "edge_cost_pct", "visible_styled_pct",
                                   "visible_valid", "figure_px")})
    stand.append(row)
    print("[stroke]   standalone %s  side-new %8d  all-new %8d  foot-new %6d  "
          "thin -%5.2f%%  edge -%5.2f%%  already-painted %5.2f%%"
          % (row["cam"], row["side_new_vs_base"], row["all_new_vs_base"],
             row["foot_new_vs_base"], row["thin_cost_pct"], row["edge_cost_pct"],
             row["visible_styled_pct"]), flush=True)

cov = base.copy()
side_h = int((cls_side & hole).sum())
foot_h = int((foot & hole).sum())
ladder = []
chosen = []
print("\n[stroke]   greedy ladder (base = stage1 UNION deck pair):", flush=True)
print("[stroke]   %-4s %-14s %10s %10s %10s %10s %9s" % (
    "pick", "camera", "side-new", "all-new", "foot-new", "deck-new", "cum side%"),
    flush=True)
for k in range(args.picks):
    best, best_g = None, -1
    for y, e in side_cams:
        if (y, e) in chosen:
            continue
        r, _ = stroke_reach(y, e)
        g = int((r & ~cov & cls_side).sum())
        if g > best_g:
            best, best_g = (y, e), g
    if best is None:
        break
    r, st = stroke_reach(*best)
    gain_side = int((r & ~cov & cls_side).sum())
    gain_all = int((r & ~cov).sum())
    gain_foot = int((r & ~cov & foot).sum())
    gain_deck = int((r & ~cov & cls_up).sum())
    cov |= r
    chosen.append(best)
    cum_side = int((cov & ~styled_v & cls_side & hole).sum())
    row = {"pick": k + 1, "cam": label(*best), "yaw": best[0], "el": best[1],
           "side_new": gain_side, "all_new": gain_all, "foot_new": gain_foot,
           "deck_new": gain_deck,
           "cum_side_holes_closed": cum_side,
           "cum_side_pct": round(pct(cum_side, side_h), 2),
           "cum_foot_styled_pct": round(pct(int((foot & (styled_v | cov)).sum()),
                                            int(foot.sum())), 2),
           "cum_all_styled_pct": round(pct(int((styled_v | cov).sum()), NV), 2)}
    ladder.append(row)
    print("[stroke]   %-4d %-14s %10d %10d %10d %10d %8.2f%%"
          % (row["pick"], row["cam"], gain_side, gain_all, gain_foot, gain_deck,
             row["cum_side_pct"]), flush=True)

print("\n[stroke]   cumulative, per ladder prefix:", flush=True)
print("[stroke]   %-4s %-14s %12s %12s %12s" % ("n", "last camera", "styled/valid",
                                                "hull-foot", "side holes closed"),
      flush=True)
for row in ladder:
    print("[stroke]   %-4d %-14s %11.2f%% %11.2f%% %11.2f%%"
          % (row["pick"], row["cam"], row["cum_all_styled_pct"],
             row["cum_foot_styled_pct"], row["cum_side_pct"]), flush=True)

# ------------------------------------------------------------------- 3. the hull bottom
bt_h = int((cls_dn & hole).sum())
print("\n[stroke] === 3. HULL BOTTOM: no strokes (Ruling 23 s3). What that leaves ===",
      flush=True)
print("[stroke]   downward-facing holes %d; closed incidentally by the proposed set: %d "
      "(%.2f%%); to dilation: %d"
      % (bt_h, int((cov & cls_dn & hole).sum()), pct(int((cov & cls_dn & hole).sum()), bt_h),
         bt_h - int((cov & cls_dn & hole).sum())), flush=True)

# ------------------------------------------------------------------------ 4. diagnostics
print("\n[stroke] === 4. DIAGNOSTIC candidates (reported, never entered in the greedy) ===",
      flush=True)
diag = []
for y, e in parse_cams(args.extra_cams):
    r, st = stroke_reach(y, e)
    d = {"cam": label(y, e), "yaw": y, "el": e,
         "side_new_vs_base": int((r & ~base & cls_side).sum()),
         "all_new_vs_final": int((r & ~cov).sum()),
         "in_production_superset": (None if SUPERSET is None
                                    else ((float(y), float(e)) in SUPERSET))}
    diag.append(d)
    print("[stroke]   %s  side-new-vs-base %8d  all-new-vs-FINAL %8d  in-superset %s"
          % (d["cam"], d["side_new_vs_base"], d["all_new_vs_final"],
             d["in_production_superset"]), flush=True)

# ---------------------------------------------------------------------- 5. spiral operand
print("\n[stroke] === 5. SPIRAL operand: how much each chosen camera already sees painted "
      "(stage 1 only) ===", flush=True)
spiral = []
for y, e in deck_cams + chosen:
    _, st = stroke_reach(y, e)
    spiral.append({"cam": label(y, e), "yaw": y, "el": e,
                   "visible_valid": st["visible_valid"],
                   "visible_styled": st["visible_styled"],
                   "visible_styled_pct": st["visible_styled_pct"]})
for s in sorted(spiral, key=lambda r: -r["visible_styled_pct"]):
    print("[stroke]   %-14s visible %8d  already styled %8d  = %6.2f%%"
          % (s["cam"], s["visible_valid"], s["visible_styled"], s["visible_styled_pct"]),
          flush=True)

# ---------------------------------------------------------- 6. the spiral, ORDER-AWARE
# The operand above is standalone. What the rule actually cares about is how much of a
# camera's surface is painted AT ITS TURN, which depends on the order - so candidate orders
# are simulated and scored on their WORST-anchored stroke. E08's failure case was one
# camera opening at 95% hole and composing a plaited belt; the quantity to protect is the
# minimum, not the mean.
print("\n[stroke] === 6. SPIRAL ORDER: anchoring AT TURN, simulated per candidate order ===",
      flush=True)
ALL = deck_cams + chosen


def anchor_run(order):
    acc = styled_v.copy()
    rows = []
    for y, e in order:
        r, _ = stroke_reach(y, e)
        dtc = basis(y, e)[0]
        j = np.where((N @ dtc) > args.facing_min)[0]
        org3 = (P[j] + N[j] * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
        tv = rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [org3, np.broadcast_to(dtc.astype(np.float32), org3.shape)], axis=1)))
        vis = j[~np.isfinite(tv["t_hit"].numpy())]
        a = pct(acc[vis].sum(), max(len(vis), 1))
        rows.append({"cam": label(y, e), "anchor_pct": round(a, 2)})
        acc |= r
    return rows


def ring_from(seed, cams):
    """single sweep in +yaw from the seed - each next camera adjacent in the yaw ring"""
    eye = sorted([c for c in cams if c[1] == 0.0], key=lambda c: c[0])
    i = eye.index(seed)
    return [eye[(i + k) % len(eye)] for k in range(len(eye))]


anchor_std = {label(y, e): stroke_reach(y, e)[1]["visible_styled_pct"] for y, e in ALL}
seed = max([c for c in chosen], key=lambda c: anchor_std[label(*c)])
ORDERS = {
    "A greedy-anchor (pick the best-anchored remaining, each turn)": None,
    "B ring sweep from the best-anchored, deck pair last": ring_from(seed, chosen) + deck_cams,
    "C coverage-greedy order (section 2's own order), deck pair first": deck_cams + chosen,
    "D deck pair first, then the ring sweep": deck_cams + ring_from(seed, chosen),
}
# A is built by simulation rather than declared
acc = styled_v.copy()
orderA = []
rem = list(ALL)
while rem:
    best, ba = None, -1.0
    for y, e in rem:
        dtc = basis(y, e)[0]
        j = np.where((N @ dtc) > args.facing_min)[0]
        org3 = (P[j] + N[j] * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
        tv = rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [org3, np.broadcast_to(dtc.astype(np.float32), org3.shape)], axis=1)))
        vis = j[~np.isfinite(tv["t_hit"].numpy())]
        a = pct(acc[vis].sum(), max(len(vis), 1))
        if a > ba:
            best, ba = (y, e), a
    orderA.append(best)
    rem.remove(best)
    acc |= stroke_reach(*best)[0]
ORDERS["A greedy-anchor (pick the best-anchored remaining, each turn)"] = orderA

orders_out = {}
for nm, od in ORDERS.items():
    rows = anchor_run(od)
    mn = min(r["anchor_pct"] for r in rows)
    mean = sum(r["anchor_pct"] for r in rows) / len(rows)
    orders_out[nm] = {"order": [r["cam"] for r in rows], "per_stroke": rows,
                      "min_anchor_pct": round(mn, 2), "mean_anchor_pct": round(mean, 2)}
    print("[stroke]   %s" % nm, flush=True)
    print("[stroke]     %s" % " -> ".join(r["cam"] for r in rows), flush=True)
    print("[stroke]     anchoring %s" % "  ".join("%.1f" % r["anchor_pct"] for r in rows),
          flush=True)
    print("[stroke]     MIN %.2f%%   mean %.2f%%" % (mn, mean), flush=True)

# ------------------------------------------------------- 7. provenance mix, per prefix
print("\n[stroke] === 7. PROVENANCE MIX per ladder prefix (against the 42.72%% ceiling) ===",
      flush=True)
mix = []
for n in range(0, len(ladder) + 1):
    c = base.copy()
    for k in range(n):
        c |= stroke_reach(ladder[k]["yaw"], ladder[k]["el"])[0]
    ref = int(styled_v.sum())
    brush = int((c & ~styled_v).sum())
    dil = NV - ref - brush
    mix.append({"side_strokes": n, "strokes_total": 2 + n,
                "reference_pct": round(pct(ref, NV), 2),
                "brush_pct": round(pct(brush, NV), 2),
                "dilation_pct": round(pct(dil, NV), 2)})
    print("[stroke]   %2d side strokes (%2d total): reference %5.2f%%  brush %5.2f%%  "
          "dilation %5.2f%%   [character: 68.8 / 4.2 / 27.0]"
          % (n, 2 + n, mix[-1]["reference_pct"], mix[-1]["brush_pct"],
             mix[-1]["dilation_pct"]), flush=True)

# ------------------------------------------------- 8. WHY the ladder is flat: decompose
# the residual. A flat ladder has two very different explanations - the remaining holes are
# obliquity holes some better-angled camera would take (so more cameras help), or they are
# occlusion/thin/edge holes no eye-level camera can take at all (so they cannot). Asserting
# either without measuring it is exactly the move this repo keeps paying for, so the funnel
# is unioned across EVERY candidate and the residual is attributed to the stage that
# rejected it everywhere.
print("\n[stroke] === 8. RESIDUAL side-class holes, attributed across ALL %d eye-level "
      "candidates ===" % len(side_cams), flush=True)
u_face = np.zeros(NV, dtype=bool)
u_vis = np.zeros(NV, dtype=bool)
u_thin = np.zeros(NV, dtype=bool)
u_edge = np.zeros(NV, dtype=bool)
for y, e in side_cams + deck_cams:
    dtc, look, right, up = basis(y, e)
    xs = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
    ys = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
    gx, gy = np.meshgrid(xs, ys)
    org = (bmid[None, None, :] + gx[..., None] * right[None, None, :]
           + gy[..., None] * up[None, None, :] - look[None, None, :] * D)
    aF = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
    tF = aF["t_hit"].numpy().reshape(H, W)
    hit = np.isfinite(tF)
    aB = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org + look[None, None, :] * (2 * D), np.broadcast_to(-look, org.shape)],
        axis=-1).reshape(-1, 6).astype(np.float32)))
    tB = aB["t_hit"].numpy().reshape(H, W)
    both = hit & np.isfinite(tB)
    ext = np.full((H, W), np.inf, dtype=np.float64)
    ext[both] = 2 * D - tF[both] - tB[both]
    job = (hit & ~((ext < args.thin_extent) & hit)).astype(np.float32)
    dist = distance_transform_edt(hit).astype(np.float32)
    hidx = np.where(hole)[0]
    i1 = hidx[(N[hidx] @ dtc) > args.facing_min]
    u_face[i1] = True
    org2 = (P[i1] + N[i1] * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
    t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org2, np.broadcast_to(dtc.astype(np.float32), org2.shape)], axis=1)))
    i2 = i1[~np.isfinite(t["t_hit"].numpy())]
    u_vis[i2] = True
    pxx = ((P[i2] - bmid) @ right / h_ext + 0.5) * W - 0.5
    pyy = (0.5 - (P[i2] - bmid) @ up / v_ext) * H - 0.5
    i3 = i2[bilin(job, pxx, pyy) > 0.5]
    u_thin[i3] = True
    pxx = ((P[i3] - bmid) @ right / h_ext + 0.5) * W - 0.5
    pyy = (0.5 - (P[i3] - bmid) @ up / v_ext) * H - 0.5
    u_edge[i3[bilin(dist, pxx, pyy) >= args.edge_dist]] = True
SH = cls_side & hole
attrib = [("never faces any candidate at %.2f" % args.facing_min, SH & ~u_face),
          ("faces one, OCCLUDED on every one", SH & u_face & ~u_vis),
          ("visible somewhere, THIN-WITHHELD on every one", SH & u_vis & ~u_thin),
          ("survives thin, EDGE-TRIMMED on every one", SH & u_thin & ~u_edge),
          ("REACHABLE by some candidate stroke", SH & u_edge)]
resid = {}
for nm, s in attrib:
    resid[nm] = int(s.sum())
    print("[stroke]   %-46s %9d  %6.2f%% of side holes"
          % (nm, int(s.sum()), pct(s.sum(), SH.sum())), flush=True)
got = int((SH & cov).sum())
print("[stroke]   the proposed set closes %d = %.2f%% of side holes, against a %.2f%% "
      "ceiling for ALL %d eye-level candidates together"
      % (got, pct(got, SH.sum()), pct(int((SH & u_edge).sum()), SH.sum()),
         len(side_cams)), flush=True)

out = {"inherited_check": [{"name": n, "measured": g, "reported": w, "ok": g == w}
                           for n, g, w in INHERIT],
       "orders": orders_out, "mix": mix, "side_residual": resid,
       "side_stroke_ceiling": int((SH & u_edge).sum()),
       "params": {"facing_min": args.facing_min, "thin_extent": args.thin_extent,
                  "edge_dist": args.edge_dist, "aspect": args.aspect,
                  "fit_axis": args.fit_axis, "margin": args.margin,
                  "deck_normal": args.deck_normal, "waterline_frac": args.waterline_frac},
       "totals": {"valid": NV, "styled": int(styled_v.sum()), "holes": int(hole.sum()),
                  "side_holes": side_h, "deck_holes": dk_h, "bottom_holes": bt_h,
                  "foot_texels": int(foot.sum()), "foot_holes": foot_h},
       "deck_pair": deck_rows,
       "deck_pair_union": int(deck_union.sum()),
       "deck_holes_closed_by_pair": dk_got,
       "side_standalone": stand, "greedy": ladder,
       "diagnostics": diag, "spiral": spiral}
json.dump(out, open(os.path.join(args.out, "stroke_cameras.json"), "w"), indent=1)
print("\n[stroke] wrote %s" % os.path.join(args.out, "stroke_cameras.json"), flush=True)
