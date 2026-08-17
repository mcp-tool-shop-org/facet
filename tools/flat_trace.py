# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Trace a render flat back to the twin that painted it.

WHY THIS EXISTS. Consult #15 / build #15. The Director named flat
olive/gold/green angular patches. E50 measured them 90-99% written.
Written means a twin. Nobody asked which twin, or whether that twin
is flat. The regen spend is correct iff the flats are in the plates.

THE BINARY IS THE WRONG SPLIT (measured 2026-08-17, before this file
existed).

  E50 compared owner_complete_0 to view_0's twin at the SAME xy and
  found the front plate clean. That comparison is the wrong plate
  for most of the olive. In y490-540, x280-360 of owner_complete_0,
  115 olive-classified pixels: owner 6 = 97, owner 0 = 9, owner
  -1 = 8, owner 7 = 1. View 6 is the +X profile (dtc = -X). Those
  97 samples land on view 6's side tunic, mean RGB (100, 114, 68),
  not on a polygonal blob. View 0 facing on the same texels is
  0.60; view 6 facing is 0.68 — not a grazing steal.

  The front twin is not flat there. The colour is in the contributing
  twin as a different green of the same named surface (N3). The
  angular shape is ownership. Completing the four canon holes
  (hands, greaves) does not rename the tunic.

  Asymmetry: 'contributing twin is flat here' would prove the
  defect predates projection for THAT view. 'Front twin is clean
  here' does not poll the other seven. State it, then look.

CALIBRATION CLAIM (run --selftest; T89 pins it).
  Olive pixels in owner_complete_0 [490:540, 280:360] with
  G>90, R>70, B<140, G>=R-10, G>B+15: n==115, owner==6 on 97.
  Fixture: one texel owned by view 1 whose twin is (180, 90, 50);
  trace.owner_twin[y,x] == (180, 90, 50).

  python tools/flat_trace.py --selftest

YES/NO INTERVALS.

  owner            atlas owner.npy, -1 = unowned, 0..7 = view.
  twin sample      nearest pixel of that view's twin after
                   project_point(decode_pos(texel), cam_v).
  same-xy twin     the render view's twin at the render pixel.
                   Not the source unless owner == render view.
  sheet            render | owner-twin | same-xy twin | atlas
                   native crops. Numbers do not replace the sheet.

  python tools/flat_trace.py --render R.png --surfid S.npy \\
         --owner owner.npy --pos pos.npy --meta meta.json \\
         --cams cams.json --twin-dir DIR --out DIR --view 0
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile

import numpy as np
from PIL import Image

_TOOLS = os.path.dirname(os.path.abspath(__file__))
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import atlas_from_aovs as A  # noqa: E402
import s3_composite as S  # noqa: E402
import s3_sheet as SH  # noqa: E402

TOOL_VERSION = "1.0.0"
ATLAS_RES = 4096
CALIBRATION_OLIVE_N = 115
CALIBRATION_OWNER6 = 97
CALIBRATION_BOX = (490, 540, 280, 360)
OLIVE_TWIN_RGB = (180, 90, 50)
STRUCTURE4 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.int32)


class Andon(ValueError):
    pass


def _andon(msg):
    raise Andon("ANDON: " + msg)


def olive_mask(rgb, box=None):
    """Spec of the named class: olive/khaki, not magenta, not dark teal.

    Not seeded from E50's two components. The box is an optional
    window, not the detector's definition.
    """
    a = np.asarray(rgb)
    if box is not None:
        y0, y1, x0, x1 = box
        sl = np.zeros(a.shape[:2], dtype=bool)
        sl[y0:y1, x0:x1] = True
    else:
        sl = np.ones(a.shape[:2], dtype=bool)
    r = a[..., 0].astype(np.int16)
    g = a[..., 1].astype(np.int16)
    b = a[..., 2].astype(np.int16)
    return sl & (g > 90) & (r > 70) & (b < 140) & (g + 10 >= r) & (g > b + 15)


def decode_surfid(surfid, atlas_res=ATLAS_RES):
    s = np.asarray(surfid)
    sil = s >= 0
    row = np.full(s.shape, -1, dtype=np.int64)
    col = np.full(s.shape, -1, dtype=np.int64)
    row[sil] = s[sil] // int(atlas_res)
    col[sil] = s[sil] % int(atlas_res)
    return sil, row, col


