"""T29 - the operator contract of the two PUBLISHED console scripts (E21).

`facet-index` and `facet-mcp` are what `pip install facet-mcp` puts on a PATH.
This file pins what an operator gets back from them: an exit code per outcome
class, and a failure that names its next step instead of a traceback.

WHY SUBPROCESS AND NOT IMPORT. The dispatch's words - "asserted on the installed
console scripts or a subprocess, not by reading source". An exit code is a
property of a process, and `main()` returning 2 is not the same claim as the
command exiting 2: setuptools' generated console-script wrapper is what turns
one into the other, and the contract wrapper had to move INTO main() for exactly
that reason. A test that imported and called main() would pass with the contract
sitting uselessly in the `if __name__` block.

EVERY CODE HERE HAS A CAN-FAIL LEG. The repo's most-repeated defect is a check
that cannot fail (a silhouette IoU that returned 1.00000 on a holed mesh; an
erosion probe compared against its own dilation). So each assertion below is
paired with a row that must produce a DIFFERENT number: `test_..._discriminates`
runs the ok-class and the failure-class through the same helper and asserts they
disagree. If the tool started exiting the same value for everything, the pairs
break, not just the halves.

WHAT THIS FILE DELIBERATELY DOES NOT PIN. Two outcome classes were E21's open
questions when it was written:

  * what a fired ANDON exits (question 1)
  * what a failing `verify` leg exits (question 2)

So this file asserts of those only that the gate still fires and still refuses
(E08 Amendment 32), and that a failing verify still reports its failures and
does not report success. It does NOT assert their integers, because pinning an
unruled number would anchor it.

BOTH ARE NOW RULED - E21 Ruling 4 gave them one shared code, `EXIT_REFUSED`, and
E22 carried it. The integers are pinned in tests/test_t30, which is also where
the -O legs live. Nothing here changed: these `!= OK` assertions were correct
before the ruling and stay correct after it, and leaving them alone keeps a
second, weaker witness to the same behaviour that does not depend on the
constant's value.

Everything printed here is ASCII (the repo's law).
"""
import os
import shutil
import sqlite3
import subprocess
import sys

import pytest

from conftest import REPO, tool

IDX = tool("facet_index.py")
MCP = tool("record_mcp.py")

TRACEBACK_MARK = "Traceback (most recent call last)"

# The contract's own numbers, read from the module rather than retyped, so a
# constant rename cannot leave this file quietly asserting stale integers.
sys.path.insert(0, str(REPO / "tools")) if str(REPO / "tools") not in sys.path else None
import facet_index                                            # noqa: E402

OK = facet_index.EXIT_OK
USER = facet_index.EXIT_USER
RUNTIME = facet_index.EXIT_RUNTIME


def run(script, args, env_extra=None, timeout=1800):
    """One command, one process, decoded explicitly. Returns (rc, out, err)."""
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    p = subprocess.run([sys.executable, script] + [str(a) for a in args],
                       cwd=str(REPO), env=env, capture_output=True,
                       timeout=timeout)
    return (p.returncode,
            p.stdout.decode("utf-8", "replace"),
            p.stderr.decode("utf-8", "replace"))


@pytest.fixture(scope="module")
def corrupt_db(tmp_path_factory):
    """A file that is not a database - the cheapest genuine RUNTIME error."""
    p = tmp_path_factory.mktemp("t29") / "corrupt.db"
    p.write_bytes(b"this is not a sqlite database\n" * 64)
    return p


# ---------------------------------------------------------------------------
# 0 - the ok class
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("script,args", [
    (IDX, ["--help"]),
    (MCP, ["--help"]),
    (MCP, ["--print-tools"]),
])
def test_t29_ok_paths_exit_zero(script, args):
    rc, out, err = run(script, args)
    assert rc == OK, "%s %s exited %d\n%s%s" % (script, args, rc, out, err)


def test_t29_help_exits_zero_not_the_user_error_code(built_db):
    """--help reaches the operator through argparse's exit(0), NOT error().

    The contract overrides error() and deliberately leaves exit() alone; if a
    future change overrode exit() instead, help would start reporting failure.
    """
    for script in (IDX, MCP):
        rc, out, _ = run(script, ["--help"])
        assert rc == OK, "%s --help exited %d" % (script, rc)
        assert "usage:" in out


