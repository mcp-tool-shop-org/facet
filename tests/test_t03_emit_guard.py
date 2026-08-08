"""T3 - an unprofiled `emit` refuses loudly, before it touches any input.

Source: E16-4's anchor (Ruling 29c). An unprofiled emit used to succeed at
--aspect's default 752x1024 - one subject's portrait framing, 3.1x too wide
for the prop - with nothing in the output distinguishing a right frame from a
wrong one.

Hermeticity is PROVEN, not assumed (the dispatch's own open tier call:
"hermetic if the guard fires pre-load - verify that"): --state and --prep
point at paths that do not exist, so the run can only refuse via the guard,
which sits after parse_args and before the first file open. If the guard were
downstream of input loading, this test would see FileNotFoundError instead of
the ANDON text.

The exit code alone is NOT the assertion - on CI a missing dependency would
also exit non-zero, which would make this a check that cannot fail. The
guard's own message is asserted, and a control run with an explicit --aspect
proves the message assertion can discriminate.
"""
from conftest import run_py


def test_t03_unprofiled_emit_refuses(tmp_path):
    state = tmp_path / "no_such_state"
    prep = tmp_path / "no_such_prep"
    rc, out, err = run_py(
        "texpass_iter.py", ["emit", "--state", state, "--prep", prep])
    assert rc != 0, "unprofiled emit did not refuse (rc 0)\n%s\n%s" % (out, err)
    text = out + err
    assert "ANDON" in text and "E14 Ruling 29c" in text, (
        "refusal is not the emit guard's message:\n%s" % text)
    # the message names the repair
    assert "--profile" in text and "--aspect" in text, (
        "guard message does not name the repair:\n%s" % text)
    # it refused BEFORE any output: no job dir, no state dir materialised
    assert not state.exists(), "guard fired but a state path was created"


def test_t03_control_explicit_aspect_passes_the_guard(tmp_path):
    """The can-fail proof: with --aspect explicit the guard stands down, and
    the same dummy paths now fail DOWNSTREAM (loading state) without the
    ANDON text - so the guard, not an import error, produced T3's refusal.

    HARDENED at T18, having been measured passing for the wrong reason: under
    an interpreter without open3d this control PASSED, because a
    ModuleNotFoundError satisfies both "exits non-zero" and "carries no ANDON
    text" - a check that cannot fail, sitting inside the control that exists
    to prove another check CAN. It was the eighth open3d-touching test in the
    7-failed/20-passed run and the reason that count is 7 and not 8. T18's
    session refusal makes the state unreachable; this asserts the reason
    directly as well, because the repo's rule is to fix a root cause at every
    consumer rather than only where it was noticed.
    """
    state = tmp_path / "no_such_state"
    prep = tmp_path / "no_such_prep"
    rc, out, err = run_py(
        "texpass_iter.py",
        ["emit", "--state", state, "--prep", prep, "--aspect", "752,1024"])
    assert rc != 0  # dummy paths cannot load
    text = out + err
    assert "E14 Ruling 29c" not in text, (
        "the guard fired despite an explicit --aspect - the legacy path is gone:\n%s"
        % text)
    assert "ModuleNotFoundError" not in text and "ImportError" not in text, (
        "this control passed on an import failure, not on the guard standing "
        "down - the environment cannot drive the tool (see T18):\n%s" % text)
    # it must have got far enough to fail on the ABSENT INPUTS, which is the
    # only failure that proves the guard let it through
    assert "FileNotFoundError" in text or "No such file" in text, (
        "expected a missing-input failure downstream of the guard:\n%s" % text)
