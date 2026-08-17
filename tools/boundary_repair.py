# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Atlas-space material-boundary repair. Retract a smear. Do not invent a sleeve.

WHY THIS EXISTS. Consult #12 / build #12. Every region the Director circled
is a material edge (armhole, fingers, boot-top). E51 repairs invented
orphans. Nothing yet repairs the mangled edge itself. This module is that
attempt, and it is built to argue with the brief that commissioned it.

THE THESIS, ATTACKED (measured 2026-08-17, before this file existed).

  "The mesh knows better than the paint does."
  The TRELLIS.2 prep mesh (`facet_E06/C1/prep/prep_uv.glb`) is
  TextureVisuals + a single PBRMaterial. There is no per-face material
  assignment. Geometry does not know tunic from flesh.

  Atlas island topology is not a material either. E33 packed 13,715
  islands. The spec names sixteen materials. Snapping paint to a UV
  chart snaps to a packer seam.

  The only material classifier already in this repo is palette_gate.py,
  and W3's palette has TWO hue bands: warm (skin, gold, leather, beard,
  red skirt) and green (tunic, green skirt panels). Gold-against-leather
  at the boot-top is TWO WARMS. This tool cannot see that edge. It can
  see green-against-warm, which is the armhole smear (tunic onto bare
  arm) and the fingers. The boot-top needs a different instrument.

  "Is this pixel near a boundary" is not contamination. A 2 px structure
  is entirely boundary. The rewrite set is the PROPERTY: above the
  chroma floor and in no declared band (the 105-125 gap on W3), with
  both neighbouring bands present as confident interiors. Clean thin
  paint is left alone.

  Snapping a contested edge to one answer trades a smear for a
  confidently-wrong edge. The sleeveless rule is the bound that
  remains after crispness is guaranteed by construction: GREEN area
  must not increase. The armhole smear is green on flesh; retracting
  green is the only direction this tool is allowed to move. Inventing
  a sleeve is the failure it exists to refuse.

  Atlas space is the right home. surfid = row * atlas_res + col
  (emit_view_aovs.py:300-304) is invertible on all 8 E45 views, 0 OOB.
  A few unique IDs land in the prep gutter (view_0: 374 of 100250).
  Re-projection is a nearest-texel lookup (--surfid / --view-out), not
  a second projector. Brush-through-the-cloud remains a Director-spend
  lever; this file spends none.

ENUMERATION (do not re-commission).
  palette_gate.py     LAB + chroma floor + two-threshold. Reused.
                      Cannot be imported (parse_args at module level);
                      to_lab is copied verbatim and T86 pins the source.
  mask_geometry.py    local_thickness. Available; this tool uses per-
                      component EDT width instead so a 4096 atlas does
                      not pay an O(R) EDT sweep. Same law, cheaper form.
  render_geomaps.py   MV-Adapter pos/nor maps. Not a repair.
  resample_atlas.py   dense-to-retopo transfer. Closed path.
  twin_fuse.py        multi-seed median. Not an edge.
  e13_harmonize.py    Reinhard tone transfer. Cannot move a family.
  texpass_iter        peel of a brush commit, not a material snap.
  callieri_border.py  a WEIGHT, not a rewrite.
  e37_fire_repaints   cloud composite. Credits.

CALIBRATION CLAIM (run --selftest; T86 pins the same numbers).
  32x32. Cols 0-13 solid warm (180,90,50). Cols 18-31 solid green
  (30,120,80). Cols 14-17 the mid mix (105,105,65) — W3 forbidden gap,
  classified OFF. A 2x8 green bar at [28:30, 2:10] and a 2x8 steel
  bar at [2:4, 2:10] (140,142,145, C* 1.85).
  After repair: out[8, 15] equals the warm solid (the mix snaps
  toward flesh). out[8, 17] stays the mix under --sleeveless
  (snapping it green would grow the tunic).
  The green bar is unchanged (thin + already in-band).
  The steel bar is byte-identical (below chroma floor).
  green_px does not increase.
  Construction: a near-boundary rewrite would eat the 2 px bar.
  A hue-on-steel rewrite would recolour the blade-like stripe.
  Growing green would fail the sleeveless gate.

  python tools/boundary_repair.py --selftest