def test_t29_a_passing_verify_and_claims_exit_zero(built_db):
    rc_v, out_v, err_v = run(IDX, ["verify", "--db", built_db])
    assert rc_v == OK, "verify exited %d:\n%s\n%s" % (rc_v, out_v, err_v)
    rc_c, out_c, _ = run(IDX, ["claims", "--db", built_db])
    assert rc_c == OK, "claims exited %d:\n%s" % (rc_c, out_c)


# ---------------------------------------------------------------------------
# 1 - the user-error class (was argparse's 2 before E21)
# ---------------------------------------------------------------------------

USER_ROWS = [
    (IDX, ["bogus-verb"], "an unknown verb"),
    (IDX, [], "no arguments at all"),
    (IDX, ["--bogus-flag", "q", "x"], "an unrecognised flag"),
    (IDX, ["q", "--limit", "not-an-int", "x"], "a non-integer for --limit"),
    (MCP, ["--bogus-flag"], "an unrecognised flag"),
    (MCP, ["--db"], "a flag missing its value"),
    (MCP, ["serve"], "a stray positional"),
]


@pytest.mark.parametrize("script,args,why", USER_ROWS,
                         ids=[r[2].replace(" ", "-") for r in USER_ROWS])
def test_t29_argparse_user_errors_exit_one(script, args, why):
    """argparse's own convention is 2. The registry says 1 = user error."""
    rc, out, err = run(script, args)
    assert rc == USER, (
        "%s with %s (%s) exited %d, want %d\n%s" % (script, args, why, rc, USER, err))
    assert "usage:" in err, "a usage error must print usage:\n%s" % err
    assert TRACEBACK_MARK not in err


def test_t29_a_hand_rolled_user_error_uses_the_same_code(built_db):
    """`q` with no term is a user error the parser cannot express as a rule.

    Before E21 it returned a hardcoded 2, matching argparse by hand. It has to
    move with argparse, or the two halves of the same class disagree.
    """
    rc, out, err = run(IDX, ["q", "--db", built_db])
    assert rc == USER, "q with no term exited %d, want %d" % (rc, USER)
    assert "q needs a term" in err
    assert "hint:" in err, "every refusal names the next step:\n%s" % err
    assert TRACEBACK_MARK not in err


def test_t29_the_user_code_discriminates(built_db):
    """CAN-FAIL LEG: the same verb, one legal call and one illegal one.

    If `q` started exiting 1 for everything - or 0 for everything - this fails.
    A code asserted only on its failing row proves nothing about the code.
    """
    rc_ok, _, _ = run(IDX, ["q", "--db", built_db, "clay"])
    rc_bad, _, _ = run(IDX, ["q", "--db", built_db])
    assert rc_ok == OK
    assert rc_bad == USER
    assert rc_ok != rc_bad


# ---------------------------------------------------------------------------
# 2 - the runtime-error class (was CPython's uncaught-exception 1 before E21)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("verb", ["q", "verify", "claims"])
def test_t29_runtime_errors_exit_two_with_no_traceback(corrupt_db, verb):
    args = [verb, "--db", str(corrupt_db)] + (["clay"] if verb == "q" else [])
    rc, out, err = run(IDX, args)
    assert rc == RUNTIME, "%s on a corrupt DB exited %d, want %d\n%s" % (
        verb, rc, RUNTIME, err)
    assert TRACEBACK_MARK not in err, (
        "a raw traceback reached the operator without --debug:\n%s" % err)
    assert "RUNTIME_ERROR" in err
    for field in ("message:", "cause:", "hint:"):
        assert field in err, "the structured failure has no %s\n%s" % (field, err)


def test_t29_the_runtime_code_discriminates(built_db, corrupt_db):
    """CAN-FAIL LEG: the identical verb over a good DB and a corrupt one."""
    rc_ok, _, _ = run(IDX, ["q", "--db", built_db, "clay"])
    rc_bad, _, _ = run(IDX, ["q", "--db", str(corrupt_db), "clay"])
    assert rc_ok == OK
    assert rc_bad == RUNTIME
    assert rc_ok != rc_bad


