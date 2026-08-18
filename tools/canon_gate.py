# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Canon database gates. Surface is the row. A hole is a null occupant.

WHY THIS EXISTS. Consult #13 / build #13. W3-IDENTITY.md names seventeen
elements. The profile default that still sits on restylize_views /
texpass_brush named six. Nothing refused the generation. Four arcs then
repaired composition downstream of paint that was wrong at the source
(E50 ordinary painted texels; E51 fills that did not move the eye;
#12 no geometry to snap to; #11 plates that agree and are wrong).

THE THESIS, ATTACKED.

  ELEMENT is the wrong primary key. N17 was not on the N1-N16 list;
  reading that list could not reveal the grip. A SURFACE list with a
  nullable occupant makes the hole a row. Coverage is then
  (surfaces that have an occupant) / (surfaces that must), not a
  fight about pixels we cannot segment (#12: one PBR material,
  13,715 islands, palette blind to gold-against-leather).

  Where surfaces come from: a human walks the reference (or the clay,
  for forward-authored subjects) once. Not geometry, not palette
  bands, not atlas islands. The ratification of that list is the
  gate, not a formality.

  Joints are first-class. Adjacency is the pair of surface ids;
  the joint row is the cut (armhole, boot-top, grip/guard). The
  joint is not a fifth garment. Sleeveless is expressed by occupying
  upper_arm with kind=bare and forbidding the word sleeve (except
  inside sleeveless).

  Prompt coverage is case-insensitive phrase substring with a
  negation window and a sleeve/sleeveless word rule. It cannot
  catch a paraphrase ("bald warrior" for "a bald head") or a
  synonym. Semantic matching would put a model inside a gate.
  Exact-with-negation is the honest check: it would have refused
  the six-element default; it will not refuse a clever rewrite.

THE ROUTER (build #18 / #20). canon_gate is the component every
spend asks: what does the canon say, for THIS subject, at THIS
scope, and is this prompt covered? It refuses when the answer is
not covered, and it refuses when there is no answer at all.

FAIL-CLOSED (#20). An optional `if args.canon` is not a gate. A
missing flag is the same defect as a shell chain that can drop the
check. require_canon is the spend helper: silence is dead. The
escape for a subject that genuinely has no surfaces is census-
backed `--no-canon --subject NAME`. `--no-canon` on a subject that
HAS surfaces is a refuse (the checkbox trap). A run that proceeds
ungated prints `[canon] UNGATED:` and names the identity-only
subject.

THE BOUNDARY. The gate stands in front of every file that AUTHORS
a spend (restylize_views, texpass_brush, brush_cloud_step,
e12_pair_cloud_step). The transport (MCP submit, texpass_loop.ps1)
does not re-check. Submission-time theatre is declined: if the
graph was refused, there is nothing licensed to post.

  Resolve     subject id -> file over SEARCH_PATH + CENSUS_ROWS.
              GALLEON/DRAGON/LOGO/E10-LAYER refuse by name
              (identity exists, surfaces missing).
  Cover both  canon ⊆ prompt (exists) and prompt ⊆ canon (missing).
              Reverse is armed only when legal_clauses is declared.
              Unlicensed residue refuses. No warn verdict.
  Scope       subject | view:ID | stroke:ID. A scope names surface
              ids. No declaration is no answer. Boxes stay unbound
              (s3_sheet_regions.json is PROPOSALS; verify --regions
              is still free text). The human declares the id list
              once per subject per view. Geometry and colour cannot
              name a surface here (one PBR, 13,715 islands).
  Version     schema 1 still loads. schema > SCHEMA_MAX is a stale
              consumer. Schema 2 adds legal_clauses and scopes.
  Binding     tools/canon_bind.py. A surface is a face set. Empty
              faces are 0.00% of the figure. Names stay on the
              surfaces file.

WHAT THIS DOES NOT COVER.

  Paraphrase and synonym matching. Semantic matching puts a model
  inside a gate. Kind templates, occupant filling, IDENTITY ->
  surfaces emission, spatial box binding, and the element-count
  readout are tools/canon_worksheet.py (t93). Per-view --prompts
  stems are not auto-checked until a view scope exists. Deriving
  a prompt from the canon is still refused. s3_sheet_regions
  names are not surface ids. e37_fire_repaints is a REPLAY of a
  recorded prompt: refuse_uncovered would halt a faithful replay
  the moment the canon moved under it (t87: ARMB 16/17 -> 14/19).
  report_replay_drift reports and does not refuse. ig2mv is a
  different backbone with no subject binding; it is not this
  gate. The MCP transport is not a second gate.

  python tools/canon_gate.py resolve --subject GALLEON
  python tools/canon_gate.py check --subject W3 --prompt "..." --scope subject

  Two files, one pin, neither generated from the other. IDENTITY.md
  keeps the arguments a JSON row cannot hold (four reasons the grip
  is leather; one argument recorded as unused). The JSON is what
  tools load. T87 pins: every IDENTITY NAMED phrase is an occupant
  or a blocked_addition; every JSON occupant/blocked phrase with an
  N-/L- id appears in the NAMED table. Hole rows exist only in JSON.

  sdlab/projects/facet-assets is a finished-image rubric
  (constitution.json) with empty terminology stubs. It has no
  per-element identity. No bridge. Wrong layer.

  Verification is never hand-set. `verify` writes a sidecar from a
  measurement (CIE76 Lab dE, same transform as e08_deltaE.py /
  palette_gate.py). The surfaces file does not carry a grade.

CALIBRATION CLAIM (run --selftest; T87 pins the same numbers).
  profiles/character.json restylize prompt contains exactly 5 of the
  W3 NAMED phrases (article-stripped). Was 6 until the kilt ruling
  renamed N8/N9; the live default still says skirt. The ARMB
  workflow (stroke_1_y+090_e+00_workflow.json) was 16 of 17 when
  recorded (missing N17 only). The canon then moved under the
  frozen string: NAMED 17->19 (N18/N19) then the kilt rename, so
  the same bytes now hit 14 of 19 (miss N8, N9, N17, N18, N19).
  t87 artifacts pins the sha256 and the 14. The numerators moved
  because the canon was corrected, not because the recording did.
  The brief's "six" was the profile default, not that file.

  W3_NAMED is 19 (the NAMED table). Completing the canon widened
  the gap without the profile default moving a character, which
  is why the ratio is computed and never stored.

  python tools/canon_gate.py --selftest

YES/NO INTERVALS.

  coverage          named / prompt_surfaces. Occupancy, not ratification.
                    ratified / prompt_surfaces is the spend number.
                    A drafted row (ratify: true) stays in named and
                    sits in unratified_ids. Holes sit in the denominator.
  prompt check      ratified occupant/blocked phrases must occur.
                    Unratified phrases are named, not required.
                    Forbidden words still fire on every row.
                    Negation window: 24 chars.
                    Schema 2 reverse: residue after licensed spans
                    (occupant phrases + blocked + legal_clauses)
                    refuse. Same two verdicts as #17: refuse or
                    report. Unlicensed is a refuse.
                    A legal_clause marked required:true (E59 Stage
                    0) must also occur, at every scope — folded
                    into the same missing list, same refusal shape
                    as a missing ratified occupant phrase. Unmarked
                    clauses (the default) stay licensed-but-optional,
                    unchanged.
  occupancy         one prompt occupant per surface_id. A blocked
                    addition naming a surface that already has a
                    prompt occupant is the predicted-drop class,
                    recorded, not installed.
  verify            sidecar only. median Lab dE; state landed if
                    median <= 2.3, missed if median > 10, else
                    uncertain. Never written into the surfaces file.

  python tools/canon_gate.py coverage --canon canon/w3.surfaces.json
  python tools/canon_gate.py check --canon canon/w3.surfaces.json --prompt "..."
  python tools/canon_gate.py pin-identity --canon canon/w3.surfaces.json
  python tools/canon_gate.py verify --canon C --twin T --reference R --regions J
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile

import numpy as np
from PIL import Image

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_TOOLS)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

TOOL_VERSION = "1.0.0"
SCHEMA_MIN = 1
SCHEMA_MAX = 2
# SCHEMA is the consumer's understood ceiling. A file above it is a stale
# consumer, not a bad file. Schema-1 files still load.
SCHEMA = SCHEMA_MAX
NEGATION = re.compile(r"\b(no|not|without|lacking)\b", re.I)
SLEEVE = re.compile(r"\bsleeve(?!less)\b", re.I)
NAMED_ROW = re.compile(
    r"^\|\s*([A-Z]\d+)\s*\|\s*(.*?)\s*\|", re.M)
ARTICLE = re.compile(r"^a\s+", re.I)
# Residue stopwords only. Not a style allowlist and not framing. "holding"
# and "burly" stay off this list on purpose: they are declared on the subject
# as legal_clauses or they are unlicensed.
STOP = re.compile(
    r"\b(a|an|the|with|and|or|of|on|in|at|to|for|from|by|as|"
    r"his|her|its|their|this|that|each)\b", re.I)
DE_LANDED = 2.3
DE_MISSED = 10.0
NEG_WINDOW = 24
# A negator binds inside its own clause, so the look-back stops at the
# nearest clause boundary as well as at NEG_WINDOW chars.
CLAUSE_END = re.compile(r"[,.;]")
# "staging" joined 2026-08-17 (E57 fold): shot clauses - backdrop, no weapons,
# no held objects, clear silhouette - are neither the paint nor the subject.
# A1's ratified canon carries four; census FIRED on the ratified file first.
CLAUSE_CLASSES = ("style", "framing", "staging")
SEARCH_PATH = (os.path.join(_REPO, "canon"),)

# Article-stripped NAMED phrases in the profile default (measured).
#
# W3_NAMED is 19 (the NAMED table). The two live numerators DID move, and
# that is the finding: the profile default went 6 -> 5 when the garment
# was ruled a kilt (the prompt still says skirt); the frozen ARMB string
# went 16 -> 14 for the same rename plus the N18/N19 draft sitting under
# a recording that never named them. Completing the canon WIDENED the
# gap. Numerators stay pinned separately from the total; the ratio is
# never stored, only computed.
#
# 6 -> 5 on 2026-08-17: the Director ruled the garment is a KILT, not a skirt.
# The live default still says skirt, so renaming the canon cost a hit without
# anyone touching the prompt - 6/17 -> 6/19 -> 5/19. Every canon repair so far
# has WIDENED this gap, which is what a specimen is supposed to do.
PROFILE_DEFAULT_HITS = 5
ARMB_HITS = 14
W3_NAMED = 19


class Andon(ValueError):
    pass


def _andon(msg):
    raise Andon("ANDON: " + msg)


def to_lab(rgb):
    """sRGB -> Lab. Verbatim e08_deltaE / palette_gate. T87 pins identity."""
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16,
                     500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


def load_canon(path):
    if not os.path.isfile(path):
        _andon("no canon %s" % path)
    doc = json.load(open(path, encoding="utf-8"))
    if not isinstance(doc, dict):
        _andon("canon must be an object")
    try:
        ver = int(doc.get("schema", -1))
    except (TypeError, ValueError):
        ver = -1
    if ver < SCHEMA_MIN:
        _andon("canon schema %r is not >= %d" % (doc.get("schema"), SCHEMA_MIN))
    if ver > SCHEMA_MAX:
        _andon("stale consumer: canon schema %d > %d" % (ver, SCHEMA_MAX))
    if "surfaces" not in doc or not isinstance(doc["surfaces"], list):
        _andon("canon needs a surfaces list")
    ids = []
    for i, s in enumerate(doc["surfaces"]):
        if not isinstance(s, dict) or "id" not in s:
            _andon("surface %d needs id" % i)
        if s["id"] in ids:
            _andon("duplicate surface id %s" % s["id"])
        ids.append(s["id"])
        occ = s.get("occupant")
        if occ is not None and not isinstance(occ, dict):
            _andon("surface %s occupant must be object or null" % s["id"])
    for j in doc.get("joints") or []:
        if j.get("a") not in ids or j.get("b") not in ids:
            _andon("joint %s names unknown surfaces" % j.get("id"))
    _validate_router_fields(doc, ids)
    return doc


def _validate_router_fields(doc, ids):
    """Schema 2 fields. Legal on schema 1 if present; required of nothing."""
    if "legal_clauses" in doc:
        if not isinstance(doc["legal_clauses"], list):
            _andon("legal_clauses must be a list")
        cids = []
        for i, c in enumerate(doc["legal_clauses"]):
            if not isinstance(c, dict) or "id" not in c or "phrase" not in c:
                _andon("legal_clause %d needs id and phrase" % i)
            if c["id"] in cids:
                _andon("duplicate legal_clause id %s" % c["id"])
            cids.append(c["id"])
            cls = c.get("class", "style")
            if cls not in CLAUSE_CLASSES:
                _andon("legal_clause %s class %r is not one of %s"
                       % (c["id"], cls, "/".join(CLAUSE_CLASSES)))
            if "required" in c and not isinstance(c["required"], bool):
                _andon("legal_clause %s required must be a bool, got %r"
                       % (c["id"], c["required"]))
    if "scopes" not in doc:
        return
    if not isinstance(doc["scopes"], dict):
        _andon("scopes must be an object")
    for bucket_name in ("views", "strokes"):
        bucket = doc["scopes"].get(bucket_name)
        if bucket is None:
            continue
        if not isinstance(bucket, dict):
            _andon("scopes.%s must be an object" % bucket_name)
        for name, rec in bucket.items():
            if not isinstance(rec, dict):
                _andon("scopes.%s.%s must be an object" % (bucket_name, name))
            surfs = rec.get("surfaces")
            if surfs is None:
                continue
            if not isinstance(surfs, list):
                _andon("scopes.%s.%s.surfaces must be a list"
                       % (bucket_name, name))
            for sid in surfs:
                if sid not in ids:
                    _andon("scopes.%s.%s names unknown surface %s"
                           % (bucket_name, name, sid))


def prompt_surfaces(doc):
    """Surfaces that belong in the coverage denominator."""
    out = []
    for s in doc["surfaces"]:
        occ = s.get("occupant")
        if occ is None:
            out.append(s)
            continue
        prov = occ.get("provenance")
        if prov == "prompt":
            out.append(s)
    return out


def is_named(s):
    occ = s.get("occupant")
    if occ is None:
        return False
    if occ.get("phrase"):
        return True
    if occ.get("kind") == "bare":
        return True
    return False


def is_unratified(s):
    occ = s.get("occupant") or {}
    return occ.get("ratify") is True


def coverage(doc):
    """Occupancy is not ratification. Both numbers are returned.

    `coverage` stays named/prompt_surfaces so a drafted row is still a
    filled hole. `ratified` / `ratified_coverage` are what a spend may
    treat as the Director's canon. A 1.0000 occupancy with unratified
    rows is not done.
    """
    ps = prompt_surfaces(doc)
    if not ps:
        _andon("no prompt-relevant surfaces")
    named = [s for s in ps if is_named(s)]
    holes = [s for s in ps if s.get("occupant") is None]
    unrat = [s for s in ps if is_unratified(s)]
    ratified = [s for s in named if not is_unratified(s)]
    n_ps = len(ps)
    return {
        "subject": doc.get("subject"),
        "prompt_surfaces": n_ps,
        "named": len(named),
        "holes": len(holes),
        "hole_ids": [s["id"] for s in holes],
        "coverage": float(len(named)) / float(n_ps),
        "unratified": len(unrat),
        "unratified_ids": [s["id"] for s in unrat],
        "ratified": len(ratified),
        "ratified_coverage": float(len(ratified)) / float(n_ps),
        "denominator": "prompt-relevant surfaces (prompt provenance or null occupant); mesh/style excluded",
    }


def _neg_window(hay, i):
    """The look-back a negator may bind across: NEG_WINDOW chars, cut at the
    nearest clause boundary.

    THE CUT IS THE FIX (E60 Stage 1, reproduced). A flat character window
    lets an adjacent list item's own negator leak forward. In A1-RECIPE.json's
    positive_text the 24 chars before "no held objects" are
    "l features, no weapons, " - the `no` that fires belongs to the PRECEDING
    item - so two of A1's three staging clauses read absent while textually
    present and unnegated.

    DECLARED BOUNDARY. This trades one error for its opposite: a negator that
    distributes over a list - "without a sword, a shield" - now reads the
    second item as present. That form was never reliably handled, because the
    flat window only reached it when the intervening items fit inside 24
    characters; it was a property of item lengths, not a design. The direction
    kept is the one a gate cares about: the flat window's failure is a false
    REFUSAL of a prompt that carries its required phrase, and this one's is a
    false accept of a form the corpus does not contain.
    """
    w = hay[max(0, i - NEG_WINDOW):i]
    last = None
    for m in CLAUSE_END.finditer(w):
        last = m
    return w if last is None else w[last.end():]


def _present(phrase, prompt):
    """True if phrase occurs and is not negated in the preceding window."""
    p = phrase.strip()
    if not p:
        return False
    hay = prompt.lower()
    needle = p.lower()
    start = 0
    while True:
        i = hay.find(needle, start)
        if i < 0:
            return False
        if not NEGATION.search(_neg_window(hay, i)):
            return True
        start = i + 1


def required_phrases(doc, scope_ids=None):
    out = []
    for s in doc["surfaces"]:
        if scope_ids is not None and s["id"] not in scope_ids:
            continue
        occ = s.get("occupant") or {}
        ph = occ.get("phrase")
        if ph and occ.get("provenance") == "prompt":
            out.append((s["id"], ph))
    for b in doc.get("blocked_additions") or []:
        if not b.get("phrase"):
            continue
        onto = b.get("onto")
        if scope_ids is not None and onto not in scope_ids:
            continue
        out.append(("blocked:%s" % b.get("id"), b["phrase"]))
    return out


def forbidden_hits(doc, prompt):
    hits = []
    for s in doc["surfaces"]:
        occ = s.get("occupant") or {}
        for w in occ.get("forbidden") or []:
            if w.lower() == "sleeve":
                if SLEEVE.search(prompt):
                    hits.append((s["id"], w))
            elif re.search(r"\b%s\b" % re.escape(w), prompt, re.I):
                hits.append((s["id"], w))
    return hits


def _unratified_ids(doc):
    return {s["id"] for s in doc["surfaces"] if is_unratified(s)}


def parse_scope(scope):
    """'subject' | 'view:ID' | 'stroke:ID' | ('view', id)."""
    if scope is None or scope == "subject":
        return ("subject", None)
    if isinstance(scope, tuple) and len(scope) == 2:
        kind, name = scope
        kind = str(kind).strip().lower()
        if kind in ("subject",):
            return ("subject", None)
        if kind in ("view", "views"):
            return ("view", None if name is None else str(name))
        if kind in ("stroke", "strokes"):
            return ("stroke", None if name is None else str(name))
        _andon("scope kind %r is not subject, view, or stroke" % (kind,))
    if isinstance(scope, str):
        raw = scope.strip()
        if raw == "subject":
            return ("subject", None)
        if ":" in raw:
            kind, name = raw.split(":", 1)
            return parse_scope((kind, name.strip()))
    _andon("scope %r is not subject, view:ID, or stroke:ID" % (scope,))


def scope_surface_ids(doc, scope="subject"):
    """Which surface ids the gate requires at this scope.

    subject -> None (all prompt surfaces). view/stroke -> the declared
    list. A missing declaration is no answer: refuse. Empty surfaces
    on a declared scope is no answer: refuse.
    """
    kind, name = parse_scope(scope)
    if kind == "subject":
        return None
    bucket_name = "views" if kind == "view" else "strokes"
    bucket = ((doc.get("scopes") or {}).get(bucket_name)) or {}
    if name not in bucket:
        _andon("no %s scope %s declared for %s"
               % (kind, name, doc.get("subject")))
    rec = bucket[name]
    ids = rec.get("surfaces")
    if not ids:
        _andon("scope %s:%s names no surfaces" % (kind, name))
    return set(ids)


def licensed_phrases(doc):
    """Spans the reverse check may remove from a prompt.

    Occupant phrases (any provenance), blocked additions, and declared
    legal_clauses. Not a model. Not a synonym table.
    """
    out = []
    for s in doc["surfaces"]:
        ph = (s.get("occupant") or {}).get("phrase")
        if ph and str(ph).strip():
            out.append(str(ph).strip())
    for b in doc.get("blocked_additions") or []:
        if b.get("phrase") and str(b["phrase"]).strip():
            out.append(str(b["phrase"]).strip())
    for c in doc.get("legal_clauses") or []:
        if c.get("phrase") and str(c["phrase"]).strip():
            out.append(str(c["phrase"]).strip())
    return out


def required_legal_clauses(doc):
    """legal_clauses marked `required: true`. E59 Stage 0.

    Until now every legal_clause was licensed-but-optional: `licensed_phrases()`
    lets it occur without tripping the reverse/unlicensed check, but nothing
    required it to occur, so a staging clause (e.g. A1's `stage_head_forward`,
    "head facing straight ahead") could silently drop out of a prompt and the
    gate would stay quiet. That made a ratified staging clause decorative.

    Checked at EVERY scope, not filtered by scope_ids. A legal_clause names no
    surface id, so the surface-id narrowing that view/stroke scopes use has no
    honest way to exempt one — and the properties these clauses express
    ("the head stays forward") are meant to hold at every view, not just at
    subject scope. This is the strictest reading and the fail-closed one.

    Unmarked clauses (no `required` key, or `required: false`) are untouched:
    they keep exactly today's behaviour, licensed but optional. This list only
    grows when a clause's own author opts it in — it does not retroactively
    make every staging clause on every subject mandatory (W3 carries five
    unmarked legal_clauses; none of them enter this list).
    """
    out = []
    for c in doc.get("legal_clauses") or []:
        if c.get("required") is True:
            out.append(("clause:%s" % c["id"], c["phrase"]))
    return out


def unlicensed_residue(doc, prompt):
    """prompt minus licensed spans. Empty list if reverse is not armed.

    Reverse is armed iff the file declares `legal_clauses` (schema 2).
    Schema 1 stays one-directional: it cannot name the style class, so
    it cannot honestly ask prompt ⊆ canon.
    """
    if "legal_clauses" not in doc:
        return []
    if prompt is None:
        _andon("need a prompt")
    work = prompt.lower()
    phrases = sorted({p.lower() for p in licensed_phrases(doc) if p},
                     key=len, reverse=True)
    for ph in phrases:
        work = work.replace(ph, " ")
    work = re.sub(r"[^a-z0-9]+", " ", work)
    work = STOP.sub(" ", work)
    work = re.sub(r"\s+", " ", work).strip()
    if not work:
        return []
    return [{"span": work}]


def check_prompt(doc, prompt, scope="subject"):
    """Ratified phrases are required. Unratified phrases are reported.

    A drafted row (`ratify: true`) is not the Director's canon. Requiring
    it spends his credits on a phrase he has not seen. Omitting it from
    the report would hide the draft. Forbidden words still fire on every
    row, including drafts: adding a gauntlet is a spend in the wrong
    direction.

    Reverse (schema 2): a residue after licensed spans are removed is
    unlicensed and refuses. Same two verdicts as #17 — refuse or report.
    Unlicensed is a refuse. There is no warn.

    A `required: true` legal_clause (E59 Stage 0) is folded into the same
    `missing` list, checked at every scope regardless of scope_ids — it
    refuses exactly the way a missing ratified occupant phrase does, through
    the same list and the same ANDON message shape. Clauses carry no
    ratification flag (nothing in this schema drafts a legal_clause), so
    there is no unratified-clause path to mirror `unrat_missing`.
    """
    if prompt is None:
        _andon("need a prompt")
    scope_ids = scope_surface_ids(doc, scope)
    unrat_ids = _unratified_ids(doc)
    missing = []
    unrat_missing = []
    req = 0
    for sid, ph in required_phrases(doc, scope_ids):
        raw_id = sid.split(":", 1)[-1] if sid.startswith("blocked:") else sid
        # blocked additions are author-time inventory, not drafts
        drafted = (raw_id in unrat_ids) and not sid.startswith("blocked:")
        if drafted:
            if not _present(ph, prompt):
                unrat_missing.append({"surface": sid, "phrase": ph})
            continue
        req += 1
        if not _present(ph, prompt):
            missing.append({"surface": sid, "phrase": ph})
    for cid, ph in required_legal_clauses(doc):
        req += 1
        if not _present(ph, prompt):
            missing.append({"surface": cid, "phrase": ph})
    forbidden = [{"surface": s, "word": w} for s, w in forbidden_hits(doc, prompt)]
    unlicensed = unlicensed_residue(doc, prompt)
    ok = (not missing) and (not forbidden) and (not unlicensed)
    kind, name = parse_scope(scope)
    return {
        "ok": ok,
        "missing": missing,
        "unratified_missing": unrat_missing,
        "forbidden": forbidden,
        "unlicensed": unlicensed,
        "required": req,
        "scope": {"kind": kind, "id": name},
    }


def resolve_canon(path):
    if not path:
        return None
    if os.path.isfile(path):
        return os.path.abspath(path)
    alt = os.path.join(_REPO, path)
    if os.path.isfile(alt):
        return os.path.abspath(alt)
    _andon("no canon %s" % path)


def resolve_subject(subject, search_path=None):
    """subject id -> surfaces file. Census first, then the search path.

    A subject with an IDENTITY.md and no surfaces file is a named
    refusal, not an unknown-subject error. That is the design: four
    subjects stay undone until a human walks them.
    """
    if not subject or not str(subject).strip():
        _andon("need a subject")
    key = str(subject).strip()
    ident_rel = None
    surf_rel = None
    for sub, ident, surf, _prof in CENSUS_ROWS:
        if sub.lower() == key.lower():
            ident_rel, surf_rel = ident, surf
            break
    if surf_rel:
        path = os.path.join(_REPO, surf_rel.replace("/", os.sep))
        if os.path.isfile(path):
            return os.path.abspath(path)
        _andon("no canon for subject %s (surfaces path %s missing)"
               % (key, surf_rel))
    roots = list(search_path) if search_path is not None else list(SEARCH_PATH)
    names = (key + ".surfaces.json",
             key.lower() + ".surfaces.json",
             key.upper() + ".surfaces.json")
    for root in roots:
        for name in names:
            p = os.path.join(root, name)
            if os.path.isfile(p):
                return os.path.abspath(p)
    if ident_rel:
        _andon("no canon for subject %s (identity exists, surfaces missing)"
               % key)
    _andon("unknown subject %s" % key)


def cover(doc, prompt, scope="subject"):
    """The router question: at this scope, is this prompt covered?"""
    chk = check_prompt(doc, prompt, scope=scope)
    cov = coverage(doc)
    return {"check": chk, "coverage": cov}


def ask(subject, prompt, scope="subject", search_path=None):
    """Resolve + load + cover. Refuses when there is no canon at all."""
    path = resolve_subject(subject, search_path=search_path)
    doc = load_canon(path)
    out = cover(doc, prompt, scope=scope)
    out["path"] = path
    return out


def refuse_uncovered(canon_path, prompt, scope="subject"):
    """The path gate. Import this; do not re-roll the check at each caller."""
    path = resolve_canon(canon_path)
    doc = load_canon(path)
    chk = check_prompt(doc, prompt, scope=scope)
    cov = coverage(doc)
    if not chk["ok"]:
        _andon(
            "canon does not cover ratified prompt: missing=%s forbidden=%s "
            "unlicensed=%s; unratified named not required: %s"
            % (chk["missing"], chk["forbidden"], chk.get("unlicensed") or [],
               cov["unratified_ids"]))
    return chk, cov


def subject_status(subject):
    """Census lookup that does not raise. Used by require_canon.

    surfaces       - IDENTITY + a surfaces file that loads
    identity-only  - IDENTITY, no surfaces (GALLEON/DRAGON/LOGO/E10-LAYER)
    unknown        - not in the census
    """
    if not subject or not str(subject).strip():
        return {"status": "unknown", "subject": None, "path": None,
                "identity": None}
    key = str(subject).strip()
    for sub, ident, surf, _prof in CENSUS_ROWS:
        if sub.lower() != key.lower():
            continue
        if surf:
            path = os.path.join(_REPO, surf.replace("/", os.sep))
            if os.path.isfile(path):
                return {"status": "surfaces", "subject": sub, "path": path,
                        "identity": ident}
            return {"status": "identity-only", "subject": sub, "path": None,
                    "identity": ident}
        return {"status": "identity-only", "subject": sub, "path": None,
                "identity": ident}
    return {"status": "unknown", "subject": key, "path": None, "identity": None}


def infer_subject_from_profile(profile_path):
    """Match a profile path to a CENSUS_ROWS subject. None if not listed."""
    if not profile_path:
        return None
    try:
        have = os.path.normcase(os.path.abspath(profile_path))
    except (TypeError, ValueError, OSError):
        return None
    for sub, _ident, _surf, prof_rel in CENSUS_ROWS:
        if not prof_rel:
            continue
        want = os.path.normcase(os.path.abspath(
            os.path.join(_REPO, prof_rel.replace("/", os.sep))))
        if have == want:
            return sub
    return None


def report_replay_drift(doc, prompt, scope="subject"):
    """Replay verdict. Reports; never refuses on missing/unlicensed/forbidden.

    A recorded prompt is a historical object. The canon moving under it
    (t87: ARMB 16/17 -> 14/19) is drift to name, not a reason to halt a
    faithful replay. refuses is always False. That is not a warn checkbox:
    the record is mandatory and a test pins that a covering-fail still
    returns replay_drift rather than ok-and-silent.
    """
    chk = check_prompt(doc, prompt, scope=scope)
    return {
        "verdict": "replay_match" if chk["ok"] else "replay_drift",
        "check": chk,
        "refuses": False,
    }


def require_canon(prompt, canon_path=None, subject=None, no_canon=False,
                  profile_path=None, scope="subject"):
    """Fail-closed spend gate. Silence is dead.

    --no-canon is the named escape, and only for a census identity-only
    subject. Combining it with a surfaces path, or aiming it at W3, is
    a refuse. That is the checkbox trap.
    """
    if prompt is None:
        _andon("need a prompt")
    path = (str(canon_path).strip() if canon_path else None) or None
    subj = (str(subject).strip() if subject else None) or None
    if not subj:
        subj = infer_subject_from_profile(profile_path)
    if no_canon and path:
        _andon("no-canon refused: surfaces attached at %s" % path)
    if path:
        chk, cov = refuse_uncovered(path, prompt, scope=scope)
        return {"gated": True, "subject": subj, "path": path,
                "check": chk, "coverage": cov, "note": None}
    if subj:
        st = subject_status(subj)
        if st["status"] == "surfaces":
            if no_canon:
                _andon(
                    "no-canon refused: %s has surfaces at %s"
                    % (st["subject"], st["path"]))
            chk, cov = refuse_uncovered(st["path"], prompt, scope=scope)
            return {"gated": True, "subject": st["subject"], "path": st["path"],
                    "check": chk, "coverage": cov, "note": None}
        if st["status"] == "identity-only":
            if not no_canon:
                _andon(
                    "no canon for subject %s (identity exists, surfaces "
                    "missing); pass --no-canon to proceed ungated"
                    % st["subject"])
            note = ("%s identity exists, surfaces missing"
                    % st["subject"])
            return {"gated": False, "subject": st["subject"], "path": None,
                    "check": None, "coverage": None, "note": note}
        _andon("unknown subject %s" % subj)
    if no_canon:
        _andon("no-canon requires a census subject")
    _andon(
        "no canon: pass --canon PATH, or --subject NAME, or "
        "--no-canon --subject NAME for an identity-only subject")


def occupancy(doc):
    """One prompt occupant per surface. Blocked additions stay blocked."""
    collisions = []
    by_id = {s["id"]: s for s in doc["surfaces"]}
    for b in doc.get("blocked_additions") or []:
        onto = b.get("onto")
        if onto not in by_id:
            _andon("blocked addition %s names unknown surface %s" % (
                b.get("id"), onto))
        occ = by_id[onto].get("occupant")
        if occ and occ.get("provenance") == "prompt" and occ.get("phrase"):
            # this is the predicted-drop class, recorded on purpose
            collisions.append({
                "addition": b.get("id"),
                "onto": onto,
                "occupant": occ.get("id"),
                "disposition": "blocked",
            })
    # two surfaces may share a phrase (paired pauldrons); two occupants
    # on ONE surface cannot be expressed in this schema. The check is:
    # occupant is a single object or null. Already enforced at load.
    return {"ok": True, "blocked": collisions}


def parse_named_table(text):
    """IDENTITY NAMED-table rows: id + phrase (markdown bold stripped)."""
    rows = []
    in_named = False
    for ln in text.splitlines():
        if ln.startswith("## NAMED"):
            in_named = True
            continue
        if in_named and ln.startswith("## "):
            break
        if not in_named:
            continue
        m = NAMED_ROW.match(ln)
        if not m:
            continue
        nid, raw = m.group(1), m.group(2)
        phrase = re.sub(r"\*\*", "", raw).strip()
        if nid and phrase:
            rows.append((nid, phrase))
    return rows


def pin_identity(doc, identity_path):
    if not os.path.isfile(identity_path):
        _andon("no identity %s" % identity_path)
    text = open(identity_path, encoding="utf-8").read()
    named = parse_named_table(text)
    if not named:
        _andon("no NAMED rows in %s" % identity_path)
    json_phrases = {}
    for s in doc["surfaces"]:
        occ = s.get("occupant") or {}
        if occ.get("id") and occ.get("phrase"):
            json_phrases[occ["id"]] = occ["phrase"]
    for b in doc.get("blocked_additions") or []:
        if b.get("id") and b.get("phrase"):
            json_phrases[b["id"]] = b["phrase"]
    missing_in_json = []
    for nid, phrase in named:
        if nid not in json_phrases:
            missing_in_json.append(nid)
        elif json_phrases[nid] != phrase:
            missing_in_json.append("%s phrase %r != %r" % (
                nid, json_phrases[nid], phrase))
    extra = []
    named_ids = {n for n, _ in named}
    for nid in json_phrases:
        if re.match(r"^[A-Z]\d+$", nid) and nid not in named_ids:
            extra.append(nid)
    if missing_in_json or extra:
        _andon(
            "identity pin failed: missing_in_json=%s extra_named_ids=%s"
            % (missing_in_json, extra))
    return {"ok": True, "named_rows": len(named), "json_phrases": len(json_phrases)}


def sidecar_path(canon_path):
    if canon_path.endswith(".surfaces.json"):
        return canon_path[: -len(".surfaces.json")] + ".verify.json"
    return os.path.splitext(canon_path)[0] + ".verify.json"


def load_sidecar(canon_path):
    side = sidecar_path(canon_path)
    if not os.path.isfile(side):
        return None, side
    return json.load(open(side, encoding="utf-8")), side


def verify_regions(twin_rgb, ref_rgb, regions, mask=None):
    """Per-region median CIE76 dE. Writes state; does not edit the canon."""
    if twin_rgb.shape != ref_rgb.shape:
        _andon("twin %s vs reference %s" % (twin_rgb.shape, ref_rgb.shape))
    H, W = twin_rgb.shape[:2]
    t01 = twin_rgb.astype(np.float64) / 255.0
    r01 = ref_rgb.astype(np.float64) / 255.0
    dE = np.linalg.norm(to_lab(t01) - to_lab(r01), axis=-1)
    if mask is None:
        mask = np.ones((H, W), dtype=bool)
    out = []
    for reg in regions:
        name = reg["name"]
        x0, y0, x1, y1 = [int(v) for v in reg["box"]]
        if x0 < 0 or y0 < 0 or x1 > W or y1 > H or x1 <= x0 or y1 <= y0:
            _andon("region %s box %s exceeds %dx%d" % (name, [x0, y0, x1, y1], W, H))
        sel = np.zeros((H, W), dtype=bool)
        sel[y0:y1, x0:x1] = True
        sel &= mask
        if not sel.any():
            out.append({"name": name, "px": 0, "state": "empty"})
            continue
        med = float(np.median(dE[sel]))
        if med <= DE_LANDED:
            state = "landed"
        elif med > DE_MISSED:
            state = "missed"
        else:
            state = "uncertain"
        out.append({
            "name": name,
            "px": int(sel.sum()),
            "median_dE": med,
            "state": state,
        })
    return out


def phrase_hits_in_text(text, phrases):
    hit = []
    miss = []
    for nid, ph in phrases:
        key = ARTICLE.sub("", ph.strip()).lower()
        if key and key in text.lower():
            hit.append(nid)
        else:
            miss.append(nid)
    return hit, miss


def w3_named_phrases():
    path = os.path.join(_REPO, "canon", "W3-IDENTITY.md")
    text = open(path, encoding="utf-8").read()
    return parse_named_table(text)


def profile_default_prompt():
    path = os.path.join(_REPO, "profiles", "character.json")
    doc = json.load(open(path, encoding="utf-8"))
    return doc["tools"]["restylize_views.py"]["prompt"]["value"]


# Identity files and the surfaces / profile they pair with, when they do.
# LOGO has no NAMED table. E10-LAYER is a layer identity, not a twin subject.
# Generating missing surfaces files is not this build.
CENSUS_ROWS = (
    ("W3", "canon/W3-IDENTITY.md", "canon/w3.surfaces.json",
     "profiles/character.json"),
    ("GALLEON", "canon/GALLEON-IDENTITY.md", None, "profiles/ship.json"),
    ("DRAGON", "canon/DRAGON-IDENTITY.md", None, "profiles/beast.json"),
    ("LONGSWORD", "canon/LONGSWORD-IDENTITY.md",
     "canon/longsword.surfaces.json", "profiles/prop.json"),
    ("E10-LAYER", "canon/E10-LAYER-IDENTITY.md", None, None),
    ("LOGO", "canon/LOGO-IDENTITY.md", None, None),
    # A1 - the reference-first exemplar (E57 2026-08-17; profiled E58 2026-08-18).
    # profiles/a1.json is A1's OWN profile, authored at E58 Stage D from the ratified
    # canon directly (not relocated from an accepted asset - A1 has none yet). The
    # placeholder pairing to W3's profiles/character.json (E57) is retired here.
    ("A1", "canon/A1-IDENTITY.md", "canon/a1.surfaces.json",
     "profiles/a1.json"),
)


def _profile_restylize_prompt(rel):
    path = os.path.join(_REPO, rel.replace("/", os.sep))
    if not os.path.isfile(path):
        return None
    doc = json.load(open(path, encoding="utf-8"))
    block = (doc.get("tools") or {}).get("restylize_views.py") or {}
    ent = block.get("prompt") or {}
    return ent.get("value")


def census():
    """One row per IDENTITY.md. Quoteable. Does not invent surfaces files."""
    rows = []
    for subject, ident_rel, surf_rel, prof_rel in CENSUS_ROWS:
        ident_path = os.path.join(_REPO, ident_rel.replace("/", os.sep))
        named = []
        if os.path.isfile(ident_path):
            named = parse_named_table(open(ident_path, encoding="utf-8").read())
        rec = {
            "subject": subject,
            "identity": ident_rel,
            "identity_named": len(named),
            "surfaces": surf_rel,
            "occupancy": None,
            "ratified": None,
            "unratified": None,
            "profile": prof_rel,
            "profile_hits": None,
            "profile_named": len(named) if named else None,
        }
        if surf_rel:
            doc = load_canon(os.path.join(_REPO, surf_rel.replace("/", os.sep)))
            cov = coverage(doc)
            rec["occupancy"] = "%d/%d" % (cov["named"], cov["prompt_surfaces"])
            rec["ratified"] = "%d/%d" % (cov["ratified"], cov["prompt_surfaces"])
            rec["unratified"] = cov["unratified"]
            rec["unratified_ids"] = cov["unratified_ids"]
        if prof_rel and named:
            prompt = _profile_restylize_prompt(prof_rel)
            if prompt is not None:
                hit, _miss = phrase_hits_in_text(prompt, named)
                rec["profile_hits"] = len(hit)
        rec["bind"] = None
        if surf_rel:
            rec["bind"] = _bind_census_cell(surf_rel)
        rows.append(rec)
    return rows


def _bind_census_cell(surf_rel):
    """Sibling .binding.json coverage, or NONE. Faces, not pixels."""
    import canon_bind as B
    path = os.path.join(_REPO, surf_rel.replace("/", os.sep))
    bpath = B.binding_path(path)
    if not os.path.isfile(bpath):
        return "NONE"
    try:
        surf = load_canon(path)
        bind = B.load_binding(bpath, surf)
        cov = B.coverage(bind)
    except Exception as e:
        return "ANDON %s" % e
    return "%d/%d faces, %d proposed" % (
        cov["bound"], cov["surfaces"], cov["proposed"])


def format_census(rows):
    lines = [
        "canon_gate %s  census  (occupancy is not ratification)"
        % TOOL_VERSION,
        "%-10s %7s %11s %10s %10s %s"
        % ("subject", "named", "occupancy", "ratified", "prof_hit", "surfaces"),
    ]
    for r in rows:
        lines.append(
            "%-10s %7d %11s %10s %10s %s"
            % (r["subject"], r["identity_named"],
               r["occupancy"] or "-",
               r["ratified"] or "-",
               ("-" if r["profile_hits"] is None
                else "%d/%d" % (r["profile_hits"], r["profile_named"])),
               r["surfaces"] or "NONE"))
    lines.append("bind (faces; 0.00 is unbound; names live on the surfaces file)")
    for r in rows:
        lines.append("  %-10s %s" % (r["subject"], r.get("bind") or "NONE"))
    return "\n".join(lines) + "\n"


def _selftest_calibration():
    named = w3_named_phrases()
    if len(named) != W3_NAMED:
        _andon("W3 NAMED rows are %d, not %d" % (len(named), W3_NAMED))
    prompt = profile_default_prompt()
    hit, miss = phrase_hits_in_text(prompt, named)
    if len(hit) != PROFILE_DEFAULT_HITS:
        _andon(
            "profile default hits %d of %d, not %d (hit=%s miss=%s)"
            % (len(hit), W3_NAMED, PROFILE_DEFAULT_HITS, hit, miss))
    return hit, miss


def _selftest_gates(scratch):
    fixture = {
        "subject": "FIXT",
        "kind": "prop",
        "schema": 1,
        "surfaces": [
            {"id": "blade", "occupant": {
                "id": "P1", "phrase": "a steel blade", "provenance": "prompt"}},
            {"id": "grip", "occupant": {
                "id": "P2", "phrase": "a leather grip", "provenance": "prompt"}},
            {"id": "pommel", "occupant": None},
            {"id": "sil", "occupant": {
                "id": "M1", "phrase": None, "provenance": "mesh"}},
            {"id": "arm", "occupant": {
                "id": "bare", "phrase": None, "provenance": "prompt",
                "kind": "bare", "forbidden": ["sleeve"]}},
        ],
        "blocked_additions": [
            {"id": "P9", "phrase": "gold inlay on the blade", "onto": "blade"},
        ],
        "joints": [{"id": "j1", "a": "blade", "b": "grip", "phrase": "cut"}],
    }
    path = os.path.join(scratch, "fixt.surfaces.json")
    json.dump(fixture, open(path, "w", encoding="utf-8"))
    doc = load_canon(path)
    cov = coverage(doc)
    # prompt surfaces: blade, grip, pommel (hole), arm (bare) = 4
    # named: blade, grip, arm = 3; coverage 0.75
    if cov["prompt_surfaces"] != 4 or cov["named"] != 3:
        _andon("fixture coverage counts %s" % cov)
    if abs(cov["coverage"] - 0.75) > 1e-12:
        _andon("fixture coverage is %r, not 0.75" % cov["coverage"])
    good = "a steel blade, a leather grip, gold inlay on the blade"
    chk = check_prompt(doc, good)
    if not chk["ok"]:
        _andon("complete fixture prompt refused: %s" % chk)
    thin = "a steel blade"
    chk2 = check_prompt(doc, thin)
    if chk2["ok"] or not any(m["phrase"] == "a leather grip" for m in chk2["missing"]):
        _andon("thin prompt did not fail on leather grip")
    neg = "a steel blade, no a leather grip, gold inlay on the blade"
    chk3 = check_prompt(doc, neg)
    if chk3["ok"]:
        _andon("negated leather grip passed")
    sleeve = good + ", a long sleeve"
    chk4 = check_prompt(doc, sleeve)
    if chk4["ok"] or not chk4["forbidden"]:
        _andon("sleeve on a bare arm did not fire")
    sless = good + ", sleeveless"
    chk5 = check_prompt(doc, sless)
    if not chk5["ok"]:
        _andon("sleeveless was treated as a sleeve: %s" % chk5)
    # schema 1: reverse is not armed
    if chk.get("unlicensed"):
        _andon("schema-1 fixture armed reverse: %s" % chk)
    occ = occupancy(doc)
    if not occ["blocked"] or occ["blocked"][0]["addition"] != "P9":
        _andon("blocked addition was not reported")
    # verify: identical images land; a recolour misses
    a = np.full((16, 16, 3), 40, dtype=np.uint8)
    b = a.copy()
    b[:, 8:] = (200, 20, 20)
    regs = [{"name": "left", "box": [0, 0, 8, 16]},
            {"name": "right", "box": [8, 0, 16, 16]}]
    same = verify_regions(a, a, regs)
    if same[0]["state"] != "landed" or same[1]["state"] != "landed":
        _andon("identical images did not land: %s" % same)
    diff = verify_regions(b, a, regs)
    if diff[0]["state"] != "landed":
        _andon("unchanged half did not land: %s" % diff)
    if diff[1]["state"] != "missed":
        _andon("recoloured half was not missed: %s" % diff)
    _selftest_router(scratch)
    return cov


def _selftest_router(scratch):
    """Schema 2: both directions, scope, resolve, stale consumer."""
    fixture = {
        "subject": "R2",
        "kind": "prop",
        "schema": 2,
        "legal_clauses": [
            {"id": "bg", "phrase": "plain grey background", "class": "style"},
        ],
        "scopes": {
            "views": {
                "0": {"surfaces": ["blade", "grip"], "status": "draft"},
            },
            "strokes": {},
        },
        "surfaces": [
            {"id": "blade", "occupant": {
                "id": "P1", "phrase": "a steel blade", "provenance": "prompt"}},
            {"id": "grip", "occupant": {
                "id": "P2", "phrase": "a leather grip", "provenance": "prompt"}},
            {"id": "pommel", "occupant": {
                "id": "P3", "phrase": "a gold pommel", "provenance": "prompt"}},
        ],
        "blocked_additions": [],
        "joints": [],
    }
    path = os.path.join(scratch, "r2.surfaces.json")
    json.dump(fixture, open(path, "w", encoding="utf-8"))
    doc = load_canon(path)
    covering = "a steel blade, a leather grip, a gold pommel, plain grey background"
    chk = check_prompt(doc, covering)
    if not chk["ok"]:
        _andon("schema-2 covering prompt refused: %s" % chk)
    neck = covering + ", gold necklace"
    chk_n = check_prompt(doc, neck)
    if chk_n["ok"]:
        _andon("gold necklace passed the reverse check")
    if not any("gold necklace" in (u.get("span") or "") for u in chk_n["unlicensed"]):
        _andon("unlicensed residue missed gold necklace: %s" % chk_n)
    view0 = check_prompt(doc, "a steel blade, a leather grip, plain grey background",
                         scope="view:0")
    if not view0["ok"]:
        _andon("view:0 covering prompt refused: %s" % view0)
    view0_thin = check_prompt(doc, "a steel blade, plain grey background",
                              scope="view:0")
    if view0_thin["ok"] or not any(m["phrase"] == "a leather grip"
                                   for m in view0_thin["missing"]):
        _andon("view:0 did not require the in-scope grip")
    try:
        check_prompt(doc, covering, scope="view:9")
        _andon("undeclared view:9 did not refuse")
    except Andon as e:
        if "no view scope 9" not in str(e):
            _andon("view:9 refused for the wrong reason: %s" % e)
    try:
        check_prompt(doc, covering, scope="stroke:k")
        _andon("undeclared stroke did not refuse")
    except Andon as e:
        if "no stroke scope k" not in str(e):
            _andon("stroke refused for the wrong reason: %s" % e)
    stale = dict(fixture)
    stale["schema"] = 3
    stale_path = os.path.join(scratch, "stale.surfaces.json")
    json.dump(stale, open(stale_path, "w", encoding="utf-8"))
    try:
        load_canon(stale_path)
        _andon("schema 3 loaded on a schema-2 consumer")
    except Andon as e:
        if "stale consumer" not in str(e):
            _andon("schema 3 refused for the wrong reason: %s" % e)
    try:
        resolve_subject("GALLEON")
        _andon("GALLEON resolved to a surfaces file")
    except Andon as e:
        if "identity exists, surfaces missing" not in str(e):
            _andon("GALLEON refused for the wrong reason: %s" % e)
    w3 = resolve_subject("W3")
    if not os.path.isfile(w3):
        _andon("W3 did not resolve")
    # fail-closed
    try:
        require_canon("anything")
        _andon("silence did not refuse")
    except Andon as e:
        if "no canon:" not in str(e):
            _andon("silence refused for the wrong reason: %s" % e)
    try:
        require_canon("anything", no_canon=True, subject="W3")
        _andon("no-canon on W3 did not refuse")
    except Andon as e:
        if "no-canon refused" not in str(e):
            _andon("no-canon W3 refused for the wrong reason: %s" % e)
    ung = require_canon("anything", no_canon=True, subject="GALLEON")
    if ung["gated"] or "GALLEON" not in (ung.get("note") or ""):
        _andon("GALLEON --no-canon was not ungated: %s" % ung)
    drift = report_replay_drift(load_canon(w3), "plain grey background")
    if drift["refuses"] or drift["verdict"] != "replay_drift":
        _andon("replay_drift refused or misnamed: %s" % drift)
    _selftest_required_clause(scratch)


def _selftest_required_clause(scratch):
    """E59 Stage 0: legal_clause required:true must occur; unmarked must not.

    Two can-fail checks, named separately in the charter so neither one alone
    proves the change did what it says: (a) stripping the required clause
    refuses, naming it, same shape as a missing ratified occupant phrase;
    (b) stripping an UNMARKED clause does NOT refuse — without this half a
    change that made every legal_clause mandatory by accident would pass (a)
    and go unnoticed, on this fixture and on W3's five unmarked clauses alike.
    """
    fixture = {
        "subject": "R3",
        "kind": "prop",
        "schema": 2,
        "legal_clauses": [
            {"id": "bg", "phrase": "plain grey background", "class": "style"},
            {"id": "pose", "phrase": "head facing straight ahead",
             "class": "staging", "required": True},
        ],
        "surfaces": [
            {"id": "blade", "occupant": {
                "id": "P1", "phrase": "a steel blade", "provenance": "prompt"}},
        ],
        "blocked_additions": [],
        "joints": [],
    }
    path = os.path.join(scratch, "r3.surfaces.json")
    json.dump(fixture, open(path, "w", encoding="utf-8"))
    doc = load_canon(path)
    full = "a steel blade, plain grey background, head facing straight ahead"
    chk_full = check_prompt(doc, full)
    if not chk_full["ok"]:
        _andon("required-clause fixture: full prompt refused: %s" % chk_full)
    # (a) the required clause, stripped -> refuses, naming it
    stripped_required = "a steel blade, plain grey background"
    chk_req = check_prompt(doc, stripped_required)
    if chk_req["ok"] or not any(
            m["phrase"] == "head facing straight ahead" for m in chk_req["missing"]):
        _andon("required-clause fixture: missing required clause did not "
               "refuse naming it: %s" % chk_req)
    # (b) the UNMARKED clause ("bg"), stripped -> still ok. This is the half
    # that proves the change did not make every staging clause mandatory.
    stripped_unmarked = "a steel blade, head facing straight ahead"
    chk_unmarked = check_prompt(doc, stripped_unmarked)
    if not chk_unmarked["ok"]:
        _andon("required-clause fixture: an UNMARKED clause's absence wrongly "
               "refused (every staging clause would be mandatory): %s"
               % chk_unmarked)
    # a malformed `required` value is a load failure, not a silent default
    bad = dict(fixture)
    bad["legal_clauses"] = [dict(fixture["legal_clauses"][0]),
                            {"id": "pose", "phrase": "x", "class": "staging",
                             "required": "yes"}]
    bad_path = os.path.join(scratch, "r3bad.surfaces.json")
    json.dump(bad, open(bad_path, "w", encoding="utf-8"))
    try:
        load_canon(bad_path)
        _andon("required: \"yes\" (a string, not a bool) loaded without refusing")
    except Andon as e:
        if "required must be a bool" not in str(e):
            _andon("malformed required refused for the wrong reason: %s" % e)


def selftest(scratch=None):
    _selftest_calibration()
    if scratch is None:
        scratch = tempfile.mkdtemp(prefix="canon_gate_")
    return _selftest_gates(scratch)


def build_parser():
    p = argparse.ArgumentParser(
        description="Canon router: resolve a subject, cover a prompt at a scope.")
    p.add_argument("--selftest", action="store_true")
    sub = p.add_subparsers(dest="cmd")
    def add_source(sp):
        sp.add_argument("--canon", default=None)
        sp.add_argument("--subject", default=None)
    c = sub.add_parser("coverage")
    add_source(c)
    k = sub.add_parser("check")
    add_source(k)
    k.add_argument("--prompt", required=True)
    k.add_argument("--scope", default="subject",
                   help="subject | view:ID | stroke:ID")
    o = sub.add_parser("occupancy")
    add_source(o)
    i = sub.add_parser("pin-identity")
    add_source(i)
    i.add_argument("--identity", default=None)
    r = sub.add_parser("resolve", help="subject id -> surfaces file")
    r.add_argument("--subject", required=True)
    sub.add_parser("census", help="every IDENTITY + surfaces + profile default")
    v = sub.add_parser("verify")
    add_source(v)
    v.add_argument("--twin", required=True)
    v.add_argument("--reference", required=True)
    v.add_argument("--regions", required=True,
                   help="JSON list of {name, box:[x0,y0,x1,y1]}")
    v.add_argument("--write-sidecar", action="store_true")
    return p


def _load_from_args(args):
    if getattr(args, "canon", None):
        path = resolve_canon(args.canon)
        return load_canon(path), path
    if getattr(args, "subject", None):
        path = resolve_subject(args.subject)
        return load_canon(path), path
    _andon("need --canon or --subject")


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.selftest:
            selftest()
            sys.stdout.write(
                "calibration profile-default hits %d of %d  "
                "fixture coverage 0.75  sleeve refused  sleeveless held  "
                "router reverse held  fail-closed held  "
                "required clause held\n"
                % (PROFILE_DEFAULT_HITS, W3_NAMED))
            return 0
        if not args.cmd:
            _andon("need a subcommand or --selftest")
        if args.cmd == "census":
            sys.stdout.write(format_census(census()))
            return 0
        if args.cmd == "resolve":
            sys.stdout.write(resolve_subject(args.subject) + "\n")
            return 0
        doc, canon_path = _load_from_args(args)
        if args.cmd == "coverage":
            cov = coverage(doc)
            sys.stdout.write(
                "canon_gate %s  %s  occupancy %d/%d  "
                "ratified %d/%d  unratified %d %s  holes %s\n"
                % (TOOL_VERSION, cov["subject"],
                   cov["named"], cov["prompt_surfaces"],
                   cov["ratified"], cov["prompt_surfaces"],
                   cov["unratified"],
                   ("(" + ",".join(cov["unratified_ids"]) + ")")
                   if cov["unratified_ids"] else "",
                   ",".join(cov["hole_ids"]) or "-"))
            return 0
        if args.cmd == "check":
            chk = check_prompt(doc, args.prompt, scope=args.scope)
            if not chk["ok"]:
                _andon(
                    "prompt failed: missing=%s forbidden=%s unlicensed=%s"
                    % (chk["missing"], chk["forbidden"], chk["unlicensed"]))
            extra = ""
            if chk["unratified_missing"]:
                extra = "  unratified_missing %d" % len(chk["unratified_missing"])
            sys.stdout.write(
                "prompt covers %d required phrases%s\n"
                % (chk["required"], extra))
            return 0
        if args.cmd == "occupancy":
            occ = occupancy(doc)
            sys.stdout.write(
                "occupancy ok  blocked_additions %d\n" % len(occ["blocked"]))
            return 0
        if args.cmd == "pin-identity":
            ident = args.identity or os.path.join(
                _REPO, doc.get("source_identity", ""))
            pin = pin_identity(doc, ident)
            sys.stdout.write(
                "identity pin ok  named %d  json phrases %d\n"
                % (pin["named_rows"], pin["json_phrases"]))
            return 0
        if args.cmd == "verify":
            twin = np.asarray(Image.open(args.twin).convert("RGB"))
            ref = np.asarray(Image.open(args.reference).convert("RGB"))
            regs = json.load(open(args.regions, encoding="utf-8"))
            if isinstance(regs, dict):
                regs = regs.get("regions") or regs.get("views", {}).get("0") or []
            rows = verify_regions(twin, ref, regs)
            payload = {
                "tool": "canon_gate.py",
                "tool_version": TOOL_VERSION,
                "canon": os.path.abspath(canon_path),
                "regions": rows,
            }
            sys.stdout.write(
                "verify %d regions: %s\n"
                % (len(rows),
                   ", ".join("%s=%s" % (r["name"], r["state"]) for r in rows)))
            if args.write_sidecar:
                _side = sidecar_path(canon_path)
                # never write next to a canon in-repo unless asked; sidecar
                # beside the canon path the caller named
                with open(_side, "w", encoding="utf-8", newline="\n") as f:
                    json.dump(payload, f, indent=1)
                    f.write("\n")
            return 0
        _andon("unknown command %s" % args.cmd)
    except Andon as e:
        sys.stderr.write(str(e) + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
