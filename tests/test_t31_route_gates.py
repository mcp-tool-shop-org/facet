"""T31 - the twelve route tools' gates, after E23's conversion.

E22 converted seven tools and had a behavioural net under it: T7's byte-identity
replay, T10's projection, T26's three fired ANDONs. **E23 had none.** Measured at
dispatch and re-measured here: before this file existed, no test under tests/
mentioned any of the twelve. The whole-file AST proof carried that arc, and it
cannot be a standing test - it needs the pre-conversion tree, and after the
commit HEAD *is* the converted state, so a re-run would be a tautology (E22's
report says the same of its own two checks). What is portable is ported here.

WHAT THIS FILE PINS, and what it deliberately does not:

  * every one of the twelve still compiles                          (12 cases)
  * the ten non-Blender tools reach argparse and write NOTHING, in
    all three interpreter modes                                     (30 cases)
  * no ANDON gate in the twelve is a bare `assert`, by AST, with a
    can-fail leg that plants one and sees it caught
  * the reachable gates on synthetic input REFUSE in all three modes,
    leaving nothing behind. Sixteen at E23; seventeen at t91 when
    restylize_views grew the canon path gate.
  * the census, so a later arc has to move these numbers on purpose

NO TEST HERE ASSERTS THAT `PYTHONOPTIMIZE=1` DISABLES A GATE. That would anchor
the defect. T30 already pins the stripping mechanism on throwaway source, which
is what stops the `-O` legs below from passing vacuously; this file depends on
that test rather than repeating it.

THE TWELVE ARE NOT IMPORTED. Eleven of them execute at import - three have zero
function definitions - so importing one RUNS it. E20 met this wall and refused
to restructure accepted-asset tooling; that refusal stands, and every check here
is a subprocess or an AST walk over source text.

THE BLENDER PAIR gets compile + AST only. `bake_hero_prep` and `bake_hero_pack`
import bpy, so the pinned interpreter cannot run them at all; that reason is
itself checked below rather than left as prose, and their 19 sites' behaviour is
an openly stated gap.

Everything printed here is ASCII (the repo's law).
"""
import ast
import io
import json
import os
import py_compile
import subprocess
import sys

import pytest

from conftest import REPO, tool

# ---------------------------------------------------------------------------
# the population, as E23 enumerated it (docs/experiments/E23-route-gates-report.md)
# ---------------------------------------------------------------------------
BLENDER = ["bake_hero_prep.py", "bake_hero_pack.py"]
PINNED = ["bake_hero_fuse.py", "brush_cloud_step.py", "cull_unseen.py",
          "e13_harmonize.py", "export_asset_source.py", "palette_gate.py",
          "resample_atlas.py", "restylize_views.py", "silhouette_masks.py",
          "subject_profile.py"]
ROUTE = sorted(BLENDER + PINNED)

# per-file ANDON site counts, measured at E23's census and again after the
# conversion. Pinned so that a later arc moves them deliberately rather than by
# accident - the same service E22's message census did for the seven.
#
# MOVED silhouette_masks.py 4 -> 5 BY THE E35 ARM SLATE, in the commit that earns it.
# The `--depth` leg adds one ANDON: the depth map's support must be byte-identical to
# the silhouette the same raycast produced, or the encode has eaten surface. It is a
# real gate, it raises (never asserts), and it is shown FIRING under plain Python and
# under PYTHONOPTIMIZE=1 in tests/test_t69_silhouette_depth.py by running a copy of the
# tool with the encode's 1.. floor removed.
#
# WHY IT IS NOT ALSO IN `FIRE` BELOW: every FIRE entry fires on crafted INPUT and is
# checked for -O survival and for writing nothing. This one fires on an internal
# invariant no CLI argument can violate, so it has no `build(tmp_path)` and cannot join
# that population honestly. T69 carries the same two properties for it instead - the
# firing legs in both interpreter modes, and the encode is checked before the output
# directory is created, so it has no business in DIR_AHEAD_OF_GATE either.
SITES = {"bake_hero_prep.py": 15, "brush_cloud_step.py": 10, "subject_profile.py": 6,
         "e13_harmonize.py": 5, "bake_hero_fuse.py": 4, "bake_hero_pack.py": 4,
         "silhouette_masks.py": 5, "cull_unseen.py": 3, "export_asset_source.py": 2,
         "palette_gate.py": 2, "resample_atlas.py": 2, "restylize_views.py": 2}

