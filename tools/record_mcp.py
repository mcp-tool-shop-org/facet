#!/usr/bin/env python
"""record_mcp - the record-index MCP server (spec 1, E18).

WHAT THIS IS. A stdio MCP server that puts the derived index over this repo's
markdown record in front of a session, so the session QUERIES the record and
then reads the forty lines the query pointed at rather than the six hundred it
would have skimmed. The contract is docs/specs/index-mcp-spec.md; placement in
facet is docs/specs/placement-memo.md; the tool it productizes is
tools/facet_index.py, accepted at two seats under E15 Ruling 1.

THE DIFFERENTIATOR IS NOT THE INDEX - IT IS THAT A FAILING INDEX REFUSES TO
ANSWER. Three states, spec section 5:

  certificate PASSED, corpus unchanged   -> serves
  certificate PASSED, corpus has moved   -> serves WITH a staleness banner
                                            naming what moved
  certificate FAILED, or none at all     -> REFUSES, loudly, with a structured
                                            error naming the failing leg and
                                            the one command that fixes it

There is NO SKIP FLAG and adding one is out of scope permanently (E08 Amendment
32: a check a scripting accident can separate from the action it gates is not a
gate; 47,020 texels were committed after a fired ANDON because a shell chain
walked past an exit code). Here the gated step is ANSWERING A QUESTION, so the
check lives in the query path.

WHAT IT NEVER DOES. It never writes the corpus - not to fix a malformed heading,
not to normalise a date, not ever. Malformed-by-convention text is a REPORT
ITEM. This module writes exactly two paths, both derived and both regenerable:
the DB artifact and the certificate sidecar beside it. The corpus is opened
read-only on every path and the DB is opened through a `mode=ro` URI on every
read path; tests/test_t19_record_mcp_readonly.py greps this source with an AST
walk so the property is CHECKED, not promised (spec section 4.1).

THE CERTIFICATE IS A SIDECAR, NEVER A DB ROW (spec section 4.4). Writing the
health result into the DB would make the DB no longer a pure function of the
corpus and THE DETERMINISM LEG WOULD FAIL ON ITS OWN OUTPUT. It sits beside the
DB at <db>.cert.json, is pure ASCII bytes, and travels with the DB on the DB's
own commit cadence - so a fresh clone either carries a certificate or gets a
refusal until the standing kickoff build line runs.

CONVENTIONS ARE NOT OWNED HERE. facet_index carries them - the discovery globs,
the status-from-position rules, the ranking, the seeded question set with its
withdrawal history. This module binds them and adds none. Spec section 6's
config machinery is deliberately UNBUILT (the placement memo's ruling: config
for a user base of one is the speculative infrastructure the studio constitution
names by name); it stays in the spec as the contract extraction would honour.

WHAT WAS MEASURED, NOT ASSUMED, WHILE THIS WAS WRITTEN
  - the official SDK is `mcp` 2.0.0 (verified on PyPI 2026-08-08 and pinned in
    .github/workflows/ci.yml). `FastMCP` is GONE in 2.0.0; the high-level
    decorator server is `mcp.server.mcpserver.MCPServer`. Field names on the
    wire objects are snake_case (`is_error`, `server_info`).
  - `facet_index.verify()` returns an int and PRINTS its legs, so the
    certificate's per-leg detail is parsed from verify's own transcript. The
    VERDICT is read from the single line verify prints exactly once; the
    per-leg attribution only refines it and CANNOT turn a failure into a pass.
    A transcript this module cannot read is a FAILED certificate, never a
    silent one.

Standards compliance
  PIN_PER_STEP        every decision is pinned to its ruling or spec section in
                      the comment beside it; the SDK is pinned by version; the
                      DB stays a pure function of the corpus and this module
                      adds no tuning parameter to the build.
  ANDON_AUTHORITY     the health surface refuses rather than serving a suspect
                      citation, with no skip flag by construction; an
                      unparseable verify transcript refuses too.
  NAMED_COMPENSATORS  the two written paths are derived: re-run record_build
                      (leg 1 guarantees the DB comes back byte-identical) and
                      the certificate is rewritten by record_verify. Corpus
                      writes are impossible by construction, not undone.
  DECOMPOSE_BY_SECRETS conventions live in facet_index, the seeded set lives in
                      the corpus's own tool, the wire shape lives here.
  UNCERTAINTY_GATED_HUMANS every response carries the certificate state, not
                      only refusals; recorded retrieval boundaries surface in
                      `notes` instead of being engineered around.
  EXTERNAL_VERIFIER   this module grades nothing of its own: the verdict is
                      facet_index's four legs, whose leg-2 greps are written
                      independently of the parser and whose seeded key lives
                      outside this file.
"""
import argparse
import contextlib
import hashlib
import io
import json
import os
import pathlib
import re
import sqlite3
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import facet_index                                    # noqa: E402  the conventions

from mcp.server.mcpserver import MCPServer            # noqa: E402
from mcp.server.mcpserver.exceptions import ToolError  # noqa: E402
from mcp.types import ToolAnnotations                 # noqa: E402

