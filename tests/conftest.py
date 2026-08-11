"""E17 harness fixtures (docs/experiments/E17-harness-kickoff.md).

Two tiers. The hermetic set reads only the repo and runs anywhere, including
CI. The `artifacts` set replays recorded runs from the trees under
FACET_ASSETS (default E:\\AI\\training on the rig) - those trees are NOT in
git and NOT in CI, so absence is a SKIP whose message names the exact missing
path. A silent skip is a check that cannot fail; pytest.ini's -rA keeps every
skip reason in the run summary.

All output from this file and every test is ASCII (the repo's law; E16-1 is
why it is a law). Tools are invoked at subprocess level with sys.executable -
the porting rule prefers that over restructuring tools for importability, and
texpass_iter parses argv at import so it cannot be imported at all.

Shared-copy discipline (the E17 dispatch): recorded trees are READ, never
written - every state a tool mutates is copied to scratch first, and the
replay tests re-hash their recorded inputs afterward to prove the citable
tree did not move.
"""
import importlib.util
import locale
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "tools"
ASSETS_ENV = "FACET_ASSETS"
DEFAULT_ASSETS = "E:\\AI\\training" if os.name == "nt" else "/nonexistent/facet-assets"


def tool(rel):
    return str(TOOLS / rel)


# ---------------------------------------------------------------------------
# T18 - the interpreter pre-check (E17 Ruling 2)
# ---------------------------------------------------------------------------
# The trap, measured at TWO seats on 2026-08-08: run under an interpreter
# without open3d and this suite returns "7 failed, 20 passed" with import
# tracebacks - which reads as a suite defect rather than an environment one.
# The ruling seat lost a diagnosis to it (its first hypothesis, an encoding
# delta, was stated, tested and FALSIFIED before the ModuleNotFoundError in
# T3's own failure text named the true mechanism).
#
# MEASURED, not assumed - the third-party modules this suite's tools import at
# MODULE level, so a tool cannot be invoked at all without them:
#     texpass_iter      numpy scipy PIL trimesh open3d   (T2, T3, T11)
#     project_twins     numpy scipy PIL trimesh open3d   (T10)
#     e08_ceiling       numpy         trimesh open3d     (T8)
#     e12_elevated      numpy         trimesh open3d     (T9)
#     mesh_stats        numpy scipy   trimesh            (T12)
#     texpass_finalize  numpy     PIL                    (T7)
#     record_mcp        mcp                              (T19-T22, E18)
#     facet_index, e04_registry_sweep   stdlib only      (T1, T4, T5, T13, T16)
# The stdlib-only pair is exactly why a wrong interpreter reads as a PARTIAL
# green instead of an obvious environment error - the twenty that pass are the
# ones that never needed the environment.
#
# `mcp` joined this table with the E18 server (2026-08-08), and for the same
# reason the others are here: tools/record_mcp.py imports it at MODULE level, so
# T22's stdio subprocess cannot start without it, and an interpreter missing it
# would produce the same partial-green misreading Ruling 2 closed. The pin lives
# in .github/workflows/ci.yml beside the rest.
# `cv2` joined this table with E23's T31 (2026-08-08), for exactly the reason the
# table exists. T31 is the first test in this repo's history to invoke any of the
# twelve route tools, and tools/restylize_views.py imports cv2 at MODULE level -
# so an interpreter without it produces the partial-green misreading Ruling 2
# closed, one module short. Measured over all twelve: cv2 is the ONLY third-party
# module-level import outside this table, apart from bpy and mathutils, which
# belong to the two Blender scripts nothing here runs.
# `record_index` joined this table with the S02 extraction (2026-08-11), for the
# same reason and with one difference worth naming. The index moved into its own
# package and tools/facet_index.py imports it at MODULE level, so an interpreter
# without it produces the partial-green misreading Ruling 2 closed - and the
# stdlib-only pair the table's own note calls out as the reason a wrong
# interpreter reads as a partial green is EXACTLY the pair that stops being
# stdlib-only here. The difference: this is the studio's own package rather than
# a third-party one, declared in pyproject as a RUNTIME dependency (not a test
# pin), with its CI install beside the rest in .github/workflows/ci.yml.
REQUIRED_CHILD_MODULES = ("numpy", "scipy", "PIL", "trimesh", "open3d", "mcp",
                          "cv2", "record_index")

_PROBE_SRC = (
    "import importlib, sys\n"
    "miss = []\n"
    "for m in sys.argv[1:]:\n"
    "    try:\n"
    "        importlib.import_module(m)\n"
    "    except Exception:\n"
    "        miss.append(m)\n"
    "sys.stdout.write(' '.join(miss))\n"
)


def probe_child_modules(interpreter, modules=REQUIRED_CHILD_MODULES):
    """Which of `modules` the child interpreter cannot import, in order.

    A REAL import, not importlib.util.find_spec: a present-but-broken install
    (a DLL that will not load) produces the same trap as an absent one, and
    find_spec would call it present. Measured cost on the rig: ~1.2 s once per
    session, against a 93 s suite.

    `interpreter` is sys.executable in the only caller, so it is by definition
    launchable; an OSError is still handled rather than left to surface as a
    harness crash during the check that exists to prevent confusing crashes.
    """
    try:
        p = subprocess.run([str(interpreter), "-c", _PROBE_SRC, *modules],
                           capture_output=True, timeout=600)
    except OSError:
        return tuple(modules)
    return tuple(p.stdout.decode("ascii", errors="replace").split())


