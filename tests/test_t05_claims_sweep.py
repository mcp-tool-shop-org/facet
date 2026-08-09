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

E26 Half B widened the SWEEP's scan set to the front-door files the index
deliberately does not index - CHANGELOG, SHIP_GATE, SCORECARD, SECURITY and the
published site handbook. The legs below pin the property that makes that safe:
`sweep_markdown()` is a strict superset of `record_markdown()`, and
`record_markdown()` still does NOT reach any of them, so the index build, its
FTS rows and verify's seeded rankings cannot move because a REPORT was widened.
The synthetic fixture now patches `sweep_markdown`, which is what the sweep
reads.
"""
import os
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
    monkeypatch.setattr(m, "sweep_markdown", lambda: list(fixture))
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


# ---------------------------------------------------------------------------
# E26 Half B - the widened scan set, and the index it must not disturb
# ---------------------------------------------------------------------------

def test_t05_sweep_scan_set_is_a_strict_superset_of_the_record(facet_index_mod):
    m = facet_index_mod
    rec, swp = set(m.record_markdown()), set(m.sweep_markdown())
    assert rec < swp, (
        "the sweep's scan set must strictly contain the record's - "
        "record %d files, sweep %d" % (len(rec), len(swp)))
    for rel in m.SWEEP_EXTRA:
        assert rel in swp, "%s is not in the sweep's scan set" % rel
    assert any(r.startswith("site/src/content/docs/") for r in swp), (
        "the published site handbook is not in the sweep's scan set")


def test_t05_the_index_still_does_not_reach_the_front_door(facet_index_mod):
    """Gate 4's property, kept runnable. `record_markdown()` feeds the index
    BUILD as well as the sweep; if the widening ever leaks into it, seven
    non-English translations and 2,768 lines of front-door prose join the FTS5
    index and move the seeded rankings verify's leg 4 gates on."""
    m = facet_index_mod
    rec = set(m.record_markdown())
    leaked = [rel for rel in m.SWEEP_EXTRA if rel in rec]
    leaked += [rel for rel in rec if rel.startswith("site/")]
    leaked += [rel for rel in rec if re.match(r"^README\.[a-zA-Z-]+\.md$", rel)]
    assert not leaked, (
        "the index's own file list has grown front-door files: %s"
        % ", ".join(sorted(set(leaked))))


def test_t05_changelog_splits_at_the_first_released_heading(facet_index_mod):
    """The rule E26 had to state: an entry under `## [x.y.z]` is correct
    forever, while `## [Unreleased]` above it is a current-state claim wearing a
    released entry's clothes. A file-scoped rule cannot express that."""
    m = facet_index_mod
    at = m._first_released_line("CHANGELOG.md")
    assert at is not None, "CHANGELOG.md has no released version heading"
    above, why_a = m.classify_document("CHANGELOG.md", at - 1)
    below, why_b = m.classify_document("CHANGELOG.md", at + 1)
    assert above == "current-state", "above the first release: %s (%s)" % (above, why_a)
    assert below == "historical", "inside a released entry: %s (%s)" % (below, why_b)


def test_t05_every_widened_surface_is_classified(facet_index_mod):
    """A swept file that lands `unclassified` is swept but not routed - its
    disagreements can never be STALE, so it is watched in appearance only."""
    m = facet_index_mod
    unclassified = []
    for rel in m.SWEEP_EXTRA:
        cls, _ = m.classify_document(rel, 1)
        if cls == "unclassified":
            unclassified.append(rel)
    for rel in m.sweep_markdown():
        if rel.startswith("site/src/content/docs/"):
            cls, _ = m.classify_document(rel, 1)
            if cls == "unclassified":
                unclassified.append(rel)
    assert not unclassified, (
        "widened surfaces with no classification: %s"
        % ", ".join(sorted(unclassified)))


def test_t05_widening_the_sweep_left_the_build_alone(facet_index_mod, built_db):
    """No front-door file reached the searchable index. This is the direct
    statement of what gate 4 measured by hand, and it is checked on the rows
    verify's leg 4 actually ranks: `fts`."""
    con = sqlite3.connect(str(built_db))
    n_fts = con.execute("SELECT COUNT(*) FROM fts").fetchone()[0]
    files = {r[0] for r in con.execute("SELECT DISTINCT file FROM fts")}
    con.close()
    assert n_fts > 0, "the scratch index has no fts rows to check"
    extra = set(facet_index_mod.SWEEP_EXTRA)
    strays = sorted(f for f in files
                    if f and (f.startswith("site/") or f in extra
                              or re.match(r"^README\.[a-zA-Z-]+\.md$", f)))
    assert not strays, (
        "front-door files reached the searchable index: %s" % strays)
