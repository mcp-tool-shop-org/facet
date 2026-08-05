"""E04 Ruling 25 - the sweep. Is every SUBJECT-DATA flag on this subject's route decided?

WHY THIS EXISTS AND WHY IT IS NOT --coverage. `e04_profile_check --coverage` diffs a
subject profile against `character.json`'s per-tool keys, and Ruling 25 corrected what that
reference is: character.json is the registry of flags *the character needed to write down*,
not the registry of flags that matter. A flag whose character value equals the tool's own
default was never written there, so an absent key cannot be reported as absent. Measured at
two sites, one of them live:

  * a whole tool with no block in the reference (texpass_finalize, bake_hero_pack - the next
    two steps of the route as of this writing);
  * a key at the character's own default (texpass_iter's aspect/fit-axis, which let a
    LANDSCAPE subject reach the stroke stage carrying a portrait frame and clipped four of
    six ruled stroke cameras).

So the reference here is Task 2's CLASSIFICATION TABLE instead
(docs/experiments/E04-profile-extraction.md), applied with its own stated rule:

  > A value goes in the profile unless there is a stated reason it is subject-independent.
  > The burden of proof is on "principle".

Implemented exactly that way round. Every flag of every route-active tool is subject data
UNLESS it is named CODE in the table's section 6, or it is N/A (a required path, a
store_true, or default=None). CODE_ROWS below is a transcription of section 6, tool by tool,
and every entry carries the table's own reason - so a flag nobody classified shows up as
subject data and demands a decision, which is the direction that fails safe.

A decision is any of Ruling 22's four forms: a value, a vacuous suspension (a value the tool
receives that cannot fire), `_not_on_route`, or `_NOT_CLEARED`.

  e04_registry_sweep.py --profile profiles/ship.json --tools tools

Standards compliance: DECOMPOSE_BY_SECRETS - this is that standard's registry, rebuilt on a
reference that does not inherit another subject's silences. ANDON_AUTHORITY - exits non-zero
on any undecided subject-data flag. EXTERNAL_VERIFIER - the flag list comes from the tools'
own argparse source, which neither this file nor the profile controls.
"""
import argparse
import ast
import json
import os
import re
import sys

# The ship's route, in order. E06's recipe (prep, project, loop, finalize, pack) plus the
# render/mask/generation tools that feed it. Tools this subject puts off-route are still
# listed - the profile has to SAY they are off-route, which is itself a decision.
ROUTE = ["verify/turn_render.py", "silhouette_masks.py", "restylize_views.py",
         "bake_hero_prep.py", "cull_unseen.py", "project_twins.py", "texpass_iter.py",
         "texpass_brush.py", "brush_cloud_step.py", "texpass_finalize.py",
         "bake_hero_pack.py", "smart_decimate.py", "verify/head_render.py",
         "verify/mesh_stats.py"]

