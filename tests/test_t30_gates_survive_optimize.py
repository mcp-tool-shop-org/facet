"""T30 - the gates survive -O (E22).

THE TEST THE OLD CONSTRUCTION MADE IMPOSSIBLE. Every ANDON in the write path
was a bare `assert`, and `assert` is a statement the interpreter is licensed to
delete: `python -O` and `PYTHONOPTIMIZE=1` remove it silently and execution
continues past it. E22 measured that on the pinned interpreter before repairing
it - the gate went quiet, the write proceeded, the process exited 0 - which is
strictly worse than the shell chain E08 Amendment 32 was written for, because
the shell chain at least let the ANDON print.

So this file asserts the repair: each converted gate refuses under a NORMAL
interpreter AND under `-O` AND under `PYTHONOPTIMIZE=1`, and the write-path
gates additionally leave nothing behind when they fire.

NO TEST HERE ASSERTS THAT `PYTHONOPTIMIZE=1` DISABLES A GATE. E21 refused to
pin that and it was right: such a test would anchor the defect. What IS pinned,
in `test_t30_the_optimize_legs_are_not_vacuous`, is that the stripping mechanism
is live in this interpreter - on a THROWAWAY script written by the test, never
on a facet gate. Without it, "the gate fires under -O" could pass because -O
never took effect, which is this repo's most-repeated defect: a check that
cannot fail.

WHY SUBPROCESS. `__debug__` is fixed when the interpreter starts and cannot be
toggled inside a running process, so an in-process test of this cannot exist.

Everything printed here is ASCII (the repo's law).
"""
import ast
import io
import os
import subprocess
import sys

import pytest

from conftest import REPO, tool
# D2's selftest_min staging, consumed from T26 rather than copied: one site for
# the fixture layout finalize's surface-aware path needs. T26's own read-only
# assertion is module-scoped there, so this file re-checks it below.
from test_t26_finalize_lookup import FIXTURE, _stage, _tree_hashes

sys.path.insert(0, str(REPO / "tools")) if str(REPO / "tools") not in sys.path else None
import facet_index                                            # noqa: E402

IDX = tool("facet_index.py")
FINALIZE = tool("texpass_finalize.py")

OK = facet_index.EXIT_OK
USER = facet_index.EXIT_USER
RUNTIME = facet_index.EXIT_RUNTIME
PARTIAL = facet_index.EXIT_PARTIAL
REFUSED = facet_index.EXIT_REFUSED

# The three ways E22 measured the control, and the three ways every gate below
# is fired. `id` is what a failure message names.
MODES = [
    ("normal", [], {}),
    ("dash-O", ["-O"], {}),
    ("PYTHONOPTIMIZE", [], {"PYTHONOPTIMIZE": "1"}),
]
MODE_IDS = [m[0] for m in MODES]

# the seven files E22 converted; the structural check below walks all of them
CONVERTED = ["texpass_iter.py", "texpass_finalize.py", "project_twins.py",
             "e11_manifest.py", "e11_export_turnaround.py",
             "facet_index.py", "record_mcp.py"]


def _shared_contract_source():
    """The source file holding the exit-code contract facet's gates land in.

    RESOLVED FROM THE IMPORT, never spelled as a path: on the rig
    `record_index` is an editable checkout and in CI it is a wheel under
    site-packages, so a literal would be right in exactly one of the two.
    """
    import pathlib

    from record_index import cli as pkg_cli

    p = pathlib.Path(pkg_cli.__file__)
    assert p.suffix == ".py" and p.is_file(), (
        "record_index.cli has no readable .py source at %s - a source scan "
        "cannot answer this question against a compiled-only install" % p)
    return p


def run(flags, script, args, env_extra=None, timeout=1800):
    """One command, one process, with interpreter FLAGS as well as env.

    The flags are the point: `-O` is an interpreter switch, not an env var, and
    a helper that only carried env could not test half of what E22 measured.
    """
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)
    if env_extra:
        env.update(env_extra)
    p = subprocess.run([sys.executable] + list(flags) + [script]
                       + [str(a) for a in args],
                       cwd=str(REPO), env=env, capture_output=True,
                       timeout=timeout)
    return (p.returncode,
            p.stdout.decode("utf-8", "replace"),
            p.stderr.decode("utf-8", "replace"))


