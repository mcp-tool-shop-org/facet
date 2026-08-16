"""T34 - the stated counts, on every surface that states them (E26 Half A).

TWO QUANTITIES NOW. Legs 0-3 pin the TEST count (E26). THE FOURTH LEG, at the
bottom of this file, pins the EXPERIMENT count (E28 task 0) - a second
live-moving quantity on the same front door, drifting the same way and watched
by nothing. Its truth is the status table in `docs/experiments/README.md`; it
has its own pins, its own sweep and its own can-fail proofs, and its notation
boundary is declared there rather than here because it is a different matching
problem: the experiment count is spelled in ENGLISH WORDS on two of its four
sites, where a test count is always digits.

WHY THIS FILE EXISTS. The repo's stated test count drifted on its public
surfaces four times in two days, once inside the very commit that fixed the
previous drift. Every one was caught by a person reading the page. Nothing
watched it: the index's claims sweep has seven families and none of them
mentions tests, and it structurally cannot grow one, because that sweep reads
the INDEX and the index is a pure function of the corpus markdown while a test
count is a property of `tests/`.

So the shape is E23 Ruling 9's, adopted here by the E26 dispatch: a live-moving
quantity goes UNDER A TEST. Moving it then requires editing this file on
purpose, in the commit that moves it.

THE TRUTH IS `pytest --collect-only`, in a subprocess, both tiers. Not a
constant in this file - a constant would be a fifth surface to drift. There is
no recursion: the child collects and never executes, so this test is imported
by the child and run by nobody.

    THE SELF-REFERENCE, STATED. The child counts THIS FILE's tests. Adding or
    removing a test here moves the number every surface must state, in the same
    commit. That is not a defect to design around - it is the property that
    makes the pin real, and it is why E26 EDITS the surfaces rather than merely
    auditing them.

THREE LEGS, because a count can go wrong three ways.

  1. PINS - the current-state sites, each anchored on its own phrasing. A pin
     that stops matching fails as loudly as a pin that reads the wrong number:
     a rewritten sentence must be re-pinned deliberately.
  2. DIGITS - each of the eight READMEs carries both counts exactly twice.
     Language-agnostic on purpose; the seven translations are generated and a
     Japanese sentence has no anchorable English phrasing. Digits are digits.
  3. SWEEP - every test-count-shaped number on every declared surface must be
     either consumed by a pin or inside a declared historical region.
     Otherwise a NEW surface, or a new stale number on an old one, passes
     unseen - which is exactly the failure this file exists for, and it is the
     failure a hand-written list of surfaces has already had (`SHIP_GATE.md`
     item D records the v0.2.0 seat's handoff naming four surfaces and missing
     `SHIP_GATE.md` itself).

THE SWEEP'S SHAPE IS THE PHRASE FORM, AND THAT IS A DECLARED BOUNDARY (E26
Ruling 3). It matches `N tests` / `N hermetic`; it does NOT match `N/M` or
`N -> M`. Measured at the ruling seat, planted on README.md at HEAD:

    "The suite is 999 tests as of this line."   -> 3 FAILED, caught
    "The suite is 999/991 as of this line."     -> 34 passed, SLIPS
    "The suite moved 384 -> 999 this week."     -> 34 passed, SLIPS

The matcher is deliberately NOT widened to close that. This file's first
matcher was proximity-shaped and its own census returned 45 hits of which 15
were not test counts at all (`RTX 5090`, four ISO dates, six identifiers,
`limit=999`) while MISSING a real French site, because French spells it
`hermetiques`. A matcher loose enough to catch `648/640` is loose enough to
catch a version string and a date range.

SO THE RULE IS A WRITING CONVENTION, NOT A REGEX: state a current-state test
count in the phrase form above. A count written any other way is not pinned and
is not claimed to be - the same disposition the translations carry below.

CURRENT VERSUS HISTORICAL. A historical count is not a drift. `CHANGELOG`'s
released entries state what a version shipped and are correct forever;
`SHIP_GATE`'s lineage is a list of past values on purpose. The rule here is
SPAN-scoped, not file-scoped and not line-scoped, and it had to be:
`SHIP_GATE.md` item D carries four current-state claims and eight historical
pairs ON ONE PHYSICAL LINE. A file rule calls the whole line historical and
watches nothing; a line rule calls the whole line current and fires on the
lineage every time it is extended. Only spans separate them.

Everything printed here is ASCII (the repo's law) - the surfaces are UTF-8 and
seven of them are not English, so every failure message names a site by
`file:line` and a number, never by quoting its context.
"""
import io
import os
import re
import shutil
import subprocess
import sys

import pytest

from conftest import REPO

# ---------------------------------------------------------------------------
# the truth
# ---------------------------------------------------------------------------

_COLLECTED_FULL = re.compile(r"^(\d+) tests collected", re.M)
_COLLECTED_SPLIT = re.compile(r"^(\d+)/(\d+) tests collected \((\d+) deselected\)", re.M)


def _collect(args):
    """(selected, total) from a `--collect-only` child. Raises on an unparseable
    summary rather than guessing - a count this file cannot read is a count it
    must not silently substitute for."""
    p = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q",
         "-p", "no:cacheprovider", *args],
        cwd=str(REPO), capture_output=True, timeout=1800)
    out = p.stdout.decode("utf-8", errors="replace")
    if p.returncode != 0:
        raise AssertionError(
            "ANDON: `pytest --collect-only %s` exited %d, so this file has no "
            "truth to pin against. Collection must succeed before any surface "
            "can be checked.\n%s"
            % (" ".join(args), p.returncode, out[-2000:].encode(
                "ascii", "replace").decode("ascii")))
    m = _COLLECTED_SPLIT.search(out)
    if m:
        sel, tot, des = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if sel + des != tot:
            raise AssertionError(
                "ANDON: pytest's own summary does not add up - %d selected + %d "
                "deselected != %d total." % (sel, des, tot))
        return sel, tot
    m = _COLLECTED_FULL.search(out)
    if m:
        return int(m.group(1)), int(m.group(1))
    raise AssertionError(
        "ANDON: could not parse a collection summary from `pytest "
        "--collect-only %s`. Neither the plain nor the deselected form matched, "
        "so the count this file pins is unknown.\nlast 800 chars:\n%s"
        % (" ".join(args), out[-800:].encode("ascii", "replace").decode("ascii")))


@pytest.fixture(scope="module")
def counts():
    """(full, hermetic, gap) as the collector reports them, measured once."""
    full, full_total = _collect([])
    herm, herm_total = _collect(["-m", "not artifacts"])
    assert full == full_total, (
        "the unmarked run deselected something; `pytest` with no -m should "
        "select every collected test (%d selected of %d)" % (full, full_total))
    assert herm_total == full, (
        "the two collector runs disagree about the total: %d vs %d"
        % (herm_total, full))
    return full, herm, full - herm


# ---------------------------------------------------------------------------
# the surfaces
# ---------------------------------------------------------------------------

READMES = ["README.md"] + ["README.%s.md" % lang for lang in
                           ("ja", "zh", "es", "fr", "hi", "it", "pt-BR")]

# Every file that may state a test count. Globbed where a set can grow (a new
# translation, a new handbook page) so the surface list is not itself a
# hand-written live-moving quantity.
def surfaces(root):
    out = []
    for rel in READMES + ["SHIP_GATE.md", "SCORECARD.md", "SECURITY.md",
                          "CHANGELOG.md", "docs/advisor-kickoff.md",
                          "site/src/site-config.ts"]:
        out.append(rel)
    for sub in ("docs/handbook", "site/src/content/docs",
                "site/src/pages", ".github"):
        base = os.path.join(root, sub.replace("/", os.sep))
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames.sort()
            for fn in sorted(filenames):
                if fn.endswith((".md", ".astro", ".ts")):
                    p = os.path.join(dirpath, fn)
                    out.append(os.path.relpath(p, root).replace("\\", "/"))
    return sorted(set(out))


