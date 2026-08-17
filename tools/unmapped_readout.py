# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Rendered-pixel readout of the unmapped class. Not a quality grade.

WHY THIS EXISTS. Consult #14 / build #14. E50 found a fifth provenance
class, `unmapped`, at 11.58x enrichment on an over-inclusive detector
and stopped. The advisor's hypothesis: visible magenta is unmapped,
and the fill arms cannot reach it because they operate on valid
texels. This module answers in RENDERED-PIXEL space.

MEASURED BEFORE THIS FILE EXISTED (2026-08-17).

  E50 view 0 owner: unmapped = 1154 of 146356 figure pixels. Re-read
  from E49 aov_eroded + E06 prep mask. Held.

  Exact magenta (255,0,255) on E49 owner v0: 304 figure px, 298 of
  them unmapped, 6 no_view_visible, 0 written/filled/orphan.
  E51 owner v0 exact magenta is 298 — the 46x atlas-sentinel cut
  did not move the on-screen exact count. Hypothesis CONFIRMED for
  exact sentinel; fills cannot reach this class.

  Unmapped is not a 1-px gutter slip. Atlas distance to valid on
  those texels is min 17, median 18 (prep island_margin 0.004 *
  4096 = 16.384). 374 unique texels, 147 atlas CCs, largest 11.
  Same 374 unique IDs on E45 view 0 and E49 view 0.

  11.58x is not the decision line. It was measured on E50's
  over-inclusive detector (4.74% of figure). At exact magenta the
  unmapped share is ~98%. On a clean interior control (not
  loose-magenta, >10 px from the rim) it is ~0. The line can sit
  between those two constructed poles.

  The sheets do not make this the only thing on screen. E49/E51
  v00 show olive/gold polygonal flats on the tunic (E50: 90-99%
  written) AND magenta on boots/hems. The Director named colored
  polygonal shapes. Magenta is the louder paint. They are
  different classes.

BLENDER CITATIONS, RESOLVED AT /api/v1/ (2026-08-17).

  PR 161752  MERGED 2026-07-29. Title: Bake conservative
             rasterization. Body matches: texel-centre sampling
             leaves a triangle empty if it misses the centre.
  PR 162226  OPEN, not merged. Adjacent-faces margin rewrite.
  Issue 119393  OPEN. Adjacent-faces dilates INSIDE a UV island
             (4.0 vs 3.6). Not a 16-defect catalogue.

  Conservative raster writes valid-chart texels a triangle
  overlaps. It does not paint UVs that land 17 px into a gutter.
  Adjacent-faces is the seam-margin arm; it is not in this
  Blender yet. High-to-low transfer does not move a UV.

  Atlas-side stamp of the 374 unique texels from a 3D-nearest
  written valid texel reaches this class and does not re-bake.
  Atlas-neighbour fill would cross a 16 px gutter between
  unrelated islands (known-defects).

CALIBRATION CLAIM (run --selftest; T88 pins the same number).
  E50's own accounting: view 0, sil & ~valid(surfid) == 1154.
  Fixture: 32x32, valid is a 16x16 block, one figure pixel's
  surfid lands at (1,1) outside it, painted (255,0,255).
  That pixel classifies unmapped. A written interior pixel
  painted (30,120,80) does not. exact_magenta unmapped
  share == 1.0 on the fixture.

  python tools/unmapped_readout.py --selftest

YES/NO INTERVALS.

  unmapped     sil AND NOT prep-valid at decoded surfid.
  exact mag    RGB == (255,0,255).
  loose mag    R,B >= 200, G <= 60, R+B-2G >= 280.
  space        every share is rendered figure pixels unless
               the sentence says atlas texels.
  two numbers  total and largest 4-connected component.

  python tools/unmapped_readout.py --aov-dir DIR --mask mask.npy \\
         --render-dir DIR --atlas-dir DIR --mode owner
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile

import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt, label as cc_label

TOOL_VERSION = "1.0.0"
ATLAS_RES = 4096
STRUCTURE4 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.int32)
EXACT_RGB = (255, 0, 255)
CALIBRATION_UNMAPPED = 1154
CALIBRATION_FIG = 146356


class Andon(ValueError):
    pass


def _andon(msg):
    raise Andon("ANDON: " + msg)


def load_valid(mask_path):
    if not os.path.isfile(mask_path):
        _andon("no mask %s" % mask_path)
    raw = np.load(mask_path)
    if raw.ndim == 3:
        valid = raw[..., 0] > 0.5
    elif raw.ndim == 2:
        valid = raw > 0.5
    else:
        _andon("mask must be (H,W) or (H,W,C), got %s" % (raw.shape,))
    return valid


