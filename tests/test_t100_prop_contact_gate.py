"""T100 - the held-prop contact gate, on synthetic meshes with a KNOWN separation.

This is a behavioural test, not an AST one: the gate's whole value is that it returns a
number nobody has to squint at, so a test that only reads its source would miss the thing
it exists for. Two boxes are built at a stated gap, exported as a GLB with the same node
naming the route produces, and the tool is run as a subprocess.

THE CAN-FAIL LEG IS THE FIRST ONE. A gate that never refuses is not a gate, and this repo
has shipped two checks that returned a clean 0 because nothing could have made them
non-zero. Here the separated pair MUST exit 2 before the touching pair's exit 0 means
anything.

WHY AN AREA FLOOR AND NOT JUST A MINIMUM. A minimum of zero says two surfaces meet
somewhere; one vertex meets somewhere. The real asset that prompted this tool had a
minimum of 0.00072 and a contact patch of 97 points out of 624,510 - it passed "touching"
and was plainly not held. The point-touch leg pins that a kiss is refused while a face
contact is accepted, which is the distinction the tool is for. That floor is an AREA: a
count is a fraction of however many samples the prop got, and this file's own first fixture
could not construct a point-touch that a count would refuse.

Everything printed here is ASCII (the repo's law).
"""
import json
import pathlib
import subprocess
import sys
import tempfile

import numpy as np
import trimesh

TOOL = pathlib.Path(__file__).resolve().parents[1] / "tools" / "verify" / "prop_contact.py"


def _scene(gap, prop_size=(0.10, 0.10, 0.01)):
    """A body box, and a prop slab `gap` away from its +X face along X."""
    body = trimesh.creation.box(extents=(0.20, 0.20, 0.40))
    prop = trimesh.creation.box(extents=prop_size)
    prop.apply_translation([0.10 + gap + prop_size[0] / 2.0, 0.0, 0.0])
    s = trimesh.Scene()
    s.add_geometry(body, node_name="body", geom_name="g_body")
    s.add_geometry(prop, node_name="prop", geom_name="g_prop")
    return s


def _run(scene, *extra):
    with tempfile.TemporaryDirectory() as d:
        glb = pathlib.Path(d) / "s.glb"
        out = pathlib.Path(d) / "r.json"
        glb.write_bytes(scene.export(file_type="glb"))
        p = subprocess.run(
            [sys.executable, str(TOOL), "--glb", str(glb), "--prop", "prop",
             "--json-out", str(out), *extra],
            capture_output=True, text=True, stdin=subprocess.DEVNULL)
        data = json.loads(out.read_text()) if out.exists() else None
        return p.returncode, p.stdout + p.stderr, data


def test_t100_a_separated_prop_is_refused():
    """CAN-FAIL LEG. 5 mm of air must exit 2 and say so, or nothing below means anything."""
    rc, log, data = _run(_scene(gap=0.005))
    assert rc == 2, "a prop 5 mm clear of the body was not refused (rc=%d)\n%s" % (rc, log)
    assert "ANDON" in log and "AIR" in log, log
    assert data is not None and abs(data["min_surface_distance"] - 0.005) < 5e-4, (
        "measured %r for a built-in 0.005 gap" % (data or {}).get("min_surface_distance"))


def test_t100_a_point_touch_is_refused_as_not_gripped():
    """The defect that prompted the tool: minimum zero, contact area near nothing.

    A 10 mm sphere resting 0.02 mm into the box touches, and cannot be gripping. Built as
    a SPHERE rather than a tilted slab because the first version of this fixture did not
    construct the case it claimed - the rotated slab ended up face-deep in the box and
    passed, which is how the count-vs-area defect in the tool was found.
    """
    body = trimesh.creation.box(extents=(0.20, 0.20, 0.40))
    ball = trimesh.creation.icosphere(subdivisions=4, radius=0.005)
    ball.apply_translation([0.10 + 0.005 - 0.00002, 0.0, 0.0])
    s = trimesh.Scene()
    s.add_geometry(body, node_name="body", geom_name="g_body")
    s.add_geometry(ball, node_name="prop", geom_name="g_prop")
    rc, log, data = _run(s)
    assert data is not None and data["min_surface_distance"] <= 0.002, (
        "the fixture does not touch at all, so it tests the wrong refusal: %r" % data)
    assert rc == 2, ("a 10 mm ball resting on the surface passed as a grip (rc=%d)\n%s"
                     % (rc, log))
    assert "not gripped" in log, log
    assert data["contact_area_prop_side"] < 0.0005, data


def test_t100_a_face_contact_is_accepted():
    rc, log, data = _run(_scene(gap=-0.002), "--min-area", "0.0005")
    assert rc == 0, "a prop sunk 2 mm into the body was refused (rc=%d)\n%s" % (rc, log)
    assert data["min_surface_distance"] <= 0.002, data
    assert data["contact_area_prop_side"] >= 0.0005, data


def test_t100_a_single_mesh_glb_is_refused_rather_than_guessed_at():
    body = trimesh.creation.box(extents=(0.2, 0.2, 0.4))
    s = trimesh.Scene()
    s.add_geometry(body, node_name="body", geom_name="g_body")
    rc, log, _ = _run(s)
    assert rc != 0 and "ANDON" in log, "a GLB with no prop node was not refused\n%s" % log


def test_t100_the_tolerance_is_a_flag_not_a_constant():
    """A gate whose threshold is buried in the source cannot be stated in a report."""
    src = TOOL.read_text(encoding="utf-8")
    assert '"--tol"' in src and '"--min-area"' in src
    assert "not derived from the result" in src, (
        "the tool no longer states that its thresholds are set independently of the "
        "result they judge - that sentence is the guard against retuning after seeing")
