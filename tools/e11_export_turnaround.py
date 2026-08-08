"""E11 — the dense-turnaround exporter: accepted assets become training data.

Spec: docs/experiments/E11-dense-turnaround-export.md. The export is a pure function
of the accepted artifacts — no generation, no judgment, and the base assets are never
opened for writing (all reads; every write lands in a NEW directory).

WHAT RENDERS. `texpass_iter emit` is the renderer, invoked as a subprocess with the
subject profile — the same tool, same code path, same profile that produced the
recorded Gate-1 sheet renders. This exporter orchestrates; it does not reimplement
the raycast. Per camera it collects emit's render.png (flat readout) and hit.png
(the exact silhouette).

WHAT THIS TOOL ADDS PER VIEW, beyond emit: a texel-ID raycast (the head-render
construction from texel_provenance.py: primitive ids + barycentric uv -> atlas texel)
that yields EXACT per-pixel maps with no antialiasing:
  - prov_class_<view>.png  — E09 indexed discipline BY CONSTRUCTION: indexed PNG,
    PLTE == the declared class palette (background/reference/brush/dilation), one
    class per pixel from the anchored claim map. Born indexed - no truecolor
    conversion happens, so X-H3's lossless-proof obligation is met by construction
    for renders (the texture atlas's conversion was already proven by the staged
    manifest's round-trip).
  - owner_id_<view>.npy    — int8 per-pixel view-owner (from view_owner.npy; -1
    where unstyled or no surface), the render-space slice of the native sidecar.
  - loss_mask_<view>.png   — the owner-boundary distance field, grayscale: distance
    in px to the nearest stage-1 owner boundary, clipped at 32 px and scaled to
    0..255 (0 = on a boundary). Whether it gates admission or weights loss is the
    lane's Phase-0 decision; the export carries it (spec item 5).
  - admission_<view>.json  — per-render class shares inside the exact silhouette
    (reference/brush/dilation share, owner-boundary stats) — reference-share per
    render (spec item 5's other half).

FRAMES (the Ruling 2/4 discipline): this tool transcribes NO world quantity. The
camera basis and framing live inside emit (profile-bound); the texel-ID raycast reads
emit's own cam.json back rather than recomputing extents, and converts nothing
between frames. The canonical scene is built once with the same re-axis the whole
pipeline uses, documented at the function.

STEP 0 (--step0): the one-view anchor. Beam view only, every channel checked against
the recorded artifacts — asset render byte-identical to the sheet's, silhouette to
Step 0.2's hit.png, prov/owner renders to their sheet jobs, the owner display atlas
proven a pure function of (view_owner.npy, claim) in texture space, and the emit run
twice from fresh states for X-H1's byte-stability. HALT on any digit.

  e11_export_turnaround.py --step0
  e11_export_turnaround.py --arm X1
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import distance_transform_edt

Image.MAX_IMAGE_PIXELS = None

FACET = r"E:\AI\facet"
PREP = r"E:\AI\training\facet_next\E04_shipprep"
STROKE = r"E:\AI\training\facet_next\E04_stroke"
PROFILE = os.path.join(FACET, "profiles", "ship.json")
PYTOOL = os.path.join(FACET, "tools", "texpass_iter.py")
J = os.path.join

# The three atlases of the accepted asset (read-only sources).
CHANNELS = {
    "asset": J(STROKE, "out", "galleon_final.png"),
    "prov": J(STROKE, "out", "prov_atlas.png"),
    "owner": J(STROKE, "out", "owner_atlas.png"),
}
# The recorded sheet states supply holes/styled byte-identical to the shipped state,
# so an emitted render has the same inputs the recorded renders had.
SHEET_STATE = {ch: J(STROKE, "sheet", ch) for ch in CHANNELS}

CLAIM_CLASSES = [("background", (0, 0, 0)), ("reference", (46, 176, 88)),
                 ("brush", (40, 110, 235)), ("dilation", (232, 132, 32))]
LOSS_CLIP_PX = 32.0

# The production camera superset (profiles/ship.json cull_unseen.production) is read
# from the profile at runtime — never transcribed here.


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def key_of(yaw, el):
    return f"y+{int(round(yaw)):03d}_e+{int(round(el)):02d}"


def run_emit(state_dir, yaw, el, glb, prep=PREP, profile=PROFILE):
    cmd = [sys.executable, PYTOOL, "emit", "--state", state_dir, "--prep", prep,
           "--glb", glb, "--yaw", str(yaw), "--el", str(el),
           "--profile", profile]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=FACET)
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr)
        raise SystemExit(f"ANDON: emit failed for yaw {yaw} el {el} in {state_dir}")
    return J(state_dir, "job_" + key_of(yaw, el))


def fresh_state(channel, dest):
    """A new emit state whose inputs are byte-identical to the recorded sheet state."""
    os.makedirs(dest, exist_ok=True)
    shutil.copyfile(CHANNELS[channel], J(dest, "atlas.png"))
    shutil.copyfile(J(SHEET_STATE[channel], "holes.png"), J(dest, "holes.png"))
    shutil.copyfile(J(SHEET_STATE[channel], "styled_mask.npy"), J(dest, "styled_mask.npy"))
    return dest


def bytes_equal(a, b):
    return open(a, "rb").read() == open(b, "rb").read()


# ─── the texel-ID raycast (texel_provenance.py's head-render construction,
#     generalised to emit's own cam.json — no extents recomputed) ─────────

class IdCaster:
    def __init__(self, prep=PREP):
        m = trimesh.load(J(prep, "prep_uv.glb"), force="mesh", process=False)
        v = np.asarray(m.vertices, dtype=np.float64)
        self.f = np.asarray(m.faces, dtype=np.int64)
        self.uv = np.asarray(m.visual.uv, dtype=np.float64)
        # canonical mesh frame: Y-up -> Z-up re-axed, max-abs normalised * 0.5 —
        # the load_scene() frame every cam.json speaks (E10 Ruling 2).
        self.v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
        self.rs = o3d.t.geometry.RaycastingScene()
        self.rs.add_triangles(o3d.core.Tensor(self.v.astype(np.float32)),
                              o3d.core.Tensor(self.f.astype(np.uint32)))
        meta = json.load(open(J(prep, "meta.json")))
        self.RES = meta["res"]

    def texel_ids(self, cam):
        """Per-pixel atlas texel id for the camera emit recorded, -1 off-surface."""
        yaw, el = cam["yaw"], cam["el"]
        th, e = np.radians(yaw), np.radians(el)
        cd = np.array([np.sin(th) * np.cos(e), -np.cos(th) * np.cos(e), np.sin(e)])
        look = -cd / np.linalg.norm(cd)
        right = np.cross(look, [0.0, 0.0, 1.0])
        right /= np.linalg.norm(right) + 1e-12
        up = np.cross(right, look)
        up /= np.linalg.norm(up) + 1e-12
        W, H = cam["W"], cam["H"]
        bmid = np.array(cam["bmid"])
        xs = (np.arange(W) + 0.5) / W * cam["h_ext"] - cam["h_ext"] / 2
        ys = cam["v_ext"] / 2 - (np.arange(H) + 0.5) / H * cam["v_ext"]
        gx, gy = np.meshgrid(xs, ys)
        org = (bmid[None, None, :] + gx[..., None] * right[None, None, :]
               + gy[..., None] * up[None, None, :] - look[None, None, :] * 2.0)
        ans = self.rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [org, np.broadcast_to(look, org.shape)], axis=-1
        ).reshape(-1, 6).astype(np.float32)))
        hit = np.isfinite(ans["t_hit"].numpy()).reshape(H, W)
        prim = ans["primitive_ids"].numpy().reshape(H, W)
        buv = ans["primitive_uvs"].numpy().reshape(H, W, 2)
        tex = np.full((H, W), -1, dtype=np.int64)
        if hit.any():
            tr = self.f[prim[hit]]
            wu, wv = buv[hit][:, 0:1], buv[hit][:, 1:2]
            uvp = (1 - wu - wv) * self.uv[tr[:, 0]] + wu * self.uv[tr[:, 1]] \
                + wv * self.uv[tr[:, 2]]
            ax = np.clip((uvp[:, 0] * self.RES).astype(np.int64), 0, self.RES - 1)
            ay = np.clip(((1 - uvp[:, 1]) * self.RES).astype(np.int64), 0, self.RES - 1)
            tex[hit] = ay * self.RES + ax
        return tex, hit


def write_indexed_png(path, class_map, palette=None):
    """class_map uint8 HxW with values 0..len(palette)-1 -> indexed PNG,
    PLTE == the declared palette exactly (E09 Amendment 1 discipline)."""
    palette = palette or CLAIM_CLASSES
    im = Image.fromarray(class_map, mode="P")
    im.putpalette([c for _, rgb in palette for c in rgb])
    im.save(path, optimize=False)
    # prove the write: reread, palette prefix == declared, pixels identical
    back = Image.open(path)
    if not (back.mode == "P"):
        raise AssertionError("ANDON: indexed write came back non-indexed")
    plte = back.getpalette()[:len(palette) * 3]
    want = [c for _, rgb in palette for c in rgb]
    if not (plte == want):
        raise AssertionError(f"ANDON: {path} PLTE != declared palette")
    if not (np.array_equal(np.asarray(back), class_map)):
        raise AssertionError(f"ANDON: {path} pixels changed through the indexed write")


def view_products(caster, cam, claim_flat, owner_flat, out_dir, view_id, palette=None,
                  class_flat=None):
    """The exact per-view maps: indexed class render, owner slice, loss mask, shares.

    owner_flat=None means the asset has NO owner sidecar (W3) — owner products are
    then honestly ABSENT, not synthesized (the spec's X2 clause verbatim).

    class_flat is the X4 addition: a per-texel class INDEX into `palette`, used
    directly instead of the three-way claim mapping below. The longsword's
    provenance atlas carries FIVE non-background classes (the stone kept as its own
    sub-class, E14 Rulings 30/31b), which the 0/1..254/255 claim encoding cannot
    express. Absent, every prior subject takes the identical code path."""
    palette = palette or CLAIM_CLASSES
    tex, hit = caster.texel_ids(cam)
    H, W = hit.shape
    cls = np.zeros((H, W), dtype=np.uint8)          # background
    ok = tex >= 0
    t = tex[ok]
    if class_flat is not None:
        cls[ok] = class_flat[t]
    else:
        cvals = claim_flat[t]
        out = np.zeros(len(t), dtype=np.uint8)
        out[cvals == 0] = 1
        out[(cvals >= 1) & (cvals <= 254)] = 2
        out[cvals == 255] = 3
        cls[ok] = out

    write_indexed_png(J(out_dir, f"prov_class_{view_id}.png"), cls, palette)

    npx = int(hit.sum())
    shares = {name: round(100.0 * float(((cls == i) & hit).sum()) / max(npx, 1), 4)
              for i, (name, _) in enumerate(palette) if i > 0}
    if owner_flat is None:
        adm = {"view": view_id, "figure_px": npx, "class_share_pct": shares,
               "owner_channel": "absent — this asset has no view_owner sidecar; "
                                "nothing synthesized"}
        json.dump(adm, open(J(out_dir, f"admission_{view_id}.json"), "w"), indent=1)
        return adm

    own = np.full((H, W), -1, dtype=np.int8)
    own[ok] = owner_flat[t]
    np.save(J(out_dir, f"owner_id_{view_id}.npy"), own)

    # owner-boundary distance field over stage-1 pixels: boundary = 4-neighbour
    # owner-id disagreement between styled (owner>=0) pixels; distance clipped and
    # scaled. Pixels with no owner (or no surface) render 255 (far / not applicable).
    o = own.astype(np.int16)
    styled = o >= 0
    b = np.zeros((H, W), dtype=bool)
    b[:, 1:] |= styled[:, 1:] & styled[:, :-1] & (o[:, 1:] != o[:, :-1])
    b[:, :-1] |= b[:, 1:] & False | (styled[:, :-1] & styled[:, 1:] & (o[:, :-1] != o[:, 1:]))
    b[1:, :] |= styled[1:, :] & styled[:-1, :] & (o[1:, :] != o[:-1, :])
    b[:-1, :] |= styled[:-1, :] & styled[1:, :] & (o[:-1, :] != o[1:, :])
    if b.any():
        dist = distance_transform_edt(~b)
    else:
        dist = np.full((H, W), LOSS_CLIP_PX, dtype=np.float64)
    lm = np.clip(dist / LOSS_CLIP_PX, 0.0, 1.0)
    lm_img = (lm * 255).round().astype(np.uint8)
    lm_img[~styled] = 255
    Image.fromarray(lm_img, mode="L").save(J(out_dir, f"loss_mask_{view_id}.png"))

    adm = {"view": view_id, "figure_px": npx, "class_share_pct": shares,
           "owner_boundary_px": int(b.sum()),
           "loss_mask_clip_px": LOSS_CLIP_PX,
           "owner_values_present": sorted(int(x) for x in np.unique(own[ok]))}
    json.dump(adm, open(J(out_dir, f"admission_{view_id}.json"), "w"), indent=1)
    return adm


def owner_atlas_vs_sidecar(claim_flat, owner_flat, valid_flat):
    """Texture-space proof: the owner display atlas is a pure function of
    (view_owner sidecar, claim map). Returns the value->colour tables or halts."""
    oa = np.asarray(Image.open(CHANNELS["owner"]).convert("RGB"), dtype=np.uint8)
    oa = oa.reshape(-1, 3)
    tables = {}
    # stage-1 texels: colour keyed by sidecar view id
    for v in range(0, 8):
        sel = valid_flat & (claim_flat == 0) & (owner_flat == v)
        if not sel.any():
            continue
        cols = np.unique(oa[sel], axis=0)
        if not (len(cols) == 1):
            raise AssertionError(
                f"ANDON: owner atlas has {len(cols)} colours for sidecar view {v} "
                f"on stage-1 texels — not a pure function of the sidecar")
        tables[f"view_{v}"] = [int(c) for c in cols[0]]
    bad = valid_flat & (claim_flat == 0) & (owner_flat < 0)
    if bad.any():
        raise AssertionError(
            f"ANDON: {int(bad.sum()):,} stage-1 texels carry sidecar owner -1 — "
            f"the sidecar disagrees with the claim map")
    for k in range(1, 7):
        sel = valid_flat & (claim_flat == k)
        if not sel.any():
            continue
        cols = np.unique(oa[sel], axis=0)
        if not (len(cols) == 1):
            raise AssertionError(f"ANDON: stroke {k} renders {len(cols)} colours")
        tables[f"stroke_{k}"] = [int(c) for c in cols[0]]
    sel = valid_flat & (claim_flat == 255)
    cols = np.unique(oa[sel], axis=0)
    if not (len(cols) == 1):
        raise AssertionError(f"ANDON: dilation renders {len(cols)} colours")
    tables["dilation"] = [int(c) for c in cols[0]]
    return tables


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step0", action="store_true", help="one-view anchor; HALT on any digit")
    ap.add_argument("--arm", choices=["X1", "X2", "X3", "X4"],
                    help="X1: galleon superset; X2: W3 dense; X3: dragon dense; "
                         "X4: longsword dense")
    ap.add_argument("--claim", help="anchored claim.npy (per-stroke replay; X1/step0)")
    ap.add_argument("--glb", default=J(PREP, "prep_uv.glb"),
                    help="the GLB emit renders with; the Step-0 byte anchor is what "
                         "verifies this operand is the recorded one")
    ap.add_argument("--out", default=J(STROKE, "export", "turnaround"))
    args = ap.parse_args()

    if args.arm == "X2":
        return arm_x2(args)
    if args.arm == "X3":
        if args.out == J(STROKE, "export", "turnaround"):
            args.out = J(r"E:\AI\training\facet_next\E13_stroke", "export", "turnaround")
        return arm_dragon(args)
    if args.arm == "X4":
        if args.out == J(STROKE, "export", "turnaround"):
            args.out = J(r"E:\AI\training\facet_next\E14_strokes", "export", "turnaround")
        return arm_longsword(args)

    if not (args.claim):
        raise AssertionError("ANDON: --claim is required for the galleon legs")
    claim = np.load(args.claim).reshape(-1)
    owner = np.load(J(STROKE, "export", "view_owner.npy")).reshape(-1)
    valid = np.load(J(PREP, "mask.npy"))[..., 0].reshape(-1) > 0.5

    if args.step0:
        return step0(args, claim, owner, valid)
    if args.arm == "X1":
        return arm_x1(args, claim, owner, valid)
    print("nothing to do: pass --step0 or --arm X1/X2")
    return 0


# ─── X2: W3 re-exported dense — the two-subjects-from-birth proof ────────────
# W3's route prep is facet_E06/C1/prep (named by masks/silhouettes.json's own
# "prep" pointer). Its provenance atlas is an EXACT 4-colour class map (measured:
# bg 0,0,0 / reference 60,200,110 / brush 70,170,255 / dilation 235,120,40), so
# the claim map derives from colours with no replay. The owner channel is
# honestly ABSENT — recorded, never synthesized.

W3_PREP = r"E:\AI\training\facet_E06\C1\prep"
W3_ROOT = r"E:\AI\training\facet_E08\ARMB"
W3_PROFILE = os.path.join(FACET, "profiles", "character.json")
W3_PALETTE = [("background", (0, 0, 0)), ("reference", (60, 200, 110)),
              ("brush", (70, 170, 255)), ("dilation", (235, 120, 40))]


def w3_claim_from_colors():
    pa = np.asarray(Image.open(J(W3_ROOT, "out", "provenance_atlas.png")).convert("RGB"))
    flat = pa.reshape(-1, 3)
    claim = np.full(flat.shape[0], -1, dtype=np.int16)   # background
    ref = np.all(flat == W3_PALETTE[1][1], axis=1)
    bru = np.all(flat == W3_PALETTE[2][1], axis=1)
    dil = np.all(flat == W3_PALETTE[3][1], axis=1)
    bg = np.all(flat == W3_PALETTE[0][1], axis=1)
    n_other = flat.shape[0] - int(ref.sum() + bru.sum() + dil.sum() + bg.sum())
    if not (n_other == 0):
        raise AssertionError(
            f"ANDON: {n_other:,} pixels outside the 4 measured class colours")
    claim[ref] = 0
    claim[bru] = 1
    claim[dil] = 255
    return claim


def arm_x2(args):
    out_root = J(W3_ROOT, "export", "turnaround")
    print(f"[X2] W3 dense export — prep {W3_PREP}, owner channel ABSENT by record")
    claim = w3_claim_from_colors()
    print("[X2] claim map derived from the exact 4-colour provenance atlas")

    # X-H3's lossless leg: truecolor -> indexed, class map pixel-identical.
    os.makedirs(out_root, exist_ok=True)
    pa = np.asarray(Image.open(J(W3_ROOT, "out", "provenance_atlas.png")).convert("RGB"))
    idx = np.zeros(pa.shape[:2], dtype=np.uint8)
    for i, (_, rgb) in enumerate(W3_PALETTE):
        idx[np.all(pa == rgb, axis=-1)] = i
    ipath = J(out_root, "provenance_atlas_indexed.png")
    write_indexed_png(ipath, idx, W3_PALETTE)
    back = np.asarray(Image.open(ipath).convert("RGB"))
    if not (np.array_equal(back, pa)):
        raise AssertionError("ANDON: indexed conversion is not lossless")
    print(f"[X2] X-H3 lossless conversion PROVEN: {ipath} pixel-identical to the "
          f"truecolor source through PLTE round-trip")

    channels = {"asset": J(W3_ROOT, "out", "atlas_final.png"),
                "prov": J(W3_ROOT, "out", "provenance_atlas.png")}
    states = {}
    for ch, atlas in channels.items():
        st = J(out_root, "_state", ch)
        os.makedirs(st, exist_ok=True)
        shutil.copyfile(atlas, J(st, "atlas.png"))
        shutil.copyfile(J(W3_ROOT, "state", "holes.png"), J(st, "holes.png"))
        shutil.copyfile(J(W3_ROOT, "state", "styled_mask.npy"), J(st, "styled_mask.npy"))
        states[ch] = st

    glb = J(W3_PREP, "prep_uv.glb")

    # one-view anchor attempt BEFORE volume (the Step-0 pattern applied to W3;
    # not pre-registered by the spec, so a mismatch is REPORTED, not a halt).
    job = run_emit(states["asset"], 0.0, 0.0, glb, prep=W3_PREP, profile=W3_PROFILE)
    rec_render = J(W3_ROOT, "out", "renders_flat", "final_0.png")
    rec_sil = J(W3_ROOT, "masks", "w3clay_0.png")
    same_r = bytes_equal(J(job, "render.png"), rec_render)
    same_s = bytes_equal(J(job, "hit.png"), rec_sil)
    print(f"[X2] anchor attempt: beam render byte-identical to renders_flat/final_0: "
          f"{same_r}; hit byte-identical to masks/w3clay_0: {same_s}")
    if not (same_r and same_s):
        # pixel-level diagnosis, since file bytes are not pixel values
        a = np.asarray(Image.open(J(job, "render.png")).convert("RGB"), dtype=np.int16)
        b = np.asarray(Image.open(rec_render).convert("RGB"), dtype=np.int16)
        if a.shape == b.shape:
            dd = np.abs(a - b).max(axis=-1)
            print(f"[X2]   pixel diff vs recorded render: {(dd > 0).sum():,} px differ, "
                  f"max {dd.max()} levels")
        else:
            print(f"[X2]   shapes differ: emitted {a.shape} vs recorded {b.shape}")
        ah = np.asarray(Image.open(J(job, "hit.png")).convert("L")) > 127
        bh = np.asarray(Image.open(rec_sil).convert("L")) > 127
        if ah.shape == bh.shape:
            print(f"[X2]   silhouette pixel diff: {(ah != bh).sum():,} px")
        print("[X2]   REPORTED — the recorded flat renders' generator is not this emit "
              "path, or its state differed. The dense export below is still X-H1-pure; "
              "which render set the record keeps is the ruling's call.")

    # X-H1 spot check on W3: same view, fresh state, byte-identical
    st2 = J(out_root, "_state", "asset_rerun")
    os.makedirs(st2, exist_ok=True)
    for f in ("atlas.png", "holes.png", "styled_mask.npy"):
        shutil.copyfile(J(states["asset"], f), J(st2, f))
    job2 = run_emit(st2, 0.0, 0.0, glb, prep=W3_PREP, profile=W3_PROFILE)
    same2 = bytes_equal(J(job, "render.png"), J(job2, "render.png"))
    print(f"[X2] X-H1 spot check (two fresh emits, beam): byte-identical {same2}")
    if not same2:
        print("[X2] HALT — the export is not a pure function on this subject.")
        return 1

    # the dense set: the character's cull superset — 24 yaws @ 15deg + 0,55 + 180,55
    cams = [(y * 15.0, 0.0) for y in range(24)] + [(0.0, 55.0), (180.0, 55.0)]
    caster = IdCaster(prep=W3_PREP)
    renders = []
    for (y, e) in cams:
        vid = key_of(y, e)
        dest = J(out_root, "views", vid)
        os.makedirs(dest, exist_ok=True)
        for ch in channels:
            jb = run_emit(states[ch], y, e, glb, prep=W3_PREP, profile=W3_PROFILE)
            shutil.copyfile(J(jb, "render.png"), J(dest, f"{ch}.png"))
            if ch == "asset":
                shutil.copyfile(J(jb, "hit.png"), J(dest, "silhouette.png"))
                shutil.copyfile(J(jb, "cam.json"), J(dest, "cam.json"))
        cam = json.load(open(J(dest, "cam.json")))
        adm = view_products(caster, cam, claim, None, dest, vid, palette=W3_PALETTE)
        renders.append({"id": vid, "yaw": y, "el": e,
                        "admission": adm["class_share_pct"]})
        print(f"[X2] {vid}: reference {adm['class_share_pct']['reference']:.2f}%  "
              f"figure {adm['figure_px']:,}px", flush=True)

    json.dump({"cameras": len(cams), "anchor_render_byte_identical": bool(same_r),
               "anchor_silhouette_byte_identical": bool(same_s),
               "renders": renders},
              open(J(out_root, "x2_run.json"), "w"), indent=1)
    print(f"[X2] wrote {J(out_root, 'x2_run.json')}")
    return 0


# ─── X3: the dragon (E12/E13), dataset asset #3 ──────────────────────────────
# Third subject, third owner configuration. The galleon carried BOTH a numeric
# owner sidecar and a rendered owner display atlas; W3 carried NEITHER. This
# subject carries the NUMERIC channel and no display atlas — none was ever built
# for it, and synthesizing one here would be inventing a channel rather than
# exporting one (the X2 clause, applied to the half that is missing).
#
# The claim map derives from colours with no replay: the provenance atlas is an
# exact 4-colour class map whose counts reproduce the ruled mix to the texel
# (reference 1,430,687 / brush 99,643 / dilation 1,710,180 = valid 3,240,510,
# E12 Ruling 27e). Verified in code below, not asserted.
#
# The camera set is READ FROM THE PROFILE at runtime (X1's mechanism), never
# transcribed. The anchors are stronger here than on either predecessor: the
# eight route yaws have RECORDED renders on both channels — the Gate-1 sheets'
# own columns, emitted through this same path by run/render_final.ps1 — so 16
# cameras anchor byte-for-byte against artifacts this session did not produce.

DRAGON_PREP = r"E:\AI\training\facet_next\E12_prep"
DRAGON_RUN = r"E:\AI\training\facet_next\E13_stroke\run"
DRAGON_STAGE1 = r"E:\AI\training\facet_next\E13_stage1"
DRAGON_PROFILE = os.path.join(FACET, "profiles", "beast.json")
DRAGON_PALETTE = [("background", (16, 16, 18)), ("reference", (118, 146, 110)),
                  ("brush", (240, 176, 48)), ("dilation", (150, 90, 150))]
# The ruled mix (E12 Ruling 27e / run_log.jsonl "mix"), checked against the atlas.
DRAGON_MIX = {"reference": 1430687, "brush": 99643, "dilation": 1710180}


def dragon_claim_from_colors():
    """Exact 4-colour class map -> claim (0 reference, 1 brush, 255 dilation)."""
    pa = np.asarray(Image.open(J(DRAGON_RUN, "prov_final_atlas.png")).convert("RGB"))
    flat = pa.reshape(-1, 3)
    claim = np.full(flat.shape[0], -1, dtype=np.int16)
    sel = {name: np.all(flat == rgb, axis=1) for name, rgb in DRAGON_PALETTE}
    n_other = flat.shape[0] - int(sum(s.sum() for s in sel.values()))
    if not (n_other == 0):
        raise AssertionError(
            f"ANDON: {n_other:,} pixels outside the 4 declared class colours")
    for name, want in DRAGON_MIX.items():
        got = int(sel[name].sum())
        if not (got == want):
            raise AssertionError(
                f"ANDON: provenance atlas has {got:,} {name} texels; the ruled mix "
                f"(E12 Ruling 27e) says {want:,}")
    claim[sel["reference"]] = 0
    claim[sel["brush"]] = 1
    claim[sel["dilation"]] = 255
    print(f"[X3] claim map from the exact 4-colour atlas; class counts reproduce "
          f"the ruled mix to the texel")
    return claim, pa


def arm_dragon(args):
    out_root = args.out
    os.makedirs(out_root, exist_ok=True)
    print(f"[X3] dragon dense export -> {out_root}")

    claim, pa = dragon_claim_from_colors()
    owner = np.load(J(DRAGON_STAGE1, "A0_stage1_owner.npy")).reshape(-1)

    # the owner sidecar must agree with the claim map: every stage-1 texel owned,
    # and nothing outside stage 1 claiming an owner. The galleon's Step-0 check,
    # minus the display-atlas half it has no atlas for.
    st1 = claim == 0
    unowned = int((st1 & (owner < 0)).sum())
    if not (unowned == 0):
        raise AssertionError(
            f"ANDON: {unowned:,} stage-1 texels carry sidecar owner -1 — the sidecar "
            f"disagrees with the claim map")
    stray = int((~st1 & (owner >= 0)).sum())
    if not (stray == 0):
        raise AssertionError(
            f"ANDON: {stray:,} texels outside stage 1 carry an owner id")
    print(f"[X3] owner sidecar agrees with the claim map: "
          f"{int(st1.sum()):,} stage-1 texels all owned, "
          f"owner ids present {sorted(int(x) for x in np.unique(owner[st1]))}")

    # X-H3's lossless leg: truecolor provenance atlas -> indexed, pixel-identical.
    idx = np.zeros(pa.shape[:2], dtype=np.uint8)
    for i, (_, rgb) in enumerate(DRAGON_PALETTE):
        idx[np.all(pa == rgb, axis=-1)] = i
    ipath = J(out_root, "provenance_atlas_indexed.png")
    write_indexed_png(ipath, idx, DRAGON_PALETTE)
    back = np.asarray(Image.open(ipath).convert("RGB"))
    if not (np.array_equal(back, pa)):
        raise AssertionError("ANDON: indexed conversion is not lossless")
    print(f"[X3] X-H3 lossless conversion PROVEN: indexed atlas pixel-identical "
          f"to the truecolor source through PLTE round-trip")

    # fresh emit states, copied out of the read-only run tree (Ruling 28: the
    # accepted asset and everything under run/ is citable-only).
    src_state = {"asset": J(DRAGON_RUN, "state_final"),
                 "prov": J(DRAGON_RUN, "state_prov")}
    states = {}
    for ch, src in src_state.items():
        st = J(out_root, "_state", ch)
        os.makedirs(st, exist_ok=True)
        for f in ("atlas.png", "holes.png", "styled_mask.npy"):
            shutil.copyfile(J(src, f), J(st, f))
        states[ch] = st
    glb = J(DRAGON_PREP, "prep_uv.glb")

    # the camera superset, READ from the profile — never transcribed.
    prof = json.load(open(DRAGON_PROFILE, encoding="utf-8"))
    prod = prof["tools"]["cull_unseen.py"]["production"]["value"]
    cams, seen = [], set()
    for spec in prod.split(";"):
        y, e = (float(x) for x in spec.split(","))
        if (y, e) not in seen:
            seen.add((y, e))
            cams.append((y, e))
    print(f"[X3] camera superset derived from profiles/beast.json: {len(cams)} cameras "
          f"x {len(states)} channels")

    caster = IdCaster(prep=DRAGON_PREP)
    anchors = []
    renders = []
    for (y, e) in cams:
        vid = key_of(y, e)
        dest = J(out_root, "views", vid)
        os.makedirs(dest, exist_ok=True)
        for ch in states:
            jb = run_emit(states[ch], y, e, glb, prep=DRAGON_PREP, profile=DRAGON_PROFILE)
            shutil.copyfile(J(jb, "render.png"), J(dest, f"{ch}.png"))
            if ch == "asset":
                shutil.copyfile(J(jb, "hit.png"), J(dest, "silhouette.png"))
                shutil.copyfile(J(jb, "cam.json"), J(dest, "cam.json"))
            # RECORDED-ARTIFACT ANCHOR: the eight route yaws were rendered through
            # this same path for the Gate-1 sheets. Byte-identity or it is reported.
            tag = {"asset": "final", "prov": "prov"}[ch]
            rec = J(DRAGON_RUN, f"FINAL_{tag}_y{int(y)}.png")
            if e == 0 and float(y).is_integer() and os.path.exists(rec):
                same = bytes_equal(J(dest, f"{ch}.png"), rec)
                anchors.append({"view": vid, "channel": ch,
                                "recorded": os.path.basename(rec), "byte_identical": same})
                if not same:
                    print(f"[X3] ANCHOR MISMATCH {vid} {ch} vs {os.path.basename(rec)}")
        cam = json.load(open(J(dest, "cam.json")))
        adm = view_products(caster, cam, claim, owner, dest, vid, palette=DRAGON_PALETTE)
        renders.append({"id": vid, "yaw": y, "el": e,
                        "admission": adm["class_share_pct"]})
        print(f"[X3] {vid}: reference {adm['class_share_pct']['reference']:.2f}%  "
              f"brush {adm['class_share_pct']['brush']:.2f}%  "
              f"dilation {adm['class_share_pct']['dilation']:.2f}%  "
              f"figure {adm['figure_px']:,}px", flush=True)

    n_anch = sum(1 for a in anchors if a["byte_identical"])
    print(f"[X3] recorded-artifact anchors: {n_anch}/{len(anchors)} byte-identical")

    # X-H1 purity spot check: a SECOND fresh state, a different directory, one
    # camera. (Comparing a file to itself would return identical however the
    # export behaved — the two files below are produced independently.)
    st2 = J(out_root, "_state", "asset_rerun")
    os.makedirs(st2, exist_ok=True)
    for f in ("atlas.png", "holes.png", "styled_mask.npy"):
        shutil.copyfile(J(src_state["asset"], f), J(st2, f))
    jb2 = run_emit(st2, 0.0, 0.0, glb, prep=DRAGON_PREP, profile=DRAGON_PROFILE)
    pure = bytes_equal(J(out_root, "views", key_of(0, 0), "asset.png"),
                       J(jb2, "render.png"))
    print(f"[X3] X-H1 spot check (independent fresh state, yaw 0): byte-identical {pure}")
    if not pure:
        print("[X3] HALT — the export is not a pure function on this subject.")
        return 1

    json.dump({"cameras": len(cams), "channels": sorted(states),
               "owner_channel": "numeric present (view_owner.npy + per-view "
                                "owner_id/loss_mask); no display atlas exists for "
                                "this subject and none was synthesized",
               "recorded_anchors": anchors,
               "purity_spot_check_byte_identical": bool(pure),
               "renders": renders},
              open(J(out_root, "x3_run.json"), "w"), indent=1)
    print(f"[X3] wrote {J(out_root, 'x3_run.json')}")
    return 0


# ─── X4: the longsword (E14), dataset asset #4 ───────────────────────────────
# Fourth subject, fourth subject CLASS (character, ship, beast, prop), and the
# first whose provenance atlas carries more than three classes. Rulings 30/31b
# keep THE STONE as its own provenance sub-class — projected reference paint,
# colour-corrected, never blended into the brush's numbers — so the class map is
# six-valued (background + stage-1b projection + garnet re-projection + collar
# repair + brush + dilation) and rides through view_products' class_flat path.
#
# The owner channel: NUMERIC present, display ABSENT — the dragon's configuration.
# The array declared is stage 1b's, because it is the one that agrees EXACTLY with
# the accepted asset's reference partition; the re-projection's own owner array
# (the same six twins re-projected, whose atlas WRITE was restricted afterward but
# whose owner sidecar never was — Ruling 27b's catch one layer over) disagrees and
# rides undeclared beside it. Measured in the preflight below, not asserted.
#
# The camera set is READ FROM THE PROFILE at runtime. --profile is bound on every
# emit and the 240x1024 frame asserted after each (Ruling 29c: an unprofiled emit
# silently produces a 752-wide frame).

LS_PREP = r"E:\AI\training\facet_next\E14_prep"
LS_FINAL = r"E:\AI\training\facet_next\E14_strokes\run\final"
LS_STAGE1 = J(LS_PREP, "stage1")
LS_PROFILE = os.path.join(FACET, "profiles", "prop.json")
LS_PALETTE = [("background", (16, 16, 18)),
              ("stage1b_projection", (118, 146, 110)),
              ("garnet_reprojection", (220, 60, 220)),
              ("collar_repair", (40, 230, 230)),
              ("brush", (240, 176, 48)),
              ("dilation", (150, 90, 150))]
# run/final/provenance_legend.json + E14 Ruling 31b, checked against the atlas.
LS_MIX = {"stage1b_projection": 1588943, "garnet_reprojection": 66468,
          "collar_repair": 1436, "brush": 75890, "dilation": 1929166}
LS_VALID = 3661903
# owner id k is the POSITIONAL index into stage 1b's six-view input list — NOT a
# route view index (views 2 and 6 have no accepted twin, E14 Ruling 20). Verified
# below against stage1b_provenance_legend.json's own per-view committed counts.
LS_OWNER_VIEWS = [0, 1, 3, 4, 5, 7]
LS_FRAME = (240, 1024)


def longsword_class_from_colors():
    """Exact 6-colour class map -> per-texel class index into LS_PALETTE."""
    pa = np.asarray(Image.open(J(LS_FINAL, "provenance_atlas.png")).convert("RGB"))
    flat = pa.reshape(-1, 3)
    sel = {name: np.all(flat == rgb, axis=1) for name, rgb in LS_PALETTE}
    n_other = flat.shape[0] - int(sum(s.sum() for s in sel.values()))
    if not (n_other == 0):
        raise AssertionError(
            f"ANDON: {n_other:,} texels outside the 6 declared class colours")
    for name, want in LS_MIX.items():
        got = int(sel[name].sum())
        if not (got == want):
            raise AssertionError(
                f"ANDON: provenance atlas has {got:,} {name} texels; the record "
                f"(run/final/provenance_legend.json, E14 Ruling 31b) says {want:,}")
    valid = int(sum(sel[n].sum() for n in LS_MIX))
    if not (valid == LS_VALID):
        raise AssertionError(
            f"ANDON: classes partition {valid:,} texels, not {LS_VALID:,}")
    cls = np.zeros(flat.shape[0], dtype=np.uint8)
    for i, (name, _rgb) in enumerate(LS_PALETTE):
        if i:
            cls[sel[name]] = i
    print(f"[X4] class map from the exact 6-colour atlas; all five non-background "
          f"class counts reproduce the record to the texel over {valid:,} valid")
    return cls, pa, sel


def arm_longsword(args):
    out_root = args.out
    os.makedirs(out_root, exist_ok=True)
    print(f"[X4] longsword dense export -> {out_root}")

    cls_flat, pa, sel = longsword_class_from_colors()
    reference = sel["stage1b_projection"] | sel["garnet_reprojection"] | sel["collar_repair"]
    n_ref = int(reference.sum())

    # ── the owner sidecar, chosen on evidence and reported either way ──────────
    owner = np.load(J(LS_STAGE1, "stage1b_atlas_owner.npy")).reshape(-1)
    alt = np.load(J(r"E:\AI\training\facet_next\E14_strokes\garnet",
                    "reproj_corrected", "atlas_owner.npy")).reshape(-1)
    owner_report = {}
    for tag, arr in (("stage1b", owner), ("reprojection", alt)):
        own = arr >= 0
        owner_report[tag] = {
            "owned": int(own.sum()),
            "reference_unowned": int((reference & ~own).sum()),
            "owned_outside_reference": int((own & ~reference).sum()),
            "ids": sorted(int(x) for x in np.unique(arr[own])),
        }
        print(f"[X4] owner sidecar [{tag}]: owned {owner_report[tag]['owned']:,}  "
              f"reference unowned {owner_report[tag]['reference_unowned']:,}  "
              f"owned outside reference {owner_report[tag]['owned_outside_reference']:,}")
    # the dragon's ANDON, on the array this subject declares
    unowned = owner_report["stage1b"]["reference_unowned"]
    if not (unowned == 0):
        raise AssertionError(
            f"ANDON: {unowned:,} reference texels carry sidecar owner -1 — the sidecar "
            f"disagrees with the class map")
    stray = owner_report["stage1b"]["owned_outside_reference"]
    if not (stray == 0):
        raise AssertionError(
            f"ANDON: {stray:,} texels outside the reference class carry an owner id")
    if not (owner_report["stage1b"]["ids"] == list(range(len(LS_OWNER_VIEWS)))):
        raise AssertionError(
            f"ANDON: owner ids {owner_report['stage1b']['ids']} are not 0..{len(LS_OWNER_VIEWS)-1}")

    # the id -> view mapping VERIFIED against stage 1b's own committed counts,
    # never assumed: a consumer reading owner id 2 as "view 2" would read the
    # EXCLUDED view (Ruling 20).
    legend = json.load(open(J(LS_STAGE1, "stage1b_provenance_legend.json"), encoding="utf-8"))
    for k, view in enumerate(LS_OWNER_VIEWS):
        got = int((owner == k).sum())
        want = int(legend["committed"][str(view)])
        if not (got == want):
            raise AssertionError(
                f"ANDON: owner id {k} covers {got:,} texels; stage 1b's legend records "
                f"{want:,} committed for view {view} — the id->view mapping is not "
                f"positional as assumed")
    print(f"[X4] owner id -> view mapping VERIFIED positionally against stage 1b's "
          f"legend: {dict(enumerate(LS_OWNER_VIEWS))}, every count exact; "
          f"{n_ref:,} reference texels all owned")

    # X-H3's lossless leg: truecolor provenance atlas -> indexed, pixel-identical.
    idx = np.zeros(pa.shape[:2], dtype=np.uint8)
    for i, (_, rgb) in enumerate(LS_PALETTE):
        idx[np.all(pa == rgb, axis=-1)] = i
    ipath = J(out_root, "provenance_atlas_indexed.png")
    write_indexed_png(ipath, idx, LS_PALETTE)
    back = np.asarray(Image.open(ipath).convert("RGB"))
    if not (np.array_equal(back, pa)):
        raise AssertionError("ANDON: indexed conversion is not lossless")
    print(f"[X4] X-H3 lossless conversion: indexed 6-class atlas pixel-identical to "
          f"the truecolor source through PLTE round-trip")

    # fresh emit states, copied out of the read-only run tree (Ruling 32a: the
    # accepted asset and everything under run/final/ is citable-only).
    src_state = {"asset": J(LS_FINAL, "rstate_final"), "prov": J(LS_FINAL, "rstate_prov")}
    states = {}
    for ch, src in src_state.items():
        st = J(out_root, "_state", ch)
        os.makedirs(st, exist_ok=True)
        for f in ("atlas.png", "holes.png", "styled_mask.npy"):
            shutil.copyfile(J(src, f), J(st, f))
        states[ch] = st
    glb = J(LS_PREP, "prep_uv.glb")

    prof = json.load(open(LS_PROFILE, encoding="utf-8"))
    prod = prof["tools"]["cull_unseen.py"]["production"]["value"]
    cams, seen = [], set()
    for spec in prod.split(";"):
        y, e = (float(x) for x in spec.split(","))
        if (y, e) not in seen:
            seen.add((y, e))
            cams.append((y, e))
    print(f"[X4] camera superset derived from profiles/prop.json: {len(cams)} cameras "
          f"x {len(states)} channels")

    caster = IdCaster(prep=LS_PREP)
    anchors, renders, frames = [], [], set()
    for (y, e) in cams:
        vid = key_of(y, e)
        dest = J(out_root, "views", vid)
        os.makedirs(dest, exist_ok=True)
        for ch in states:
            jb = run_emit(states[ch], y, e, glb, prep=LS_PREP, profile=LS_PROFILE)
            cj = json.load(open(J(jb, "cam.json")))
            frames.add((cj["W"], cj["H"]))
            if not ((cj["W"], cj["H"]) == LS_FRAME):
                raise AssertionError(
                    f"ANDON: {vid} {ch} emitted a {cj['W']}x{cj['H']} frame, not "
                    f"{LS_FRAME[0]}x{LS_FRAME[1]} — Ruling 29c's unprofiled-emit trap")
            shutil.copyfile(J(jb, "render.png"), J(dest, f"{ch}.png"))
            if ch == "asset":
                shutil.copyfile(J(jb, "hit.png"), J(dest, "silhouette.png"))
                shutil.copyfile(J(jb, "cam.json"), J(dest, "cam.json"))
            # RECORDED-ARTIFACT ANCHOR: the eight route yaws were rendered through
            # this same path for the Gate-1 sheets (handoff 9 step 4).
            sub = {"asset": "render_final", "prov": "render_prov"}[ch]
            rec = J(LS_FINAL, sub, f"flat_{int(y)}.png")
            if e == 0 and float(y).is_integer() and os.path.exists(rec):
                same = bytes_equal(J(dest, f"{ch}.png"), rec)
                anchors.append({"view": vid, "channel": ch,
                                "recorded": f"{sub}/flat_{int(y)}.png",
                                "byte_identical": same})
                if not same:
                    a = np.asarray(Image.open(J(dest, f"{ch}.png")).convert("RGB"),
                                   dtype=np.int16)
                    b = np.asarray(Image.open(rec).convert("RGB"), dtype=np.int16)
                    if a.shape == b.shape:
                        dd = np.abs(a - b).max(axis=-1)
                        print(f"[X4] ANCHOR MISMATCH {vid} {ch}: "
                              f"{(dd > 0).sum():,} px differ, max {dd.max()} levels")
                        anchors[-1]["px_differing"] = int((dd > 0).sum())
                        anchors[-1]["max_levels"] = int(dd.max())
                    else:
                        print(f"[X4] ANCHOR MISMATCH {vid} {ch}: shapes "
                              f"{a.shape} vs {b.shape}")
        cam = json.load(open(J(dest, "cam.json")))
        adm = view_products(caster, cam, None, owner, dest, vid,
                            palette=LS_PALETTE, class_flat=cls_flat)
        renders.append({"id": vid, "yaw": y, "el": e,
                        "admission": adm["class_share_pct"]})
        s = adm["class_share_pct"]
        print(f"[X4] {vid}: stage1b {s['stage1b_projection']:.2f}%  "
              f"garnet {s['garnet_reprojection']:.2f}%  repair {s['collar_repair']:.2f}%  "
              f"brush {s['brush']:.2f}%  dilation {s['dilation']:.2f}%  "
              f"figure {adm['figure_px']:,}px", flush=True)

    n_anch = sum(1 for a in anchors if a["byte_identical"])
    print(f"[X4] recorded-artifact anchors: {n_anch}/{len(anchors)} byte-identical")
    print(f"[X4] frames emitted: {sorted(frames)} (asserted {LS_FRAME} on every emit)")

    # X-H1 purity spot check: a SECOND fresh state, a different directory, one
    # camera. (Comparing a file to itself would return identical however the export
    # behaved — the two files below are produced independently.)
    st2 = J(out_root, "_state", "asset_rerun")
    os.makedirs(st2, exist_ok=True)
    for f in ("atlas.png", "holes.png", "styled_mask.npy"):
        shutil.copyfile(J(src_state["asset"], f), J(st2, f))
    jb2 = run_emit(st2, 0.0, 0.0, glb, prep=LS_PREP, profile=LS_PROFILE)
    pure = bytes_equal(J(out_root, "views", key_of(0, 0), "asset.png"),
                       J(jb2, "render.png"))
    print(f"[X4] X-H1 spot check (independent fresh state, yaw 0): byte-identical {pure}")
    if not pure:
        print("[X4] HALT — the export is not a pure function on this subject.")
        return 1

    json.dump({"cameras": len(cams), "channels": sorted(states),
               "frame": list(LS_FRAME),
               "owner_channel": "numeric present (view_owner.npy = stage 1b's "
                                "owner sidecar + per-view owner_id/loss_mask); no "
                                "display atlas exists for this subject and none was "
                                "synthesized",
               "owner_id_to_view": {str(k): v for k, v in enumerate(LS_OWNER_VIEWS)},
               "owner_sidecar_comparison": owner_report,
               "class_palette": [{"name": n, "rgb": list(rgb)} for n, rgb in LS_PALETTE],
               "recorded_anchors": anchors,
               "purity_spot_check_byte_identical": bool(pure),
               "renders": renders},
              open(J(out_root, "x4_run.json"), "w"), indent=1)
    print(f"[X4] wrote {J(out_root, 'x4_run.json')}")
    return 0


def step0(args, claim, owner, valid):
    print("[step0] E11 one-view anchor — beam, every channel, HALT on any digit")
    base = J(args.out, "_step0")
    rec = {ch: J(STROKE, "sheet", ch, "job_y+000_e+00") for ch in CHANNELS}

    # X-H1: two independent emits from fresh states must be byte-identical.
    jobs = {}
    for attempt in ("a", "b"):
        for ch in CHANNELS:
            st = fresh_state(ch, J(base, attempt, ch))
            jobs[(attempt, ch)] = run_emit(st, 0.0, 0.0, args.glb)
            print(f"[step0] emitted {ch} ({attempt})")

    ok = True
    for ch in CHANNELS:
        a, b = jobs[("a", ch)], jobs[("b", ch)]
        same = bytes_equal(J(a, "render.png"), J(b, "render.png"))
        print(f"[step0] X-H1 {ch}: two fresh emits byte-identical: {same}")
        ok &= same

    # X-H2 + the silhouette anchor: against the recorded artifacts.
    for ch in CHANNELS:
        mine = J(jobs[("a", ch)], "render.png")
        theirs = J(rec[ch], "render.png")
        same = bytes_equal(mine, theirs)
        print(f"[step0] ANCHOR render[{ch}] byte-identical to recorded: {same}"
              f"  ({sha256(mine)[:12]} vs {sha256(theirs)[:12]})")
        ok &= same
    sil_mine = J(jobs[("a", "asset")], "hit.png")
    sil_rec = J(rec["asset"], "hit.png")
    same = bytes_equal(sil_mine, sil_rec)
    print(f"[step0] ANCHOR silhouette byte-identical to Step 0.2's: {same}")
    ok &= same
    for ch in ("prov", "owner"):
        same = bytes_equal(J(jobs[("a", ch)], "hit.png"), sil_rec)
        print(f"[step0] cross-check hit[{ch}] == hit[asset]: {same}")
        ok &= same

    # the owner slice vs the sidecar — texture space, exact.
    tables = owner_atlas_vs_sidecar(claim, owner, valid)
    print(f"[step0] ANCHOR owner atlas is a pure function of (sidecar, claim): "
          f"{len(tables)} distinct value->colour rows, no ambiguity")

    # the exporter's own per-view products, on the anchored beam camera.
    caster = IdCaster()
    cam = json.load(open(J(jobs[("a", "asset")], "cam.json")))
    os.makedirs(J(base, "products"), exist_ok=True)
    adm = view_products(caster, cam, claim, owner, J(base, "products"), key_of(0, 0))
    print(f"[step0] beam admission shares: {adm['class_share_pct']}  "
          f"owner boundary px {adm['owner_boundary_px']:,}")

    if not ok:
        print("[step0] HALT — a digit differed. Reported above; nothing proceeds.")
        return 1
    print("[step0] ALL ANCHORS PASS")
    json.dump({"anchors": "pass", "owner_tables": tables, "beam_admission": adm},
              open(J(base, "step0.json"), "w"), indent=1)
    return 0


def arm_x1(args, claim, owner, valid):
    prof = json.load(open(PROFILE, encoding="utf-8"))
    prod = prof["tools"]["cull_unseen.py"]["production"]["value"]
    cams = []
    seen = set()
    for spec in prod.split(";"):
        y, e = (float(x) for x in spec.split(","))
        if (y, e) not in seen:
            seen.add((y, e))
            cams.append((y, e))
    print(f"[X1] full superset export: {len(cams)} cameras x {len(CHANNELS)} channels")

    caster = IdCaster()
    states = {ch: fresh_state(ch, J(args.out, "_state", ch)) for ch in CHANNELS}
    renders = []
    for (y, e) in cams:
        vid = key_of(y, e)
        row = {"id": vid, "yaw": y, "el": e}
        for ch in CHANNELS:
            job = run_emit(states[ch], y, e, args.glb)
            dest = J(args.out, "views", vid)
            os.makedirs(dest, exist_ok=True)
            shutil.copyfile(J(job, "render.png"), J(dest, f"{ch}.png"))
            if ch == "asset":
                shutil.copyfile(J(job, "hit.png"), J(dest, "silhouette.png"))
                shutil.copyfile(J(job, "cam.json"), J(dest, "cam.json"))
        cam = json.load(open(J(args.out, "views", vid, "cam.json")))
        adm = view_products(caster, cam, claim, owner, J(args.out, "views", vid), vid)
        row["admission"] = adm["class_share_pct"]
        renders.append(row)
        print(f"[X1] {vid}: reference {adm['class_share_pct']['reference']:.2f}%  "
              f"figure {adm['figure_px']:,}px", flush=True)

    json.dump({"cameras": len(cams), "renders": renders},
              open(J(args.out, "x1_run.json"), "w"), indent=1)
    print(f"[X1] wrote {J(args.out, 'x1_run.json')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