# ---------------------------------------------------------------------------
# the pins - one entry per current-state site, anchored on its own phrasing
# ---------------------------------------------------------------------------
# key: "full" | "hermetic" | "gap"; a two-group pattern takes a tuple of keys.
PINS = [
    ("README.md", "the bullet, full",
     r"\*\* [—-] (\d+) passing at two seats", "full"),
    ("README.md", "the bullet, hermetic",
     r"paths-gated CI on the (\d+) hermetic ones", "hermetic"),
    ("README.md", "Requirements, full",
     r"runs all \*\*(\d+)\*\* tests", "full"),
    ("README.md", "Requirements, hermetic",
     r"runs the \*\*(\d+)\*\* CI reproduces", "hermetic"),

    ("SHIP_GATE.md", "item D, full",
     r"runs the full \*\*(\d+)-test\*\* suite", "full"),
    ("SHIP_GATE.md", "item D, hermetic",
     r"runs the \*\*(\d+)\*\* hermetic tests CI reproduces", "hermetic"),
    # Both of these sit INSIDE the lineage clause and are current-state anyway:
    # "now N/M" is this line's present reading, and the lineage's terminal
    # element is the value it presently ends at. They are why the historical
    # rule here had to be span-scoped rather than line-scoped.
    ("SHIP_GATE.md", "item D, the lineage's 'now' pair",
     r"now (\d+)/(\d+) [—-] lineage", ("full", "hermetic")),
    ("SHIP_GATE.md", "item D, the lineage's terminal element",
     r"lineage(?: \d+ →)+ (\d+)\.", "full"),

    ("site/src/site-config.ts", "the card, full",
     r"desc: '(\d+) tests passing at two seats", "full"),
    ("site/src/site-config.ts", "the card, hermetic",
     r"paths-gated CI on the (\d+) hermetic ones", "hermetic"),

    ("site/src/content/docs/handbook/getting-started.md", "the command comment",
     r"# the (\d+) hermetic tests CI reproduces", "hermetic"),
    ("site/src/content/docs/handbook/getting-started.md", "the prose, full",
     r"The full suite is (\d+) tests", "full"),
    ("site/src/content/docs/handbook/getting-started.md", "the prose, gap",
     r"The (\d+) it deselects are the \*artifacts\* tier", "gap"),

    ("site/src/content/docs/handbook/reference.md", "the command comment",
     r"# the (\d+) hermetic tests CI runs", "hermetic"),

    ("docs/advisor-kickoff.md", "the RE-COUNT step",
     r"currently (\d+) total / (\d+) hermetic", ("full", "hermetic")),
    ("docs/advisor-kickoff.md", "THE SUITE line",
     r"THE SUITE: (\d+) tests, (\d+) hermetic", ("full", "hermetic")),
]

# ---------------------------------------------------------------------------
# the historical regions - declared, with the reason, never inferred
# ---------------------------------------------------------------------------
# Whole files whose every count is a statement about a past state.
HISTORICAL_FILES = {
    "SCORECARD.md":
        "the before/after treatment scorecard - its narrative counts are the "
        "state at treatment entry, corrected in place and correct as written",
}
# Whole-file glob prefixes.
HISTORICAL_PREFIXES = (
    (".github/release-notes-",
     "a published release note - it states what that version shipped"),
)
# An inline span: from `marker` to end of line, minus whatever a pin consumed.
HISTORICAL_INLINE = [
    ("SHIP_GATE.md", "Re-counted repeatedly:",
     "item D's lineage - a list of past readings, on purpose"),
]


def changelog_historical_from(root):
    """1-based line of CHANGELOG's first RELEASED heading.

    The rule, and the reason it is this one: an entry under `## [x.y.z]` states
    what that version shipped and is correct forever, while `## [Unreleased]`
    is shaped like a released entry and dated like the present - any count in
    it is a current-state claim wearing a released entry's clothes. So the
    boundary is the first released heading, not the file.
    """
    rel = os.path.join(root, "CHANGELOG.md")
    if not os.path.exists(rel):
        return None
    for i, ln in enumerate(_lines(rel), 1):
        if re.match(r"^## \[\d+\.\d+\.\d+\]", ln):
            return i
    return None


def _lines(path):
    with io.open(path, encoding="utf-8") as fh:
        return fh.read().replace("\r\n", "\n").split("\n")


# ---------------------------------------------------------------------------
# the sweep's matcher
# ---------------------------------------------------------------------------
# A hit is a number IMMEDIATELY FOLLOWED by a word that makes it a claim about
# the suite. Phrase-shaped, not proximity-shaped, and written against the
# SPECIFICATION - "a number claiming something about the suite" - rather than
# against the four drifts already noticed.
#
# THE FIRST VERSION OF THIS WAS PROXIMITY-SHAPED and it is worth recording why
# it was replaced rather than tuned. A +/-90-character window over the whole
# front door returned 45 hits, of which SIX were not test counts at all: `RTX
# 5090`, a `57`-gate-site sentence, four ISO dates, `limit=999`, and the
# identifiers `T27` `T29` `T30` `E21` `A32` `Ruling 35`. Proximity fires on
# whatever correlates with it, including the record's own habit of naming a
# test file and a test count in the same sentence. It also had a HOLE the same
# census exposed: French writes `hermetiques`, which no spelling of
# `herm[e]tic` matches, so one real stale site was invisible. A wider window
# would have found it and doubled the false positives.
#
# THE TRANSLATIONS ARE NOT SWEPT. Six of the seven false positives above were
# in them, and no phrase list survives seven languages that a generator
# rewrites. They are covered by the DIGITS leg instead - which is what the
# dispatch specified, and which fails on a stale file by finding ZERO
# occurrences of the current count. This is a declared boundary, not an
# oversight: a NEW test-count site invented inside a translation is not
# watched by anything here.
NOT_SWEPT = tuple(r for r in READMES if r != "README.md")

# Trailing `-` is allowed (`384-test`); a leading letter is not, so `T29`,
# `E21` and `A32` are identifiers rather than counts. `=` blocks `limit=999`.
NUMBER = re.compile(r"(?<![A-Za-z\d.,:/=-])(\d{1,4})(?![\d.,:/])")
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
# What must follow, within a short reach, for the number to be a claim. `total`
# is here for the advisor kickoff's `N total / M hermetic`; `it deselects` for
# the handbook's tier-gap sentence.
CLAIM_TAIL = re.compile(
    r"^\*{0,2}[\s-]*\*{0,2}"
    r"(?:tests?|passing|hermetic|total|collected|deselected|it deselects)\b",
    re.IGNORECASE)
TAIL_REACH = 22


def shaped_hits(path):
    """[(line, col_start, col_end, value)] - every test-count-shaped number."""
    out = []
    for i, ln in enumerate(_lines(path), 1):
        dates = [(d.start(), d.end()) for d in ISO_DATE.finditer(ln)]
        for m in NUMBER.finditer(ln):
            if any(s <= m.start() < e for s, e in dates):
                continue
            if not CLAIM_TAIL.match(ln[m.end():m.end() + TAIL_REACH]):
                continue
            out.append((i, m.start(), m.end(), int(m.group(1))))
    return out


# Hits that are real claims but are DELIBERATELY not pinned by this arc, named
# with the reason. Excusing one is an edit; leaving one unexcused is a failure.
DECLARED_NOT_PINNED = [
    ("SHIP_GATE.md", "T29, 30 tests", 30,
     "a PER-TEST-FILE count, not the suite count. E26 pins the suite; this is "
     "a second class of test-count claim on the front door, named here rather "
     "than silently swept up, and reported to the ruling"),
]


