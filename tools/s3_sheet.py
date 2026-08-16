# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Acceptance sheet for S3 stills. Layout only. The Director's eye grades.

WHY THIS EXISTS. Director, 2026-08-16: every arc ends with a picture that
can be put beside the current one, or it does not count as done. s3_run
writes stills and maps; this module lays them next to the reference twin
and the shipped flat so the three-world readout is visible.

  clean composite + low disagreement  -> 3D path degrades the plates
  blotchy + high disagreement         -> sources inconsistent (warp lead)
  blotchy + ~0 disagreement           -> plates share the defect

This file moves pixels. It does not grade them. A local seat runs the
chain. The advisor folds. The Director judges.

WHAT ONE SHEET IS. One PNG per target view:

  reference twin | shipped flat | S3 view-dependent | S3 view-independent
  | disagreement heat

plus one native-pixel row per named region, a stats line under each
region, and a provenance panel at the bottom (path + sha256 of every
file consumed). Missing inputs become an explicit MISSING panel of the
row's size -- never a skip, never a thinner sheet.

ORDER (argue-with-the-brief). Keep the five-panel order above. The eye
reads two adjacent pairs then a diagnostic:

  reference | shipped   the week-long defect, already how the Director
                        judges "is the current look the look"
  VD | VI               the three-world split
  heat                  where sources fight

Putting shipped beside VI would make "did S3-B beat the current still"
one pair, and would break both of the pairs this arc is actually about.
No --order flag. If a later seat wants that comparison, it is a second
sheet, not a reshuffle of this one.

HEAT SCALE (argue-with-the-brief). Default is GLOBAL per target: vmax
is the max of that view's full disagreement.npy. Every region row of
that view uses the same LUT, and the caption states vmax. A per-region
scale (--heat-scale region) is exposed because a uniformly-moderate
crop is invisible on a global scale -- but it is not the default. The
three-world readout is "high vs ~0"; a per-region scale would paint a
moderate crop as saturated hot and the Director would mis-read world 2
as world 3.

WHAT THIS ASSUMES, NAMED.

  * t81 was assigned here and is already taken by the E45 warp
    instrument (test_t81_twin_mesh_warp.py). Tests for this file are
    t82. The brief's t81 is a collision, not a second T81.
  * twin_i pairs with final_i pairs with s3_run's t0i. Recorded
    convention. Measured 2026-08-16 on ARMB: both rings are 752x1024,
    same pose, unflipped IoU > flip-LR IoU on all 8 views. The tool
    ANDON's on a size mismatch and does not rotate, flip, or resize.
  * E40 boxes in the starter JSON are transcribed from
    facet_E40_A/task3_sheet.py (cx, cy, r) -> [cx-r, cy-r, cx+r, cy+r].
    Blade and grip boxes are PROPOSALS from the 752x1024 twin ring.
    The JSON is labelled as such. This tool does not treat it as a
    ruling.
  * s3_run writes coverage.png / fallback.png (not npy) and
    disagreement.npy / owner.npy. We load what that runner wrote.
  * Native pixels or integer nearest-neighbour zoom. No other
    resample. A defect that decides acceptance is invisible at
    thumbnail scale and falsified by interpolation.
  * One PNG per view, not one stack of eight native full-figures.
    Eight 1024-tall rows is a poster. The picture that sits beside
    "the current one" is one camera.

CALIBRATION CLAIM (run --selftest; T82 pins the same number).
  Canvas 32x32, zeros, except pixel (y=5, x=7) = 200.
  box = [7, 5, 15, 13]  (half-open, crop origin is that pixel).
  zoom = 2, nearest-neighbour.
  crop[0, 0] == 200.
  Construction: crop[0,0] is source[5,7]. NN zoom repeats that value.
  A swapped (x,y), a 1-px origin slip, a clamp, or a bilinear zoom
  cannot land 200 at [0,0] next to zero neighbours.

  python tools/s3_sheet.py --selftest

YES/NO INTERVALS.

  crop box            half-open [x0,y0,x1,y1]. Exceeding the source
                      ANDON's. Empty (x1<=x0 or y1<=y0) ANDON's.
  panel sizes in a row must match. Mismatch ANDON's. No auto-resize.
  MISSING panel       fill (180, 0, 140). Detectably not a real still.
  disagreement heat   LUT of the scalar map. 0 -> (0,0,255),
                      vmax -> (255,80,0). vmax is stated on the sheet.
  stats               region-scoped reductions of s3_run maps.
                      coverage_px / area, fallback_px / area,
                      disagreement mean and p90 over coverage pixels,
                      owner histogram. Missing maps: the stats line
                      names them, it does not invent numbers.
  provenance          sha256 of file bytes actually read. Recompute
                      independently; do not trust a hash the sheet
                      echoed without rereading the file.

  python tools/s3_sheet.py --s3-dir DIR --ref-dir DIR --shipped-dir DIR
         --regions JSON --out DIR [--zoom N] [--heat-scale global|region]
         [--views 0,1,7]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

