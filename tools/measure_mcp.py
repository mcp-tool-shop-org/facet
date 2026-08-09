#!/usr/bin/env python
"""measure_mcp - the mesh/texture measurement MCP server (spec 2, E27).

WHAT THIS IS. A stdio MCP server that puts this repo's measurement instruments
in front of a session as job-shaped tools, so any mesh or textured asset is
measured by THE SAME CODE PATH that measured every subject in the record. The
contract is docs/specs/measurement-mcp-spec.md; placement in facet is
docs/specs/placement-memo.md (the Director's word, 2026-08-08). The instruments
live in tools/ and are invoked as subprocesses under the pinned interpreter -
THIS MODULE WRAPS; IT DOES NOT RE-IMPLEMENT (the E27 bar, gate 3). Where the
spec names a tool no in-scope instrument can serve, that tool REFUSES and names
the finding rather than growing a second implementation of a measurement the
record already cites.

THE SURFACE IS THE SPEC'S EIGHT NAMES, exactly. Seven wrap (the Director ruled
the e12_*/e14_* family IN, 2026-08-09 - spec open question 2; the three released
wraps landed at E28 task 2b, after the census halt was ruled):

  mesh_stats        tools/verify/mesh_stats.py
  mesh_topology     tools/diagnostics/e14_topology.py - ALONE, by E28 Ruling 4:
                    e12_nonmanifold.py computes the same count independently
                    but its output is a picture drawn onto a render set it
                    requires as input - evidence for the eye, the Director's
                    channel - so it is NAMED in the payload notes, never
                    wrapped. The tie crash E27 measured (wide = 3-thin-tall
                    with argmin == argmax on all-equal extents) was repaired at
                    E28 2a with its proof in T42.
  reach_ceiling     tools/diagnostics/e08_ceiling.py
  thin_extent_curve tools/diagnostics/e12_thin_curve.py - the per-view
                    screen-space extent curve. e13_thin_inputs.py remains NOT a
                    substitute (brush-level withholding, a different question).
                    The instrument's --preview flag is not exposed: previews
                    are artifacts for the eye, not payload numbers.
  offsurface_rate   tools/diagnostics/e12_offsurface.py - the BAKE half only.
                    The erode / margin-statistic half the spec asks for exists
                    in NEITHER offsurface instrument (measured at the E27
                    ruling seat; --margin here is the camera-framing margin, a
                    different quantity) - named in the payload notes, an open
                    commission, not computed here. e10_offsurface.py stays the
                    ship-bound sibling whose ruled numbers this instrument was
                    validated against (E12 task 2).
  texel_provenance  tools/diagnostics/texel_provenance.py
  measure_report    tools/verify/gate1_sheet.py (the sheet half) + the
                    payload-comparison half, which is this server's own
                    envelope contract, not a measurement

and ONE refuses, naming exactly what is missing and whose question it is:

  anchor_check      NO instrument exists. tools/diagnostics/e13_anchor_check
                    .py is a name collision - it is the spiral-law adjacency
                    guard, not the anchored-regression pattern. The pattern
                    lives in the harness's artifacts tier (T07-T11) and
                    session procedure. The census swept both instrument homes
                    (E28) and found no candidate; the commission stands.

INSTRUMENT IDENTITY IS THE CONTRACT (the spec's own law). Every successful
payload carries a `measure` envelope: this server's version, the wrapped
instrument's repo path AND ITS FILE sha256, the resolved parameters, and a
config hash over all of it. `measure_report` REFUSES to place two measurements
side by side when any of those differ, naming which - two assets measured by
different instruments are not comparable, and the refusal is the product.

THE INSTRUMENT LAWS TRAVEL IN THE PAYLOAD, not in prose nobody reads:
  - every ratio names its numerator and denominator beside it (`ratios`);
  - instrument WARNING/NOTE lines are surfaced as `warnings`, never swallowed
    (the e08 bias-vs-wall caveat, mesh_stats' not-a-face-readout);
  - NaN is not a number a caller can use: it becomes null and the conversion
    is named in `nan_as_null` (mesh_stats' curv_var on a rect-empty mesh);
  - every metric is labelled: `metrics_label` is "diagnostic" across this
    surface, because promoting a metric to gate-eligible requires asking what
    else moves it, and that is a ruling, not a default (the spec's
    diagnostics-are-not-gates law; E15 Ruling 9b's precedent).

WHAT IT NEVER DOES. It never modifies a mesh, a bake, or a recorded tree. The
wrapped instruments write derived outputs only (JSON, a sheet PNG), and the one
instrument path that writes beside its input - texel_provenance's claim.npy,
written only when --render is passed - is gated: pointing that path at the
recorded trees under FACET_ASSETS refuses with SEALED_TREE, because those trees
are citable-only (Ruling 33's ledger) and detection-by-manifest is their only
compensator. Verdicts do not exist here: no field says good, pass, or ship.
The Director judges; this server measures.

Standards compliance
  PIN_PER_STEP        the instrument file hash and the resolved parameters ride
                      in every payload; the config hash makes "same instrument"
                      checkable rather than assumed.
  ANDON_AUTHORITY     refusal-first: unmet preconditions name the exact missing
                      file; the sealed-tree gate and the comparison-mismatch
                      gate raise, with no skip flag anywhere.
  NAMED_COMPENSATORS  every output is derived and regenerable; the recorded
                      trees are unreachable by construction on the one writing
                      path. Undo = delete the output file.
  DECOMPOSE_BY_SECRETS  measurements live in the instruments, subject values in
                      profiles (subject_profile), the wire shape here. This
                      module adds no threshold and no measurement arithmetic.
  UNCERTAINTY_GATED_HUMANS  no verdict field exists to put a verdict in; ratios
                      ship numerator and denominator so a caller can
                      re-normalise; refusals name whose question blocks them.
  EXTERNAL_VERIFIER   the fixture tests pin exact analytic numbers (a quad
                      ladder that must read 0 then 1024); the instruments are
                      not graded by their own wrapper.
"""
import argparse
import hashlib
import json
import locale
import math
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import facet_index                                     # noqa: E402  the contract

