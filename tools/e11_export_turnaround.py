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
    assert back.mode == "P", "ANDON: indexed write came back non-indexed"
    plte = back.getpalette()[:len(palette) * 3]
    want = [c for _, rgb in palette for c in rgb]
    assert plte == want, f"ANDON: {path} PLTE != declared palette"
    assert np.array_equal(np.asarray(back), class_map), \
        f"ANDON: {path} pixels changed through the indexed write"


def view_products(caster, cam, claim_flat, owner_flat, out_dir, view_id, palette=None):
    """The exact per-view maps: indexed class render, owner slice, loss mask, shares.

    owner_flat=None means the asset has NO owner sidecar (W3) — owner products are
    then honestly ABSENT, not synthesized (the spec's X2 clause verbatim)."""
    palette = palette or CLAIM_CLASSES
    tex, hit = caster.texel_ids(cam)
    H, W = hit.shape
    cls = np.zeros((H, W), dtype=np.uint8)          # background
    ok = tex >= 0
    t = tex[ok]
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
        assert len(cols) == 1, (
            f"ANDON: owner atlas has {len(cols)} colours for sidecar view {v} "
            f"on stage-1 texels — not a pure function of the sidecar")
        tables[f"view_{v}"] = [int(c) for c in cols[0]]
    bad = valid_flat & (claim_flat == 0) & (owner_flat < 0)
    assert not bad.any(), (
        f"ANDON: {int(bad.sum()):,} stage-1 texels carry sidecar owner -1 — "
        f"the sidecar disagrees with the claim map")
    for k in range(1, 7):
        sel = valid_flat & (claim_flat == k)
        if not sel.any():
            continue
        cols = np.unique(oa[sel], axis=0)
        assert len(cols) == 1, f"ANDON: stroke {k} renders {len(cols)} colours"
        tables[f"stroke_{k}"] = [int(c) for c in cols[0]]
    sel = valid_flat & (claim_flat == 255)
    cols = np.unique(oa[sel], axis=0)
    assert len(cols) == 1, f"ANDON: dilation renders {len(cols)} colours"
    tables["dilation"] = [int(c) for c in cols[0]]
    return tables


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step0", action="store_true", help="one-view anchor; HALT on any digit")
    ap.add_argument("--arm", choices=["X1", "X2"], help="X1: galleon superset; X2: W3 dense")
    ap.add_argument("--claim", help="anchored claim.npy (per-stroke replay; X1/step0)")
    ap.add_argument("--glb", default=J(PREP, "prep_uv.glb"),
                    help="the GLB emit renders with; the Step-0 byte anchor is what "
                         "verifies this operand is the recorded one")
    ap.add_argument("--out", default=J(STROKE, "export", "turnaround"))
    args = ap.parse_args()

    if args.arm == "X2":
        return arm_x2(args)

    assert args.claim, "ANDON: --claim is required for the galleon legs"
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
    assert n_other == 0, f"ANDON: {n_other:,} pixels outside the 4 measured class colours"
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
    assert np.array_equal(back, pa), "ANDON: indexed conversion is not lossless"
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
