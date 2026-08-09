"""T61 - the frozen binary cannot run an instrument, and nothing in the source
says so (E31 task 4).

WHAT WAS MEASURED, AND WHERE IT LIVES. E31 built a PyInstaller one-file binary
carrying `measure_mcp`, both instrument directories and all five third-party
dependencies: 162,962,583 bytes on win-x64, well inside GitHub's 2 GB asset
cap. `--print-tools` exits 0 and lists eight tools. A MEASUREMENT VERB does
not run, and the failure names its own mechanism:

    facet-measure.exe: error: unrecognized arguments:
      C:\\Users\\...\\Temp\\tools\\verify\\mesh_stats.py --glb ...

Two facts collide there. `run_instrument` spawns
`[sys.executable, tool_path(rel)]`, and inside a one-file build
`sys.executable` IS THE BINARY - so the server re-invokes its own argparse
with a script path as an argument, and the instrument never runs. And
`REPO = dirname(HERE)` in a frozen build is the extraction directory's parent,
which is why the path says `Temp\\tools\\`: the same defect `FROZEN` exists to
handle at `record_mcp.py:110`, on a module that never received it.

    Size was never the blocker. `bin/facet.js:18` reasons that the 2 GB cap
    "does not apply to a package whose dependencies are stdlib, sqlite3 and
    mcp"; shipping the measurement server voids that SENTENCE while leaving
    its CONCLUSION standing, and the thing that actually stops the binary
    route is the subprocess model, not the bytes.

WHY THIS FILE IS PINS AND NOT THE MEASUREMENT. Building a 163 MB binary takes
minutes and 600 MB of dependencies; CI cannot run it on every push, and a test
that skips on the gate that fires every push is the defect's own shape (E24
Ruling 3). So the harness pins the two SOURCE FACTS that produce the measured
failure, and the report carries the measurement. Both pins are AST walks, not
source-string matches: E24 Ruling 4 ruled that a string match survives nothing
- rename a variable and it fails on correct code, keep the string and it
passes on broken code.

Everything printed here is ASCII (the repo's law).
"""
import ast
import os

from conftest import TOOLS


def tree_of(name):
    with open(str(TOOLS / name), encoding="utf-8") as fh:
        return ast.parse(fh.read())


def assigns_from_sys_frozen(tree):
    """Does this module read `sys.frozen` anywhere - the runtime question a
    frozen build has to answer."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr == "frozen":
            return True
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "getattr" and len(node.args) >= 2
                and isinstance(node.args[1], ast.Constant)
                and node.args[1].value == "frozen"):
            return True
    return False


def _argv_head(node):
    """The first element of an argv expression.

    The real call is `[sys.executable, tool_path(rel)] + [str(a) for a in args]`
    - a BinOp, not a List - so a walker that only accepts `ast.List` misses the
    exact site it exists to find. Measured while writing this file: it did.
    """
    while isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        node = node.left
    if isinstance(node, ast.List) and node.elts:
        return node.elts[0]
    return None


def subprocess_argv0_is_sys_executable(tree):
    """Find a subprocess call whose argv list starts with `sys.executable`."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else \
            getattr(func, "id", None)
        if name not in ("run", "Popen", "check_call", "check_output"):
            continue
        head = _argv_head(node.args[0]) if node.args else None
        if (isinstance(head, ast.Attribute) and head.attr == "executable"
                and isinstance(head.value, ast.Name) and head.value.id == "sys"):
            return True
    return False


# ---------------------------------------------------------------------------
# the can-fail legs, on SYNTHETIC source
# ---------------------------------------------------------------------------

