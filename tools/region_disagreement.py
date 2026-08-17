# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Plate-disagreement inside named regions. The spend-decision instrument.

WHY THIS EXISTS. Consult #11 / build #11. A canon build-out plus eight-twin
regen costs Comfy Cloud credits the Director approves personally. The
advisor's inference: high plate disagreement => regen; agree-and-still-wrong
=> a compositor pass is the cheaper fix. This module measures the number
that inference wants, and it is built to argue with that inference rather
than to ratify it.

WHAT THE INFERENCE MISSES (measured on facet_E46, 2026-08-17, before this
file existed).

  S3 already has three worlds, not two:

    clean + low disagreement   -> plates compose; 3D path degrades them
    blotchy + high             -> sources inconsistent (warp or plate fight)
    blotchy + ~0               -> plates share the defect; this map is blind

  The advisor's "agree and still wrong => compositor" collapses world 1
  and world 3. World 3 is a shared source defect (thin canon, unnamed
  joints). A compositor cannot invent a named greave. This instrument
  therefore NEVER emits a spend recommendation. Low disagreement means
  "this map cannot see the defect." High disagreement means "the plates
  do not agree here." Which of those is worth credits is the Director's
  eye plus whether the plates themselves are blotchy.

  Photometric disagreement and owner-flicker are different questions.
  On s3_off t07 the grip box is BELOW figure median (0.72x) and ABOVE
  figure flicker (2.27x). Collapsing them into "plates disagree about
  what a surface is" hides that split.

  A share-of-nonzero is dead on arrival. s3_on/t00: 141165 owned of
  770048; disagreement is nonzero on 122439 frame pixels (121112 of
  those owned). 122439/141165 = 86.7% mixes an all-frame numerator
  with an owned denominator. Owned-only is 85.8%. Either way the
  statistic cannot separate a region from the figure.

WHAT THIS EMITS. Per (mode, view, region), including a figure row:

  owned_px          the denominator. Measured: disagreement is an AREA
                    quantity. Coverage-edge median is LOWER than interior.
                    Owner-edge is only mildly enriched (mass share ~1.25x
                    pixel share). Interior still carries 45-60% of the
                    mass. Perimeter normalisation is the wrong law here.
  dis_median/p90    magnitude inside owned pixels of the region
  fig_median/p90    the same reductions on the whole figure (base rate)
  hot_px, hot_lcc   owned pixels with dis > fig_p90, and the largest
                    4-connected component of those. Two-thresholds law:
                    a total alone must choose between missing a blob and
                    firing on speckle.
  flicker_rate      share of owned 4-neighbour pairs whose owner labels
                    differ, region vs figure. Semantic, not photometric.

Threshold is figure-owned p90, computed on the WHOLE figure before any
region is reduced. Deriving it from the region under test is a tautology.

WHICH FLOW MODE. Default s3_off. Flow is a compositor-side correction;
using s3_on mixes "did flow help" into "do the plates disagree." Rank
order of the E40 boxes was the same in both modes on E46; magnitudes
are 8-16% lower with flow on. --mode both reports both.

REGION SET. This tool does not invent boxes. tools/s3_sheet_regions.json
is labelled PROPOSALS, covers views 0/1/7 only, and has no arm and no
hand. The Director named arm (not a sleeve; the reference is sleeveless),
hand, boot-tops/greaves, tabard, skirt. Filling those is a transcription
of his pointing, not a derivation from owner islands. --figure-only
runs without a spec. A box that misses the figure reports owned_px=0
and refuses to invent ratios.

CALIBRATION CLAIM (run --selftest; T85 pins the same numbers).
  32x32. Figure owner=0 on [8:24, 8:24] (256 px), else -1.
  disagreement = 0.04 on the figure, except a 4x4 coherent block at
  [12:16, 12:16] = 0.40 and four isolated corners of the figure = 0.40.
  field box [8,8,24,24]: median == 0.04, hot_px == 20, hot_lcc == 16.
  blob  box [12,12,16,16]: median == 0.40, hot_px == 16, hot_lcc == 16.
  Construction: 236 px at 0.04 keep figure p90 at 0.04, so hot is
  dis > 0.04. A region-derived threshold on the blob (p90=0.40) would
  report hot_px == 0. A total-only readout cannot separate 20 from 16.

  python tools/region_disagreement.py --selftest