def test_t29_user_and_runtime_are_different_codes(built_db, corrupt_db):
    """CAN-FAIL LEG for the whole registry: the three live classes are three
    distinct integers. Before E21 the user class and the runtime class were
    2 and 1 - separate, but INVERTED against the registry - and a test that
    only asserted 'they differ' would have passed on the broken surface. So
    this asserts the identities as well as the difference."""
    rc_ok, _, _ = run(IDX, ["q", "--db", built_db, "clay"])
    rc_user, _, _ = run(IDX, ["q", "--db", built_db])
    rc_run, _, _ = run(IDX, ["q", "--db", str(corrupt_db), "clay"])
    assert (rc_ok, rc_user, rc_run) == (OK, USER, RUNTIME), (
        "the three live outcome classes are (%d, %d, %d), want (%d, %d, %d)"
        % (rc_ok, rc_user, rc_run, OK, USER, RUNTIME))
    assert len({rc_ok, rc_user, rc_run}) == 3


# ---------------------------------------------------------------------------
# 3 - partial success: DECLARED AND UNUSED
# ---------------------------------------------------------------------------

def test_t29_the_partial_code_is_declared_and_never_returned(built_db,
                                                             corrupt_db):
    """E21 measured no partial-completion path in either command, so 3 is
    reserved rather than populated. This pins the reservation: if a future
    change starts returning 3, it must arrive with the path that justifies it
    and with this test updated to describe it."""
    assert facet_index.EXIT_PARTIAL == 3
    rows = [
        (IDX, ["--help"]), (IDX, ["bogus-verb"]), (IDX, []),
        (IDX, ["q", "--db", built_db]), (IDX, ["q", "--db", built_db, "clay"]),
        (IDX, ["q", "--db", str(corrupt_db), "clay"]),
        (IDX, ["claims", "--db", built_db]),
        (MCP, ["--help"]), (MCP, ["--print-tools"]), (MCP, ["--bogus-flag"]),
    ]
    seen = {}
    for script, args in rows:
        rc, _, _ = run(script, args)
        seen.setdefault(rc, (script, args))
    assert facet_index.EXIT_PARTIAL not in seen, (
        "something returned the reserved partial-success code: %s"
        % (seen.get(facet_index.EXIT_PARTIAL),))
    # the sweep must have exercised more than one class, or its silence is empty
    assert len(seen) >= 3, "the sweep only produced %s" % sorted(seen)


# ---------------------------------------------------------------------------
# --debug changes presentation and NOTHING else
# ---------------------------------------------------------------------------

def test_t29_debug_adds_the_traceback_and_moves_no_exit_code(corrupt_db):
    plain_rc, plain_out, plain_err = run(IDX, ["q", "--db", str(corrupt_db), "x"])
    dbg_rc, dbg_out, dbg_err = run(
        IDX, ["q", "--db", str(corrupt_db), "x", "--debug"])
    assert plain_rc == dbg_rc == RUNTIME, (
        "--debug moved the exit code: %d -> %d" % (plain_rc, dbg_rc))
    assert TRACEBACK_MARK not in plain_err
    assert TRACEBACK_MARK in dbg_err, (
        "--debug printed no traceback:\n%s" % dbg_err)
    assert "RUNTIME_ERROR" in plain_err and "RUNTIME_ERROR" in dbg_err


def test_t29_debug_changes_no_side_effect(tmp_path):
    """Same command twice, once with --debug, byte-compared on what it WROTE.

    A presentation flag that altered the artifact would be a different change
    wearing a presentation flag's name. The DB is compared as bytes because the
    build is byte-deterministic by contract (leg 1) - here the bytes ARE the
    claim, which is the narrow case where a hash is the right instrument.
    """
    a = tmp_path / "plain.db"
    b = tmp_path / "debug.db"
    rc_a, _, _ = run(IDX, ["build", "--db", str(a)])
    rc_b, _, _ = run(IDX, ["build", "--db", str(b), "--debug"])
    assert rc_a == rc_b == OK
    assert a.read_bytes() == b.read_bytes(), (
        "--debug changed the artifact the build wrote")


def _shared_contract_source():
    """The source file that holds the exit-code contract both commands run on.

    RESOLVED FROM THE IMPORT, never spelled as a path. `record_index` is a
    dependency: on the rig it is an editable checkout and in CI it is a wheel
    under site-packages, so any literal path would be right in one place and
    wrong in the other. Asking the module where it lives is the only form that
    is true in both, and it also fails loudly if the package ever ships without
    source.
    """
    import pathlib

    from record_index import cli as pkg_cli

    p = pathlib.Path(pkg_cli.__file__)
    assert p.suffix == ".py" and p.is_file(), (
        "record_index.cli has no readable .py source at %s - a source scan "
        "cannot answer this question against a compiled-only install" % p)
    return p