REPO = facet_index.REPO
DB_DEFAULT = os.path.join(REPO, facet_index.DB_REL)
CERT_SUFFIX = ".cert.json"
CERT_SCHEMA = "facet-record-index-certificate/1"

# No version is claimed beyond a placeholder: this server publishes nothing and
# has no package. A real version attaches on the day extraction happens (spec
# section 12 / the placement memo's gated trigger), not before.
SERVER_VERSION = "0.0.0"

# The env var exists so tests and scratch runs bind a copy instead of the
# tracked artifact. It selects WHICH derived DB, never which corpus.
DB_ENV = "FACET_INDEX_DB"

FIX_COMMAND = "python tools/facet_index.py build   (or call record_build)"


# ---------------------------------------------------------------------------
# the structured error - the studio's ErrorShape, matching ollama-intern-mcp
# ---------------------------------------------------------------------------
#
# Loud rather than a flag on the payload (spec section 5): a caller that must
# read a field to discover the answer is untrustworthy will not read it. So a
# refusal is BOTH an MCP error result (is_error true on the wire) AND a
# structured body a program can parse - the human-readable head names the code
# and the fix, and the last line is the JSON object.

CODES = (
    "INDEX_VERIFY_FAILED",      # the certificate says a leg failed
    "INDEX_NEVER_VERIFIED",     # no certificate, an unreadable one, or one that
                                # describes a different DB than the one present
    "INDEX_MISSING",            # no DB artifact at all
    "CORPUS_NOT_FOUND",         # the repo this server binds is not the record
    "CONVENTIONS_INVALID",      # facet_index does not carry what this binds
    "SEEDED_SET_INVALID",       # the external verifier's key is unusable
    "ANCHOR_NOT_FOUND",         # record_get pointed at a row that is not there
    "BAD_ARGUMENT",             # an input outside the spec's stated bounds.
                                # ADDED beyond spec section 5's minimum set and
                                # flagged in the E18 report for the ruling: a
                                # tool that silently returns nothing for a
                                # typo'd table name is worse than one that says
                                # so, and the spec's set names failure modes of
                                # the index rather than of its inputs.
    "INTERNAL",                 # anything unexpected, wrapped rather than a raw
                                # stack (shipcheck gate B)
)


class RecordError(Exception):
    """A refusal with the studio's shape. Raised, never returned as a flag."""

    def __init__(self, code, message, hint, retryable=False):
        assert code in CODES, "unnamed error code: %s" % code
        self.code = code
        self.message = message
        self.hint = hint
        self.retryable = retryable
        Exception.__init__(self, message)

    def shape(self):
        return {"error": True, "code": self.code, "message": self.message,
                "hint": self.hint, "retryable": self.retryable}

    def loud(self):
        return (
            "REFUSED: %s\n"
            "  code:      %s\n"
            "  message:   %s\n"
            "  hint:      %s\n"
            "  retryable: %s\n"
            "%s"
            % (self.message, self.code, self.message, self.hint,
               "true" if self.retryable else "false",
               json.dumps(self.shape(), ensure_ascii=True, sort_keys=True)))


def _raise(err):
    """Every refusal leaves through here, so the wire shape has one site."""
    raise ToolError(err.loud())


# ---------------------------------------------------------------------------
# read-only access
# ---------------------------------------------------------------------------

def _ro_con(db_path):
    """The ONLY sqlite handle this module opens. `mode=ro` on every read path.

    A read-write handle here would make read-only-by-construction a policy
    instead of a property, and the AST guard in tests/test_t19 asserts this is
    the sole `sqlite3.connect` call site in the file.
    """
    uri = pathlib.Path(db_path).absolute().as_uri() + "?mode=ro"
    return sqlite3.connect(uri, uri=True)


def _sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# corpus identity - CONTENT-derived, never git-state-derived
# ---------------------------------------------------------------------------
#
# An uncommitted edit counts as moved (the kickoff pins this). The digest is
# taken over the text the BUILDER reads - facet_index.read normalises CRLF to
# LF - so a line-ending churn that cannot change the DB does not read as a
# corpus move either. The file set is facet_index's own: every markdown of the
# record plus the profiles whose registry becomes the decisions table.

def _corpus_files():
    return list(facet_index.record_markdown()) + list(facet_index.PROFILE_FILES)


def _corpus_manifest():
    """{rel: sha256} over the corpus as the builder reads it.

    CORPUS_NOT_FOUND rather than a stack trace when the bound repo is not the
    record: an empty enumeration or a missing CLAUDE.md means this server is
    pointed at something else, and guessing would be worse than refusing.
    """
    files = _corpus_files()
    if not files or not os.path.exists(os.path.join(REPO, "CLAUDE.md")):
        raise RecordError(
            "CORPUS_NOT_FOUND",
            "no record corpus under %s" % REPO,
            "This server binds facet's own conventions; run it from a checkout "
            "of the facet repo.")
    out = {}
    for rel in files:
        try:
            out[rel] = _sha256_bytes(facet_index.read(rel).encode("utf-8"))
        except OSError as exc:
            raise RecordError(
                "CORPUS_NOT_FOUND",
                "corpus file unreadable: %s (%s)" % (rel, exc.__class__.__name__),
                "The index enumerates this file; restore it or rebuild the "
                "index so the manifest matches the tree.")
    return out


