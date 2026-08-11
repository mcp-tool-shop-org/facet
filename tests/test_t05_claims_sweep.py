"""T5 - the claims sweep: report-only, 0 STALE on the current corpus, and the
widened scan set that must not disturb the index.

Source: E15 Ruling 8a (the sweep, and why it never gates); E16-9/E16-11
(STALE: 0 measured on this corpus today).

E26 Half B widened the SWEEP's scan set to the front-door files the index
deliberately does not index - CHANGELOG, SHIP_GATE, SCORECARD, SECURITY and the
published site handbook. The legs below pin the property that makes that safe:
`sweep_markdown()` is a strict superset of `record_markdown()`, and
`record_markdown()` still does NOT reach any of them, so the index build, its
FTS rows and verify's seeded rankings cannot move because a REPORT was widened.

⚑ WHAT S02 MOVED, AND WHAT STAYED (2026-08-11). The two lists this file read
off the module - `SWEEP_EXTRA` and `SWEEP_EXTRA_DIRS` - are DECLARED fields now
(`corpora.sweep_extra_files` and `corpora.sweep_extra_dirs` in
`docs/index/conventions.json`), carrying the same four filenames and the same
one directory. The legs below read the declaration, so they check the thing
facet actually states rather than a constant that happened to agree with it.

  * RETIRED: `test_t05_semantics_on_synthetic_fixtures`. It fed the sweep
    fabricated documents by monkeypatching this module's `sweep_markdown` and
    `lines_of`, and `claims` no longer reads either name - it builds a fresh
    `Record` and asks that. The patch became a no-op, so the leg exercised
    nothing but the real corpus wearing a fixture's name. Every semantic it
    covered is pinned in `record-index tests/test_claims.py`, on that package's
    own two fixture repos, one clause per test:

      range vs cardinal  test_a_current_state_document_disagreeing_with_the_record_is_stale
      starts-at-1        test_a_range_that_does_not_start_at_one_is_not_a_count_claim
      AMBIGUOUS          test_a_modifier_makes_an_assertion_ambiguous_rather_than_resolved
      routing            test_a_historical_document_disagreeing_is_as_of_writing_and_not_stale
      unparseable        test_a_count_claim_no_family_parses_is_reported_not_guessed_at
      never gates        test_the_sweep_exits_zero_with_stale_rows_on_the_record

    Rebuilding them here would mean facet's suite re-asserting another
    package's parser against fixtures facet does not own. What facet keeps is
    the leg that reads facet's OWN corpus and requires STALE: 0.
"""
import re
import sqlite3

from record_index import claims as _pkg_claims

from conftest import run_py

STALE_PREFIX = "STALE (current-state documents disagreeing with the record):"
AMB_PREFIX = "AMBIGUOUS (a modifier makes the assertion unresolvable):"
UNPARSE_PREFIX = "UNPARSEABLE (count-claim-shaped, no family):"


def _sweep_extra(m):
    """The extra files facet DECLARES the sweep reads, from its declaration.

    Read rather than transcribed: a list repeated in this file would be a
    second surface for one fact, and the first thing it would do is drift from
    `conventions.json` without either copy noticing.
    """
    return list(m.CONV.sweep_extra_files)


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


# ---------------------------------------------------------------------------
# E26 Half B - the widened scan set, and the index it must not disturb
# ---------------------------------------------------------------------------

def test_t05_sweep_scan_set_is_a_strict_superset_of_the_record(facet_index_mod):
    m = facet_index_mod
    rec, swp = set(m.record_markdown()), set(m.sweep_markdown())
    assert rec < swp, (
        "the sweep's scan set must strictly contain the record's - "
        "record %d files, sweep %d" % (len(rec), len(swp)))
    declared = _sweep_extra(m)
    assert declared, (
        "facet declares no corpora.sweep_extra_files, so this leg would pass "
        "on an empty loop - the check must have something to check")
    for rel in declared:
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
    leaked = [rel for rel in _sweep_extra(m) if rel in rec]
    leaked += [rel for rel in rec if rel.startswith("site/")]
    leaked += [rel for rel in rec if re.match(r"^README\.[a-zA-Z-]+\.md$", rel)]
    assert not leaked, (
        "the index's own file list has grown front-door files: %s"
        % ", ".join(sorted(set(leaked))))


def test_t05_changelog_splits_at_the_first_released_heading(facet_index_mod):
    """The rule E26 had to state: an entry under `## [x.y.z]` is correct
    forever, while `## [Unreleased]` above it is a current-state claim wearing a
    released entry's clothes. A file-scoped rule cannot express that.

    ⚑ The SPLITTER is the package's and is pinned there on the package's own
    fixture (`test_the_changelog_splits_at_its_first_release`); the SUBJECT here
    is facet's real CHANGELOG.md, which is what this leg is for and what that
    one cannot see. Calling the package's private locator is deliberate rather
    than incidental: re-deriving "where is the first released heading" in this
    file would make the leg agree with itself instead of with the tool, which
    is the fixture-side check-that-cannot-fail.
    """
    m = facet_index_mod
    at = _pkg_claims._first_released_line(m.BINDING.record(), "CHANGELOG.md")
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
    for rel in _sweep_extra(m):
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
    extra = set(_sweep_extra(facet_index_mod))
    strays = sorted(f for f in files
                    if f and (f.startswith("site/") or f in extra
                              or re.match(r"^README\.[a-zA-Z-]+\.md$", f)))
    assert not strays, (
        "front-door files reached the searchable index: %s" % strays)