def interpreter_refusal(interpreter, missing):
    """The one loud line the wrong-interpreter run gets instead of N failures."""
    return (
        "ANDON: this interpreter cannot import %s, so the tools this suite "
        "tests cannot run at all.\n"
        "  interpreter: %s\n"
        "  The repo's environment law (CLAUDE.md, Environment) names ONE python:\n"
        "    E:\\AI-Models\\trellis2-env\\Scripts\\python.exe -m pytest\n"
        "  CI installs the same modules by pin (.github/workflows/ci.yml).\n"
        "  Refusing instead of running, because a wrong interpreter does not\n"
        "  fail cleanly here: the stdlib-only tools (facet_index,\n"
        "  e04_registry_sweep) keep passing while everything that touches a\n"
        "  mesh fails with import tracebacks - 7 failed / 20 passed, measured\n"
        "  at two seats. That reads as a suite defect instead of an\n"
        "  environment one. [E17 Ruling 2]"
        % (", ".join(missing), interpreter))


def pytest_sessionstart(session):
    """Assert the child interpreter's capability ONCE, before anything runs.

    Deliberately strict - it refuses the whole session rather than only the
    tests that need a mesh library. Under a wrong interpreter every result is
    suspect: the twenty that would still pass are the ones that never exercise
    the environment, and "20 passed" is precisely the misreading this closes.
    """
    missing = probe_child_modules(sys.executable)
    if missing:
        pytest.exit(interpreter_refusal(sys.executable, missing),
                    returncode=pytest.ExitCode.USAGE_ERROR)


def run_py(script_rel, args, env_extra=None, cwd=None, timeout=3600, encoding=None):
    """Run a repo tool with the suite's own interpreter; decode output explicitly.

    Output is captured as bytes and decoded with the encoding the child
    actually wrote (PYTHONIOENCODING when forced, the locale's preferred
    encoding otherwise), errors=replace - so an encoding defect in a tool
    surfaces as a failed assertion on its output, never as a crash in the
    harness.
    """
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    # PYTHONIOENCODING may carry an ":errors" suffix ("utf-8:surrogateescape",
    # the ambient value on this rig) or even be pure-errors (":surrogateescape");
    # only the encoding half selects the decode codec here
    env_enc = env.get("PYTHONIOENCODING", "").split(":", 1)[0]
    enc = encoding or env_enc or locale.getpreferredencoding(False)
    p = subprocess.run(
        [sys.executable, tool(script_rel)] + [str(a) for a in args],
        cwd=str(cwd or REPO), env=env, capture_output=True, timeout=timeout)
    out = p.stdout.decode(enc, errors="replace")
    err = p.stderr.decode(enc, errors="replace")
    return p.returncode, out, err


def last_nonempty(text):
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
    return lines[-1] if lines else ""


def copy_state(src_dir, dst_dir, names=("atlas.png", "holes.png", "styled_mask.npy")):
    """Copy a recorded state's mutable files into scratch. The recorded tree is
    citable-only (Ruling 33's ledger); anything a tool writes runs on the copy."""
    dst_dir = Path(dst_dir)
    dst_dir.mkdir(parents=True, exist_ok=True)
    for n in names:
        shutil.copyfile(str(Path(src_dir) / n), str(dst_dir / n))
    return dst_dir


def assets_root():
    return Path(os.environ.get(ASSETS_ENV, DEFAULT_ASSETS))


@pytest.fixture(scope="session")
def assets():
    root = assets_root()
    if not root.is_dir():
        pytest.skip(
            "artifacts tier: recorded-trees root not found at %s "
            "(set %s; the trees live under E:\\AI\\training on the rig and are "
            "not in git, not in CI)" % (root, ASSETS_ENV))
    return root


def need(root, rel):
    """A specific recorded input, or a skip that names exactly what is missing."""
    p = Path(root) / rel
    if not p.exists():
        pytest.skip(
            "artifacts tier: recorded input missing: %s (%s=%s)"
            % (p, ASSETS_ENV, Path(root)))
    return p


@pytest.fixture(scope="session")
def built_db(tmp_path_factory):
    """The index built ONCE to a per-run scratch path (T1's subject; T4/T5's
    operand). Scratch --db keeps the tracked DB untouched and gives leg 1's
    det temps per-run paths, so nothing here races a live session's verify on
    the fixed docs/index/facet.db.det_a (E16 report section 2)."""
    db = tmp_path_factory.mktemp("index") / "facet.db"
    rc, out, err = run_py("facet_index.py", ["build", "--db", db])
    assert rc == 0, "index build failed (rc %d):\n%s\n%s" % (rc, out, err)
    assert db.exists(), "build exited 0 but wrote no DB at %s" % db
    return db


@pytest.fixture(scope="session")
def facet_index_mod():
    """facet_index imported in-process for the guard tests (T4/T5). Its module
    level is constants and function defs only - main() is __main__-guarded -
    so import has no side effects; measured before this fixture was written."""
    spec = importlib.util.spec_from_file_location("facet_index", tool("facet_index.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