def load_twins(twin_dir, n=8):
    out = {}
    for v in range(n):
        p = os.path.join(twin_dir, "view_%d" % v, "twin.png")
        if not os.path.isfile(p):
            p = os.path.join(twin_dir, "twin_%d.png" % v)
        if not os.path.isfile(p):
            _andon("no twin for view %d under %s" % (v, twin_dir))
        out[v] = np.asarray(Image.open(p).convert("RGB"))
    return out


def trace_pixels(ys, xs, surfid, owner, P_atlas, cams, twins, render_view=0):
    """For render pixels (ys, xs): owner, owner-twin sample, same-xy twin."""
    ys = np.asarray(ys, dtype=np.int64)
    xs = np.asarray(xs, dtype=np.int64)
    atlas_res = int(owner.shape[0])
    sil, row, col = decode_surfid(surfid, atlas_res=atlas_res)
    n = ys.size
    rec_owner = np.full(n, -1, dtype=np.int16)
    src = np.zeros((n, 3), dtype=np.uint8)
    same = np.zeros((n, 3), dtype=np.uint8)
    pxv = np.full(n, np.nan)
    pyv = np.full(n, np.nan)
    H, W = surfid.shape
    inside = (ys >= 0) & (xs >= 0) & (ys < H) & (xs < W)
    if not inside.all():
        _andon("pixel outside render")
    on = sil[ys, xs]
    ah, aw = owner.shape[:2]
    rr = row[ys[on], xs[on]]
    cc = col[ys[on], xs[on]]
    inb = (rr >= 0) & (rr < ah) & (cc >= 0) & (cc < aw)
    tmp = np.full(int(on.sum()), -1, dtype=np.int16)
    tmp[inb] = owner[rr[inb], cc[inb]]
    rec_owner[on] = tmp
    rv = twins[int(render_view)]
    same[:] = rv[ys, xs]
    for v in range(8):
        m = on & (rec_owner == v)
        if not m.any():
            continue
        P = P_atlas[row[ys[m], xs[m]], col[ys[m], xs[m]]]
        key = "view_%d" % v
        if key not in cams:
            _andon("cams missing %s" % key)
        px, py, _z = S.project_point(P, cams[key])
        pxv[m] = px
        pyv[m] = py
        th, tw = twins[v].shape[:2]
        xi = np.clip(np.rint(px).astype(np.int64), 0, tw - 1)
        yi = np.clip(np.rint(py).astype(np.int64), 0, th - 1)
        src[m] = twins[v][yi, xi]
    return {
        "owner": rec_owner,
        "owner_twin": src,
        "same_xy_twin": same,
        "px": pxv,
        "py": pyv,
        "on": on,
    }


def owner_hist(ow):
    return {str(int(v)): int((ow == v).sum())
            for v in range(-1, 8) if (ow == v).any()}


def lcc_count(mask):
    from scipy.ndimage import label as cc_label
    m = np.asarray(mask, dtype=bool)
    tot = int(m.sum())
    if tot == 0:
        return 0, 0
    lab, n = cc_label(m, structure=STRUCTURE4)
    if n == 0:
        return tot, 0
    counts = np.bincount(lab.ravel())
    return tot, int(counts[1:].max()) if counts.size > 1 else 0


def summarize(name, rgb, tr, mask):
    rend = np.asarray(rgb)
    src = tr["owner_twin"]
    same = tr["same_xy_twin"]
    tot, big = lcc_count(mask)
    return {
        "name": name,
        "n": int(mask.sum()) if mask.ndim == 2 else int(len(tr["owner"])),
        "lcc": big,
        "owner_hist": owner_hist(tr["owner"]),
        "render_mean": [float(x) for x in rend.reshape(-1, 3).mean(0)],
        "render_std": float(rend.std()),
        "owner_twin_mean": [float(x) for x in src.mean(0)],
        "owner_twin_std": float(src.std()),
        "same_xy_twin_mean": [float(x) for x in same.mean(0)],
        "same_xy_twin_std": float(same.std()),
        "mean_abs_render_minus_owner_twin": float(
            np.abs(rend.reshape(-1, 3).astype(np.int16) - src.astype(np.int16)).mean()),
        "mean_abs_render_minus_same_xy": float(
            np.abs(rend.reshape(-1, 3).astype(np.int16) - same.astype(np.int16)).mean()),
    }


def paint_from_trace(shape, ys, xs, colours):
    out = np.zeros(shape[:2] + (3,), dtype=np.uint8)
    out[ys, xs] = colours
    return out