def _corpus_id(manifest):
    payload = "".join("%s\0%s\n" % (k, manifest[k]) for k in sorted(manifest))
    return _sha256_bytes(payload.encode("utf-8"))


def _corpus_diff(old, new):
    """What moved, by name. A staleness banner that cannot name a file is a
    banner nobody can act on."""
    o, n = set(old), set(new)
    added = sorted(n - o)
    removed = sorted(o - n)
    modified = sorted(k for k in (o & n) if old[k] != new[k])
    return {"added": added, "removed": removed, "modified": modified,
            "moved_total": len(added) + len(removed) + len(modified)}


# ---------------------------------------------------------------------------
# the conventions this server binds - checked, not assumed
# ---------------------------------------------------------------------------

REQUIRED_CONVENTIONS = ("build", "verify", "query", "claims", "read",
                        "record_markdown", "PROFILE_FILES", "DB_REL", "REPO")


def _check_conventions():
    """CONVENTIONS_INVALID rather than an AttributeError three frames deep.

    Spec section 6 says a server refuses a repo that has not declared its
    conventions rather than guessing a pattern. Under in-facet placement the
    declaration IS facet_index, so this asserts that module still carries what
    this file binds - a rename there must fail here loudly, not silently.
    """
    missing = [n for n in REQUIRED_CONVENTIONS if not hasattr(facet_index, n)]
    if missing:
        raise RecordError(
            "CONVENTIONS_INVALID",
            "facet_index is missing %s" % ", ".join(missing),
            "The conventions module changed shape under this server; the "
            "server binds facet_index and declares none of its own.")
    seeded = getattr(facet_index, "SEEDED", None)
    if not seeded or not isinstance(seeded, (list, tuple)):
        raise RecordError(
            "SEEDED_SET_INVALID",
            "the seeded question set is empty or not a sequence",
            "Leg 4 is the external verifier; without its key `verify` proves "
            "nothing about retrieval. Restore SEEDED in tools/facet_index.py.")
    for row in seeded:
        if not (isinstance(row, (list, tuple)) and len(row) == 3):
            raise RecordError(
                "SEEDED_SET_INVALID",
                "malformed seeded row: %r" % (row,),
                "Each seeded row is (question, phrase, target). Withdrawals are "
                "removed with their history recorded, never left malformed.")


# ---------------------------------------------------------------------------
# verify's transcript -> the certificate's legs
# ---------------------------------------------------------------------------
#
# facet_index.verify() returns 0/1 and prints. Each pattern below is pinned to
# the print site that emits it; tests/test_t20 runs a REAL verify and asserts
# every one of them was found, so a wording change in facet_index fails here
# loudly instead of degrading the certificate quietly.

LEG_HEADERS = {
    "1_determinism": "[leg 1] determinism",
    "2_counts": "[leg 2] counts",
    "3_pointers": "[leg 3] pointers",
    "4_seeded": "[leg 4] the seeded question set",
}
DISCOVERY_HEADER = "[corpus] ruling documents discovered"
VERDICT_PASS = "VERIFY PASSED - all four legs"
VERDICT_FAIL = "VERIFY FAILED - "
DET_PREFIX = "determinism leg that held: "

# Failure text -> the leg it belongs to. Every entry names the fails.append()
# site in facet_index.verify that produces it.
FAIL_ROUTES = (
    ("determinism:", "1_determinism"),                    # leg 1, both builds differ
    ("rulings from files the glob", "0_discovery"),       # the inverse guard
    ("handoffs from files the glob", "0_discovery"),      # the inverse guard
    ("count ", "2_counts"),                               # grep != db
    ("sequence gaps", "2_counts"),
    ("E12 handoff coverage", "2_counts"),
    ("experiments missing", "2_counts"),
    ("dangling pointers", "3_pointers"),
    ("seeded question MISS:", "4_seeded"),
)
LEG_KEYS = ("0_discovery",) + tuple(LEG_HEADERS)


