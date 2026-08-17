# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Diagnostic layer: classify, sheet, flats. Library plus thin verbs.

WHY THIS EXISTS. Consult #16 / build #16. Seven sheet builders, 33
throwaway scripts, three seats writing a surfid decode. The waste is
not a missing monolith. It is that the 4/5-class classifier and
s3_sheet's layout primitives were never the default import.

ARGUE-WITH-THE-BRIEF.

  1. One entry point that must know every subject class is how this
     ends up unusable for the galleon. Library plus thin verbs:
     classify / sheet / flats. Import the functions. The CLI is a
     dispatch, not a subject router.

  2. Layer vs arc. Layer if (a) two or more arcs wrote the same
     function, AND (b) a wrong implementation would silently change
     a recorded number, AND (c) it does not name a defect class.
     Arc if the detector is specified from a named defect, the
     script's only consumer is one report, or the question cannot
     be asked without this state's files. Olive stays in flat_trace.
     E51 deltaE tables stay in the arc.

  3. Brief 15's question is a TRACE, not a classification.
     tools/flat_trace.py already exists (t89). `evidence flats`
     imports it. This file does not rebuild the invertibility chip.

  4. Anchors re-derived 2026-08-17, before this file existed.
     E50 Gate A owner atlas 4-way over prep-valid:
       written 1985599 / filled 300187 / orphan_fill 5199 /
       no_view_visible 111825. sum == valid == 2402810,
       pairwise disjoint.
     E50 view 0 rendered 5-way (via unmapped_readout):
       fig 146356 / written 141526 / filled 3478 / orphan 40 /
       nvv 158 / unmapped 1154. exact magenta 304.
     The 5.4x (dilation 26.95% atlas vs 4.95% rendered) is the
     OLD texel_provenance classes. This layer names the space so
     that confusion cannot recur. It does not re-roll that census.

  5. Unnamed. The five classes are not the same object in both
     spaces. Atlas 4-way is exhaustive over valid. Unmapped lives
     outside valid (a surfid that lands off the mask). Treating
     ~valid as unmapped is the gutter, not the class E50 found.
     ANDON if asked for atlas-unmapped without a surfid.

CALIBRATION CLAIM (run --selftest; T90 pins the same numbers).
  Fixture 32x32. valid [8:24,8:24] = 256.
  written 128, filled 64, orphan 32, nvv 32.
  They are disjoint and sum to valid.
  A constructed overlap ANDON's.
  Rendered: one unmapped pixel, classified by unmapped_readout.
  Sheet: crop[0,0] == 200 via s3_sheet.crop_nn, not a new crop.

  python tools/evidence.py --selftest

YES/NO INTERVALS.

  atlas 4-way     owner>=0 / filled / orphan / nvv, each AND valid.
                  overlap or uncovered valid ANDON's.
  unmapped atlas  unique texels a surfid references that fail valid.
                  not ~valid. requires a surfid.
  rendered 5-way  unmapped_readout.classes_for_view. space is
                  "rendered figure pixels".
  every share     carries n, lcc, denominator, space.
  sheet columns   spec-driven roles, not hardcoded S3 five-panel.
                  crop / zoom / footer are s3_sheet's.
  flats           flat_trace.main. same-xy is not the source.

  python tools/evidence.py classify --atlas-dir D --mask M --out DIR
  python tools/evidence.py sheet --col role=path --regions J --out D
  python tools/evidence.py flats --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np
from PIL import Image

_TOOLS = os.path.dirname(os.path.abspath(__file__))
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import s3_sheet as SH  # noqa: E402
import unmapped_readout as U  # noqa: E402

TOOL_VERSION = "1.0.0"
ATLAS_SPACE = "atlas texels (prep-valid)"
RENDER_SPACE = "rendered figure pixels"
UNMAPPED_ATLAS_SPACE = "atlas texels (referenced, not prep-valid)"
FOUR = ("written", "filled", "orphan_fill", "no_view_visible")
FIVE = FOUR + ("unmapped",)

