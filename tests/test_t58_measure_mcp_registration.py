"""T58 - the measurement server is REACHABLE OVER MCP, not merely importable.

WHY THIS FILE EXISTS. [E29 Ruling 7] found that `.mcp.json` declared ONE
server, `facet-record`, and that `tools/measure_mcp.py` was in neither that
file nor the workspace's own - so no session could reach the measurement
surface over the transport at all. E29 graded its meshes by importing the
module and unwrapping the tool functions in-process, which proved THE CODE
PATH and says nothing about THE TRANSPORT. "The measurement server serves 8 of
8" was true of one and false of the other.

The registration is one line. THE LINE IS NOT THE DELIVERABLE - adding it and
declaring it fixed is the same shape as running `--help` and declaring a wheel
good, which is exactly how four releases shipped a broken resolver (E24). So
the line ships with THIS: a test that starts the declared command as a
SUBPROCESS, speaks stdio to it, calls a served tool, and asserts a payload
comes back carrying its identity envelope.

WHAT IS LAUNCHED, AND WHAT IS ONLY ASSERTED. `.mcp.json` declares the rig's
one pinned interpreter by absolute path, and that path does not exist on a CI
runner. So the DECLARATION is asserted (both servers name the same interpreter
- the environment law names exactly one python) and the RUN uses the suite's
own `sys.executable` with the declared arguments. Launching the literal
declared command would make this file skip on the only gate that fires every
push, which is the defect's own shape (E24 Ruling 3).

Everything printed here is ASCII (the repo's law).
"""
import asyncio
import hashlib
import json
import os
import sys

import pytest

from conftest import REPO, TOOLS

MCP_JSON = REPO / ".mcp.json"
MEASURE_SERVER = "facet-measure"
RECORD_SERVER = "facet-record"

# The eight names spec 2 serves. Duplicated from measure_mcp.TOOL_ORDER on
# purpose: this file asks what a MOUNT sees, and reading the surface from the
# module under test would make the assertion a tautology.
SPEC_EIGHT = {"mesh_stats", "mesh_topology", "reach_ceiling",
              "thin_extent_curve", "offsurface_rate", "texel_provenance",
              "anchor_check", "measure_report"}

CUBE = str(REPO / "tests" / "fixtures" / "measure_min" / "meshes" / "cube.glb")


def declared(name):
    """The server's entry in .mcp.json, or None. Reads the file every call so
    a test cannot pass against a stale parse."""
    with open(str(MCP_JSON), encoding="utf-8") as fh:
        doc = json.load(fh)
    return doc.get("mcpServers", {}).get(name)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# the declaration - and the can-fail leg FIRST
# ---------------------------------------------------------------------------

def test_t58_the_config_reader_can_miss():
    """THE CAN-FAIL LEG. Before trusting any pass below, prove a miss is
    reachable: a server nobody declared must read as absent, and a server that
    IS declared must not."""
    assert declared("facet-there-is-no-such-server") is None
    assert declared(RECORD_SERVER) is not None, (
        "the reader returns None for a server the repo has served since E18 - "
        "it is not reading .mcp.json at all")


def test_t58_the_measurement_server_is_declared():
    """E29 Ruling 7's finding, closed. A session that mounts this repo must be
    able to reach the measurement surface without importing anything."""
    entry = declared(MEASURE_SERVER)
    assert entry is not None, (
        ".mcp.json declares no %r - the served surface is unreachable over "
        "MCP and every claim that it 'serves 8 of 8' is about the code path "
        "only (E29 Ruling 7)" % MEASURE_SERVER)
    args = entry.get("args") or []
    assert any(a.replace("\\", "/").endswith("tools/measure_mcp.py")
               for a in args), (
        "%r is declared but does not point at tools/measure_mcp.py: %r"
        % (MEASURE_SERVER, args))