from mcp.server.mcpserver import MCPServer             # noqa: E402
from mcp.server.mcpserver.exceptions import ToolError  # noqa: E402
from mcp.types import ToolAnnotations                  # noqa: E402

REPO = os.path.dirname(HERE)

# This server's own version, NOT the facet-mcp package version: the package
# publishes the record server and its number is pinned across four sites by
# T27. This module is deliberately NOT in the wheel (pyproject py-modules) -
# whether it joins a release is the Director's, and versioning it here keeps
# the identity contract live in the meantime.
# 0.1.0 -> 0.2.0 at E28 task 2b: the surface moved from 4-of-8 serving to
# 7-of-8. The identity law is why this bumps: a payload's envelope carries the
# server version and measure_report refuses cross-version comparison, so two
# surfaces must not share a number. No 0.1.0 payload of the four
# already-serving tools changes behaviour; the bump marks the surface, not
# the instruments.
MEASURE_VERSION = "0.2.0"
SERVER_NAME = "facet-measure"

# The sealed recorded trees. Same resolution as the test harness: the env var
# selects, the rig default stands in. A path under this root may be READ by any
# tool here; the one instrument invocation that would WRITE beside its input
# (texel_provenance --render) refuses instead.
ASSETS_ENV = "FACET_ASSETS"
DEFAULT_ASSETS = "E:\\AI\\training" if os.name == "nt" else "/nonexistent/facet-assets"


def sealed_root():
    return os.path.abspath(os.environ.get(ASSETS_ENV) or DEFAULT_ASSETS)


def under_sealed_root(path):
    root = sealed_root()
    p = os.path.abspath(path)
    try:
        return os.path.commonpath([root, p]) == root
    except ValueError:                     # different drives - not under it
        return False


# ---------------------------------------------------------------------------
# the structured error - the studio ErrorShape, record_mcp's sibling
# ---------------------------------------------------------------------------

CODES = {
    # code                exit  meaning
    "NOT_WRAPPED":        facet_index.EXIT_REFUSED,   # no in-scope instrument
    "PRECONDITION_MISSING": facet_index.EXIT_REFUSED,  # a named input is absent
    "SEALED_TREE":        facet_index.EXIT_REFUSED,   # write path aimed at the
                                                      # recorded trees
    "MEASUREMENT_MISMATCH": facet_index.EXIT_REFUSED,  # incomparable payloads
    "BAD_ARGUMENT":       facet_index.EXIT_USER,      # outside stated bounds
    "INSTRUMENT_FAILED":  facet_index.EXIT_RUNTIME,   # the subprocess broke
    "INTERNAL":           facet_index.EXIT_RUNTIME,   # wrapped, never raw
}


class MeasureError(Exception):
    """A refusal with the studio's shape. Raised, never returned as a flag."""

    def __init__(self, code, message, hint):
        if code not in CODES:
            raise AssertionError("unnamed error code: %s" % code)
        self.code = code
        self.message = message
        self.hint = hint
        self.exit_code = CODES[code]
        Exception.__init__(self, message)

    def shape(self):
        return {"error": True, "code": self.code, "message": self.message,
                "hint": self.hint, "exit_code": self.exit_code}

    def loud(self):
        return (
            "REFUSED: %s\n"
            "  code:      %s\n"
            "  exit_code: %d  (0 ok / 1 user / 2 runtime / 4 refused)\n"
            "  hint:      %s\n"
            "%s"
            % (self.message, self.code, self.exit_code, self.hint,
               json.dumps(self.shape(), ensure_ascii=True, sort_keys=True)))


def _raise(err):
    """Every refusal leaves through here, so the wire shape has one site."""
    raise ToolError(err.loud())


def _need_file(path, what, hint):
    """PRECONDITION_MISSING naming the exact absent input - never a stack."""
    if not os.path.exists(path):
        _raise(MeasureError(
            "PRECONDITION_MISSING",
            "%s is missing: %s" % (what, path), hint))
    return path


# ---------------------------------------------------------------------------
# instrument identity
# ---------------------------------------------------------------------------

def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _canonical(obj):
    return json.dumps(obj, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":"))


def envelope(tool, instrument_rel, params, ratios=None, warnings=None,
             nan_paths=None, notes=None):
    """The identity block every successful payload carries (spec: 'every
    payload carries the server version and a hash of the measurement
    configuration')."""
    inst = None
    if instrument_rel:
        path = os.path.join(REPO, instrument_rel.replace("/", os.sep))
        inst = {"path": instrument_rel, "sha256": _sha256_file(path)}
    doc = {"server": {"name": SERVER_NAME, "version": MEASURE_VERSION},
           "tool": tool, "instrument": inst, "params": params}
    doc["config_hash"] = hashlib.sha256(
        _canonical(doc).encode("ascii")).hexdigest()
    doc["metrics_label"] = "diagnostic"
    doc["metrics_label_rationale"] = (
        "every metric on this surface is diagnostic: promotion to "
        "gate-eligible requires asking what else moves it, which is a ruling "
        "(spec: diagnostics are not gates; E15 Ruling 9b)")
    if ratios:
        doc["ratios"] = ratios
    doc["warnings"] = warnings or []
    if nan_paths:
        doc["nan_as_null"] = nan_paths
    if notes:
        doc["notes"] = notes
    return doc