YES/NO INTERVALS.

  labels     -2 = below chroma floor, -1 = off-palette, 0..B-1 = band.
  contested  OFF, chroma > floor, 3x3 contains >=1 confident pixel of
             two different bands. Not "distance to an edge < k".
  sleeveless GREEN count(out) <= GREEN count(in). Default on.
  peel       a contested texel may snap only if its distance to the
             opposing confident class is <= peel_frac * (2 * max EDT)
             of its nearest in-band component. Default peel_frac=1/3
             (A3). Per component, reported.
  low-chroma never rewritten.
  --atlas is read. --out is written beside. Undo = delete --out.

  python tools/boundary_repair.py --atlas A.png --mask mask.npy \\
         --palette docs/experiments/E08-W3-palette.json --out repaired.png
  python tools/boundary_repair.py --selftest
"""
from __future__ import annotations

import argparse
import ast
import io
import json
import os
import sys
import tempfile

import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt, label as cc_label

_TOOLS = os.path.dirname(os.path.abspath(__file__))
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

TOOL_VERSION = "1.0.0"
ATLAS_RES = 4096
DEFAULT_PEEL_FRAC = 1.0 / 3.0
LABEL_LOW = -2
LABEL_OFF = -1
STRUCTURE4 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.int32)

# Fixture solids. Hues checked against E08-W3-palette.json on 2026-08-17.
WARM_RGB = (180, 90, 50)      # C* 51.48  H 49.4   warm
GREEN_RGB = (30, 120, 80)     # C* 38.93  H 157.9  green
MIX_RGB = (105, 105, 65)      # C* 23.52  H 106.7  OFF (105-125 gap)
STEEL_RGB = (140, 142, 145)   # C* 1.85   H 265.8  low-chroma
CALIBRATION_Y = 8
CALIBRATION_X = 15  # mix, closer to warm than green; 17 is the refused side


class Andon(ValueError):
    pass


def _andon(msg):
    raise Andon("ANDON: " + msg)


def palette_gate_to_lab_source():
    """palette_gate.to_lab body, extracted without importing the module.

    palette_gate.py calls parse_args at module level, so `import palette_gate`
    cannot succeed under pytest's argv. Same extraction T64 uses on
    project_twins.fit_background.
    """
    src = io.open(os.path.join(_TOOLS, "palette_gate.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    fn = [n for n in tree.body
          if isinstance(n, ast.FunctionDef) and n.name == "to_lab"]
    if len(fn) != 1:
        _andon("palette_gate.to_lab not found exactly once")
    mod = ast.Module(body=[fn[0]], type_ignores=[])
    ns = {"np": np}
    exec(compile(ast.fix_missing_locations(mod), "<palette_gate>", "exec"), ns)
    return ns["to_lab"]


# Verbatim copy of palette_gate.to_lab (lines 98-109). T86 pins identity.
def to_lab(rgb):
    """sRGB -> linear -> XYZ (D65) -> Lab. Same transform as e08_deltaE.py."""
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16,
                     500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


def load_palette(path):
    if not os.path.isfile(path):
        _andon("no palette %s" % path)
    pal = json.load(open(path, encoding="utf-8"))
    if "allowed_bands" not in pal or "min_chroma" not in pal:
        _andon("palette needs allowed_bands and min_chroma: %s" % path)
    bands = []
    for b in pal["allowed_bands"]:
        bands.append((str(b["name"]), float(b["hue_deg"][0]), float(b["hue_deg"][1])))
    if not bands:
        _andon("palette has no bands")
    return pal, bands, float(pal["min_chroma"])


def classify(rgb01, bands, cmin):
    """Per-pixel label. -2 low chroma, -1 off-palette, 0..B-1 a band."""
    lab = to_lab(np.asarray(rgb01, dtype=np.float64))
    C = np.hypot(lab[..., 1], lab[..., 2])
    Hd = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360.0
    labels = np.full(C.shape, LABEL_OFF, dtype=np.int16)
    for i, (_n, lo, hi) in enumerate(bands):
        if lo <= hi:
            m = (Hd >= lo) & (Hd <= hi)
        else:
            m = (Hd >= lo) | (Hd <= hi)
        labels[m] = i
    labels[C <= cmin] = LABEL_LOW
    return labels, lab, C, Hd


def circular_hue_deg(lab, mask):
    """Hue of the mean chromatic vector. Not an arithmetic median of angles."""
    m = np.asarray(mask, dtype=bool)
    if not m.any():
        return None
    a = np.asarray(lab)[..., 1][m]
    b = np.asarray(lab)[..., 2][m]
    return float(np.degrees(np.arctan2(float(b.mean()), float(a.mean()))) % 360.0)


def load_atlas(path):
    if not os.path.isfile(path):
        _andon("no atlas %s" % path)
    im = Image.open(path).convert("RGB")
    return np.asarray(im, dtype=np.uint8)


def load_mask(path, hw):
    if not os.path.isfile(path):
        _andon("no mask %s" % path)
    raw = np.load(path)
    if raw.ndim == 3:
        valid = raw[..., 0] > 0.5
    elif raw.ndim == 2:
        valid = raw > 0.5
    else:
        _andon("mask must be (H,W) or (H,W,C), got %s" % (raw.shape,))
    if valid.shape != hw:
        _andon("mask %s vs atlas %s" % (valid.shape, hw))
    return valid


def confident_interior(labels, valid):
    """In-band pixels whose 4-neighbours are the same band or invalid."""
    lab = np.asarray(labels)
    conf = valid & (lab >= 0)
    h, w = lab.shape
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        ys = slice(max(0, dy), h + min(0, dy))
        xs = slice(max(0, dx), w + min(0, dx))
        y2 = slice(max(0, -dy), h + min(0, -dy))
        x2 = slice(max(0, -dx), w + min(0, -dx))
        nb = lab[y2, x2]
        nb_valid = valid[y2, x2]
        me = lab[ys, xs]
        bad = nb_valid & (nb >= 0) & (nb != me)
        tmp = conf[ys, xs].copy()
        tmp[bad] = False
        conf[ys, xs] = tmp
    return conf


def contested_off(labels, valid, conf, n_bands, peel_frac, band_width):
    """OFF (not low-chroma) reachable from two confident bands inside
    each band's own peel. Not 'distance to any edge < k'.
    """
    off = valid & (labels == LABEL_OFF)
    if not off.any():
        return np.zeros_like(off)
    reach = np.zeros(off.shape, dtype=np.int16)
    for b in range(n_bands):
        src = conf & (labels == b)
        if not src.any():
            continue
        limit = max(1.0, np.floor(peel_frac * float(band_width[b])))
        d = distance_transform_edt(~src)
        reach += (d <= limit).astype(np.int16)
    return off & (reach >= 2)


def component_widths(labels, valid, n_bands):
    """Per-pixel width = 2 * max EDT of that pixel's in-band component."""
    width = np.zeros(labels.shape, dtype=np.float64)
    reports = []
    for b in range(n_bands):
        m = valid & (labels == b)
        if not m.any():
            continue
        # One EDT of the band equals per-component EDT inside each
        # component: components of one band do not touch.
        edt = distance_transform_edt(m)
        lab, n = cc_label(m, structure=STRUCTURE4)
        max_edt = np.zeros(n + 1, dtype=np.float64)
        np.maximum.at(max_edt, lab, edt)
        wmap = 2.0 * max_edt[lab]
        wmap[lab == 0] = 0.0
        width[m] = wmap[m]
        counts = np.bincount(lab.ravel())
        reports.append({
            "band": int(b),
            "n_components": int(n),
            "area_px": int(m.sum()),
            "width_max_px": float(2.0 * max_edt[1:].max()) if n else 0.0,
            "largest_component_px": int(counts[1:].max()) if n else 0,
        })
    return width, reports