TOOL_VERSION = "1.0.0"

MISSING_RGB = (180, 0, 140)
BG_RGB = (20, 20, 24)
FG_RGB = (230, 230, 230)
ACCENT_RGB = (255, 210, 90)
PAD = 8
ROLE_H = 16
PATH_H = 14
TITLE_H = 20
STATS_H = 18
FOOTER_LINE = 14

ROLES = (
    "reference",
    "shipped",
    "s3-vd",
    "s3-vi",
    "disagreement",
)

CALIBRATION_Y = 5
CALIBRATION_X = 7
CALIBRATION_VALUE = 200
CALIBRATION_BOX = [7, 5, 15, 13]
CALIBRATION_ZOOM = 2

DEFAULT_REGIONS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "s3_sheet_regions.json")


class Andon(ValueError):
    """A fired gate. Never an `assert`."""


def _andon(msg):
    raise Andon("ANDON: " + msg)


def as_box(box):
    if box is None or len(box) != 4:
        _andon("box must be [x0, y0, x1, y1], got %r" % (box,))
    x0, y0, x1, y1 = (int(box[0]), int(box[1]), int(box[2]), int(box[3]))
    if x1 <= x0 or y1 <= y0:
        _andon("empty box %s" % ([x0, y0, x1, y1],))
    return x0, y0, x1, y1


def box_hw(box):
    x0, y0, x1, y1 = as_box(box)
    return (y1 - y0, x1 - x0)


def crop_array(arr, box, name, source):
    """Half-open crop. Exceeding the source is an ANDON, never a clamp."""
    x0, y0, x1, y1 = as_box(box)
    a = np.asarray(arr)
    if a.ndim < 2:
        _andon("%s is not an image, shape %s" % (source, a.shape))
    H, W = a.shape[:2]
    if x0 < 0 or y0 < 0 or x1 > W or y1 > H:
        _andon(
            "crop box %s %s exceeds source %s %dx%d"
            % (name, [x0, y0, x1, y1], source, W, H))
    return np.ascontiguousarray(a[y0:y1, x0:x1])


def nn_zoom(arr, zoom):
    """Integer nearest-neighbour only. No other resample exists here."""
    if zoom != int(zoom) or int(zoom) < 1:
        _andon("zoom must be integer >= 1, got %r" % (zoom,))
    z = int(zoom)
    a = np.ascontiguousarray(arr)
    if z == 1:
        return a
    return np.repeat(np.repeat(a, z, axis=0), z, axis=1)


def crop_nn(arr, box, zoom, name="crop", source="array"):
    return nn_zoom(crop_array(arr, box, name, source), zoom)


def missing_panel(h, w):
    if h <= 0 or w <= 0:
        _andon("MISSING panel size %dx%d" % (h, w))
    return np.full((int(h), int(w), 3), MISSING_RGB, dtype=np.uint8)


def is_missing_panel(arr):
    a = np.asarray(arr)
    if a.ndim != 3 or a.shape[-1] < 3:
        return False
    return (
        int(a[0, 0, 0]) == MISSING_RGB[0]
        and int(a[0, 0, 1]) == MISSING_RGB[1]
        and int(a[0, 0, 2]) == MISSING_RGB[2]
    )


def colorize_heat(dmap, vmax):
    """Per-pixel LUT. Not a spatial resample."""
    d = np.asarray(dmap, dtype=np.float64)
    if d.ndim != 2:
        _andon("disagreement map must be (H,W), got %s" % (d.shape,))
    vm = float(vmax)
    if vm < 0:
        _andon("heat vmax < 0: %r" % vm)
    if vm == 0.0:
        t = np.zeros_like(d)
    else:
        t = np.clip(d / vm, 0.0, 1.0)
    rgb = np.empty(d.shape + (3,), dtype=np.uint8)
    rgb[..., 0] = np.clip(np.round(255.0 * t), 0, 255).astype(np.uint8)
    rgb[..., 1] = np.clip(np.round(80.0 * t), 0, 255).astype(np.uint8)
    rgb[..., 2] = np.clip(np.round(255.0 * (1.0 - t)), 0, 255).astype(np.uint8)
    return rgb