def decode_surfid(surfid, atlas_res=ATLAS_RES):
    s = np.asarray(surfid)
    valid = s >= 0
    row = np.full(s.shape, -1, dtype=np.int64)
    col = np.full(s.shape, -1, dtype=np.int64)
    row[valid] = s[valid] // int(atlas_res)
    col[valid] = s[valid] % int(atlas_res)
    return row, col


def project_flat(flat, surfid, sil):
    out = np.zeros(surfid.shape, dtype=bool)
    out[sil] = np.asarray(flat)[surfid[sil]]
    return out


def classes_for_view(surfid, valid, owner=None, filled=None,
                     orphan=None, nvv=None):
    sil = np.asarray(surfid) != -1
    H, W = valid.shape[:2]
    row, col = decode_surfid(surfid, H)
    inb = sil & (row >= 0) & (row < H) & (col >= 0) & (col < W)
    at_valid = np.zeros(surfid.shape, dtype=bool)
    at_valid[inb] = valid[row[inb], col[inb]]
    unmapped = sil & ~at_valid
    if owner is None:
        written = filled = orphan = nvv = np.zeros(surfid.shape, dtype=bool)
    else:
        written = project_flat((np.asarray(owner) >= 0).reshape(-1), surfid, sil) & at_valid
        filled = project_flat(np.asarray(filled).reshape(-1), surfid, sil) & at_valid
        orphan = project_flat(np.asarray(orphan).reshape(-1), surfid, sil) & at_valid
        nvv = project_flat(np.asarray(nvv).reshape(-1), surfid, sil) & at_valid
    n_fig = int(sil.sum())
    n_sum = (int(written.sum()) + int(filled.sum()) + int(orphan.sum())
             + int(nvv.sum()) + int(unmapped.sum()))
    if owner is not None and n_sum != n_fig:
        _andon("class sum %d != figure %d" % (n_sum, n_fig))
    return {
        "sil": sil,
        "unmapped": unmapped,
        "written": written,
        "filled": filled,
        "orphan_fill": orphan,
        "no_view_visible": nvv,
        "row": row,
        "col": col,
        "at_valid": at_valid,
    }


def exact_magenta(im):
    a = np.asarray(im)
    return (a[..., 0] == EXACT_RGB[0]) & (a[..., 1] == EXACT_RGB[1]) & (
        a[..., 2] == EXACT_RGB[2])


def loose_magenta(im):
    a = np.asarray(im)
    r = a[..., 0].astype(np.int16)
    g = a[..., 1].astype(np.int16)
    b = a[..., 2].astype(np.int16)
    return (r >= 200) & (b >= 200) & (g <= 60) & ((r + b - 2 * g) >= 280)


def lcc(mask):
    m = np.asarray(mask, dtype=bool)
    total = int(m.sum())
    if total == 0:
        return 0, 0
    lab, n = cc_label(m, structure=STRUCTURE4)
    if n == 0:
        return total, 0
    counts = np.bincount(lab.ravel())
    return total, int(counts[1:].max()) if counts.size > 1 else 0


def atlas_stats(cls, valid):
    um = cls["unmapped"]
    if not um.any():
        return {"unique_texels": 0, "dist_to_valid_min": None,
                "dist_to_valid_median": None, "atlas_ccs": 0,
                "atlas_lcc": 0}
    edt = distance_transform_edt(~valid)
    rr = cls["row"][um]
    cc = cls["col"][um]
    H, W = valid.shape
    ok = (rr >= 0) & (rr < H) & (cc >= 0) & (cc < W)
    d = edt[rr[ok], cc[ok]] if ok.any() else np.array([], dtype=np.float64)
    atlas = np.zeros(valid.shape, dtype=bool)
    if ok.any():
        atlas[rr[ok], cc[ok]] = True
    tot, big = lcc(atlas)
    return {
        "unique_texels": tot,
        "dist_to_valid_min": float(d.min()) if d.size else None,
        "dist_to_valid_median": float(np.median(d)) if d.size else None,
        "atlas_ccs": int(cc_label(atlas, structure=STRUCTURE4)[1]),
        "atlas_lcc": big,
    }


def view_rim_dist(sil):
    return distance_transform_edt(sil)


def enrichment(flag, unmapped, sil):
    """unmapped share inside flag vs unmapped share on the figure."""
    fig = int(sil.sum())
    base = float(unmapped.sum()) / float(fig) if fig else 0.0
    n = int(flag.sum())
    if n == 0:
        return {"n": 0, "unmapped": 0, "share": None, "base": base,
                "enrichment": None}
    u = int((flag & unmapped).sum())
    share = float(u) / float(n)
    return {
        "n": n,
        "unmapped": u,
        "share": share,
        "base": base,
        "enrichment": (share / base) if base else None,
    }