def parse_verify(rc, text):
    """verify's transcript -> {state, legs, determinism_leg, failures, andon}.

    THE VERDICT COMES FROM ONE LINE verify prints exactly once, and from its
    exit code; the per-leg attribution only refines that verdict. An
    unattributable failure line therefore cannot turn a FAILED into a PASSED -
    it lands in `unattributed` and the state stays FAILED.

    A transcript this cannot read is FAILED with an andon note. A parse that
    fell back to a shrug and served anyway would be the silent-pass class the
    whole health surface exists to prevent.
    """
    lines = text.splitlines()
    andon = []

    missing_headers = [k for k, h in LEG_HEADERS.items()
                       if not any(h in ln for ln in lines)]
    if missing_headers:
        andon.append("verify printed no header for: %s" % ", ".join(missing_headers))
    if not any(DISCOVERY_HEADER in ln for ln in lines):
        andon.append("verify printed no discovery audit")

    passed_line = any(ln.strip() == VERDICT_PASS for ln in lines)
    failed_line = any(ln.strip().startswith(VERDICT_FAIL) for ln in lines)
    if passed_line == failed_line:
        andon.append("verify printed %s verdict line"
                     % ("no" if not passed_line else "both a PASSED and a FAILED"))

    det = None
    for ln in lines:
        s = ln.strip()
        if s.startswith(DET_PREFIX):
            det = s[len(DET_PREFIX):].strip()
    if det is None:
        andon.append("verify printed no determinism-leg line")

    failures = [ln.strip()[2:].strip() for ln in lines if ln.strip().startswith("X ")]

    legs = dict.fromkeys(LEG_KEYS, "PASSED")
    unattributed = []
    for f in failures:
        for needle, key in FAIL_ROUTES:
            if needle in f:
                legs[key] = "FAILED"
                break
        else:
            unattributed.append(f)

    if rc != 0 and passed_line:
        andon.append("verify exited %d while printing PASSED" % rc)

    state = "PASSED" if (rc == 0 and passed_line and not failed_line
                         and not andon) else "FAILED"
    if state == "FAILED" and not failures and not andon:
        andon.append("verify exited %d with no failure lines" % rc)
    if state == "FAILED":
        for k in legs:
            if legs[k] == "PASSED" and (andon or unattributed):
                legs[k] = "UNKNOWN"

    # A .dump fallback is NOT a silent pass (spec section 3.4). It is a weaker
    # claim than byte-identity and the certificate says so in its own field.
    return {"state": state, "legs": legs, "determinism_leg": det,
            "failures": failures, "unattributed": unattributed,
            "andon": andon, "exit_code": rc}


