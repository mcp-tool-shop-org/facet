# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Canon binding. A surface id is a word until it owns a face set.

WHY THIS EXISTS. Consult #22 / build #22. An Opus seat halted at its
first gate: the asset the Director accepted and the asset he called
defective on the wrong-material class are the same file. Per-asset
labels collapse. Per-surface labels need a pixel (or a face) that
is that surface. scopes.views is empty. The router knows the
material for torso and nothing knows which pixels are torso.
Canon binds 0.00% of the figure.

THE UNIT IS THE FACE. Faces survive a re-bake; texels do not, and
this route re-bakes. The raycast already speaks faces (then
surfid). Atlas islands partition cheaply but 13,715 of them
against 21 occupants is a 650:1 authoring problem. Pixels are
derived at read time: face -> surface id AND visibility. They are
not stored.

AUTHORING. Colour cannot name a surface (one PBR, 13,715 islands,
palette blind to gold-against-leather). Boxes reach 7.95% and
three of five names do not resolve (skirt, tunic, boot_tops).
seed_boxes copies a box only when incoming name equals a surface
id. skirt stays unmatched. Faces stay empty. That is a proposal,
not a binding, and it is not ratified.

ONE PLACE OWNS NAMES. Surface ids live in the surfaces file.
This file references them. An unknown id ANDON's. A missing
surfaces row ANDON's. A face owned by two surfaces ANDON's.

SCOPES. propose_scopes never writes a ratified list. Empty faces
produce empty open slots. Filling lists is a human walk.

NOT THIS BUILD. The wrong-material check. Filling occupants.
Regeneration. Claiming DIRECTOR-VERIFIED on a box file.

CALIBRATION CLAIM (run --selftest; T97 pins the same numbers).
  emit(w3.surfaces) has one row per surface, every faces=[],
  bound 0. seed_boxes: grip and blade become proposals; skirt
  is unmatched; faces stay empty. A row named skirt ANDON's.

  python tools/canon_bind.py --selftest