def pin_spans(root):
    """{rel: [(line, start, end)]} consumed by a pin, and {rel+name: values}."""
    spans, read = {}, {}
    for rel, name, pat, keys in PINS:
        p = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.exists(p):
            read[(rel, name)] = ("MISSING FILE", [])
            continue
        found = []
        for i, ln in enumerate(_lines(p), 1):
            for m in re.finditer(pat, ln):
                found.append((i, m.start(), m.end(),
                              [int(g) for g in m.groups()]))
        read[(rel, name)] = ("%d match(es)" % len(found), found)
        for i, s, e, _ in found:
            spans.setdefault(rel, []).append((i, s, e))
    return spans, read


def historical_spans(root):
    """{rel: 'whole'} or {rel: [(line, start, end_of_line)]}, with reasons."""
    whole, inline, why = {}, {}, {}
    for rel, reason in HISTORICAL_FILES.items():
        whole[rel] = reason
    cl = changelog_historical_from(root)
    if cl is not None:
        why["CHANGELOG.md"] = ("released entries, from L%d down" % cl)
    for rel, marker, reason in HISTORICAL_INLINE:
        p = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.exists(p):
            continue
        for i, ln in enumerate(_lines(p), 1):
            k = ln.find(marker)
            if k >= 0:
                inline.setdefault(rel, []).append((i, k, len(ln)))
                why[rel] = reason
    return whole, inline, cl, why


def unaccounted(root):
    """Every shaped hit that is neither pinned nor declared historical.

    Returns [(rel, line, value)] - ASCII only, so a Japanese surface's failure
    reads the same as an English one.
    """
    spans, _ = pin_spans(root)
    whole, inline, cl_from, _ = historical_spans(root)
    bad = []
    for rel in surfaces(root):
        p = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.exists(p):
            continue
        if rel in NOT_SWEPT:
            continue
        if rel in whole or rel.startswith(HISTORICAL_PREFIXES[0][0]):
            continue
        lines = _lines(p)
        for (i, s, e, v) in shaped_hits(p):
            if any(li == i and s >= ls and e <= le
                   for (li, ls, le) in spans.get(rel, [])):
                continue
            if rel == "CHANGELOG.md" and cl_from is not None and i >= cl_from:
                continue
            if any(li == i and s >= ls for (li, ls, le) in inline.get(rel, [])):
                continue
            if any(r == rel and val == v and anchor in lines[i - 1]
                   for r, anchor, val, _why in DECLARED_NOT_PINNED):
                continue
            bad.append((rel, i, v))
    return bad


# ---------------------------------------------------------------------------
# leg 0 - the collector, and that it is not vacuous
# ---------------------------------------------------------------------------

def test_t34_the_collector_reports_two_tiers_that_add_up(counts):
    full, herm, gap = counts
    assert full > 0 and herm > 0, "collection returned nothing to pin"
    assert gap >= 0, "the hermetic tier cannot be larger than the full one"
    assert herm + gap == full, "%d + %d != %d" % (herm, gap, full)


def test_t34_the_tiers_are_actually_different(counts):
    """Guard against the check-that-cannot-fail. If the artifacts marker ever
    selects nothing, `full == hermetic` and both pins would agree trivially
    while the two-tier claim on every surface quietly became untrue."""
    full, herm, gap = counts
    assert gap > 0, (
        "the artifacts tier deselects nothing (full %d == hermetic %d), so "
        "every surface's two-tier claim is now a claim about one tier. Either "
        "the marker was dropped or its tests were - either way the surfaces "
        "say something that is no longer true." % (full, herm))


# ---------------------------------------------------------------------------
# leg 1 - the pins
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rel,name,pat,keys",
                         PINS, ids=["%s::%s" % (p[0], p[1]) for p in PINS])
def test_t34_every_pinned_site_states_the_collected_count(
        rel, name, pat, keys, counts):
    full, herm, gap = counts
    want = {"full": full, "hermetic": herm, "gap": gap}
    p = os.path.join(str(REPO), rel.replace("/", os.sep))
    assert os.path.exists(p), "pinned surface is gone: %s" % rel
    found = []
    for i, ln in enumerate(_lines(p), 1):
        for m in re.finditer(pat, ln):
            found.append((i, [int(g) for g in m.groups()]))
    assert len(found) == 1, (
        "%s :: %s - the anchor matched %d times, expected exactly 1. A rewritten "
        "sentence must be re-pinned in the commit that rewrites it; a duplicated "
        "one is a second site nobody is watching." % (rel, name, len(found)))
    line, got = found[0]
    ks = keys if isinstance(keys, tuple) else (keys,)
    assert len(got) == len(ks), (
        "%s :: %s - anchor captured %d numbers, the pin declares %d"
        % (rel, name, len(got), len(ks)))
    for value, key in zip(got, ks):
        assert value == want[key], (
            "%s:%d :: %s - states %s %d, the collector reports %d. The stated "
            "count moved (or this surface did not). Every surface in T34's PINS "
            "table changes in the same commit."
            % (rel, line, name, key, value, want[key]))


# ---------------------------------------------------------------------------
# leg 2 - digits, for the eight READMEs
# ---------------------------------------------------------------------------

DIGIT_SITES_PER_README = 2


# European locales write a thousands separator this matcher cannot read.
# French renders 1072 as "1 072", so NUMBER - whose lookbehind class is
# [A-Za-z\d.,:/=-] and does not contain   - sees the integers 1 and 72,
# and the site reports ZERO. That is the SAME reading a stale translation
# produces, so the leg cannot tell a correct French file from a dead one.
# It FIRED on correct work for exactly this reason (2026-08-16, README.fr.md,
# whose counts were current and non-breaking-space separated).
#
# A no-break or narrow-no-break space BETWEEN two digits is a group separator
# and is never anything else, so collapsing it is unambiguous. This ADDS a form
# the leg can read and REMOVES NO COVERAGE: a missing or stale count still
# yields zero occurrences and still fails, which the second fixture below pins.
#
# Alternatives considered and rejected in writing, because each removes
# coverage rather than adding capability: dropping README.fr.md from the
# parametrization (loses French entirely); lowering DIGIT_SITES_PER_README to 1
# (loses a site on all eight files); reverting the French translation to its
# stale state (discards a correct file and restores the defect the run existed
# to fix - this was done once, on this same misreading); and rewriting
# README.fr.md to use bare digits (degrades the public French surface to suit a
# test, and the generator reproduces the correct form on every future run).
#
# Scoped to this leg deliberately. The sweep at NUMBER's other consumer reads
# English source surfaces, which carry no locale separators; narrowing the
# change to the leg that reads generated translations keeps it auditable.
GROUP_SEP = re.compile(r"(?<=\d)[  ](?=\d)")


def digit_occurrences(root, rel, value):
    """How many times `value` appears as a standalone integer in `rel`,
    reading a locale group separator as part of the number."""
    p = os.path.join(root, rel)
    if not os.path.exists(p):
        return None
    text = GROUP_SEP.sub("", "\n".join(_lines(p)))
    return sum(1 for m in NUMBER.finditer(text) if int(m.group(1)) == value)


