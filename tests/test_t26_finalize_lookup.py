"""T26 (E20 U4) - texpass_finalize's lookup: both ANDONs FIRED, and the edge
length proved measured rather than hardcoded.

WHY THESE ARE SUBPROCESS TESTS AND NOT UNIT TESTS. texpass_finalize.py has ZERO
function definitions - the whole tool, both lookup paths and both ANDONs, is
straight-line module-level code, so there is no unit to call. The dispatch's U4
("surface-aware nearest-painted-in-3D on a small synthetic mesh with
hand-computable answers") cannot be written as stated without restructuring the
tool, which is a tool change this session does not take. Reported in
E20-coverage-report.md with the seam proposed rather than applied; what IS
achievable without touching the tool is everything below, and it includes the
part U4 called for most - the can-fail proofs.

THE FIXTURE IS E18's, CONSUMED NOT EDITED (E20-ruling 2). D2's selftest_min
carries state/ and prep/, and finalize's surface-aware path additionally wants
`prep_uv.glb` INSIDE --prep while D2 names its mesh `mesh_uv.glb` at the fixture
root. So each test copies D2 into tmp_path and places the mesh where finalize
looks for it. The committed fixture is read-only here and a hash check proves it.

Source is ASCII bytes (the repo's law).
"""
import hashlib
import json
import os
import shutil

import numpy as np
import pytest
import trimesh
from PIL import Image

from conftest import REPO, run_py

FIXTURE = REPO / "tests" / "fixtures" / "selftest_min"


def _stage(tmp_path, scale=1.0):
    """D2's state+prep in tmp_path, with the mesh where finalize looks for it.

    `scale` multiplies the mesh's vertex coordinates. That is the lever for the
    edge-length test: it changes the geometry's absolute size and nothing else,
    so a per-mesh measurement must move with it and a hardcoded constant cannot.
    """
    state = tmp_path / "state"
    prep = tmp_path / "prep"
    shutil.copytree(str(FIXTURE / "state"), str(state))
    shutil.copytree(str(FIXTURE / "prep"), str(prep))
    mesh = trimesh.load(str(FIXTURE / "mesh_uv.glb"), force="mesh", process=False)
    if scale != 1.0:
        mesh.vertices = mesh.vertices * scale
    with open(str(prep / "prep_uv.glb"), "wb") as fh:
        fh.write(trimesh.exchange.gltf.export_glb(
            trimesh.Scene(mesh), include_normals=True))
    return state, prep


def _tree_hashes(root):
    out = {}
    for base, dirs, names in os.walk(str(root)):
        dirs.sort()
        for n in sorted(names):
            p = os.path.join(base, n)
            with open(p, "rb") as fh:
                out[os.path.relpath(p, str(root)).replace("\\", "/")] = \
                    hashlib.sha256(fh.read()).hexdigest()
    return out


@pytest.fixture(autouse=True)
def _fixture_is_read_only():
    """E18's committed fixture must come back untouched from every test here."""
    before = _tree_hashes(FIXTURE)
    yield
    assert _tree_hashes(FIXTURE) == before, (
        "a test in this file modified E18's committed fixture tree - it is "
        "consumed, never edited (E20-ruling 2)")


def _run(state, prep, out, *extra):
    return run_py("texpass_finalize.py",
                  ["--state", state, "--prep", prep, "--out", out] + list(extra))


# ---------------------------------------------------------------------------
# the two lookup paths, and the zero that is structural vs the zero that is earned
# ---------------------------------------------------------------------------

def test_t26_surface_aware_fills_every_hole(tmp_path):
    state, prep = _stage(tmp_path)
    out = tmp_path / "sa.png"
    js = tmp_path / "sa.json"
    rc, o, e = _run(state, prep, out, "--surface-aware", "--json", js)
    assert rc == 0, "surface-aware exited %d\n%s\n%s" % (rc, o, e)
    rep = json.loads(js.read_text(encoding="ascii"))
    assert rep["mode"] == "surface_aware"
    assert rep["hole_texels"] == 512, rep
    assert rep["painted_texels"] == rep["hole_texels"], (
        "%d of %d holes filled" % (rep["painted_texels"], rep["hole_texels"]))
    assert out.exists()