# ANDON gates in these files that ALREADY raised AssertionError before E23, so
# the raise census below is not read as a conversion count. Measured at 48fa733:
# exactly one, bake_hero_prep's --head-scale < 1 refusal, which an author wrote
# as a raise from the start. It also reconciles E22 Ruling 5's repo-wide
# "AssertionError 88" as 87 of E22's own conversions plus this site.
PRE_EXISTING_RAISES = {"bake_hero_prep.py": 1}

# E22 Ruling 4 measured 191 ANDON asserts left after E22, across tools/. E23 took
# the 57 route sites, leaving 134: 132 in diagnostics/, 1 in verify/, and 1 in
# superseded/ (never converted, by that ruling - those tools are kept so they fail
# the same way).
#
# MOVED 134 -> 1 BY E25, in the commit that earned it. E25 converted the 132 + 1, so
# superseded/'s site is all that is left and it stays forever. This constant is E23
# Ruling 9's structural fix for the scope-number defect that beat two consecutive
# arcs - a scope that cannot drift silently, because moving it takes a deliberate
# edit - and this is the first time it has been moved. T33 additionally pins WHICH
# file the survivor is in, so a later arc cannot convert superseded/ and stay green.
REMAINING_ELSEWHERE = 1

# THE TWO TOOLS THAT CREATE THEIR OUTPUT DIRECTORY AHEAD OF THEIR GATE. Measured,
# not tolerated: when these two fire they leave an empty `--out`/`--outdir` behind.
# No file is written by any of the sixteen - that half is asserted for every site
# below - but "nothing was written" is not literally true for these two, and
# pinning WHICH two means a third joining them fails this file.
DIR_AHEAD_OF_GATE = {"silhouette_masks:107": ["o"], "restylize_views:216": ["o"]}

MODES = [("normal", [], {}),
         ("dash-O", ["-O"], {}),
         ("PYTHONOPTIMIZE", [], {"PYTHONOPTIMIZE": "1"})]
MODE_IDS = [m[0] for m in MODES]


def _andon_asserts(src):
    """Assert nodes whose MESSAGE carries the ANDON token - E22's definition,
    reused verbatim so the two arcs count the same population."""
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
    """Every directory and file under `root`, recursively, as a comparable set.
    Recursive on purpose: a top-level listing would miss a file written INTO an
    output directory the tool had just created."""
    out = set()
    for dp, dirs, fns in os.walk(str(root)):
        for d in dirs:
            out.add(("DIR", os.path.relpath(os.path.join(dp, d), str(root)).replace("\\", "/")))
        for f in fns:
            out.add(("FILE", os.path.relpath(os.path.join(dp, f), str(root)).replace("\\", "/")))
    return out


def run(flags, script, args, cwd, env_extra=None, timeout=1800):
    """One command, one process, interpreter FLAGS as well as env, in `cwd`.

    cwd is always a scratch directory. Nothing in this file may run one of these
    tools in the repo or anywhere near a recorded tree (E23's compensator rule);
    the emptiness checks below are what make that testable rather than asserted.
    """
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)      # the ambient value must not leak in
    if env_extra:
        env.update(env_extra)
    p = subprocess.run([sys.executable] + list(flags) + [script]
                       + [str(a) for a in args],
                       cwd=str(cwd), env=env, capture_output=True, timeout=timeout)
    return (p.returncode,
            p.stdout.decode("utf-8", "replace"),
            p.stderr.decode("utf-8", "replace"))


