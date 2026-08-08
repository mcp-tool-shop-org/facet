"""T20 - the certificate: a sidecar, ASCII, and a parse that cannot pass quietly.

Sources: index-mcp-spec.md section 3.3 (build and verify are ONE act), section
3.4 (the four legs; the .dump fallback is reported, never silent), section 4.4
(the certificate is a sidecar, NEVER a DB row - writing it into the DB makes the
DB no longer a pure function of the corpus and THE DETERMINISM LEG WOULD FAIL ON
ITS OWN OUTPUT), and the E18 kickoff's content-derived corpus identity.

The load-bearing test here is the first one: `parse_verify` is coupled to
facet_index's print sites, and that coupling is checked against a REAL verify
run rather than against a transcript this file wrote. If facet_index rewords a
leg header, this fails loudly - which is the whole point, because the failure
mode of a transcript parse is a certificate that silently loses detail.
"""
import json
import os

import pytest

from conftest import run_py
from mcp_support import (FAILED_PARSE, PASSED_PARSE, SYNTHETIC_TRANSCRIPT,
                         certify, load_cert, record_mcp)


# ---------------------------------------------------------------------------
# the parse, against the real thing
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def real_transcript(built_db):
    rc, out, err = run_py("facet_index.py", ["verify", "--db", built_db])
    assert out.strip(), "verify printed nothing:\n%s" % err
    return rc, out


@pytest.mark.fold
def test_t20_parse_reads_a_real_verify(real_transcript):
    rc, out = real_transcript
    p = record_mcp.parse_verify(rc, out)
    assert p["andon"] == [], (
        "the parse could not read verify's own output - every entry here is a "
        "print site in facet_index.py that moved:\n  %s" % "\n  ".join(p["andon"]))
    assert p["state"] == "PASSED", p
    assert set(p["legs"]) == set(record_mcp.LEG_KEYS)
    assert all(v == "PASSED" for v in p["legs"].values()), p["legs"]
    assert p["failures"] == [] and p["unattributed"] == []
    # WHICH leg held is reported, never asserted: the .dump fallback is
    # pre-registered and legal, and pinning byte-identity here would turn a
    # legal weaker claim into a red suite on some other filesystem.
    assert p["determinism_leg"], "no determinism leg recorded"
    print("T20 determinism leg that held: %s" % p["determinism_leg"])


@pytest.mark.fold
def test_t20_parse_fails_loudly_when_a_leg_header_moves(real_transcript):
    """The can-fail proof for the coupling above."""
    rc, out = real_transcript
    for key, header in record_mcp.LEG_HEADERS.items():
        damaged = "\n".join(ln for ln in out.splitlines() if header not in ln)
        p = record_mcp.parse_verify(rc, damaged)
        assert p["state"] == "FAILED", (
            "removing the %s header still parsed as PASSED" % key)
        assert any(key in a for a in p["andon"]), p["andon"]


def _fabricate(verdict="VERIFY PASSED - all four legs", failures=(),
               det="byte-identity", drop=()):
    lines = []
    for key, header in record_mcp.LEG_HEADERS.items():
        if key not in drop:
            lines.append("  %s - synthetic" % header)
    if "discovery" not in drop:
        lines.append("  %s by the sorted glob" % record_mcp.DISCOVERY_HEADER)
    if det is not None:
        lines.append("%s%s" % (record_mcp.DET_PREFIX, det))
    if verdict:
        lines.append(verdict)
    for f in failures:
        lines.append("  X %s" % f)
    return "\n".join(lines)


def test_t20_each_failure_routes_to_its_leg():
    cases = [
        ("determinism: two builds differ logically", "1_determinism"),
        ("rulings from files the glob does not discover: ['x.md']", "0_discovery"),
        ("handoffs from files the glob does not discover: ['x.md']", "0_discovery"),
        ("count E14 numbered rulings: grep 35 != db 34", "2_counts"),
        ("E12 ruling sequence gaps [7]", "2_counts"),
        ("E12 handoff coverage unexpected: missing [1, 2]", "2_counts"),
        ("experiments missing ['E09']", "2_counts"),
        ("rulings: 4 dangling pointers", "3_pointers"),
        ("seeded question MISS: the hollow finding", "4_seeded"),
    ]
    for text, leg in cases:
        p = record_mcp.parse_verify(1, _fabricate("VERIFY FAILED - 1", [text]))
        assert p["state"] == "FAILED", text
        assert p["legs"][leg] == "FAILED", (text, leg, p["legs"])
        assert p["unattributed"] == [], (text, p["unattributed"])


