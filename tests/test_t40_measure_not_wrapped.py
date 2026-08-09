"""T40 - the tool that REFUSES, pinned to the state of tools/ it names.

Gate 2's shape: a tool that cannot establish its precondition refuses with
exit code 4 and names what is missing. AT E27 FOUR TOOLS REFUSED HERE; at E28
task 2b three of them began serving (the Director ruled the e12_*/e14_* family
in, the census halt was ruled, and the tie crash was repaired with its proof
in T42), so THIS PIN MOVED DELIBERATELY IN THAT COMMIT - the dispatch's own
words: T40 moving is correct and deliberate; it is not a test being weakened.
The three wraps are tested at their served surface in T43/T44/T45.

What remains is `anchor_check`, and its refusal is still live and still
pinned: the census swept BOTH instrument homes (99 diagnostics + 8 verify
files, E28) and found no candidate - the five nearest files are all judged
`ambiguous` and none is the anchored-regression pattern. The commission
stands, unscoped, not this arc's.

THE PIN IS LIVE: every path the refusal names is asserted to EXIST on disk.
If a later session builds anchor_check's instrument - or moves the named
collision file - this test fails and the refusal text is updated consciously,
in that commit, rather than drifting into fiction.

One stdio spawn rides at the end: the mount path itself, proven runnable.
"""
import asyncio
import os
import sys

import pytest

from conftest import REPO, TOOLS
from measure_support import MESHES, call, refusal

CASES = {
    # tool           args to provoke it   path the refusal names
    "anchor_check": ({}, "tools/diagnostics/e13_anchor_check.py"),
}


@pytest.mark.parametrize("tool", sorted(CASES))
def test_t40_refuses_with_exit_4_naming_a_real_instrument(tool):
    args, named = CASES[tool]
    err = refusal(call(tool, args))
    assert err["code"] == "NOT_WRAPPED"
    assert err["exit_code"] == 4
    text = err["message"] + " " + err["hint"]
    assert named.rsplit("/", 1)[-1] in text, (
        "%s's refusal must name %s" % (tool, named))
    assert os.path.exists(os.path.join(str(REPO),
                                       named.replace("/", os.sep))), (
        "the refusal names %s and that file is GONE - update the refusal "
        "text with whatever moved it" % named)


def test_t40_anchor_check_refusal_states_the_name_collision():
    err = refusal(call("anchor_check", {}))
    text = err["message"] + " " + err["hint"]
    assert "e13_anchor_check" in text and "NAME COLLISION" in text, (
        "the one file named anchor_check is the spiral-law guard; a reader "
        "who greps will find it and must not mistake it for the pattern")


def test_t40_the_formerly_refusing_three_now_serve():
    """The deliberate other half of this pin's move: the three tools that
    refused at E27 must NOT refuse with NOT_WRAPPED any more. Each is asked
    with arguments whose failure mode is a PRECONDITION (a missing file), so
    a NOT_WRAPPED here would mean a refusal handler quietly came back."""
    for tool, args in (("mesh_topology", {"glb": "no-such.glb"}),
                       ("thin_extent_curve", {"glb": "no-such.glb"}),
                       ("offsurface_rate", {"prep": "no-such-dir"})):
        err = refusal(call(tool, args))
        assert err["code"] == "PRECONDITION_MISSING", (
            "%s should serve (and refuse this call only for its missing "
            "input); got %s - if NOT_WRAPPED, the E28 wrap regressed"
            % (tool, err["code"]))


def test_t40_the_wrapped_registry_matches_the_surface():
    """WRAPPED is the printable claim about who serves; the served handlers
    are the fact. One entry per spec name, exactly one None left."""
    import measure_support
    W = measure_support.measure_mcp.WRAPPED
    assert sorted(W) == sorted(measure_support.measure_mcp.TOOL_ORDER)
    unserved = sorted(k for k, v in W.items() if v is None)
    assert unserved == ["anchor_check"], (
        "the refusing set is %r; this pin says exactly anchor_check refuses. "
        "Moving it is deliberate - update T40 and the module docstring in "
        "the same commit." % unserved)
    for tool, rel in W.items():
        if rel is None:
            continue
        assert os.path.exists(os.path.join(str(REPO),
                                           rel.replace("/", os.sep))), (
            "%s claims to wrap %s, which does not exist" % (tool, rel))


@pytest.mark.slow
def test_t40_stdio_subprocess_serves_the_surface():
    """The mount path, end to end (T22's pattern): the entry point spawned
    and driven over stdio, one live measurement through the literal wire."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    async def go():
        params = StdioServerParameters(
            command=sys.executable,
            args=[str(TOOLS / "measure_mcp.py")],
            env=dict(os.environ), cwd=str(REPO))
        async with stdio_client(params) as (r, w):
            async with ClientSession(r, w) as s:
                init = await s.initialize()
                tools = await s.list_tools()
                stats = await s.call_tool(
                    "mesh_stats",
                    {"glb": os.path.join(MESHES, "cube.glb")})
                return init, tools, stats

    init, tools, stats = asyncio.run(go())
    assert init.server_info.name == "facet-measure"
    assert len(tools.tools) == 8
    assert not stats.is_error
    import json
    doc = json.loads(stats.content[0].text)
    assert doc["mesh"]["components"] == 1