YES/NO INTERVALS.

  disagreement      (H,W) float, >= 0. 0 = agree or a single valid plate.
  owner             (H,W) int, -1 = unowned, 0..V-1 = plate.
  box               half-open [x0,y0,x1,y1]. Exceeding the source ANDON's.
                    Empty (x1<=x0 or y1<=y0) ANDON's.
  owned_px          count of owner >= 0 inside the box. Denominator.
  hot               owned AND disagreement > figure_owned_p90 (strict).
  flicker           flips / owned-owned 4-neighbour pairs. 0 if no pair.

  python tools/region_disagreement.py --tree DIR --mode s3_off \\
         --regions tools/s3_sheet_regions.json [--json-out PATH]
  python tools/region_disagreement.py --tree DIR --mode both --figure-only
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile

import numpy as np
from scipy.ndimage import label as cc_label

_TOOLS = os.path.dirname(os.path.abspath(__file__))
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import s3_sheet as S  # noqa: E402

TOOL_VERSION = "1.0.0"

MODES = ("s3_off", "s3_on")
HOT_PERCENTILE = 90.0
CALIBRATION_FIELD_MEDIAN = 0.04
CALIBRATION_BLOB_MEDIAN = 0.40
CALIBRATION_FIELD_HOT = 20
CALIBRATION_FIELD_LCC = 16
CALIBRATION_BLOB_HOT = 16
CALIBRATION_BLOB_LCC = 16
CALIBRATION_OWNED = 256
STRUCTURE4 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.int32)


class Andon(ValueError):
    pass


def _andon(msg):
    raise Andon("ANDON: " + msg)


def parse_views(text):
    """Comma-separated view indices. argparse would eat a leading minus
    on a numeric flag; this path is a string on purpose."""
    if text is None or text == "":
        return None
    out = []
    for part in str(text).split(","):
        p = part.strip()
        if not p:
            continue
        try:
            out.append(int(p, 10))
        except ValueError:
            _andon("views must be comma-separated integers, got %r" % text)
    if not out:
        _andon("views is empty")
    return out


def load_regions(path):
    if not os.path.isfile(path):
        _andon("no regions file %s" % path)
    with open(path, encoding="utf-8") as f:
        spec = json.load(f)
    if not isinstance(spec, dict) or "views" not in spec:
        _andon("regions file needs a views object: %s" % path)
    views = spec["views"]
    if not isinstance(views, dict):
        _andon("views must be an object")
    out = {}
    for key, regs in views.items():
        try:
            vi = int(key)
        except (TypeError, ValueError):
            _andon("view key %r is not an int" % (key,))
        if not isinstance(regs, list):
            _andon("view %s regions must be a list" % key)
        cleaned = []
        for i, r in enumerate(regs):
            if not isinstance(r, dict) or "name" not in r or "box" not in r:
                _andon("view %s region %d needs name and box" % (key, i))
            box = S.as_box(r["box"])
            cleaned.append({
                "name": str(r["name"]),
                "box": [int(box[0]), int(box[1]), int(box[2]), int(box[3])],
                "from": r.get("from"),
            })
        out[vi] = cleaned
    return spec, out


def load_view(tree, mode, view):
    if mode not in MODES:
        _andon("mode must be s3_off or s3_on, got %r" % (mode,))
    if int(view) != view or int(view) < 0:
        _andon("view must be a non-negative int, got %r" % (view,))
    td = os.path.join(tree, mode, "t%02d" % int(view))
    d_path = os.path.join(td, "disagreement.npy")
    o_path = os.path.join(td, "owner.npy")
    if not os.path.isdir(td):
        _andon("missing view dir %s" % td)
    if not os.path.isfile(d_path):
        _andon("missing %s" % d_path)
    if not os.path.isfile(o_path):
        _andon("missing %s" % o_path)
    dis = np.load(d_path)
    own = np.load(o_path)
    if dis.ndim != 2:
        _andon("disagreement must be (H,W), got %s from %s" % (dis.shape, d_path))
    if own.ndim != 2:
        _andon("owner must be (H,W), got %s from %s" % (own.shape, o_path))
    if dis.shape != own.shape:
        _andon(
            "disagreement %s and owner %s differ at view %s"
            % (dis.shape, own.shape, view))
    if np.any(dis < 0):
        _andon("disagreement has negatives in %s" % d_path)
    return {
        "disagreement": np.asarray(dis, dtype=np.float64),
        "owner": np.asarray(own),
        "dir": td,
        "disagreement_path": os.path.abspath(d_path),
        "owner_path": os.path.abspath(o_path),
    }


