"""T101 - the auto-rig return check, on synthetic glTF and on a real unskinned GLB.

The gate this file pins is the one that decides whether an auto-rig round trip is usable at
all: did the service skin OUR mesh, or return a NEW one? Both look the same in a viewer and
only one of them keeps the accepted asset.

THE CAN-FAIL LEGS COME FIRST. A mesh-identity check that cannot see a replaced mesh, and a
skin check that cannot see an unskinned file, would both return a clean pass on the exact
failure they exist for. So: a doc whose vertex count moved must refuse, a doc whose BBOX
moved at an unchanged count must refuse, and a real unskinned GLB must refuse --require-skin.

The parser legs run on dicts rather than GLB bytes on purpose - hand-assembling a skinned
GLB would be testing my fixture, not the tool - while two legs go through the real container
so the struct/chunk reading is exercised on a file this route actually produced.

Everything printed here is ASCII (the repo's law).
"""
import copy
import importlib.util
import json
import pathlib
import struct
import subprocess
import sys
import tempfile

import trimesh

TOOL = pathlib.Path(__file__).resolve().parents[1] / "tools" / "verify" / "rig_report.py"
_spec = importlib.util.spec_from_file_location("rig_report", TOOL)
rig_report = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rig_report)

BODY = pathlib.Path(r"E:\AI\training\saltroad_harbour\drell\drell_body_s42.glb")

# A minimal rigged document: one skinned primitive, a two-joint skeleton with a named hand.
RIGGED = {
    "asset": {"version": "2.0"},
    "nodes": [
        {"name": "Hips", "children": [1]},
        {"name": "LeftHand", "children": [2]},
        {"name": "LeftHandIndex1"},
        {"name": "body", "mesh": 0, "skin": 0},
    ],
    "skins": [{"joints": [0, 1, 2]}],
    "meshes": [{"name": "body", "primitives": [{"attributes": {
        "POSITION": 0, "JOINTS_0": 1, "WEIGHTS_0": 2}}]}],
    "accessors": [
        {"count": 1000, "min": [-1.0, -2.0, -0.5], "max": [1.0, 2.0, 0.5]},
        {"count": 1000}, {"count": 1000},
    ],
}


def _glb(doc):
    """Pack a glTF document into a JSON-only GLB, which is a legal container."""
    body = json.dumps(doc).encode("utf-8")
    body += b" " * ((4 - len(body) % 4) % 4)
    chunk = struct.pack("<II", len(body), 0x4E4F534A) + body
    return struct.pack("<III", 0x46546C67, 2, 12 + len(chunk)) + chunk


def _run(doc, *extra, against=None):
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "r.glb"
        p.write_bytes(_glb(doc))
        cmd = [sys.executable, str(TOOL), "--glb", str(p), "--json-out", str(pathlib.Path(d) / "o.json")]
        if against is not None:
            a = pathlib.Path(d) / "a.glb"
            a.write_bytes(_glb(against))
            cmd += ["--against", str(a)]
        cmd += list(extra)
        r = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL)
        out = pathlib.Path(d) / "o.json"
        return r.returncode, r.stdout + r.stderr, (json.loads(out.read_text()) if out.exists() else None)


def test_t101_a_replaced_mesh_is_refused():
    """CAN-FAIL LEG. A different vertex count must refuse, or nothing below means anything."""
    returned = copy.deepcopy(RIGGED)
    returned["accessors"][0]["count"] = 900          # retopologised
    rc, log, data = _run(returned, "--require-same-mesh", against=RIGGED)
    assert rc == 2, "a mesh with 900 vertices passed against a 1000-vertex original\n%s" % log
    assert "replaced the geometry" in log, log
    assert data["same_mesh"] is False, data


def test_t101_a_rescaled_mesh_is_refused_at_an_unchanged_count():
    """The subtler replacement: same vertex count, different bbox. Count alone would pass."""
    returned = copy.deepcopy(RIGGED)
    returned["accessors"][0]["max"] = [1.0, 2.5, 0.5]
    rc, log, data = _run(returned, "--require-same-mesh", against=RIGGED)
    assert rc == 2, "a rescaled mesh passed because its vertex count was unchanged\n%s" % log
    assert data["total_vertices"] == data["reference_vertices"], (
        "the fixture failed for the wrong reason - counts should match here: %r" % data)


