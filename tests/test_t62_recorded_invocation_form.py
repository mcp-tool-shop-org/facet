"""T62 - `python tools/<name>.py` still runs, which is what packaging the
instruments would have to preserve (E31 task 3 / P5).

WHAT IS AT STAKE. `pyproject.toml:43-47` states the reason the two modules
ship as `py-modules` rather than as a package: making `tools/` a package would
rewrite the `python tools/<name>.py` invocation that every recorded command in
this record cites, and those commands are citable evidence. E31 measured
whether packaging the two instrument directories actually breaks that. It does
not - adding `__init__.py` changes nothing about `sys.path[0]`, which is the
script's own directory either way - but "it does not" is only worth having if
something keeps checking.

THE POPULATION IS NOT ALL OF THE FILES, AND THAT IS THE INTERESTING PART. This
directory's house style is a STRAIGHT-LINE MODULE-LEVEL SCRIPT (E28 measured 6
of 99 corpus-wide carrying a `__main__` guard), so running most of these files
EXECUTES them, and some of them write. The runnable population is exactly the
files carrying BOTH a `__main__` guard and an argparse surface: `--help` on
one of those parses and exits without reaching any work. Measured at E31: 108
files, SEVEN runnable. E32 added two invocable tools, so the set is now NINE
of 110 - still the small minority the assertion below checks for.

They are pinned BY NAME rather than by count. A new instrument with an
argparse surface joins the set that `--help` can exercise, and joining it
should be a deliberate edit here - the same discipline T34 applies to a test
count and E23 applied to its successor sites. E32 is the first arc to make
that edit, and it made it in the commit that added the instruments.

Everything printed here is ASCII (the repo's law).
"""
import ast
import os
import subprocess
import sys

import pytest

from conftest import REPO, TOOLS

DIRS = ("diagnostics", "verify")

# MEASURED at E31 over tools/diagnostics + tools/verify: the files that carry
# BOTH a __main__ guard and an argparse import, so `--help` is safe to run.
RUNNABLE = (
    "diagnostics/e10_claim_replay.py",
    "diagnostics/e10_consumers_subject.py",
    "diagnostics/e10_offsurface.py",
    "diagnostics/e10_offsurface_consumers.py",
    "diagnostics/e10_offsurface_where.py",
    # E32: both new tools carry a __main__ guard AND an argparse surface, so
    # `--help` parses and exits without reaching any work. Joining the set is a
    # deliberate edit here, exactly as this file's docstring requires.
    "diagnostics/e32_plate_geometry.py",
    "diagnostics/e32_route_preprocess.py",
    # E33: same form - a __main__ guard and an argparse surface, so `--help` parses and
    # exits before any file is opened. Named here on purpose, not swept in.
    "diagnostics/e33_register_sheet.py",
    "verify/anchor_compare.py",
    "verify/gate_mesh.py",
)


def has_main_guard(tree):
    for node in tree.body:
        if isinstance(node, ast.If):
            t = node.test
            if (isinstance(t, ast.Compare) and isinstance(t.left, ast.Name)
                    and t.left.id == "__name__"):
                return True
    return False


