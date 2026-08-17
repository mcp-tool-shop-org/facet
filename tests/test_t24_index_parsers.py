"""T24 (E20 U1) - facet_index's parsers, unit level, on fixture strings.

WHY BELOW THE REPLAY LEVEL. T1 replays the whole build and adjudicates ~1,500
pointers, so the mainline heading forms are densely anchored - but only through
the front door. These conventions ARE the law the record is written in, and
their edge cases are where the law lives: the one closure marker that is not a
sub-ruling, the arc label that must not merge, the lower-case "accepted" that is
an adjective. None of that had a test naming it.

THE ASSERTION LAW (E20 kickoff). Every expectation here is pinned to a source
the tool itself carries - a MEASURED comment, a documented convention, or a
mathematical property - and each test names which. Where a probe revealed
behavior this session could not trace to an anchor, it is reported as a finding
in E20-coverage-report.md and NO test pins it either way.

The functions are reached through conftest's `facet_index_mod` fixture (import
has no side effects - facet_index guards main; measured before that fixture was
written). SOURCE IS ASCII BYTES: the record uses all three dashes, so they are
written as \\u escapes rather than typed. That is E18's D2 lesson one file over,
and this file paid for it twice - a post-hoc converter truncated the first draft
to zero bytes, because "w" truncates before the encode raises.
"""
import re
import sqlite3

import pytest

# Built with chr() rather than typed, so the SOURCE stays ASCII bytes while the
# VALUES are the real characters the record uses. Spelling them as "--" would
# quietly weaken every dash test below: the dash class is one character, so a
# two-hyphen stand-in still matches on its first hyphen and the em-dash case
# would never actually be exercised. Caught in this file, one draft in.
EM = chr(0x2014)      # em dash
EN = chr(0x2013)      # en dash
ELL = chr(0x2026)     # the ellipsis one_line appends
WARN = chr(0x26A0)    # the warning glyph E08 puts in some amendment headers


# ---------------------------------------------------------------------------
# the arc-label derivations, and the asymmetry between them
# ---------------------------------------------------------------------------
# ANCHOR: ruling_documents' own docstring - "THE ARC LABEL IS DERIVED BY
# STRIPPING FROM `ruling` ONWARD ... `E10-offsurface-ruling.md` must stay its own
# arc. Keyed on the E-number alone it would merge into `E10`, and twelve rulings
# and seven rulings would collide on numbers 1-7 - a primary-key failure."

def test_t24_ruling_arc_labels_are_unique(facet_index_mod):
    """The property the derivation exists to protect, not a list of labels.

    Asserting the label set itself would pin the corpus; asserting uniqueness
    pins the primary-key invariant, which is what the docstring says the rule is
    for. It also stays true as the record grows, which a length would not.
    """
    docs = facet_index_mod.ruling_documents()
    arcs = [arc for arc, _ in docs]
    dupes = sorted({a for a in arcs if arcs.count(a) > 1})
    assert not dupes, (
        "two ruling documents share an arc label %s - rulings from different "
        "documents would collide on numbers 1-N, the primary-key failure the "
        "stripping derivation exists to prevent" % dupes)


def test_t24_the_e10_offsurface_collision_is_the_reason(facet_index_mod):
    """E10 and E10-offsurface are DISTINCT arcs, both present.

    The named case in the docstring. If these ever merge, the uniqueness test
    above fails too - this one says which pair did it and why it matters.
    """
    by_file = {rel: arc for arc, rel in facet_index_mod.ruling_documents()}
    plain = by_file.get("docs/experiments/E10-ruling.md")
    offs = by_file.get("docs/experiments/E10-offsurface-ruling.md")
    assert plain == "E10", "E10-ruling.md derived arc %r" % plain
    assert offs == "E10-offsurface", (
        "E10-offsurface-ruling.md derived arc %r - stripped to the E-number it "
        "would merge into E10 and collide on numbers 1-7" % offs)