# E50 Gate A owner, facet_E49/atlas_owner_eroded + E06 C1 prep.
CALIBRATION_ATLAS_WRITTEN = 1985599
CALIBRATION_ATLAS_FILLED = 300187
CALIBRATION_ATLAS_ORPHAN = 5199
CALIBRATION_ATLAS_NVV = 111825
CALIBRATION_ATLAS_VALID = 2402810

# Constructed fixture (selftest / T90 hermetic).
FIX_WRITTEN = 128
FIX_FILLED = 64
FIX_ORPHAN = 32
FIX_NVV = 32
FIX_VALID = 256


class Andon(ValueError):
    pass


def _andon(msg):
    raise Andon("ANDON: " + msg)


def _as_bool(arr, name):
    a = np.asarray(arr)
    if a.ndim == 3:
        a = a[..., 0]
    if a.ndim != 2:
        _andon("%s must be (H,W) or (H,W,C), got %s" % (name, a.shape))
    if a.dtype == np.bool_ or a.dtype == bool:
        return a
    return a > 0.5


def _as_owner(arr):
    a = np.asarray(arr)
    if a.ndim != 2:
        _andon("owner must be (H,W), got %s" % (a.shape,))
    return a


def _same_hw(items):
    hw0 = None
    name0 = None
    for name, a in items:
        hw = a.shape[:2]
        if hw0 is None:
            hw0, name0 = hw, name
        elif hw != hw0:
            _andon(
                "mismatched atlas size: %s is %dx%d, %s is %dx%d"
                % (name0, hw0[1], hw0[0], name, hw[1], hw[0]))
    return hw0


def classify_atlas(owner, filled, orphan, nvv, valid):
    """Four-way over prep-valid. Disjoint and exhaustive, or ANDON.

    Does not emit unmapped. Unmapped is not ~valid.
    """
    own = _as_owner(owner)
    fil = _as_bool(filled, "filled")
    orp = _as_bool(orphan, "orphan_fill")
    nv = _as_bool(nvv, "no_view_visible")
    val = _as_bool(valid, "valid")
    _same_hw((
        ("owner", own), ("filled", fil), ("orphan_fill", orp),
        ("no_view_visible", nv), ("valid", val),
    ))
    masks = {
        "written": (own >= 0) & val,
        "filled": fil & val,
        "orphan_fill": orp & val,
        "no_view_visible": nv & val,
    }
    for a, b in (
        ("written", "filled"),
        ("written", "orphan_fill"),
        ("written", "no_view_visible"),
        ("filled", "orphan_fill"),
        ("filled", "no_view_visible"),
        ("orphan_fill", "no_view_visible"),
    ):
        n = int((masks[a] & masks[b]).sum())
        if n:
            _andon("atlas overlap %s & %s: %d texels" % (a, b, n))
    covered = (
        masks["written"] | masks["filled"]
        | masks["orphan_fill"] | masks["no_view_visible"])
    hole = int((val & ~covered).sum())
    if hole:
        _andon("atlas valid uncovered by 4-way: %d" % hole)
    extra = int((covered & ~val).sum())
    if extra:
        _andon("atlas 4-way outside valid: %d" % extra)
    return {
        "masks": masks,
        "valid": val,
        "space": ATLAS_SPACE,
    }


def atlas_unmapped_from_surfid(surfid, valid, atlas_res=None):
    """Unique texels a surfid references that fail valid.

    Not ~valid. The gutter is the rest of the atlas.
    """
    val = _as_bool(valid, "valid")
    H, W = val.shape[:2]
    res = int(atlas_res) if atlas_res is not None else int(H)
    row, col = U.decode_surfid(surfid, res)
    sil = np.asarray(surfid) != -1
    inb = sil & (row >= 0) & (row < H) & (col >= 0) & (col < W)
    atlas = np.zeros(val.shape, dtype=bool)
    if inb.any():
        rr = row[inb]
        cc = col[inb]
        atlas[rr, cc] = True
    um = atlas & ~val
    tot, big = U.lcc(um)
    return {
        "mask": um,
        "n": tot,
        "lcc": big,
        "space": UNMAPPED_ATLAS_SPACE,
        "referenced_valid": int((atlas & val).sum()),
        "referenced_total": int(atlas.sum()),
    }