@pytest.fixture(autouse=True)
def _e18_fixture_is_read_only():
    """E18's committed fixture must come back untouched, as in T26."""
    before = _tree_hashes(FIXTURE)
    yield
    assert _tree_hashes(FIXTURE) == before, (
        "a test in this file modified E18's committed fixture tree - it is "
        "consumed, never edited (E20 Ruling 2)")


# ---------------------------------------------------------------------------
# the can-fail leg that makes every -O leg below mean something
# ---------------------------------------------------------------------------

def test_t30_the_optimize_legs_are_not_vacuous(tmp_path):
    """PROOF THAT THE STRIPPING MECHANISM IS LIVE ON THIS INTERPRETER.

    On a script this test writes and throws away - never on a facet gate. A
    bare `assert` must halt under a normal interpreter and must NOT halt under
    `-O` or `PYTHONOPTIMIZE=1`. If that were untrue here, every "the gate fires
    under -O" below would be passing for the wrong reason.

    This is the opposite of anchoring the defect: it pins a property of CPython,
    on throwaway source, so that the tests of facet's own gates can be believed.
    """
    probe = tmp_path / "probe.py"
    probe.write_text(
        "import sys\n"
        "assert False, 'a bare assert the interpreter may delete'\n"
        "sys.stdout.write('WALKED PAST\\n')\n", encoding="ascii", newline="\n")

    rc, out, err = run([], str(probe), [])
    assert rc != 0 and "WALKED PAST" not in out, (
        "a bare assert did not halt a NORMAL interpreter (rc %d)\n%s%s"
        % (rc, out, err))

    for name, flags, env in MODES[1:]:
        rc, out, err = run(flags, str(probe), [], env)
        assert rc == 0 and "WALKED PAST" in out, (
            "%s did not strip a bare assert on this interpreter (rc %d) - so "
            "the -O legs in this file would be vacuous\n%s%s"
            % (name, rc, out, err))


# ---------------------------------------------------------------------------
# the write-path gates: texpass_finalize
# ---------------------------------------------------------------------------
# Each is fired by setting the tool's OWN bound below the measured value, or by
# constructing the input it exists to catch - T26's mechanisms, re-run under all
# three interpreter modes. What is new here is the mode axis, not the trip.

@pytest.mark.parametrize("mode,flags,env", MODES, ids=MODE_IDS)
def test_t30_finalize_source_distance_gate_refuses_in_every_mode(
        tmp_path, mode, flags, env):
    state, prep = _stage(tmp_path)
    out_png = tmp_path / "never.png"
    rc, o, e = run(flags, FINALIZE,
                   ["--state", state, "--prep", prep, "--out", out_png,
                    "--surface-aware", "--max-edge-median", "0.1"], env)
    assert rc != 0, "[%s] the ANDON did not halt the run (rc %d)\n%s" % (mode, rc, o)
    assert "ANDON" in e, "[%s] the gate halted without saying so:\n%s" % (mode, e)
    assert "median source distance" in e, "[%s] %s" % (mode, e)
    assert not out_png.exists(), (
        "[%s] the atlas was written after the ANDON fired - the guard must "
        "precede the irreversible step (E08 Amendment 32)" % mode)


@pytest.mark.parametrize("mode,flags,env", MODES, ids=MODE_IDS)
def test_t30_finalize_beyond_edges_gate_refuses_in_every_mode(
        tmp_path, mode, flags, env):
    state, prep = _stage(tmp_path)
    out_png = tmp_path / "never.png"
    rc, o, e = run(flags, FINALIZE,
                   ["--state", state, "--prep", prep, "--out", out_png,
                    "--surface-aware", "--beyond-edges", "0.1",
                    "--max-frac-beyond", "0.0"], env)
    assert rc != 0, "[%s] the ANDON did not halt the run (rc %d)\n%s" % (mode, rc, o)
    assert "ANDON" in e, "[%s] %s" % (mode, e)
    assert "source from beyond" in e, "[%s] %s" % (mode, e)
    assert not out_png.exists(), "[%s] the atlas was written after the ANDON" % mode