def test_t24_handoff_arc_is_the_leading_e_number_deliberately(facet_index_mod):
    """The OPPOSITE rule, and its docstring says why it is not a bug.

    handoff_documents does NOT strip from the keyword: doing so would yield
    `E04-executor` and `E15-context-index`, "labels the handoffs table has never
    used and which would break every existing anchor". The asymmetry is the
    anchored behavior, so this pins it as such.
    """
    by_file = {rel: arc for arc, rel in facet_index_mod.handoff_documents()}
    got = by_file.get("docs/experiments/E15-context-index-kickoff.md")
    assert got == "E15", (
        "kickoff arc derived as %r; the leading E-number is the anchored rule "
        "here (see handoff_documents' docstring)" % got)


@pytest.mark.parametrize("fn,is_ruling,is_kickoff", [
    ("E14-ruling.md", True, False),
    ("E10-offsurface-ruling.md", True, False),
    ("E08-director-canon-ruling.md", True, False),
    ("E20-coverage-kickoff.md", False, True),
    ("E15-context-index-kickoff.md", False, True),
    # near-misses: the patterns are anchored at the start and need two digits
    ("ruling.md", False, False),
    ("E1-ruling.md", False, False),
    ("notes-E14-ruling.md", False, False),
    ("E14-report.md", False, False),
])
def test_t24_discovery_patterns_admit_and_reject(facet_index_mod, fn,
                                                 is_ruling, is_kickoff):
    """ANCHOR: the patterns themselves plus E16-9's discovery law (kickoffs are
    DISCOVERED, not listed). The near-misses are the half nobody tests."""
    assert bool(facet_index_mod.RULING_DOC_RE.match(fn)) is is_ruling
    assert bool(facet_index_mod.KICKOFF_DOC_RE.match(fn)) is is_kickoff


# ---------------------------------------------------------------------------
# the measured marker convention, and its ONE closure exception
# ---------------------------------------------------------------------------
# ANCHOR: the comment above SUB_RULING, which states the measurement - "across
# all five ruling documents the lettered marker is `**<n><letter> <dash>` -
# letter, SPACE, dash - 151 times out of 152. The single exception is not a
# sub-ruling at all but a CLOSURE marker ... A dash class that tolerates a bare
# hyphen swallows it into 18g and loses one of the two holdings."

CLOSURE_LINE = '**18g-CLOSED (Director, 2026-08-06): "Keep ivory, judge on asset."'


@pytest.mark.parametrize("line,num,letter", [
    ("**25c " + EM + " dark desaturated crevice", "25", "c"),
    ("**7a " + EN + " the elevated cameras are closed", "7", "a"),
    ("**3b - a bare hyphen is in the dash class", "3", "b"),
    ("**16c  " + EM + " extra space before the dash", "16", "c"),
])
def test_t24_sub_ruling_matches_the_measured_form(facet_index_mod, line, num, letter):
    m = facet_index_mod.SUB_RULING.match(line)
    assert m, "SUB_RULING did not match the measured form: %r" % line
    assert m.group(1) == num and m.group(2) == letter


def test_t24_the_closure_marker_is_not_a_sub_ruling(facet_index_mod):
    """The 1-of-152 exception, both directions.

    This is the assertion the comment's reasoning demands: if SUB_RULING matched
    the closure line, 18g would swallow the Director's own sentence and one of
    the two holdings would be lost.
    """
    assert not facet_index_mod.SUB_RULING.match(CLOSURE_LINE), (
        "SUB_RULING matched the closure marker - it would swallow it into 18g "
        "and lose one of the two holdings (the measured 1-of-152 exception)")
    m = facet_index_mod.SUB_CLOSURE.match(CLOSURE_LINE)
    assert m, "SUB_CLOSURE did not match its own case: %r" % CLOSURE_LINE
    assert (m.group(1), m.group(2), m.group(3)) == ("18", "g", "CLOSED")


def test_t24_the_space_before_the_dash_is_required(facet_index_mod):
    """No space means not a sub-ruling. That is what makes the closure form
    separable at all."""
    assert not facet_index_mod.SUB_RULING.match("**18g" + EM + " no space"), (
        "SUB_RULING matched without the space the measurement requires")