def _one_number(mask, space, denom, denom_name):
    m = np.asarray(mask, dtype=bool)
    tot, big = U.lcc(m)
    n = int(tot)
    d = int(denom)
    return {
        "n": n,
        "lcc": big,
        "share": (float(n) / float(d)) if d else None,
        "denominator": d,
        "denominator_name": denom_name,
        "space": space,
    }


def numbers_atlas(cls):
    val_n = int(cls["valid"].sum())
    out = {
        "space": ATLAS_SPACE,
        "denominator": val_n,
        "denominator_name": "prep-valid texels",
        "classes": {},
    }
    for name in FOUR:
        out["classes"][name] = _one_number(
            cls["masks"][name], ATLAS_SPACE, val_n, "prep-valid texels")
    s = sum(out["classes"][k]["n"] for k in FOUR)
    if s != val_n:
        _andon("atlas class sum %d != valid %d" % (s, val_n))
    return out


def numbers_rendered(rec):
    """Wrap an unmapped_readout view record. Do not re-count."""
    fig = int(rec["n_fig_px"])
    space = rec.get("space", RENDER_SPACE)
    raw = {
        "written": rec["n_written"],
        "filled": rec["n_filled"],
        "orphan_fill": rec["n_orphan_fill"],
        "no_view_visible": rec["n_no_view_visible"],
        "unmapped": rec["n_unmapped"],
    }
    out = {
        "space": space,
        "denominator": fig,
        "denominator_name": "figure pixels (surfid != -1)",
        "classes": {},
        "unmapped_lcc": rec.get("unmapped_lcc"),
        "exact_magenta": rec.get("exact_magenta"),
        "exact_by_class": rec.get("exact_by_class"),
    }
    for name, n in raw.items():
        lcc = rec.get("unmapped_lcc") if name == "unmapped" else None
        out["classes"][name] = {
            "n": int(n),
            "lcc": lcc,
            "share": (float(n) / float(fig)) if fig else None,
            "denominator": fig,
            "denominator_name": "figure pixels (surfid != -1)",
            "space": space,
        }
    return out


def share_ratios(atlas_nums, rend_nums):
    """atlas share / rendered share. Names the 5.4x class of confusion."""
    out = {"note": "atlas_share / rendered_share; not a grade"}
    for name in FOUR:
        a = atlas_nums["classes"][name]["share"]
        r = rend_nums["classes"][name]["share"]
        if a is None or r is None or r == 0:
            out[name] = None
        else:
            out[name] = float(a) / float(r)
    return out


def consume(path):
    if path is None or not os.path.isfile(path):
        return {"path": path, "sha256": None}
    return {"path": os.path.abspath(path), "sha256": SH.sha256_file(path)}


def build_manifest(params, inputs, extra=None):
    man = {
        "tool": "evidence.py",
        "tool_version": TOOL_VERSION,
        "params": params,
        "inputs": list(inputs),
    }
    if extra:
        man.update(extra)
    return man


def write_json(path, payload):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, indent=1)
        f.write("\n")