def _functions_reading(path, ident):
    """Every top-level function whose body reads the name `ident`.

    Parsed rather than grepped, so a mention inside a docstring or a comment
    does not count as a read - the claim is about what the CODE consults.
    """
    import ast
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out = set()
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for sub in ast.walk(node):
            if isinstance(sub, ast.Name) and sub.id == ident:
                out.add(node.name)
            elif isinstance(sub, ast.Attribute) and sub.attr == ident:
                out.add(node.name)
    return out


def test_t29_debug_is_read_only_where_a_failure_is_PRINTED():
    """--debug reaches presentation and nothing else.

    Asserted on the parsed source rather than on one run's behaviour: no
    behavioural test can show that no OTHER branch consults a flag. E08
    Amendment 32 rules that a gate carries no skip flag, and the failure mode
    this closes is --debug quietly becoming one - so the check is that the
    identifier is confined to the functions that decide what gets PRINTED
    after a failure has already been decided.

    Naming the exact three is deliberate. A looser form ("no function named
    like a gate reads it") would pass on a tool where the guard itself grew a
    debug branch under some other name.

    ⚑ RE-POINTED 2026-08-11 (S02). The contract moved into `record_index.cli`
    when the index was extracted, and this scan stayed pointed at
    `tools/facet_index.py` - where it returned the EMPTY SET, which a
    confinement check reads as "perfectly confined". It went red only because
    the leg below requires the walk to find SOMETHING; without that pair this
    guard would have gone quietly green on a shim, which is worse than absent.
    The scan follows the code, and facet keeps the half that is facet's.
    """
    # `debug_requested` is NOT in this set and that is not an oversight: it
    # tests argv against the STRING "--debug" and never binds the name, so the
    # walk does not see it as a reader. The two below are the whole path from
    # the bool to the print.
    allowed = {"run_contract",      # holds the bool, passes it on
               "_report_failure"}   # decides whether a traceback is printed
    readers = _functions_reading(_shared_contract_source(), "debug")
    assert readers == allowed, (
        "--debug is read outside the presentation path: %s"
        % sorted(readers - allowed))
    # FACET'S OWN HALF, and after S02 it is the stronger statement: neither
    # published module branches on the flag AT ALL - both reach the shared
    # contract and nothing else.
    for rel in ("facet_index.py", "record_mcp.py"):
        own = _functions_reading(REPO / "tools" / rel, "debug")
        assert not own, (
            "%s branches on --debug; it must reach the shared contract and "
            "nothing else: %s" % (rel, sorted(own)))


def test_t29_the_debug_confinement_check_can_fail():
    """CAN-FAIL LEG: the parser must actually FIND readers when they exist.

    Without this, an ast walk that silently returned an empty set would make
    the guard above vacuous - the repo's most-repeated defect, in the test
    written to prevent it. It is not belt-and-braces: this is the leg that
    caught the re-point above, by refusing to call an empty set a pass.
    """
    src = _shared_contract_source()
    readers = _functions_reading(src, "debug")
    assert readers, (
        "the ast walk found no readers at all in %s - it is not looking, or "
        "the contract moved again" % src)
    unrelated = _functions_reading(src, "no_such_identifier_anywhere")
    assert unrelated == set(), "the ast walk matches names that do not exist"


# ---------------------------------------------------------------------------
# the gate still fires - the RULED half of E21 question 1
# ---------------------------------------------------------------------------

STRAY_REL = os.path.join("docs", "experiments", "E29-ZZ-t29-stray-handoff.md")
STRAY_BODY = (
    "# a file T29 writes and removes, to trip the inverse discovery guard\n"
    "\n"
    "## Session handoff 1 (2026-08-08, T29)\n"
    "\n"
    "It does not match KICKOFF_DOC_RE, so the glob cannot reach it - which is\n"
    "exactly the condition assert_no_undiscovered_handoffs asks about.\n")


@pytest.fixture
def stray_handoff():
    """A handoff header in a file the kickoff glob cannot reach.

    Written into the repo tree because the guard reads REPO directly, and
    removed in the fixture's teardown. Named E29-ZZ so a leak is obvious.
    """
    p = REPO / STRAY_REL
    assert not p.exists(), "T29's probe file is already present: %s" % p
    p.write_text(STRAY_BODY, encoding="ascii", newline="\n")
    try:
        yield p
    finally:
        if p.exists():
            p.unlink()