def flicker_rate(owner, mask):
    """flips / owned-owned 4-neighbour pairs inside mask. None if no pair."""
    own = np.asarray(owner)
    m = np.asarray(mask, dtype=bool)
    if own.shape != m.shape:
        _andon("flicker mask shape %s != owner %s" % (m.shape, own.shape))
    pairs = 0
    flips = 0
    h, w = own.shape
    for dy, dx in ((0, 1), (1, 0)):
        a = own[0:h - dy, 0:w - dx]
        b = own[dy:h, dx:w]
        ma = m[0:h - dy, 0:w - dx]
        mb = m[dy:h, dx:w]
        both = (a >= 0) & (b >= 0) & ma & mb
        pairs += int(both.sum())
        flips += int((both & (a != b)).sum())
    if pairs == 0:
        return {"pairs": 0, "flips": 0, "rate": None}
    return {"pairs": pairs, "flips": flips, "rate": float(flips) / float(pairs)}


def largest_cc(mask):
    """Largest 4-connected component of a boolean mask. 0 if empty."""
    m = np.asarray(mask, dtype=bool)
    total = int(m.sum())
    if total == 0:
        return 0, 0
    lab, n = cc_label(m, structure=STRUCTURE4)
    if n == 0:
        return total, 0
    counts = np.bincount(lab.ravel())
    # index 0 is background
    return total, int(counts[1:].max()) if counts.size > 1 else 0


def _reductions(dis, owned):
    if not owned.any():
        return {
            "owned_px": 0,
            "median": None,
            "p90": None,
            "mean": None,
        }
    vals = np.asarray(dis)[owned]
    return {
        "owned_px": int(owned.sum()),
        "median": float(np.median(vals)),
        "p90": float(np.percentile(vals, HOT_PERCENTILE)),
        "mean": float(vals.mean()),
    }


def figure_stats(dis, owner):
    owned = np.asarray(owner) >= 0
    red = _reductions(dis, owned)
    flick = flicker_rate(owner, owned)
    p90 = red["p90"]
    if red["owned_px"] == 0 or p90 is None:
        hot = np.zeros(owned.shape, dtype=bool)
    else:
        hot = owned & (np.asarray(dis) > p90)
    hot_px, hot_lcc = largest_cc(hot)
    red.update({
        "box_px": int(np.asarray(dis).size),
        "flicker_pairs": flick["pairs"],
        "flicker_flips": flick["flips"],
        "flicker_rate": flick["rate"],
        "hot_px": hot_px,
        "hot_lcc": hot_lcc,
        "hot": hot,
        "owned": owned,
    })
    return red


def region_row(dis, owner, box, fig, name, view, mode):
    x0, y0, x1, y1 = S.as_box(box)
    H, W = np.asarray(dis).shape[:2]
    if x0 < 0 or y0 < 0 or x1 > W or y1 > H:
        _andon(
            "crop box %s %s exceeds source %dx%d"
            % (name, [x0, y0, x1, y1], W, H))
    box_mask = np.zeros((H, W), dtype=bool)
    box_mask[y0:y1, x0:x1] = True
    owned = (np.asarray(owner) >= 0) & box_mask
    red = _reductions(dis, owned)
    flick = flicker_rate(owner, owned)
    fig_p90 = fig["p90"]
    if red["owned_px"] == 0 or fig_p90 is None:
        hot = np.zeros((H, W), dtype=bool)
    else:
        hot = owned & (np.asarray(dis) > fig_p90)
    hot_px, hot_lcc = largest_cc(hot)
    owned_px = red["owned_px"]
    fig_owned = fig["owned_px"]
    fig_med = fig["median"]
    fig_flick = fig["flicker_rate"]
    med = red["median"]
    p90 = red["p90"]
    rate = flick["rate"]
    return {
        "mode": mode,
        "view": int(view),
        "name": name,
        "box": [int(x0), int(y0), int(x1), int(y1)],
        "box_px": int(box_mask.sum()),
        "owned_px": owned_px,
        "dis_median": med,
        "dis_p90": p90,
        "dis_mean": red["mean"],
        "fig_owned_px": fig_owned,
        "fig_median": fig_med,
        "fig_p90": fig_p90,
        "fig_flicker_rate": fig_flick,
        "ratio_median": (
            None if med is None or not fig_med else float(med) / float(fig_med)),
        "ratio_p90": (
            None if p90 is None or not fig_p90 else float(p90) / float(fig_p90)),
        "hot_px": hot_px,
        "hot_share": (
            None if owned_px == 0 else float(hot_px) / float(owned_px)),
        "hot_lcc": hot_lcc,
        "hot_lcc_share": (
            None if hot_px == 0 else float(hot_lcc) / float(hot_px)),
        "flicker_pairs": flick["pairs"],
        "flicker_flips": flick["flips"],
        "flicker_rate": rate,
        "flicker_ratio": (
            None if rate is None or not fig_flick
            else float(rate) / float(fig_flick)),
        "threshold": "figure_owned_p90",
        "hot_rule": "disagreement > figure_owned_p90",
        "denominator": "owned_px",
    }


