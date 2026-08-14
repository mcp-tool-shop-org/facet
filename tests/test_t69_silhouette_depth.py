"""T69 (E35 arm slate) - the depth leg of silhouette_masks.py: the raycast that already
computes t_hit now emits it, and the encode does not eat surface.

WHY THIS LEG EXISTS AT ALL, AND WHY IT IS NOT A BLENDER SCRIPT. The arm slate's depth arm
needs a hint registered pixel-exactly to the clay init. turn_render.py renders under
BLENDER_WORKBENCH, which has no Z pass, so a Blender depth render would mean a different
engine and therefore a re-derived camera - and a re-derived camera is where this repo
bleeds. silhouette_masks.py already casts at turn_render's camera (its docstring derives
the convention from turn_render's own lines, and --anchor asserts byte-identity against
known-good masks), and it already computed t_hit and threw away everything but isfinite.
The depth map is that array, kept.

WHY THE FIGURE IS ENCODED INTO 1..255 AND NOT 0..255. Under a 0..255 map the FARTHEST
surface pixel takes the background's own value, and the support check can no longer tell
far surface from no surface - it would return agreement by construction. This repo has
caught two such checks already (a silhouette IoU returning 1.00000 on a holed mesh, a
dilation comparison returning 0.00% because dilation cannot lose a pixel). Leg 4 removes
the floor from a COPY of the tool and shows the ANDON firing, so the check is demonstrated
capable of failing rather than asserted to be.

WHY A SPHERE. Orientation ("near = white") has to be checked against geometry whose near
and far points are known without tracking the tool's axis remap. On an ortho camera a
sphere's nearest surface is the centre of its projected disk and its farthest is the rim,
whichever way the frame is remapped - so the check is a property of the shape, not of my
arithmetic about the shape.

WHY LEG 3 RUNS THE TOOL TWICE. The G4 gate in the field compares generated masks against
recorded ones. In-tree the equivalent question is narrower and answerable: does passing
--depth change what the mask leg writes. It must not, and leg 3 is the proof that shipped
with the edit rather than after it.

THE ANDON IS `raise`, NEVER `assert` - `python -O` and PYTHONOPTIMIZE=1 delete asserts
silently (E21 Ruling 2). Leg 4b runs the firing case under both and asserts it still halts.

Hermetic: the mesh is built in-process, nothing is read from the recorded trees.
Source is ASCII bytes (the repo's law).
"""
import json
import os
import subprocess
import sys

import numpy as np
import pytest
import trimesh
from PIL import Image

from conftest import tool

TAG = "t69synth"          # synthetic, so no census or corpus sweep can mistake it for a
                          # subject of this repo (E28's self-reference lesson)
FRAME = (64, 64)
MARGIN = 1.6              # framing only - wider than turn_render's 1.204 so the disk sits
                          # near 31% of frame, clear of the tool's 0.5-60% silhouette ANDON


@pytest.fixture(scope="module")
def prep(tmp_path_factory):
    """A unit sphere as prep_uv.glb - near point at the disk centre, far at the rim."""
    d = tmp_path_factory.mktemp("t69_prep")
    m = trimesh.creation.icosphere(subdivisions=3, radius=1.0)
    m.export(os.path.join(str(d), "prep_uv.glb"))
    return str(d)


def _run(prep_dir, out_dir, depth_dir=None, script=None, env_extra=None, expect_ok=True):
    args = [script or tool("silhouette_masks.py"),
            "--prep", prep_dir, "--out", out_dir, "--tag", TAG,
            "--views", "0", "--step", "45",
            "--aspect", "%d,%d" % FRAME, "--margin", str(MARGIN)]
    if depth_dir:
        args += ["--depth", depth_dir]
    env = dict(os.environ)
    env.update(env_extra or {})
    p = subprocess.run([sys.executable] + args, capture_output=True, text=True, env=env)
    if expect_ok and p.returncode != 0:
        raise AssertionError("tool exited %d\nSTDOUT:\n%s\nSTDERR:\n%s"
                             % (p.returncode, p.stdout, p.stderr))
    return p


def _grey(path):
    a = np.asarray(Image.open(path))
    assert a.ndim == 3 and a.shape[2] == 3, "a ControlNet hint is a 3-channel IMAGE"
    assert (a[:, :, 0] == a[:, :, 1]).all() and (a[:, :, 1] == a[:, :, 2]).all(), \
        "grey must be replicated across channels, not encoded per-channel"
    return a[:, :, 0].astype(np.int32)


@pytest.fixture(scope="module")
def run(prep, tmp_path_factory):
    out = str(tmp_path_factory.mktemp("t69_out"))
    dep = str(tmp_path_factory.mktemp("t69_depth"))
    p = _run(prep, out, dep)
    mask = np.asarray(Image.open(os.path.join(out, "%s_0.png" % TAG)).convert("L")) > 127
    near = _grey(os.path.join(dep, "%s_0_depth.png" % TAG))
    far = _grey(os.path.join(dep, "%s_0_depth_far.png" % TAG))
    with open(os.path.join(out, "silhouettes.json")) as fh:
        report = json.load(fh)
    return {"stdout": p.stdout, "mask": mask, "near": near, "far": far,
            "report": report, "out": out, "depth": dep, "prep": prep}


# --- leg 1: the support IS the silhouette -------------------------------------------

def test_t69_depth_support_is_exactly_the_mask(run):
    for name in ("near", "far"):
        arr = run[name]
        assert arr.shape == run["mask"].shape
        assert np.array_equal(arr > 0, run["mask"]), (
            "%s support differs from the mask by %d px"
            % (name, int(((arr > 0) != run["mask"]).sum())))


