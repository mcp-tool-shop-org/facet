"""T33 - the 43 instrument files' gates, after E25's conversion.

E22 took the seven, E23 the twelve route tools, E25 the last 133 deletable ANDONs:
132 in `tools/diagnostics/` and 1 in `tools/verify/`. Before this file existed, no
test under tests/ mentioned any of the 43. The whole-file AST proof carried the arc
and cannot be a standing test - it needs the pre-conversion tree, and after the commit
HEAD *is* the converted state, so a re-run would be a tautology. What is portable is
ported here, on the pattern T31 set.

WHAT THIS FILE PINS, and what it deliberately does not:

  * every one of the 43 still compiles                              (43 cases)
  * the 41 non-excluded tools reach argparse and write NOTHING, in
    all three interpreter modes                                    (123 cases)
  * no ANDON gate in the 43 is a bare `assert`, by AST, with a
    can-fail leg that plants one and sees it caught
  * the gates reachable on synthetic input REFUSE in all three modes
  * the census, so a later arc has to move these numbers on purpose

NO TEST HERE ASSERTS THAT `PYTHONOPTIMIZE=1` DISABLES A GATE. T30 pins the stripping
mechanism on throwaway source, which is what stops the `-O` legs below from passing
vacuously; this file depends on that test rather than repeating it.

THE 43 ARE NOT IMPORTED. Most execute at import, so importing one RUNS it. Every check
here is a subprocess or an AST walk over source text.

TWO ARE EXCLUDED FROM THE SMOKE, each for a measured reason that is itself checked
below rather than left as prose:
  * `e12_head_render.py` imports bpy, so the pinned interpreter cannot run it at all.
  * `e04_make_brush_prompts.py` does file work BEFORE argparse and dies on a missing
    profile path, so it has no clean `--help`. That is a defect in the tool, reported
    to the E25 ruling rather than repaired here - a pure-move arc does not change
    behaviour, and widening an exclusion quietly is how a gap becomes forgotten.

Everything printed here is ASCII (the repo's law).
"""
import ast
import io
import json
import os
import py_compile
import sys

import pytest

from conftest import REPO, tool

# ---------------------------------------------------------------------------
# the population, as E25 enumerated and re-measured it
# ---------------------------------------------------------------------------
SITES = {
    "diagnostics/e14_repair_collar.py": 13, "diagnostics/e14_make_brush_prompts.py": 8,
    "diagnostics/e04_blotch.py": 7, "diagnostics/e14_demote_garnet.py": 7,
    "diagnostics/e08_intersect_delta.py": 6, "diagnostics/e14_garnet_reproject.py": 6,
    "diagnostics/e04_make_brush_prompts.py": 5, "diagnostics/e08_acceptance.py": 5,
    "diagnostics/e13_crop_registration.py": 5, "diagnostics/e12_mouth_geometry.py": 4,
    "diagnostics/e12_thin_curve.py": 4, "diagnostics/e13_hole_map.py": 4,
    "diagnostics/e14_atlas_anatomy.py": 4, "diagnostics/e04_stroke_cameras.py": 3,
    "diagnostics/e08_contradiction.py": 3, "diagnostics/e12_head_render.py": 3,
    "diagnostics/e12_region_colour.py": 3, "diagnostics/e13_anchor_check.py": 3,
    "diagnostics/e13_gate1_sheet.py": 3, "diagnostics/e14_band_density.py": 3,
    "diagnostics/gained_bg_check.py": 3, "diagnostics/silhouette_agree.py": 3,
    "diagnostics/e08_ceiling.py": 2, "diagnostics/e12_frame.py": 2,
    "diagnostics/e12_head_sheet.py": 2, "diagnostics/e12_twin_readout.py": 2,
    "diagnostics/e13_a2_allocation.py": 2, "diagnostics/e13_payoff_sheet.py": 2,
    "diagnostics/e14_pair_readout.py": 2, "diagnostics/brush_reach.py": 1,
    "diagnostics/e12_ab_sheet.py": 1, "diagnostics/e12_crop_silhouette.py": 1,
    "diagnostics/e12_elevated.py": 1, "diagnostics/e12_head_evidence.py": 1,
    "diagnostics/e12_nonmanifold.py": 1, "diagnostics/e12_view_visibility.py": 1,
    "diagnostics/e13_stroke_cameras.py": 1, "diagnostics/e13_thin_inputs.py": 1,
    "diagnostics/e14_backdrop_checks.py": 1, "diagnostics/e14_topology.py": 1,
    "diagnostics/flagged_identity.py": 1, "diagnostics/keyed_outside.py": 1,
    "verify/gate0_sheet.py": 1,
}
SCOPE = sorted(SITES)

