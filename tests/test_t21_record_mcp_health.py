"""T21 - the three-state health surface, every state DEMONSTRATED.

Source: index-mcp-spec.md section 5.

    PASSED, corpus unchanged  -> serves
    PASSED, corpus has moved  -> serves WITH a staleness banner naming what moved
    FAILED, or no certificate -> REFUSES, loudly, with the structured error

Why staleness warns rather than refuses: the DB commits at SESSION boundaries,
not every fold (E15 Ruling 4.2), so bounded staleness is the ruled normal state
of a fresh clone and a refusal there would fire on correct work. Put the andon
on the direction the invariant does not bound.

Why no-certificate refuses: a gate trusted from the fold before is not a gate,
and here there is no gate result at all - only a DB somebody produced.

THERE IS NO SKIP FLAG and adding one is out of scope permanently (E08 Amendment
32). The last test in this file is what makes that structural rather than a
sentence in a docstring.
"""
import json
import os
import shutil

import pytest

from mcp_support import (FAILED_PARSE, certify, load_cert, record_mcp,
                         save_cert)

# Which test reaches which named code. The mapping is asserted against
# record_mcp.CODES at the bottom, so a code added without a test fails here.
CODE_COVERAGE = {
    "INDEX_MISSING": "test_t21_refuses_with_no_index",
    "INDEX_NEVER_VERIFIED": "test_t21_refuses_with_no_certificate",
    "INDEX_VERIFY_FAILED": "test_t21_refuses_on_a_failed_certificate",
    "CORPUS_NOT_FOUND": "test_t21_refuses_when_the_repo_is_not_the_record",
    "CONVENTIONS_INVALID": "test_t21_refuses_when_the_conventions_module_moved",
    "SEEDED_SET_INVALID": "test_t21_refuses_on_an_unusable_seeded_set",
    "ANCHOR_NOT_FOUND": "tests/test_t22_record_mcp_tools.py",
    "BAD_ARGUMENT": "tests/test_t22_record_mcp_tools.py",
    "INTERNAL": "test_t21_internal_wraps_rather_than_raising_a_stack",
}


def _err(h):
    assert h["serving"] is False, "expected a refusal, got %s" % h["state"]
    assert h["state"] == "REFUSING"
    e = h["error"]
    for k in ("error", "code", "message", "hint", "retryable"):
        assert k in e, "the error shape is missing %r: %s" % (k, e)
    assert e["error"] is True
    assert e["code"] in record_mcp.CODES
    assert e["message"] and e["hint"], e
    return e


# ---------------------------------------------------------------------------
# state 1 - serving
# ---------------------------------------------------------------------------

def test_t21_serves_when_the_certificate_passes_and_the_corpus_is_still(
        tmp_path, built_db):
    db = certify(tmp_path, built_db)
    h = record_mcp.health(db)
    assert h["serving"] is True
    assert h["state"] == "SERVING"
    assert h["staleness"] is None
    assert h["certificate"]["state"] == "PASSED"
    assert h["certificate"]["determinism_leg"] == "byte-identity"
    assert h["corpus"]["id_now"] == h["certificate"]["corpus_id_at_build"]


# ---------------------------------------------------------------------------
# state 2 - serving, stale, and the banner NAMES what moved
# ---------------------------------------------------------------------------

def test_t21_stale_banner_names_the_file_that_moved(tmp_path, built_db):
    """The corpus moving after the build is simulated FROM THE CERTIFICATE
    SIDE - the recorded digest for one file is falsified - so the diff, the
    banner and the counts are the real mechanism firing against the real live
    corpus. (The live corpus is not written by any test; this repo's rules
    forbid a test that edits the record.)"""
    db = certify(tmp_path, built_db)
    doc = load_cert(db)
    doc["corpus"]["manifest"]["CLAUDE.md"] = "0" * 64
    save_cert(db, doc)

    h = record_mcp.health(db)
    assert h["serving"] is True, "staleness must WARN, never refuse"
    assert h["state"] == "SERVING_STALE"
    s = h["staleness"]
    assert s["counts"] == {"modified": 1, "added": 0, "removed": 0}
    assert s["modified"] == ["CLAUDE.md"]
    assert "CLAUDE.md" in s["banner"], s["banner"]
    assert "STALE INDEX" in s["banner"]
    assert record_mcp.FIX_COMMAND in s["banner"], (
        "the banner does not name the one command that fixes it")