def load_atlas_dir(atlas_dir, mask_path):
    if not os.path.isdir(atlas_dir):
        _andon("no atlas-dir %s" % atlas_dir)
    owner_p = os.path.join(atlas_dir, "owner.npy")
    fil_p = os.path.join(atlas_dir, "filled_mask.npy")
    orp_p = os.path.join(atlas_dir, "orphan_fill_mask.npy")
    nvv_p = os.path.join(atlas_dir, "no_view_visible_mask.npy")
    for p in (owner_p, fil_p, orp_p, nvv_p, mask_path):
        if not os.path.isfile(p):
            _andon("missing %s" % p)
    valid = U.load_valid(mask_path)
    owner = np.load(owner_p)
    filled = np.load(fil_p)
    orphan = np.load(orp_p)
    nvv = np.load(nvv_p)
    inputs = [consume(p) for p in (owner_p, fil_p, orp_p, nvv_p, mask_path)]
    return owner, filled, orphan, nvv, valid, inputs


def classify_paths(atlas_dir, mask_path, aov_path=None, render_path=None,
                   surfid_path=None):
    owner, filled, orphan, nvv, valid, inputs = load_atlas_dir(
        atlas_dir, mask_path)
    cls = classify_atlas(owner, filled, orphan, nvv, valid)
    atlas_nums = numbers_atlas(cls)
    payload = {
        "tool": "evidence.py",
        "tool_version": TOOL_VERSION,
        "atlas": atlas_nums,
    }
    if surfid_path:
        if not os.path.isfile(surfid_path):
            _andon("no surfid %s" % surfid_path)
        surfid = np.load(surfid_path)
        um = atlas_unmapped_from_surfid(surfid, valid)
        payload["atlas_unmapped"] = {
            "n": um["n"],
            "lcc": um["lcc"],
            "share_of_referenced": (
                float(um["n"]) / float(um["referenced_total"])
                if um["referenced_total"] else None),
            "denominator": um["referenced_total"],
            "denominator_name": "unique texels referenced by this surfid",
            "space": um["space"],
            "referenced_valid": um["referenced_valid"],
        }
        inputs.append(consume(surfid_path))
    if aov_path or render_path:
        if not aov_path or not render_path:
            _andon("rendered classify needs both --aov and --render")
        if not os.path.isfile(aov_path):
            _andon("no surfid %s" % aov_path)
        if not os.path.isfile(render_path):
            _andon("no render %s" % render_path)
        surfid = np.load(aov_path)
        im = np.asarray(Image.open(render_path).convert("RGB"))
        rec, _masks = U.readout_view(
            surfid, valid, im, owner, filled, orphan, nvv)
        payload["rendered"] = numbers_rendered(rec)
        payload["share_ratio_atlas_over_rendered"] = share_ratios(
            atlas_nums, payload["rendered"])
        inputs.append(consume(aov_path))
        inputs.append(consume(render_path))
    payload["manifest"] = build_manifest(
        {
            "atlas_dir": os.path.abspath(atlas_dir),
            "mask": os.path.abspath(mask_path),
            "aov": os.path.abspath(aov_path) if aov_path else None,
            "render": os.path.abspath(render_path) if render_path else None,
            "surfid": os.path.abspath(surfid_path) if surfid_path else None,
        },
        inputs,
    )
    return payload


def format_classify(payload):
    lines = [
        "evidence %s  classify  (not a grade)" % TOOL_VERSION,
        "atlas space: %s  denom=%d %s" % (
            payload["atlas"]["space"],
            payload["atlas"]["denominator"],
            payload["atlas"]["denominator_name"]),
        "%-16s %10s %8s %s" % ("class", "n", "lcc", "share"),
    ]
    for name in FOUR:
        c = payload["atlas"]["classes"][name]
        lines.append(
            "%-16s %10d %8d %s"
            % (name, c["n"], c["lcc"],
               "-" if c["share"] is None else "%.6f" % c["share"]))
    if "atlas_unmapped" in payload:
        u = payload["atlas_unmapped"]
        lines.append(
            "atlas unmapped (referenced-not-valid): n=%d lcc=%d space=%s"
            % (u["n"], u["lcc"], u["space"]))
    if "rendered" in payload:
        r = payload["rendered"]
        lines.append(
            "rendered space: %s  denom=%d %s" % (
                r["space"], r["denominator"], r["denominator_name"]))
        for name in FIVE:
            c = r["classes"][name]
            lcc = "-" if c["lcc"] is None else str(c["lcc"])
            lines.append(
                "%-16s %10d %8s %s"
                % (name, c["n"], lcc,
                   "-" if c["share"] is None else "%.6f" % c["share"]))
        rat = payload.get("share_ratio_atlas_over_rendered") or {}
        bits = []
        for name in FOUR:
            v = rat.get(name)
            bits.append(
                "%s=%s" % (name, "-" if v is None else "%.2fx" % v))
        lines.append("atlas/rendered share  " + " ".join(bits))
    return "\n".join(lines) + "\n"