BLENDER = "diagnostics/e12_head_render.py"
PRE_ARGPARSE_FILE_WORK = "diagnostics/e04_make_brush_prompts.py"
SMOKE = [r for r in SCOPE if r not in (BLENDER, PRE_ARGPARSE_FILE_WORK)]

# ANDON gates in the 43 that already raised SystemExit before E25, so the raise census
# below is not read as a conversion count. E22 Ruling 5 ruled these stay: SystemExit is
# not deletable by -O, so none of them carries the defect this arc exists to fix.
# 28 across 12 files at E25; 30 across 14 at E32, which added one
# `raise SystemExit("ANDON: ...")` to each of its two tools; 32 across 15 at E33, whose
# single tool carries two - a candidate whose size is off its control's, and a missing
# candidate. This pin finding them is the pin working: all four are raises, not asserts,
# so none is deletable by -O, and T65 runs E33's firing case under both -O and
# PYTHONOPTIMIZE=1 and asserts no sheet is written after the gate fires.
# 35 across 16 at the E35 close: `tools/verify/tree_manifest.py` carries three -
# --emit without --out/--occasion, a manifest that does not verify, and the selftest
# refusing to report PASSED on a walk that misbehaves. All three are raises, so -O
# cannot delete them, and T70 runs the fixture under PYTHONOPTIMIZE=1 to show it.
SYSTEMEXIT_ANDONS = 35          # across 16 files; 3 of those also hold assert ANDONs
SYSTEMEXIT_ANDON_FILES = 16

# After E25 the only ANDON assert left anywhere under tools/ is superseded/'s one.
# E22 Ruling 4 ruled it NEVER converted - those tools are kept so anyone can run them
# and watch them fail the same way, and changing how they fail is the one thing that
# would spoil them. E23 Ruling 9 made this constant the structural fix for the
# scope-number defect that beat two consecutive arcs: moving it takes a deliberate edit.
REMAINING_ELSEWHERE = 1
SUPERSEDED_SITE = ("superseded/texpass_thin_mask.py", 160)

# Tools that create their output directory AHEAD of the gate that fires. Measured, not
# tolerated: pinning WHICH ones means a new one joining them fails this file.
DIR_AHEAD_OF_GATE = {
    "e12_mouth_geometry:61": ["o"],
    "e12_mouth_geometry:63": ["o"],
}

MODES = [("normal", [], {}),
         ("dash-O", ["-O"], {}),
         ("PYTHONOPTIMIZE", [], {"PYTHONOPTIMIZE": "1"})]
MODE_IDS = [m[0] for m in MODES]


def _andon_asserts(src):
    """Assert nodes whose MESSAGE carries the ANDON token - E22's definition, reused
    verbatim so every arc counts the same population."""
    return [n for n in ast.walk(ast.parse(src))
            if isinstance(n, ast.Assert) and n.msg is not None
            and "ANDON" in (ast.get_source_segment(src, n.msg) or "")]


def _andon_raises(src):
    """`raise AssertionError(<msg carrying ANDON>)` - the converted form."""
    out = []
    for n in ast.walk(ast.parse(src)):
        if (isinstance(n, ast.Raise) and isinstance(n.exc, ast.Call)
                and isinstance(n.exc.func, ast.Name)
                and n.exc.func.id == "AssertionError" and len(n.exc.args) == 1):
            if "ANDON" in (ast.get_source_segment(src, n.exc.args[0]) or ""):
                out.append(n)
    return out


