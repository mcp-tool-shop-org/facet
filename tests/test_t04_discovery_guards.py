"""T4 - document discovery and BOTH inverse guards, proven able to fail.

Source: E16-9 (kickoff documents are discovered, not listed - and the glob
found the two E15 dispatches the hardcoded list had lost); E15 Ruling 8b /
9a's class for the ruling documents (a gate must test the operation's failure
mode - a list can show a listed file lost a row, never that a file was
missing from the list).

The synthetic miss is injected by E16-9's own method - a TRUNCATED discovered
list - never by writing a decoy .md into the shared working copy another
session builds from.
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


def test_t04_ruling_doc_miss_fails_verify(facet_index_mod, built_db, monkeypatch, capsys):
    """The rulings-side inverse guard lives inside verify (the orphans check):
    rows indexed from a file the glob no longer discovers must FAIL the run."""
    m = facet_index_mod
    full = m.ruling_documents()
    dropped = [(a, r) for a, r in full if r != "docs/experiments/E14-ruling.md"]
    assert len(dropped) == len(full) - 1, "E14-ruling.md was not in the discovery set"
    monkeypatch.setattr(m, "ruling_documents", lambda: dropped)
    rc = m.verify(str(built_db))
    out = capsys.readouterr().out
    assert rc == 1, "verify returned %d on a synthetic undiscovered-file miss" % rc
    assert "ROWS FROM UNDISCOVERED FILES" in out
    assert "E14-ruling.md" in out, "the miss report does not name the dropped file"


def test_t04_handoff_guard_passes_on_the_real_set(facet_index_mod):
    m = facet_index_mod
    m.assert_no_undiscovered_handoffs(m.handoff_documents())


def test_t04_handoff_guard_fires_on_a_synthetic_miss(facet_index_mod):
    """E16-9's demonstrated method verbatim: hand the guard a discovery list
    missing a file that carries `## Session handoff` headers."""
    m = facet_index_mod
    full = m.handoff_documents()
    target = "docs/experiments/E15-context-index-kickoff.md"  # carries TWO headers
    truncated = [(a, r) for a, r in full if r != target]
    assert len(truncated) == len(full) - 1
    with pytest.raises(AssertionError) as exc:
        m.assert_no_undiscovered_handoffs(truncated)
    msg = str(exc.value)
    assert "ANDON" in msg and "E15-context-index-kickoff.md" in msg