def parse_col(text):
    if "=" not in str(text):
        _andon("--col must be role=path, got %r" % (text,))
    role, path = str(text).split("=", 1)
    role = role.strip()
    path = path.strip()
    if not role or not path:
        _andon("empty --col role or path: %r" % (text,))
    return role, path


def resolve_col(path_tmpl, view_i):
    return path_tmpl.replace("{v}", str(int(view_i)))


def build_column_sheet(columns, regions, view_i, zoom=1):
    """columns: list of {role, rgb_or_None, path}. regions from s3_sheet."""
    if not columns:
        _andon("sheet needs at least one --col")
    still_items = [
        (None if c["rgb"] is None else c["rgb"].shape[:2], c["path"])
        for c in columns
    ]
    full_hw = SH.agreed_hw(still_items)
    if full_hw is None:
        _andon("view %d: no source gives a panel size" % int(view_i))

    def one_row(box, title, stats_line=None):
        hw = full_hw if box is None else SH.box_hw(box)
        panels = []
        caps = []
        for c in columns:
            src = c["rgb"]
            cropped = None
            if src is not None:
                cropped = src if box is None else SH.crop_array(
                    src, box, title, c["path"])
            pan, ok = SH.panel_for(cropped, hw, c["path"], zoom)
            panels.append(pan)
            caps.append({
                "role": c["role"],
                "path": SH._short_path(c["path"]) if ok else "MISSING",
            })
        return SH.compose_row(panels, caps, title, stats_line=stats_line)

    rows = []
    title = "view %d  FULL  zoom=%d" % (int(view_i), int(zoom))
    rows.append(one_row(None, title))
    for reg in regions or []:
        box = reg["box"]
        name = reg["name"]
        rtitle = "view %d  %s  box=%s" % (int(view_i), name, box)
        rows.append(one_row(box, rtitle))
    consumed = [consume(c["path"]) for c in columns]
    rgb = SH.render_sheet({"rows": rows}, consumed)
    return rgb, consumed, full_hw


def run_sheet(col_specs, regions_path, out_dir, views, zoom=1):
    spec = SH.load_regions(regions_path)
    parsed = spec["_parsed"]
    if views is None:
        views = sorted(parsed)
    os.makedirs(out_dir, exist_ok=True)
    results = []
    for vi in views:
        columns = []
        for role, tmpl in col_specs:
            path = resolve_col(tmpl, vi)
            rgb = SH.load_rgb(path)
            columns.append({"role": role, "rgb": rgb, "path": path})
        regs = parsed.get(int(vi), [])
        rgb, consumed, full_hw = build_column_sheet(
            columns, regs, vi, zoom=zoom)
        tag = "v%02d" % int(vi)
        png = os.path.join(out_dir, "sheet_%s.png" % tag)
        SH.write_png(png, rgb)
        rec = {
            "view": int(vi),
            "sheet": os.path.abspath(png),
            "width": int(rgb.shape[1]),
            "height": int(rgb.shape[0]),
            "zoom": int(zoom),
            "full_hw": [int(full_hw[0]), int(full_hw[1])],
            "regions_path": os.path.abspath(regions_path),
            "roles": [c["role"] for c in columns],
            "consumed": consumed,
        }
        results.append(rec)
    man = build_manifest(
        {
            "columns": [{"role": r, "path": p} for r, p in col_specs],
            "regions": os.path.abspath(regions_path),
            "views": [int(v) for v in views],
            "zoom": int(zoom),
        },
        [consume(regions_path)],
        extra={"sheets": results},
    )
    write_json(os.path.join(out_dir, "sheet_manifest.json"), man)
    return man