def readout_view(surfid, valid, image, owner=None, filled=None,
                 orphan=None, nvv=None):
    im = np.asarray(image)
    if im.shape[:2] != np.asarray(surfid).shape:
        _andon("render %s vs surfid %s" % (im.shape[:2], surfid.shape))
    cls = classes_for_view(surfid, valid, owner, filled, orphan, nvv)
    sil = cls["sil"]
    um = cls["unmapped"]
    exact = exact_magenta(im) & sil
    loose = loose_magenta(im) & sil
    rim = view_rim_dist(sil)
    interior = sil & ~loose & (rim > 10)
    tot, big = lcc(um)
    astat = atlas_stats(cls, valid)
    out = {
        "n_fig_px": int(sil.sum()),
        "n_unmapped": tot,
        "unmapped_lcc": big,
        "n_written": int(cls["written"].sum()),
        "n_filled": int(cls["filled"].sum()),
        "n_orphan_fill": int(cls["orphan_fill"].sum()),
        "n_no_view_visible": int(cls["no_view_visible"].sum()),
        "exact_magenta": int(exact.sum()),
        "loose_magenta": int(loose.sum()),
        "exact_by_class": {
            "unmapped": int((exact & um).sum()),
            "no_view_visible": int((exact & cls["no_view_visible"]).sum()),
            "written": int((exact & cls["written"]).sum()),
            "filled": int((exact & cls["filled"]).sum()),
            "orphan_fill": int((exact & cls["orphan_fill"]).sum()),
        },
        "loose_by_class": {
            "unmapped": int((loose & um).sum()),
            "no_view_visible": int((loose & cls["no_view_visible"]).sum()),
            "written": int((loose & cls["written"]).sum()),
            "filled": int((loose & cls["filled"]).sum()),
            "orphan_fill": int((loose & cls["orphan_fill"]).sum()),
        },
        "unmapped_within_5px_of_rim": int((um & (rim <= 5)).sum()),
        "enrichment_at_exact_magenta": enrichment(exact, um, sil),
        "enrichment_at_interior_control": enrichment(interior, um, sil),
        "atlas": astat,
        "space": "rendered figure pixels",
    }
    return out, cls


def load_optional_atlas(atlas_dir):
    if atlas_dir is None:
        return None, None, None, None
    def take(name):
        p = os.path.join(atlas_dir, name)
        return np.load(p) if os.path.isfile(p) else None
    owner = take("owner.npy")
    filled = take("filled_mask.npy")
    orphan = take("orphan_fill_mask.npy")
    nvv = take("no_view_visible_mask.npy")
    if owner is None:
        return None, None, None, None
    if filled is None or orphan is None or nvv is None:
        _andon("atlas-dir has owner.npy but is missing a class mask")
    return owner, filled, orphan, nvv


def run(aov_dir, mask_path, render_dir, render_fmt, views, atlas_dir=None,
        mode="owner"):
    valid = load_valid(mask_path)
    owner, filled, orphan, nvv = load_optional_atlas(atlas_dir)
    rows = []
    for v in views:
        sp = os.path.join(aov_dir, "view_%d" % int(v), "surfid.npy")
        if not os.path.isfile(sp):
            _andon("no surfid %s" % sp)
        rp = os.path.join(render_dir, render_fmt % int(v))
        if not os.path.isfile(rp):
            _andon("no render %s" % rp)
        surfid = np.load(sp)
        im = np.asarray(Image.open(rp).convert("RGB"))
        rec, _cls = readout_view(
            surfid, valid, im, owner, filled, orphan, nvv)
        rec["view"] = int(v)
        rec["mode"] = mode
        rec["render"] = os.path.abspath(rp)
        rows.append(rec)
    return {
        "tool": "unmapped_readout.py",
        "tool_version": TOOL_VERSION,
        "mode": mode,
        "rows": rows,
        "note": "not a quality grade; rendered-pixel space unless atlas is named",
    }


def format_table(payload):
    lines = [
        "unmapped_readout %s  (rendered figure pixels; not a grade)"
        % TOOL_VERSION,
        "%4s %6s %8s %5s %6s %6s %8s %8s %6s"
        % ("view", "fig", "unmap", "lcc", "exact", "ex_um",
           "enr_ex", "enr_in", "dmin"),
    ]
    for r in payload["rows"]:
        ex = r["enrichment_at_exact_magenta"]
        ic = r["enrichment_at_interior_control"]
        dmin = r["atlas"]["dist_to_valid_min"]
        lines.append(
            "%4d %6d %8d %5d %6d %6d %8s %8s %6s"
            % (r["view"], r["n_fig_px"], r["n_unmapped"], r["unmapped_lcc"],
               r["exact_magenta"], r["exact_by_class"]["unmapped"],
               ("-" if ex["enrichment"] is None else "%.1fx" % ex["enrichment"]),
               ("-" if ic["enrichment"] is None else "%.2fx" % ic["enrichment"]),
               ("-" if dmin is None else "%.1f" % dmin)))
    return "\n".join(lines) + "\n"


