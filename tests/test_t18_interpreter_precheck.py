"""T18 - the interpreter pre-check refuses in one line instead of seven FAILs.

Source: E17 Ruling 2 - the ruling seat's own verification miss, owned in
place. Its first suite run returned 7 failed / 20 passed under a shell that
resolved bare `python` to an interpreter without open3d, against the repo's
own environment law; the first hypothesis (an ambient-encoding delta) was
stated, tested and FALSIFIED before the ModuleNotFoundError in T3's own
failure text named the true mechanism.

The trap is closed at `conftest.pytest_sessionstart`. This test runs the trap
itself: a child pytest under a PYTHONPATH whose `open3d` raises on import -
the same failure shape as an absent one - must exit with ONE refusal naming
the law and the module, having run NOTHING.

Recursion is bounded deliberately: the child is scoped with `-k t03`, so if
the hook ever regresses the child runs two fast tests and stops rather than
re-entering this file.
"""
import os
import re
import subprocess
import sys

import pytest

from conftest import (REPO, REQUIRED_CHILD_MODULES, interpreter_refusal,
                      probe_child_modules)


def test_t18_probe_passes_on_this_interpreter():
    """The session running at all is half the proof; this states it."""
    assert probe_child_modules(sys.executable) == ()


def test_t18_probe_detects_an_absent_module():
    """The probe's can-fail proof: it must report a name that cannot import."""
    absent = "open3d_absent_e17_probe_check"
    assert probe_child_modules(sys.executable, [absent]) == (absent,)
    # and it must not invent misses among the real ones
    assert probe_child_modules(sys.executable, ["json"]) == ()


def test_t18_refusal_names_the_law_and_the_module():
    msg = interpreter_refusal(r"C:\some\other\python.exe", ["open3d"])
    assert "ANDON" in msg
    assert "open3d" in msg
    assert r"C:\some\other\python.exe" in msg          # what you ran
    assert "trellis2-env" in msg                        # what to run instead
    assert "E17 Ruling 2" in msg                        # where it was ruled


def test_t18_wrong_interpreter_refuses_once_and_runs_nothing(tmp_path):
    poison = tmp_path / "poison" / "open3d"
    poison.mkdir(parents=True)
    (poison / "__init__.py").write_text(
        'raise ImportError("T18 test: simulated unavailable open3d")\n',
        encoding="utf-8")
    env = os.environ.copy()
    env["PYTHONPATH"] = (str(poison.parent) + os.pathsep
                         + env.get("PYTHONPATH", ""))
    p = subprocess.run(
        [sys.executable, "-m", "pytest", "-k", "t03", "-p", "no:cacheprovider"],
        cwd=str(REPO), env=env, capture_output=True, timeout=900)
    out = (p.stdout + p.stderr).decode("utf-8", errors="replace")

    assert p.returncode == int(pytest.ExitCode.USAGE_ERROR), (
        "wrong-interpreter run exited %d, expected USAGE_ERROR\n%s"
        % (p.returncode, out))
    assert "ANDON" in out and "open3d" in out and "E17 Ruling 2" in out, (
        "the refusal does not name the module and the ruling:\n%s" % out)
    assert "trellis2-env" in out, "the refusal does not name the fix:\n%s" % out

    # THE POINT: nothing ran. Before T18 this exact invocation produced test
    # failures with import tracebacks; the refusal precedes collection.
    #
    # Checked STRUCTURALLY, on pytest's own report lines, not by substring:
    # the refusal message itself quotes "7 failed / 20 passed", so a naive
    # `" passed" not in out` fires on the message it is meant to accept. The
    # first cut of this test did exactly that. pytest.ini runs -rA, so a
    # session that executed anything emits PASSED/FAILED lines and a summary
    # bar; both must be absent.
    reported = [ln for ln in out.splitlines()
                if re.match(r"^(PASSED|FAILED|ERROR|SKIPPED)\b", ln.strip())]
    assert not reported, (
        "the wrong-interpreter run still executed tests:\n%s" % "\n".join(reported))
    assert "collected" not in out, "the run reached collection:\n%s" % out
    assert not re.search(r"=+\s+\d+\s+(passed|failed)", out), (
        "the run produced a pytest summary bar:\n%s" % out)


def test_t18_required_set_is_not_silently_empty():
    """A pre-check over an empty module list cannot fail - guard the guard."""
    assert "open3d" in REQUIRED_CHILD_MODULES
    assert len(REQUIRED_CHILD_MODULES) >= 5
    # E18: tools/record_mcp.py imports `mcp` at module level, so T22's stdio
    # subprocess is the same trap class the ruling closed for open3d.
    assert "mcp" in REQUIRED_CHILD_MODULES