def _snapshot(root):
    """Every directory and file under `root`, recursively. Recursive on purpose: a
    top-level listing would miss a file written INTO a directory just created."""
    out = set()
    for dp, dirs, fns in os.walk(str(root)):
        for d in dirs:
            out.add(("DIR", os.path.relpath(os.path.join(dp, d), str(root)).replace("\\", "/")))
        for f in fns:
            out.add(("FILE", os.path.relpath(os.path.join(dp, f), str(root)).replace("\\", "/")))
    return out


def run(flags, script, args, cwd, env_extra=None, timeout=900):
    """One command, one process, interpreter FLAGS as well as env, in `cwd`.

    cwd is ALWAYS a scratch directory. Nothing in this file may run one of these tools
    in the repo or anywhere near a recorded tree (E23's compensator rule); the
    emptiness checks below are what make that testable rather than asserted.
    """
    import subprocess
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)      # the ambient value must not leak in
    if env_extra:
        env.update(env_extra)
    p = subprocess.run([sys.executable] + list(flags) + [script] + [str(a) for a in args],
                       cwd=str(cwd), env=env, capture_output=True, timeout=timeout)
    return (p.returncode,
            p.stdout.decode("utf-8", "replace"),
            p.stderr.decode("utf-8", "replace"))


# ---------------------------------------------------------------------------
# 1. it still compiles - the real risk of a mechanical rewrite
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rel", SCOPE)
def test_t33_instrument_compiles(rel, tmp_path):
    """A splice that broke indentation or dropped a paren fails HERE, first, and names
    its file. Hermetic: needs no bpy, so it covers the Blender file too. Measured 43/43
    clean before the conversion, so this is a real before/after."""
    py_compile.compile(tool(rel), cfile=str(tmp_path / "x.pyc"), doraise=True)


# ---------------------------------------------------------------------------
# 2. --help reaches argparse and writes nothing, in every mode
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mode,flags,envx", MODES, ids=MODE_IDS)
@pytest.mark.parametrize("rel", SMOKE)
def test_t33_help_is_clean_in_every_mode(rel, mode, flags, envx, tmp_path):
    """Most of the 43 execute at import, so `--help` exercises real module-level code:
    a splice that re-parented a statement out of a function surfaces here as an
    exception at import rather than at the gate.

    The empty-cwd half is the compensator rule made checkable - a tool that wrote on
    this path would be caught in scratch instead of beside a recorded tree.
    """
    rc, out, err = run(flags, tool(rel), ["--help"], cwd=tmp_path, env_extra=envx)
    assert rc == 0, "%s --help exited %d under %s:\n%s" % (rel, rc, mode, err[-2000:])
    assert not list(tmp_path.iterdir()), (
        "%s wrote %s into the scratch cwd on its --help path under %s"
        % (rel, sorted(p.name for p in tmp_path.iterdir()), mode))


# ---------------------------------------------------------------------------
# 3. the structural law, extended to the 43
# ---------------------------------------------------------------------------

def test_t33_no_instrument_gate_is_an_assert():
    """THE STANDING LAW (E21 Ruling 2, folded into CLAUDE.md at E22 Ruling 9): a check
    that decides whether an irreversible step proceeds must `raise`, because `-O`
    deletes an `assert` silently."""
    offenders = []
    for rel in SCOPE:
        src = io.open(tool(rel), encoding="utf-8").read()
        offenders += ["%s:%d" % (rel, n.lineno) for n in _andon_asserts(src)]
    assert not offenders, (
        "%d ANDON gate(s) in the instruments are still bare asserts, which -O "
        "deletes:\n  %s" % (len(offenders), "\n  ".join(offenders)))


