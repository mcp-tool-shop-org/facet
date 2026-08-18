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

CLI:
  python tools/canon_compose.py --selftest
  python tools/canon_compose.py compose --canon canon/a1.surfaces.json \
      --view front --form grouped
  python tools/canon_compose.py anchor --canon canon/a1.surfaces.json \
      --recipe canon/A1-RECIPE.json --view front
"""
from __future__ import annotations

import argparse
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


def _join_grouped_garments(phrases):
    """Arm P: the first two garments and-bound (the worn-together pair the
    recipe expressed with the illegal 'over'), the remainder a comma list
    with a final 'and'. Degrades to a plain and-list below 4 items, where
    the head-plus-rest construction would just repeat 'and' twice."""
    phrases = [p for p in phrases if p]
    n = len(phrases)
    if n <= 3:
        return _join_and_list(phrases)
    head = phrases[0] + " and " + phrases[1]
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


def compose(doc, view="front", form="grouped"):
    """canon -> prompt. Pure function: does not check the gate (see
    check_composed) and does not write anything."""
    if form not in FORMS:
        _andon("form must be one of %s, got %r" % (FORMS, form))
    fv = face_visible(view)
    garments, features = _garment_feature_split(doc, fv)
    framing = clause(doc, "frame_subject") or ""
    style_phrases = _style_phrases(doc, fv)
    pose, bg, neg = _staging_groups(doc)

    if form == "flat":
        # profiles/a1.json's own convention: framing, garments, features,
        # style, backdrop, negatives, THEN pose last (E59 Stage 0 literally
        # appended the pose clauses to an already-written flat string).
        parts = [framing] + garments + features + style_phrases + bg + neg + pose
        parts = [p for p in parts if p]
        return _cap(", ".join(parts) + ".")

    # grouped / consolidated: framing -> staging -> style -> identity
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

    garment_joiner = (_join_consolidated_garments if form == "consolidated"
                       else _join_grouped_garments)
    garment_text = garment_joiner(garments)
    feature_text = _join_and_list(features)
    if garment_text and feature_text:
        sec_identity = _cap(garment_text) + "; " + feature_text + "."
    else:
        sec_identity = _cap(garment_text or feature_text) + "."

    sections = [s for s in (sec_framing, sec_staging, sec_style, sec_identity) if s]
    return " ".join(sections)


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

    p_front = compose(doc, view="front", form="grouped")
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
    p_rear = compose(doc, view="rear", form="grouped")
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

    return {
        "front_ok": True, "flat_ok": True, "consolidated_ok": True,
        "rear_drops_face": True,
        "anchor_in_both": len(diff["in_both"]),
        "anchor_canon_only": len(diff["canon_only"]),
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
                "rear drops face  anchor in_both=%d canon_only=%d\n"
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