def write_sheet(out_dir, tag, render, owner_img, same_img, atlas_img, box, zoom=4):
    y0, y1, x0, x1 = box
    crops = []
    for src, name in (
            (render, "render"),
            (owner_img, "owner_twin"),
            (same_img, "same_xy_twin"),
            (atlas_img, "atlas")):
        c = SH.crop_array(src, [x0, y0, x1, y1], name, name)
        crops.append(SH.nn_zoom(c, zoom))
    # pad to same height
    h = max(c.shape[0] for c in crops)
    w = max(c.shape[1] for c in crops)
    row = []
    for c in crops:
        pad = np.zeros((h, w, 3), dtype=np.uint8)
        pad[:c.shape[0], :c.shape[1]] = c
        row.append(pad)
        row.append(np.zeros((h, 4, 3), dtype=np.uint8))
    sheet = np.concatenate(row[:-1], axis=1)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "sheet_%s.png" % tag)
    Image.fromarray(sheet).save(path)
    return path


def atlas_falsecolor(owner, H, W):
    """View-index as a distinct colour. -1 = black."""
    lut = np.array([
        [0, 0, 0],
        [220, 40, 40], [40, 180, 40], [40, 80, 220], [220, 180, 40],
        [180, 40, 180], [40, 180, 180], [220, 120, 40], [160, 160, 160],
    ], dtype=np.uint8)
    idx = np.clip(np.asarray(owner, dtype=np.int16) + 1, 0, 8)
    return lut[idx]


def fixture_calibration():
    """32x32. View 0 dark teal. View 1 olive at one texel the owner map
    assigns to view 1. Render shows that olive at (8, 8)."""
    n = 32
    render = np.zeros((n, n, 3), dtype=np.uint8)
    render[:] = (20, 50, 40)
    render[8, 8] = OLIVE_TWIN_RGB
    surfid = np.full((n, n), -1, dtype=np.int64)
    yy, xx = np.indices((n, n))
    fig = (yy >= 4) & (yy < 28) & (xx >= 4) & (xx < 28)
    surfid[fig] = yy[fig] * n + xx[fig]
    owner = np.zeros((n, n), dtype=np.int16)
    owner[8, 8] = 1
    pos = np.zeros((n, n, 3), dtype=np.float64)
    pos[..., 0] = (xx / n)
    pos[..., 1] = (yy / n)
    pos[..., 2] = 0.5
    meta = {"lo": [0.0, 0.0, 0.0], "hi": [2.0, 2.0, 2.0], "maxabs": 2.0}
    # cams: view 0 looks -Y, view 1 looks -X, both ortho covering [0,1]
    def cam(dtc, right, W=n, H=n):
        dtc = np.asarray(dtc, dtype=np.float64)
        right = np.asarray(right, dtype=np.float64)
        up = np.cross(right, -dtc)
        up = up / (np.linalg.norm(up) + 1e-12)
        return {
            "bmid": [0.5, 0.5, 0.5],
            "dtc": dtc.tolist(),
            "right": right.tolist(),
            "up": up.tolist(),
            "h_ext": 1.0,
            "v_ext": 1.0,
            "W": W,
            "H": H,
        }
    cams = {
        "view_0": cam([0, -1, 0], [1, 0, 0]),
        "view_1": cam([-1, 0, 0], [0, 1, 0]),
    }
    for v in range(2, 8):
        cams["view_%d" % v] = cams["view_0"]
    twins = {}
    for v in range(8):
        t = np.zeros((n, n, 3), dtype=np.uint8)
        t[:] = (20, 50, 40)
        twins[v] = t
    # Put olive in view 1 at the projection of texel (8,8).
    P = A.decode_pos(pos[8:9, 8:9], meta)[0, 0]
    px, py, _z = S.project_point(P, cams["view_1"])
    xi = int(np.clip(np.rint(px), 0, n - 1))
    yi = int(np.clip(np.rint(py), 0, n - 1))
    twins[1][yi, xi] = OLIVE_TWIN_RGB
    return {
        "render": render, "surfid": surfid, "owner": owner,
        "pos": pos, "meta": meta, "cams": cams, "twins": twins,
        "hit_xy": (yi, xi),
    }


