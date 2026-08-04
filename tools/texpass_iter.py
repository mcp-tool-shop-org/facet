"""TEXTURE-SPACE PASS, stage 2 write-head — emit / commit / selftest.

The progressive loop's deterministic half. The atlas is the single accumulating
state; diffusion only ever paints PIXELS of an emitted view, and commit writes
those pixels into HOLE texels only — styled texels are never overwritten.

  emit    — render the asset wearing the current atlas from (yaw, el) + the
            projected hole mask (dilated) + cam.json  ->  an inpaint job
  commit  — take the edited render, write masked hole texels back into the
            atlas (visibility + facing tested), shrink the hole map
  selftest— emit; fake-inpaint by local blur; commit; assert styled texels
            byte-identical and holes strictly shrink. Run before any real brush.

Framing = the twin/turn_render convention (v_ext = bbox_z*1.204, 752x1024),
so emitted views are drop-in for the measured Qwen+saltroad graphs.
Standards compliance: see bake_hero_fuse.py (same stage family).

  texpass_iter.py emit    --state DIR --prep DIR --glb packed.glb --yaw 90 [--el 0]
  texpass_iter.py commit  --state DIR --prep DIR --edited img.png --cam cam.json
  texpass_iter.py selftest --state DIR --prep DIR --glb packed.glb [--yaw 90]

--state holds: atlas.png, holes.png, styled_mask.npy (project_twins output copied in).
"""
import argparse
import json
import os
import shutil

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import (distance_transform_edt, gaussian_filter, maximum_filter,
                           minimum_filter)

Image.MAX_IMAGE_PIXELS = None
W, H = 752, 1024
D = 2.0

ap = argparse.ArgumentParser()
ap.add_argument("mode", choices=["emit", "commit", "selftest"])
ap.add_argument("--state", required=True)
ap.add_argument("--prep", required=True)
ap.add_argument("--glb", help="packed GLB with UVs (emit/selftest)")
ap.add_argument("--yaw", type=float, default=90.0)
ap.add_argument("--el", type=float, default=0.0)
ap.add_argument("--edited", help="inpainted render (commit)")
ap.add_argument("--cam", help="cam.json from the matching emit (commit)")
ap.add_argument("--facing-min", type=float, default=0.25,
                help="commit acceptance: grazing texels near the silhouette were the "
                     "white-fleck class (first full loop, 2026-08-04)")
ap.add_argument("--edge-dist", type=float, default=4.0,
                help="commit: reject brush pixels this close to the figure edge — "
                     "they carry background-grey mix")
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--mask-dilate", type=int, default=9)
ap.add_argument("--thin-extent", type=float, default=0.0,
                help="emit: withhold from diffusion any pixel whose figure extent "
                     "ALONG THE VIEW RAY is below this (std-frame units, figure "
                     "~1.0 tall). 0 = off. This is the blade policy — thin "
                     "hard-surface props take projected/dilated colour, never "
                     "invented content — expressed as geometry instead of as the "
                     "hardcoded pixel rectangle it used to be. Measured by casting "
                     "the CAMERA's rays from the front plane and again from the "
                     "back plane: extent = 2*D - t_front - t_back. Two probes that "
                     "look like the obvious ones both FAILED on this mesh and are "
                     "recorded in tools/superseded/texpass_thin_mask.py — a probe "
                     "along the surface normal measures the triangle spacing "
                     "(median 0.0020 against a median edge length of 0.0029), and "
                     "any containment test is meaningless because prep_uv.glb is "
                     "seam-split (293,099 verts for 287,170 faces) so signed "
                     "distance at the figure's own bbox centre comes back POSITIVE. "
                     "Camera rays need neither a normal nor an interior.")
args = ap.parse_args()

S = args.state
atlas = np.asarray(Image.open(os.path.join(S, "atlas.png")).convert("RGB"),
                   dtype=np.float32) / 255.0
holes = np.asarray(Image.open(os.path.join(S, "holes.png")).convert("L"),
                   dtype=np.float32) / 255.0
styled = np.load(os.path.join(S, "styled_mask.npy"))
RES = atlas.shape[0]

meta = json.load(open(os.path.join(args.prep, "meta.json")))
mask_np = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5


