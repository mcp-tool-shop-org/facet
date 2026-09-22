"""What came back from an auto-rig: is it OUR mesh, and what skeleton is on it?

An auto-rig service is a black box that returns a GLB. Two different things can arrive in
that file and they look identical in a viewer:

  (a) our mesh, skinned to a new skeleton   <- the whole point
  (b) a NEW mesh the service retopologised, skinned to a new skeleton

(b) loses the accepted asset and puts the route back where it started by another road, so
it is checked BEFORE anything downstream is believed. The check is cheap and exact: a
glTF POSITION accessor carries its own count and its own min/max, so mesh identity is
readable from the JSON chunk without decoding a single vertex.

Reads the GLB container directly - json + struct, no glTF library - because the question is
about the file's structure (skins, joints, JOINTS_0/WEIGHTS_0) and mesh loaders discard
exactly that. trimesh's scene, for instance, applies node transforms and drops the skin.

Reports:
  * mesh identity against --against: vertex count, bbox, and whether they match
  * the skeleton: joint count, the root, hand/finger joints by name, full hierarchy depth
  * skinning: whether primitives carry JOINTS_0 and WEIGHTS_0 at all

ANDON on --require-same-mesh when the vertex count or the bbox moved, and on
--require-skin when nothing in the file is skinned. Both are stated on the command line.

  python rig_report.py --glb rigged.glb [--against original.glb]
                       [--require-same-mesh] [--require-skin] [--json-out ...]
"""
import argparse
import json
import struct
import sys

# Joint-name fragments that indicate a hand and fingers. Lowercased substring match, which
# is how both conventions this route can receive spell them: Tripo native and Mixamo
# (mixamorig:LeftHandIndex1). A name-based test is honest about what it is - it reports what
# the skeleton CALLS things, and a rig with unnamed joints reports zero rather than lying.
HAND_HINTS = ("hand", "wrist", "palm")
FINGER_HINTS = ("thumb", "index", "middle", "ring", "pinky", "little", "finger")


def read_gltf_json(path):
    with open(path, "rb") as fh:
        magic, version, _length = struct.unpack("<III", fh.read(12))
        if magic != 0x46546C67:
            raise SystemExit("ANDON: %s is not a GLB (magic %#x)" % (path, magic))
        if version != 2:
            raise SystemExit("ANDON: %s is glTF version %d, expected 2" % (path, version))
        while True:
            head = fh.read(8)
            if len(head) < 8:
                raise SystemExit("ANDON: %s has no JSON chunk" % path)
            clen, ctype = struct.unpack("<II", head)
            data = fh.read(clen)
            if ctype == 0x4E4F534A:
                return json.loads(data.decode("utf-8"))
            # 0x004E4942 is BIN; skip it, the question is structural


def mesh_summary(g):
    """Vertex count and bbox from the POSITION accessors, per primitive."""
    prims = []
    for mi, mesh in enumerate(g.get("meshes", [])):
        for pi, prim in enumerate(mesh.get("primitives", [])):
            attrs = prim.get("attributes", {})
            acc_i = attrs.get("POSITION")
            if acc_i is None:
                continue
            acc = g["accessors"][acc_i]
            prims.append({
                "mesh": mi, "mesh_name": mesh.get("name"), "primitive": pi,
                "vertices": acc.get("count"),
                "min": acc.get("min"), "max": acc.get("max"),
                "has_joints": "JOINTS_0" in attrs,
                "has_weights": "WEIGHTS_0" in attrs,
            })
    return prims


