"""T22 - the six tools at PROTOCOL level, plus one run over the literal wire.

Source: index-mcp-spec.md section 3 (the tool table and its annotations),
section 3.2 (record_get reads the CORPUS, not the DB's copy), section 3.5
(record_claims is report-only by ruling and exits 0 whatever it finds),
section 8 (every response carries the certificate state, and file:line goes
last on a row).

WHY PROTOCOL-LEVEL RATHER THAN FUNCTION-LEVEL. What a mounted session actually
gets is a `tools/list` payload and a `tools/call` result - the annotations, the
input-schema validation and the is_error flag are produced by the SDK, not by
this repo's code, and a function-level test cannot see any of them. So the
surface is tested through `Client(server)`, which drives the same dispatch a
mount drives, and ONE test spawns the server as a subprocess and speaks stdio
to it, because an in-process client cannot prove the entry point runs at all.
"""
import asyncio
import json
import os
import shutil
import sys

import pytest

from conftest import REPO, TOOLS
from mcp_support import (bind_db, call, certify, list_tools, payload, record_mcp,
                         refusal, text_of)

SPEC_SURFACE = {
    "record_query": "readOnly",
    "record_get": "readOnly",
    "record_build": "notDestructive",
    "record_verify": "notDestructive",
    "record_health": "readOnly",
    "record_claims": "readOnly",
}


@pytest.fixture
def served(tmp_path, built_db, monkeypatch):
    """A certified scratch index, bound for the duration of one test."""
    db = certify(tmp_path, built_db)
    bind_db(monkeypatch, db)
    return db


# ---------------------------------------------------------------------------
# the surface
# ---------------------------------------------------------------------------

def test_t22_the_surface_is_exactly_the_specs_six_tools():
    tools = {t.name: t for t in list_tools().tools}
    assert set(tools) == set(SPEC_SURFACE), (
        "the tool surface drifted from spec section 3's table: %s"
        % sorted(set(tools) ^ set(SPEC_SURFACE)))
    for name, kind in SPEC_SURFACE.items():
        ann = tools[name].annotations
        assert ann is not None, "%s carries no annotations" % name
        if kind == "readOnly":
            assert ann.read_only_hint is True, name
        else:
            assert ann.destructive_hint is False, name
            assert ann.read_only_hint is not True, (
                "%s writes; it must not claim readOnlyHint" % name)
        assert (tools[name].description or "").strip(), (
            "%s has no description - the description is what a session reads "
            "to decide whether to call it" % name)


def test_t22_query_answers_a_seeded_question_with_its_pointer(served):
    """The seeded set is the external verifier's key; this asks one of its
    questions through the wire and requires the ruling it points at."""
    import facet_index

    question, phrase, target = facet_index.SEEDED[0]
    want_file, want_anchor = target
    body = payload(call("record_query", {"query": phrase, "limit": 3}))
    assert body["returned"] >= 1
    hit = [r for r in body["rows"]
           if r["file"] == want_file and r["anchor"] == want_anchor]
    assert hit, ("seeded question %r did not return %s :: %s in the top 3:\n%s"
                 % (question, want_file, want_anchor,
                    json.dumps(body["rows"], indent=1)))
    row = hit[0]
    for k in ("table", "anchor", "holding", "file", "line"):
        assert k in row, k
    # section 8: file:line goes LAST on a row, so a long path is never
    # truncated - the whole point of the row is that a human can open it
    keys = list(row)
    assert keys.index("file") > keys.index("holding")
    assert keys[-1] == "locator" and row["locator"].endswith(":%d" % row["line"])
    # every response carries the certificate state, not just refusals
    assert body["state"] == "SERVING"
    assert body["certificate"]["state"] == "PASSED"


def test_t22_query_bounds_its_inputs(served):
    for args, why in (({"query": "x" * 501}, "query too long"),
                      ({"query": ""}, "query empty"),
                      ({"query": "ok", "limit": 0}, "limit under 1"),
                      ({"query": "ok", "limit": 51}, "limit over 50"),
                      ({"query": "ok", "table": "rulingz"}, "unknown table")):
        e = refusal(call("record_query", args))
        assert e["code"] == "BAD_ARGUMENT", (why, e)
        assert e["hint"], why


def test_t22_query_filters_by_table_and_arc(served):
    body = payload(call("record_query",
                        {"query": "the hollow finding", "limit": 8,
                         "table": "rulings"}))
    assert body["rows"], "the table filter emptied a query that has rulings"
    assert {r["table"] for r in body["rows"]} == {"rulings"}
    body = payload(call("record_query",
                        {"query": "the hollow finding", "limit": 8,
                         "arc": "E14"}))
    assert body["rows"]
    for r in body["rows"]:
        assert "e14" in ("%s %s" % (r["file"], r["anchor"])).lower(), r


