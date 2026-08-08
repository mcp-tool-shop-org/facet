"""Shared helpers for the record-index MCP tests (T19-T22, E18).

Deliberately NOT in conftest.py: conftest is imported for every collection,
and importing `record_mcp` there would make an absent `mcp` SDK kill the whole
suite at collection time instead of failing the tests that need it. The
interpreter pre-check (T18, E17 Ruling 2) is the place that refuses on a
missing module, and `mcp` joins its measured table in the same commit as these
tests.

Everything here is ASCII (the repo's law).
"""
import asyncio
import json
import os
import shutil
import sys

from conftest import REPO, TOOLS

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import facet_index                                   # noqa: E402
import record_mcp                                    # noqa: E402
from mcp import Client                               # noqa: E402

# A synthetic verify RESULT, used to drive the health state machine cheaply.
# It is not a synthetic verify RUN: T20 pins the real parse against a real
# transcript, and this dict is the shape that parse produces when the four
# legs hold. Using it here keeps the state-machine tests off a 3-build verify.
PASSED_PARSE = {
    "state": "PASSED",
    "legs": {k: "PASSED" for k in record_mcp.LEG_KEYS},
    "determinism_leg": "byte-identity",
    "failures": [],
    "unattributed": [],
    "andon": [],
    "exit_code": facet_index.EXIT_OK,
}

# E21 F3 found this constant hardcoded and unasserted: nothing compared it
# against a live failing run, so it could encode a wrong value indefinitely.
# E22 moves it to 4 with the ruling (E21 Ruling 4) and BINDS it to the tool's
# own constant rather than re-hardcoding the new number, because a literal here
# is a fixture that can silently disagree with the command it stands in for.
FAILED_PARSE = {
    "state": "FAILED",
    "legs": dict(PASSED_PARSE["legs"], **{"3_pointers": "FAILED"}),
    "determinism_leg": "byte-identity",
    "failures": ["rulings: 4 dangling pointers"],
    "unattributed": [],
    "andon": [],
    "exit_code": facet_index.EXIT_REFUSED,
}

SYNTHETIC_TRANSCRIPT = "[synthetic] this transcript was authored by the test\n"


def certify(tmp_path, src_db, parsed=None, verb="test-fixture"):
    """A scratch DB + a certificate for it, in the test's own tmp_path.

    The DB is COPIED (the recorded/tracked artifact is never touched) and the
    certificate is written by the server's own writer, so the corpus manifest
    inside it is the live one at this instant.
    """
    os.makedirs(str(tmp_path), exist_ok=True)     # scripts create their own dirs
    db = os.path.join(str(tmp_path), "facet.db")
    shutil.copyfile(str(src_db), db)
    record_mcp.write_certificate(db, verb, parsed or PASSED_PARSE,
                                 SYNTHETIC_TRANSCRIPT)
    return db


def load_cert(db):
    with open(record_mcp.cert_path(db), "r", encoding="ascii") as fh:
        return json.load(fh)


def save_cert(db, doc):
    with open(record_mcp.cert_path(db), "w", encoding="ascii", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=True, indent=1, sort_keys=True)
        fh.write("\n")


def bind_db(monkeypatch, db):
    """Point the server at a scratch index for the duration of one test."""
    monkeypatch.setenv(record_mcp.DB_ENV, str(db))


def call(tool, args=None):
    """One protocol-level tool call against the real MCPServer instance.

    `Client(server)` speaks the same MCP request/response objects a mounted
    session speaks - list_tools/call_tool go through the server's dispatch,
    schema validation and error wrapping. The subprocess-over-stdio path (the
    literal wire) is exercised once, in T22, rather than per assertion.
    """
    async def go():
        async with Client(record_mcp.srv) as c:
            return await c.call_tool(tool, args or {})
    return asyncio.run(go())


def list_tools():
    async def go():
        async with Client(record_mcp.srv) as c:
            return await c.list_tools()
    return asyncio.run(go())


def payload(result):
    """The JSON body of a successful tool result."""
    assert not result.is_error, "tool refused: %s" % text_of(result)
    return json.loads(text_of(result))


def text_of(result):
    return result.content[0].text if result.content else ""


def refusal(result):
    """The structured error out of a REFUSED result.

    The refusal is loud on purpose (spec section 5): the SDK marks the result
    is_error, the human-readable head names the code and the fix, and the last
    line is the machine-readable object. This reads that last line.
    """
    assert result.is_error, "expected a refusal, got: %s" % text_of(result)[:400]
    body = text_of(result)
    last = [ln for ln in body.splitlines() if ln.strip()][-1]
    return json.loads(last)


__all__ = ["REPO", "record_mcp", "PASSED_PARSE", "FAILED_PARSE", "certify",
           "load_cert", "save_cert", "bind_db", "call", "list_tools",
           "payload", "text_of", "refusal"]
