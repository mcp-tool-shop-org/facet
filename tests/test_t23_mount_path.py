"""T23 - the mount path: .mcp.json is what makes the server reachable.

The E18 kickoff's words: the repo-root `.mcp.json` "IS the polish arc's
consumption path". A mount config nobody checks is a config that silently stops
working - and its failure mode is invisible, because a session that cannot see
the server simply reads the record the old way and never notices.

TWO SERVERS SINCE E31. This file asserted `list(servers) == ["facet-record"]`
- one server, exactly - and that assertion is why adding the measurement
server had to come here, in the commit that added it, rather than slipping in
unnoticed. [E29 Ruling 7] found `tools/measure_mcp.py` declared nowhere, so no
session could reach the eight measured tools over the transport at all; the
registration lands at E31 and the exact-set assertion below moves with it. The
set stays EXACT: a third server still fires.

TWO TIERS, deliberately:

  hermetic  - the file parses, names exactly the declared servers, and each
              one's args point at an entry point that exists in this repo.
              Runs anywhere, CI included.
  on-rig    - the interpreter the file names is LAUNCHED and driven over stdio,
              which is the only way to prove the command line in the file
              actually starts a server. Skipped with a printed reason where
              that interpreter does not exist (CI, any other machine), because
              the path is this rig's environment law (CLAUDE.md, Environment)
              and E17 Ruling 2 is why it is spelled out rather than left to
              whatever `python` resolves to.

The absolute interpreter path is deliberate and it is the SAME decision T18
enforces for the suite: bare `python` on this rig resolves to an interpreter
without the tool dependencies, which is the trap that cost the ruling seat a
diagnosis. A mount that inherits PATH would reproduce it silently.
"""
import asyncio
import json
import os

import pytest

from conftest import REPO

MOUNT = REPO / ".mcp.json"
SERVER_NAME = "facet-record"          # the on-rig tier's subject, below

# Every server the mount declares, and the entry point each must name. The set
# is exact on purpose: a server added without a line here is a server nobody
# checked. `facet-measure` joined at E31 (E29 Ruling 7).
DECLARED = {
    "facet-record": "tools/record_mcp.py",
    "facet-measure": "tools/measure_mcp.py",
}


@pytest.fixture(scope="module")
def mount():
    assert MOUNT.exists(), (
        "%s is missing - the server is built but unreachable" % MOUNT)
    with open(str(MOUNT), "r", encoding="ascii") as fh:
        return json.load(fh)


def test_t23_mount_declares_exactly_the_known_servers(mount):
    assert "mcpServers" in mount, mount
    servers = mount["mcpServers"]
    assert set(servers) == set(DECLARED), (
        "the mount's server set moved: %s. Adding one is welcome - add it to "
        "DECLARED in this same commit, or nothing checks it."
        % sorted(set(servers) ^ set(DECLARED)))


@pytest.mark.parametrize("name", sorted(DECLARED))
def test_t23_each_declared_server_points_at_a_real_entry_point(mount, name):
    entry = mount["mcpServers"][name]
    assert entry["args"] == [DECLARED[name]], entry
    assert (REPO / DECLARED[name]).exists(), (
        "the mount points at a file that is not here: %s" % DECLARED[name])
    assert entry["command"], "the mount declares no interpreter for %s" % name
    # no bare `python`: T18's trap, one config file over. Parse the mount's
    # OWN separators, not the host's: the command is a Windows absolute path
    # and this test also runs on CI's ubuntu, where posixpath neither splits
    # backslashes nor calls "E:\..." absolute - os.path.basename returned the
    # whole string there and the startswith failed (ci runs 31264937296 and
    # 31266198244, the shape test's own platform defect, repaired 2026-08-08).
    cmd = entry["command"]
    leaf = cmd.replace("\\", "/").rsplit("/", 1)[-1]
    assert leaf.lower().startswith("python"), cmd
    assert "/" in cmd or "\\" in cmd, (
        "the mount inherits PATH for its interpreter - on this rig bare "
        "`python` has no mcp and no open3d (E17 Ruling 2)")


def test_t23_every_declared_server_names_the_same_interpreter(mount):
    """The environment law names exactly ONE python and T18 refuses the rest.
    Two mounts pointing at two interpreters would serve two different
    measurement environments out of one repo, and the difference would be
    invisible from a session."""
    cmds = {n: mount["mcpServers"][n]["command"] for n in DECLARED}
    assert len(set(cmds.values())) == 1, cmds


def test_t23_mount_file_is_ascii():
    raw = open(str(MOUNT), "rb").read()
    raw.decode("ascii")
    assert b"\r\n" not in raw, ".mcp.json carries CRLF"


@pytest.mark.slow
def test_t23_the_declared_command_actually_starts_the_server(mount, tmp_path,
                                                             built_db):
    """The only test that proves the mount works rather than parses."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from mcp_support import certify, record_mcp

    entry = mount["mcpServers"][SERVER_NAME]
    if not os.path.exists(entry["command"]):
        pytest.skip(
            "mount tier: the interpreter named in .mcp.json is not on this "
            "machine: %s (this is the rig's environment law; CI runs the "
            "hermetic half of this file only)" % entry["command"])

    db = certify(tmp_path, built_db)
    env = dict(os.environ)
    env[record_mcp.DB_ENV] = db

    async def go():
        params = StdioServerParameters(
            command=entry["command"], args=list(entry["args"]),
            env=env, cwd=str(REPO))
        async with stdio_client(params) as (r, w):
            async with ClientSession(r, w) as s:
                init = await s.initialize()
                tools = await s.list_tools()
                health = await s.call_tool("record_health", {})
                return init, tools, health

    init, tools, health = asyncio.run(go())
    assert init.server_info.name == SERVER_NAME
    assert len(tools.tools) == 6, [t.name for t in tools.tools]
    assert not health.is_error
    body = json.loads(health.content[0].text)
    # SERVING vs SERVING_STALE is deliberately NOT pinned here, and this is a
    # measured decision rather than a soft one: the first run of this file
    # failed on a `== "SERVING"` pin because THREE sessions were live in this
    # shared working copy and one of them wrote a doc during the ~2 s the
    # subprocess takes to start. What this test is about is that the mount
    # ANSWERS. Staleness has its own tests (T21/T22), driven from the
    # certificate side where the diff is deterministic.
    assert body["serving"] is True, body
    print("T23 mount health state: %s" % body["state"])