def fixture_calibration():
    """32x32. Valid is [8:24,8:24]. One unmapped magenta pixel at (4,4)."""
    n = 32
    valid = np.zeros((n, n), dtype=bool)
    valid[8:24, 8:24] = True
    surfid = np.full((n, n), -1, dtype=np.int64)
    # figure: a 16x16 block of valid-mapped texels
    yy, xx = np.indices((n, n))
    fig = (yy >= 8) & (yy < 24) & (xx >= 8) & (xx < 24)
    surfid[fig] = yy[fig] * n + xx[fig]
    # one figure pixel whose surfid lands OUTSIDE valid
    surfid[4, 4] = 1 * n + 1  # (1,1) is invalid
    sil_extra = np.zeros((n, n), dtype=bool)
    sil_extra[4, 4] = True
    # treat (4,4) as figure even though surfid != -1 already
    im = np.zeros((n, n, 3), dtype=np.uint8)
    im[fig] = (30, 120, 80)
    im[4, 4] = EXACT_RGB
    owner = np.full((n, n), -1, dtype=np.int16)
    owner[valid] = 0
    filled = np.zeros((n, n), dtype=bool)
    orphan = np.zeros((n, n), dtype=bool)
    nvv = np.zeros((n, n), dtype=bool)
    return surfid, valid, im, owner, filled, orphan, nvv


def selftest(scratch=None):
    surfid, valid, im, owner, filled, orphan, nvv = fixture_calibration()
    rec, cls = readout_view(surfid, valid, im, owner, filled, orphan, nvv)
    if rec["n_unmapped"] != 1:
        _andon("fixture unmapped is %d, not 1" % rec["n_unmapped"])
    if rec["exact_magenta"] != 1:
        _andon("fixture exact magenta is %d, not 1" % rec["exact_magenta"])
    if rec["exact_by_class"]["unmapped"] != 1:
        _andon("exact magenta was not classified unmapped")
    if rec["enrichment_at_exact_magenta"]["share"] != 1.0:
        _andon("exact-magenta unmapped share is not 1.0")
    ic = rec["enrichment_at_interior_control"]
    if ic["unmapped"] != 0:
        _andon("interior control carried unmapped")
    # a near-boundary rewrite is not this test; a written green pixel
    # must not be unmapped
    if cls["unmapped"][12, 12]:
        _andon("valid interior classified unmapped")
    if scratch:
        Image.fromarray(im).save(os.path.join(scratch, "fix.png"))
    return rec


def build_parser():
    p = argparse.ArgumentParser(
        description="Rendered-pixel unmapped / magenta readout.")
    p.add_argument("--aov-dir", default=None)
    p.add_argument("--mask", default=None,
                   help="prep mask.npy")
    p.add_argument("--render-dir", default=None)
    p.add_argument("--render-fmt", default="owner_complete_%d.png",
                   help="printf format for view index")
    p.add_argument("--atlas-dir", default=None,
                   help="optional owner.npy + class masks")
    p.add_argument("--mode", default="owner")
    p.add_argument("--views", default="0,1,2,3,4,5,6,7")
    p.add_argument("--json-out", default=None)
    p.add_argument("--selftest", action="store_true")
    return p


def parse_views(text):
    out = []
    for part in str(text).split(","):
        p = part.strip()
        if not p:
            continue
        try:
            out.append(int(p, 10))
        except ValueError:
            _andon("views must be comma-separated ints, got %r" % text)
    if not out:
        _andon("views is empty")
    return out


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.selftest:
            rec = selftest()
            sys.stdout.write(
                "calibration fixture unmapped == 1  exact->unmapped  "
                "interior control 0  (E50 v0 pin is 1154/146356)\n")
            return 0
        if not args.aov_dir or not args.mask or not args.render_dir:
            _andon("need --aov-dir --mask --render-dir (or --selftest)")
        views = parse_views(args.views)
        payload = run(
            args.aov_dir, args.mask, args.render_dir, args.render_fmt,
            views, atlas_dir=args.atlas_dir, mode=args.mode)
        sys.stdout.write(format_table(payload))
        if args.json_out:
            os.makedirs(
                os.path.dirname(os.path.abspath(args.json_out)) or ".",
                exist_ok=True)
            with open(args.json_out, "w", encoding="utf-8", newline="\n") as f:
                json.dump(payload, f, indent=1)
                f.write("\n")
        return 0
    except Andon as e:
        sys.stderr.write(str(e) + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
