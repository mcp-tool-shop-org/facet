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
  profiles/character.json restylize prompt contains exactly 6 of the
  W3 NAMED phrases (article-stripped). The ARMB workflow the
  older handoff cited (stroke_1_y+090_e+00_workflow.json:181) contains
  16 and is missing only N17; grip/gauntlet/greave/hand appear
  zero times in that string. The brief's "six" is the profile default,
  not that file. Both numbers are the defect.

  W3_NAMED was 17 when this was written, 19 when the hand and shin rows were
  drafted, and is 20 since the Director caught the hand draft: the free hand carries a
  GAUNTLET, so the armour is ASYMMETRIC. The forearm rows were NOT enacted -
  three contested readings in one session is where the advisor stopped. Neither hit count moved at any
  step. Completing the canon widened the gap 6/17 -> 6/19 without a
  single character of either prompt changing, which is the whole reason the
  ratio is computed and never stored.

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
SCHEMA = 1
NEGATION = re.compile(r"\b(no|not|without|lacking)\b", re.I)
SLEEVE = re.compile(r"\bsleeve(?!less)\b", re.I)
NAMED_ROW = re.compile(
    r"^\|\s*([A-Z]\d+)\s*\|\s*(.*?)\s*\|", re.M)
ARTICLE = re.compile(r"^a\s+", re.I)
DE_LANDED = 2.3
DE_MISSED = 10.0
NEG_WINDOW = 24

# Article-stripped NAMED phrases in the profile default (measured).
#
# W3_NAMED moved 17 -> 19 -> 21 on purpose 2026-08-17: the hand and shin rows,
# then the asymmetric-arm correction the Director caught (N20 gauntlet, N21/N21b
# bare arms). The two hit counts DID NOT MOVE
# and that is the finding: the profile default still names 6 and the ARMB
# workflow still names 16, so completing the canon WIDENED the gap rather than
# closing it. A denominator that grows while the numerators hold is exactly the
# moving-denominator trap this repo has been bitten by five times - so both
# numerators stay pinned separately from the total, and the ratios are never
# stored, only computed.
#
# 6 -> 5 on 2026-08-17: the Director ruled the garment is a KILT, not a skirt.
# The live default still says skirt, so renaming the canon cost a hit without
# anyone touching the prompt - 6/17 -> 6/19 -> 5/19. Every canon repair so far
# has WIDENED this gap, which is what a specimen is supposed to do.
PROFILE_DEFAULT_HITS = 5
ARMB_HITS = 16
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
    if int(doc.get("schema", -1)) != SCHEMA:
        _andon("canon schema %r is not %d" % (doc.get("schema"), SCHEMA))
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
    return doc


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
        window = hay[max(0, i - NEG_WINDOW):i]
        if not NEGATION.search(window):
            return True
        start = i + 1


def required_phrases(doc):
    out = []
    for s in doc["surfaces"]:
        occ = s.get("occupant") or {}
        ph = occ.get("phrase")
        if ph and occ.get("provenance") == "prompt":
            out.append((s["id"], ph))
    for b in doc.get("blocked_additions") or []:
        if b.get("phrase"):
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


def check_prompt(doc, prompt):
    """Ratified phrases are required. Unratified phrases are reported.

    A drafted row (`ratify: true`) is not the Director's canon. Requiring
    it spends his credits on a phrase he has not seen. Omitting it from
    the report would hide the draft. Forbidden words still fire on every
    row, including drafts: adding a gauntlet is a spend in the wrong
    direction.
    """
    if prompt is None:
        _andon("need a prompt")
    unrat_ids = _unratified_ids(doc)
    missing = []
    unrat_missing = []
    req = 0
    for sid, ph in required_phrases(doc):
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
    forbidden = [{"surface": s, "word": w} for s, w in forbidden_hits(doc, prompt)]
    ok = (not missing) and (not forbidden)
    return {
        "ok": ok,
        "missing": missing,
        "unratified_missing": unrat_missing,
        "forbidden": forbidden,
        "required": req,
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


def refuse_uncovered(canon_path, prompt):
    """The path gate. Import this; do not re-roll the check at each caller."""
    path = resolve_canon(canon_path)
    doc = load_canon(path)
    chk = check_prompt(doc, prompt)
    cov = coverage(doc)
    if not chk["ok"]:
        _andon(
            "canon does not cover ratified prompt: missing=%s forbidden=%s; "
            "unratified named not required: %s"
            % (chk["missing"], chk["forbidden"], cov["unratified_ids"]))
    return chk, cov


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
        rows.append(rec)
    return rows


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
    return cov


def selftest(scratch=None):
    _selftest_calibration()
    if scratch is None:
        scratch = tempfile.mkdtemp(prefix="canon_gate_")
    return _selftest_gates(scratch)


def build_parser():
    p = argparse.ArgumentParser(
        description="Canon surface database and the gates that load it.")
    p.add_argument("--selftest", action="store_true")
    sub = p.add_subparsers(dest="cmd")
    def add_canon(sp):
        sp.add_argument("--canon", required=True)
    c = sub.add_parser("coverage")
    add_canon(c)
    k = sub.add_parser("check")
    add_canon(k)
    k.add_argument("--prompt", required=True)
    o = sub.add_parser("occupancy")
    add_canon(o)
    i = sub.add_parser("pin-identity")
    add_canon(i)
    i.add_argument("--identity", default=None)
    sub.add_parser("census", help="every IDENTITY + surfaces + profile default")
    v = sub.add_parser("verify")
    add_canon(v)
    v.add_argument("--twin", required=True)
    v.add_argument("--reference", required=True)
    v.add_argument("--regions", required=True,
                   help="JSON list of {name, box:[x0,y0,x1,y1]}")
    v.add_argument("--write-sidecar", action="store_true")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.selftest:
            selftest()
            sys.stdout.write(
                "calibration profile-default hits %d of %d  "
                "fixture coverage 0.75  sleeve refused  sleeveless held\n"
                % (PROFILE_DEFAULT_HITS, W3_NAMED))
            return 0
        if not args.cmd:
            _andon("need a subcommand or --selftest")
        if args.cmd == "census":
            sys.stdout.write(format_census(census()))
            return 0
        doc = load_canon(args.canon)
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
            chk = check_prompt(doc, args.prompt)
            if not chk["ok"]:
                _andon(
                    "prompt failed: missing=%s forbidden=%s"
                    % (chk["missing"], chk["forbidden"]))
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
                "canon": os.path.abspath(args.canon),
                "regions": rows,
            }
            sys.stdout.write(
                "verify %d regions: %s\n"
                % (len(rows),
                   ", ".join("%s=%s" % (r["name"], r["state"]) for r in rows)))
            if args.write_sidecar:
                _side = sidecar_path(args.canon)
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
