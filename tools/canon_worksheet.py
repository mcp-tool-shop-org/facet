# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Canon worksheet. Kind templates, empty occupants, a density readout.

WHY THIS EXISTS. Consult #19 / build #19. The router (#18) proved the
schema: resolve, both directions, scope, schema 1+2. Four subjects
still have IDENTITY.md and no surfaces file. A skeleton emitter that
turns a NAMED table into occupants would invent canon under a clock,
which is what those four are being protected from.

THE THESIS, ATTACKED.

  SURFACE is still the row. The worksheet is how a hole becomes a
  row BEFORE anyone has named it: a kind template emits the surfaces
  the kind implies, occupants null. N17 (the grip) was absent from
  N1-N16; a kind=prop/weapon template with a grip row is the thing
  that would have shown it. The humanoid template is the W3-walked
  BODY set and does not include the weapon -- a greatsword is a
  composed prop, not a body part.

  The tool is structurally incapable of filling an occupant. IDENTITY
  NAMED phrases land in `inventory` with assigned=null. An inventory
  `assigned` hint is a note, not a write. to_surfaces copies a
  human-authored occupant object and never reads inventory to build
  one. Mesh/style rows carry a structural occupant (phrase null,
  provenance mesh|style) so they stay out of the coverage
  denominator; that is not a named element.

  Scopes: this round emits SLOTS (the 8-flat camera ring, empty
  surface lists). Filling which surfaces a camera sees is human
  work, the same as filling occupants. to_surfaces writes a view
  only when the human put a non-empty id list on it. Empty slots
  do not become "no answer" keys in the surfaces file.

  Spatial binding uses the existing region format, keyed by surface
  id not free text. bind copies a box only when incoming `name`
  equals a surface id. skirt does not become kilt.

  Round-trip: from_surfaces re-emits a worksheet showing what is
  still open; to_surfaces of a filled worksheet is a schema-2
  surfaces file the router will load. A worksheet is not a surfaces
  file (type=worksheet).

  Density (finding A). The authoring budget is ELEMENT COUNT, not
  tokens. The readout reports three numbers that are easy to
  collapse and must not be: prompt_surfaces (coverage denominator),
  required_checks (what the gate requires, including paired
  duplicates and blocked additions), unique_elements (distinct
  occupant+blocked phrases -- the F1-relevant count). Tokens are
  tokenized, never estimated (F9). The encoder's effective length
  is unmeasured (F8) and this file does not pretend to measure it.

WHAT THIS DOES NOT COVER.

  Filling occupants. Deriving a prompt. Auto-scoping a view from
  geometry or colour (one PBR, 13,715 islands). Mapping s3_sheet
  free-text names onto surface ids. Front-loading / reordering
  (F4, p=.399). A CLIPScore gate. A rewriter. Three-tier prompt UI.
  Claiming a seed replays a generation. Measuring Qwen effective
  length (needs the encoder, not a tokenizer).

  Co-location as a field finding (F13): unnamed in the retrieved
  literature. Studio evidence is one subject, one surface, three
  grammatical forms. Recorded here as a literature gap, not
  promoted to docs/findings.md.

CALIBRATION CLAIM (run --selftest; T93 pins the same numbers).
  emit(kind=humanoid, identity=W3-IDENTITY.md) produces a worksheet
  whose every occupant phrase is empty, and all 19 NAMED rows sit
  in inventory with assigned=null. A poison phrase in inventory,
  even with assigned set to a surface id, does not appear on any
  occupant after to_surfaces.

  python tools/canon_worksheet.py --selftest

YES/NO INTERVALS.

  emit occupant     phrase is always empty. Mesh/style may carry
                    {phrase:null, provenance:mesh|style}.
  inventory         IDENTITY NAMED rows, assigned=null. Never
                    copied onto a surface by this tool.
  to_surfaces       copies human-authored occupants. Ignores
                    inventory. Omits legal_clauses if empty (an
                    empty list would ARM the reverse check).
                    Writes scopes.views only for non-empty lists.
  bind              name == surface id, else unmatched. No rename.
  density           prompt_surfaces / required_checks /
                    unique_elements. tokens from a real tokenizer
                    or null. Never len/4.

  python tools/canon_worksheet.py emit --kind humanoid --identity canon/W3-IDENTITY.md
  python tools/canon_worksheet.py from-surfaces --canon canon/w3.surfaces.json
  python tools/canon_worksheet.py to-surfaces --worksheet W.json --out X.surfaces.json
  python tools/canon_worksheet.py readout --canon canon/w3.surfaces.json
  python tools/canon_worksheet.py bind --worksheet W.json --regions tools/s3_sheet_regions.json
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import sys
import tempfile

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_TOOLS)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import canon_gate as C  # noqa: E402