def basis(yaw_d, el_d):
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    look = -cd / np.linalg.norm(cd)
    up0 = np.array([0.0, 0.0, 1.0])
    right = np.cross(look, up0)
    right /= np.linalg.norm(right) + 1e-12
    up = np.cross(right, look)
    return cd, look, right, up / (np.linalg.norm(up) + 1e-12)


def load_scene():
    m = trimesh.load(args.glb, force="mesh", process=False)
    v = np.asarray(m.vertices, dtype=np.float64)
    f = np.asarray(m.faces, dtype=np.int64)
    uv = np.asarray(m.visual.uv, dtype=np.float64)
    vmax = np.abs(v).max()
    v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / vmax * 0.5
    rs = o3d.t.geometry.RaycastingScene()
    rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                     o3d.core.Tensor(f.astype(np.uint32)))
    return v, f, uv, rs


def bilin(img, x, y):
    Hh, Ww = img.shape[:2]
    x = np.clip(x, 0.0, Ww - 1.001)
    y = np.clip(y, 0.0, Hh - 1.001)
    x0, y0 = x.astype(np.int64), y.astype(np.int64)
    fx, fy = x - x0, y - y0
    if img.ndim == 3:
        fx, fy = fx[:, None], fy[:, None]
    return (img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy)
            + img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy)


def emit(yaw, el, tag="job"):
    v, f, uv, rs = load_scene()
    blo, bhi = v.min(axis=0), v.max(axis=0)
    bmid = (blo + bhi) / 2
    v_ext = (bhi[2] - blo[2]) * 1.204
    h_ext = v_ext * (W / H)
    cd, look, right, up = basis(yaw, el)
    xs = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
    ys = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
    gx, gy = np.meshgrid(xs, ys)
    origins = (bmid[None, None, :] + gx[..., None] * right[None, None, :]
               + gy[..., None] * up[None, None, :] - look[None, None, :] * D)
    dirs = np.broadcast_to(look, origins.shape)
    ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [origins, dirs], axis=-1).reshape(-1, 6).astype(np.float32)))
    prim = ans["primitive_ids"].numpy().reshape(H, W)
    buv = ans["primitive_uvs"].numpy().reshape(H, W, 2)
    hit = np.isfinite(ans["t_hit"].numpy().reshape(H, W))
    render = np.full((H, W, 3), 0.42, dtype=np.float32)
    holemask = np.zeros((H, W), dtype=np.float32)
    if hit.any():
        tri = f[prim[hit]]
        w_u = buv[hit][:, 0:1]
        w_v = buv[hit][:, 1:2]
        w0 = 1.0 - w_u - w_v
        uvp = w0 * uv[tri[:, 0]] + w_u * uv[tri[:, 1]] + w_v * uv[tri[:, 2]]
        ax = uvp[:, 0] * RES - 0.5
        ay = (1.0 - uvp[:, 1]) * RES - 0.5
        render[hit] = bilin(atlas, ax, ay)
        holemask[hit] = bilin(holes, ax, ay)
    hm = (maximum_filter(holemask, size=args.mask_dilate) > 0.05) & hit
    thin = np.zeros((H, W), dtype=bool)
    if args.thin_extent > 0.0:
        # Second pass with the SAME grid, fired from the far plane back toward the
        # camera. origins sit at -look*D from bmid, so +look*2D lands on +look*D.
        ansB = rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [origins + look[None, None, :] * (2 * D),
             np.broadcast_to(-look, origins.shape)],
            axis=-1).reshape(-1, 6).astype(np.float32)))
        tB = ansB["t_hit"].numpy().reshape(H, W)
        tF = ans["t_hit"].numpy().reshape(H, W)
        both = hit & np.isfinite(tB)
        ext = np.full((H, W), np.inf, dtype=np.float64)
        ext[both] = 2 * D - tF[both] - tB[both]
        thin = (ext < args.thin_extent) & hit
        hm = hm & ~thin
        print(f"[emit] thin-extent {args.thin_extent}: withheld "
              f"{int(thin.sum()):,} px ({thin.sum() / max(int(hit.sum()), 1) * 100:.1f}%"
              f" of figure) from diffusion", flush=True)
    outdir = os.path.join(S, f"{tag}_y{int(yaw):+04d}_e{int(el):+03d}")
    os.makedirs(outdir, exist_ok=True)
    Image.fromarray((render * 255).round().astype(np.uint8)).save(
        os.path.join(outdir, "render.png"))
    Image.fromarray((hm * 255).astype(np.uint8)).save(os.path.join(outdir, "mask.png"))
    # THE GEOMETRY HIT MASK (E08 Amendment 32). emit RENDERED the figure, so it knows
    # exactly where surface is — no keying, no threshold, no dependence on how the brush
    # lit anything. commit intersects the brush output's keyed mask with this before its
    # distance transform, which is Amendment 26's fix at this site: paint on no surface
    # cannot be asked whether it is trustworthy, and must not set the boundary of a
    # distance field that decides trust for texels that DO exist.
    Image.fromarray((hit * 255).astype(np.uint8)).save(os.path.join(outdir, "hit.png"))
    if args.thin_extent > 0.0:
        Image.fromarray((thin * 255).astype(np.uint8)).save(
            os.path.join(outdir, "thin.png"))
    json.dump({"yaw": yaw, "el": el, "v_ext": v_ext, "h_ext": h_ext,
               "bmid": bmid.tolist(), "W": W, "H": H},
              open(os.path.join(outdir, "cam.json"), "w"))
    print(f"[emit] {outdir}: {int(hit.sum()):,} figure px, "
          f"{int(hm.sum()):,} hole px to inpaint", flush=True)
    return outdir


