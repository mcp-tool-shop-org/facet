"""T5 - the claims sweep: report-only, 0 STALE on the current corpus, and its
parsing semantics exercised on synthetic fixtures.

Source: E15 Ruling 8a (the sweep, and why it never gates); E16-9/E16-11
(STALE: 0 measured on this corpus today).

The synthetic half feeds the sweep fabricated documents via monkeypatched
`record_markdown`/`lines_of` while the MEASUREMENTS stay real (the scratch
DB), so the semantics under test are the sweep's own wiring, not a re-
implementation of it:

  * range vs cardinal - `handoffs 1-N` asserts the highest number and is
    checked against MAX; `N handoffs` asserts how many exist and is checked
    against COUNT. E12 is the record's own motivating case (handoffs numbered
    to 16, only 15 exist - handoff 1 was never labelled), so conflating the
    two manufactures a stale row.
  * starts-at-1 - `Rulings 21-23` names three rulings and asserts nothing
    about the total: no claim row, and NOT unparseable either.
  * AMBIGUOUS - a modifier (`at least`, `so far`, `+ the close`, `or so`)
    makes the assertion unresolvable; it is reported, never resolved.
  * routing - the same wrong cardinal is STALE in a current-state document
    and as-of-writing in a historical one.
  * never gates - exit 0 even WITH a STALE row present.
"""
import re
import sqlite3

from conftest import run_py

STALE_PREFIX = "STALE (current-state documents disagreeing with the record):"
AMB_PREFIX = "AMBIGUOUS (a modifier makes the assertion unresolvable):"
UNPARSE_PREFIX = "UNPARSEABLE (count-claim-shaped, no family):"


def _summary_count(out, prefix, label):
    for ln in out.splitlines():
        if ln.startswith(prefix):
            return int(ln[len(prefix):].strip())
    raise AssertionError("%s: summary line %r not found in:\n%s" % (label, prefix, out))


def test_t05_current_corpus_zero_stale(built_db):
    rc, out, err = run_py("facet_index.py", ["claims", "--db", built_db])
    assert rc == 0, "claims must never gate (rc %d)\n%s\n%s" % (rc, out, err)
    assert _summary_count(out, STALE_PREFIX, "T5") == 0, (
        "STALE rows on the current corpus:\n%s" % out)


def test_t05_semantics_on_synthetic_fixtures(facet_index_mod, built_db, monkeypatch, capsys):
    m = facet_index_mod
    con = sqlite3.connect(str(built_db))
    h_count, h_max = con.execute(
        "SELECT COUNT(*), MAX(number) FROM handoffs WHERE arc='E12'").fetchone()
    con.close()
    assert h_count and h_max, "E12 handoffs missing from the scratch DB"

    current_state_rel = "README.md"                        # on the current-state list
    historical_rel = "docs/experiments/E99-synthetic-kickoff.md"  # a kickoff path
    fixture = {
        current_state_rel: [
            # range claim at the true MAX: ok (checked against max, not count)
            "The E12 arc carries handoffs 1-%d in the record." % h_max,
            # cardinal claim at the true COUNT: ok (checked against count)
            "The E12 arc carries %d handoffs in the record." % h_count,
            # wrong cardinal in a current-state document: STALE
            "The E12 arc carries %d handoffs in the record." % (h_count + 1),
            # an ambiguity modifier in the tail: AMBIGUOUS, never resolved
            "The E12 arc carries %d handoffs at least." % h_count,
            # a range that does not start at 1 asserts nothing about the
            # total: no claim row AND not unparseable
            "Rulings 21-23 of E12 discuss the twin registration.",
        ],
        historical_rel: [
            # the SAME wrong cardinal in a historical document: as-of-writing
            "The E12 arc carries %d handoffs in the record." % (h_count + 1),
        ],
    }
    monkeypatch.setattr(m, "record_markdown", lambda: list(fixture))
    monkeypatch.setattr(m, "lines_of", lambda rel: fixture[rel])

    rc = m.claims(str(built_db))
    out = capsys.readouterr().out

    assert rc == 0, "claims gated (rc %d) - it must always exit 0" % rc
    assert _summary_count(out, STALE_PREFIX, "T5-syn") == 1, out
    assert _summary_count(out, AMB_PREFIX, "T5-syn") == 1, out
    # starts-at-1: the 21-23 range produced neither a family row nor an
    # unparseable (if it had parsed as a range it would be a second STALE;
    # if it were merely claim-shaped it would appear here)
    assert _summary_count(out, UNPARSE_PREFIX, "T5-syn") == 0, out
    # the STALE row is the current-state document, line 3
    assert re.search(r"^   README\.md:3\s", out, re.M), (
        "STALE detail does not name README.md:3\n%s" % out)
    # the identical wrong claim in the historical document routed to
    # as-of-writing, not STALE
    assert re.search(
        r"^as-of-writing\s+historical\s.*E99-synthetic-kickoff\.md:1$", out, re.M), (
        "historical routing row not found\n%s" % out)