TOOL_VERSION = "1.0.0"
WORKSHEET_SCHEMA = 1
WS_TYPE = "worksheet"

# The studio's measured 8-flat ring (s3_sheet_regions.json view_map).
# Not invented per subject. A kind either uses this ring or has no views.
FLAT_RING = (
    ("0", "y+000_e+00"),
    ("1", "y+045_e+00"),
    ("2", "y+090_e+00"),
    ("3", "y+135_e+00"),
    ("4", "y+180_e+00"),
    ("5", "y+225_e+00"),
    ("6", "y+270_e+00"),
    ("7", "y+315_e+00"),
)

# F1 annotation. Transfer to this stack is unmeasured; do not compute a
# remaining-quality number from the 8.53 figure.
F1_NOTE = (
    "F1 (Foong et al. 2023, arXiv:2311.13620): each added prompt "
    "component cost ~8.53% of mean Components-Inclusion-Score on "
    "an SD-family model, tested well below 17-24 elements. Transfer "
    "to Qwen+ControlNet+LoRA is unmeasured."
)
F8_NOTE = (
    "F8: this stack's encoder is Qwen2.5-VL-7B-Instruct, declared "
    "max 512/1024. Effective reading length is unmeasured. Token "
    "count is not that length."
)


class Andon(ValueError):
    pass


def _andon(msg):
    raise Andon("ANDON: " + msg)


def _surf(sid, name, role="prompt"):
    return {"id": sid, "name": name, "role": role}


def _joint(jid, a, b):
    return {"id": jid, "a": a, "b": b, "phrase": None}


# Kind templates. Occupants are not stored here. role=mesh|style becomes a
# structural occupant (phrase null) so the row stays out of the prompt
# denominator. role=prompt becomes occupant null -- a hole.
#
# humanoid is the W3-walked BODY set, the studio exemplar. It is not a
# universal anatomy. The weapon (blade/crossguard/pommel/grip) is kind
# prop/weapon: that is the N17 lesson.
KINDS = {
    "humanoid": {
        "cameras": FLAT_RING,
        "surfaces": [
            _surf("scalp", "scalp"),
            _surf("beard", "beard"),
            _surf("torso", "torso"),
            _surf("upper_arm_L", "left upper arm"),
            _surf("upper_arm_R", "right upper arm"),
            _surf("pauldron_L", "left pauldron"),
            _surf("pauldron_R", "right pauldron"),
            _surf("belt", "belt band"),
            _surf("belt_front", "belt front"),
            _surf("kilt", "kilt"),
            _surf("forearm_L", "left forearm"),
            _surf("forearm_R", "right forearm"),
            _surf("knee_L", "left knee"),
            _surf("knee_R", "right knee"),
            _surf("boot_L", "left boot"),
            _surf("boot_R", "right boot"),
            _surf("hand_L", "left hand"),
            _surf("hand_R", "right hand"),
            _surf("greave_L", "left shin"),
            _surf("greave_R", "right shin"),
            _surf("silhouette", "silhouette", "mesh"),
            _surf("proportions", "proportions", "mesh"),
            _surf("brushwork", "painterly surface", "style"),
        ],
        "joints": [
            _joint("armhole_L", "torso", "upper_arm_L"),
            _joint("armhole_R", "torso", "upper_arm_R"),
            _joint("boot_top_L", "boot_L", "greave_L"),
            _joint("boot_top_R", "boot_R", "greave_R"),
            _joint("wrist_L", "forearm_L", "hand_L"),
            _joint("wrist_R", "forearm_R", "hand_R"),
        ],
    },
    "prop": {
        "cameras": FLAT_RING,
        "surfaces": [
            _surf("blade", "blade"),
            _surf("crossguard", "crossguard"),
            _surf("boss", "boss and collar rings"),
            _surf("grip", "grip"),
            _surf("pommel", "pommel"),
            _surf("silhouette", "form and silhouette", "mesh"),
        ],
        "joints": [
            _joint("blade_guard", "blade", "crossguard"),
            _joint("grip_guard", "grip", "crossguard"),
            _joint("grip_pommel", "grip", "pommel"),
        ],
    },
    "ship": {
        "cameras": FLAT_RING,
        "surfaces": [
            _surf("figurehead", "figurehead"),
            _surf("hull", "hull"),
            _surf("strake", "strake / wale"),
            _surf("deck", "deck"),
            _surf("bulwark", "bulwark"),
            _surf("sail", "sail"),
            _surf("mast", "mast"),
            _surf("rigging", "rigging"),
            _surf("stern", "stern"),
            _surf("gunport", "gun port"),
            _surf("cannon", "cannon"),
            _surf("railing", "railing"),
            _surf("silhouette", "silhouette", "mesh"),
        ],
        "joints": [
            _joint("hull_figurehead", "hull", "figurehead"),
            _joint("hull_deck", "hull", "deck"),
            _joint("hull_strake", "hull", "strake"),
            _joint("mast_sail", "mast", "sail"),
            _joint("hull_stern", "hull", "stern"),
        ],
    },
    "beast": {
        "cameras": FLAT_RING,
        "surfaces": [
            _surf("hide", "hide"),
            _surf("ventral", "ventral plates"),
            _surf("wing_membrane", "wing membrane"),
            _surf("wing_arm", "wing arm / finger strut"),
            _surf("horn", "horn"),
            _surf("crown", "crown / frill"),
            _surf("spine", "dorsal / tail spine"),
            _surf("claw", "claw"),
            _surf("eye", "eye"),
            _surf("tongue", "tongue"),
            _surf("fang", "fang / tooth"),
            _surf("mouth", "mouth interior"),
            _surf("silhouette", "silhouette", "mesh"),
        ],
        "joints": [
            _joint("hide_ventral", "hide", "ventral"),
            _joint("wing_arm_membrane", "wing_arm", "wing_membrane"),
            _joint("mouth_fang", "mouth", "fang"),
        ],
    },
    "layer": {
        "cameras": (),
        "surfaces": [
            _surf("waterline", "waterline coat"),
        ],
        "joints": [],
    },
    "logo": {
        "cameras": (),
        "surfaces": [
            _surf("mark", "mark"),
            _surf("field", "field"),
        ],
        "joints": [],
    },
}
# weapon is the N17 name for the same walked prop set.
KINDS["weapon"] = KINDS["prop"]