def snap(rgb, labels, valid, conf, contested, width, peel_frac, n_bands,
         green_band, sleeveless, band_width):
    """Rewrite contested texels. Green may retract; it may not grow."""
    if peel_frac <= 0 or peel_frac > 1:
        _andon("peel-frac must be in (0, 1], got %r" % peel_frac)
    out = np.asarray(rgb, dtype=np.uint8).copy()
    green_in = int((valid & (labels == green_band)).sum()) if green_band is not None else 0
    if not contested.any():
        return out, {
            "touched_px": 0,
            "green_in": green_in,
            "green_out": green_in,
            "refused_green_growth": 0,
            "touched": np.zeros(labels.shape, dtype=bool),
            "per_component_touched": [],
        }
    dist = []
    for b in range(n_bands):
        src = conf & (labels == b)
        if src.any():
            dist.append(distance_transform_edt(~src))
        else:
            dist.append(np.full(labels.shape, np.inf))
    stacked = np.stack(
        [d if np.isfinite(d).any() else np.full(labels.shape, 1e18)
         for d in dist],
        axis=-1)
    vote = np.argmin(stacked, axis=-1)
    nearest = np.take_along_axis(stacked, vote[..., None], -1)[..., 0]
    bw = np.asarray(band_width, dtype=np.float64)
    limit = np.maximum(1.0, np.floor(peel_frac * width))
    z = width <= 0
    if z.any() and bw.size:
        limit = np.where(z, np.maximum(1.0, np.floor(peel_frac * bw[vote])), limit)
    apply = contested & (nearest <= limit)
    refused = 0
    if sleeveless and green_band is not None:
        grow = apply & (vote == green_band) & (labels != green_band)
        refused = int(grow.sum())
        apply = apply & ~grow
    mean_rgb = []
    for b in range(n_bands):
        m = conf & (labels == b)
        if m.any():
            mean_rgb.append(np.mean(out[m], axis=0))
        else:
            mean_rgb.append(None)
    for b in range(n_bands):
        if mean_rgb[b] is None:
            continue
        sel = apply & (vote == b)
        if sel.any():
            out[sel] = np.clip(np.rint(mean_rgb[b]), 0, 255).astype(np.uint8)
    touched = apply
    return out, {
        "touched_px": int(touched.sum()),
        "green_in": green_in,
        "refused_green_growth": refused,
        "touched": touched,
        "per_component_touched": [],
    }