def test_t101_the_same_mesh_skinned_is_accepted():
    rc, log, data = _run(RIGGED, "--require-same-mesh", "--require-skin", against=RIGGED)
    assert rc == 0, "an identical skinned mesh was refused (rc=%d)\n%s" % (rc, log)
    assert data["same_mesh"] is True and data["skinned"] is True, data


def test_t101_the_skeleton_is_read_by_name():
    rc, log, data = _run(RIGGED)
    assert rc == 0, log
    s = data["skeleton"]
    assert s["joint_count"] == 3 and s["skins"] == 1, s
    # "LeftHandIndex1" contains "hand". A finger must be counted once, as a finger:
    # T101 found the tool counting every finger as a hand joint too.
    assert s["hand_joints"] == ["LeftHand"], s
    assert s["finger_joints"] == ["LeftHandIndex1"], s
    assert s["roots"] == ["Hips"], s
    assert s["max_depth"] == 2, s


def test_t101_an_unnamed_skeleton_reports_none_rather_than_guessing():
    """A rig whose joints carry no names must report NONE, not invent a hand."""
    doc = copy.deepcopy(RIGGED)
    for n in doc["nodes"][:3]:
        n.pop("name", None)
    rc, log, data = _run(doc)
    assert rc == 0, log
    assert data["skeleton"]["hand_joints"] == [] and data["skeleton"]["finger_joints"] == [], data
    assert "NONE" in log