@pytest.mark.parametrize("line,num", [
    ("## Ruling 25 " + EM + " the thing", "25"),
    ("## Ruling 3", "3"),
])
def test_t24_ruling_header(facet_index_mod, line, num):
    m = facet_index_mod.RULING_HDR.match(line)
    assert m and m.group(1) == num


def test_t24_amendment_header_tolerates_the_warning_glyph(facet_index_mod):
    """ANCHOR: AMEND_HDR's own optional warning-glyph group - E08 writes both."""
    plain = "> ### Amendment 32 (2026-08-07): the check lives in the tool"
    warned = "> ### " + WARN + " Amendment 27 (2026-08-06): the trust mask"
    for line, num in ((plain, "32"), (warned, "27")):
        m = facet_index_mod.AMEND_HDR.match(line)
        assert m, "AMEND_HDR did not match %r" % line
        assert m.group(1) == num


def test_t24_handoff_header_accepts_the_unnumbered_form(facet_index_mod):
    """ANCHOR: parse_handoffs' docstring - E04's first handoff carries NO number
    and "is recorded as number `1` with its unnumbered form kept in the locator,
    because dropping a real dispatch to satisfy a regex would lose a row"."""
    numbered = "## Session handoff 7 (2026-08-06) " + EM + " the stroke"
    bare = "## Session handoff (2026-08-04, evening) " + EM + " SUPERSEDED"
    m = facet_index_mod.HANDOFF_HDR.match(numbered)
    assert m and m.group(1) == "7"
    m = facet_index_mod.HANDOFF_HDR.match(bare)
    assert m, "HANDOFF_HDR rejected the unnumbered form - the row would be lost"
    assert m.group(1) == "", "expected an empty number group, got %r" % m.group(1)


# ---------------------------------------------------------------------------
# the status-position law: capitals carry verdicts
# ---------------------------------------------------------------------------
# ANCHOR: classify's docstring, which carries the bug it fixed - "An earlier
# version of this function upper-cased the holding first and so marked three
# rulings ACCEPTED that accept nothing, which put two of them above the actual
# acceptance in the ranking. Match case-sensitively."

def test_t24_capitals_carry_the_verdict(facet_index_mod):
    v, auth = facet_index_mod.classify("THE PAIR IS ACCEPTED at the Director's word")
    assert v == "ACCEPTED"
    assert auth == "Director"


def test_t24_lower_case_accepted_is_an_adjective(facet_index_mod):
    """The exact sentence the docstring names as the case that broke the ranking."""
    v, auth = facet_index_mod.classify(
        "D9's wine has no cluster on the accepted pair")
    assert v is None, (
        "lower-case 'accepted' read as a verdict %r - this is the adjectival "
        "case classify's docstring says cost three false ACCEPTEDs" % v)
    assert auth == "advisor"


def test_t24_authority_defaults_to_the_advisor(facet_index_mod):
    assert facet_index_mod.classify("the blade is REJECTED") == ("REJECTED", "advisor")


def test_t24_verdict_order_is_most_to_least_specific(facet_index_mod):
    """ANCHOR: the comment above VERDICTS - "Ordered most- to least specific;
    the first hit in the holding wins." A holding carrying both ACCEPTED and
    RULED is an acceptance, whichever word came first in the text."""
    assert facet_index_mod.classify("this is RULED and the pair is ACCEPTED")[0] \
        == "ACCEPTED"
    idx = facet_index_mod.VERDICTS.index
    assert idx("ACCEPTED") < idx("RULED"), (
        "VERDICTS order changed; the first-hit-wins rule now resolves "
        "differently and this expectation is stale")


def test_t24_a_verdict_needs_word_boundaries(facet_index_mod):
    assert facet_index_mod.classify("UNACCEPTEDX nonsense")[0] is None
    assert facet_index_mod.classify("the CLOSED gate")[0] == "CLOSED"