def band_index(bands, name):
    for i, (n, _lo, _hi) in enumerate(bands):
        if n == name:
            return i
    return None


def repair(rgb_u8, valid, bands, cmin, peel_frac=DEFAULT_PEEL_FRAC,
           sleeveless=True):
    rgb = np.asarray(rgb_u8, dtype=np.uint8)
    if rgb.ndim != 3 or rgb.shape[-1] < 3:
        _andon("atlas must be HxWx3, got %s" % (rgb.shape,))
    if valid.shape != rgb.shape[:2]:
        _andon("mask %s vs atlas %s" % (valid.shape, rgb.shape[:2]))
    labels, lab, C, Hd = classify(rgb.astype(np.float64) / 255.0, bands, cmin)
    labels = labels.copy()
    labels[~valid] = LABEL_OFF
    conf = confident_interior(labels, valid)
    width, comp_rep = component_widths(labels, valid, len(bands))
    band_width = []
    for b in range(len(bands)):
        ws = [c["width_max_px"] for c in comp_rep if c["band"] == b]
        band_width.append(max(ws) if ws else 0.0)
    contested = contested_off(
        labels, valid, conf, len(bands), peel_frac, band_width)
    green_i = band_index(bands, "green")
    out, snap_rep = snap(
        rgb, labels, valid, conf, contested, width, peel_frac,
        len(bands), green_i, sleeveless, band_width)
    out_labels, out_lab, _, _ = classify(
        out.astype(np.float64) / 255.0, bands, cmin)
    out_labels[~valid] = LABEL_OFF
    green_in = int((valid & (labels == green_i)).sum()) if green_i is not None else 0
    green_out = int((valid & (out_labels == green_i)).sum()) if green_i is not None else 0
    if sleeveless and green_i is not None and green_out > green_in:
        _andon(
            "sleeveless: green area grew %d -> %d (invented sleeve / tunic expansion)"
            % (green_in, green_out))
    # low-chroma must be byte-identical
    low = valid & (labels == LABEL_LOW)
    if low.any() and not np.array_equal(out[low], rgb[low]):
        _andon("low-chroma texels were rewritten; hue is not a colour below the floor")
    touched = snap_rep["touched"]
    per = []
    for rec in comp_rep:
        rec = dict(rec)
        rec["peel_px"] = float(max(1.0, np.floor(peel_frac * rec["width_max_px"])))
        rec["touched_px"] = int(touched.sum()) if rec["band"] >= 0 else 0
        per.append(rec)
    report = {
        "tool": "boundary_repair.py",
        "tool_version": TOOL_VERSION,
        "bands": [{"name": n, "lo": lo, "hi": hi} for n, lo, hi in bands],
        "min_chroma": cmin,
        "peel_frac": float(peel_frac),
        "sleeveless": bool(sleeveless),
        "valid_px": int(valid.sum()),
        "contested_px": int(contested.sum()),
        "touched_px": int(touched.sum()),
        "green_in": green_in,
        "green_out": green_out,
        "refused_green_growth": snap_rep["refused_green_growth"],
        "low_chroma_px": int(low.sum()),
        "components": per,
        "note": "not a quality grade; the Director's eye is the acceptance gate",
    }
    return out, report


