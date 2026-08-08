"""T23 - the mount path: .mcp.json is what makes the server reachable.

The E18 kickoff's words: the repo-root `.mcp.json` "IS the polish arc's
consumption path". A mount config nobody checks is a config that silently stops
working - and its failure mode is invisible, because a session that cannot see
the server simply reads the record the old way and never notices.

TWO TIERS, deliberately:

  hermetic  - the file parses, names exactly one server, and its args point at
              the entry point that exists in this repo. Runs anywhere, CI
              included.
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
SERVER_NAME = "facet-record"
ENTRY = "tools/record_mcp.py"


@pytest.fixture(scope="module")
def mount():
    assert MOUNT.exists(), (
        "%s is missing - the server is built but unreachable" % MOUNT)
    with open(str(MOUNT), "r", encoding="ascii") as fh:
        return json.load(fh)


def test_t23_mount_declares_the_server(mount):
    assert "mcpServers" in mount, mount
    servers = mount["mcpServers"]
    assert list(servers) == [SERVER_NAME], (
        "expected exactly one server named %r, got %s" % (SERVER_NAME, list(servers)))
    entry = servers[SERVER_NAME]
    assert entry["args"] == [ENTRY], entry
    assert (REPO / ENTRY).exists(), "the mount points at a file that is not here"
    assert entry["command"], "the mount declares no interpreter"
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