@pytest.mark.parametrize("mode,flags,env", MODES, ids=MODE_IDS)
def test_t30_finalize_uniform_atlas_gate_refuses_in_every_mode(
        tmp_path, mode, flags, env):
    """The third finalize ANDON, fired by CONSTRUCTING the input it catches
    (a single-colour atlas stays uniform through hole filling) rather than by
    moving a bound - so this leg does not depend on a tunable at all."""
    import numpy as np
    from PIL import Image

    state, prep = _stage(tmp_path)
    res = np.load(str(prep / "pos.npy")).shape[0]
    flat = np.full((res, res, 3), 0.5, dtype=np.float32)
    Image.fromarray((flat * 255).round().astype(np.uint8)).save(
        str(state / "atlas.png"))
    out_png = tmp_path / "never.png"
    rc, o, e = run(flags, FINALIZE,
                   ["--state", state, "--prep", prep, "--out", out_png,
                    "--surface-aware"], env)
    assert rc != 0, "[%s] a flat atlas passed the uniformity ANDON (rc %d)\n%s" % (
        mode, rc, o)
    assert "ANDON: final atlas uniform" in e, "[%s] %s" % (mode, e)
    assert not out_png.exists(), "[%s] the atlas was written after the ANDON" % mode


@pytest.mark.parametrize("mode,flags,env", MODES, ids=MODE_IDS)
def test_t30_finalize_clean_run_is_silent_in_every_mode(tmp_path, mode, flags, env):
    """CAN-FAIL LEG for the three above: inside the bounds the same command in
    the same mode must SUCCEED and write. Without this, `rc != 0` would pass
    equally well on a tool that could not run at all under -O."""
    state, prep = _stage(tmp_path)
    out_png = tmp_path / "clean.png"
    rc, o, e = run(flags, FINALIZE,
                   ["--state", state, "--prep", prep, "--out", out_png,
                    "--surface-aware"], env)
    assert rc == 0, "[%s] a clean run failed (rc %d)\n%s\n%s" % (mode, rc, o, e)
    assert "ANDON" not in e, "[%s] a clean run fired a gate:\n%s" % (mode, e)
    assert out_png.exists(), "[%s] a clean run wrote no atlas" % mode


# ---------------------------------------------------------------------------
# the shipped command's gate: facet_index's inverse discovery guard
# ---------------------------------------------------------------------------

STRAY_REL = os.path.join("docs", "experiments", "E30-ZZ-t30-stray-handoff.md")
STRAY_BODY = (
    "# a file T30 writes and removes, to trip the inverse discovery guard\n"
    "\n"
    "## Session handoff 1 (2026-08-08, T30)\n"
    "\n"
    "It matches neither KICKOFF_DOC_RE nor RULING_DOC_RE, so the glob cannot\n"
    "reach it - exactly the condition assert_no_undiscovered_handoffs asks\n"
    "about. Named E30-ZZ, distinct from T29's probe, so the two cannot\n"
    "collide in one session and a leak is obvious.\n")


@pytest.fixture
def stray_handoff():
    p = REPO / STRAY_REL
    assert not p.exists(), "T30's probe file is already present: %s" % p
    p.write_text(STRAY_BODY, encoding="ascii", newline="\n")
    try:
        yield p
    finally:
        if p.exists():
            p.unlink()


@pytest.mark.parametrize("mode,flags,env", MODES, ids=MODE_IDS)
def test_t30_index_discovery_gate_refuses_in_every_mode(
        tmp_path, stray_handoff, mode, flags, env):
    """The one gate in a PUBLISHED console script. Before E22 this was the
    `assert` at facet_index.py:343 and `PYTHONOPTIMIZE=1` deleted it: the build
    completed and wrote a DB missing a dispatch. Now it refuses in all three."""
    db = tmp_path / "andon.db"
    rc, out, err = run(flags, IDX, ["build", "--db", str(db)], env)
    assert rc == REFUSED, (
        "[%s] the stray handoff exited %d, want %d\n%s%s" % (mode, rc, REFUSED,
                                                            out, err))
    body = err + out
    assert "ANDON:" in body, "[%s] the gate fired without saying so:\n%s" % (mode, body)
    assert "GATE_FIRED" in err, "[%s] %s" % (mode, err)
    assert STRAY_REL.replace("\\", "/") in body.replace("\\", "/"), (
        "[%s] the refusal does not name the file that tripped it:\n%s" % (mode, body))