def test_t20_an_unattributable_failure_cannot_become_a_pass():
    """The parse REFINES the verdict; it can never overturn it. A failure line
    no route matches lands in `unattributed` and the state stays FAILED."""
    p = record_mcp.parse_verify(
        1, _fabricate("VERIFY FAILED - 1", ["a failure mode invented in 2027"]))
    assert p["state"] == "FAILED"
    assert p["unattributed"] == ["a failure mode invented in 2027"]


def test_t20_a_lying_transcript_is_refused():
    """rc and the verdict line must agree. If they do not, the certificate says
    FAILED - a verifier that exits non-zero while printing PASSED is exactly the
    state nobody should serve from."""
    p = record_mcp.parse_verify(1, _fabricate("VERIFY PASSED - all four legs"))
    assert p["state"] == "FAILED"
    assert any("exited 1 while printing PASSED" in a for a in p["andon"]), p["andon"]

    p = record_mcp.parse_verify(0, _fabricate(verdict=""))
    assert p["state"] == "FAILED"
    assert any("no verify" in a or "verdict line" in a for a in p["andon"]), p["andon"]

    p = record_mcp.parse_verify(0, _fabricate(det=None))
    assert p["state"] == "FAILED"
    assert any("determinism-leg" in a for a in p["andon"]), p["andon"]

    p = record_mcp.parse_verify(0, "")
    assert p["state"] == "FAILED" and p["andon"]


def test_t20_a_clean_synthetic_transcript_does_parse():
    """Guard the guard: the fabricator above must be able to produce a PASS, or
    every negative case here is passing for the wrong reason."""
    p = record_mcp.parse_verify(0, _fabricate())
    assert p["state"] == "PASSED", p


# ---------------------------------------------------------------------------
# the sidecar
# ---------------------------------------------------------------------------

def test_t20_certificate_is_a_sidecar_and_leaves_the_db_untouched(tmp_path, built_db):
    """Section 4.4's whole reason: a certificate written INTO the DB would make
    the DB no longer a pure function of the corpus, and leg 1 would fail on its
    own output."""
    import hashlib
    import shutil
    import sqlite3

    db = os.path.join(str(tmp_path), "facet.db")
    shutil.copyfile(str(built_db), db)
    before = hashlib.sha256(open(db, "rb").read()).hexdigest()
    record_mcp.write_certificate(db, "test", PASSED_PARSE, SYNTHETIC_TRANSCRIPT)
    after = hashlib.sha256(open(db, "rb").read()).hexdigest()
    assert before == after, "writing the certificate changed the DB's bytes"

    assert os.path.exists(record_mcp.cert_path(db))
    assert record_mcp.cert_path(db) != db
    con = sqlite3.connect(db)
    names = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    con.close()
    assert not any("cert" in n.lower() or "health" in n.lower() for n in names), (
        "a certificate-shaped table exists in the DB: %s" % sorted(names))


def test_t20_certificate_is_ascii_bytes(tmp_path, built_db):
    """The record carries characters cp1252 cannot encode; a certificate that
    cannot be read back on the platform that wrote it is not a certificate."""
    db = certify(tmp_path, built_db)
    raw = open(record_mcp.cert_path(db), "rb").read()
    raw.decode("ascii")                              # raises if it is not
    assert b"\r\n" not in raw, "the certificate carries CRLF"
    doc = json.loads(raw.decode("ascii"))
    assert doc["schema"] == record_mcp.CERT_SCHEMA
    for key in ("state", "legs", "determinism_leg", "verified_utc", "db",
                "corpus", "transcript", "failures", "andon"):
        assert key in doc, "certificate has no %r" % key