def _sanitize_nan(obj):
    """NaN/Inf are not numbers a caller can use, and NaN is not valid strict
    JSON. They become null, and the conversion is NAMED (nan_as_null).
    Returns (sanitized, list-of-paths-converted)."""
    found = []

    def walk(o, path):
        if isinstance(o, dict):
            return {k: walk(v, "%s.%s" % (path, k) if path else str(k))
                    for k, v in o.items()}
        if isinstance(o, list):
            return [walk(v, "%s[%d]" % (path, i)) for i, v in enumerate(o)]
        if isinstance(o, float) and not math.isfinite(o):
            found.append(path)
            return None
        return o

    return walk(obj, ""), found


# ---------------------------------------------------------------------------
# running an instrument
# ---------------------------------------------------------------------------

def tool_path(rel):
    return os.path.join(REPO, "tools", rel.replace("/", os.sep))


def run_instrument(rel, args, timeout=3600):
    """One instrument, as a subprocess of THIS interpreter (the pinned one -
    the environment law names exactly one python and T18 refuses the rest).

    Output decoded the way the child wrote it (PYTHONIOENCODING's encoding
    half when set, the locale otherwise, errors=replace) - the harness's own
    rule, so an encoding defect surfaces as text, never as a crash here.
    """
    env_enc = os.environ.get("PYTHONIOENCODING", "").split(":", 1)[0]
    enc = env_enc or locale.getpreferredencoding(False)
    try:
        p = subprocess.run(
            [sys.executable, tool_path(rel)] + [str(a) for a in args],
            cwd=REPO, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        _raise(MeasureError(
            "INSTRUMENT_FAILED",
            "%s exceeded %d s" % (rel, timeout),
            "The subject may be far larger than this instrument expects; "
            "run the tool directly to watch it."))
    out = p.stdout.decode(enc, errors="replace")
    err = p.stderr.decode(enc, errors="replace")
    if p.returncode != 0:
        tail = "\n".join((out + "\n" + err).strip().splitlines()[-8:])
        _raise(MeasureError(
            "INSTRUMENT_FAILED",
            "%s exited %d" % (rel, p.returncode),
            "Its own last lines:\n%s" % tail))
    return out, err


def warning_lines(text):
    """Instrument WARNING/NOTE lines, surfaced verbatim. A caveat that lives
    only in a transcript nobody kept is not a caveat."""
    return [ln.strip() for ln in text.splitlines()
            if "WARNING" in ln or "NOTE:" in ln]


# ---------------------------------------------------------------------------
# the tool surface - spec 2's table, exactly eight
# ---------------------------------------------------------------------------

srv = MCPServer(
    name=SERVER_NAME,
    title="facet mesh/texture measurement",
    version=MEASURE_VERSION,
    instructions=(
        "Identical measurement of any mesh or textured asset - the numeric "
        "half of a comparison. Instruments are this repo's own, wrapped, so "
        "two assets measured months apart went through one code path. Every "
        "payload carries the server version, the instrument's file hash and a "
        "config hash; measure_report refuses to compare across a mismatch. "
        "Nothing here says whether output is GOOD - the Director judges."))


@srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
def mesh_stats(glb: str, profile: str | None = None,
               crop: str | None = None, crop_res: int | None = None,
               bound: float | None = None, grid: int | None = None) -> dict:
    """Measure this mesh identically to every other mesh.

    Wraps tools/verify/mesh_stats.py: components (welded AND unwelded, the
    weld law made visible), watertightness, face-rect curvature, bbox and
    std-frame extents, projected silhouette area. One mesh per call; compare
    two calls with measure_report.

    glb        path to the mesh
    profile    optional subject profile JSON (subject_profile.bind); explicit
               arguments still win over it
    crop, crop_res, bound, grid   optional overrides; the instrument's
               defaults are the character subject's and the payload echoes
               what actually ran
    """
    _need_file(glb, "the mesh", "Pass a path to a .glb this rig can read.")
    args = ["--glb", glb]
    params = {"glb": os.path.abspath(glb)}
    if profile:
        _need_file(profile, "the subject profile",
                   "Pass a profiles/*.json path, or omit for the defaults.")
        args += ["--profile", profile]
        params["profile"] = os.path.abspath(profile)
    for name, val in (("crop", crop), ("crop-res", crop_res),
                      ("bound", bound), ("grid", grid)):
        if val is not None:
            args += ["--%s" % name, str(val)]
            params[name.replace("-", "_")] = val
    out, _ = run_instrument("verify/mesh_stats.py", args)

    lines = out.splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith("{")]
    if not starts:
        _raise(MeasureError(
            "INSTRUMENT_FAILED", "mesh_stats printed no JSON blob",
            "Its output shape changed under this server; run it directly."))
    blob_text = "\n".join(lines[starts[-1]:])
    end = blob_text.rfind("}")
    blob = json.loads(blob_text[:end + 1])
    if len(blob.get("meshes", [])) != 1:
        _raise(MeasureError(
            "INTERNAL",
            "expected one mesh row, parsed %d" % len(blob.get("meshes", [])),
            "This wrapper passes exactly one --glb; the blob disagrees."))
    row, nan_paths = _sanitize_nan(blob["meshes"][0])

    ratios = {
        "largest_component_frac": {
            "numerator": "faces in the largest welded component",
            "denominator": "faces (total welded faces, in this payload)"},
        "rect_frac_of_figure": {
            "numerator": "face-rect area in front-view px^2 (from crop)",
            "denominator": "figure_area_px2 (in this payload)"},
        "face_rect_density": {
            "numerator": "face_rect_faces (in this payload)",
            "denominator": "rect_frac_of_figure (in this payload)"},
    }
    return {"mesh": row, "instrument_params": blob.get("params"),
            "measure": envelope("mesh_stats", "tools/verify/mesh_stats.py",
                                params, ratios=ratios,
                                warnings=warning_lines(out),
                                nan_paths=nan_paths)}


@srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
def mesh_topology(glb: str, slab: float | None = None,
                  face_deg: float | None = None, sections: int | None = None,
                  section_window: float | None = None,
                  wall_gap: float | None = None,
                  label: str | None = None) -> dict:
    """The topology facts mesh_stats does not print.

    Wraps tools/diagnostics/e14_topology.py (the Director ruled the family in,
    2026-08-09; the tie crash was repaired at E28 2a with its proof in T42):
    the boundary-edge triplet (count AND total length AND longest single
    edge - a zero-length boundary edge and a hole's loop are the same integer
    and different facts), non-manifold census, the shell count under BOTH
    definitions named (shared-vertex = mesh_stats' quantity; shared-manifold-
    edge beside it), the nested-wall hollow test, cross-section wall scan, and
    the extremal-slab floor test.

    glb    path to the mesh
    slab, face_deg, sections, section_window, wall_gap
           optional overrides; the instrument derives its windows from THIS
           mesh's own extent and the payload echoes what actually ran
    """
    _need_file(glb, "the mesh", "Pass a path to a .glb this rig can read.")
    args = ["--glb", glb]
    params = {"glb": os.path.abspath(glb)}
    for name, val in (("slab", slab), ("face-deg", face_deg),
                      ("sections", sections),
                      ("section-window", section_window),
                      ("wall-gap", wall_gap), ("label", label)):
        if val is not None:
            args += ["--%s" % name, str(val)]
            params[name.replace("-", "_")] = val
    fd, out_json = tempfile.mkstemp(suffix=".json", prefix="topo_")
    os.close(fd)
    try:
        out, _ = run_instrument("diagnostics/e14_topology.py",
                                args + ["--out", out_json])
        with open(out_json, encoding="utf-8") as fh:
            doc = json.load(fh)
    finally:
        if os.path.exists(out_json):
            os.remove(out_json)

    ratios = {
        "nonmanifold_frac": {
            "numerator": "nonmanifold_edges (in this payload)",
            "denominator": "edges_unique (in this payload)"},
        "largest_shell_frac": {
            "numerator": "faces in the largest shared-vertex shell",
            "denominator": "faces (in this payload)"},
        "nested_wall_test.material_frac_of_outer": {
            "numerator": "outer_volume + inner_volume (signed; inner is "
                         "negative on a nested wall)",
            "denominator": "outer_volume (in this payload)"},
    }
    notes = [
        "shells vs pieces_manifold_adjacency are BOTH in this payload because "
        "the two definitions do not agree on a pinched surface - the "
        "instrument's own operand warning; `shells` is the only one "
        "comparable with the record's family table.",
        "where the non-manifold edges CONCENTRATE is not in this payload: "
        "tools/diagnostics/e12_nonmanifold.py computes the same count "
        "independently and projects every edge midpoint onto the turnaround "
        "renders - a picture, on a render set it requires as input, evidence "
        "for the eye rather than a payload number (E28 Ruling 4: named, not "
        "wrapped)."]
    doc, nan_paths = _sanitize_nan(doc)
    doc["measure"] = envelope("mesh_topology",
                              "tools/diagnostics/e14_topology.py", params,
                              ratios=ratios, warnings=warning_lines(out),
                              nan_paths=nan_paths, notes=notes)
    return doc


@srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
def reach_ceiling(prep: str, sets: str = "2,4,6,8,12",
                  facing_min: float | None = None,
                  head_facing_min: float | None = None,
                  bias: float | None = None, noffs: float | None = None,
                  elev: str | None = None) -> dict:
    """How much of this surface can a given camera set actually paint?

    Wraps tools/diagnostics/e08_ceiling.py: the reachable-texel ceiling over
    camera ladders, computed from geometry alone BEFORE an expensive arm is
    spent, using the projection route's own acceptance construction (facing
    floors, ray bias, normal offset - project_twins' defaults).

    prep   a bake-prep directory: meta.json (with crop + crop_res), mask.npy,
           pos.npy, nor.npy, prep_uv.glb
    sets   comma-separated camera counts, e.g. "2,4,6,8,12"
    elev   extra elevated cameras, "yaw:el,yaw:el"
    """
    _need_file(prep, "the prep directory",
               "Pass the bake-prep directory the route produced.")
    for member in ("meta.json", "mask.npy", "pos.npy", "nor.npy",
                   "prep_uv.glb"):
        _need_file(os.path.join(prep, member),
                   "prep member %s" % member,
                   "reach_ceiling reads the full bake-prep; this file is "
                   "part of its contract.")
    with open(os.path.join(prep, "meta.json"), encoding="utf-8") as fh:
        meta = json.load(fh)
    missing = [k for k in ("res", "lo", "hi", "maxabs", "crop", "crop_res")
               if k not in meta]
    if missing:
        _raise(MeasureError(
            "PRECONDITION_MISSING",
            "meta.json lacks %s" % ", ".join(missing),
            "The ceiling needs the head-band crop keys; a prep written "
            "before they existed cannot answer the head/body split."))

    params = {"prep": os.path.abspath(prep), "sets": sets}
    args = ["--prep", prep, "--sets", sets]
    for name, val in (("facing-min", facing_min),
                      ("head-facing-min", head_facing_min),
                      ("bias", bias), ("noffs", noffs)):
        if val is not None:
            args += ["--%s" % name, str(val)]
            params[name.replace("-", "_")] = val
    if elev:
        args += ["--elev", elev]
        params["elev"] = elev
    fd, out_json = tempfile.mkstemp(suffix=".json", prefix="ceiling_")
    os.close(fd)
    try:
        out, _ = run_instrument("diagnostics/e08_ceiling.py",
                                args + ["--out-json", out_json])
        with open(out_json, encoding="utf-8") as fh:
            doc = json.load(fh)
    finally:
        if os.path.exists(out_json):
            os.remove(out_json)

    ratios = {"settings.*.N*.pct": {
        "numerator": "reachable (in the same row)",
        "denominator": "valid_texels (top level of this payload)"}}
    doc, nan_paths = _sanitize_nan(doc)
    doc["measure"] = envelope("reach_ceiling",
                              "tools/diagnostics/e08_ceiling.py", params,
                              ratios=ratios, warnings=warning_lines(out),
                              nan_paths=nan_paths)
    return doc


@srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
def thin_extent_curve(glb: str, aspect: str | None = None,
                      margin: float | None = None,
                      fit_axis: str | None = None, views: str | None = None,
                      el: float | None = None, values: str | None = None,
                      region_a: str | None = None, region_b: str | None = None,
                      region_name: str | None = None,
                      z_tol: float | None = None) -> dict:
    """What does this thin-structure threshold cost on THIS mesh?

    Wraps tools/diagnostics/e12_thin_curve.py (the Director ruled the family
    in, 2026-08-09): the per-view screen-space front-to-back extent curve,
    computed by emit's own construction - same canonicalisation, same D, same
    fit-axis block - so a value read off the curve means the same thing when
    texpass_iter receives it. 0.0 is a curve point, not an absent one: the
    tool default runs the guard DISABLED, and the curve shows what undecided
    actually does.

    glb        path to the mesh
    views      comma-separated yaws (instrument default: the 8-view ring)
    values     comma-separated thin_extent candidates, canonical units
    region_a, region_b   optional spatial region as VIEW:x0,y0,x1,y1 pixel
               rects on two ORTHOGONAL views; the region fraction rides
               beside the figure fraction, and its known impurity (thick
               struts inside the box) can only push it DOWN
    The instrument's --preview flag is deliberately not exposed: previews are
    artifacts for the eye, not payload numbers - run the tool directly for
    them.
    """
    _need_file(glb, "the mesh", "Pass a path to a .glb this rig can read.")
    if (region_a is None) != (region_b is None):
        _raise(MeasureError(
            "BAD_ARGUMENT", "region_a and region_b come as a pair",
            "The region is read off TWO orthogonal views or not at all - "
            "one rect cannot place a box in three dimensions."))
    args = ["--glb", glb]
    params = {"glb": os.path.abspath(glb)}
    for name, val in (("aspect", aspect), ("margin", margin),
                      ("fit-axis", fit_axis), ("views", views), ("el", el),
                      ("values", values), ("region-a", region_a),
                      ("region-b", region_b), ("region-name", region_name),
                      ("z-tol", z_tol)):
        if val is not None:
            args += ["--%s" % name, str(val)]
            params[name.replace("-", "_")] = val
    fd, out_json = tempfile.mkstemp(suffix=".json", prefix="thin_")
    os.close(fd)
    try:
        out, _ = run_instrument("diagnostics/e12_thin_curve.py",
                                args + ["--out", out_json])
        with open(out_json, encoding="utf-8") as fh:
            doc = json.load(fh)
    finally:
        if os.path.exists(out_json):
            os.remove(out_json)

    ratios = {
        "curve.*.figure_pct": {
            "numerator": "pixels with ext < value, all views pooled",
            "denominator": "total_hit_px (in this payload)"},
        "curve.*.region_pct": {
            "numerator": "region pixels with ext < value, all views pooled",
            "denominator": "total_region_px (in this payload)"},
        "curve.*.ratio_region_over_figure": {
            "numerator": "region_pct (in the same row)",
            "denominator": "figure_pct (in the same row)"},
    }
    notes = [
        "the curve is a CURVE, not a threshold: the server returns costs so a "
        "human decides, and will return this curve where it is asked for a "
        "threshold (the spec's no-subject-values law)."]
    doc, nan_paths = _sanitize_nan(doc)
    doc["measure"] = envelope("thin_extent_curve",
                              "tools/diagnostics/e12_thin_curve.py", params,
                              ratios=ratios, warnings=warning_lines(out),
                              nan_paths=nan_paths, notes=notes)
    return doc


@srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
def offsurface_rate(prep: str, aspect: str | None = None,
                    margin: float | None = None, fit_axis: str | None = None,
                    v_ext: float | None = None, sample: int | None = None,
                    seed: int | None = None, label: str | None = None) -> dict:
    """Does this bake's position map lie on the mesh? - the BAKE half.

    Wraps tools/diagnostics/e12_offsurface.py (the Director ruled the family
    in, 2026-08-09): world position per uv-valid texel reconstructed from
    meta.json, distance to the surface from the raycasting scene, a fixed-seed
    sample, and the emit-pixel unit DERIVED from the subject's own framing
    with the derivation echoed in the payload. The instrument was validated
    against the ship's ruled number before first use (E12 task 2: 2.5065%
    via this instrument against E10 Ruling 4's 2.5%).

    prep     a bake-prep directory: meta.json, mask.npy, pos.npy, prep_uv.glb
    v_ext    override the derived emit-camera vertical extent - getting the
             unit wrong scales every threshold, which is why the payload
             carries v_ext_derivation
    seed, sample   the fixed-seed sample; defaults reproduce the recorded
             invocations
    """
    _need_file(prep, "the prep directory",
               "Pass the bake-prep directory the route produced.")
    for member in ("meta.json", "mask.npy", "pos.npy", "prep_uv.glb"):
        _need_file(os.path.join(prep, member),
                   "prep member %s" % member,
                   "offsurface_rate reads the bake-prep's position map "
                   "against its mesh; this file is part of that contract.")
    args = ["--prep", prep]
    params = {"prep": os.path.abspath(prep)}
    for name, val in (("aspect", aspect), ("margin", margin),
                      ("fit-axis", fit_axis), ("v-ext", v_ext),
                      ("sample", sample), ("seed", seed), ("label", label)):
        if val is not None:
            args += ["--%s" % name, str(val)]
            params[name.replace("-", "_")] = val
    fd, out_json = tempfile.mkstemp(suffix=".json", prefix="offsurf_")
    os.close(fd)
    try:
        out, _ = run_instrument("diagnostics/e12_offsurface.py",
                                args + ["--out", out_json])
        with open(out_json, encoding="utf-8") as fh:
            doc = json.load(fh)
    finally:
        if os.path.exists(out_json):
            os.remove(out_json)

    ratios = {
        "pct_off_surface_gt_1px": {
            "numerator": "sampled texels whose reconstructed position sits "
                         "more than one emit pixel off the surface",
            "denominator": "sampled (in this payload)"},
        "pct_off_surface_gt_5px": {
            "numerator": "sampled texels more than five emit pixels off",
            "denominator": "sampled (in this payload)"},
    }
    notes = [
        "the ERODE / MARGIN-STATISTIC half the spec asks for is NOT in this "
        "payload: it exists in neither offsurface instrument (measured at "
        "the E27 ruling seat - --margin on this instrument is the CAMERA "
        "FRAMING margin, a different quantity). Commissioned in principle at "
        "E27, unscoped; this wrapper does not compute it.",
        "tools/diagnostics/e10_offsurface.py remains the ship-bound sibling "
        "whose ruled numbers this instrument reproduces (E12 task 2); its "
        "stroke-comparison half needs an emitted stroke directory and is a "
        "different question."]
    doc, nan_paths = _sanitize_nan(doc)
    doc["measure"] = envelope("offsurface_rate",
                              "tools/diagnostics/e12_offsurface.py", params,
                              ratios=ratios, warnings=warning_lines(out),
                              nan_paths=nan_paths, notes=notes)
    return doc


@srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
def texel_provenance(prep: str, state: str, stage1: str, order: str,
                     facing_min: float | None = None,
                     edge_dist: float | None = None,
                     render: str | None = None,
                     regions: str | None = None,
                     out_json: str | None = None) -> dict:
    """Where did this pixel's colour come from - projected, synthesised, or
    dilated?

    Wraps tools/diagnostics/texel_provenance.py: replays the commit chain
    offline from the saved job directories and reports the census - TWINS
    (stage 1 projection), BRUSH stroke n (synthesis), DILATION (never
    painted; atlas adjacency is not surface adjacency, so this is the defect
    class).

    prep     the bake-prep directory
    state    the brush state directory holding job_<key>/ subdirectories
    stage1   the stage-1 atlas; _holes.png and _styled_mask.npy sit beside it
    order    comma-separated job keys in stroke order
    render   OPTIONAL head render to sample through. THIS PATH WRITES
             claim.npy INTO state/ (the instrument's own contract), so it
             refuses when state is under the sealed recorded trees.
    """
    _need_file(prep, "the prep directory", "Pass the route's bake-prep.")
    _need_file(state, "the state directory", "Pass the brush state root.")
    base = os.path.splitext(stage1)[0]
    _need_file(base + "_holes.png", "the stage-1 hole map",
               "texel_provenance replays from stage-1's holes; the file "
               "sits beside the stage-1 atlas.")
    _need_file(base + "_styled_mask.npy", "the stage-1 styled mask",
               "The census's TWINS class is this mask; it sits beside the "
               "stage-1 atlas.")
    keys = [k.strip() for k in order.split(",") if k.strip()]
    if not keys:
        _raise(MeasureError("BAD_ARGUMENT", "order names no job keys",
                            "Pass the stroke order, e.g. "
                            "'y+045_e+00,y+315_e+00'."))
    for k in keys:
        jdir = os.path.join(state, "job_" + k)
        for member in ("cam.json", "inpainted.png", "mask.png"):
            _need_file(os.path.join(jdir, member),
                       "job %s member %s" % (k, member),
                       "Every job in --order must carry its camera, its "
                       "inpainted frame and its job mask.")
    if render is not None and under_sealed_root(state):
        _raise(MeasureError(
            "SEALED_TREE",
            "the --render path writes claim.npy into %s, which is under the "
            "sealed recorded trees (%s)" % (os.path.abspath(state),
                                            sealed_root()),
            "The recorded trees are citable-only with no revert; copy the "
            "state to scratch (the harness's copy_state pattern) and point "
            "this tool at the copy."))

    params = {"prep": os.path.abspath(prep),
              "state": os.path.abspath(state), "order": order}
    args = ["--prep", prep, "--state", state, "--stage1", stage1,
            "--order", order]
    for name, val in (("facing-min", facing_min), ("edge-dist", edge_dist)):
        if val is not None:
            args += ["--%s" % name, str(val)]
            params[name.replace("-", "_")] = val
    if render:
        _need_file(render, "the head render", "Pass the render to sample.")
        args += ["--render", render]
        params["render"] = os.path.abspath(render)
    if regions:
        args += ["--regions", regions]
        params["regions"] = regions
    if out_json:
        args += ["--out-json", out_json]
        params["out_json"] = os.path.abspath(out_json)
    out, _ = run_instrument("diagnostics/texel_provenance.py", args)

    # the census, parsed against pinned print sites (tests run a REAL replay
    # and assert every pattern below was found, the record_mcp precedent)
    census = {"strokes": []}
    total = None
    for ln in out.splitlines():
        m = re.match(r"\[prov\] whole atlas, valid texels ([\d,]+)", ln)
        if m:
            total = int(m.group(1).replace(",", ""))
        m = re.match(r"\[prov\]\s+TWINS \(stage 1\)\s+([\d,]+)\s+"
                     r"([\d.]+)%", ln)
        if m:
            census["twins"] = int(m.group(1).replace(",", ""))
        m = re.match(r"\[prov\]\s+BRUSH stroke (\d+) \((.+?)\)\s+([\d,]+)\s+"
                     r"([\d.]+)%", ln)
        if m:
            census["strokes"].append(
                {"stroke": int(m.group(1)), "key": m.group(2),
                 "texels": int(m.group(3).replace(",", ""))})
        m = re.match(r"\[prov\]\s+DILATION \(never painted\)\s+([\d,]+)\s+"
                     r"([\d.]+)%", ln)
        if m:
            census["dilation"] = int(m.group(1).replace(",", ""))
    if total is None or "twins" not in census or "dilation" not in census:
        _raise(MeasureError(
            "INSTRUMENT_FAILED",
            "texel_provenance's census lines did not parse",
            "Its print shape changed under this server; run it directly and "
            "update the pinned patterns WITH their tests."))
    census["valid_texels"] = total

    ratios = {"census.*": {
        "numerator": "the class's texel count",
        "denominator": "valid_texels (in this payload)"}}
    notes = [
        "largest-connected-component per class is NOT measured: the wrapped "
        "instrument reports totals only. The record's own law wants the "
        "total AND the largest component for blob-shaped defect classes "
        "(DILATION especially); adding it is a measurement, so it is an E27 "
        "finding for the ruling seat, not something this wrapper computes."]
    if render:
        notes.append("claim.npy was written into %s (the instrument's own "
                     "contract on the --render path)" % os.path.abspath(state))
    return {"census": census,
            "measure": envelope("texel_provenance",
                                "tools/diagnostics/texel_provenance.py",
                                params, ratios=ratios,
                                warnings=warning_lines(out), notes=notes)}


@srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
def anchor_check(subject: str | None = None) -> dict:
    """Does this recorded output still reproduce? - NOT SERVABLE YET.

    Refuses (a gate-3 finding): no instrument exists under tools/.
    """
    _raise(MeasureError(
        "NOT_WRAPPED",
        "anchor_check has no instrument: nothing under tools/ implements the "
        "anchored-regression pattern as a tool. "
        "tools/diagnostics/e13_anchor_check.py is a NAME COLLISION - it is "
        "the spiral-law painted-adjacency guard that runs before a brush "
        "stroke, not a regeneration check",
        "The pattern itself lives in the harness's artifacts tier (T07-T11 "
        "replay recorded runs and re-hash their inputs) and in session "
        "procedure (the E04 hardware anchor, dE 0.84 against the 1.07 "
        "floor). Building it as a tool is a commission for the ruling seat; "
        "E27's report carries the finding."))


@srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
def measure_report(left: dict | None = None, right: dict | None = None,
                   sheet: dict | None = None) -> dict:
    """Put the numbers on one sheet beside the reference.

    Two halves, either or both:

    left, right   two payloads previously returned by THIS server's tools.
                  Placed side by side with per-key deltas - REFUSING when
                  their identity blocks differ (tool, server version,
                  instrument hash, config hash), naming which. Two assets
                  measured by different instruments are not comparable; the
                  refusal is the product.
    sheet         compose the reference | asset | provenance | error sheet
                  via tools/verify/gate1_sheet.py. Keys: twins, asset, prov,
                  masks (directories), views (comma string), out (the PNG
                  path); optional out_json, owner, mask_tag, ref_pattern,
                  asset_pattern, prov_pattern, owner_pattern, no_error,
                  crop, scale.
    """
    if left is None and right is None and sheet is None:
        _raise(MeasureError(
            "BAD_ARGUMENT", "nothing to do",
            "Pass left+right payloads to compare, a sheet spec, or both."))
    if (left is None) != (right is None):
        _raise(MeasureError(
            "BAD_ARGUMENT", "comparison needs BOTH left and right",
            "Pass the two payloads exactly as this server returned them."))

    out = {}
    if left is not None:
        for name, doc in (("left", left), ("right", right)):
            if not (isinstance(doc, dict) and isinstance(doc.get("measure"),
                                                         dict)):
                _raise(MeasureError(
                    "BAD_ARGUMENT",
                    "%s carries no measure envelope" % name,
                    "Only payloads returned by this server's tools are "
                    "comparable; the envelope IS the identity."))
        lm, rm = left["measure"], right["measure"]
        mismatched = []
        for field, lv, rv in (
                ("tool", lm.get("tool"), rm.get("tool")),
                ("server.version", (lm.get("server") or {}).get("version"),
                 (rm.get("server") or {}).get("version")),
                ("instrument.sha256",
                 (lm.get("instrument") or {}).get("sha256"),
                 (rm.get("instrument") or {}).get("sha256")),
                ("config_hash", lm.get("config_hash"), rm.get("config_hash"))):
            if lv != rv:
                mismatched.append("%s (%r vs %r)" % (field, lv, rv))
        # config_hash covers params - including the subject path, which a
        # before/after pair legitimately shares; two DIFFERENT subjects also
        # differ here, and that is correct: the comparison this tool exists
        # for is same-subject-before-and-after, the polish arc's own shape.
        if mismatched:
            _raise(MeasureError(
                "MEASUREMENT_MISMATCH",
                "the two payloads are not comparable: %s"
                % "; ".join(mismatched),
                "Re-measure both sides with the same tool, same server, same "
                "instrument, same parameters. Two assets measured by "
                "different versions of this server are not comparable - the "
                "spec's identity law."))

        def leaves(d, prefix=""):
            for k, v in d.items():
                if k == "measure":
                    continue
                p = "%s.%s" % (prefix, k) if prefix else str(k)
                if isinstance(v, dict):
                    yield from leaves(v, p)
                elif isinstance(v, (int, float)) and not isinstance(v, bool):
                    yield p, v

        lvals = dict(leaves(left))
        rvals = dict(leaves(right))
        rows = {}
        for key in sorted(set(lvals) | set(rvals)):
            lv, rv = lvals.get(key), rvals.get(key)
            row = {"left": lv, "right": rv}
            if lv is not None and rv is not None:
                row["delta"] = rv - lv
            rows[key] = row
        out["comparison"] = {
            "tool": lm.get("tool"), "config_hash": lm.get("config_hash"),
            "rows": rows}

    sheet_env = None
    if sheet is not None:
        for k in ("twins", "asset", "prov", "out"):
            if k not in sheet:
                _raise(MeasureError(
                    "BAD_ARGUMENT", "sheet spec lacks %r" % k,
                    "The sheet needs twins/asset/prov directories and an "
                    "out path; masks too unless no_error."))
        no_error = bool(sheet.get("no_error"))
        if not no_error and "masks" not in sheet:
            _raise(MeasureError(
                "BAD_ARGUMENT", "sheet spec lacks 'masks'",
                "The error column's denominator is the exact silhouette; "
                "pass masks, or no_error=true to drop the column AND its "
                "statistics."))
        for k in ("twins", "asset", "prov") + (() if no_error else ("masks",)):
            _need_file(sheet[k], "sheet directory %r" % k,
                       "Every panel directory must exist.")
        args = ["--twins", sheet["twins"], "--asset", sheet["asset"],
                "--prov", sheet["prov"], "--out", sheet["out"],
                "--views", str(sheet.get("views", "4,5,6"))]
        params = {k: sheet[k] for k in ("twins", "asset", "prov", "out")}
        params["views"] = str(sheet.get("views", "4,5,6"))
        if not no_error:
            args += ["--masks", sheet["masks"]]
            params["masks"] = sheet["masks"]
        scratch_json = None
        out_json = sheet.get("out_json")
        if not out_json:
            fd, scratch_json = tempfile.mkstemp(suffix=".json",
                                                prefix="sheet_")
            os.close(fd)
            out_json = scratch_json
        args += ["--out-json", out_json]
        for name in ("owner", "mask_tag", "ref_pattern", "asset_pattern",
                     "prov_pattern", "owner_pattern", "crop"):
            if sheet.get(name) is not None:
                args += ["--%s" % name.replace("_", "-"), str(sheet[name])]
                params[name] = sheet[name]
        if no_error:
            args += ["--no-error"]
            params["no_error"] = True
        if sheet.get("scale") is not None:
            args += ["--scale", str(sheet["scale"])]
            params["scale"] = sheet["scale"]
        try:
            text, _ = run_instrument("verify/gate1_sheet.py", args)
            stats = {}
            if os.path.exists(out_json):
                with open(out_json, encoding="utf-8") as fh:
                    stats = json.load(fh)
        finally:
            if scratch_json and os.path.exists(scratch_json):
                os.remove(scratch_json)
        out["sheet"] = {"path": os.path.abspath(sheet["out"]),
                        "stats": stats,
                        "transcript": [ln for ln in text.splitlines()
                                       if ln.startswith("[sheet]")]}
        sheet_env = envelope(
            "measure_report", "tools/verify/gate1_sheet.py", params,
            ratios={"sheet.stats.*.dE_*": {
                "numerator": "dE over silhouette pixels",
                "denominator": "figure_px (per view, in this payload) - "
                               "the exact silhouette, never a keyed mask"},
                "sheet.stats.*.pct_over_*": {
                "numerator": "silhouette pixels over the dE threshold",
                "denominator": "figure_px (per view, in this payload)"}},
            warnings=warning_lines(text))

    out["measure"] = sheet_env or envelope(
        "measure_report", None,
        {"comparison_only": True}, notes=[
            "no instrument ran: the comparison half is this server's own "
            "envelope contract, not a measurement"])
    return out


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