def test_t33_the_structural_check_can_fail():
    """CAN-FAIL LEG. A walk that cannot find an ANDON assert would report zero over the
    43 whatever they contained, which is this repo's most-repeated defect. So: it must
    find a planted one, and must ignore a token-less one."""
    planted = "def f(x):\n    assert x > 0, 'ANDON: planted by the can-fail leg'\n"
    assert len(_andon_asserts(planted)) == 1, "the walk missed a planted ANDON assert"
    assert not _andon_asserts("def f(x):\n    assert x > 0, 'ordinary'\n"), (
        "the walk flags an assert carrying no ANDON token")


def test_t33_the_census_is_the_one_e25_measured():
    """The population, pinned. Every converted site is now a raise and the per-file
    counts are unchanged."""
    for rel, n in SITES.items():
        src = io.open(tool(rel), encoding="utf-8").read()
        got = len(_andon_raises(src))
        assert got == n, "%s carries %d ANDON raises; E25 converted %d" % (rel, got, n)
    assert sum(SITES.values()) == 133
    assert len(SITES) == 43


def test_t33_the_only_andon_assert_left_is_the_superseded_one():
    """E23 Ruling 9's structural fix, moved deliberately in the commit that earns it:
    T31 pinned 134 before this arc; after it the number is 1.

    That one is `superseded/texpass_thin_mask.py` and it is PERMANENTLY out of scope
    (E22 Ruling 4) - those tools are kept precisely so anyone can run them and watch
    them fail the same way, and changing how they fail is the one thing that spoils
    them. So this test does two jobs: it holds the remainder at 1, and it names WHICH
    one, so a future arc cannot convert it by accident and still see a green suite.
    """
    found = []
    for dirpath, dirnames, filenames in os.walk(str(REPO / "tools")):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in sorted(filenames):
            if not fn.endswith(".py"):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, str(REPO / "tools")).replace("\\", "/")
            for n in _andon_asserts(io.open(p, encoding="utf-8").read()):
                found.append((rel, n.lineno))
    assert len(found) == REMAINING_ELSEWHERE, (
        "%d ANDON asserts remain under tools/; E25 left exactly %d (superseded/'s, "
        "never converted). Found: %s" % (len(found), REMAINING_ELSEWHERE, found))
    assert found[0] == SUPERSEDED_SITE, (
        "the surviving ANDON assert is %s, not the superseded site %s. Either "
        "superseded/ was converted - which E22 Ruling 4 forbids - or an unconverted "
        "gate has arrived somewhere new." % (found[0], SUPERSEDED_SITE))


def test_t33_the_systemexit_collision_is_unchanged():
    """E22 Ruling 5 / E23 Ruling 13: 28 ANDONs in this scope already raise SystemExit,
    across 12 files. They STAY - SystemExit is not deletable by -O, so none of them
    carries this arc's defect, and normalising a type nobody ruled is not a pure move.
    Pinned so the collision is a measured standing fact rather than a remembered one.
    """
    n = 0
    files = set()
    for sub in ("diagnostics", "verify"):
        for p in sorted((REPO / "tools" / sub).glob("*.py")):
            src = io.open(str(p), encoding="utf-8").read()
            for node in ast.walk(ast.parse(src)):
                if (isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call)
                        and isinstance(node.exc.func, ast.Name)
                        and node.exc.func.id == "SystemExit" and node.exc.args):
                    if "ANDON" in (ast.get_source_segment(src, node.exc.args[0]) or ""):
                        n += 1
                        files.add(p.name)
    assert (n, len(files)) == (SYSTEMEXIT_ANDONS, SYSTEMEXIT_ANDON_FILES), (
        "the SystemExit ANDON population is %d across %d files; the pin says %d across %d"
        % (n, len(files), SYSTEMEXIT_ANDONS, SYSTEMEXIT_ANDON_FILES))


