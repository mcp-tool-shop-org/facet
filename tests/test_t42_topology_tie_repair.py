"""T42 - e14_topology.py's tie repair, and the proof it perturbs nothing (E28 2a).

THE CRASH (E27 F1, reproduced at three seats). `thin = argmin(ext)`,
`tall = argmax(ext)`, `wide = 3 - thin - tall`: argmin == argmax exactly when
min(ext) == max(ext) - the first-of-min and first-of-max positions can only
coincide if the values do - so on a mesh whose three extents are ALL equal,
`wide` is 3 and `lo[wide]` raises IndexError. The unit cube fixture is that
mesh. Two-way ties do NOT crash: argmin != argmax whenever min != max.

THE REPAIR is a guard: `if thin == tall: thin, tall = 0, 2`. Its proof
obligation, from the dispatch, discharged here rather than cited from
E27 Ruling 3: on any input where the OLD expression produces indices at all -
distinct extents AND two-way ties - the repaired selection is IDENTICAL,
because the guard branch is dead there. Shown by:

  1. a randomized sweep over distinct-extent triples (hermetic, below),
  2. a randomized sweep over two-way-tie triples (hermetic, below - the class
     the dispatch's invariant does not mention and the repair must also hold),
  3. tool-conformance runs proving the SHIPPED FILE implements the expression
     this file sweeps (hermetic, synthetic GLBs - without these the sweep
     would be two in-test expressions agreeing with each other),
  4. the recorded subjects (artifacts tier): every one has three pairwise
     distinct extents - E28-task2-predictions P9b, pinned - so the guard is
     dead on all of them and the byte-identity claim's domain is real.

THE CAN-FAIL LEG carries the crash: the old expression, applied to the cube
fixture's own measured extents, must still index out of bounds - and the
repaired TOOL, run on the same fixture, must exit 0 with three distinct axes.
If the fixture ever stops being extent-degenerate, the leg says so instead of
passing vacuously.
"""
import io
import json
import os
import subprocess
import sys

import numpy as np
import pytest

from conftest import REPO, ASSETS_ENV, DEFAULT_ASSETS

TOOL = os.path.join(str(REPO), "tools", "diagnostics", "e14_topology.py")
CUBE = os.path.join(str(REPO), "tests", "fixtures", "measure_min", "meshes",
                    "cube.glb")

# the transform and weld the tool itself applies - extents here must be the
# extents the tool sees, or the sweep proves a property of different numbers
GLTF_TO_BLENDER = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]])


def old_selection(ext):
    """The pre-repair expression, verbatim. Returns (thin, tall, wide) or
    raises IndexError exactly where the old tool did - `wide` is used as an
    index into a 3-vector, so 3 is out of bounds."""
    thin = int(np.argmin(ext))
    tall = int(np.argmax(ext))
    wide = 3 - thin - tall
    _ = np.zeros(3)[wide]            # the crash site, faithfully
    return thin, tall, wide


def new_selection(ext):
    """The repaired expression, verbatim from the shipped file. Leg 3 below
    proves the SHIPPED FILE implements this; without that leg this function
    would be a re-implementation the sweep grades against itself."""
    thin = int(np.argmin(ext))
    tall = int(np.argmax(ext))
    if thin == tall:
        thin, tall = 0, 2
    wide = 3 - thin - tall
    return thin, tall, wide


def tool_axes(glb, tmp, timeout=300):
    """(thin, tall, wide) as the SHIPPED tool reports them, via its JSON."""
    out = os.path.join(str(tmp), "t.json")
    p = subprocess.run(
        [sys.executable, TOOL, "--glb", str(glb), "--out", out],
        cwd=str(REPO), capture_output=True, timeout=timeout)
    assert p.returncode == 0, (
        "e14_topology exited %d on %s:\n%s"
        % (p.returncode, glb, p.stderr.decode("utf-8", "replace")[-800:]))
    with io.open(out, encoding="utf-8") as fh:
        rec = json.load(fh)
    ax = {"x": 0, "y": 1, "z": 2}
    thin = ax[rec["cross_sections"]["thin_axis"]]
    tall = ax[rec["cross_sections"]["scan_axis"]]
    return thin, tall, 3 - thin - tall