def test_t101_a_real_unskinned_glb_is_refused_by_require_skin():
    """Through the real container, on a file this route produced: no skin means no skin."""
    if not BODY.exists():
        return  # the asset tree is not in git; skip rather than fail a clean checkout
    p = subprocess.run([sys.executable, str(TOOL), "--glb", str(BODY), "--require-skin"],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    assert p.returncode == 2, (
        "the un-rigged body GLB reported as skinned\n%s" % (p.stdout + p.stderr))
    assert "nothing in this file is skinned" in (p.stdout + p.stderr)


def test_t101_a_real_glb_reports_its_own_vertex_count_through_the_container():
    """Exercises the struct/chunk reader, and pins the number the rig round trip must return."""
    if not BODY.exists():
        return
    doc = rig_report.read_gltf_json(str(BODY))
    prims = rig_report.mesh_summary(doc)
    total = sum(p["vertices"] for p in prims)
    # 664,162 is the FILE's number, read from the POSITION accessor. trimesh reports
    # 666,988 for the same file because its scene load splits vertices; that figure was
    # quoted as the mesh's size earlier in this arc and it is not what the container says.
    # The rig round trip is graded against the file, because the file is what was sent.
    assert total == 664162, (
        "drell_body_s42.glb reads %d vertices; the rig round trip is graded against this "
        "number, so a change here is a change to the subject, not to the tool" % total)


def test_t101_a_non_glb_is_refused_rather_than_parsed():
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "x.glb"
        p.write_bytes(b"not a glb at all, not even close")
        r = subprocess.run([sys.executable, str(TOOL), "--glb", str(p)],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        assert r.returncode != 0 and "ANDON" in (r.stdout + r.stderr)


# ---------------------------------------------------------------------------
# --require-same-shape: the gate the Comfy consult's Q3 criticism produced.
# A rig round trip may re-index or weld on export. A count-and-bbox gate cannot
# tell that from a retopology and false-halts on the harmless one; these legs
# pin that the shape gate tells them apart, in BOTH directions.
# ---------------------------------------------------------------------------

def _real_glb(mesh, path):
    path.write_bytes(trimesh.exchange.gltf.export_glb(trimesh.Scene({"body": mesh})))
    return path


def test_t101_a_reindexed_mesh_passes_the_shape_gate():
    """Same points, shuffled order and a changed vertex count. This is the case the
    count-and-bbox gate gets WRONG, so it is checked here as a pass AND as a false-halt."""
    import numpy as np
    base = trimesh.creation.icosphere(subdivisions=3, radius=0.4)
    rng = np.random.default_rng(0)
    perm = rng.permutation(len(base.vertices))
    inv = np.argsort(perm)
    shuffled = trimesh.Trimesh(vertices=base.vertices[perm], faces=inv[base.faces],
                               process=False)
    with tempfile.TemporaryDirectory() as d:
        a = _real_glb(base, pathlib.Path(d) / "sent.glb")
        b = _real_glb(shuffled, pathlib.Path(d) / "back.glb")
        out = pathlib.Path(d) / "o.json"
        r = subprocess.run([sys.executable, str(TOOL), "--glb", str(b), "--against", str(a),
                            "--require-same-shape", "--json-out", str(out)],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        log = r.stdout + r.stderr
        assert r.returncode == 0, "a re-indexed mesh was refused by the shape gate\n%s" % log
        data = json.loads(out.read_text())
        assert data["shape"]["fraction"] >= 0.999, data["shape"]
        assert data["shape"]["max"] < 1e-5, data["shape"]


def test_t101_a_decimated_mesh_fails_the_shape_gate():
    """CAN-FAIL LEG for the shape gate. New vertices land on the old SURFACE but not on
    an old VERTEX, which is the only thing separating a retopology from a re-index."""
    with tempfile.TemporaryDirectory() as d:
        sent = trimesh.creation.icosphere(subdivisions=4, radius=0.4)
        back = trimesh.creation.icosphere(subdivisions=3, radius=0.4)
        # a coarser icosphere shares its parent's vertices, so rotate it off the shared
        # lattice: the fixture must be a genuinely different vertex SET or it cannot fail
        back.apply_transform(trimesh.transformations.rotation_matrix(0.21, [0.3, 1, 0.2]))
        a = _real_glb(sent, pathlib.Path(d) / "sent.glb")
        b = _real_glb(back, pathlib.Path(d) / "back.glb")
        out = pathlib.Path(d) / "o.json"
        r = subprocess.run([sys.executable, str(TOOL), "--glb", str(b), "--against", str(a),
                            "--require-same-shape", "--json-out", str(out)],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        log = r.stdout + r.stderr
        assert r.returncode == 2, "a re-tessellated mesh passed the shape gate\n%s" % log
        assert "newly PLACED" in log, log
        data = json.loads(out.read_text())
        assert data["shape"]["median"] > 0, data["shape"]


def test_t101_the_shape_gate_needs_something_to_compare_against():
    with tempfile.TemporaryDirectory() as d:
        p = _real_glb(trimesh.creation.icosphere(subdivisions=2), pathlib.Path(d) / "x.glb")
        r = subprocess.run([sys.executable, str(TOOL), "--glb", str(p), "--require-same-shape"],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        assert r.returncode == 2 and "nothing to compare to" in (r.stdout + r.stderr)


def test_t101_the_reference_spacing_is_not_zero_on_a_seamed_mesh():
    """A reconstruction carries coincident vertices at UV and normal seams, so a naive
    2nd-nearest query returns 0.000 and the reported spacing means nothing. Measured on
    drell_body_s42.glb, which is exactly that shape. The figure must come from UNIQUE
    positions or the number beside the verdict is noise."""
    if not BODY.exists():
        return
    import json as _json
    with tempfile.TemporaryDirectory() as d:
        out = pathlib.Path(d) / "o.json"
        r = subprocess.run([sys.executable, str(TOOL), "--glb", str(BODY), "--against",
                            str(BODY), "--require-same-shape", "--json-out", str(out)],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        assert r.returncode == 0, r.stdout + r.stderr
        shape = _json.loads(out.read_text())["shape"]
        assert shape["fraction"] == 1.0 and shape["max"] == 0.0, shape
        assert shape["reference_spacing"] > 0.0, (
            "reference spacing came back %r - the duplicate-vertex trap is back, and the "
            "number printed beside the verdict is meaningless" % shape["reference_spacing"])