def test_t33_the_blender_file_cannot_run_under_this_interpreter():
    """The stated reason `e12_head_render.py` gets no smoke, made falsifiable. If bpy
    ever became importable here, this fails and the exclusion should be revisited
    rather than silently kept - the difference between a documented gap and a
    forgotten one."""
    src = io.open(tool(BLENDER), encoding="utf-8").read()
    top = [n for n in ast.parse(src).body if isinstance(n, (ast.Import, ast.ImportFrom))]
    names = [a.name for n in top if isinstance(n, ast.Import) for a in n.names]
    names += [n.module for n in top if isinstance(n, ast.ImportFrom) and n.module]
    assert "bpy" in names, "%s no longer imports bpy at module level" % BLENDER
    with pytest.raises(Exception):
        __import__("bpy")


def test_t33_the_other_smoke_exclusion_is_the_tools_own_defect(tmp_path):
    """`e04_make_brush_prompts.py` is excluded from the smoke because it does file work
    BEFORE argparse, so even `--help` dies on a missing profile path. That is a finding
    about the tool, not a property of this arc, and it is pinned here so the exclusion
    cannot outlive its reason: if the tool is ever fixed to parse arguments first, this
    test fails and the file should rejoin SMOKE.
    """
    rc, out, err = run([], tool(PRE_ARGPARSE_FILE_WORK), ["--help"], cwd=tmp_path)
    assert rc != 0, (
        "%s now exits 0 on --help; it no longer does file work before argparse, so it "
        "should be moved into SMOKE" % PRE_ARGPARSE_FILE_WORK)
    assert "FileNotFoundError" in err or "No such file" in err, (
        "%s fails --help for a reason other than the measured missing-profile-path "
        "one:\n%s" % (PRE_ARGPARSE_FILE_WORK, err[-2000:]))


# ---------------------------------------------------------------------------
# 4. fire what can be fired
# ---------------------------------------------------------------------------
# WHICH gates was MEASURED, not chosen: a prober walked every non-Blender tool, built
# an argv from its own argparse spec plus synthetic files, and recorded which ANDON
# reached stderr. The set below is that measurement plus the sibling gates in the same
# files that the prober's mutations did not happen to try.
#
# THIS IS A LOWER BOUND ON REACHABILITY, NOT AN UPPER ONE. A gate absent here may still
# be reachable by a cleverer input; nothing proves otherwise. The dominant blocker is
# measured and stated in the E25 report: these instruments consume a prep tree, an
# atlas, a state dump and several twins that must be MUTUALLY CONSISTENT in resolution,
# view count, UV layout and owner indices, and their gates sit after those loads - so
# an ordinary exception arrives before the gate does.

def _png(path, w=8, h=8, v=200):
    from PIL import Image
    import numpy as np
    Image.fromarray(np.zeros((h, w, 3), dtype="uint8") + v).save(str(path))
    return str(path)


def _npz(path, views=("v0", "v1"), trust=False):
    import numpy as np
    np.savez(str(path), __views__=np.array(list(views)),
             __trust_intersect__=np.array(bool(trust)))
    return str(path)


def _prep(d):
    """A SYNTHETIC prep tree with the layout a recorded one has - meta.json, pos/nor/
    mask .npy and prep_uv.glb - at res 64 instead of 4096. NEVER a copy of a recorded
    tree, and never a path into one."""
    import numpy as np
    p = d / "prep"
    p.mkdir(exist_ok=True)
    R = 64
    for nm in ("pos", "nor", "mask"):
        np.save(str(p / (nm + ".npy")), np.zeros((R, R, 3), dtype="float32"))
    _png(p / "atlas.png", R, R, 128)
    import trimesh
    trimesh.creation.box((1.0, 1.0, 2.0)).export(str(p / "prep_uv.glb"))
    (p / "meta.json").write_text(json.dumps({
        "res": R, "lo": [-0.5, -0.25, -0.5], "hi": [0.5, 0.25, 0.5],
        "maxabs": 0.5, "bound": 0.55, "crop": [0.0, 0.0, float(R), float(R)],
        "crop_res": R, "head_scale": 1.0, "head_uv_area_share": 0.24,
        "head_face_share": 0.27}), encoding="utf-8")
    return str(p)