def run_verify(db_path):
    """facet_index.verify with its transcript captured. Returns (rc, text)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = facet_index.verify(db_path)
    return rc, buf.getvalue()


def run_claims(db_path):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = facet_index.claims(db_path)
    return rc, buf.getvalue()


# ---------------------------------------------------------------------------
# the certificate
# ---------------------------------------------------------------------------

def cert_path(db_path):
    return db_path + CERT_SUFFIX


def write_certificate(db_path, verb, parsed, transcript, counts=None):
    """The ONLY write this module performs besides the DB facet_index builds.

    ASCII bytes by construction (`ensure_ascii=True`): the record carries
    characters a cp1252 console cannot encode, and a certificate that cannot be
    read back on the platform it was written on is not a certificate.
    """
    manifest = _corpus_manifest()
    doc = {
        "schema": CERT_SCHEMA,
        "written_by": "tools/record_mcp.py",
        "server_version": SERVER_VERSION,
        "verb": verb,
        "verified_utc": _now(),
        "state": parsed["state"],
        "determinism_leg": parsed["determinism_leg"],
        "legs": parsed["legs"],
        "failures": parsed["failures"],
        "unattributed_failures": parsed["unattributed"],
        "andon": parsed["andon"],
        "verify_exit_code": parsed["exit_code"],
        "db": {
            "path": os.path.relpath(db_path, REPO).replace("\\", "/")
                    if db_path.startswith(REPO) else db_path,
            "bytes": os.path.getsize(db_path) if os.path.exists(db_path) else None,
            "sha256": _sha256_file(db_path) if os.path.exists(db_path) else None,
        },
        "counts": counts,
        "corpus": {"files": len(manifest), "id": _corpus_id(manifest),
                   "manifest": manifest},
        "transcript": transcript.splitlines(),
    }
    path = cert_path(db_path)
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)                       # scripts create their own dirs
    with open(path, "w", encoding="ascii", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=True, indent=1, sort_keys=True)
        fh.write("\n")
    return doc


def read_certificate(db_path):
    """The certificate, or a RecordError naming which of the three states holds.

    Order matters and each step is its own refusal:
      1 no DB           -> INDEX_MISSING
      2 no/unreadable   -> INDEX_NEVER_VERIFIED  (a gate result nobody can read
        certificate         is not a gate result)
      3 state FAILED    -> INDEX_VERIFY_FAILED
      4 DB sha moved    -> INDEX_NEVER_VERIFIED  (the DB present is not the one
                                                  that was verified)
    """
    if not os.path.exists(db_path):
        raise RecordError(
            "INDEX_MISSING", "no index at %s" % db_path,
            "Run %s" % FIX_COMMAND, retryable=True)
    path = cert_path(db_path)
    if not os.path.exists(path):
        raise RecordError(
            "INDEX_NEVER_VERIFIED",
            "the index at %s carries no certificate" % db_path,
            "A DB somebody produced is not a verified DB. Run %s" % FIX_COMMAND,
            retryable=True)
    try:
        with open(path, "r", encoding="ascii") as fh:
            doc = json.load(fh)
        if not isinstance(doc, dict):
            raise ValueError("certificate is not an object")
        for k in ("schema", "state", "legs", "corpus", "db"):
            if k not in doc:
                raise ValueError("certificate has no %r" % k)
        if doc["schema"] != CERT_SCHEMA:
            raise ValueError("certificate schema %r, expected %r"
                             % (doc["schema"], CERT_SCHEMA))
        if not isinstance(doc["corpus"], dict) or "manifest" not in doc["corpus"]:
            raise ValueError("certificate carries no corpus manifest")
    except (ValueError, OSError, UnicodeDecodeError) as exc:
        raise RecordError(
            "INDEX_NEVER_VERIFIED",
            "the certificate at %s is unreadable: %s" % (path, exc),
            "An unreadable gate result is no gate result. Run %s" % FIX_COMMAND,
            retryable=True)
    if doc["state"] != "PASSED":
        legs = doc.get("legs") or {}
        bad = sorted(k for k, v in legs.items() if v != "PASSED")
        first = (doc.get("failures") or ["(no failure line recorded)"])[0]
        raise RecordError(
            "INDEX_VERIFY_FAILED",
            "%s: %s" % (", ".join(bad) or "verify", first),
            "Run %s. If it still fails, the corpus moved something a row points "
            "at - the failing rows are in the certificate's transcript."
            % FIX_COMMAND)
    live = _sha256_file(db_path)
    recorded = (doc.get("db") or {}).get("sha256")
    if recorded and live != recorded:
        raise RecordError(
            "INDEX_NEVER_VERIFIED",
            "the certificate describes a different index (certified %s..., "
            "present %s...)" % (recorded[:12], live[:12]),
            "This DB was not the one that was verified - a build without its "
            "verify is the ungated state the E15 ritual closes. Run %s"
            % FIX_COMMAND, retryable=True)
    return doc


def health(db_path):
    """The three-state surface, as a value. record_health reports it; every
    read tool gates on it. Never raises - it returns the refusal instead, so a
    caller can ASK what state the index is in without being refused."""
    try:
        _check_conventions()
        doc = read_certificate(db_path)
    except RecordError as err:
        return {"serving": False, "state": "REFUSING", "error": err.shape(),
                "certificate": None}
    try:
        live = _corpus_manifest()
    except RecordError as err:
        return {"serving": False, "state": "REFUSING", "error": err.shape(),
                "certificate": None}
    diff = _corpus_diff(doc["corpus"]["manifest"], live)
    stale = diff["moved_total"] > 0
    return {
        "serving": True,
        "state": "SERVING_STALE" if stale else "SERVING",
        "error": None,
        "certificate": {
            "state": doc["state"],
            "verified_utc": doc.get("verified_utc"),
            "determinism_leg": doc.get("determinism_leg"),
            "legs": doc.get("legs"),
            "verb": doc.get("verb"),
            "corpus_id_at_build": doc["corpus"].get("id"),
            "corpus_files_at_build": doc["corpus"].get("files"),
        },
        "corpus": {"id_now": _corpus_id(live), "files_now": len(live)},
        "staleness": _staleness(diff) if stale else None,
    }


STALE_NAMES = 12          # named files per class; the total is always exact


def _staleness(diff):
    """The banner. It NAMES what moved - spec section 5's own word - because a
    warning a session cannot act on is a warning it will learn to ignore.

    Staleness WARNS rather than refuses on purpose: the DB commits at session
    boundaries, not every fold (E15 Ruling 4.2), so bounded staleness is the
    ruled normal state of a fresh clone and a refusal there would fire on
    correct work. Put the andon on the direction the invariant does not bound.
    """
    def head(k):
        v = diff[k]
        return v[:STALE_NAMES] + (["... and %d more" % (len(v) - STALE_NAMES)]
                                  if len(v) > STALE_NAMES else [])
    parts = []
    for k in ("modified", "added", "removed"):
        if diff[k]:
            parts.append("%d %s (%s)" % (len(diff[k]), k, ", ".join(head(k))))
    return {
        "banner": "STALE INDEX: the corpus has moved since this index was built "
                  "- %s. Citations below are a faithful map of the OLDER record. "
                  "Run %s to refresh." % ("; ".join(parts), FIX_COMMAND),
        "modified": head("modified"), "added": head("added"),
        "removed": head("removed"),
        "counts": {k: len(diff[k]) for k in ("modified", "added", "removed")},
    }


def _gate(db_path):
    """Every read tool's first act. Returns the health block or REFUSES."""
    h = health(db_path)
    if not h["serving"]:
        e = h["error"]
        _raise(RecordError(e["code"], e["message"], e["hint"], e["retryable"]))
    return h


def _cert_block(h):
    """Every response carries the certificate state, not just refusals
    (spec section 8)."""
    block = {"state": h["state"], "certificate": h["certificate"]}
    if h.get("staleness"):
        block["staleness_banner"] = h["staleness"]["banner"]
        block["moved"] = h["staleness"]["counts"]
    return block


# ---------------------------------------------------------------------------
# the tool surface - spec section 3's table, exactly six
# ---------------------------------------------------------------------------