def test_t26_the_flood_path_also_runs_and_reports_a_different_mode(tmp_path):
    state, prep = _stage(tmp_path)
    js = tmp_path / "fl.json"
    rc, o, e = _run(state, prep, tmp_path / "fl.png", "--json", js)
    assert rc == 0, e
    rep = json.loads(js.read_text(encoding="ascii"))
    assert rep["mode"] != "surface_aware", rep["mode"]
    assert "atlas-space flood" in o, o


def test_t26_the_structural_zero_is_labelled_as_such(tmp_path):
    """ANCHOR: the tool's own comment at L160-170 - in surface-aware mode
    `valid & ~grown` "is empty by construction and `left` is 0 on every run
    regardless of the atlas. Three subjects quoted that zero as a pass; the
    dragon's celebrated zero was structural, not earned. A check that cannot
    fail is not a check, so this mode must not print the count as if it were
    informative."

    So the two paths must be DISTINGUISHABLE in their output, and they are.
    """
    state, prep = _stage(tmp_path)
    _, sa_out, _ = _run(state, prep, tmp_path / "a.png", "--surface-aware")
    state2, prep2 = _stage(tmp_path / "second")
    _, fl_out, _ = _run(state2, prep2, tmp_path / "b.png")

    assert "STRUCTURAL in surface-aware mode" in sa_out, sa_out
    assert "not a measured pass" in sa_out
    assert "STRUCTURAL" not in fl_out, (
        "the flood path claimed a structural zero; its zero is earned and must "
        "read as the ordinary count")
    assert "took mean fallback" in fl_out, fl_out


# ---------------------------------------------------------------------------
# the edge length: MEASURED per mesh, not hardcoded from one
# ---------------------------------------------------------------------------

def test_t26_edge_length_is_invariant_under_a_uniform_rescale(tmp_path):
    """ANCHOR: the measurement's own line - the vertices are divided by
    `np.abs(_v).max()` and scaled to 0.5 before any edge is measured, so a
    uniform rescale of the mesh is divided straight back out.

    That invariance is REQUIRED, not incidental: the gate is stated in edges
    (`med_e = median(dist) / edge`) and `dist` is measured in the same normalized
    frame, so both operands must move together or the ratio would depend on what
    units the glb happened to be authored in.

    This test began life asserting the OPPOSITE - that scaling 3x would move the
    reported edge - on the theory that a value which cannot move must be
    hardcoded. It measured 1.00000 both times, and the cause was normalization,
    not a constant. The premise was mine and it was wrong; the invariance is the
    real property and this is it.
    """
    s1, p1 = _stage(tmp_path / "one", scale=1.0)
    s3, p3 = _stage(tmp_path / "three", scale=3.0)
    j1, j3 = tmp_path / "one.json", tmp_path / "three.json"
    rc1, o1, e1 = _run(s1, p1, tmp_path / "one.png", "--surface-aware", "--json", j1)
    rc3, _, e3 = _run(s3, p3, tmp_path / "three.png", "--surface-aware", "--json", j3)
    assert rc1 == 0 and rc3 == 0, (e1, e3)
    r1 = json.loads(j1.read_text(encoding="ascii"))
    r3 = json.loads(j3.read_text(encoding="ascii"))
    assert r1["median_edge_len"] == r3["median_edge_len"], (
        "a uniform rescale moved the measured edge %.6f -> %.6f; both operands "
        "of the edge-stated gate live in the normalized frame and must not"
        % (r1["median_edge_len"], r3["median_edge_len"]))
    assert r1["dist_median_edges"] == r3["dist_median_edges"], (
        "the gated ratio moved under a pure rescale: %.3f -> %.3f"
        % (r1["dist_median_edges"], r3["dist_median_edges"]))
    assert "measured on this mesh" in o1, o1