def as_rgb_u8(arr):
    a = np.asarray(arr)
    if a.ndim == 2:
        a = np.stack([a, a, a], axis=-1)
    if a.ndim != 3 or a.shape[-1] < 3:
        _andon("need (H,W) or (H,W,C), got %s" % (a.shape,))
    if a.dtype == np.uint8:
        return np.ascontiguousarray(a[..., :3])
    x = np.asarray(a[..., :3], dtype=np.float64)
    mx = float(np.max(x)) if x.size else 0.0
    if mx <= 1.0 + 1e-6:
        x = x * 255.0
    return np.clip(np.round(x), 0, 255).astype(np.uint8)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load_rgb(path):
    if path is None or not os.path.isfile(path):
        return None
    return as_rgb_u8(Image.open(path))


def load_gray_bool(path):
    if path is None or not os.path.isfile(path):
        return None
    a = np.asarray(Image.open(path).convert("L"))
    return a > 0


def load_npy(path):
    if path is None or not os.path.isfile(path):
        return None
    return np.load(path)


def agreed_hw(items):
    """items: list of (hw_or_None, name). Mismatch ANDON's. All-None -> None."""
    seen = [(hw, name) for hw, name in items if hw is not None]
    if not seen:
        return None
    hw0, n0 = seen[0]
    for hw, name in seen[1:]:
        if hw != hw0:
            _andon(
                "mismatched panel size: %s is %dx%d, %s is %dx%d"
                % (n0, hw0[1], hw0[0], name, hw[1], hw[0]))
    return hw0


def _font(size):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def _short_path(path):
    if path is None:
        return "MISSING"
    p = os.path.normpath(path)
    parts = p.replace("\\", "/").split("/")
    if len(parts) >= 2:
        return "/".join(parts[-2:])
    return parts[-1]


def _draw_missing_label(arr):
    im = Image.fromarray(arr, mode="RGB")
    dr = ImageDraw.Draw(im)
    dr.text((2, 2), "MISSING", fill=(255, 255, 255), font=_font(12))
    return np.asarray(im, dtype=np.uint8)


def panel_for(arr, hw, path, zoom):
    """Real content or a MISSING panel of size hw, then zoom."""
    h, w = hw
    if arr is None:
        p = missing_panel(h, w)
        p = _draw_missing_label(p)
        return nn_zoom(p, zoom), False
    got = arr.shape[:2]
    if got != (h, w):
        _andon(
            "mismatched panel size: %s is %dx%d, row expects %dx%d"
            % (path, got[1], got[0], w, h))
    return nn_zoom(as_rgb_u8(arr), zoom), True


def compose_row(panels, captions, title, stats_line=None):
    """panels: list of uint8 (H,W,3), already zoomed, same size.

    ANDON if any two differ. Returns a uint8 sheet strip.
    """
    if not panels:
        _andon("compose_row: no panels")
    hw0 = panels[0].shape[:2]
    for i, p in enumerate(panels):
        if p.shape[:2] != hw0:
            _andon(
                "mismatched panel size in row %r: panel 0 is %dx%d, panel %d is %dx%d"
                % (title, hw0[1], hw0[0], i, p.shape[1], p.shape[0]))
        if p.ndim != 3 or p.shape[-1] < 3:
            _andon("panel %d is not RGB, shape %s" % (i, p.shape))
    ph, pw = hw0
    n = len(panels)
    stats_h = STATS_H if stats_line else 0
    width = n * pw + (n + 1) * PAD
    height = PAD + TITLE_H + ROLE_H + PATH_H + ph + stats_h + PAD
    canvas = np.full((height, width, 3), BG_RGB, dtype=np.uint8)
    im = Image.fromarray(canvas, mode="RGB")
    dr = ImageDraw.Draw(im)
    font = _font(12)
    small = _font(10)
    dr.text((PAD, PAD), title, fill=ACCENT_RGB, font=font)
    y_role = PAD + TITLE_H
    y_path = y_role + ROLE_H
    y_img = y_path + PATH_H
    for i, (p, cap) in enumerate(zip(panels, captions)):
        x = PAD + i * (pw + PAD)
        role = cap.get("role", "")
        path = cap.get("path", "")
        extra = cap.get("extra", "")
        dr.text((x, y_role), role, fill=FG_RGB, font=small)
        label = path if not extra else "%s  %s" % (path, extra)
        dr.text((x, y_path), label, fill=ACCENT_RGB, font=small)
        im.paste(Image.fromarray(as_rgb_u8(p), mode="RGB"), (x, y_img))
    if stats_line:
        dr.text(
            (PAD, y_img + ph + 2), stats_line, fill=FG_RGB, font=small)
    return np.asarray(im, dtype=np.uint8)