def decode_surfid(surfid, atlas_res=ATLAS_RES):
    s = np.asarray(surfid)
    valid = s >= 0
    row = np.full(s.shape, -1, dtype=np.int64)
    col = np.full(s.shape, -1, dtype=np.int64)
    row[valid] = s[valid] // int(atlas_res)
    col[valid] = s[valid] % int(atlas_res)
    recon = np.full(s.shape, -1, dtype=np.int64)
    recon[valid] = row[valid] * int(atlas_res) + col[valid]
    if valid.any() and not np.array_equal(recon[valid], s[valid]):
        _andon("surfid is not row * atlas_res + col")
    return row, col


def project_atlas_through_surfid(atlas, surfid, atlas_res=ATLAS_RES):
    row, col = decode_surfid(surfid, atlas_res)
    valid = surfid >= 0
    H, W = atlas.shape[:2]
    if H != atlas_res or W != atlas_res:
        _andon("atlas is %dx%d, atlas_res=%d" % (H, W, atlas_res))
    out = np.zeros(surfid.shape + (3,), dtype=np.uint8)
    rr = row[valid]
    cc = col[valid]
    inside = (rr >= 0) & (rr < H) & (cc >= 0) & (cc < W)
    idx = np.where(valid)
    keep_y = idx[0][inside]
    keep_x = idx[1][inside]
    out[keep_y, keep_x] = atlas[rr[inside], cc[inside]]
    return out


def fixture_calibration(n=32):
    rgb = np.zeros((n, n, 3), dtype=np.uint8)
    rgb[:, 0:14] = WARM_RGB
    rgb[:, 18:n] = GREEN_RGB
    rgb[:, 14:18] = MIX_RGB
    rgb[28:30, 2:10] = GREEN_RGB
    rgb[2:4, 2:10] = STEEL_RGB
    valid = np.ones((n, n), dtype=bool)
    return rgb, valid


def write_png(path, arr):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    Image.fromarray(np.asarray(arr, dtype=np.uint8), mode="RGB").save(path)


def default_palette_path():
    return os.path.join(
        os.path.dirname(_TOOLS), "docs", "experiments", "E08-W3-palette.json")


def _selftest_calibration(scratch, palette_path):
    rgb, valid = fixture_calibration()
    _pal, bands, cmin = load_palette(palette_path)
    out, rep = repair(rgb, valid, bands, cmin, peel_frac=DEFAULT_PEEL_FRAC,
                      sleeveless=True)
    got = tuple(int(v) for v in out[CALIBRATION_Y, CALIBRATION_X])
    if got != WARM_RGB:
        _andon(
            "calibration out[%d,%d] is %s, not warm %s "
            "(mix did not snap, or snapped the wrong way)"
            % (CALIBRATION_Y, CALIBRATION_X, got, WARM_RGB))
    if not np.array_equal(out[28:30, 2:10], rgb[28:30, 2:10]):
        _andon("thin green bar was rewritten; near-boundary proxy ate a structure")
    if not np.array_equal(out[2:4, 2:10], rgb[2:4, 2:10]):
        _andon("steel bar was rewritten; hue was applied below the chroma floor")
    if rep["green_out"] > rep["green_in"]:
        _andon("sleeveless failed: green %d -> %d" % (
            rep["green_in"], rep["green_out"]))
    write_png(os.path.join(scratch, "in.png"), rgb)
    write_png(os.path.join(scratch, "out.png"), out)
    return out, rep