def commit(edited_path, cam_path):
    cam = json.load(open(cam_path))
    edited = np.asarray(Image.open(edited_path).convert("RGB"),
                        dtype=np.float32) / 255.0
    jobmask = np.asarray(Image.open(
        os.path.join(os.path.dirname(cam_path), "mask.png")).convert("L"),
        dtype=np.float32) / 255.0
    v, f, uv, rs = load_scene() if args.glb else (None,) * 4
    if rs is None:
        m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"),
                         force="mesh", process=False)
        v = np.asarray(m.vertices, dtype=np.float64)
        fc = np.asarray(m.faces, dtype=np.int64)
        v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
        rs = o3d.t.geometry.RaycastingScene()
        rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                         o3d.core.Tensor(fc.astype(np.uint32)))
    pos_e = np.load(os.path.join(args.prep, "pos.npy"))
    nor_e = np.load(os.path.join(args.prep, "nor.npy"))
    lo = np.array(meta["lo"])
    hi = np.array(meta["hi"])
    hole_flat = (holes.reshape(-1) > 0.5) & mask_np.reshape(-1)
    hidx = np.where(hole_flat)[0]
    P = (pos_e.reshape(-1, 3)[hidx].astype(np.float64)
         * (hi - lo) + lo) / meta["maxabs"] * 0.5
    Nn = nor_e.reshape(-1, 3)[hidx].astype(np.float64) * 2.0 - 1.0
    Nn /= np.linalg.norm(Nn, axis=1, keepdims=True) + 1e-12
    cd, look, right, up = basis(cam["yaw"], cam["el"])
    dtc = -look
    facing = Nn @ dtc
    keep = facing > args.facing_min
    hidx, P, Nn, facing = hidx[keep], P[keep], Nn[keep], facing[keep]
    origins = (P + Nn * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
    t_hit = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [origins, np.broadcast_to(dtc.astype(np.float32), origins.shape)],
        axis=1)))["t_hit"].numpy()
    vis = ~np.isfinite(t_hit)
    hidx, P = hidx[vis], P[vis]
    bmid = np.array(cam["bmid"])
    px = ((P - bmid) @ right / cam["h_ext"] + 0.5) * cam["W"] - 0.5
    py = (0.5 - (P - bmid) @ up / cam["v_ext"]) * cam["H"] - 0.5
    injob = bilin(jobmask, px, py) > 0.5
    hidx, px, py = hidx[injob], px[injob], py[injob]
    # figure-mask + edge-distance guard on the BRUSH OUTPUT: silhouette pixels mix
    # background grey and commit as white flecks on grazing texels (measured on the
    # first full loop). Same guard family as project_twins' stage-1 fix.
    c8 = np.concatenate([edited[:8, :8].reshape(-1, 3), edited[:8, -8:].reshape(-1, 3)])
    bg = np.median(c8, axis=0)
    # ANDON, IN THE TOOL THAT PERFORMS THE IRREVERSIBLE STEP (E08 Amendment 32). The bg
    # estimator above reads exactly these 8x8 corners; if the inpaint moved them, the
    # estimator's operand is not the emitted backdrop and everything downstream keys off a
    # colour the pipeline did not choose. This check CANNOT be walked past by a shell — it
    # was a separate script once, a chained call skipped it after it fired, and 47,020
    # texels committed behind a fired gate. A gate a scripting accident can separate from
    # the action it gates is not a gate.
    ep_dir = os.path.dirname(os.path.abspath(edited_path))
    rpath = os.path.join(ep_dir, "render.png")
    if os.path.exists(rpath):
        emr = np.asarray(Image.open(rpath).convert("RGB"), dtype=np.float32) / 255.0
        assert emr.shape == edited.shape, (
            f"ANDON: edited {edited.shape} != emitted {emr.shape} — the brush resized the "
            f"frame, so nothing maps back")
        c8e = np.concatenate([emr[:8, :8].reshape(-1, 3), emr[:8, -8:].reshape(-1, 3)])
        d_corner = float(np.abs(np.median(c8e, axis=0) - bg).max() * 255.0)
        assert d_corner <= 1.0, (
            f"ANDON: the 8x8 corner medians the background estimator reads moved "
            f"{d_corner:.2f} levels between the emitted render and the brush output. The "
            f"estimator's operand is no longer the emitted backdrop; its key, its erosion "
            f"and every texel colour downstream are keyed off a colour the pipeline did "
            f"not choose. HALT.")
        # DEMOTED TO A DIAGNOSTIC (E08 Amendment 32). The whole-image outside-figure
        # residual was a halt for exactly one stroke; the intersection below forecloses the
        # direction it watched, and a halt on a foreclosed direction fires on correct work
        # (A26/A27, third instance). Its verdict on stroke 7 AS COMMITTED stands unrevised.
        # ⚠ THE OPERAND IS GEOMETRY, NOT COLOUR (corrected 2026-08-04, after it produced a
        # FALSE ANDON that a chained shell then committed past). The first version defined
        # "outside the figure" as `|render - 0.42| < 1.5/255` — colour as a proxy for
        # absence of surface. But 0.42 is ALSO project_twins' --hole-grey, so an unpainted
        # HOLE ON REAL SURFACE renders at exactly the background value and is
        # indistinguishable from background by colour, by construction. Measured on
        # stroke 7: 8,331 px the check called "outside the figure" are geometry hits, 7,832
        # of them inside the job mask — i.e. holes the brush was explicitly told to paint.
        # The 202 px blob it halted on was 100% hit and 100% masked: the brush doing its job.
        # `hit` answers "is there surface" exactly, and emit saves it. Test the property,
        # not a proxy for it.
        out_m = np.ones(edited.shape[:2], dtype=bool)
        hp0 = os.path.join(ep_dir, "hit.png")
        if os.path.exists(hp0):
            h0 = (np.asarray(Image.open(hp0).convert("L"), dtype=np.float32) / 255.0) > 0.5
            out_m = maximum_filter(h0.astype(np.float32), size=9) < 0.5
        if out_m.any():
            r_out = np.abs(edited - emr).max(axis=-1)[out_m]
            print(f"[commit] diagnostic — outside-figure residual mean "
                  f"{r_out.mean() * 255:.3f} lv, max {r_out.max() * 255:.1f} lv, "
                  f"over-4lv {int((r_out > 4 / 255).sum()):,} px  (NOT a halt)", flush=True)
    fm_e = minimum_filter(
        (np.abs(edited - bg).max(axis=-1) > 0.06).astype(np.float32), size=5)
    # ⚠ THE A26 FIX AT THIS SITE (E08 Amendment 32, the sixth keyed-mask distance transform).
    # Intersect the brush output's keyed figure with the GEOMETRY emit rendered. Measured
    # trigger: stroke 7's elevated camera saw through the gap between the raised greatsword
    # and the head, the inpaint filled that pocket at 84.5 levels, keying put it in `fm_e`,
    # and connected near the rim it inflates dist_e — weakening the very erosion that
    # decides commit-trust, exactly where the sword meets the head. Same object as the
    # twin_6 cast shadow, same fix. Geometry has no threshold and no dependence on lighting.
    hpath = os.path.join(ep_dir, "hit.png")
    if os.path.exists(hpath):
        hitm = (np.asarray(Image.open(hpath).convert("L"), dtype=np.float32) / 255.0) > 0.5
        n0 = int((fm_e > 0.5).sum())
        fm_e = ((fm_e > 0.5) & hitm).astype(np.float32)
        n1 = int((fm_e > 0.5).sum())
        # ASCII ONLY IN PRINTS. Fourth time this session a non-cp1252 glyph in a print has
        # raised UnicodeEncodeError on a Windows console — and this one crashed commit
        # mid-replay on all six strokes. The comment lives here as well as in the three
        # diagnostics that hit it first, because a note in another file did not help.
        print(f"[commit] trust mask AND geometry: {n0:,} -> {n1:,} px "
              f"(-{n0 - n1:,} keyed on no surface)", flush=True)
    else:
        print(f"[commit] NOTE: no hit.png beside {os.path.basename(edited_path)} — this "
              f"job predates Amendment 32's emit; the trust mask is NOT intersected",
              flush=True)
    dist_e = distance_transform_edt(fm_e > 0.5).astype(np.float32)
    ok = bilin(dist_e, px, py) >= args.edge_dist
    hidx, px, py = hidx[ok], px[ok], py[ok]
    col = bilin(edited, px, py).astype(np.float32)
    before = int((holes > 0.5).sum())
    a2 = atlas.reshape(-1, 3).copy()
    a2[hidx] = col
    h2 = holes.reshape(-1).copy()
    h2[hidx] = 0.0
    s2 = styled.reshape(-1).copy()
    s2[hidx] = True
    protected = styled.reshape(-1)
    assert not protected[hidx].any(), "ANDON: commit tried to touch styled texels"
    shutil.copy(os.path.join(S, "atlas.png"), os.path.join(S, "atlas.prev.png"))
    Image.fromarray((a2.reshape(RES, RES, 3) * 255).round().astype(np.uint8)).save(
        os.path.join(S, "atlas.png"))
    Image.fromarray((h2.reshape(RES, RES) * 255).astype(np.uint8)).save(
        os.path.join(S, "holes.png"))
    np.save(os.path.join(S, "styled_mask.npy"), s2.reshape(RES, RES))
    after = int((h2 > 0.5).sum())
    print(f"[commit] wrote {len(hidx):,} texels; holes {before:,} -> {after:,}",
          flush=True)
    assert after < before or len(hidx) == 0, "ANDON: holes did not shrink"
    return len(hidx)


