"""T4 - document discovery and the inverse guard, proven able to fail.

Source: E16-9 (kickoff documents are discovered, not listed - and the glob
found the two E15 dispatches the hardcoded list had lost); E15 Ruling 8b /
9a's class for the ruling documents (a gate must test the operation's failure
mode - a list can show a listed file lost a row, never that a file was
missing from the list).

The synthetic miss is injected by E16-9's own method - a TRUNCATED discovered
list - never by writing a decoy .md into the shared working copy another
session builds from.

⚑ WHAT S02 MOVED, AND WHAT STAYED (2026-08-11). The index became a declaration
(`docs/index/conventions.json`) plus an adapter (`tools/facet_index.py`), and
the discovery machinery now lives in `record_index.parse.Record`. The split
this file was rewritten against is the one S02's closing Ruling 3 states: a
property that is FACET'S stays here re-pointed at the package, and a property
that is the PACKAGE'S retires in favour of the package's own suite rather than
being kept as a scan of a shim - because a test that scans a shim is green
rather than red, which is worse than absent.

  * KEPT, re-pointed: the glob's coverage of facet's real corpus, and the
    inverse guard run against facet's real declaration. A new facet document
    carrying `## Session handoff` that neither declared glob reaches still
    fires here, which is the whole reason the guard exists.
  * RETIRED: `test_t04_ruling_doc_miss_fails_verify`. It injected its miss by
    monkeypatching this module's `ruling_documents`, and `verify` no longer
    reads that name - it builds a fresh `Record` and calls the method on it, so
    the patch is a no-op and the leg measured nothing after the migration. The
    property is the package's orphan check and it is pinned there, on a corpus
    the package controls, by
    `record-index tests/test_verify.py::test_a_row_from_a_file_the_glob_does_not_discover_fails`.
    Re-pointing it here would mean facet's suite monkeypatching a method on
    `record_index.parse.Record` - facet asserting on another package's
    internals, which breaks on any refactor and still would not be facet's
    property.
"""
import pytest


def test_t04_discovery_covers_the_current_corpus(facet_index_mod):
    m = facet_index_mod
    rd = dict(
        (rel, arc) for arc, rel in m.ruling_documents())
    # known members, with the arc labels the derivation rule must preserve:
    # E10-offsurface must NOT merge into E10 (the load-bearing strip rule)
    assert rd.get("docs/experiments/E14-ruling.md") == "E14"
    assert rd.get("docs/experiments/E12-ruling.md") == "E12"
    assert rd.get("docs/experiments/E15-ruling.md") == "E15"
    assert rd.get("docs/experiments/E10-offsurface-ruling.md") == "E10-offsurface"
    hd = dict((rel, arc) for arc, rel in m.handoff_documents())
    # the file the old list was missing (E16-9's finding), plus the arcs
    # dispatched since - each arc keyed by leading E-number
    assert hd.get("docs/experiments/E15-context-index-kickoff.md") == "E15"
    assert hd.get("docs/experiments/E16-errands-kickoff.md") == "E16"
    assert hd.get("docs/experiments/E17-harness-kickoff.md") == "E17"


def test_t04_handoff_guard_passes_on_the_real_set(facet_index_mod):
    """Facet's own corpus, through facet's own declaration.

    ⚑ Called on the RECORD rather than on the module, and the two are not
    interchangeable. The module-level `handoff_documents` export returns
    `(arc, rel)` PAIRS for the surface this suite has always bound; the guard
    takes the `(arc, experiment, rel)` TRIPLES the record produces, because
    `experiment` is the grouping column the extraction added. Handing it pairs
    would unpack wrong rather than fail informatively.
    """
    rec = facet_index_mod.BINDING.record()
    rec.assert_no_undiscovered_handoffs(rec.handoff_documents())


def test_t04_handoff_guard_fires_on_a_synthetic_miss(facet_index_mod):
    """E16-9's demonstrated method verbatim: hand the guard a discovery list
    missing a file that carries `## Session handoff` headers.

    CAN-FAIL LEG for the one above - without it, a guard that had quietly
    become a no-op under the migration would pass on the real set forever.
    """
    rec = facet_index_mod.BINDING.record()
    full = rec.handoff_documents()
    target = "docs/experiments/E15-context-index-kickoff.md"  # carries TWO headers
    truncated = [row for row in full if row[-1] != target]
    assert len(truncated) == len(full) - 1, (
        "%s is not in the discovery set, so truncating it removes nothing"
        % target)
    with pytest.raises(AssertionError) as exc:
        rec.assert_no_undiscovered_handoffs(truncated)
    msg = str(exc.value)
    assert "ANDON" in msg and "E15-context-index-kickoff.md" in msg