def test_t29_the_andon_fires_and_refuses(tmp_path, stray_handoff):
    """RULED (E08 Amendment 32): the gate refuses and there is no flag past it.

    The exit CODE is E21 question 1 and is not asserted here - only that the
    run did not succeed and that the operator was told what fired.
    """
    db = tmp_path / "andon.db"
    rc, out, err = run(IDX, ["build", "--db", str(db)])
    assert rc != OK, "the stray handoff did not stop the build (exit %d)" % rc
    body = err + out
    assert "ANDON:" in body, "the gate fired without saying so:\n%s" % body
    assert STRAY_REL.replace("\\", "/") in body.replace("\\", "/"), (
        "the refusal does not name the file that tripped it:\n%s" % body)


def test_t29_the_andon_check_can_fail(tmp_path):
    """CAN-FAIL LEG for the gate test above: with no stray file, the same
    command must SUCCEED. Without this, `assert rc != OK` would pass equally
    well on a tool that could never build at all."""
    db = tmp_path / "clean.db"
    rc, out, err = run(IDX, ["build", "--db", str(db)])
    assert rc == OK, "a clean tree failed to build (exit %d)\n%s\n%s" % (rc, out, err)
    assert "ANDON:" not in (err + out)


def test_t29_debug_does_not_skip_the_gate(tmp_path, stray_handoff):
    """The U2 trap, tested rather than asserted: --debug is presentation, so it
    must not turn a refusal into a build. E08 Amendment 32 exists because a
    construction that COULD walk past a fired gate did."""
    db = tmp_path / "andon_debug.db"
    rc, out, err = run(IDX, ["build", "--db", str(db), "--debug"])
    assert rc != OK, "--debug walked past a fired gate (exit %d)" % rc
    assert "ANDON:" in (err + out)


def test_t29_the_gate_prints_no_raw_traceback_without_debug(tmp_path,
                                                            stray_handoff):
    """A fired gate is the tool WORKING, so it gets the structured form too.

    Before E21 it arrived as a bare AssertionError traceback. What is NOT
    pinned here is the exit code it leaves behind.
    """
    db = tmp_path / "andon_plain.db"
    rc, out, err = run(IDX, ["build", "--db", str(db)])
    assert rc != OK
    assert TRACEBACK_MARK not in err, (
        "a fired gate still shows a raw traceback:\n%s" % err)
    assert "GATE_FIRED" in err, err
    dbg_rc, _, dbg_err = run(IDX, ["build", "--db", str(db), "--debug"])
    assert TRACEBACK_MARK in dbg_err, "--debug did not restore the traceback"
    assert dbg_rc == rc, "--debug moved the gate's exit code: %d -> %d" % (rc, dbg_rc)


# ---------------------------------------------------------------------------
# a failing verify - the RULED half of E21 question 2
# ---------------------------------------------------------------------------

def test_t29_a_failing_verify_refuses_legibly_and_carries_no_traceback(
        built_db, tmp_path):
    """Three rulings rows deleted from a COPY: leg 2's independent grep must
    notice, and the run must report the mismatch rather than crash.

    The exit code is E21 question 2 and is not asserted. What is asserted is
    that the verdict line says FAILED, that the failing evidence is printed,
    and that this is a measured outcome rather than a crash.
    """
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

    rc, out, err = run(IDX, ["verify", "--db", str(broken)])
    assert rc != OK, "verify passed a DB three rulings short (exit %d)" % rc
    assert "VERIFY FAILED" in out, "no FAILED verdict line:\n%s" % out[-2000:]
    assert any(ln.strip().startswith("X ") for ln in out.splitlines()), (
        "FAILED with no failing evidence printed")
    assert TRACEBACK_MARK not in err, (
        "a failed leg is a measured outcome, not a crash:\n%s" % err)


def test_t29_the_failing_verify_check_can_fail(built_db):
    """CAN-FAIL LEG: the unmodified DB must PASS the same command."""
    rc, out, err = run(IDX, ["verify", "--db", built_db])
    assert rc == OK, "the built DB failed verify (exit %d):\n%s" % (rc, out[-2000:])
    assert "VERIFY PASSED" in out
    assert "VERIFY FAILED" not in out
