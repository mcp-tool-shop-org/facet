"""E12 Gate 0 — head-region evidence on a raw reconstruction. NO VERDICT.

WHY THIS EXISTS AND WHY IT IS NOT `mesh_stats`' FACE RECT. `mesh_stats` finds "the head" by
projecting a fixed front-view rectangle authored against one standing humanoid at the
character line's framing. A dragon has a face and that rect has not found it, so this
experiment quotes none of `mesh_stats`' rect columns and derives the region here instead —
per subject, from what the geometry is, with the derivation recorded.

HOW THE REGION IS FOUND, and the rule it obeys. **Never by height.** Horns, raised wingtips
and tail spines all rise above the crown; a height band on this subject measures a horn,
which is the raised-weapon rule wearing wings. The head is located BY EYE on two orthogonal
`--clay` renders of the mesh itself, as two pixel rectangles, and those are converted to one
axis-aligned world box by the exact inverse of `turn_render.py`'s camera.

THE CAMERA CONVENTION IS TAKEN FROM AN EXISTING TOOL, NOT RE-DERIVED HERE. It is
`silhouette_masks.py`'s, whose header states it and whose `--anchor` flag proved it
byte-identical against masks on disk:

    direction to camera  dtc = ( sin th, -cos th, 0)
    camera right         rgt = ( cos th,  sin th, 0)
    camera up            up  = cross(rgt, -dtc) = (0, 0, 1)

with `turn_render`'s height-fit framing, `ortho_scale = size.z * margin`, mapped by Blender
to the render's VERTICAL axis because `sensor_fit` is VERTICAL under `--fit-axis height`.
So world-units-per-pixel is `ortho_scale / H` on both screen axes.

WHAT THE BOX IS, STATED PLAINLY SO THE NUMBER IS NOT OVER-READ. Two silhouette rectangles
90 degrees apart bound a REGION OF SPACE, not a semantic head. Anything else occupying that
box — a neck, a wing passing behind the skull, a horn sweeping back into it — is inside the
count. This tool reports what is in the box; it does not claim the box contains only a head,
and the report says which structures the eye sees inside it.

WHAT IT MEASURES. Faces whose centroid is inside the box, as a share of total; and the
MEDIAN face area inside against outside, which is the density contrast. Median rather than
mean: a reconstruction's face-area distribution has a long tail and a mean would track it.

WHAT IT DOES NOT DO. It does not decide whether the share is high or low, does not compare
candidates, and does not recommend a polygon allocation. Whether the beast gets E01's
bust-crop lever is a `profiles/beast.json` decision that does not exist yet and is made
after designation, from these numbers.

Standards compliance:
  PIN_PER_STEP — every input (frame, margin, step, both pixel boxes) is an explicit flag and
    is echoed into the JSON, so the derivation replays from the record alone.
  ANDON_AUTHORITY — raises if a named view's `right` vector is not a world axis (the box
    could not be axis-aligned), if the two views' Z ranges disagree beyond --z-tol, or if
    the box lies outside the mesh bbox. It halts rather than returning a number.
  NAMED_COMPENSATORS — reads a GLB, writes one JSON. Undo = delete the JSON. Owner: the
    session running it. Nothing irreversible.
  DECOMPOSE_BY_SECRETS — no subject constant is inherited: the frame comes from the caller,
    the region from the caller's eye on this mesh's own renders.
  EXTERNAL_VERIFIER — grades nothing; it reports numbers a human rules on. The welding and
    the Blender-convention rotation are `mesh_stats`' own code path, so the face totals here
    are comparable with the stats table rather than a second opinion about the same mesh.

  e12_head_evidence.py --glb m.glb --w 1600 --h 1024
                       --view-a 0 --box-a x0,y0,x1,y1
                       --view-b 2 --box-b x0,y0,x1,y1
                       [--margin 1.204] [--step 45] [--z-tol 0.05] [--out head.json]
"""
import argparse
import json
import os

import numpy as np
import trimesh

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--label", default=None)
ap.add_argument("--w", type=int, required=True, help="render width the pixel boxes were read on")
ap.add_argument("--h", type=int, required=True, help="render height ditto")
ap.add_argument("--margin", type=float, default=1.204, help="turn_render's --margin")
ap.add_argument("--step", type=float, default=45.0, help="turn_render's --step")
ap.add_argument("--view-a", type=int, required=True)
ap.add_argument("--box-a", required=True, help="x0,y0,x1,y1 in view-a pixels, y from TOP")
ap.add_argument("--view-b", type=int, required=True)
ap.add_argument("--box-b", required=True, help="x0,y0,x1,y1 in view-b pixels, y from TOP")
ap.add_argument("--z-tol", type=float, default=0.05,
                help="allowed disagreement between the two views' Z ranges, as a fraction "
                     "of the mesh's Z extent, before this raises")