"""
from __future__ import annotations

import argparse
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
BIND_SCHEMA = 1
BIND_TYPE = "binding"
BIND_UNIT = "face"


class Andon(ValueError):
    pass


def _andon(msg):
    raise Andon("ANDON: " + msg)


def binding_path(surfaces_path):
    if surfaces_path.endswith(".surfaces.json"):
        return surfaces_path[: -len(".surfaces.json")] + ".binding.json"
    return os.path.splitext(surfaces_path)[0] + ".binding.json"


def emit(surfaces_doc, source_rel=None):
    """One row per surface, faces empty. A hole is a row."""
    if not isinstance(surfaces_doc, dict) or "surfaces" not in surfaces_doc:
        _andon("emit needs a surfaces document")
    rows = []
    ids = []
    for s in surfaces_doc["surfaces"]:
        if "id" not in s:
            _andon("surface missing id")
        if s["id"] in ids:
            _andon("duplicate surface id %s" % s["id"])
        ids.append(s["id"])
        rows.append({
            "id": s["id"],
            "faces": [],
            "status": "open",
            "seeds": [],
            "ratified": False,
        })
    return {
        "type": BIND_TYPE,
        "schema": BIND_SCHEMA,
        "tool": "canon_bind.py",
        "tool_version": TOOL_VERSION,
        "subject": surfaces_doc.get("subject"),
        "kind": surfaces_doc.get("kind"),
        "source_surfaces": source_rel,
        "unit": BIND_UNIT,
        "surfaces": rows,
    }


def load_binding(path, surfaces_doc=None):
    if not os.path.isfile(path):
        _andon("no binding %s" % path)
    doc = json.load(open(path, encoding="utf-8"))
    return validate(doc, surfaces_doc)


def validate(doc, surfaces_doc=None):
    if not isinstance(doc, dict) or doc.get("type") != BIND_TYPE:
        _andon("not a binding (type=%r)" % (
            doc.get("type") if isinstance(doc, dict) else type(doc).__name__))
    try:
        ver = int(doc.get("schema"))
    except (TypeError, ValueError):
        _andon("binding schema %r is not an int" % doc.get("schema"))
    if ver > BIND_SCHEMA:
        _andon("stale consumer: binding schema %d > %d" % (ver, BIND_SCHEMA))
    if doc.get("unit") != BIND_UNIT:
        _andon("binding unit %r is not %s" % (doc.get("unit"), BIND_UNIT))
    rows = doc.get("surfaces")
    if not isinstance(rows, list) or not rows:
        _andon("binding needs a surfaces list")
    ids = []
    owned = {}
    for s in rows:
        if not isinstance(s, dict) or "id" not in s:
            _andon("binding row needs id")
        if s["id"] in ids:
            _andon("duplicate binding id %s" % s["id"])
        ids.append(s["id"])
        faces = s.get("faces")
        if faces is None:
            _andon("surface %s missing faces (use [])" % s["id"])
        if not isinstance(faces, list):
            _andon("surface %s faces must be a list" % s["id"])
        for f in faces:
            try:
                fi = int(f)
            except (TypeError, ValueError):
                _andon("surface %s face %r is not an int" % (s["id"], f))
            if fi < 0:
                _andon("surface %s face %d is negative" % (s["id"], fi))
            if fi in owned:
                _andon("face %d owned by %s and %s"
                       % (fi, owned[fi], s["id"]))
            owned[fi] = s["id"]
        if s.get("ratified") and not faces:
            _andon("surface %s is ratified with no faces" % s["id"])
    if surfaces_doc is not None:
        want = [s["id"] for s in surfaces_doc.get("surfaces") or []]
        missing = [i for i in want if i not in ids]
        extra = [i for i in ids if i not in want]
        if missing or extra:
            _andon("binding ids drifted from surfaces: missing=%s extra=%s"
                   % (missing, extra))
    return doc


def coverage(doc):
    rows = doc.get("surfaces") or []
    n = len(rows)
    bound = [s for s in rows if s.get("faces")]
    proposed = [s for s in rows
                if s.get("status") == "proposal" and not s.get("faces")]
    open_rows = [s for s in rows if s.get("status") == "open"]
    n_faces = sum(len(s.get("faces") or []) for s in rows)
    return {
        "subject": doc.get("subject"),
        "surfaces": n,
        "bound": len(bound),
        "proposed": len(proposed),
        "open": len(open_rows),
        "bound_faces": n_faces,
        "figure_fraction": 0.0 if n_faces == 0 else None,
        "note": ("figure bind 0.00% — no face sets; scopes.views cannot "
                 "be derived" if n_faces == 0 else None),
    }


def format_coverage(cov):
    return (
        "canon_bind %s  %s  bound %d/%d  proposed %d  open %d  "
        "faces %d  figure %.2f%%\n"
        % (TOOL_VERSION, cov.get("subject") or "-",
           cov["bound"], cov["surfaces"], cov["proposed"], cov["open"],
           cov["bound_faces"],
           0.0 if cov["figure_fraction"] is None else 100.0 * cov["figure_fraction"])
    )


def seed_boxes(binding, regions_doc):
    """Copy boxes whose name equals a surface id. Report the rest.

    Does not invent faces. Does not rename. Does not ratify.
    """
    if not isinstance(regions_doc, dict):
        _andon("regions must be an object")
    by_id = {s["id"]: s for s in binding.get("surfaces") or []}
    unmatched = []
    bound = 0
    incoming = regions_doc.get("views") or {}
    for vid, entries in incoming.items():
        if not isinstance(entries, list):
            continue
        for ent in entries:
            if not isinstance(ent, dict):
                continue
            name = ent.get("name") or ent.get("surface")
            if name not in by_id:
                unmatched.append({"view": str(vid), "name": name})
                continue
            row = by_id[name]
            seed = {
                "kind": "box",
                "view": str(vid),
                "box": list(ent.get("box") or []),
                "from": ent.get("from") or "seed_boxes",
            }
            row.setdefault("seeds", []).append(seed)
            if not row.get("faces"):
                row["status"] = "proposal"
                row["ratified"] = False
            bound += 1
    return {"bound": bound, "unmatched": unmatched}


def propose_scopes(binding, cameras=None):
    """Empty open slots. Never ratified. Empty faces cannot name a view."""
    cams = cameras if cameras is not None else (
        "0", "1", "2", "3", "4", "5", "6", "7")
    views = {}
    for vid in cams:
        views[str(vid)] = {"surfaces": [], "status": "open"}
    return {"views": views, "strokes": {}}


def margin_holds(named_rates, control_rates, min_margin):
    """A gate pair a known-bad instrument cannot pass.

    Direction-only (named fires, control silent) is satisfied by any
    boundary detector, because named regions contain boundaries.
    Require min(named) - max(control) >= min_margin. Overlap fails.
    """
    if min_margin < 0:
        _andon("min_margin must be >= 0")
    if not named_rates or not control_rates:
        _andon("need named rates and control rates")
    named = [float(x) for x in named_rates]
    ctrl = [float(x) for x in control_rates]
    gap = min(named) - max(ctrl)
    return {
        "ok": gap >= float(min_margin),
        "gap": gap,
        "min_named": min(named),
        "max_control": max(ctrl),
        "min_margin": float(min_margin),
    }


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


def _selftest(scratch):
    w3_path = os.path.join(_REPO, "canon", "w3.surfaces.json")
    w3 = C.load_canon(w3_path)
    doc = emit(w3, source_rel="canon/w3.surfaces.json")
    n = len(w3["surfaces"])
    if len(doc["surfaces"]) != n:
        _andon("emit rows %d, surfaces %d" % (len(doc["surfaces"]), n))
    if any(s.get("faces") for s in doc["surfaces"]):
        _andon("emit invented a face set")
    cov = coverage(doc)
    if cov["bound"] != 0 or cov["figure_fraction"] != 0.0:
        _andon("empty emit is not 0.00: %s" % cov)
    regs = json.load(open(
        os.path.join(_REPO, "tools", "s3_sheet_regions.json"),
        encoding="utf-8"))
    result = seed_boxes(doc, regs)
    names = {u["name"] for u in result["unmatched"]}
    if "skirt" not in names or "tunic" not in names or "boot_tops" not in names:
        _andon("unresolved box names not reported: %s" % names)
    if "grip" in names or "blade" in names:
        _andon("exact-id boxes were unmatched: %s" % names)
    by_id = {s["id"]: s for s in doc["surfaces"]}
    if by_id["grip"]["status"] != "proposal" or by_id["grip"]["faces"]:
        _andon("grip seed wrote faces or did not propose")
    if by_id["grip"].get("ratified"):
        _andon("seed ratified a row")
    if by_id["torso"]["status"] != "open":
        _andon("torso should stay open")
    bad = dict(doc)
    bad["surfaces"] = list(doc["surfaces"]) + [
        {"id": "skirt", "faces": [], "status": "open",
         "seeds": [], "ratified": False}]
    try:
        validate(bad, w3)
        _andon("extra id skirt did not refuse")
    except Andon as e:
        if "extra" not in str(e):
            _andon("skirt refused for the wrong reason: %s" % e)
    m_bad = margin_holds([0.399, 0.0756], [0.3990, 0.0096], 0.10)
    if m_bad["ok"]:
        _andon("overlapping named/control passed the margin")
    m_ok = margin_holds([0.80, 0.90], [0.10, 0.05], 0.30)
    if not m_ok["ok"]:
        _andon("separated rates failed the margin")
    scopes = propose_scopes(doc)
    if any(v["surfaces"] for v in scopes["views"].values()):
        _andon("propose_scopes invented a view list")
    if any(v["status"] != "open" for v in scopes["views"].values()):
        _andon("propose_scopes ratified a view")
    return cov


def selftest(scratch=None):
    if scratch is None:
        scratch = tempfile.mkdtemp(prefix="canon_bind_")
    return _selftest(scratch)


def build_parser():
    p = argparse.ArgumentParser(
        description="Canon binding: surface id -> face set. Names stay on surfaces.")
    p.add_argument("--selftest", action="store_true")
    sub = p.add_subparsers(dest="cmd")
    e = sub.add_parser("emit", help="empty face rows from a surfaces file")
    e.add_argument("--canon", required=True)
    e.add_argument("--out", default=None)
    s = sub.add_parser("seed", help="copy boxes whose name equals a surface id")
    s.add_argument("--binding", required=True)
    s.add_argument("--regions", required=True)
    s.add_argument("--out", default=None)
    c = sub.add_parser("coverage", help="bound / proposed / open / 0.00 figure")
    c.add_argument("--binding", default=None)
    c.add_argument("--canon", default=None)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.selftest:
            selftest()
            sys.stdout.write(
                "calibration emit-W3 faces empty  bound 0  "
                "skirt unmatched  grip proposed  margin overlap refused\n")
            return 0
        if not args.cmd:
            _andon("need a subcommand or --selftest")
        if args.cmd == "emit":
            path = C.resolve_canon(args.canon)
            doc = C.load_canon(path)
            rel = os.path.relpath(path, _REPO).replace("\\", "/")
            out = emit(doc, source_rel=rel)
            dest = args.out or binding_path(path)
            dump(out, dest)
            sys.stdout.write(format_coverage(coverage(out)))
            return 0
        if args.cmd == "seed":
            surf = None
            raw = json.load(open(args.binding, encoding="utf-8"))
            src = raw.get("source_surfaces")
            if src:
                sp = os.path.join(_REPO, src.replace("/", os.sep))
                if os.path.isfile(sp):
                    surf = C.load_canon(sp)
            bind = validate(raw, surf)
            regs = json.load(open(args.regions, encoding="utf-8"))
            result = seed_boxes(bind, regs)
            dest = args.out or args.binding
            dump(bind, dest)
            sys.stdout.write(
                "bound %d  unmatched %d\n"
                % (result["bound"], len(result["unmatched"])))
            for u in result["unmatched"]:
                sys.stdout.write("  unmatched view %s name %s\n"
                                 % (u["view"], u["name"]))
            return 0
        if args.cmd == "coverage":
            if args.binding:
                bpath = args.binding
            elif args.canon:
                bpath = binding_path(C.resolve_canon(args.canon))
            else:
                _andon("need --binding or --canon")
            surf = None
            raw = json.load(open(bpath, encoding="utf-8"))
            src = raw.get("source_surfaces")
            if src:
                sp = os.path.join(_REPO, src.replace("/", os.sep))
                if os.path.isfile(sp):
                    surf = C.load_canon(sp)
            bind = validate(raw, surf)
            sys.stdout.write(format_coverage(coverage(bind)))
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