@pytest.mark.parametrize("rel", READMES)
def test_t34_every_readme_carries_both_counts_twice(rel, counts):
    """The translations are generated and carry no anchorable English phrasing,
    so they are checked as digits: each README states the full count twice and
    the hermetic count twice - a bullet and a Requirements paragraph. This is
    the leg that fires on a stale translation, and it fires by finding ZERO
    occurrences, not a wrong one."""
    full, herm, _ = counts
    assert os.path.exists(os.path.join(str(REPO), rel)), (
        "README surface is gone: %s" % rel)
    for key, value in (("full", full), ("hermetic", herm)):
        n = digit_occurrences(str(REPO), rel, value)
        assert n == DIGIT_SITES_PER_README, (
            "%s states the %s count (%d) %d time(s), expected %d. The eight "
            "READMEs regenerate together: `translate-all.mjs README.md "
            "--cache-clear` before the release commit, per the release-ordering "
            "law." % (rel, key, value, n, DIGIT_SITES_PER_README))


def test_t34_digit_leg_reads_a_locale_group_separator(tmp_path):
    """French writes 1072 as "1 072". Before this leg learned the group
    separator, NUMBER read the integers 1 and 72 and the site reported ZERO -
    identical to what a stale translation produces. The gate fired on a correct
    file for that reason (2026-08-16, README.fr.md).

    THE DISCRIMINATOR, and the reason this fixture is worth having: it asserts
    first that the RAW matcher cannot find the value in this text. A fixture
    that passes under the implementation it replaces does not test the change,
    so if that assertion ever stops holding, this test has quietly stopped
    testing anything and says so instead of going green."""
    p = tmp_path / "README.xx.md"
    p.write_text(
        "les 1 072 tests, dont 1 027 hermetiques\n"
        "localement 1 072 et 1 027 reproduits par le CI\n",
        encoding="utf-8")
    raw = [int(m.group(1))
           for m in NUMBER.finditer(p.read_text(encoding="utf-8"))]
    assert 1072 not in raw and 1027 not in raw, (
        "fixture no longer discriminates: the raw matcher already reads the "
        "separated form, so this test cannot fail under the old implementation")
    assert digit_occurrences(str(tmp_path), "README.xx.md", 1072) == 2
    assert digit_occurrences(str(tmp_path), "README.xx.md", 1027) == 2


def test_t34_digit_leg_still_fires_on_a_stale_locale_file(tmp_path):
    """The repair must not blunt the leg. A separator-formatted file quoting a
    DEAD count still reports zero for the live one - and the second assertion
    is what makes the first mean something, by proving the zero is a real
    ABSENCE rather than a matcher that cannot read the form at all."""
    p = tmp_path / "README.xx.md"
    p.write_text("les 9 999 tests, dont 8 888 hermetiques\n",
                 encoding="utf-8")
    assert digit_occurrences(str(tmp_path), "README.xx.md", 1072) == 0
    assert digit_occurrences(str(tmp_path), "README.xx.md", 9999) == 1


def test_t34_every_declared_exemption_is_real():
    """A DECLARED_NOT_PINNED entry that matches nothing is a dead exemption
    quietly widening the sweep's blind spot. Each must still be findable."""
    dead = []
    for rel, anchor, value, _why in DECLARED_NOT_PINNED:
        p = os.path.join(str(REPO), rel.replace("/", os.sep))
        text = "\n".join(_lines(p)) if os.path.exists(p) else ""
        if anchor not in text:
            dead.append("%s :: %s" % (rel, anchor))
    assert not dead, (
        "declared exemptions that match nothing: %s" % ", ".join(dead))


# ---------------------------------------------------------------------------
# leg 3 - the sweep
# ---------------------------------------------------------------------------

def test_t34_no_unaccounted_test_count_on_any_surface():
    """Every test-count-shaped number on a declared surface is either pinned as
    current-state or declared historical. An unaccounted hit means a NEW site
    exists that nothing is watching - the exact failure a hand-written surface
    list has already had at a release seat."""
    bad = unaccounted(str(REPO))
    assert not bad, (
        "%d test-count-shaped number(s) on a declared surface are neither "
        "pinned nor declared historical:\n%s\n\n"
        "Pin it in T34's PINS table if it states the CURRENT suite, or add it "
        "to HISTORICAL_FILES / HISTORICAL_INLINE with its reason if it states "
        "a past one. Deciding which is a deliberate edit, which is the point."
        % (len(bad), "\n".join("   %s:%d  (%d)" % b for b in bad)))


def test_t34_every_declared_surface_exists():
    """A pin against a file that has been moved or deleted must fail here, not
    silently pass by having nothing to check."""
    missing = [rel for rel, _, _, _ in PINS
               if not os.path.exists(os.path.join(str(REPO),
                                                  rel.replace("/", os.sep)))]
    assert not missing, "pinned surfaces missing: %s" % ", ".join(sorted(set(missing)))


def test_t34_the_historical_regions_are_real():
    """A declared historical region that matches nothing is a dead declaration
    which would silently widen the sweep's blind spot if the surface changed."""
    root = str(REPO)
    whole, inline, cl_from, _ = historical_spans(root)
    for rel in whole:
        assert os.path.exists(os.path.join(root, rel.replace("/", os.sep))), (
            "HISTORICAL_FILES names %s, which does not exist" % rel)
    for rel, marker, _ in HISTORICAL_INLINE:
        assert inline.get(rel), (
            "HISTORICAL_INLINE names %s :: %r, which matches no line"
            % (rel, marker))
    assert cl_from is not None, (
        "CHANGELOG.md has no released `## [x.y.z]` heading, so the "
        "current-versus-historical boundary this file relies on does not exist")


# ---------------------------------------------------------------------------
# leg 4 - the legs above are not vacuous (E26 gate 2, kept runnable)
# ---------------------------------------------------------------------------
# The dispatch requires that this test FAIL on a deliberately stale surface and
# pass at HEAD. Run once by hand that is a demonstration; run here it is a
# check, and this repo's rule is that a re-runnable anchor is ported into the
# harness rather than left in a report.

_STALE_TREE = [
    ("README.md", "the bullet", "384 passing at two seats", "999 passing at two seats"),
    ("README.ja.md", "a translation", None, None),
    ("SHIP_GATE.md", "item D", "runs the full **384-test** suite",
     "runs the full **999-test** suite"),
]


