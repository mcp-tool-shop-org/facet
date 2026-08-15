"""T41 - the instrument census's classifier, and the population it counts (E28).

WHY THIS FILE EXISTS, AND WHY ITS LEGS ARE SHAPED AS FAILURES. `tools/instrument_census.py`
produces the numbers the measurement surface's boundary is ruled against. A
NUMBER FROM AN UNFALSIFIED CLASSIFIER IS NOT A MEASUREMENT, and this repo has
caught two checks that could not fail: a silhouette IoU that returned 1.00000 on
a mesh with a hole clean through it, and a dilation comparison that returned
0.00% by construction. So every axis below is shown FAILING on synthetic input
built to fail it, not merely agreeing with the directory as it happens to stand.

E28 gate 2: these legs pass before any census number is believed.

THE POPULATION IS PINNED HERE, the E23 Ruling 9 pattern. `tools/diagnostics/`
holds 102 `.py` files (99 through E28; E32 added two, E33 one); the spec estimated "~80"
and that estimate is what the census exists to replace. Moving the count
requires editing this file, on purpose, in the commit that moves it - it cannot
drift silently.

    THE SPEC'S ESTIMATE IS THE ARGUMENT FOR THE PIN. "~80" was not a lie; it was
    a hand-read, and a hand-read has no way to notice it has gone stale.
"""
import io
import os
import subprocess
import sys

import pytest

from conftest import REPO

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import instrument_census as IC          # noqa: E402


# ---------------------------------------------------------------------------
# the population - pinned, PER HOME
# ---------------------------------------------------------------------------
# Extended DELIBERATELY at E28 task 2-pre (Amendment 1 / Ruling 5): the
# boundary's backing map spans two homes, so the pin does too. Moving either
# number requires editing this dict on purpose, in the commit that moves it.

EXPECTED_PY_FILES = {
    # UNMOVED by E31 Ruling 6's packaging, and that is worth a line because it
    # nearly did move. Packaging these directories does NOT require an
    # `__init__.py` in the source tree: setuptools ships every `.py` in an
    # explicitly-listed `packages` entry, and nothing imports these
    # directories anyway - the server spawns instruments as SUBPROCESSES by
    # path. Measured both ways on clean builds; the wheel carries 99 + 9
    # either way. Adding the two marker files would have grown this population
    # by two AND fired the census's own duplicate-basename ANDON, since it
    # keys axes D/E/G on the filename and `__init__.py` would exist in both
    # homes. The gate was right and the change was unnecessary.
    # 99 -> 101 at E32: e32_plate_geometry.py + e32_route_preprocess.py, both
    # judged for axis G in the same commit (E32 Ruling 7's procedure - the pin
    # moves deliberately, driven off the tree, never off a transcribed list).
    # 101 -> 102 at E33: e33_register_sheet.py, judged for axis G in the same
    # commit under the same procedure.
    "tools/diagnostics": 102,
    # 8 -> 9 at E28 task 2c: anchor_compare.py entered by ruling + wrap
    # (Ruling 10, Ruling 3's entry rule), census re-run in the same commit.
    # 9 -> 10 at the E35 close: tree_manifest.py, the protection-manifest walk that
    # three arcs had been rewriting inline (and that E35's open session got wrong,
    # firing a false halt on E34's declared `excludes_self`). Judged `none` for axis G
    # in this same commit under the file's own rule - line 1 names tree integrity, not
    # one of the eight spec questions, and it returns HELD/FIRED rather than a
    # measurement, on `gate_mesh`'s verdict-tool precedent. Census re-run here too.
    "tools/verify": 10,
}


@pytest.mark.parametrize("dir_rel,expected", sorted(EXPECTED_PY_FILES.items()))
def test_t41_the_population_is_what_the_census_claims(dir_rel, expected):
    """E23 Ruling 9's pattern. If this fires, the directory moved: re-run the
    census, re-read its diff, and change the number here deliberately."""
    names, others = IC.members(dir_rel)
    assert len(names) == expected, (
        "%s holds %d .py files, this test pins %d. That is not "
        "a failure to route around - the census's every denominator is this "
        "number. Re-run `python tools/instrument_census.py --committed`, read "
        "the diff in docs/instrument-census.json, and move this pin in the "
        "same commit." % (dir_rel, len(names), expected))