def selftest(scratch=None):
    fx = fixture_calibration()
    P = A.decode_pos(fx["pos"], fx["meta"])
    tr = trace_pixels(
        np.array([8]), np.array([8]),
        fx["surfid"], fx["owner"], P, fx["cams"], fx["twins"],
        render_view=0)
    if int(tr["owner"][0]) != 1:
        _andon("fixture owner is %r, not 1" % int(tr["owner"][0]))
    got = tuple(int(c) for c in tr["owner_twin"][0])
    if got != OLIVE_TWIN_RGB:
        _andon("owner-twin sample is %s, not %s" % (got, OLIVE_TWIN_RGB))
    same = tuple(int(c) for c in tr["same_xy_twin"][0])
    if same == OLIVE_TWIN_RGB:
        _andon("same-xy twin was olive; the fixture cannot discriminate")
    return tr


def build_parser():
    p = argparse.ArgumentParser(
        description="Trace render flats to the contributing twin.")
    p.add_argument("--render", default=None)
    p.add_argument("--surfid", default=None)
    p.add_argument("--owner", default=None)
    p.add_argument("--pos", default=None)
    p.add_argument("--meta", default=None)
    p.add_argument("--cams", default=None)
    p.add_argument("--twin-dir", default=None)
    p.add_argument("--view", type=int, default=0)
    p.add_argument("--out", default=None)
    p.add_argument("--box", default=None,
                   help="optional y0,y1,x0,x1 window; detector still uses the spec")
    p.add_argument("--selftest", action="store_true")
    return p


def parse_box(text):
    if not text:
        return None
    parts = [int(x, 10) for x in str(text).split(",")]
    if len(parts) != 4:
        _andon("box must be y0,y1,x0,x1")
    return tuple(parts)


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.selftest:
            selftest()
            sys.stdout.write(
                "calibration owner-twin == %s  same-xy is not  "
                "(E50 olive window: n=%d owner6=%d)\n"
                % (OLIVE_TWIN_RGB, CALIBRATION_OLIVE_N, CALIBRATION_OWNER6))
            return 0
        need = (args.render, args.surfid, args.owner, args.pos,
                args.meta, args.cams, args.twin_dir, args.out)
        if not all(need):
            _andon("need --render --surfid --owner --pos --meta "
                   "--cams --twin-dir --out (or --selftest)")
        render = np.asarray(Image.open(args.render).convert("RGB"))
        surfid = np.load(args.surfid)
        owner = np.load(args.owner)
        pos = np.load(args.pos)
        meta = json.load(open(args.meta, encoding="utf-8"))
        cams = json.load(open(args.cams, encoding="utf-8"))
        twins = load_twins(args.twin_dir)
        P = A.decode_pos(pos, meta)
        box = parse_box(args.box) or CALIBRATION_BOX
        mask = olive_mask(render, box=box)
        ys, xs = np.where(mask)
        if ys.size == 0:
            _andon("no olive-spec pixels in the window")
        tr = trace_pixels(ys, xs, surfid, owner, P, cams, twins,
                          render_view=int(args.view))
        rend_px = render[ys, xs]
        summ = summarize("olive", rend_px, tr, mask)
        owner_img = paint_from_trace(render.shape, ys, xs, tr["owner_twin"])
        same_img = paint_from_trace(render.shape, ys, xs, tr["same_xy_twin"])
        lut = np.array([
            [20, 20, 20], [220, 40, 40], [40, 180, 40], [40, 80, 220],
            [220, 180, 40], [180, 40, 180], [40, 180, 180],
            [220, 120, 40], [200, 200, 200],
        ], dtype=np.uint8)
        ac = np.zeros_like(render)
        ac[ys, xs] = lut[np.clip(tr["owner"] + 1, 0, 8)]
        sheet = write_sheet(
            args.out, "v%02d" % int(args.view),
            render, owner_img, same_img, ac, box, zoom=4)
        payload = {
            "tool": "flat_trace.py",
            "tool_version": TOOL_VERSION,
            "view": int(args.view),
            "box": list(box),
            "sheet": os.path.abspath(sheet),
            "summary": summ,
            "note": (
                "same-xy twin is not the source unless owner==view. "
                "not a spend recommendation, not a grade"
            ),
        }
        sys.stdout.write(
            "flat_trace %s  n=%d  owner_hist=%s  "
            "owner_twin_std=%.1f same_xy_std=%.1f  sheet=%s\n"
            % (TOOL_VERSION, summ["n"], summ["owner_hist"],
               summ["owner_twin_std"], summ["same_xy_twin_std"], sheet))
        man = os.path.join(args.out, "flat_trace_v%02d.json" % int(args.view))
        with open(man, "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, indent=1)
            f.write("\n")
        return 0
    except Andon as e:
        sys.stderr.write(str(e) + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