# ---------------------------------------------------------------------------
# 1. it still compiles - the real risk of a mechanical rewrite
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rel", ROUTE)
def test_t31_route_tool_compiles(rel, tmp_path):
    """A splice that broke indentation or dropped a paren fails HERE, first, and
    names its file. Hermetic: needs no bpy, so it covers the Blender pair too.
    Measured 12/12 clean before the conversion, so this is a real before/after."""
    py_compile.compile(tool(rel), cfile=str(tmp_path / "x.pyc"), doraise=True)


# ---------------------------------------------------------------------------
# 2. --help reaches argparse and writes nothing, in every mode
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mode,flags,envx", MODES, ids=MODE_IDS)
@pytest.mark.parametrize("rel", PINNED)
def test_t31_help_is_clean_in_every_mode(rel, mode, flags, envx, tmp_path):
    """Eleven of the twelve execute at import, so `--help` exercises real
    module-level code: a splice that re-parented a statement out of a function
    surfaces here as an exception at import rather than at the gate.

    The empty-cwd half is the compensator rule made checkable - a tool that
    wrote on this path would be caught in scratch instead of in a recorded tree.
    """
    rc, out, err = run(flags, tool(rel), ["--help"], cwd=tmp_path, env_extra=envx)
    assert rc == 0, "%s --help exited %d under %s:\n%s" % (rel, rc, mode, err[-2000:])
    assert not list(tmp_path.iterdir()), (
        "%s wrote %s into the scratch cwd on its --help path under %s"
        % (rel, sorted(p.name for p in tmp_path.iterdir()), mode))


# ---------------------------------------------------------------------------
# 3. the structural law, extended to the twelve
# ---------------------------------------------------------------------------

def test_t31_no_route_gate_is_an_assert():
    """THE STANDING LAW (E21 Ruling 2, folded into CLAUDE.md at E22 Ruling 9):
    a check that decides whether an irreversible step proceeds must `raise`,
    because `-O` deletes an `assert` silently.

    Scope is the twelve E23 converted. When this file was written the 134 ANDON
    asserts still elsewhere in tools/ were a measured, reported remainder,
    deliberately not pinned here - pinning a class nobody had been asked to
    convert would fail on work that had not been done. E25 has since done that
    work, so the remainder is 1 and T33 pins the whole class by name.
    """
    offenders = []
    for rel in ROUTE:
        src = io.open(tool(rel), encoding="utf-8").read()
        offenders += ["%s:%d" % (rel, n.lineno) for n in _andon_asserts(src)]
    assert not offenders, (
        "%d ANDON gate(s) in the route tools are still bare asserts, which -O "
        "deletes:\n  %s" % (len(offenders), "\n  ".join(offenders)))


def test_t31_the_structural_check_can_fail():
    """CAN-FAIL LEG. A walk that cannot find an ANDON assert would report zero
    over the twelve whatever they contained, which is this repo's most-repeated
    defect. So: it must find a planted one, and must ignore a token-less one."""
    planted = "def f(x):\n    assert x > 0, 'ANDON: planted by the can-fail leg'\n"
    assert len(_andon_asserts(planted)) == 1, "the walk missed a planted ANDON assert"
    assert not _andon_asserts("def f(x):\n    assert x > 0, 'ordinary'\n"), (
        "the walk flags an assert carrying no ANDON token")