# ---------------------------------------------------------------------------
# paragraphs / bold_lead_title - the discriminator that keeps prose out
# ---------------------------------------------------------------------------
# ANCHOR: paragraphs' docstring - "A paragraph boundary is a blank line. This is
# the discriminator that keeps a wrapped `**word**` mid-sentence from being read
# as a bold-lead heading - CLAUDE.md:141 is exactly that case."

def test_t24_paragraphs_split_on_blank_lines_with_true_line_numbers(facet_index_mod):
    block = ["first para", "still first", "", "second para", "", "", "third"]
    got = facet_index_mod.paragraphs(block, 10)
    assert got == [
        (10, ["first para", "still first"]),
        (13, ["second para"]),
        (16, ["third"]),
    ], got


def test_t24_paragraphs_handles_leading_and_trailing_blanks(facet_index_mod):
    assert facet_index_mod.paragraphs(["", "x", ""], 1) == [(2, ["x"])]
    assert facet_index_mod.paragraphs([], 5) == []
    assert facet_index_mod.paragraphs(["", ""], 5) == []


def test_t24_bold_lead_closes_across_wrapped_lines(facet_index_mod):
    """ANCHOR: bold_lead_title's docstring - the bold run "may span several
    wrapped lines ... so the closing `**` is searched across the whole
    paragraph"."""
    par = ["**27d " + EM + " THE FIFTH SIGNATURE IS NAMED FORWARD: dark",
           "desaturated crevice** and then the body follows"]
    title, rest = facet_index_mod.bold_lead_title(par)
    assert title == ("27d " + EM + " THE FIFTH SIGNATURE IS NAMED FORWARD: dark\n"
                     "desaturated crevice")
    assert rest.startswith(" and then the body")


def test_t24_a_paragraph_not_opening_in_bold_is_not_a_title(facet_index_mod):
    assert facet_index_mod.bold_lead_title(
        ["ordinary prose with **bold** inside"]) == (None, None)


def test_t24_an_unclosed_bold_run_is_not_a_title(facet_index_mod):
    """A check that can fail: an opener with no closer must return (None, None)
    rather than swallowing the rest of the document as a title."""
    assert facet_index_mod.bold_lead_title(["**opened and never closed"]) \
        == (None, None)


# ---------------------------------------------------------------------------
# the small text utilities every holding passes through
# ---------------------------------------------------------------------------

def test_t24_one_line_collapses_and_trims(facet_index_mod):
    assert facet_index_mod.one_line("  a\n  b   c \n") == "a b c"
    assert facet_index_mod.one_line("trailing dot.") == "trailing dot"


def test_t24_one_line_truncates_at_the_limit_with_an_ellipsis(facet_index_mod):
    out = facet_index_mod.one_line("x" * 300)
    assert len(out) == 240, len(out)
    assert out.endswith(ELL)
    short = facet_index_mod.one_line("abc", limit=10)
    assert short == "abc" and not short.endswith(ELL)


def test_t24_one_line_boundary_is_exact(facet_index_mod):
    """At exactly the limit nothing is cut; one over and it is."""
    assert facet_index_mod.one_line("y" * 240) == "y" * 240
    assert facet_index_mod.one_line("y" * 241).endswith(ELL)


def test_t24_strip_md_removes_markup_not_words(facet_index_mod):
    got = facet_index_mod.strip_md(
        "a `code` and **bold** and *em* and [link](http://x) and > quote")
    assert got == "a code and bold and em and link and   quote", repr(got)


def test_t24_github_slug_lowercases_and_strips_markup(facet_index_mod):
    """Only the parts the implementation states as its own intent are pinned.

    NOT PINNED, DELIBERATELY: whether the output equals GitHub's slug for a
    heading whose words are separated by a dash. This function collapses
    whitespace RUNS (`\\s+` -> one hyphen), so `Ruling 25 -- The Thing` loses the
    dash and yields ONE hyphen where a per-space replacement would yield two.
    Which is correct is a claim about an external renderer that this session
    could not verify offline, and `github_slug` has NO CALLER in tools/ or
    tests/, so nothing in the repo depends on the answer today. Reported as a
    finding in E20-coverage-report.md; the assertion law forbids pinning it
    either way before the ruling.
    """
    slug = facet_index_mod.github_slug("## `Ruling` **25** The Thing (2026-08-06)")
    assert slug.islower() or slug == slug.lower()
    assert "`" not in slug and "*" not in slug
    assert "(" not in slug and ")" not in slug
    assert " " not in slug
    assert "ruling" in slug and "25" in slug and "2026-08-06" in slug