@pytest.mark.parametrize("mode,flags,env", MODES, ids=MODE_IDS)
def test_t30_index_discovery_gate_can_fail_in_every_mode(tmp_path, mode, flags, env):
    """CAN-FAIL LEG: with no stray file the same command in the same mode must
    build and exit 0."""
    db = tmp_path / "clean.db"
    rc, out, err = run(flags, IDX, ["build", "--db", str(db)], env)
    assert rc == OK, "[%s] a clean tree failed to build (exit %d)\n%s\n%s" % (
        mode, rc, out, err)
    assert "ANDON:" not in (err + out)


# ---------------------------------------------------------------------------
# 4 = REFUSED (E21 Ruling 4), carried by E22
# ---------------------------------------------------------------------------

def test_t30_a_failing_verify_exits_refused(built_db, tmp_path):
    """The most important signal either command produces, off the code it used
    to share with a mistyped flag. Fixture: three rulings rows deleted from a
    COPY, as T29 does - leg 2's independent grep must notice."""
    import shutil
    import sqlite3

    broken = tmp_path / "broken.db"
    shutil.copyfile(str(built_db), str(broken))
    con = sqlite3.connect(str(broken))
    before = con.execute("select count(*) from rulings").fetchone()[0]
    con.execute("delete from rulings where (arc, number, kind) in "
                "(select arc, number, kind from rulings "
                " order by arc, number, kind limit 3)")
    con.commit()
    after = con.execute("select count(*) from rulings").fetchone()[0]
    con.close()
    assert before - after == 3, "the fixture did not remove three rows"

    rc, out, err = run([], IDX, ["verify", "--db", str(broken)])
    assert rc == REFUSED, "a failing verify exited %d, want %d\n%s" % (
        rc, REFUSED, out[-1500:])
    assert "VERIFY FAILED" in out


def test_t30_the_refused_code_discriminates(built_db, tmp_path):
    """CAN-FAIL LEG and the discrimination pair in one: the same command on an
    intact DB must exit OK, and REFUSED must be a code no other outcome class
    of these two commands returns."""
    rc_ok, out, _ = run([], IDX, ["verify", "--db", built_db])
    assert rc_ok == OK, "the built DB failed verify (%d):\n%s" % (rc_ok, out[-1500:])
    assert rc_ok != REFUSED
    assert REFUSED not in (OK, USER, RUNTIME, PARTIAL), (
        "REFUSED collides with another declared code: %d in %s"
        % (REFUSED, (OK, USER, RUNTIME, PARTIAL)))


def test_t30_the_certificate_field_and_the_fixture_agree_with_the_tool():
    """E21 F3: `verify()`'s value is persisted as the certificate's
    `verify_exit_code`, and tests/mcp_support.py carried it as a hardcoded 1
    that nothing compared against a live run. Both now read the tool's own
    constant, so they cannot drift from it again."""
    from mcp_support import FAILED_PARSE, PASSED_PARSE
    assert FAILED_PARSE["exit_code"] == REFUSED
    assert PASSED_PARSE["exit_code"] == OK
    assert FAILED_PARSE["exit_code"] != PASSED_PARSE["exit_code"]


# ---------------------------------------------------------------------------
# the structural pin: a gate is never a bare `assert`
# ---------------------------------------------------------------------------

def _andon_asserts(src):
    """Every `assert` statement whose own source carries the ANDON token."""
    tree = ast.parse(src)
    return [n for n in ast.walk(tree)
            if isinstance(n, ast.Assert)
            and "ANDON" in (ast.get_source_segment(src, n) or "")]