def _mirror(root, dst):
    """Copy just the surfaces into a scratch tree - fast, and it keeps the
    mutation nowhere near the working copy."""
    for rel in surfaces(root):
        src = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.exists(src):
            continue
        out = os.path.join(dst, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copyfile(src, out)
    return dst


def _rewrite(path, old, new):
    with io.open(path, encoding="utf-8") as fh:
        t = fh.read()
    assert old in t, "the stale-tree fixture's own anchor is gone: %r" % old
    with io.open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(t.replace(old, new, 1))


def _pin_failures(root, counts_tuple):
    """Which pins would fail against `root` - the pin leg, run off-tree."""
    full, herm, gap = counts_tuple
    want = {"full": full, "hermetic": herm, "gap": gap}
    bad = []
    for rel, name, pat, keys in PINS:
        p = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.exists(p):
            bad.append((rel, name, "missing"))
            continue
        found = [[int(g) for g in m.groups()]
                 for ln in _lines(p) for m in re.finditer(pat, ln)]
        if len(found) != 1:
            bad.append((rel, name, "%d matches" % len(found)))
            continue
        ks = keys if isinstance(keys, tuple) else (keys,)
        for value, key in zip(found[0], ks):
            if value != want[key]:
                bad.append((rel, name, "%s %d != %d" % (key, value, want[key])))
    return bad


def test_t34_a_stale_surface_fails_the_pin_leg(tmp_path, counts):
    """Behavioural, not incidental: the tree is byte-identical to HEAD except
    for ONE number, and the failure names that site. E24's gate 3 reddened an
    old tree for the wrong reason - ten AttributeErrors on symbols that did not
    exist yet - so this proves the failure is the count, not the plumbing."""
    root = _mirror(str(REPO), str(tmp_path / "stale"))
    assert not _pin_failures(root, counts), (
        "the MIRROR of HEAD already fails the pin leg, so the next assertion "
        "would prove nothing about staleness")
    _rewrite(os.path.join(root, "README.md"),
             "%d passing at two seats" % counts[0],
             "%d passing at two seats" % (counts[0] + 15))
    bad = _pin_failures(root, counts)
    assert len(bad) == 1, "expected exactly one pin to fail, got %r" % (bad,)
    assert bad[0][0] == "README.md" and "full" in bad[0][2], (
        "the failure did not name the site that was made stale: %r" % (bad,))


def test_t34_a_stale_translation_fails_the_digits_leg(tmp_path, counts):
    """The seven translations were the surfaces stale at HEAD when this file
    was written, so the leg that catches them gets its own proof - run against
    the same function the real leg calls, not a re-implementation of it."""
    full, herm, _ = counts
    root = _mirror(str(REPO), str(tmp_path / "stale_tr"))
    assert digit_occurrences(root, "README.ja.md", full) == DIGIT_SITES_PER_README, (
        "the mirror's Japanese README does not already carry the full count "
        "twice, so the mutation below would prove nothing")
    p = os.path.join(root, "README.ja.md")
    with io.open(p, encoding="utf-8") as fh:
        before = fh.read()
    with io.open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(before.replace(str(full), str(full - 14)))
    assert digit_occurrences(root, "README.ja.md", full) == 0, (
        "a translation rolled back to an older count still satisfies the "
        "digits leg, which would make it blind to exactly the drift it exists "
        "for")


def test_t34_a_new_unwatched_site_fails_the_sweep(tmp_path, counts):
    """The sweep's own can-fail leg: add a test count to a surface without
    pinning it, and the sweep must find it. Without this the sweep could pass
    because its matcher matches nothing, which is this repo's most-repeated
    defect."""
    root = _mirror(str(REPO), str(tmp_path / "newsite"))
    assert not unaccounted(root), (
        "the MIRROR of HEAD already has unaccounted hits, so the next "
        "assertion would prove nothing: %r" % (unaccounted(root)[:5],))
    p = os.path.join(root, "SECURITY.md")
    with io.open(p, "a", encoding="utf-8", newline="") as fh:
        fh.write("\n\nThe suite is 271 tests.\n")
    bad = unaccounted(root)
    assert bad, "the sweep did not see a brand-new unpinned test count"
    assert any(rel == "SECURITY.md" and v == 271 for rel, _, v in bad), (
        "the sweep fired, but not on the site that was added: %r" % (bad,))


def test_t34_the_sweep_does_not_fire_on_a_historical_count(tmp_path, counts):
    """E26 gate 3, kept runnable. A released CHANGELOG entry and SHIP_GATE's
    lineage are correct forever; adding another past reading to either must not
    fire, while the SAME number added ABOVE the released boundary must."""
    root = _mirror(str(REPO), str(tmp_path / "hist"))
    assert not unaccounted(root)

    cl = os.path.join(root, "CHANGELOG.md")
    lines = _lines(cl)
    at = changelog_historical_from(root)
    assert at is not None
    lines.insert(at + 2, "**311 tests, 311 passing** - 303 hermetic + 8 artifacts.")
    with io.open(cl, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(lines))
    assert not unaccounted(root), (
        "a count inside a RELEASED changelog entry fired the sweep; released "
        "entries state what a version shipped and are correct forever")

    # and the same sentence above the boundary is a current-state claim
    lines = _lines(cl)
    lines.insert(at - 1, "**311 tests, 311 passing** - 303 hermetic + 8 artifacts.")
    with io.open(cl, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(lines))
    bad = unaccounted(root)
    assert any(rel == "CHANGELOG.md" and v == 311 for rel, _, v in bad), (
        "a count in the Unreleased block did NOT fire the sweep, so the "
        "boundary this file draws does not actually separate anything: %r"
        % (bad[:5],))


# ===========================================================================
# THE FOURTH LEG - the EXPERIMENT count (E28 task 0)
# ===========================================================================
# Legs 0-3 above pin the TEST count. This one pins a SECOND live-moving
# quantity on the same surfaces, and it is here for the same reason: it
# drifted three times in 24 hours, twice INSIDE the commit that fixed the
# previous drift (E27's ruling corrected the front door from "twenty-three"
# to "twenty-six" and undercounted by one while doing it; E26's drift landed
# in its own fix). A class that re-drifts while being fixed does not need
# another careful reader - it needs the mechanism this repo already has.
#
# THE TRUTH IS THE STATUS TABLE in `docs/experiments/README.md`, counted
# here, never a constant - a constant would be one more surface to drift.
# `docs/experiments/README.md` is therefore NOT a swept surface: it is the
# instrument, not a claim about the instrument.
#
# ---------------------------------------------------------------------------
# THE NOTATION BOUNDARY, DECLARED - which spellings this leg catches
# ---------------------------------------------------------------------------
# This is a DIFFERENT matching problem from the test count, and the difference
# is the whole reason this section is separate. A test count is always digits
# ("648 tests"), so the digits leg is language-agnostic and the seven
# translations are covered for free. An experiment count is spelled in ENGLISH
# WORDS on two of its four sites ("Twenty-eight experiments are in the
# record"), and a generator TRANSLATES a word.
#
#   CAUGHT   - decimal digits            "27 experiments"
#            - English cardinals 0-99, hyphenated or space-separated,
#              case-insensitive         "Twenty-eight experiments"
#                                        "twenty six experiments"
#
#   NOT CAUGHT - and each is a declared boundary, not an oversight. NOT
#   CAUGHT here means DECLINED, never mis-read: a hyphenated pair that does
#   not parse returns nothing rather than falling back to its right-hand
#   half, which is what `vingt-six` did on this leg's first run (it returned
#   SIX). See `trailing_count`.
#            - non-English number words. Measured on the seven generated
#              READMEs at the time this leg was written: `veintiseis`,
#              `vingt-six`, `ventisei`, `vinte e seis`, the Devanagari and
#              the CJK forms. Six languages, six spellings, and no phrase
#              list survives a generator that rewrites them. This is the same
#              disposition leg 3 already carries for the translations
#              (NOT_SWEPT), reached the same way and for the same reason -
#              E26 Ruling 3 ruled a WIDER MATCHER out, with a census: the
#              first proximity-shaped one returned 45 hits of which 15 were
#              not counts, while missing a real French site.
#              The Japanese README writes the DIGIT (`26 件`), so it alone
#              would be catchable by a digits leg; one of seven is not a leg.
#            - vague quantifiers: "several experiments", "a few experiments".
#            - ordinals as counts: "the twenty-eighth experiment".
#            - numbers above 99 spelled in words.
#            - A CLAIM SPLIT ACROSS A LINE BREAK. `shaped_hits` and
#              `experiment_hits` are both line-scoped, so prose that wraps
#              between the number and the noun ("...reports 28\nexperiments")
#              is invisible to both. Found the honest way: this leg fired on
#              the CHANGELOG entry announcing it, caught one of two counts in
#              that entry, and the survivor had wrapped. Declared rather than
#              closed - a multi-line matcher over a corpus this size is how
#              the proximity-shaped matcher E26 Ruling 3 rejected got its 15
#              false positives. The writing convention absorbs it: keep a
#              count and its noun on one line.
#
# THE REMEDY FOR WHAT IS NOT CAUGHT IS A WRITING CONVENTION, NOT A REGEX -
# E26 Ruling 3's disposition, carried: state the record's size on an English
# surface, in the phrase forms pinned below. A count written any other way is
# not pinned and is NOT CLAIMED TO BE.
#
# `test_experiment_notation_boundary_is_what_it_says` below makes every line
# of the above runnable. Widening the parser is allowed - it just has to be
# done ON PURPOSE, in the commit that edits that test.

_CARDINAL_UNITS = (
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen seventeen eighteen nineteen").split()
_CARDINAL_TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
                  "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}


def english_cardinal(text):
    """int for a decimal or an English cardinal 0-99, else None.

    Returns None rather than guessing, because every non-number token in the
    corpus reaches this function - it is the filter, not a parser applied to
    something already known to be a number."""
    t = text.strip().lower().replace(" ", "-")
    if re.match(r"^\d{1,4}$", t):
        return int(t)
    if t in _CARDINAL_UNITS:
        return _CARDINAL_UNITS.index(t)
    if t in _CARDINAL_TENS:
        return _CARDINAL_TENS[t]
    m = re.match(r"^([a-z]+)-([a-z]+)$", t)
    if m and m.group(1) in _CARDINAL_TENS and m.group(2) in _CARDINAL_UNITS[1:10]:
        return _CARDINAL_TENS[m.group(1)] + _CARDINAL_UNITS.index(m.group(2))
    return None


_EXP_WORD = re.compile(r"experiments?\b", re.IGNORECASE)
_LAST_TWO = re.compile(r"([A-Za-z]+|\d{1,4})([- ])([A-Za-z]+|\d{1,4})\s*$")
_LAST_ONE = re.compile(r"([A-Za-z]+|\d{1,4})\s*$")


def trailing_count(head):
    """(value, start_col) for the number immediately preceding `head`'s end.

    TWO TOKENS ARE TRIED BEFORE ONE, and that ordering is load-bearing rather
    than tidy: a single greedy regex matches `redirected four` in "redirected
    four experiments", fails to parse it, and having consumed the region never
    sees the `four` that is actually there. Longest-first with an explicit
    fallback is what makes the hyphenated `Twenty-eight` and the bare `four`
    both reachable.

    A HYPHENATED PAIR IS ALL-OR-NOTHING, AND THIS COST A DEFECT TO LEARN.
    The first version fell back to the right-hand token whatever the
    separator, so French `vingt-six` - which fails to parse as a pair - fell
    through to `six` and returned SIX. That is not a missed reading, it is a
    CONFIDENTLY WRONG one, and it is worse than declining: the leg would have
    reported a number for a surface it cannot read. Caught by this leg's own
    notation-boundary test on its first run, which is the argument for having
    written that test at all. A hyphen joins one lexical unit; a space does
    not, so the space fallback stays and the hyphen fallback is refused."""
    m = _LAST_TWO.search(head)
    if m:
        v = english_cardinal("%s-%s" % (m.group(1), m.group(3)))
        if v is not None:
            return v, m.start(1)
        if m.group(2) == "-":
            return None
    m = _LAST_ONE.search(head)
    if m:
        v = english_cardinal(m.group(1))
        if v is not None:
            return v, m.start(1)
    return None


def experiment_hits(path):
    """[(line, col_start, col_end, value)] - every experiment-count-shaped
    number. Shaped, not necessarily a claim about the record's SIZE: the
    handbook says "Four experiments ran without one", which is a true
    statement about the past and not a count of the record. Separating those
    is the sweep's job below, by DECLARATION rather than by a cleverer
    regex."""
    out = []
    for i, ln in enumerate(_lines(path), 1):
        for m in _EXP_WORD.finditer(ln):
            got = trailing_count(ln[:m.start()])
            if got is None:
                continue
            value, col = got
            out.append((i, col, m.end(), value))
    return out


# ---------------------------------------------------------------------------
# the experiment pins - one per site that states the RECORD'S SIZE
# ---------------------------------------------------------------------------
# Same contract as PINS above: exactly one match, anchored on its own
# phrasing, so a rewritten sentence must be re-pinned deliberately. The
# captured group is a digit run OR an English cardinal; `english_cardinal`
# decides which, so a site may be written either way.
EXPERIMENT_PINS = [
    ("README.md", "the discipline bullet",
     r"([A-Za-z][A-Za-z-]*|\d+) experiments are in\b"),
    # Added at E28 2c: this site read "Twenty of them are in" - a real stale
    # count (the record held 28) in a phrasing the sweep structurally cannot
    # see, found by a person editing the file for the suite count. Rephrased
    # into the pinned form and pinned, the writing-convention remedy.
    ("site/src/content/docs/handbook/getting-started.md", "reading the record",
     r"([A-Za-z][A-Za-z-]*|\d+) experiments are in\b"),
    ("README.md", "the where-to-read table",
     r"\| ([A-Za-z][A-Za-z-]*|\d+) experiments: spec, report, ruling"),
    ("site/src/site-config.ts", "the method card",
     r"([A-Za-z][A-Za-z-]*|\d+) experiments are in the record"),
    ("docs/advisor-kickoff.md", "the index-health line",
     r"([A-Za-z][A-Za-z-]*|\d+) experiments\. No staleness"),
]

# Shaped hits that are REAL and TRUE but are not claims about the record's
# size. Each is narrative about a past state - "four experiments ran without
# a provenance sheet" is correct forever however many experiments exist -
# which is the same disposition the historical rule carries for CHANGELOG,
# reached per-site because these sit inside live prose. Excusing one is an
# edit; leaving one unexcused is a failure.
EXPERIMENT_NOT_TOTAL = [
    ("docs/handbook/index.md", "Four experiments ran without one", 4,
     "narrative: how many arcs ran before the provenance sheet existed"),
    ("docs/handbook/index.md", "before you build on it.** Four experiments", 4,
     "narrative: how many arcs were graded on high-pass statistics"),
    ("site/src/content/docs/handbook/index.md",
     "Four experiments ran without one", 4,
     "narrative, the site mirror of docs/handbook/index.md"),
    ("site/src/content/docs/handbook/index.md",
     "before you build on it.** Four experiments", 4,
     "narrative, the site mirror of docs/handbook/index.md"),
    ("site/src/content/docs/handbook/getting-started.md",
     "exist for the first seven experiments", 7,
     "narrative: how many arcs preceded the provenance sheet"),
    ("site/src/site-config.ts", "redirected four experiments", 4,
     "narrative: how much work one negative result redirected"),
]


def experiment_rows(root):
    """(count, ids) from the status table in `docs/experiments/README.md`.

    THE TRUTH FUNCTION. A row is a table line whose first cell opens with an
    experiment id, linked or bare - E09 and E03 are listed without links, so
    the bracket is optional. Raises rather than returning 0 if the table's
    header is gone, because a truth function that silently returns nothing
    would make every pin below fail for the wrong reason and every stale
    surface look like a table problem."""
    p = os.path.join(root, "docs", "experiments", "README.md")
    if not os.path.exists(p):
        raise AssertionError(
            "ANDON: docs/experiments/README.md is missing, so the experiment "
            "count has no truth to pin against.")
    lines = _lines(p)
    if not any(re.match(r"^\|\s*id\s*\|", ln) for ln in lines):
        raise AssertionError(
            "ANDON: docs/experiments/README.md has no `| id |` status-table "
            "header, so this leg cannot locate the table it counts. If the "
            "table was restructured, re-point this function in the same "
            "commit.")
    ids = []
    for ln in lines:
        m = re.match(r"^\|\s*\[?(E\d{2,3})\b", ln)
        if m:
            ids.append(m.group(1))
    return len(ids), ids


@pytest.fixture(scope="module")
def experiments():
    """The record's size, measured once."""
    n, _ = experiment_rows(str(REPO))
    return n


# ---------------------------------------------------------------------------
# fourth leg, part 1 - the truth function, and that it is not vacuous
# ---------------------------------------------------------------------------

def test_the_status_table_yields_a_usable_experiment_count(experiments):
    n, ids = experiment_rows(str(REPO))
    assert n > 0, "the status table produced no rows to count"
    assert len(set(ids)) == n, (
        "the status table lists an id twice, which inflates the count every "
        "surface must state: %s"
        % ", ".join(sorted(i for i in set(ids) if ids.count(i) > 1)))
    assert n == experiments


def test_the_experiment_counter_actually_counts(tmp_path):
    """Can-fail leg for the TRUTH itself. A counter that returned a constant
    would make every pin below agree with it forever while the front door
    said whatever it liked. Remove one row off-tree; the count must fall by
    exactly one."""
    root = str(tmp_path / "rows")
    os.makedirs(os.path.join(root, "docs", "experiments"))
    src = os.path.join(str(REPO), "docs", "experiments", "README.md")
    dst = os.path.join(root, "docs", "experiments", "README.md")
    shutil.copyfile(src, dst)
    before, ids = experiment_rows(root)
    lines = _lines(dst)
    kept = []
    dropped = 0
    for ln in lines:
        if dropped == 0 and re.match(r"^\|\s*\[?E\d{2,3}\b", ln):
            dropped = 1
            continue
        kept.append(ln)
    with io.open(dst, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(kept))
    after, _ = experiment_rows(root)
    assert dropped == 1, "the fixture removed no row, so nothing was tested"
    assert after == before - 1, (
        "removing one status-table row moved the count from %d to %d; a "
        "counter that does not track its own table cannot pin anything"
        % (before, after))


def test_the_experiment_counter_refuses_a_headerless_table(tmp_path):
    """The other direction: a restructured table must HALT, not quietly
    return a number from a document it no longer understands."""
    root = str(tmp_path / "noheader")
    os.makedirs(os.path.join(root, "docs", "experiments"))
    dst = os.path.join(root, "docs", "experiments", "README.md")
    src = _lines(os.path.join(str(REPO), "docs", "experiments", "README.md"))
    with io.open(dst, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(ln for ln in src if not re.match(r"^\|\s*id\s*\|", ln)))
    with pytest.raises(AssertionError) as e:
        experiment_rows(root)
    assert "status-table header" in str(e.value)


# ---------------------------------------------------------------------------
# fourth leg, part 2 - the pins
# ---------------------------------------------------------------------------

def experiment_pin_spans(root):
    """{rel: [(line, start, end)]} consumed by an experiment pin."""
    spans = {}
    for rel, _name, pat in EXPERIMENT_PINS:
        p = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.exists(p):
            continue
        for i, ln in enumerate(_lines(p), 1):
            for m in re.finditer(pat, ln):
                spans.setdefault(rel, []).append((i, m.start(), m.end()))
    return spans


def experiment_pin_failures(root, want):
    """Which experiment pins would fail against `root` - run off-tree by the
    can-fail legs, and by the real leg against REPO."""
    bad = []
    for rel, name, pat in EXPERIMENT_PINS:
        p = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.exists(p):
            bad.append((rel, name, "missing"))
            continue
        found = []
        for i, ln in enumerate(_lines(p), 1):
            for m in re.finditer(pat, ln):
                found.append((i, m.group(1)))
        if len(found) != 1:
            bad.append((rel, name, "%d matches" % len(found)))
            continue
        line, token = found[0]
        value = english_cardinal(token)
        if value is None:
            bad.append((rel, name, "L%d states %r, which this leg's declared "
                                   "notation does not read as a number"
                        % (line, token)))
        elif value != want:
            bad.append((rel, name, "L%d states %d, the table holds %d"
                        % (line, value, want)))
    return bad


@pytest.mark.parametrize("rel,name,pat", EXPERIMENT_PINS,
                         ids=["%s::%s" % (p[0], p[1]) for p in EXPERIMENT_PINS])
def test_every_pinned_site_states_the_experiment_count(
        rel, name, pat, experiments):
    p = os.path.join(str(REPO), rel.replace("/", os.sep))
    assert os.path.exists(p), "pinned surface is gone: %s" % rel
    found = [(i, m.group(1)) for i, ln in enumerate(_lines(p), 1)
             for m in re.finditer(pat, ln)]
    assert len(found) == 1, (
        "%s :: %s - the anchor matched %d times, expected exactly 1. A "
        "rewritten sentence must be re-pinned in the commit that rewrites it."
        % (rel, name, len(found)))
    line, token = found[0]
    value = english_cardinal(token)
    assert value is not None, (
        "%s:%d :: %s - states %r, which is not a notation this leg reads. "
        "See the NOTATION BOUNDARY block above: digits and English cardinals "
        "0-99 only." % (rel, line, name, token))
    assert value == experiments, (
        "%s:%d :: %s - states %d experiments, the status table in "
        "docs/experiments/README.md holds %d. Every surface in "
        "EXPERIMENT_PINS changes in the commit that adds an experiment row."
        % (rel, line, name, value, experiments))


# ---------------------------------------------------------------------------
# fourth leg, part 3 - the sweep
# ---------------------------------------------------------------------------

def experiment_unaccounted(root):
    """Every experiment-count-shaped hit that is neither pinned, nor declared
    non-total, nor inside a region the test-count legs already declared
    historical. Returns [(rel, line, value)], ASCII only."""
    spans = experiment_pin_spans(root)
    whole, inline, cl_from, _ = historical_spans(root)
    bad = []
    for rel in surfaces(root):
        p = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.exists(p):
            continue
        if rel in NOT_SWEPT:
            continue
        if rel in whole or rel.startswith(HISTORICAL_PREFIXES[0][0]):
            continue
        lines = _lines(p)
        for (i, s, e, v) in experiment_hits(p):
            if any(li == i and s >= ls and e <= le
                   for (li, ls, le) in spans.get(rel, [])):
                continue
            if rel == "CHANGELOG.md" and cl_from is not None and i >= cl_from:
                continue
            if any(li == i and s >= ls for (li, ls, le) in inline.get(rel, [])):
                continue
            if any(r == rel and val == v and anchor in lines[i - 1]
                   for r, anchor, val, _why in EXPERIMENT_NOT_TOTAL):
                continue
            bad.append((rel, i, v))
    return bad


def test_no_unaccounted_experiment_count_on_any_surface():
    """Every experiment-count-shaped number on a declared surface is pinned as
    the record's size, declared narrative, or declared historical. An
    unaccounted hit means a site exists that nothing is watching - which is
    how `site/src/site-config.ts` sat at "Twenty experiments" while the record
    held twenty-eight, and how `docs/advisor-kickoff.md` sat at 27. Both were
    found by THIS leg on the tree it was written against."""
    bad = experiment_unaccounted(str(REPO))
    assert not bad, (
        "%d experiment-count-shaped number(s) on a declared surface are "
        "neither pinned nor declared:\n%s\n\n"
        "Pin it in EXPERIMENT_PINS if it states the record's SIZE, or add it "
        "to EXPERIMENT_NOT_TOTAL with its reason if it is narrative about a "
        "past state. Deciding which is a deliberate edit, which is the point."
        % (len(bad), "\n".join("   %s:%d  (%d)" % b for b in bad)))


def test_every_declared_non_total_experiment_site_is_real():
    """A declaration that matches nothing is a dead exemption quietly widening
    the sweep's blind spot."""
    dead = []
    for rel, anchor, _value, _why in EXPERIMENT_NOT_TOTAL:
        p = os.path.join(str(REPO), rel.replace("/", os.sep))
        text = "\n".join(_lines(p)) if os.path.exists(p) else ""
        if anchor not in text:
            dead.append("%s :: %s" % (rel, anchor))
    assert not dead, (
        "declared non-total experiment sites that match nothing: %s"
        % ", ".join(dead))


# ---------------------------------------------------------------------------
# fourth leg, part 4 - the legs above are not vacuous (E26 gate 2)
# ---------------------------------------------------------------------------
# The dispatch requires that this leg FAIL on a deliberately stale surface
# before it passes at HEAD. It did better than that: it fired on TWO REAL
# STALE SITES on the tree it was written against - `site/src/site-config.ts`
# at "Twenty" and `docs/advisor-kickoff.md` at 27, against a table holding
# twenty-eight. Those are corrected in the same commit, so the proof below is
# the synthetic one that stays runnable afterwards.

def test_a_stale_experiment_site_fails_the_pin_leg(tmp_path, experiments):
    """Byte-identical to HEAD except one number, and the failure names it."""
    root = _mirror(str(REPO), str(tmp_path / "exp_stale"))
    os.makedirs(os.path.join(root, "docs", "experiments"), exist_ok=True)
    shutil.copyfile(
        os.path.join(str(REPO), "docs", "experiments", "README.md"),
        os.path.join(root, "docs", "experiments", "README.md"))
    assert not experiment_pin_failures(root, experiments), (
        "the MIRROR of HEAD already fails the experiment pin leg, so the next "
        "assertion would prove nothing about staleness")
    _rewrite(os.path.join(root, "docs", "advisor-kickoff.md"),
             "%d experiments. No staleness" % experiments,
             "%d experiments. No staleness" % (experiments - 3))
    bad = experiment_pin_failures(root, experiments)
    assert len(bad) == 1, "expected exactly one pin to fail, got %r" % (bad,)
    assert bad[0][0] == "docs/advisor-kickoff.md", (
        "the failure did not name the site that was made stale: %r" % (bad,))


def test_a_stale_word_spelled_site_fails_the_pin_leg(tmp_path, experiments):
    """The word form gets its own proof, because it is the notation this leg
    exists for - the test-count legs never had to read one."""
    root = _mirror(str(REPO), str(tmp_path / "exp_word"))
    os.makedirs(os.path.join(root, "docs", "experiments"), exist_ok=True)
    shutil.copyfile(
        os.path.join(str(REPO), "docs", "experiments", "README.md"),
        os.path.join(root, "docs", "experiments", "README.md"))
    assert not experiment_pin_failures(root, experiments)
    p = os.path.join(root, "README.md")
    with io.open(p, encoding="utf-8") as fh:
        t = fh.read()
    m = re.search(r"([A-Za-z][A-Za-z-]*) experiments are in\b", t)
    assert m and english_cardinal(m.group(1)) == experiments, (
        "the fixture's own anchor no longer reads the current count")
    with io.open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(t.replace("%s experiments are in" % m.group(1),
                           "Nineteen experiments are in", 1))
    bad = experiment_pin_failures(root, experiments)
    assert any(r == "README.md" and "19" in msg for r, _n, msg in bad), (
        "a word-spelled stale count did not fire the pin leg: %r" % (bad,))


def test_a_new_unwatched_experiment_site_fails_the_sweep(tmp_path):
    """The sweep's own can-fail leg."""
    root = _mirror(str(REPO), str(tmp_path / "exp_newsite"))
    assert not experiment_unaccounted(root), (
        "the MIRROR of HEAD already has unaccounted experiment hits, so the "
        "next assertion would prove nothing: %r"
        % (experiment_unaccounted(root)[:5],))
    p = os.path.join(root, "SECURITY.md")
    with io.open(p, "a", encoding="utf-8", newline="") as fh:
        fh.write("\n\nThirty-one experiments are in the record.\n")
    bad = experiment_unaccounted(root)
    assert any(rel == "SECURITY.md" and v == 31 for rel, _, v in bad), (
        "the sweep did not see a brand-new unpinned experiment count: %r"
        % (bad,))


def test_the_experiment_sweep_does_not_fire_on_a_historical_count(tmp_path):
    """A released CHANGELOG entry is correct forever; the same sentence above
    the released boundary is a current-state claim. Same boundary the test
    count uses, exercised for this quantity."""
    root = _mirror(str(REPO), str(tmp_path / "exp_hist"))
    assert not experiment_unaccounted(root)
    cl = os.path.join(root, "CHANGELOG.md")
    at = changelog_historical_from(root)
    assert at is not None
    lines = _lines(cl)
    lines.insert(at + 2, "Sixteen experiments were in the record at this tag.")
    with io.open(cl, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(lines))
    assert not experiment_unaccounted(root), (
        "a count inside a RELEASED changelog entry fired the experiment "
        "sweep; released entries state what a version shipped")
    lines = _lines(cl)
    lines.insert(at - 1, "Sixteen experiments were in the record at this tag.")
    with io.open(cl, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(lines))
    bad = experiment_unaccounted(root)
    assert any(rel == "CHANGELOG.md" and v == 16 for rel, _, v in bad), (
        "a count in the Unreleased block did NOT fire the experiment sweep: "
        "%r" % (bad[:5],))


def test_the_release_note_historical_count_does_not_fire():
    """`.github/release-notes-v0.1.0.md` says "Twenty experiments" and is
    correct forever - it states what that version shipped. It must not fire,
    and it must still BE there, or this assertion is testing nothing."""
    p = os.path.join(str(REPO), ".github", "release-notes-v0.1.0.md")
    assert os.path.exists(p)
    hits = experiment_hits(p)
    assert any(v == 20 for _i, _s, _e, v in hits), (
        "the release note no longer carries the historical count this test "
        "exists to prove is exempt")
    assert not [b for b in experiment_unaccounted(str(REPO))
                if b[0].startswith(".github/release-notes-")], (
        "a published release note's historical count fired the sweep")


def test_experiment_notation_boundary_is_what_it_says():
    """Every line of the NOTATION BOUNDARY block above, made runnable.

    THIS TEST ASSERTS WHAT IS **NOT** CAUGHT, on purpose. Widening the parser
    to read French or Devanagari is a legitimate change - it just has to be
    made ON PURPOSE, in the commit that edits this test, which is the whole
    point of putting a boundary under a test rather than in a comment."""
    # caught
    assert english_cardinal("27") == 27
    assert english_cardinal("Twenty-eight") == 28
    assert english_cardinal("twenty six") == 26
    assert english_cardinal("four") == 4
    assert english_cardinal("seven") == 7
    assert english_cardinal("NINETY-NINE") == 99
    # not caught - the six generated translations' spellings, measured from
    # the READMEs at the time this leg was written
    for foreign in ("veintiseis", "vingt-six", "ventisei", "vinte e seis",
                    "twenty-eighth", "several", "a few", "one hundred and one"):
        assert english_cardinal(foreign) is None, (
            "%r now parses, so this leg's declared notation boundary has "
            "moved. That may be correct - update this test and the NOTATION "
            "BOUNDARY block together." % foreign)
    # and the boundary is reached through `trailing_count`, not just the
    # parser, because that is the function the sweep actually calls.
    #
    # THE HYPHEN RULE, which is the part that was wrong first time round:
    # an unparseable HYPHENATED pair declines outright; an unparseable
    # SPACE-separated pair still falls back to its last token.
    assert trailing_count("vingt-six ") is None, (
        "a French compound now returns a number. It would be read as SIX - "
        "a confidently wrong reading, which is the failure mode this rule "
        "exists for.")
    assert trailing_count("redirected four ")[0] == 4, (
        "the space fallback died with the hyphen fix; `four experiments` in "
        "ordinary prose would stop being seen")
    assert trailing_count("Twenty-eight ")[0] == 28
    assert trailing_count("81 laws, 27 ")[0] == 27
    assert trailing_count("the first seven ")[0] == 7