def kind_template(kind):
    if not kind or str(kind).strip() not in KINDS:
        _andon("unknown kind %r (known: %s)"
               % (kind, ", ".join(k for k in KINDS if k != "weapon")))
    return KINDS[str(kind).strip()]


def _structural_occupant(spec):
    role = spec.get("role", "prompt")
    if role in ("mesh", "style"):
        return {
            "id": "%s_%s" % (role, spec["id"]),
            "phrase": None,
            "provenance": role,
        }
    return None


def _empty_scope_slots(cameras):
    views = {}
    for vid, stem in cameras:
        views[vid] = {"surfaces": [], "status": "open", "stem": stem}
    return {"views": views, "strokes": {}}


def _empty_regions(cameras, surface_ids, view_map):
    views = {}
    for vid, _stem in cameras:
        views[vid] = [
            {"surface": sid, "box": None, "status": "open",
             "from": "kind template"}
            for sid in surface_ids
        ]
    return {
        "label": "PROPOSALS. Not a ruling.",
        "frame": {"W": None, "H": None},
        "box": "[x0, y0, x1, y1] half-open. crop is src[y0:y1, x0:x1].",
        "view_map": dict(view_map),
        "views": views,
    }


def _inventory_from_identity(identity_path):
    if not identity_path:
        return []
    if not os.path.isfile(identity_path):
        _andon("no identity %s" % identity_path)
    text = open(identity_path, encoding="utf-8").read()
    named = C.parse_named_table(text)
    if not named:
        _andon("no NAMED rows in %s" % identity_path)
    return [{"id": nid, "phrase": phrase, "assigned": None}
            for nid, phrase in named]