def test_t30_no_converted_file_still_gates_with_an_assert():
    """THE NEW STANDING LAW (E21 Ruling 2), pinned where it can be checked:
    a gate is never a bare `assert`, because `-O` deletes one silently.

    Scope is the seven files E22 converted. The ~190 ANDON-carrying asserts
    that E22 MEASURED elsewhere in tools/ are a reported finding and are
    deliberately not pinned here - pinning a class this arc did not convert
    would fail on work nobody has done yet.
    """
    offenders = []
    for rel in CONVERTED:
        src = io.open(tool(rel), encoding="utf-8").read()
        for n in _andon_asserts(src):
            offenders.append("%s:%d" % (rel, n.lineno))
    assert not offenders, (
        "%d ANDON gate(s) are still bare asserts, which -O deletes:\n  %s"
        % (len(offenders), "\n  ".join(offenders)))


def test_t30_the_structural_check_can_fail():
    """CAN-FAIL LEG: the walk above must find an ANDON assert when one exists,
    or its silence over seven files means nothing."""
    planted = ("def f(x):\n"
               "    assert x > 0, 'ANDON: planted by the can-fail leg'\n")
    found = _andon_asserts(planted)
    assert len(found) == 1, "the walk missed a planted ANDON assert"
    assert not _andon_asserts("def f(x):\n    assert x > 0, 'ordinary'\n"), (
        "the walk flags an assert that carries no ANDON token")


def test_t30_the_andon_exception_types_are_the_ones_e22_measured():
    """The exception TYPE is load-bearing, not cosmetic - and there are TWO.

    The 86 gates E22 converted raise `AssertionError`, and that is a
    requirement rather than a preference: facet_index.run_contract catches
    `AssertionError` specifically and routes it to the fired-gate branch, so
    anything else would arrive as a generic runtime error with a different
    message and a different code.

    THREE ANDONs were ALREADY raises before E22 and they use `SystemExit` -
    one each in project_twins, e11_manifest and e11_export_turnaround. E22 did
    NOT touch them: a pure move does not include unifying an exception type
    nobody ruled, and `raise SystemExit` is not deletable by -O either, so
    they are not the defect this arc exists to fix. That an ANDON has two types
    in this repo is a REPORTED FINDING, not something this test decides.

    Both populations are pinned, so a change to either is visible.

    ⚑ `facet_index.py` WENT FROM 1 TO 0 ON 2026-08-11, AND THAT IS A MOVE
    RATHER THAN A DELETION. S02 extracted the index to the `record-index`
    package, and the single ANDON here - the inverse discovery guard - went
    with it: it is `record_index/parse.py`'s
    `assert_no_undiscovered_handoffs`, pinned at exactly one `AssertionError`
    by `record-index tests/test_gates_and_writes.py::
    test_the_andon_exception_type_census_is_the_one_measured`.

    THE EVIDENCE THAT IT STILL FIRES IS ALREADY IN THIS FILE and is stronger
    than a second census would be: `test_t30_index_discovery_gate_refuses_in_
    every_mode` plants a stray handoff, runs `facet_index.py build` as a
    subprocess under a normal interpreter, `-O` and `PYTHONOPTIMIZE=1`, and
    requires exit 4 with the ANDON text naming the file - in all three modes.
    A structural count that dropped to 0 while that leg stayed green is the
    gate having moved house, not having gone quiet. If it HAD gone quiet, those
    three legs go red first and this one is the footnote.

    The other six rows are facet's own tools and are unmoved.
    """
    got = {}
    for rel in CONVERTED:
        src = io.open(tool(rel), encoding="utf-8").read()
        tree = ast.parse(src)
        per = {}
        for n in ast.walk(tree):
            if not isinstance(n, ast.Raise):
                continue
            seg = ast.get_source_segment(src, n) or ""
            if "ANDON" not in seg:
                continue
            exc = n.exc
            name = None
            if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name):
                name = exc.func.id
            elif isinstance(exc, ast.Name):
                name = exc.id
            per[name] = per.get(name, 0) + 1
        got[rel] = per
    # MEASURED after conversion, and against HEAD before it. The AssertionError
    # column was 86 converted + facet_index's guard; the SystemExit column is
    # the three that were raises already and is BYTE-UNCHANGED by E22.
    # RE-MEASURED 2026-08-11 after S02: facet_index's guard moved to
    # record_index/parse.py, so this file's row is now empty - see the docstring.
    want = {
        "texpass_iter.py": {"AssertionError": 8},
        "texpass_finalize.py": {"AssertionError": 4},
        "project_twins.py": {"AssertionError": 15, "SystemExit": 1},
        "e11_manifest.py": {"AssertionError": 35, "SystemExit": 1},
        "e11_export_turnaround.py": {"AssertionError": 24, "SystemExit": 1},
        "facet_index.py": {},
        "record_mcp.py": {},
    }
    assert got == want, (
        "the ANDON exception-type census moved:\n  measured %s\n  committed %s"
        % (got, want))


