"""Shared helpers for the measurement MCP tests (T35-T40, E27).

Deliberately NOT in conftest.py, for mcp_support's own stated reason: conftest
is imported for every collection, and importing `measure_mcp` there would make
an absent `mcp` SDK kill the whole suite at collection time. T18's interpreter
pre-check is the place that refuses on a missing module.

Everything here is ASCII (the repo's law).
"""
import asyncio
import json
import os
import sys

from conftest import REPO, TOOLS

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import measure_mcp                                   # noqa: E402
from mcp import Client                               # noqa: E402

FIXTURE = os.path.join(str(REPO), "tests", "fixtures", "measure_min")
MESHES = os.path.join(FIXTURE, "meshes")
PREP = os.path.join(FIXTURE, "prep")
STATE = os.path.join(FIXTURE, "state")
REPORT = os.path.join(FIXTURE, "report")


def call(tool, args=None):
    """One protocol-level tool call against the real MCPServer instance -
    the same dispatch, schema validation and error wrapping a mount drives."""
    async def go():
        async with Client(measure_mcp.srv) as c:
            return await c.call_tool(tool, args or {})
    return asyncio.run(go())


def list_tools():
    async def go():
        async with Client(measure_mcp.srv) as c:
            return await c.list_tools()
    return asyncio.run(go())


def payload(result):
    """The JSON body of a successful tool result."""
    assert not result.is_error, "tool refused: %s" % text_of(result)[:600]
    return json.loads(text_of(result))


def text_of(result):
    return result.content[0].text if result.content else ""


def refusal(result):
    """The structured error out of a REFUSED result: the human-readable head
    names the code and the fix, and the last line is the machine object."""
    assert result.is_error, "expected a refusal, got: %s" % text_of(result)[:400]
    body = text_of(result)
    last = [ln for ln in body.splitlines() if ln.strip()][-1]
    return json.loads(last)


__all__ = ["REPO", "TOOLS", "measure_mcp", "FIXTURE", "MESHES", "PREP",
           "STATE", "REPORT", "call", "list_tools", "payload", "text_of",
           "refusal"]