def skeleton_summary(g):
    nodes = g.get("nodes", [])
    skins = g.get("skins", [])
    joints = []
    for s in skins:
        joints.extend(s.get("joints", []))
    joints = sorted(set(joints))
    names = [nodes[j].get("name") or "" for j in joints if j < len(nodes)]
    low = [n.lower() for n in names]
    child_of = {}
    for i, n in enumerate(nodes):
        for c in n.get("children", []):
            child_of[c] = i

    def depth(i, seen=None):
        seen = seen or set()
        d = 0
        while i in child_of and i not in seen:
            seen.add(i)
            i = child_of[i]
            d += 1
        return d

    roots = [j for j in joints if child_of.get(j) not in joints]
    return {
        "skins": len(skins),
        "joint_count": len(joints),
        "joint_names": names,
        "roots": [nodes[r].get("name") or "" for r in roots if r < len(nodes)],
        "max_depth": max((depth(j) for j in joints), default=0),
        # Fingers are classified FIRST and removed from the hand set. "LeftHandIndex1"
        # contains "hand", so a naive two-pass count reports every finger as a hand joint
        # too and inflates the number a reader uses to judge whether a grip is riggable.
        # T101 caught this: the hint lists are not disjoint and the names are nested.
        "hand_joints": [n for n, l in zip(names, low)
                        if any(h in l for h in HAND_HINTS)
                        and not any(f in l for f in FINGER_HINTS)],
        "finger_joints": [n for n, l in zip(names, low) if any(f in l for f in FINGER_HINTS)],
        "animations": len(g.get("animations", [])),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb", required=True, help="the GLB that came back")
    ap.add_argument("--against", default=None,
                    help="the GLB that was sent, for the mesh-identity comparison")
    ap.add_argument("--require-same-mesh", action="store_true",
                    help="ANDON if the returned vertex count or bbox differs from --against. "
                         "This is the gate that catches a service quietly retopologising.")
    ap.add_argument("--require-skin", action="store_true",
                    help="ANDON if no primitive carries JOINTS_0 and WEIGHTS_0")
    ap.add_argument("--bbox-tol", type=float, default=1e-4,
                    help="per-axis bbox tolerance for --require-same-mesh, in model units")
    ap.add_argument("--json-out", default=None)
    args = ap.parse_args()

    g = read_gltf_json(args.glb)
    prims = mesh_summary(g)
    skel = skeleton_summary(g)
    total_v = sum(p["vertices"] or 0 for p in prims)

    print("%s" % args.glb)
    print("  primitives %d   total vertices %d" % (len(prims), total_v))
    for p in prims:
        print("    mesh %d/%s prim %d  verts %8d  joints=%s weights=%s"
              % (p["mesh"], p["mesh_name"], p["primitive"], p["vertices"] or 0,
                 p["has_joints"], p["has_weights"]))
    print("  skins %d   joints %d   max depth %d   animations %d"
          % (skel["skins"], skel["joint_count"], skel["max_depth"], skel["animations"]))
    print("  roots        %s" % (skel["roots"] or "-"))
    print("  hand joints  %s" % (skel["hand_joints"] or "NONE"))
    print("  finger joints %s" % (skel["finger_joints"] or "NONE"))

    same = None
    ref_total = None
    if args.against:
        ref = read_gltf_json(args.against)
        ref_prims = mesh_summary(ref)
        ref_total = sum(p["vertices"] or 0 for p in ref_prims)
        print("\n  against %s: %d vertices in %d primitives"
              % (args.against, ref_total, len(ref_prims)))

        def box(ps):
            mins = [p["min"] for p in ps if p["min"]]
            maxs = [p["max"] for p in ps if p["max"]]
            if not mins or not maxs:
                return None
            return ([min(m[i] for m in mins) for i in range(3)],
                    [max(m[i] for m in maxs) for i in range(3)])

        b_new, b_ref = box(prims), box(ref_prims)
        v_same = total_v == ref_total
        b_same = (b_new is not None and b_ref is not None and
                  all(abs(b_new[0][i] - b_ref[0][i]) <= args.bbox_tol and
                      abs(b_new[1][i] - b_ref[1][i]) <= args.bbox_tol for i in range(3)))
        same = bool(v_same and b_same)
        print("  vertex count %s (%d vs %d)" % ("SAME" if v_same else "MOVED", total_v, ref_total))
        print("  bbox         %s" % ("SAME" if b_same else "MOVED"))
        if b_new and b_ref:
            print("    returned %s" % [[round(c, 5) for c in b_new[0]], [round(c, 5) for c in b_new[1]]])
            print("    sent     %s" % [[round(c, 5) for c in b_ref[0]], [round(c, 5) for c in b_ref[1]]])

    skinned = any(p["has_joints"] and p["has_weights"] for p in prims)
    result = {"glb": args.glb, "against": args.against, "total_vertices": total_v,
              "reference_vertices": ref_total, "same_mesh": same, "skinned": skinned,
              "primitives": prims, "skeleton": skel}
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

    fail = []
    if args.require_same_mesh:
        if not args.against:
            fail.append("--require-same-mesh needs --against; there is nothing to compare to")
        elif not same:
            fail.append("the returned mesh is NOT the one that was sent - the service "
                        "replaced the geometry rather than skinning it")
    if args.require_skin and not skinned:
        fail.append("no primitive carries both JOINTS_0 and WEIGHTS_0 - nothing in this "
                    "file is skinned")
    print()
    if fail:
        print("ANDON: " + "; ".join(fail))
        sys.exit(2)
    print("RIG REPORT OK: %d vertices, %d joints, skinned=%s, same_mesh=%s"
          % (total_v, skel["joint_count"], skinned, same))


if __name__ == "__main__":
    main()