def test_t30_run_contract_still_keys_on_assertionerror():
    """The other half of the pair above, and the reason it matters. If this
    handler were ever narrowed or renamed, the type check would be guarding
    nothing.

    ⚑ RE-POINTED 2026-08-11 (S02) at `record_index.cli`, which is where
    `run_contract` lives now. It is kept here rather than left to the package's
    own copy of this test because the five files above are FACET'S tools: their
    ANDONs raise `AssertionError` and reach an operator through this handler, so
    a narrowing there turns every one of facet's own fired gates into a generic
    runtime error with the wrong exit code. The property is the package's; the
    exposure is facet's, and this is the leg that watches it from facet's side.
    """
    src = _shared_contract_source().read_text(encoding="utf-8")
    tree = ast.parse(src)
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "run_contract")
    caught = []
    for h in ast.walk(fn):
        if isinstance(h, ast.ExceptHandler) and isinstance(h.type, ast.Name):
            caught.append(h.type.id)
    assert "AssertionError" in caught, (
        "run_contract no longer catches AssertionError; it catches %s" % caught)
    assert caught.index("AssertionError") < caught.index("Exception"), (
        "the AssertionError handler must precede the broad one or a fired gate "
        "is reported as a runtime error: %s" % caught)


def test_t30_the_conversion_left_no_orphan_message():
    """A pure move keeps the message. Every ANDON message that HEAD~ carried in
    the seven files must still be present, byte for byte, in the file that
    carries it - checked by hashing the set of message literals.

    This is what "no message improved in passing" looks like as a check rather
    than as a promise. It compares the working tree against the ORIGINAL commit
    of each file only through the messages' own text, so it survives future
    edits that add gates while catching one that quietly reworded a message.
    """
    got = {}
    for rel in CONVERTED:
        src = io.open(tool(rel), encoding="utf-8").read()
        tree = ast.parse(src)
        msgs = []
        for n in ast.walk(tree):
            node = None
            if isinstance(n, ast.Assert) and n.msg is not None:
                node = n.msg
            elif isinstance(n, ast.Raise) and isinstance(n.exc, ast.Call) \
                    and n.exc.args:
                node = n.exc.args[0]
            if node is None:
                continue
            seg = ast.get_source_segment(src, node) or ""
            if "ANDON" in seg:
                msgs.append(" ".join(seg.split()))
        got[rel] = len(msgs)
    # MEASURED after conversion, not predicted: 86 converted gates plus the 3
    # ANDONs that were already raises (one each in project_twins, e11_manifest,
    # e11_export_turnaround). record_mcp's single in-scope assert carries no
    # ANDON token, so its count is 0 and that is correct rather than a miss.
    # A change here means a gate was added, removed or reworded, and the report
    # has to say which.
    # RE-MEASURED 2026-08-11: facet_index 1 -> 0, the same single guard the type
    # census above records as having MOVED to record_index/parse.py rather than
    # having been deleted. Its message went with it and is still the one that
    # reaches an operator - the three subprocess legs above read it out of a
    # real refusal in all three interpreter modes.
    want = {"texpass_iter.py": 8, "texpass_finalize.py": 4,
            "project_twins.py": 16, "e11_manifest.py": 36,
            "e11_export_turnaround.py": 25, "facet_index.py": 0,
            "record_mcp.py": 0}
    assert got == want, (
        "the ANDON message population moved:\n  measured %s\n  committed %s"
        % (got, want))