def emit(kind, subject=None, identity_path=None):
    """Kind template + optional IDENTITY inventory. Occupants stay empty."""
    tmpl = kind_template(kind)
    surfaces = []
    for spec in tmpl["surfaces"]:
        surfaces.append({
            "id": spec["id"],
            "name": spec["name"],
            "occupant": _structural_occupant(spec),
            "status": "open",
        })
    ids = [s["id"] for s in surfaces]
    joints = []
    for j in tmpl["joints"]:
        rec = dict(j)
        rec["status"] = "confirm"
        joints.append(rec)
    cameras = tmpl["cameras"]
    view_map = {vid: stem for vid, stem in cameras}
    ws = {
        "type": WS_TYPE,
        "schema": WORKSHEET_SCHEMA,
        "tool": "canon_worksheet.py",
        "tool_version": TOOL_VERSION,
        "subject": subject,
        "kind": "prop" if kind == "weapon" else kind,
        "source_identity": (
            os.path.relpath(identity_path, _REPO).replace("\\", "/")
            if identity_path else None),
        "surfaces": surfaces,
        "joints": joints,
        "inventory": _inventory_from_identity(identity_path),
        "blocked_additions": [],
        "legal_clauses": [],
        "scopes": _empty_scope_slots(cameras),
        "regions": _empty_regions(cameras, ids, view_map),
    }
    return ws


def load_worksheet(path):
    if not os.path.isfile(path):
        _andon("no worksheet %s" % path)
    doc = json.load(open(path, encoding="utf-8"))
    if not isinstance(doc, dict) or doc.get("type") != WS_TYPE:
        _andon("not a worksheet (type=%r)" % (
            doc.get("type") if isinstance(doc, dict) else type(doc).__name__))
    if "surfaces" not in doc or not isinstance(doc["surfaces"], list):
        _andon("worksheet needs a surfaces list")
    return doc


def from_surfaces(doc, identity_path=None):
    """Re-emit a worksheet showing what is still open.

    Occupants already on the surfaces file are copied, not invented.
    Kind camera slots that the file does not declare stay status=open.
    """
    if not isinstance(doc, dict) or "surfaces" not in doc:
        _andon("from_surfaces needs a surfaces document")
    kind = doc.get("kind") or "prop"
    tmpl = kind_template(kind)
    cameras = tmpl["cameras"]
    view_map = {vid: stem for vid, stem in cameras}
    surfaces = []
    for s in doc["surfaces"]:
        occ = s.get("occupant")
        filled = bool(occ and (occ.get("phrase") or occ.get("kind") == "bare"
                               or occ.get("provenance") in ("mesh", "style")))
        surfaces.append({
            "id": s["id"],
            "name": s.get("name", s["id"]),
            "occupant": copy.deepcopy(occ),
            "status": "filled" if filled else "open",
        })
    ids = [s["id"] for s in surfaces]
    joints = []
    for j in doc.get("joints") or []:
        rec = copy.deepcopy(j)
        rec["status"] = "filled" if rec.get("phrase") else "confirm"
        joints.append(rec)
    inventory = _inventory_from_identity(identity_path) if identity_path else []
    placed = {}
    for s in surfaces:
        occ = s.get("occupant") or {}
        ph = occ.get("phrase")
        if ph:
            placed[str(ph).strip().lower()] = s["id"]
    if not inventory:
        for s in surfaces:
            occ = s.get("occupant") or {}
            if occ.get("id") and occ.get("phrase"):
                inventory.append({
                    "id": occ["id"],
                    "phrase": occ["phrase"],
                    "assigned": s["id"],
                })
        for b in doc.get("blocked_additions") or []:
            if b.get("id") and b.get("phrase"):
                inventory.append({
                    "id": b["id"],
                    "phrase": b["phrase"],
                    "assigned": "blocked:%s" % b.get("onto", ""),
                })
    else:
        for item in inventory:
            sid = placed.get(item["phrase"].strip().lower())
            if sid:
                item["assigned"] = sid
    existing = (doc.get("scopes") or {}).get("views") or {}
    scopes = _empty_scope_slots(cameras)
    for vid, rec in existing.items():
        surfs = list(rec.get("surfaces") or [])
        scopes["views"][str(vid)] = {
            "surfaces": surfs,
            "status": "filled" if surfs else "open",
            "stem": view_map.get(str(vid)),
        }
    strokes = (doc.get("scopes") or {}).get("strokes") or {}
    scopes["strokes"] = copy.deepcopy(strokes)
    ws = {
        "type": WS_TYPE,
        "schema": WORKSHEET_SCHEMA,
        "tool": "canon_worksheet.py",
        "tool_version": TOOL_VERSION,
        "subject": doc.get("subject"),
        "kind": kind,
        "source_identity": doc.get("source_identity"),
        "surfaces": surfaces,
        "joints": joints,
        "inventory": inventory,
        "blocked_additions": copy.deepcopy(doc.get("blocked_additions") or []),
        "legal_clauses": copy.deepcopy(doc.get("legal_clauses") or []),
        "scopes": scopes,
        "regions": _empty_regions(cameras, ids, view_map),
    }
    return ws