def test_t22_get_returns_corpus_text_not_the_dbs_copy(served):
    """Section 3.2: the markdown is canonical, so the full text comes from the
    markdown. Proved by requiring the returned block to be a literal substring
    of the corpus file on disk."""
    import facet_index

    _, phrase, (want_file, want_anchor) = facet_index.SEEDED[0]
    got = payload(call("record_get", {"file": want_file, "anchor": want_anchor}))
    assert got["text"].strip(), "record_get returned nothing"
    corpus = facet_index.read(want_file)
    assert got["text"] in corpus, (
        "the returned block is not literally present in %s - it did not come "
        "from the markdown" % want_file)
    assert got["lines"] == len(got["text"].splitlines())
    assert got["start_line"] >= 1 and got["end_line"] >= got["start_line"]
    assert got["state"] == "SERVING"


def test_t22_get_is_bounded(served):
    import facet_index

    _, _, (want_file, want_anchor) = facet_index.SEEDED[0]
    got = payload(call("record_get", {"file": want_file, "anchor": want_anchor,
                                      "max_lines": 3}))
    assert got["lines"] <= 3, got
    assert got["truncated"] is True
    e = refusal(call("record_get", {"file": want_file, "anchor": want_anchor,
                                    "max_lines": 4000}))
    assert e["code"] == "BAD_ARGUMENT"


def test_t22_get_refuses_an_anchor_that_is_not_there(served):
    e = refusal(call("record_get", {"file": "CLAUDE.md",
                                    "anchor": "Ruling 9999z"}))
    assert e["code"] == "ANCHOR_NOT_FOUND"
    e = refusal(call("record_get", {"file": "docs/does-not-exist.md",
                                    "locator": "anything"}))
    assert e["code"] == "ANCHOR_NOT_FOUND"


def test_t22_get_resolves_every_seeded_target(served):
    """19 anchors of four different shapes - `## Ruling 3` headings, `**25c -`
    bold leads, and a CLAUDE.md prose section - through one bounding rule."""
    import facet_index

    misses = []
    for question, _, target in facet_index.SEEDED:
        targets = target if isinstance(target, list) else [target]
        for want_file, want_anchor in targets:
            if want_anchor is None:
                continue
            res = call("record_get", {"file": want_file, "anchor": want_anchor})
            if res.is_error:
                misses.append("%s :: %s -> %s"
                              % (want_file, want_anchor, text_of(res)[:120]))
                continue
            body = json.loads(text_of(res))
            if not body["text"].strip():
                misses.append("%s :: %s -> empty block" % (want_file, want_anchor))
    assert not misses, "record_get could not resolve:\n  " + "\n  ".join(misses)


def test_t22_claims_is_report_only(served):
    """Section 3.5 / E15 handoff 2: report-only BY RULING, exits 0 whatever it
    finds. A diagnostic and a gate are different objects."""
    res = call("record_claims", {})
    assert not res.is_error, text_of(res)[:400]
    body = json.loads(text_of(res))
    assert body["exit_code"] == 0
    assert body["gates"] is False
    assert body["unreadable_summary_lines"] == [], (
        "the claims summary could not be read: %s" % body["unreadable_summary_lines"])
    for k in ("stale", "ambiguous", "unparseable"):
        assert isinstance(body["summary"][k], int), body["summary"]
    assert len(body["stale_rows"]) == body["summary"]["stale"]
    assert body["state"] in ("SERVING", "SERVING_STALE")


def test_t22_health_reports_all_three_states_over_the_wire(tmp_path, built_db,
                                                           monkeypatch):
    from mcp_support import FAILED_PARSE

    absent = os.path.join(str(tmp_path), "absent", "facet.db")
    bind_db(monkeypatch, absent)
    body = payload(call("record_health", {}))          # never refuses
    assert body["serving"] is False and body["state"] == "REFUSING"
    assert body["error"]["code"] == "INDEX_MISSING"

    db = certify(tmp_path, built_db)
    bind_db(monkeypatch, db)
    body = payload(call("record_health", {}))
    assert body["state"] == "SERVING" and body["serving"] is True

    from mcp_support import load_cert, save_cert
    doc = load_cert(db)
    doc["corpus"]["manifest"]["CLAUDE.md"] = "0" * 64
    save_cert(db, doc)
    body = payload(call("record_health", {}))
    assert body["state"] == "SERVING_STALE"
    assert "CLAUDE.md" in body["staleness"]["banner"]

    failed = certify(tmp_path / "f", built_db, parsed=FAILED_PARSE)
    bind_db(monkeypatch, failed)
    body = payload(call("record_health", {}))
    assert body["state"] == "REFUSING"
    assert body["error"]["code"] == "INDEX_VERIFY_FAILED"