def test_t58_both_servers_name_the_same_interpreter():
    """The environment law names exactly ONE python (CLAUDE.md, Environment),
    and T18 refuses the rest. Two declarations pointing at two interpreters
    would serve two different measurement environments from one repo."""
    a = declared(RECORD_SERVER)["command"]
    b = declared(MEASURE_SERVER)["command"]
    assert a == b, (
        "the two servers are declared with different interpreters:\n"
        "  %s = %s\n  %s = %s" % (RECORD_SERVER, a, MEASURE_SERVER, b))
    assert a.replace("\\", "/").endswith("python.exe") or \
        a.replace("\\", "/").endswith("python"), \
        "the declared command is not a python interpreter: %r" % a


# ---------------------------------------------------------------------------
# the transport - the half an in-process client cannot see
# ---------------------------------------------------------------------------

def _over_stdio(tool, arguments):
    """Start the DECLARED arguments under the suite's interpreter and drive
    one tool call over a real stdio transport."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    entry = declared(MEASURE_SERVER)
    assert entry is not None, "no %r declared" % MEASURE_SERVER

    async def go():
        params = StdioServerParameters(
            command=sys.executable, args=list(entry["args"]),
            env=dict(os.environ), cwd=str(REPO))
        async with stdio_client(params) as (r, w):
            async with ClientSession(r, w) as s:
                init = await s.initialize()
                tools = await s.list_tools()
                res = await s.call_tool(tool, arguments)
                return init, tools, res

    return asyncio.run(go())


@pytest.mark.slow
def test_t58_stdio_subprocess_serves_the_eight_and_returns_an_envelope():
    """THE WHOLE POINT. A subprocess, a real transport, a served tool, and a
    payload whose identity block is populated - not a banner, not an
    in-process function call."""
    init, tools, res = _over_stdio("mesh_stats", {"glb": CUBE})

    assert init.server_info.name == MEASURE_SERVER, (
        "the entry point announced %r" % init.server_info.name)
    assert {t.name for t in tools.tools} == SPEC_EIGHT, (
        "the mounted surface is not spec 2's eight: %s"
        % sorted({t.name for t in tools.tools} ^ SPEC_EIGHT))

    assert not res.is_error, "mesh_stats refused over stdio:\n%s" % (
        res.content[0].text if res.content else "(no content)")
    doc = json.loads(res.content[0].text)

    env = doc.get("measure")
    assert isinstance(env, dict), "the payload carries no measure envelope"
    assert env["server"]["name"] == MEASURE_SERVER
    assert env["server"]["version"], "the envelope names no server version"
    assert env["tool"] == "mesh_stats"
    assert env["config_hash"], "the envelope carries no config hash"
    assert env["metrics_label"] == "diagnostic", (
        "every metric on this surface is diagnostic; promotion is a ruling")

    inst = env["instrument"]
    assert inst["path"] == "tools/verify/mesh_stats.py", inst
    on_disk = sha256_file(str(REPO / inst["path"].replace("/", os.sep)))
    assert inst["sha256"] == on_disk, (
        "the envelope's instrument hash does not match the file it names - "
        "the identity contract is decorative if this can drift:\n"
        "  payload: %s\n  on disk: %s" % (inst["sha256"], on_disk))

    assert doc["mesh"], "a payload came back with no measurement in it"


@pytest.mark.slow
def test_t58_a_refusal_also_travels_the_transport():
    """A refusal is this server's product too, and an in-process client cannot
    prove one survives the wire. A precondition that cannot be met must arrive
    as a structured error rather than a dead subprocess."""
    _init, _tools, res = _over_stdio(
        "mesh_stats", {"glb": str(REPO / "tests" / "fixtures" /
                                 "there-is-no-such-mesh.glb")})
    assert res.is_error, "a missing subject returned a payload"
    body = res.content[0].text
    assert "PRECONDITION_MISSING" in body, (
        "the refusal did not name its code over the wire:\n%s" % body[:400])
    assert "there-is-no-such-mesh.glb" in body, (
        "the refusal did not name the exact absent input")