def test_t21_stale_banner_classes_added_and_removed(tmp_path, built_db):
    db = certify(tmp_path, built_db)
    doc = load_cert(db)
    victim = "README.md"
    assert victim in doc["corpus"]["manifest"]
    del doc["corpus"]["manifest"][victim]             # live file the cert lacks
    doc["corpus"]["manifest"]["docs/a-file-that-never-existed.md"] = "1" * 64
    save_cert(db, doc)

    h = record_mcp.health(db)
    assert h["state"] == "SERVING_STALE"
    s = h["staleness"]
    assert s["counts"]["added"] == 1 and s["counts"]["removed"] == 1
    assert victim in s["added"]
    assert "docs/a-file-that-never-existed.md" in s["removed"]


def test_t21_stale_banner_bounds_its_own_list(tmp_path, built_db):
    """A banner that pastes 200 filenames is a banner nobody reads. The names
    are bounded; the COUNT stays exact."""
    db = certify(tmp_path, built_db)
    doc = load_cert(db)
    man = doc["corpus"]["manifest"]
    for k in sorted(man)[: record_mcp.STALE_NAMES + 5]:
        man[k] = "2" * 64
    save_cert(db, doc)
    s = record_mcp.health(db)["staleness"]
    assert s["counts"]["modified"] == record_mcp.STALE_NAMES + 5
    assert len(s["modified"]) == record_mcp.STALE_NAMES + 1
    assert s["modified"][-1].startswith("... and 5 more")


# ---------------------------------------------------------------------------
# state 3 - refusing, in every way it can be reached
# ---------------------------------------------------------------------------

def test_t21_refuses_with_no_index(tmp_path):
    e = _err(record_mcp.health(os.path.join(str(tmp_path), "absent.db")))
    assert e["code"] == "INDEX_MISSING"
    assert e["retryable"] is True


def test_t21_refuses_with_no_certificate(tmp_path, built_db):
    db = os.path.join(str(tmp_path), "facet.db")
    shutil.copyfile(str(built_db), db)               # a DB somebody produced
    assert not os.path.exists(record_mcp.cert_path(db))
    e = _err(record_mcp.health(db))
    assert e["code"] == "INDEX_NEVER_VERIFIED"
    assert record_mcp.FIX_COMMAND in e["hint"]


@pytest.mark.parametrize("damage,label", [
    ("", "empty"),
    ("{", "truncated json"),
    ('{"schema": "facet-record-index-certificate/1"}', "no state"),
    ('{"schema": "something-else/9", "state": "PASSED", "legs": {}, '
     '"corpus": {"manifest": {}}, "db": {}}', "wrong schema"),
    ('{"schema": "facet-record-index-certificate/1", "state": "PASSED", '
     '"legs": {}, "db": {}, "corpus": {}}', "no manifest"),
    ('["not", "an", "object"]', "not an object"),
])
def test_t21_refuses_on_a_corrupted_certificate(tmp_path, built_db, damage, label):
    db = certify(tmp_path, built_db)
    with open(record_mcp.cert_path(db), "w", encoding="ascii") as fh:
        fh.write(damage)
    e = _err(record_mcp.health(db))
    assert e["code"] == "INDEX_NEVER_VERIFIED", (label, e)
    assert "unreadable" in e["message"] or "certificate" in e["message"], (label, e)


def test_t21_refuses_on_a_failed_certificate(tmp_path, built_db):
    db = certify(tmp_path, built_db, parsed=FAILED_PARSE)
    e = _err(record_mcp.health(db))
    assert e["code"] == "INDEX_VERIFY_FAILED"
    assert "3_pointers" in e["message"], e
    assert "dangling pointers" in e["message"], e
    assert e["retryable"] is False
    assert record_mcp.FIX_COMMAND in e["hint"]


def test_t21_refuses_when_the_db_is_not_the_one_that_was_certified(
        tmp_path, built_db):
    """A build without its verify is the ungated state the E15 ritual closes.
    A certificate that describes a different artifact is no certificate for
    the one present."""
    db = certify(tmp_path, built_db)
    assert record_mcp.health(db)["serving"] is True
    with open(db, "ab") as fh:                       # the DB moved after certifying
        fh.write(b"\x00")
    e = _err(record_mcp.health(db))
    assert e["code"] == "INDEX_NEVER_VERIFIED"
    assert "different index" in e["message"], e


def test_t21_refuses_when_the_repo_is_not_the_record(tmp_path, monkeypatch):
    import facet_index

    empty = tmp_path / "not-the-record"
    empty.mkdir()
    monkeypatch.setattr(record_mcp, "REPO", str(empty))
    monkeypatch.setattr(facet_index, "REPO", str(empty))
    with pytest.raises(record_mcp.RecordError) as exc:
        record_mcp._corpus_manifest()
    assert exc.value.code == "CORPUS_NOT_FOUND"
    assert exc.value.shape()["error"] is True