def test_t61_the_walkers_can_return_false():
    """THE CAN-FAIL LEG. Both walkers must miss on source that does not carry
    the property, or the pins below prove nothing."""
    plain = ast.parse("import subprocess, sys\n"
                      "subprocess.run(['echo', 'hi'])\n")
    assert subprocess_argv0_is_sys_executable(plain) is False
    assert assigns_from_sys_frozen(plain) is False

    loaded = ast.parse("import subprocess, sys\n"
                       "F = bool(getattr(sys, 'frozen', False))\n"
                       "subprocess.run([sys.executable, 'x.py'])\n")
    assert subprocess_argv0_is_sys_executable(loaded) is True
    assert assigns_from_sys_frozen(loaded) is True

    # the REAL shape - a concatenation, not a bare list. Written out because
    # the first version of the walker accepted only ast.List and returned
    # False on the one call site in this repo that it exists to find.
    concat = ast.parse("import subprocess, sys\n"
                       "subprocess.run([sys.executable, p] + [str(a) "
                       "for a in args])\n")
    assert subprocess_argv0_is_sys_executable(concat) is True
    other = ast.parse("import subprocess\n"
                      "subprocess.run(['python', p] + list(args))\n")
    assert subprocess_argv0_is_sys_executable(other) is False


# ---------------------------------------------------------------------------
# the two source facts behind the measured failure
# ---------------------------------------------------------------------------

def test_t61_the_measurement_server_spawns_sys_executable():
    """Fact one. Every instrument runs as a subprocess of `sys.executable`,
    which is the right thing under a real interpreter (it pins the environment
    law's one python) and is the binary itself under a one-file build."""
    assert subprocess_argv0_is_sys_executable(tree_of("measure_mcp.py")), (
        "measure_mcp no longer spawns sys.executable - the frozen-runtime "
        "finding in the E31 report describes a mechanism that has changed")


def test_t61_the_measurement_server_has_no_frozen_branch():
    """Fact two, and the asymmetry is the finding. `record_mcp` reads
    `sys.frozen` because INSTALLING THE PUBLISHED 0.1.0 BINARY and reading its
    own banner is how the extraction-directory defect was found. `measure_mcp`
    was written later, carries the same `dirname(HERE)` expression, and asks
    the question nowhere.

    When a ruling addresses the binary route, this test fails and is rewritten
    in that commit - which is the only way a pin on an absence can work.
    """
    assert assigns_from_sys_frozen(tree_of("record_mcp.py")), (
        "record_mcp stopped reading sys.frozen; T28 pins that branch and this "
        "leg's contrast has lost its other half")
    assert not assigns_from_sys_frozen(tree_of("measure_mcp.py")), (
        "measure_mcp now reads sys.frozen - the frozen route may have been "
        "addressed; re-run the binary measurement in the E31 report before "
        "trusting either claim")


def test_t61_the_binary_route_states_a_precondition_that_names_its_deps():
    """`bin/facet.js` carries the binary route's premise in writing, and the
    premise is about DEPENDENCIES. This leg does not judge it - it asserts the
    sentence is still the one the E31 report quotes, so a ruling that voids it
    has to edit the file rather than let a report drift away from it."""
    from conftest import REPO
    js = (REPO / "bin" / "facet.js").read_text(encoding="utf-8")
    assert "stdlib, sqlite3 and mcp" in js, (
        "bin/facet.js no longer states its dependency premise; E31's finding "
        "about voiding it needs re-anchoring")
    assert "2GB" in js or "2 GB" in js, (
        "the asset cap the premise reasons about is no longer named at the "
        "site that reasons about it")


def test_t61_release_workflow_still_builds_only_the_record_server():
    """The binary that exists today carries `record_mcp` and nothing else, so
    none of the above is reachable by a user yet. Pinned because the day the
    workflow's entry point changes is the day the measured failure ships."""
    from conftest import REPO
    wf = (REPO / ".github" / "workflows" / "release.yml").read_text(
        encoding="utf-8")
    assert "tools/record_mcp.py" in wf
    assert "tools/measure_mcp.py" not in wf, (
        "release.yml now freezes the measurement server; E31 measured that "
        "binary answering --print-tools and failing every measurement verb")
    assert os.path.exists(str(TOOLS / "measure_mcp.py"))