def provenance_panel(entries, width):
    """A panel, not metadata. One line per consumed or missing input."""
    lines = ["PROVENANCE  sha256  path"]
    for e in entries:
        if e.get("sha256"):
            lines.append("%s  %s" % (e["sha256"], e["path"]))
        else:
            lines.append("MISSING                                 %s" % e["path"])
    h = PAD * 2 + FOOTER_LINE * max(len(lines), 1)
    canvas = np.full((h, max(int(width), 64), 3), (12, 12, 16), dtype=np.uint8)
    im = Image.fromarray(canvas, mode="RGB")
    dr = ImageDraw.Draw(im)
    font = _font(10)
    y = PAD
    for i, line in enumerate(lines):
        fill = ACCENT_RGB if i == 0 else FG_RGB
        dr.text((PAD, y), line, fill=fill, font=font)
        y += FOOTER_LINE
    return np.asarray(im, dtype=np.uint8)


def stack_rows(rows):
    if not rows:
        _andon("no rows to stack")
    width = max(r.shape[1] for r in rows)
    height = sum(r.shape[0] for r in rows)
    canvas = np.full((height, width, 3), BG_RGB, dtype=np.uint8)
    y = 0
    for r in rows:
        canvas[y:y + r.shape[0], :r.shape[1]] = r
        y += r.shape[0]
    return canvas


def region_stats(box, coverage, fallback, disagreement, owner):
    """Region-scoped summaries of existing maps. No new measurement."""
    h, w = box_hw(box)
    area = int(h * w)
    out = {
        "area": area,
        "coverage_px": None,
        "fallback_px": None,
        "disagreement_mean": None,
        "disagreement_p90": None,
        "owner_hist": None,
        "missing": [],
    }
    cov = None
    if coverage is None:
        out["missing"].append("coverage")
    else:
        cov = crop_array(np.asarray(coverage).astype(bool), box, "coverage",
                         "coverage")
        out["coverage_px"] = int(cov.sum())
    if fallback is None:
        out["missing"].append("fallback")
    else:
        fb = crop_array(np.asarray(fallback).astype(bool), box, "fallback",
                        "fallback")
        out["fallback_px"] = int(fb.sum())
    if disagreement is None:
        out["missing"].append("disagreement")
    else:
        d = crop_array(np.asarray(disagreement, dtype=np.float64), box,
                       "disagreement", "disagreement.npy")
        if cov is not None and int(cov.sum()) > 0:
            vals = d[cov]
        else:
            vals = d.reshape(-1)
        out["disagreement_mean"] = float(vals.mean()) if vals.size else 0.0
        out["disagreement_p90"] = (
            float(np.percentile(vals, 90)) if vals.size else 0.0)
    if owner is None:
        out["missing"].append("owner")
    else:
        ow = crop_array(np.asarray(owner), box, "owner", "owner.npy")
        hist = {}
        for v in np.unique(ow):
            hist[int(v)] = int((ow == v).sum())
        out["owner_hist"] = hist
    return out


def format_stats(name, st):
    if st["missing"]:
        return "%s  stats MISSING %s" % (name, ",".join(st["missing"]))
    hist = st["owner_hist"] or {}
    keys = sorted(hist, key=lambda k: (k < 0, k))
    bits = ["%d:%d" % (k, hist[k]) for k in keys]
    return (
        "%s  cov %d/%d  d_mean %.4f  d_p90 %.4f  fallback %d/%d  owners %s"
        % (name, st["coverage_px"], st["area"],
           st["disagreement_mean"], st["disagreement_p90"],
           st["fallback_px"], st["area"], " ".join(bits) if bits else "-")
    )


def load_regions(path):
    if not os.path.isfile(path):
        _andon("regions file does not exist: %s" % path)
    with open(path, encoding="utf-8") as f:
        spec = json.load(f)
    views = spec.get("views")
    if not isinstance(views, dict) or not views:
        _andon("regions JSON has no views object: %s" % path)
    parsed = {}
    for vk, regs in views.items():
        try:
            vi = int(vk)
        except (TypeError, ValueError):
            _andon("regions view key not an int: %r" % (vk,))
        if not isinstance(regs, list):
            _andon("regions for view %s is not a list" % vk)
        items = []
        for r in regs:
            if not isinstance(r, dict) or "name" not in r or "box" not in r:
                _andon("region needs name+box, got %r" % (r,))
            as_box(r["box"])
            items.append({
                "name": str(r["name"]),
                "box": [int(x) for x in r["box"]],
                "from": str(r.get("from", "")),
            })
        parsed[vi] = items
    spec["_parsed"] = parsed
    spec["_path"] = os.path.abspath(path)
    return spec