def _glb(d):
    import trimesh
    trimesh.creation.box((1.0, 1.0, 2.0)).export(str(d / "m.glb"))
    return str(d / "m.glb")


def _lp(d, bad):
    """The LABEL=PATH family: three separate tools parse --image/--mask with the same
    kv() helper, so the same two malformed specs reach the same two gates in each."""
    good = _png(d / "g.png")
    return ["--image", bad, "--mask", "a=" + good]


# (id, tool, build(scratch_dir) -> argv, a substring of the gate's own message)
FIRE = [
    # --- the LABEL=PATH family: same kv() helper, three separate tools
    ("e12_region_colour:68", "diagnostics/e12_region_colour.py",
     lambda d: _lp(d, "NOEQUALS") + ["--region", "0,0,4,4:r"],
     "wants LABEL=PATH"),
    ("e12_region_colour:70", "diagnostics/e12_region_colour.py",
     lambda d: _lp(d, "a=" + str(d / "nope.png")) + ["--region", "0,0,4,4:r"],
     "no such file"),
    ("e12_twin_readout:81", "diagnostics/e12_twin_readout.py",
     lambda d: _lp(d, "NOEQUALS"), "wants LABEL=PATH"),
    ("e12_twin_readout:83", "diagnostics/e12_twin_readout.py",
     lambda d: _lp(d, "a=" + str(d / "nope.png")), "no such file"),
    ("e13_crop_registration:67", "diagnostics/e13_crop_registration.py",
     lambda d: _lp(d, "NOEQUALS"), "wants LABEL=PATH"),
    ("e13_crop_registration:69", "diagnostics/e13_crop_registration.py",
     lambda d: _lp(d, "a=" + str(d / "nope.png")), "no such file"),

    # --- the two dump readers, whose gates key on a flag recorded IN the dump
    ("e08_intersect_delta:40", "diagnostics/e08_intersect_delta.py",
     lambda d: ["--r0", _npz(d / "r0.npz", ("v0",)),
                "--r1", _npz(d / "r1.npz", ("v1",), True)], "view lists differ"),
    ("e08_intersect_delta:42", "diagnostics/e08_intersect_delta.py",
     lambda d: ["--r0", _npz(d / "r0.npz", trust=True),
                "--r1", _npz(d / "r1.npz", trust=True)],
     "--r0 was run WITH --trust-intersect"),
    ("e08_intersect_delta:44", "diagnostics/e08_intersect_delta.py",
     lambda d: ["--r0", _npz(d / "r0.npz"), "--r1", _npz(d / "r1.npz")],
     "--r1 was run WITHOUT --trust-intersect"),
    ("gained_bg_check:63", "diagnostics/gained_bg_check.py",
     lambda d: ["--r0", _npz(d / "r0.npz", trust=True),
                "--r1", _npz(d / "r1.npz", trust=True), "--twins", str(d)],
     "--r0 has the intersection ON"),
    ("gained_bg_check:65", "diagnostics/gained_bg_check.py",
     lambda d: ["--r0", _npz(d / "r0.npz"), "--r1", _npz(d / "r1.npz"),
                "--twins", str(d)], "--r1 has the intersection OFF"),

    # --- an arity gate and the degeneracy gate behind it
    ("e12_mouth_geometry:61", "diagnostics/e12_mouth_geometry.py",
     lambda d: ["--glb", _glb(d), "--out", str(d / "o"), "--box", "1",
                "--sections", "0"], "--box wants x0,y0,z0,x1,y1,z1"),
    ("e12_mouth_geometry:63", "diagnostics/e12_mouth_geometry.py",
     lambda d: ["--glb", _glb(d), "--out", str(d / "o"),
                "--box", "1,1,1,0,0,0", "--sections", "0"], "degenerate cavity box"),

    # --- a missing input each, behind real geometry work in two of them
    ("keyed_outside:87", "diagnostics/keyed_outside.py",
     lambda d: ["--prep", _prep(d), "--twins", str(d / "empty"), "--views", "1"],
     "no twin at"),
    ("silhouette_agree:98", "diagnostics/silhouette_agree.py",
     lambda d: ["--prep", _prep(d), "--mask", str(d), "--views", "1"],
     "no sidecar at"),
    ("e13_gate1_sheet:53", "diagnostics/e13_gate1_sheet.py",
     lambda d: ["--yaw", "0", "--reference", str(d / "nope.png"),
                "--asset", _png(d / "a.png"), "--prov", _png(d / "p.png"),
                "--clay", _png(d / "c.png"), "--mask", _png(d / "m.png"),
                "--out", str(d / "o" / "s.png")], "panel missing:"),
    ("gate0_sheet:53", "verify/gate0_sheet.py",
     lambda d: ["--concept", _png(d / "c.png"), "--renders", str(d / "empty"),
                "--out", str(d / "o" / "s.png")], "no clay_*.png in"),
]
FIRE_IDS = [f[0].replace(":", "_") for f in FIRE]