if args.mode == "emit":
    emit(args.yaw, args.el)
elif args.mode == "commit":
    commit(args.edited, args.cam)
else:
    job = emit(args.yaw, args.el, tag="selftest")
    r = np.asarray(Image.open(os.path.join(job, "render.png")).convert("RGB"),
                   dtype=np.float32) / 255.0
    jm = np.asarray(Image.open(os.path.join(job, "mask.png")).convert("L"),
                    dtype=np.float32) / 255.0
    fake = np.stack([gaussian_filter(r[..., k], 12.0) for k in range(3)], axis=-1)
    edited = np.where(jm[..., None] > 0.5, fake, r)
    ep = os.path.join(job, "fake_inpaint.png")
    Image.fromarray((edited * 255).round().astype(np.uint8)).save(ep)
    pre_styled = styled.copy()
    pre_atlas = atlas.copy()
    n = commit(ep, os.path.join(job, "cam.json"))
    a_new = np.asarray(Image.open(os.path.join(S, "atlas.png")).convert("RGB"),
                       dtype=np.float32) / 255.0
    diff = np.abs(a_new - pre_atlas)[pre_styled].max() if pre_styled.any() else 0
    print(f"[selftest] styled-texel max delta {diff:.6f} (must be ~0), "
          f"committed {n:,}", flush=True)
    assert diff < 1e-3, "ANDON: selftest — styled texels were modified"
    print("[selftest] PASS — write-head is lossless on styled texels", flush=True)
