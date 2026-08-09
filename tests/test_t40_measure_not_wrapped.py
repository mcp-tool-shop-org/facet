"""T40 - the serving registry, pinned; NOT_WRAPPED has no live site.

Gate 2's shape: a tool that cannot establish its precondition refuses with
exit code 4 and names what is missing. AT E27 FOUR TOOLS REFUSED HERE with
NOT_WRAPPED; at E28 task 2b three began serving (the Director ruled the
e12_*/e14_* family in, the census halt was ruled, the tie crash was repaired
with its proof in T42), and at 2c the fourth followed (Ruling 10 commissioned
anchor_compare at the Director's word, compare-only). THIS PIN HAS NOW MOVED
TWICE, DELIBERATELY, in those commits - the dispatch's own words: T40 moving
is correct and deliberate; it is not a test being weakened. The wraps are
tested at their served surfaces in T43/T44/T45/T46.

What this file pins now: the WRAPPED registry serves ALL EIGHT names with a
real file behind each; the four former refusers fail on PRECONDITION, never
NOT_WRAPPED; and the e13_anchor_check NAME COLLISION - which lived in the old
refusal text - is carried in the served tool's notes (E27 Ruling 4), where
T46 asserts it.

One stdio spawn rides at the end: the mount path itself, proven runnable.
"""
import asyncio
import os
import sys

import pytest

from conftest import REPO, TOOLS
from measure_support import MESHES, call, refusal


def test_t40_the_formerly_refusing_four_now_serve():
    """The deliberate half of this pin's two moves: every tool that refused
    with NOT_WRAPPED at E27 must now fail a bad call on its PRECONDITION - a
    NOT_WRAPPED here would mean a refusal handler quietly came back."""
    for tool, args in (("mesh_topology", {"glb": "no-such.glb"}),
                       ("thin_extent_curve", {"glb": "no-such.glb"}),
                       ("offsurface_rate", {"prep": "no-such-dir"}),
                       ("anchor_check", {"a": "no-such.png",
                                         "b": "no-such.png"})):
        err = refusal(call(tool, args))
        assert err["code"] == "PRECONDITION_MISSING", (
            "%s should serve (and refuse this call only for its missing "
            "input); got %s - if NOT_WRAPPED, an E28 wrap regressed"
            % (tool, err["code"]))


def test_t40_the_wrapped_registry_serves_all_eight():
    """WRAPPED is the printable claim about who serves; the served handlers
    are the fact. One entry per spec name, NONE unserved, every named file
    real. A future session that unserves a tool moves this pin on purpose,
    in that commit, with the module docstring."""
    import measure_support
    W = measure_support.measure_mcp.WRAPPED
    assert sorted(W) == sorted(measure_support.measure_mcp.TOOL_ORDER)
    unserved = sorted(k for k, v in W.items() if v is None)
    assert unserved == [], (
        "the refusing set is %r; since E28 2c every spec name serves. "
        "Moving this is deliberate - update T40 and the module docstring in "
        "the same commit." % unserved)
    for tool, rel in W.items():
        assert os.path.exists(os.path.join(str(REPO),
                                           rel.replace("/", os.sep))), (
            "%s claims to wrap %s, which does not exist" % (tool, rel))


def test_t40_the_collision_file_still_exists_where_the_notes_point():
    """The old refusal named tools/diagnostics/e13_anchor_check.py as the
    NAME COLLISION; that pointer now lives in the served tool's notes (T46
    asserts the text). THIS leg keeps the file's existence pinned, so if
    anyone moves the spiral-law guard the pointer is updated consciously
    rather than drifting into fiction."""
    assert os.path.exists(os.path.join(
        str(REPO), "tools", "diagnostics", "e13_anchor_check.py"))


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