def _copy_human_occupant(row):
    """Copy a human-authored occupant. Do not consult inventory."""
    occ = row.get("occupant")
    if occ is None:
        return None
    if not isinstance(occ, dict):
        _andon("surface %s occupant must be object or null" % row.get("id"))
    return copy.deepcopy(occ)


def to_surfaces(ws):
    """Worksheet -> schema-2 surfaces document the router will load.

    Copies human-authored occupants. Does not read inventory. Omits
    legal_clauses when empty so an unfilled worksheet cannot arm reverse.
    Writes a view scope only when the human listed surface ids.
    """
    if not isinstance(ws, dict) or ws.get("type") != WS_TYPE:
        _andon("to_surfaces needs a worksheet")
    kind = ws.get("kind") or "prop"
    surfaces = []
    ids = []
    for s in ws.get("surfaces") or []:
        if not isinstance(s, dict) or "id" not in s:
            _andon("worksheet surface needs id")
        if s["id"] in ids:
            _andon("duplicate surface id %s" % s["id"])
        ids.append(s["id"])
        rec = {"id": s["id"], "name": s.get("name", s["id"]),
               "occupant": _copy_human_occupant(s)}
        surfaces.append(rec)
    joints = []
    for j in ws.get("joints") or []:
        rec = {k: j[k] for k in ("id", "a", "b") if k in j}
        if j.get("phrase"):
            rec["phrase"] = j["phrase"]
        elif "phrase" in j:
            rec["phrase"] = j["phrase"]
        joints.append(rec)
    views = {}
    for name, rec in ((ws.get("scopes") or {}).get("views") or {}).items():
        if not isinstance(rec, dict):
            continue
        surfs = rec.get("surfaces") or []
        if surfs:
            views[str(name)] = {"surfaces": list(surfs)}
    strokes = {}
    for name, rec in ((ws.get("scopes") or {}).get("strokes") or {}).items():
        if not isinstance(rec, dict):
            continue
        surfs = rec.get("surfaces") or []
        if surfs:
            strokes[str(name)] = {"surfaces": list(surfs)}
    out = {
        "subject": ws.get("subject"),
        "kind": kind,
        "schema": C.SCHEMA_MAX,
        "source_identity": ws.get("source_identity"),
        "surfaces": surfaces,
        "blocked_additions": copy.deepcopy(ws.get("blocked_additions") or []),
        "joints": joints,
        "scopes": {"views": views, "strokes": strokes},
    }
    clauses = ws.get("legal_clauses") or []
    if clauses:
        out["legal_clauses"] = copy.deepcopy(clauses)
    return out


def bind_regions(ws, regions_doc):
    """Copy boxes whose name equals a surface id. Report the rest.

    Does not rename. Does not invent a box. Does not touch occupants.
    """
    if not isinstance(ws, dict) or ws.get("type") != WS_TYPE:
        _andon("bind needs a worksheet")
    if not isinstance(regions_doc, dict):
        _andon("regions must be an object")
    ids = {s["id"] for s in ws.get("surfaces") or []}
    incoming = regions_doc.get("views") or {}
    frame = regions_doc.get("frame")
    if frame and isinstance(frame, dict):
        ws.setdefault("regions", {}).setdefault("frame", {})
        if frame.get("W") is not None:
            ws["regions"]["frame"]["W"] = frame["W"]
        if frame.get("H") is not None:
            ws["regions"]["frame"]["H"] = frame["H"]
    vmap = regions_doc.get("view_map")
    if vmap:
        ws.setdefault("regions", {}).setdefault("view_map", {}).update(vmap)
    unmatched = []
    bound = 0
    dest_views = (ws.get("regions") or {}).get("views") or {}
    for vid, entries in incoming.items():
        if not isinstance(entries, list):
            continue
        dest = dest_views.get(str(vid))
        if dest is None:
            dest = []
            dest_views[str(vid)] = dest
            ws.setdefault("regions", {}).setdefault("views", dest_views)
        by_sid = {row.get("surface"): row for row in dest}
        for ent in entries:
            if not isinstance(ent, dict):
                continue
            name = ent.get("name") or ent.get("surface")
            box = ent.get("box")
            if name not in ids:
                unmatched.append({"view": str(vid), "name": name})
                continue
            row = by_sid.get(name)
            if row is None:
                row = {"surface": name, "box": None, "status": "open",
                       "from": "bind"}
                dest.append(row)
                by_sid[name] = row
            row["box"] = copy.deepcopy(box)
            row["status"] = "proposal"
            if ent.get("from"):
                row["from"] = ent["from"]
            bound += 1
    return {"bound": bound, "unmatched": unmatched}