def cmd_flats(argv):
    try:
        import flat_trace as F
    except ImportError:
        _andon("flat_trace.py is not importable; t89 is the instrument")
    return F.main(list(argv) if argv is not None else None)


def fixture_atlas():
    n = 32
    valid = np.zeros((n, n), dtype=bool)
    valid[8:24, 8:24] = True
    owner = np.full((n, n), -1, dtype=np.int16)
    filled = np.zeros((n, n), dtype=bool)
    orphan = np.zeros((n, n), dtype=bool)
    nvv = np.zeros((n, n), dtype=bool)
    owner[8:16, 8:24] = 0
    filled[16:20, 8:24] = True
    orphan[20:22, 8:24] = True
    nvv[22:24, 8:24] = True
    return owner, filled, orphan, nvv, valid


def fixture_overlap():
    owner, filled, orphan, nvv, valid = fixture_atlas()
    filled[10, 10] = True
    return owner, filled, orphan, nvv, valid


def selftest():
    owner, filled, orphan, nvv, valid = fixture_atlas()
    cls = classify_atlas(owner, filled, orphan, nvv, valid)
    nums = numbers_atlas(cls)
    got = {k: nums["classes"][k]["n"] for k in FOUR}
    expect = {
        "written": FIX_WRITTEN,
        "filled": FIX_FILLED,
        "orphan_fill": FIX_ORPHAN,
        "no_view_visible": FIX_NVV,
    }
    if got != expect:
        _andon("fixture 4-way %s != %s" % (got, expect))
    if nums["denominator"] != FIX_VALID:
        _andon("fixture valid is %d, not %d" % (
            nums["denominator"], FIX_VALID))
    for k in FOUR:
        if nums["classes"][k]["space"] != ATLAS_SPACE:
            _andon("atlas class %s missing space" % k)

    try:
        classify_atlas(*fixture_overlap())
        _andon("overlap did not fire")
    except Andon as e:
        if "overlap" not in str(e):
            raise

    # ~valid is the gutter, not unmapped
    gutter = int((~valid).sum())
    um = atlas_unmapped_from_surfid(
        np.full((32, 32), -1, dtype=np.int64), valid)
    if um["n"] != 0:
        _andon("empty surfid produced atlas unmapped %d" % um["n"])
    if gutter == 0:
        _andon("fixture gutter is empty")

    surfid, u_valid, im, u_owner, u_filled, u_orphan, u_nvv = (
        U.fixture_calibration())
    rec, _c = U.readout_view(
        surfid, u_valid, im, u_owner, u_filled, u_orphan, u_nvv)
    rend = numbers_rendered(rec)
    if rend["classes"]["unmapped"]["n"] != 1:
        _andon("rendered unmapped is %d, not 1" % (
            rend["classes"]["unmapped"]["n"],))
    if rend["space"] != RENDER_SPACE:
        _andon("rendered space is %r" % rend["space"])

    src = SH.fixture_calibration_canvas(32)
    columns = [{
        "role": "reference",
        "rgb": src,
        "path": "fixture.png",
    }]
    rgb, _cons, _hw = build_column_sheet(
        columns,
        [{"name": "pin", "box": list(SH.CALIBRATION_BOX)}],
        0, zoom=SH.CALIBRATION_ZOOM)
    # The FULL row is first; the pin crop is the second compose_row.
    # Verify through s3_sheet's crop, which is what build_column_sheet calls.
    crop = SH.crop_nn(
        src, SH.CALIBRATION_BOX, SH.CALIBRATION_ZOOM,
        name="pin", source="fixture")
    if int(crop[0, 0, 0]) != SH.CALIBRATION_VALUE:
        _andon(
            "sheet crop[0,0] is %r, not %d"
            % (int(crop[0, 0, 0]), SH.CALIBRATION_VALUE))
    if rgb.shape[0] < 16 or rgb.shape[1] < 16:
        _andon("sheet too small: %s" % (rgb.shape,))
    return nums, rend