def test_t20_certificate_records_the_corpus_by_content(tmp_path, built_db):
    db = certify(tmp_path, built_db)
    doc = load_cert(db)
    man = doc["corpus"]["manifest"]
    assert doc["corpus"]["files"] == len(man)
    assert "CLAUDE.md" in man and "README.md" in man
    assert any(k.startswith("profiles/") for k in man), sorted(man)[:5]
    assert doc["corpus"]["id"] == record_mcp._corpus_id(man)
    # content-derived, not git-derived: the digest is over the text the BUILDER
    # reads, so it moves on an uncommitted edit and does not move on a
    # line-ending change the builder normalises away
    live = record_mcp._corpus_manifest()
    assert man["CLAUDE.md"] == live["CLAUDE.md"]
    assert record_mcp._corpus_diff(man, dict(man, **{"CLAUDE.md": "0" * 64})) == {
        "added": [], "removed": [], "modified": ["CLAUDE.md"], "moved_total": 1}


def test_t20_a_failed_verify_still_writes_the_db_and_a_failed_certificate(
        tmp_path, built_db):
    """Section 3.3: 'A build whose verify fails still writes the DB - you cannot
    diagnose a failure you refused to produce - but the certificate records
    FAILED.'"""
    db = certify(tmp_path, built_db, parsed=FAILED_PARSE)
    assert os.path.exists(db), "the DB was removed on a failed certification"
    doc = load_cert(db)
    assert doc["state"] == "FAILED"
    assert doc["legs"]["3_pointers"] == "FAILED"
    assert doc["failures"] == ["rulings: 4 dangling pointers"]


@pytest.mark.fold
def test_t20_verify_then_build_in_one_process(tmp_path, monkeypatch, built_db):
    """The composition the CLI could never exercise, and the defect it hid.

    Found by E18's LIVE dogfood, not by this suite: `facet_index.verify` and
    `facet_index.claims` each opened a sqlite connection and never closed it.
    Harmless in a CLI that exits a millisecond later - fatal in a long-lived
    server, because `build` begins with `os.remove(db_path)` and Windows
    refuses to remove a file any handle still holds. record_build after
    record_verify died with PermissionError WinError 32 and surfaced as
    INTERNAL.

    So this runs the sequence in ONE interpreter, which is what a mounted
    session does all day: verify, claims, build, verify. A leaked handle fails
    it on Windows immediately; on a POSIX runner the removal succeeds anyway,
    so the assertion there is that the sequence completes and stays PASSED.
    """
    import shutil

    from mcp_support import bind_db

    db = os.path.join(str(tmp_path), "facet.db")
    shutil.copyfile(str(built_db), db)
    bind_db(monkeypatch, db)

    first = record_mcp.record_verify()
    assert first["state"] == "PASSED", first
    claims_out = record_mcp.record_claims()
    assert claims_out["exit_code"] == 0
    rebuilt = record_mcp.record_build()          # os.remove(db) happens here
    assert rebuilt["state"] == "PASSED", rebuilt
    again = record_mcp.record_verify()
    assert again["state"] == "PASSED", again


@pytest.mark.fold
def test_t20_build_runs_verify_and_writes_the_certificate(tmp_path, monkeypatch):
    """The E15 ritual is build + verify as ONE act (Ruling 4.1). This is the one
    test that runs the real thing end to end - three builds and four legs."""
    from mcp_support import bind_db

    db = os.path.join(str(tmp_path), "facet.db")
    bind_db(monkeypatch, db)
    res = record_mcp.record_build()
    assert res["built"] is True
    assert os.path.exists(db)
    assert os.path.exists(record_mcp.cert_path(db))
    assert res["state"] == "PASSED", res
    assert res["andon"] == [], res["andon"]
    assert res["counts"]["rulings"] > 0 and res["counts"]["fts"] > 0
    assert res["transcript_lines"] > 20, "verify's transcript was not captured"
    doc = load_cert(db)
    assert doc["verb"] == "record_build"
    assert doc["counts"] == res["counts"]
    assert doc["db"]["sha256"], "the certificate does not pin the DB it certifies"