def selftest(scratch=None, palette_path=None):
    if scratch is None:
        scratch = tempfile.mkdtemp(prefix="boundary_repair_")
    if palette_path is None:
        palette_path = default_palette_path()
    # source-identity of to_lab against palette_gate
    theirs = palette_gate_to_lab_source()
    x = np.linspace(0.0, 1.0, 12, dtype=np.float64).reshape(2, 2, 3)
    if not np.allclose(to_lab(x), theirs(x), rtol=0, atol=0):
        _andon("to_lab drifted from palette_gate.to_lab")
    return _selftest_calibration(scratch, palette_path)


def build_parser():
    p = argparse.ArgumentParser(
        description="Retract an off-palette smear at a warm/green edge. "
                    "Does not invent a sleeve.")
    p.add_argument("--atlas", default=None, help="source atlas PNG (read-only)")
    p.add_argument("--mask", default=None, help="prep mask.npy")
    p.add_argument("--palette", default=None,
                   help="palette_gate JSON (W3: docs/experiments/E08-W3-palette.json)")
    p.add_argument("--out", default=None, help="repaired atlas PNG")
    p.add_argument("--json-out", default=None)
    p.add_argument("--peel-frac", default=None,
                   help="fraction of per-component width (default 1/3). "
                        "Pass as --peel-frac=0.33 — argparse eats a leading minus.")
    p.add_argument("--sleeveless", dest="sleeveless", action="store_true",
                   default=True)
    p.add_argument("--allow-green-growth", dest="sleeveless",
                   action="store_false",
                   help="opt out of the sleeveless retract-only rule")
    p.add_argument("--surfid", default=None,
                   help="optional view-space surfid.npy to preview the repair")
    p.add_argument("--view-out", default=None,
                   help="PNG of the repaired atlas looked up through --surfid")
    p.add_argument("--selftest", action="store_true")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.selftest:
            _out, _rep = selftest()
            sys.stdout.write(
                "calibration out[%d,%d] == %s  thin bar held  steel held  "
                "green did not grow\n"
                % (CALIBRATION_Y, CALIBRATION_X, WARM_RGB))
            return 0
        if not args.atlas or not args.mask or not args.out:
            _andon("need --atlas, --mask, --out (or --selftest)")
        palette = args.palette or default_palette_path()
        peel = DEFAULT_PEEL_FRAC if args.peel_frac is None else float(args.peel_frac)
        rgb = load_atlas(args.atlas)
        valid = load_mask(args.mask, rgb.shape[:2])
        _pal, bands, cmin = load_palette(palette)
        out, report = repair(
            rgb, valid, bands, cmin, peel_frac=peel,
            sleeveless=bool(args.sleeveless))
        if os.path.abspath(args.out) == os.path.abspath(args.atlas):
            _andon("--out must not be --atlas; this tool writes beside")
        write_png(args.out, out)
        report["atlas"] = os.path.abspath(args.atlas)
        report["out"] = os.path.abspath(args.out)
        report["palette"] = os.path.abspath(palette)
        if args.surfid:
            if not args.view_out:
                _andon("--surfid needs --view-out")
            sid = np.load(args.surfid)
            view = project_atlas_through_surfid(out, sid, atlas_res=out.shape[0])
            write_png(args.view_out, view)
            report["view_out"] = os.path.abspath(args.view_out)
        sys.stdout.write(
            "boundary_repair %s  contested=%d  touched=%d  green %d -> %d  "
            "refused_growth=%d  (not a spend recommendation, not a grade)\n"
            % (TOOL_VERSION, report["contested_px"], report["touched_px"],
               report["green_in"], report["green_out"],
               report["refused_green_growth"]))
        if args.json_out:
            os.makedirs(
                os.path.dirname(os.path.abspath(args.json_out)) or ".",
                exist_ok=True)
            with open(args.json_out, "w", encoding="utf-8", newline="\n") as f:
                json.dump(report, f, indent=1)
                f.write("\n")
        return 0
    except Andon as e:
        sys.stderr.write(str(e) + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