TOOL_ORDER = ("mesh_stats", "mesh_topology", "reach_ceiling",
              "thin_extent_curve", "offsurface_rate", "texel_provenance",
              "anchor_check", "measure_report")

WRAPPED = {
    "mesh_stats": "tools/verify/mesh_stats.py",
    "mesh_topology": "tools/diagnostics/e14_topology.py",
    "reach_ceiling": "tools/diagnostics/e08_ceiling.py",
    "thin_extent_curve": "tools/diagnostics/e12_thin_curve.py",
    "offsurface_rate": "tools/diagnostics/e12_offsurface.py",
    "texel_provenance": "tools/diagnostics/texel_provenance.py",
    "anchor_check": None,
    "measure_report": "tools/verify/gate1_sheet.py",
}


def _print_tools():
    """The surface, printable without a client. ASCII on every print path."""
    print("facet measurement MCP - %d tools "
          "(spec docs/specs/measurement-mcp-spec.md)" % len(TOOL_ORDER))
    print("server: %s %s" % (SERVER_NAME, MEASURE_VERSION))
    print("sealed recorded trees: %s ($%s)" % (sealed_root(), ASSETS_ENV))
    for name in TOOL_ORDER:
        fn = globals()[name]
        head = (fn.__doc__ or "").strip().splitlines()[0]
        wrapped = WRAPPED[name] or "REFUSES - no in-scope instrument"
        print("  %-18s %s" % (name, head))
        print("  %-18s   wraps: %s" % ("", wrapped))
    return facet_index.EXIT_OK


def main(argv=None):
    """Console entry under the shared exit-code contract (0/1/2/4)."""
    return facet_index.run_contract(_main, argv)


def _main(argv=None):
    ap = facet_index.ContractParser(
        description="the mesh/texture measurement MCP server over facet's "
                    "instruments")
    ap.add_argument("--print-tools", action="store_true",
                    help="print the tool surface and exit; no server, no "
                         "client")
    ap.add_argument("--debug", action="store_true", help=facet_index.DEBUG_HELP)
    args = ap.parse_args(argv)
    if args.print_tools:
        return _print_tools()
    srv.run("stdio")
    return facet_index.EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