srv = MCPServer(
    name="facet-record",
    title="facet record index",
    version=SERVER_VERSION,
    instructions=(
        "Query this repo's governed decision record instead of reading it, then "
        "read the rows the query points at. The pointer is the product: every "
        "row carries file, line and anchor. A failing index REFUSES rather than "
        "answering, because a wrong citation is worse than no answer. Start with "
        "record_query; follow up with record_get on a row you want in full."))

TABLES = ("rulings", "laws", "experiments", "handoffs", "artifacts",
          "phenomena", "decisions", "prose")

# E15 Ruling 7: recorded boundaries are SURFACED, not engineered around.
BOUNDARY_NOTE = (
    "recorded boundary (E15 Ruling 7): the index serves the record's own "
    "vocabulary best. Content phrasings return their target at rank 1; "
    "conversational phrasings surface the evidence documents above the ruling. "
    "A report or kickoff ranked above a ruling here is the documented "
    "behaviour, not a defect - read down the page.")


def _db_path():
    return os.environ.get(DB_ENV) or DB_DEFAULT


def _need(cond, code, message, hint):
    if not cond:
        _raise(RecordError(code, message, hint))


@srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
def record_query(query: str, limit: int = 8, table: str | None = None,
                 arc: str | None = None) -> dict:
    """What did we decide about X, and where is it written.

    Ranked rows from the record's index; each carries file, line, anchor, table
    and a one-line holding. THE POINTER IS THE PRODUCT - the holding helps you
    choose among pointers, it is never a substitute for reading the row
    (follow up with record_get). Refuses if the index is not verified.

    query  a phrase, 1-500 chars; the record's own words work best
    limit  1-50, default 8
    table  optional: rulings laws experiments handoffs artifacts phenomena
           decisions prose
    arc    optional: an arc label such as E14, matched against the row's key
           and file
    """
    db = _db_path()
    _need(isinstance(query, str) and 1 <= len(query) <= 500, "BAD_ARGUMENT",
          "query must be 1-500 characters", "Shorten or supply the query.")
    _need(isinstance(limit, int) and 1 <= limit <= 50, "BAD_ARGUMENT",
          "limit must be between 1 and 50", "Pass limit within 1-50.")
    _need(table is None or table in TABLES, "BAD_ARGUMENT",
          "unknown table %r" % (table,), "Valid tables: %s" % ", ".join(TABLES))
    h = _gate(db)
    con = _ro_con(db)
    try:
        # The ranking mechanism ports UNTOUCHED (E15 Ruling 3: three variants
        # were scored on the fixed seeded key and two were falsified;
        # re-litigating it requires re-running that key). The over-fetch factor
        # is the CLI's own, so a filtered page matches what `q` prints.
        rows = facet_index.query(con, query, limit=limit * 6)
    finally:
        con.close()
    out = []
    for f, anchor, disp, line, tbl, rank in rows:
        if table and tbl != table:
            continue
        if arc and arc.lower() not in ("%s %s" % (f, anchor)).lower():
            continue
        out.append({"table": tbl, "anchor": anchor,
                    "holding": facet_index.one_line(disp or "", 240),
                    "bm25": round(rank, 4),
                    "file": f, "line": line,          # file:line LAST (section 8)
                    "locator": "%s:%d" % (f, line)})
        if len(out) >= limit:
            break
    notes = []
    tables = [r["table"] for r in out]
    # A ruling present but outranked by something that merely points at it is
    # the recorded behaviour, and the response says so rather than leaving the
    # caller to infer a defect.
    if "rulings" in tables and tables[0] != "rulings":
        notes.append(BOUNDARY_NOTE)
    if h.get("staleness"):
        notes.append(h["staleness"]["banner"])
    return {"query": query, "returned": len(out), "rows": out, "notes": notes,
            **_cert_block(h)}


# Block boundaries for record_get. Each is a shape the record actually uses -
# a markdown heading, a bold numbered lead (rulings and sub-rulings), a quoted
# amendment header, a rule. Bounding by the NEXT one keeps a row's own block
# and nothing else: the parent-does-not-re-index-its-children rule (spec
# section 6.3) applies to reading as much as to indexing.
#
# The dash class is written as \u escapes rather than as literal characters:
# the record uses the em dash, the en dash AND the hyphen (facet_index's own
# DASH constant says so), but this file must be ASCII BYTES - section 8's rule
# read at its strongest, and tests/test_t19 enforces it at the byte level. It
# fired on the first run of that test against this very line.
BLOCK_BOUNDARIES = (
    re.compile(r"^#{1,6} "),                    # any markdown heading
    re.compile(r"^\*\*[A-Za-z]?\d+[a-z]? *[\u2014\u2013-]"),   # 25c - / A32 -
    re.compile(r"^> #{1,6} "),                  # quoted amendment header
    re.compile(r"^-{3,}\s*$"),                  # horizontal rule
)
GET_DEFAULT_LINES = 120
GET_MAX_LINES = 400


@srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
def record_get(file: str, anchor: str | None = None, locator: str | None = None,
               max_lines: int = GET_DEFAULT_LINES) -> dict:
    """Give me the full text at this anchor.

    Takes a file plus an anchor (or a raw locator) from a record_query row and
    returns that row's own block from the MARKDOWN, bounded. It reads the
    CORPUS, not the DB's copy: the markdown is canonical and the DB is a map.
    This is what keeps the query -> read loop from opening a 2,000-line
    document to see forty lines.

    file       repo-relative, as printed by record_query
    anchor     the row's anchor, e.g. "Ruling 25c"
    locator    alternative to anchor: the exact findable string
    max_lines  1-400, default 120
    """
    db = _db_path()
    _need(isinstance(file, str) and file, "BAD_ARGUMENT", "file is required",
          "Pass the `file` value from a record_query row.")
    _need(anchor or locator, "BAD_ARGUMENT", "anchor or locator is required",
          "Pass the `anchor` value from a record_query row.")
    _need(isinstance(max_lines, int) and 1 <= max_lines <= GET_MAX_LINES,
          "BAD_ARGUMENT", "max_lines must be between 1 and %d" % GET_MAX_LINES,
          "Pass max_lines within 1-%d." % GET_MAX_LINES)
    h = _gate(db)

    row_line, tbl = None, None
    if locator is None:
        con = _ro_con(db)
        try:
            hit = con.execute(
                "SELECT locator, line, tbl FROM fts WHERE file=? AND anchor=? "
                "ORDER BY line LIMIT 1", (file, anchor)).fetchone()
        finally:
            con.close()
        if hit is None:
            _raise(RecordError(
                "ANCHOR_NOT_FOUND",
                "no row at %s :: %s" % (file, anchor),
                "Anchors come from record_query rows. If this one came from a "
                "query, the index moved under you - check record_health."))
        locator, row_line, tbl = hit

    try:
        lines = facet_index.lines_of(file)
    except OSError:
        _raise(RecordError(
            "ANCHOR_NOT_FOUND", "no corpus file at %s" % file,
            "The index points at a file that is not on disk; run record_verify "
            "- leg 3 is exactly this check."))

    start = None
    if row_line and 0 < row_line <= len(lines) and locator in lines[row_line - 1]:
        start = row_line - 1
    else:
        for i, ln in enumerate(lines):
            if locator in ln:
                start = i
                break
    if start is None:
        _raise(RecordError(
            "ANCHOR_NOT_FOUND",
            "locator %r is not in %s" % (locator, file),
            "The corpus moved the text this row points at. Run record_build; "
            "leg 3 reports every such row."))

    end = len(lines)
    for i in range(start + 1, min(len(lines), start + max_lines)):
        if any(rx.match(lines[i]) for rx in BLOCK_BOUNDARIES):
            end = i
            break
    else:
        end = min(len(lines), start + max_lines)
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1

    return {"table": tbl, "anchor": anchor, "locator": locator,
            "lines": end - start, "truncated": (end - start) >= max_lines,
            "text": "\n".join(lines[start:end]),
            "file": file, "start_line": start + 1, "end_line": end,
            **_cert_block(h)}


@srv.tool(annotations=ToolAnnotations(destructiveHint=False))
def record_build() -> dict:
    """Make the index current with the working tree.

    Regenerates the DB from scratch - never incremental, because the DB is a
    pure function of the corpus at a commit and an incremental update is a state
    machine that can drift. THEN RUNS THE FOUR VERIFY LEGS AND WRITES THE HEALTH
    CERTIFICATE BEFORE RETURNING: the E15 ritual is build + verify as ONE act
    (Ruling 4.1), and separating them in the product would re-open the gap the
    ritual closes. A build whose verify fails still writes the DB - you cannot
    diagnose a failure you refused to produce - but the certificate records
    FAILED and every read tool then refuses.
    """
    db = _db_path()
    try:
        _check_conventions()
        counts = facet_index.build(db, quiet=True)
    except RecordError as err:
        _raise(err)
    except Exception as exc:                       # noqa: BLE001 - wrapped, not raw
        _raise(RecordError("INTERNAL", "build failed: %s: %s"
                           % (exc.__class__.__name__, exc),
                           "This is a defect in the builder, not in the corpus; "
                           "run tools/facet_index.py build to see it directly."))
    rc, transcript = run_verify(db)
    parsed = parse_verify(rc, transcript)
    doc = write_certificate(db, "record_build", parsed, transcript, counts=counts)
    return {"built": True, "counts": counts,
            "certificate_path": os.path.relpath(cert_path(db), REPO).replace("\\", "/")
                                if cert_path(db).startswith(REPO) else cert_path(db),
            **_verify_result(doc, parsed)}