# ---------------------------------------------------------------------------
# leg 0 - the can-fail pair: the crash is real, and the repair returns axes
# ---------------------------------------------------------------------------

def cube_extents():
    import trimesh
    m = trimesh.load(CUBE, force="mesh", process=False)
    m.merge_vertices(merge_tex=True, merge_norm=True)
    co = np.asarray(m.vertices, dtype=np.float64) @ GLTF_TO_BLENDER.T
    return co.max(axis=0) - co.min(axis=0)


def test_t42_the_old_expression_still_crashes_on_the_cube_fixture():
    """The mechanism, pinned to the fixture's MEASURED extents rather than to
    an assumed [1,1,1]. If the fixture ever stops being extent-degenerate this
    fails loudly instead of the whole file passing vacuously."""
    ext = cube_extents()
    assert float(ext.min()) == float(ext.max()), (
        "the cube fixture's extents are no longer all equal (%r), so nothing "
        "below exercises the tie class it exists for" % (ext.tolist(),))
    with pytest.raises(IndexError):
        old_selection(ext)


def test_t42_the_repaired_tool_returns_three_distinct_axes_on_the_cube(tmp_path):
    """The other half of the can-fail pair: the SHIPPED tool, not the
    expression, run on the mesh that crashed it at three seats."""
    thin, tall, wide = tool_axes(CUBE, tmp_path)
    assert sorted((thin, tall, wide)) == [0, 1, 2], (
        "the repaired tool selected %r, which is not a permutation of the "
        "three axes" % ((thin, tall, wide),))


# ---------------------------------------------------------------------------
# legs 1 + 2 - the sweeps. Deterministic seed: replayable, not tunable.
# ---------------------------------------------------------------------------

def test_t42_sweep_distinct_extents_old_and_new_select_identically():
    """The dispatch's invariant, discharged: >=10,000 random triples with three
    pairwise-distinct extents; one differing selection falsifies the repair."""
    rng = np.random.default_rng(28)
    tried = 0
    while tried < 10_000:
        ext = rng.uniform(0.01, 10.0, size=3)
        if len({float(v) for v in ext}) != 3:
            continue
        tried += 1
        assert old_selection(ext) == new_selection(ext), (
            "selection diverged on distinct extents %r" % (ext.tolist(),))
    # and the corners of the space: every permutation of a fixed distinct triple
    from itertools import permutations
    for p in permutations((1.0, 2.0, 3.0)):
        ext = np.array(p)
        assert old_selection(ext) == new_selection(ext), (
            "selection diverged on permutation %r" % (p,))


def test_t42_sweep_two_way_ties_old_does_not_crash_and_new_agrees():
    """The class the dispatch's invariant does not mention, and the reason the
    repair is a GUARD rather than an argsort: the old expression does NOT
    crash on a two-way tie (argmin != argmax whenever min != max), so a repair
    that changed the selection there would be a behaviour change wearing a
    crash fix's clothes. All six tie shapes x both orders, plus a sweep."""
    rng = np.random.default_rng(282)
    cases = []
    for _ in range(2_000):
        a, b = rng.uniform(0.01, 10.0, size=2)
        if float(a) == float(b):
            continue
        cases.extend([(a, a, b), (a, b, a), (b, a, a)])
    for ext in cases:
        e = np.array(ext)
        assert old_selection(e) == new_selection(e), (
            "selection diverged on two-way tie %r" % (list(ext),))


def test_t42_all_equal_new_returns_a_permutation_where_old_raises():
    """The repaired class itself: every all-equal triple must yield a
    permutation of the axes from the new expression and IndexError from the
    old one."""
    for v in (1.0, 0.5, 2.75):
        ext = np.array([v, v, v])
        with pytest.raises(IndexError):
            old_selection(ext)
        assert sorted(new_selection(ext)) == [0, 1, 2]