def test_t26_the_edge_length_tracks_this_meshs_own_tessellation(tmp_path):
    """The can-fail proof that the edge really is measured per mesh.

    CLAUDE.md records that `texpass_finalize.py` "had that edge length hardcoded
    from one mesh" - past tense, and the tool's own comment says "The scale must
    come from THIS mesh - a hardcoded constant is the same family as the blade
    pixel-rectangle the loop was rewritten to remove". Uniform scale cannot test
    that (see the test above), but TESSELLATION can: subdividing the same surface
    halves its triangle edges in the normalized frame while the geometry is
    unchanged. A hardcoded constant cannot follow that; a measurement must.
    """
    state, prep = _stage(tmp_path / "coarse")
    state_f, prep_f = _stage(tmp_path / "fine")
    mesh = trimesh.load(str(FIXTURE / "mesh_uv.glb"), force="mesh", process=False)
    fine = mesh.subdivide().subdivide()
    with open(str(prep_f / "prep_uv.glb"), "wb") as fh:
        fh.write(trimesh.exchange.gltf.export_glb(
            trimesh.Scene(fine), include_normals=True))

    jc, jf = tmp_path / "c.json", tmp_path / "f.json"
    rc1, _, e1 = _run(state, prep, tmp_path / "c.png", "--surface-aware", "--json", jc)
    rc2, _, e2 = _run(state_f, prep_f, tmp_path / "f.png", "--surface-aware",
                      "--json", jf)
    assert rc1 == 0 and rc2 == 0, (e1, e2)
    coarse = json.loads(jc.read_text(encoding="ascii"))["median_edge_len"]
    finer = json.loads(jf.read_text(encoding="ascii"))["median_edge_len"]
    assert finer < coarse * 0.6, (
        "median edge %.6f -> %.6f after two subdivisions of the same surface; a "
        "value hardcoded from one mesh could not follow the tessellation"
        % (coarse, finer))


# ---------------------------------------------------------------------------
# THE CAN-FAIL PROOFS - both distance ANDONs fired
# ---------------------------------------------------------------------------
# Each is fired by setting the tool's OWN bound below the measured value. That
# proves the guard is wired, halts, and refuses before writing - it does NOT
# claim anything about whether the DEFAULT bound is calibrated, which is a
# different question and not this session's to answer.

def test_t26_andon_source_distance_median_fires_and_refuses_the_write(tmp_path):
    """The ANDON at texpass_finalize.py:129."""
    state, prep = _stage(tmp_path)
    out = tmp_path / "never.png"
    rc, o, e = _run(state, prep, out, "--surface-aware", "--max-edge-median", "0.1")
    assert rc != 0, "the ANDON did not halt the run (rc %d)\n%s" % (rc, o)
    assert "ANDON" in e, e
    assert "median source distance" in e, e
    assert "colour is coming from elsewhere on the figure" in e, e
    assert not out.exists(), (
        "the atlas was written after the ANDON fired - the guard must precede "
        "the irreversible step (E08 Amendment 32)")


def test_t26_andon_fraction_beyond_n_edges_fires_and_refuses_the_write(tmp_path):
    """The ANDON at texpass_finalize.py:132."""
    state, prep = _stage(tmp_path)
    out = tmp_path / "never.png"
    rc, o, e = _run(state, prep, out, "--surface-aware",
                    "--beyond-edges", "0.1", "--max-frac-beyond", "0.0")
    assert rc != 0, "the ANDON did not halt the run (rc %d)\n%s" % (rc, o)
    assert "ANDON" in e, e
    assert "source from beyond" in e, e
    assert not out.exists(), "the atlas was written after the ANDON fired"


def test_t26_a_clean_run_does_not_fire_either_andon(tmp_path):
    """The other half of a can-fail proof: the guards must be silent when the
    measurement is inside the bound, or they are not measuring anything."""
    state, prep = _stage(tmp_path)
    out = tmp_path / "clean.png"
    rc, o, e = _run(state, prep, out, "--surface-aware")
    assert rc == 0, e
    assert "ANDON" not in e, e
    assert out.exists()


def test_t26_andon_uniform_atlas_fires_on_a_flat_state(tmp_path):
    """The third ANDON (`assert var > 0.001`, "final atlas uniform").

    Fired by constructing the input it exists to catch rather than by moving a
    bound: a state whose atlas is a single colour stays uniform through hole
    filling, so the variance check has something to catch. The fixture is built
    here from D2's shapes, not by editing D2.
    """
    state, prep = _stage(tmp_path)
    res = np.load(str(prep / "pos.npy")).shape[0]
    flat = np.full((res, res, 3), 0.5, dtype=np.float32)
    Image.fromarray((flat * 255).round().astype(np.uint8)).save(
        str(state / "atlas.png"))
    out = tmp_path / "uniform.png"
    rc, o, e = _run(state, prep, out, "--surface-aware")
    assert rc != 0, "a flat atlas passed the uniformity ANDON (rc %d)\n%s" % (rc, o)
    assert "ANDON: final atlas uniform" in e, e
    assert not out.exists()