def s3_target_dir(s3_dir, view_i):
    return os.path.join(s3_dir, "t%02d" % int(view_i))


def load_target_inputs(s3_dir, ref_dir, shipped_dir, view_i):
    """Thin loader. Missing files stay None. Hashes only for files read."""
    tag = int(view_i)
    ref_p = os.path.join(ref_dir, "twin_%d.png" % tag) if ref_dir else None
    ship_p = (
        os.path.join(shipped_dir, "final_%d.png" % tag) if shipped_dir else None)
    td = s3_target_dir(s3_dir, tag) if s3_dir else None
    vd_p = os.path.join(td, "dependent.png") if td else None
    vi_p = os.path.join(td, "independent.png") if td else None
    d_png = os.path.join(td, "disagreement.png") if td else None
    d_npy = os.path.join(td, "disagreement.npy") if td else None
    cov_p = os.path.join(td, "coverage.png") if td else None
    fb_p = os.path.join(td, "fallback.png") if td else None
    own_p = os.path.join(td, "owner.npy") if td else None

    consumed = []

    def take_rgb(path):
        arr = load_rgb(path)
        if arr is None:
            consumed.append({"path": path, "sha256": None, "kind": "rgb"})
            return None
        consumed.append({
            "path": os.path.abspath(path),
            "sha256": sha256_file(path),
            "kind": "rgb",
        })
        return arr

    def take_bool(path):
        arr = load_gray_bool(path)
        if arr is None:
            consumed.append({"path": path, "sha256": None, "kind": "mask"})
            return None
        consumed.append({
            "path": os.path.abspath(path),
            "sha256": sha256_file(path),
            "kind": "mask",
        })
        return arr

    def take_npy(path, kind):
        arr = load_npy(path)
        if arr is None:
            consumed.append({"path": path, "sha256": None, "kind": kind})
            return None
        consumed.append({
            "path": os.path.abspath(path),
            "sha256": sha256_file(path),
            "kind": kind,
        })
        return arr

    ref = take_rgb(ref_p)
    shipped = take_rgb(ship_p)
    vd = take_rgb(vd_p)
    vi = take_rgb(vi_p)
    dmap = take_npy(d_npy, "disagreement")
    if dmap is None:
        # png is a display dump scaled to 1.0; not the measurement.
        consumed.append({"path": d_png, "sha256": None, "kind": "disagreement"})
    coverage = take_bool(cov_p)
    fallback = take_bool(fb_p)
    owner = take_npy(own_p, "owner")

    maps = {
        "reference": ref,
        "shipped": shipped,
        "s3-vd": vd,
        "s3-vi": vi,
        "disagreement": dmap,
        "coverage": coverage,
        "fallback": fallback,
        "owner": owner,
    }
    paths = {
        "reference": ref_p,
        "shipped": ship_p,
        "s3-vd": vd_p,
        "s3-vi": vi_p,
        "disagreement": d_npy,
        "coverage": cov_p,
        "fallback": fb_p,
        "owner": own_p,
    }
    return maps, paths, consumed


def _heat_vmax(dmap, box, scale):
    if dmap is None:
        return 0.0
    d = np.asarray(dmap, dtype=np.float64)
    if scale == "region" and box is not None:
        d = crop_array(d, box, "heat", "disagreement.npy")
    if d.size == 0:
        return 0.0
    return float(np.max(d))


def _heat_panel(dmap, hw, box, vmax, zoom, path):
    if dmap is None:
        p = missing_panel(hw[0], hw[1])
        p = _draw_missing_label(p)
        return nn_zoom(p, zoom), False
    if box is None:
        src = np.asarray(dmap, dtype=np.float64)
        if src.shape[:2] != hw:
            _andon(
                "mismatched panel size: %s is %dx%d, row expects %dx%d"
                % (path, src.shape[1], src.shape[0], hw[1], hw[0]))
    else:
        src = crop_array(np.asarray(dmap, dtype=np.float64), box,
                         "disagreement", path)
        if src.shape[:2] != hw:
            _andon(
                "mismatched panel size: %s crop is %dx%d, row expects %dx%d"
                % (path, src.shape[1], src.shape[0], hw[1], hw[0]))
    return nn_zoom(colorize_heat(src, vmax), zoom), True