# Section 6 of the classification table, transcribed tool by tool with its reasons. A flag
# is CODE only if it is here; everything else carries the burden the table put on it.
CODE_ROWS = {
    "cull_unseen.py": {
        "bias": "ray-offset epsilon in a normalised frame - numerical, not geometric",
        "noffs": "ray-offset epsilon in a normalised frame",
        "cameras": "visibility SUPERSET construction",
        "rings": "visibility superset construction",
        "samples": "visibility superset construction",
        "raster-res": "classifier grid",
        "iou-res": "deliberately different from raster-res so the gate samples a different "
                   "grid than the classifier - equal values would make it a tautology",
        "iou-cameras": "the gate's own camera count",
        "max-recession": "gate bound",
        "max-missed-area": "gate bound"},
    "project_twins.py": {
        "bias": "ray-offset epsilon", "noffs": "ray-offset epsilon",
        "edge-frac": "A3's invariant - erosion may never exceed a third of a structure's "
                     "own local half-width. A derived law, not a tuned number",
        "hole-grey": "design collision with emit's background fill, recorded and unchanged"},
    "texpass_iter.py": {"bias": "ray-offset epsilon", "noffs": "ray-offset epsilon"},
    "texpass_finalize.py": {
        "max-edge-median": "stated in MEDIAN TRIANGLE EDGES, measured from this mesh at run "
                           "time - the unit normalises the subject away",
        "beyond-edges": "stated in median triangle edges, per-mesh",
        "max-frac-beyond": "stated against a per-mesh edge unit"},
    "bake_hero_prep.py": {
        "island-margin": "a function of atlas resolution and chart size, not of the "
                         "subject. WARNING in the table: re-measure if chart statistics "
                         "differ materially",
        "pack-margin": "same arithmetic, same warning",
        "angle-limit": "off-route (only under --reunwrap) and independently falsified",
        "bound": "the std-frame half-extent CONVENTION five tools share"},
    "smart_decimate.py": {"weld-dist": "merge-by-distance epsilon - physics of the "
                                       "seam-split export",
                          "bound": "the shared std-frame convention"},
    "restylize_views.py": {
        "tol": "kept in code as a KNOWN DEFECT, not a principle - making it a profile value "
               "would let each subject tune around a broken mechanism. Belongs to the blade arm",
        "erode": "same row"},
    "verify/turn_render.py": {
        "exposure": "matched to the reference renders these must line up with",
        "bg": "derived by e08_bg_derive.py rather than chosen",
        "scale": "instrument label / sampling density"},
    "brush_cloud_step.py": {
        "tol": "ANDON bound in 8-bit levels - sub-unit is a codec boundary",
        "conc-tol": "ANDON bound in 8-bit levels", "dilate": "ANDON operand"},
    "verify/head_render.py": {}, "verify/mesh_stats.py": {"grid": "sampling density",
                                                          "curv-samples": "sampling density"},
    "bake_hero_pack.py": {},
    # section 6's catch-all row - "`host`, `model` paths, `tag`, `yaw-offset 0.0`, `scale`,
    # `grid 256`, `curv-samples 4000`, `views 4,5,6` | various | Endpoints, filename labels
    # and instrument sampling density. Not behaviour". Only `host` is transcribed from that
    # row, scoped to the two tools that have one: `views` there means mesh_stats' INSTRUMENT
    # views, and marking `views` CODE globally would classify the camera set - which section
    # 4 lists as PROFILE - as a principle. `tag`, `yaw-offset` and `scale` are left as
    # subject data even though the row names them, because ship.json already decides two of
    # them and over-inclusion costs one decision where under-inclusion costs a silent
    # inheritance.
    "_catch_all_host": {},
}
for _t in ("restylize_views.py", "texpass_brush.py"):
    CODE_ROWS.setdefault(_t, {})["host"] = (
        "section 6 catch-all: an endpoint, not behaviour. Note that on "
                             "this subject generation is cloud-only, so neither tool's local "
                             "posting path runs at all")
CODE_ROWS.pop("_catch_all_host")

ap = argparse.ArgumentParser()
ap.add_argument("--profile", required=True)
ap.add_argument("--tools", default="tools")
args = ap.parse_args()
prof = json.load(open(args.profile, encoding="utf-8"))
tools_skip = prof.get("_tools_not_on_route", {})