def test_t31_the_census_is_the_one_e23_measured():
    """The population, pinned. Every converted site is now a raise, the per-file
    counts are unchanged, and the remainder outside the twelve is stated so the
    diagnostics arc has to move it on purpose."""
    for rel, n in SITES.items():
        src = io.open(tool(rel), encoding="utf-8").read()
        want = n + PRE_EXISTING_RAISES.get(rel, 0)
        assert len(_andon_raises(src)) == want, (
            "%s carries %d ANDON raises; E23 converted %d and %d already raised"
            % (rel, len(_andon_raises(src)), n, PRE_EXISTING_RAISES.get(rel, 0)))
    # 57 was E23's route total; 58 since the E35 arm slate added silhouette_masks'
    # depth-support ANDON; 59 at t91 when restylize_views grew the canon path
    # gate (raise before mkdir); 60 at t92 when brush_cloud_step grew the
    # router (raise before the workflow JSON is written). The literal moves
    # in the commit that moves the table above, which is the whole service
    # this pin performs.
    assert sum(SITES.values()) == 60

    elsewhere = 0
    for dirpath, dirnames, filenames in os.walk(str(REPO / "tools")):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            p = os.path.join(dirpath, fn)
            if os.path.dirname(p) == str(REPO / "tools") and fn in SITES:
                continue
            elsewhere += len(_andon_asserts(io.open(p, encoding="utf-8").read()))
    assert elsewhere == REMAINING_ELSEWHERE, (
        "%d ANDON asserts remain outside the twelve; after E25 the number is %d - "
        "superseded/texpass_thin_mask.py:160, which E22 Ruling 4 ruled is never "
        "converted. A change here is an unconverted gate arriving, or superseded/ "
        "being tidied away." % (elsewhere, REMAINING_ELSEWHERE))


def test_t31_the_blender_pair_cannot_run_under_this_interpreter():
    """The stated reason the two Blender tools get no smoke, made falsifiable.

    If bpy ever became importable here, this test fails and the smoke exclusion
    above should be revisited rather than silently kept - which is the whole
    difference between a documented gap and a forgotten one.
    """
    for rel in BLENDER:
        src = io.open(tool(rel), encoding="utf-8").read()
        top = [n for n in ast.parse(src).body
               if isinstance(n, (ast.Import, ast.ImportFrom))]
        names = [a.name for n in top if isinstance(n, ast.Import) for a in n.names]
        names += [n.module for n in top if isinstance(n, ast.ImportFrom) and n.module]
        assert "bpy" in names, "%s no longer imports bpy at module level" % rel
    with pytest.raises(Exception):
        __import__("bpy")


# ---------------------------------------------------------------------------
# 4. fire what can be fired
# ---------------------------------------------------------------------------
# Seventeen are reachable on synthetic input under the pinned
# interpreter (sixteen at E23; restylize_views:115 added at t91).
# Which ones was MEASURED, not chosen: E23's probe walked every
# candidate and reported the ones whose intended ANDON reached stderr. The
# unreachable remainder, and the reason for each, is in the report - including
# brush_cloud_step:204, which no profile shape can reach because :353 tests the
# same precondition harder and stands in front of it.

def _png(path, w, h, v=200):
    from PIL import Image
    import numpy as np
    Image.fromarray(np.zeros((h, w, 3), dtype="uint8") + v).save(str(path))
    return str(path)


def _rv_thin_canon(d):
    """restylize + a one-phrase canon the warrior default cannot cover."""
    p = d / "c.surfaces.json"
    p.write_text(json.dumps({
        "subject": "X", "kind": "prop", "schema": 1,
        "surfaces": [{
            "id": "blade",
            "occupant": {
                "id": "P1", "phrase": "a steel blade", "provenance": "prompt"},
        }],
    }), encoding="utf-8")
    return ["--inputs", _png(d / "a.png", 8, 8),
            "--outdir", str(d / "o"), "--canon", str(p)]


def _write_json(path, obj):
    with io.open(str(path), "w", encoding="utf-8") as fh:
        json.dump(obj, fh)
    return str(path)


def _profile(d, body):
    return ["--profile", _write_json(d / "p.json", body)]


def _sp(tools_block):
    return {"name": "x", "tools": {"silhouette_masks.py": tools_block}}


