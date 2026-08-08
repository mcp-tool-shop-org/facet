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