def test_t21_refuses_when_the_conventions_module_moved(monkeypatch):
    """Section 6: the server refuses a repo whose conventions it cannot find
    rather than guessing a pattern. Under in-facet placement the declaration IS
    facet_index, so a rename there must refuse loudly."""
    import facet_index

    monkeypatch.delattr(facet_index, "query")
    with pytest.raises(record_mcp.RecordError) as exc:
        record_mcp._check_conventions()
    assert exc.value.code == "CONVENTIONS_INVALID"
    assert "query" in exc.value.message


@pytest.mark.parametrize("bad", [[], (), [("q", "phrase")], ["not a row"]])
def test_t21_refuses_on_an_unusable_seeded_set(monkeypatch, bad):
    """Leg 4 is the external verifier. Without its key, `verify` proves nothing
    about retrieval, and a server that shipped its own key would be grading
    itself (spec section 4.3)."""
    import facet_index

    monkeypatch.setattr(facet_index, "SEEDED", bad)
    with pytest.raises(record_mcp.RecordError) as exc:
        record_mcp._check_conventions()
    assert exc.value.code == "SEEDED_SET_INVALID"


def test_t21_internal_wraps_rather_than_raising_a_stack():
    """Shipcheck gate B: structured errors, no raw stacks. INTERNAL exists so
    an unexpected exception still leaves as the studio's shape."""
    e = record_mcp.RecordError("INTERNAL", "build failed: ValueError: x",
                               "This is a defect in the builder.")
    s = e.shape()
    assert s == {"error": True, "code": "INTERNAL",
                 "message": "build failed: ValueError: x",
                 "hint": "This is a defect in the builder.", "retryable": False}
    loud = e.loud()
    assert loud.startswith("REFUSED:")
    assert json.loads(loud.splitlines()[-1]) == s
    with pytest.raises(AssertionError):
        record_mcp.RecordError("NOT_A_CODE", "m", "h")   # codes are a closed set


# ---------------------------------------------------------------------------
# the guards on the guard
# ---------------------------------------------------------------------------

def test_t21_every_named_code_is_reachable():
    assert set(CODE_COVERAGE) == set(record_mcp.CODES), (
        "a named error code has no test:\n  unreached: %s\n  unnamed: %s"
        % (sorted(set(record_mcp.CODES) - set(CODE_COVERAGE)),
           sorted(set(CODE_COVERAGE) - set(record_mcp.CODES))))


def test_t21_there_is_no_skip_flag(tmp_path, built_db, monkeypatch):
    """E08 Amendment 32, made structural.

    A check a scripting accident can separate from the action it gates is not a
    gate - 47,020 texels were committed after a fired ANDON because a shell
    chain walked past an exit code. Here the gated step is ANSWERING, so the
    check lives in the query path and there is no way around it: not a CLI
    flag, not an environment variable, not an argument.
    """
    import contextlib
    import io

    # 1. the CLI offers exactly two options and neither of them skips
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        with pytest.raises(SystemExit):
            record_mcp.main(["--help"])
    help_text = buf.getvalue()
    for word in ("--force", "--skip", "--no-verify", "--allow-stale",
                 "--ignore-certificate"):
        assert word not in help_text, "the CLI carries a bypass: %s" % word
    opts = set()
    for line in help_text.splitlines():
        for tok in line.split():
            if tok.startswith("--"):
                opts.add(tok.strip(",").split("=")[0])
    assert opts <= {"--help", "--db", "--print-tools"}, sorted(opts)

    # 2. no environment variable turns the gate off. The one env var this
    #    module reads selects WHICH derived index, never whether it is checked.
    db = certify(tmp_path, built_db, parsed=FAILED_PARSE)
    monkeypatch.setenv(record_mcp.DB_ENV, db)
    for var in ("FACET_SKIP_VERIFY", "FACET_FORCE", "RECORD_MCP_SKIP",
                "FACET_INDEX_SKIP_HEALTH"):
        monkeypatch.setenv(var, "1")
    with pytest.raises(Exception) as exc:            # ToolError from the gate
        record_mcp.record_query("anything")
    assert "INDEX_VERIFY_FAILED" in str(exc.value), str(exc.value)[:300]


def test_t21_health_itself_never_refuses(tmp_path):
    """record_health is how you find out the others are refusing. If it refused
    too, a broken index would be undiagnosable from the client."""
    h = record_mcp.health(os.path.join(str(tmp_path), "absent.db"))
    assert h["serving"] is False and h["error"]["code"] == "INDEX_MISSING"
    assert isinstance(h, dict), "health raised instead of returning"