def test_t24_find_date_takes_the_first_iso_date(facet_index_mod):
    assert facet_index_mod.find_date("(2026-08-06) and 2026-08-07") == "2026-08-06"
    assert facet_index_mod.find_date("no date here") is None
    assert facet_index_mod.find_date("2026-8-6") is None


# ---------------------------------------------------------------------------
# the supersession verbs - conservative by construction
# ---------------------------------------------------------------------------
# ANCHOR: the comment above SUPERSEDE_RE - "Conservative by design: a phrase this
# does not match is under-counted, never mis-attributed", and
# link_supersessions' docstring - "A lower bound by construction".

@pytest.mark.parametrize("text,target", [
    ("Ruling 15 is CORRECTED in place", "15"),
    ("Ruling 8a is superseded by the measurement", "8a"),
    ("Amendment 27 is WITHDRAWN", "27"),
    ("Ruling 3's premise is void", "3"),
])
def test_t24_supersede_re_finds_explicit_verbs(facet_index_mod, text, target):
    assert facet_index_mod.SUPERSEDE_RE.findall(text) == [target]


def test_t24_supersede_re_declines_to_guess(facet_index_mod):
    """The under-count is the DESIGNED behavior, so it gets a test that fails if
    the pattern ever becomes greedy: narrative correction must not be read."""
    assert facet_index_mod.SUPERSEDE_RE.findall(
        "the word stands, anchored by the later measurement") == []
    assert facet_index_mod.SUPERSEDE_RE.findall("Ruling 15 is discussed again") == []


@pytest.mark.parametrize("text,found", [
    # the form the pattern describes: the number ADJACENT to the verb
    ("15i is corrected in place", ["15i"]),
    ("15i corrected in place", ["15i"]),
    ("8a is WITHDRAWN", ["8a"]),
    ("30 is withdrawn", ["30"]),
    # and the conservative half: prose between the number and the verb is NOT
    # read. My first fixture here asserted the opposite and was wrong - the
    # pattern requires adjacency, which is what keeps it from mis-attributing a
    # correction to whichever number appeared earlier in the sentence.
    ("15i " + EM + " the backdrop word is corrected in place", []),
    ("Ruling 15i, whose premise is corrected in place", []),
])
def test_t24_supersede_title_re_requires_adjacency(facet_index_mod, text, found):
    assert facet_index_mod.SUPERSEDE_TITLE_RE.findall(text) == found


# ---------------------------------------------------------------------------
# the claim families - range vs cardinal vs starts-at-1 vs AMBIGUOUS
# ---------------------------------------------------------------------------
# ANCHOR: the comment above CLAIM_FAMILIES - "A RANGE claim asserts the highest
# number; a CARDINAL claim asserts how many exist. They are different assertions
# ... E12 carries handoffs numbered to 16 but only 15 of them" - and the comment
# above CLAIM_SHAPED - "A RANGE IS ONLY A COUNT-CLAIM IF IT STARTS AT 1.
# `Rulings 1-30` asserts that thirty exist; `Rulings 21-23` names three of them
# and asserts nothing about the total."
#
# T5 exercises the sweep's ROUTING on synthetic documents. This exercises the
# patterns themselves, which T5 reaches only through the sweep.

def _family(mod, name):
    for label, kind, mode, rx in mod.CLAIM_FAMILIES:
        if label == name:
            return kind, mode, rx
    raise AssertionError("no claim family named %r" % name)