def build_view_sheet(maps, paths, regions, view_i, zoom=1,
                     heat_scale="global"):
    """Pure layout. maps/paths from load_target_inputs. regions is a list."""
    if heat_scale not in ("global", "region"):
        _andon("heat-scale must be global or region, got %r" % (heat_scale,))
    still_items = [
        (None if maps[k] is None else maps[k].shape[:2], paths[k])
        for k in ("reference", "shipped", "s3-vd", "s3-vi")
    ]
    full_hw = agreed_hw(still_items)
    if maps["disagreement"] is not None:
        dhw = maps["disagreement"].shape[:2]
        if full_hw is None:
            full_hw = dhw
        elif dhw != full_hw:
            _andon(
                "mismatched panel size: disagreement.npy is %dx%d, stills are %dx%d"
                % (dhw[1], dhw[0], full_hw[1], full_hw[0]))
    if full_hw is None:
        _andon("view %d: no source gives a panel size" % int(view_i))

    vmax_global = _heat_vmax(maps["disagreement"], None, "global")
    rows = []
    row_meta = []

    def still_row(box, title, stats_line, vmax):
        hw = full_hw if box is None else box_hw(box)
        panels = []
        caps = []
        present = {}
        for role in ("reference", "shipped", "s3-vd", "s3-vi"):
            src = maps[role]
            cropped = None
            if src is not None:
                cropped = src if box is None else crop_array(
                    src, box, title, paths[role])
            pan, ok = panel_for(cropped, hw, paths[role], zoom)
            panels.append(pan)
            present[role] = ok
            caps.append({
                "role": role,
                "path": _short_path(paths[role]) if ok else "MISSING",
            })
        hpan, hok = _heat_panel(
            maps["disagreement"], hw, box, vmax, zoom, paths["disagreement"])
        panels.append(hpan)
        caps.append({
            "role": "disagreement",
            "path": _short_path(paths["disagreement"]) if hok else "MISSING",
            "extra": "vmax=%.4f %s" % (vmax, heat_scale),
        })
        strip = compose_row(panels, caps, title, stats_line=stats_line)
        return strip, present

    title = "view %d  FULL  zoom=%d  heat=global vmax=%.4f" % (
        int(view_i), int(zoom), vmax_global)
    strip, _ = still_row(None, title, None, vmax_global)
    rows.append(strip)
    row_meta.append({"name": "FULL", "box": None, "stats": None})

    stats_out = []
    for reg in regions or []:
        box = reg["box"]
        name = reg["name"]
        vmax = vmax_global
        if heat_scale == "region":
            vmax = _heat_vmax(maps["disagreement"], box, "region")
        st = region_stats(
            box, maps["coverage"], maps["fallback"],
            maps["disagreement"], maps["owner"])
        line = format_stats(name, st)
        rtitle = "view %d  %s  box=%s" % (int(view_i), name, box)
        strip, _ = still_row(box, rtitle, line, vmax)
        rows.append(strip)
        row_meta.append({"name": name, "box": box, "stats": st})
        stats_out.append({"name": name, "box": box, "stats": st})

    return {
        "rows": rows,
        "row_meta": row_meta,
        "stats": stats_out,
        "full_hw": full_hw,
        "vmax_global": vmax_global,
        "zoom": int(zoom),
        "heat_scale": heat_scale,
    }


def render_sheet(built, consumed):
    body = stack_rows(built["rows"])
    foot = provenance_panel(consumed, body.shape[1])
    if foot.shape[1] < body.shape[1]:
        pad = np.full(
            (foot.shape[0], body.shape[1], 3), (12, 12, 16), dtype=np.uint8)
        pad[:, :foot.shape[1]] = foot
        foot = pad
    elif foot.shape[1] > body.shape[1]:
        pad = np.full(
            (body.shape[0], foot.shape[1], 3), BG_RGB, dtype=np.uint8)
        pad[:, :body.shape[1]] = body
        body = pad
    return stack_rows([body, foot])


def write_view(out_dir, view_i, rgb, consumed, built, regions_path):
    os.makedirs(out_dir, exist_ok=True)
    tag = "v%02d" % int(view_i)
    png = os.path.join(out_dir, "sheet_%s.png" % tag)
    Image.fromarray(as_rgb_u8(rgb), mode="RGB").save(png)
    return {
        "view": int(view_i),
        "sheet": os.path.abspath(png),
        "width": int(rgb.shape[1]),
        "height": int(rgb.shape[0]),
        "zoom": built["zoom"],
        "heat_scale": built["heat_scale"],
        "vmax_global": built["vmax_global"],
        "full_hw": [int(built["full_hw"][0]), int(built["full_hw"][1])],
        "regions_path": regions_path,
        "consumed": consumed,
        "stats": [
            {
                "name": s["name"],
                "box": s["box"],
                "area": s["stats"]["area"],
                "coverage_px": s["stats"]["coverage_px"],
                "fallback_px": s["stats"]["fallback_px"],
                "disagreement_mean": s["stats"]["disagreement_mean"],
                "disagreement_p90": s["stats"]["disagreement_p90"],
                "owner_hist": (
                    {str(k): v for k, v in s["stats"]["owner_hist"].items()}
                    if s["stats"]["owner_hist"] is not None else None),
                "missing": s["stats"]["missing"],
            }
            for s in built["stats"]
        ],
    }