def _cube(d):
    """A synthetic mesh, so silhouette_masks gets far enough to parse --anchor.
    Never a recorded prep tree."""
    import trimesh
    p = d / "prep"
    p.mkdir(exist_ok=True)
    trimesh.creation.box((1.0, 1.0, 2.0)).export(str(p / "prep_uv.glb"))
    return str(p)


def _eh(d, ref=None, image=None):
    good = _png(d / "r.png", 8, 8)
    return ["--reference", ref or ("R=" + good), "--ref-mask", good,
            "--image", image or ("a=" + good), "--mask", "a=" + good,
            "--outdir", str(d / "o")]


def _bcs(d, prompts=None, block=None):
    pr = _write_json(d / "prompts.json",
                     prompts if prompts is not None else {"K": "a prompt", "_negative": "n"})
    pf = _write_json(d / "p.json",
                     {"name": "x", "tools": {"texpass_brush.py": block if block is not None else {}}})
    job = d / "job"
    job.mkdir(exist_ok=True)
    return ["graph", "--job", str(job), "--key", "K", "--prompts", pr,
            "--out", str(d / "g.json"), "--profile", pf]


def _ent(v):
    return {"value": v, "why": "w", "from": "E00"}


def _bcs_canon(d):
    """Past pre-flight, then the router refuses, and --out is not written."""
    pr = _write_json(d / "prompts.json",
                     {"K": "plain grey background", "_negative": "n"})
    canon = _write_json(d / "c.surfaces.json", {
        "subject": "X", "kind": "prop", "schema": 2,
        "legal_clauses": [
            {"id": "bg", "phrase": "plain grey background", "class": "style"},
        ],
        "surfaces": [{
            "id": "blade",
            "occupant": {
                "id": "P1", "phrase": "a steel blade", "provenance": "prompt"},
        }],
    })
    block = {
        "seed": _ent(770700), "steps": _ent(20), "cfg": _ent(2.5),
        "cn-strength": _ent(1.0), "lora-w": _ent(0.75),
        "prompt": _ent("x"), "negative": _ent("n"),
    }
    pf = _write_json(d / "p.json", {
        "name": "x",
        "tools": {"texpass_brush.py": block},
        "_fixtures": {
            "canon": {"path": canon},
            "brush_prompts": {"path": pr},
        },
    })
    job = d / "job"
    job.mkdir(exist_ok=True)
    return ["graph", "--job", str(job), "--key", "K", "--prompts", pr,
            "--out", str(d / "g.json"), "--profile", pf]


def _pg(d):
    a, b = _png(d / "a.png", 8, 8), _png(d / "b.png", 8, 8)
    return ["--palette", _write_json(d / "pal.json", {"bands": []}),
            "--images", a, b, "--masks", a]