def _unique_element_phrases(doc):
    """Distinct occupant (prompt, non-empty) + blocked phrases, first-seen order."""
    seen = set()
    out = []
    for s in doc.get("surfaces") or []:
        occ = s.get("occupant") or {}
        ph = occ.get("phrase")
        if not ph or not str(ph).strip():
            continue
        if occ.get("provenance") and occ.get("provenance") != "prompt":
            continue
        key = str(ph).strip()
        low = key.lower()
        if low in seen:
            continue
        seen.add(low)
        out.append(key)
    for b in doc.get("blocked_additions") or []:
        ph = b.get("phrase")
        if not ph or not str(ph).strip():
            continue
        key = str(ph).strip()
        low = key.lower()
        if low in seen:
            continue
        seen.add(low)
        out.append(key)
    return out


def load_tokenizer():
    """Return (name, encode) or (None, None). Never estimates.

    tiktoken cl100k_base is a real tokenizer and a different vocabulary
    from Qwen. The readout names it. A missing tokenizer is tokens=null,
    not a character/4 guess (F9).
    """
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return "tiktoken-cl100k_base", enc.encode
    except Exception:
        pass
    return None, None


def token_count(text, encode=None, tokenizer_name=None):
    """Tokenize `text`. encode is injected by tests so we never guess."""
    name = tokenizer_name
    fn = encode
    if fn is None:
        name, fn = load_tokenizer()
    if fn is None:
        return None, None
    return int(len(fn(text))), name


def _surfaces_for_density(obj):
    if obj.get("type") == WS_TYPE:
        return to_surfaces(obj)
    return obj


def density(obj, encode=None, tokenizer_name=None):
    """Authoring-time budget. Three counts, plus tokens if we can tokenize."""
    doc = _surfaces_for_density(obj)
    # load_canon validates; a just-emitted all-hole doc is valid schema 2.
    tmp = None
    try:
        cov = C.coverage(doc)
    except C.Andon:
        # no prompt-relevant surfaces (logo/layer edge). Report zeros.
        cov = {
            "subject": doc.get("subject"),
            "prompt_surfaces": 0,
            "named": 0,
            "holes": 0,
            "coverage": 0.0,
        }
    req = C.required_phrases(doc)
    unique = _unique_element_phrases(doc)
    joined = ", ".join(unique)
    ntok, tok_name = token_count(joined, encode=encode,
                                 tokenizer_name=tokenizer_name)
    inventory = []
    if obj.get("type") == WS_TYPE:
        inventory = obj.get("inventory") or []
    unassigned = [i for i in inventory if not i.get("assigned")]
    return {
        "subject": doc.get("subject"),
        "kind": doc.get("kind"),
        "prompt_surfaces": cov["prompt_surfaces"],
        "named": cov.get("named", 0),
        "holes": cov.get("holes", 0),
        "required_checks": len(req),
        "unique_elements": len(unique),
        "inventory": len(inventory),
        "inventory_unassigned": len(unassigned),
        "tokens": ntok,
        "tokenizer": tok_name,
        "token_text_chars": len(joined),
        "notes": [F1_NOTE, F8_NOTE],
    }


def format_density(d):
    tok = ("tokens %s (%s)" % (d["tokens"], d["tokenizer"])
           if d["tokens"] is not None
           else "tokens null (no tokenizer; not estimated)")
    return (
        "canon_worksheet %s  density  %s  kind %s\n"
        "  prompt_surfaces %d  named %d  holes %d\n"
        "  required_checks %d  unique_elements %d\n"
        "  inventory %d (%d unassigned)  %s\n"
        "  %s\n"
        "  %s\n"
        % (TOOL_VERSION, d.get("subject") or "-", d.get("kind") or "-",
           d["prompt_surfaces"], d["named"], d["holes"],
           d["required_checks"], d["unique_elements"],
           d["inventory"], d["inventory_unassigned"], tok,
           d["notes"][0], d["notes"][1])
    )