@pytest.mark.parametrize("dash", [EM, EN, "-"])
def test_t24_rulings_range_reads_all_three_dashes(facet_index_mod, dash):
    _, mode, rx = _family(facet_index_mod, "rulings range")
    assert mode == "max"
    assert rx.findall("Rulings 1 %s 30 are in" % dash) == ["30"]


def test_t24_range_and_cardinal_are_different_families(facet_index_mod):
    _, range_mode, range_rx = _family(facet_index_mod, "rulings range")
    _, card_mode, card_rx = _family(facet_index_mod, "rulings cardinal")
    assert (range_mode, card_mode) == ("max", "count")
    assert range_rx.findall("29 rulings") == []
    assert card_rx.findall("Rulings 1" + EM + "30") == []
    assert card_rx.findall("29 rulings landed") == ["29"]


def test_t24_a_range_not_starting_at_one_is_not_a_count_claim(facet_index_mod):
    """The named case: `Rulings 21-23` asserts nothing about the total, and an
    earlier pattern reported 35 such references as unparseable noise."""
    assert facet_index_mod.CLAIM_SHAPED.search("Rulings 1" + EM + "30")
    assert not facet_index_mod.CLAIM_SHAPED.search("Rulings 21" + EM + "23"), (
        "a mid-range reference read as claim-shaped - this is the 35-row noise "
        "the starts-at-1 rule removed")
    _, _, rx = _family(facet_index_mod, "rulings range")
    assert rx.findall("Rulings 21" + EM + "23") == []


@pytest.mark.parametrize("text", [
    "29 rulings + the close",
    "30 rulings so far",
    "at least 29 rulings",
    "29 rulings or so",
])
def test_t24_ambiguous_suffixes_are_flagged_not_read(facet_index_mod, text):
    """ANCHOR: "`29 rulings + the close` may assert 29 or 30 ... choosing a
    reading would be inventing a claim to check"."""
    assert facet_index_mod.AMBIGUOUS_SUFFIX.search(text), text


def test_t24_a_plain_cardinal_is_not_ambiguous(facet_index_mod):
    assert not facet_index_mod.AMBIGUOUS_SUFFIX.search("29 rulings landed")


def test_t24_claim_shaped_is_case_insensitive(facet_index_mod):
    assert facet_index_mod.CLAIM_SHAPED.search("30 RULINGS")
    assert facet_index_mod.CLAIM_SHAPED.search("E01" + EM + "E14")


def test_t24_arc_re_needs_exactly_two_digits(facet_index_mod):
    assert facet_index_mod.ARC_RE.findall("E14 and E08") == ["14", "08"]
    assert facet_index_mod.ARC_RE.findall("E1 and E123") == []


# ---------------------------------------------------------------------------
# laws.paid_for_by - a declared BOUND, and it has to track the record
# ---------------------------------------------------------------------------
# THE DEFECT THESE THREE CLOSE, measured 2026-08-11. `laws.paid_for_by` was
# declared as an E01-E15 range - frozen at E15 while the record ran to E33 - so
# a law body citing E21, E22, E23, E27, E28, E29, E30, E31 or E32 got
# `paid_for_by` NULL and NOTHING SAID SO. Measured on the corpus at the time:
# 95 laws parsed, 31 of their bodies mention an experiment, 16 were attributed
# and 15 were silently null. It is the SAME failure S02 halted its extraction
# over on a second record - "the law corpus parsed 38 rows and left paid_for_by
# NULL on every one, because the declared pattern matched an arc range that
# repo does not use" - reproduced on facet's own, which is where it was written.
#
# Two things were needed and neither substitutes for the other: the package's
# vocabulary counter makes it VISIBLE (verify printed `law paid_for_by ...
# unrecognised` with the tokens named), and the declaration has to be RIGHT.
# These legs are the second half, and they are what keeps it right when E34
# lands.
#
# WHY A BOUND RATHER THAN A WILDCARD OVER TWO DIGITS. The counter's population
# probe IS the two-digit E form; declaring the same thing would make its
# unrecognised count 0 by construction, forever, whatever the corpus said.
# This repo's law: grade an arm only on what it can move - if a metric reads
# the same when the arm works and when it does nothing, it is not measuring the
# arm. So the declaration states the arcs facet HAS, the counter keeps
# something to report, and the second leg below is what makes the next arc's
# bump a deliberate edit rather than a silence.

