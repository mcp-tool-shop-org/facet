"""T40 - the four tools that REFUSE, pinned to the state of tools/ they name.

Gate 2's shape: an instrument that cannot establish its precondition refuses
with exit code 4 and names what is missing. For these four the missing thing
is the instrument itself, and each refusal names a real file and whose
question unblocks it (the Director's open question 2, or a commission).

THE PIN IS LIVE: every path a refusal names is asserted to EXIST on disk. If
a later session wraps one of these tools - or moves the named instrument -
this test fails and the refusal text is updated consciously, in that commit,
rather than drifting into fiction (the fabricated-citation law's little
sibling: a refusal that names a file that is not there is a pointer nobody
can follow).

One stdio spawn rides at the end: the mount path itself, proven runnable.
"""
import asyncio
import os
import sys

import pytest

from conftest import REPO, TOOLS
from measure_support import MESHES, call, refusal

CASES = {
    # tool               args to provoke it            path the refusal names
    "mesh_topology": ({"glb": "unused.glb"},
                      "tools/diagnostics/e14_topology.py"),
    "thin_extent_curve": ({"glb": "unused.glb"},
                          "tools/diagnostics/e12_thin_curve.py"),
    "offsurface_rate": ({}, "tools/diagnostics/e10_offsurface.py"),
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


def test_t40_the_excluded_family_refusals_name_whose_question():
    for tool in ("mesh_topology", "thin_extent_curve"):
        err = refusal(call(tool, {"glb": "unused.glb"}))
        text = err["message"] + " " + err["hint"]
        assert "open question 2" in text, (
            "%s is blocked on the Director's open question 2 and the "
            "refusal must say so, not just point at a file" % tool)


def test_t40_mesh_topology_refusal_carries_the_measured_crash():
    err = refusal(call("mesh_topology", {"glb": "unused.glb"}))
    assert "argmin == argmax" in err["message"] + " " + err["hint"], (
        "the tie-crash was measured while this server was built (unit cube, "
        "pinch fixture); ruling the family in without knowing it is a trap")


def test_t40_offsurface_refusal_names_both_halves():
    err = refusal(call("offsurface_rate", {}))
    text = err["message"] + " " + err["hint"]
    assert "e10_offsurface" in text and "e12_offsurface" in text, (
        "the finding has two halves - the hardcoded in-scope instrument and "
        "the excluded erode/margin form - and the refusal carries both")


def test_t40_anchor_check_refusal_states_the_name_collision():
    err = refusal(call("anchor_check", {}))
    text = err["message"] + " " + err["hint"]
    assert "e13_anchor_check" in text and "NAME COLLISION" in text, (
        "the one file named anchor_check is the spiral-law guard; a reader "
        "who greps will find it and must not mistake it for the pattern")


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