def build_parser():
    p = argparse.ArgumentParser(
        description="Diagnostic layer: classify, sheet, flats.")
    p.add_argument("--selftest", action="store_true")
    sub = p.add_subparsers(dest="cmd")

    c = sub.add_parser("classify", help="5-class readout, space named")
    c.add_argument("--atlas-dir", required=True)
    c.add_argument("--mask", required=True, help="prep mask.npy")
    c.add_argument("--aov", default=None, help="one view's surfid.npy")
    c.add_argument("--render", default=None, help="one view's RGB render")
    c.add_argument("--surfid", default=None,
                   help="optional surfid for atlas-unmapped (referenced-not-valid)")
    c.add_argument("--out", required=True)

    s = sub.add_parser("sheet", help="reference | shipped | candidate(s)")
    s.add_argument("--col", action="append", default=[],
                   help="repeatable role=path; path may contain {v}")
    s.add_argument("--regions", default=SH.DEFAULT_REGIONS)
    s.add_argument("--out", required=True)
    s.add_argument("--views", default=None)
    s.add_argument("--zoom", type=int, default=1)

    sub.add_parser("flats", help="delegate to flat_trace (brief 15)")
    return p


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        if argv and argv[0] == "flats":
            return cmd_flats(argv[1:])
        args, _rest = build_parser().parse_known_args(argv)
        if args.selftest and args.cmd is None:
            selftest()
            sys.stdout.write(
                "calibration atlas 4-way %d/%d/%d/%d  "
                "overlap ANDON  rendered unmapped == 1  "
                "sheet crop[0,0] == %d  "
                "(E50 Gate A pin is %d/%d/%d/%d of %d)\n"
                % (FIX_WRITTEN, FIX_FILLED, FIX_ORPHAN, FIX_NVV,
                   SH.CALIBRATION_VALUE,
                   CALIBRATION_ATLAS_WRITTEN, CALIBRATION_ATLAS_FILLED,
                   CALIBRATION_ATLAS_ORPHAN, CALIBRATION_ATLAS_NVV,
                   CALIBRATION_ATLAS_VALID))
            return 0
        if args.cmd is None:
            _andon("need classify|sheet|flats or --selftest")
        if args.cmd == "classify":
            payload = classify_paths(
                args.atlas_dir, args.mask,
                aov_path=args.aov, render_path=args.render,
                surfid_path=args.surfid)
            os.makedirs(args.out, exist_ok=True)
            write_json(os.path.join(args.out, "classify.json"), payload)
            sys.stdout.write(format_classify(payload))
            return 0
        if args.cmd == "sheet":
            if not args.col:
                _andon("sheet needs at least one --col role=path")
            cols = [parse_col(x) for x in args.col]
            views = U.parse_views(args.views) if args.views else None
            man = run_sheet(
                cols, args.regions, args.out, views, zoom=int(args.zoom))
            sys.stdout.write(
                "evidence %s  sheet  views=%s  roles=%s  out=%s\n"
                % (TOOL_VERSION,
                   ",".join(str(s["view"]) for s in man["sheets"]),
                   ",".join(r for r, _p in cols),
                   os.path.abspath(args.out)))
            return 0
        _andon("unknown cmd %r" % args.cmd)
    except Andon as e:
        sys.stderr.write(str(e) + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