ap.add_argument("--overlay", default=None,
                help="dir of <tag>_N.png turnaround renders; draws the DERIVED world box "
                     "back onto every one of them so the region measured can be checked by "
                     "eye instead of trusted. An axis-aligned world box under a yawed "
                     "orthographic camera with up=+Z projects to a rectangle exactly.")
ap.add_argument("--overlay-tag", default="clay")
ap.add_argument("--overlay-out", default=None)
ap.add_argument("--out", default=None)
args = ap.parse_args()

# glTF Y-up -> Blender Z-up: the convention mesh_stats reports extents in, silhouette_masks
# raycasts in, and turn_render renders in. One frame for all of them.
GLTF_TO_BLENDER = np.array([[1.0, 0.0, 0.0],
                            [0.0, 0.0, -1.0],
                            [0.0, 1.0, 0.0]])

m = trimesh.load(args.glb, force="mesh", process=False)
# weld exactly as mesh_stats does, so `faces` here IS the faces column of the stats table
m.merge_vertices(merge_tex=True, merge_norm=True)
faces = np.asarray(m.faces)
co = np.asarray(m.vertices, dtype=np.float64) @ GLTF_TO_BLENDER.T
lo, hi = co.min(axis=0), co.max(axis=0)
mid = (lo + hi) / 2.0
size = hi - lo

# turn_render, --fit-axis height (the default): ortho_scale = size.z * margin, and
# sensor_fit = VERTICAL puts that span on the render's H axis. Square pixels.
ortho = float(size[2] * args.margin)
s = ortho / args.h
print("[head] %s: %d faces | extent (Blender xyz) %s | ortho_scale %.6f | %.8f world/px"
      % (args.label or os.path.basename(args.glb), len(faces),
         [round(float(v), 4) for v in size], ortho, s), flush=True)


def axis_of(view):
    """The world axis the render's +X maps to for this view, as (index, sign)."""
    th = np.radians(view * args.step)
    rgt = np.array([np.cos(th), np.sin(th), 0.0])
    for i in (0, 1):
        for sgn in (1.0, -1.0):
            e = np.zeros(3)
            e[i] = sgn
            if np.allclose(rgt, e, atol=1e-9):
                return i, sgn, rgt
    raise SystemExit(
        "ANDON: view %d has camera right %s, which is not a world axis. An axis-aligned "
        "box cannot be read off it; pick views that are multiples of 90 degrees of yaw."
        % (view, np.round(rgt, 6).tolist()))


def unproject(view, box):
    """Pixel rect -> (world range along the view's right axis, world Z range)."""
    x0, y0, x1, y1 = [float(v) for v in box.split(",")]
    ax, sgn, rgt = axis_of(view)
    # world = mid + rgt * ((px + 0.5 - W/2) * s) + up * ((H/2 - py - 0.5) * s), up = +Z
    hx0 = mid[ax] + sgn * ((min(x0, x1) + 0.5 - args.w / 2.0) * s)
    hx1 = mid[ax] + sgn * ((max(x0, x1) + 0.5 - args.w / 2.0) * s)
    zt = mid[2] + (args.h / 2.0 - min(y0, y1) - 0.5) * s
    zb = mid[2] + (args.h / 2.0 - max(y0, y1) - 0.5) * s
    return ax, (min(hx0, hx1), max(hx0, hx1)), (min(zb, zt), max(zb, zt))


ax_a, rng_a, z_a = unproject(args.view_a, args.box_a)
ax_b, rng_b, z_b = unproject(args.view_b, args.box_b)
if ax_a == ax_b:
    raise SystemExit("ANDON: views %d and %d both read the same world axis (%s). Two "
                     "orthogonal views are needed to bound a box."
                     % (args.view_a, args.view_b, "xyz"[ax_a]))

zdis = max(abs(z_a[0] - z_b[0]), abs(z_a[1] - z_b[1])) / float(size[2])
if zdis > args.z_tol:
    raise SystemExit(
        "ANDON: the two views disagree about the head's Z range by %.4f of the mesh's "
        "height (tolerance %.4f). view %d says %s, view %d says %s. Either a box was read "
        "on the wrong structure or the frames differ; halting rather than averaging them."
        % (zdis, args.z_tol, args.view_a, [round(v, 4) for v in z_a],
           args.view_b, [round(v, 4) for v in z_b]))

box = np.zeros((2, 3))
box[:, ax_a] = rng_a
box[:, ax_b] = rng_b
box[:, 2] = (min(z_a[0], z_b[0]), max(z_a[1], z_b[1]))   # union, stated
if np.any(box[1] < lo) or np.any(box[0] > hi):
    raise SystemExit("ANDON: derived box %s lies outside the mesh bbox %s"
                     % (box.tolist(), [lo.tolist(), hi.tolist()]))