@pytest.mark.parametrize("dir_rel", sorted(EXPECTED_PY_FILES))
def test_t41_the_population_has_no_non_py_members(dir_rel):
    """Task 1 measured 0 files of any other extension in diagnostics and 2-pre
    measured 0 in verify. A stray `.json` or `.md` would silently sit outside
    every axis."""
    _names, others = IC.members(dir_rel)
    assert others == [], (
        "%s now holds non-.py files, which no axis measures: %s"
        % (dir_rel, ", ".join(others)))


def test_t41_the_committed_homes_are_the_pinned_homes():
    """COMMITTED_DIRS and this file's pin must name the same homes - a home
    added to one and not the other would be censused but unpinned, or pinned
    but never emitted."""
    assert sorted(IC.COMMITTED_DIRS) == sorted(EXPECTED_PY_FILES), (
        "the census emits %r, this file pins %r"
        % (sorted(IC.COMMITTED_DIRS), sorted(EXPECTED_PY_FILES)))


def test_t41_members_refuses_a_missing_directory():
    """A census whose population directory is gone must HALT, not return an
    empty list that reads as `no instruments`."""
    with pytest.raises(RuntimeError) as e:
        IC.members("tools/not-here")
    assert "ANDON" in str(e.value)


def test_t41_build_refuses_a_filename_shared_across_homes(tmp_path, monkeypatch):
    """Axes D/E/G key on the FILENAME, so one name in two censused homes would
    merge two files' evidence into one row. The census must refuse, not merge."""
    for sub in ("home_a", "home_b"):
        d = tmp_path / sub
        d.mkdir()
        with io.open(str(d / "same_name.py"), "w", encoding="utf-8",
                     newline="\n") as fh:
            fh.write('"""A file with a twin elsewhere."""\n')
    monkeypatch.setattr(IC, "REPO", str(tmp_path))
    monkeypatch.setattr(IC, "G_PROPOSAL", {})
    with pytest.raises(RuntimeError) as e:
        IC.build(sys.executable, 5, True, progress=False,
                 dirs=("home_a", "home_b"))
    assert "ANDON" in str(e.value) and "same_name.py" in str(e.value)


# ---------------------------------------------------------------------------
# a synthetic corpus, so every leg below fails on purpose
# ---------------------------------------------------------------------------