def run(s3_dir, ref_dir, shipped_dir, regions_path, out_dir,
        zoom=1, heat_scale="global", views=None):
    spec = load_regions(regions_path)
    parsed = spec["_parsed"]
    if views is None:
        views = sorted(parsed)
    os.makedirs(out_dir, exist_ok=True)
    results = []
    for vi in views:
        maps, paths, consumed = load_target_inputs(
            s3_dir, ref_dir, shipped_dir, vi)
        built = build_view_sheet(
            maps, paths, parsed.get(int(vi), []), vi,
            zoom=zoom, heat_scale=heat_scale)
        rgb = render_sheet(built, consumed)
        results.append(write_view(
            out_dir, vi, rgb, consumed, built, os.path.abspath(regions_path)))
    manifest = {
        "tool": "s3_sheet.py",
        "tool_version": TOOL_VERSION,
        "s3_dir": os.path.abspath(s3_dir) if s3_dir else None,
        "ref_dir": os.path.abspath(ref_dir) if ref_dir else None,
        "shipped_dir": os.path.abspath(shipped_dir) if shipped_dir else None,
        "regions": os.path.abspath(regions_path),
        "zoom": int(zoom),
        "heat_scale": heat_scale,
        "views": [int(v) for v in views],
        "results": results,
    }
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    return manifest


# ---------------------------------------------------------------------------
# selftest fixtures and can-fail legs
# ---------------------------------------------------------------------------

def fixture_calibration_canvas(n=32):
    """Zeros, one hot pixel at the calibration origin."""
    a = np.zeros((n, n, 3), dtype=np.uint8)
    a[CALIBRATION_Y, CALIBRATION_X] = (CALIBRATION_VALUE, 0, 0)
    return a


def write_png(path, arr):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    Image.fromarray(as_rgb_u8(arr), mode="RGB").save(path)


def _selftest_calibration():
    src = fixture_calibration_canvas(32)
    crop = crop_nn(src, CALIBRATION_BOX, CALIBRATION_ZOOM,
                   name="pin", source="fixture")
    got = int(crop[0, 0, 0])
    if got != CALIBRATION_VALUE:
        _andon(
            "calibration crop[0,0] is %r, not %d"
            % (got, CALIBRATION_VALUE))
    # NN zoom of an 8x8 box is 16x16. A 1-px inclusive-box slip is 18.
    if crop.shape[0] != 16 or crop.shape[1] != 16:
        _andon("calibration crop shape is %s, not (16,16,3)" % (crop.shape,))
    return got


def _selftest_andon_can_fail():
    src = fixture_calibration_canvas(32)
    try:
        crop_array(src, [0, 0, 40, 40], "big", "fixture")
    except Andon:
        pass
    else:
        _andon("oversized box did not fire")
    a = np.zeros((32, 32, 3), dtype=np.uint8)
    b = np.zeros((16, 16, 3), dtype=np.uint8)
    try:
        compose_row([a, b], [{"role": "a", "path": "a"},
                             {"role": "b", "path": "b"}], "mismatch")
    except Andon:
        pass
    else:
        _andon("mismatched row did not fire")