cen = co[faces].mean(axis=1)
inside = np.all((cen >= box[0]) & (cen <= box[1]), axis=1)
n_in = int(inside.sum())
area = np.asarray(m.area_faces, dtype=np.float64)
med_in = float(np.median(area[inside])) if n_in else float("nan")
med_out = float(np.median(area[~inside])) if n_in < len(faces) else float("nan")
ratio = med_out / med_in if med_in else float("nan")

rec = {
    "label": args.label or os.path.splitext(os.path.basename(args.glb))[0],
    "glb": os.path.abspath(args.glb),
    "frame": {"w": args.w, "h": args.h, "margin": args.margin, "step": args.step,
              "fit_axis": "height", "ortho_scale": round(ortho, 6),
              "world_per_px": s},
    "pixel_boxes": {str(args.view_a): args.box_a, str(args.view_b): args.box_b},
    "axes_read": {str(args.view_a): "xyz"[ax_a], str(args.view_b): "xyz"[ax_b]},
    "z_ranges": {str(args.view_a): [round(v, 5) for v in z_a],
                 str(args.view_b): [round(v, 5) for v in z_b],
                 "disagreement_frac_of_height": round(float(zdis), 5)},
    "head_box_blender": [[round(float(v), 5) for v in box[0]],
                         [round(float(v), 5) for v in box[1]]],
    "head_box_extent": [round(float(v), 5) for v in (box[1] - box[0])],
    "mesh_bbox_blender": [[round(float(v), 5) for v in lo], [round(float(v), 5) for v in hi]],
    "mesh_extent_blender": [round(float(v), 5) for v in size],
    "faces_total": int(len(faces)),
    "faces_in_box": n_in,
    "faces_in_box_frac": round(n_in / len(faces), 6),
    "median_face_area_in": med_in,
    "median_face_area_out": med_out,
    "density_contrast_out_over_in": round(float(ratio), 4),
    "mean_face_area_in": float(area[inside].mean()) if n_in else float("nan"),
    "mean_face_area_out": float(area[~inside].mean()) if n_in < len(faces) else float("nan"),
    "box_volume_frac_of_bbox": round(float(np.prod(box[1] - box[0]) / np.prod(size)), 6),
    "caveat": "The box is a two-silhouette visual-hull box: a region of space, not a "
              "segmentation. Anything else occupying it is counted.",
}
print("[head] box (Blender xyz) %s -> %s" % (rec["head_box_blender"][0],
                                             rec["head_box_blender"][1]), flush=True)
print("[head] faces in box %s / %s = %.3f%% | median face area in %.4g vs out %.4g "
      "(out/in %.3f)" % (f"{n_in:,}", f"{len(faces):,}", 100 * n_in / len(faces),
                         med_in, med_out, ratio), flush=True)
print("[head] box is %.3f%% of the bbox volume; Z ranges disagree by %.4f of height"
      % (100 * rec["box_volume_frac_of_bbox"], zdis), flush=True)
if args.overlay:
    import glob
    from PIL import Image, ImageDraw

    Image.MAX_IMAGE_PIXELS = None
    odir = args.overlay_out or os.path.join(args.overlay, "boxed")
    os.makedirs(odir, exist_ok=True)
    corners = np.array([[box[i, 0], box[j, 1], box[k, 2]]
                        for i in (0, 1) for j in (0, 1) for k in (0, 1)])
    for p in sorted(glob.glob(os.path.join(args.overlay, "%s_*.png" % args.overlay_tag)),
                    key=lambda q: int(os.path.splitext(q)[0].rsplit("_", 1)[1])):
        idx = int(os.path.splitext(p)[0].rsplit("_", 1)[1])
        th = np.radians(idx * args.step)
        rgt = np.array([np.cos(th), np.sin(th), 0.0])
        u = (corners - mid) @ rgt
        px0 = args.w / 2.0 + u.min() / s - 0.5
        px1 = args.w / 2.0 + u.max() / s - 0.5
        py0 = args.h / 2.0 - (corners[:, 2].max() - mid[2]) / s - 0.5
        py1 = args.h / 2.0 - (corners[:, 2].min() - mid[2]) / s - 0.5
        im = Image.open(p).convert("RGB")
        if not (im.size == (args.w, args.h)):
            raise AssertionError(
                "ANDON: %s is %s but the box was read on a %dx%d frame"
                % (os.path.basename(p), im.size, args.w, args.h))
        d = ImageDraw.Draw(im)
        d.rectangle([px0, py0, px1, py1], outline=(255, 90, 60), width=3)
        d.text((px0 + 6, py0 + 6), "head box, view %d" % idx, fill=(255, 200, 60))
        q = os.path.join(odir, "boxed_%d.png" % idx)
        im.save(q)
        print("[head] overlay view %d -> %s  rect (%.0f,%.0f)-(%.0f,%.0f)"
              % (idx, q, px0, py0, px1, py1), flush=True)

if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(rec, open(args.out, "w"), indent=1)
    print("[head] wrote %s" % os.path.abspath(args.out), flush=True)