def _record_arc_span(m):
    """The highest experiment number the record itself carries.

    Derived, never transcribed - `parse_experiments` reads the authored status
    table plus the filesystem, which is the source `verify` counts against.
    """
    ids = sorted(e["id"] for e in m.parse_experiments())
    assert ids, "the record parsed no experiments; this leg has no denominator"
    for i in ids:
        assert re.match(r"^E\d\d$", i), (
            "an experiment id is not the two-digit E form (%r), so a numeric "
            "bound over them is not defined" % i)
    return max(int(i[1:]) for i in ids)


def test_t24_paid_for_by_reads_every_arc_the_record_has(facet_index_mod):
    """FAILS AT THE FROZEN VALUE. E16 through E33 are all in the record and the
    old declaration matched none of them."""
    m = facet_index_mod
    # E54 repair pin (2026-08-17). The span-derived check below is the primary
    # leg, but it can only fail while parse_experiments still reads the record:
    # a broken span computation would silently shrink its range, and the leg
    # could then no longer fail for exactly the arcs it exists to cover. The
    # two arcs the router round added are pinned by name, so this block FAILS
    # against the pre-repair declaration (bounded at E51:
    # \b(E0[1-9]|E[1-4]\d|E5[01])\b) whatever the span computation returns.
    # The bound leg below still refuses beyond-span arcs; extending the bound
    # stays a deliberate edit, per the WHY A BOUND comment above.
    for arc in ("E52", "E53"):
        assert m.PAID_RE.search("this law was paid for by %s." % arc), (
            "laws.paid_for_by cannot read %s, which the record has (pinned "
            "by name; the span-derived check below is the general form)" % arc)
    hi = _record_arc_span(m)
    unreadable = ["E%02d" % n for n in range(1, hi + 1)
                  if not m.PAID_RE.search("this law was paid for by E%02d." % n)]
    assert not unreadable, (
        "laws.paid_for_by cannot read %d of the record's own arcs, so a law "
        "citing one is attributed to nobody and nothing says so: %s"
        % (len(unreadable), ", ".join(unreadable)))


def test_t24_paid_for_by_is_a_bound_and_not_a_wildcard(facet_index_mod):
    """CAN-FAIL LEG, and the one that keeps the vocabulary counter alive.

    A declaration matching any two-digit E token would pass the leg above
    forever and would make `law paid_for_by`'s unrecognised count structurally
    zero. Requiring the bound to STOP at the record's own span is what leaves
    the counter something to report - and it is deliberately the leg that goes
    red the first time an arc lands without this declaration being edited.
    """
    m = facet_index_mod
    beyond = "E%02d" % (_record_arc_span(m) + 1)
    assert not m.PAID_RE.search("this law was paid for by %s." % beyond), (
        "laws.paid_for_by matches %s, which the record does not have - it is a "
        "wildcard rather than a bound, and the vocabulary counter that watches "
        "it can no longer read anything but zero" % beyond)


def test_t24_no_law_citing_an_arc_is_left_unattributed(facet_index_mod):
    """THE MEASUREMENT THAT FOUND THE DEFECT, kept runnable.

    Over the real law corpus rather than a fixture: a law whose body names an
    experiment must come out of the parser with a non-empty `paid_for_by`. It
    is a different question from the two above - those ask what the pattern
    admits, this asks what the corpus actually got, which is the end the
    declaration exists for.
    """
    m = facet_index_mod
    laws = m.parse_laws()
    assert laws, "the law corpus is empty; this leg would pass on nothing"
    orphans = [(l["file"], l["statement"][:60],
                ",".join(sorted(set(re.findall(r"\bE\d\d\b", l["body"])))))
               for l in laws
               if re.search(r"\bE\d\d\b", l["body"]) and not l["paid_for_by"]]
    assert not orphans, (
        "%d law(s) cite an experiment that laws.paid_for_by cannot read, so "
        "their attribution is silently null:\n  %s"
        % (len(orphans), "\n  ".join("%s :: %s :: %s" % o for o in orphans)))