# ---------------------------------------------------------------------------
# leg 3 - the shipped file implements the expression the sweeps proved
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("extents", [
    (1.0, 2.0, 3.0),     # distinct, ascending
    (3.0, 2.0, 1.0),     # distinct, descending
    (2.0, 3.0, 1.0),     # distinct, mixed
    (1.0, 1.0, 2.0),     # two-way tie, the pair first
    (2.0, 1.0, 1.0),     # two-way tie, the pair last
], ids=["asc", "desc", "mixed", "tie-low", "tie-high"])
def test_t42_the_shipped_tool_matches_the_swept_expression(tmp_path, extents):
    """Without this leg the sweeps are two in-test expressions agreeing with
    each other. A box with known extents goes through the REAL tool - load,
    weld, GLTF axis swap and all - and the tool's own JSON must select the
    axes `new_selection` predicts for the extents the tool measures.

    The GLTF round-trip swaps Y and Z (the tool maps back), so the box is
    built in Blender-frame extents and the prediction is computed on the
    extents the tool actually reports."""
    import trimesh
    m = trimesh.creation.box(extents=extents)
    glb = os.path.join(str(tmp_path), "box.glb")
    m.export(glb)
    got = tool_axes(glb, tmp_path)
    # read back what the tool measured, through its own pipeline
    m2 = trimesh.load(glb, force="mesh", process=False)
    m2.merge_vertices(merge_tex=True, merge_norm=True)
    co = np.asarray(m2.vertices, dtype=np.float64) @ GLTF_TO_BLENDER.T
    ext = co.max(axis=0) - co.min(axis=0)
    assert got == new_selection(ext), (
        "the shipped tool selected %r where the swept expression selects %r "
        "on the extents the tool measures (%r)"
        % (got, new_selection(ext), ext.tolist()))


# ---------------------------------------------------------------------------
# leg 4 - the recorded subjects (artifacts tier): P9b, and the domain is real
# ---------------------------------------------------------------------------
# Every GLB the record shows this tool's family measuring, plus the four
# accepted assets and their preps. Extents-only: load + weld + min/max, no
# tool run - the byte-level old-vs-new comparison ran once at the 2a seat and
# is recorded in the report; THIS leg keeps the domain claim (distinct
# extents everywhere, so the guard is dead on every recorded subject)
# runnable forever.
RECORDED_SUBJECTS = [
    "facet_next/E14_gate0/longsword_00001_raw.glb",
    "facet_next/E14_gate0/longsword_00002_raw.glb",
    "facet_next/E14_gate0/longsword_00003_raw.glb",
    "facet_next/E14_prep/prep_uv.glb",
    "facet_next/E14_strokes/run/final/longsword_hero.glb",
    "facet_next/E12_gate0/dragon_00001_raw.glb",
    "facet_next/E12_gate0/dragon_00002_raw.glb",
    "facet_next/E12_gate0/dragon_00003_raw.glb",
    "facet_next/E12_prep/prep_uv.glb",
    "facet_next/E13_stroke/run/dragon_hero.glb",
    "facet_next/E04_gate0/galleon_00004_raw.glb",
    "facet_next/E04_gate0/galleon_00005_raw.glb",
    "facet_next/E04_gate0/galleon_00006_raw.glb",
    "facet_next/E04_shipprep/prep_uv.glb",
    "facet_next/E04_stroke/out/galleon_final.glb",
    "facet_E08/ARMB/out/W3_final.glb",
    "facet_E01/tex_W3/prepV2/prep_uv.glb",
]


@pytest.mark.artifacts
@pytest.mark.parametrize("rel", RECORDED_SUBJECTS)
def test_t42_every_recorded_subject_has_distinct_extents(rel):
    """P9b, pinned. A tie in a recorded mesh would mean the old tool cannot
    produce bytes there and the byte-identity claim narrows - the falsifier
    the predictions file names. Skips with a printed reason when the recorded
    trees are absent (CI), per the artifacts-tier contract."""
    root = os.environ.get(ASSETS_ENV, DEFAULT_ASSETS)
    p = os.path.join(root, rel.replace("/", os.sep))
    if not os.path.exists(p):
        pytest.skip("recorded tree absent: %s" % p)
    import trimesh
    m = trimesh.load(p, force="mesh", process=False)
    m.merge_vertices(merge_tex=True, merge_norm=True)
    co = np.asarray(m.vertices, dtype=np.float64) @ GLTF_TO_BLENDER.T
    ext = co.max(axis=0) - co.min(axis=0)
    assert len({float(v) for v in ext}) == 3, (
        "%s has tied extents %r - the old expression could not produce bytes "
        "here, and the repair's byte-identity domain excludes it. Report it; "
        "do not widen this assertion." % (rel, ext.tolist()))
    assert old_selection(ext) == new_selection(ext)