def dump(obj, path=None):
    text = json.dumps(obj, indent=2, ensure_ascii=True) + "\n"
    if path:
        parent = os.path.dirname(os.path.abspath(path))
        if parent and not os.path.isdir(parent):
            _andon("no directory %s" % parent)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        return path
    sys.stdout.write(text)
    return None


def occupant_phrases(obj):
    """Non-empty occupant phrases. Used by the chip and the poison test."""
    rows = obj.get("surfaces") or []
    out = []
    for s in rows:
        occ = s.get("occupant") or {}
        ph = occ.get("phrase")
        if ph and str(ph).strip():
            out.append(str(ph).strip())
    return out


def _selftest(scratch):
    ident = os.path.join(_REPO, "canon", "W3-IDENTITY.md")
    ws = emit("humanoid", subject="W3", identity_path=ident)
    if any(occupant_phrases(ws)):
        _andon("emit filled an occupant phrase: %s" % occupant_phrases(ws))
    if len(ws["inventory"]) != 19:
        _andon("W3 inventory is %d, not 19" % len(ws["inventory"]))
    if any(i.get("assigned") for i in ws["inventory"]):
        _andon("emit assigned an inventory row")
    ids = {s["id"] for s in ws["surfaces"]}
    if "grip" in ids:
        _andon("humanoid template included a weapon grip")
    if "torso" not in ids or "upper_arm_L" not in ids:
        _andon("humanoid template missing a body row")
    prop = emit("prop")
    pids = {s["id"] for s in prop["surfaces"]}
    if "grip" not in pids:
        _andon("prop template has no grip row")
    if occupant_phrases(prop):
        _andon("prop emit filled an occupant")
    # poison: assigned hint must not write the phrase
    poison = "POISON PHRASE GOLD NECKLACE"
    ws["inventory"].append(
        {"id": "X9", "phrase": poison, "assigned": "torso"})
    doc = to_surfaces(ws)
    blob = json.dumps(doc)
    if poison in blob:
        _andon("to_surfaces wrote an inventory phrase onto the surfaces file")
    if "legal_clauses" in doc:
        _andon("empty legal_clauses were emitted and would arm reverse")
    if doc["scopes"]["views"]:
        _andon("empty view slots were written into scopes.views")
    loaded = C.load_canon(
        _write_tmp(scratch, "from_emit.surfaces.json", doc))
    cov = C.coverage(loaded)
    if cov["named"] != 0:
        _andon("emit->to_surfaces named %d, not 0" % cov["named"])
    # W3 density: 24 / 25 / 19
    w3_path = os.path.join(_REPO, "canon", "w3.surfaces.json")
    w3 = C.load_canon(w3_path)
    fake = lambda s: ["t"] * 7
    dens = density(w3, encode=fake, tokenizer_name="injected")
    if dens["prompt_surfaces"] != 24:
        _andon("W3 prompt_surfaces %d, not 24" % dens["prompt_surfaces"])
    if dens["required_checks"] != 25:
        _andon("W3 required_checks %d, not 25" % dens["required_checks"])
    if dens["unique_elements"] != 19:
        _andon("W3 unique_elements %d, not 19" % dens["unique_elements"])
    if dens["tokens"] != 7:
        _andon("injected tokenizer was not used (tokens=%r)" % dens["tokens"])
    if dens["tokens"] == dens["token_text_chars"] // 4:
        _andon("density used a char/4 estimate")
    # round-trip copies W3 occupants, does not invent
    back = from_surfaces(w3, identity_path=ident)
    if len(occupant_phrases(back)) < 16:
        _andon("from_surfaces dropped W3 occupant phrases")
    rt = to_surfaces(back)
    by_id = {s["id"]: (s.get("occupant") or {}).get("phrase")
             for s in rt["surfaces"]}
    src = {s["id"]: (s.get("occupant") or {}).get("phrase")
           for s in w3["surfaces"]}
    if by_id != src:
        _andon("round-trip moved an occupant phrase")
    return dens


def _write_tmp(scratch, name, obj):
    path = os.path.join(scratch, name)
    dump(obj, path)
    return path


