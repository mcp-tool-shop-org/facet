# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""canon_compose.py - CANON -> PROMPT. E60 Stage 0.

WHY THIS EXISTS. E60's question is whether a prompt COMPOSED from the
ratified canon produces a reference at least as good as the hand-written
prose that made canon/A1_reference.png. This module is the composer half of
that question: canon/a1.surfaces.json (occupant phrases + legal_clauses) in,
a generation-ready prompt out. It does not judge, rank, or decide which arm
wins - it only builds text and checks that text against tools/canon_gate.py,
the same gate every other spend site in this repo answers to.

THE HARD CONSTRAINT THIS FILE WAS BUILT AGAINST, discovered while writing it
rather than assumed from the charter. canon_gate.check_prompt()'s reverse
check (schema 2, unlicensed_residue()) strips every licensed phrase from the
prompt, then strips punctuation and a FIXED stopword list -
"a|an|the|with|and|or|of|on|in|at|to|for|from|by|as|his|her|its|their|this|
that|each" - and refuses if anything survives. The reference's OWN prompt
uses "over" to join the vest and shirt ("...embroidery over a cream
high-collared shirt...") and "over" is not in that list: canon/A1-IDENTITY.md
already documents that the raw recipe text does not pass this gate for
exactly this reason. So Arm P's "join related garments with prepositions"
(the charter's own words) can only use STOP-LIST prepositions - with/of/on/
in/at/to/for/from/by/as - never "over". Every joiner function below is built
from that closed set on purpose; nothing here invents connective vocabulary.

THE VIEW ARGUMENT, and its actual scope. canon/A1-IDENTITY.md's POSE section
states the law this mechanises: "only the front view shows the face
frontally." The face-bearing clauses this file drops at a non-front view are
exactly the charter's own list - eyes (N9), mouth/smile (N10), and the
style_face legal_clause ("crisp readable facial features") - not a general
per-surface visibility table for all ten NAMED elements across all eight
yaws (that is twin-ring territory and out of E60's scope by the charter's
own words). A1's canon carries no declared `scopes.views` entries, so
canon_gate.check_prompt(scope="view:N") ANDONs for any view id on this
subject; Gate 1 (the composer's prompt must pass the gate) is therefore only
exercised, and only claimed to hold, at the FRONT view (scope="subject"),
which is the only view Stage 2 ever spends against. A rear-view compose is
checked directly against its OWN text (does it still contain a face phrase)
rather than through the gate, because there is no declared scope for the
gate to check it against - this is reported, not glossed over, in
selftest()'s own comments.

THREE FORMS, one composer:
  grouped       (Arm P) - framing -> staging -> style -> identity, garments
                joined as "G1 and G2, G3, G4 and G5" (the first two
                and-bound as a worn-together pair, the rest a comma list
                with a final "and"), features the same shape.
  flat          (Arm L) - the E58/profiles/a1.json convention: framing, then
                every phrase (garments, features, style, backdrop,
                negatives, pose) joined with a bare comma, in the SAME order
                profiles/a1.json's own fallback prompt uses (pose clauses
                appended last, because that is literally how that string
                grew - E59 Stage 0 appended them to an already-written flat
                list). No "and" appears anywhere in this form except inside
                a phrase's own text (e.g. "hands empty and open").
  consolidated  (Arm G) - identical to grouped except the GARMENTS are
                chained with "with" instead of commas ("G1 with G2 with G3
                with G4 and G5"), collapsing five list positions into one
                unbroken noun phrase. Only the garment span changes -
                finding 1 (Rassin et al., SynGen) is about entity count, not
                grammar, so the manipulation is isolated to the clause the
                finding is about. Features are untouched (charter: "Arm G -
                composed prose with the GARMENT consolidated").

GARMENT VS FEATURE, a heuristic and its scope. There is no declared field in
the schema for "this occupant is worn, that one is anatomy" - a1.surfaces.json
gives NAMED occupants and the SURFACE ids they sit on, nothing more. This
file classifies by a substring hint list against every surface id an
occupant shares (GARMENT_HINTS below); for A1 the split is exact (vest,
shirt, sash, trousers, shoes vs hair, skin, eyes, mouth, ink-stained hands).
It is declared here as a heuristic, not asserted as a general solution -
a future subject with an un-hinted garment name would need a hint added, not
a rewrite.

NAMED ORDER. Occupants are ordered by the numeric part of their N-id (N1,
N2, ... N10), not by file-appearance order. For A1 this is not a stylistic
default: it is the same order profiles/a1.json's flat prompt and E58's own
per-view prompts already use, and it happens to reproduce the ORIGINAL
recipe's own feature ordering (olive skin, curls, ink, eyes, smile = N6..
N10) without being tuned toward it - the convergence falls out of N-id order
being a sensible reading order on this subject, the same way it already was
for the studio's established flat form.

Standards compliance (CLAUDE.md workflow-standards.md, scored 0-3):
  PIN_PER_STEP        - 2. Every phrase this file emits is read live from the
    loaded canon doc (never retyped), so a composed prompt cannot silently
    diverge from the ratified text. Not 3: the joiner CHOICES (which
    prepositions, which grouping) are code, not data, so a different
    grouping requires a code change, not a config change.
  ANDON_AUTHORITY      - 2. `Andon`/`_andon` here, `raise` not `assert`
    (E21 Ruling 2 / E22's law), mirroring canon_gate.py's own class. Gate 1
    (front-view compose must pass canon_gate) is enforced by the CLI's exit
    code and by selftest(); nothing here silently drops to a warn.
  NAMED_COMPENSATORS   - n/a. This module performs no irreversible action
    (no spend, no write outside stdout); Stage 2's batch-submission script
    carries the compensators table for the paid generations.
  DECOMPOSE_BY_SECRETS - 3. Phrase extraction (named_occupants, clause,
    mesh_style_phrases), classification (is_garment, is_face_bound), joining
    (three separate joiner functions, one per form), and gate-checking
    (check_composed, a thin wrapper) are each their own function - a form
    change touches only its own joiner, a classification change touches
    only the hint list.
  UNCERTAINTY_GATED_HUMANS - 2. The anchor's three-way diff (Stage 1) reports
    canon-only / recipe-only sets rather than resolving them; canon debt is
    surfaced for the Director, never silently patched by this file.
  EXTERNAL_VERIFIER    - 3. Every gate check runs through tools/canon_gate.py
    unmodified - this file never re-implements or loosens the reverse/
    forward coverage check it depends on.

  E61 ADDENDUM (garment_join, joints, with_occupant_phrase): scores
  unchanged from above - same shape, same guarantees. PIN_PER_STEP stays 2
  (still code, not data, that decides which preposition/joints a caller may
  request). ANDON_AUTHORITY stays 2 (three new can-fail legs in selftest(),
  same raise-not-assert class as everything else here). EXTERNAL_VERIFIER
  stays 3 (with_occupant_phrase's own can-fail leg checks the SAME text
  against BOTH the modified doc and the live one, proving the live gate's
  requirement is real and enforced, not just internally consistent with
  itself).

  E62 ADDENDUM (depends_on consultation): PIN_PER_STEP - 2, unchanged (the
  edge is read live from canon_gate.depends_on_pairs(doc), never retyped).
  ANDON_AUTHORITY - 2 (the new refusal is unconditional - runs on every
  form's output, not opt-in - and carries three REQUIRED can-fail legs,
  each proven by reversion: see the fence-1 legs in selftest() and this
  arc's report for the monkeypatch transcripts). NAMED_COMPENSATORS - n/a,
  unchanged. DECOMPOSE_BY_SECRETS - 2 (the depends_on check is its own
  function, _refuse_if_and_joins_a_dependent_pair, called from both
  compose() return points rather than folded into either joiner).
  UNCERTAINTY_GATED_HUMANS - 2 (A1's depends_on rows are DRAFT canon,
  marked as such in a1.surfaces.json's own notes, reported for the
  Director's ratification at the fold - same standing as every other
  canon-data decision in this file). EXTERNAL_VERIFIER - 2 (the check runs
  through canon_gate.depends_on_pairs(), never re-deriving the edge; not 3
  because the "and" vs "over"/unjoined DECISION is this file's own code,
  same as every other joiner choice here).

E61 ADDITIONS (layering-repair arms, docs/experiments/E61-layering-repairs-
kickoff.md). Three new knobs, all opt-in via keyword args so every existing
call (E60's Stage 2, this file's own selftest) keeps producing byte-identical
output with no argument supplied.

  garment_join="and" (default) | "over" - only wired into form="grouped"
    (Andon otherwise). Changes ONE connector: the head-pair join inside
    _join_grouped_garments from " and " to " over ", isolating the single
    preposition E60 traced its failure to (the reference's own recipe joins
    vest+shirt with "over"; STOP already admits it - E60 fold). Everything
    else about the grouped join (comma list, final "and") is untouched. Has
    no effect when a subject has <=3 garments (the degenerate plain-list
    branch of _join_grouped_garments never reaches the head-pair code path)
    - declared, not silently absorbed; A1 always has 5.

  joints=() - a tuple of doc["joints"] ids to emit as additional trailing
    sentences (capitalised, period-closed), via the now-licensed (E60 fold)
    joint phrases. Licensing is not requiring: joints=() (default) emits
    nothing and is unaffected; nothing in canon_gate requires a joint phrase
    to appear. Wired into BOTH flat and grouped/consolidated forms
    symmetrically, so the parameter is never silently a no-op in one branch.

  with_occupant_phrase(doc, n_id, phrase) - returns a DEEP-COPIED doc with
    every surface carrying occupant id `n_id` given a new phrase; the caller
    passes this copy to compose() AND to check_composed() so a prompt is
    always composed and gated against the SAME assumptions. Built because
    E61's P0/P1 arms compose against A1's PRE-repair N1 text ("a plum
    long-vest with fine gold embroidery", no "sleeveless") without touching
    canon/a1.surfaces.json on disk - the charter's own words: "Build it by
    parameterising the composer, NOT by reverting the canon files on disk."
    Checking such text against the LIVE (post-repair) doc would ANDON on a
    missing required phrase for a reason that has nothing to do with the arm
    under test; checking it against the doc this same function produced
    tests what the arm can actually be honest about.

E62 ADDITIONS (the schema patch, docs/experiments/E62-schema-patch-kickoff.
md). compose() now REFUSES a depends_on pair coordinated with "and" -
unconditionally, on every form's output, not behind a keyword arg.

  _refuse_if_and_joins_a_dependent_pair(doc, composed_text) - called at
    BOTH of compose()'s return points (flat's early return, and the
    grouped/consolidated join at the bottom). Reads canon_gate.
    depends_on_pairs(doc), resolves each edge to its two occupants' CURRENT
    phrases via named_occupants() (honest for a with_occupant_phrase-
    modified doc too), and refuses if the composed text contains either
    phrase directly adjacent to " and " the other - case-insensitive, both
    orders, an exact two-phrase substring test rather than a bare "and"
    search (which would fire on a phrase's own internal "and", e.g. "hands
    empty and open"). "over" is licensed; leaving the pair unjoined (flat
    form) is licensed; "and" between exactly those two phrases is the one
    illegal join, and it is not opt-in - a caller cannot silently produce
    it by omitting an argument.

  LOAD-BEARING CONSEQUENCE, stated rather than left to be discovered: A1's
  canon (canon/a1.surfaces.json) now declares vest_torso/vest_skirt
  depends_on: ["N2"] (the vest layers over the shirt). Because
  garment_join's OWN default has always been "and" (E60's original,
  unfixed behaviour, kept as the default on purpose - see the E61 ADDITIONS
  note above), compose(doc, form="grouped") with NO garment_join argument
  now ANDONs on A1 by design: the bare default coordinates exactly the
  depends_on pair with "and" in the head-pair join. This is fence 1a
  working, not a regression - every caller of compose() on a subject with a
  depends_on-linked head pair must now pass garment_join="over" or use
  form="flat" (or "consolidated", if the pair does not land in ITS last
  two garments - A1's does not, so consolidated is unaffected). selftest()
  below passes garment_join="over" explicitly everywhere its OWN leg is
  not itself testing the "and" refusal.

CLI:
  python tools/canon_compose.py --selftest
  python tools/canon_compose.py compose --canon canon/a1.surfaces.json \
      --view front --form grouped
  python tools/canon_compose.py anchor --canon canon/a1.surfaces.json \
      --recipe canon/A1-RECIPE.json --view front
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_TOOLS)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import canon_gate  # noqa: E402

TOOL_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# view handling
# ---------------------------------------------------------------------------
VIEW_ALIASES = {"front": 0, "rear": 180, "back": 180}


class Andon(ValueError):
    pass


def _andon(msg):
    raise Andon("ANDON: " + msg)


def parse_view(view):
    """Normalize a view argument to an integer yaw degree, 0-359.

    'front' -> 0, 'rear'/'back' -> 180, a bare number is read as a yaw
    degree directly (matching the studio's 8-camera convention: 0, 45, 90,
    135, 180, 225, 270, 315). Anything else refuses rather than guessing.
    """
    if view is None:
        return 0
    if isinstance(view, (int, float)):
        return int(view) % 360
    s = str(view).strip().lower()
    if s in VIEW_ALIASES:
        return VIEW_ALIASES[s]
    try:
        return int(float(s)) % 360
    except ValueError:
        _andon("unrecognized view %r (use front/rear/back or a yaw degree)" % (view,))


def face_visible(view):
    """canon/A1-IDENTITY.md POSE section: 'only the front view shows the
    face frontally.' Mechanised as: face-bearing clauses appear ONLY at
    yaw 0. This is deliberately binary, not a graded band across the 45-
    and 315-degree views - see the module docstring's VIEW ARGUMENT note
    for why a finer table is out of this arc's scope."""
    return parse_view(view) == 0


# ---------------------------------------------------------------------------
# phrase extraction
# ---------------------------------------------------------------------------
_NID_RE = re.compile(r"^N(\d+)$")


def _n_sort_key(n_id):
    m = _NID_RE.match(str(n_id))
    return (0, int(m.group(1))) if m else (1, str(n_id))


def named_occupants(doc):
    """Unique (n_id, phrase, surface_ids) for every prompt-provenance
    occupant, deduplicated across surfaces that share one occupant (N1 sits
    on both vest_torso and vest_skirt; N2 on shirt_collar/sleeve_L/sleeve_R;
    N5 on shoe_L/shoe_R; N6 on face/neck; N8 on hand_L/hand_R), ordered by
    N-number. `surface_ids` carries EVERY surface id sharing the occupant,
    not just the first, so classification below can check all of them.

    ANDONs if one occupant id is attached to two different phrase strings -
    that would mean the canon file disagrees with itself about what an
    occupant IS, which no composer should paper over.
    """
    seen = {}
    order = []
    for s in doc["surfaces"]:
        occ = s.get("occupant") or {}
        if occ.get("provenance") != "prompt":
            continue
        ph = occ.get("phrase")
        if not ph:
            continue
        nid = occ.get("id")
        if nid not in seen:
            seen[nid] = {"n_id": nid, "phrase": ph, "surface_ids": []}
            order.append(nid)
        elif seen[nid]["phrase"] != ph:
            _andon(
                "occupant %s carries two different phrases across surfaces "
                "(%r vs %r)" % (nid, seen[nid]["phrase"], ph))
        seen[nid]["surface_ids"].append(s["id"])
    order.sort(key=_n_sort_key)
    return [seen[n] for n in order]


# Substring hints against a SURFACE id (not the phrase text) that mark an
# occupant as worn rather than anatomical. Declared, not exhaustive - see
# the module docstring's GARMENT VS FEATURE note.
GARMENT_HINTS = ("vest", "shirt", "sleeve", "sash", "trouser", "pant",
                 "shoe", "boot", "glove", "gauntlet", "coat", "cloak",
                 "belt", "pauldron", "bracer", "kilt", "tunic", "cuff",
                 "cape", "hat", "helm", "armor", "armour")

# charter Stage 0: "Face-bearing clauses (eyes, smile, crisp facial
# features)". Keyed on SURFACE id (stable across subjects), not N-id
# (subject-specific).
FACE_SURFACE_IDS = {"eyes", "mouth"}
FACE_LEGAL_CLAUSE_IDS = {"style_face"}


def is_garment(entry):
    for sid in entry["surface_ids"]:
        low = sid.lower()
        if any(h in low for h in GARMENT_HINTS):
            return True
    return False


def is_face_bound(entry):
    return any(sid in FACE_SURFACE_IDS for sid in entry["surface_ids"])


def clause(doc, clause_id):
    for c in doc.get("legal_clauses") or []:
        if c.get("id") == clause_id:
            return c.get("phrase")
    return None


def _joint_phrase(doc, joint_id):
    """doc['joints'] entry's phrase, by id. E61 addition. ANDONs on an
    unknown id rather than silently emitting nothing - a typo'd id here
    should never quietly compose as if joints=() had been passed."""
    for j in doc.get("joints") or []:
        if j.get("id") == joint_id:
            ph = j.get("phrase")
            if not ph:
                _andon("joint %r has no phrase" % (joint_id,))
            return ph
    _andon("no joint %r in canon (declared: %s)"
           % (joint_id, [j.get("id") for j in doc.get("joints") or []]))


def with_occupant_phrase(doc, n_id, phrase):
    """A DEEP COPY of doc with every surface carrying occupant id `n_id`
    given `phrase` instead. E61 addition - see module docstring's E61
    ADDITIONS note for why this exists: compose() AND check_composed() are
    meant to run against the SAME modified doc, never the live one for one
    and this copy for the other.

    ANDONs if n_id names no occupant in doc - a silent no-op here would let
    a typo'd id compose against the UNCHANGED live phrase while the caller
    believes it built pre-repair text, which is exactly the kind of
    unmeasured claim this repo's own rules warn against."""
    d2 = copy.deepcopy(doc)
    found = False
    for s in d2["surfaces"]:
        occ = s.get("occupant")
        if occ and occ.get("id") == n_id:
            occ["phrase"] = phrase
            found = True
    if not found:
        _andon("with_occupant_phrase: no occupant %r in doc" % (n_id,))
    return d2


def _dependent_phrase_pairs(doc):
    """(child_phrase, parent_phrase) for every depends_on edge declared on
    doc, lowercased, resolved via named_occupants() so a phrase reflects
    whatever text is ACTUALLY live in `doc` right now - honest for a
    with_occupant_phrase-modified copy too, matching this file's existing
    E61 discipline (compose() and check_composed() always run against the
    SAME doc). E62 addition - the composer's own consultation of the
    depends_on edge (charter: "canon_compose consults the edge")."""
    pairs = canon_gate.depends_on_pairs(doc)
    if not pairs:
        return []
    by_id = {o["n_id"]: o["phrase"] for o in named_occupants(doc)}
    out = []
    for pair in pairs:
        a, b = tuple(pair)
        pa, pb = by_id.get(a), by_id.get(b)
        if pa and pb:
            out.append((pa.lower(), pb.lower()))
    return out


def _refuse_if_and_joins_a_dependent_pair(doc, composed_text):
    """E62 fence 1: a depends_on pair may be composed with 'over' (licensed,
    E61/5df9d20) or left unjoined (flat form, Arm L - also licensed, held
    3/3 in E61) but may NEVER be coordinated with the bare word 'and'
    directly between their two phrases - no comma, no other word between
    them. Over is not required; and is the one illegal join.

    Checked on the OUTPUT TEXT, case-insensitively (matching this file's own
    p_rear.lower()/lower_front convention elsewhere), in both phrase orders,
    as an EXACT two-phrase adjacency test - not a bare 'and' substring
    search, which would fire on the word appearing anywhere else in the
    prompt (a phrase's own internal text can carry 'and', e.g. "hands empty
    and open"). This runs uniformly across all three forms rather than as a
    flag threaded through every joiner: flat is safe by construction (it
    never emits 'and' between garment phrases at all - see this file's own
    module docstring); consolidated is safe for a HEAD pair specifically
    (its 'and' joins only the LAST two garments); grouped's head-pair join
    is exactly where 'and' is the historical default this law forbids for a
    depends_on pair. Checking the text once, generically, covers all three
    without assuming which internal code path built it."""
    lower = composed_text.lower()
    for pa, pb in _dependent_phrase_pairs(doc):
        if (pa + " and " + pb) in lower or (pb + " and " + pa) in lower:
            _andon(
                "depends_on pair coordinated with 'and': %r / %r - licensed "
                "joins are 'over' or leaving them unjoined, never 'and' "
                "(E62 fence 1)" % (pa, pb))


def clauses_by_class(doc, cls):
    return [c for c in doc.get("legal_clauses") or [] if c.get("class") == cls]


def mesh_style_phrases(doc):
    """Mesh-provenance surfaces carrying a non-null phrase ('realistic
    stylized proportions' on A1) - dual-attested: present in the generating
    prompt AND destined to arrive from the mesh once one exists (W3
    Amendment 12 precedent, cited in canon/A1-IDENTITY.md). Licensed (any
    occupant.phrase is, regardless of provenance - canon_gate.licensed_
    phrases()) but not REQUIRED (provenance != "prompt", so canon_gate.
    required_phrases() does not demand it); including it is this composer's
    own choice, made because the recipe's own style clause carries it."""
    out = []
    for s in doc["surfaces"]:
        occ = s.get("occupant") or {}
        if occ.get("provenance") == "mesh" and occ.get("phrase"):
            out.append(occ["phrase"])
    return out


# ---------------------------------------------------------------------------
# joiners - every connective word here is in canon_gate.STOP or is a
# licensed phrase's own internal text. See module docstring's hard-
# constraint note.
# ---------------------------------------------------------------------------

def _cap(s):
    return s[:1].upper() + s[1:] if s else s


def _join_and_list(items):
    """'A' | 'A and B' | 'A, B and C' - comma list, final separator ' and '
    rather than a comma (the recipe's own list style)."""
    items = [i for i in items if i]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def _join_grouped_garments(phrases, head_sep=" and "):
    """Arm P: the first two garments joined by `head_sep` (the worn-together
    pair the recipe expressed with the illegal 'over'; E61 adds the option
    to pass ' over ', the reference's own word, now STOP-admitted), the
    remainder a comma list with a final 'and'. Degrades to a plain and-list
    below 4 items, where the head-plus-rest construction would just repeat
    'and' twice - head_sep has NO EFFECT in that branch (declared, not
    silently absorbed; see module docstring's E61 ADDITIONS note)."""
    phrases = [p for p in phrases if p]
    n = len(phrases)
    if n <= 3:
        return _join_and_list(phrases)
    head = phrases[0] + head_sep + phrases[1]
    middle = phrases[2:-1]
    tail = phrases[-1]
    return ", ".join([head] + middle) + " and " + tail


def _join_consolidated_garments(phrases):
    """Arm G: every garment chained with 'with' except the last, which
    takes 'and' - zero internal commas, one unbroken noun phrase, the
    literal operationalisation of 'fewer, richer noun phrases' under the
    gate's closed connector set (no adjective fusion is possible without
    inventing vocabulary the gate would flag as unlicensed residue)."""
    phrases = [p for p in phrases if p]
    n = len(phrases)
    if n == 0:
        return ""
    if n == 1:
        return phrases[0]
    return " with ".join(phrases[:-1]) + " and " + phrases[-1]


# ---------------------------------------------------------------------------
# section builders (grouped / consolidated share these; flat does not use
# sections at all - see compose())
# ---------------------------------------------------------------------------

def _staging_groups(doc):
    """(pose, bg, negatives) - three lists of legal_clause phrases, staging
    class only. pose is ordered head/arms/hands/feet by hint match; bg and
    negatives keep file order. Declared sub-grouping, not schema data."""
    staging = clauses_by_class(doc, "staging")
    pose_hints = ("head", "arms", "hands", "feet")

    def pose_rank(c):
        for i, h in enumerate(pose_hints):
            if h in c["id"]:
                return i
        return len(pose_hints)

    pose = sorted((c for c in staging if any(h in c["id"] for h in pose_hints)),
                  key=pose_rank)
    pose_ids = {c["id"] for c in pose}
    bg = [c for c in staging
          if c["id"] not in pose_ids and ("bg" in c["id"] or "backdrop" in c["id"])]
    bg_ids = {c["id"] for c in bg}
    neg = [c for c in staging if c["id"] not in pose_ids and c["id"] not in bg_ids]
    return ([c["phrase"] for c in pose],
            [c["phrase"] for c in bg],
            [c["phrase"] for c in neg])


def _style_phrases(doc, fv):
    out = []
    for c in clauses_by_class(doc, "style"):
        if c["id"] in FACE_LEGAL_CLAUSE_IDS and not fv:
            continue
        out.append(c["phrase"])
    out += mesh_style_phrases(doc)
    return out


def _garment_feature_split(doc, fv):
    occs = named_occupants(doc)
    garments = [o["phrase"] for o in occs if is_garment(o)]
    features = [o for o in occs if not is_garment(o)]
    if not fv:
        features = [o for o in features if not is_face_bound(o)]
    return garments, [o["phrase"] for o in features]


# ---------------------------------------------------------------------------
# compose
# ---------------------------------------------------------------------------
FORMS = ("grouped", "flat", "consolidated")


def compose(doc, view="front", form="grouped", garment_join="and", joints=()):
    """canon -> prompt. Pure function: does not check the gate (see
    check_composed) and does not write anything.

    garment_join and joints are E61 additions (see module docstring's E61
    ADDITIONS note); both default to values that reproduce E60's own output
    byte-for-byte when omitted."""
    if form not in FORMS:
        _andon("form must be one of %s, got %r" % (FORMS, form))
    if garment_join not in ("and", "over"):
        _andon("garment_join must be 'and' or 'over', got %r" % (garment_join,))
    if garment_join != "and" and form != "grouped":
        _andon("garment_join=%r only applies to form='grouped' (got form=%r) "
               "- flat has no head-pair to redirect and consolidated's "
               "joiner is a different construction entirely"
               % (garment_join, form))
    fv = face_visible(view)
    garments, features = _garment_feature_split(doc, fv)
    framing = clause(doc, "frame_subject") or ""
    style_phrases = _style_phrases(doc, fv)
    pose, bg, neg = _staging_groups(doc)
    joint_phrases = [_joint_phrase(doc, jid) for jid in joints]

    if form == "flat":
        # profiles/a1.json's own convention: framing, garments, features,
        # style, backdrop, negatives, THEN pose last (E59 Stage 0 literally
        # appended the pose clauses to an already-written flat string).
        # joint_phrases appended last of all (E61) - empty by default, so
        # this is a no-op unless a caller opts in.
        parts = ([framing] + garments + features + style_phrases + bg + neg
                 + pose + joint_phrases)
        parts = [p for p in parts if p]
        result = _cap(", ".join(parts) + ".")
        _refuse_if_and_joins_a_dependent_pair(doc, result)
        return result

    # grouped / consolidated: framing -> staging -> style -> identity -> joints
    sec_framing = (_cap(framing) + ".") if framing else ""

    staging_bits = []
    if pose:
        staging_bits.append(_cap(_join_and_list(pose)) + ".")
    if bg:
        staging_bits.append(_cap(_join_and_list(bg)) + ".")
    if neg:
        staging_bits.append(_cap(_join_and_list(neg)) + ".")
    sec_staging = " ".join(staging_bits)

    sec_style = (_cap(_join_and_list(style_phrases)) + ".") if style_phrases else ""

    if form == "consolidated":
        garment_text = _join_consolidated_garments(garments)
    else:
        head_sep = " over " if garment_join == "over" else " and "
        garment_text = _join_grouped_garments(garments, head_sep=head_sep)
    feature_text = _join_and_list(features)
    if garment_text and feature_text:
        sec_identity = _cap(garment_text) + "; " + feature_text + "."
    else:
        sec_identity = _cap(garment_text or feature_text) + "."

    sec_joints = (_cap(_join_and_list(joint_phrases)) + ".") if joint_phrases else ""

    sections = [s for s in (sec_framing, sec_staging, sec_style, sec_identity, sec_joints)
                if s]
    result = " ".join(sections)
    _refuse_if_and_joins_a_dependent_pair(doc, result)
    return result


def check_composed(doc, prompt, scope="subject"):
    """Thin wrapper - never re-implements canon_gate's own check."""
    return canon_gate.check_prompt(doc, prompt, scope=scope)


# ---------------------------------------------------------------------------
# anchor (Stage 1) - three-way diff between the composer's licensed phrase
# set and the recipe's raw positive text. NOT a byte match; reuses canon_
# gate's own presence/residue instruments rather than a bespoke text diff,
# so the diff is exactly what the gate itself would see.
# ---------------------------------------------------------------------------

def anchor_diff(doc, recipe_text):
    phrases = sorted(set(p for p in canon_gate.licensed_phrases(doc) if p))
    in_both, canon_only = [], []
    for p in phrases:
        if canon_gate._present(p, recipe_text):
            in_both.append(p)
        else:
            canon_only.append(p)
    residue = canon_gate.unlicensed_residue(doc, recipe_text)
    return {"in_both": in_both, "canon_only": canon_only,
            "recipe_only_residue": residue}


# ---------------------------------------------------------------------------
# selftest - in-tool, ANDON-raising, mirrors canon_gate.py's own convention.
# This is where this file's real test coverage lives (see the file's own
# commit for why: T34 pins the collected-pytest-item count against 15 doc
# surfaces across 8 languages, and a Sonnet executor session cannot
# regenerate 7 of them - the studio's translation rule reserves that to
# advisor sessions/the user. Following E59's precedent exactly: substantive
# coverage lives here, in-tool, and the pytest-visible seam is one line
# added to an ALREADY-collected test rather than a new item.)
# ---------------------------------------------------------------------------

def selftest():
    doc = canon_gate.load_canon(os.path.join(_REPO, "canon", "a1.surfaces.json"))

    # E62: A1's canon now declares vest_torso/vest_skirt depends_on: ["N2"]
    # (the vest layers over the shirt). garment_join="over" is passed
    # EXPLICITLY everywhere below that this function needs a passing
    # grouped compose, because the bare default (garment_join="and") now
    # ANDONs on this doc by design - fence 1's own can-fail leg (a), proven
    # with real data further down, is exactly that refusal. Every leg below
    # this point that is not itself testing garment_join uses "over" so its
    # own (unrelated) assertions stay isolated from the fence-1 concern.
    p_front = compose(doc, view="front", form="grouped", garment_join="over")
    chk = check_composed(doc, p_front)
    if not chk["ok"]:
        _andon("front-view grouped compose failed the gate: missing=%s "
               "forbidden=%s unlicensed=%s"
               % (chk["missing"], chk["forbidden"], chk["unlicensed"]))

    p_flat = compose(doc, view="front", form="flat")
    chk_flat = check_composed(doc, p_flat)
    if not chk_flat["ok"]:
        _andon("front-view flat compose failed the gate: missing=%s "
               "forbidden=%s unlicensed=%s"
               % (chk_flat["missing"], chk_flat["forbidden"], chk_flat["unlicensed"]))

    p_cons = compose(doc, view="front", form="consolidated")
    chk_cons = check_composed(doc, p_cons)
    if not chk_cons["ok"]:
        _andon("front-view consolidated compose failed the gate: missing=%s "
               "forbidden=%s unlicensed=%s"
               % (chk_cons["missing"], chk_cons["forbidden"], chk_cons["unlicensed"]))

    # CAN-FAIL LEG (charter Stage 0): a rear-view compose that still
    # contained a face phrase must fail. Checked directly against the
    # composed text - A1 declares no view scopes, so canon_gate cannot be
    # asked to gate a specific view (see module docstring).
    p_rear = compose(doc, view="rear", form="grouped", garment_join="over")
    lower_rear = p_rear.lower()
    face_phrases = ("curious brown eyes", "a slight smile",
                     "crisp readable facial features")
    for ph in face_phrases:
        if ph in lower_rear:
            _andon("rear-view compose still contains the face phrase %r - "
                   "the per-view drop is not working" % ph)
    # the other half of the pair: the front view MUST carry them, or a
    # composer that dropped face phrases everywhere would pass the leg
    # above for the wrong reason
    lower_front = p_front.lower()
    for ph in face_phrases:
        if ph not in lower_front:
            _andon("front-view compose is missing the face phrase %r" % ph)

    # dropping face content must not silently drop anything else
    for entry in named_occupants(doc):
        if is_face_bound(entry):
            continue
        if entry["phrase"].lower() not in lower_rear:
            _andon("rear-view compose dropped a non-face phrase: %r"
                   % entry["phrase"])

    # anchor sanity - non-degenerate, not a re-assertion of Stage 1's own
    # numbers (those are reported, never pinned - charter: "not a byte
    # match ... must not be tuned toward one")
    recipe_path = os.path.join(_REPO, "canon", "A1-RECIPE.json")
    recipe = json.load(open(recipe_path, encoding="utf-8"))
    diff = anchor_diff(doc, recipe["positive_text"])
    if not diff["in_both"]:
        _andon("anchor diff found nothing in common with the recipe - the "
               "presence check is broken")
    if not diff["recipe_only_residue"]:
        _andon("anchor diff found zero recipe-only residue - the raw "
               "recipe text is known to carry unlicensed staging prose "
               "(canon/A1-IDENTITY.md), so an empty residue means this "
               "function is not really stripping licensed phrases")

    # CAN-FAIL LEG (E61): garment_join="over" changes exactly the vest-shirt
    # connector and the result still passes the gate. Proven by reverting -
    # if compose() ignored the parameter (E60's hardcoded " and "), " over "
    # would never appear here and this leg would ANDON.
    p_over = compose(doc, view="front", form="grouped", garment_join="over")
    if " over " not in p_over:
        _andon("garment_join='over' did not produce ' over ' in the "
               "composed text: %r" % p_over)
    chk_over = check_composed(doc, p_over)
    if not chk_over["ok"]:
        _andon("garment_join='over' compose failed the gate: missing=%s "
               "forbidden=%s unlicensed=%s"
               % (chk_over["missing"], chk_over["forbidden"], chk_over["unlicensed"]))
    # an inapplicable combination refuses rather than silently ignoring the knob
    try:
        compose(doc, view="front", form="flat", garment_join="over")
    except Andon:
        pass
    else:
        _andon("garment_join='over' with form='flat' did not refuse")

    # CAN-FAIL LEG (E61): joints=(...) emits the named joint phrase and the
    # result still passes the gate; the DEFAULT (no joints requested) must
    # NOT emit it - licensing is not requiring, proven in both directions.
    p_joint = compose(doc, view="front", form="grouped", joints=("vest_shirt",),
                      garment_join="over")
    if "plum vest edge against cream shirt" not in p_joint.lower():
        _andon("joints=('vest_shirt',) did not emit the joint phrase: %r" % p_joint)
    chk_joint = check_composed(doc, p_joint)
    if not chk_joint["ok"]:
        _andon("joints=('vest_shirt',) compose failed the gate: missing=%s "
               "forbidden=%s unlicensed=%s"
               % (chk_joint["missing"], chk_joint["forbidden"], chk_joint["unlicensed"]))
    if "plum vest edge against cream shirt" in p_front.lower():
        _andon("default compose (joints=()) unexpectedly emitted a joint "
               "phrase - licensing must not be requiring")
    try:
        compose(doc, view="front", form="grouped", joints=("no-such-joint",))
    except Andon:
        pass
    else:
        _andon("an unknown joint id did not refuse")

    # CAN-FAIL LEG (E61): with_occupant_phrase actually changes composed
    # text, the modified doc's OWN gate accepts its own (older) text, and -
    # critically - that SAME text is REJECTED by the LIVE canon, proving the
    # live sleeveless requirement is real and would catch a regressed arm
    # rather than merely being internally consistent with itself.
    old_n1 = "a plum long-vest with fine gold embroidery"
    doc_pre = with_occupant_phrase(doc, "N1", old_n1)
    # with_occupant_phrase deep-copies the WHOLE doc and overrides only the
    # occupant.phrase field, so doc_pre still carries vest_torso/vest_skirt's
    # depends_on: ["N2"] (a sibling of "occupant", untouched by the
    # override) - garment_join="over" is needed here for the same E62
    # reason as p_front/p_rear/p_joint above; this leg's own concern is the
    # "sleeveless" wording, not the connector.
    p_pre = compose(doc_pre, view="front", form="grouped", garment_join="over")
    if "sleeveless" in p_pre.lower():
        _andon("with_occupant_phrase override did not take effect - "
               "'sleeveless' is still present: %r" % p_pre)
    chk_pre_own = check_composed(doc_pre, p_pre)
    if not chk_pre_own["ok"]:
        _andon("pre-repair compose failed its OWN (modified-doc) gate: %s" % chk_pre_own)
    chk_pre_vs_live = check_composed(doc, p_pre)
    if chk_pre_vs_live["ok"]:
        _andon("pre-repair text unexpectedly PASSED the live canon's gate - "
               "the sleeveless requirement is not being enforced: %s" % chk_pre_vs_live)
    try:
        with_occupant_phrase(doc, "N_NO_SUCH_OCCUPANT", "x")
    except Andon:
        pass
    else:
        _andon("with_occupant_phrase silently accepted an unknown occupant id")

    # CAN-FAIL LEG (E62 fence 1a, REQUIRED): the OLD default
    # (garment_join="and") on the LIVE A1 doc - which now declares
    # vest_torso/vest_skirt depends_on: ["N2"] - must refuse. Real data, not
    # a synthetic fixture: this is the concrete case the charter names.
    try:
        compose(doc, view="front", form="grouped")  # garment_join defaults to "and"
        _andon("compose() with the default garment_join='and' did NOT "
               "refuse A1's depends_on-linked pair (N1 vest / N2 shirt) - "
               "fence 1a is not enforced")
    except Andon as e:
        if "depends_on pair coordinated with" not in str(e):
            _andon("default and-join refused for the wrong reason: %s" % e)

    # CAN-FAIL LEG (E62 fence 1b, REQUIRED): a FLAT list naming both
    # garments as separate noun phrases with NO preposition must still
    # pass - this is Arm L, which E61 measured held 3/3. p_flat/chk_flat
    # above already prove the gate accepts it; asserted explicitly here so
    # this leg exists so nobody "helpfully" requires the word "over" and
    # refuses Arm L (the charter's own words).
    vest_ph = shirt_ph = None
    for o in named_occupants(doc):
        if o["n_id"] == "N1":
            vest_ph = o["phrase"].lower()
        if o["n_id"] == "N2":
            shirt_ph = o["phrase"].lower()
    if not vest_ph or not shirt_ph:
        _andon("could not resolve N1/N2 phrases to check the flat-form leg")
    lower_flat = p_flat.lower()
    if (vest_ph + " and " + shirt_ph) in lower_flat or (shirt_ph + " and " + vest_ph) in lower_flat:
        _andon("flat form unexpectedly coordinates the depends_on pair with "
               "'and' - fence 1b (Arm L must pass unjoined) is violated")
    if vest_ph not in lower_flat or shirt_ph not in lower_flat:
        _andon("flat form dropped a depends_on occupant phrase entirely - "
               "cannot prove the unjoined leg without both phrases present")

    # CAN-FAIL LEG (E62 fence 1c, REQUIRED): 'over' composes cleanly for the
    # SAME depends_on pair. p_over/chk_over above already prove the gate
    # accepts it; this additionally proves 'over' sits directly between the
    # two dependent phrases specifically, not merely present somewhere in
    # the prompt.
    lower_over = p_over.lower()
    if (vest_ph + " over " + shirt_ph) not in lower_over:
        _andon("garment_join='over' did not place 'over' directly between "
               "the depends_on pair's own two phrases: %r" % p_over)

    return {
        "front_ok": True, "flat_ok": True, "consolidated_ok": True,
        "rear_drops_face": True,
        "anchor_in_both": len(diff["in_both"]),
        "anchor_canon_only": len(diff["canon_only"]),
        "garment_join_over_ok": True,
        "joint_emit_ok": True,
        "occupant_override_ok": True,
        "depends_on_and_refused": True,
        "depends_on_flat_ok": True,
        "depends_on_over_ok": True,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(
        description="Canon -> prompt composer (E60 Stage 0/1).")
    p.add_argument("--selftest", action="store_true")
    sub = p.add_subparsers(dest="cmd")

    def add_source(sp):
        sp.add_argument("--canon", default=None)
        sp.add_argument("--subject", default=None)

    c = sub.add_parser("compose")
    add_source(c)
    c.add_argument("--view", default="front")
    c.add_argument("--form", default="grouped", choices=FORMS)

    a = sub.add_parser("anchor")
    add_source(a)
    a.add_argument("--recipe", required=True)
    a.add_argument("--view", default="front")
    return p


def _load(args):
    if getattr(args, "canon", None):
        path = canon_gate.resolve_canon(args.canon)
    elif getattr(args, "subject", None):
        path = canon_gate.resolve_subject(args.subject)
    else:
        _andon("need --canon or --subject")
    return canon_gate.load_canon(path), path


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.selftest:
            r = selftest()
            sys.stdout.write(
                "selftest PASS  front/flat/consolidated gated  "
                "rear drops face  anchor in_both=%d canon_only=%d  "
                "garment-join-over held  joint-emit held  occupant-override held  "
                "depends-on and-refused  depends-on flat-held  depends-on over-held\n"
                % (r["anchor_in_both"], r["anchor_canon_only"]))
            return 0
        if not args.cmd:
            _andon("need a subcommand or --selftest")
        doc, _path = _load(args)
        if args.cmd == "compose":
            prompt = compose(doc, view=args.view, form=args.form)
            chk = check_composed(doc, prompt)
            sys.stdout.write(prompt + "\n")
            sys.stdout.write(
                "[gate] ok=%s missing=%d forbidden=%d unlicensed=%d\n"
                % (chk["ok"], len(chk["missing"]), len(chk["forbidden"]),
                   len(chk["unlicensed"])))
            if not chk["ok"]:
                sys.stdout.write(
                    "[gate] missing=%s forbidden=%s unlicensed=%s\n"
                    % (chk["missing"], chk["forbidden"], chk["unlicensed"]))
            return 0 if chk["ok"] else 2
        if args.cmd == "anchor":
            prompt = compose(doc, view=args.view, form="grouped")
            chk = check_composed(doc, prompt)
            recipe = json.load(open(args.recipe, encoding="utf-8"))
            diff = anchor_diff(doc, recipe["positive_text"])
            sys.stdout.write("composed: %s\n" % prompt)
            sys.stdout.write(
                "[gate] ok=%s missing=%s forbidden=%s unlicensed=%s\n"
                % (chk["ok"], chk["missing"], chk["forbidden"], chk["unlicensed"]))
            sys.stdout.write("in_both (%d): %s\n" % (len(diff["in_both"]), diff["in_both"]))
            sys.stdout.write(
                "canon_only / recipe-missing (%d): %s\n"
                % (len(diff["canon_only"]), diff["canon_only"]))
            sys.stdout.write("recipe_only / canon debt: %s\n" % diff["recipe_only_residue"])
            if not chk["ok"]:
                _andon(
                    "Gate 1: composed front-view prompt failed canon_gate - "
                    "the composer is not shippable: missing=%s forbidden=%s "
                    "unlicensed=%s" % (chk["missing"], chk["forbidden"], chk["unlicensed"]))
            return 0
        _andon("unknown command %s" % args.cmd)
    except Andon as e:
        sys.stderr.write(str(e) + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
