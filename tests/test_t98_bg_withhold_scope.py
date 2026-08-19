"""T98 - the head-band background withhold (E68) widened to every face (E69):
--bg-withhold-scope {headband,all}, default "headband".

Source: E69's own dispatch (docs/experiments/
E69-whole-figure-withhold-kickoff.md) and report
(docs/experiments/E69-whole-figure-withhold-report.md). The default scope
must reproduce E68's own recorded behavior EXACTLY (E68 itself added no
pytest coverage for its own flag; this closes that gap as a side effect of
covering what E69 adds, since both scopes share the same code path up to
the `hb` computation). `all` is a new, NOT-YET-ADOPTED mode (E69's charter:
prep restart is the Director's decision, not this session's) -- its own
measured withheld count is REPORTED, matching T11's precedent for an
unadopted mode, not strictly pinned. What IS strictly pinned for `all` is
the STRUCTURAL guarantee E69's report calls P1: the withhold predicate and
the ANDON's own re-test use the identical array and comparison, so the
post-withhold residual is 0.00% by construction, not by empirical luck --
a future change that breaks that identity should fail this test.

Single view (0) throughout, matching T11's cost discipline: every one of
these three invocations halts (or would halt on a wider view set) via the
SAME per-view ANDON, so one view exercises the code path fully without
paying for all 8.
"""
import re

import pytest

from conftest import need, run_py, REPO

PREP_REL = "facet_E67/prep"
VIEW0_REL = "facet_A1_accepted_ring/a1_v0.png"


def _run(assets, extra=()):
    prep = need(assets, PREP_REL)
    view0 = need(assets, VIEW0_REL)
    return run_py(
        "project_twins.py",
        ["--prep", prep, "--view", "0=%s" % view0, "--aspect", "576,1024",
         "--out", "UNUSED_atlas.png", *extra],
        cwd=None, timeout=600)


@pytest.mark.artifacts
@pytest.mark.slow
def test_t98_bare_default_halts_unchanged(assets, tmp_path):
    rc, out, err = _run(assets, extra=["--out", str(tmp_path / "atlas.png")])
    assert rc == 1, "bare default should still halt on view 0's ANDON (rc %d)\n%s\n%s" % (rc, out, err)
    assert "within dE 10 of it 30.29%" in out, (
        "recorded view-0 background-probe line missing or moved:\n%s" % out)
    assert "over the 2.0% limit" in (out + err), "ANDON message text moved:\n%s\n%s" % (out, err)


@pytest.mark.artifacts
@pytest.mark.slow
def test_t98_headband_scope_default_reproduces_e68(assets, tmp_path):
    """--headband-bg-withhold with NO --bg-withhold-scope (defaults to
    "headband") must reproduce E68's own recorded view-0 numbers exactly:
    4,380 of 146,546 (2.99%) withheld, 4.56% residual -- E68's report,
    per-view limit-comparison table, view 0."""
    rc, out, err = _run(assets, extra=[
        "--headband-bg-withhold", "--out", str(tmp_path / "atlas.png")])
    assert rc == 1, "headband-scope should still halt on view 0 (rc %d)\n%s\n%s" % (rc, out, err)
    assert ("head-band withhold — 4,380 of 146,546 head-band-accepted texels "
            "(2.99%)" in out), "E68's own recorded withhold line moved:\n%s" % out
    assert "within dE 10 of it 4.56%" in out, (
        "E68's own recorded residual percentage moved:\n%s" % out)


@pytest.mark.artifacts
@pytest.mark.slow
def test_t98_scope_all_widens_beyond_headband_and_passes(assets, tmp_path):
    """--bg-withhold-scope all must (a) actually widen -- the withhold line
    must name WHOLE-FIGURE and a larger accepted-texel denominator than the
    head-band's 146,546, and (b) the post-widen residual must be EXACTLY
    0.00%, not merely small -- P1's structural guarantee, not an empirical
    approximation (the withhold predicate and the ANDON's own re-test share
    the identical array and comparison once headband no longer gates it).
    Consequently the run must COMPLETE (rc 0), unlike every other
    invocation in this file and every recorded run before E69."""
    out_path = tmp_path / "atlas.png"
    rc, out, err = _run(assets, extra=[
        "--headband-bg-withhold", "--bg-withhold-scope", "all", "--out", str(out_path)])
    assert rc == 0, "scope=all should PASS the ANDON on view 0, not halt (rc %d)\n%s\n%s" % (rc, out, err)
    assert "WHOLE-FIGURE withhold" in out, "scope=all's own label missing:\n%s" % out
    assert "within dE 10 of it 0.00%" in out, (
        "P1's structural guarantee (exact zero residual) did not hold:\n%s" % out)
    m = re.search(r"WHOLE-FIGURE withhold — ([\d,]+) of ([\d,]+) WHOLE-FIGURE-accepted", out)
    assert m, "could not find the WHOLE-FIGURE withhold count line:\n%s" % out
    n_withheld = int(m.group(1).replace(",", ""))
    n_accepted = int(m.group(2).replace(",", ""))
    assert n_accepted > 146546, (
        "WHOLE-FIGURE-accepted (%d) should exceed the head-band-only denominator "
        "(146,546) -- if it does not, the scope did not actually widen" % n_accepted)
    # REPORTED, not strictly pinned -- this mode is adopted nowhere (E69's own
    # charter: the Director decides whether prep restarts). T11 set this
    # precedent for an unadopted mode's own measured numbers.
    print("T98 scope=all withheld %d of %d WHOLE-FIGURE-accepted texels on view 0 "
          "(E69's report recorded 4,918 of 436,490 against this exact recorded input)"
          % (n_withheld, n_accepted))
    assert out_path.exists(), "scope=all completed but wrote no atlas"


def test_t98_gateB_thresholds_unchanged_in_source():
    """Hermetic (no FACET_ASSETS needed): --bg-de and --bg-max-pct must
    still declare defaults 10.0 / 2.0 exactly once each in the live source.
    E69's charter: 'assert both byte-unchanged IN CODE and print them' --
    this is that assertion, kept runnable rather than left as a one-off
    session script."""
    src = (REPO / "tools" / "project_twins.py").read_text(encoding="utf-8")
    assert src.count('ap.add_argument("--bg-de"') == 1
    assert 'ap.add_argument("--bg-de", type=float, default=10.0,' in src
    assert src.count('ap.add_argument("--bg-max-pct"') == 1
    assert 'ap.add_argument("--bg-max-pct", type=float, default=2.0,' in src