def write(tmp_path, name, body):
    p = tmp_path / name
    with io.open(str(p), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    return str(p)


INVOCABLE = '''"""Measure a thing, any subject."""
import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb")
    ap.add_argument("--out")
    return ap.parse_args()

if __name__ == "__main__":
    main()
'''

NO_FLAGS = '''"""Has argparse and a guard but takes nothing."""
import argparse

if __name__ == "__main__":
    argparse.ArgumentParser().parse_args()
'''

NO_GUARD = '''"""Takes flags but is not runnable as a script."""
import argparse

def build():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb")
    return ap
'''

LIBRARY = '''"""A helper other diagnostics import."""

def helper(x):
    return x + 1
'''

SUBJECT_MODULE_LEVEL = '''"""Bound to one arc's run."""
import argparse

PREP = r"E:\\AI\\training\\facet_next\\E12_prep"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    return ap.parse_args()

if __name__ == "__main__":
    main()
'''

SUBJECT_DEEP_ONLY = '''"""Subject only as an argparse default, inside a function."""
import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prep", default="E:/AI/training/saltroad_bake_fix")
    return ap.parse_args()

if __name__ == "__main__":
    main()
'''

SUBJECT_IN_DOCSTRING_ONLY = r'''r"""Run me against E:\AI\training\facet_next\thing.

Only the docstring names a subject, which is documentation, not binding.
"""
import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb")
    return ap.parse_args()

if __name__ == "__main__":
    main()
'''

NO_DOCSTRING = '''import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb")
    return ap.parse_args()

if __name__ == "__main__":
    main()
'''

BROKEN = '''"""This file does not parse."""
def main(:
    pass
'''

BPY_IMPORTER = '''"""Needs Blender's Python, which the pinned interpreter is not."""
import argparse
import bpy

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb")
    return ap.parse_args()

if __name__ == "__main__":
    main()
'''

NOISY_HELP = '''"""Exits 0 on --help but writes to stderr while importing."""
import argparse
import sys

sys.stderr.write("a deprecation notice nobody reads\\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb")
    return ap.parse_args()

if __name__ == "__main__":
    main()
'''


# ---------------------------------------------------------------------------
# axis A - can-fail
# ---------------------------------------------------------------------------

def test_t41_axis_a_finds_flags_when_they_are_there(tmp_path):
    r = IC.source_axes(write(tmp_path, "a_ok.py", INVOCABLE))
    assert r["a_argparse"] is True
    assert r["a_add_argument"] == 2
    assert r["a_main_guard"] is True
    assert r["invocable"] is True


@pytest.mark.parametrize("name,body,why", [
    ("a_noflags.py", NO_FLAGS, "argparse and a guard but zero add_argument"),
    ("a_noguard.py", NO_GUARD, "flags but no __main__ guard"),
    ("a_library.py", LIBRARY, "no argparse at all"),
])
def test_t41_axis_a_says_no_when_any_clause_is_missing(tmp_path, name, body, why):
    """ALL THREE CLAUSES, and each one is shown to matter on its own. A
    two-of-three definition would call `a_noguard.py` invocable, and axis F
    would then RUN it - which is the case the census must never reach."""
    r = IC.source_axes(write(tmp_path, name, body))
    assert r["invocable"] is False, "axis A accepted a file that %s" % why


def test_t41_axis_a_counts_flags_rather_than_detecting_them(tmp_path):
    """`add_argument` is a COUNT, not a boolean - E27 Ruling 2 turned on
    `grep -c add_argument` returning 9 rather than `argparse is present`."""
    r = IC.source_axes(write(tmp_path, "a_two.py", INVOCABLE))
    r2 = IC.source_axes(write(tmp_path, "a_one.py", SUBJECT_MODULE_LEVEL))
    assert (r["a_add_argument"], r2["a_add_argument"]) == (2, 1)


# ---------------------------------------------------------------------------
# axis B - can-fail, and the B1/B2 split is the point
# ---------------------------------------------------------------------------

def test_t41_axis_b_flags_a_hardcoded_recorded_tree_path(tmp_path):
    """The dispatch's named leg."""
    r = IC.source_axes(write(tmp_path, "b_bound.py", SUBJECT_MODULE_LEVEL))
    assert r["b1_literals"], "axis B missed a module-level recorded-tree path"
    assert any("facet_next" in s for s in r["b1_literals"])


def test_t41_axis_b_separates_module_level_from_deeper(tmp_path):
    """B1 and B2 answer different questions, and a file bound only by an
    argparse default must NOT read as a hardcoded subject constant - that is
    the distinction that separates `e10_offsurface`'s shape from a general
    tool with an unfortunate default."""
    r = IC.source_axes(write(tmp_path, "b_deep.py", SUBJECT_DEEP_ONLY))
    assert r["b1_literals"] == [], (
        "a subject inside a function body was reported as module-level")
    assert r["b2_literals"], "axis B2 missed a subject in an argparse default"


def test_t41_axis_b_ignores_a_subject_named_only_in_a_docstring(tmp_path):
    """Documentation is not binding. A file whose docstring says `run me
    against E:\\...` is not thereby bound to it."""
    r = IC.source_axes(write(tmp_path, "b_doc.py", SUBJECT_IN_DOCSTRING_ONLY))
    assert r["b1_literals"] == [] and r["b2_literals"] == []


def test_t41_axis_b_says_nothing_when_there_is_nothing(tmp_path):
    """The can-fail direction: a clean file must come back empty, or `b1`
    is firing on something other than a subject."""
    r = IC.source_axes(write(tmp_path, "b_clean.py", INVOCABLE))
    assert r["b1_literals"] == [] and r["b2_literals"] == []


def test_t41_axis_b_reports_literals_not_a_boolean(tmp_path):
    """The dispatch's requirement, kept runnable: a boolean would hide WHICH
    subject a file is bound to."""
    r = IC.source_axes(write(tmp_path, "b_lit.py", SUBJECT_MODULE_LEVEL))
    assert isinstance(r["b1_literals"], list)
    assert r["b1_literals"] == [r"E:\AI\training\facet_next\E12_prep"]


# ---------------------------------------------------------------------------
# axis C - can-fail
# ---------------------------------------------------------------------------

def test_t41_axis_c_reads_the_first_nonblank_docstring_line(tmp_path):
    r = IC.source_axes(write(tmp_path, "c_ok.py", INVOCABLE))
    assert r["docstring_line1"] == "Measure a thing, any subject."


def test_t41_axis_c_distinguishes_no_docstring_from_an_empty_one(tmp_path):
    """`None` and `""` are different facts and the census must not conflate
    them - one file has no docstring, the other has one that says nothing."""
    none_r = IC.source_axes(write(tmp_path, "c_none.py", NO_DOCSTRING))
    empty_r = IC.source_axes(write(tmp_path, "c_empty.py", '"""\n\n"""\nx = 1\n'))
    assert none_r["docstring_line1"] is None
    assert empty_r["docstring_line1"] == ""


# ---------------------------------------------------------------------------
# a file that does not parse is a FINDING, not a crash
# ---------------------------------------------------------------------------

def test_t41_a_file_that_does_not_parse_is_reported(tmp_path):
    r = IC.source_axes(write(tmp_path, "broken.py", BROKEN))
    assert r["parse_error"] and "SyntaxError" in r["parse_error"]
    assert r["invocable"] is None, (
        "a file that does not parse was scored False rather than unknown; "
        "False would put it in the same bucket as a library, which is a "
        "different fact")


# ---------------------------------------------------------------------------
# axis D / E - the naming matcher, and the GLOB question P4 turns on
# ---------------------------------------------------------------------------

def test_t41_naming_finds_a_named_module_and_misses_an_unnamed_one(tmp_path):
    root = tmp_path / "r"
    (root / "docs").mkdir(parents=True)
    write(root / "docs", "a.md", "we ran `e14_topology.py` and it crashed\n")
    write(root / "docs", "b.md", "nothing relevant here\n")
    old = IC.REPO
    try:
        IC.REPO = str(root)
        got = IC.naming_files(["docs/a.md", "docs/b.md"],
                              ["e14_topology.py", "e12_thin_curve.py"])
    finally:
        IC.REPO = old
    assert got["e14_topology.py"] == ["docs/a.md"]
    assert got["e12_thin_curve.py"] == [], (
        "the matcher reported a citation for a name that appears nowhere")


def test_t41_axis_e_a_glob_does_not_name_a_module(tmp_path):
    """THE UNIT AXIS E TURNS ON, kept runnable because it is the one most
    likely to be misread. A test that walks `tools/diagnostics/*.py` EXERCISES
    every file and NAMES none of them. Axis E asks whether an edit would be
    caught BY NAME, so a globbing test scores `false` - and if that ever
    changes, this test is where the change has to be made."""
    root = tmp_path / "r"
    (root / "tests").mkdir(parents=True)
    write(root / "tests", "test_glob.py",
          'import glob\nfor p in glob.glob("tools/diagnostics/*.py"):\n    check(p)\n')
    write(root / "tests", "test_named.py",
          'MODULES = ["e14_topology.py"]\n')
    old = IC.REPO
    try:
        IC.REPO = str(root)
        got = IC.naming_files(["tests/test_glob.py", "tests/test_named.py"],
                              ["e14_topology.py", "e12_thin_curve.py"])
    finally:
        IC.REPO = old
    assert got["e14_topology.py"] == ["tests/test_named.py"]
    assert got["e12_thin_curve.py"] == [], (
        "a globbing test was credited with naming a module it never names")


def test_t41_axis_e_takes_the_module_name_without_its_extension(tmp_path):
    """THE DEFINITION REGISTERED BEFORE MEASURING is "basename OR DOTTED MODULE
    NAME as literal text" (E28-predictions.md). The first implementation
    matched only `foo.py` and under-reported axis E by two, because tests here
    name modules both ways.

    This is the leg that would have caught that, so it fails on the one-form
    matcher and passes on the two-form one.

        SYNTHETIC NAMES ONLY, AND THAT IS LOAD-BEARING RATHER THAN TIDY. Axis E
        asks whether any file under `tests/` contains a module's name as
        literal text - and THIS FILE IS UNDER `tests/`. The first draft of this
        leg wrote a real module's basename into its fixture and moved the
        basename-only count from 44 to 45 by existing. A test must not perturb
        the measurement it verifies, so nothing below names a real member."""
    root = tmp_path / "r"
    (root / "tests").mkdir(parents=True)
    write(root / "tests", "test_ext.py", 'run("zz_alpha_probe.py")\n')
    write(root / "tests", "test_stem.py", 'INSTRUMENT = "zz_beta_probe"\n')
    old = IC.REPO
    try:
        IC.REPO = str(root)
        rels = ["tests/test_ext.py", "tests/test_stem.py"]
        by_ext = IC.naming_files(rels, ["zz_alpha_probe.py", "zz_beta_probe.py"])
        by_stem = IC.naming_files(rels, ["zz_alpha_probe", "zz_beta_probe"])
    finally:
        IC.REPO = old
    assert by_ext["zz_alpha_probe.py"] == ["tests/test_ext.py"]
    assert by_ext["zz_beta_probe.py"] == [], (
        "the fixture must NOT name the second module with its extension, or "
        "this test cannot show the one-form matcher missing it")
    assert by_stem["zz_beta_probe"] == ["tests/test_stem.py"], (
        "the extensionless form is not found, so axis E under-reports every "
        "module a test names without `.py`")


def test_t41_this_file_does_not_perturb_axis_e():
    """The self-reference, kept honest. T41 may mention a real module - the
    can-fail legs above need `e14_topology` and one `bpy` importer - but no
    member may be anchored ONLY by this file, because that would be axis E
    reporting a test that exercises nothing."""
    names = committed_members()
    tests = [t for t in IC.test_files() if "t41" not in t]
    stems = [n[:-3] for n in names]
    ext = IC.naming_files(tests, names)
    stem = IC.naming_files(tests, stems)
    without_t41 = set(n for n in names if ext[n] or stem[n[:-3]])
    all_tests = IC.test_files()
    with_t41 = set(n for n in names
                   if IC.naming_files(all_tests, [n])[n]
                   or IC.naming_files(all_tests, [n[:-3]])[n[:-3]])
    only_t41 = sorted(with_t41 - without_t41)
    assert not only_t41, (
        "%d module(s) are anchored ONLY by T41's own text: %s. Use a synthetic "
        "name in the fixture that mentions them." % (len(only_t41), only_t41))


def test_t41_the_committed_census_carries_both_axis_e_readings():
    """Both readings ride in the payload because `texel_provenance` is ALSO one
    of the spec's eight tool names - a test naming the TOOL cannot be told from
    one naming the MODULE by literal matching. Picking one silently would hide
    that; the census reports both and picks neither."""
    import json
    p = os.path.join(str(REPO), "docs", "instrument-census.json")
    if not os.path.exists(p):
        pytest.skip("no committed census yet")
    with io.open(p, encoding="utf-8") as fh:
        c = json.load(fh)
    assert "anchored" in c["totals"]
    assert "anchored_basename_only" in c["totals"]
    assert c["totals"]["anchored"] >= c["totals"]["anchored_basename_only"], (
        "the either-form reading cannot be smaller than the basename-only one")
    for row in c["rows"]:
        assert "anchored_in_basename_only" in row


def test_t41_axis_d_excludes_the_census_s_own_output():
    """THE CIRCULARITY LEG. `docs/instrument-census.md` tabulates all 99
    filenames and lives under `docs/`, so it is inside `record_markdown()`'s
    set. Left in, axis D reads 99/99 on every run after the first - measured:
    76 before the output existed, 99 after. A headline number that flips to
    100% on a second invocation is not a number.

    If this fires, axis D has started counting the census as evidence about
    its own subject."""
    assert "docs/instrument-census.md" in IC.SELF_OUTPUTS
    corpus = IC.corpus_files()
    if "docs/instrument-census.md" not in corpus:
        pytest.skip("the census output has not been generated in this tree")
    kept = [r for r in corpus if not IC.is_self_document(r)]
    assert "docs/instrument-census.md" not in kept
    assert len(kept) < len(corpus)


def test_t41_axis_d_excludes_the_arc_s_own_papers_and_it_matters():
    """THE GATE THAT FIRED, kept runnable. A document ABOUT the census names
    the files the census found, so committing this arc's report made every one
    of the 99 "cited" - 76 before it existed, 99 after, 51 rows drifted.

    This asserts the contamination is REAL rather than theoretical: leaving the
    arc's papers in must credit strictly more files than excluding them. If it
    ever stops mattering, this leg says so instead of quietly passing."""
    names, _ = IC.members()          # diagnostics alone suffices: the report
    corpus = IC.corpus_files()       # names its files, which is the point
    arc_docs = [r for r in corpus if r.startswith(IC.SELF_DOC_PREFIXES)]
    if not arc_docs:
        pytest.skip("this arc's documents are not in the corpus yet")
    clean = IC.naming_files([r for r in corpus
                             if not IC.is_self_document(r)], names)
    dirty = IC.naming_files([r for r in corpus
                             if r not in IC.SELF_OUTPUTS], names)
    n_clean = sum(1 for n in names if clean[n])
    n_dirty = sum(1 for n in names if dirty[n])
    assert n_dirty > n_clean, (
        "leaving this arc's own papers in axis D credits no extra file "
        "(%d vs %d), so either the report stopped naming what it found or the "
        "exclusion is watching the wrong set" % (n_dirty, n_clean))


def test_t41_axis_d_is_idempotent_across_runs():
    """The committed census must report the same axis-D count that a fresh
    read of the corpus produces - i.e. re-running does not inflate it."""
    import json
    p = os.path.join(str(REPO), "docs", "instrument-census.json")
    if not os.path.exists(p):
        pytest.skip("no committed census yet")
    with io.open(p, encoding="utf-8") as fh:
        c = json.load(fh)
    names = committed_members()
    corpus = [r for r in IC.corpus_files() if not IC.is_self_document(r)]
    fresh = IC.naming_files(corpus, names)
    committed = dict((r["file"], r["cited_count"]) for r in c["rows"])
    drift = sorted(n for n in names if len(fresh[n]) != committed.get(n))
    assert not drift, (
        "%d file(s) have an axis-D count that no longer reproduces; re-run "
        "`python tools/instrument_census.py --committed`: %s"
        % (len(drift), drift[:10]))


# ---------------------------------------------------------------------------
# axis F - the E27 Ruling 5 leg: n/a, never a silent false
# ---------------------------------------------------------------------------

def test_t41_axis_f_returns_na_for_a_bpy_importer_not_false(tmp_path):
    """The dispatch's named leg, and the law it carries: a module whose import
    needs `bpy` tells you about the ENVIRONMENT, not about the module. Scoring
    it `false` would put an unmeasurable file in the same bucket as a measured
    failure."""
    p = write(tmp_path, "f_bpy.py", BPY_IMPORTER)
    row = IC.source_axes(p)
    f, reason, modes = IC.axis_f(row, sys.executable, p, 90, False)
    assert f == "n/a", "a bpy importer scored %r rather than n/a" % f
    assert "bpy" in reason, reason
    assert modes, "the per-mode verdicts were dropped, so the reason is unreadable"


def test_t41_axis_f_returns_na_for_a_file_with_no_cli(tmp_path):
    """A module with no `--help` has no `--help` to exit 0. Scoring it `false`
    would make the whole axis a restatement of axis A."""
    p = write(tmp_path, "f_lib.py", LIBRARY)
    row = IC.source_axes(p)
    f, reason, modes = IC.axis_f(row, sys.executable, p, 90, False)
    assert f == "n/a" and "no flag surface" in reason, reason
    assert modes == {}, "a file with no flag surface was spawned anyway"


def test_t41_axis_f_never_spawns_a_file_without_a_main_guard(tmp_path):
    """THE SAFETY PROPERTY, and it is the reason axis F is gated on axis A.
    `python <file> --help` runs the module body before argparse sees anything,
    so probing an unguarded file would EXECUTE it - against whatever subject
    its constants name. The recorded trees are not in git.

    The synthetic file here writes a sentinel at module level. If the census
    ever spawns it, the sentinel appears."""
    sentinel = tmp_path / "IT_RAN"
    body = ('import argparse\n'
            'open(%r, "w").write("x")\n'
            'ap = argparse.ArgumentParser()\n'
            'ap.add_argument("--glb")\n' % str(sentinel))
    p = write(tmp_path, "f_unguarded.py", body)
    row = IC.source_axes(p)
    assert row["invocable"] is False
    assert row["flag_surface"] is True, (
        "the fixture must HAVE a flag surface, or this test proves only that "
        "files without argparse are skipped - which is a different fact")
    f, reason, _m = IC.axis_f(row, sys.executable, p, 90, False)
    assert f == "n/a" and "__main__" in reason, reason
    assert not sentinel.exists(), (
        "the census EXECUTED a module that has no __main__ guard; that is the "
        "failure this gate exists for")


def test_t41_axis_f_says_true_for_a_clean_invocable_file(tmp_path):
    """The can-fail leg's other half: if this returned n/a or false too, the
    axis would be incapable of a positive and every count from it meaningless."""
    p = write(tmp_path, "f_ok.py", INVOCABLE)
    row = IC.source_axes(p)
    f, reason, modes = IC.axis_f(row, sys.executable, p, 90, False)
    assert f == "true", "clean file scored %r (%s) %r" % (f, reason, modes)
    assert set(modes.values()) == {"clean"}


def test_t41_axis_f_says_false_when_help_writes_to_stderr(tmp_path):
    """`--help` exiting 0 is not enough - a module that natters on stderr is
    not clean, and this is the leg that separates `false` from `n/a`."""
    p = write(tmp_path, "f_noisy.py", NOISY_HELP)
    row = IC.source_axes(p)
    f, reason, modes = IC.axis_f(row, sys.executable, p, 90, False)
    assert f == "false", "a stderr-writing file scored %r" % f
    assert set(modes.values()) == {"stderr"}


def test_t41_axis_f_probes_all_three_interpreter_modes(tmp_path):
    """Three modes, named, because `-O` and `PYTHONOPTIMIZE=1` are what delete
    a bare `assert` and this repo converted 278 sites on exactly that fact."""
    p = write(tmp_path, "f_modes.py", INVOCABLE)
    row = IC.source_axes(p)
    _f, _r, modes = IC.axis_f(row, sys.executable, p, 90, False)
    assert sorted(modes) == sorted(["normal", "-O", "PYTHONOPTIMIZE=1"])


def test_t41_the_optimize_modes_are_actually_different(tmp_path):
    """Guard against the check-that-cannot-fail: if `-O` and
    `PYTHONOPTIMIZE=1` did not actually strip asserts, all three columns would
    agree trivially forever and the axis would be one probe wearing three
    names."""
    body = ('import argparse\n'
            'import sys\n'
            'def main():\n'
            '    assert False, "an assert the optimizer deletes"\n'
            'if __name__ == "__main__":\n'
            '    try:\n'
            '        main()\n'
            '    except AssertionError:\n'
            '        sys.stderr.write("fired\\n")\n'
            '        sys.exit(3)\n')
    p = write(tmp_path, "f_assert.py", body)
    out = {}
    for name, flags, opt in IC.MODES:
        env = dict(os.environ)
        env.pop("PYTHONOPTIMIZE", None)
        if opt is not None:
            env["PYTHONOPTIMIZE"] = opt
        r = subprocess.run([sys.executable] + flags + [p], capture_output=True,
                           env=env, timeout=90)
        out[name] = r.returncode
    assert out["normal"] == 3, out
    assert out["-O"] == 0 and out["PYTHONOPTIMIZE=1"] == 0, (
        "the optimize modes did not strip the assert, so axis F's three "
        "columns are not measuring three things: %r" % (out,))


# ---------------------------------------------------------------------------
# axis G - a judgment, and it may not default
# ---------------------------------------------------------------------------

def test_t41_axis_g_values_are_the_declared_set():
    assert set(IC.SPEC_TOOLS) <= set(IC.G_VALUES)
    for extra in ("none", "ambiguous", "no opinion"):
        assert extra in IC.G_VALUES
    assert len(IC.SPEC_TOOLS) == 8, (
        "the spec names eight job-shaped tools; axis G maps against that set")


def committed_members():
    """Every member across the homes the committed outputs cover."""
    out = []
    for dir_rel in IC.COMMITTED_DIRS:
        names, _others = IC.members(dir_rel)
        out.extend(names)
    return sorted(out)


def test_t41_every_member_has_an_axis_g_judgment():
    """A missing judgment must not become a silent `none`. A table of confident
    `none`s reads as a measurement and is not one. Covers BOTH homes since
    2-pre - a verify/ file without a judgment fails here exactly as a
    diagnostics one does."""
    names = committed_members()
    missing = [n for n in names if n not in IC.G_PROPOSAL]
    assert not missing, (
        "%d file(s) have no axis-G entry: %s. Judge them, or write "
        "'no opinion' - which is a real value here, and is the honest one when "
        "the docstring does not settle it."
        % (len(missing), ", ".join(missing[:10])))


def test_t41_axis_g_entries_are_all_legal_values():
    bad = sorted(set(v for v in IC.G_PROPOSAL.values() if v not in IC.G_VALUES))
    assert not bad, "axis G carries values outside the declared set: %s" % bad


def test_t41_axis_g_entries_all_name_a_real_member():
    """A judgment about a file that no longer exists is a dead entry that would
    quietly stop being checked."""
    names = committed_members()
    orphans = sorted(set(IC.G_PROPOSAL) - set(names))
    assert not orphans, (
        "axis G judges files that are not in the population: %s" % orphans)


def test_t41_the_census_refuses_when_a_judgment_is_missing(monkeypatch):
    """The ANDON is a `raise`, not a bare assert - `python -O` deletes an
    assert and this repo converted 278 sites on that fact (E21 Ruling 2)."""
    names, _others = IC.members()
    short = dict(IC.G_PROPOSAL)
    short.pop(names[0], None)
    monkeypatch.setattr(IC, "G_PROPOSAL", short)
    with pytest.raises(RuntimeError) as e:
        IC.build(sys.executable, 5, True, progress=False)
    assert "ANDON" in str(e.value) and names[0] in str(e.value)


# ---------------------------------------------------------------------------
# the committed outputs agree with the instrument
# ---------------------------------------------------------------------------

def test_t41_the_committed_json_matches_the_population():
    """The outputs are derived; a stale one is a fifth surface to drift. This
    checks the cheap invariant - that the committed census counted the
    directories that are there now, and covers exactly the committed homes:
    a partial re-emit (diagnostics only, the CLI default) must fail here
    rather than land silently."""
    import json
    p = os.path.join(str(REPO), "docs", "instrument-census.json")
    assert os.path.exists(p), "the census output is missing: %s" % p
    with io.open(p, encoding="utf-8") as fh:
        c = json.load(fh)
    covered = sorted(d["dir"] for d in c["population"]["dirs"])
    assert covered == sorted(IC.COMMITTED_DIRS), (
        "docs/instrument-census.json covers %r; the committed homes are %r. "
        "Re-emit with `python tools/instrument_census.py --committed`."
        % (covered, sorted(IC.COMMITTED_DIRS)))
    names = committed_members()
    assert c["population"]["py_files_total"] == len(names), (
        "docs/instrument-census.json counted %d files; the homes hold "
        "%d. Re-run `python tools/instrument_census.py --committed`."
        % (c["population"]["py_files_total"], len(names)))
    assert sorted(r["file"] for r in c["rows"]) == names, (
        "the committed census's row set is not the homes' file set")