def _selftest_missing_and_provenance(scratch):
    ref = fixture_calibration_canvas(32)
    ref_dir = os.path.join(scratch, "ref")
    ship_dir = os.path.join(scratch, "ship")
    s3_dir = os.path.join(scratch, "s3", "t00")
    os.makedirs(ref_dir, exist_ok=True)
    os.makedirs(ship_dir, exist_ok=True)
    os.makedirs(s3_dir, exist_ok=True)
    write_png(os.path.join(ref_dir, "twin_0.png"), ref)
    # shipped is ABSENT on purpose -- MISSING panel leg
    write_png(os.path.join(s3_dir, "dependent.png"), ref)
    write_png(os.path.join(s3_dir, "independent.png"), ref)
    dmap = np.full((32, 32), 0.25, dtype=np.float64)
    np.save(os.path.join(s3_dir, "disagreement.npy"), dmap)
    Image.fromarray(np.full((32, 32), 255, dtype=np.uint8)).save(
        os.path.join(s3_dir, "coverage.png"))
    Image.fromarray(np.zeros((32, 32), dtype=np.uint8)).save(
        os.path.join(s3_dir, "fallback.png"))
    np.save(os.path.join(s3_dir, "owner.npy"),
            np.zeros((32, 32), dtype=np.int32))
    regions = {
        "label": "selftest",
        "views": {
            "0": [{"name": "pin", "box": CALIBRATION_BOX, "from": "calibration"}]
        },
    }
    rpath = os.path.join(scratch, "regions.json")
    with open(rpath, "w", encoding="utf-8") as f:
        json.dump(regions, f)
    out_dir = os.path.join(scratch, "out")
    man = run(
        os.path.join(scratch, "s3"), ref_dir, ship_dir, rpath, out_dir,
        zoom=CALIBRATION_ZOOM, heat_scale="global", views=[0])
    maps, paths, consumed = load_target_inputs(
        os.path.join(scratch, "s3"), ref_dir, ship_dir, 0)
    if maps["shipped"] is not None:
        _andon("selftest shipped should be missing")
    built = build_view_sheet(
        maps, paths, regions["views"]["0"], 0,
        zoom=1, heat_scale="global")
    # Reconstruct the unzoomed shipped panel of the FULL row via loader.
    hw = built["full_hw"]
    shipped_panel, ok = panel_for(None, hw, paths["shipped"], 1)
    if ok:
        _andon("MISSING panel reported present")
    if not is_missing_panel(shipped_panel):
        _andon("MISSING panel is not the placeholder fill")
    real = maps["reference"]
    if real is None or is_missing_panel(real):
        _andon("reference was treated as MISSING")
    if int(real[CALIBRATION_Y, CALIBRATION_X, 0]) == int(shipped_panel[0, 0, 0]):
        _andon("MISSING panel is not detectably different from real content")

    ref_abs = os.path.abspath(os.path.join(ref_dir, "twin_0.png"))
    expect = sha256_file(ref_abs)
    found = None
    for e in consumed:
        if e.get("sha256") and os.path.normcase(e["path"]) == os.path.normcase(ref_abs):
            found = e["sha256"]
    if found is None:
        _andon("provenance did not record the reference file")
    if found != expect:
        _andon("provenance hash %s != recomputed %s" % (found, expect))
    # Manifest must carry the same hash, still equal to a fresh reread.
    m_found = None
    for e in man["results"][0]["consumed"]:
        if e.get("sha256") and os.path.normcase(e["path"]) == os.path.normcase(ref_abs):
            m_found = e["sha256"]
    if m_found != expect:
        _andon("manifest hash %s != recomputed %s" % (m_found, expect))
    return expect


def selftest(scratch=None):
    got = _selftest_calibration()
    _selftest_andon_can_fail()
    if scratch is None:
        import tempfile
        scratch = tempfile.mkdtemp(prefix="s3_sheet_")
    _selftest_missing_and_provenance(scratch)
    return got


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Acceptance sheet for S3 stills (layout only)")
    p.add_argument("--s3-dir", default=None)
    p.add_argument("--ref-dir", default=None)
    p.add_argument("--shipped-dir", default=None)
    p.add_argument("--regions", default=DEFAULT_REGIONS)
    p.add_argument("--out", default=None)
    p.add_argument("--zoom", type=int, default=1)
    p.add_argument("--heat-scale", default="global",
                   choices=("global", "region"))
    p.add_argument("--views", default=None)
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args(argv)
    if args.selftest:
        try:
            selftest(scratch=args.out)
        except Andon as e:
            sys.stderr.write(str(e) + "\n")
            return 2
        sys.stdout.write(
            "s3_sheet selftest OK  calibration crop[0,0] == %d\n"
            % CALIBRATION_VALUE)
        return 0
    if not args.s3_dir or not args.ref_dir or not args.shipped_dir or not args.out:
        p.error("need --s3-dir --ref-dir --shipped-dir --out (or --selftest)")
    views = None
    if args.views:
        views = [int(x) for x in args.views.split(",") if x.strip() != ""]
    try:
        man = run(
            args.s3_dir, args.ref_dir, args.shipped_dir, args.regions,
            args.out, zoom=args.zoom, heat_scale=args.heat_scale, views=views)
    except Andon as e:
        sys.stderr.write(str(e) + "\n")
        return 2
    sys.stdout.write(
        "s3_sheet wrote %d view(s) under %s\n" % (len(man["views"]), args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