def test_t22_the_refusal_is_loud_on_the_wire(tmp_path, built_db, monkeypatch):
    """A caller that must read a field to discover the answer is untrustworthy
    will not read it (section 5). So: is_error on the protocol, the code and
    the fix in the human-readable head, and the machine-readable object last."""
    db = os.path.join(str(tmp_path), "facet.db")
    shutil.copyfile(str(built_db), db)                 # a DB with no certificate
    bind_db(monkeypatch, db)
    for tool, args in (("record_query", {"query": "the hollow finding"}),
                       ("record_get", {"file": "CLAUDE.md", "anchor": "x"}),
                       ("record_claims", {})):
        res = call(tool, args)
        assert res.is_error is True, "%s served from an uncertified index" % tool
        body = text_of(res)
        assert "REFUSED" in body, body[:200]
        assert "INDEX_NEVER_VERIFIED" in body, body[:200]
        assert record_mcp.FIX_COMMAND in body, body[:200]
        e = refusal(res)
        assert e == {"error": True, "code": "INDEX_NEVER_VERIFIED",
                     "message": e["message"], "hint": e["hint"],
                     "retryable": True}


def test_t22_a_stale_index_still_serves_and_says_so(served):
    """The banner rides the RESPONSE, not only record_health - a session that
    never calls health must still be told what it is reading."""
    from mcp_support import load_cert, save_cert

    doc = load_cert(served)
    doc["corpus"]["manifest"]["CLAUDE.md"] = "0" * 64
    save_cert(served, doc)
    body = payload(call("record_query", {"query": "the hollow finding"}))
    assert body["state"] == "SERVING_STALE"
    assert body["rows"], "a stale index refused instead of warning"
    assert any("STALE INDEX" in n for n in body["notes"]), body["notes"]
    assert "CLAUDE.md" in body["staleness_banner"]


def test_t22_recorded_retrieval_boundary_is_surfaced_not_hidden(served):
    """E15 Ruling 7: conversational phrasings surface the evidence documents
    above the ruling, and the response SAYS SO in `notes` rather than leaving
    the caller to infer a defect."""
    body = payload(call("record_query", {"query": "the hollow finding",
                                         "limit": 8}))
    tables = [r["table"] for r in body["rows"]]
    if "rulings" in tables and tables[0] != "rulings":
        assert any("E15 Ruling 7" in n for n in body["notes"]), body["notes"]
    else:
        # the boundary did not fire on this phrasing; force the condition so
        # the note is proved reachable rather than assumed
        body = payload(call("record_query",
                            {"query": "what happened to the crop pass",
                             "limit": 8}))
        tables = [r["table"] for r in body["rows"]]
        if "rulings" in tables and tables[0] != "rulings":
            assert any("E15 Ruling 7" in n for n in body["notes"]), body["notes"]
        else:
            pytest.skip("neither probe phrasing put a non-ruling above a ruling "
                        "on this corpus; the note's condition did not arise")


# ---------------------------------------------------------------------------
# the literal wire
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_t22_stdio_subprocess_serves_the_surface(tmp_path, built_db):
    """The mount path, end to end: the entry point launched as a subprocess and
    driven over stdio - what `.mcp.json` makes a session do. An in-process
    client cannot prove `python tools/record_mcp.py` runs at all."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    db = certify(tmp_path, built_db)
    env = dict(os.environ)
    env[record_mcp.DB_ENV] = db

    async def go():
        params = StdioServerParameters(
            command=sys.executable,
            args=[str(TOOLS / "record_mcp.py")],
            env=env, cwd=str(REPO))
        async with stdio_client(params) as (r, w):
            async with ClientSession(r, w) as s:
                init = await s.initialize()
                tools = await s.list_tools()
                health = await s.call_tool("record_health", {})
                q = await s.call_tool(
                    "record_query", {"query": "the hollow finding", "limit": 3})
                return init, tools, health, q

    init, tools, health, q = asyncio.run(go())
    assert init.server_info.name == "facet-record"
    assert {t.name for t in tools.tools} == set(SPEC_SURFACE)
    assert not health.is_error
    assert json.loads(health.content[0].text)["state"] == "SERVING"
    assert not q.is_error
    assert json.loads(q.content[0].text)["returned"] >= 1