def discover_views(tree, mode):
    root = os.path.join(tree, mode)
    if not os.path.isdir(root):
        _andon("missing mode dir %s" % root)
    found = []
    for name in sorted(os.listdir(root)):
        if len(name) == 3 and name.startswith("t") and name[1:].isdigit():
            found.append(int(name[1:]))
    if not found:
        _andon("no tNN dirs under %s" % root)
    return found


def run(tree, mode, regions_path=None, views=None, figure_only=False):
    if not os.path.isdir(tree):
        _andon("no tree %s" % tree)
    if mode == "both":
        modes = list(MODES)
    elif mode in MODES:
        modes = [mode]
    else:
        _andon("mode must be s3_off, s3_on, or both, got %r" % (mode,))
    spec = None
    spec_views = {}
    if regions_path:
        spec, spec_views = load_regions(regions_path)
    elif not figure_only:
        _andon("need --regions or --figure-only")
    rows = []
    for md in modes:
        if views is not None:
            wanted = list(views)
        elif spec_views:
            wanted = sorted(spec_views)
        else:
            wanted = discover_views(tree, md)
        for vi in wanted:
            maps = load_view(tree, md, vi)
            fig = figure_stats(maps["disagreement"], maps["owner"])
            H, W = maps["disagreement"].shape
            rows.append(region_row(
                maps["disagreement"], maps["owner"],
                [0, 0, W, H], fig, "figure", vi, md))
            for r in spec_views.get(vi, []):
                rows.append(region_row(
                    maps["disagreement"], maps["owner"],
                    r["box"], fig, r["name"], vi, md))
    return {
        "tool": "region_disagreement.py",
        "tool_version": TOOL_VERSION,
        "tree": os.path.abspath(tree),
        "mode": mode,
        "regions": (
            os.path.abspath(regions_path) if regions_path else None),
        "label": None if spec is None else spec.get("label"),
        "rows": rows,
    }


def _fmt(v, nd=4):
    if v is None:
        return "-"
    if isinstance(v, float):
        return "%.*f" % (nd, v)
    return str(v)


def format_table(payload):
    lines = [
        "region_disagreement %s  tree=%s  mode=%s"
        % (TOOL_VERSION, payload["tree"], payload["mode"]),
        "denominator=owned_px  hot=dis>figure_p90  "
        "this table is not a spend recommendation",
        "",
        "%-7s %4s %-12s %7s %7s %7s %7s %7s %6s %6s %5s %7s %7s"
        % ("mode", "view", "region", "owned", "med", "p90",
           "figmed", "figp90", "rmed", "hot", "lcc", "flick", "frat"),
    ]
    for r in payload["rows"]:
        lines.append(
            "%-7s %4d %-12s %7d %7s %7s %7s %7s %6s %6d %5d %7s %7s"
            % (r["mode"], r["view"], r["name"][:12], r["owned_px"],
               _fmt(r["dis_median"]), _fmt(r["dis_p90"]),
               _fmt(r["fig_median"]), _fmt(r["fig_p90"]),
               _fmt(r["ratio_median"], 2), r["hot_px"], r["hot_lcc"],
               _fmt(r["flicker_rate"]), _fmt(r["flicker_ratio"], 2)))
    return "\n".join(lines) + "\n"


def write_json(payload, path):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, indent=1)
        f.write("\n")


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------

def fixture_calibration():
    """The pinned construction. 32x32. See module docstring."""
    n = 32
    own = np.full((n, n), -1, dtype=np.int16)
    own[8:24, 8:24] = 0
    dis = np.zeros((n, n), dtype=np.float64)
    dis[8:24, 8:24] = CALIBRATION_FIELD_MEDIAN
    dis[12:16, 12:16] = CALIBRATION_BLOB_MEDIAN
    for y, x in ((8, 8), (8, 23), (23, 8), (23, 23)):
        dis[y, x] = CALIBRATION_BLOB_MEDIAN
    return dis, own


def write_view_tree(root, mode, view, dis, own):
    td = os.path.join(root, mode, "t%02d" % int(view))
    os.makedirs(td, exist_ok=True)
    np.save(os.path.join(td, "disagreement.npy"), dis)
    np.save(os.path.join(td, "owner.npy"), own)
    return td