@pytest.mark.parametrize("mode,flags,envx", MODES, ids=MODE_IDS)
@pytest.mark.parametrize("site,rel,build,expect", FIRE, ids=FIRE_IDS)
def test_t33_instrument_gate_refuses_in_every_mode(site, rel, build, expect, mode,
                                                   flags, envx, tmp_path):
    """Each of these refuses under a normal interpreter AND `-O` AND PYTHONOPTIMIZE=1 -
    which before E25 it did not, because `-O` deleted it.

    The `expect` substring is the point: `rc != 0` alone would pass on an unrelated
    crash, and several of these sites sit behind other work that would also produce a
    non-zero exit. Matching the gate's own words is what makes the leg specific.

    NOTHING IS WRITTEN, in two halves. No FILE may appear, for any site. Four of these
    tools create their output DIRECTORY before their gate fires; which four is pinned
    above from measurement, so a fifth joining them fails here rather than passing
    under a loosened rule.
    """
    argv = build(tmp_path)
    before = _snapshot(tmp_path)
    rc, out, err = run(flags, tool(rel), argv, cwd=tmp_path, env_extra=envx)
    both = out + err
    assert rc != 0, "%s did not refuse under %s (rc 0):\n%s" % (site, mode, both[-2000:])
    assert "ANDON" in both, "%s refused under %s without saying ANDON:\n%s" % (
        site, mode, both[-2000:])
    assert expect in both, (
        "%s refused under %s but not with its own message (wanted %r):\n%s"
        % (site, mode, expect, both[-2000:]))

    new = _snapshot(tmp_path) - before
    new_files = sorted(n for kind, n in new if kind == "FILE")
    new_dirs = sorted(n for kind, n in new if kind == "DIR")
    assert not new_files, (
        "%s WROTE A FILE when it fired under %s: %s" % (site, mode, new_files))
    assert new_dirs == DIR_AHEAD_OF_GATE.get(site, []), (
        "%s created %s under %s; the measured set for this site is %s"
        % (site, new_dirs, mode, DIR_AHEAD_OF_GATE.get(site, [])))


def test_t33_the_firing_harness_can_fail(tmp_path):
    """CAN-FAIL LEG for the block above.

    A WELL-FORMED --image/--mask pair must NOT fire either LABEL=PATH gate - the tool
    goes on and fails later, for its own reason. Without this, every leg above could be
    passing because these tools refuse whatever you hand them, and "the gate fired"
    would mean nothing.
    """
    good = _png(tmp_path / "g.png")
    argv = ["--image", "a=" + good, "--mask", "a=" + good]
    rc, out, err = run([], tool("diagnostics/e12_twin_readout.py"), argv, cwd=tmp_path)
    both = out + err
    for phrase in ("wants LABEL=PATH", "no such file"):
        assert phrase not in both, (
            "a VALID --image/--mask pair still fired the %r gate, so the legs above "
            "prove nothing:\n%s" % (phrase, both[-2000:]))