def test_t69_the_fixture_is_not_vacuous(run):
    """A support check over an empty or full mask would agree with anything."""
    px = int(run["mask"].sum())
    frac = px / run["mask"].size
    assert 0.15 < frac < 0.55, "disk is %.3f of frame - reframe the fixture" % frac
    assert px > 500


# --- leg 2: the encode's floor, and the inversion ------------------------------------

def test_t69_no_surface_pixel_encodes_as_background(run):
    """The far plane must land on 1, not 0. This is the property leg 4 removes."""
    m = run["mask"]
    assert run["near"][m].min() == 1
    assert run["far"][m].min() == 1
    assert run["near"][m].max() == 255
    assert run["far"][m].max() == 255


def test_t69_far_is_the_inversion_of_near(run):
    m = run["mask"]
    assert np.array_equal(run["near"][m] + run["far"][m], np.full(int(m.sum()), 256))


# --- leg 3: near = white, checked against geometry, not against arithmetic ------------

def test_t69_near_is_white_on_a_sphere(run):
    """Ortho + sphere: the disk centre is the nearest surface, the rim the farthest."""
    m, near = run["mask"], run["near"]
    ys, xs = np.nonzero(m)
    cy, cx = int(round(ys.mean())), int(round(xs.mean()))
    assert m[cy, cx], "centroid fell outside the disk"
    assert near[cy, cx] == 255, "the nearest surface is not the brightest"
    # a rim pixel: the mask pixel farthest from the centroid
    d2 = (ys - cy) ** 2 + (xs - cx) ** 2
    ry, rx = ys[d2.argmax()], xs[d2.argmax()]
    assert near[ry, rx] < near[cy, cx], "the rim is not darker than the centre"
    assert run["far"][ry, rx] > run["far"][cy, cx], "the far map is not oriented"


def test_t69_report_records_the_depth_provenance(run):
    d = run["report"]["views"]["0"]["depth"]
    assert d["near_white"] is True and d["figure_range"] == [1, 255]
    assert d["spread"] > 0 and d["t_max"] > d["t_min"]


# --- leg 4: the mask leg is not perturbed by asking for depth ------------------------

def test_t69_asking_for_depth_does_not_move_the_mask(prep, tmp_path):
    """The edit's own non-perturbing proof, riding the commit that makes the edit."""
    a, b = str(tmp_path / "no_depth"), str(tmp_path / "with_depth")
    os.makedirs(a), os.makedirs(b)
    _run(prep, a)
    _run(prep, b, str(tmp_path / "dep"))
    pa = np.asarray(Image.open(os.path.join(a, "%s_0.png" % TAG)))
    pb = np.asarray(Image.open(os.path.join(b, "%s_0.png" % TAG)))
    assert np.array_equal(pa, pb), "the mask moved when --depth was requested"
    assert pa.any() and not pa.all(), "a mask that is empty or full proves nothing"


# --- leg 5: the ANDON fires when the floor is removed, and survives -O ---------------

def _tool_without_the_floor(dst):
    """Copy the tool with the 1.. floor removed - E16-9's injected-miss method, applied
    to the source rather than to a decoy artifact in the shared tree."""
    src = tool("silhouette_masks.py")
    body = open(src, encoding="utf-8").read()
    needle = "near[hit] = 1 + np.rint(254.0 * (t_hi - t_in) / spread).astype(np.uint8)"
    assert needle in body, "the floor moved - this fixture is testing nothing"
    broken = body.replace(needle,
                          "near[hit] = np.rint(255.0 * (t_hi - t_in) / spread).astype(np.uint8)")
    assert broken != body
    p = os.path.join(dst, "silhouette_masks.py")
    open(p, "w", encoding="utf-8", newline="\n").write(broken)
    # the tool imports subject_profile from its own directory
    sp = os.path.join(os.path.dirname(src), "subject_profile.py")
    open(os.path.join(dst, "subject_profile.py"), "w", encoding="utf-8", newline="\n").write(
        open(sp, encoding="utf-8").read())
    return p


@pytest.mark.parametrize("env_extra", [
    {}, {"PYTHONOPTIMIZE": "1"},
], ids=["plain", "PYTHONOPTIMIZE=1"])
def test_t69_removing_the_floor_fires_the_andon(prep, tmp_path, env_extra):
    d = str(tmp_path / ("broken_%s" % ("O" if env_extra else "plain")))
    os.makedirs(d)
    script = _tool_without_the_floor(d)
    p = _run(prep, str(tmp_path / ("o_%s" % len(env_extra))), str(tmp_path / ("dp_%s" % len(env_extra))),
             script=script, env_extra=env_extra, expect_ok=False)
    assert p.returncode != 0, "the broken encode was accepted"
    assert "ANDON" in p.stderr and "support differs from the mask" in p.stderr, p.stderr


def test_t69_this_sessions_prints_are_ascii():
    """The repo's law is ASCII PRINTS, not ASCII source - measured, this file already
    carried 51 non-ASCII bytes before the depth leg was added and project_twins.py carries
    357, so a whole-file source assertion would be asserting something untrue. What is
    checked is the narrower thing that is true and that this session is responsible for:
    the depth leg's own printed strings."""
    body = open(tool("silhouette_masks.py"), encoding="utf-8").read()
    start = body.index("if args.depth:")
    end = body.index("if idx in anchors:", start)
    added = body[start:end]
    bad = sorted({c for c in added if ord(c) > 127})
    assert not bad, "non-ASCII in the depth leg: %r" % bad
