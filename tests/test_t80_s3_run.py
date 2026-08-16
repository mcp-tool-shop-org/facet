"""T80 - s3_run glue. Hermetic: refuse a missing bundle, no bare assert.

The real AOV tree is not in git. Loading it is the advisor's fold, or a
demonstration. This file only pins that a missing --aov is exit 4, not a
traceback, and that the module has no -O-deletable gates.
"""
import ast
import os

from conftest import REPO, run_py


def test_t80_missing_aov_exits_four(tmp_path):
    missing = str(tmp_path / "no_such_aov")
    rc, out, err = run_py(
        "s3_run.py",
        ["--aov", missing, "--out", str(tmp_path / "out")])
    assert rc == 4, "missing aov exited %d (want 4)\n%s\n%s" % (rc, out, err)
    assert "does not exist" in err, err


def test_t80_no_andon_is_a_bare_assert():
    src = open(os.path.join(str(REPO), "tools", "s3_run.py"),
               encoding="utf-8").read()
    tree = ast.parse(src)
    bares = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    assert bares == [], "bare assert at lines %s" % bares