def uses_argparse(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(a.name == "argparse"
                                                for a in node.names):
            return True
        if isinstance(node, ast.ImportFrom) and node.module == "argparse":
            return True
    return False


def scan():
    """Every .py under the two instrument directories, with the two properties
    that decide whether `--help` may be run against it."""
    rows = {}
    for d in DIRS:
        base = TOOLS / d
        for name in sorted(os.listdir(str(base))):
            if not name.endswith(".py"):
                continue
            with open(str(base / name), encoding="utf-8") as fh:
                tree = ast.parse(fh.read())
            rows["%s/%s" % (d, name)] = (has_main_guard(tree),
                                         uses_argparse(tree))
    return rows


# ---------------------------------------------------------------------------
# the can-fail leg, on SYNTHETIC source
# ---------------------------------------------------------------------------

def test_t62_the_property_scanner_can_return_false(tmp_path):
    """THE CAN-FAIL LEG. Both properties must be missable, or the seven below
    are a list rather than a measurement."""
    plain = ast.parse("import os\nprint(os.name)\n")
    assert has_main_guard(plain) is False
    assert uses_argparse(plain) is False
    full = ast.parse("import argparse\n"
                     "if __name__ == '__main__':\n    pass\n")
    assert has_main_guard(full) is True
    assert uses_argparse(full) is True


# ---------------------------------------------------------------------------
# the population, and the invocation form itself
# ---------------------------------------------------------------------------

def test_t62_the_runnable_population_is_the_pinned_set():
    rows = scan()
    got = tuple(sorted(k for k, (guard, ap) in rows.items() if guard and ap))
    assert got == tuple(sorted(RUNNABLE)), (
        "the runnable instrument set moved: %s\nA new argparse instrument is "
        "welcome; add it here in the same commit so `--help` covers it."
        % sorted(set(got) ^ set(RUNNABLE)))
    assert len(rows) >= 100, (
        "the two instrument directories hold %d files; E31 measured 108 and the "
        "point of the runnable set is that it is a small minority" % len(rows))


@pytest.mark.parametrize("rel", RUNNABLE)
def test_t62_the_recorded_invocation_form_still_answers(rel):
    """`python tools/<name>.py --help` from the repo root - the exact shape
    every recorded command in this record uses. Exit 0, and a usage line."""
    p = subprocess.run(
        [sys.executable, os.path.join("tools", rel.replace("/", os.sep)),
         "--help"],
        cwd=str(REPO), capture_output=True, timeout=300)
    out = p.stdout.decode("utf-8", "replace")
    assert p.returncode == 0, (
        "python tools/%s --help exited %d\n%s"
        % (rel, p.returncode, p.stderr.decode("utf-8", "replace")[-600:]))
    assert "usage" in out.lower(), out[:300]


def test_t62_the_instrument_directories_need_no_init_py():
    """⚑ THE ASSERTION IS UNCHANGED AND ITS REASON IS REWRITTEN, 2026-08-09.

    This test used to hold the PRE-PACKAGING state and said: *if `__init__.py`
    appears, the packaging decision was made and this file's claims need
    re-measuring in that commit.* The decision was made - E31 Ruling 6 adopted
    Shape A at the Director's word that facet-measure ships - and re-measuring
    is why the assertion survives it: **packaging these directories does not
    require the file.**

    Measured on clean builds both ways: with `packages = ["diagnostics",
    "verify"]` in pyproject, setuptools ships every `.py` in each directory -
    99 and 9 - with or without a marker, and an installed `mesh_stats` runs
    from a clean venv either way (786,432 faces on the box control). Nothing
    ever IMPORTS these directories: `tool_path` builds a filesystem path and
    the server spawns the instrument as a SUBPROCESS, so package-ness is not
    a property the route needs.

    And adding them was not merely unnecessary - it FIRED A GATE. The census
    keys axes D/E/G on the filename, so an `__init__.py` in both homes would
    merge two files' evidence, and `instrument_census.py` halted with exactly
    that ANDON when the two files were briefly in the tree. Keeping them out
    keeps the census's population at 99 + 9 (T41) and its keying sound.
    """
    for d in DIRS:
        assert not (TOOLS / d / "__init__.py").exists(), (
            "tools/%s/__init__.py exists. Packaging does not need it (measured "
            "both ways), it grows the census population, and it collides with "
            "the census's filename keying - `__init__.py` in both homes fires "
            "that instrument's duplicate-basename ANDON." % d)


def test_t62_every_instrument_file_compiles():
    """The cheap check that nothing in either directory is syntactically
    broken - the failure mode a packaging change could plausibly introduce by
    shadowing a name, and the one that would otherwise surface as an
    INSTRUMENT_FAILED with a traceback in a user's hint field."""
    for d in DIRS:
        p = subprocess.run(
            [sys.executable, "-m", "compileall", "-q", str(TOOLS / d)],
            capture_output=True, timeout=900)
        assert p.returncode == 0, (
            "compileall failed under tools/%s:\n%s"
            % (d, p.stdout.decode("utf-8", "replace")[-800:]))