def defaults_of(path):
    """{flag: default-source-text or None} - the same brace-matching walker
    e04_profile_check.py uses, so both instruments read the source the same way."""
    src = open(path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"\b\w+\.add_argument\(", src):
        i = m.end() - 1
        d = 0
        while i < len(src):
            if src[i] == "(":
                d += 1
            elif src[i] == ")":
                d -= 1
                if d == 0:
                    break
            i += 1
        blob = src[m.start():i + 1]
        nm = re.search(r'"(--[A-Za-z0-9\-_]+)"', blob)
        if not nm:
            continue
        key = nm.group(1)[2:]
        # The table's N/A column is "required paths, store_true flags, default=None" - things
        # that are not constants. Two more argparse forms belong to it by the same reasoning
        # and were missing from the first version of this walker: an `append` action's
        # default is an empty collection and can never be a profile value (set_defaults would
        # pre-load every invocation with it), and BooleanOptionalAction is a switch exactly
        # as store_true is. Recorded as completing the table's own definition rather than
        # widening it - neither adds a category, and the two flags this reaches
        # (silhouette_masks --anchor, project_twins --view) are repeatable INPUT paths.
        if "store_true" in blob or "store_false" in blob:
            out[key] = ("NA", "store_true/false - a switch, not a constant")
            continue
        if 'action="append"' in blob or "action='append'" in blob:
            out[key] = ("NA", "action=append - a repeatable input, default is an empty list")
            continue
        if "BooleanOptionalAction" in blob:
            out[key] = ("NA", "BooleanOptionalAction - a switch, as store_true is")
            continue
        j = blob.find("default=")
        if j < 0:
            out[key] = ("NA", "no default= - a required argument, normally a path")
            continue
        k = j + len("default=")
        depth, quote = 0, None
        while k < len(blob):
            c = blob[k]
            if quote:
                if c == "\\":
                    k += 2
                    continue
                if c == quote:
                    quote = None
            elif c in "\"'":
                quote = c
            elif c in "([{":
                depth += 1
            elif c in ")]}":
                if depth == 0:
                    break
                depth -= 1
            elif c == "," and depth == 0:
                break
            k += 1
        raw = blob[j + len("default="):k].strip()
        if raw == "None":
            out[key] = ("NA", "default=None - a placeholder, normally a path")
            continue
        try:
            out[key] = ("VAL", ast.literal_eval(raw))
        except Exception:
            out[key] = ("VAL", raw)
    return out


rows, undecided, na, code_n = [], [], 0, 0
for tool in ROUTE:
    path = os.path.join(args.tools, tool)
    if not os.path.exists(path):
        print("[sweep] ANDON: %s not found at %s" % (tool, path))
        sys.exit(2)
    blk = prof["tools"].get(tool)
    whole_off = tool in tools_skip
    skip = (blk or {}).get("_not_on_route", {})
    not_cleared = "_NOT_CLEARED" in (blk or {})
    for key, (kind, info) in sorted(defaults_of(path).items()):
        if kind == "NA":
            na += 1
            continue
        if key in CODE_ROWS.get(tool, {}):
            code_n += 1
            continue
        # subject data by the table's own burden-of-proof direction
        if whole_off:
            decided, how = True, "_tools_not_on_route"
        elif not_cleared:
            decided, how = True, "_NOT_CLEARED"
        elif blk and key in blk:
            decided, how = True, "value"
        elif key in skip:
            decided, how = True, "_not_on_route"
        else:
            decided, how = False, None
        rows.append((tool, key, info, decided, how))
        if not decided:
            undecided.append((tool, key, info))

by_how = {}
for _, _, _, d, how in rows:
    if d:
        by_how[how] = by_how.get(how, 0) + 1
print("[sweep] %d route-active tools; %d flags are CODE by the table's section 6; %d are N/A "
      "(paths/switches)" % (len(ROUTE), code_n, na))
print("[sweep] %d SUBJECT-DATA flags on this route; decided %d  (%s)"
      % (len(rows), len(rows) - len(undecided),
         ", ".join("%s %d" % (k, v) for k, v in sorted(by_how.items()))))
if undecided:
    print("[sweep] %d UNDECIDED - each of these runs this subject on the tool's own default, "
          "which on this route is the character's measurement:" % len(undecided))
    for t, k, info in undecided:
        print("[sweep]   %-24s %-18s tool default %r" % (t, k, info))
    sys.exit(1)
print("[sweep] every subject-data flag on this route carries an explicit decision.")