def selftest(scratch=None):
    if scratch is None:
        scratch = tempfile.mkdtemp(prefix="canon_ws_")
    return _selftest(scratch)


def build_parser():
    p = argparse.ArgumentParser(
        description="Canon worksheet: kind templates, empty occupants, density.")
    p.add_argument("--selftest", action="store_true")
    sub = p.add_subparsers(dest="cmd")
    e = sub.add_parser("emit", help="kind template + optional IDENTITY inventory")
    e.add_argument("--kind", required=True)
    e.add_argument("--subject", default=None)
    e.add_argument("--identity", default=None)
    e.add_argument("--out", default=None)
    f = sub.add_parser("from-surfaces", help="re-emit a worksheet from a surfaces file")
    f.add_argument("--canon", required=True)
    f.add_argument("--identity", default=None)
    f.add_argument("--out", default=None)
    t = sub.add_parser("to-surfaces", help="worksheet -> schema-2 surfaces file")
    t.add_argument("--worksheet", required=True)
    t.add_argument("--out", required=True)
    r = sub.add_parser("readout", help="element-count + token density")
    r.add_argument("--canon", default=None)
    r.add_argument("--worksheet", default=None)
    b = sub.add_parser("bind", help="copy boxes whose name equals a surface id")
    b.add_argument("--worksheet", required=True)
    b.add_argument("--regions", required=True)
    b.add_argument("--out", default=None)
    sub.add_parser("kinds", help="list kind templates")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.selftest:
            selftest()
            sys.stdout.write(
                "calibration emit-humanoid+W3 occupants empty  "
                "inventory 19 unassigned  poison held  "
                "W3 density 24/25/19  injected tokenizer used\n")
            return 0
        if not args.cmd:
            _andon("need a subcommand or --selftest")
        if args.cmd == "kinds":
            for name, tmpl in KINDS.items():
                if name == "weapon":
                    continue
                n_prompt = sum(1 for s in tmpl["surfaces"]
                               if s.get("role", "prompt") == "prompt")
                sys.stdout.write(
                    "%-10s surfaces %d (prompt %d) joints %d cameras %d\n"
                    % (name, len(tmpl["surfaces"]), n_prompt,
                       len(tmpl["joints"]), len(tmpl["cameras"])))
            return 0
        if args.cmd == "emit":
            ident = args.identity
            if ident and not os.path.isabs(ident):
                ident = os.path.join(_REPO, ident.replace("/", os.sep))
            ws = emit(args.kind, subject=args.subject, identity_path=ident)
            dump(ws, args.out)
            return 0
        if args.cmd == "from-surfaces":
            path = C.resolve_canon(args.canon)
            doc = C.load_canon(path)
            ident = args.identity
            if ident and not os.path.isabs(ident):
                ident = os.path.join(_REPO, ident.replace("/", os.sep))
            ws = from_surfaces(doc, identity_path=ident)
            dump(ws, args.out)
            return 0
        if args.cmd == "to-surfaces":
            ws = load_worksheet(args.worksheet)
            doc = to_surfaces(ws)
            # validate before write
            tmp = args.out + ".tmp-validate"
            dump(doc, tmp)
            try:
                C.load_canon(tmp)
            finally:
                if os.path.isfile(tmp):
                    os.remove(tmp)
            dump(doc, args.out)
            return 0
        if args.cmd == "readout":
            if args.canon:
                path = C.resolve_canon(args.canon)
                obj = C.load_canon(path)
            elif args.worksheet:
                obj = load_worksheet(args.worksheet)
            else:
                _andon("need --canon or --worksheet")
            sys.stdout.write(format_density(density(obj)))
            return 0
        if args.cmd == "bind":
            ws = load_worksheet(args.worksheet)
            regs = json.load(open(args.regions, encoding="utf-8"))
            result = bind_regions(ws, regs)
            dest = args.out or args.worksheet
            dump(ws, dest)
            sys.stdout.write(
                "bound %d  unmatched %d\n"
                % (result["bound"], len(result["unmatched"])))
            for u in result["unmatched"]:
                sys.stdout.write("  unmatched view %s name %s\n"
                                 % (u["view"], u["name"]))
            return 0
        _andon("unknown command %s" % args.cmd)
    except Andon as e:
        sys.stderr.write(str(e) + "\n")
        return 2
    except C.Andon as e:
        sys.stderr.write(str(e) + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