@srv.tool(annotations=ToolAnnotations(destructiveHint=False))
def record_verify() -> dict:
    """Is this index trustworthy.

    Runs the four legs against the DB as it stands and rewrites the certificate.
      leg 1 determinism  two builds from an unchanged corpus are byte-identical,
                         with a PRE-REGISTERED .dump fallback that is reported
                         as the weaker claim it is, never silently
      leg 2 counts       the verifier's OWN greps against the DB's counts, plus
                         sequence-gap and completeness checks
      leg 3 pointers     every row's file exists and its locator is findable
      leg 4 seeded set   each seeded question's known target ranks in the top 3
    Leg 2's greps are written independently of the parser's constants on
    purpose: the parser and the verifier must not be one implementation checking
    itself.
    """
    db = _db_path()
    try:
        _check_conventions()
    except RecordError as err:
        _raise(err)
    if not os.path.exists(db):
        _raise(RecordError("INDEX_MISSING", "no index at %s" % db,
                           "Run record_build first.", retryable=True))
    rc, transcript = run_verify(db)
    parsed = parse_verify(rc, transcript)
    doc = write_certificate(db, "record_verify", parsed, transcript)
    return _verify_result(doc, parsed)


TRANSCRIPT_TAIL = 15


def _verify_result(doc, parsed):
    """The write verbs' payload. The FULL transcript lives in the certificate -
    a fallback that is only visible in a response nobody kept is not reported."""
    h = health(_db_path())
    tail = doc["transcript"][-TRANSCRIPT_TAIL:]
    return {
        "state": doc["state"],
        "determinism_leg": doc["determinism_leg"],
        "legs": doc["legs"],
        "failures": doc["failures"],
        "unattributed_failures": parsed["unattributed"],
        "andon": doc["andon"],
        "corpus_files": doc["corpus"]["files"],
        "corpus_id": doc["corpus"]["id"],
        "transcript_lines": len(doc["transcript"]),
        "transcript_tail": tail,
        "health": {"state": h["state"], "serving": h["serving"],
                   "staleness_banner": (h.get("staleness") or {}).get("banner")},
    }


@srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
def record_health() -> dict:
    """What state is the index in right now.

    Cheap - it reads one small file and re-derives the corpus digest. Returns
    the certificate (which legs passed, when, which determinism leg held) plus
    the staleness state. This tool NEVER refuses: it is how you find out that
    the others are refusing, and why.
    """
    return health(_db_path())


@srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
def record_claims() -> dict:
    """Which current-state documents disagree with the record.

    The stale-claim sweep. REPORT-ONLY BY RULING and it never returns a failing
    exit code (E15 handoff 2 / Ruling 9b): its verdict swings on phrasing and on
    document class, and neither may decide a gate - a diagnostic and a gate are
    different objects. It reads the index's own measurements rather than
    re-deriving them, because a second derivation would be a second authority.
    Stale rows are the advisor's to rule, never this tool's to fix: it has no
    write path to a markdown file.
    """
    db = _db_path()
    h = _gate(db)
    rc, transcript = run_claims(db)
    lines = transcript.splitlines()
    summary = {}
    for key, prefix in (("stale", "STALE (current-state documents"),
                        ("ambiguous", "AMBIGUOUS (a modifier"),
                        ("unparseable", "UNPARSEABLE (count-claim-shaped")):
        for ln in lines:
            if ln.startswith(prefix):
                summary[key] = int(ln.rsplit(":", 1)[1].strip())
                break
    missing = [k for k in ("stale", "ambiguous", "unparseable") if k not in summary]
    stale_rows = []
    grab = False
    for ln in lines:
        if ln.startswith("STALE (current-state documents"):
            grab = True
            continue
        if grab:
            if not ln.strip():
                break
            stale_rows.append(ln.strip())
    return {"exit_code": rc, "gates": False, "summary": summary,
            "unreadable_summary_lines": missing,
            "stale_rows": stale_rows, "transcript": lines, **_cert_block(h)}


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def _print_tools():
    """The surface, printable without a client. ASCII on every print path."""
    print("facet record-index MCP - %d tools (spec docs/specs/index-mcp-spec.md)"
          % len(TOOL_ORDER))
    print("db: %s" % _db_path())
    print("certificate: %s" % cert_path(_db_path()))
    for name in TOOL_ORDER:
        fn = globals()[name]
        ann = "readOnlyHint" if name not in ("record_build", "record_verify") \
            else "destructiveHint: false"
        head = (fn.__doc__ or "").strip().splitlines()[0]
        print("  %-16s %-24s %s" % (name, ann, head))
    return 0


TOOL_ORDER = ("record_query", "record_get", "record_build", "record_verify",
              "record_health", "record_claims")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="the record-index MCP server over facet's markdown record")
    ap.add_argument("--db", default=None,
                    help="the derived index to serve (default %s, or $%s)"
                         % (facet_index.DB_REL, DB_ENV))
    ap.add_argument("--print-tools", action="store_true",
                    help="print the tool surface and exit; no server, no client")
    args = ap.parse_args(argv)
    if args.db:
        os.environ[DB_ENV] = os.path.abspath(args.db)
    if args.print_tools:
        return _print_tools()
    srv.run("stdio")
    return 0


if __name__ == "__main__":
    sys.exit(main())