# ---------------------------------------------------------------------------
# document classification for the sweep
# ---------------------------------------------------------------------------

def test_t24_current_state_and_historical_are_separated(facet_index_mod):
    """ANCHOR: classify_document plus the CURRENT_STATE / HISTORICAL_DIRS lists -
    "A kickoff or spec states its counts as of writing, and is correct as
    written"."""
    cls, why = facet_index_mod.classify_document("README.md", 1)
    assert cls == "current-state", why
    cls, why = facet_index_mod.classify_document(
        "docs/experiments/E20-coverage-kickoff.md", 1)
    assert cls == "historical", why
    cls, why = facet_index_mod.classify_document("docs/handbook/index.md", 1)
    assert cls == "current-state", why


def test_t24_an_unlisted_document_is_reported_not_assigned(facet_index_mod):
    """The property is the FALL-THROUGH branch, not the example that reaches
    it. This test named `SCORECARD.md` until E26 Half B classified that file
    `historical` and the test went red - so the example moved to a document
    that is still on neither list, and the property stayed. `docs/arc-history.md`
    is the live case: the sweep prints `unclassified` rows for it today."""
    cls, why = facet_index_mod.classify_document("docs/arc-history.md", 1)
    assert cls == "unclassified", why
    assert "neither list" in why


# ---------------------------------------------------------------------------
# the query tokenizer
# ---------------------------------------------------------------------------

def test_t24_fts_terms_drops_stopwords_and_short_words(facet_index_mod):
    assert facet_index_mod.fts_terms("what is the galleon") == ["galleon"]


def test_t24_fts_terms_never_returns_empty(facet_index_mod):
    """ANCHOR: the function's own comment - "never return an empty query". A
    phrase made only of stopwords must still produce terms, or the query is a
    syntax error rather than a miss."""
    got = facet_index_mod.fts_terms("what is the")
    assert got, "an all-stopword phrase returned no terms"
    assert set(got) <= {"what", "is", "the"}


def test_t24_fts_or_quotes_every_term(facet_index_mod):
    assert facet_index_mod.fts_or("the galleon mix") == '"galleon" OR "mix"'


def test_t24_stopwords_are_generic_not_seeded(facet_index_mod):
    """ANCHOR: the STOPWORDS comment - "This list is generic - it is not derived
    from any question in the seeded set." The discriminating terms that comment
    names must survive tokenizing."""
    for word in ("galleon", "mix", "backdrop", "hollow"):
        assert word not in facet_index_mod.STOPWORDS


# ---------------------------------------------------------------------------
# sequence gaps - a pure set operation, so a property holds
# ---------------------------------------------------------------------------

def test_t24_sequence_gaps_is_the_missing_set(facet_index_mod, built_db):
    """Over the real index: gaps are exactly the numbers in [lo, hi] absent from
    the table. Uses built_db (a per-run scratch path) so nothing here touches
    the tracked DB.
    """
    con = sqlite3.connect(str(built_db))
    try:
        present = facet_index_mod._sequence_numbers(con, "E14", "ruling")
        assert present, "E14 has no numbered rulings in the scratch index"
        lo, hi = min(present), max(present)
        gaps = facet_index_mod._sequence_gaps(con, "E14", "ruling", lo, hi)
        assert set(gaps).isdisjoint(present)
        assert set(gaps) == set(range(lo, hi + 1)) - set(present)
        # a window entirely above the record is entirely gap - the can-fail leg,
        # because an all-empty result would mean the function cannot report one
        high = facet_index_mod._sequence_gaps(con, "E14", "ruling", hi + 5, hi + 7)
        assert high == [hi + 5, hi + 6, hi + 7], high
    finally:
        con.close()
