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

THE POPULATION IS NOT ALL 108 FILES, AND THAT IS THE INTERESTING PART. This
directory's house style is a STRAIGHT-LINE MODULE-LEVEL SCRIPT (E28 measured 6
of 99 corpus-wide carrying a `__main__` guard), so running most of these files
EXECUTES them, and some of them write. The runnable population is exactly the
files carrying BOTH a `__main__` guard and an argparse surface: `--help` on
one of those parses and exits without reaching any work. Measured at E31: 108
files, SEVEN runnable.

The seven are pinned BY NAME rather than by count. A new instrument with an
argparse surface joins the set that `--help` can exercise, and joining it
should be a deliberate edit here - the same discipline T34 applies to a test
count and E23 applied to its successor sites.

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

def test_t62_the_runnable_population_is_the_pinned_seven():
    rows = scan()
    got = tuple(sorted(k for k, (guard, ap) in rows.items() if guard and ap))
    assert got == tuple(sorted(RUNNABLE)), (
        "the runnable instrument set moved: %s\nA new argparse instrument is "
        "welcome; add it here in the same commit so `--help` covers it."
        % sorted(set(got) ^ set(RUNNABLE)))
    assert len(rows) >= 100, (
        "the two instrument directories hold %d files; E31 measured 108 and "
        "the point of the seven is that they are a small minority" % len(rows))


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


def test_t62_the_instrument_directories_are_not_packages_today():
    """The pre-choice state, stated. Packaging them is a shape E31 measured and
    did not adopt; if `__init__.py` appears, the packaging decision was made
    and this file's claims about the recorded invocation need re-measuring in
    that commit (E31 measured NO breakage, so the expected edit here is one
    line, not a redesign)."""
    for d in DIRS:
        assert not (TOOLS / d / "__init__.py").exists(), (
            "tools/%s is now a package - re-run T62's --help legs and the "
            "suite before trusting the invocation form" % d)


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