# (id, tool, build(scratch_dir) -> argv, a substring of the gate's own message)
FIRE = [
    ("subject_profile:60", "silhouette_masks.py",
     lambda d: _profile(d, {"nope": 1}), "is not a subject profile"),
    ("subject_profile:79", "silhouette_masks.py",
     lambda d: ["--profile"], "--profile needs a path"),
    ("subject_profile:113", "silhouette_masks.py",
     lambda d: _profile(d, _sp({"no-such-arg": {"value": 1, "why": "w", "from": "E00"}})),
     "which has no such argument"),
    ("subject_profile:118", "silhouette_masks.py",
     lambda d: _profile(d, _sp({"tag": 5})), "must be an object with 'value'"),
    ("subject_profile:120", "silhouette_masks.py",
     lambda d: _profile(d, _sp({"tag": {"value": "z", "from": "E00"}})), "carries no 'why'"),
    ("subject_profile:124", "silhouette_masks.py",
     lambda d: _profile(d, _sp({"tag": {"value": "z", "why": "w"}})), "carries no 'from'"),
    ("silhouette_masks:107", "silhouette_masks.py",
     lambda d: ["--prep", _cube(d), "--out", str(d / "o"), "--anchor", "NOEQUALS"],
     "--anchor wants VIEW=PATH"),
    ("e13_harmonize:92", "e13_harmonize.py",
     lambda d: _eh(d, ref="R=" + str(d / "nope.png")), "--reference path missing"),
    ("e13_harmonize:85", "e13_harmonize.py",
     lambda d: _eh(d, image="NOEQUALS"), "wants LABEL=PATH"),
    ("e13_harmonize:86", "e13_harmonize.py",
     lambda d: _eh(d, image="a=" + str(d / "nope.png")), "no such file"),
    ("palette_gate:69", "palette_gate.py", _pg, "--masks is parallel"),
    ("restylize_views:115", "restylize_views.py",
     _rv_thin_canon, "canon does not cover"),
    ("restylize_views:216", "restylize_views.py",
     lambda d: ["--inputs", _png(d / "a.png", 8, 8), _png(d / "b.png", 8, 8),
                "--outdir", str(d / "o"), "--masks", str(d / "a.png")],
     "--masks is parallel"),
    ("brush_cloud_step:382", "brush_cloud_step.py",
     lambda d: _bcs(d, prompts={"other": "p", "_negative": "n"}), "no prompt for"),
    ("brush_cloud_step:393", "brush_cloud_step.py",
     lambda d: _bcs(d, block={}), "no decided value for 'lora-w'"),
    ("brush_cloud_step:219", "brush_cloud_step.py",
     lambda d: _bcs(d, block={"lora-w": {"value": 0.75}, "_NOT_CLEARED": True}), "_NOT_CLEARED"),
    ("brush_cloud_step:226", "brush_cloud_step.py",
     lambda d: _bcs(d, block={"lora-w": {"value": 0.75}}), "has no decided value for"),
    ("brush_cloud_step:407", "brush_cloud_step.py",
     _bcs_canon, "canon does not cover"),
]
FIRE_IDS = [f[0].replace(":", "_") for f in FIRE]


@pytest.mark.parametrize("mode,flags,envx", MODES, ids=MODE_IDS)
@pytest.mark.parametrize("site,rel,build,expect", FIRE, ids=FIRE_IDS)
def test_t31_route_gate_refuses_in_every_mode(site, rel, build, expect, mode, flags,
                                              envx, tmp_path):
    """Each of these refuses under a normal interpreter AND `-O` AND
    PYTHONOPTIMIZE=1 - which before E23 it did not, because `-O` deleted it.

    The `expect` substring is the point: `rc != 0` alone would pass on an
    unrelated crash, and several of these sites sit behind other gates that
    would also produce a non-zero exit. Matching the gate's own words is what
    makes the leg specific to the gate under test.

    NOTHING IS WRITTEN, in two halves. No FILE may appear, for any site - that
    is the property the dispatch asked for. Two of the sixteen do create their
    empty output DIRECTORY before their gate fires; which two is pinned above
    from measurement, so a third joining them fails here rather than passing
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


def test_t31_the_firing_harness_can_fail(tmp_path):
    """CAN-FAIL LEG for the block above.

    A well-formed profile must NOT produce a subject_profile ANDON - the tool
    goes on and fails later, for argparse's own reason (no --prep). Without
    this, every leg above could be passing because these tools refuse whatever
    you hand them, and "the gate fired" would mean nothing.
    """
    argv = _profile(tmp_path, _sp({"tag": {"value": "z", "why": "w", "from": "E00"}}))
    rc, out, err = run([], tool("silhouette_masks.py"), argv, cwd=tmp_path)
    both = out + err
    assert rc != 0, "the probe invocation was expected to fail on missing --prep"
    for phrase in ("is not a subject profile", "which has no such argument",
                   "carries no 'why'", "carries no 'from'",
                   "must be an object with 'value'"):
        assert phrase not in both, (
            "a VALID profile still fired subject_profile's %r gate, so the legs "
            "above prove nothing:\n%s" % (phrase, both[-2000:]))
