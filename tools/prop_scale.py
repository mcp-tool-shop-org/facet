"""Make a normalised reconstruction into a library prop at TRUE SIZE, and check one.

THE PROBLEM THIS EXISTS FOR, measured 2026-09-22 on four unrelated assets: every
reconstruction this route produces is normalised to **1.002 on its longest axis** - the
body, the A-pose body and both shields, to three decimals. So a prop mesh carries no true
scale at all. Loaded as-is a heater shield is 1.8 m tall, a door. The figure is correctly
sized only by coincidence, because a human is what the unit box happened to be fitted to.

The old compose script stood in for this with `HEIGHT_FRAC = 0.42` - a size chosen by eye,
per placement, with nothing recording what the object was supposed to BE. This replaces the
guess with a declaration: a prop's real size is a property of the prop, stated once, stored
in the file, and checked rather than trusted.

Scene unit system, stated once in canon/PROP-LIBRARY.md and repeated here because a tool
that silently assumes a scale is the thing being fixed: **1.0 unit = 1.8 m**.

  build:  python prop_scale.py --glb raw.glb --out props/shield.glb --name heater_shield
                               --real-mm 758 [--axis height] [--attach forearm_l]
  check:  python prop_scale.py --verify props/shield.glb
"""
import argparse
import json
import os
import sys

import numpy as np
import trimesh

METRES_PER_UNIT = 1.8
AXES = {"x": 0, "width": 0, "y": 1, "height": 1, "z": 2, "depth": 2}


def load(path):
    s = trimesh.load(path, process=False)
    return s.to_geometry() if hasattr(s, "to_geometry") else s


def sidecar_path(glb):
    return os.path.splitext(glb)[0] + ".prop.json"


def build(args):
    g = load(args.glb)
    size = g.bounds[1] - g.bounds[0]
    if args.axis == "longest":
        idx = int(np.argmax(size))
        axis_name = ["x", "y", "z"][idx]
    else:
        if args.axis not in AXES:
            raise SystemExit("ANDON: --axis must be longest/x/y/z/width/height/depth")
        idx = AXES[args.axis]
        axis_name = args.axis
    if size[idx] <= 0:
        raise SystemExit("ANDON: the chosen axis has zero extent; nothing to scale against")

    target = (args.real_mm / 1000.0) / METRES_PER_UNIT
    scale = target / size[idx]
    print("%s" % args.glb)
    print("  incoming size %s   (longest %.5f - a reconstruction normalises to ~1.002)"
          % (np.round(size, 5).tolist(), size.max()))
    print("  declared real %d mm on the %s axis -> %.5f units at %.1f m per unit"
          % (args.real_mm, axis_name, target, METRES_PER_UNIT))
    print("  scale factor  %.6f" % scale)

    g.apply_scale(scale)
    out_size = g.bounds[1] - g.bounds[0]
    # check the result rather than trusting the arithmetic - this is the leg that catches a
    # loader that re-normalises on export, which is exactly how the scale was lost upstream
    err = abs(out_size[idx] - target)
    if err > args.tol:
        raise SystemExit("ANDON: after scaling, the %s axis is %.6f but %.6f was declared "
                         "(error %.2e > --tol %.2e). The export path changed the size."
                         % (axis_name, out_size[idx], target, err, args.tol))

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "wb") as fh:
        fh.write(trimesh.exchange.gltf.export_glb(trimesh.Scene({args.name: g})))

    meta = {
        "prop": args.name,
        "source_glb": os.path.basename(args.glb),
        "real_mm": args.real_mm,
        "real_axis": axis_name,
        "metres_per_unit": METRES_PER_UNIT,
        "stored_longest_axis_units": float(out_size.max()),
        "stored_size_units": [float(v) for v in out_size],
        "stored_real_mm": [float(v * METRES_PER_UNIT * 1000.0) for v in out_size],
        "attach": args.attach,
        "face_normal_local": [float(v) for v in args.face_normal.split(",")] if args.face_normal else None,
        "grip_point_local": [float(v) for v in args.grip_point.split(",")] if args.grip_point else None,
    }
    with open(sidecar_path(args.out), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
    print("  stored size %s units = %s mm"
          % (np.round(out_size, 5).tolist(), np.round(meta["stored_real_mm"], 1).tolist()))
    print("WROTE %s  and  %s" % (args.out, sidecar_path(args.out)))
    if meta["grip_point_local"] is None:
        print("  NOTE: no --grip-point declared. Nothing gates a grip point, so a wrong one "
              "is invisible until a contact sheet shows it. Stated, not hidden.")


def verify(args):
    side = sidecar_path(args.verify)
    if not os.path.exists(side):
        raise SystemExit("ANDON: %s has no sidecar at %s - a prop without a declared size "
                         "is exactly the thing this contract forbids" % (args.verify, side))
    meta = json.load(open(side, encoding="utf-8"))
    g = load(args.verify)
    size = g.bounds[1] - g.bounds[0]
    idx = AXES[meta["real_axis"]] if meta["real_axis"] in AXES else int(np.argmax(size))
    target = (meta["real_mm"] / 1000.0) / meta.get("metres_per_unit", METRES_PER_UNIT)
    err = abs(size[idx] - target)
    print("%s" % args.verify)
    print("  declares %d mm on %s -> %.6f units; mesh measures %.6f (error %.2e)"
          % (meta["real_mm"], meta["real_axis"], target, size[idx], err))
    print("  full size %s units = %s mm"
          % (np.round(size, 5).tolist(),
             np.round(size * meta.get("metres_per_unit", METRES_PER_UNIT) * 1000.0, 1).tolist()))
    if abs(size.max() - 1.002) < 0.01:
        print("  ANDON: the longest axis is ~1.002 - this is an UNSCALED reconstruction "
              "wearing a prop's sidecar, not a prop")
        sys.exit(2)
    if err > args.tol:
        print("  ANDON: stored size does not match the declaration (error %.2e > %.2e)"
              % (err, args.tol))
        sys.exit(2)
    print("PROP OK: %s, %d mm, %s" % (meta["prop"], meta["real_mm"], meta.get("attach") or "no socket declared"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb", help="the normalised reconstruction to turn into a prop")
    ap.add_argument("--out", help="where the true-size prop GLB lands")
    ap.add_argument("--name", default="prop")
    ap.add_argument("--real-mm", type=float,
                    help="the prop's REAL size in millimetres along --axis. An authored "
                         "number: declare it, do not read it off a normalised mesh.")
    ap.add_argument("--axis", default="longest",
                    help="which axis --real-mm describes: longest (default), or "
                         "x/y/z/width/height/depth")
    ap.add_argument("--attach", default=None, help="socket name, e.g. hand_r, forearm_l")
    ap.add_argument("--grip-point", default=None, help="x,y,z in the prop's own local frame")
    ap.add_argument("--face-normal", default=None, help="x,y,z, which way the prop faces")
    ap.add_argument("--tol", type=float, default=1e-6,
                    help="how far the stored size may sit from the declaration, in units")
    ap.add_argument("--verify", help="check an existing prop GLB against its sidecar")
    args = ap.parse_args()

    if args.verify:
        return verify(args)
    if not (args.glb and args.out and args.real_mm):
        raise SystemExit("ANDON: build mode needs --glb, --out and --real-mm "
                         "(or use --verify)")
    return build(args)


if __name__ == "__main__":
    main()