def _selftest_calibration(scratch):
    dis, own = fixture_calibration()
    write_view_tree(scratch, "s3_off", 0, dis, own)
    regions = {
        "label": "selftest",
        "views": {
            "0": [
                {"name": "field", "box": [8, 8, 24, 24]},
                {"name": "blob", "box": [12, 12, 16, 16]},
            ]
        },
    }
    rpath = os.path.join(scratch, "regions.json")
    with open(rpath, "w", encoding="utf-8") as f:
        json.dump(regions, f)
    payload = run(scratch, "s3_off", rpath, views=[0])
    by = {r["name"]: r for r in payload["rows"]}
    field, blob, fig = by["field"], by["blob"], by["figure"]
    if fig["owned_px"] != CALIBRATION_OWNED:
        _andon("figure owned_px is %r, not %d" % (
            fig["owned_px"], CALIBRATION_OWNED))
    if field["owned_px"] != CALIBRATION_OWNED:
        _andon("field owned_px is %r, not %d" % (
            field["owned_px"], CALIBRATION_OWNED))
    if abs(field["dis_median"] - CALIBRATION_FIELD_MEDIAN) > 1e-12:
        _andon("field median is %r, not %s" % (
            field["dis_median"], CALIBRATION_FIELD_MEDIAN))
    if abs(blob["dis_median"] - CALIBRATION_BLOB_MEDIAN) > 1e-12:
        _andon("blob median is %r, not %s" % (
            blob["dis_median"], CALIBRATION_BLOB_MEDIAN))
    if field["hot_px"] != CALIBRATION_FIELD_HOT:
        _andon("field hot_px is %r, not %d" % (
            field["hot_px"], CALIBRATION_FIELD_HOT))
    if field["hot_lcc"] != CALIBRATION_FIELD_LCC:
        _andon("field hot_lcc is %r, not %d" % (
            field["hot_lcc"], CALIBRATION_FIELD_LCC))
    if blob["hot_px"] != CALIBRATION_BLOB_HOT:
        _andon("blob hot_px is %r, not %d" % (
            blob["hot_px"], CALIBRATION_BLOB_HOT))
    if blob["hot_lcc"] != CALIBRATION_BLOB_LCC:
        _andon("blob hot_lcc is %r, not %d" % (
            blob["hot_lcc"], CALIBRATION_BLOB_LCC))
    # A region-derived threshold on the blob would report hot_px == 0
    # because every blob pixel equals the blob p90. The figure-derived
    # rule must keep them hot.
    if blob["hot_px"] == 0:
        _andon("blob hot_px is 0: threshold was derived from the region")
    return payload


def _selftest_andon_can_fail():
    src = np.zeros((32, 32), dtype=np.float64)
    try:
        S.crop_array(src, [0, 0, 40, 40], "big", "fixture")
    except S.Andon:
        pass
    else:
        _andon("oversized box did not fire")
    try:
        S.as_box([4, 4, 4, 8])
    except S.Andon:
        pass
    else:
        _andon("empty box did not fire")


def selftest(scratch=None):
    _selftest_andon_can_fail()
    if scratch is None:
        scratch = tempfile.mkdtemp(prefix="region_disagreement_")
    return _selftest_calibration(scratch)


def build_parser():
    p = argparse.ArgumentParser(
        description="Region plate-disagreement with a figure base rate.")
    p.add_argument("--tree", default=None,
                   help="E46-style tree containing s3_off/ and/or s3_on/")
    p.add_argument("--mode", default="s3_off",
                   help="s3_off (default, honest read), s3_on, or both")
    p.add_argument("--regions", default=None,
                   help="s3_sheet_regions.json schema")
    p.add_argument("--figure-only", action="store_true",
                   help="report the figure row with no region spec")
    p.add_argument("--views", default=None,
                   help="comma-separated view indices, e.g. 0,1,7")
    p.add_argument("--json-out", default=None,
                   help="write the payload as JSON")
    p.add_argument("--selftest", action="store_true",
                   help="run the constructed calibration and exit")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.selftest:
            payload = selftest()
            sys.stdout.write(
                "calibration field.median == %s  field.hot_lcc == %d  "
                "blob.median == %s\n"
                % (CALIBRATION_FIELD_MEDIAN, CALIBRATION_FIELD_LCC,
                   CALIBRATION_BLOB_MEDIAN))
            sys.stdout.write(format_table(payload))
            return 0
        if not args.tree:
            _andon("need --tree (or --selftest)")
        views = parse_views(args.views)
        payload = run(
            args.tree, args.mode, args.regions,
            views=views, figure_only=args.figure_only)
        sys.stdout.write(format_table(payload))
        if args.json_out:
            write_json(payload, args.json_out)
        return 0
    except Andon as e:
        sys.stderr.write(str(e) + "\n")
        return 2
    except S.Andon as e:
        sys.stderr.write(str(e) + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
