# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Thin glue: load an E45 AOV bundle, run s3_composite, write stills.

Not the estimator and not the compositor. Undo = delete --out.
If --aov is missing this REFUSES with exit 4 (the instrument working,
telling you not to proceed). It does not invent a layout.

Expected layout (emit_view_aovs.py):
  AOV/cams.json
  AOV/view_N/{twin.png, depth.npy, sil.npy, pos.npy, normal_world.npy,
              surfid.npy, weight_border.npy, reject.npy}
Optional --flow-dir/view_N/flow.npy, same convention as s3_composite.

  python tools/s3_run.py --aov DIR --out DIR [--flow-dir DIR]
         [--targets 0,1,2,3,4,5,6,7] [--alpha 6] [--primary-floor 0.05]
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

import s3_composite as S  # noqa: E402

TOOL_VERSION = "1.0.0"


class Andon(ValueError):
    pass


def _andon(msg):
    raise Andon("ANDON: " + msg)


def _load_png01(path):
    im = Image.open(path)
    arr = np.asarray(im, dtype=np.float64)
    if arr.ndim == 2:
        arr = np.stack([arr, arr, arr], axis=-1)
    return (arr[..., :3] / 255.0).astype(np.float32)


def load_bundle(aov_dir, flow_dir=None):
    """List of view dicts in the brief-#5 contract, plus cams."""
    cams_path = os.path.join(aov_dir, "cams.json")
    if not os.path.isfile(cams_path):
        _andon("no cams.json under %s" % aov_dir)
    with open(cams_path, encoding="utf-8") as f:
        cams = json.load(f)
    views = []
    names = sorted(k for k in cams if k.startswith("view_"))
    if not names:
        _andon("cams.json has no view_* keys")
    for name in names:
        d = os.path.join(aov_dir, name)
        need = ("twin.png", "depth.npy", "sil.npy", "pos.npy",
                "normal_world.npy", "surfid.npy", "weight_border.npy",
                "reject.npy")
        missing = [p for p in need if not os.path.isfile(os.path.join(d, p))]
        if missing:
            _andon("%s missing %s" % (name, missing))
        cam = cams[name]
        view = {
            "twin": _load_png01(os.path.join(d, "twin.png")),
            "depth": np.load(os.path.join(d, "depth.npy")),
            "sil": np.load(os.path.join(d, "sil.npy")).astype(bool),
            "pos": np.load(os.path.join(d, "pos.npy")),
            "normal_world": np.load(os.path.join(d, "normal_world.npy")),
            "surfid": np.load(os.path.join(d, "surfid.npy")).astype(np.int32),
            "weight_border": np.load(os.path.join(d, "weight_border.npy")),
            "reject": np.load(os.path.join(d, "reject.npy")).astype(bool),
            "cam": {
                "right": cam["right"],
                "up": cam["up"],
                "dtc": cam["dtc"],
                "bmid": cam["bmid"],
                "h_ext": cam["h_ext"],
                "v_ext": cam["v_ext"],
                "W": cam["W"],
                "H": cam["H"],
            },
        }
        if flow_dir is not None:
            fp = os.path.join(flow_dir, name, "flow.npy")
            if not os.path.isfile(fp):
                _andon("flow-dir %s has no %s/flow.npy" % (flow_dir, name))
            view["flow"] = np.load(fp)
        views.append(view)
    return views


def _save_rgb(path, arr):
    pix = np.clip(np.asarray(arr) * 255.0, 0, 255).astype(np.uint8)
    Image.fromarray(pix).save(path)


def _save_gray(path, arr, scale=None):
    a = np.asarray(arr, dtype=np.float64)
    if scale is None:
        m = float(np.max(a)) if np.max(a) > 0 else 1.0
        scale = m
    pix = np.clip(a / scale * 255.0, 0, 255).astype(np.uint8)
    Image.fromarray(pix).save(path)


def run(aov_dir, out_dir, flow_dir=None, targets=None,
        alpha=6.0, primary_floor=0.05, primary_mode="target"):
    views = load_bundle(aov_dir, flow_dir=flow_dir)
    if targets is None:
        targets = list(range(len(views)))
    os.makedirs(out_dir, exist_ok=True)
    manifest = {
        "tool": "s3_run.py",
        "tool_version": TOOL_VERSION,
        "aov": os.path.abspath(aov_dir),
        "flow_dir": None if flow_dir is None else os.path.abspath(flow_dir),
        "n_views": len(views),
        "targets": list(targets),
        "alpha": float(alpha),
        "primary_floor": float(primary_floor),
        "primary_mode": primary_mode,
        "results": {},
    }
    for t in targets:
        r = S.s3_composite(
            views, int(t), alpha=alpha, primary_floor=primary_floor,
            primary_mode=primary_mode)
        tag = "t%02d" % int(t)
        sub = os.path.join(out_dir, tag)
        os.makedirs(sub, exist_ok=True)
        _save_rgb(os.path.join(sub, "dependent.png"), r["dependent"])
        _save_rgb(os.path.join(sub, "independent.png"), r["independent"])
        _save_gray(os.path.join(sub, "disagreement.png"), r["disagreement"],
                   scale=1.0)
        _save_gray(os.path.join(sub, "coverage.png"), r["coverage"])
        _save_gray(os.path.join(sub, "fallback.png"), r["fallback"])
        np.save(os.path.join(sub, "owner.npy"), r["owner"])
        np.save(os.path.join(sub, "disagreement.npy"), r["disagreement"])
        manifest["results"][tag] = {
            "coverage_px": int(r["coverage"].sum()),
            "fallback_px": int(r["fallback"].sum()),
            "disagreement_mean": float(r["disagreement"][r["coverage"]].mean())
            if r["coverage"].any() else 0.0,
            "contrib": [float(x) for x in r["contrib"]],
        }
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    return manifest


def main(argv=None):
    p = argparse.ArgumentParser(description="Run s3_composite on an AOV bundle")
    p.add_argument("--aov", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--flow-dir", default=None)
    p.add_argument("--targets", default=None)
    p.add_argument("--alpha", type=float, default=6.0)
    p.add_argument("--primary-floor", type=float, default=0.05)
    p.add_argument("--primary-mode", default="target",
                   choices=("target", "facing"))
    args = p.parse_args(argv)
    if not os.path.isdir(args.aov):
        sys.stderr.write("ANDON: aov dir does not exist: %s\n" % args.aov)
        return 4
    targets = None
    if args.targets:
        targets = [int(x) for x in args.targets.split(",") if x.strip() != ""]
    try:
        man = run(args.aov, args.out, flow_dir=args.flow_dir, targets=targets,
                  alpha=args.alpha, primary_floor=args.primary_floor,
                  primary_mode=args.primary_mode)
    except (Andon, S.Andon) as e:
        sys.stderr.write(str(e) + "\n")
        return 2
    sys.stdout.write("s3_run wrote %d targets under %s\n"
                     % (len(man["targets"]), args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
